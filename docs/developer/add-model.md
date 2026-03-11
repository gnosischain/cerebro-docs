---
title: Adding dbt Models
description: Guide to creating new dbt models in the dbt-cerebro project
---

# Adding dbt Models

All analytics transformations in the Gnosis Analytics platform happen in **dbt-cerebro**, a dbt project containing approximately 400 SQL models. This guide covers everything you need to create new models: naming conventions, layer selection, materialization strategies, testing, and the PR workflow.

## Naming Convention

Every model name follows a structured pattern:

```
{layer}_{module}_{entity}_{granularity}
```

| Segment | Description | Examples |
|---------|-------------|----------|
| `layer` | Processing layer prefix | `stg`, `int`, `fct`, `api` |
| `module` | Domain module | `execution`, `consensus`, `p2p`, `bridges`, `esg`, `contracts`, `probelab`, `crawlers` |
| `entity` | What the model represents | `blocks`, `transactions`, `validators`, `peers`, `transfers` |
| `granularity` | Time aggregation level (optional) | `daily`, `weekly`, `monthly` |

**Examples:**

| Model Name | Layer | Module | Entity | Granularity |
|------------|-------|--------|--------|-------------|
| `stg_execution__blocks` | Staging | Execution | Blocks | -- |
| `int_execution_blocks_clients_version_daily` | Intermediate | Execution | Block clients | Daily |
| `fct_consensus_attestation_rates` | Facts | Consensus | Attestation rates | -- |
| `api_p2p_client_distribution_daily` | API | P2P | Client distribution | Daily |

!!! note "Staging model naming"
    Staging models use a double underscore `__` to separate the source name from the table name: `stg_{source}__{table}`. This distinguishes the source system boundary from the rest of the name.

## Model Layers

Models are organized into four layers, each with a specific purpose and materialization strategy. Data flows from staging through to the API layer.

```
Source Tables --> stg_* (Views) --> int_* (Incremental) --> fct_* (Views) --> api_* (Views)
```

### Staging Layer (`stg_*`)

Staging models provide a clean interface over raw source tables. They apply minimal transformations: type casting, column renaming, and format standardization. No business logic belongs in this layer.

| Property | Value |
|----------|-------|
| **Materialization** | `view` |
| **Purpose** | Clean raw data, normalize types and formats |
| **References** | `source()` only |
| **Ratio** | 1:1 with source tables |

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

### Intermediate Layer (`int_*`)

Intermediate models contain the heavy transformation logic: joins, aggregations, window functions, and business calculations. This layer does the heavy lifting and produces the datasets that downstream layers reference.

| Property | Value |
|----------|-------|
| **Materialization** | `incremental` (table) |
| **Purpose** | Business logic, joins, aggregations |
| **References** | `stg_*` and other `int_*` models |
| **Strategy** | `delete+insert` with monthly partitioning |

```sql
-- models/consensus/intermediate/int_consensus_attestation_participation_daily.sql
{{
    config(
        materialized='incremental',
        incremental_strategy='delete+insert',
        engine='ReplacingMergeTree()',
        order_by='(date)',
        unique_key='(date)',
        partition_by='toStartOfMonth(date)'
    )
}}

SELECT
    toDate(slot_timestamp) AS date,
    countIf(included = true) AS included_attestations,
    count() AS total_attestations,
    round(countIf(included = true) / count() * 100, 2) AS participation_rate
FROM {{ ref('stg_consensus__attestations') }}

{{ apply_monthly_incremental_filter('slot_timestamp', 'date') }}

GROUP BY date
```

### Facts Layer (`fct_*`)

Fact models produce business-ready metrics and KPIs. They combine intermediate models and apply final calculations like percentages, rankings, or rolling averages.

| Property | Value |
|----------|-------|
| **Materialization** | `view` |
| **Purpose** | Business-ready metrics, calculated KPIs |
| **References** | `int_*` models |

```sql
-- models/consensus/marts/fct_consensus_attestation_rates.sql
{{ config(materialized='view') }}

SELECT
    date,
    included_attestations,
    total_attestations,
    participation_rate,
    avg(participation_rate) OVER (
        ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS participation_rate_7d_avg
FROM {{ ref('int_consensus_attestation_participation_daily') }}
```

### API Layer (`api_*`)

API models are the final presentation layer designed for consumption by the REST API. They project a flat, denormalized structure optimized for JSON serialization. These models include the `production` and `api:*` tags that trigger auto-discovery by the API server.

| Property | Value |
|----------|-------|
| **Materialization** | `view` |
| **Purpose** | REST API endpoint data |
| **References** | `fct_*` and `int_*` models |
| **Tags** | `production`, `api:*`, category, optional tier and granularity |

