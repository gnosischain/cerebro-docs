---
title: Gnosis Analytics Documentation
description: Comprehensive blockchain analytics platform for Gnosis Chain
---

# Gnosis Analytics Documentation

Gnosis Analytics is a comprehensive blockchain analytics platform for Gnosis Chain providing real-time and historical data through REST APIs, AI-powered tools, and interactive dashboards. The platform ingests data from execution and consensus layer nodes, P2P network crawlers, and external sources, transforming it through a robust dbt modeling pipeline and serving it via multiple interfaces.

## Data Flow

The platform is organized into four layers that form a complete data pipeline from raw blockchain data to consumer-ready APIs and dashboards.

<div class="home-data-flow" markdown>

<p class="home-data-flow-title">Gnosis Analytics Data Flow</p>

<div class="home-data-flow-diagram home-data-flow-diagram--light" markdown>

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'fontSize': '18px', 'fontFamily': 'Inter, Segoe UI, sans-serif', 'lineColor': '#334155', 'textColor': '#0F172A' }, 'flowchart': { 'nodeSpacing': 40, 'rankSpacing': 70, 'padding': 26, 'subGraphTitleMargin': { 'top': 14, 'bottom': 14 } }}}%%
flowchart TD
    subgraph L1["  DATA ACQUISITION  "]
        direction LR
        EL([Gnosis Chain EL]):::source --> CRYO[cryo-indexer]:::tool
        CL([Gnosis Chain CL]):::source --> BI[beacon-indexer]:::tool
        CL --> ERA[era-parser]:::tool
        EXT([External Data]):::source --> IPC[ip-crawler]:::tool
        EXT --> CR[click-runner]:::tool
        P2P([P2P Network]):::source --> NEB[nebula]:::tool
    end

    subgraph L2["  DATA STORAGE  "]
        CH[(ClickHouse Cloud)]:::storage
    end

    subgraph L3["  DATA MODELING  "]
        DBT[dbt-cerebro]:::modeling
    end

    subgraph L4["  DATA SERVING  "]
        direction LR
        API["cerebro-api"]:::serving ~~~ MCP["cerebro-mcp"]:::serving ~~~ DASH["metrics-dashboard"]:::serving
    end

    CRYO --> CH
    BI --> CH
    ERA --> CH
    IPC --> CH
    CR --> CH
    NEB --> CH
    CH ~~~ DBT
    CH <--> DBT
    CH --> API
    CH --> MCP
    CH --> DASH

    classDef source fill:#FFFFFF,stroke:#1D4ED8,stroke-width:2px,color:#0F172A,font-weight:700,font-size:16px
    classDef tool fill:#E2E8F0,stroke:#1D4ED8,stroke-width:2px,color:#0F172A,font-weight:700,font-size:16px
    classDef storage fill:#FEE2E2,stroke:#B91C1C,stroke-width:2px,color:#0F172A,font-weight:700,font-size:16px
    classDef modeling fill:#FEF3C7,stroke:#B45309,stroke-width:2px,color:#0F172A,font-weight:700,font-size:16px
    classDef serving fill:#DCFCE7,stroke:#15803D,stroke-width:2px,color:#0F172A,font-weight:700,font-size:16px

    style L1 fill:#EFF6FF,stroke:#1D4ED8,stroke-width:2px,color:#0F172A,font-weight:800,font-size:18px
    style L2 fill:#FEF2F2,stroke:#DC2626,stroke-width:2px,color:#0F172A,font-weight:800,font-size:18px
    style L3 fill:#FFFBEB,stroke:#D97706,stroke-width:2px,color:#0F172A,font-weight:800,font-size:18px
    style L4 fill:#F0FDF4,stroke:#16A34A,stroke-width:2px,color:#0F172A,font-weight:800,font-size:18px
