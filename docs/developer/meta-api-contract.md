---
title: meta.api Contract
description: Full specification for the metadata contract between dbt models and the API
---

# meta.api Contract

The `meta.api` block in a dbt model's configuration is the contract between dbt-cerebro and cerebro-api. It defines how the API endpoint behaves: which HTTP methods are allowed, what filters clients can use, how pagination works, and the sort order of results.

This page is the canonical reference for all `meta.api` fields and validation rules.

## Overview

The `meta.api` object is placed inside the dbt model's `config()` block under the `meta` key:

```sql
{{
    config(
        materialized='view',
        tags=['production', 'consensus', 'api:blob_commitments', 'granularity:daily'],
        meta={
            "api": {
                "methods": ["GET", "POST"],
                "allow_unfiltered": false,
                "require_any_of": [],
                "parameters": [...],
                "pagination": {...},
                "sort": [...]
            }
        }
    )
}}
```

!!! info "Legacy endpoints"
    Models without a `meta.api` block are treated as legacy endpoints. They support GET only, accept no query parameters, have no pagination or sorting, and return the full result set. All new models should include `meta.api`.

## Top-Level Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `methods` | list of strings | `["GET"]` | Allowed HTTP methods. Accepted values: `GET`, `POST`. |
| `allow_unfiltered` | boolean | `false` | When `true`, clients can call the endpoint with no business filters. When `false`, at least one declared parameter must be provided. |
| `require_any_of` | list of strings | `[]` | Parameter names where at least one must be present in the request. Each name must match a declared parameter. |
| `parameters` | list of objects | `[]` | Declared filter parameters. See [Parameter Fields](#parameter-fields). |
| `pagination` | object | Disabled | Pagination configuration. See [Pagination Fields](#pagination-fields). |
| `sort` | list of objects | `[]` | Server-side sort order. See [Sort Fields](#sort-fields). |

## Parameter Fields

Each entry in the `parameters` list declares one filter that clients can use.

| Key | Required | Type | Description |
|-----|----------|------|-------------|
| `name` | Yes | string | API field name used by clients in query strings (GET) or JSON bodies (POST). Must be unique within the endpoint. |
| `column` | Yes | string | The column in the model's final `SELECT` projection that this parameter filters on. Must exist in the model's columns. |
| `operator` | Yes | string | SQL comparison operator. One of: `=`, `>=`, `<=`, `ILIKE`, `IN`. |
| `type` | Yes | string | Parameter data type. One of: `string`, `date`, `string_list`. |
| `description` | No | string | Human-readable description displayed in OpenAPI/Swagger documentation. |
| `case` | No | string | Case normalization applied to input values before filtering. One of: `lower`, `upper`. Only valid for `string` and `string_list` types. |
| `max_items` | No | integer | Maximum number of values allowed in a list parameter. Only valid for `string_list` type. Must be a positive integer. |

### Parameter Types

=== "string"

    A single string value. Used with operators `=` and `ILIKE`.

    **GET:** `?symbol=GNO`

    **POST:** `"symbol": "GNO"`

=== "date"

    A date value in `YYYY-MM-DD` format. Used with operators `>=` and `<=` for range queries.

    **GET:** `?start_date=2024-01-01`

    **POST:** `"start_date": "2024-01-01"`

=== "string_list"

    A list of string values. Used with the `IN` operator for multi-value matching.

    **GET (repeated):** `?address=0x1&address=0x2`

    **GET (CSV):** `?address=0x1,0x2`

    **POST:** `"address": ["0x1", "0x2"]`

### Operators

| Operator | SQL Equivalent | Compatible Types | Use Case |
|----------|---------------|------------------|----------|
| `=` | `column = value` | `string` | Exact match on a single value |
| `>=` | `column >= value` | `date` | Start of a date range (inclusive) |
| `<=` | `column <= value` | `date` | End of a date range (inclusive) |
| `ILIKE` | `column ILIKE value` | `string` | Case-insensitive pattern matching (supports `%` wildcards) |
| `IN` | `column IN (values)` | `string_list` | Match any value in a list |

!!! warning "Operator-type constraints"
    The `IN` operator can only be used with `string_list` type. Attempting to use `IN` with `string` or `date` produces a validation error at manifest load time.

### Case Normalization

When a parameter declares a `case` option, input values are normalized before filtering:

- `"case": "lower"` -- Converts `0xABC` to `0xabc`
- `"case": "upper"` -- Converts `abc` to `ABC`

This ensures consistent matching regardless of how clients format their input. The `case` option applies to both `string` and `string_list` types.

### Max Items

The `max_items` field limits how many values a `string_list` parameter can accept. If a client provides more values than allowed, the API returns a 400 error:

```json
{"detail": "Parameter 'address' allows at most 200 values."}
```

## Pagination Fields

The `pagination` object controls whether an endpoint supports `limit` and `offset` parameters.

| Key | Required | Type | Description |
|-----|----------|------|-------------|
| `enabled` | Yes | boolean | Must be `true` to enable pagination. When `false` or omitted, `limit` and `offset` parameters are not accepted. |
| `default_limit` | Yes (when enabled) | integer | Default number of rows returned when the client omits `limit`. Must be a positive integer. |
| `max_limit` | Yes (when enabled) | integer | Hard upper bound for the `limit` parameter. Requests exceeding this value receive a 400 error. Must be >= `default_limit`. |

When pagination is enabled, two additional parameters become available to clients:

| Parameter | Type | Description |
|-----------|------|-------------|
| `limit` | integer | Maximum rows to return. Defaults to `default_limit`. Cannot exceed `max_limit`. |
| `offset` | integer | Number of rows to skip. Defaults to `0`. |

!!! warning "Pagination disabled by default"
    If `pagination` is not declared or `enabled` is `false`, passing `limit` or `offset` returns a 400 error: `Unsupported query parameters: limit, offset`.

## Sort Fields

Each entry in the `sort` list defines a column and direction for the server-side `ORDER BY` clause.

| Key | Required | Type | Description |
|-----|----------|------|-------------|
| `column` | Yes | string | Column name that must exist in the model's final `SELECT` projection. |
| `direction` | Yes | string | Sort direction. One of: `ASC`, `DESC`. |

Sort order is fixed per endpoint and cannot be overridden by clients. Multiple sort entries are applied in order (primary sort, secondary sort, etc.).

## Validation Rules

The API validates `meta.api` at manifest load time. Models that fail validation are skipped (not registered as endpoints) and an error is logged. The following rules are enforced:

### Column References

- Every `parameters[].column` must exist in the model's column list
- Every `sort[].column` must exist in the model's column list
- Column names are validated against the dbt manifest's column metadata

### Parameter Constraints

- Parameter `name` values must be unique within a single endpoint
- `IN` operator requires `string_list` type (and vice versa: `string_list` should use `IN`)
- `case` is only valid for `string` and `string_list` types
- `max_items` is only valid for `string_list` type and must be a positive integer
- `require_any_of` entries must reference declared parameter names

### Filter Policy

- If `allow_unfiltered` is `false`, at least one parameter must be declared
- `require_any_of` names must all be present in the `parameters` list

### Pagination Constraints

- `default_limit` must be a positive integer when pagination is enabled
- `max_limit` must be a positive integer when pagination is enabled
- `default_limit` must be less than or equal to `max_limit`

### Method Constraints

- `methods` must be a non-empty list
- Each method must be either `GET` or `POST`
- Duplicate methods are silently deduplicated

## Behavior Differences: Legacy vs Metadata-Driven

| Behavior | Legacy (no `meta.api`) | Metadata-Driven (`meta.api` present) |
|----------|------------------------|--------------------------------------|
| HTTP Methods | GET only | Declared in `methods` |
| Query Filters | None -- any parameter returns 400 | Only declared parameters accepted |
| Pagination | Disabled | Enabled via `pagination` |
| Sort | None (database default) | Explicit `ORDER BY` from `sort` |
| Unfiltered requests | Always allowed | Controlled by `allow_unfiltered` |
| POST support | No | Yes, if `POST` is in `methods` |
| Response | Complete table contents | Filtered, paginated, sorted |

## Complete Examples

### Minimal Metadata-Driven Endpoint

The simplest `meta.api` configuration -- enables the metadata-driven pipeline with no filters and allows unfiltered access:

```sql
{{
    config(
        materialized='view',
        tags=['production', 'consensus', 'tier0', 'api:network_summary', 'granularity:latest'],
        meta={
            "api": {
                "allow_unfiltered": true,
                "pagination": {
                    "enabled": true,
                    "default_limit": 10,
                    "max_limit": 100
                },
                "sort": [
                    {"column": "date", "direction": "DESC"}
                ]
            }
        }
    )
}}

SELECT date, active_validators, participation_rate
FROM {{ ref('int_consensus_network_summary_daily') }}
```

**Result:** `GET /v1/consensus/network_summary/latest` -- Public, paginated, sorted by date descending, no filters required.

### Date Range Filters with Required Filter

```sql
{{
    config(
        materialized='view',
        tags=['production', 'execution', 'tier1', 'api:gas_usage', 'granularity:daily'],
        meta={
            "api": {
                "methods": ["GET"],
                "allow_unfiltered": false,
                "parameters": [
                    {
                        "name": "start_date",
                        "column": "date",
                        "operator": ">=",
                        "type": "date",
                        "description": "Start date (inclusive)"
                    },
                    {
                        "name": "end_date",
                        "column": "date",
                        "operator": "<=",
                        "type": "date",
                        "description": "End date (inclusive)"
                    }
                ],
                "pagination": {
                    "enabled": true,
                    "default_limit": 100,
                    "max_limit": 10000
                },
                "sort": [
                    {"column": "date", "direction": "DESC"}
                ]
            }
        }
    )
}}

SELECT date, total_gas_used, avg_gas_price, transaction_count
FROM {{ ref('int_execution_gas_daily') }}
```

**Result:** `GET /v1/execution/gas_usage/daily` -- Requires at least `start_date` or `end_date`. Returns error if no filters provided.

### Multi-Value Filters with POST Support

```sql
{{
    config(
        materialized='view',
        tags=['production', 'execution', 'tier2', 'api:token_transfers', 'granularity:daily'],
        meta={
            "api": {
                "methods": ["GET", "POST"],
                "allow_unfiltered": false,
                "require_any_of": ["token_address", "from_address", "to_address"],
                "parameters": [
                    {
                        "name": "token_address",
                        "column": "token_address",
                        "operator": "IN",
                        "type": "string_list",
                        "case": "lower",
                        "max_items": 50,
                        "description": "Token contract address(es)"
                    },
                    {
                        "name": "from_address",
                        "column": "from_address",
                        "operator": "IN",
                        "type": "string_list",
                        "case": "lower",
                        "max_items": 200,
                        "description": "Sender address(es)"
                    },
                    {
                        "name": "to_address",
                        "column": "to_address",
                        "operator": "IN",
                        "type": "string_list",
                        "case": "lower",
                        "max_items": 200,
                        "description": "Recipient address(es)"
                    },
                    {
                        "name": "start_date",
                        "column": "date",
                        "operator": ">=",
                        "type": "date"
                    },
                    {
                        "name": "end_date",
                        "column": "date",
                        "operator": "<=",
                        "type": "date"
                    }
                ],
                "pagination": {
                    "enabled": true,
                    "default_limit": 100,
                    "max_limit": 5000
                },
                "sort": [
                    {"column": "date", "direction": "DESC"},
                    {"column": "token_address", "direction": "ASC"}
                ]
            }
        }
    )
}}

SELECT
    date,
    token_address,
    from_address,
    to_address,
    transfer_count,
    total_value
FROM {{ ref('int_execution_token_transfers_daily') }}
```

**Result:**

- `GET /v1/execution/token_transfers/daily` and `POST /v1/execution/token_transfers/daily`
- tier2 access required
- At least one of `token_address`, `from_address`, or `to_address` must be provided
- Addresses are case-normalized to lowercase
- Sorted by date descending, then token address ascending
- Maximum 50 token addresses and 200 sender/recipient addresses per request

### Pattern Matching with ILIKE

```sql
{{
    config(
        materialized='view',
        tags=['production', 'contracts', 'tier1', 'api:verified_contracts'],
        meta={
            "api": {
                "methods": ["GET"],
                "allow_unfiltered": false,
                "parameters": [
                    {
                        "name": "name",
                        "column": "contract_name",
                        "operator": "ILIKE",
                        "type": "string",
                        "description": "Contract name (case-insensitive, supports % wildcards)"
                    },
                    {
                        "name": "address",
                        "column": "contract_address",
                        "operator": "=",
                        "type": "string",
                        "case": "lower",
                        "description": "Exact contract address"
                    }
                ],
                "pagination": {
                    "enabled": true,
                    "default_limit": 50,
                    "max_limit": 500
                },
                "sort": [
                    {"column": "contract_name", "direction": "ASC"}
                ]
            }
        }
    )
}}

SELECT contract_address, contract_name, compiler_version, verified_at
FROM {{ ref('int_contracts_verified') }}
```

**Result:** `GET /v1/contracts/verified_contracts` -- Supports `?name=%uniswap%` for pattern matching and `?address=0x...` for exact lookup.

## Error Responses

When `meta.api` validation rules are violated at request time, the API returns 400 errors:

| Scenario | Error Message |
|----------|---------------|
| Undeclared GET parameter | `Unsupported query parameters: {param_name}` |
| Undeclared POST body field | `Unsupported body fields: {field_name}` |
| No filters when `allow_unfiltered=false` | `At least one business filter is required for this endpoint.` |
| Missing `require_any_of` filter | `At least one of [{names}] is required for this endpoint.` |
| `limit` exceeds `max_limit` | `'limit' must be <= {max_limit}.` |
| `limit`/`offset` without pagination | `Unsupported query parameters: limit, offset` |
| `string_list` exceeds `max_items` | `Parameter '{name}' allows at most {max_items} values.` |
| Query params on POST | `POST endpoints accept filter and pagination fields in JSON body only.` |
| Invalid JSON body | `Request body must be valid JSON.` |
| Legacy endpoint with params | `This endpoint does not declare API parameters. Add meta.api to the dbt model to enable filters or pagination.` |

## Next Steps

- [Adding API Endpoints](add-endpoint.md) -- Step-by-step guide using `meta.api`
- [Filtering & Pagination](../api/filtering.md) -- Client-facing documentation for using filters
- [Error Handling](../api/errors.md) -- Full error response reference
