# Consensus API Endpoints

<!-- BEGIN AUTO-GENERATED: api-catalog-consensus -->
_35 endpoints across 27 resources. Generated from the dbt manifest — edits inside this block will be overwritten. Regenerate with `python scripts/update_docs.py --only api`._

!!! warning "5 additional model(s) not live"
    5 more model(s) in this category declare `api:` tags but their `meta.api` metadata fails validation, so the live API skips them. See the generator log for the model names; the fix belongs in the dbt model.

## attestations

The api_consensus_attestations_daily model provides a daily summary of consensus attestations, capturing key metrics for monitoring and analysis of attestation activity over time.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/consensus/attestations/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/consensus/attestations/daily`"
    The api_consensus_attestations_daily model provides a daily summary of consensus attestations, capturing key metrics for monitoring and analysis of attestation activity over time.

    Model: `api_consensus_attestations_daily` — table `dbt.api_consensus_attestations_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The specific calendar date for the recorded attestation data. |
    | `inclusion_delay` | `UInt64` | The number of blocks or time units between the attestation event and its inclusion in the blockchain. |
    | `cnt` | `UInt64` | The total count of attestations recorded on the given date with the specified inclusion delay. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/consensus/attestations/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## attestations_performance

Public API view over fct_consensus_attestations_performance_daily. Network-wide daily attestation KPIs.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/consensus/attestations_performance/daily` | GET, POST | tier1 | `date_from`, `date_to` | limit/offset (envelope) | date DESC |

??? info "`GET/POST /v1/consensus/attestations_performance/daily`"
    Public API view over fct_consensus_attestations_performance_daily. Network-wide daily attestation KPIs.

    Model: `api_consensus_attestations_performance_daily` — table `dbt.api_consensus_attestations_performance_daily`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `date_from` | `>=` | `date` | date | Inclusive lower bound on date |
    | `date_to` | `<=` | `date` | date | Inclusive upper bound on date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** `limit`/`offset` — default 100, max 5000; response: envelope `{items, pagination}`

    **Sort:** `date DESC` — user-sortable via `sort_by`: `date`, `attestations_total`, `avg_inclusion_delay`, `p50_inclusion_delay`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `DateTime64` | Start-of-day UTC for the network-wide attestation KPIs. One row per day. |
    | `attestations_total` | `UInt64` | Total attestations included on the date. |
    | `avg_inclusion_delay` | `Float64` | Weighted mean inclusion delay (in slots). |
    | `p50_inclusion_delay` | `Float64` | Weighted median inclusion delay (in slots). |
    | `pct_inclusion_distance_1` | `Float64` | Share of attestations included with inclusion_delay = 1. Range [0, 1]. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/consensus/attestations_performance/daily?date_from=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## blob_commitments

The api_consensus_blob_commitments_daily model provides a daily overview of total blob commitments within the consensus layer, supporting trend analysis and capacity planning.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/consensus/blob_commitments/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/consensus/blob_commitments/daily`"
    The api_consensus_blob_commitments_daily model provides a daily overview of total blob commitments within the consensus layer, supporting trend analysis and capacity planning.

    Model: `api_consensus_blob_commitments_daily` — table `dbt.api_consensus_blob_commitments_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The specific calendar date for the recorded blob commitments, formatted as YYYY-MM-DD. |
    | `value` | `UInt64` | The total number of blob commitments made on the given date. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/consensus/blob_commitments/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## blocks

The api_consensus_blocks_daily model aggregates daily consensus block data, providing insights into blocks produced and missed each day for monitoring network performance.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/consensus/blocks/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/consensus/blocks/daily`"
    The api_consensus_blocks_daily model aggregates daily consensus block data, providing insights into blocks produced and missed each day for monitoring network performance.

    Model: `api_consensus_blocks_daily` — table `dbt.api_consensus_blocks_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The specific calendar date for the recorded metrics. |
    | `label` | `String` | Indicator specifying whether the row represents 'produced' or 'missed' blocks. |
    | `value` | `UInt64` | Count of consensus blocks, representing either produced or missed blocks on the given date. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/consensus/blocks/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## blocks_and_blobs

This view provides daily aggregated counts of consensus blocks with and without zero blob commitments, aiding in monitoring blockchain data integrity and activity levels.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/consensus/blocks_and_blobs/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/consensus/blocks_and_blobs/daily`"
    This view provides daily aggregated counts of consensus blocks with and without zero blob commitments, aiding in monitoring blockchain data integrity and activity levels.

    Model: `api_consensus_zero_blob_commitments_daily` — table `dbt.api_consensus_zero_blob_commitments_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The date for which the block commitment data is recorded, formatted as YYYY-MM-DD. |
    | `label` | `String` | A categorical label indicating whether the count pertains to blocks with or without zero blob commitments. |
    | `value` | `Int64` | The numerical count of blocks, represented as a 64-bit integer, corresponding to the specified label and date. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/consensus/blocks_and_blobs/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## consolidations

Public API view — SELECT * FROM fct_consensus_consolidations_daily. Filter/pagination metadata in model config.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/consensus/consolidations/daily` | GET, POST | tier1 | `date_from`, `date_to`, `role` | limit/offset (envelope) | date DESC |

