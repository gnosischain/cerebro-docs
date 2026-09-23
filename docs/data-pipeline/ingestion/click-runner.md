# click-runner

click-runner is a modular Python toolkit for loading data into ClickHouse from various external sources. It supports SQL query execution, CSV ingestion via ClickHouse URL engine, Parquet ingestion from S3 buckets, Google Drive CSV imports, and dedicated API ingestors for Mixpanel, CoW Protocol, Snapshot, and Discourse.

## Purpose

Not all data in the Gnosis Analytics pipeline comes from blockchain nodes. click-runner handles the ingestion of external datasets:

- **Ember** -- global electricity generation data used for ESG carbon footprint calculations
- **ProbeLab** -- daily peer-to-peer network metrics (agent versions, peer distributions, crawl statistics)
- **Governance** -- Snapshot proposals, votes, and followers plus Discourse forum topics, posts, and users (feeds the [Governance Explorer](../../mcp/mini-apps/governance.md) mini-app)
- **Mixpanel** -- product-analytics events and user profiles for Gnosis App and Gnosis Pay
- **CoW Protocol** -- open orders and trade fees from the CoW API
- **External prices** -- CoinGecko and DefiLlama token prices (`crawlers_data.coingecko_prices`, `defillama_prices`)
- **Dune** -- labels, prices and bridge flows exported from saved Dune queries
- **HOPR** -- network node and channel snapshots into `hopr_db`
- **Google Drive** -- ad-hoc CSV datasets shared via Drive
- **Administrative queries** -- schema migrations, data maintenance, and custom SQL operations

## Ingestion Modes

click-runner selects an ingestor via the `--ingestor` parameter: `query`, `csv`, `parquet`, `gdrive`, `dune-execute-only`, `mixpanel`, `mixpanel-profiles`, `cow`, `external-prices`, `snapshot`, or `forum`.

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

| Variable | Production | Description |
|----------|---------|-------------|
| `CH_HOST` | private endpoint | ClickHouse Cloud hostname, reached over the private endpoint |
| `CH_PORT` | `443` | HTTPS port (the code default `9000` is the local native-protocol port) |
| `CH_USER` | -- | Authentication username |
| `CH_PASSWORD` | -- | Authentication password |
| `CH_DB` | -- | Target database name |
| `CH_SECURE` | `true` | TLS |
| `CH_VERIFY` | `False` | TLS certificate verification is off in production — one line away from `CH_SECURE`, do not confuse them |

### Object storage (ProbeLab parquet only)

| Variable | Description |
|----------|-------------|
| `CH_QUERY_VAR_S3_ACCESS_KEY`, `CH_QUERY_VAR_S3_SECRET_KEY`, `CH_QUERY_VAR_S3_BUCKET`, `CH_QUERY_VAR_S3_REGION` | Credentials and location of the ProbeLab parquet bucket, injected as query variables |

### Data Source URLs

| Variable | Description |
|----------|-------------|
| `CH_QUERY_VAR_EMBER_DATA_URL` | URL to the Ember electricity CSV data |

### Variable Substitution in SQL

SQL files support `{{VARIABLE_NAME}}` placeholders that are replaced with values from environment variables prefixed with `CH_QUERY_VAR_`. For example:

- Environment variable: `CH_QUERY_VAR_EMBER_DATA_URL=https://example.com/data.csv`
- In SQL: `FROM url('{{EMBER_DATA_URL}}', 'CSV')`

## Operating and recovering

### How it runs

**14 CronJobs, one image**, pulling off-chain APIs into `crawlers_data`, `governance_db`, `mixpanel_ga` and `hopr_db`. Twelve append their ingestor flags via `args`; two (`dune-all`, `probelab`) replace `command` with a bash script from the deployment stack. Almost all run between **03:00 and 05:00 UTC**; Ember runs twice a month. Two are suspended by design: the Dune execute-only ingestor and the ProbeLab-latest ingestor.

Zero pods outside the window is the healthy steady state — these are CronJobs.

### Health — a green job is not fresh data

!!! warning "`dune-all` runs three queries in one pod behind a wrapper that exits 0 unless all three fail"
    Per-query status exists only in the log lines — look for `ingestion (FAILED|completed successfully)` and `"event": "(run_success|run_failure|run_exception)"`. Other silent-degradation shapes in this stack: a missing `ALTER` grant turns the price ingesters' post-insert prune into **duplicate rows** rather than an error; a keyless CoinGecko run silently drops tokens; `governance-forum` falls back to a full 400-page crawl if its watermark read fails.

**Freshness is the only real signal.** Per table, as a ratio against its SLA:

```sql
SELECT tbl, dateDiff('hour', latest_data, now()) / threshold_h AS staleness_ratio
FROM (
  SELECT 'dune_labels' AS tbl, toDateTime(max(introduced_at)) AS latest_data, 60 AS threshold_h FROM crawlers_data.dune_labels
  UNION ALL SELECT 'dune_prices', toDateTime(max(block_date)), 60 FROM crawlers_data.dune_prices
  UNION ALL SELECT 'dune_bridge_flows', toDateTime(max(timestamp)), 60 FROM crawlers_data.dune_bridge_flows
  UNION ALL SELECT 'coingecko_prices', toDateTime(max(ingested_at)), 30 FROM crawlers_data.coingecko_prices
  UNION ALL SELECT 'defillama_prices', toDateTime(max(ingested_at)), 30 FROM crawlers_data.defillama_prices
  UNION ALL SELECT 'circles_blacklisted', toDateTime(max(ingested_at)), 30 FROM crawlers_data.circles_blacklisted
  UNION ALL SELECT 'cow_api_trade_fees', toDateTime(max(ingested_at)), 30 FROM crawlers_data.cow_api_trade_fees
);
```

