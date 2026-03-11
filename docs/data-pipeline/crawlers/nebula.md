# nebula

nebula is a network-agnostic DHT (Distributed Hash Table) crawler that discovers and monitors peers on the Gnosis Chain peer-to-peer network. It is a Go application forked from [dennis-tra/nebula](https://github.com/dennis-tra/nebula) and customized for Gnosis Chain deployment.

## Purpose

nebula connects to DHT bootstrap nodes and recursively traverses their k-buckets to discover all reachable peers in the network. For each peer discovered, it records:

- Peer ID and IP address
- Agent version string (identifying the client software and version)
- Supported protocols
- Fork digest (identifying which chain fork the peer follows)
- Visit timestamps and reachability status

This data provides visibility into the health, diversity, and topology of the Gnosis Chain P2P network.

## How It Works

1. **Bootstrap** -- nebula connects to known DHT bootstrap nodes for the target network
2. **Crawl** -- Starting from bootstrap peers, it queries each peer's routing table (k-buckets) to discover additional peers
3. **Recursive discovery** -- Newly discovered peers are themselves queried, continuing until all reachable peers have been visited
4. **Record** -- For each peer, metadata (agent version, protocols, IP, fork digest) is recorded in ClickHouse
5. **Repeat** -- The crawl cycle repeats on a configurable schedule to track network changes over time

## Data Output

nebula writes to the `nebula` database in ClickHouse. The primary tables are:

### `nebula.visits`

Records each peer visit with metadata:

| Field | Description |
|-------|-------------|
| `peer_id` | Unique peer identifier |
| `peer_properties` | JSON object containing IP address, agent version, fork digest, protocols |
| `visit_started_at` | Timestamp when the visit began |
| `visit_ended_at` | Timestamp when the visit completed |
| `connect_error` | Error details if the connection failed |
| `crawl_id` | Identifier linking this visit to a specific crawl session |

### `nebula.peers`

Aggregated peer records with the latest known state.

## Deployment

nebula is deployed as a Docker container built from a pinned commit of the upstream repository:

```dockerfile
FROM golang:1.23-alpine AS builder
# Builds from dennis-tra/nebula at a specific commit
# Produces the nebula binary at /usr/local/bin/nebula
```

### Docker Compose

```bash
# Start the crawler
docker-compose up -d nebula

# Check health
docker-compose exec nebula nebula health

# View logs
docker-compose logs -f nebula
```

### Health Checks

The container includes a built-in health check that runs `nebula health` every 15 seconds.

## Crawl Scheduling

nebula runs as a continuous service. Crawl frequency depends on the network size and configuration. Each crawl cycle:

1. Starts from the bootstrap node list
2. Discovers and visits all reachable peers
3. Records results in ClickHouse
4. Waits for the configured interval before the next cycle

For the Gnosis Chain network, a full crawl typically takes a few minutes depending on network size.

## Relationship to ip-crawler

nebula discovers peer IP addresses and stores them in the `nebula.visits` table. The [ip-crawler](ip-crawler.md) reads these IPs and enriches them with geolocation data from ipinfo.io. Together they provide a complete picture of the network's geographic and organizational distribution.

## Fork Digest Filtering

The `peer_properties` JSON in `nebula.visits` includes a `fork_digest` field that identifies which chain fork a peer is following. Downstream tools (including ip-crawler) use this field to filter for Gnosis Chain peers specifically, excluding peers on other networks that may share the same DHT.

Common Gnosis Chain fork digests are configured as environment variables and updated when the network undergoes protocol upgrades.

## ClickHouse Table Schemas

All tables are stored in the `nebula` database.

??? note "Table: `nebula.visits`"
    **Engine:** MergeTree
    **ORDER BY:** (visited_at, peer_id)

    | Column | Type | Notes |
    |--------|------|-------|
    | `id` | String | Unique visit identifier |
    | `peer_id` | String | Discovered peer identifier |
    | `crawl_id` | String | Parent crawl session identifier |
    | `session_id` | String | Connection session identifier |
    | `agent_version` | String | Peer's client software and version |
    | `protocols` | Array(String) | Supported protocol list |
    | `listen_addrs` | Array(String) | Peer's advertised listen addresses |
    | `connect_error` | String | Error if connection failed |
    | `crawl_error` | String | Error if crawl query failed |
    | `visited_at` | DateTime | Timestamp of the visit |
    | `created_at` | DateTime | Row creation timestamp |

??? note "Table: `nebula.peers`"
    **Engine:** ReplacingMergeTree(updated_at)
    **ORDER BY:** (multi_hash)

    | Column | Type | Notes |
    |--------|------|-------|
    | `id` | String | Internal peer identifier |
    | `multi_hash` | String | Peer multihash (primary key) |
    | `agent_version` | String | Latest known agent version |
    | `protocols` | Array(String) | Latest known protocol list |
    | `created_at` | DateTime | First seen timestamp |
    | `updated_at` | DateTime | Last seen timestamp; deduplication version |
