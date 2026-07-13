# Model Lineage

Interactive, dbt-Explorer-style view over the dbt model DAG. The backend hydrates a per-view dataset (nodes / edges / column edges) from the manifest lineage graph and the semantic registry; a React Flow front end renders it with click-to-expand, a layer toggle (physical model DAG vs. semantic join graph), and a column-lineage drawer.

- **Resource URI:** `ui://cerebro/model_lineage`
- **Entry tool:** `open_model_lineage(seed_model?, direction="both", depth=1, layer="model")`
- **Backed by:** `src/cerebro_mcp/tools/analytics/model_lineage_app.py` + `src/cerebro_mcp/loaders/column_lineage.py`

## When to use it

Use Model Lineage when you want to **see** how models relate rather than list them:

- "What feeds `fct_execution_transactions_daily`, and what breaks if I change it?"
- "Walk the DAG outward from this staging model, one hop at a time."
- "Which upstream column does `volume_usd` actually come from?"
- "Show me the approved semantic join relationships around this mart."

For a non-visual answer, the plain lineage tools are cheaper: `get_upstream_lineage` / `get_downstream_impact` for transitive sets, `get_model_subgraph` for a bounded JSON subgraph, and `get_column_lineage` for column edges without the UI.

## Entry points

| Tool | What it does |
|---|---|
| `open_model_lineage(seed_model?, direction, depth, layer, title?)` | Opens the panel. With a `seed_model`, loads the bounded lineage subgraph around it; without one, opens a searchable catalog of every model as a start screen. `layer="model"` renders the physical dbt DAG; `layer="semantic"` renders approved semantic-registry join relationships. |
| `expand_model_lineage_node(view_id, node_id, direction, depth)` | Expands the graph one hop around `node_id` and merges the result in (deduplicated). Source nodes (`source.*`) are leaf inputs and are focused, not expanded. |
| `set_model_lineage_filters(view_id, direction?, depth?, include_kinds?, tags?, layer?)` | Re-runs the subgraph from the current seed with new filters or a different layer. |
| `load_column_lineage(view_id, model_name, column, direction="upstream", depth=1)` | Computes column-level lineage and loads it into the column drawer. |

Depth is capped at 5 per request; expansion merges into the existing view, so you can grow the graph incrementally.

## Column-level lineage

dbt's `manifest.json` has model-to-model edges but no column-to-column edges. Cerebro derives them **on demand** by parsing each model's SQL with sqlglot (ClickHouse dialect) and resolving which source columns a target column depends on. Manifests that only carry Jinja `raw_sql` are best-effort rendered (`ref`/`source`/`this` rewritten to physical relations). Heavy macro-generated SQL can defeat the parser — in that case the drawer degrades gracefully to a model-level edge plus a warning instead of failing.

## Typical flow

```text
> Where does api_bridges_flows_daily get its data?
agent calls open_model_lineage(seed_model="api_bridges_flows_daily", direction="upstream", depth=2)
→ panel renders the upstream DAG

> Expand around the int_bridges_flows model
agent calls expand_model_lineage_node(view_id="…", node_id="model.gnosis_dbt.int_bridges_flows_daily")

> Trace the amount_usd column
agent calls load_column_lineage(view_id="…", model_name="api_bridges_flows_daily", column="amount_usd")
→ column drawer shows the source columns per level
```

## Limits

- **Depth cap:** 5 hops per open/expand call.
- **Semantic layer needs the registry.** `layer="semantic"` requires a loaded semantic registry snapshot; otherwise the view warns and stays empty.
- **Column lineage is per-column, not precomputed.** Each drawer load parses SQL on demand; expect a warning (not a failure) on macro-heavy models.

## See also

- [Data Catalog](data-catalog.md) — search-first entity profiles, including a lineage tab backed by the same subgraph
- [Graph Explorer](graph-explorer.md) — cross-sector data graph (rows, not models)
- [Hybrid Search](../advanced/hybrid-search.md) — how model discovery ranks candidates before you visualise them
