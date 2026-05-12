# Quality Gates

`generate_report` runs eight enforcement rules against every report. Failing any one rejects the report with a specific, actionable message. Each rule is independently toggleable in `settings.py`.

The full ruleset lives in [`src/cerebro_mcp/prompts/agents/_shared_quality_rules.md`](https://github.com/gnosischain/cerebro-mcp/blob/main/src/cerebro_mcp/prompts/agents/_shared_quality_rules.md). Every analysis persona references this file.

## Why this exists

Without enforcement, LLM-generated reports drift toward common analytical anti-patterns:

- Aggregating stock measures over time ranges (turning TVL into a meaningless integral).
- Filtering out residual buckets without saying so.
- Computing correlations on non-stationary series.
- Double-counting aggregator volume.
- Stopping discovery at the first matching model.

Each gate maps to one of those anti-patterns. The gates are deliberately conservative — false positives are mostly harmless (the agent has to disclose or pre-aggregate), false negatives ship bad reports.

---

## The eight gates

### 1. Dimensional breakdown

**Requires:** at least one chart with `series_field`, OR a pie / treemap / heatmap / sankey.

**Why:** without a dimensional split, a report tells you only the headline number — not where it comes from.

### 2. Relational analysis

**Requires:** at least one scatter / heatmap chart, OR a correlation query (`corr`, `covarPop`, `simpleLinearRegression`).

**Why:** correlation is the cheapest way to surface joint behaviour.

### 3. Statistical query

**Requires:** at least one `quantile` / `stddev` / `corr` query.

**Why:** medians beat means on heavy-tailed on-chain data; standard deviation marks volatility.

### 4. Exploratory queries

**Requires:** at least 2 EDA queries during the run.

**Why:** rejects reports where the agent jumped straight to charts without sniffing the data.

---

### 5. `stock_flow_discipline`

**Rejects:** `SUM(tvl_usd | balance | supply | cumulative_*)` over a date range without a point-in-time constraint.

**Why:** TVL etc. are stock measures. Aggregating over time gives you "TVL × days" — not a thing.

**Fixes:**

- `argMax(col, date)` for the latest snapshot
- `WHERE date = (SELECT max(date) ...)` to constrain to one point
- Use the canonical snapshot model (`*_latest`)

### 6. `residual_bucket_disclosure`

**Rejects:** `WHERE label != ''` / `WHERE col IS NOT NULL` filters that exclude residual buckets without acknowledging the exclusion in the chart title / subtitle / description.

**Why:** the residual bucket is often huge (~30–50% of volume on Dune-labelled DEX data). Excluding it silently misleads.

**Fixes:**

- Acknowledge in subtitle: `subtitle="Excludes 32% unlabeled volume"`
- Or compute and surface the residual share alongside

### 7. `stationarity_on_correlations`

**Rejects:** `corr(x, y)` over a series with a `date` / `month` / `week` column unless the SQL or chart metadata mentions stationarity, first-differencing, Spearman, ADF, cointegration, or `lagInFrame`.

**Why:** plain `corr` over levels gives huge spurious correlations on co-trending series.

**Fixes:**

- First-difference: `corr(x - lagInFrame(x, 1), y - lagInFrame(y, 1))`
- Use Spearman: `corr(rank() OVER (ORDER BY x), rank() OVER (ORDER BY y))`
- Note ADF / cointegration in the chart description

### 8. `aggregator_volume_dedup`

**Rejects:** `SUM(volume_usd)` over `fct_execution_pools_daily` / `fct_execution_trades_by_protocol_daily` / `fct_execution_trades_by_token_daily` without a deduplication CTE or first-hop-only acknowledgment.

**Why:** aggregator orders cross multiple hops; raw `SUM(volume_usd)` double-counts every aggregator trade.

**Fixes:**

- Dedup CTE: `SELECT max(volume_usd) FROM ... GROUP BY tx_hash, log_index`
- First-hop filter: `WHERE hop_index = 0`
- Or note in the chart subtitle "first-hop-only volume"

### 9. `discovered_model_coverage`

**Rejects:** reports where any model returned by `search_models` / `discover_models` was not subsequently queried (`execute_query` / `start_query`), explored (`get_model_details`), or excluded with a stated reason via `record_model_exclusion(name, reason)`.

**Why:** a search that returns 5 candidates and you only query 2 means 3 candidates were ignored — possibly missing dimensions.

**Fixes:**

- Query each candidate
- Or explicitly: `record_model_exclusion("model_x", "snapshot model, not relevant for trend analysis")`

---

## Telemetry

| Counter | Labels | Notes |
|---|---|---|
| `cerebro_quality_gate_evaluations_total` | `gate_name`, `outcome` | Per-gate pass/fail |
| `cerebro_quality_report_generations_total` | `report_kind`, `outcome` | Overall report acceptance |
| `cerebro_discovered_model_coverage_total` | `coverage_kind` | `queried` / `excluded` / `unused` |

The `quality_metrics` MCP tool returns a markdown summary of in-process counts. For long-window analysis scrape `/metrics`.

## Toggling

Each gate has its own boolean in `settings.py`:

| Setting | Default |
|---|---|
| `QUALITY_GATE_DIMENSIONAL_BREAKDOWN` | True |
| `QUALITY_GATE_RELATIONAL_ANALYSIS` | True |
| `QUALITY_GATE_STATISTICAL_QUERY` | True |
| `QUALITY_GATE_EXPLORATORY_QUERIES` | True |
| `QUALITY_GATE_STOCK_FLOW_DISCIPLINE` | True |
| `QUALITY_GATE_RESIDUAL_BUCKET_DISCLOSURE` | True |
| `QUALITY_GATE_STATIONARITY_ON_CORRELATIONS` | True |
| `QUALITY_GATE_AGGREGATOR_VOLUME_DEDUP` | True |
| `QUALITY_GATE_DISCOVERED_MODEL_COVERAGE` | True |

Disable individually if you have a strong reason. The gates are conservative; turning them off lets bad reports through.

## Best practices

- **Treat gate failure as a real failure.** Don't paper over a stock/flow gate by changing the column name — fix the SQL.
- **Pre-aggregate before checking.** Most gate failures (stock/flow, aggregator dedup) come from forgetting to compress the data first.
- **Explain residual exclusions in chart subtitles** — the gate accepts the disclosure verbatim.

## See also

- [Reports](../reports.md) — `generate_report` overview
- [Hybrid Search](hybrid-search.md) — what `search_models` returns (drives `discovered_model_coverage`)
- [`_shared_quality_rules.md` (cerebro-mcp)](https://github.com/gnosischain/cerebro-mcp/blob/main/src/cerebro_mcp/prompts/agents/_shared_quality_rules.md) — the canonical ruleset
