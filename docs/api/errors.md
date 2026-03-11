---
title: Error Handling
description: HTTP status codes, error response format, and troubleshooting
---

# Error Handling

The Gnosis Analytics API uses standard HTTP status codes and returns error details in a consistent JSON format. This page documents every error code, the response structure, and all common error scenarios with example requests and responses.

## Error Response Format

All errors return a JSON object with a `detail` field containing a human-readable description:

```json
{
  "detail": "Human-readable error message describing what went wrong."
}
```

The `detail` field is always a string. Some error messages include contextual information such as the user's tier level, the required tier, specific parameter names, or configured limits.

## HTTP Status Codes

| Status Code | Meaning | When It Occurs |
|-------------|---------|----------------|
| **400** | Bad Request | Invalid parameters, unsupported query params/body fields, missing required filters, invalid JSON, pagination violations, list size violations |
| **403** | Forbidden | Missing API key, invalid API key, insufficient tier access |
| **404** | Not Found | Endpoint does not exist |
| **429** | Too Many Requests | Rate limit exceeded for your tier or IP |
| **500** | Internal Server Error | Database query failure, unexpected server error |

## 400 Bad Request

Returned when the request is malformed or violates the endpoint's declared contract. There are several distinct causes, each with a specific error message.

### Undeclared Query Parameter

A GET request includes query parameters not declared in the endpoint's `meta.api.parameters`:

```bash
curl "https://api.analytics.gnosis.io/v1/execution/token_balances/daily?symbol=GNO&unknown_param=foo" \
  -H "X-API-Key: YOUR_API_KEY"
```

```json
{
  "detail": "Unsupported query parameters: unknown_param"
}
```

!!! tip "Multiple undeclared parameters are listed together"
    If you pass several unknown parameters, they are all listed in alphabetical order:
    ```json
    {"detail": "Unsupported query parameters: bar, foo, xyz"}
    ```

### Undeclared Body Field

A POST request includes JSON fields not declared in the endpoint's metadata:

```bash
curl -X POST "https://api.analytics.gnosis.io/v1/execution/token_balances/daily" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_API_KEY" \
  -d '{"symbol": "GNO", "unknown_field": "value"}'
```

```json
{
  "detail": "Unsupported body fields: unknown_field"
}
```

### Missing Required Filter (`allow_unfiltered: false`)

The endpoint requires at least one business filter, but none were provided:

```bash
curl "https://api.analytics.gnosis.io/v1/execution/token_balances/daily?limit=100" \
  -H "X-API-Key: YOUR_API_KEY"
```

```json
{
  "detail": "At least one business filter is required for this endpoint."
}
```

!!! note "`limit` and `offset` are not business filters"
    Pagination parameters do not count as business filters. You must provide at least one declared filter parameter (e.g., `symbol`, `address`, `start_date`).

### Missing `require_any_of` Filter

The endpoint requires at least one of a specific set of filters, but none of them were provided:

```bash
# Endpoint declares require_any_of: ["symbol", "address"]
curl "https://api.analytics.gnosis.io/v1/execution/token_balances/daily?start_date=2024-01-01" \
  -H "X-API-Key: YOUR_API_KEY"
```

```json
{
  "detail": "At least one of [symbol, address] is required for this endpoint."
}
```

### Legacy Endpoint with Parameters

Query parameters were passed to a legacy endpoint (one without `meta.api` configuration). Legacy endpoints do not accept any query parameters:

```bash
curl "https://api.analytics.gnosis.io/v1/consensus/some_legacy_metric?date=2024-01-01" \
  -H "X-API-Key: YOUR_API_KEY"
```

```json
{
  "detail": "This endpoint does not declare API parameters. Add meta.api to the dbt model to enable filters or pagination."
}
```

### Pagination Limit Exceeded

The `limit` value exceeds the endpoint's configured `max_limit`:

```bash
curl "https://api.analytics.gnosis.io/v1/execution/token_balances/daily?symbol=GNO&limit=999999" \
  -H "X-API-Key: YOUR_API_KEY"
```

```json
{
  "detail": "'limit' must be <= 5000."
}
```

