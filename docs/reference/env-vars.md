---
title: Environment Variables
description: All environment variables across Gnosis Analytics platform components
---

# Environment Variables

This page documents all environment variables used across every component of the Gnosis Analytics platform. Variables are organized by component.

## cerebro-api

The REST API server built with FastAPI.

### Application Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `API_TITLE` | `Gnosis Cerebro Data API` | Application title displayed in Swagger UI |
| `API_VERSION` | `v1` | API version prefix for all routes |
| `DEBUG` | `false` | Enable debug mode (hot reload, verbose logging) |

### ClickHouse Connection

| Variable | Default | Description |
|----------|---------|-------------|
| `CLICKHOUSE_URL` | -- | ClickHouse Cloud hostname (e.g., `host.eu-central-1.aws.clickhouse.cloud`). Takes precedence over `CLICKHOUSE_HOST` when set. |
| `CLICKHOUSE_HOST` | `localhost` | ClickHouse server hostname. Used when `CLICKHOUSE_URL` is not set. |
| `CLICKHOUSE_PORT` | `8443` | ClickHouse HTTP(S) port |
| `CLICKHOUSE_USER` | `default` | ClickHouse authentication username |
| `CLICKHOUSE_PASSWORD` | -- | ClickHouse authentication password |
| `CLICKHOUSE_DATABASE` | `default` | Default database for queries |
| `CLICKHOUSE_SECURE` | `true` | Use HTTPS for ClickHouse connections |

### dbt Manifest

| Variable | Default | Description |
|----------|---------|-------------|
| `DBT_MANIFEST_URL` | `https://gnosischain.github.io/dbt-cerebro/manifest.json` | Remote URL for the dbt manifest. The API fetches this URL to discover endpoints. Set to empty string to disable remote fetching. |
| `DBT_MANIFEST_PATH` | `./manifest.json` | Local file path fallback when the URL is unavailable |
| `DBT_MANIFEST_REFRESH_ENABLED` | `true` | Enable periodic background manifest refresh |
| `DBT_MANIFEST_REFRESH_INTERVAL_SECONDS` | `300` | Seconds between manifest refresh polls (default: 5 minutes) |

### Authentication and Access Control

| Variable | Default | Description |
|----------|---------|-------------|
| `API_KEYS_FILE` | `./api_keys.json` | Path to JSON file containing API key definitions |
| `API_KEYS` | `{}` | API keys as a JSON environment variable. Overrides the file when set. Format: `{"sk_live_abc": {"user": "alice", "tier": "tier1", "org": "Acme"}}` |
| `DEFAULT_ENDPOINT_TIER` | `tier0` | Default access tier for endpoints without an explicit tier tag |

### Rate Limiting

Rate limits are configured per tier in the application code:

| Tier | Requests per Minute |
|------|-------------------|
| `tier0` | 20 |
| `tier1` | 100 |
| `tier2` | 500 |
| `tier3` | 10,000 |

---

## cerebro-mcp

The MCP (Model Context Protocol) server for AI-powered analytics.

### ClickHouse Connection

| Variable | Default | Description |
|----------|---------|-------------|
| `CLICKHOUSE_URL` | -- | ClickHouse Cloud hostname |
| `CLICKHOUSE_USER` | `default` | ClickHouse authentication username |
| `CLICKHOUSE_PASSWORD` | -- | ClickHouse authentication password |
| `CLICKHOUSE_DATABASE` | `dbt` | Default database for queries |

### dbt Integration

| Variable | Default | Description |
|----------|---------|-------------|
| `DBT_MANIFEST_PATH` | -- | Path to local dbt `manifest.json` file for model discovery |

### MCP Transport

| Variable | Default | Description |
|----------|---------|-------------|
| `FASTMCP_HOST` | `0.0.0.0` | Bind address for SSE/HTTP transport |
| `FASTMCP_PORT` | `8000` | Port for SSE/HTTP transport |

---

## cryo-indexer

Execution layer data indexer built on the Cryo framework.

| Variable | Default | Description |
|----------|---------|-------------|
| `RPC_URL` | -- | Gnosis Chain execution layer JSON-RPC endpoint URL |
| `OUTPUT_DIR` | -- | Directory for intermediate output files |
| `START_BLOCK` | -- | First block number to index (inclusive) |
| `END_BLOCK` | -- | Last block number to index (inclusive). Omit for continuous indexing. |
| `DATASETS` | -- | Comma-separated list of Cryo datasets to index (e.g., `blocks,transactions,logs,traces`) |
| `CLICKHOUSE_URL` | -- | ClickHouse hostname for data loading |
| `CLICKHOUSE_USER` | -- | ClickHouse username |
| `CLICKHOUSE_PASSWORD` | -- | ClickHouse password |

---

## beacon-indexer

Consensus layer data indexer using the Beacon API.

| Variable | Default | Description |
|----------|---------|-------------|
| `BEACON_API_URL` | -- | Gnosis Chain beacon node API URL (e.g., `http://beacon-node:5052`) |
| `CLICKHOUSE_HOST` | -- | ClickHouse hostname |
| `CLICKHOUSE_PORT` | `8443` | ClickHouse HTTP(S) port |
| `CLICKHOUSE_USER` | -- | ClickHouse username |
| `CLICKHOUSE_PASSWORD` | -- | ClickHouse password |
| `CLICKHOUSE_DATABASE` | `consensus` | Target database for consensus data |
| `CLICKHOUSE_SECURE` | `true` | Use HTTPS |
| `START_SLOT` | -- | First slot to index (inclusive) |
| `END_SLOT` | -- | Last slot to index (inclusive). Omit for continuous indexing. |
| `WORKERS` | `4` | Number of concurrent worker goroutines |