??? info "`GET/POST /v1/consensus/consolidations/daily`"
    Public API view — SELECT * FROM fct_consensus_consolidations_daily. Filter/pagination metadata in model config.

    Model: `api_consensus_consolidations_daily` — table `dbt.api_consensus_consolidations_daily`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `date_from` | `>=` | `date` | date | Inclusive lower bound on date |
    | `date_to` | `<=` | `date` | date | Inclusive upper bound on date |
    | `role` | `=` | `role` | string | One of self / source / target |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** `limit`/`offset` — default 5000, max 10000; response: envelope `{items, pagination}`

    **Sort:** `date DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `DateTime64` | Application date of the consolidation events (start-of-day UTC). |
    | `role` | `String` | One of 'self' / 'source' / 'target'. |
    | `cnt` | `UInt64` | Number of consolidation events on the date for the role. |
    | `transferred_amount_gno` | `Float64` | 0 for 'self' rows; positive for source/target. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/consensus/consolidations/daily?date_from=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## credentials

The api_consensus_credentials_latest model provides a snapshot of the most recent count of different credential types used in the API consensus system, supporting real-time monitoring and analysis.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/consensus/credentials/latest` | GET | tier0 | -- | -- | -- |
| `/v1/consensus/credentials/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/consensus/credentials/latest`"
    The api_consensus_credentials_latest model provides a snapshot of the most recent count of different credential types used in the API consensus system, supporting real-time monitoring and analysis.

    Model: `api_consensus_credentials_latest` — table `dbt.api_consensus_credentials_latest`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `credentials_type` | `String` | The category or type of API credential, such as API key or OAuth token. |
    | `cnt` | `UInt64` | The number of credentials of the specified type at the latest date, representing a count. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/consensus/credentials/latest"
    ```

??? info "`GET /v1/consensus/credentials/daily`"
    The api_consensus_credentials_daily model provides daily aggregated counts and percentage shares of different credential types used in the API, supporting operational and strategic analysis.

    Model: `api_consensus_credentials_daily` — table `dbt.api_consensus_credentials_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The specific calendar date for the recorded credential data. |
    | `credentials_type` | `String` | The category or type of credentials used in the API during the specified date. |
    | `cnt` | `UInt64` | The total number of credentials of a specific type recorded on the given date. |
    | `pct` | `UInt64` | The percentage share of each credential type relative to the total credentials on that date, rounded to two decimal places. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/consensus/credentials/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## deposits_and_withdrawals

The model aggregates daily counts of consensus deposits and withdrawals to monitor transaction activity trends over time.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/consensus/deposits_and_withdrawals/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/consensus/deposits_and_withdrawals/daily`"
    The model aggregates daily counts of consensus deposits and withdrawals to monitor transaction activity trends over time.

    Model: `api_consensus_deposits_withdrawls_cnt_daily` — table `dbt.api_consensus_deposits_withdrawls_cnt_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The specific calendar date for the recorded counts, formatted as YYYY-MM-DD. |
    | `label` | `String` | A categorical indicator distinguishing between deposit and withdrawal counts. |
    | `value` | `UInt64` | The number of deposits or withdrawals recorded on the given date, representing transaction volume. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/consensus/deposits_and_withdrawals/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## deposits_and_withdrawals_volume

The api_consensus_deposits_withdrawls_volume_daily model provides a daily summary of deposit and withdrawal volumes from the API, facilitating trend analysis and reporting.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/consensus/deposits_and_withdrawals_volume/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/consensus/deposits_and_withdrawals_volume/daily`"
    The api_consensus_deposits_withdrawls_volume_daily model provides a daily summary of deposit and withdrawal volumes from the API, facilitating trend analysis and reporting.

    Model: `api_consensus_deposits_withdrawls_volume_daily` — table `dbt.api_consensus_deposits_withdrawls_volume_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The specific calendar date for the recorded deposit or withdrawal volume. |
    | `label` | `String` | A categorical identifier indicating the type or source of the deposit or withdrawal event. |
    | `value` | `UInt64` | The total amount of deposits or withdrawals in the specified category on the given date, measured in the relevant currency units. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/consensus/deposits_and_withdrawals_volume/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## deposits_cnt

