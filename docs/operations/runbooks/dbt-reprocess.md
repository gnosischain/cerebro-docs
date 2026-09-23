---
title: dbt Reprocess After Upstream Repair
description: The decision tree for making the dbt layer correct again after an indexer repair, scoped, with no full refresh
---

# Reprocess dbt after an upstream repair — without a full refresh

An indexer was repaired. The dbt layer still shows the old numbers. This is how to make it correct again, scoped, with no full refresh anywhere unless a leaf below says so and why.

**Fix the raw layer first.** If `execution.logs` still lacks the rows, every dbt lever faithfully reproduces the gap.

Run everything here inside a one-shot dbt job ([how](one-shot-jobs.md)), in a quiet window. **There is no lock against the 06:00 cron or the 45-second live loop.**

## Pre-flight — repo policy, not a suggestion

```bash
python /app/scripts/agent_context/context.py --select ⟨model⟩ --task backfill
ls /app/target/refresh_state/ ; ls -la /app/target/gap_refresh_state.json
```

`context.py` prints the model's materialization, strategy, staged config, cumulative flag, hazards and the safe reprocess lever. It takes **no** `--project-dir`.

Two different state mechanisms: `refresh.py` uses `target/refresh_state/`, `gap_window_refresh.py` uses its own `--state` file. Check both. A pending run must be `--resume`d or `--clear-state`d, never deleted.

!!! warning "Capture a baseline. `REPLACE PARTITION` has no undo."
    ```sql
    SELECT toStartOfMonth(⟨date_col⟩) AS m, count() AS rows, uniqExact(⟨grain⟩) AS keys
    FROM dbt.⟨model⟩ GROUP BY m ORDER BY m;
    ```
    After the run: a shrunk date span is a **wipe**; an exact doubling is a **duplicate**. Marts read ReplacingMergeTree **without** `FINAL`, so both copies count.

## Find the blast radius

```bash
dbt ls -s source:⟨db⟩.⟨table⟩+ --resource-type model --output name > /tmp/closure.txt
grep -rl '{{ this }}' models/ | sort > /tmp/cumulative.txt
comm -12 <(sort /tmp/closure.txt) /tmp/cumulative.txt
```

The intersection is the **cumulative** set — 39 models today; re-run the grep rather than trusting that number. Cumulative models read their own previous output, so they are wrong from the gap **day** forward, not just inside the gap month. They must be rebuilt **history-first, chronologically, through the current month**.

## Branch 1 — which source was repaired

| Source | Lever |
|---|---|
| `execution.logs` / `blocks` / `transactions` (cryo) | `gap_window_refresh.py` over the decode subtree |
| `consensus` (beacon) | same lever; check each intermediate's strategy with `context.py` first |
| `rpc_state_indexer` | nothing to flip — dbt selects the published attempt from the base tables. Current month: plain run. Past months: drop-partition + append, **both month vars**, then OPTIMIZE |
| `crawlers_data` prices | [`refill_after_price_gap.sh`](../prices-gap-recovery.md) |
| other `crawlers_data` / `governance_db` / `hopr_db` | plain `dbt run -s source:⟨x⟩+` |
| `envio_ga` | fix the mirror with `maintain reprocess` first, then a plain run of the int layer |
| `cow_db` | **nothing** — dbt does not read `cow_db`. The CoW models read the on-chain decode, so this is the first row |

### Why decode models cannot self-heal

Decode models are `incremental_strategy='append'` with a **literal block watermark and no lookback**. Anything backfilled *below* that watermark is invisible to every subsequent run, forever.

!!! warning "Never use the daily microbatch runner to recover backfilled history"
    It only advances watermarks. It produces a completely green run that fixes nothing.

!!! warning "Never add a daily lookback to an append decode"
    It duplicates rows until a background merge, and downstreams read without `FINAL`, so they double-count.

## `gap_window_refresh.py` — the lever, and its guards

It drops the gap-month partition (which *lowers* the watermark), then re-runs scoped.

```bash
python /app/scripts/refresh/gap_window_refresh.py \
  --select ⟨decode_model⟩+ \
  --exclude 'tag:live+' \
  --months 2026-07-01,2026-08-01,2026-09-01 \
  --state /app/target/gap_refresh_state.json \
  --full-refresh-row-cap 0 \
  --dry-run
```

Every flag above is load-bearing:

!!! warning "Always `--dry-run` first, and read the ACTION column"
    The script branches three ways. Month-partitioned models get drop + scoped re-run. But any **append or delete+insert model with no `start_month` branch** gets `dbt run --select ⟨m⟩ --full-refresh` — a full drop and rebuild. The only guard is a row cap defaulting to 5,000,000, so any such table below that is silently rebuilt. Any line beginning `full-refresh` is that case.

