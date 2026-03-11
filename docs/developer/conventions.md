---
title: Conventions
description: Naming, tagging, code style, and workflow standards for the Gnosis Analytics platform
---

# Conventions

This page documents the naming conventions, tagging rules, code style, PR workflow, and testing standards used across the Gnosis Analytics platform. Following these conventions ensures consistency and enables the metadata-driven architecture to function correctly.

## Naming Conventions

### Model Names

All dbt model names use `snake_case` and follow a structured pattern:

```
{layer}_{module}_{entity}_{granularity}
```

| Component | Convention | Examples |
|-----------|-----------|----------|
| Layer prefix | Required, one of `stg_`, `int_`, `fct_`, `api_` | `stg_`, `int_`, `fct_`, `api_` |
| Module | Required, lowercase module name | `execution`, `consensus`, `p2p`, `bridges` |
| Entity | Required, descriptive noun(s) | `blocks`, `validators`, `token_transfers` |
| Granularity | Optional, time aggregation | `daily`, `weekly`, `monthly` |

**Staging models** use a double underscore to separate source from table:

```
stg_{source}__{table}
```

Examples: `stg_execution__blocks`, `stg_consensus__attestations`, `stg_p2p__visits`

### File Names

SQL model files match their model name exactly:

```
int_execution_blocks_clients_version_daily.sql
api_consensus_blob_commitments_daily.sql
stg_execution__blocks.sql
```

### Column Names

All column names use `snake_case`:

| Convention | Example | Avoid |
|-----------|---------|-------|
| Lowercase snake_case | `block_number` | `blockNumber`, `BlockNumber` |
| Descriptive names | `total_gas_used` | `tgu`, `gas` |
| Date columns named `date` | `date` | `dt`, `day`, `timestamp` (for daily aggregations) |
| Boolean prefixes: `is_`, `has_` | `is_active`, `has_blobs` | `active`, `blobs_exist` |
| Count suffixes: `_count` | `transaction_count` | `num_transactions`, `txns` |
| Metric naming: specific | `avg_gas_price` | `gas_price` (ambiguous -- avg? max? latest?) |

### Database and Schema Names

| Component | Convention | Examples |
|-----------|-----------|----------|
| Database names | `snake_case` | `execution`, `consensus`, `crawlers_data` |
| Table names | Match model name | `int_execution_blocks_clients_version_daily` |
| No prefixes on raw tables | Source tables as-is | `blocks`, `transactions`, `visits` |

## Tags

Tags control API endpoint generation, access tiers, URL routing, and selective dbt runs.

### Required Tags for API Models

Every API-facing model must have these tags:

| Tag | Purpose | Format |
|-----|---------|--------|
| `production` | Marks model for API exposure | Literal string |
| Category | URL prefix and Swagger group | Lowercase: `consensus`, `execution`, `bridges`, `p2p`, `esg`, `contracts`, `financial` |
| `api:{name}` | Resource name in URL path | Lowercase with underscores: `api:blob_commitments`, `api:token_balances` |

### Optional Tags

| Tag | Purpose | Format | Default |
|-----|---------|--------|---------|
| `tier0` - `tier3` | Access control level | Literal: `tier0`, `tier1`, `tier2`, `tier3` | `tier0` |
| `granularity:{period}` | URL suffix for time dimension | `granularity:daily`, `granularity:latest`, `granularity:weekly` | No suffix |

### Tag Ordering

While tag order does not affect functionality, maintain a consistent ordering for readability:

```sql
tags=[
    'production',           -- 1. Production flag
    'consensus',            -- 2. Category
    'tier1',                -- 3. Access tier
    'api:blob_commitments', -- 4. Resource name
    'granularity:daily'     -- 5. Granularity
]
```

### Tags for Non-API Models

Intermediate and staging models do not need `production` or `api:*` tags. Use the module name as a tag for selective runs:

```sql
-- Intermediate model
{{ config(
    materialized='incremental',
    tags=['consensus']
) }}
```

### System Tags (Filtered from URL)

These tags are silently ignored when constructing API URLs and Swagger groupings:

`production`, `view`, `table`, `incremental`, `staging`, `intermediate`

## Code Style

### SQL Formatting

Follow these SQL formatting rules for consistency across the dbt project:

**Keywords:** Use uppercase SQL keywords.

```sql
-- Good
SELECT date, count() AS transaction_count
FROM {{ ref('stg_execution__transactions') }}
WHERE date >= '2024-01-01'
GROUP BY date

-- Avoid
select date, count() as transaction_count
from {{ ref('stg_execution__transactions') }}
where date >= '2024-01-01'
group by date
```

**Indentation:** Use 4 spaces (no tabs).

**Column lists:** One column per line for queries with more than 3 columns:

```sql
SELECT
    date,
    client_name,
    client_version,
    count() AS block_count,
    sum(gas_used) AS total_gas_used,
    avg(gas_used) AS avg_gas_used
FROM {{ ref('stg_execution__blocks') }}
```

**Trailing commas:** Use trailing commas on column lists for cleaner diffs:

```sql
SELECT
    date,
    block_count,
    total_gas_used,  -- trailing comma
FROM ...
```

### CTEs (Common Table Expressions)

Use CTEs to break complex queries into readable, named steps. Prefer CTEs over subqueries.