The model provides the latest consensus information on the total number of deposits, serving as a key metric for monitoring deposit activity trends.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/consensus/deposits_cnt/latest` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/consensus/deposits_cnt/latest`"
    The model provides the latest consensus information on the total number of deposits, serving as a key metric for monitoring deposit activity trends.

    Model: `api_consensus_info_deposits_cnt_latest` — table `dbt.api_consensus_info_deposits_cnt_latest`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `value` | `Float64` | The current total count of deposits, representing the latest available figure. |
    | `change_pct` | `Float64` | The percentage change in the deposit count compared to the previous measurement period. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/consensus/deposits_cnt/latest"
    ```

## entry_queue

The api_consensus_entry_queue_daily model provides daily aggregated statistics on the validator entry queue, enabling analysis of queue size and distribution over time for consensus monitoring.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/consensus/entry_queue/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/consensus/entry_queue/daily`"
    The api_consensus_entry_queue_daily model provides daily aggregated statistics on the validator entry queue, enabling analysis of queue size and distribution over time for consensus monitoring.

    Model: `api_consensus_entry_queue_daily` — table `dbt.api_consensus_entry_queue_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The specific calendar date for the recorded metrics. |
    | `validator_count` | `UInt64` | Number of validators active on the given date. |
    | `q05` | `Float64` | 5th percentile of the entry queue size, indicating the lower bound of queue length distribution. |
    | `q10` | `Float64` | 10th percentile of the entry queue size, representing the lower tail of the distribution. |
    | `q25` | `Float64` | 25th percentile (first quartile) of the queue size distribution. |
    | `q50` | `Float64` | Median queue size, representing the middle value of the distribution. |
    | `q75` | `Float64` | 75th percentile (third quartile) of the queue size, indicating the upper quartile. |
    | `q90` | `Float64` | 90th percentile of the queue size, showing the upper tail of the distribution. |
    | `q95` | `Float64` | 95th percentile of the queue size, highlighting the extreme upper values. |
    | `mean` | `Float64` | Average queue size across all validators for the given date. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/consensus/entry_queue/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## forks_info

The api_consensus_forks model provides a consolidated view of consensus fork information used in the blockchain network, facilitating analysis of fork versions and their identifiers.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/consensus/forks_info/latest` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/consensus/forks_info/latest`"
    The api_consensus_forks model provides a consolidated view of consensus fork information used in the blockchain network, facilitating analysis of fork versions and their identifiers.

    Model: `api_consensus_forks` — table `dbt.api_consensus_forks`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `fork_name` | `String` | The human-readable name identifying the specific consensus fork. |
    | `fork_version` | `String` | The numeric version identifier of the fork, used for ordering and comparison. |
    | `fork_digest` | `String` | A unique cryptographic digest representing the fork's specific state or configuration. |
    | `fork_epoch` | `UInt64` | The epoch number indicating the activation point of the fork within the blockchain's timeline. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/consensus/forks_info/latest"
    ```

## graffities_labels

The api_consensus_graffiti_label_daily model aggregates daily counts of graffiti labels to support trend analysis and reporting for consensus graffiti labeling efforts.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/consensus/graffities_labels/daily` | GET | tier1 | -- | -- | -- |
| `/v1/consensus/graffities_labels/in_ranges` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/consensus/graffities_labels/daily`"
    The api_consensus_graffiti_label_daily model aggregates daily counts of graffiti labels to support trend analysis and reporting for consensus graffiti labeling efforts.

    Model: `api_consensus_graffiti_label_daily` — table `dbt.api_consensus_graffiti_label_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The specific calendar date for the aggregated data, formatted as YYYY-MM-DD. |
    | `label` | `String` | The identifier or category of the graffiti label being counted. |
    | `value` | `UInt64` | The total count of occurrences for the given label on the specified date. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/consensus/graffities_labels/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/consensus/graffities_labels/in_ranges`"
    The api_consensus_graffiti_cloud model aggregates consensus data related to graffiti labels and their associated values, facilitating analysis of graffiti patterns and trends at a granular level.

    Model: `api_consensus_graffiti_cloud` — table `dbt.api_consensus_graffiti_cloud`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `label` | `String` | The category or type of graffiti label being analyzed. |
    | `graffiti` | `String` | The specific graffiti instance or identifier associated with the label. |
    | `value` | `Float64` | Numerical score or metric representing the consensus or confidence level for the graffiti label, typically within a defined range. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/consensus/graffities_labels/in_ranges"
    ```

## staked_gno

The api_consensus_info_staked_latest model provides the most recent total staked GNO value and its percentage change, supporting real-time analysis of staking metrics in the GNO ecosystem.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/consensus/staked_gno/latest` | GET | tier0 | -- | -- | -- |
| `/v1/consensus/staked_gno/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/consensus/staked_gno/latest`"
    The api_consensus_info_staked_latest model provides the most recent total staked GNO value and its percentage change, supporting real-time analysis of staking metrics in the GNO ecosystem.

    Model: `api_consensus_info_staked_latest` — table `dbt.api_consensus_info_staked_latest`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `value` | `Float64` | The total amount of GNO currently staked, represented as an unsigned 32-bit integer. |
    | `change_pct` | `Float64` | The percentage change in the staked GNO amount compared to the previous measurement. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/consensus/staked_gno/latest"
    ```

??? info "`GET /v1/consensus/staked_gno/daily`"
    The api_consensus_staked_daily model provides daily aggregated data on the effective staked GNO across validators, facilitating analysis of staking trends over time.

    Model: `api_consensus_staked_daily` — table `dbt.api_consensus_staked_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The specific calendar date for the recorded staked balance. |
    | `value` | `Float64` | The network's total effective balance in real GNO (mGNO->GNO conversion happens upstream in int_consensus_validators_balances_daily). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/consensus/staked_gno/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## validators_active_ongoing

