---
title: Platform Overview
description: Overview of the Gnosis Analytics 15-repo ecosystem
---

# Platform Overview

Gnosis Analytics is a blockchain analytics platform composed of 15 repositories that together form a complete data pipeline for Gnosis Chain. The system ingests raw blockchain data from multiple sources, stores it in ClickHouse, transforms it through dbt models, and serves it through REST APIs, AI-powered tools, and interactive dashboards.

## Architecture Layers

The platform is organized into four distinct layers, each with clearly defined responsibilities.

### 1. Data Acquisition Layer

The acquisition layer is responsible for extracting raw data from Gnosis Chain nodes, the peer-to-peer network, and external data providers.

| Repository | Description |
|-----------|-------------|
| **cryo-indexer** | Indexes execution layer (EL) data using [Cryo](https://github.com/paradigmxyz/cryo). Extracts blocks, transactions, logs, traces, and state data from Gnosis Chain EL nodes. |
| **beacon-indexer** | Indexes consensus layer (CL) data directly from the Beacon API. Captures validator activity, attestations, proposals, sync committees, and blob sidecars. |
| **click-runner** | Ingests external data from third-party sources including Ember (energy data), ProbeLab (network metrics), Dune Analytics, Snapshot and Discourse governance data, Mixpanel events and profiles, CoinGecko and DefiLlama prices, CoW trade fees and HOPR network snapshots. Runs as 14 scheduled import jobs. |
| **cow-indexer** | Standalone multi-chain CoW Protocol indexer. Reads canonical CoW contract events via EVM JSON-RPC, enriches orders and settlements through the public CoW API, and imports off-chain order-book history from export bundles into `cow_db`. |
| **rpc-state-indexer** | Historical EVM state indexer. Reads contract state at exact UTC day-end anchor blocks via archive JSON-RPC and publishes only verified snapshots into `rpc_state_indexer`, serving as an independent cross-check of warehouse balances. |
| **rpc-log-indexer** | Durable `eth_getLogs` event indexer. Decodes the Snapshot DelegateRegistry on Ethereum and Gnosis into `rpc_log_indexer` with per-chain checkpoints and reorg-safe canonical views. |
| **envio_ga-indexer** | Mirrors the Circles / Metri / Gnosis Pay GraphQL API (28 entities) into `envio_ga`, with a realtime loop and a daily reconcile for upstream deletes. |
| **nebula** | Crawls the Gnosis Chain P2P DHT (Distributed Hash Table) network to discover and monitor peer connectivity, client diversity, and network topology. |
| **ip-crawler** | Enriches peer data from nebula with IP geolocation information. Maps IP addresses to geographic coordinates, ISPs, and autonomous system numbers. |

### 2. Data Storage Layer

All raw and processed data is stored in a centralized **ClickHouse Cloud** cluster. ClickHouse provides columnar storage optimized for analytical queries across billions of rows.

The cluster contains the following databases:

| Database | Contents |
|----------|----------|
| `execution`, `execution_live`, `celo_execution` | Raw execution layer data: blocks, transactions, logs, traces, contracts, native transfers |
| `consensus` | Raw and transformed consensus layer data: blocks, validators, rewards, sidecars |
| `crawlers_data` | External data imported via click-runner (Dune, prices, CoW fees) and ip-crawler |
| `governance_db` | Snapshot proposals/votes and Discourse forum data via click-runner |
| `mixpanel_ga`, `hopr_db` | Product analytics; HOPR network snapshots via click-runner |
| `nebula`, `nebula_discv4` | P2P network crawl data: peer sessions, discovery results, agent strings |
| `cow_db` | CoW Protocol trades, settlements, and order-book history via cow-indexer |
| `rpc_state_indexer` | Verified day-end contract state published by rpc-state-indexer |
| `rpc_log_indexer` | Decoded DelegateRegistry events from rpc-log-indexer |
| `envio_ga` | Circles / Metri / Gnosis Pay entities mirrored by envio_ga-indexer |
| `dbt` | Transformed and modeled data produced by dbt-cerebro |

### 3. Data Analysis & Modeling Layer

The modeling layer transforms raw data into analytics-ready datasets using dbt (data build tool).

| Repository | Description |
|-----------|-------------|
| **dbt-cerebro** | The core dbt project containing about 1,370 models (roughly 1,250 in production) organized into 15 modules, including `execution`, `consensus`, `p2p`, `bridges`, `ESG`, `probelab`, `crawlers_data`, `contracts`, `celo`, `revenue`, `quarterly_data`, `mixpanel_ga`, `mta`, and `mmm`. Models follow a staging/intermediate/marts pattern and produce the API-facing views. |
| **dbt-schema-gen** | An LLM-powered tool that automatically generates dbt schema YAML files. Analyzes SQL models and produces column descriptions, tests, and documentation. |
| **cryo-base** | Docker base image for the Cryo indexer. Provides a pre-built ARM64 container with Cryo installed, used as the foundation for cryo-indexer deployments. |

### 4. Data Serving Layer

The serving layer exposes transformed data to end users through three complementary interfaces.

| Repository | Description |
|-----------|-------------|
| **cerebro-api** | A FastAPI-based REST API that auto-generates endpoints from the dbt manifest. Provides tiered authentication, rate limiting, and both GET and POST query interfaces. |
| **cerebro-mcp** | An AI assistant tool server implementing the Model Context Protocol (MCP). Enables LLM-powered analysis of Gnosis Chain data through natural language queries, chart generation, and report building. |
| **metrics-dashboard** | A React + ECharts web application providing interactive dashboards and visualizations of Gnosis Chain metrics. Renders charts from the cerebro-api data. |

## Repository Summary

| Repository | Language | Purpose |
|-----------|----------|---------|
| cryo-indexer | Python + Cryo (Rust) | Execution layer data indexing via Cryo |
| beacon-indexer | Python | Consensus layer data indexing from Beacon API |
| click-runner | Python / SQL | External data ingestion (Dune, CoinGecko, DefiLlama, CoW fees, Snapshot, Discourse, Mixpanel, HOPR, Ember) |
| cow-indexer | Python / ClickHouse | Multi-chain CoW Protocol event + order-book indexing |
| rpc-state-indexer | Python / ClickHouse | Verified historical contract state via archive RPC |
| rpc-log-indexer | Python / ClickHouse | Durable event-log decoding (Snapshot DelegateRegistry) |
| envio_ga-indexer | Python / ClickHouse | Mirror of the Circles / Metri / Gnosis Pay GraphQL API |
| nebula | Go | P2P DHT network crawler |
| ip-crawler | Python | IP geolocation enrichment for peer data |
| dbt-cerebro | SQL / dbt | ~1,370 analytics models across 15 modules |
| dbt-schema-gen | Python | LLM-powered dbt schema generation |
| cryo-base | Docker | Base image for Cryo deployments |
| cerebro-api | Python / FastAPI | REST API with auto-generated endpoints |
| cerebro-mcp | Python / TypeScript | AI assistant tools (MCP server) |
| metrics-dashboard | TypeScript / React | Interactive analytics dashboards |

## Next Steps

- [Architecture](architecture.md) -- Detailed technical architecture with diagrams
- [Quick Start](quickstart.md) -- Make your first API call
- [API Reference](../api/index.md) -- Full REST API documentation