---

## click-runner

External data ingestion toolkit for CSV, Parquet, and SQL-based imports.

### ClickHouse Connection

| Variable | Default | Description |
|----------|---------|-------------|
| `CH_HOST` | -- | ClickHouse server hostname |
| `CH_PORT` | `9000` | ClickHouse native protocol port |
| `CH_USER` | -- | ClickHouse authentication username |
| `CH_PASSWORD` | -- | ClickHouse authentication password |
| `CH_DB` | -- | Target database name |
| `CH_SECURE` | `false` | Use TLS connection |
| `CH_VERIFY` | `false` | Verify TLS certificate |

!!! note "Port difference"
    click-runner uses the ClickHouse native protocol (port 9000/9440) rather than the HTTP protocol (port 8123/8443) used by other components.

### S3 Integration

| Variable | Default | Description |
|----------|---------|-------------|
| `S3_ACCESS_KEY` | -- | AWS access key ID for S3 |
| `S3_SECRET_KEY` | -- | AWS secret access key for S3 |
| `S3_BUCKET` | `prod-use1-gnosis` | S3 bucket name |
| `S3_REGION` | `us-east-1` | AWS region |

### Data Source URLs

| Variable | Description |
|----------|-------------|
| `EMBER_DATA_URL` | URL to the Ember electricity generation CSV data |

### Variable Substitution

SQL files support `{{VARIABLE_NAME}}` placeholders that are replaced with values from environment variables prefixed with `CH_QUERY_VAR_`. For example:

- Environment variable: `CH_QUERY_VAR_EMBER_DATA_URL=https://example.com/data.csv`
- In SQL: `FROM url('{{EMBER_DATA_URL}}', 'CSV')`

---

## nebula

P2P DHT network crawler for peer discovery.

| Variable | Default | Description |
|----------|---------|-------------|
| `CRAWL_INTERVAL` | -- | Seconds between crawl cycles |
| `CLICKHOUSE_HOST` | -- | ClickHouse hostname |
| `CLICKHOUSE_PORT` | -- | ClickHouse port |
| `CLICKHOUSE_USER` | -- | ClickHouse username |
| `CLICKHOUSE_PASSWORD` | -- | ClickHouse password |
| `CLICKHOUSE_DATABASE` | `nebula` | Target database |
| `NETWORKS` | -- | Comma-separated list of networks to crawl |

---

## ip-crawler

IP geolocation enrichment service for P2P peer data.

### Required Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `CLICKHOUSE_HOST` | -- | ClickHouse server hostname |
| `CLICKHOUSE_PASSWORD` | -- | ClickHouse authentication password |
| `IPINFO_API_TOKEN` | -- | ipinfo.io API token for IP lookups |

### ClickHouse Connection

| Variable | Default | Description |
|----------|---------|-------------|
| `CLICKHOUSE_PORT` | -- | ClickHouse server port |
| `CLICKHOUSE_USER` | -- | ClickHouse username |
| `CLICKHOUSE_DATABASE` | `crawlers_data` | Target database for enrichment results |
| `CLICKHOUSE_SECURE` | -- | Use TLS connection |

### Processing Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `BATCH_SIZE` | `50` | Number of IPs per processing batch |
| `SLEEP_INTERVAL` | `60` | Seconds between processing cycles (continuous mode) |
| `REQUEST_TIMEOUT` | `10` | Seconds before an API request times out |
| `MAX_RETRIES` | `3` | Maximum retry attempts for failed API requests |
| `RETRY_DELAY` | `5` | Seconds between retries |
| `IPINFO_RATE_LIMIT` | `1000` | Daily API request limit |
| `CRAWLER_MODE` | `continuous` | Set to `once` for one-time processing mode |

### Fork Digest Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `FORK_DIGESTS` | `0x56fdb5e0,0x824be431,0x21a6f836,0x3ebfd484,0x7d5aab40,0xf9ab5f85` | Comma-separated Gnosis Chain fork digests for peer filtering |

---

## dbt-cerebro

The dbt project for data transformation. These variables are used by the dbt profile configuration.

| Variable | Default | Description |
|----------|---------|-------------|
| `CLICKHOUSE_URL` | -- | ClickHouse Cloud hostname |
| `CLICKHOUSE_PORT` | `8443` | ClickHouse HTTP(S) port |
| `CLICKHOUSE_USER` | `default` | ClickHouse username |
| `CLICKHOUSE_PASSWORD` | -- | ClickHouse password |
| `CLICKHOUSE_SECURE` | `True` | Use HTTPS |
| `CLICKHOUSE_DATABASE` | -- | Target database for dbt models |

---

## Common Patterns

### ClickHouse Connection Across Components

Most components share the same ClickHouse connection pattern but with slightly different variable names:

| Component | Host Variable | Port | Protocol |
|-----------|--------------|------|----------|
| cerebro-api | `CLICKHOUSE_URL` or `CLICKHOUSE_HOST` | 8443 | HTTPS |
| cerebro-mcp | `CLICKHOUSE_URL` | 8443 | HTTPS |
| beacon-indexer | `CLICKHOUSE_HOST` | 8443 | HTTPS |
| ip-crawler | `CLICKHOUSE_HOST` | 8443 | HTTPS |
| click-runner | `CH_HOST` | 9000/9440 | Native |
| dbt-cerebro | `CLICKHOUSE_URL` | 8443 | HTTPS |

!!! warning "click-runner uses different variable names"
    click-runner uses the `CH_` prefix (e.g., `CH_HOST`, `CH_PASSWORD`) instead of the `CLICKHOUSE_` prefix used by other components. It also connects via the native protocol (port 9000) rather than HTTP (port 8443).
