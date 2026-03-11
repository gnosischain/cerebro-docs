# Data Pipeline

The Gnosis Analytics data pipeline is a modular system that continuously ingests, enriches, and transforms blockchain data from Gnosis Chain into analytics-ready datasets. It spans the full lifecycle from raw on-chain events to queryable API endpoints.

## Pipeline Architecture

```mermaid
graph LR
    subgraph Sources
        EL[Execution Layer<br/>RPC Node]
        CL[Consensus Layer<br/>Beacon Node]
        P2P[P2P Network<br/>DHT Peers]
        EXT[External<br/>Ember, ProbeLab]
    end

    subgraph Indexers
        CRYO[cryo-indexer]
        BEACON[beacon-indexer]
        ERA[era-parser]
        CR[click-runner]
        NEB[nebula]
        IPC[ip-crawler]
    end

    subgraph Storage
        CH[(ClickHouse Cloud)]
    end

    subgraph Transformation
        DBT[dbt-cerebro<br/>~400 models]
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
    P2P --> NEB
    NEB --> IPC

    CRYO --> CH
    BEACON --> CH
    ERA --> CH
    CR --> CH
    NEB --> CH
    IPC --> CH

    CH --> DBT
    DBT --> CH

    CH --> API
    API --> MCP
    API --> DASH
```

## Sections

| Section | Description |
|---------|-------------|
| [Pipeline Overview](overview.md) | End-to-end explanation of data flow, storage layout, and transformation strategy |
| [Data Ingestion](ingestion/index.md) | Indexers that extract data from blockchain nodes and external sources |
| [Network Crawlers](crawlers/index.md) | P2P network topology crawling and IP geolocation enrichment |
| [Data Transformation](transformation/index.md) | dbt models that transform raw data into analytics-ready datasets |
