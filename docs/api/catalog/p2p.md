# P2P API Endpoints

<!-- BEGIN AUTO-GENERATED: api-catalog-p2p -->
<!-- generated: 2026-07-23 -->
_9 endpoints across 7 resources. Generated from the dbt manifest — edits inside this block will be overwritten. Regenerate with `python scripts/update_docs.py --only api`._

## clients_count

This view provides the latest counts and percentage changes of P2P clients for discv4 and discv5 protocols, enabling monitoring of client growth trends over the most recent week.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/p2p/clients_count/latest` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/p2p/clients_count/latest`"
    This view provides the latest counts and percentage changes of P2P clients for discv4 and discv5 protocols, enabling monitoring of client growth trends over the most recent week.

    Model: `api_p2p_clients_latest` — table `dbt.api_p2p_clients_latest`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The date corresponding to the latest available data for the client counts. |
    | `discv4_count` | `UInt64` | The total number of discv4 clients recorded on the latest date. |
    | `change_discv4_pct` | `Float64` | Percentage change in Discv4 clients compared to 7 days prior. |
    | `discv5_count` | `UInt64` | Number of Discv5 clients for the latest date. |
    | `change_discv5_pct` | `Float64` | Percentage change in Discv5 clients compared to 7 days prior. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/p2p/clients_count/latest"
    ```

## discv4_clients_count

The api_p2p_discv4_clients_latest view provides the most recent aggregated counts of Discv4 P2P clients, facilitating real-time monitoring of client metrics at the latest date.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/p2p/discv4_clients_count/latest` | GET | tier0 | -- | -- | -- |
| `/v1/p2p/discv4_clients_count/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/p2p/discv4_clients_count/latest`"
    The api_p2p_discv4_clients_latest view provides the most recent aggregated counts of Discv4 P2P clients, facilitating real-time monitoring of client metrics at the latest date.

    Model: `api_p2p_discv4_clients_latest` — table `dbt.api_p2p_discv4_clients_latest`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `metric` | `String` | The name of the specific client metric being reported. |
    | `label` | `String` | A categorical identifier or subcategory associated with the metric. |
    | `value` | `UInt64` | The numeric value of the metric, representing client counts or measurements. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/p2p/discv4_clients_count/latest"
    ```

??? info "`GET /v1/p2p/discv4_clients_count/daily`"
    The api_p2p_discv4_clients_daily view tracks daily metrics related to the number of Discv4 clients in the P2P network, supporting operational monitoring and trend analysis.

    Model: `api_p2p_discv4_clients_daily` — table `dbt.api_p2p_discv4_clients_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The specific calendar date for the recorded metrics, formatted as YYYY-MM-DD. |
    | `metric` | `String` | The type of metric being reported, such as client counts or other relevant measurements. |
    | `label` | `String` | A categorical identifier providing additional context or segmentation for the metric, such as client type or network segment. |
    | `value` | `UInt64` | The numeric measurement corresponding to the metric and label, representing counts or other quantitative data. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/p2p/discv4_clients_count/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## discv5_clients_count

The api_p2p_discv5_clients_latest model provides a snapshot of the latest Discv5 peer-to-peer client metrics, enabling real-time monitoring of client counts and statuses.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/p2p/discv5_clients_count/latest` | GET | tier0 | -- | -- | -- |
| `/v1/p2p/discv5_clients_count/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/p2p/discv5_clients_count/latest`"
    The api_p2p_discv5_clients_latest model provides a snapshot of the latest Discv5 peer-to-peer client metrics, enabling real-time monitoring of client counts and statuses.

    Model: `api_p2p_discv5_clients_latest` — table `dbt.api_p2p_discv5_clients_latest`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `metric` | `String` | The name of the specific metric being reported, such as client count or status indicator. |
    | `label` | `String` | A descriptive label categorizing the metric, such as client type or status category. |
    | `value` | `UInt64` | The numerical value associated with the metric and label, representing counts or measurements at the latest date. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/p2p/discv5_clients_count/latest"
    ```

