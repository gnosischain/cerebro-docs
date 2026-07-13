# Available Tools

Cerebro MCP exposes a large static tool surface spanning discovery, governed metrics, query execution, visualisation, on-chain RPC, multi-phase workflows, and interactive mini-apps — plus a small set of dynamically registered SQL tools. This page is the categorised reference; for step-by-step recipes see the [Usage Guide](advanced/usage-guide.md), and for individual workflow walk-throughs see [Workflows](workflows/index.md).

!!! tip "How to discover tools at runtime"
    From any MCP host: `find(query)` is the single front door — one call routes a request to the right tools, metrics, and models with a pre-filled next action (see [Finding Tools](advanced/discovery.md)). `get_help()` returns the top-level navigation; `system_status()` confirms the server is healthy; `list_custom_tools()` enumerates the dynamically registered SQL tools.

<!-- BEGIN AUTO-GENERATED: mcp-tools-summary -->
**159 static tools** across 8 packages, plus **7 dynamic SQL-templated tools** from `custom_tools.yaml`.

| Package | Tools | Core | Advanced |
|---------|:-----:|:----:|:--------:|
| analytics | 47 | 5 | 42 |
| governance | 6 | 1 | 5 |
| research | 15 | 0 | 15 |
| semantic | 25 | 5 | 20 |
| storyteller | 11 | 0 | 11 |
| visualization | 34 | 7 | 27 |
| web3 | 18 | 0 | 18 |
| workflow | 3 | 0 | 3 |

| Risk class | Tools |
|------------|:-----:|
| app_only | 2 |
| external_write | 1 |
| read_only | 129 |
| server_state_write | 26 |
| subprocess | 1 |

| Feature flag | Tools gated |
|--------------|:-----------:|
| `CUSTOM_TOOLS_ENABLED` | 1 |
| `DASHBOARD_BUILDER_ENABLED` | 2 |
| `GRAFANA_TOOLS_ENABLED` | 5 |
| `LEAN_CORE_ENABLED` | 1 |
| `RPC_SCAN_ENABLED` | 11 |
| `SANDBOX_ENABLED` | 4 |
| `SEMANTIC_ENABLED` | 8 |
| `WORKFLOW_RESUME_TOOLS_ENABLED` | 3 |
<!-- END AUTO-GENERATED: mcp-tools-summary -->

---

## Analytics

The raw data-warehouse surface: dbt model discovery (`search_models`, `discover_models`, `get_model_details`), exact schema inspection (`describe_table` — call it before writing SQL), and query execution. Use `execute_query` for synchronous exploration (< 30s) and `start_query` + `get_query_results` for long-running queries; `save_query` / `run_saved_query` persist and replay SQL by name. This package also carries the metadata helpers (docs search, platform constants, token metadata, address resolution), deterministic networkx lineage (`get_upstream_lineage`, `get_downstream_impact`), the DuckDB + Parquet [simulation sandbox](workflows/simulation-sandboxes.md) tools (registered when `SANDBOX_ENABLED=true`), and the [Model Lineage Explorer](mini-apps/model-lineage.md) mini-app.

<!-- BEGIN AUTO-GENERATED: mcp-tools-analytics -->
**Custom query tools** (`custom_queries.py`)

| Tool | Summary | Tier | Risk | Gate |
|------|---------|------|------|------|
| `list_custom_tools` | List all available custom parameterized query tools. | advanced | read_only | `CUSTOM_TOOLS_ENABLED` |

**Model discovery & lineage** (`dbt.py`)

| Tool | Summary | Tier | Risk | Gate |
|------|---------|------|------|------|
| `search_models` | Search dbt models by name, description, or tags. | advanced | read_only | -- |
| `discover_models` | Search models AND return full details for top N matches in one call. | advanced | read_only | -- |
| `get_model_details` | Get comprehensive details about a dbt model including SQL, columns, and lineage. | core | read_only | -- |
| `get_relevant_columns` | Return a column-scoped schema block for a dbt model, ranked by | advanced | read_only | -- |
| `get_upstream_lineage` | Return the full transitive set of upstream dependencies for a dbt model. | advanced | read_only | -- |
| `get_downstream_impact` | Return the full transitive set of dbt models that depend on this one. | advanced | read_only | -- |

**Lineage graphs** (`lineage_graph.py`)

