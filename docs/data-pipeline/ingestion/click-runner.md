# click-runner

click-runner is a modular Python toolkit for loading data into ClickHouse from various external sources. It supports SQL query execution, CSV ingestion via ClickHouse URL engine, Parquet ingestion from S3 buckets, Google Drive CSV imports, and dedicated API ingestors for Mixpanel, CoW Protocol, Snapshot, and Discourse.

## Purpose

Not all data in the Gnosis Analytics pipeline comes from blockchain nodes. click-runner handles the ingestion of external datasets:

- **Ember** -- global electricity generation data used for ESG carbon footprint calculations
- **ProbeLab** -- daily peer-to-peer network metrics (agent versions, peer distributions, crawl statistics)
- **Governance** -- Snapshot proposals, votes, and followers plus Discourse forum topics, posts, and users (feeds the [Governance Explorer](../../mcp/mini-apps/governance.md) mini-app)
- **Mixpanel** -- product-analytics events and user profiles for Gnosis App and Gnosis Pay
- **CoW Protocol** -- open orders and trade fees from the CoW API
- **Gnosis Pay on Celo** -- card transfers and wallet events (`crawlers_data.celo_gpay_*`)
- **Google Drive** -- ad-hoc CSV datasets shared via Drive
- **Administrative queries** -- schema migrations, data maintenance, and custom SQL operations

## Ingestion Modes

click-runner selects an ingestor via the `--ingestor` parameter: `query`, `csv`, `parquet`, `gdrive`, `dune-execute-only`, `mixpanel`, `mixpanel-profiles`, `cow`, `snapshot`, or `forum`.

### Query Mode

Executes arbitrary SQL files against ClickHouse. Used for administrative tasks, schema updates, and custom transformations.

```bash
python run_queries.py --ingestor=query \
  --queries=queries/file1.sql,queries/file2.sql
```

### CSV Mode

Imports data from CSV files using ClickHouse's built-in URL engine. The typical workflow involves three SQL files: table creation, data insertion (reading from a remote CSV URL), and optional optimization.

```bash
python run_queries.py --ingestor=csv \
  --create-table-sql=queries/ember/create_ember_table.sql \
  --insert-sql=queries/ember/insert_ember_data.sql \
  --optimize-sql=queries/ember/optimize_ember_data.sql
```

### Parquet Mode

Imports data from Parquet files stored in S3 buckets. Supports three sub-modes:

| Sub-mode | Description | Use Case |
|----------|-------------|----------|
| `latest` | Import only the most recent file | Daily incremental updates |
| `date` | Import a file for a specific date | Targeted backfills |
| `all` | Import all available files | Full historical load |

```bash
# Import latest file
python run_queries.py --ingestor=parquet \
  --create-table-sql=queries/probelab/probelab_agent_semvers_avg_1d.up.sql \
  --s3-path=assets/agent_semvers_avg_1d_data/{{DATE}}.parquet \
  --table-name=crawlers_data.probelab_agent_semvers_avg_1d \
  --mode=latest

# Import file for a specific date
python run_queries.py --ingestor=parquet \
  --create-table-sql=queries/probelab/probelab_agent_semvers_avg_1d.up.sql \
  --s3-path=assets/agent_semvers_avg_1d_data/{{DATE}}.parquet \
  --table-name=crawlers_data.probelab_agent_semvers_avg_1d \
  --mode=date --date=2025-04-13
```

### Google Drive Mode

Imports a CSV file shared on Google Drive by its file ID.

```bash
python run_queries.py --ingestor=gdrive \
  --create-table-sql=queries/new_source/create_table.sql \
  --table-name=crawlers_data.my_table \
  --file-id=<drive-file-id> --max-rows=1000000
```

### Mixpanel Modes

Two ingestors cover Mixpanel: `mixpanel` exports raw events and `mixpanel-profiles` exports user profiles. Both write to the database configured via `MIXPANEL_DATABASE` (`mixpanel_raw_events`, `mixpanel_raw_profiles`, plus an ingestion-state watermark table).

```bash
# Daily incremental event export
python run_queries.py --ingestor=mixpanel --mixpanel-mode=daily --mixpanel-region=EU

# Historical backfill for a date range
python run_queries.py --ingestor=mixpanel --mixpanel-mode=backfill \
  --mixpanel-from-date=2026-01-01 --mixpanel-to-date=2026-06-30
```

`--mixpanel-region` selects the data-residency region (`US`, `EU`, `IN`); `--mixpanel-event-filter` restricts the export to a JSON array of event names.

### CoW Mode

Fetches open orders and trade fees from the CoW Protocol API for owner addresses read from a source table (`--cow-source-table`, e.g. `dbt.int_execution_cow_trades`). Tables land in the database configured via `COW_DATABASE`.

| Mode | Behavior |
|------|----------|
| `daily` | Refresh orders for owners active in the last `--cow-lookback-days` (default 7) |
| `backfill` | Fetch for all owners, optionally bounded by `--cow-backfill-from` |
| `repair` | Re-fetch orders whose on-chain fills are missing from the target table |

