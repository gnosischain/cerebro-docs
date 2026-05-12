---
title: Recovering from a Prices Gap
description: Step-by-step recovery flow for re-deriving USD-denominated columns after the Dune prices source skipped a day
---

# Recovering from a Prices Gap

When the Dune query that feeds `int_execution_token_prices_daily` skips a day, every dbt model that joins prices either drops rows (the LEFT JOIN's NULL price collapses to a zero `*_usd`) or has zero rows for that date entirely. After Dune backfills the missing day, the affected dbt rows still hold their original (wrong) values until they're re-derived.

This page walks through the recovery flow end-to-end using the 2026-04-17 incident as a worked example.

## TL;DR

```bash
docker exec dbt /app/scripts/maintenance/refill_after_price_gap.sh \
  --from-date 2026-04-17
```

That single command triggers the two-phase flow described below. The rest of this page explains what's happening and how to handle the edge cases.

## Why three phases

Models split cleanly into two recovery cohorts, plus a final rebuild step for downstream tables:

| Phase | Cohort / target | Recovery path | Why |
| --- | --- | --- | --- |
| **1** | Heavy aggregates (`tag:refill_append`) | **Two-pass** append-rewrite per month + `OPTIMIZE PARTITION FINAL DEDUPLICATE` between passes | `delete+insert` over a multi-day lookback issues `ALTER TABLE DELETE` mutations that OOM on big GROUP BYs (CH 341). Two passes are needed because RMT merges are *eventually consistent* — a single-pass refill can let aggregators read upstream's unmerged duplicates and bake inflated values. |
| **1.5** | Canary check | Adjacent-day ratio scan on `int_execution_tokens_supply_holders_daily` (GNO) | Confirms Phase 1 actually converged. Warns and stops the script if a > 1.5× jump appears on the month boundary. |
| **2** | Lighter consumers (`int_execution_token_prices_daily+ --exclude tag:refill_append`) | `delete+insert` with widened `price_lookback_days` | Small tables, lookback mutations are cheap. |
| **3** | Downstream `fct_*` (table) + `api_*` (view) of the cohort | `dbt run --select tag:refill_append+ --exclude tag:refill_append` | `fct_*` tables are full-rebuild materializations — they hold STALE values until explicitly re-run, even after Phase 1 corrects the `int_*` upstream. |

### The two-pass requirement

This is the subtle one. Even though dbt resolves DAG order within a single `dbt run`, ClickHouse's RMT engine merges parts *lazily, in the background*. So in a single-pass refill:

1. dbt runs `int_execution_tokens_balances_daily` in append mode → writes new April rows alongside old ones (RMT to merge later).
2. dbt then runs `int_execution_tokens_supply_holders_daily` immediately, executing `sum(balance) GROUP BY (date, token_address)` against `int_execution_tokens_balances_daily`.
3. Because RMT hasn't merged yet, the source has 4 unmerged rows per address → the `sum(...)` is **4× the correct value** → that wrong value is appended to `supply_holders`.
4. RMT later collapses both layers, but the surviving `supply_holders` row is still the wrong one.

Symptom: a clean row count (`count() = count(DISTINCT unique_key)`) but a large *value* jump on the first day of the refilled month. The 2026-04-17 incident produced exactly this — every model that aggregated from `int_execution_tokens_balances_daily` (supply_holders, balance_cohorts, balances_by_sector, account_balance_history) showed a 4× supply value for April that persisted past the refill.

**Fix:** force RMT to merge before running aggregators. Phase 1 now runs every model, OPTIMIZEs every partition, then runs every model AGAIN, and OPTIMIZEs again. The second pass writes correct values; the second OPTIMIZE retains them.

### Phase 1 — `tag:refill_append` (two-pass)

The script discovers Phase 1 models via `dbt ls --select tag:refill_append`. As of this writing the cohort is:

- `int_execution_tokens_balances_daily`
- `int_execution_lending_aave_user_balances_daily`
- `int_execution_account_balance_history_daily`
- `int_execution_tokens_balance_cohorts_daily`
- `int_execution_tokens_balances_by_sector_daily`
- `int_execution_tokens_supply_holders_daily`
- `int_execution_lending_aave_balance_cohorts_daily`
- `int_execution_gpay_activity`
- `int_execution_pools_fees_daily`
- `int_revenue_holdings_fees_daily`
- `int_revenue_sdai_fees_daily`
- `int_revenue_gpay_fees_daily`

For each affected month, the script runs **two full passes**:

```bash
# Pass A — append-rewrite + OPTIMIZE every model
dbt run --select tag:refill_append \
  --vars '{"start_month":"2026-04-01","end_month":"2026-04-01"}'
for model in $(dbt ls --select tag:refill_append --resource-type model --output name); do
  dbt run-operation optimize_partition_final \
    --args "{database: dbt, table_name: ${model}, partition: \"2026-04-01\"}"
done

# Pass B — same, but now upstream is merged so aggregators read correct values
dbt run --select tag:refill_append \
  --vars '{"start_month":"2026-04-01","end_month":"2026-04-01"}'
for model in $(dbt ls --select tag:refill_append --resource-type model --output name); do
  dbt run-operation optimize_partition_final \
    --args "{database: dbt, table_name: ${model}, partition: \"2026-04-01\"}"
done
```

### Phase 2 — `int_execution_token_prices_daily+ --exclude tag:refill_append`

```bash
dbt run --select int_execution_token_prices_daily+ \
  --exclude tag:refill_append \
  --vars '{"price_lookback_days": 12}' \
  --project-dir /app --profiles-dir /app
```

The lineage selector pulls every model that transitively `ref()`s the prices view. The exclude removes Phase-1 cohort. The `price_lookback_days` var widens the lookback in `apply_monthly_incremental_filter` for every model in the run — no per-model edits required.

### Phase 3 — rebuild downstream `fct_*` tables and `api_*` views

```bash
dbt run --select tag:refill_append+ \
  --exclude tag:refill_append \
  --project-dir /app --profiles-dir /app
```

The `+` operator is "all descendants". This refreshes:

- `fct_*` tables (e.g. `fct_execution_tokens_metrics_daily`) — full rebuild against the corrected `int_*` rows.
- `api_*` views — automatically reflect the corrected upstream on next read; rebuilding them is a no-op for data correctness but verifies they still compile.

**Without Phase 3**, the API views show STALE values even after Phase 1 fixes the `int_*` source — because `fct_*` tables in between hold the old aggregate.

## Worked example — 2026-04-17 gap

### What happened

1. Dune query that feeds `int_execution_token_prices_daily` skipped 2026-04-17.
2. Daily cron continued running for ~10 days. Every `*_usd` column for 04-17 in every downstream model was zero (price=NULL → `coalesce(p.price, 0)` → 0 USD).
3. Dune later backfilled 04-17 — `int_execution_token_prices_daily` (a view) immediately reflected the correct prices on every read.
4. But the materialized downstream tables still had the zeroes.

### Step 1 — Compute the lookback

```bash
docker exec dbt /app/scripts/maintenance/refill_after_price_gap.sh \
  --from-date 2026-04-17 --dry-run
```

Output:

```
[Mon Apr 27 22:56:18 UTC 2026] refill_after_price_gap.sh
  from-date           : 2026-04-17  (gap = 10 d, +1 buffer)
  price_lookback_days : 12
  affected months     : 2026-04-01
  selector (phase 2)  : int_execution_token_prices_daily+
  phase 1 selector    : tag:refill_append
  ...
```

Lookback is `(today − from-date) + 1 (inclusive) + buffer (default 1) = 10 + 1 + 1 = 12`. Affected months is the unique set of `toStartOfMonth(date)` covering the gap window — here just `2026-04-01`.

### Step 2 — Run the recovery

```bash
docker exec dbt /app/scripts/maintenance/refill_after_price_gap.sh \
  --from-date 2026-04-17
```

Phase 1 logs look like:

```
=== Phase 1: append-rewrite tag:refill_append + OPTIMIZE ===
[phase1] month=2026-04-01  rewrite (append, dbt-managed DAG order)
1 of 12 START sql incremental model `dbt`.`int_execution_tokens_balances_daily`  [RUN]
1 of 12 OK created sql incremental model `dbt`.`int_execution_tokens_balances_daily`  [OK in 9.54s]
2 of 12 START sql incremental model `dbt`.`int_execution_lending_aave_user_balances_daily`  [RUN]
...
[phase1] int_execution_tokens_balances_daily  month=2026-04-01  OPTIMIZE PARTITION FINAL DEDUPLICATE
[phase1] int_execution_lending_aave_user_balances_daily  month=2026-04-01  OPTIMIZE PARTITION FINAL DEDUPLICATE
...
```

Phase 2:

```
=== Phase 2: int_execution_token_prices_daily+ --exclude tag:refill_append  (price_lookback_days=12) ===
1 of 312 START sql incremental model `dbt`.`int_revenue_fees_unified_daily` [RUN]
...
312 of 312 OK created sql view model `dbt`.`api_execution_account_search_index` [OK in 0.14s]
Done. PASS=312 WARN=0 ERROR=0 SKIP=0 TOTAL=312
```

### Step 3 — Verify

```sql
-- Confirm balance_usd is non-zero on the gap day
SELECT toDate(date) AS d, count() AS rows, countIf(balance_usd IS NULL OR balance_usd = 0) AS zero_usd
FROM dbt.int_execution_tokens_balances_daily
WHERE toDate(date) >= toDate('2026-04-15')
GROUP BY d ORDER BY d;
```

Expected: `zero_usd = 0` for every day post-fix.

```sql
-- Confirm a downstream API view has data on the gap day
SELECT date, label, value
FROM dbt.api_execution_gpay_volume_payments_by_token_daily
WHERE date = toDate('2026-04-17')
ORDER BY label;
```

Expected: non-zero `value` for each token symbol.

## Edge cases and flags

### Specifying lookback directly

If you don't have a clean from-date (e.g. you just want to widen the window):

```bash
docker exec dbt /app/scripts/maintenance/refill_after_price_gap.sh \
  --lookback-days 14
```

### Skipping a phase

```bash
# Only Phase 1 (heavy refill), skip the lighter downstream re-pull
--skip-price-dependent

# Only Phase 2, skip the heavy month rewrite
--skip-balances-rewrite
```

### Restricting Phase 2

```bash
# Only re-pull a specific subtree
--select int_revenue_sdai_fees_daily+
```

### Buffer days

```bash
# Pad the trailing edge of the lookback (default 1)
--buffer-days 3
```

The buffer covers cases where the gap window has soft edges — partial data on adjacent days that needs the same re-pull.

### Several-week-old gaps

```bash
docker exec dbt /app/scripts/maintenance/refill_after_price_gap.sh \
  --from-date 2026-03-30
```

The script auto-derives the month list (`2026-03-01`, `2026-04-01` for that example) and runs Phase 1's append+OPTIMIZE for each. Phase 2's lookback is `(today − 2026-03-30) + 2 = ~30+`, which the macro applies to every consumer in the lineage.

## Failure modes

### Phase 1 hits `Code: 241 — MEMORY_LIMIT_EXCEEDED`

Symptom: a `refill_append` model OOMs during the append rewrite.

Fix: that model is missing the spill-to-disk pre-hook contract. Add it via the shared macro:

```python
{{ config(
    ...
    pre_hook=refill_safe_pre_hook(),
    post_hook=refill_safe_post_hook(),
    tags=[..., 'refill_append'],
) }}
```

The macros are in `macros/db/refill_safe_hooks.sql`. They cap memory at 8 GiB and force GROUP BY / sort to spill at 2 GiB, with `join_algorithm='grace_hash'` so JOINs spill too. Then re-run the script — it's idempotent (RMT + OPTIMIZE collapses any duplicates from prior partial runs).

### Phase 1 hits `Code: 341 — Mutation memory limit exceeded`

Should not happen — Phase 1 is `append`, not `delete+insert`. If it does, check that the model's strategy expression includes the `start_month` branch:

```python
incremental_strategy=(
  'append' if (var('start_month', none) or var('incremental_end_date', none))
  else 'delete+insert'
)
```

### Phase 1 leaves duplicates if `OPTIMIZE` is killed mid-run

Re-run the script. Append + OPTIMIZE is idempotent — re-appending a month that's already been written queues more duplicates, which the next OPTIMIZE collapses regardless of how many append passes occurred.

### A poisoned mutation blocks subsequent runs

Symptom: `Code: 341 referencing dropped temporary table __dbt_new_data_*`. A previous `delete+insert` run was killed mid-mutation.

Fix:

```bash
docker exec dbt dbt run-operation kill_failed_mutations \
  --project-dir /app --profiles-dir /app
```

Then retry. The `dbt_incremental_runner.py` does this automatically on startup, but the refill script doesn't (yet) — so on rare occasions you may need to run it by hand.

## Adding a model to Phase 1

If you discover a new heavy model (OOMs under wide-lookback `delete+insert`, e.g. it has window functions over many partitions or a `countDistinct` over a month of source data):

1. Tag it `refill_append`:

   ```python
   tags=['production', '...', 'refill_append']
   ```

2. Make sure its strategy expression is the three-branch form:

   ```python
   incremental_strategy=(
     'append' if (var('start_month', none) or var('incremental_end_date', none))
     else 'delete+insert'
   )
   ```

3. Make sure the model's WHERE clause has the `start_month`/`end_month` filter branch (the standard pattern in this repo):

   ```jinja
   {% if start_month and end_month %}
     AND toStartOfMonth(date) >= toDate('{{ start_month }}')
     AND toStartOfMonth(date) <= toDate('{{ end_month }}')
   {% else %}
     {{ apply_monthly_incremental_filter('date', 'date', true) }}
   {% endif %}
   ```

4. Add the spill-to-disk hooks:

   ```python
   pre_hook=refill_safe_pre_hook(),
   post_hook=refill_safe_post_hook(),
   ```

That's it — `refill_after_price_gap.sh` picks the model up via the tag selector. No edits to the script.

## Why we don't tag every prices descendant

An earlier iteration used a `price_dependent` tag on every prices consumer. That had three problems:

1. **Manual & easy to miss.** Every new consumer had to remember to add the tag and plumb a `var()` call. The 2026-04-17 incident exposed two missed models in the gpay chain that left zero values in `api_execution_gpay_volume_payments_by_token_daily`.
2. **Tag drift.** The set of consumers grew silently as new models were added.
3. **Two coordinated edits per model** (tag + var) — either alone was silently wrong.

The current design fixes all three:

- **Lineage replaces the tag** for the lighter cohort. `int_execution_token_prices_daily+` enumerates every prices consumer transitively from the dbt graph. New consumers are picked up automatically.
- **The macro reads the var directly** for the lighter cohort. `apply_monthly_incremental_filter` reads `var('price_lookback_days', lookback_days)`, so widening the window is a global operation — no per-model plumbing.
- **`refill_append` is much narrower** — it identifies models that need a different *recovery semantics* (append + OPTIMIZE), not models that *consume prices*. As a property of the model itself (heavy aggregate prone to mutation OOM), it's stable and self-documenting.

## Related

- [Incremental Strategies](../data-pipeline/transformation/incremental-strategies.md) — the four invocation modes and how the strategy expression routes between them
- [Running Models](../data-pipeline/transformation/running-models.md) — the four runners
- [Troubleshooting](troubleshooting.md) — broader incident response