The model provides the latest consensus information on active and ongoing items, serving as a key reference for monitoring current operational states.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/consensus/validators_active_ongoing/latest` | GET | tier0 | -- | -- | -- |
| `/v1/consensus/validators_active_ongoing/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/consensus/validators_active_ongoing/latest`"
    The model provides the latest consensus information on active and ongoing items, serving as a key reference for monitoring current operational states.

    Model: `api_consensus_info_active_ongoing_latest` — table `dbt.api_consensus_info_active_ongoing_latest`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `value` | `Float64` | The numeric value representing the current measurement or count related to active and ongoing consensus data. |
    | `change_pct` | `Float64` | The percentage change in the value compared to the previous measurement, indicating the trend or variation over time. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/consensus/validators_active_ongoing/latest"
    ```

??? info "`GET /v1/consensus/validators_active_ongoing/daily`"
    The api_consensus_validators_active_daily model provides a daily snapshot of the number of validators that are actively participating in the consensus process, supporting monitoring and analysis of validator activity trends.

    Model: `api_consensus_validators_active_daily` — table `dbt.api_consensus_validators_active_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The specific calendar date for the recorded validator activity count. |
    | `cnt` | `UInt64` | The total number of validators actively participating on the given date. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/consensus/validators_active_ongoing/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## validators_apy

The api_consensus_info_apy_latest model provides the most recent annual percentage yield (APY) data from consensus sources, enabling analysis of current yield trends.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/consensus/validators_apy/latest` | GET | tier0 | -- | -- | -- |
| `/v1/consensus/validators_apy/daily` | GET, POST | tier1 | `date_from`, `date_to` | limit/offset (envelope) | date DESC |
| `/v1/consensus/validators_apy/daily` | GET, POST | tier1 | `date_from`, `date_to` | limit/offset (envelope) | date DESC |

??? info "`GET /v1/consensus/validators_apy/latest`"
    The api_consensus_info_apy_latest model provides the most recent annual percentage yield (APY) data from consensus sources, enabling analysis of current yield trends.

    Model: `api_consensus_info_apy_latest` — table `dbt.api_consensus_info_apy_latest`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `value` | `Float64` | The latest APY value, representing the annual percentage yield as a decimal or percentage. |
    | `change_pct` | `Float64` | The percentage change in APY compared to the previous measurement period. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/consensus/validators_apy/latest"
    ```

??? info "`GET/POST /v1/consensus/validators_apy/daily`"
    Public API view — SELECT * FROM fct_consensus_validators_apy_mean_daily. Filter/pagination metadata in model config.

    Model: `api_consensus_validators_apy_mean_daily` — table `dbt.api_consensus_validators_apy_mean_daily`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `date_from` | `>=` | `date` | date | Inclusive lower bound on date |
    | `date_to` | `<=` | `date` | date | Inclusive upper bound on date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** `limit`/`offset` — default 2000, max 10000; response: envelope `{items, pagination}`

    **Sort:** `date DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `DateTime64` | Start-of-day UTC for the network-wide daily mean APY. One row per day. |
    | `apy` | `Float64` | Average APY (%) across all validators on the date, outliers filtered. |
    | `apy_rolling_7d_median` | `Float64` | 7-day trailing median of apy. Smoothing overlay for the dashboard band chart. |
    | `apy_rolling_30d_median` | `Float64` | 30-day trailing median of apy. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/consensus/validators_apy/daily?date_from=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET/POST /v1/consensus/validators_apy/daily`"
    Public API view — SELECT * FROM int_consensus_validators_apy_dist_income_daily. Filter/pagination metadata in model config.

    Model: `api_consensus_validators_apy_dist_income_daily` — table `dbt.api_consensus_validators_apy_dist_income_daily`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `date_from` | `>=` | `date` | date | Inclusive lower bound on date |
    | `date_to` | `<=` | `date` | date | Inclusive upper bound on date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** `limit`/`offset` — default 2000, max 10000; response: envelope `{items, pagination}`

    **Sort:** `date DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `DateTime` | Start-of-day UTC for the network-wide APY distribution. |
    | `q05_apy` | `Float64` | 5th-percentile (T-Digest) validator APY across active validators on the date. |
    | `q10_apy` | `Float64` | 10th-percentile (T-Digest) validator APY across active validators on the date. |
    | `q25_apy` | `Float64` | 25th-percentile (T-Digest) validator APY across active validators on the date. |
    | `q50_apy` | `Float64` | Median (T-Digest) validator APY across active validators on the date. |
    | `q75_apy` | `Float64` | 75th-percentile (T-Digest) validator APY across active validators on the date. |
    | `q90_apy` | `Float64` | 90th-percentile (T-Digest) validator APY across active validators on the date. |
    | `q95_apy` | `Float64` | 95th-percentile (T-Digest) validator APY across active validators on the date. |
    | `avg_apy_weighted` | `Float64` | Balance-weighted mean APY on the date. Matches fct_consensus_validators_apy_mean_daily.apy. |
    | `validators_included` | `UInt64` | Count of (date, validator_index) rows that passed the outlier+active filters. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/consensus/validators_apy/daily?date_from=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## validators_apy_dististribution