| Tool | Summary | Tier | Risk | Gate |
|------|---------|------|------|------|
| `get_model_subgraph` | Return a bounded model-lineage subgraph as JSON for traversal. | advanced | read_only | -- |
| `get_column_lineage` | Trace column-level lineage for a model column as JSON. | advanced | read_only | -- |

**Unified listing** (`list_unifier.py`)

| Tool | Summary | Tier | Risk | Gate |
|------|---------|------|------|------|
| `list` | List things of a given `kind` — one front door for the listing family. | advanced | read_only | -- |

**Metadata & reference** (`metadata.py`)

| Tool | Summary | Tier | Risk | Gate |
|------|---------|------|------|------|
| `list_databases` | List all available ClickHouse databases with descriptions and table counts. | advanced | read_only | -- |
| `quality_metrics` | Show quality-discipline gate evaluations and discovered-model coverage. | advanced | read_only | -- |
| `system_status` | Show server status: ClickHouse connectivity, manifest state, config. | core | read_only | -- |
| `resolve_address` | Look up an address label or find addresses by name using dune_labels (5.3M entries). | advanced | read_only | -- |
| `get_token_metadata` | Look up token metadata: address, decimals, name, and price data availability. | advanced | read_only | -- |
| `search_models_by_address` | Find dbt models related to a specific smart contract address. | advanced | read_only | -- |
| `search_docs` | Search across all platform documentation and reference resources. | advanced | read_only | -- |
| `get_doc_chunk` | Retrieve full text of a documentation page by its location path. | advanced | read_only | -- |
| `get_docs_overview` | Retrieve the curated docs overview published at llms.txt. | advanced | read_only | -- |
| `get_docs_context` | Retrieve the generated broad docs context artifact. | advanced | read_only | -- |
| `get_gnosis_chain_docs_context` | Retrieve the Gnosis Chain docs llms context artifact. | advanced | read_only | -- |
| `get_gnosis_chain_doc_chunk` | Retrieve a single Gnosis Chain docs section from the llms artifact. | advanced | read_only | -- |
| `get_help` | Overview of all available tools, prompts, and resources in Cerebro MCP. | core | read_only | -- |
| `get_platform_constants` | Returns hardcoded Gnosis Chain platform constants: chain parameters, | advanced | read_only | -- |

**Model Lineage mini-app** (`model_lineage_app.py`)

| Tool | Summary | Tier | Risk | Gate |
|------|---------|------|------|------|
| `open_model_lineage` | Open the Model Lineage Explorer mini app. | advanced | read_only | -- |
| `expand_model_lineage_node` | Expand the lineage graph by one hop around `node_id` and merge it in. | advanced | read_only | -- |
| `set_model_lineage_filters` | Re-run the subgraph from the current seed with new filters/layer. | advanced | read_only | -- |
| `load_column_lineage` | Compute column-level lineage and load it into the column drawer. | advanced | read_only | -- |

**Query execution** (`query.py`)

| Tool | Summary | Tier | Risk | Gate |
|------|---------|------|------|------|
| `execute_query` | Execute a read-only SQL query against a Gnosis Chain ClickHouse database. | core | read_only | -- |
| `explain_query` | Show the execution plan for a SQL query without running it. | advanced | read_only | -- |

**Async queries** (`query_async.py`)

| Tool | Summary | Tier | Risk | Gate |
|------|---------|------|------|------|
| `start_query` | Submit a long-running query for async execution. Returns a query ID to poll. | advanced | read_only | -- |
| `get_query_results` | Check status and retrieve paginated results of an async query. | advanced | read_only | -- |

**Simulation sandboxes** (`sandbox.py`)

| Tool | Summary | Tier | Risk | Gate |
|------|---------|------|------|------|
| `create_simulation_sandbox` | Fork ClickHouse data into a private DuckDB sandbox for what-if analysis. | advanced | read_only | `SANDBOX_ENABLED` |
| `query_sandbox` | Run any SQL against a sandbox. Reads, UPDATEs, INSERTs, DELETEs allowed. | advanced | read_only | `SANDBOX_ENABLED` |
| `destroy_sandbox` | Close and remove a simulation sandbox. Idempotent. | advanced | read_only | `SANDBOX_ENABLED` |
| `list_sandboxes` | List active simulation sandboxes (id, table, rows, bytes, idle time). | advanced | read_only | `SANDBOX_ENABLED` |

**Saved queries** (`saved_queries.py`)