```sql
-- models/consensus/marts/api_consensus_attestation_rates_daily.sql
{{
    config(
        materialized='view',
        tags=['production', 'consensus', 'tier1', 'api:attestation_rates', 'granularity:daily'],
        meta={
            "api": {
                "methods": ["GET"],
                "allow_unfiltered": false,
                "parameters": [
                    {"name": "start_date", "column": "date", "operator": ">=", "type": "date"},
                    {"name": "end_date", "column": "date", "operator": "<=", "type": "date"}
                ],
                "pagination": {"enabled": true, "default_limit": 100, "max_limit": 5000},
                "sort": [{"column": "date", "direction": "DESC"}]
            }
        }
    )
}}

SELECT
    date,
    included_attestations,
    total_attestations,
    participation_rate,
    participation_rate_7d_avg
FROM {{ ref('fct_consensus_attestation_rates') }}
```

## Layer Dependencies

Models must only reference models in their own layer or the layer directly above:

| Model Layer | Can Reference |
|-------------|---------------|
| `stg_*` | `source()` only |
| `int_*` | `stg_*` and other `int_*` models |
| `fct_*` | `int_*` models |
| `api_*` | `fct_*` and `int_*` models |

!!! warning "No skip-layer references"
    An `api_*` model should not reference a `stg_*` model directly. If you need staging data in the API layer, create an intermediate model to bridge the gap. This keeps the dependency graph clean and ensures data passes through appropriate transformation steps.

## Module Placement

Place your model files in the correct module directory:

```
models/
├── execution/           # Blocks, transactions, gas, contracts, tokens
│   ├── staging/
│   ├── intermediate/
│   └── marts/
├── consensus/           # Validators, attestations, proposals, blobs
│   ├── staging/
│   ├── intermediate/
│   └── marts/
├── bridges/             # Cross-chain bridge transfers and volume
│   ├── staging/
│   ├── intermediate/
│   └── marts/
├── p2p/                 # Peer discovery, client diversity, geography
│   ├── staging/
│   ├── intermediate/
│   └── marts/
├── contracts/           # Decoded smart contract data, protocol-specific
│   └── {protocol}/      # One subdirectory per protocol
├── ESG/                 # Energy, carbon, sustainability metrics
│   ├── staging/
│   ├── intermediate/
│   └── marts/
├── probelab/            # ProbeLab network performance metrics
│   └── ...
└── crawlers/            # Crawler data transformations
    └── ...
```

Choose the module based on the data domain. If your model bridges multiple domains (e.g., validator data with geographic enrichment), place it in the primary domain and reference models from other modules.

## Incremental Strategy

Most intermediate models use ClickHouse's incremental materialization with the `delete+insert` strategy. This is the recommended approach for all time-series data.

### Configuration Template

```sql
{{
    config(
        materialized='incremental',
        incremental_strategy='delete+insert',
        engine='ReplacingMergeTree()',
        order_by='(date, dimension_column)',
        unique_key='(date, dimension_column)',
        partition_by='toStartOfMonth(date)'
    )
}}

SELECT
    toDate(timestamp_column) AS date,
    dimension_column,
    count() AS metric_value
FROM {{ ref('stg_source__table') }}

{{ apply_monthly_incremental_filter('timestamp_column', 'date') }}

GROUP BY date, dimension_column
```

### How Incremental Processing Works

The `apply_monthly_incremental_filter` macro limits processing to only the months containing new data:

1. **First run (full refresh)**: All historical data is processed
2. **Incremental runs**: Only months where new source data exists are reprocessed
3. **Delete+Insert**: Existing rows in affected partitions are deleted, then fresh rows are inserted

This approach is:

- **Idempotent** -- Safe to re-run without creating duplicates
- **Efficient** -- Only processes changed partitions, not the entire table
- **Correct** -- Handles late-arriving data by reprocessing entire monthly partitions

### Key Configuration Fields

| Field | Purpose | Example |
|-------|---------|---------|
| `engine` | ClickHouse table engine | `ReplacingMergeTree()` |
| `order_by` | Primary sort key (must match `unique_key`) | `(date, client_name)` |
| `unique_key` | Deduplication key | `(date, client_name)` |
| `partition_by` | Partitioning expression | `toStartOfMonth(date)` |

!!! tip "Always use `ReplacingMergeTree`"
    Even though `delete+insert` handles deduplication at the dbt level, `ReplacingMergeTree` provides an additional safety net by deduplicating rows during ClickHouse background merges. This guards against edge cases where a run is interrupted mid-partition.

## Testing

### Schema Tests

Add tests in the `schema.yml` file alongside your model:

