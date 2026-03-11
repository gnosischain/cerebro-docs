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

### Hosted Endpoint (SSE)

Connect to the team-hosted instance at `mcp.analytics.gnosis.io`:

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

```json
{
  "servers": {
    "cerebro": {
      "url": "https://mcp.analytics.gnosis.io/sse",
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

## Running as an SSE Server

To host your own remote instance:

```bash
cerebro-mcp --sse
# Default: http://127.0.0.1:8000
```

Configure the server with environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `FASTMCP_HOST` | `127.0.0.1` | Bind address |
| `FASTMCP_PORT` | `8000` | Bind port |
| `MCP_AUTH_TOKEN` | _(unset)_ | Bearer token for authentication (disabled when unset) |

When `MCP_AUTH_TOKEN` is set, all requests require an `Authorization: Bearer <token>` header. The `/health` endpoint bypasses authentication for Kubernetes liveness/readiness probes.

## Environment Variables

Complete list of configuration variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `CLICKHOUSE_HOST` | `ujt1j3jrk0.eu-central-1.aws.clickhouse.cloud` | ClickHouse server hostname |
| `CLICKHOUSE_PORT` | `8443` | ClickHouse HTTPS port |
| `CLICKHOUSE_USER` | `default` | ClickHouse username |
| `CLICKHOUSE_PASSWORD` | _(required)_ | ClickHouse password |
| `CLICKHOUSE_SECURE` | `True` | Enable TLS for ClickHouse connections |
| `DBT_MANIFEST_URL` | `https://gnosischain.github.io/dbt-cerebro/manifest.json` | URL for the published dbt manifest |
| `DBT_MANIFEST_PATH` | _(unset)_ | Local filesystem path to a manifest.json (overrides URL) |
| `MAX_ROWS` | `10000` | Maximum rows returned per query |
| `QUERY_TIMEOUT_SECONDS` | `30` | Query execution timeout |
| `MAX_QUERY_LENGTH` | `10000` | Maximum SQL string length accepted |
| `TOOL_RESPONSE_MAX_CHARS` | `40000` | Maximum characters per tool response |
| `THINKING_ALWAYS_ON` | `True` | Automatically capture all tool calls in reasoning traces |
| `THINKING_LOG_DIR` | `.cerebro/logs` | Directory for reasoning trace files |
| `THINKING_LOG_RETENTION_DAYS` | `30` | Days to retain trace logs before auto-pruning |
| `CEREBRO_REPORT_DIR` | `~/.cerebro/reports` | Directory for saved report HTML files |
| `CEREBRO_SAVED_QUERIES_DIR` | `~/.cerebro-mcp` | Directory for saved query files |
| `MCP_AUTH_TOKEN` | _(unset)_ | Bearer token for SSE authentication |
| `FASTMCP_HOST` | `127.0.0.1` | SSE server bind address |
| `FASTMCP_PORT` | `8000` | SSE server port |

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

When using SSE transport with `MCP_AUTH_TOKEN`, rotate the token periodically:

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
| SSE connection timeout | Check `FASTMCP_HOST`/`FASTMCP_PORT` and ensure the server is running (`cerebro-mcp --sse`) |
| Tools not appearing in Claude Desktop | Restart Claude Desktop after editing `claude_desktop_config.json` |
| Bearer token rejected | Confirm `MCP_AUTH_TOKEN` matches between server and client `Authorization` header |

## Testing with MCP Inspector

The MCP Inspector provides a web UI for testing tools interactively:

```bash
uv run mcp dev src/cerebro_mcp/server.py
```

This spawns the server with the Inspector UI, allowing you to call individual tools and inspect responses.
