# Metric registry

The metric registry is the **named, versioned interface** that AI
agents, dashboards, and downstream tools talk to. It lives in
`target/semantic_registry.json` (compiled from
`semantic/authoring/<module>/semantic_models.yml` files) and is served
remotely via GitHub Pages so the MCP can refresh from it.

This page is about how to **use** the registry. Authoring is covered in
[architecture](architecture.md); operational discipline is covered in
[maintenance](maintenance.md).

## Quality tiers

Every metric and every semantic_model has a `quality_tier`:

| Tier | Meaning | Visibility |
| --- | --- | --- |
| `approved` | Analyst-reviewed, stable contract, ready for production consumers. | Returned by `discover_metrics`. Executable by `query_metrics` without opt-in. |
| `candidate` | Authored but not yet vetted. Useful for documentation / drafting. | Hidden from `discover_metrics`. `query_metrics` rejects unless caller passes `allow_candidate=true`. |
| `blocked` | Explicitly excluded from the registry (e.g. for privacy reasons). | Removed from the registry entirely. |

The gate is **three-part** (cerebro-mcp `_metric_is_executable`):

```python
return (
    metric.quality_tier == "approved"
    and metric.semantic_status == "approved"
    and root_model.semantic_status == "approved"
)
```

All three must hold. Common gotcha: you set the metric to `approved` but
forget the underlying semantic_model. Result: the metric appears in
`discover_metrics` but `query_metrics` rejects it. See
[maintenance](maintenance.md#promotion-checklist) for the promotion
sequence.

## The four MCP tools

### `discover_metrics`

Free-text search over the metric registry. Returns ranked metric metadata
without executing anything.

```python
mcp__cerebro-dev__discover_metrics(query="bridge volume 7d")
```

Returns:

```json
{
  "results": [
    {"name": "bridge_volume_7d", "label": "...", "score": 150, ...},
    {"name": "cow_volume_usd", "label": "...", "score": 47, ...}
  ]
}
```

Scoring (cerebro-mcp `semantic_index.score_metric`):

- **100** — query exactly equals the metric name.
- **90** — query exactly equals a synonym.
- **50** — metric name starts with the query.
- **25** — query is a substring of the metric's search blob (name +
  label + description + synonyms).
- **+ idf-weighted token bonus** — per matched token, weighted by how
  rare the token is across all metrics' search blobs. Capped per token
  so it can't outscore the 90/100 shortcut paths.
- **+ 20** — metric is `approved`.
- **+ 15** — query mentions a module name (`execution`, `consensus`,
  `bridges`, ...) and the metric belongs to it.

The idf weighting (introduced in cerebro-mcp PR 6) means rare tokens
like `passkey` score higher than generic ones like `weekly`. Useful for
keeping discovery noise-free.

Only `approved` metrics show up. To find a candidate metric, you need
to know its name and use `get_metric_details`.

### `get_metric_details`

Inspect a specific metric (even if not approved).

```python
mcp__cerebro-dev__get_metric_details(metric_name="cow_volume_usd")
```

Returns the full metadata: root model, allowed dimensions, supported
time grains, synonyms, description.

### `query_metrics`

Execute the metric. Returns a result set + the compiled SQL.

```python
mcp__cerebro-dev__query_metrics(
    metrics=["cow_volume_usd", "lending_deposits_volume_weekly"],
    dimensions=["week"],
    filters=[{"column": "protocol", "operator": "=", "value": "Aave V3"}],
    order_by=["week DESC"],
    limit=12,
)
```

Filter shape supports both `column`/`operator` (public API) and
`field`/`op` (internal) keys interchangeably — cerebro-mcp PR 1 fixed a
filter-rendering bug that produced malformed `WHERE = 'val'` SQL when
the key shape didn't match. Filters now raise on unknown fields with a
helpful "valid fields: [...]" message.

Five planner modes (cerebro-mcp `semantic_planner.plan_metric_query`):

| Mode | When | Emits |
| --- | --- | --- |
| `single_model` | All metrics share one root, dimensions all local. | Simple `SELECT ... FROM <root> GROUP BY ...`. |
| `enriched_single_model` | One root, some dimensions reached through a relationship. | Single SELECT with `LEFT JOIN` chain for the remote dimensions. |
| `multi_branch_aggregate_join` | Metrics span multiple roots, sharing a dimension. | Branch CTEs per root + `UNION DISTINCT` of keys + `LEFT JOIN`. |
| `unsupported` | Planner can't find a valid path. | Returns a structured error explaining what's reachable. |

The planner also synthesises **time-spine upcasts** when a coarse-grain
dimension (e.g. `week`) is requested against a fine-grain metric (e.g.
daily). See [time spines](time-spines.md).

### `reload_semantic_registry`

Admin tool. Forces a refresh of the runtime's cached registry, bypassing
the 300s ETag-based poll. Use during authoring loops:

```python
mcp__cerebro-dev__reload_semantic_registry()
# → {"changed": true,
#    "registry_hash_before": "...", "registry_hash_after": "...",
#    "manifest_hash_before": "...", "manifest_hash_after": "...",
#    "catalog_hash_before": "...", "catalog_hash_after": "...",
#    "metric_count": 1037, "approved_metric_count": 72}
```