| Tool | Summary | Tier | Risk | Gate |
|------|---------|------|------|------|
| `save_query` | Save a query for later reuse. Validates SQL before saving. | advanced | server_state_write | -- |
| `list_saved_queries` | List all saved queries with their names, databases, and descriptions. | advanced | read_only | -- |
| `run_saved_query` | Execute a previously saved query by name. | advanced | read_only | -- |

**Schema & sampling** (`schema.py`)

| Tool | Summary | Tier | Risk | Gate |
|------|---------|------|------|------|
| `list_tables` | List tables in a ClickHouse database with cursor pagination. | advanced | read_only | -- |
| `record_model_exclusion` | Mark a model surfaced by `search_models` / `discover_models` as | advanced | read_only | -- |
| `record_model_exclusion_batch` | Exclude multiple discovered models from the coverage gate in | advanced | read_only | -- |
| `exclude_models_by_prefix` | Exclude every discovered model whose name starts with `prefix`. | advanced | read_only | -- |
| `exclude_module` | Exclude every discovered model belonging to a dbt module. | advanced | read_only | -- |
| `exclude_all_discovered_except` | Inverse exclusion: keep the named discovered models in scope, | advanced | read_only | -- |
| `describe_table` | Get the column schema for a specific table. | core | read_only | -- |
| `get_sample_data` | Get sample rows from a table to understand data shape and values. | advanced | read_only | -- |
<!-- END AUTO-GENERATED: mcp-tools-analytics -->

---

## Semantic

Governed metrics and semantic-layer routing (registered when `SEMANTIC_ENABLED=true`). Prefer `query_metrics` over raw SQL whenever an approved metric covers the question — it runs the canonical, pre-validated query (see [Semantic Metrics](advanced/semantic-metrics.md)). The `find` router is the recommended first call for almost any analytical question, and `preflight_analytics_request` is the hard gate in front of chart/report generation. The package also hosts the [Data Catalog](mini-apps/data-catalog.md) (search-first browse over models, metrics, and glossary terms, with Elementary-backed run/test health) and the [Graph Explorer](mini-apps/graph-explorer.md) mini-app.

<!-- BEGIN AUTO-GENERATED: mcp-tools-semantic -->
**Data Catalog** (`data_catalog.py`)

| Tool | Summary | Tier | Risk | Gate |
|------|---------|------|------|------|
| `catalog_search_tool` | Search the data catalog (models, metrics, glossary) with facets. | advanced | read_only | -- |
| `get_catalog_entity_tool` | Return a structured catalog profile for one entity (model/metric/glossary). | advanced | read_only | -- |
| `catalog_sample` | Return up to `limit` live sample rows for a model's table. | advanced | read_only | -- |
| `catalog_table_stats` | Row count + on-disk size for a model's physical table (n/a for views). | advanced | read_only | -- |
| `catalog_run_state` | Latest run + recent history for a model (Elementary; feature-flagged). | advanced | read_only | -- |
| `catalog_test_results` | Latest test pass/fail/warn for a model (Elementary; feature-flagged). | advanced | read_only | -- |
| `catalog_health` | Platform freshness / failing-tests health (Elementary; feature-flagged). | advanced | read_only | -- |
| `catalog_observability` | Platform observability dashboard: model-run + test health, needs-attention, | advanced | read_only | -- |
| `open_data_catalog` | Open the Data Catalog mini app. | advanced | read_only | -- |

**Discovery router** (`find.py`)

| Tool | Summary | Tier | Risk | Gate |
|------|---------|------|------|------|
| `find` | Single front door: one call routes a request to the right tools, | core | read_only | `SEMANTIC_ENABLED` |

**Graph Explorer** (`graph_explorer.py`)

| Tool | Summary | Tier | Risk | Gate |
|------|---------|------|------|------|
| `open_graph_explorer` | Open the Graph Explorer mini app. | advanced | read_only | -- |
| `load_graph_explorer_seed` | Load a bounded 1-hop subgraph around seed_node_id. | advanced | read_only | -- |
| `expand_graph_explorer_node` | Expand `node_id` by one hop across the selected profiles. | advanced | read_only | -- |
| `update_graph_explorer_focus` | Mutate view state only (selection, filters, layout). No refetch. | advanced | read_only | -- |
| `search_graph_catalog` | Search the knowledge-graph catalog (node types, edge profiles). | advanced | read_only | -- |
| `explore_neighborhood` | Bounded multi-hop neighborhood traversal around seed node ids. | advanced | read_only | -- |
| `calculate_flow_efficiency` | Per-node weighted-flow efficiency = outflow / inflow for a profile. | advanced | read_only | -- |
| `graph_usage_analytics` | Adoption analytics for the graph tools (WS12). | advanced | read_only | -- |