This view provides a distribution of validator APYs over the last 30 days, enabling analysis of APY variability and trends within the validator set.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/consensus/validators_apy_dististribution/last_30d` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/consensus/validators_apy_dististribution/last_30d`"
    This view provides a distribution of validator APYs over the last 30 days, enabling analysis of APY variability and trends within the validator set.

    Model: `api_consensus_validators_apy_dist_last_30_days` — table `dbt.api_consensus_validators_apy_dist_last_30_days`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The specific date for which the APY distribution data is aggregated. |
    | `q05` | `Float64` | The 5th percentile of validator APYs, indicating the lower bound of the APY distribution. |
    | `q10` | `Float64` | The 10th percentile of validator APYs, representing the lower tail of the distribution. |
    | `q25` | `Float64` | The 25th percentile (first quartile) of validator APYs, marking the lower quartile boundary. |
    | `q50` | `Float64` | The median APY value, dividing the distribution into two equal halves. |
    | `q75` | `Float64` | The 75th percentile (third quartile) of validator APYs, indicating the upper quartile boundary. |
    | `q90` | `Float64` | The 90th percentile of validator APYs, representing the upper tail of the distribution. |
    | `q95` | `Float64` | The 95th percentile of validator APYs, capturing the highest APYs within the distribution. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/consensus/validators_apy_dististribution/last_30d"
    ```

## validators_apy_distribution

This view provides daily distribution metrics of validator APYs, enabling analysis of validator performance variability over time.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/consensus/validators_apy_distribution/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/consensus/validators_apy_distribution/daily`"
    This view provides daily distribution metrics of validator APYs, enabling analysis of validator performance variability over time.

    Model: `api_consensus_validators_apy_dist_daily` — table `dbt.api_consensus_validators_apy_dist_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The specific day for which the APY distribution data is recorded. |
    | `q05` | `Float64` | The 5th percentile of validator APYs on the given date, indicating the lower tail of the distribution. |
    | `q10` | `Float64` | The 10th percentile of validator APYs, representing the lower decile of the distribution. |
    | `q25` | `Float64` | The 25th percentile (first quartile) of validator APYs, marking the lower quartile boundary. |
    | `q50` | `Float64` | The median validator APY for the date, dividing the distribution into two equal halves. |
    | `q75` | `Float64` | The 75th percentile (third quartile) of validator APYs, indicating the upper quartile boundary. |
    | `q90` | `Float64` | The 90th percentile of validator APYs, representing the upper decile of the distribution. |
    | `q95` | `Float64` | The 95th percentile of validator APYs, indicating the upper tail of the distribution. |
    | `average` | `Float64` | The mean validator APY for the date, providing an overall average across validators. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/consensus/validators_apy_distribution/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## validators_balance_dististribution

This view provides the distribution of validator balances over the last 30 days, summarized through various quantiles to analyze balance spread and trends.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/consensus/validators_balance_dististribution/last_30d` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/consensus/validators_balance_dististribution/last_30d`"
    This view provides the distribution of validator balances over the last 30 days, summarized through various quantiles to analyze balance spread and trends.

    Model: `api_consensus_validators_balance_dist_last_30_days` — table `dbt.api_consensus_validators_balance_dist_last_30_days`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The date corresponding to the balance distribution snapshot. |
    | `q05` | `Float64` | The 5th percentile of validator balances, indicating the lower tail of the distribution. |
    | `q10` | `Float64` | The 10th percentile of validator balances, representing the lower decile of the distribution. |
    | `q25` | `Float64` | The 25th percentile (first quartile) of validator balances, marking the lower quartile boundary. |
    | `q50` | `Float64` | The median validator balance, dividing the distribution into two equal halves. |
    | `q75` | `Float64` | The 75th percentile (third quartile) of validator balances, marking the upper quartile boundary. |
    | `q90` | `Float64` | The 90th percentile of validator balances, indicating the upper tail of the distribution. |
    | `q95` | `Float64` | The 95th percentile of validator balances, representing the upper extreme of the distribution. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/consensus/validators_balance_dististribution/last_30d"
    ```

## validators_balances

The api_consensus_validators_balances_daily model provides a daily overview of validator balances and effective balances to support consensus and validator health analysis.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/consensus/validators_balances/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/consensus/validators_balances/daily`"
    The api_consensus_validators_balances_daily model provides a daily overview of validator balances and effective balances to support consensus and validator health analysis.

    Model: `api_consensus_validators_balances_daily` — table `dbt.api_consensus_validators_balances_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The specific calendar date for the recorded validator balances. |
    | `label` | `String` | Identifier indicating whether the row represents 'balance' or 'eff. balance'. |
    | `value` | `Float64` | The numeric value of the validator balance or effective balance for the given date. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/consensus/validators_balances/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## validators_balances_distribution