Returns the hash delta and count summary so the caller can verify the
refresh actually picked up new content. As of the cerebro-mcp sync fix,
a force reload refreshes **all four artifacts together** (registry +
docs + manifest + catalog), so the returned manifest/catalog hashes
let you confirm a post-deploy mismatch is fully cleared in a single
call — see [maintenance → stale registry](maintenance.md#drift-modes-what-to-watch-for).

## Candidate-metric opt-in for authoring

When iterating on a new metric, you don't want to flip `quality_tier:
approved` just to test the SQL — analyst review hasn't happened yet.
Pass `allow_candidate=true`:

```python
mcp__cerebro-dev__query_metrics(
    metrics=["my_new_draft_metric"],
    dimensions=["week"],
    allow_candidate=True,
)
```

This bypasses the `quality_tier` gate but keeps the structural checks
(the root model must still be approved, and the metric must have at
least one `allowed_dimension`). Never use in production dashboards —
the caller is explicitly opting out of the contract.

## Scalar-KPI metrics

A scalar KPI is a metric whose underlying view is a **single-row**
output — typically `api_*_kpi_*_latest` views that return one value +
maybe a `change_pct` for a dashboard card. These have **no
`allowed_dimensions`** because there's nothing to group by.

The semantic planner can't usefully handle these — there's no aggregate
to compose. Calling `query_metrics` on a scalar KPI returns a dedicated
error message:

```
Error: Metric 'bridge_volume_7d' is a scalar / single-row KPI
(no `allowed_dimensions` declared). The semantic planner has nothing
to group by. Query the underlying view directly with `execute_query`
on `api_bridges_kpi_volume_7d`.
```

These metrics still appear in `discover_metrics` for documentation —
they tell agents that a KPI exists and where to find it. They're just
fetched directly via `execute_query` rather than `query_metrics`.

(This dedicated error path was added in cerebro-mcp PR 3; the previous
behaviour returned the misleading "not approved" message.)

## Patterns: choosing the right tool

Decision flow when an agent has an analytics question:

```
┌────────────────────────────────────────────────┐
│ Agent receives analytics question              │
└────────────────────┬───────────────────────────┘
                     ▼
┌────────────────────────────────────────────────┐
│ preflight_analytics_request(query, mode)       │
│ → suggests metrics + coverage assessment       │
└────────────────────┬───────────────────────────┘
                     ▼
       ┌─────────────┴─────────────┐
       │ All topics covered?       │
       └─────────────┬─────────────┘
                     ▼
            ┌────────┴────────┐
            ▼                 ▼
       YES                   NO
            │                 │
            ▼                 ▼
   discover_metrics    Fall back to:
            │             - search_models / discover_models
            ▼             - describe_table / get_model_details
   query_metrics         - execute_query
                            (use_clickhouse_query_rules for hygiene)
```

The hybrid path is the norm — most real analytics questions touch
*some* registered metrics and *some* fields that need raw access (free-
form filters, scatter plots, correlation matrices, ad-hoc joins).

## What's in the registry today

The registry now carries **~1,037 metrics** (~72 `approved`, ~965
`candidate`) across ~1,095 semantic-mapped models and 51 cross-sector
relationships. The jump from the original hand-authored ~70 metrics is
deliberate: `scripts/semantic/scaffold_metrics.py` emits **one candidate
metric for every eligible measure** across all 26 authoring domains, so
no measure is invisible to `discover_metrics` / `query_metrics` just
because nobody hand-wrote a metric for it.

Practical consequences:

- **`discover_metrics` is unchanged in feel.** It only surfaces
  `approved` metrics, so the ~965 auto-generated candidates don't add
  noise — you reach them by name via `get_metric_details` or with
  `allow_candidate=true`.
- **Promotion is the curation step.** A candidate becomes a first-class,
  discoverable metric only when an analyst reviews it and flips both the
  metric and its root model to `approved` (see the
  [promotion checklist](maintenance.md#promotion-checklist)).
- **Measure names are globally unique** — a hard prerequisite for
  binding a metric to every measure. The scaffolder enforces this; see
  [maintenance invariant #1](maintenance.md#1-measure-names-are-globally-unique).

Run-time count from the most recent build:

```bash
python3 -c "import json; r = json.load(open('target/semantic_registry.json')); \
            print('metrics:', len(r['metrics']),
                  '  approved:', sum(1 for m in r['metrics'].values()
                                     if m['quality_tier'] == 'approved'))"
```

See the [semantic graph](graph.md) for the auto-generated current state
(now an interactive cytoscape explorer with a static-Mermaid fallback).

## Adding a new metric

See [maintenance](maintenance.md#authoring-checklist) for the full
checklist. The three things that bite if you skip them:

1.  **Measure names must be globally unique.** Use `<metric_name>_value`
    convention. Two `value_value` measures in two semantic_models is an
    error caught by `validate_registry` *once a metric references them*.
    `scripts/semantic/scaffold_metrics.py` enforces this automatically:
    it rewrites only collided names (to `<semantic_model>__<measure>`)
    and emits a candidate metric for every eligible measure, so a
    measure without a metric should not exist. Re-run it after adding
    measures rather than hand-authoring the metric block.
2.  **The root semantic_model's `quality_tier` must be approved too.**
    Promoting only the metric leaves the root candidate and the metric
    becomes silently unqueryable.
3.  **`allowed_dimensions` must list every dimension a caller might
    pass.** A `dimension is not supported` error from the planner is
    almost always a missing entry here.
