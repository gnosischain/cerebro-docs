---
title: API Reference
description: REST API documentation for Gnosis Analytics
---

# API Reference

The Gnosis Analytics API provides programmatic access to blockchain analytics data for Gnosis Chain. It is built with **FastAPI** and backed by **ClickHouse**, with endpoints auto-generated from the dbt manifest.

## Base URL

```
https://api.analytics.gnosis.io/v1
```

All endpoint paths are prefixed with `/v1`. For example, the full URL for the daily blob commitments endpoint is:

```
https://api.analytics.gnosis.io/v1/consensus/blob_commitments/daily
```

## Key Features

- **Metadata-driven**: Endpoints are automatically generated from dbt model tags and `meta.api` configuration. No custom Python code is needed to expose new data.
- **Tiered access control**: Four access tiers (tier0 through tier3) with hierarchical permissions. Public endpoints require no API key.
- **Dual query interface**: Supports both GET requests with query parameters and POST requests with JSON bodies for complex filters.
- **Auto-generated documentation**: OpenAPI (Swagger UI) and ReDoc documentation are generated automatically and always reflect the current endpoint catalog.
- **Automatic endpoint discovery**: The API periodically refreshes its route registry from the dbt manifest, so new dbt models become API endpoints without redeployment.

## Interactive Documentation

Explore all endpoints interactively:

- **Swagger UI**: [https://api.analytics.gnosis.io/docs](https://api.analytics.gnosis.io/docs)
- **ReDoc**: [https://api.analytics.gnosis.io/redoc](https://api.analytics.gnosis.io/redoc)

## API Sections

| Section | Description |
|---------|-------------|
| [Authentication](authentication.md) | API key setup, tier hierarchy, and access control |
| [Endpoints](endpoints.md) | URL conventions, categories, granularities, and tag mapping |
| [Filtering & Pagination](filtering.md) | Query parameters, POST bodies, operators, and pagination |
| [Rate Limits](rate-limits.md) | Per-tier rate limits and throttling behavior |
| [Swagger UI](swagger.md) | Interactive API documentation |
| [Error Handling](errors.md) | HTTP status codes, error response format, and common scenarios |

## Quick Example

Fetch the latest blob commitment data (no API key required):

```bash
curl -s "https://api.analytics.gnosis.io/v1/consensus/blob_commitments/latest" \
  -H "accept: application/json"
```

Fetch daily token balances with filters (requires tier1 key):

```bash
curl -s "https://api.analytics.gnosis.io/v1/execution/token_balances/daily?symbol=GNO&start_date=2024-01-01&limit=50" \
  -H "accept: application/json" \
  -H "X-API-Key: YOUR_API_KEY"
```
