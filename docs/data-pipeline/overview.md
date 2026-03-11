# Pipeline Overview

This document describes the end-to-end data pipeline that powers the Gnosis Analytics platform. The pipeline collects raw blockchain data from multiple sources, stores it in ClickHouse Cloud, transforms it through layered dbt models, and serves it through a REST API.

## Data Sources

The pipeline ingests data from four categories of sources.

### Execution Layer

The execution layer provides transaction-level blockchain data. The **cryo-indexer** connects to a Gnosis Chain RPC node and extracts:

- **Blocks** -- headers, timestamps, gas usage, withdrawals
- **Transactions** -- sender, receiver, value, gas, input data, status
- **Logs** -- smart contract event emissions
- **Traces** -- internal call trees and execution traces
- **Contracts** -- contract creation events
- **Native transfers** -- xDAI transfers (including internal)
- **State diffs** -- balance, nonce, code, and storage changes

### Consensus Layer

The consensus layer provides validator and attestation data. Two tools handle this:

- **beacon-indexer** -- fetches live data from the beacon node REST API, covering blocks, validators, attestations, sync committees, and rewards
- **era-parser** -- parses compressed historical era archive files (8192 slots per era), extracting all beacon chain data types across all forks from Phase 0 through Electra

### Peer-to-Peer Network

Network topology data is collected by:

- **nebula** -- a DHT crawler that discovers peers, records reachability, and captures client metadata (agent versions, protocols, fork digests)
- **ip-crawler** -- enriches discovered peer IPs with geolocation data from ipinfo.io (city, country, ASN, organization)

### External Sources

Additional datasets are ingested via **click-runner**:

- **Ember** -- global electricity generation data (for ESG carbon footprint calculations)
- **ProbeLab** -- daily P2P network metrics (agent versions, peer counts, crawl statistics)
- **Administrative queries** -- schema migrations and maintenance SQL

## Storage Architecture

All data lands in **ClickHouse Cloud**, organized across dedicated databases:

| Database | Contents | Primary Indexer |
|----------|----------|-----------------|
| `execution` | Blocks, transactions, logs, traces, contracts, state diffs | cryo-indexer |
| `consensus` | Beacon blocks, validators, attestations, sync committees, rewards | beacon-indexer, era-parser |
| `nebula` | Peer visits, peer metadata, crawl sessions | nebula |
| `crawlers_data` | IP geolocation, ProbeLab metrics | ip-crawler, click-runner |
| `dbt` | All transformed models (staging, intermediate, facts, API views) | dbt-cerebro |

ClickHouse was chosen for its columnar storage, high compression ratios, and fast analytical query performance. Tables use `ReplacingMergeTree` engines with monthly partitioning for efficient incremental processing and deduplication.

## Transformation Layer

Raw data is transformed by **dbt-cerebro**, a dbt project containing approximately 400 SQL models organized into eight domain modules. The transformation follows a strict layered architecture:

```
Raw Tables (execution.blocks, consensus.blocks, ...)
    |
    v
Staging (stg_*) -- Light cleanup, type casting, column renaming. Materialized as views.
    |
    v
Intermediate (int_*) -- Business logic, joins, aggregations. Materialized as incremental tables.
    |
    v
Facts (fct_*) -- Business-ready metrics and KPIs. Materialized as views.
    |
    v
API (api_*) -- Optimized for REST API consumption. Materialized as views.
```

Key transformation capabilities include:

- **Incremental processing** using `delete+insert` strategy with monthly partitions
- **Contract ABI decoding** that converts raw transaction input data and event logs into human-readable function calls and events
- **Cross-layer joins** linking execution transactions to consensus proposers
- **Time-series aggregation** at daily, weekly, and monthly grains

## Serving Layer

Transformed data is consumed through:

- **REST API** (`cerebro-api`) -- serves `api_*` model data as HTTP endpoints, with auto-discovery from the dbt manifest
- **MCP Tools** -- AI-powered natural language interface for querying Gnosis Chain analytics
- **Dashboards** -- visualization layer built on the API endpoints

## Data Freshness

| Data Type | Typical Latency | Update Mechanism |
|-----------|----------------|------------------|
| Execution layer (blocks, txs) | ~2 minutes | cryo-indexer continuous mode (10s poll, 12 block confirmations) |
| Consensus layer (validators) | ~5 minutes | beacon-indexer real-time sync |
| P2P network topology | ~30 minutes | nebula crawl cycles |
| IP geolocation | ~1 hour | ip-crawler continuous mode (60s batch intervals) |
| dbt transformations | Varies by model | Scheduled dbt runs |
| External sources (Ember, ProbeLab) | Daily | click-runner cron jobs |