!!! warning "CoW API access requires TLS impersonation"
    The CoW API sits behind a CloudFront WAF that blocks plain Python TLS clients by JA3 fingerprint, even with a valid `X-API-Key`. The ingestor uses `curl_cffi` with Chrome browser impersonation to make requests. Keep this dependency in place when extending the ingestor.

### Snapshot Mode (Governance)

Ingests Snapshot Hub GraphQL data — space metadata, proposals, votes, and followers — into the database configured via `GOVERNANCE_DATABASE` (`snapshot_space`, `snapshot_proposals`, `snapshot_votes`, `snapshot_follows`).

```bash
# Daily: refresh open + recently-closed proposals
python run_queries.py --ingestor=snapshot --snapshot-mode=daily --snapshot-vote-refresh-days=5

# Full backfill of all proposals and votes
python run_queries.py --ingestor=snapshot --snapshot-mode=backfill
```

### Forum Mode (Governance)

Crawls the Discourse forum JSON API into `forum_categories`, `forum_topics`, `forum_posts`, and `forum_users` in the same governance database. Daily mode processes topics bumped since the stored watermark; backfill crawls everything (bounded by `--forum-max-pages`, 30 topics per page).

```bash
python run_queries.py --ingestor=forum --forum-mode=daily
```

### Dune Execute-Only Mode

Triggers execution of dedicated Dune queries without ingesting results (used to refresh Dune-side materializations):

```bash
python run_queries.py --ingestor=dune-execute-only \
  --dune-execute-only-query-ids=123456,234567
```

## Configuration

### ClickHouse Connection

| Variable | Default | Description |
|----------|---------|-------------|
| `CH_HOST` | -- | ClickHouse server hostname |
| `CH_PORT` | `9000` | ClickHouse native protocol port |
| `CH_USER` | -- | Authentication username |
| `CH_PASSWORD` | -- | Authentication password |
| `CH_DB` | -- | Target database name |
| `CH_SECURE` | `False` | Use TLS connection |
| `CH_VERIFY` | `False` | Verify TLS certificate |

### S3 Integration

| Variable | Default | Description |
|----------|---------|-------------|
| `S3_ACCESS_KEY` | -- | AWS access key ID |
| `S3_SECRET_KEY` | -- | AWS secret access key |
| `S3_BUCKET` | `prod-use1-gnosis` | S3 bucket name |
| `S3_REGION` | `us-east-1` | AWS region |

### Data Source URLs

| Variable | Description |
|----------|-------------|
| `EMBER_DATA_URL` | URL to the Ember electricity CSV data |

### Variable Substitution in SQL

SQL files support `{{VARIABLE_NAME}}` placeholders that are replaced with values from environment variables prefixed with `CH_QUERY_VAR_`. For example:

- Environment variable: `CH_QUERY_VAR_EMBER_DATA_URL=https://example.com/data.csv`
- In SQL: `FROM url('{{EMBER_DATA_URL}}', 'CSV')`

## Docker Compose Services

The `docker-compose.yml` provides preconfigured services:

| Service | Mode | Description |
|---------|------|-------------|
| `click-runner` | Any | Generic service, accepts any `--ingestor` argument |
| `ember-ingestor` | CSV | Preconfigured for Ember electricity data |
| `probelab-agent-semvers-ingestor` | Parquet | Preconfigured for ProbeLab agent version data |

```bash
# Run the Ember ingestor
docker-compose run --rm ember-ingestor

# Run the ProbeLab ingestor
docker-compose run --rm probelab-agent-semvers-ingestor

# Run arbitrary queries
docker-compose run click-runner --ingestor=query \
  --queries=queries/file1.sql
```

## Scheduling

click-runner services are typically scheduled as daily cron jobs:

```bash
# Daily Ember data update at 2 AM
0 2 * * * cd /path/to/click-runner && docker-compose run --rm ember-ingestor

# Daily ProbeLab data update at 3 AM
0 3 * * * cd /path/to/click-runner && docker-compose run --rm probelab-agent-semvers-ingestor
```

A convenience script `cron_setup.sh` is included to automatically create these cron entries.

## Adding New Data Sources

### New CSV Source

1. Create SQL files in `queries/new_source/`:
    - `create_table.sql` -- table schema definition
    - `insert_data.sql` -- INSERT using ClickHouse URL engine
    - `optimize.sql` (optional) -- post-load optimization
2. Set the data URL as an environment variable
3. Run with `--ingestor=csv`

### New Parquet Source

1. Create a table definition SQL file in `queries/new_source/`
2. Run with `--ingestor=parquet`, specifying the S3 path pattern with `{{DATE}}` placeholder
3. Add a Docker Compose service for convenient scheduling

### New File Format

Extend the framework by creating a new ingestor class that inherits from `BaseIngestor` in `ingestors/`:

1. Create `ingestors/new_format_ingestor.py` extending `BaseIngestor`
2. Implement the `ingest()` method
3. Register the new ingestor type in `run_queries.py`

