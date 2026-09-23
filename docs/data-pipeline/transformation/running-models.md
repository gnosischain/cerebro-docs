---
title: Running Models
description: The levers that drive dbt-cerebro models in production — daily cron, live loop, microbatch catch-up, full-refresh batching, gap-window refresh, refill recovery — and when each one is safe
---

# Running Models

Five scripts and the plain `dbt run` drive dbt-cerebro models in production. Which lever is safe depends on the model's materialization and on *why* you are running it. The decision tree lives on [dbt reprocess after upstream repair](../../operations/runbooks/dbt-reprocess.md); this page is the reference for each lever.

If you haven't read [Incremental Strategies](incremental-strategies.md) yet, do so first — it explains why the same model behaves differently across these runners.

!!! warning "Where these run"
    In production every command below runs inside a one-shot clone of the daily dbt CronJob, in a quiet window — see [One-shot jobs](../../operations/runbooks/one-shot-jobs.md). **There is no lock against the 06:00 cron or the 45-second live loop.** The `docker exec dbt …` form is the local Compose equivalent.

## TL;DR

| Goal | Lever |
| --- | --- |
| Run a single model right now (default daily-incremental behaviour) | `dbt run --select ⟨model⟩` |
| Bring an annotated incremental model up to today via per-day slices | `python /app/scripts/refresh/dbt_incremental_runner.py --select ⟨model⟩` |
| Backfill a model month-by-month from its declared start date | `python /app/scripts/full_refresh/refresh.py --select ⟨model⟩` |
| Catch up a model the cron **refused**, without dropping the table | `python /app/scripts/full_refresh/full_refresh.py --select ⟨model⟩ --stage _default --incremental-only` |
| Repair dbt after an indexer backfilled history **below** a watermark | `python /app/scripts/refresh/gap_window_refresh.py … --dry-run` first — Mode 4 |
| Recover after the prices source skipped a day | `/app/scripts/maintenance/refill_after_price_gap.sh --from-date YYYY-MM-DD` |
| Know which of the above is safe for *this* model | `python /app/scripts/agent_context/context.py --select ⟨model⟩ --task backfill` |

Flag gotchas that have cost time: only `dbt_incremental_runner.py` accepts `--project-dir` / `--profiles-dir` — `refresh.py` and `gap_window_refresh.py` reject them and exit 2 at argparse. `context.py` takes no `--project-dir`. `classify_failed_nodes.py` takes `--stash-dir`, not `--dir`.

---

## Mode 1 — Daily cron (`run_dbt_observability.sh`)

