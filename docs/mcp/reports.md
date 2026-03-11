# Report Generation

Cerebro MCP can produce interactive, self-contained HTML reports with ECharts visualizations, narrative markdown, and a polished UI. Reports are rendered as native UI elements in Claude Desktop and VS Code, or opened in the default browser from Claude Code.

## Workflow Overview

Report generation follows a structured pipeline with three phases:

```
Phase 1: Analytics Reporter
  search_models  -->  describe_table  -->  execute_query  -->  generate_chart
  (discover)         (verify)              (sample)            (visualize)
       |                                                           |
       +---  Repeat for each metric  <-----------------------------+
                                                                   |
Phase 2: UI Designer                                               v
  Assemble markdown with {{chart:CHART_ID}} placeholders
  generate_report(title="...", content_markdown="...")
                                                                   |
Phase 3: Reality Checker                                           v
  Validate column names, date ranges, chart types, data integrity
```

## Step-by-Step Guide

### Step 1: Discover Relevant Models

Use `search_models` to find dbt models relevant to your report topic.

```
search_models("transactions daily")
search_models("validator active", module="consensus")
search_models("bridge netflow")
```

### Step 2: Verify Table Schemas

Before writing any SQL, always call `describe_table` to confirm exact column names. Column names in the dbt models are non-obvious and guessing will produce errors.

```
describe_table("api_execution_transactions_daily")
```

### Step 3: Sample Data

Optionally use `get_sample_data` to preview what the data looks like.

```
get_sample_data("api_execution_transactions_daily", limit=3)
```

### Step 4: Generate Charts

Call `generate_chart` for each metric. The tool executes the SQL query, builds an ECharts specification, and registers the chart in an in-memory registry (2-hour TTL). It returns a `chart_id` (e.g., `chart_1`, `chart_2`) used as a placeholder in the report.

```
generate_chart(
    sql="SELECT dt, txs FROM dbt.api_execution_transactions_daily WHERE dt >= today() - 30 ORDER BY dt",
    chart_type="line",
    x_field="dt",
    y_field="txs",
    title="Daily Transactions (30d)"
)
# Returns: chart_1

generate_chart(
    sql="SELECT dt, active_validators FROM dbt.api_consensus_validators_active_daily WHERE dt >= today() - 30 ORDER BY dt",
    chart_type="area",
    x_field="dt",
    y_field="active_validators",
    title="Active Validators (30d)"
)
# Returns: chart_2
```

### Step 5: Assemble the Report

Call `generate_report` with a title and markdown content. Use `{{chart:CHART_ID}}` placeholders where charts should appear. The markdown supports standard formatting: headings, lists, bold, italic, tables, and code blocks.

```
generate_report(
    title="Weekly Gnosis Chain Report",
    content_markdown="""
## Network Activity

Transaction volume over the past 30 days shows consistent growth.

{{chart:chart_1}}

Key observations:
- Average daily transactions: 145,000
- Peak day: March 7 with 182,000 transactions

## Validator Set

The validator set continues to grow with strong attestation participation.

{{chart:chart_2}}

- Active validators: 150,234
- Net new validators this week: +312
"""
)
```

### Step 6: Output

The report is saved as a standalone HTML file at `~/.cerebro/reports/` and rendered according to the client:

| Client | Rendering |
|--------|-----------|
| Claude Desktop | Native MCP App iframe embedded in the conversation |
| VS Code | MCP App rendered in the chat panel |
| Claude Code | Summary text with a `file://` link; opens in default browser |

## Chart Types

### Line Chart

Best for time series trends and continuous data.

```
generate_chart(
    sql="SELECT dt, txs FROM ...",
    chart_type="line",
    x_field="dt",
    y_field="txs",
    title="Daily Transactions"
)
```

### Area Chart

Similar to line charts but with filled area beneath, emphasizing volume.

```
generate_chart(
    sql="SELECT dt, active_validators FROM ...",
    chart_type="area",
    x_field="dt",
    y_field="active_validators",
    title="Validator Growth"
)
```

### Bar Chart

Best for categorical comparisons and rankings.

```
generate_chart(
    sql="SELECT client_name, node_count FROM ...",
    chart_type="bar",
    x_field="client_name",
    y_field="node_count",
    title="Client Distribution"
)
```

### Pie Chart

Best for proportional distribution of a single dimension.

```
generate_chart(
    sql="SELECT cloud_provider, node_count FROM ...",
    chart_type="pie",
    x_field="cloud_provider",
    y_field="node_count",
    title="Cloud Provider Share"
)
```

### Number Display

Single KPI or headline metric, rendered as a large number with optional delta.

```
generate_chart(
    sql="SELECT count() as total_txs FROM ...",
    chart_type="numberDisplay",
    y_field="total_txs",
    title="Total Transactions"
)
```

## Multi-Series Charts

Use the `series_field` parameter to split data into multiple series on the same chart. This works with line, area, and bar chart types.

```
generate_chart(
    sql="SELECT dt, client_name, node_count FROM dbt.api_p2p_nodes_by_client_daily WHERE dt >= today() - 30 ORDER BY dt",
    chart_type="line",
    x_field="dt",
    y_field="node_count",
    series_field="client_name",
    title="Node Count by Client"
)
```

## Report UI Features

Generated reports include a React-based UI with the following features:

- **Collapsible sidebar** (224px expanded / 56px collapsed) with section navigation derived from markdown `##` headings
- **Light/dark theme** toggle (light by default), syncs with the MCP host preference
- **Gnosis owl watermark** on every chart (theme-aware SVG)
- **Chart toolbar**: save chart as PNG image (2x resolution), view raw data as a table
- **Value coloring**: positive values (`+`) rendered in green, negative values (`-`) in red
- **Responsive layout** that adapts to viewport width
- **Print-friendly** rendering with sidebar hidden when printing

## Managing Reports

### List Saved Reports

```
list_reports()
```

Returns a table of saved reports with IDs, dates, file sizes, and `file://` links.

### Reopen a Report

```
open_report("abc12345")
```

Accepts the full UUID or the 8-character short ID shown in report summaries.

### Report Storage

Reports are saved as self-contained HTML files at `~/.cerebro/reports/` (configurable via `CEREBRO_REPORT_DIR`). Each file embeds all chart data as JSON, so reports can be shared and opened in any browser without a server.

## Agent Personas

For complex reports, Cerebro MCP provides three agent personas that define strict operational rules and success metrics:

| Persona | Role | Loaded via |
|---------|------|------------|
| Analytics Reporter | Data discovery, schema verification, query writing, chart generation | `get_agent_persona("analytics_reporter")` |
| UI Designer | Chart type selection, markdown layout, report structure | `get_agent_persona("ui_designer")` |
| Reality Checker | SQL validation, data integrity, chart spec review, formatting QA | `get_agent_persona("reality_checker")` |

Each persona provides specific formatting rules, example patterns, and zero-tolerance constraints (e.g., no guessed column names, no charts without titles, minimum two `##` sections per report).