### Invalid Pagination Values

The `limit` or `offset` value is not a valid integer or is below the minimum:

=== "limit below minimum"

    ```json
    {"detail": "'limit' must be >= 1."}
    ```

=== "offset below minimum"

    ```json
    {"detail": "'offset' must be >= 0."}
    ```

=== "non-integer value"

    ```json
    {"detail": "'limit' must be an integer."}
    ```

### List Parameter Max Items Exceeded

A `string_list` parameter received more values than its configured `max_items`:

```bash
# Endpoint allows at most 200 addresses
curl "https://api.analytics.gnosis.io/v1/execution/token_balances/daily?address=0x1&address=0x2&...&address=0x201" \
  -H "X-API-Key: YOUR_API_KEY"
```

```json
{
  "detail": "Parameter 'address' allows at most 200 values."
}
```

### Scalar Parameter Receives List

A `string` or `date` parameter received a list value (in a POST body):

```json
{
  "detail": "Parameter 'symbol' expects a single value."
}
```

### POST with Query Parameters

Query string parameters were included on a POST request. POST endpoints accept filters only in the JSON body:

```bash
curl -X POST "https://api.analytics.gnosis.io/v1/execution/token_balances/daily?symbol=GNO" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_API_KEY" \
  -d '{}'
```

```json
{
  "detail": "POST endpoints accept filter and pagination fields in JSON body only."
}
```

### Invalid JSON Body

The POST request body is not valid JSON:

```bash
curl -X POST "https://api.analytics.gnosis.io/v1/execution/token_balances/daily" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_API_KEY" \
  -d 'not valid json'
```

```json
{
  "detail": "Request body must be valid JSON."
}
```

### Non-Object JSON Body

The POST request body is valid JSON but not a JSON object (e.g., an array or scalar):

```bash
curl -X POST "https://api.analytics.gnosis.io/v1/execution/token_balances/daily" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_API_KEY" \
  -d '["not", "an", "object"]'
```

```json
{
  "detail": "Request body must be a JSON object."
}
```

## 403 Forbidden

Returned for authentication and authorization failures. All 403 errors relate to the `X-API-Key` header or the user's tier level.

### Missing API Key

A non-public endpoint (tier1+) was called without the `X-API-Key` header:

```bash
curl "https://api.analytics.gnosis.io/v1/consensus/blob_commitments/daily"
```

```json
{
  "detail": "Missing authentication header: X-API-Key"
}
```

### Invalid API Key

The provided API key does not exist in the server's key registry. This applies to **all** endpoints, including tier0. If you provide a key, it must be valid:

```bash
curl "https://api.analytics.gnosis.io/v1/consensus/blob_commitments/latest" \
  -H "X-API-Key: sk_live_nonexistent_key"
```

```json
{
  "detail": "Invalid API Key"
}
```

### Insufficient Tier Access

The API key's tier level is lower than the endpoint's required tier:

```bash
# tier1 key attempting to access a tier2 endpoint
curl "https://api.analytics.gnosis.io/v1/financial/treasury/all_time" \
  -H "X-API-Key: sk_live_partner_key"
```

```json
{
  "detail": "Access denied. This endpoint requires tier2 access. User 'bob' has tier1 access."
}
```

The error message includes both the required tier and the user's actual tier to aid debugging.

## 404 Not Found

Returned when the requested endpoint path does not exist. This typically means:

- The URL path is misspelled
- The dbt model has not been deployed yet
- The model does not have the required `production` and `api:*` tags

```bash
curl "https://api.analytics.gnosis.io/v1/consensus/nonexistent_resource/daily" \
  -H "X-API-Key: YOUR_API_KEY"
```

```json
{
  "detail": "Not Found"
}
```

## 429 Too Many Requests

Returned when the rate limit for your tier (or IP address) has been exceeded:

```http
HTTP/1.1 429 Too Many Requests
Content-Type: application/json
Retry-After: 42

{
  "detail": "Rate limit exceeded. Try again in 42 seconds."
}
```

The `Retry-After` header indicates how many seconds to wait before the rate limit window resets.

