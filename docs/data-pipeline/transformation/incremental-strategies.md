---
title: Incremental Strategies
description: How dbt-cerebro models advance over time — daily catch-up, microbatch slicing, full-refresh batching, and recovery rewrites
---

# Incremental Strategies

Most `int_*` models in dbt-cerebro are incrementally materialized: each run only writes the rows that have changed since the last run. The rest of this page explains the four invocation modes that the same model supports, when each fires, and how a single config expression routes between them.

## The four invocation modes

A typical `int_*` model accepts the same model SQL but behaves differently depending on which dbt vars are set when you run it.

| Mode | Vars set | Strategy | Window written | Used by |
| --- | --- | --- | --- | --- |
| **Daily incremental** | _none_ | `delete+insert` | `[max(date) − N + 1, max(date)]` (lookback) | Cron / `dbt run` |
| **Microbatch slice** | `incremental_end_date` | `append` | `(max(date), incremental_end_date]` (no overlap) | `scripts/refresh/dbt_incremental_runner.py` |
| **Full-refresh month** | `start_month` + `end_month` | `append` | All rows in `[start_month, end_month]` | `scripts/full_refresh/refresh.py` |
| **Refill recovery** | `start_month` + `end_month` (often single month) followed by `OPTIMIZE PARTITION FINAL` | `append` | One full month, idempotent | `scripts/maintenance/refill_after_price_gap.sh` |

The four modes share one config expression on the model:

```python
{{
  config(
    materialized='incremental',
    incremental_strategy=(
      'append'
      if (var('start_month', none) or var('incremental_end_date', none))
      else 'delete+insert'
    ),
    engine='ReplacingMergeTree()',
    unique_key='(date, ...)',
    partition_by='toStartOfMonth(date)',
    ...
  )
}}
```

`append` whenever either runner is driving (no mutation, fixed cost regardless of window width); `delete+insert` for plain daily runs (small window, ALTER TABLE DELETE is cheap).

The actual filter is produced by the macro `apply_monthly_incremental_filter` (defined in `dbt-cerebro/macros/db/get_incremental_filter.sql`) — see below.

## How `apply_monthly_incremental_filter` routes the modes

```jinja
{{ apply_monthly_incremental_filter('date', 'date', true) }}
```

The macro produces one of two WHERE clauses:

=== "Microbatch path (`incremental_end_date` set)"

    ```sql
    AND toDate(date) > (
      SELECT coalesce(max(toDate(x1.date)), toDate('1970-01-01'))
      FROM {{ this }} AS x1
    )
    AND toDate(date) <= toDate('2026-04-21')
    ```

    Strict greater-than on `max(date)` and less-than-or-equal on the runner-supplied upper bound. Each slice writes only strictly-new dates → no duplicates produced → no OPTIMIZE needed.

=== "Default daily path (no var)"

    ```sql
    AND toStartOfMonth(toDate(date)) >= (
      SELECT toStartOfMonth(addDays(max(toDate(x1.date)), -N))
      FROM {{ this }} AS x1
    )
    AND toDate(date) >= (
      SELECT addDays(max(toDate(x2.date)), -N) FROM {{ this }} AS x2
    )
    ```

    Re-pulls the last `N` days under `delete+insert`, with `N = lookback_days - 1`. The default `N` is per-model (`lookback_days=1` or `2`); a global override is available via `var('price_lookback_days', N)`.

The `start_month`/`end_month` branch is **not** in the macro — each model writes it inline, because the filter applies to the *source* (not `{{ this }}`):

```jinja
{% if start_month and end_month %}
  AND toStartOfMonth(date) >= toDate('{{ start_month }}')
  AND toStartOfMonth(date) <= toDate('{{ end_month }}')
{% else %}
  {{ apply_monthly_incremental_filter('date', 'date', true) }}
{% endif %}
```

## The `refill_append` tag

Some intermediate models perform heavy aggregations (`countDistinct`, window functions, large GROUP BYs) that OOM under `delete+insert` when the lookback window is wide. Recovery for those models must use append-mode whole-month rewrites, not lookback. They carry the `refill_append` tag.

```python
tags=['production', 'execution', 'tokens', 'balance_cohorts_daily', 'refill_append']
```

Heavy `refill_append` models also need a memory contract — pre-hooks that cap memory and force GROUP BY / sort to spill to disk. The shared macro `refill_safe_pre_hook` (defined in `dbt-cerebro/macros/db/refill_safe_hooks.sql`) provides the standard block:

```python
{{ config(
    ...
    pre_hook=refill_safe_pre_hook(),
    post_hook=refill_safe_post_hook(),
    tags=[..., 'refill_append'],
) }}
```

What the macro emits:

```sql
-- pre_hook
SET max_memory_usage = 8000000000;
SET max_bytes_before_external_group_by = 2000000000;
SET max_bytes_before_external_sort = 2000000000;
SET join_algorithm = 'grace_hash';
-- post_hook resets all four to defaults
```

ClickHouse Cloud has a hard ~10.8 GiB per-query cap. Without spill thresholds, a wide GROUP BY trips OvercommitTracker → `Code: 241 — MEMORY_LIMIT_EXCEEDED`. With them, the hash table spills at 2 GiB and the run completes.

## Choosing a mode when you author a model

| You're writing | Use this contract |
| --- | --- |
| Lightweight `int_*` with a small daily window | `delete+insert` only; default `apply_monthly_incremental_filter` lookback |
| `int_*` whose daily volume is large enough that mutations are painful | Add the three-branch `incremental_strategy` expression so the runner can drive it in `append` mode |
| `int_*` with heavy aggregation (cohorts, supply distributions, distinct counts over a month) | Three-branch strategy + `refill_append` tag + `refill_safe_pre_hook()` / `refill_safe_post_hook()` |
| `fct_*` table (full rebuild each run) | `materialized='table'` — none of the incremental machinery applies |

See [Running Models](running-models.md) for end-to-end examples of each mode in action, and [Recovering from a Prices Gap](../../operations/prices-gap-recovery.md) for the refill flow.
