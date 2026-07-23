# Data Ingestion

The data ingestion layer is responsible for extracting raw blockchain data from various sources and loading it into ClickHouse. Each indexer is purpose-built for a specific data source and runs as an independent containerized service.

This section covers all ingestion components: the execution-layer and consensus-layer indexers, the era file parser for historical backfills, the click-runner for external data sources, the CoW Protocol indexer, the RPC state indexer for verified historical contract state, and the network crawlers that capture P2P topology.

## Pipeline Architecture

```mermaid
graph LR
    subgraph Sources
        EL[Execution Layer<br/>RPC Node]
        CL[Consensus Layer<br/>Beacon Node]
        P2P[P2P Network<br/>DHT Peers]
        EXT[External<br/>Ember, ProbeLab, Snapshot]
        COWAPI[CoW Protocol API]
        ARC[Archive RPC Node]
    end

    subgraph Indexers
        CRYO[cryo-indexer]
        BEACON[beacon-indexer]
        ERA[era-parser]
        CR[click-runner]
        COWIDX[cow-indexer]
        RPCSI[rpc-state-indexer]
        NEB[nebula]
        IPC[ip-crawler]
    end

    subgraph Storage
        CH[(ClickHouse Cloud)]
    end

    subgraph Transformation
        DBT[dbt-cerebro<br/>~1,200 models]
    end

    subgraph Serving
        API[REST API]
        MCP[MCP / AI Tools]
        DASH[Dashboards]
    end

    EL --> CRYO
    CL --> BEACON
    CL --> ERA
    EXT --> CR
    EL --> COWIDX
    COWAPI --> COWIDX
    ARC --> RPCSI
    P2P --> NEB
    NEB --> IPC

    CRYO --> CH
    BEACON --> CH
    ERA --> CH
    CR --> CH
    COWIDX --> CH
    RPCSI --> CH
    NEB --> CH
    IPC --> CH

    CH --> DBT
    DBT --> CH

    CH --> API
    API --> MCP
    API --> DASH
```

## Indexer Overview

| Indexer | Source | Target Database | Language | Key Capability |
|---------|--------|----------------|----------|----------------|
| [cryo-indexer](cryo-indexer.md) | Execution layer RPC | `execution` | Python + Cryo (Rust) | Blocks, transactions, logs, traces, state diffs |
| [beacon-indexer](beacon-indexer.md) | Beacon node REST API | `consensus` | Python | Validators, attestations, sync committees |
| [era-parser](era-parser.md) | Era archive files | `consensus` | Python | Historical beacon chain bulk loading |
| [click-runner](click-runner.md) | CSV/Parquet/SQL/APIs | Various | Python | External data ingestion (Ember, ProbeLab, Snapshot, Discourse, Mixpanel, Celo GPay) |
| [cow-indexer](cow-indexer.md) | EVM RPC + CoW API | `cow_db` | Python | Multi-chain CoW Protocol events, settlements, order-book history |
| [rpc-state-indexer](rpc-state-indexer.md) | Archive EVM RPC | `rpc_indexer` | Python | Verified day-end contract state as an independent cross-check |

## Supporting Components

| Component | Purpose |
|-----------|---------|
| [cryo-base](cryo-base.md) | Docker base image with pre-compiled Cryo binary and custom patches |

## Design Principles

All indexers in this layer follow common design principles:

**Atomic processing** -- Data is loaded in complete chunks. A range of blocks is either fully committed or not committed at all. Partial writes are avoided.

**State tracking** -- Each indexer maintains a state table in ClickHouse that records which ranges have been processed, enabling resumability and failure recovery.

**Incremental operation** -- Indexers support both historical backfill (bulk loading of past data) and continuous mode (following the chain tip in real time).

**Containerized deployment** -- Every indexer ships as a Docker image with Docker Compose configurations for straightforward deployment and orchestration.

**Idempotency** -- Reprocessing a range that has already been loaded produces the same result, using `ReplacingMergeTree` engines and deduplication strategies in ClickHouse.
