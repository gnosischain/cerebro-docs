---
title: Quick Start
description: Make your first Gnosis Analytics API call in under a minute
---

# Quick Start

This guide walks you through making your first API call to the Gnosis Analytics platform. Public (tier0) endpoints require no API key, so you can start exploring data immediately.

## Prerequisites

None. Tier0 endpoints are publicly accessible. All you need is an HTTP client such as `curl`, a web browser, or any programming language with HTTP support.

## Step 1: Make Your First API Call

The base URL for all API endpoints is:

```
https://api.analytics.gnosis.io/v1
```

Make a request to a public endpoint to retrieve the latest blob commitment data from the Gnosis Chain consensus layer:

```bash
curl -s "https://api.analytics.gnosis.io/v1/consensus/blob_commitments/latest" \
  -H "accept: application/json" | python3 -m json.tool
```

You should receive a JSON response containing the most recent blob commitment metrics.

## Step 2: Explore the Interactive Docs

The API ships with auto-generated interactive documentation powered by Swagger UI. Open the following URL in your browser:

```
https://api.analytics.gnosis.io/docs
```

From Swagger UI you can:

- Browse all available endpoints grouped by category (Consensus, Execution, etc.)
- View request parameters, response schemas, and required access tiers
- Execute API calls directly from the browser using the "Try it out" button

An alternative documentation view powered by ReDoc is available at:

```
https://api.analytics.gnosis.io/redoc
```

## Step 3: Get an API Key

Public (tier0) endpoints are available without authentication. To access higher-tier endpoints with richer data and higher rate limits, you need an API key.

| Tier | Access Level | Rate Limit |
|------|-------------|------------|
| `tier0` | Public | 20 requests/min |
| `tier1` | Partner | 100 requests/min |
| `tier2` | Premium | 500 requests/min |
| `tier3` | Internal | 10,000 requests/min |

To request an API key, contact the Gnosis Analytics team or visit the self-service portal (if available for your organization).

## Step 4: Make an Authenticated Request

Once you have an API key, include it in the `X-API-Key` header:

```bash
curl -s "https://api.analytics.gnosis.io/v1/consensus/blob_commitments/daily" \
  -H "accept: application/json" \
  -H "X-API-Key: YOUR_API_KEY" | python3 -m json.tool
```

Higher-tier keys grant access to all endpoints at or below their tier level. For example, a `tier2` key can access `tier0`, `tier1`, and `tier2` endpoints.

## Next Steps

- [API Reference](../api/index.md) -- Full API documentation with endpoint details
- [Authentication](../api/authentication.md) -- Detailed authentication and tier system
- [Filtering & Pagination](../api/filtering.md) -- Query parameters, POST bodies, and pagination
- [Platform Overview](platform-overview.md) -- Understand the full analytics ecosystem
