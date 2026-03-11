---
title: Glossary
description: Definitions of blockchain, infrastructure, and platform terms used in the Gnosis Analytics documentation
---

# Glossary

Definitions of terms used throughout the Gnosis Analytics documentation, organized by domain.

## Gnosis Chain

Attestation
:   A vote by a validator confirming the validity of a beacon block and checkpoint. Validators are expected to attest once per epoch. Attestation participation rate is a key network health metric.

Beacon Chain
:   The consensus layer of Gnosis Chain (and Ethereum). Manages the validator registry, processes attestations, handles block proposals, and coordinates the proof-of-stake consensus mechanism.

Blob
:   A large binary data object attached to a beacon block, introduced by EIP-4844 (Proto-Danksharding). Blobs are used for rollup data availability and are stored temporarily (pruned after approximately 18 days).

Consensus Layer (CL)
:   The part of the blockchain responsible for proof-of-stake consensus. Manages validators, block proposals, attestations, and finality. Operates on the beacon chain with slots and epochs.

Epoch
:   A period of 16 slots on Gnosis Chain (32 slots on Ethereum). At the end of each epoch, the beacon chain finalizes checkpoints and processes validator rewards and penalties. One epoch is approximately 80 seconds on Gnosis Chain.

Era File
:   An archive file format (`.era`) containing historical beacon chain state snapshots. Used for efficient backfilling of consensus layer data without replaying the entire chain.

Execution Layer (EL)
:   The part of the blockchain that processes transactions, executes smart contracts, and maintains account state. Formerly the entire blockchain before the merge to proof-of-stake.

Fork Digest
:   A 4-byte identifier derived from the genesis validators root and the current fork version. Used to distinguish peers on different networks or chain forks in the P2P layer.

GNO
:   The native governance and staking token of Gnosis Chain. Validators stake GNO to participate in consensus. Also used for governance voting.

Gnosis Chain
:   An Ethereum-compatible Layer 1 blockchain using proof-of-stake consensus with a focus on decentralization and community governance. Formerly known as xDai Chain.

OmniBridge
:   A cross-chain bridge connecting Gnosis Chain to Ethereum and other networks. Enables transfer of ERC-20 tokens between chains.

Sidecar
:   In the context of blobs, a blob sidecar is the metadata accompanying a blob including the KZG commitment, KZG proof, and the blob data itself. Sidecars are propagated separately from beacon blocks.

Slot
:   The smallest time unit in the consensus layer. On Gnosis Chain, each slot is 5 seconds. One validator is assigned to propose a block per slot, and committees of validators attest to each slot.

STAKE
:   A legacy token from the xDai Chain era, previously used for staking. Replaced by GNO when xDai Chain merged with the Gnosis beacon chain.

Validator
:   A participant in the proof-of-stake consensus mechanism. Validators stake 1 GNO on Gnosis Chain, propose blocks when selected, and attest to blocks in their assigned committees.

xDai
:   The original stablecoin and gas token of the xDai Chain (now Gnosis Chain). xDai is pegged to the US Dollar and is used to pay transaction fees on Gnosis Chain.

xDai Bridge
:   A bridge specifically for converting DAI on Ethereum to xDai on Gnosis Chain and vice versa. One of the oldest production cross-chain bridges.

## Data Infrastructure

ClickHouse
:   A column-oriented database management system designed for online analytical processing (OLAP). Used as the primary data warehouse for all Gnosis Analytics data. Excels at scanning billions of rows per second for aggregation queries.

dbt (data build tool)
:   An open-source transformation framework that enables data analysts and engineers to transform data using SQL. dbt-cerebro is the platform's dbt project containing approximately 400 models.

Incremental Model
:   A dbt materialization strategy where only new or changed data is processed on each run, rather than rebuilding the entire table. The platform uses `delete+insert` incremental strategy with monthly partitioning.

Manifest
:   The `manifest.json` file produced by dbt that contains metadata about all models, sources, tests, and their configurations. The cerebro-api reads this file to auto-generate API endpoints.

Materialization
:   How a dbt model is persisted in the database. Common materializations: `view` (SQL view, no storage), `table` (full table rebuild), `incremental` (append or update changed rows).

MergeTree
:   The primary table engine family in ClickHouse. `MergeTree` stores data sorted by a primary key and supports efficient range queries. `ReplacingMergeTree` adds deduplication during background merge operations.

Partition
:   A physical division of a ClickHouse table. The platform partitions most tables by month (`toStartOfMonth(date)`) to enable efficient partition-level deletes and queries.

