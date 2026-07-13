# Grafana Publishing

Publish ClickHouse-backed Grafana dashboards straight from a conversation. The model declares a `GrafanaDashboardDef` (intent: title, UID, sections, panels with roles and SQL); a deterministic compiler produces the Grafana JSON; publishing goes through Grafana's HTTP API. Backed by `src/cerebro_mcp/tools/visualization/grafana.py`.

This is the one tool family that **writes outside the server boundary** — `publish_grafana_dashboard` is classified `external_write` in the [security registry](../security.md), distinct from `server_state_write` because the side effect lands in an external system.

## Enabling

Registration is gated by `GRAFANA_TOOLS_ENABLED` (default off) — when the flag is off, none of the tools exist. Publishing additionally requires the connection settings:

| Variable | Purpose |
|---|---|
| `GRAFANA_URL` | Grafana base URL |
| `GRAFANA_API_TOKEN` | Service-account token (used as a Bearer header; scrubbed from any error output) |
| `GRAFANA_CLICKHOUSE_DATASOURCE_UID` | UID of the ClickHouse datasource panels query |
| `GRAFANA_CLICKHOUSE_DATASOURCE_TYPE` | Datasource plugin type (default `grafana-clickhouse-datasource`) |
| `GRAFANA_FOLDER_UID` | Target folder; empty publishes to the default (General) folder |

Compiler guardrails from `config.py`: `GRAFANA_MAX_PANELS=30`, `GRAFANA_MIN_REFRESH_SECONDS=60`, `GRAFANA_SCHEMA_VERSION=41`, `GRAFANA_REQUEST_TIMEOUT_SECONDS=20`.

## The tools

| Tool | Purpose |
|---|---|
| `preview_grafana_dashboard(dashboard)` | ASCII sketch of the layout (widths proportional to the real 24-column grid) plus the metric each card shows — **without publishing**. Always show this to the user for approval first. |
| `validate_grafana_dashboard(dashboard)` | Two-layer check: every panel's SQL (Grafana macros substituted) passes the same read-only guards as `execute_query`; then, if Grafana is configured, every panel executes against the live datasource and per-panel row counts / errors are reported. |
| `verify_grafana_dashboard(dashboard)` | Just the live check: run every panel through `POST /api/ds/query` and report per-panel rows / errors. Catches SQL that errors against the datasource and panels that return no data — things the local lint cannot see. |
| `publish_grafana_dashboard(dashboard)` | Compile and publish. Validates, verifies live data, then POSTs to `/api/dashboards/db`. Returns the dashboard URL. |
| `get_grafana_dashboard(uid)` | Fetch metadata (title, tags, version, folder, URL) for a published dashboard. |

## Publish semantics

- **Idempotent by UID.** Re-publishing the same `uid` updates the existing dashboard in place (Grafana versions it); a new UID creates a new dashboard.
- **Tag-guarded overwrite.** Dashboards published by this server carry the `cerebro-mcp` tag. Publishing refuses to overwrite an existing dashboard *without* that tag unless the spec sets `force_overwrite=true` — so a human-edited dashboard is never silently clobbered.
- **No broken or empty panels.** Publish runs the live per-panel verification first and refuses if any panel errors, or returns zero rows (unless the spec sets `allow_empty=true`).

## Recommended flow

```text
get_agent_persona("grafana_architect")        # dashboard-composition rules
preview_grafana_dashboard(spec)               # show the sketch, get user approval
validate_grafana_dashboard(spec)              # SQL guards + live data check
publish_grafana_dashboard(spec)               # → "Published dashboard '<uid>' (version N). View: <url>"
```

The `grafana_architect` persona ([Agent Fleet](../agents.md)) encodes the composition rules — mixed-audience layout, panel roles, units, and section ordering — and should be loaded before designing a non-trivial dashboard.

## See also

- [Security & Audit](../security.md) — the `external_write` risk class
- [Setup — Feature flags](../setup.md#feature-flags) — the full variable list
- [Observability](../observability.md) — the server's *own* Grafana dashboard (metrics about Cerebro, not published by it)
