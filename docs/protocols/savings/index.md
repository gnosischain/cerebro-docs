# Savings xDAI (sDAI / sxDAI)

## Vault Fundamentals

The Gnosis Savings vault is a standard **ERC-4626** vault at address `0xaf204776c7245bF4147c2612BF6e5972Ee483701`, deployed on **2023-09-28**. It has been the onchain home of "Savings DAI" on Gnosis Chain since launch; the same address now holds **Savings USDS** after the 2025-11-07 Sky migration (see [regime section](#usds-migration)).

The vault exposes the canonical 4626 interface:

- `deposit(assets)` / `mint(shares)` → emits `Deposit(caller, owner, assets, shares)` and mints shares to `owner`.
- `withdraw(assets)` / `redeem(shares)` → emits `Withdraw(caller, receiver, owner, assets, shares)` and burns shares.
- `totalAssets()` reflects reserve value including accrued yield; `share_price = totalAssets / totalSupply`.

At any observable exchange event the ratio `assets / shares` gives the prevailing share price. This is the primary signal all downstream analytics run on.

## Yield Mechanism (why share-price is NOT continuous)

The vault does **not** accrue yield block-by-block. The path by which xDAI vault holders earn Sky DSR / sUSDS interest involves a periodic cross-chain relay:

1. **Mainnet.** The xDAI bridge (`0x4aa42145Aa6Ebf72e164C9bBC74fbD3788045016`) was upgraded such that DAI (now USDS) bridged into the xDAI pool is automatically deposited into the Spark sDAI vault on Mainnet, where it accrues Sky DSR / sUSDS interest continuously.
2. **Relay.** A permissionless `relayInterest()` (plus helpers `refillBridge()` / `investDAI()`) can be called every 1–2 days. It pulls accumulated xDAI/WXDAI into an `InterestReceiver` on Gnosis.
3. **Gnosis.** The `InterestReceiver` calls `payInterest()` which deposits the batch into the Savings xDAI vault. This **steps up `totalAssets()`** in a single tx, increasing `share_price` for every existing holder proportionally.

**Consequence for analytics.** Between relays the `share_price` observed from `Deposit` / `Withdraw` events is effectively flat; on a relay day it jumps. Viewed as a time series, `share_price` is a piecewise-constant staircase with ~daily risers, not a smooth exponential. Any "same-day ratio" APY estimator will hit 0% on flat days and huge spikes on relay days.

**Sources:**

- [Gnosis forum: Deposit DAI of the xDAI bridge in sDAI vault from Spark](https://forum.gnosis.io/t/deposit-dai-of-the-xdai-bridge-in-sdai-vault-from-spark/7236)
- [Spark docs: sDAI](https://docs.spark.fi/user-guides/earning-savings/sdai)

## USDS Migration (2025-11-07) {#usds-migration}

On **2025-11-07 18:07:25 UTC** (block `43027713`), Safe tx [`0xb6d709f3f6fe73958bf4de18a2d8ba81b8981a18e0c17c9f608e61c03ec0e166`](https://gnosisscan.io/tx/0xb6d709f3f6fe73958bf4de18a2d8ba81b8981a18e0c17c9f608e61c03ec0e166) executed the Sky DAI→USDS governance rename for the Gnosis vault.

- **Same vault address.** No redeployment, no new share series.
- **Backing flipped** from DAI-via-sDAI to USDS-via-sUSDS. Rate source flipped from Sky Savings Rate (SSR, inherited from DSR) to Sky Savings Rate on sUSDS — numerically the same governance-set rate, just relabelled.
- **Analytics metadata** lives in [`seeds/savings_xdai_regimes.csv`](https://github.com/gnosischain/dbt-cerebro/blob/main/seeds/savings_xdai_regimes.csv) — 2 rows, open-ended `end_ts_utc` on the post-migration regime. Downstream models attach these columns via an `argMax` lookup (ClickHouse `LEFT JOIN ON` forbids non-equi predicates; see [rate computation](#rate-computation)).

## dbt Models

### Canonical

- **`int_yields_savings_xdai_rate_daily`** — one row per calendar day from 2023-09-28 onwards. Columns: `date, share_price, daily_rate, canonical_label, legacy_symbol, backing_asset, yield_source`.
- **`fct_yields_savings_xdai_apy_daily`** — long-format APY with `label ∈ {Daily, 7DMA, 30DMA, 7DMM, 30DMM}`, one row per `(date, label)`. Regime columns pass through.

### Legacy wrappers (URL/consumer compat, unchanged shape)

- **`int_yields_sdai_rate_daily`** — thin `SELECT date, share_price AS sdai_conversion, daily_rate AS rate FROM int_yields_savings_xdai_rate_daily`.
- **`fct_yields_sdai_apy_daily`** — `SELECT date, apy, label FROM fct_yields_savings_xdai_apy_daily`.

## Rate Computation — Full Derivation {#rate-computation}

This is the load-bearing section of the doc. It walks through **two rejected approaches** and the **adopted rolling 7-day geometric slope**, with numeric examples from live data. Re-read this before touching [`int_yields_savings_xdai_rate_daily.sql`](https://github.com/gnosischain/dbt-cerebro/blob/main/models/execution/yields/intermediate/int_yields_savings_xdai_rate_daily.sql).

### Inputs

Decoded `Deposit` and `Withdraw` events from `contracts_sdai_events`. Extract `share_price` per event:

```sql
toFloat64(toUInt256OrNull(decoded_params['assets']))
  / nullIf(toFloat64(toUInt256OrNull(decoded_params['shares'])), 0) AS share_price
```

### End-of-day price via `argMax`

Collapse to one observation per calendar day — the **last** observed price within the day, broken by `(block_timestamp, log_index)`:

```sql
share_price_eod AS (
    SELECT
        toDate(block_timestamp) AS date,
        argMax(share_price, (block_timestamp, log_index)) AS share_price
    FROM vault_exchange_events
    GROUP BY date
)
```

### Forward-fill across event-less days

Left-join a calendar CTE and forward-fill with `last_value(share_price) IGNORE NULLS OVER (ORDER BY date)`. After this step every calendar day has a `share_price`.

### Attempt 1 — naive day-over-day ratio (REJECTED)

```sql
daily_rate = share_price / lagInFrame(share_price) OVER (ORDER BY date) - 1
```

**Symptom.** Steady-state APY swings 3.2%–5.5% day-to-day even during a quiet Sky DSR regime where the true rate is constant.

**Cause.** `argMax(share_price, (block_timestamp, log_index))` anchors each day at the timestamp of the day's last event. Consecutive days span anywhere from ~2h to ~46h of real accrual. Treating every such interval as exactly 24h is wrong.

### Attempt 2 — single-interval time-weighting (REJECTED)

Observed timestamps (carried alongside the price) let us normalise each ratio to a 24h equivalent:

```sql
daily_rate = pow(
    share_price / prev_price,
    86400.0 / greatest(dateDiff('second', prev_observed_at, observed_at), 1)
) - 1
```

**Steady-state fix.** This collapses the 3.2%–5.5% swings to a smooth ~0.012%/day ≈ 4.4% APY — correct when the share price accrues smoothly.

**Still fails on step-jumps.** Concretely, the **week-1 warmup** blows up:

| Day | `share_price` | Notes |
|-----|--------------|-------|
| 2023-09-28 → 2023-10-04 | `≈ 1.0000000001` | Vault dormant, no yield paid yet |
| 2023-10-05 23:35 UTC | `1.01345` | First `payInterest()` batch |

- Interval: ~89 400 seconds ≈ 24.8h.
- `daily_rate = pow(1.01345 / 1.0, 86400/89400) - 1 ≈ 0.01299` (1.3%/day)
- APY: `pow(1.013, 365) - 1 ≈ 110.52` → **~11 051% APY**

Time-weighting cannot help when a discrete payout is *compressed into a single day* — the elapsed interval is already near 24h, so the normalisation is a no-op. **Any single-day rate estimator has this problem.**

### Attempt 3 — rolling 7-day geometric slope (ADOPTED)

```sql
daily_rate = pow(
    share_price / first_value(share_price) OVER (
        ORDER BY date
        ROWS BETWEEN 7 PRECEDING AND 7 PRECEDING
    ),
    1.0 / 7
) - 1
```

**Intuition.** Compute the geometric growth rate that would have produced the observed 7-day price ratio if applied uniformly each day. A discrete payout on day `D` appears in the window for days `D..D+6` and is amortised across them.

**ClickHouse note.** ClickHouse does *not* expose `nthValue` as a window aggregate — error: `DB::Exception: Aggregate function with name 'nthValue' does not exist`. Use `first_value(...) OVER (ORDER BY date ROWS BETWEEN N PRECEDING AND N PRECEDING)` to read exactly the value `N` days ago.

**Guard conditions** (in the model):

```sql
CASE
    WHEN day_idx <= 7                         THEN NULL
    WHEN window_start_price IS NULL
      OR window_start_price = 0               THEN NULL
    ELSE pow(share_price / window_start_price, 1.0 / 7) - 1
END AS daily_rate
```

**Live-data results** (2023-09-28 → 2026-04-16, 931 daily rows):

- **Max `Daily` APY drops from 11 051% → 134.73%.** The 134% peak is residual warmup (a single 1.3% jump divided across 7 days ≈ 0.19%/day ≈ 97% APY on day 1, decaying as the window fills).
- **Steady-state `Daily` APY stays in 4.19%–4.44%** over the last 30 days — matching the Sky DSR / sUSDS rate set by governance.
- **7DMA / 30DMA / 7DMM / 30DMM** labels in `fct_yields_savings_xdai_apy_daily` then smooth the warmup tail further.

### Why not clamp outliers?

Clamping (`WHERE daily_rate < threshold`, `CASE WHEN rate > X THEN NULL`) was **explicitly rejected**: it hides real model problems and makes the output unreliable. The geometric-slope approach is mathematically clean; any remaining warmup artefact is transparent and decays without manual intervention. This repo's general rule: **never put cuts like `balance > 0` or `borrow > supply` to paper over bugs — they mask model issues**.

### Regime attachment

ClickHouse `LEFT JOIN ... ON` requires equality conditions. The regime boundaries are time-ranges, so we pre-compute each date's regime via `argMax` over the seed:

```sql
regime_lookup AS (
    SELECT
        r_outer.date,
        argMax(r.canonical_label, parseDateTimeBestEffort(r.start_ts_utc)) AS canonical_label,
        argMax(r.legacy_symbol,   parseDateTimeBestEffort(r.start_ts_utc)) AS legacy_symbol,
        argMax(r.backing_asset,   parseDateTimeBestEffort(r.start_ts_utc)) AS backing_asset,
        argMax(r.yield_source,    parseDateTimeBestEffort(r.start_ts_utc)) AS yield_source
    FROM rated_with_rate r_outer
    CROSS JOIN {{ ref('savings_xdai_regimes') }} r
    WHERE parseDateTimeBestEffort(r.start_ts_utc) <= toDateTime(r_outer.date)
      AND (r.end_ts_utc = '' OR toDateTime(r_outer.date) < parseDateTimeBestEffort(r.end_ts_utc))
    GROUP BY r_outer.date
)
```

### APY + moving windows

In `fct_yields_savings_xdai_apy_daily`:

- `apy = floor(pow(1 + daily_rate, 365) - 1, 4) * 100`
- `apy_7DMA = floor(avg(pow(1 + daily_rate, 365) - 1) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW), 4) * 100`
- `apy_30DMA` — same, 29 preceding.
- `apy_7DMM` / `apy_30DMM` — `median(...)` instead of `avg(...)`.

Labels are emitted long-format via 5× `UNION ALL` so the frontend drives a single `seriesField: label` chart.

## Pitfalls to know before touching this pipeline

1. **`nthValue` does not exist** as a ClickHouse window aggregate. Use `first_value(x) OVER (ORDER BY date ROWS BETWEEN N PRECEDING AND N PRECEDING)`.
2. **Do not filter placeholder-looking prices** like `1.0000000001`. Those are the vault's first real `Deposit` events and are needed to anchor the 7-day window.
3. **Do not clamp `daily_rate`.** Expose the warmup period honestly — it falls off as more data accumulates.
4. **Forward-fill preserves the price**; if you carry the observed timestamp for other logic, carry it alongside (don't forward-fill the timestamp).
5. **Compute `pow(1 + rate, 365) - 1` in Float64.** If `rate` is Decimal, cast first, or ClickHouse will silently overflow on intermediate values.
6. **Regime join must use `argMax`**, not `LEFT JOIN ON` with range predicates — ClickHouse rejects non-equi join conditions.

## Example Queries

### Daily / 7DMA / 30DMM APY last 90 days

```sql
SELECT date, label, apy
FROM dbt.fct_yields_savings_xdai_apy_daily
WHERE date >= today() - 90
  AND label IN ('Daily', '7DMA', '30DMM')
ORDER BY date, label
```

### Pre/post-USDS APY mean comparison

```sql
SELECT
    backing_asset,
    avg(apy) AS mean_apy,
    count() AS days
FROM dbt.fct_yields_savings_xdai_apy_daily
WHERE label = 'Daily'
GROUP BY backing_asset
ORDER BY backing_asset
```

### Detect relay-day step-jumps

```sql
SELECT date, share_price, daily_rate
FROM dbt.int_yields_savings_xdai_rate_daily
WHERE daily_rate > 2 * avg(daily_rate) OVER (ORDER BY date ROWS BETWEEN 30 PRECEDING AND 1 PRECEDING)
ORDER BY date
```

### Supply trend by regime

```sql
SELECT
    toStartOfWeek(date) AS week,
    backing_asset,
    argMax(share_price, date) AS end_of_week_price
FROM dbt.int_yields_savings_xdai_rate_daily
GROUP BY week, backing_asset
ORDER BY week
```

## See Also

- [Lending Protocols — Aave V3](../lending/aave-v3.md) and [SparkLend](../lending/spark.md) — the `SXDAI` reserve that lists this vault token as collateral
- [Adding a New Protocol](../../developer/add-protocol.md) — blueprint for wiring up any new EVM protocol
- [Contract ABI Decoding](../../data-pipeline/transformation/abi-decoding.md)
