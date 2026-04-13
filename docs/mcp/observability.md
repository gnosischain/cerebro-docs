# Observability

Cerebro MCP provides comprehensive observability through Prometheus metrics, structured JSON logs, reasoning traces, and a ready-to-import Grafana dashboard.

## Grafana Dashboard

A complete Grafana dashboard is maintained at [`grafana/cerebro-mcp-observability.json`](https://github.com/gnosischain/cerebro-mcp/blob/main/grafana/cerebro-mcp-observability.json) in the Cerebro MCP repository.

### Importing

1. Open your Grafana instance
2. Go to **Dashboards > Import**
3. Upload or paste the JSON file
4. Configure the template variables to match your Prometheus/Loki datasources

### Dashboard Sections

The dashboard contains 9 row sections with 61 panels:

#### Overview
Kubernetes deployment health: desired/available replicas, active pods, total restarts, pod/node mapping, container images.

#### HTTP / SSE
HTTP transport metrics: request rate by path and status code, p95 latency by path, in-progress requests, 4xx/5xx error rates.

#### MCP Internals
MCP protocol metrics: request rate by method, p95 MCP latency, tool call rate by tool and status, p95 tool latency, top 10 failing tools.

#### Security Audit
Security detection metrics:

- **KPI stats**: suspicious calls, high-risk tool calls, app-only calls, report auth denials
- **Trends**: suspicious calls over time by flag type, high-risk calls by risk class (stacked area)
- **Breakdown**: top high-risk tools by volume (bar gauge)
- **Live log**: security audit events from Loki

See [Security & Audit](security.md) for details on the risk classification and detection system.

#### Tool Usage Details
Granular tool analytics:

- **Top 15 tools by volume** (bar gauge)
- **Tool call distribution** (pie chart)
- **Error rate by tool** (timeseries)
- **Slowest tools** p99 latency (table)

#### Semantic Layer
Semantic execution health:

- **State**: semantic enabled flag, registry model/metric counts, snapshot age with yellow (>5 min) / red (>10 min) thresholds
- **Query flow**: semantic query attempts by result (stacked), route decisions (pie chart)
- **Performance**: end-to-end semantic latency p95, planner failures by reason

#### ClickHouse
Database query metrics: query rate by database/status, p95 latency, error rate, p95 rows returned.

#### Pod Resources
Container resource usage: CPU usage/requests/limits, CPU throttling, memory usage/requests/limits, network RX/TX, pod restarts over time.

#### Logs
Structured log exploration from Loki:

- Warnings/errors volume timeline
- Live structured logs (all events)
- Tool call logs (`mcp_tool_call` events)
- MCP request logs (`mcp_request` events)
- ClickHouse query logs
- Failed events
- Security audit log (`security_audit` events)
- Artifact reload log (`artifact_reload` events)

### Template Variables

| Variable | Type | Default | Description |
|---|---|---|---|
| `$prometheus` | Datasource | `thanos-gnosisanalytics` | Prometheus datasource |
| `$loki` | Datasource | `loki-gnosisanalytics` | Loki datasource |
| `$cluster` | Query | *(auto)* | Kubernetes cluster |
| `$namespace` | Query | `analytics-preview` | Kubernetes namespace |
| `$workload` | Custom | `cerebro-mcp` | Deployment name |
| `$pod` | Query | All | Pod selector |

## Prometheus Metrics Reference

All metrics are exposed at the `/metrics` endpoint (unauthenticated, exempt from bearer auth middleware in SSE mode).

### HTTP Transport

| Metric | Type | Labels |
|---|---|---|
| `cerebro_http_requests_total` | Counter | `method`, `path`, `status` |
| `cerebro_http_request_duration_seconds` | Histogram | `method`, `path` |
| `cerebro_http_requests_in_progress` | Gauge | `method`, `path` |

### MCP Protocol

| Metric | Type | Labels |
|---|---|---|
| `cerebro_mcp_requests_total` | Counter | `method`, `status` |
| `cerebro_mcp_request_duration_seconds` | Histogram | `method` |
| `cerebro_mcp_tool_calls_total` | Counter | `tool_name`, `status` |
| `cerebro_mcp_tool_duration_seconds` | Histogram | `tool_name` |

### ClickHouse

| Metric | Type | Labels |
|---|---|---|
| `cerebro_clickhouse_query_duration_seconds` | Histogram | `database`, `audience`, `fetch_mode`, `status` |
| `cerebro_clickhouse_query_errors_total` | Counter | `database`, `audience` |
| `cerebro_clickhouse_rows_returned` | Histogram | `database`, `audience` |

### Security Audit

| Metric | Type | Labels |
|---|---|---|
| `cerebro_security_high_risk_tool_calls_total` | Counter | `tool_name`, `risk_class`, `transport` |
| `cerebro_security_suspicious_calls_total` | Counter | `tool_name`, `flag_type` |
| `cerebro_security_app_only_calls_total` | Counter | `tool_name`, `transport` |
| `cerebro_report_token_auth_total` | Counter | `status` |

### Semantic Layer

| Metric | Type | Labels |
|---|---|---|
| `semantic_tool_calls_total` | Counter | `tool_name`, `status`, `agent_role`, `entrypoint` |
| `semantic_query_attempts_total` | Counter | `planner_mode`, `attempt`, `result`, `agent_role` |
| `semantic_query_repairs_total` | Counter | `repair_action`, `error_class`, `agent_role` |
| `semantic_planner_failures_total` | Counter | `reason`, `planner_mode`, `agent_role` |
| `semantic_fallback_total` | Counter | `fallback_target`, `reason`, `agent_role` |
| `semantic_route_total` | Counter | `route`, `mode` |
| `semantic_bypass_total` | Counter | `stage`, `reason` |
| `semantic_snapshot_reload_total` | Counter | `status` |
| `semantic_snapshot_stale_total` | Counter | `reason` |
| `semantic_planner_latency_seconds` | Histogram | `planner_mode` |
| `semantic_sql_compile_latency_seconds` | Histogram | `planner_mode` |
| `semantic_query_end_to_end_latency_seconds` | Histogram | `planner_mode`, `repair_state` |
| `semantic_snapshot_reload_latency_seconds` | Histogram | `status` |
| `semantic_snapshot_age_seconds` | Gauge | *(none)* |
| `semantic_registry_models_total` | Gauge | `semantic_status` |
| `semantic_registry_metrics_total` | Gauge | `quality_tier` |
| `semantic_registry_relationships_total` | Gauge | `quality_tier` |
| `semantic_semantic_enabled` | Gauge | `state` |

## Structured JSON Logging

All server logs are emitted as single-line JSON via `JsonFormatter` to stderr. Each line includes:

```json
{
  "timestamp": "2026-04-10T14:32:01.123456+00:00",
  "level": "INFO",
  "logger": "cerebro_mcp.tools.reasoning",
  "message": "mcp_tool_call",
  "event": "mcp_tool_call",
  "tool_name": "execute_query",
  "duration_ms": 142,
  "success": true
}
```

### Event Types

| Event | Source | When |
|---|---|---|
| `mcp_tool_call` | `tools/reasoning.py` | Every tool invocation |
| `mcp_request` | `tools/reasoning.py` | Low-level MCP protocol requests |
| `clickhouse_query` | `clickhouse_client.py` | ClickHouse query execution |
| `security_audit` | `security.py` | Suspicious tool calls (non-empty flags) |
| `report_token_auth` | `server.py` | Report endpoint access attempts |
| `artifact_reload` | `artifact_loader.py` | Artifact load/reload with hash and source |
| `transport_selected` | `server.py` | Server startup transport choice |

### Useful Loki Queries

=== "All structured logs"

    ```logql
    {namespace="$namespace", pod=~"cerebro-mcp-.*"} |= "\"timestamp\":\""
    ```

=== "Tool calls"

    ```logql
    {namespace="$namespace", pod=~"cerebro-mcp-.*"} |= "\"event\":\"mcp_tool_call\""
    ```

=== "Security events"

    ```logql
    {namespace="$namespace", pod=~"cerebro-mcp-.*"} |= "\"event\":\"security_audit\""
    ```

=== "Artifact reloads"

    ```logql
    {namespace="$namespace", pod=~"cerebro-mcp-.*"} |= "\"event\":\"artifact_reload\""
    ```

=== "Failed events"

    ```logql
    {namespace="$namespace", pod=~"cerebro-mcp-.*"} |= "\"success\":false"
    ```

=== "Errors and warnings"

    ```logql
    {namespace="$namespace", pod=~"cerebro-mcp-.*"} |~ "\"level\":\"(ERROR|WARNING)\""
    ```

## Reasoning Traces

The reasoning/tracing system captures detailed tool execution traces for debugging and performance analysis. Traces are separate from the security JSONL audit log.

### What is captured

- Tool name, redacted arguments, and redacted result
- Timing (start timestamp, duration)
- Success/failure status with error details
- Low-level MCP request/response pairs

### Storage

Traces are persisted as session JSON files in `THINKING_LOG_DIR` (default `.cerebro/logs/`). Retention is controlled by `THINKING_LOG_RETENTION_DAYS` (default 30 days).

### Tools

| Tool | Description |
|---|---|
| `set_thinking_mode(enabled)` | Start or stop a trace session |
| `log_reasoning(step, content)` | Add a manual reasoning step |
| `get_reasoning_log(session_id)` | Retrieve a full session trace |
| `get_performance_stats(last_n)` | Aggregate performance metrics across recent sessions |

### Configuration

| Variable | Default | Description |
|---|---|---|
| `THINKING_MODE_ENABLED` | `True` | Enable the reasoning trace system |
| `THINKING_ALWAYS_ON` | `True` | Auto-capture tool calls without explicit `set_thinking_mode` |
| `THINKING_LOG_DIR` | `.cerebro/logs` | Trace storage directory |
| `THINKING_LOG_RETENTION_DAYS` | `30` | Automatic trace cleanup after N days |