**Governed metrics** (`semantic.py`)

| Tool | Summary | Tier | Risk | Gate |
|------|---------|------|------|------|
| `preflight_analytics_request` | Route an analytics question to the right workflow before charting or reporting. | core | read_only | `SEMANTIC_ENABLED` |
| `discover_metrics` | Search the semantic layer for metrics matching a natural-language query. | advanced | read_only | `SEMANTIC_ENABLED` |
| `get_metric_details` | Get the full definition of one governed metric: dimensions, grains, lineage, docs. | core | read_only | `SEMANTIC_ENABLED` |
| `explain_metric_query` | Show the planner's plan and compiled ClickHouse SQL without executing it. | core | read_only | `SEMANTIC_ENABLED` |
| `query_metrics` | Execute governed metrics through the semantic layer and return result rows. | core | read_only | `SEMANTIC_ENABLED` |
| `reload_semantic_registry` | Force an immediate refresh of the semantic registry, bypassing | advanced | read_only | `SEMANTIC_ENABLED` |
| `get_clickhouse_query_rules` | Return the ClickHouse query-writing rules for raw-SQL fallback work. | advanced | read_only | `SEMANTIC_ENABLED` |
<!-- END AUTO-GENERATED: mcp-tools-semantic -->

---

## Visualization & Reporting

Charts, reports, dashboards, and the mini-app plumbing. `generate_charts` is the batch chart generator (always ≥ 3 charts in one call — required for reports); `generate_chart` / `quick_chart` are for one-off scratch plots; the `*_metric_chart*` variants are driven by metric names instead of raw SQL. Three report layouts exist: dashboard (`generate_report`), research essay (`generate_research_report`), and scrollytelling case study (`generate_case_study_report`) — see [Report Generation](reports.md) and [Quality Gates](advanced/quality-gates.md) for the enforcement rules. The package also carries the [Metric Lab](mini-apps/metric-lab.md) and [Portfolio](mini-apps/portfolio.md) mini-apps, `export_report` (docx / pdf / pptx), and the [Grafana dashboard publishing](advanced/grafana-publishing.md) family (registered when `GRAFANA_TOOLS_ENABLED=true`).

<!-- BEGIN AUTO-GENERATED: mcp-tools-visualization -->
**Charts & reports** (`charts.py`)

| Tool | Summary | Tier | Risk | Gate |
|------|---------|------|------|------|
| `generate_chart` | Generate a single ad-hoc chart. For reports, use `generate_charts` instead. | core | read_only | -- |
| `quick_chart` | Generate a quick ad-hoc chart for a one-off plot request. | core | read_only | -- |
| `generate_charts` | Create multiple charts in ONE tool call. | core | read_only | -- |
| `quick_metric_chart` | Generate a one-off semantic chart without writing SQL. | core | read_only | -- |
| `generate_metric_charts` | Create multiple semantic charts in one batch call. | core | read_only | -- |
| `list_charts` | List all charts in the registry with IDs, titles, and types. | advanced | read_only | -- |
| `generate_report` | Create an interactive report rendered as a native UI in the chat client. | core | server_state_write | -- |
| `generate_research_report` | Create a long-form research report in the Anthropic-essay style. | advanced | read_only | -- |
| `generate_case_study_report` | Create a scrollytelling case-study report (marketing / growth pitch style). | advanced | read_only | -- |
| `open_report` | Reopen a previously generated report by its ID. | advanced | server_state_write | -- |
| `list_reports` | List previously generated reports saved on disk. | advanced | read_only | -- |
| `export_report` | Export a report as standalone HTML that can be saved and opened in any browser. | advanced | server_state_write | -- |

**Dashboard builder** (`dashboard_builder.py`)

| Tool | Summary | Tier | Risk | Gate |
|------|---------|------|------|------|
| `discover_dashboard_metrics` | Discover dbt models suitable for dashboard metrics. | advanced | read_only | `DASHBOARD_BUILDER_ENABLED` |
| `scaffold_dashboard_tab` | Scaffold a dashboard tab from a JSON blueprint. | advanced | subprocess | `DASHBOARD_BUILDER_ENABLED` |