- `--full-refresh-row-cap 0` makes it **skip and report** those models instead of rebuilding them (`--allow-big-full-refresh` is the explicit override).
- `--state` is mandatory in-cluster. The default path is on the read-only image layer, so the first save raises `OSError` — **after** partitions have already been dropped.
- `--exclude 'tag:live+'` is the correct selector. `--exclude '*_live+'` excludes a model the live loop never touches and fails to exclude the 19 it does.
- `--months` must span the gap month **through the current month** whenever a month boundary has been crossed since the gap, because of the cumulative rule above. Gap-month-only is correct only while the gap month *is* the current month.

Never run it on a `table`-materialized model. Batched or windowed runs truncate a `table` to the last batch; a plain `dbt run -s` is the only correct lever there.

## Branch 2 — the model's materialization

From `context.py`:

| Materialization / strategy | Lever |
|---|---|
| `insert_overwrite`, month-partitioned | Whole-month plain run, **or** drop partition + run. Never a narrower window |
| `append` (decode) | `gap_window_refresh.py`. Never a lookback, never a scoped append over a populated month |
| `delete+insert` (10 grandfathered) | Per slice, never wide. Check `system.mutations` after any failure |
| `table` | Plain `dbt run -s` **only** |
| `view` | Nothing — live |
| the five `reprocess_overwrite` models | `--vars '{start_month: M, end_month: M, reprocess_overwrite: true}'`, **one month at a time**, then OPTIMIZE |
| cumulative (`{{ this }}` reader) | History first, chronological, through the current month |

!!! warning "`reprocess_overwrite` is honoured by exactly five models"
    `int_execution_tokens_balances_native_daily`, `int_execution_lending_aave_user_balances_daily`, `int_execution_lending_aave_balance_cohorts_daily`, `int_execution_pools_uniswap_v3_daily`, `int_revenue_fees_weekly_per_user` — confirm with `grep -rl "var('reprocess_overwrite'" models/`. Elsewhere the var is **inert** and the run appends a duplicate month.

!!! warning "Always pass both `start_month` and `end_month`"
    `start_month` alone selects append *plus* the legacy lookback window and duplicates rows.

## The five hazards that have actually cost data

1. **Never stage or batch an `insert_overwrite` model.** Any run window narrower than the partition REPLACEs the whole partition — a month collapses to one day.
2. **Never run a scoped append over an already-populated month.** It is a backfill-into-empty tool; re-running exactly doubles the data.
3. **Never run a wide `delete+insert`.** With `mutations_sync: 0` the DELETE keeps executing after dbt reports failure; the DELETE lands, the INSERT never runs, months vanish with no error.
4. **Never select a source model and an aggregator that reads it in the same append-mode invocation.** DAG order runs the append first and the aggregator bakes in the un-merged duplicate rows.
5. **Never retry an append that was killed mid-insert without dropping the partition first.**

## Seeds — the failure that froze everything green

A `dbt seed` deployed from a **stale checkout** once wiped the `chain` column on the signature and ABI seeds, and because `decode_logs` filters `WHERE chain = 'gnosis'`, the entire decode fleet silently appended zero rows. Every run stayed green for days.

Deploy seeds only from the merged tip, with `--full-refresh`, and verify **row counts *and* the `chain` distribution** afterwards. The symptom to recognise is decode models appending 0 rows with no error.

## Verify

```sql
-- no duplicates at the published grain
SELECT count() FROM (
  SELECT ⟨grain_cols⟩, count() c FROM dbt.⟨model⟩
  WHERE toStartOfMonth(⟨date_col⟩) = '⟨YYYY-MM-01⟩' GROUP BY ⟨grain_cols⟩ HAVING c > 1
);                                   -- want 0

-- decoded == raw, per family per month (catches BOTH missing and doubled)
SELECT toStartOfMonth(block_timestamp) m, count() FROM dbt.⟨decode_model⟩
WHERE block_number >= ⟨lo⟩ AND block_number < ⟨hi⟩ GROUP BY m;
SELECT toStartOfMonth(block_timestamp) m, count() FROM execution.logs
WHERE address = '⟨contract⟩' AND block_number >= ⟨lo⟩ AND block_number < ⟨hi⟩ GROUP BY m;
```

Equality, not "more than before". Then `max(⟨date_col⟩)` against the upstream — **a green run is not proof.** Refused stages exit 0, silently-empty slices report success, and a never-seeded incremental passes forever at 0 rows.

Where the protocol requires it, OPTIMIZE through the macro so it is synchronous:

```bash
dbt run-operation optimize_partition_final \
  --args '{"database":"dbt","table_name":"⟨T⟩","partition":"⟨YYYY-MM-01⟩"}'
```

Finally, `dbt test --select tag:data_quality_daily`. Note `dq_daily_registry_abi_coverage` is `severity='error'` — the other 11 are warnings.

!!! info "Internal runbook"
    [runbooks/31-dbt-reprocess-after-upstream-repair.md](https://github.com/gnosisdevops/infrastructure-gnosis-analytics/blob/main/runbooks/31-dbt-reprocess-after-upstream-repair.md) — private repository; carries the cluster-specific commands for this page.