**The Dune lag rule.** Dune-backed tables land **T-1 or T-2**, which is why their SLA is 60 h and everything else is 30 h. One day behind is expected. Three days is a stall. Do not delete-and-re-ingest a day that simply has not landed: the dune tables are plain MergeTree with no dedupe, and a duplicate doubles the bridge-flow sums.

Prometheus `click_runner_*` counters are a debug surface, not a health signal: the pods are ephemeral and the scrape races their lifetime.

### Rerun

Trigger the ingestor's CronJob as a one-off Job ([how](../../operations/runbooks/one-shot-jobs.md)). `concurrencyPolicy: Forbid` cannot see a hand-created Job — check nothing is active first, and do not fire one near a scheduled slot. To rerun **one leg** of `dune-all`, clone it with `args` overridden to that leg's invocation:

```bash
python run_queries.py --ingestor=csv \
  --create-table-sql=queries/dune/labels/create_table.sql \
  --insert-sql=queries/dune/labels/insert_daily.sql
```

!!! warning "`circles-blacklist` truncates before inserting"
    Between the TRUNCATE and the INSERT the table is empty, and nothing alerts on zero rows — only on staleness. A partial manual re-run, or killing it mid-run, is destructive.

!!! warning "Suspending and un-suspending"
    Never un-suspend a cron within its 1800 s `startingDeadlineSeconds` unless you want the missed slot replayed immediately. And every `cron-miss-*` alert is guarded by `unless kube_cronjob_spec_suspend == 1`, so a **suspended** cron alerts on nothing at all.

### Backfill, per ingestor

| Ingestor | Invocation |
|---|---|
| Dune | the `dune-{labels,prices,bridge-flows}-full-ingestor` Compose services (the "full" query IDs; there is no date range) |
| Mixpanel | `--ingestor=mixpanel --mixpanel-mode=backfill --mixpanel-from-date=… --mixpanel-to-date=…` |
| CoW fees | `--ingestor=cow --cow-mode=backfill --cow-max-pages=500` (also `--cow-mode=repair`) |
| External prices | `--ingestor=external-prices --external-prices-mode=backfill` (CoinGecko beyond 365 d needs `scripts/full_history_coingecko_prices.py`) |
| Snapshot / forum | `--ingestor={snapshot,forum} --{snapshot,forum}-mode=backfill` |

!!! warning "Two backfills that look like success and are not"
    Re-ingesting Mixpanel without first clearing `mixpanel_ingestion_state` for the range skips every already-complete day and exits 0. And a suspension longer than **5 days** loses Snapshot votes permanently: daily mode only refreshes proposals open or closed within `--snapshot-vote-refresh-days` (5), and nothing surfaces the gap. After a long outage, run manually with a wider window rather than just un-suspending.

Find the proposals with lost votes (the alias goes **before** `FINAL`, or it is a syntax error):

```sql
SELECT p.id, p.end_ts, count(v.id) AS votes
FROM governance_db.snapshot_proposals AS p FINAL
LEFT JOIN governance_db.snapshot_votes AS v FINAL ON v.proposal = p.id
WHERE p.end_ts BETWEEN ⟨from⟩ AND ⟨to⟩ GROUP BY p.id, p.end_ts HAVING votes = 0;
```

### Corrupt rows — delete then re-ingest

Only for the plain-MergeTree targets (the dune and external-prices tables). ReplacingMergeTree targets (cow, snapshot, forum, hopr, mixpanel) self-correct on re-ingest.

```sql
ALTER TABLE crawlers_data.⟨table⟩ DELETE WHERE ⟨date_col⟩ = ⟨day⟩ SETTINGS mutations_sync = 2;
```

!!! warning "`mutations_sync = 2` is not optional"
    Without it the lightweight delete keeps executing server-side after the client reports failure — the DELETE lands and your re-ingest runs against a moving table. Run it outside 03:00–05:00 UTC. And never `DROP PARTITION` on `hopr_db.hopr_network_online_hourly` or `hopr_network_nodes`: they are partitioned by **year**, and the hourly series is the only multi-year HOPR history.

### CoW 403

Never retry immediately. The CloudFront block lasts ~1 h and retrying inside it prolongs the cooldown for **everything sharing the cluster's egress address** — including [cow-indexer](cow-indexer.md).

`cow-fees` timing is settled: a trade on day X reaches `fct_execution_cow_trades` complete at 06:00 on X+2 under **any** schedule, because the mart is `insert_overwrite` partitioned by month and rebuilds the whole current month each run. Moving the job does not change that. The completeness signal is the `cow-fees-coverage-incomplete` alert, which measures the anti-join of on-chain fills against the raw fee table.

### Then dbt

Find the consumers and rerun scoped — `dbt ls -s source:crawlers_data.⟨table⟩+ --resource-type model --output name` — following [dbt reprocess](../../operations/runbooks/dbt-reprocess.md). For a Dune prices gap specifically, [Recovering from a prices gap](../../operations/prices-gap-recovery.md) is the full procedure. There is no lock against the 06:00 cron or the 45-second live loop.

!!! note "Expected noise"
    - The Dune execute-only and ProbeLab-latest ingestors permanently suspended.
    - `ember-ingestor` stale for two weeks at a time — it runs twice a month with a 480 h SLA.
    - `click_runner_*` panels empty between runs.

!!! info "Internal runbook"
    [runbooks/26-click-runner.md](https://github.com/gnosisdevops/infrastructure-gnosis-analytics/blob/main/runbooks/26-click-runner.md) — private repository; carries the cluster-specific commands for this page.

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
