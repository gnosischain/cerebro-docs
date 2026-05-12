# Metric Lab

Two-pane workspace for drafting metrics. Left: source (raw SQL, semantic registry lookup, or model browser). Right: live chart + table with editable spec.

## What it is

Metric Lab is the prototyping surface for charts and metrics. You can:

1. Paste raw SQL.
2. Pick a metric from the semantic registry (`fct_*`, `api_*`, `metric_*`).
3. Browse models and click columns into the editor.

The right pane renders the result as a chart and a table; both update as you tweak the SQL or chart spec. Once you have what you want, save it via `save_query` or promote it to a `generate_chart` call for inclusion in a report.

Resource URI: `ui://cerebro/metric_lab`.

## When to use it

- Iterating on a metric before committing to a report.
- Prototyping a chart with multiple chart types ("does this read better as line or area?").
- Promoting an ad-hoc query to a saved query / scheduled chart.
- Teaching: pasting a query and walking through the columns.

For one-shot chart generation without iteration, use `quick_chart` directly.

## Step-by-step tutorial

### 1. Open from SQL

```text
open_metric_lab_from_sql(
  sql="""
    SELECT date, sum(volume_usd) AS volume
    FROM dbt.fct_execution_pools_daily
    WHERE date >= today() - 90
    GROUP BY date
    ORDER BY date
  """,
  chart_type="line",
)
```

### 2. Open from a registered metric

```text
open_metric_lab_from_metrics(
  metric_name="dex_daily_volume",
  dims=["protocol"],
  range_days=90,
)
```

### 3. Open from a model browser seed

```text
open_metric_lab(seed_model="fct_execution_pools_daily")
```

### 4. Iterate

```text
load_metric_lab_metric(metric_name="dex_daily_volume_by_token")
update_metric_lab_chart(chart_type="area", series_field="protocol", stack=True)
```

## Tool reference

| Tool | Purpose |
|---|---|
| `open_metric_lab(seed_model?)` | Open the panel; optionally pre-pick a model |
| `open_metric_lab_from_sql(sql, chart_type?)` | Open seeded with SQL |
| `open_metric_lab_from_metrics(metric_name, dims?, range_days?)` | Open seeded with a registered metric |
| `load_metric_lab_metric(metric_name)` | Swap the right pane to a different metric |
| `update_metric_lab_chart(...)` | Change chart_type, series_field, stack, sort, ... |

## Worked example

```text
> open_metric_lab_from_sql(
    sql="SELECT date, protocol, sum(volume_usd) AS volume FROM dbt.fct_execution_pools_daily WHERE date >= today() - 90 GROUP BY 1, 2",
    chart_type="line",
  )
# pane shows a flat-overlapping line chart — hard to read

> update_metric_lab_chart(chart_type="area", series_field="protocol", stack=True)
# now stacked area; volume share by protocol, daily

# happy with it — save and promote
> save_query(name="dex_volume_stacked_90d", sql="...")
> generate_chart(spec={...})  # for a report
```

## Best practices

- **Start from the semantic registry** (`open_metric_lab_from_metrics`) when one exists — semantics are pre-validated, no risk of column hallucination.
- **Use `update_metric_lab_chart` aggressively.** Chart-type matters more than the SQL: the same data tells different stories as line vs area vs scatter.
- **Save before promoting.** A `save_query` lets you replay; `generate_chart` produces a chart_id for a single report.

## Pitfalls

- **Editing SQL in the right pane that uses `WHERE date != ''`** without acknowledging in the chart subtitle — the [residual-bucket gate](../advanced/quality-gates.md) will reject the report.
- **Forgetting `series_field` when you have a category dimension.** A line chart of multi-protocol data without `series_field` plots one line for everything.
- **Hitting the row cap** (`MAX_ROWS=10000`). Pre-aggregate in the SQL.

## See also

- [Mini-Apps overview](index.md)
- [Semantic Metrics](../advanced/semantic-metrics.md) — `query_metrics` vs raw SQL
- [Reports](../reports.md) — how to take a Metric Lab chart to a report
