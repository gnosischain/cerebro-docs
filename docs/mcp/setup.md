# Setup Guide

This guide covers how to install Cerebro MCP and connect it to Claude Desktop, VS Code, and Claude Code.

## Prerequisites

- **Python 3.10+**
- **Node.js 20+** (for building the report UI)
- **ClickHouse Cloud credentials** for the Gnosis Chain instance (or access to the hosted endpoint)

## Installation

### From Source

```bash
git clone https://github.com/gnosischain/cerebro-mcp.git
cd cerebro-mcp

# Configure environment
cp .env.example .env
# Edit .env and set CLICKHOUSE_PASSWORD

# Build UI and install Python package
make install
# This runs: npm ci && npm run build -> pip install -e .
```

### Docker

```bash
docker build -t cerebro-mcp .
docker run --env-file .env cerebro-mcp
```

Pre-built images are published to GitHub Container Registry on every push to `main`:

```
ghcr.io/gnosischain/gc-cerebro-mcp:latest
ghcr.io/gnosischain/gc-cerebro-mcp:<commit-sha>
```

## Connecting to Claude Desktop

Add the following to your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

### Local Installation (stdio)

```json
{
  "mcpServers": {
    "cerebro": {
      "command": "cerebro-mcp",
      "env": {
        "CLICKHOUSE_PASSWORD": "your_password"
      }
    }
  }
}
```

If `cerebro-mcp` is not on your PATH, use the full path to the executable or invoke via `uv`:

```json
{
  "mcpServers": {
    "cerebro": {
      "command": "/path/to/uv",
      "args": ["--directory", "/path/to/cerebro-mcp", "run", "cerebro-mcp"],
      "env": {
        "CLICKHOUSE_PASSWORD": "your_password"
      }
    }
  }
}
```

### Hosted Endpoint (Streamable HTTP)

Connect to the team-hosted instance at `mcp.analytics.gnosis.io`. If your deployment runs the current image (which starts with `cerebro-mcp --http`), the recommended endpoint is the Streamable HTTP path `/mcp`:

```json
{
  "mcpServers": {
    "cerebro": {
      "url": "https://mcp.analytics.gnosis.io/mcp",
      "headers": {
        "Authorization": "Bearer <your-token>"
      }
    }
  }
}
```

If the client cannot set custom headers (for example, a native connector UI that only accepts a URL), append the token as a query parameter instead: `https://mcp.analytics.gnosis.io/mcp?token=<your-token>`. The Bearer header remains the preferred path -- query tokens can leak into access logs.

### Hosted Endpoint (Legacy SSE)

Deployments still running the SSE-only transport (`cerebro-mcp --sse`), and current-image deployments during migration (`--http` dual-serves both), also accept the legacy `/sse` endpoint:

```json
{
  "mcpServers": {
    "cerebro": {
      "url": "https://mcp.analytics.gnosis.io/sse",
      "headers": {
        "Authorization": "Bearer <your-token>"
      }
    }
  }
}
```

## Connecting to VS Code

Add the following to `.vscode/mcp.json` in your workspace, or to your user-level `settings.json` for global access.

### Workspace Configuration (`.vscode/mcp.json`)

```json
{
  "servers": {
    "cerebro": {
      "command": "/path/to/uv",
      "args": ["--directory", "/path/to/cerebro-mcp", "run", "cerebro-mcp"],
      "env": {
        "CLICKHOUSE_PASSWORD": "your_password"
      }
    }
  }
}
```

### User Settings (`settings.json`)

```json
{
  "mcp": {
    "servers": {
      "cerebro": {
        "command": "/path/to/uv",
        "args": ["--directory", "/path/to/cerebro-mcp", "run", "cerebro-mcp"],
        "env": {
          "CLICKHOUSE_PASSWORD": "your_password"
        }
      }
    }
  }
}
```

### Hosted Endpoint

Use the Streamable HTTP endpoint `/mcp` if your deployment runs the current image; use the legacy `/sse` path for SSE-only deployments:

```json
{
  "servers": {
    "cerebro": {
      "url": "https://mcp.analytics.gnosis.io/mcp",
      "headers": {
        "Authorization": "Bearer <your-token>"
      }
    }
  }
}
```

## Connecting to Claude Code

Claude Code supports MCP server configuration at both project and global scope.