See [Rate Limits](rate-limits.md) for per-tier limits, headers, and best practices for handling throttling.

## 500 Internal Server Error

Returned when an unexpected server-side error occurs, typically a database query failure or configuration issue:

```json
{
  "detail": "Internal server error description."
}
```

500 errors should be rare. If you encounter persistent 500 errors, contact the Gnosis Analytics team with:

- The full request URL and method
- Any request body (redact your API key)
- The timestamp of the error
- The exact error message from the `detail` field

## Error Quick-Reference Table

| Error | Status | Detail Message Pattern |
|-------|--------|----------------------|
| Missing API key | 403 | `Missing authentication header: X-API-Key` |
| Invalid API key | 403 | `Invalid API Key` |
| Insufficient tier | 403 | `Access denied. This endpoint requires {tier} access. User '{user}' has {tier} access.` |
| Undeclared query param | 400 | `Unsupported query parameters: {names}` |
| Undeclared body field | 400 | `Unsupported body fields: {names}` |
| No business filter | 400 | `At least one business filter is required for this endpoint.` |
| Missing require_any_of | 400 | `At least one of [{names}] is required for this endpoint.` |
| Legacy endpoint params | 400 | `This endpoint does not declare API parameters...` |
| Limit exceeded | 400 | `'limit' must be <= {max}.` |
| Invalid limit/offset | 400 | `'{field}' must be an integer.` |
| Max items exceeded | 400 | `Parameter '{name}' allows at most {max} values.` |
| POST with query string | 400 | `POST endpoints accept filter and pagination fields in JSON body only.` |
| Invalid JSON | 400 | `Request body must be valid JSON.` |
| Non-object JSON | 400 | `Request body must be a JSON object.` |
| Scalar expects single | 400 | `Parameter '{name}' expects a single value.` |
| Rate limited | 429 | `Rate limit exceeded. Try again in {n} seconds.` |
| Server error | 500 | Varies |

## Troubleshooting

### I get 403 but my key looks correct

- Verify there are no trailing spaces or newline characters in your key.
- Confirm the key starts with `sk_live_`.
- Check that you are using the `X-API-Key` header (not `Authorization: Bearer`).
- If the error says "insufficient tier access," your key is valid but your tier is too low for the endpoint. Check the endpoint's required tier in the [Swagger UI](swagger.md).

### I get 400 "Unsupported query parameters" for `limit`

The endpoint does not have pagination enabled. Only endpoints that declare `meta.api.pagination` accept `limit` and `offset`. Check the endpoint's documentation in the Swagger UI to see if pagination is available.

### I get 400 "At least one business filter is required"

The endpoint has `allow_unfiltered: false` (the default). You must provide at least one declared filter parameter. Check the Swagger UI for the list of available filters on this endpoint. Note that `limit` and `offset` do not count as business filters.

### I get 429 but I am not making many requests

- If you are not using an API key on a tier0 endpoint, the rate limit is shared with all other users on your IP address. Provide your API key to get a dedicated counter.
- The fixed-window strategy means all requests near the window boundary count toward the same window. Spread requests evenly rather than sending bursts.

### I get 500 errors intermittently

This may indicate a transient database issue. Wait a few minutes and retry. If the problem persists, report it to the Gnosis Analytics team with the request details and error message.

### My endpoint returns 404 but the model is deployed

- Verify the model has both the `production` tag and an `api:{resource_name}` tag.
- The API may not have refreshed its manifest yet. The refresh interval is 5 minutes by default. Wait for the next refresh cycle, or ask a tier3 user to trigger a manual refresh via `POST /v1/system/manifest/refresh`.
- Check for `meta.api` configuration errors. If the `meta.api` block has validation errors (e.g., referencing a nonexistent column), the endpoint is skipped during route generation. Check server logs for warnings.

## Next Steps

- [Authentication](authentication.md) -- Understand tier access and API key setup.
- [Filtering & Pagination](filtering.md) -- Construct valid requests that avoid 400 errors.
- [Rate Limits](rate-limits.md) -- Avoid 429 errors and handle throttling gracefully.
