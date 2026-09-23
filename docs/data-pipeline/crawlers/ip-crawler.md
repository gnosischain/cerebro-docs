# ip-crawler

ip-crawler is a Python service that enriches peer IP addresses discovered by [nebula](nebula.md) with geolocation and network data from the [ipinfo.io](https://ipinfo.io) API, into `crawlers_data.ipinfo`. It feeds three **public-dashboard** HOPR marts.

## Purpose

While nebula discovers which peers exist on the network and captures their IP addresses, ip-crawler adds geographic and organizational context to each IP. This enables analytics such as:

- Geographic distribution of Gnosis Chain nodes by country and city
- Hosting provider and ASN concentration analysis
- Network diversity metrics
- Identification of centralization risks

## How It Works

1. **Find un-enriched IPs** — a server-side anti-join of `nebula.visits` against `crawlers_data.ipinfo`, bounded by a memory fuse. There is no state table and no cursor: **the anti-join is the state.**
2. **Look up once, ever** — an IP is queried once, including failures, which are written as permanent negatives so they are never retried.
3. **Batch lookup** — IPs go to the ipinfo.io API in batches, under two per-run caps.
4. **Write** — enriched rows land in `crawlers_data.ipinfo`.

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


`company`, `carrier` and `abuse_*` are **legitimately empty** — the current ipinfo plan returns only the nine core fields. The table is a plain MergeTree and does **not** dedupe: readers need `LIMIT 1 BY ip`. There are 71 known legacy duplicate rows.

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
| `BATCH_SIZE` | `50` | Number of IPs per API batch |
| `REQUEST_TIMEOUT` | `10` | Seconds before an API request times out |
| `MAX_RETRIES` | `3` | Maximum retry attempts for failed API requests |
| `RETRY_DELAY` | `5` | Seconds between retries |
| `IPINFO_RATE_LIMIT` | `1000` | Pacing value. **The real ipinfo limit is 50,000 per month, not per day**; the two per-run caps are the actual budget control |

### Fork Digest Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `FORK_DIGESTS` | `0x56fdb5e0,0x824be431,0x21a6f836,0x3ebfd484,0x7d5aab40,0xf9ab5f85` | Comma-separated list of Gnosis Chain fork digests to filter for |

Fork digests are updated when the Gnosis Chain undergoes protocol upgrades.

## Operating and recovering

### How it runs

A daily CronJob at **02:00 UTC**, `concurrencyPolicy: Forbid`, with a 36,000 s deadline. Runs are stateless and idempotent: every run re-derives its work list from the anti-join, so re-running is always safe. There is no continuous mode in production.

### Health — one log line

**There are zero alert rules and no cron-miss rule.** Health is the single `run_summary` JSON line each run emits. Alert-worthy: no `run_summary` for 26 h; `exit_code != 0`; `truncated=true` on the *recent* window; `clickhouse_errors > 0`. `phases.sweep.truncated` alone is normal while a backlog drains.

The data check is the same as every other source: `max(created_at)` on `crawlers_data.ipinfo` should be within a day.

### Backfill

Backfill a window explicitly (always single-phase):

```bash
python -m src.crawler --since ⟨YYYY-MM-DD⟩ --until ⟨YYYY-MM-DD⟩
```

Run it as a one-shot job cloned from the CronJob ([how](../../operations/runbooks/one-shot-jobs.md)). `Forbid` cannot see a hand-created Job, so space manual runs yourself.

!!! warning "This job once caused a platform-wide Code 241 event"
    Under an older image it paged `nebula.visits` with a growing `NOT IN` list, took ~6 h to find nothing, and with `concurrencyPolicy: Allow` left **three runs alive at once**, holding the warehouse over its memory limit and producing 241 errors for unrelated jobs. The fix moved the anti-join server-side with a 1 GiB fuse and set `Forbid` plus the deadline. If you see long ip-crawler runs, treat it as a warehouse risk, not a local one.

**The `hopr` preset has an ordering bug.** It reads `dbt.int_hopr_nodes` and writes a table dbt reads back, so it should run *after* the dbt cron. It fires at 02:00; dbt runs at 06:00. Not currently harmful for the default preset, which reads `nebula.visits`, but do not add dbt-reading presets to this schedule without moving it.

### Then dbt

The three HOPR marts are rebuilt by the nightly run; nothing to do by hand unless the gap is older than the models' incremental window — see [dbt reprocess](../../operations/runbooks/dbt-reprocess.md).

!!! info "Internal runbook"
    [runbooks/27-nebula-and-ip-crawler.md](https://github.com/gnosisdevops/infrastructure-gnosis-analytics/blob/main/runbooks/27-nebula-and-ip-crawler.md) — private repository; carries the cluster-specific commands for this page.

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