### Project-Level (`.mcp.json`)

Create a `.mcp.json` file in your project root:

```json
{
  "mcpServers": {
    "cerebro": {
      "command": "/path/to/uv",
      "args": ["--directory", "/path/to/cerebro-mcp", "run", "cerebro-mcp"],
      "env": {
        "CLICKHOUSE_PASSWORD": "your_password"
      }
    }
  }
}
```

### Global Configuration (`~/.claude/.mcp.json`)

For access across all projects:

```json
{
  "mcpServers": {
    "cerebro": {
      "command": "/path/to/uv",
      "args": ["--directory", "/path/to/cerebro-mcp", "run", "cerebro-mcp"],
      "env": {
        "CLICKHOUSE_PASSWORD": "your_password"
      }
    }
  }
}
```

### CLAUDE.md Instructions

You can also add instructions to your project's `CLAUDE.md` file to guide Claude Code on how to use the MCP tools effectively. The cerebro-mcp repository includes a `CLAUDE.md` with client-side instructions for optimal tool usage patterns.

### Hosted Endpoint

Use the Streamable HTTP endpoint `/mcp` if your deployment runs the current image; use the legacy `/sse` path for SSE-only deployments:

```json
{
  "mcpServers": {
    "cerebro": {
      "url": "https://mcp.analytics.gnosis.io/mcp",
      "headers": {
        "Authorization": "Bearer <your-token>"
      }
    }
  }
}
```

## Running a Remote Server

The server selects its transport from command-line flags, with precedence `--http` > `--sse` > stdio (no flag).

### Streamable HTTP (Recommended)

To host your own remote instance:

```bash
cerebro-mcp --http
# Serves the MCP Streamable HTTP endpoint at /mcp
# and dual-serves the legacy /sse + /messages/ routes from the same process
```

Streamable HTTP is the modern, load-balancer-friendly MCP transport: a single `/mcp` endpoint, no long-lived idle stream for a proxy to reap, and -- with `STREAMABLE_HTTP_STATELESS` on (the default) -- no per-pod session affinity requirement, so requests can land on any replica. It is also the transport Claude Desktop's native remote connector speaks, removing the need for the `mcp-remote` bridge. Because `--http` dual-serves the legacy SSE routes, existing `/sse` clients keep working during migration -- a zero-downtime cutover rather than a hard switch.

The published Docker image starts with `cerebro-mcp --http` by default.

Client configuration points at the `/mcp` URL:

```json
{
  "mcpServers": {
    "cerebro": {
      "url": "https://your-host.example.com/mcp",
      "headers": {
        "Authorization": "Bearer <your-token>"
      }
    }
  }
}
```

For clients that cannot set custom headers, `/mcp` additionally accepts the token as a query parameter: `https://your-host.example.com/mcp?token=<your-token>`. This is a fallback, not a replacement -- query tokens can leak into access logs, so prefer the Bearer header. The query-parameter fallback applies only to `/mcp`; the legacy `/sse` and `/messages/` routes require the header.

### Legacy SSE

To run the SSE-only transport (the previous remote default):

```bash
cerebro-mcp --sse
# Serves /sse + /messages/ only
```

Use this only if a client cannot speak Streamable HTTP and you do not want the dual-serving `--http` mode; new deployments should prefer `--http`.

### Server Environment Variables

Both remote transports are configured with:

| Variable | Default | Description |
|----------|---------|-------------|
| `FASTMCP_HOST` | `0.0.0.0` | Bind address |
| `FASTMCP_PORT` | `8000` | Bind port |
| `MCP_AUTH_TOKEN` | _(unset)_ | Bearer token for authentication |
| `ALLOW_INSECURE_REMOTE_TRANSPORT` | `false` | Allow a remote transport to start without `MCP_AUTH_TOKEN` |
| `STREAMABLE_HTTP_STATELESS` | `true` | No server-side session between requests -- required for multi-replica deployments behind a load balancer. Set `false` only for a single replica that needs a persistent session |
| `STREAMABLE_HTTP_JSON_RESPONSE` | `true` | Return plain JSON instead of an SSE-framed stream -- simplest and most proxy-friendly for request/response tool calls |

