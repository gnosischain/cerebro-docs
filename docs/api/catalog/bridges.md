# Bridges API Endpoints

<!-- BEGIN AUTO-GENERATED: api-catalog-bridges -->
<!-- generated: 2026-07-23 -->
_12 endpoints across 10 resources. Generated from the dbt manifest — edits inside this block will be overwritten. Regenerate with `python scripts/update_docs.py --only api`._

## bridges_count

This model provides the most recent count of distinct bridges tracked over time, serving as a key performance indicator for bridge coverage analysis.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/bridges/bridges_count/latest` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/bridges/bridges_count/latest`"
    This model provides the most recent count of distinct bridges tracked over time, serving as a key performance indicator for bridge coverage analysis.

    Model: `api_bridges_kpi_distinct_bridges_all_time` — table `dbt.api_bridges_kpi_distinct_bridges_all_time`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `value` | `UInt64` | The latest number of unique bridges identified, representing the total count at the most recent snapshot. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/bridges/bridges_count/latest"
    ```

## chains_count

This dbt view provides the most recent count of distinct API bridge chains, serving as a key performance indicator for monitoring API connectivity and diversity over time.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/bridges/chains_count/latest` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/bridges/chains_count/latest`"
    This dbt view provides the most recent count of distinct API bridge chains, serving as a key performance indicator for monitoring API connectivity and diversity over time.

    Model: `api_bridges_kpi_distinct_chains_all_time` — table `dbt.api_bridges_kpi_distinct_chains_all_time`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `value` | `UInt64` | The total number of distinct API bridge chains as of the latest snapshot, representing a count metric. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/bridges/chains_count/latest"
    ```

## cum_netflow_per_bridge

This view aggregates cumulative net flow in USD per bridge on a weekly basis, supporting trend analysis and reporting for infrastructure financial flows.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/bridges/cum_netflow_per_bridge/weekly` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/bridges/cum_netflow_per_bridge/weekly`"
    This view aggregates cumulative net flow in USD per bridge on a weekly basis, supporting trend analysis and reporting for infrastructure financial flows.

    Model: `api_bridges_cum_netflow_weekly_by_bridge` — table `dbt.api_bridges_cum_netflow_weekly_by_bridge`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The starting date of the week for which the net flow data is aggregated, formatted as a date. |
    | `series` | `String` | Identifier for the specific bridge associated with the net flow data. |
    | `value` | `Float64` | Cumulative net flow in USD for the specified bridge during the week. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/bridges/cum_netflow_per_bridge/weekly" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## inflow

This view aggregates inbound token transfer flows between sources and targets over specified time ranges, supporting analysis of token inflow patterns in the Gnosis ecosystem.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/bridges/inflow/in_ranges` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/bridges/inflow/in_ranges`"
    This view aggregates inbound token transfer flows between sources and targets over specified time ranges, supporting analysis of token inflow patterns in the Gnosis ecosystem.

    Model: `api_bridges_sankey_gnosis_in_ranges` — table `dbt.api_bridges_sankey_gnosis_in_ranges`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `d` | `DateTime64(0, 'UTC')` | The date associated with the data, representing the latest date in the dataset for the respective range. |
    | `range` | `String` | The time range over which the transactions are aggregated. Possible values include '1D', '7D', '30D', '90D', and 'All'. |
    | `source` | `String` | The originating address or identifier from which the value is transferred. |
    | `target` | `String` | The destination address or identifier to which the value is transferred. |
    | `value` | `UInt64` | The total value transferred from source to target within the specified range. Measured in wei. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/bridges/inflow/in_ranges"
    ```

## inflow_per_token

This model aggregates inbound transfer values for each token over the last 7 days, facilitating analysis of token inflows in bridge operations.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/bridges/inflow_per_token/last_7d` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/bridges/inflow_per_token/last_7d`"
    This model aggregates inbound transfer values for each token over the last 7 days, facilitating analysis of token inflows in bridge operations.

    Model: `api_bridges_sankey_gnosis_in_by_token_7d` — table `dbt.api_bridges_sankey_gnosis_in_by_token_7d`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `d` | `DateTime64(0, 'UTC')` | The most recent date in the dataset, representing the end of the 7-day aggregation window. |
    | `token` | `String` | The token involved in the bridge transaction, represented by its symbol or contract address. |
    | `source` | `String` | The originating source of the token flow in the bridge transaction. |
    | `target` | `String` | The destination target of the token flow in the bridge transaction. |
    | `value` | `UInt64` | The total value of the token flow in the bridge transaction over the past 7 days, measured in the smallest unit of the token. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/bridges/inflow_per_token/last_7d"
    ```

## netflow

The api_bridges_kpi_netflow_7d model provides a snapshot of net flow metrics over the last 7 days, enabling trend analysis and performance monitoring for API bridge operations.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/bridges/netflow/last_7d` | GET | tier0 | -- | -- | -- |
| `/v1/bridges/netflow/all_time` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/bridges/netflow/last_7d`"
    The api_bridges_kpi_netflow_7d model provides a snapshot of net flow metrics over the last 7 days, enabling trend analysis and performance monitoring for API bridge operations.

    Model: `api_bridges_kpi_netflow_7d` — table `dbt.api_bridges_kpi_netflow_7d`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `value` | `Float64` | The net flow value over the last 7 days, rounded to two decimal places. |
    | `prev_value` | `Float64` | The net flow value for the previous 7-day period, rounded to two decimal places. |
    | `change_pct` | `Float64` | The percentage change in net flow between the current and previous 7-day periods. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/bridges/netflow/last_7d"
    ```

??? info "`GET /v1/bridges/netflow/all_time`"
    This dbt view aggregates the total net flow in USD over all time periods, providing a comprehensive KPI snapshot for API bridge performance.

    Model: `api_bridges_kpi_total_netflow_all_time` — table `dbt.api_bridges_kpi_total_netflow_all_time`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `value` | `Float64` | The total net flow in USD, rounded to two decimal places, representing the cumulative net flow across all time. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/bridges/netflow/all_time"
    ```

