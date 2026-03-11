---
title: Filtering & Pagination
description: Query parameters, POST bodies, filter operators, data types, pagination, and sort
---

# Filtering & Pagination

Metadata-driven endpoints support filtering, pagination, and sorting as declared in the dbt model's `meta.api` configuration. Only parameters explicitly declared in the model metadata are accepted -- any undeclared parameter returns a 400 error.

## GET vs POST

Endpoints can support GET, POST, or both methods. The method(s) available are declared in the dbt model's `meta.api.methods` field (default: `["GET"]`).

| Aspect | GET | POST |
|--------|-----|------|
| Filters passed via | Query string parameters | JSON request body |
| List values | Repeated params or CSV | JSON arrays |
| Query string allowed | Yes | No (returns 400) |
| Content-Type header | Not required | `application/json` |
| Best for | Simple queries, few parameters | Large filter lists, structured queries |

## GET Requests

Filters are passed as query string parameters. All parameters are optional unless the endpoint's filter policy requires at least one (see [Filter Policy](#filter-policy) below).

```bash
curl "https://api.analytics.gnosis.io/v1/execution/token_balances/daily?symbol=GNO&start_date=2024-01-01&limit=50" \
  -H "accept: application/json" \
  -H "X-API-Key: YOUR_API_KEY"
```

### List Parameters on GET

Parameters of type `string_list` accept values in two interchangeable formats. Both produce identical results and can be mixed freely.

=== "Repeated parameters"

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/token_balances/daily?address=0xabc&address=0xdef&address=0x123" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

=== "CSV notation"

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/token_balances/daily?address=0xabc,0xdef,0x123" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

=== "Mixed (both at once)"

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/token_balances/daily?address=0xabc,0xdef&address=0x123" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

All three examples above resolve to the same filter: `address IN ('0xabc', '0xdef', '0x123')`.

## POST Requests

POST endpoints accept a JSON body containing the same fields declared in the endpoint's metadata. Query string parameters are **not** allowed on POST requests -- passing any query string returns a 400 error.

```bash
curl -X POST "https://api.analytics.gnosis.io/v1/execution/token_balances/daily" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_API_KEY" \
  -d '{
    "symbol": "GNO",
    "address": ["0xabc", "0xdef", "0x123"],
    "start_date": "2024-01-01",
    "end_date": "2024-06-30",
    "limit": 100,
    "offset": 0
  }'
```

!!! tip "When to use POST"
    POST is preferred when:

    - You need to pass large lists of values (e.g., hundreds of addresses)
    - Filter values would create an excessively long URL
    - You prefer structured JSON over query string encoding
    - You are building programmatic integrations and want a consistent request format

### POST Body Rules

