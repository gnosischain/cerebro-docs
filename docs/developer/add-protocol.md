# Adding a New Protocol

A step-by-step blueprint for onboarding a new EVM protocol (lending market, DEX, yield vault, bridge) that emits decodable events on Gnosis Chain into `dbt-cerebro` and surfacing it in `metrics-dashboard`.

This is the how-to the next agent or engineer should be able to run top-to-bottom without re-discovering tooling. It was distilled from the SparkLend + Savings xDAI rollout — every command, path, and pitfall below was actually hit during that work.

## When to use this guide

- Adding a lending, DEX, or yield protocol that speaks through well-known contract addresses on Gnosis Chain.
- You have the contract addresses and (ideally) an ABI source (Gnosisscan, GitHub registry).
- You want events decoded, intermediate/mart models wired up, and cards shown in the dashboard.

Out of scope: non-EVM crawlers (beacon chain), off-chain event streams (Mixpanel/GA4) — those have their own runbooks under `developer/add-scraper.md`.

## Prerequisites

- `docker compose up -d dbt` running in the `dbt-cerebro` repo. Sanity check: `docker exec dbt dbt --version`.
- Access to the `cerebro-dev` MCP server (for live ClickHouse sanity queries during build).
- Contract registry / source-of-truth URL for the protocol (e.g. Spark's `sparkdotfi/spark-address-registry/src/Gnosis.sol`).

## Step 1 — Whitelist metadata seeds

Start with the seed files, not the models. Downstream intermediates `ref()` these.

1. **Reserve / pool mapping.** Add rows to a protocol-specific seed (see [`seeds/lending_market_mapping.csv`](https://github.com/gnosischain/dbt-cerebro/blob/main/seeds/lending_market_mapping.csv) for the pattern — columns `protocol, reserve, aToken, variableDebtToken, …`). If the protocol follows the same shape as an existing one, **widen the existing seed with a new `protocol` column**; don't fork.
2. **Token metadata.** Append aTokens / LP-tokens / vault tokens to [`seeds/tokens_whitelist.csv`](https://github.com/gnosischain/dbt-cerebro/blob/main/seeds/tokens_whitelist.csv). If they're wrapped yield-bearing variants (aTokens), also list them in `symbol_exclude` so they don't double-count in general token-balance marts while still flowing metadata through.
3. **Wire seed config** in `dbt_project.yml` under `seeds: gnosis_dbt:` with `+engine`, `+order_by`, and column types (copy shape from an existing seed).
4. **Load:**

   ```bash
   docker exec dbt dbt seed --select <seed_name>
   ```

## Step 2 — Fetch ABIs + regenerate signatures

The decoder joins `execution.logs` to `event_signatures` on `(contract_address, topic0)`. Missing ABIs = silent empty rows.

Per contract:

```bash
docker exec dbt python3 scripts/signatures/fetch_abi_to_csv.py 0xADDRESS
```

After all addresses are fetched, regenerate signatures and reload seeds:

```bash
docker exec dbt dbt seed --select contracts_abi
docker exec dbt python3 scripts/signatures/signature_generator.py
docker exec dbt dbt seed --select event_signatures function_signatures
```

Single-shot chain (runs the above end-to-end for one address):

```bash
docker exec dbt python3 scripts/signatures/fetch_abi_to_csv.py 0xADDRESS --regen
```

**Egress-less fallback** (use if Gnosisscan is blocked from the dbt container):

```bash
docker exec dbt dbt run-operation fetch_and_insert_abi --args '{address: "0xADDRESS"}'
docker exec dbt python3 scripts/signatures/fetch_abi_to_csv.py 0xADDRESS --from-ch
```

**Verification** (via `mcp__cerebro-dev__execute_query`):

```sql
SELECT contract_address, count() AS signatures
FROM dbt.event_signatures
WHERE lower(contract_address) IN ('0xaddress1', '0xaddress2')
GROUP BY contract_address
```

If any address is missing, the decoder will emit rows with empty `event_name` and empty `decoded_params`. Go back and fix Step 2 before continuing.

## Step 3 — Create raw decoder models

Path: `models/contracts/<protocol>/contracts_<protocol>_<Contract>_events.sql`.

Copy the config block and `decode_logs(...)` macro call from [`models/contracts/aave/contracts_aaveV3_PoolInstance_events.sql`](https://github.com/gnosischain/dbt-cerebro/blob/main/models/contracts/aave/contracts_aaveV3_PoolInstance_events.sql). One decoder per address group:

- Pool (single address).
- AToken / LP list (array of addresses → macro takes a list).
- Configurator (single address).

Add schema entries to `models/contracts/<protocol>/schema.yml` with `meta.full_refresh.start_date` and `batch_months`.

## Step 4 — Run decoders via `refresh.py`

**Do not** `dbt run --full-refresh` heavy decoders directly — it rebuilds the entire range in one go and usually OOMs. Use the full-refresh orchestrator which reads `meta.full_refresh` from `schema.yml`:

```bash
# Dry run first
docker exec dbt python3 scripts/full_refresh/refresh.py \
  --select contracts_<protocol>_Pool_events contracts_<protocol>_AToken_events \
  --dry-run

# Then without --dry-run
docker exec dbt python3 scripts/full_refresh/refresh.py \
  --select contracts_<protocol>_Pool_events contracts_<protocol>_AToken_events

# If anything fails, resume from saved state
docker exec dbt python3 scripts/full_refresh/refresh.py --resume
```

State persists in `.refresh_state.json`. Long runs can be backgrounded — come back when you're notified.

**Sanity check** via MCP:

```sql
SELECT event_name, count() AS n
FROM dbt.contracts_<protocol>_Pool_events
GROUP BY event_name
ORDER BY n DESC
```

Empty `event_name` with non-zero counts ⇒ missing signatures (Step 2 regression).

## Step 5 — Build intermediate + mart models

Patterns for protocol-aware widening:

```sql
pool_events_raw AS (
    SELECT 'Aave V3'   AS protocol, * FROM {{ ref('contracts_aaveV3_PoolInstance_events') }}
    UNION ALL
    SELECT 'SparkLend' AS protocol, * FROM {{ ref('contracts_spark_Pool_events') }}
)
```

Then join the mapping seed on `(protocol, address)`. **Always include `protocol` in `unique_key`, window `PARTITION BY`, and `order_by`**, otherwise cumulative sums will cross-contaminate between protocols.

Reuse the shared macros:

- `apply_monthly_incremental_filter('block_timestamp', 'date', 'true')` — monthly incremental slicing.
- `symbol_filter(...)` — centralise token allow/exclude logic.

### ASOF JOIN for event pairing

For any model that pairs a user-action event to a preceding state snapshot (`ReserveDataUpdated`, oracle update, price poke), **do not** use `row_number()`-based rank pairing. Forks that emit extra state snapshots on FlashLoans (e.g. SparkLend: 54 223 FlashLoan RDUs on WETH alone vs ~5k user actions) will silently mis-align ranks. Use `ASOF INNER JOIN` on `log_index`:

```sql
FROM supply_events s
ASOF INNER JOIN reserve_index_by_tx r
    ON  r.protocol         = s.protocol
    AND r.transaction_hash = s.transaction_hash
    AND r.token_address    = s.token_address
    AND r.log_index        <  s.log_index
WHERE r.liquidity_index > toUInt256OrZero('0')
```

The `r.log_index < s.log_index` predicate selects the snapshot with the largest `log_index` strictly preceding the user action — robust regardless of how many extra snapshots interleave.

### Cumulative sums with `UNION ALL + GROUP BY`, not `FULL OUTER JOIN`

When computing per-day supply and borrow deltas together, a `FULL OUTER JOIN` on `(protocol, date, token)` can silently drop the `protocol` dimension in ClickHouse on days where only one side has rows. Prefer:

```sql
deltas AS (
    SELECT protocol, date, token_address,
           sum(scaled_delta) AS delta_supply, toInt256(0) AS delta_borrow
    FROM supply_scaled GROUP BY protocol, date, token_address
    UNION ALL
    SELECT protocol, date, token_address,
           toInt256(0) AS delta_supply, sum(scaled_delta) AS delta_borrow
    FROM borrow_scaled GROUP BY protocol, date, token_address
),
deltas_daily AS (
    SELECT protocol, date, token_address,
           sum(delta_supply) AS delta_supply,
           sum(delta_borrow) AS delta_borrow
    FROM deltas GROUP BY protocol, date, token_address
)
```

## Step 6 — Seed full-refresh metadata

Every heavy incremental model needs `meta.full_refresh` in its `schema.yml` so `refresh.py` can batch it. Two canonical patterns:

**Pattern 1 — time-batched (most models):**

```yaml
meta:
  full_refresh:
    mode: monthly
    start_date: '2023-09-05'
    batch_months: 3
```

**Pattern 2 — staged by symbol (token-balance-class models):** a list of stages each rebuilding a subset of symbols in sequence. Copy from an existing balance-daily model.

## Step 7 — Expose in metrics-dashboard

1. Regenerate query JSONs: `cd metrics-dashboard && node scripts/export-queries.js`.
2. Purge affected `/tmp/cache/` entries.
3. `vercel dev --listen 3001` and visit the tab.

For protocol-aware widgets, set `applySecondaryGlobalFilter: true` on the metric and use `filterField3 / filterValue3` (the third AND-filter in `api/metrics.js`) to narrow by protocol.

## Pitfalls & Gotchas (the juicy part)

The list below is the most valuable section — these are failures the SparkLend + Savings xDAI rollout actually hit.

### Data-pipeline

- **Missing ABI is silent.** Decoder produces rows with empty `event_name` and empty `decoded_params`. Always verify signature coverage right after Step 2.
- **ClickHouse address storage.** `execution.logs.address` is stored lowercase, no `0x` prefix. Always `lower(replaceAll(address, '0x', ''))` in JOINs against raw logs.
- **`decode_logs` single-vs-list.** Single-address call does `address = 'X'` (exact, case-sensitive on lowercase stored form). List call does `lower(replaceAll(address,'0x','')) IN (…)` (case-insensitive). Both work — just be aware.
- **Fork-of-Aave FlashLoan density.** SparkLend emits `ReserveDataUpdated` on *every* FlashLoan. WETH alone has 54 223 FlashLoan RDUs. Rank-based pairing silently picks the wrong RDU — use ASOF.
- **`FULL OUTER JOIN` drops dimensions.** For `(protocol, date, token)` cumulative sums, prefer UNION ALL + GROUP BY.
- **ERC-4626 vaults with discrete payouts** (Savings xDAI, sUSDS, any similar protocol-paid vault): share_price step-jumps on `payInterest()`. A day-over-day ratio produces nonsense — use a rolling-window geometric slope. See [Savings xDAI docs](../protocols/savings/index.md#rate-computation).
- **`nthValue` does not exist in ClickHouse** as a window aggregate. Use `first_value(x) OVER (ORDER BY date ROWS BETWEEN N PRECEDING AND N PRECEDING)`.
- **`symbol_exclude` semantics.** aTokens and wrapped yield-bearing variants live in `tokens_whitelist.csv` (so their metadata flows) *and* in `symbol_exclude` (so they don't double-count in general token-balance marts). Treat new protocol wrapper-tokens the same way.
- **Never clamp outliers** (`WHERE value > 0`, `WHERE borrow < supply`, `WHERE rate < 1`). They hide model bugs. Find the root cause.
- **`dbt --full-refresh` on incremental models** rebuilds from scratch in one job — OOMs on anything of interesting size. Always drive full refreshes through `scripts/full_refresh/refresh.py`, which respects `meta.full_refresh` batching.

### MCP (cerebro-dev) gotchas

- **Forbidden queries.** `SYSTEM …`, `SHOW TABLES`, reads from `system.tables` are all blocked. Use `mcp__cerebro-dev__list_tables` or query data directly.
- **Stale `describe_table`.** After rebuilding a view, `describe_table` may cache the old schema. Re-run the model via dbt, then query the view directly (e.g. `SELECT * … LIMIT 0`) to confirm columns.
- **Address filters must be lowercased.** Matches on `execution.logs.address` should always `lower(...)` both sides.

### Dashboard / API

- **`URLSearchParams` encodes space as `+`.** If a filter value contains a space (e.g. protocol `Aave V3`) and isn't matching on the server, verify `api/metrics.js` normalises `+` → ` ` on the `filterValue*` params. Canonical fix:

  ```js
  const normalizeValue = (v) => (typeof v === 'string' ? v.replace(/\+/g, ' ') : null);
  ```

- **Flicker from cascading dropdowns.** If secondary dropdown re-loads after primary selection flickers, check `secondaryCascadesOnPrimary` on the tab config — set to `false` for reverse-cascade (child list stable under parent change).

## MCP verification recipes

Copy-paste templates for common sanity checks.

**Decoded-event coverage:**

```sql
SELECT event_name, count() AS n
FROM dbt.contracts_<protocol>_<contract>_events
GROUP BY event_name
ORDER BY n DESC
```

**Per-protocol mart integrity:**

```sql
SELECT protocol, count() AS rows, countDistinct(token) AS tokens
FROM dbt.<mart_view>
GROUP BY protocol
```

**Missing signatures for a whitelist:**

```sql
SELECT lower(replaceAll(address, '0x', '')) AS addr
FROM (SELECT arrayJoin(['0xaddr1','0xaddr2']) AS address)
WHERE lower(replaceAll(address, '0x', '')) NOT IN (
    SELECT lower(contract_address) FROM dbt.event_signatures
)
```

**Rank-vs-ASOF divergence spot-check** (if you suspect a fork is breaking rank pairing):

```sql
SELECT event_name, count() AS n
FROM dbt.contracts_<protocol>_Pool_events
WHERE decoded_params['reserve'] = '0x...'
GROUP BY event_name
-- FlashLoan or similar with count >> Supply/Borrow ⇒ use ASOF JOIN
```

## See Also

- [Adding dbt Models](add-model.md) — mechanics of model layers, `meta.api` contract, schema conventions
- [Adding Scrapers](add-scraper.md) — for non-EVM / off-chain data sources
- [Contract ABI Decoding](../data-pipeline/transformation/abi-decoding.md)
- [Aave V3](../protocols/lending/aave-v3.md) / [SparkLend](../protocols/lending/spark.md) — canonical protocol-aware lending example
- [Savings xDAI](../protocols/savings/index.md) — canonical ERC-4626 vault example with full rate derivation