**Grafana publishing** (`grafana.py`)

| Tool | Summary | Tier | Risk | Gate |
|------|---------|------|------|------|
| `preview_grafana_dashboard` | Return an ASCII sketch of the dashboard layout plus the metric each | advanced | read_only | `GRAFANA_TOOLS_ENABLED` |
| `validate_grafana_dashboard` | Validate a dashboard spec without publishing. | advanced | read_only | `GRAFANA_TOOLS_ENABLED` |
| `verify_grafana_dashboard` | Run every panel against the live Grafana datasource and report | advanced | read_only | `GRAFANA_TOOLS_ENABLED` |
| `publish_grafana_dashboard` | Compile and publish a dashboard to Grafana (idempotent by UID). | advanced | external_write | `GRAFANA_TOOLS_ENABLED` |
| `get_grafana_dashboard` | Fetch metadata for a published dashboard by UID. | advanced | read_only | `GRAFANA_TOOLS_ENABLED` |

**Metric Lab mini-app** (`metric_lab.py`)

| Tool | Summary | Tier | Risk | Gate |
|------|---------|------|------|------|
| `open_metric_lab` | Open the interactive Metric Lab app with an empty metric catalog. | advanced | read_only | -- |
| `load_metric_lab_metric` | Load a dbt model (or legacy semantic metric) into an open view. | advanced | read_only | -- |
| `open_metric_lab_from_sql` | Open the interactive Metric Lab app from a raw SQL query. | advanced | read_only | -- |
| `open_metric_lab_from_metrics` | Open the interactive Metric Lab app from a semantic metric request. | advanced | read_only | -- |
| `update_metric_lab_chart` | Patch the chart configuration in an open Metric Lab view. | advanced | read_only | -- |
| `search_metric_catalog` | [App-only] Search / page the model catalog for the frontend. | advanced | read_only | -- |
| `get_metric_catalog_entry` | [App-only] Full detail for one catalog entry (metric or model). | advanced | read_only | -- |

**Mini-app infrastructure** (`mini_apps.py`)

| Tool | Summary | Tier | Risk | Gate |
|------|---------|------|------|------|
| `load_tools` | Un-hide advanced tools so they appear in the tool list (lean-core mode). | core | read_only | `LEAN_CORE_ENABLED` |

**Portfolio mini-app** (`portfolio.py`)

| Tool | Summary | Tier | Risk | Gate |
|------|---------|------|------|------|
| `open_portfolio` | Open an empty Portfolio mini app. | advanced | read_only | -- |
| `load_portfolio_address` | Load one address into an existing Portfolio view. | advanced | read_only | -- |
| `navigate_portfolio_relation` | Drill one hop into a related Safe or owner address. | advanced | read_only | -- |
| `load_portfolio_section` | Lazy-load one portfolio section into an existing view. | advanced | read_only | -- |
| `update_portfolio_focus` | Patch client-side section focus and filters. | advanced | read_only | -- |

<details>
<summary>App-internal tools (2) — called by mini-app UIs, not meant for direct use</summary>

| Tool | Summary | Tier | Risk | Gate |
|------|---------|------|------|------|
| `get_mini_app_rows` | [App-only] Fetch the next page of rows for a mini-app dataset. | advanced | app_only | -- |
| `get_mini_app_state` | [App-only] Return the current view state and dataset metadata. | advanced | app_only | -- |

</details>
<!-- END AUTO-GENERATED: mcp-tools-visualization -->

---

## Web3

Direct read access to EVM contracts via JSON-RPC. Prefer the single-call tools (`contract_explore`, `contract_call_function`, `contract_decode_transaction_input`, `contract_decode_receipt_logs`) over dbt for **single-address current state** — dbt is for sweeps, historical data, USD conversion, and aggregations. The [Contract Explorer](mini-apps/contract-explorer.md) mini-app wraps the same engine as an interactive surface. For **bulk** work — sweeping logs, batched view calls, storage slots, bytecode classification, or trace scans across thousands of addresses — the `rpc_scan_*` / `rpc_batch_call` family (registered when `RPC_SCAN_ENABLED=true`) streams results into ClickHouse scratch tables for SQL analysis; see [RPC Scans](advanced/rpc-scans.md). Archive reads (non-`latest` blocks) and trace scans require `GNOSIS_ARCHIVE_RPC_URL`.

