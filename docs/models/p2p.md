# P2P Network Module

The P2P Network module contains approximately **27 models** that analyze the peer-to-peer network infrastructure of Gnosis Chain. It covers node discovery protocols (discv4 and discv5), network topology, geographic distribution of nodes, client version tracking, ISP diversity, and connectivity metrics.

## Data Sources

P2P data is sourced from two ClickHouse databases:

- **nebula** -- P2P network crawl results and visit records from the Nebula crawler (discv5)
- **nebula_discv4** -- Discovery v4 protocol-specific data (variant schema)

The Nebula crawler periodically discovers and visits nodes on the Gnosis Chain network, recording their capabilities, geographic location (via IP geolocation), client identifiers, ISP information, and protocol support.

## Key Concepts

**Nebula Crawler**

: An open-source network measurement tool that systematically discovers and visits P2P nodes. Each crawl session attempts to connect to all known nodes and records reachability, latency, client agent string, and supported protocols. Crawl frequency is approximately every 30 minutes.

**discv4 vs discv5**

: Two generations of the Ethereum node discovery protocol.

    - **discv4** uses a Kademlia-based DHT for peer discovery. It is the legacy protocol still used by older clients and is simpler but less feature-rich.
    - **discv5** is the newer protocol supporting topic advertisement, improved NAT traversal, and better ENR (Ethereum Node Record) handling. Most modern clients support both protocols.

**Agent String**

: The self-reported client identifier sent during the P2P handshake (e.g., `Nethermind/v1.25.0/linux-x64`). Agent strings are parsed to extract structured fields: client name, version, platform, and runtime. This enables tracking client diversity and upgrade adoption rates.

**Reachable vs. Total Nodes**

: Total nodes include all peers discovered in the DHT. Reachable nodes are those that responded to a connection attempt during the crawl. The ratio of reachable to total nodes is a health indicator for the network.

## Model Categories

<!-- BEGIN AUTO-GENERATED: models-p2p -->
**Clients**

| Model | Layer | Description |
|-------|-------|-------------|
| `api_p2p_clients_latest` | API | This view provides the latest counts and percentage changes of P2P clients for discv4 and discv5 protocols, enabling ... |

**Discovery**

| Model | Layer | Description |
|-------|-------|-------------|
| `stg_nebula_discv4__discovery_id_prefixes_x_peer_ids` | Staging | This view maps discovery ID prefixes to their associated peer IDs within the Nebula DiscV4 dataset, facilitating anal... |
| `stg_nebula_discv5__discovery_id_prefixes_x_peer_ids` | Staging | This view maps discovery ID prefixes to their associated peer IDs within the Nebula DiscV5 dataset, facilitating anal... |

**Discv4**

| Model | Layer | Description |
|-------|-------|-------------|
| `int_p2p_discv4_clients_daily` | Intermediate | The `int_p2p_discv4_clients_daily` model aggregates peer discovery data for the discv4 protocol, providing daily metr... |
| `int_p2p_discv4_peers` | Intermediate | The int_p2p_discv4_peers model aggregates and processes peer visit data from the Discv4 network, enabling analysis of... |
| `int_p2p_discv4_topology_latest` | Intermediate | The model captures the latest peer-to-peer discovery topology by aggregating neighbor relationships and associated me... |
| `int_p2p_discv4_visits_daily` | Intermediate | The `int_p2p_discv4_visits_daily` model aggregates daily peer-to-peer DISCv4 visit data, providing insights into visi... |
| `api_p2p_discv4_clients_daily` | API | The api_p2p_discv4_clients_daily view tracks daily metrics related to the number of Discv4 clients in the P2P network... |
| `api_p2p_discv4_clients_latest` | API | The api_p2p_discv4_clients_latest view provides the most recent aggregated counts of Discv4 P2P clients, facilitating... |

**Discv5**