- The body must be valid JSON (`Content-Type: application/json`)
- The body must be a JSON object (not an array or scalar)
- An empty body `{}` is valid (subject to the endpoint's filter policy)
- Undeclared fields return a 400 error
- List parameters accept both JSON arrays and single strings

```json
{
  "address": ["0xabc", "0xdef"]
}
```

is equivalent to:

```json
{
  "address": "0xabc,0xdef"
}
```

## Parameter Types

Each declared parameter has a `type` that determines how values are parsed, validated, and used in queries.

| Type | GET Format | POST Format | SQL Behavior |
|------|-----------|-------------|--------------|
| `string` | `?symbol=GNO` | `"symbol": "GNO"` | Single-value comparison (`=`, `ILIKE`) |
| `date` | `?start_date=2024-01-01` | `"start_date": "2024-01-01"` | Date comparison (`>=`, `<=`) |
| `string_list` | `?address=0x1&address=0x2` | `"address": ["0x1", "0x2"]` | Multi-value match (`IN`) |

### `string`

A single text value. Used with the `=` or `ILIKE` operator.

```bash
# Exact match
?symbol=GNO

# Case-insensitive pattern match (ILIKE operator)
?name=gnosis
```

### `date`

A date string in `YYYY-MM-DD` format. Typically paired with `>=` or `<=` operators to define date ranges.

```bash
# All data from January 1, 2024 onward
?start_date=2024-01-01

# Combined date range
?start_date=2024-01-01&end_date=2024-06-30
```

### `string_list`

A list of string values. Always used with the `IN` operator. On GET, accepts repeated parameters and/or CSV. On POST, accepts JSON arrays.

```bash
# GET: repeated params
?address=0xabc&address=0xdef

# GET: CSV
?address=0xabc,0xdef

# POST: JSON array
{"address": ["0xabc", "0xdef"]}
```

## Filter Operators

Each parameter is bound to a fixed SQL operator defined in the dbt model metadata. The operator cannot be changed at query time by the client.

| Operator | SQL Expression | Compatible Types | Description |
|----------|---------------|------------------|-------------|
| `=` | `column = 'value'` | `string`, `date` | Exact match |
| `>=` | `column >= 'value'` | `string`, `date` | Greater than or equal |
| `<=` | `column <= 'value'` | `string`, `date` | Less than or equal |
| `ILIKE` | `column ILIKE '%value%'` | `string` | Case-insensitive substring match with automatic wildcard wrapping |
| `IN` | `column IN ('a', 'b', 'c')` | `string_list` | Match any value in the provided list |

!!! info "ILIKE wildcard behavior"
    When using the `ILIKE` operator, the API automatically wraps the value with `%` wildcards if none are present. So `?name=gnosis` becomes `column ILIKE '%gnosis%'`. If the value already contains `%` characters, they are preserved as-is.

### Operator Examples

```bash
# = (exact match on string)
?symbol=GNO

# >= (date range start)
?start_date=2024-01-01

# <= (date range end)
?end_date=2024-12-31

# ILIKE (case-insensitive search)
?name=uniswap

# IN (match any from list)
?address=0xabc&address=0xdef
```

## Case Normalization

Parameters can declare a `case` option that normalizes input values before filtering:

| Case Mode | Behavior | Example |
|-----------|----------|---------|
| `lower` | Converts value to lowercase before query | `0xABC` becomes `0xabc` |
| `upper` | Converts value to uppercase before query | `gno` becomes `GNO` |

Case normalization applies to both `string` and `string_list` types. When `case` is set, the SQL query also wraps the column in the corresponding function (e.g., `lower(address)`) to ensure a case-insensitive match.

```bash
# With "case": "lower" declared, these are equivalent:
?address=0xAbC123
?address=0xabc123
```

## Max Items

`string_list` parameters can declare a `max_items` limit to cap the number of values per request. Exceeding the limit returns a 400 error:

```json
{"detail": "Parameter 'address' allows at most 200 values."}
```

This safeguard prevents excessively large `IN` clauses that could degrade database performance.

## Pagination

Pagination is enabled per-endpoint via the `meta.api.pagination` configuration. When enabled, two additional parameters become available: `limit` and `offset`.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `limit` | integer | Endpoint-specific `default_limit` | Maximum number of rows to return (min: 1) |
| `offset` | integer | `0` | Number of rows to skip before returning results |

Each endpoint declares its own:

- **`default_limit`** -- Applied when the client omits `limit`
- **`max_limit`** -- Hard upper bound; requests exceeding this return a 400 error

### Pagination Examples

=== "GET"

    ```bash
    # First page (100 rows starting from 0)
    curl "https://api.analytics.gnosis.io/v1/execution/token_balances/daily?symbol=GNO&limit=100&offset=0" \
      -H "X-API-Key: YOUR_API_KEY"

    # Second page (next 100 rows)
    curl "https://api.analytics.gnosis.io/v1/execution/token_balances/daily?symbol=GNO&limit=100&offset=100" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

=== "POST"

    ```bash
    # First page
    curl -X POST "https://api.analytics.gnosis.io/v1/execution/token_balances/daily" \
      -H "Content-Type: application/json" \
      -H "X-API-Key: YOUR_API_KEY" \
      -d '{"symbol": "GNO", "limit": 100, "offset": 0}'

    # Second page
    curl -X POST "https://api.analytics.gnosis.io/v1/execution/token_balances/daily" \
      -H "Content-Type: application/json" \
      -H "X-API-Key: YOUR_API_KEY" \
      -d '{"symbol": "GNO", "limit": 100, "offset": 100}'
    ```

!!! warning "Pagination must be enabled on the endpoint"
    If pagination is **not** enabled in the endpoint's metadata, passing `limit` or `offset` is treated as an undeclared parameter and returns a 400 error:

    ```json
    {"detail": "Unsupported query parameters: limit, offset"}
    ```

### Pagination Constraints

| Constraint | Behavior |
|------------|----------|
| `limit` < 1 | Returns 400: `'limit' must be >= 1.` |
| `limit` > `max_limit` | Returns 400: `'limit' must be <= {max_limit}.` |
| `offset` < 0 | Returns 400: `'offset' must be >= 0.` |
| `limit` omitted | Uses the endpoint's `default_limit` |
| `offset` omitted | Defaults to `0` |

## Sort

Sort order is declared in the dbt model metadata and applied server-side. **Clients cannot override the sort order.** The sort is fixed per endpoint and defined as a list of columns with directions.

A typical pattern sorts by date descending so the most recent data appears first:

```json
"sort": [{"column": "date", "direction": "DESC"}]
```

Multi-column sorting is supported:

```json
"sort": [
  {"column": "date", "direction": "DESC"},
  {"column": "symbol", "direction": "ASC"}
]
```

When no `sort` is declared, rows are returned in the database's natural order (which is not guaranteed to be deterministic).

## Filter Policy

Each metadata-driven endpoint has a filter policy that governs whether requests without filters are permitted. This prevents accidental full-table scans on large datasets.

### `allow_unfiltered`

| Value | Behavior |
|-------|----------|
| `false` (default) | At least one business filter must be provided. Requests with zero filters return 400. |
| `true` | Requests with no filters are allowed. The full dataset is returned (subject to pagination). |

When `allow_unfiltered` is `false` and no filters are provided:

```json
{"detail": "At least one business filter is required for this endpoint."}
```

!!! note "Business filters vs pagination"
    `limit` and `offset` are **not** considered business filters. An endpoint with `allow_unfiltered: false` still requires at least one declared filter parameter -- providing only `limit` is not sufficient.

### `require_any_of`

A stronger constraint than `allow_unfiltered`. Specifies a list of parameter names where **at least one** must be present in the request. The client must supply at least one of the named filters, regardless of whether other filters are also provided.

For example, if an endpoint declares:

```json
"require_any_of": ["symbol", "address"]
```

Then the client must provide either `symbol`, `address`, or both. Providing only `start_date` (which is not in the `require_any_of` list) returns:

```json
{"detail": "At least one of [symbol, address] is required for this endpoint."}
```

### How `allow_unfiltered` and `require_any_of` Interact

| `allow_unfiltered` | `require_any_of` | Behavior |
|--------------------|-------------------|----------|
| `true` | `[]` (empty) | No filter requirements. Fully open queries allowed. |
| `false` | `[]` (empty) | Any one declared filter must be provided. |
| `false` | `["symbol", "address"]` | At least `symbol` or `address` must be present. |
| `true` | `["symbol", "address"]` | At least `symbol` or `address` must be present (`require_any_of` takes precedence). |

## Undeclared Parameters

The API enforces a strict contract: only parameters declared in the endpoint's `meta.api.parameters` (plus `limit`/`offset` when pagination is enabled) are accepted. Any other parameter is rejected.

=== "GET"

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/token_balances/daily?symbol=GNO&unknown_param=foo" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

    ```json
    {"detail": "Unsupported query parameters: unknown_param"}
    ```

=== "POST"

    ```bash
    curl -X POST "https://api.analytics.gnosis.io/v1/execution/token_balances/daily" \
      -H "Content-Type: application/json" \
      -H "X-API-Key: YOUR_API_KEY" \
      -d '{"symbol": "GNO", "unknown_field": "value"}'
    ```

    ```json
    {"detail": "Unsupported body fields: unknown_field"}
    ```

## Complete Request Example

Here is a full example showing a metadata-driven endpoint with all features in use.

**Endpoint configuration (in dbt model):**

```json
{
  "methods": ["GET", "POST"],
  "allow_unfiltered": false,
  "require_any_of": ["symbol", "address"],
  "parameters": [
    {"name": "symbol", "column": "symbol", "operator": "=", "type": "string"},
    {"name": "address", "column": "address", "operator": "IN", "type": "string_list", "case": "lower", "max_items": 200},
    {"name": "start_date", "column": "date", "operator": ">=", "type": "date"},
    {"name": "end_date", "column": "date", "operator": "<=", "type": "date"}
  ],
  "pagination": {"enabled": true, "default_limit": 100, "max_limit": 5000},
  "sort": [{"column": "date", "direction": "DESC"}]
}
```

=== "GET request"

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/token_balances/daily?symbol=GNO&address=0xAbC,0xDeF&start_date=2024-01-01&end_date=2024-06-30&limit=50&offset=0" \
      -H "accept: application/json" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

=== "POST request"

    ```bash
    curl -X POST "https://api.analytics.gnosis.io/v1/execution/token_balances/daily" \
      -H "Content-Type: application/json" \
      -H "X-API-Key: YOUR_API_KEY" \
      -d '{
        "symbol": "GNO",
        "address": ["0xAbC", "0xDeF"],
        "start_date": "2024-01-01",
        "end_date": "2024-06-30",
        "limit": 50,
        "offset": 0
      }'
    ```

Both requests generate the equivalent SQL:

```sql
SELECT *
FROM dbt_table
WHERE symbol = 'GNO'
  AND lower(address) IN ('0xabc', '0xdef')
  AND date >= '2024-01-01'
  AND date <= '2024-06-30'
