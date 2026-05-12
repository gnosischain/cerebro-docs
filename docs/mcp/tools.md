# Available Tools

Cerebro MCP exposes ~50 tools spanning discovery, query execution, visualisation, workflows, mini-apps, simulation, and resume. This page is the categorised reference. For step-by-step recipes see the [Usage Guide](advanced/usage-guide.md); for individual workflow walk-throughs see [Workflows](workflows/index.md).

!!! tip "How to discover tools at runtime"
    From any MCP host: `list_custom_tools()` returns the live set; `get_help()` returns the top-level navigation; `system_status()` confirms the server is healthy.

---

## 1. Discovery & schema

| Tool | Purpose |
|------|---------|
| `search_models(query)` | Hybrid BM25 + RRF + token-overlap search. Returns api_*, fct_*, int_*, stg_* tiers. See [Hybrid Search](advanced/hybrid-search.md). |
| `discover_models(filters)` | Filtered listing — by tier, tag, module, semantic-status. |
| `get_model_details(name)` | Lineage (upstream + downstream), columns, tests, freshness, doc blocks. |
| `describe_table(table)` | Exact ClickHouse column types — call before writing SQL. |
| `get_relevant_columns(model, query, top_k=20)` | BM25-ranked column subset for wide tables. Always includes join keys + time grains. |
| `search_models_by_address(address)` | Reverse lookup: which dbt models reference this address? |
| `list_databases()` / `list_tables(db)` | Raw catalog browse. |
| `get_upstream_lineage(model)` | Transitive ancestors via networkx. |
| `get_downstream_impact(model)` | Transitive descendants — schema-change blast radius. |
| `get_clickhouse_query_rules()` | The CH dialect cheat sheet — load before writing complex SQL. |
| `get_platform_constants()` | Network constants (epoch length, slot duration, etc.). |
| `get_token_metadata(symbol \| address)` | Decimals, price availability, contract address. |
| `resolve_address(input)` | ENS, Safe, Circles, GPay, Dune label resolution. |

---

## 2. Query execution

| Tool | When to use |
|------|------|
| `execute_query(sql, database)` | Synchronous, < 30s queries. Default for EDA. |
| `start_query(sql, database)` + `get_query_results(query_id)` | Long-running queries. Returns immediately, poll later. |
| `query_metrics(metric, dims, range)` | Pre-defined metric semantics — safer than raw SQL. See [Semantic Metrics](advanced/semantic-metrics.md). |
| `run_saved_query(name)` | Replay a previously `save_query`'d SQL. |
| `save_query(name, sql)` | Persist SQL by name. |
| `list_saved_queries()` | Catalogue of saved queries. |
| `explain_query(sql)` / `explain_metric_query(...)` | ClickHouse `EXPLAIN` — check the plan before running heavy queries. |
| `verify_numbers(claim, sql)` | Cross-check a numerical claim against fresh SQL. |
| `preflight_analytics_request(question, domain)` | Dispatcher gate — emitted as part of the dispatch manifest. |
| `discover_metrics(filters)` / `get_metric_details(name)` | Browse the semantic metric catalogue. |
| `discover_dashboard_metrics(dashboard)` | Per-dashboard metric inventory. |
| `get_sample_data(table)` | Preview a few rows of any table. |

---

## 3. Visualisation & reporting

| Tool | Purpose |
|------|---------|
| `generate_charts(specs=[...])` | **Batch** chart generator. Always ≥ 3 charts in one call. Required for reports. |
| `generate_chart(spec)` | Single chart — only for one-off scratch plots. |
| `generate_metric_charts(...)` / `quick_metric_chart(...)` | Charts driven by metric names instead of raw SQL. |
| `quick_chart(...)` | Inline shortcut for SQL → chart. |
| `generate_report(markdown)` | Dashboard layout — the standard analytical report. |
| `generate_research_report(markdown, deck, key_takeaways, ...)` | Long-form research essay (Anthropic-style). |
| `generate_case_study_report(markdown, deck, key_points, ...)` | Scrollytelling layout for marketing / customer stories. |
| `export_report(report_id, format)` | docx / pdf / pptx conversion. |
| `list_reports()` / `open_report(id)` | Reopen past reports (dashboard + research kinds). |
| `list_charts()` | Catalogue of chart specs in this server. |

See [Report Generation](reports.md) for the full pipeline and [Quality Gates](advanced/quality-gates.md) for the eight enforcement rules.

---

## 4. Research workflow

