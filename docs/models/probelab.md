# ProbeLab Module

The ProbeLab module contains approximately **9 models** that analyze network infrastructure data collected by the ProbeLab crawler. This module focuses on cloud provider distribution, QUIC protocol support adoption, and agent version tracking across Gnosis Chain nodes, complementing the P2P module's broader network topology analysis.

## Data Sources

ProbeLab data is stored in the `crawlers_data` ClickHouse database under `probelab_*` tables. The [ProbeLab](https://probelab.io/) project is an independent network measurement initiative that provides detailed infrastructure-level metrics beyond what the Nebula crawler captures.

ProbeLab crawlers perform IP-level analysis to classify nodes by:

- Cloud provider (matching against known IP ranges for major providers)
- Autonomous system number (ASN) and ISP
- Transport protocol support (TCP, QUIC)
- Client agent string (parsed into client name, version, OS, architecture)

## Model Categories

<!-- BEGIN AUTO-GENERATED: models-probelab -->
**Clients**

| Model | Layer | Description |
|-------|-------|-------------|
| `api_probelab_clients_cloud_daily` | API | The `api_probelab_clients_cloud_daily` view aggregates daily counts of crawler instances by client type and cloud pro... |
| `api_probelab_clients_country_daily` | API | The api_probelab_clients_country_daily model aggregates daily crawler data to track client activity across different ... |
| `api_probelab_clients_daily` | API | The api_probelab_clients_daily model aggregates daily maximum crawl creation dates and agent version types for Probel... |
| `api_probelab_clients_quic_daily` | API | This view aggregates daily counts of Probelab clients' support for the QUIC protocol, aiding in monitoring client ado... |
| `api_probelab_clients_version_daily` | API | The api_probelab_clients_version_daily model aggregates daily counts of unique client agent versions to monitor versi... |

<!-- END AUTO-GENERATED: models-probelab -->

## Infrastructure Decentralization

The ProbeLab module provides key metrics for assessing Gnosis Chain's infrastructure decentralization:

| Metric | Healthy Threshold | Risk |
|--------|-------------------|------|
| Top cloud provider share | < 33% | Single-provider outage could disrupt consensus |
| Residential node share | > 10% | Low residential share indicates cloud dependency |
| Top 3 providers combined | < 66% | Oligopoly risk in hosting infrastructure |
| QUIC adoption | > 30% | Low adoption limits transport layer improvements |

These metrics are displayed in the dashboard's ESG sector and are used by the ESG module for energy attribution (cloud providers have published PUE values that improve power consumption estimates).

## Key Models Reference

| Model | Description | Key Columns |
|-------|-------------|-------------|
| `api_probelab_cloud_providers_daily` | Cloud hosting distribution | `dt`, `cloud_provider`, `node_count`, `pct_of_total` |
| `api_probelab_quic_support_daily` | QUIC transport adoption | `dt`, `quic_nodes`, `tcp_only_nodes`, `quic_pct` |
| `api_probelab_agent_versions_daily` | Client version distribution | `dt`, `agent_name`, `agent_version`, `node_count` |

## Query Examples

Check cloud provider distribution:

```sql
SELECT dt, cloud_provider, node_count, pct_of_total
FROM dbt.api_probelab_cloud_providers_daily
WHERE dt = today() - 1
ORDER BY node_count DESC
```

Track QUIC adoption over time:

```sql
SELECT dt, quic_nodes, tcp_only_nodes, quic_pct
FROM dbt.api_probelab_quic_support_daily
WHERE dt >= today() - 30
ORDER BY dt
```

Monitor client version upgrades:

```sql
SELECT dt, agent_name, agent_version, node_count
FROM dbt.api_probelab_agent_versions_daily
WHERE dt = today() - 1
ORDER BY node_count DESC
LIMIT 20
```

Check cloud concentration trend:

```sql
SELECT
    dt,
    cloud_provider,
    node_count,
    pct_of_total,
    sum(pct_of_total) OVER (PARTITION BY dt ORDER BY node_count DESC) AS cumulative_pct
FROM dbt.api_probelab_cloud_providers_daily
WHERE dt >= today() - 7
ORDER BY dt, node_count DESC
```

## Related Modules

- [P2P](p2p.md) -- Broader network topology and node discovery data
- [ESG](esg.md) -- Cloud provider data supplements energy attribution analysis
- [Consensus](consensus.md) -- Agent versions correlate with consensus client distribution