ORDER BY date DESC
LIMIT 50 OFFSET 0
```

Note how the `address` values are automatically lowercased due to `"case": "lower"`.

## Full `meta.api` Reference

The `meta.api` object in the dbt model configuration controls all endpoint behavior.

### Top-Level Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `methods` | list of strings | `["GET"]` | Allowed HTTP methods (`GET`, `POST`) |
| `allow_unfiltered` | boolean | `false` | Allow requests with no business filters |
| `require_any_of` | list of strings | `[]` | At least one of these filter names must be present |
| `parameters` | list of objects | `[]` | Declared filter parameters (see below) |
| `pagination` | object | disabled | Pagination configuration (see below) |
| `sort` | list of objects | `[]` | Server-side sort order (see below) |

### Parameter Object

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `name` | Yes | string | API field name used by clients |
| `column` | Yes | string | ClickHouse column name to filter on (must exist in the model's `SELECT`) |
| `operator` | Yes | string | One of `=`, `>=`, `<=`, `ILIKE`, `IN` |
| `type` | Yes | string | One of `string`, `date`, `string_list` |
| `description` | No | string | Description shown in OpenAPI docs |
| `case` | No | string | `lower` or `upper` -- normalizes input and wraps column in `lower()`/`upper()` |
| `max_items` | No | integer | Maximum list size (`string_list` only) |

### Pagination Object

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `enabled` | Yes | boolean | Must be `true` to enable `limit`/`offset` parameters |
| `default_limit` | Yes (when enabled) | integer | Default row limit when client omits `limit` |
| `max_limit` | Yes (when enabled) | integer | Hard upper bound for `limit` |

### Sort Object

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `column` | Yes | string | Column name present in the model's final `SELECT` |
| `direction` | Yes | string | `ASC` or `DESC` |

## Next Steps

- [Endpoints](endpoints.md) -- Understand URL structure and available categories.
- [Rate Limits](rate-limits.md) -- Per-tier rate limits and throttling behavior.
- [Error Handling](errors.md) -- All error codes and response formats.
