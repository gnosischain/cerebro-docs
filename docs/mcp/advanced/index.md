# Advanced

Deep-dive references for the systems that sit underneath the everyday tools.

| Page | Topic |
|---|---|
| [Finding Tools](discovery.md) | The `find` router, the `list` unifier, and the lean-core surface (`load_tools`, `LEAN_CORE_ENABLED`). |
| [Hybrid Search](hybrid-search.md) | BM25 + RRF + networkx lineage powering `search_models`, `discover_models`, `get_relevant_columns`. |
| [Memory & Resume](memory-and-resume.md) | The four persistence layers, event log schema, registry handlers. |
| [Quality Gates](quality-gates.md) | Eight enforcement rules `generate_report` runs against your output. |
| [Multi-Tenant](multi-tenant.md) | `CEREBRO_OWNER` hashing, salt rotation, cross-tenant isolation. |
| [Semantic Metrics](semantic-metrics.md) | When to use `query_metrics` vs `execute_query`. |
| [RPC Scans](rpc-scans.md) | Bulk on-chain log / call / storage / code / trace scans into ClickHouse scratch tables. |
| [Grafana Publishing](grafana-publishing.md) | Preview, validate, and publish ClickHouse-backed Grafana dashboards. |
| [Usage Guide](usage-guide.md) | The full how-to: setup, recipes, recovery, pitfalls. |

If you're new to Cerebro, start with the [Setup](../setup.md) and [Usage Guide](usage-guide.md). The other pages here exist mostly to answer "why is Cerebro doing X?" questions.