| Tool | Purpose |
|------|---------|
| `start_research_project(question, hypothesis, scope)` | Creates project + first research workflow. |
| `plan_research_phase(project_id, phase, plan_markdown)` | Phase planning — appends `phase_planned` event. |
| `execute_research_phase(project_id, phase)` | Phase execution loop. |
| `verify_research_phase(project_id, phase, passed, summary)` | Verification gate. |
| `record_research_finding(project_id, finding)` | Persists a finding (auto-emits `finding_recorded`). |
| `record_research_memory(project_id, memory)` | Persists a memory note. |
| `attach_research_evidence(project_id, ref)` | Binds a chart/query to a finding. |
| `capture_schema_snapshot(project_id, tables)` | Pin schemas for the project's lifetime. |
| `prepare_peer_review(project_id)` / `record_peer_review(project_id, status, summary)` | Peer-review gate. |
| `publish_research_report(project_id, ...)` | Terminal step — flips workflow to `complete`. |
| `get_research_project(id)` / `get_research_findings(id)` / `get_research_memory(id)` / `get_research_evidence(id)` | Read-side accessors. |

See [Research Projects](workflows/research-projects.md) for the end-to-end recipe.

---

## 5. Storyteller (narrative pipeline)

| Tool | Purpose |
|------|---------|
| `storyteller_start_session(session_id, deliverable_kind)` | Begins narrative-first deliverable. |
| `storyteller_record_context_brief(audience, mechanism, required_action)` | Phase 1: who's reading, what action. |
| `storyteller_record_big_idea(sentence, stakes)` | Phase 2: one-sentence thesis. |
| `storyteller_record_storyboard(scene_count, narrative_order, rationale)` | Phase 3: scene plan. |
| `storyteller_record_visual_spec(scene_index, chart_family, ...)` | Phase 4: per-scene chart design. |
| `storyteller_record_final_story(title, content_length)` | Phase 5: drafted prose. |
| `storyteller_run_clarity_checks()` | Clarity gate. |
| `storyteller_record_accessibility_pass()` | Accessibility gate. |
| `storyteller_generate_story_report(style)` | Terminal — emits the report. `style="research" \| "scrollytelling" \| "dashboard"`. |
| `storyteller_status()` / `storyteller_end_session()` | Inspection / cleanup. |

See [Storyteller](workflows/storyteller.md).

---

## 6. Mini-apps (live UI surfaces)

These open interactive panels in the GUI:

| Tool group | Surface |
|---|---|
| `open_portfolio` / `load_portfolio_address` / `load_portfolio_section` / `update_portfolio_focus` / `navigate_portfolio_relation` | [Portfolio Explorer](mini-apps/portfolio.md) |
| `open_graph_explorer` / `load_graph_explorer_seed` / `expand_graph_explorer_node` / `update_graph_explorer_focus` | [Graph Explorer](mini-apps/graph-explorer.md) |
| `open_metric_lab` / `open_metric_lab_from_sql` / `open_metric_lab_from_metrics` / `load_metric_lab_metric` / `update_metric_lab_chart` | [Metric Lab](mini-apps/metric-lab.md) |
| `open_contract_explorer` / `load_contract_explorer_address` / `contract_explorer_call_function` | [Contract Explorer](mini-apps/contract-explorer.md) |
| `open_report` | Past reports |

---

## 7. On-chain RPC & contract tools

Direct read access to EVM contracts via JSON-RPC. Prefer these over dbt for **single-address current state** — dbt is for sweeps, historical, USD conversion, and aggregations.

| Tool | Purpose |
|------|---------|
| `contract_explore(address, include_abi=False)` | Resolve ABI (catalog → Sourcify → 4byte fallback), follow proxies, list callable functions + events. |
| `contract_call_function(address, function_name, args?, block_identifier="latest", function_signature?, target="auto", from_address?)` | Static `eth_call` against a verified read function. Pass `function_signature` to disambiguate overloads. State-changing functions are rejected. |
| `contract_decode_transaction_input(address?, tx_hash?, input_data?, target="auto")` | Decode a past tx's calldata back into function + args using the target ABI. |
| `contract_decode_receipt_logs(tx_hash, ...)` | Decode events from a tx receipt. |
| `contract_explorer_call_function(...)` | Same as `contract_call_function` but pinned to the open Contract Explorer mini-app. |
| `resolve_address(address)` | ENS / known-tag lookup. |
| `get_token_metadata(address)` | Symbol, decimals, supply via RPC. |

See [Contract Explorer](mini-apps/contract-explorer.md) for the interactive surface. Archive reads (non-`latest` blocks) require `GNOSIS_ARCHIVE_RPC_URL`.

