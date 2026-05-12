# Semantic Metrics

When to use `query_metrics` (the semantic catalogue) vs `execute_query` (raw SQL).

## What it is

Cerebro ships a semantic registry — a curated catalogue of pre-defined metrics with validated SQL, dimensional rules, and quality tiers. `query_metrics(metric, dims, range)` looks up a metric by name and runs the canonical query, instead of letting you author SQL from scratch.

Backed by `dbt-cerebro` semantic YAML; the registry is reloaded periodically and metrics are tagged by quality tier (approved / candidate / experimental).

## When to use it

| Use `query_metrics` when… | Use `execute_query` when… |
|---|---|
| The metric exists in `discover_metrics` | No semantic metric matches |
| You want pre-validated dimensional rules | You're prototyping a new metric |
| You're being graded by the [quality gates](quality-gates.md) — semantic metrics auto-satisfy several | You need an aggregation the registry doesn't expose |
| You want consistent answers across users | One-off calculation that won't recur |

The semantic layer also feeds [Metric Lab](../mini-apps/metric-lab.md) and `quick_metric_chart` — both let you iterate on a metric visually without writing SQL.

## Step-by-step tutorial

### 1. Discover available metrics

```text
discover_metrics(filters={"sector": "dex"})
# Returns metric names + descriptions + dims + quality_tier

get_metric_details(metric_name="dex_daily_volume")
# Full spec: SQL, dimensions, expected ranges, freshness
```

### 2. Run a metric

```text
query_metrics(
  metric_name="dex_daily_volume",
  dims=["protocol"],
  range_days=90,
)
```

Returns the same shape as `execute_query` but with metric metadata attached.

### 3. Chart directly

```text
quick_metric_chart(
  metric_name="dex_daily_volume",
  dims=["protocol"],
  chart_type="area",
  series_field="protocol",
  stack=True,
)
```

Or batch via `generate_metric_charts(specs=[...])`.

## Worked example

Comparing semantic vs raw for the same question — "DEX volume by protocol over the last quarter":

### Semantic

```text
> discover_metrics(filters={"name_contains": "dex_volume"})
< | name | description | dims | quality_tier |
  | dex_daily_volume | Daily DEX volume by protocol | protocol, token | approved |

> query_metrics(metric_name="dex_daily_volume", dims=["protocol"], range_days=90)
< [Result with metric metadata: dedup applied, residual handled, etc.]
```

### Raw

```text
> describe_table("dbt.fct_execution_pools_daily")
> execute_query("""
    SELECT date, protocol, sum(volume_usd) AS volume
    FROM dbt.fct_execution_pools_daily
    WHERE date >= today() - 90
    GROUP BY 1, 2
  """)
< [Quality gate REJECT: aggregator_volume_dedup — fct_execution_pools_daily needs dedup CTE]

# Have to fix:
> execute_query("""
    WITH dedup AS (
      SELECT tx_hash, log_index, max(volume_usd) AS volume_usd, protocol, date
      FROM dbt.fct_execution_pools_daily
      WHERE date >= today() - 90
      GROUP BY 1, 2, 4, 5
    )
    SELECT date, protocol, sum(volume_usd) AS volume FROM dedup GROUP BY 1, 2
  """)
```

The semantic metric encodes the dedup. The raw path requires you to remember.

## Tool reference

| Tool | Purpose |
|---|---|
| `discover_metrics(filters?)` | Browse the catalogue |
| `get_metric_details(metric_name)` | Full spec for a metric |
| `query_metrics(metric_name, dims, range)` | Run the canonical query |
| `quick_metric_chart(...)` | Run + render in one call |
| `generate_metric_charts(specs=[...])` | Batch-render multiple metrics |
| `discover_dashboard_metrics(dashboard)` | Per-dashboard inventory |
| `open_metric_lab_from_metrics(metric_name, ...)` | Iterate visually |
| `explain_metric_query(metric_name, ...)` | EXPLAIN the underlying SQL |

## Best practices

- **Always check `discover_metrics` first** before writing raw SQL. Saves time and helps the [`discovered_model_coverage` gate](quality-gates.md#9-discovered_model_coverage).
- **`approved` > `candidate` > `experimental`.** Pick the highest tier that satisfies the question.
- **Use `quick_metric_chart`** for one-shot visualisations — no SQL authoring.
- **Promote a recurring raw query** to a semantic metric (open a PR on `dbt-cerebro`) once you've reused it three times.

## Pitfalls

- **Treating `experimental` metrics as canonical.** They exist for prototyping; numbers may shift.
- **Filtering inside the metric SQL by editing it directly.** The metric is the canonical query — for filters, use `dims` and `range`, not SQL surgery.
- **Bypassing `query_metrics` because the dimensions don't quite match.** File a request to extend the metric instead of forking it via raw SQL.

## See also

- [Mini-Apps → Metric Lab](../mini-apps/metric-lab.md) — visual iteration
- [Tools §2](../tools.md#2-query-execution) — `query_metrics`, `execute_query`
- [Quality Gates](quality-gates.md) — semantic metrics auto-satisfy several gates
- [`dbt-cerebro` semantic YAML](https://github.com/gnosis-org/dbt-cerebro/tree/main/semantic) — where metrics are authored
