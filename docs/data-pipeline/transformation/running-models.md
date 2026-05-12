---
title: Running Models
description: How to run dbt-cerebro models — daily cron, microbatch catch-up, full-refresh batching, and on-demand commands
---

# Running Models

There are three runners that drive dbt-cerebro models in production, plus the plain `dbt run` command for ad-hoc work. This page walks through each one with concrete examples.

If you haven't read [Incremental Strategies](incremental-strategies.md) yet, do so first — it explains why the same model behaves differently across these runners.

## TL;DR

| Goal | Command |
| --- | --- |
| Run a single model right now (default daily-incremental behavior) | `docker exec dbt dbt run --select <model> --project-dir /app --profiles-dir /app` |
| Bring an annotated incremental model up to today via per-day slices | `docker exec dbt python /app/scripts/refresh/dbt_incremental_runner.py --select <model>` |
| Backfill a model month-by-month from its declared start date | `docker exec dbt python /app/scripts/full_refresh/refresh.py --select <model>` |
| Recover after the prices source skipped a day | `docker exec dbt /app/scripts/maintenance/refill_after_price_gap.sh --from-date YYYY-MM-DD` |

---

## Mode 1 — Daily cron (`run_dbt_observability.sh`)

The production cron runs `scripts/run_dbt_observability.sh`, which delegates each batch to `scripts/refresh/dbt_incremental_runner.py`. For models with no microbatch annotation, the runner falls back to plain `dbt run --select <batch>` with no vars set — that triggers the **daily incremental** mode (`delete+insert` over the macro's lookback).

You don't normally invoke this manually. To reproduce a single batch the cron would run:

```bash
docker exec dbt dbt run \
  --select int_execution_blocks_daily \
  --project-dir /app --profiles-dir /app
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

The mutation deletes the previous version of the rewritten dates so RMT doesn't have to dedupe. Cheap on small daily windows; expensive on large windows (which is why the next two modes exist).

---

## Mode 2 — Microbatch runner (`dbt_incremental_runner.py`)

For models tagged `microbatch` (and configured in `meta.full_refresh.incremental` in their `schema.yml`), the runner slices the gap between `max(target_date)` and today into per-day windows.

```bash
docker exec dbt python /app/scripts/refresh/dbt_incremental_runner.py \
  --select int_consensus_validators_income_daily \
  --project-dir /app --profiles-dir /app
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

### Common runner flags

| Flag | Effect |
| --- | --- |
| `--select <selector>` | Same syntax as `dbt run`; supports `+`, `tag:`, `path:` |
| `--max-end-date YYYY-MM-DD` | Cap slicing at this date (otherwise stops at today) |
| `--max-slices-per-stage N` | Refuse if the gap is longer than N days (default 30) — large gaps should go through Mode 3 |
| `--dry-run` | Print the slice plan, no DB writes |
| `--resume` | Skip slices already completed in `target/incremental_microbatch_state.json` |

### When the runner refuses

```
gap is 615 day(s); exceeds --max-slices-per-stage=30
```

The microbatch path is for daily catch-up, not historical backfill. For long gaps, run [Mode 3](#mode-3) once to fill the hole, then microbatch resumes naturally on the next cron tick.

---

<a id="mode-3"></a>

## Mode 3 — Full-refresh batched (`full_refresh.py`)

For historical backfill, monthly batches are the right granularity. Each model declares its history under `meta.full_refresh` in `schema.yml`:

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
docker exec dbt python /app/scripts/full_refresh/refresh.py \
  --select int_consensus_validators_income_daily \
  --project-dir /app --profiles-dir /app
```

The runner iterates `(stage × month)` and emits one `dbt run` per batch with `start_month` / `end_month` and the stage's vars. Strategy flips to `append`.

### Resume on failure

Each completed batch is written to `target/full_refresh_state.json`. Re-invoking the same command picks up where it left off.

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

## Mode 4 — Refill recovery (`refill_after_price_gap.sh`)

For incidents — a Dune prices skip, an upstream backfill, a model that drifted out of sync. Two-phase by design:

```bash
docker exec dbt /app/scripts/maintenance/refill_after_price_gap.sh \
  --from-date 2026-04-17
```

| Phase | What | How |
| --- | --- | --- |
| 1 | For each affected month, append-rewrite every `tag:refill_append` model in DAG order, then `OPTIMIZE PARTITION '<month>' FINAL DEDUPLICATE` each one | `dbt run --select tag:refill_append --vars '{"start_month":"<m>","end_month":"<m>"}'`, then a `dbt run-operation optimize_partition_final` per model |
| 2 | Re-pull every prices descendant *not* in Phase 1 with the wider lookback | `dbt run --select int_execution_token_prices_daily+ --exclude tag:refill_append --vars '{"price_lookback_days": 12}'` |

See [Recovering from a Prices Gap](../../operations/prices-gap-recovery.md) for the full walk-through.

---

## Plain `dbt run` recipes

For ad-hoc work outside the runners.

### A single model with default daily behavior

```bash
docker exec dbt dbt run \
  --select int_execution_blocks_daily \
  --project-dir /app --profiles-dir /app
```

### A model and everything downstream of it

```bash
docker exec dbt dbt run \
  --select int_execution_token_prices_daily+ \
  --project-dir /app --profiles-dir /app
```

### Full-refresh of a single incremental model (drops & rebuilds)

Avoid for large incremental tables — prefer Mode 3, which batches the rebuild into months.

```bash
docker exec dbt dbt run \
  --select int_execution_blocks_daily --full-refresh \
  --project-dir /app --profiles-dir /app
```

### Compile only (debug the rendered SQL without writing)

```bash
docker exec dbt dbt compile \
  --select int_execution_tokens_balances_daily \
  --vars '{"price_lookback_days": 12}' \
  --project-dir /app --profiles-dir /app

# Inspect target/compiled/.../<model>.sql
```

### Append-mode rewrite of a single month (the Phase-1 primitive)

```bash
docker exec dbt dbt run \
  --select int_execution_tokens_balances_daily \
  --vars '{"start_month": "2026-04-01", "end_month": "2026-04-01"}' \
  --project-dir /app --profiles-dir /app

docker exec dbt dbt run-operation optimize_partition_final \
  --args '{database: dbt, table_name: int_execution_tokens_balances_daily, partition: "2026-04-01"}' \
  --project-dir /app --profiles-dir /app
```

The `OPTIMIZE` collapses any duplicates RMT would otherwise merge lazily. Skip it if you don't need immediate convergence — background merges will eventually do the same work.