<!-- BEGIN AUTO-GENERATED: mcp-tools-web3 -->
**Contract Explorer mini-app** (`contract_explorer.py`)

| Tool | Summary | Tier | Risk | Gate |
|------|---------|------|------|------|
| `open_contract_explorer` | Launch the Contract Explorer — an Etherscan-style read-only contract page. | advanced | read_only | -- |
| `load_contract_explorer_address` | Swap to a different contract inside an open Contract Explorer view. | advanced | read_only | -- |
| `contract_explorer_call_function` | Call one view/pure function on the Contract Explorer's current contract. | advanced | read_only | -- |

**Contract inspection** (`rpc.py`)

| Tool | Summary | Tier | Risk | Gate |
|------|---------|------|------|------|
| `contract_explore` | Quickly inspect one contract by address — what functions/events it exposes, the proxy implementation, and where the ABI was resolved from. | advanced | read_only | -- |
| `contract_call_function` | Get current on-chain state at one address with one RPC round-trip. | advanced | read_only | -- |
| `contract_decode_transaction_input` | Decode a single transaction's calldata back into function name + arguments using the resolved contract ABI. | advanced | read_only | -- |
| `contract_decode_receipt_logs` | Decode the event logs in a transaction receipt back into event name + args, with ABIs resolved per emitting contract. | advanced | read_only | -- |

**Bulk RPC scans** (`rpc_scan.py`)

| Tool | Summary | Tier | Risk | Gate |
|------|---------|------|------|------|
| `rpc_scan_logs` | Sweep eth_getLogs over ANY block window into a ClickHouse scratch table. | advanced | read_only | `RPC_SCAN_ENABLED` |
| `rpc_batch_call` | Batch view-function reads across thousands of addresses via | advanced | read_only | `RPC_SCAN_ENABLED` |
| `rpc_read_storage` | Read raw storage slots (eth_getStorageAt) across an address set at | advanced | read_only | `RPC_SCAN_ENABLED` |
| `rpc_get_code` | Classify every address in a set by its bytecode (eth_getCode): | advanced | read_only | `RPC_SCAN_ENABLED` |
| `rpc_scan_traces` | Sweep trace_filter for NATIVE xDAI value flows (and internal calls) | advanced | read_only | `RPC_SCAN_ENABLED` |
| `rpc_trace_transaction` | Render one transaction's full execution as an indented call tree | advanced | read_only | `RPC_SCAN_ENABLED` |
| `rpc_find_block` | Binary-search block finders (O(log N) RPC reads per target). | advanced | read_only | `RPC_SCAN_ENABLED` |
| `rpc_scan_status` | Status of an RPC scan job. | advanced | read_only | `RPC_SCAN_ENABLED` |
| `rpc_scan_cancel` | Stop a running RPC scan. Partial rows are KEPT in the scratch table | advanced | read_only | `RPC_SCAN_ENABLED` |
| `rpc_scan_resume` | Resume a partial/cancelled/restart-orphaned scan from its persisted | advanced | read_only | `RPC_SCAN_ENABLED` |
| `rpc_list_scans` | List RPC scan jobs — in-memory ones plus the persisted registry | advanced | read_only | `RPC_SCAN_ENABLED` |
<!-- END AUTO-GENERATED: mcp-tools-web3 -->

---

## Governance

Verification, reasoning traces, and the agent-persona loader. `verify_numbers` cross-checks a numerical claim against fresh SQL; `get_agent_persona(role)` loads one of the [28 persona contracts](agents.md) (the `cerebro_dispatcher` persona is the front door for non-trivial requests — see [Dispatcher](dispatcher.md)). The reasoning tools (`set_thinking_mode`, `log_reasoning`, `get_reasoning_log`, `get_performance_stats`) manage the 30-day reasoning trace, and the model-exclusion family (`record_model_exclusion`, `exclude_module`, …) satisfies the discovered-model-coverage gate that `generate_report` enforces.

<!-- BEGIN AUTO-GENERATED: mcp-tools-governance -->
**Agent personas** (`agents.py`)

| Tool | Summary | Tier | Risk | Gate |
|------|---------|------|------|------|
| `get_agent_persona` | Fetch strict operational rules for a specific agent persona. | advanced | read_only | -- |

**Verification** (`cross_check.py`)

| Tool | Summary | Tier | Risk | Gate |
|------|---------|------|------|------|
| `verify_numbers` | Verify numerical claims before reporting to the user. | core | read_only | -- |

