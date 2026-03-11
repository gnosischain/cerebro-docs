# Available Tools

Cerebro MCP exposes over 30 tools organized into seven categories. All tools are read-only and operate within the safety boundaries described in the [MCP Overview](index.md).

## Query and Schema Tools

Tools for executing SQL queries and inspecting database schemas.

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `execute_query` | Run a read-only SQL query against ClickHouse. Returns results as a formatted table with metadata. | `sql` (required), `database` (default: `dbt`), `max_rows` (default: 100, max: 10000) |
| `start_query` | Submit a long-running query for asynchronous execution. Returns a query ID for polling. Use for queries that may exceed the 30-second timeout. | `sql` (required), `database` (default: `dbt`), `max_rows` (default: 100) |
| `get_query_results` | Check the status and retrieve results of an async query submitted via `start_query`. | `query_id` (required) |
| `explain_query` | Show the ClickHouse execution plan for a query without running it. Useful for optimizing query performance. | `sql` (required), `database` (default: `dbt`) |
| `list_tables` | List all tables in a ClickHouse database with engine type, row counts, and size. | `database` (required), `name_pattern` (optional LIKE pattern, e.g., `'stg_%'`) |
| `describe_table` | Get the column schema for a specific table including column names, types, default values, and dbt-generated descriptions. | `table` (required), `database` (default: `dbt`) |
| `get_sample_data` | Retrieve sample rows from a table to understand data shape and representative values. | `table` (required), `database` (default: `dbt`), `limit` (default: 5, max: 20) |

!!! warning "Column Name Verification"
    Always call `describe_table` or `get_model_details` before writing queries. Column names are non-obvious (e.g., `value` not `staked_gno`, `cnt` not `count`, `txs` not `transactions`). Never guess column names.

## dbt Model Tools

Tools for discovering and inspecting the ~400 dbt models in the Gnosis Analytics platform.

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `search_models` | Search dbt models by name, description, or tags. Supports multi-word queries with independent word matching. | `query` (search term), `tags` (optional list), `module` (optional: `execution`, `consensus`, `contracts`, `p2p`, `bridges`, `ESG`, `probelab`, `crawlers_data`), `limit` (default: 50) |
| `get_model_details` | Get comprehensive details about a dbt model including SQL code, column descriptions, materialization type, and upstream/downstream dependencies. | `model_name` (required, exact name) |

### Model Search Examples

```
search_models("transactions daily")
search_models(module="execution")
search_models(tags=["production"])
search_models("validator", module="consensus")
```

## Visualization Tools

Tools for creating ECharts visualizations and assembling interactive reports.

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `generate_chart` | Execute a query and generate an ECharts visualization specification. Returns a chart ID for use in reports. | `sql` (required), `chart_type` (`line`, `area`, `bar`, `pie`, `numberDisplay`; default: `line`), `x_field`, `y_field`, `series_field` (optional, for multi-series), `title`, `database` (default: `dbt`), `max_rows` (default: 500) |
| `generate_report` | Assemble an interactive report from markdown content with `{{chart:CHART_ID}}` placeholders. Renders as native UI in MCP hosts or saves as standalone HTML. | `title` (required), `content_markdown` (required) |
| `list_charts` | List all charts registered in the current session with their IDs, titles, and types. | _(none)_ |
| `open_report` | Reopen a previously generated report by its full UUID or 8-character short ID. | `report_ref` (required) |
| `list_reports` | List all saved reports on disk, sorted newest-first with file links and sizes. | `limit` (default: 20) |

### Supported Chart Types

| Type | Use Case | Required Fields |
|------|----------|-----------------|
| `line` | Time series trends, continuous data | `x_field`, `y_field` |
| `area` | Time series with volume emphasis | `x_field`, `y_field` |
| `bar` | Categorical comparisons, rankings | `x_field`, `y_field` |
| `pie` | Proportional distribution | `x_field` (labels), `y_field` (values) |
| `numberDisplay` | Single KPI or headline number | `y_field` |

## Metadata Tools

Tools for system information, address resolution, and token lookups.

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `list_databases` | List all available ClickHouse databases with descriptions and table counts. | _(none)_ |
| `system_status` | Show server health: ClickHouse connectivity, dbt manifest state, and configuration. | _(none)_ |
| `resolve_address` | Look up an address label or search for addresses by name using the Dune label directory (5.3M entries). | `address_or_name` (required, either `0x...` address or keyword like `'Uniswap'`) |
| `get_token_metadata` | Look up token metadata including contract address, decimals, name, and price data availability. | `symbol_or_address` (required, e.g., `'GNO'`, `'USDC'`, or `0x...`) |
| `search_models_by_address` | Find dbt models related to a specific smart contract address. Searches contract whitelist, ABI registry, and model SQL. | `contract_address` (required, `0x...`) |
| `search_docs` | Search across platform documentation, SQL guide, address directory, metric definitions, and query cookbook. | `topic` (required, e.g., `'partition pruning'`, `'bridge'`) |

## Saved Query Tools

Tools for persisting and reusing queries across sessions.

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `save_query` | Save a query for later reuse. Validates SQL before saving. | `name` (required, alphanumeric + underscores), `sql` (required), `database` (default: `dbt`), `description` (optional), `overwrite` (default: false) |
| `list_saved_queries` | List all saved queries with names, databases, and descriptions. | _(none)_ |
| `run_saved_query` | Execute a previously saved query by name. | `name` (required), `max_rows` (default: 100) |

Saved queries are stored at `~/.cerebro-mcp/` as individual files.

## Reasoning and Tracing Tools

Tools for capturing reasoning steps and analyzing performance across sessions.

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `set_thinking_mode` | Enable or disable reasoning capture mode. When enabled, creates a new session trace. | `enabled` (required, boolean) |
| `log_reasoning` | Record a reasoning step at a key decision point for audit and analysis. Only active when thinking mode is enabled. | `step` (required, short label), `content` (required, reasoning explanation), `agent` (optional), `action` (optional), `duration_ms`, `success`, `input_summary`, `output_summary`, `error` |
| `get_reasoning_log` | Retrieve the reasoning trace for a session. | `session_id` (optional, defaults to current session) |
| `get_performance_stats` | Aggregate performance metrics across recent sessions for benchmarking. | `last_n` (default: 10) |

## Agent Persona Tools

Tools for loading specialized agent personas used in multi-phase report generation.

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `get_agent_persona` | Fetch operational rules, success metrics, and formatting guidelines for a specific agent role. | `role` (required: `analytics_reporter`, `ui_designer`, or `reality_checker`) |

### Agent Roles

| Role | Responsibility |
|------|---------------|
| `analytics_reporter` | Data discovery, schema verification, query execution, chart generation |
| `ui_designer` | Chart type selection, markdown layout, report assembly with `generate_report` |
| `reality_checker` | SQL validation, data integrity checks, chart spec verification, formatting QA |

## Target Databases

All query tools accept a `database` parameter. Available databases:

| Database | Content |
|----------|---------|
| `dbt` | Materialized dbt models (~400 tables). **Default and recommended.** |
| `execution` | Raw execution layer: blocks, transactions, logs, traces, contracts |
| `consensus` | Raw consensus layer: validators, attestations, rewards, deposits |
| `crawlers_data` | External data: Dune labels, prices, bridge flows, GNO supply |
| `nebula` | P2P network crawl data (discv5) |
| `nebula_discv4` | P2P discovery v4 protocol data |