`MCP_AUTH_TOKEN` is required for both remote transports: the server refuses to start without it unless `ALLOW_INSECURE_REMOTE_TRANSPORT=true`. When set, all requests require an `Authorization: Bearer <token>` header (or, on `/mcp` only, the `?token=` query parameter). The `/health` and `/metrics` endpoints bypass authentication for Kubernetes liveness/readiness probes and Prometheus scraping.

## Multi-tenant identity

If multiple humans share one Cerebro deployment, set `CEREBRO_OWNER` to identify the caller. Cerebro hashes the value with `CEREBRO_OWNER_HASH_SALT` (SHA-256) and stamps every workflow row, so `list_resumable_workflows` and `get_workflow_resume_hint` can filter by owner. See [Multi-Tenant](advanced/multi-tenant.md) for the full trust model.

### stdio

```json
{
  "mcpServers": {
    "cerebro": {
      "command": "cerebro-mcp",
      "env": {
        "CLICKHOUSE_PASSWORD": "your_password",
        "CEREBRO_OWNER": "alice@gnosis.io",
        "CEREBRO_OWNER_HASH_SALT": "rotate-me-quarterly"
      }
    }
  }
}
```

### Remote (Streamable HTTP or SSE)

Send `X-Cerebro-Owner` per request:

```json
{
  "mcpServers": {
    "cerebro": {
      "url": "https://mcp.analytics.gnosis.io/mcp",
      "headers": {
        "Authorization": "Bearer <your-token>",
        "X-Cerebro-Owner": "alice@gnosis.io"
      }
    }
  }
}
```

If neither is set, workflows write `owner=NULL` and the server runs in single-tenant fallback mode.

## Environment Variables

The authoritative source is `src/cerebro_mcp/config.py` (a pydantic `Settings` class); `.env.example` covers the common subset. The tables below list the variables you are most likely to touch.

### Connectivity

| Variable | Default | Description |
|----------|---------|-------------|
| `CLICKHOUSE_HOST` | `localhost` | ClickHouse server hostname (`.env.example` ships the ClickHouse Cloud host) |
| `CLICKHOUSE_PORT` | `8443` | ClickHouse HTTPS port |
| `CLICKHOUSE_USER` | `default` | ClickHouse username |
| `CLICKHOUSE_PASSWORD` | _(required)_ | ClickHouse password |
| `CLICKHOUSE_SECURE` | `True` | Enable TLS for ClickHouse connections |
| `DBT_MANIFEST_URL` | `https://gnosischain.github.io/dbt-cerebro/manifest.json` | URL for the published dbt manifest |
| `DBT_MANIFEST_PATH` | _(unset)_ | Local filesystem path to a manifest.json (takes precedence over the URL) |
| `DBT_CATALOG_URL` | `https://gnosischain.github.io/dbt-cerebro/catalog.json` | URL for the published dbt catalog |
| `DBT_CATALOG_PATH` | _(unset)_ | Local filesystem path to a catalog.json (takes precedence over the URL) |

### Feature flags

Each flag gates the registration of a whole tool family — when off, the tools do not appear at all.