This view provides daily distribution percentiles of validator balances in GNO, enabling analysis of validator balance variability over time.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/consensus/validators_balances_distribution/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/consensus/validators_balances_distribution/daily`"
    This view provides daily distribution percentiles of validator balances in GNO, enabling analysis of validator balance variability over time.

    Model: `api_consensus_validators_balances_dist_daily` — table `dbt.api_consensus_validators_balances_dist_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The specific day for which the balance distribution data is recorded. |
    | `q05` | `Float64` | The 5th percentile of validator balances in GNO, representing the lower tail of the distribution. |
    | `q10` | `Float64` | The 10th percentile of validator balances in GNO, indicating the balance below which 10% of validators fall. |
    | `q25` | `Float64` | The 25th percentile (first quartile) of validator balances in GNO. |
    | `q50` | `Float64` | The median validator balance in GNO, dividing the distribution into two equal halves. |
    | `q75` | `Float64` | The 75th percentile (third quartile) of validator balances in GNO. |
    | `q90` | `Float64` | The 90th percentile of validator balances in GNO, representing the upper tail of the distribution. |
    | `q95` | `Float64` | The 95th percentile of validator balances in GNO, indicating the top 5% of validator balances. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/consensus/validators_balances_distribution/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## validators_explorer

Balance-distribution histogram across co-validators sharing a withdrawal credential. Light view over fct_consensus_validators_status_latest (~558k rows); the API prunes by withdrawal_credentials before the bucketing runs so the query is cheap even without a physical index on credentials. Bucket e...

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/consensus/validators_explorer/latest` | GET, POST | tier1 | `withdrawal_credentials` | limit/offset (envelope) | bucket_order ASC |
| `/v1/consensus/validators_explorer/daily` | GET, POST | tier1 | `withdrawal_credentials`, `date_from`, `date_to` | limit/offset (envelope) | date DESC |
| `/v1/consensus/validators_explorer/daily` | GET, POST | tier1 | `withdrawal_credentials`, `date_from`, `date_to` | limit/offset (envelope) | date DESC |

??? info "`GET/POST /v1/consensus/validators_explorer/latest`"
    Balance-distribution histogram across co-validators sharing a withdrawal credential. Light view over fct_consensus_validators_status_latest (~558k rows); the API prunes by withdrawal_credentials before the bucketing runs so the query is cheap even without a physical index on credentials. Bucket e...

    Model: `api_consensus_validators_explorer_balance_dist` — table `dbt.api_consensus_validators_explorer_balance_dist`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `withdrawal_credentials` | `=` | `withdrawal_credentials` | string | Withdrawal credential (32-byte hex) — returns balance histogram across co-validators; case: lower |

    **Filter policy:** At least one filter required. Must provide one of: `withdrawal_credentials`.

    **Pagination:** `limit`/`offset` — default 16, max 64; response: envelope `{items, pagination}`

    **Sort:** `bucket_order ASC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `withdrawal_credentials` | `String` | Lowercased withdrawal credentials whose co-validators are bucketed (the required API filter). |
    | `bucket` | `String` | Label for the balance bucket ('<1', '1-16', '16-32', '32-48', '48-64', '64-128', '128-256', '>=256'). |
    | `bucket_order` | `UInt8` | Integer ordering key for the bucket (0-7) so downstream charts keep bars in ascending balance order. |
    | `validator_count` | `UInt64` | Number of validators under this credential falling in the balance bucket. |
    | `balance_gno_total` | `Float64` | Total balance in GNO across the validators in this credential-and-bucket. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/consensus/validators_explorer/latest?withdrawal_credentials=VALUE" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET/POST /v1/consensus/validators_explorer/daily`"
    Public API view — SELECT * FROM fct_consensus_validators_explorer_daily. Requires withdrawal_credentials filter; see model config.

    Model: `api_consensus_validators_explorer_daily` — table `dbt.api_consensus_validators_explorer_daily`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `withdrawal_credentials` | `=` | `withdrawal_credentials` | string | Withdrawal credential (32-byte hex) — aggregates daily metrics across every validator sharing this credential; case: lower |
    | `date_from` | `>=` | `date` | date | Inclusive lower bound on date |
    | `date_to` | `<=` | `date` | date | Inclusive upper bound on date |

    **Filter policy:** At least one filter required. Must provide one of: `withdrawal_credentials`.

    **Pagination:** `limit`/`offset` — default 1000, max 10000; response: envelope `{items, pagination}`

    **Sort:** `date DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `DateTime64` | Day of the roll-up (start-of-day UTC timestamp). Grain is one row per (date, withdrawal_credentials). |
    | `withdrawal_credentials` | `String` | Lowercased withdrawal credentials — the per-operator grouping key. |
    | `balance_gno` | `Float64` | Sum of end-of-day validator balances across validators sharing the credential, in GNO. |
    | `effective_balance_gno` | `Float64` | Sum of end-of-day effective balances across validators sharing the credential, in GNO. |
    | `consensus_income_amount_gno` | `Float64` | Sum of daily spec-bounded consensus income across validators sharing the credential, in GNO. |
    | `apy` | `Float64` | Mean APY across validators sharing this credential on the date, outliers filtered. |
    | `proposer_reward_total_gno` | `Float64` | Sum of proposer rewards earned on the date by validators sharing the credential, in GNO. |
    | `proposed_blocks_count` | `UInt64` | Total blocks proposed on the date by validators sharing the credential. |
    | `deposits_amount_gno` | `Float64` | Sum of raw reported deposit amounts on the date, in GNO. Post-Pectra these are request amounts that may be credited gradually via the pending-deposits queue ... |
    | `withdrawals_amount_gno` | `Float64` | Sum of amounts withdrawn on the date across validators sharing the credential, in GNO. |
    | `consolidation_inflow_gno` | `Float64` | Sum of consolidation amounts received (target role) on the date, in GNO. |
    | `consolidation_outflow_gno` | `Float64` | Sum of consolidation amounts transferred out (source role) on the date, in GNO. |
    | `validator_count_active` | `UInt64` | Count of distinct validator_index rows included in this (date, credential) aggregation. Dashboard uses this to decide between quantile bands (N>1) and a clea... |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/consensus/validators_explorer/daily?date_from=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET/POST /v1/consensus/validators_explorer/daily`"
    Public API view — SELECT * FROM int_consensus_validators_explorer_apy_dist_daily. Requires withdrawal_credentials filter; see model config.

    Model: `api_consensus_validators_explorer_apy_dist_daily` — table `dbt.api_consensus_validators_explorer_apy_dist_daily`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `withdrawal_credentials` | `=` | `withdrawal_credentials` | string | Withdrawal credential (32-byte hex) — per-day cross-sectional APY quantiles across the validators under this credenti...; case: lower |
    | `date_from` | `>=` | `date` | date | Inclusive lower bound on date |
    | `date_to` | `<=` | `date` | date | Inclusive upper bound on date |

    **Filter policy:** At least one filter required. Must provide one of: `withdrawal_credentials`.

    **Pagination:** `limit`/`offset` — default 1000, max 10000; response: envelope `{items, pagination}`

    **Sort:** `date DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `DateTime` | Start-of-day UTC for the credential's cross-sectional APY distribution. |
    | `withdrawal_credentials` | `String` | Lowercased withdrawal credentials grouping the validators whose APYs are aggregated. |
    | `q05_apy` | `Float64` | 5th-percentile (T-Digest) cross-sectional APY across validators under this credential on the date. |
    | `q10_apy` | `Float64` | 10th-percentile (T-Digest) cross-sectional APY across validators under this credential on the date. |
    | `q25_apy` | `Float64` | 25th-percentile (T-Digest) cross-sectional APY across validators under this credential on the date. |
    | `q50_apy` | `Float64` | Cross-sectional median APY across validators under this credential. |
    | `q75_apy` | `Float64` | 75th-percentile (T-Digest) cross-sectional APY across validators under this credential on the date. |
    | `q90_apy` | `Float64` | 90th-percentile (T-Digest) cross-sectional APY across validators under this credential on the date. |
    | `q95_apy` | `Float64` | 95th-percentile (T-Digest) cross-sectional APY across validators under this credential on the date. |
    | `apy_weighted` | `Float64` | Balance-weighted mean APY for the credential on the date. |
    | `validator_count_active` | `UInt64` | Distinct validators under this credential contributing to the day's stats. |
    | `apy_rolling_7d_median` | `Float64` | 7-day trailing median of apy_weighted per credential. Primary smoothing line for solo credentials. |
    | `apy_rolling_30d_median` | `Float64` | 30-day trailing median of apy_weighted per credential. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/consensus/validators_explorer/daily?date_from=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## validators_income

Public API view — SELECT * FROM fct_consensus_validators_income_total_daily. Filter/pagination metadata in model config.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/consensus/validators_income/daily` | GET, POST | tier1 | `date_from`, `date_to` | limit/offset (envelope) | date DESC |

