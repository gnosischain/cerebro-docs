# Security & Audit

Cerebro MCP includes a detection-first security layer that classifies tool risk, detects suspicious invocations, and maintains an append-only audit trail. The security layer is **observation-only** — it logs and measures but never blocks tool execution.

## Why This Exists

LLM supply-chain attacks are a real and growing threat. Research such as ["Your Agent Is Mine" (arXiv:2604.08407)](https://arxiv.org/abs/2604.08407) demonstrates that intermediary routers between clients and LLM providers can inject malicious tool calls that reach servers unverified. Cerebro's security layer makes such attacks visible and auditable.

## Tool Risk Classification

Every tool registered with Cerebro MCP is assigned a risk class:

| Risk Class | Description | Example Tools |
|---|---|---|
| `read_only` | No side effects | `execute_query`, `describe_table`, `search_models`, `generate_charts`, `quick_chart` |
| `server_state_write` | Persists state to disk or memory | `save_query`, `generate_report`, `start_research_project`, `storyteller_record_*` |
| `workspace_write` | Writes to the workspace filesystem | `scaffold_dashboard_tab` |
| `subprocess` | Spawns external processes | `scaffold_dashboard_tab` |
| `app_only` | Hidden from the model; only callable by the frontend | `get_mini_app_rows`, `get_mini_app_state` |

!!! note "Unknown tools"
    Dynamically registered tools (e.g., custom query tools from YAML) that are not in the static registry default to `read_only` and are flagged as `unknown_tool` in the audit log.

### Risk Priority

When a tool has multiple risk classes, the **primary** class is determined by severity: `subprocess` > `workspace_write` > `app_only` > `server_state_write` > `read_only`.

## Suspicious-Call Detection

The security layer flags calls as suspicious in three cases:

| Flag | Trigger |
|---|---|
| `app_only_tool_called` | An `app_only` tool is invoked — these should only come from the frontend SDK |
| `workspace_write_via_sse` | A filesystem-writing or process-spawning tool is called over the SSE (remote) transport |
| `unknown_tool` | The tool name is not in the static risk registry |

!!! warning "Suspicious does not mean blocked"
    In `log_only` mode, suspicious calls are logged and counted but **not blocked**. This allows operators to establish baselines and tune thresholds before enabling enforcement in a future phase.

## Audit Log

Every tool call — successful or failed, suspicious or not — produces an append-only JSONL audit event.

### Storage

- **Directory:** configured via `MCP_SECURITY_LOG_DIR` (default `.cerebro/security_audit/`)
- **File naming:** `security_audit_YYYY-MM-DD.jsonl` (UTC date, daily rotation)
- **Thread-safe:** writes are serialized via a lock for concurrent SSE sessions

### Event Schema

```json
{
  "timestamp": "2026-04-10T14:32:01.123456+00:00",
  "transport": "stdio",
  "auth_present": false,
  "tool_name": "execute_query",
  "risk_class": "read_only",
  "visibility": "public",
  "redacted_arg_summary": "{\"sql\":\"SELECT count()...\",\"database\":\"dbt\"}",
  "arg_hash": "a1b2c3d4e5f6...",
  "result_hash": "f6e5d4c3b2a1...",
  "duration_ms": 142,
  "success": true,
  "suspicious_flags": []
}
```

| Field | Description |
|---|---|
| `transport` | `stdio` (local) or `sse` (remote) |
| `auth_present` | Whether `MCP_AUTH_TOKEN` is configured in the environment |
| `risk_class` | Primary risk class of the tool |
| `visibility` | `public` (model-visible) or `app_only` (frontend-only) |
| `redacted_arg_summary` | First 200 characters of redacted JSON arguments |
| `arg_hash` / `result_hash` | SHA-256 of canonical JSON of redacted payloads |
| `suspicious_flags` | List of flag strings; empty when the call is not suspicious |

### Redaction

Arguments and results are redacted before hashing using the same redaction engine as the reasoning trace system. Keys matching `password`, `token`, `api_key`, `secret`, `authorization`, `private_key`, and related patterns are replaced with `***REDACTED***`.

## Artifact Provenance

When remote artifacts (dbt manifest, catalog, semantic registry, docs index) are loaded or reloaded, the server emits a structured `artifact_reload` log event with the artifact label, source (`local`/`remote`), content hash (SHA-256), ETag, and Last-Modified header. These events are queryable in Loki:

```logql
{namespace="analytics-preview", pod=~"cerebro-mcp-.*"} |= "\"event\":\"artifact_reload\""
```

## Report Endpoint Auth Audit

The `/reports/{id}` endpoint logs every access attempt when `MCP_AUTH_TOKEN` is configured:

- Auth method: `bearer`, `query_token`, or `none`
- Success/denial status
- Report ID

Denied attempts increment `cerebro_report_token_auth_total{status="denied"}`.

## Configuration

| Variable | Default | Description |
|---|---|---|
| `MCP_SECURITY_POLICY_MODE` | `log_only` | Security policy mode. Future: `warn`, `enforce` |
| `MCP_SECURITY_LOG_DIR` | `.cerebro/security_audit` | Daily JSONL audit file directory |
| `MCP_EXPECTED_MANIFEST_SHA256` | *(empty)* | Optional SHA-256 pin for the dbt manifest; empty = disabled |

## Prometheus Metrics

Security counters are exposed at the `/metrics` endpoint and visualized in the [Grafana dashboard](observability.md#grafana-dashboard):

| Metric | Labels | Description |
|---|---|---|
| `cerebro_security_high_risk_tool_calls_total` | `tool_name`, `risk_class`, `transport` | Non-read_only tool invocations |
| `cerebro_security_suspicious_calls_total` | `tool_name`, `flag_type` | Suspicious call flags |
| `cerebro_security_app_only_calls_total` | `tool_name`, `transport` | App-only tool invocations |
| `cerebro_report_token_auth_total` | `status` | Report endpoint auth events |

## Architecture

```
                    Tool Call
                        |
                        v
            +------------------------+
            |  _wrapped_call_tool()  |  (tools/reasoning.py)
            |  - timing              |
            |  - tracing             |
            |  - observability       |
            +----------+-------------+
                       |
                       v
            +------------------------+
            |   assess_tool_call()   |  (security.py)
            |  - risk lookup         |
            |  - flag detection      |
            |  - hash computation    |
            |  - JSONL audit write   |
            |  - Prometheus counters |
            +------------------------+
                       |
            (never blocks — try/except)
```

The security assessment runs **after** the tool has executed. It is wrapped in `try/except Exception` to guarantee it never interferes with tool execution. If the security layer itself fails, a debug-level log is emitted and the tool result is returned unchanged.

## Future: Enforcement Phase

The `MCP_SECURITY_POLICY_MODE` setting supports future enforcement modes:

- **`warn`**: Log suspicious calls and emit warnings in tool responses, but do not block
- **`enforce`**: Block calls that match configurable rules (e.g., workspace writes over SSE without explicit authorization)

The JSONL audit trail and Prometheus counters provide the observability foundation needed to establish baselines and tune enforcement thresholds before enabling them.