```yaml
version: 2

models:
  - name: int_consensus_attestation_participation_daily
    description: Daily attestation participation rates
    columns:
      - name: date
        description: Calendar date (UTC)
        data_type: Date
        tests:
          - not_null
          - unique
      - name: participation_rate
        description: Percentage of attestations included in blocks
        data_type: Float64
        tests:
          - not_null
      - name: total_attestations
        description: Total number of attestations expected
        data_type: UInt64
        tests:
          - not_null
```

### Common Test Types

| Test | Purpose | Example |
|------|---------|---------|
| `not_null` | Column must not contain NULL values | Primary keys, dates, metrics |
| `unique` | Column values must be unique | Date columns in daily aggregations |
| `accepted_values` | Column must contain only specified values | Status fields, categories |
| `relationships` | Foreign key integrity | `ref()` columns linking to dimension tables |

### Data Tests

For more complex validation, create SQL-based data tests in `tests/`:

```sql
-- tests/assert_no_future_dates.sql
SELECT date
FROM {{ ref('int_consensus_attestation_participation_daily') }}
WHERE date > today()
```

This test passes if the query returns zero rows.

### Running Tests

```bash
# Test a specific model
dbt test --select int_consensus_attestation_participation_daily

# Test all models in a module
dbt test --select consensus

# Test with upstream dependencies
dbt test --select +api_consensus_attestation_rates_daily
```

## Documentation

Every model must have a `schema.yml` entry with:

1. **Model description** -- What data this model contains and its business purpose
2. **Column descriptions** -- Human-readable description for every column
3. **Data types** -- ClickHouse data type for each column
4. **Tests** -- At minimum `not_null` on primary key columns

```yaml
version: 2

models:
  - name: api_consensus_attestation_rates_daily
    description: >
      Daily attestation participation rates for the Gnosis Chain consensus layer.
      Includes raw counts and rolling averages for trend analysis.
    columns:
      - name: date
        description: Calendar date (UTC)
        data_type: Date
        tests:
          - not_null
      - name: included_attestations
        description: Number of attestations successfully included in blocks
        data_type: UInt64
      - name: total_attestations
        description: Total expected attestations based on active validator count
        data_type: UInt64
      - name: participation_rate
        description: Percentage of attestations included (0-100)
        data_type: Float64
      - name: participation_rate_7d_avg
        description: 7-day rolling average of participation rate
        data_type: Float64
```

!!! tip "Use dbt-schema-gen"
    The `dbt-schema-gen` tool can automatically generate `schema.yml` files using LLM analysis of your SQL models. Run it against your new model to get a starting point, then refine the descriptions manually.

## Tags

### Required Tags for API Models

| Tag | Purpose |
|-----|---------|
| `production` | Marks the model for API exposure |
| `api:{resource_name}` | Defines the URL resource segment |
| Category tag (e.g., `consensus`) | URL prefix and Swagger UI grouping |

### Optional Tags

| Tag | Purpose | Default |
|-----|---------|---------|
| `tier0` through `tier3` | Access control level | `tier0` |
| `granularity:{period}` | URL suffix for time dimension | None |

### Tags for Non-API Models

Intermediate and staging models do not need `production` or `api:*` tags. However, adding the module name as a tag helps with selective dbt runs:

```sql
{{ config(
    materialized='incremental',
    tags=['consensus']
) }}
```

This allows running all consensus models with `dbt run --select tag:consensus`.

## PR Workflow

### 1. Create a Branch

```bash
git checkout -b feat/add-attestation-rates-model
```

### 2. Add Your Model Files

- SQL model file in the appropriate `models/{module}/{layer}/` directory
- `schema.yml` entry with descriptions and tests

### 3. Test Locally

```bash
# Compile to check SQL syntax
dbt compile --select api_consensus_attestation_rates_daily

# Run the model
dbt run --select +api_consensus_attestation_rates_daily

# Run tests
dbt test --select api_consensus_attestation_rates_daily

# Preview results
dbt show --select api_consensus_attestation_rates_daily --limit 10

# Generate documentation
dbt docs generate
```

### 4. Submit a Pull Request

Include in your PR description:

- What data the model exposes and its business purpose
- The resulting API endpoint path and access tier
- Sample query results (output from `dbt show`)
- Any upstream model dependencies that were added or modified

### 5. After Merge

Once your PR is merged:

1. CI runs `dbt build` to deploy the model to ClickHouse
2. An updated `manifest.json` is published
3. The API auto-discovers the new endpoint within 5 minutes
4. The endpoint appears in the Swagger UI documentation

## Next Steps

- [Adding API Endpoints](add-endpoint.md) -- Focus specifically on the `meta.api` configuration
- [meta.api Contract](meta-api-contract.md) -- Full specification for API metadata
- [Model Layers](../data-pipeline/transformation/model-layers.md) -- Detailed layer reference
- [Conventions](conventions.md) -- Naming and code style standards