**Reasoning & tracing** (`reasoning.py`)

| Tool | Summary | Tier | Risk | Gate |
|------|---------|------|------|------|
| `set_thinking_mode` | Enable or disable thinking/reasoning capture mode. | advanced | server_state_write | -- |
| `log_reasoning` | Record a reasoning step for audit and performance analysis. | advanced | read_only | -- |
| `get_reasoning_log` | Retrieve the reasoning trace for a session. | advanced | read_only | -- |
| `get_performance_stats` | Aggregate performance metrics across recent sessions. | advanced | read_only | -- |
<!-- END AUTO-GENERATED: mcp-tools-governance -->

---

## Research Workflow

Multi-phase research projects: plan → execute → verify per phase, with findings, memory notes, evidence bindings, schema snapshots, and a peer-review gate before `publish_research_report` flips the workflow to `complete`. Every step appends to the durable event log, so a crashed project resumes where it stopped. See [Research Projects](workflows/research-projects.md) for the end-to-end recipe.

<!-- BEGIN AUTO-GENERATED: mcp-tools-research -->
**Research workflow** (`research.py`)

| Tool | Summary | Tier | Risk | Gate |
|------|---------|------|------|------|
| `start_research_project` | Create a new durable research project with explicit workflow phases. | advanced | server_state_write | -- |
| `get_research_project` | Return a compact summary of a research project's state. | advanced | read_only | -- |
| `plan_research_phase` | Record a structured plan for the current research phase. | advanced | server_state_write | -- |
| `execute_research_phase` | Advance a research phase after the user/client completes the planned work. | advanced | server_state_write | -- |
| `get_research_memory` | List project memory entries with pagination. | advanced | read_only | -- |
| `get_research_evidence` | List research evidence refs with optional phase filtering. | advanced | read_only | -- |
| `get_research_findings` | List project findings with pagination. | advanced | read_only | -- |
| `attach_research_evidence` | Attach an existing query/chart/report/schema artifact to a research project. | advanced | server_state_write | -- |
| `capture_schema_snapshot` | Persist a schema snapshot and register it as research evidence. | advanced | server_state_write | -- |
| `record_research_memory` | Store a durable research memory entry linked to supporting evidence. | advanced | server_state_write | -- |
| `record_research_finding` | Store a project-specific conclusion backed by evidence references. | advanced | server_state_write | -- |
| `verify_research_phase` | Run structural validation checks before peer review/publication. | advanced | server_state_write | -- |
| `prepare_peer_review` | Build a compact review packet for the research peer-review prompt. | advanced | server_state_write | -- |
| `record_peer_review` | Store the structured result of an adversarial peer review. | advanced | server_state_write | -- |
| `publish_research_report` | Publish a research report after verification and peer review. | advanced | server_state_write | -- |
<!-- END AUTO-GENERATED: mcp-tools-research -->

---

## Storyteller Workflow

The narrative-first deliverable pipeline (*Storytelling with Data*): context brief → big idea → storyboard → per-scene visual specs → final story, with clarity and accessibility gates before `storyteller_generate_story_report` emits the report. Phase order is enforced in a state machine — skipping a gate raises an error. See [Storyteller](workflows/storyteller.md).

<!-- BEGIN AUTO-GENERATED: mcp-tools-storyteller -->
**Storyteller workflow** (`storyteller.py`)

| Tool | Summary | Tier | Risk | Gate |
|------|---------|------|------|------|
| `storyteller_start_session` | Begin a new storyteller session. | advanced | server_state_write | -- |
| `storyteller_end_session` | End the current storyteller session and clear all artifacts. | advanced | server_state_write | -- |
| `storyteller_status` | Return a snapshot of the current storyteller session state. | advanced | read_only | -- |
| `storyteller_record_context_brief` | Record the context brief that gates the whole pipeline. | advanced | server_state_write | -- |
| `storyteller_record_big_idea` | Record the single governing takeaway as one declarative sentence. | advanced | server_state_write | -- |
| `storyteller_record_storyboard` | Record the low-fidelity storyboard before any chart is rendered. | advanced | server_state_write | -- |
| `storyteller_record_visual_spec` | Record the design rationale for one storyboard scene's visual. | advanced | server_state_write | -- |
| `storyteller_record_final_story` | Record the assembled final story (title + markdown with chart placeholders). | advanced | server_state_write | -- |
| `storyteller_run_clarity_checks` | Record the clarity review report from the Critic Agent. | advanced | server_state_write | -- |
| `storyteller_record_accessibility_pass` | Record the accessibility and tone review outcome. | advanced | server_state_write | -- |
| `storyteller_generate_story_report` | Render the final story as an interactive report. | advanced | server_state_write | -- |
<!-- END AUTO-GENERATED: mcp-tools-storyteller -->