??? info "`GET /v1/p2p/discv5_clients_count/daily`"
    The api_p2p_discv5_clients_daily model tracks daily metrics related to Discv5 clients in the P2P network, providing insights into client activity and distribution over time.

    Model: `api_p2p_discv5_clients_daily` — table `dbt.api_p2p_discv5_clients_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The specific day for which the metrics are recorded, formatted as YYYY-MM-DD. |
    | `metric` | `String` | The type of metric being measured, indicating the aspect of Discv5 clients (e.g., total count, active clients). |
    | `label` | `String` | A categorical identifier that further classifies the metric, such as client version or network segment. |
    | `value` | `UInt64` | The numerical measurement of the metric for the given date and label. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/p2p/discv5_clients_count/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## discv5_current_fork_count

The `api_p2p_discv5_current_fork_daily` view tracks the daily count of current Discv5 network forks, providing insights into network stability and changes over time.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/p2p/discv5_current_fork_count/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/p2p/discv5_current_fork_count/daily`"
    The `api_p2p_discv5_current_fork_daily` view tracks the daily count of current Discv5 network forks, providing insights into network stability and changes over time.

    Model: `api_p2p_discv5_current_fork_daily` — table `dbt.api_p2p_discv5_current_fork_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The specific calendar date for the recorded fork counts, formatted as YYYY-MM-DD. |
    | `fork` | `String` | Identifier or name of the specific network fork being tracked. |
    | `cnt` | `UInt64` | The number of nodes or instances associated with the specified fork on the given date. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/p2p/discv5_current_fork_count/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## discv5_next_fork_count

The api_p2p_discv5_next_fork_daily model provides daily counts of upcoming Discv5 network forks, enabling monitoring of network upgrade activity over time.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/p2p/discv5_next_fork_count/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/p2p/discv5_next_fork_count/daily`"
    The api_p2p_discv5_next_fork_daily model provides daily counts of upcoming Discv5 network forks, enabling monitoring of network upgrade activity over time.

    Model: `api_p2p_discv5_next_fork_daily` — table `dbt.api_p2p_discv5_next_fork_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The specific calendar date for the recorded fork count, formatted as YYYY-MM-DD. |
    | `fork` | `String` | Identifier or version of the upcoming fork being tracked. |
    | `cnt` | `UInt64` | The number of occurrences or instances of the specified fork on the given date. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/p2p/discv5_next_fork_count/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## network_topology

The api_p2p_topology_latest model provides a real-time view of peer-to-peer network topology, capturing the latest connections and their geographic and organizational attributes for analysis and monitoring.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/p2p/network_topology/latest` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/p2p/network_topology/latest`"
    The api_p2p_topology_latest model provides a real-time view of peer-to-peer network topology, capturing the latest connections and their geographic and organizational attributes for analysis and monitoring.

    Model: `api_p2p_topology_latest` — table `dbt.api_p2p_topology_latest`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `protocol` | `String` | The communication protocol used between peers, such as TCP or UDP. |
    | `date` | `Date` | The date when the topology data was recorded, in YYYY-MM-DD format. |
    | `peer_discovery_id_prefix` | `UInt64` | Prefix of the unique identifier for the peer discovered in the network. |
    | `peer_client` | `String` | The client software or implementation used by the peer. |
    | `peer_city` | `String` | City where the peer is located. |
    | `peer_country` | `String` | Country where the peer is located. |
    | `peer_org` | `String` | Organization associated with the peer, if available. |
    | `peer_lat` | `Float64` | Latitude coordinate of the peer's geographic location. |
    | `peer_lon` | `Float64` | Longitude coordinate of the peer's geographic location. |
    | `neighbor_discovery_id_prefix` | `UInt64` | Prefix of the unique identifier for the neighboring peer. |
    | `neighbor_client` | `String` | Client software or implementation used by the neighboring peer. |
    | `neighbor_city` | `String` | City where the neighboring peer is located. |
    | `neighbor_country` | `String` | Country where the neighboring peer is located. |
    | `neighbor_org` | `String` | Organization associated with the neighboring peer, if available. |
    | `neighbor_lat` | `Float64` | Latitude coordinate of the neighboring peer's location. |
    | `neighbor_lon` | `Float64` | Longitude coordinate of the neighboring peer's location. |
    | `cnt` | `UInt64` | Count of occurrences or connections between the peer and neighbor, representing the connection strength or frequency. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/p2p/network_topology/latest"
    ```

## visits_per_protocol

This view provides the latest daily visit metrics for P2P protocols (discv4 and discv5), including total visits, success rates, and crawl counts, along with their percentage changes compared to the previous 7 days.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/p2p/visits_per_protocol/latest` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/p2p/visits_per_protocol/latest`"
    This view provides the latest daily visit metrics for P2P protocols (discv4 and discv5), including total visits, success rates, and crawl counts, along with their percentage changes compared to the previous 7 days.

    Model: `api_p2p_visits_latest` — table `dbt.api_p2p_visits_latest`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The date for which the visit metrics are reported. |
    | `crawls` | `UInt64` | The number of crawl attempts recorded on the specified date. |
    | `discv4_total_visits` | `UInt64` | Total number of Discv4 visits in the latest data snapshot. |
    | `discv4_pct_successful` | `Float64` | Percentage of successful Discv4 visits, rounded to one decimal. |
    | `discv4_crawls` | `UInt64` | Number of Discv4 crawl attempts in the latest data. |
    | `change_discv4_crawls_pct` | `Float64` | Percentage change in Discv4 crawls compared to the previous week. |
    | `discv5_total_visits` | `UInt64` | Total number of Discv5 visits in the latest data snapshot. |
    | `discv5_pct_successful` | `Float64` | Percentage of successful Discv5 visits, rounded to one decimal. |
    | `discv5_crawls` | `UInt64` | Number of Discv5 crawl attempts in the latest data. |
    | `change_discv5_crawls_pct` | `Float64` | Percentage change in Discv5 crawls compared to the previous week. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/p2p/visits_per_protocol/latest"
    ```
<!-- END AUTO-GENERATED: api-catalog-p2p -->