??? info "`GET/POST /v1/consensus/validators_income/daily`"
    Public API view — SELECT * FROM fct_consensus_validators_income_total_daily. Filter/pagination metadata in model config.

    Model: `api_consensus_validators_income_total_daily` — table `dbt.api_consensus_validators_income_total_daily`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `date_from` | `>=` | `date` | date | Inclusive lower bound on date |
    | `date_to` | `<=` | `date` | date | Inclusive upper bound on date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** `limit`/`offset` — default 2000, max 10000; response: envelope `{items, pagination}`

    **Sort:** `date DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `DateTime64` | Start-of-day UTC for the network-wide daily income total. One row per day. |
    | `income_gno` | `Float64` | Sum of consensus_income_amount_gno across all validators on the date. |
    | `income_gno_rolling_7d_median` | `Float64` | 7-day trailing median of income_gno. Advisory overlay for the dashboard chart. |
    | `income_gno_rolling_30d_median` | `Float64` | 30-day trailing median of income_gno. |
    | `validators_snapshot_count` | `UInt64` | Count of validators snapshotted on the date from int_consensus_validators_snapshots_daily. |
    | `anomaly_flag` | `UInt8` | 1 when abs(income_gno) > 5 * trailing-30d median(abs(income_gno)) AND abs(income_gno) > 16 GNO (the old 500-mGNO floor in real-GNO terms). Advisory only — ra... |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/consensus/validators_income/daily?date_from=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## validators_search

Dropdown source for the Validator Explorer tab. Grain is one row per WITHDRAWAL_CREDENTIALS (not per validator) — on Gnosis today this is ~3,400 rows vs 558k at validator-grain, so the dashboard can load the full list in a single request (a few hundred KB on the wire) without 30s timeouts. Collap...

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/consensus/validators_search/latest` | GET, POST | tier1 | -- | limit/offset (envelope) | validator_count DESC |

