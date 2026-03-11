# ip-crawler

ip-crawler is a Python service that enriches peer IP addresses discovered by nebula with geolocation and network data from the [ipinfo.io](https://ipinfo.io) API.

## Purpose

While nebula discovers which peers exist on the network and captures their IP addresses, ip-crawler adds geographic and organizational context to each IP. This enables analytics such as:

- Geographic distribution of Gnosis Chain nodes by country and city
- Hosting provider and ASN concentration analysis
- Network diversity metrics
- Identification of centralization risks

## How It Works

1. **Query for new IPs** -- ip-crawler reads the `nebula.visits` table and identifies IP addresses that have not yet been enriched
2. **Filter by fork digest** -- Only IPs associated with configured Gnosis Chain fork digests are processed
3. **Batch lookup** -- IPs are sent to the ipinfo.io API in batches (default 50 per batch)
4. **Rate limiting** -- Requests are throttled to 10 per second to respect API limits
5. **Store results** -- Enriched data is written to the `crawlers_data.ipinfo` table
6. **Incremental processing** -- The table is processed month-by-month to avoid memory issues with large datasets

## Operation Modes

### Continuous Mode (Default)

Runs as a persistent daemon, processing new batches every 60 seconds:

```bash
docker-compose up -d ip-crawler
```

The crawler automatically:

- Detects new IPs from `nebula.visits`
- Processes them in batches
- Sleeps between cycles
- Resumes from the last processed partition on restart

### One-Time Mode

Processes a single batch of IPs and exits. Useful for scheduled jobs (cron, Kubernetes CronJob) or testing:

```bash
# CLI
python -m src.crawler --once --batch-size 200

# Docker
docker-compose run --rm -e CRAWLER_MODE=once ip-crawler
```

One-time mode produces a summary report and saves statistics to `logs/last_run_stats.json`.

## Data Schema

The `crawlers_data.ipinfo` table stores enrichment results:

| Column | Type | Description |
|--------|------|-------------|
| `ip` | String | IP address (primary key component) |
| `hostname` | String | Reverse DNS hostname |
| `city` | String | City name |
| `region` | String | Region/state name |
| `country` | String | ISO country code |
| `loc` | String | Latitude,longitude coordinates |
| `org` | String | Organization name |
| `postal` | String | Postal/ZIP code |
| `timezone` | String | IANA timezone identifier |
| `asn` | String | Autonomous System Number |
| `company` | String | Company name |
| `carrier` | String | Mobile carrier (if applicable) |
| `is_bogon` | Boolean | Whether the IP is a bogon (private/reserved) |
| `is_mobile` | Boolean | Whether the IP is a mobile connection |
| `abuse_email` | String | Abuse contact email |
| `abuse_phone` | String | Abuse contact phone |
| `error` | String | Error message if lookup failed |
| `attempts` | UInt8 | Number of lookup attempts |
| `success` | Boolean | Whether the lookup succeeded |
| `created_at` | DateTime | First lookup timestamp |
| `updated_at` | DateTime | Most recent lookup timestamp |

## Configuration

### Required Settings

| Variable | Description |
|----------|-------------|
| `CLICKHOUSE_HOST` | ClickHouse server hostname |
| `CLICKHOUSE_PASSWORD` | ClickHouse authentication password |
| `IPINFO_API_TOKEN` | ipinfo.io API token |

### ClickHouse Connection

| Variable | Default | Description |
|----------|---------|-------------|
| `CLICKHOUSE_PORT` | -- | ClickHouse server port |
| `CLICKHOUSE_USER` | -- | Username |
| `CLICKHOUSE_DATABASE` | `crawlers_data` | Target database |
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
| `CRAWLER_MODE` | `continuous` | Set to `once` for one-time mode |

### Fork Digest Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `FORK_DIGESTS` | `0x56fdb5e0,0x824be431,0x21a6f836,0x3ebfd484,0x7d5aab40,0xf9ab5f85` | Comma-separated list of Gnosis Chain fork digests to filter for |

Fork digests are updated when the Gnosis Chain undergoes protocol upgrades. The variable can be changed at runtime -- the crawler detects the update automatically.

## Incremental Processing

To handle the potentially large `nebula.visits` table without exceeding memory limits, ip-crawler processes data month-by-month:

1. Queries are scoped to a single month partition at a time
2. Processing state is saved to `logs/partition_state.json`
3. The crawler automatically resumes from the last processed month on restart
4. Once a month is fully processed, it moves to the next

## Monitoring

### Logs

```bash
# View container logs
docker-compose logs -f ip-crawler
```

Log files are stored in the `logs/` directory:

| File | Description |
|------|-------------|
| `crawler.log` | Main application log |
| `health.log` | Health check status |
| `partition_state.json` | Incremental processing state |
| `last_run_stats.json` | Statistics from the last one-time run |

### Health Checks

The container includes a health check that verifies the crawler process is running by checking for the existence of the health log file.

## Docker Deployment

```bash
# Setup
cp .env.example .env
# Edit .env with ClickHouse credentials and ipinfo.io token

# Run in continuous mode
docker-compose up -d

# Run one-time batch
docker-compose run --rm -e CRAWLER_MODE=once ip-crawler
```

## ClickHouse Table Schemas

??? note "Table: `crawlers_data.ipinfo`"
    **Engine:** MergeTree()
    **ORDER BY:** (ip, updated_at)
    **INDEX:** minmax on ip

    | Column | Type | Notes |
    |--------|------|-------|
    | `ip` | String | IP address |
    | `hostname` | String | Reverse DNS hostname |
    | `city` | String | City name |
    | `region` | String | Region / state name |
    | `country` | String | ISO country code |
    | `loc` | String | Latitude,longitude coordinates |
    | `org` | String | Organization name |
    | `postal` | String | Postal / ZIP code |
    | `timezone` | String | IANA timezone identifier |
    | `asn` | String | Autonomous System Number |
    | `company` | String | Company name |
    | `carrier` | String | Mobile carrier (if applicable) |
    | `is_bogon` | Boolean | Default false; private/reserved IP |
    | `is_mobile` | Boolean | Default false; mobile connection |
    | `abuse_email` | String | Abuse contact email |
    | `abuse_phone` | String | Abuse contact phone |
    | `error` | String | Error message if lookup failed |
    | `attempts` | UInt8 | Default 1; number of lookup attempts |
    | `success` | Boolean | Default true; whether lookup succeeded |
    | `created_at` | DateTime | Default now(); first lookup timestamp |
    | `updated_at` | DateTime | Default now(); most recent lookup timestamp |