Source
:   In dbt, a source is a declaration of a raw table in the database that dbt models can reference using the `{{ source() }}` function. Sources are defined in `sources.yml` files.

View
:   A stored SQL query that does not physically store data. When queried, the view's SQL is executed against the underlying tables. Used for staging, fact, and API layer models.

## API and Access

API Key
:   A secret string (format: `sk_live_<identifier>`) used to authenticate requests to non-public API endpoints. Each key is associated with a user, organization, and access tier.

Pagination
:   A mechanism for retrieving large result sets in smaller chunks using `limit` (maximum rows per response) and `offset` (number of rows to skip). Configured per endpoint via `meta.api.pagination`.

Rate Limit
:   The maximum number of API requests allowed per time window. Limits are applied per API key (or per IP for unauthenticated requests) using a fixed 60-second window.

Tier
:   An access level in the API's hierarchical permission system. Four tiers exist: tier0 (public, no key), tier1 (partner), tier2 (premium), tier3 (internal). Higher tiers inherit access to lower-tier endpoints.

## MCP (Model Context Protocol)

MCP (Model Context Protocol)
:   An open standard protocol that allows AI applications (hosts) to connect to external data sources and tools (servers) through a unified interface. The cerebro-mcp server implements MCP to provide AI-powered analytics.

stdio Transport
:   The default MCP transport mechanism where the host spawns the server as a subprocess and communicates via standard input/output streams. Used with Claude Desktop and Claude Code.

SSE Transport (Server-Sent Events)
:   An HTTP-based MCP transport mechanism for remote deployments. The server runs as an HTTP service that clients connect to over the network. Used for hosted team instances.

Tool
:   In MCP, a tool is a function that the AI assistant can call to perform actions: query databases, inspect schemas, generate charts, or build reports. cerebro-mcp provides over 30 tools.

## Platform Components

beacon-indexer
:   A Go application that indexes consensus layer data from Gnosis Chain beacon nodes via the standard Beacon API. Captures validator activity, attestations, proposals, and blob sidecars.

cerebro-api
:   The Python FastAPI REST API server that auto-generates endpoints from the dbt manifest. Provides tiered authentication, rate limiting, and both GET and POST query interfaces.

cerebro-mcp
:   The MCP server that provides AI assistant capabilities for Gnosis Chain analytics. Enables natural language queries, chart generation, and interactive report building.

click-runner
:   A Python toolkit for loading external data into ClickHouse. Supports SQL execution, CSV ingestion via URL engine, and Parquet file imports from S3.

cryo-indexer
:   An execution layer data indexer built on the Cryo framework. Extracts blocks, transactions, logs, traces, and state data from Gnosis Chain EL nodes.

dbt-cerebro
:   The core dbt project containing approximately 400 SQL models organized into 8 modules. Transforms raw blockchain data into analytics-ready datasets.

dbt-schema-gen
:   An LLM-powered tool that automatically generates dbt schema YAML files with column descriptions, tests, and documentation from SQL model definitions.

ip-crawler
:   A Python service that enriches peer IP addresses discovered by nebula with geolocation data from the ipinfo.io API. Maps IPs to geographic coordinates, ISPs, and ASNs.

metrics-dashboard
:   A React + ECharts web application providing interactive dashboards and visualizations of Gnosis Chain metrics.

nebula
:   A Go application that crawls the Gnosis Chain P2P DHT network to discover and monitor peer connectivity, client diversity, and network topology.

## Infrastructure

ALB (Application Load Balancer)
:   An AWS load balancer operating at the HTTP/HTTPS layer (Layer 7). Provides TLS termination, path-based routing, and health checking for the cerebro-api and dashboard.

ARM64 / Graviton
:   The CPU architecture used by AWS Graviton processors. The platform runs on ARM64 nodes (M6G instances) for better price-performance than equivalent x86 instances.

CronJob
:   A Kubernetes resource that creates Jobs on a recurring schedule. Used for periodic data ingestion tasks like click-runner imports.

EKS (Elastic Kubernetes Service)
:   AWS managed Kubernetes service used to run the platform's containerized workloads.

ESO (External Secrets Operator)
:   A Kubernetes operator that synchronizes secrets from external secret management systems (like AWS SSM Parameter Store) into Kubernetes Secrets.

GHCR (GitHub Container Registry)
:   GitHub's container image registry where all platform Docker images are stored and pulled from.

SSM Parameter Store
:   AWS Systems Manager Parameter Store, a service for storing configuration data and secrets. All platform credentials are stored here and synced to Kubernetes via ESO.

Terraform
:   An infrastructure-as-code tool used to provision and manage the AWS infrastructure (EKS cluster, networking, IAM, etc.).