??? info "`GET/POST /v1/consensus/validators_search/latest`"
    Dropdown source for the Validator Explorer tab. Grain is one row per WITHDRAWAL_CREDENTIALS (not per validator) — on Gnosis today this is ~3,400 rows vs 558k at validator-grain, so the dashboard can load the full list in a single request (a few hundred KB on the wire) without 30s timeouts. Collap...

    Model: `api_consensus_validators_search` — table `dbt.api_consensus_validators_search`

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** `limit`/`offset` — default 5000, max 10000; response: envelope `{items, pagination}`

    **Sort:** `validator_count DESC` — user-sortable via `sort_by`: `validator_count`, `withdrawal_credentials`, `display_name`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `withdrawal_credentials` | `String` | Lowercased withdrawal credentials — the per-row grouping key (one row per credential). |
    | `first_validator_index` | `UInt32` | Lowest validator_index (min) among all validators sharing this withdrawal_credentials; seeds the display_name and serves as a stable per-credential identifier. |
    | `validator_count` | `UInt64` | Number of validators sharing this withdrawal_credentials (COUNT(*)); 1 for a solo validator, N for an operator. |
    | `withdrawal_address` | `Nullable(String)` | 20-byte execution withdrawal address for the credential (any() representative); NULL for 0x00 BLS credentials. |
    | `display_name` | `String` | '<prefix-4>…<address-tail-10> · N validator(s) (v#<first-index>)' — the credential tail keeps same-prefix operators distinguishable; used by LabelSelector fo... |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/consensus/validators_search/latest" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## validators_status

The api_consensus_validators_status_daily model provides a daily summary of validator statuses, excluding ongoing active and withdrawal completed states, to monitor validator health and transitions over time.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/consensus/validators_status/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/consensus/validators_status/daily`"
    The api_consensus_validators_status_daily model provides a daily summary of validator statuses, excluding ongoing active and withdrawal completed states, to monitor validator health and transitions over time.

    Model: `api_consensus_validators_status_daily` — table `dbt.api_consensus_validators_status_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The specific calendar date for the recorded validator status counts. |
    | `status` | `String` | The current state of validators, such as 'pending', 'slashed', or other status categories relevant to validator lifecycle. |
    | `cnt` | `UInt64` | The number of validators in the given status on the specified date. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/consensus/validators_status/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## withdrawal_credentials_frequency

This view aggregates daily counts of validators categorized by their withdrawal credentials frequency, supporting analysis of validator credential patterns over time.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/consensus/withdrawal_credentials_frequency/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/consensus/withdrawal_credentials_frequency/daily`"
    This view aggregates daily counts of validators categorized by their withdrawal credentials frequency, supporting analysis of validator credential patterns over time.

    Model: `api_consensus_withdrawal_credentials_freq_daily` — table `dbt.api_consensus_withdrawal_credentials_freq_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The specific calendar date for the recorded data, formatted as YYYY-MM-DD. |
    | `label` | `String` | The bin number representing a specific withdrawal credentials frequency category. |
    | `value` | `UInt64` | The count of validators within the specified withdrawal credentials frequency bin for the given date. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/consensus/withdrawal_credentials_frequency/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## withdrawls_cnt

This view provides the latest count of withdrawal events from the consensus API, enabling monitoring of withdrawal activity trends over time.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/consensus/withdrawls_cnt/latest` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/consensus/withdrawls_cnt/latest`"
    This view provides the latest count of withdrawal events from the consensus API, enabling monitoring of withdrawal activity trends over time.

    Model: `api_consensus_info_withdrawls_cnt_latest` — table `dbt.api_consensus_info_withdrawls_cnt_latest`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `value` | `Float64` | The most recent total number of withdrawal events recorded, typically representing a count within a specific period. |
    | `change_pct` | `Float64` | The percentage change in withdrawal count compared to the previous measurement, indicating growth or decline trends. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/consensus/withdrawls_cnt/latest"
    ```
<!-- END AUTO-GENERATED: api-catalog-consensus -->