| Variable | Default | Description |
|----------|---------|-------------|
| `SEMANTIC_ENABLED` | `False` | Register the semantic tools (`find`, `query_metrics`, `preflight_analytics_request`, …). Requires a healthy registry snapshot at execution time |
| `SEMANTIC_REGISTRY_URL` | `https://gnosischain.github.io/dbt-cerebro/semantic_registry.json` | Semantic registry artifact (local `SEMANTIC_REGISTRY_PATH` takes precedence) |
| `SEMANTIC_DOCS_INDEX_URL` | `https://gnosischain.github.io/dbt-cerebro/semantic_docs_index.json` | Semantic docs index artifact (local `SEMANTIC_DOCS_INDEX_PATH` takes precedence) |
| `CUSTOM_TOOLS_ENABLED` | `False` | Register the dynamic SQL tools defined in the custom-tools YAML |
| `CUSTOM_TOOLS_PATH` | _(unset)_ | Path to the `custom_tools.yaml` file |
| `SANDBOX_ENABLED` | `False` | Register the DuckDB + Parquet [simulation sandbox](workflows/simulation-sandboxes.md) tools |
| `WORKFLOW_RESUME_TOOLS_ENABLED` | `False` | Register `list_resumable_workflows` / `get_workflow_resume_hint` / `recompute_workflow_resume_hint`. The underlying event store records workflow state regardless |
| `RPC_SCAN_ENABLED` | `False` | Register the bulk [RPC scan](advanced/rpc-scans.md) family (`rpc_scan_logs`, `rpc_batch_call`, …). Results stream into ClickHouse scratch tables, so the ClickHouse user needs `GRANT CREATE DATABASE, CREATE TABLE, INSERT, DROP TABLE, SELECT ON scratch.*` |
| `GRAFANA_TOOLS_ENABLED` | `False` | Register the [Grafana dashboard publishing](advanced/grafana-publishing.md) tools |
| `GRAFANA_URL` | _(empty)_ | Grafana base URL (required for publishing) |
| `GRAFANA_API_TOKEN` | _(empty)_ | Grafana service-account token |
| `GRAFANA_CLICKHOUSE_DATASOURCE_UID` | _(empty)_ | UID of the ClickHouse datasource dashboards should query |
| `GRAFANA_CLICKHOUSE_DATASOURCE_TYPE` | `grafana-clickhouse-datasource` | Datasource plugin type |
| `GRAFANA_FOLDER_UID` | _(empty)_ | Target folder UID; empty publishes to the default (General) folder |
| `LEAN_CORE_ENABLED` | `False` | Advertise only the ~18 core tools; advanced tools stay callable and can be un-hidden via `load_tools`. See [Finding Tools](advanced/discovery.md) |

### Web3 / RPC

| Variable | Default | Description |
|----------|---------|-------------|
| `GNOSIS_RPC_URL` | `https://rpc.gnosischain.com` | JSON-RPC endpoint for latest-state reads |
| `GNOSIS_ARCHIVE_RPC_URL` | _(empty)_ | Archive node endpoint — required for non-`latest` block reads; trace scans additionally require a trace-capable node (Erigon, or Nethermind with Trace) |
| `BLOCKSCOUT_API_BASE_URL` | `https://gnosis.blockscout.com/api/v2` | Blockscout API used for ABI / contract metadata resolution |
| `RPC_TIMEOUT_SECONDS` | `15` | Per-request timeout for single-call RPC tools |
| `RPC_MAX_RETRIES` | `3` | Retry budget for single-call RPC tools |

### Query and tool limits

| Variable | Default | Description |
|----------|---------|-------------|
| `MAX_ROWS` | `10000` | Maximum rows returned per query |
| `QUERY_TIMEOUT_SECONDS` | `30` | Query execution timeout (`CLICKHOUSE_QUERY_TIMEOUT_SECONDS` overrides it when set) |
| `MAX_QUERY_LENGTH` | `10000` | Maximum SQL string length accepted |
| `TOOL_RESULT_MAX_ROWS` | `200` | Maximum rows embedded in a tool response |
| `TOOL_RESULT_MAX_CHARS` | `40000` | Maximum characters per tool response (falls back to the legacy `TOOL_RESPONSE_MAX_CHARS` when unset) |
| `CLICKHOUSE_MAX_QUERY_MEMORY_GB` | `4.0` | Per-query memory ceiling in GiB (`0` disables the cap) |

### Storage

| Variable | Default | Description |
|----------|---------|-------------|
| `CEREBRO_REPORT_DIR` | `~/.cerebro/reports` | Directory for saved report HTML files |
| `CEREBRO_SAVED_QUERIES_DIR` | `~/.cerebro-mcp` | Directory for saved query files |
| `THINKING_LOG_DIR` | `.cerebro/logs` | Directory for reasoning trace files |
| `THINKING_LOG_RETENTION_DAYS` | `30` | Days to retain trace logs before auto-pruning |
| `THINKING_ALWAYS_ON` | `True` | Automatically capture all tool calls in reasoning traces |

### Event log + workflows (Phase 3)

| Variable | Default | Description |
|----------|---------|-------------|
| `EVENT_STORE_PATH` | `.cerebro/cerebro_state.db` | SQLite event log location |
| `WORKFLOW_ORPHAN_AGE_SECONDS` | `86400` | Idle threshold for marking workflows orphaned (24h) |
| `EVENT_PAYLOAD_COMPRESSION_THRESHOLD_BYTES` | `4096` | Payloads above this are gzipped |
| `WORKFLOW_MAX_PARALLEL` | `8` | Cap on parallel sub-tasks in `run_parallel_phase` |

