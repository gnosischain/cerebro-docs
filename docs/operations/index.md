---
title: Operations
description: Infrastructure, deployment, monitoring, and troubleshooting for the Gnosis Analytics platform
---

# Operations

This section covers the operational aspects of the Gnosis Analytics platform: infrastructure architecture, deployment procedures, monitoring and observability, and troubleshooting guides.

## Overview

The platform runs on **AWS EKS** (Elastic Kubernetes Service) with all workloads containerized and deployed via Kubernetes. Data is stored in **ClickHouse Cloud**, and the CI/CD pipeline uses **GitHub Actions** with images published to **GitHub Container Registry (GHCR)**.

```mermaid
flowchart TD
    subgraph GitHub["GitHub"]
        REPO[Source Repositories] --> GHA[GitHub Actions]
        GHA --> GHCR[Container Registry]
    end
    subgraph AWS["AWS"]
        subgraph EKS["EKS Cluster (ARM64)"]
            API[cerebro-api]
            IDX[Indexers]
            CRW[Crawlers]
        end
        ALB[Application Load Balancer] --> API
        SSM[SSM Parameter Store] --> ESO[External Secrets Operator]
        ESO --> EKS
    end
    subgraph External["External"]
        CH[(ClickHouse Cloud)]
    end
    GHCR --> EKS
    EKS --> CH
```

## Sections

| Section | Description |
|---------|-------------|
| [Infrastructure](infrastructure.md) | AWS EKS cluster architecture, node groups, networking, and storage |
| [Deployment](deployment.md) | Docker builds, CI/CD pipeline, Kubernetes deployment, and secrets management |
| [Monitoring](monitoring.md) | Metrics, logging, alerting, and health checks |
| [Troubleshooting](troubleshooting.md) | Common issues and their resolution steps |

## Key Contacts

| Area | Team |
|------|------|
| API and dbt models | Gnosis Analytics engineering |
| Infrastructure and Kubernetes | Gnosis DevOps |
| ClickHouse Cloud | Managed by ClickHouse (external) |
