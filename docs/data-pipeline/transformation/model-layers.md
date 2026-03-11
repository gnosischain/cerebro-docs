# Model Layers

dbt-cerebro organizes models into four layers, each with a distinct purpose, naming convention, and materialization strategy. Data flows from raw source tables through each layer in sequence.

## Layer Overview

```
Raw Source Tables (execution.blocks, consensus.blocks, nebula.visits, ...)
        |
        v
    stg_*  (Staging)        -- Thin views, type casting, column renaming
        |
        v
    int_*  (Intermediate)   -- Heavy transformations, joins, aggregations
        |
        v
    fct_*  (Facts)          -- Business-ready metrics and KPIs
        |
        v
    api_*  (API)            -- Optimized for REST API consumption
```

## Layer Reference

| Layer | Prefix | Materialization | Purpose | Typical Row Count |
|-------|--------|-----------------|---------|-------------------|
| Staging | `stg_` | View | Light cleanup of raw source data | Same as source |
| Intermediate | `int_` | Incremental table | Business logic, joins, aggregations | Varies |
| Facts | `fct_` | View | Business-ready metrics | Aggregated |
| API | `api_` | View | REST API endpoint data | Aggregated |

## Staging Layer (`stg_*`)

### Purpose

Staging models provide a clean interface over raw source tables. They apply minimal transformations: type casting, column renaming, and format standardization. No business logic belongs here.

### Characteristics

- **1:1 relationship** with source tables -- one staging model per source table
- **Materialized as views** -- no additional storage cost
- **No business logic** -- only data cleanup operations
- **Source isolation** -- downstream models reference staging models, never raw tables directly

### Naming Convention

```
stg_{source}__{table}
```

The double underscore `__` separates the source system name from the table name.

### Example

```sql
-- models/execution/staging/stg_execution__blocks.sql
{{ config(materialized='view') }}

SELECT
    block_number,
    CONCAT('0x', author) AS author,
    block_timestamp,
    gas_used,
    gas_limit,
    base_fee_per_gas
FROM {{ source('execution', 'blocks') }}
```

### Examples by Module

| Model | Source Table | Key Transformations |
|-------|-------------|---------------------|
| `stg_execution__blocks` | `execution.blocks` | Hex address formatting |
| `stg_execution__transactions` | `execution.transactions` | Type casting, address normalization |
| `stg_consensus__blocks` | `consensus.blocks` | Fork version extraction |
| `stg_p2p__visits` | `nebula.visits` | JSON field extraction from `peer_properties` |

## Intermediate Layer (`int_*`)

### Purpose

Intermediate models contain the heavy transformation logic: complex joins, aggregations, window functions, and business calculations. This is where raw data becomes meaningful analytics.

### Characteristics

- **Materialized as incremental tables** using `delete+insert` strategy
- **Partitioned by month** with `toStartOfMonth()` for efficient processing
- **Uses `ReplacingMergeTree`** engine for deduplication
- **Contains business logic** -- calculations, joins, classifications
- **Largest processing cost** -- these models do the heavy lifting

### Naming Convention

```
int_{domain}_{metric}_{grain}
```

Where `{grain}` indicates the time granularity (e.g., `daily`, `weekly`, `monthly`).

### Example

```sql
-- models/execution/intermediate/int_execution_blocks_clients_version_daily.sql
{{
    config(
        materialized='incremental',
        incremental_strategy='delete+insert',
        engine='ReplacingMergeTree()',
        order_by='(date, client_name, client_version)',
        unique_key='(date, client_name, client_version)',
        partition_by='toStartOfMonth(date)'
    )
}}

SELECT
    toDate(block_timestamp) AS date,
    extractClientName(extra_data) AS client_name,
    extractClientVersion(extra_data) AS client_version,
    count() AS block_count,
    sum(gas_used) AS total_gas_used
FROM {{ ref('stg_execution__blocks') }}

{{ apply_monthly_incremental_filter('block_timestamp', 'date') }}

GROUP BY date, client_name, client_version
```

### Incremental Processing Details

The `apply_monthly_incremental_filter` macro limits processing to only the months containing new data. On the first run (full refresh), all data is processed. On subsequent runs, only months where new source data exists are reprocessed.

The `delete+insert` strategy works as follows:

1. Identify which monthly partitions have new source data
2. Delete existing rows in those partitions from the target table
3. Insert freshly computed rows for those partitions

This approach is idempotent and handles late-arriving data correctly.

### Examples by Module

| Model | Description | Grain |
|-------|-------------|-------|
| `int_execution_blocks_clients_version_daily` | Block proposer client distribution | Daily |
| `int_execution_transactions_gas_daily` | Gas usage statistics | Daily |
| `int_consensus_validators_active_daily` | Active validator counts | Daily |
| `int_consensus_attestation_participation_daily` | Attestation rates | Daily |
| `int_p2p_peers_geo_daily` | Peer geographic distribution | Daily |
| `int_bridges_transfers_daily` | Cross-chain bridge volume | Daily |

## Facts Layer (`fct_*`)

### Purpose

Fact models produce business-ready metrics and KPIs. They typically combine multiple intermediate models and apply final business transformations like percentage calculations, rankings, or rolling averages.

### Characteristics

- **Materialized as views** -- read from pre-computed intermediate tables
- **Business-ready** -- can be consumed directly by analysts
- **Contains calculated metrics** -- ratios, percentages, rankings
- **Optimized for querying** -- clean column names, pre-computed aggregations

### Naming Convention

```
fct_{domain}_{metric}_{grain}
```

### Example

```sql
-- models/execution/marts/fct_execution_gas_daily.sql
{{ config(materialized='view') }}

SELECT
    date,
    total_gas_used,
    avg_gas_price,
    total_gas_used * avg_gas_price AS total_fees,
    block_count,
    total_gas_used / block_count AS avg_gas_per_block
FROM {{ ref('int_execution_transactions_gas_daily') }}
```

## API Layer (`api_*`)

### Purpose

API models are the final presentation layer, specifically designed for consumption by the REST API (`cerebro-api`). They ensure consistent structure, naming, and response format across all endpoints.

### Characteristics

- **Materialized as views** -- real-time data without additional storage
- **Simplified structure** -- flat, denormalized for easy JSON serialization
- **Consistent naming** -- follows API endpoint naming conventions
- **Read-optimized** -- designed for fast query execution
- **Auto-discovered** -- `cerebro-api` scans the dbt manifest for `api_*` models and automatically creates HTTP endpoints

### Naming Convention

```
api_{domain}_{metric}_{grain}
```

### Example

```sql
-- models/execution/marts/api_execution_transactions_daily.sql
{{ config(materialized='view') }}

SELECT
    date,
    transaction_count,
    unique_senders,
    unique_receivers,
    total_value_wei,
    avg_gas_price
FROM {{ ref('fct_execution_transactions_daily') }}
ORDER BY date DESC
```

## Layer Dependencies

Models must only reference models in the same layer or the layer directly above:

| Model Layer | Can Reference |
|-------------|---------------|
| `stg_*` | `source()` only |
| `int_*` | `stg_*` and other `int_*` models |
| `fct_*` | `int_*` models |
| `api_*` | `fct_*` and `int_*` models |

This constraint ensures a clean dependency graph and prevents circular references.