| Model | Layer | Description |
|-------|-------|-------------|
| `int_p2p_discv5_clients_daily` | Intermediate | The int_p2p_discv5_clients_daily model aggregates daily peer discovery data for P2P clients using the DiscV5 protocol... |
| `int_p2p_discv5_forks_daily` | Intermediate | The `int_p2p_discv5_forks_daily` model tracks daily counts of peers associated with specific current and next forks i... |
| `int_p2p_discv5_peers` | Intermediate | The `int_p2p_discv5_peers` model consolidates peer visit data to analyze peer properties, fork versions, and network ... |
| `int_p2p_discv5_topology_latest` | Intermediate | This model captures the latest peer-to-peer discovery topology, including peer and neighbor information along with as... |
| `int_p2p_discv5_visits_daily` | Intermediate | The `int_p2p_discv5_visits_daily` model aggregates daily peer-to-peer network visit data, focusing on successful and ... |
| `api_p2p_discv5_clients_daily` | API | The api_p2p_discv5_clients_daily model tracks daily metrics related to Discv5 clients in the P2P network, providing i... |
| `api_p2p_discv5_clients_latest` | API | The api_p2p_discv5_clients_latest model provides a snapshot of the latest Discv5 peer-to-peer client metrics, enablin... |
| `api_p2p_discv5_current_fork_daily` | API | The `api_p2p_discv5_current_fork_daily` view tracks the daily count of current Discv5 network forks, providing insigh... |
| `api_p2p_discv5_next_fork_daily` | API | The api_p2p_discv5_next_fork_daily model provides daily counts of upcoming Discv5 network forks, enabling monitoring ... |

**Neighbors**

| Model | Layer | Description |
|-------|-------|-------------|
| `stg_nebula_discv4__neighbors` | Staging | The stg_nebula_discv4__neighbors view captures neighbor discovery data from the Nebula v4 network, facilitating analy... |
| `stg_nebula_discv5__neighbors` | Staging | This model captures neighbor discovery data from the Nebula DISCv5 protocol, facilitating analysis of peer relationsh... |

**Topology**

| Model | Layer | Description |
|-------|-------|-------------|
| `fct_p2p_topology_latest` | Fact | This view consolidates the latest peer-to-peer topology data from DiscV4 and DiscV5 protocols, enabling analysis of n... |
| `api_p2p_topology_latest` | API | The api_p2p_topology_latest model provides a real-time view of peer-to-peer network topology, capturing the latest co... |

**Visits**

| Model | Layer | Description |
|-------|-------|-------------|
| `stg_nebula_discv4__visits` | Staging | The stg_nebula_discv4__visits model captures detailed information about network discovery visits, including connectio... |
| `stg_nebula_discv5__visits` | Staging | The stg_nebula_discv5__visits model captures detailed information about network discovery visits, including connectio... |
| `api_p2p_visits_latest` | API | This view provides the latest daily visit metrics for P2P protocols (discv4 and discv5), including total visits, succ... |

<!-- END AUTO-GENERATED: models-p2p -->

## Network Health Metrics

The P2P module provides several network health indicators:

| Metric | Healthy Range | Description |
|--------|---------------|-------------|
| Reachable ratio | > 70% | Percentage of discovered nodes that are reachable |
| Dial success rate | > 60% | Percentage of connection attempts that succeed |
| Client diversity (top client) | < 33% | No single client should dominate the network |
| Geographic spread | 20+ countries | Nodes should be distributed across multiple jurisdictions |
| ISP concentration (top ISP) | < 25% | No single ISP should host a quarter of the network |

## Key Models Reference

| Model | Description | Key Columns |
|-------|-------------|-------------|
| `api_p2p_network_size_daily` | Network size over time | `dt`, `total_nodes`, `reachable_nodes` |
| `api_p2p_nodes_by_client_daily` | Client distribution | `dt`, `client_name`, `node_count` |
| `api_p2p_nodes_by_country_daily` | Geographic distribution | `dt`, `country`, `country_code`, `node_count` |
| `api_p2p_discovered_nodes_daily` | Discovery metrics | `dt`, `discovered_nodes`, `new_nodes` |

## Query Examples

Retrieve daily network size for the past 30 days:

```sql
SELECT dt, total_nodes, reachable_nodes
FROM dbt.api_p2p_network_size_daily
WHERE dt >= today() - 30
ORDER BY dt
```

Check client distribution:

```sql
SELECT dt, client_name, node_count
FROM dbt.api_p2p_nodes_by_client_daily
WHERE dt = today() - 1
ORDER BY node_count DESC
```

Analyze geographic spread:

```sql
SELECT country, node_count,
       round(node_count / sum(node_count) OVER () * 100, 2) AS pct_of_total
FROM dbt.api_p2p_nodes_by_country_daily
WHERE dt = today() - 1
ORDER BY node_count DESC
LIMIT 20
```

Track version adoption after a client release:

```sql
SELECT dt, client_version, node_count
FROM dbt.int_p2p_nodes_by_client_version_daily
WHERE client_name = 'Nethermind'
  AND dt >= today() - 14
ORDER BY dt, node_count DESC
```

## Related Modules

- [Consensus](consensus.md) -- Validator data correlates with consensus client distribution
- [ESG](esg.md) -- Geographic node distribution feeds energy consumption estimates
- [ProbeLab](probelab.md) -- Additional network monitoring with cloud provider classification