```sql
WITH daily_blocks AS (
    SELECT
        toDate(block_timestamp) AS date,
        count() AS block_count,
        sum(gas_used) AS total_gas
    FROM {{ ref('stg_execution__blocks') }}
    GROUP BY date
),

daily_transactions AS (
    SELECT
        toDate(block_timestamp) AS date,
        count() AS tx_count,
        countDistinct(from_address) AS unique_senders
    FROM {{ ref('stg_execution__transactions') }}
    GROUP BY date
)

SELECT
    b.date,
    b.block_count,
    b.total_gas,
    t.tx_count,
    t.unique_senders
FROM daily_blocks AS b
LEFT JOIN daily_transactions AS t ON b.date = t.date
```

### Jinja Usage

**Ref and source:** Always use `{{ ref() }}` and `{{ source() }}` for model references. Never hardcode table names.

```sql
-- Good
FROM {{ ref('stg_execution__blocks') }}
FROM {{ source('execution', 'blocks') }}

-- Bad
FROM dbt.stg_execution__blocks
FROM execution.blocks
```

**Config blocks:** Place the `config()` block at the top of every model file:

```sql
{{
    config(
        materialized='incremental',
        incremental_strategy='delete+insert',
        engine='ReplacingMergeTree()',
        order_by='(date, client_name)',
        unique_key='(date, client_name)',
        partition_by='toStartOfMonth(date)',
        tags=['execution']
    )
}}
```

**Macros:** Use the project's custom macros for common patterns:

```sql
-- Incremental filter macro
{{ apply_monthly_incremental_filter('block_timestamp', 'date') }}
```

## PR Workflow

### Branch Naming

Use descriptive branch names with a prefix indicating the type of change:

| Prefix | Use Case | Example |
|--------|----------|---------|
| `feat/` | New feature or model | `feat/add-blob-commitments-daily` |
| `fix/` | Bug fix | `fix/attestation-rate-null-handling` |
| `refactor/` | Code improvement | `refactor/execution-staging-models` |
| `docs/` | Documentation only | `docs/update-consensus-schema` |
| `chore/` | Maintenance task | `chore/update-dbt-version` |

### Commit Messages

Write clear, concise commit messages:

```
feat: add daily blob commitment model for consensus module

- Create int_consensus_blob_commitments_daily with delete+insert strategy
- Add api_consensus_blob_commitments_daily with tier1 access
- Add meta.api config with date range filters and pagination
- Add schema.yml with column descriptions and tests
```

### Pull Request Structure

Include in your PR:

1. **Description** -- What the change does and why
2. **Endpoint details** (for API models) -- URL path, access tier, available filters
3. **Sample output** -- Results from `dbt show`
4. **Testing** -- Confirmation that `dbt build` and `dbt test` pass
5. **Dependencies** -- Any upstream model changes required

### Review Process

All PRs require at least one code review before merging. Reviewers check:

- [ ] Model follows naming conventions
- [ ] Correct layer and module placement
- [ ] Appropriate materialization strategy
- [ ] `schema.yml` with descriptions and tests
- [ ] `meta.api` configuration is valid (for API models)
- [ ] SQL is well-formatted and uses CTEs appropriately
- [ ] No hardcoded table references (uses `ref()` and `source()`)
- [ ] Incremental models use `apply_monthly_incremental_filter`

## Testing Standards

### Required Tests

Every model must have at minimum:

| Test | Applied To | Purpose |
|------|-----------|---------|
| `not_null` | Primary key columns, date columns | Ensure no missing keys |
| `unique` | Date column in daily aggregations | Ensure no duplicate dates |

### Recommended Tests

| Test | Applied To | Purpose |
|------|-----------|---------|
| `accepted_values` | Status/type columns | Validate enumerated values |
| `relationships` | Foreign key columns | Ensure referential integrity |
| Custom data tests | Business logic | Validate invariants (e.g., no future dates) |

### CI Checks

The CI pipeline runs the following checks on every PR:

1. **`dbt compile`** -- Validates SQL syntax and Jinja rendering
2. **`dbt run`** -- Builds all changed models and their dependencies
3. **`dbt test`** -- Runs all schema and data tests
4. **`dbt docs generate`** -- Ensures documentation compiles

All checks must pass before a PR can be merged.

## Documentation Standards

### schema.yml Requirements

Every model needs a `schema.yml` entry in the same directory containing:

1. **Model description** -- Business purpose and data contents
2. **Column descriptions** -- Human-readable description for every column
3. **Data types** -- ClickHouse data type for each column
4. **Tests** -- At minimum `not_null` on key columns

```yaml
version: 2

models:
  - name: int_consensus_blob_commitments_daily
    description: >
      Daily aggregation of blob commitments on the Gnosis Chain consensus layer.
      Each row represents one calendar day with blob count, size, and gas metrics.
    columns:
      - name: date
        description: Calendar date (UTC)
        data_type: Date
        tests:
          - not_null
          - unique
      - name: total_blob_commitments
        description: Total number of blob commitments submitted on this date
        data_type: UInt64
        tests:
          - not_null
```

### Source Documentation

Source tables should be documented in a `sources.yml` file:

```yaml
version: 2

sources:
  - name: execution
    database: execution
    description: Raw execution layer data from cryo-indexer
    tables:
      - name: blocks
        description: Execution layer blocks with header information
        columns:
          - name: block_number
            description: Block height
          - name: block_timestamp
            description: Block timestamp (UTC)
```

## Next Steps

- [Adding dbt Models](add-model.md) -- Apply these conventions when creating new models
- [Adding API Endpoints](add-endpoint.md) -- Endpoint-specific conventions
- [meta.api Contract](meta-api-contract.md) -- Full metadata specification
