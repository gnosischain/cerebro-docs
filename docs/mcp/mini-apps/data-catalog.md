# Data Catalog

An OpenMetadata-style, search-first catalog over everything the semantic registry knows about: dbt models, semantic metrics, and knowledge-graph glossary terms. One ranked, faceted search leads to per-entity profile pages (schema, properties, lineage, metrics, relationships), plus a governance view and an Elementary-backed observability dashboard.

- **Resource URI:** `ui://cerebro/data_catalog`
- **Entry tool:** `open_data_catalog(query?, entity?, entity_type="model")`
- **Backed by:** `src/cerebro_mcp/tools/semantic/data_catalog.py` (registry-native; a cached BM25 index over the registry snapshot powers search)

## When to use it

Use the Data Catalog when the question is about the **data platform itself** rather than the data:

- "What models / metrics exist around bridges?"
- "Show me everything about `fct_execution_gpay_kpi_daily` — columns, owner, tier, lineage, tests."
- "Is this table fresh? Did its last dbt run succeed?"
- "What does the glossary say `active user` means here?"

For pure model discovery in an analytical flow, `search_models` / `discover_models` (or the `find` router) are the shorter path.

## Entry points

| Tool | What it does |
|---|---|
| `open_data_catalog(query?, entity?, entity_type)` | Opens the panel. With no args, the Explore/Search landing (overview + governance render instantly, no DB round-trip). With `entity`, deep-links straight to that entity's profile page. |
| `catalog_search_tool(query, entity_types?, module?, tier?, tags?, owner?, limit)` | Ranked search across models / metrics / glossary with `facets` for type, module, tier, tags, and owner. |
| `get_catalog_entity_tool(name, entity_type)` | Full structured profile for one entity (schema, properties, lineage, metrics, relationships). |
| `catalog_sample(name, limit)` | Up to `limit` live sample rows for a model's table. Privacy-gated: privacy-restricted models return `{available: false, restricted: true}` without querying. |
| `catalog_table_stats(name)` | Row count + on-disk size for a model's physical table (n/a for views). |

## Elementary-backed health tools

Four tools surface dbt run/test observability from the [Elementary](https://docs.elementary-data.com/) tables (`elementary.*` in ClickHouse):

| Tool | What it does |
|---|---|
| `catalog_run_state(name, history)` | Latest run + recent run history for a model (status, duration, rows affected). |
| `catalog_test_results(name)` | Latest test pass / fail / warn results for a model. |
| `catalog_health()` | Platform-level freshness / failing-tests health summary. |
| `catalog_observability()` | The observability dashboard payload: model-run + test health, needs-attention list, recent runs, data as-of timestamp. |

These are feature-gated at runtime, not by an env var: on first use the server probes for the `elementary` schema and, when it is absent or unreachable, every health tool degrades to `{available: false, reason: "elementary not connected"}` instead of erroring.

## Typical flow

```text
> What do we have on Gnosis Pay?
agent calls open_data_catalog(query="gnosis pay")
→ panel opens with ranked model/metric/glossary hits + facets

> Open the KPI model
agent calls get_catalog_entity_tool(name="fct_execution_gpay_kpi_daily")
→ profile page: columns, tier, owner, lineage tab, attached metrics

> Is it fresh?
agent calls catalog_run_state(name="fct_execution_gpay_kpi_daily")
→ latest run status + history
```

## Notes and limits

- **Registry-native.** Search, profiles, overview, and governance come from the semantic registry snapshot — no ClickHouse access. Only the sample / stats / Elementary tools and the interactive lineage tab touch live systems.
- **Lineage is bounded.** The profile lineage tab reaches into the dbt manifest for a depth-controlled subgraph, capped so hub models can't blow up the renderer.
- **Web-only helpers.** A few endpoints (`catalog_lineage`, `catalog_overview`, `catalog_governance`, `catalog_run_config`) are exposed through the web-app dispatch registry for the browser UI rather than as agent tools.

## See also

- [Model Lineage](model-lineage.md) — the dedicated DAG explorer
- [Semantic Metrics](../advanced/semantic-metrics.md) — approved vs candidate metric tiers
- [Finding Tools](../advanced/discovery.md) — the `find` router that uses the same catalog index for model hits