---

## 8. Simulation sandbox (DuckDB + Parquet)

| Tool | Purpose |
|------|---------|
| `create_simulation_sandbox(sandbox_id, source_query, table_name, database)` | Spin up a DuckDB+Parquet copy of CH data. |
| `query_sandbox(sandbox_id, sql, max_rows)` | Free-form SQL — read OR write — against the sandbox. |
| `list_sandboxes()` | Diagnostic: id, table, row_count, bytes, idle_seconds. |
| `destroy_sandbox(sandbox_id)` | Tear down. Idempotent. |

See [Simulation Sandboxes](workflows/simulation-sandboxes.md).

---

## 9. Resume & state inspection

| Tool | Purpose |
|------|---------|
| `list_resumable_workflows(min_idle_seconds=0)` | All running / waiting_gate workflows the registry can resume. |
| `get_workflow_resume_hint(workflow_id)` | Latest hint payload (work / content / notes blocks + `next_action`). |
| `recompute_workflow_resume_hint(workflow_id)` | Force a re-scan over the full event log. |

See [Resumable Workflows](workflows/resumable-workflows.md) and [Memory & Resume](advanced/memory-and-resume.md).

---

## 10. Bridges, validators, on-chain helpers

| Tool | Purpose |
|------|---------|
| `get_bridge_flows_by_token(token)` | Cross-chain flow aggregates. |
| `get_deposit_events(...)` | Validator-deposit ledger. |
| `get_validator_balance_history(...)` / `get_validator_withdrawals(...)` | Consensus-layer accounting. |
| `get_liquidity_providers_by_token(token)` | LP positions across DEXes. |
| `get_token_transfers_for_address(address)` | Transfer history. |
| `get_gpay_wallet_activity(address)` | Gnosis Pay wallet detail. |

---

## 11. Documentation & reasoning

| Tool | Purpose |
|------|---------|
| `search_docs(query)` | Search this docs site (LLM-friendly markdown mirror). |
| `get_doc_chunk(path)` / `get_docs_context(...)` / `get_docs_overview()` | Doc retrieval. |
| `get_gnosis_chain_doc_chunk(path)` / `get_gnosis_chain_docs_context(query)` | Same for `docs.gnosischain.com`. |
| `set_thinking_mode(enabled)` | Toggle reasoning trace. |
| `log_reasoning(step, content)` | Manual trace event. |
| `get_reasoning_log(session_id)` | Retrieve a session trace. |
| `get_performance_stats(last_n)` | Aggregated tool latency. |
| `quality_metrics()` | Prometheus counter snapshot in markdown. |

---

## 12. Agent personas

| Tool | Purpose |
|------|---------|
| `get_agent_persona(role)` | Loads a persona's operational rules. The dispatcher (`cerebro_dispatcher`) is the front door for non-trivial requests. |

See [Agent Fleet](agents.md) for the persona catalogue and [Cerebro Dispatcher](dispatcher.md) for the routing rules.

---

## 13. Other & utility

| Tool | Purpose |
|------|---------|
| `system_status()` | Health check + version. |
| `list_custom_tools()` | Enumerate tools in this build. |
| `record_model_exclusion(model, reason)` | Required when skipping a single discovered model — `generate_report` enforces coverage. |
| `record_model_exclusion_batch(model_names, reason)` | Batch variant — exclude an explicit list in one call. |
| `exclude_models_by_prefix(prefix, reason)` | Sweep every discovered model whose name starts with `prefix`. |
| `exclude_module(module, reason)` | Sweep every discovered model in a dbt module (e.g. `circles`, `bridges`). |
| `exclude_all_discovered_except(keep, reason)` | Inverse: keep listed names, exclude all other discovered models. |
| `scaffold_dashboard_tab(...)` | Workspace-write: scaffold a new dashboard tab. |
| `get_help()` | Top-level navigation. |

---

## Tool-classification rules

Every tool is classified by risk class. See [Security & Audit](security.md) for the full rules.

| Risk class | Examples |
|---|---|
| `read_only` | `execute_query`, `search_models`, `generate_charts`, `list_resumable_workflows` |
| `server_state_write` | `save_query`, `generate_report`, `start_research_project`, `record_*` storyteller tools |
| `workspace_write` | `scaffold_dashboard_tab` |
| `subprocess` | `scaffold_dashboard_tab` (runs `pnpm build`) |
| `app_only` | `get_mini_app_rows`, `get_mini_app_state` (hidden from agents) |