```

</div>

<div class="home-data-flow-diagram home-data-flow-diagram--dark" markdown>

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'fontSize': '18px', 'fontFamily': 'Inter, Segoe UI, sans-serif', 'lineColor': '#CBD5E1', 'textColor': '#E2E8F0' }, 'flowchart': { 'nodeSpacing': 40, 'rankSpacing': 70, 'padding': 26, 'subGraphTitleMargin': { 'top': 14, 'bottom': 14 } }}}%%
flowchart TD
    subgraph D1["  DATA ACQUISITION  "]
        direction LR
        ELD([Gnosis Chain EL]):::source --> CRYOD[cryo-indexer]:::tool
        CLD([Gnosis Chain CL]):::source --> BID[beacon-indexer]:::tool
        CLD --> ERAD[era-parser]:::tool
        EXTD([External Data]):::source --> IPCD[ip-crawler]:::tool
        EXTD --> CRD[click-runner]:::tool
        P2PD([P2P Network]):::source --> NEBD[nebula]:::tool
    end

    subgraph D2["  DATA STORAGE  "]
        CHD[(ClickHouse Cloud)]:::storage
    end

    subgraph D3["  DATA MODELING  "]
        DBTD[dbt-cerebro]:::modeling
    end

    subgraph D4["  DATA SERVING  "]
        direction LR
        APID["cerebro-api"]:::serving ~~~ MCPD["cerebro-mcp"]:::serving ~~~ DASHD["metrics-dashboard"]:::serving
    end

    CRYOD --> CHD
    BID --> CHD
    ERAD --> CHD
    IPCD --> CHD
    CRD --> CHD
    NEBD --> CHD
    CHD ~~~ DBTD
    CHD <--> DBTD
    CHD --> APID
    CHD --> MCPD
    CHD --> DASHD

    classDef source fill:#1E293B,stroke:#60A5FA,stroke-width:2px,color:#E2E8F0,font-weight:700,font-size:16px
    classDef tool fill:#2A3A53,stroke:#60A5FA,stroke-width:2px,color:#E2E8F0,font-weight:700,font-size:16px
    classDef storage fill:#4A1F22,stroke:#F87171,stroke-width:2px,color:#FECACA,font-weight:700,font-size:16px
    classDef modeling fill:#4A3814,stroke:#FBBF24,stroke-width:2px,color:#FDE68A,font-weight:700,font-size:16px
    classDef serving fill:#1B3F30,stroke:#4ADE80,stroke-width:2px,color:#BBF7D0,font-weight:700,font-size:16px

    style D1 fill:#132A47,stroke:#60A5FA,stroke-width:2px,color:#DBEAFE,font-weight:800,font-size:18px
    style D2 fill:#3A1B1F,stroke:#F87171,stroke-width:2px,color:#FECACA,font-weight:800,font-size:18px
    style D3 fill:#3F2F13,stroke:#FBBF24,stroke-width:2px,color:#FDE68A,font-weight:800,font-size:18px
    style D4 fill:#163427,stroke:#4ADE80,stroke-width:2px,color:#BBF7D0,font-weight:800,font-size:18px
```

</div>

</div>

## Quick Links

<div class="grid cards" markdown>

-   **API Reference**

    ---

    REST API documentation including authentication, endpoints, filtering, and error handling.

    [:octicons-arrow-right-24: API Reference](api/index.md)

-   **Data Pipeline**

    ---

    Architecture overview, data acquisition, storage, and transformation layers.

    [:octicons-arrow-right-24: Data Pipeline](data-pipeline/index.md)

-   **Model Catalog**

    ---

    Browse the ~400 dbt models across 8 modules powering the analytics platform.

    [:octicons-arrow-right-24: Model Catalog](models/index.md)

-   **Developer Guide**

    ---

    Get started quickly with the API, understand the platform, and integrate with your applications.

    [:octicons-arrow-right-24: Developer Guide](developer/index.md)

</div>

## Getting Started

New to Gnosis Analytics? Start here:

- [Quick Start](getting-started/quickstart.md) -- Make your first API call in under a minute
- [Platform Overview](getting-started/platform-overview.md) -- Understand the 13-repo ecosystem
- [Architecture](getting-started/architecture.md) -- Deep dive into the 4-layer architecture
