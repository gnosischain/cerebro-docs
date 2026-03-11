---
title: Platform Overview
description: Overview of the Gnosis Analytics 13-repo ecosystem
---

# Platform Overview

Gnosis Analytics is a blockchain analytics platform composed of 13 repositories that together form a complete data pipeline for Gnosis Chain. The system ingests raw blockchain data from multiple sources, stores it in ClickHouse, transforms it through dbt models, and serves it through REST APIs, AI-powered tools, and interactive dashboards.

## Architecture Layers

The platform is organized into four distinct layers, each with clearly defined responsibilities.

### 1. Data Acquisition Layer

The acquisition layer is responsible for extracting raw data from Gnosis Chain nodes, the peer-to-peer network, and external data providers.

| Repository | Description |
|-----------|-------------|
| **cryo-indexer** | Indexes execution layer (EL) data using [Cryo](https://github.com/paradigmxyz/cryo). Extracts blocks, transactions, logs, traces, and state data from Gnosis Chain EL nodes. |
| **beacon-indexer** | Indexes consensus layer (CL) data directly from the Beacon API. Captures validator activity, attestations, proposals, sync committees, and blob sidecars. |
| **era-parser** | Parses historical era archive files for backfilling consensus layer data. Processes the `.era` file format containing historical beacon chain state. |
| **click-runner** | Ingests external data from third-party sources including Ember (energy data), ProbeLab (network metrics), and Dune Analytics. Runs scheduled ClickHouse-based import jobs. |
| **nebula** | Crawls the Gnosis Chain P2P DHT (Distributed Hash Table) network to discover and monitor peer connectivity, client diversity, and network topology. |
| **ip-crawler** | Enriches peer data from nebula with IP geolocation information. Maps IP addresses to geographic coordinates, ISPs, and autonomous system numbers. |

### 2. Data Storage Layer

All raw and processed data is stored in a centralized **ClickHouse Cloud** cluster. ClickHouse provides columnar storage optimized for analytical queries across billions of rows.

The cluster contains five databases:

| Database | Contents |
|----------|----------|
| `execution` | Raw execution layer data: blocks, transactions, logs, traces, contracts |
| `consensus` | Raw consensus layer data: validators, attestations, proposals, slots, epochs |
| `crawlers_data` | External data imported via click-runner (Ember, ProbeLab, Dune) |
| `nebula` | P2P network crawl data: peer sessions, discovery results, agent strings |
| `dbt` | Transformed and modeled data produced by dbt-cerebro |

### 3. Data Analysis & Modeling Layer

The modeling layer transforms raw data into analytics-ready datasets using dbt (data build tool).

| Repository | Description |
|-----------|-------------|
| **dbt-cerebro** | The core dbt project containing approximately 400 models organized into 8 modules: `execution`, `consensus`, `p2p`, `bridges`, `ESG`, `probelab`, `crawlers_data`, and `contracts`. Models follow a staging/intermediate/marts pattern and produce the API-facing views. |
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
| cryo-indexer | Rust / Docker | Execution layer data indexing via Cryo |
| beacon-indexer | Go | Consensus layer data indexing from Beacon API |
| era-parser | Rust | Historical era file parsing for CL backfill |
| click-runner | Python / SQL | External data ingestion (Ember, ProbeLab, Dune) |
| nebula | Go | P2P DHT network crawler |
| ip-crawler | Go | IP geolocation enrichment for peer data |
| dbt-cerebro | SQL / dbt | ~400 analytics models across 8 modules |
| dbt-schema-gen | Python | LLM-powered dbt schema generation |
| cryo-base | Docker | Base image for Cryo deployments |
| cerebro-api | Python / FastAPI | REST API with auto-generated endpoints |
| cerebro-mcp | Python / TypeScript | AI assistant tools (MCP server) |
| metrics-dashboard | TypeScript / React | Interactive analytics dashboards |

## Next Steps

- [Architecture](architecture.md) -- Detailed technical architecture with diagrams
- [Quick Start](quickstart.md) -- Make your first API call
- [API Reference](../api/index.md) -- Full REST API documentation