The daily CronJob at **06:00 UTC** runs `cron_preview.sh` → `scripts/run_dbt_observability.sh`, which delegates each batch to `scripts/refresh/dbt_incremental_runner.py`. One attempt, no Kubernetes retries — the orchestrator owns retries internally (transients are retried once at `--threads 1`). For models with no microbatch annotation, the runner falls back to plain `dbt run --select <batch>` with no vars set — the **daily incremental** mode (`delete+insert` over the macro's lookback).

You don't normally invoke this manually. To reproduce a single batch the cron would run:

```bash
dbt run --select int_execution_blocks_daily
```

What ClickHouse sees:

```sql
INSERT INTO dbt.int_execution_blocks_daily SELECT ...
WHERE toStartOfMonth(toDate(block_timestamp)) >= ( -- last month's start
  SELECT toStartOfMonth(addDays(max(toDate(x1.date)), 0)) FROM dbt.int_execution_blocks_daily AS x1
)
AND toDate(block_timestamp) >= (
  SELECT addDays(max(toDate(x2.date)), 0) FROM dbt.int_execution_blocks_daily AS x2
);
ALTER TABLE dbt.int_execution_blocks_daily DELETE WHERE date IN (...inserted dates...);
```

The mutation deletes the previous version of the rewritten dates so RMT doesn't have to dedupe. Cheap on small daily windows; expensive on large windows (which is why the next modes exist).

When the run fails, [The dbt daily run failed](../../operations/runbooks/dbt-daily-run-failed.md) is the procedure: reading the log, classifying transient vs permanent, rerunning only what failed.

### The live loop

Separately, a one-replica Deployment runs `dbt run --select tag:live` (19 models) every 45 seconds. It is `Recreate` and must never be scaled — two pods would run the same incremental models against the same tables. Restarting it opens a gap that closes on the next tick; restarting it twice in quick succession is two gaps. Anything windowed you run by hand should carry `--exclude 'tag:live+'`.

---

## Mode 2 — Microbatch runner (`dbt_incremental_runner.py`)

For models tagged `microbatch` (and configured in `meta.full_refresh.incremental` in their `schema.yml`), the runner slices the gap between `max(target_date)` and today into per-day windows.

```bash
python /app/scripts/refresh/dbt_incremental_runner.py \
  --select int_consensus_validators_income_daily
```

Internally the runner emits one `dbt run` per slice, with `incremental_end_date` set:

```bash
dbt run --select int_consensus_validators_income_daily \
  --vars '{"incremental_end_date": "2026-04-21", "validator_index_start": 0, "validator_index_end": 100000}'
dbt run --select int_consensus_validators_income_daily \
  --vars '{"incremental_end_date": "2026-04-22", "validator_index_start": 0, "validator_index_end": 100000}'
...
```

Two important effects:

1. **Strategy flips to `append`** because the strategy expression is `('append' if (start_month or incremental_end_date) else 'delete+insert')`. No mutation per slice.
2. **`apply_monthly_incremental_filter` takes its no-overlap branch** — `WHERE date > max(target_date) AND date <= incremental_end_date`. Re-running the same slice writes nothing (idempotent).

!!! warning "The runner only advances watermarks"
    It cannot see anything backfilled *below* a model's watermark. After an indexer repair it produces a completely green run that fixes nothing — that case is Mode 4.

### Common runner flags

| Flag | Effect |
| --- | --- |
| `--select <selector>` | Same syntax as `dbt run`; supports `+`, `tag:`, `path:` |
| `--max-end-date YYYY-MM-DD` | Cap slicing at this date (otherwise stops at today) |
| `--max-slices-per-stage N` | Refuse if the gap is longer than N days (default 30). Never raise it on the cron path |
| `--dry-run` | Print the slice plan, no DB writes |
| `--resume` | Skip slices already completed in `target/incremental_microbatch_state.json` — **inert in a one-shot job**, whose `target/` dies with the pod |

### When the runner refuses

```
gap is 615 day(s); exceeds --max-slices-per-stage=30
```

A refusal has three possible causes — no consumers, stalled, or dormant — and each has a different answer. The triage table is on [The dbt daily run failed](../../operations/runbooks/dbt-daily-run-failed.md#5-refused-stages).

!!! warning "The runner's printed fix drops the table"
    It prints a `full_refresh.py` command per refused model **without `--incremental-only`**. Run as printed it drops the table and rebuilds from the model's configured start date. For a stalled model the correct command is `full_refresh.py --select ⟨m⟩ --stage _default --incremental-only`, followed by its downstream chain.

---

<a id="mode-3"></a>

## Mode 3 — Full-refresh batched (`refresh.py`)

For historical backfill into an **empty** or dropped table, monthly batches are the right granularity. Each model declares its history under `meta.full_refresh` in `schema.yml`:

```yaml
- name: int_consensus_validators_income_daily
  meta:
    full_refresh:
      start_date: "2021-12-01"
      batch_months: 1
      stages:
        - name: validators_0_100k
          start_date: "2021-12-01"
          vars: { validator_index_start: 0, validator_index_end: 100000 }
        - name: validators_100k_200k
          ...
```

Run the whole annotated history:

```bash
python /app/scripts/full_refresh/refresh.py --select int_consensus_validators_income_daily
```

The runner iterates `(stage × month)` and emits one `dbt run` per batch with `start_month` / `end_month` and the stage's vars. Strategy flips to `append`.

!!! warning "A scoped append over an already-populated month exactly doubles the data"
    This is a backfill-into-empty tool. Marts read ReplacingMergeTree **without** `FINAL`, so both copies count. Drop the partition first, or use Mode 4, which does that for you.

### Resume on failure

Each completed batch is written to `target/refresh_state/`. Re-invoking the same command in the same container picks up where it left off. In a one-shot job that state lives on the pod's ephemeral volume, so a new Job starts from scratch — rebuild the remaining list from each model's own `max(date)` instead. A pending run must be `--resume`d or `--clear-state`d, never deleted.

### Transient retries

`Code: 241 / 159 / 209 / 210` and `MEMORY_LIMIT_EXCEEDED` / `OvercommitTracker` errors are auto-retried with exponential backoff (30s → 60s → 120s → 240s → 480s, max 5 attempts). Logs show `[transient] retry n/5 in Ns` between attempts.

### Restricting to a subset

```bash
# A single month
--start-date 2024-04-01 --end-date 2024-04-30

# A single stage
--stages validators_0_100k

# A single (stage, month)
--stages validators_0_100k --start-date 2024-04-01 --end-date 2024-04-30
```

---

## Mode 4 — Gap-window refresh (`gap_window_refresh.py`)

For the case Modes 1–3 cannot handle: an indexer backfilled rows **below** a decode model's watermark. Decode models are `append` with a literal block watermark and no lookback, so nothing that runs forward will ever see those rows. This script drops the gap-month partition (which *lowers* the watermark) and re-runs scoped.

```bash
python /app/scripts/refresh/gap_window_refresh.py \
  --select ⟨decode_model⟩+ \
  --exclude 'tag:live+' \
  --months 2026-07-01,2026-08-01,2026-09-01 \
  --state /app/target/gap_refresh_state.json \
  --full-refresh-row-cap 0 \
  --dry-run
```

Every flag is load-bearing:

- **`--dry-run` first, and read the ACTION column.** The script branches three ways. Month-partitioned models get drop + scoped re-run; any append or `delete+insert` model with no `start_month` branch gets `dbt run --full-refresh` — a full drop and rebuild, guarded only by a row cap that defaults to 5,000,000.
- **`--full-refresh-row-cap 0`** makes it skip and report those models instead of rebuilding them (`--allow-big-full-refresh` is the explicit override).
- **`--state`** is mandatory in-cluster: the default path is on the read-only image layer and the first save raises `OSError` — *after* partitions have already been dropped.
- **`--exclude 'tag:live+'`** is the correct selector; `'*_live+'` matches the wrong models.
- **`--months`** must span the gap month through the current month whenever a month boundary has been crossed, because cumulative models (the 39 that read `{{ this }}`) are wrong from the gap day forward.

Never run it on a `table`-materialized model. The full branch logic, hazards and verification queries are on [dbt reprocess after upstream repair](../../operations/runbooks/dbt-reprocess.md).

---

## Mode 5 — Refill recovery (`refill_after_price_gap.sh`)

For a Dune prices skip specifically. Two-phase by design:

```bash
/app/scripts/maintenance/refill_after_price_gap.sh --from-date 2026-04-17
```

| Phase | What | How |
| --- | --- | --- |
| 1 | For each affected month, append-rewrite every `tag:refill_append` model in DAG order, then `OPTIMIZE PARTITION '<month>' FINAL DEDUPLICATE` each one | `dbt run --select tag:refill_append --vars '{"start_month":"<m>","end_month":"<m>"}'`, then a `dbt run-operation optimize_partition_final` per model |
| 2 | Re-pull every prices descendant *not* in Phase 1 with the wider lookback | `dbt run --select int_execution_token_prices_daily+ --exclude tag:refill_append --vars '{"price_lookback_days": 12}'` |

See [Recovering from a Prices Gap](../../operations/prices-gap-recovery.md) for the full walk-through.

---

## Plain `dbt run` recipes

For ad-hoc work outside the runners. Run `context.py` first; it tells you the model's materialization and the safe lever.

### A single model with default daily behavior

```bash
dbt run --select int_execution_blocks_daily
```

### A model and everything downstream of it

```bash
dbt run --select int_execution_token_prices_daily+
```

### Full-refresh of a single incremental model (drops & rebuilds)

!!! warning "Not the fix for stale data"
    A stale model is almost always a stale *source*; a full refresh rebuilds the same gap from scratch and, on a large table, takes hours and a lot of warehouse memory. Fix the raw layer, then use the scoped lever from the decision tree. Reserve `--full-refresh` for genuinely empty or corrupt small tables.

```bash
dbt run --select int_execution_blocks_daily --full-refresh
```

### Compile only (debug the rendered SQL without writing)

```bash
dbt compile --select int_execution_tokens_balances_daily \
  --vars '{"price_lookback_days": 12}'

# Inspect target/compiled/.../<model>.sql
```

### Append-mode rewrite of a single month (the Phase-1 primitive)

Always pass **both** `start_month` and `end_month` — `start_month` alone selects append *plus* the legacy lookback window and duplicates rows.

```bash
dbt run --select int_execution_tokens_balances_daily \
  --vars '{"start_month": "2026-04-01", "end_month": "2026-04-01"}'

dbt run-operation optimize_partition_final \
  --args '{database: dbt, table_name: int_execution_tokens_balances_daily, partition: "2026-04-01"}'
```

The `OPTIMIZE` collapses any duplicates RMT would otherwise merge lazily. Run it through the macro so it is synchronous; skip it only if you don't need immediate convergence.
