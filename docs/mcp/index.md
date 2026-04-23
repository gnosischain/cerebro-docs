# Cerebro MCP Server

Cerebro MCP is a [Model Context Protocol](https://modelcontextprotocol.io/) server that connects AI assistants to Gnosis Chain's on-chain analytics infrastructure. It provides over 30 tools for querying a ClickHouse data warehouse, exploring ~400 dbt models, generating interactive visualizations, and assembling standalone HTML reports -- all through natural language.

## What is MCP?

The Model Context Protocol (MCP) is an open standard that allows AI applications (hosts) to connect to external data sources and tools (servers) through a unified interface. Instead of building custom integrations for each AI assistant, a single MCP server can serve Claude Desktop, VS Code Copilot, Claude Code, and any other MCP-compatible client.

## Architecture

```
                      +-----------------------------------------+
                      |           MCP Host (Client)             |
                      | Claude Desktop / VS Code / Claude Code  |
                      +-------------------+---------------------+
                                          | MCP Protocol
                                          | (stdio / SSE)
                      +-------------------v---------------------+
                      |         cerebro-mcp (FastMCP)           |
                      |                                         |
                      |  +----------+ +----------+ +--------+  |
                      |  |  Query   | |  Schema  | |  dbt   |  |
                      |  |  Tools   | |  Tools   | |  Tools |  |
                      |  +----+-----+ +----+-----+ +---+----+  |
                      |       |            |           |        |
                      |  +----v------------v-----------v----+   |
                      |  |       ClickHouse Client          |   |
                      |  |   (clickhouse-connect + cache)   |   |
                      |  +----------------+-----------------+   |
                      |                   |                     |
                      |  +--------+-------+--------+            |
                      |  | Visualization | Reasoning|           |
                      |  | Tools         | Tracing  |           |
                      |  +-------+-------+---------+            |
                      |          |                              |
                      |  +-------v----------------------------+ |
                      |  | React Report UI (Vite bundle)      | |
                      |  | ECharts + Sidebar + Theme toggle   | |
                      |  +------------------------------------+ |
                      +-------------------+---------------------+
                                          |
                      +-------------------v---------------------+
                      |     ClickHouse Cloud (Gnosis Chain)     |
                      |                                         |
                      |  execution | consensus | crawlers_data  |
                      |  nebula    | nebula_discv4 | dbt        |
                      +---------------------------------------------+
```

## Transport Modes

Cerebro MCP supports two transport mechanisms:

### stdio (Default)

The default transport for local use with Claude Desktop and Claude Code. The MCP host spawns the server as a subprocess and communicates over stdin/stdout.

```bash
cerebro-mcp
```

### SSE / HTTP (Remote)

Server-Sent Events transport for remote deployments. Starts an HTTP server (uvicorn) that MCP clients connect to over the network.

```bash
cerebro-mcp --sse
# Listens on http://0.0.0.0:8000 by default
```

Configure the bind address and port via `FASTMCP_HOST` and `FASTMCP_PORT` environment variables.

The hosted team instance is available at `mcp.analytics.gnosis.io` with Bearer token authentication.

## Key Capabilities

### Agent Fleet

- **23 agent personas** organised in three tiers — top-level dispatcher, workflow leads, domain specialists
- Gated handoffs between personas (e.g. MMM `generate_report` blocked until `mmm_causal_reviewer` returns PASS)
- See [Agent Fleet](agents.md), [Cerebro Dispatcher](dispatcher.md), and [Marketing Mix Modeling](mmm.md)

### Data Exploration

- Query 6 ClickHouse databases containing Gnosis Chain data
- Browse ~400 dbt models across 8 modules (execution, consensus, bridges, p2p, contracts, ESG, probelab, crawlers)
- Inspect table schemas with column types and dbt-generated descriptions
- Resolve over 5.3 million address labels from Dune Analytics
- Look up token metadata (address, decimals, price availability)

### Visualization and Reporting

- Generate ECharts visualizations (line, area, bar, pie, number display)
- Assemble multi-chart interactive reports with markdown narrative
- Reports render as native UI in Claude Desktop/VS Code, or open in browser from Claude Code
- Save reports as standalone HTML files at `~/.cerebro/reports/`

### Safety

- All SQL execution is read-only (only `SELECT`, `EXPLAIN`, `DESCRIBE`, `SHOW`)
- Write operations (`INSERT`, `UPDATE`, `DELETE`, `DROP`, etc.) are blocked at the validation layer
- Maximum 10,000 rows per query, 30-second timeout, auto-appended `LIMIT` clauses
- Identifier validation prevents SQL injection

### Reasoning and Tracing

- Automatic capture of every tool call with timestamps, durations, and outcomes
- Sensitive data (passwords, tokens) automatically redacted from traces
- 30-day trace retention with session-level performance aggregation

## Next Steps

- [Available Tools](tools.md) -- Complete reference of all 30+ tools
- [Agent Fleet](agents.md) -- 23 personas loadable via `get_agent_persona(role)`
- [Cerebro Dispatcher](dispatcher.md) -- Top-level intent triage + gated routing
- [Marketing Mix Modeling (MMM)](mmm.md) -- Sector contribution / ROI attribution with causal-DAG gate
- [MMM User Guide](mmm-user-guide.md) -- Practical playbook for day-to-day MMM usage (prompt recipes, Sector Readiness Matrix, coefficient interpretation, FAQ)
- [Report Generation](reports.md) -- How to build interactive reports
- [Setup Guide](setup.md) -- Connect Cerebro MCP to your AI assistant
- [Model Catalog](../models/index.md) -- Explore the dbt model library