## Project Structure

```
click-runner/
├── run_queries.py          # Main CLI entry point
├── ingestors/
│   ├── base.py             # Abstract base ingestor
│   ├── csv_ingestor.py     # CSV ingestion logic
│   ├── parquet_ingestor.py # Parquet/S3 ingestion logic
│   ├── gdrive_ingestor.py  # Google Drive CSV imports
│   ├── mixpanel_ingestor.py            # Mixpanel raw events
│   ├── mixpanel_profiles_ingestor.py   # Mixpanel user profiles
│   ├── cow_ingestor.py     # CoW API orders + fees
│   ├── snapshot_ingestor.py# Snapshot governance data
│   └── forum_ingestor.py   # Discourse forum data
├── utils/
│   ├── s3.py               # S3 file discovery utilities
│   ├── db.py               # ClickHouse connection helpers
│   └── date.py             # Date parsing utilities
├── queries/
│   ├── ember/              # Ember electricity data SQL
│   ├── probelab/           # ProbeLab metrics SQL
│   ├── governance/         # Snapshot + forum table DDL
│   ├── celo_gpay/          # Gnosis Pay on Celo tables
│   ├── mixpanel/           # Mixpanel raw event tables
│   ├── mixpanel_profiles/  # Mixpanel profile tables
│   ├── cow/                # CoW API tables
│   └── dune/               # Dune imports
├── Dockerfile
└── docker-compose.yml
```

## ClickHouse Table Schemas

The legacy CSV/Parquet sources below land in the `crawlers_data` database. The newer API ingestors write to env-configured databases instead: governance tables via `GOVERNANCE_DATABASE`, Mixpanel tables via `MIXPANEL_DATABASE`, and CoW tables via `COW_DATABASE`; Celo Gnosis Pay tables land in `crawlers_data.celo_gpay_*`.

??? note "Table: `crawlers_data.dune_labels`"
    **Engine:** MergeTree
    **ORDER BY:** (address, label, introduced_at)

    | Column | Type | Notes |
    |--------|------|-------|
    | `address` | String | Contract or EOA address |
    | `label` | String | Human-readable label |
    | `introduced_at` | DateTime | When the label was first seen |
    | `source` | LowCardinality(String) | Label data source |

??? note "Table: `crawlers_data.dune_prices`"
    **Engine:** MergeTree
    **ORDER BY:** (symbol, block_date)

    | Column | Type | Notes |
    |--------|------|-------|
    | `block_date` | Date | Price date |
    | `symbol` | LowCardinality(String) | Token symbol |
    | `price` | Float64 | Token price in USD |

??? note "Table: `crawlers_data.dune_bridge_flows`"
    **Engine:** MergeTree
    **ORDER BY:** (bridge, source_chain, dest_chain, token, timestamp)

    | Column | Type | Notes |
    |--------|------|-------|
    | `timestamp` | DateTime | Bridge event timestamp |
    | `bridge` | LowCardinality(String) | Bridge protocol name |
    | `source_chain` | LowCardinality(String) | Origin chain |
    | `dest_chain` | LowCardinality(String) | Destination chain |
    | `token` | LowCardinality(String) | Bridged token |
    | `amount_token` | Float64 | Amount in token units |
    | `amount_usd` | Float64 | Amount in USD |
    | `net_usd` | Float64 | Net USD flow |

??? note "Table: `crawlers_data.dune_gno_supply`"
    **Engine:** MergeTree
    **ORDER BY:** (label, block_date)

    | Column | Type | Notes |
    |--------|------|-------|
    | `label` | LowCardinality(String) | Supply category label |
    | `block_date` | Date | Snapshot date |
    | `supply` | Float64 | GNO supply amount |

??? note "Table: `crawlers_data.ember_electricity_data`"
    **Engine:** ReplacingMergeTree(version)
    **ORDER BY:** (Date, Area, Category, Subcategory, Variable)

    | Column | Type | Notes |
    |--------|------|-------|
    | `Area` | String | Country or region |
    | `ISO 3 code` | String | ISO 3166-1 alpha-3 country code |
    | `Date` | Date | Data date |
    | `Continent` | String | Continent name |
    | `Category` | String | Electricity data category |
    | `Subcategory` | String | Electricity data subcategory |
    | `Variable` | String | Measured variable |
    | `Unit` | String | Measurement unit |
    | `Value` | Float64 | Measured value |
    | `YoY absolute change` | Float64 | Year-over-year absolute change |
    | `YoY % change` | Float64 | Year-over-year percentage change |
    | `version` | DateTime | Row version for deduplication |

??? note "Table: `crawlers_data.gpay_wallets`"
    **Engine:** MergeTree
    **ORDER BY:** (SAFE_address, SAFE_createdAt)

    | Column | Type | Notes |
    |--------|------|-------|
    | `SAFE_address` | String | Safe wallet address |
    | `SAFE_createdAt` | DateTime | Wallet creation timestamp |