## netflow_per_token_per_bridge

This view aggregates daily net flow values for each token across individual bridges and provides a combined total for all bridges, supporting analysis of token movement at a daily granularity.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/bridges/netflow_per_token_per_bridge/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/bridges/netflow_per_token_per_bridge/daily`"
    This view aggregates daily net flow values for each token across individual bridges and provides a combined total for all bridges, supporting analysis of token movement at a daily granularity.

    Model: `api_bridges_token_netflow_daily_by_bridge` — table `dbt.api_bridges_token_netflow_daily_by_bridge`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The specific calendar date for the recorded net flow data. |
    | `bridge` | `String` | The name or identifier of the bridge; 'All' indicates the aggregate across all bridges. |
    | `token` | `String` | The identifier of the token involved in the net flow calculation. |
    | `value` | `UInt64` | The net flow value for the token on the given date, representing the total transfer amount. |
    | `bridge_order` | `UInt64` | An order indicator used to prioritize specific bridge data over the 'All' category in sorting operations. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/bridges/netflow_per_token_per_bridge/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## outflow

This view aggregates outflow token transfer data across different time ranges for API bridges, supporting analysis of token flow patterns over specified periods.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/bridges/outflow/in_ranges` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/bridges/outflow/in_ranges`"
    This view aggregates outflow token transfer data across different time ranges for API bridges, supporting analysis of token flow patterns over specified periods.

    Model: `api_bridges_sankey_gnosis_out_ranges` — table `dbt.api_bridges_sankey_gnosis_out_ranges`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `d` | `Date` | Represents the date range label (e.g., 1D, 7D, 30D, 90D, All) corresponding to the aggregation period. |
    | `range` | `String` | The time range for which the transaction data is aggregated. Possible values include '1D', '7D', '30D', '90D', and 'All'. |
    | `source` | `String` | The originating point of the bridge transaction, typically an address or identifier for the source network or entity. |
    | `target` | `String` | The destination point of the bridge transaction, typically an address or identifier for the target network or entity. |
    | `value` | `UInt64` | The total value of transactions from the source to the target within the specified range, measured in the smallest unit of the currency. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/bridges/outflow/in_ranges"
    ```

## outflow_per_token

This view aggregates the total outflow values of tokens between sources and targets over the last 7 days, providing insights into token transfer flows within the system.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/bridges/outflow_per_token/last_7d` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/bridges/outflow_per_token/last_7d`"
    This view aggregates the total outflow values of tokens between sources and targets over the last 7 days, providing insights into token transfer flows within the system.

    Model: `api_bridges_sankey_gnosis_out_by_token_7d` — table `dbt.api_bridges_sankey_gnosis_out_by_token_7d`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `d` | `DateTime64(0, 'UTC')` | The most recent date in the dataset, representing the end of the 7-day aggregation window. |
    | `token` | `String` | The token involved in the bridge transaction, identified by its symbol. |
    | `source` | `String` | The originating bridge or network of the transaction. |
    | `target` | `String` | The destination bridge or network of the transaction. |
    | `value` | `UInt64` | The total value of the transactions in the smallest unit of the token, aggregated over the past seven days. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/bridges/outflow_per_token/last_7d"
    ```

## volume

The api_bridges_kpi_volume_7d model provides a snapshot of API volume metrics over the last 7 days, enabling trend analysis and performance monitoring.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/bridges/volume/last_7d` | GET | tier0 | -- | -- | -- |
| `/v1/bridges/volume/all_time` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/bridges/volume/last_7d`"
    The api_bridges_kpi_volume_7d model provides a snapshot of API volume metrics over the last 7 days, enabling trend analysis and performance monitoring.

    Model: `api_bridges_kpi_volume_7d` — table `dbt.api_bridges_kpi_volume_7d`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `value` | `Float64` | The total API volume over the most recent 7-day period, rounded to two decimal places. |
    | `prev_value` | `Float64` | The API volume for the previous 7-day period, rounded to two decimal places. |
    | `change_pct` | `Float64` | The percentage change in API volume between the current and previous 7-day periods. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/bridges/volume/last_7d"
    ```

??? info "`GET /v1/bridges/volume/all_time`"
    The `api_bridges_kpi_total_volume_all_time` model provides the most recent total volume in USD across all bridges, serving as a key metric for overall bridge activity over time.

    Model: `api_bridges_kpi_total_volume_all_time` — table `dbt.api_bridges_kpi_total_volume_all_time`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `value` | `Float64` | The cumulative total volume in USD, rounded to two decimal places, representing the all-time total transaction volume. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/bridges/volume/all_time"
    ```
<!-- END AUTO-GENERATED: api-catalog-bridges -->