### Sandboxes (Phase 2)

| Variable | Default | Description |
|----------|---------|-------------|
| `SANDBOX_ROOT` | `.cerebro/sandboxes` | Where Parquet snapshots live |
| `SANDBOX_MAX_CONCURRENT` | `4` | LRU eviction threshold |
| `SANDBOX_TTL_SECONDS` | `1800` | Idle TTL (30 min) |
| `SANDBOX_MAX_BYTES_PER_EXPORT` | `2147483648` | Hard cap per export (2 GB) |

### Multi-tenant

| Variable | Default | Description |
|----------|---------|-------------|
| `CEREBRO_OWNER` | _(unset)_ | Caller identifier (hashed before persistence) |
| `CEREBRO_OWNER_HASH_SALT` | _(unset)_ | Salt for SHA-256 owner hash; rotation = tenant reset |

### Remote transports / auth

| Variable | Default | Description |
|----------|---------|-------------|
| `MCP_AUTH_TOKEN` | _(unset)_ | Bearer token for remote transport authentication (`--http` and `--sse`) |
| `ALLOW_INSECURE_REMOTE_TRANSPORT` | `false` | Allow a remote transport to start without `MCP_AUTH_TOKEN` |
| `STREAMABLE_HTTP_STATELESS` | `true` | Stateless Streamable HTTP sessions -- requests can land on any replica behind a load balancer |
| `STREAMABLE_HTTP_JSON_RESPONSE` | `true` | Plain JSON responses on `/mcp` instead of an SSE-framed stream |
| `FASTMCP_HOST` | `0.0.0.0` | Remote server bind address |
| `FASTMCP_PORT` | `8000` | Remote server port |
| `MCP_SECURITY_LOG_DIR` | `.cerebro/security_audit` | Audit JSONL directory |
| `MCP_SECURITY_POLICY_MODE` | `log_only` | Future: `warn` / `enforce` |

## Security Recommendations

### Read-Only ClickHouse User

For production deployments, create a dedicated read-only database user:

```sql
CREATE USER mcp_reader IDENTIFIED BY '...';
GRANT SELECT ON execution.* TO mcp_reader;
GRANT SELECT ON consensus.* TO mcp_reader;
GRANT SELECT ON crawlers_data.* TO mcp_reader;
GRANT SELECT ON nebula.* TO mcp_reader;
GRANT SELECT ON dbt.* TO mcp_reader;
GRANT SELECT ON system.tables TO mcp_reader;
GRANT SELECT ON system.columns TO mcp_reader;
```

### Token Rotation

When using a remote transport (`--http` or `--sse`) with `MCP_AUTH_TOKEN`, rotate the token periodically:

```bash
export MCP_AUTH_TOKEN=$(openssl rand -hex 32)
```

## Verification

After configuring your client, verify the connection by asking your AI assistant:

- "Check the Cerebro system status"
- "List available databases"
- "Search for transaction models"

If the tools appear and respond, the connection is working correctly.

## Troubleshooting

| Issue | Resolution |
|-------|------------|
| `cerebro-mcp` command not found | Ensure the package is installed (`pip install -e .`) and on your PATH, or use the full path |
| ClickHouse connection refused | Verify `CLICKHOUSE_HOST`, `CLICKHOUSE_PORT`, and `CLICKHOUSE_PASSWORD` in your `.env` or `env` block |
| Remote connection timeout | Check `FASTMCP_HOST`/`FASTMCP_PORT` and ensure the server is running (`cerebro-mcp --http`, or `--sse` for legacy SSE-only) |
| Tools not appearing in Claude Desktop | Restart Claude Desktop after editing `claude_desktop_config.json` |
| Bearer token rejected | Confirm `MCP_AUTH_TOKEN` matches between server and client `Authorization` header |
| Client cannot set an `Authorization` header | On `/mcp` only, append `?token=<MCP_AUTH_TOKEN>` to the URL (query-parameter auth fallback) |

## Testing with MCP Inspector

The MCP Inspector provides a web UI for testing tools interactively:

```bash
uv run mcp dev src/cerebro_mcp/server.py
```

This spawns the server with the Inspector UI, allowing you to call individual tools and inspect responses.