---

## Workflow Resume

Crash recovery over the SQLite event log (registered when `WORKFLOW_RESUME_TOOLS_ENABLED=true`). `list_resumable_workflows` enumerates running / waiting-gate workflows, and `get_workflow_resume_hint` / `recompute_workflow_resume_hint` return a structured "here is where you stopped, do this next" payload. The underlying event store records workflow state regardless of this flag — it only gates the user-facing tools. See [Resumable Workflows](workflows/resumable-workflows.md) and [Memory & Resume](advanced/memory-and-resume.md).

<!-- BEGIN AUTO-GENERATED: mcp-tools-workflow -->
**Workflow resume** (`resume.py`)

| Tool | Summary | Tier | Risk | Gate |
|------|---------|------|------|------|
| `list_resumable_workflows` | List workflows currently running or waiting on a gate, with | advanced | read_only | `WORKFLOW_RESUME_TOOLS_ENABLED` |
| `get_workflow_resume_hint` | Return the most recent resume hint for a specific workflow. | advanced | read_only | `WORKFLOW_RESUME_TOOLS_ENABLED` |
| `recompute_workflow_resume_hint` | Re-run the resume scan for a single workflow and append a new | advanced | read_only | `WORKFLOW_RESUME_TOOLS_ENABLED` |
<!-- END AUTO-GENERATED: mcp-tools-workflow -->

---

## Dynamic Custom Tools

Beyond the static surface, Cerebro registers SQL-templated tools from a YAML file at startup (the MCP Toolbox pattern). Each entry in `custom_tools.yaml` declares a tool name, description, typed parameters, a target database, and a parameterised read-only `SELECT`; the server registers each one as a first-class MCP tool when `CUSTOM_TOOLS_ENABLED=true` (with `CUSTOM_TOOLS_PATH` pointing at the file). This is how the bridge-flow, validator-history, and Gnosis Pay helpers ship — curated, pre-divided (wei/Gwei-safe) queries that are cheaper and safer than having the model re-derive the SQL. `list_custom_tools()` enumerates the set loaded in the current build; dynamic tools are auto-classified `read_only` in the [security registry](security.md).

<!-- BEGIN AUTO-GENERATED: mcp-tools-custom -->
| Tool | Summary | Parameters | Database |
|------|---------|------------|----------|
| `get_validator_balance_history` | Get daily balance history for a specific Gnosis Chain validator. | -- | dbt |
| `get_validator_withdrawals` | Get withdrawal history for a specific validator on Gnosis Chain. | -- | dbt |
| `get_token_transfers_for_address` | Get daily ERC-20 token transfer summary for a specific address (sent and received). | -- | dbt |
| `get_gpay_wallet_activity` | Get Gnosis Pay transaction history for a specific wallet address. | -- | dbt |
| `get_liquidity_providers_by_token` | Get unique liquidity provider counts for a token across time windows (7D, 30D, 90D, All). | -- | dbt |
| `get_bridge_flows_by_token` | Get daily bridge flow volume for a specific token across all bridges on Gnosis Chain. | -- | dbt |
| `get_deposit_events` | Get GBC (Gnosis Beacon Chain) deposit events, optionally filtered by withdrawal credentials. | -- | dbt |
<!-- END AUTO-GENERATED: mcp-tools-custom -->

---

## Tool-classification rules

Every tool is classified by risk class; the classification drives the audit log and Prometheus counters. See [Security & Audit](security.md) for the full rules.

| Risk class | Examples |
|---|---|
| `read_only` | `execute_query`, `search_models`, `generate_charts`, `contract_call_function` |
| `server_state_write` | `save_query`, `generate_report`, `start_research_project`, `storyteller_record_*` |
| `workspace_write` | `scaffold_dashboard_tab` |
| `subprocess` | `scaffold_dashboard_tab` (runs `pnpm build`) |
| `external_write` | `publish_grafana_dashboard` (writes to an external Grafana instance) |
| `app_only` | `get_mini_app_rows`, `get_mini_app_state` (hidden from agents; frontend-only) |
