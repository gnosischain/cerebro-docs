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

Two crawlers run: the consensus-layer (discv5) crawler writes the `nebula` database and the execution-layer (discv4) crawler writes `nebula_discv4`. Together they write ~3.3 TB/month and feed 16 dbt p2p models. The primary tables in each are:

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

## Operating and recovering

### How it runs

Two Deployments, one per network — discv5 → `nebula`, discv4 → `nebula_discv4` — `Recreate`, one crawler each. The repository is a three-file build wrapper around upstream `dennis-tra/nebula`, pinned to a commit; all Gnosis configuration lives in the deployment stack, not in the repo.

These are the only pods in the estate on **public nodes** with an ephemeral IP — deliberate, because the traffic is almost entirely peer-to-peer and needs no inbound. They do **not** egress via the shared NAT address.

### Health — a data query, nothing else

**There are zero alert rules for either crawler.** Nothing will tell you they stopped.

```sql
SELECT max(visit_started_at) FROM nebula.visits;
SELECT max(visit_started_at) FROM nebula_discv4.visits;
```

!!! warning "Restart counts in the thousands are by design"
    A liveness probe fails past a maximum uptime, deliberately restarting the crawler. It is also the only thing that catches a *hung* crawl, which otherwise looks `Running` and keeps serving metrics. So a high restart count is not an incident, and a *low* one after a long uptime might be.

### Restart

Each crawl is an independent sweep with nothing to resume, so restarting is always safe. Killing mid-crawl loses that sweep's remaining peers and nothing else. There is no gap-repair procedure: a missed sweep is simply a missed sample.

Schema is owned entirely by upstream. The consensus crawler has `APPLY_MIGRATIONS=false` and the execution one does not — which of the two owns schema changes is unresolved; do not "normalise" it without deciding.

### Then dbt

The p2p models read `nebula.visits` incrementally; a plain scoped `dbt run` after the crawler is back is enough. See [dbt reprocess](../../operations/runbooks/dbt-reprocess.md) for the general rules.

!!! info "Internal runbook"
    [runbooks/27-nebula-and-ip-crawler.md](https://github.com/gnosisdevops/infrastructure-gnosis-analytics/blob/main/runbooks/27-nebula-and-ip-crawler.md) — private repository; carries the cluster-specific commands for this page.

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
