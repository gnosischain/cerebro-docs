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

The consensus layer provides validator and attestation data. The **beacon-indexer** fetches it from the beacon node REST API — blocks, rewards and data-column sidecars in real time, plus a daily validators snapshot — and transforms the raw payloads into structured tables. Historical ranges are loaded with the same `load backfill` command.

### Contract state and events

- **rpc-state-indexer** -- reads ERC-20 balances, supply and pool reserves at exact UTC day-end anchor blocks through archive RPC, publishing only verified snapshots
- **rpc-log-indexer** -- decodes Snapshot DelegateRegistry events on Ethereum and Gnosis via `eth_getLogs`
- **cow-indexer** -- CoW Protocol settlements, trades and order-book history across 11 chains
- **envio_ga-indexer** -- mirrors the Circles / Metri / Gnosis Pay GraphQL API into ClickHouse

### Peer-to-Peer Network

Network topology data is collected by:

- **nebula** -- a DHT crawler that discovers peers, records reachability, and captures client metadata (agent versions, protocols, fork digests)
- **ip-crawler** -- enriches discovered peer IPs with geolocation data from ipinfo.io (city, country, ASN, organization)

### External Sources

Additional datasets are ingested via **click-runner**:

- **Dune** -- labels, prices and bridge flows (land T-1 to T-2)
- **CoinGecko and DefiLlama** -- token prices
- **Snapshot and Discourse** -- governance proposals, votes and forum activity
- **Mixpanel** -- product-analytics events and profiles
- **HOPR** -- network node and channel snapshots
- **CoW API** -- trade fees
- **Ember** -- global electricity generation data (for ESG carbon footprint calculations), twice a month

## Storage Architecture

All data lands in **ClickHouse Cloud**, organized across dedicated databases:

| Database | Contents | Primary Indexer |
|----------|----------|-----------------|
| `execution` | Blocks, transactions, logs, traces, contracts, native transfers (Gnosis, ~66 min behind head) | cryo-indexer |
| `execution_live` | The same, ~1 min behind head, two-day TTL | cryo-indexer |
| `celo_execution` | Celo blocks, transactions, logs | cryo-indexer |
| `consensus` | Beacon blocks, validators, rewards, sidecars, and the transformed tables | beacon-indexer |
| `rpc_state_indexer` | Verified day-end contract state | rpc-state-indexer |
| `rpc_log_indexer` | Decoded DelegateRegistry events, canonical views | rpc-log-indexer |
| `cow_db` | CoW settlements, trades, order-book work items | cow-indexer |
| `envio_ga` | Circles / Metri / Gnosis Pay entities | envio_ga-indexer |
| `nebula`, `nebula_discv4` | Peer visits, peer metadata, crawl sessions | nebula |
| `crawlers_data` | IP geolocation, prices, Dune exports, CoW fees, Circles blacklist | ip-crawler, click-runner |
| `governance_db`, `mixpanel_ga`, `hopr_db` | Governance, product analytics, HOPR network snapshots | click-runner |
| `dbt` | All transformed models (staging, intermediate, facts, API views) | dbt-cerebro |

ClickHouse was chosen for its columnar storage, high compression ratios, and fast analytical query performance. dbt models use `ReplacingMergeTree` with monthly partitioning; several raw targets (the cryo `execution*` tables, `cow_db`, the plain-MergeTree Dune tables) do **not** dedupe re-inserted rows, which is why every ingestor enforces a single writer and every repair deletes before it re-inserts. The memory cap is shared by every concurrent query — see [Operations](../operations/index.md).

## Transformation Layer

Raw data is transformed by **dbt-cerebro**, a dbt project containing about 1,370 SQL models (roughly 1,250 tagged `production`) organized into 15 domain modules. The transformation follows a strict layered architecture:

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

The healthy value is not zero for most sources, and the reason matters — an operator who does not know why `execution.blocks` is an hour behind will chase it.

| Data | Healthy lag | Why |
|-----------|----------------|------------------|
| `execution` (blocks, txs, logs) | ~66 minutes | `CONFIRMATION_BLOCKS=720` at 5 s/block, 60 s poll |
| `execution_live` | ~1 minute | `CONFIRMATION_BLOCKS=6` |
| `consensus` | ~67 minutes | `REALTIME_SLOT_DELAY=700` slots |
| `consensus` validators | daily | one snapshot per UTC day, 02:00 cron, ~4 h |
| `rpc_state_indexer` | yesterday | published overnight, 00:19–03:11 UTC |
| `rpc_log_indexer` | checkpoint < 1 h | judge by checkpoint age — the contract emits a handful of events a month |
| `cow_db` | ≤ ~6 min **per chain** | a summed check hides one dead chain |
| P2P network topology | minutes | continuous crawls; a crawler restart is a missed sample, not a gap |
| IP geolocation | daily | 02:00 UTC CronJob |
| `crawlers_data` (click-runner) | 30 h SLA; Dune 60 h | Dune lands T-1 to T-2; the 03:00–05:00 window |
| dbt transformations | 06:00 UTC daily; `tag:live` every 45 s | the cron rebuilds from whatever the raw layer held at 06:00 — it does not wait |

The morning-check page under [Operations](../operations/troubleshooting.md) carries the queries behind each row.
