---
title: Swagger UI
description: Interactive API documentation, ReDoc, and OpenAPI specification
---

# Interactive Docs (Swagger UI)

The Gnosis Analytics API provides auto-generated interactive documentation through **Swagger UI** and **ReDoc**. Both interfaces are generated from the OpenAPI specification and always reflect the current endpoint catalog -- when new dbt models are deployed, they appear in the docs automatically after the next manifest refresh.

## Live Swagger UI

Browse, test, and explore all API endpoints directly in the browser:

**Swagger UI:** [https://api.analytics.gnosis.io/docs](https://api.analytics.gnosis.io/docs){ .md-button .md-button--primary }

<iframe
  src="https://api.analytics.gnosis.io/docs"
  width="100%"
  height="800px"
  style="border: 1px solid #e0e0e0; border-radius: 4px;"
  loading="lazy"
  title="Gnosis Analytics API - Swagger UI">
</iframe>

!!! note "Interactive features require the live API"
    The embedded Swagger UI above connects to the live API at `api.analytics.gnosis.io`. The "Try it out" feature sends real requests to the production API. If the iframe does not load, visit the [Swagger UI](https://api.analytics.gnosis.io/docs) link directly.

## Using the Swagger UI

### 1. Browse Endpoints by Category

Endpoints are grouped by category (Consensus, Execution, Bridges, etc.) in collapsible sections. Click a category header to expand it and see all available endpoints.

Within each category, endpoints are sorted by resource name and then by granularity priority (`latest` first, then `daily`, `weekly`, etc.).

### 2. Authenticate

To test endpoints that require an API key (tier1+):

1. Click the **Authorize** button (lock icon) at the top of the page
2. Enter your API key in the `X-API-Key` field
3. Click **Authorize**, then **Close**

All subsequent "Try it out" requests will include your API key automatically. Tier0 endpoints work without authentication.

### 3. Try It Out

To execute a live API call:

1. Click on any endpoint to expand its documentation
2. Click the **Try it out** button
3. Fill in any query parameters (filters, pagination)
4. Click **Execute**
5. View the response body, status code, and headers below

### 4. Inspect Endpoint Details

Each endpoint in the Swagger UI displays:

- **Summary** -- Resource name and granularity
- **Required access tier** -- Shown in the endpoint description (e.g., `Required Access: tier1`)
- **Declared filters** -- Parameter names, operators, and descriptions
- **Pagination settings** -- Default and maximum limits (when enabled)
- **Sort order** -- Server-side sort columns and directions
- **Column schema** -- All columns returned in the response, with their ClickHouse data types
- **HTTP methods** -- GET and/or POST (POST variants have a "(POST)" suffix)

### 5. View Request/Response Examples

After executing a request, the Swagger UI shows:

- The **curl command** that was sent (useful for reproducing the request in scripts)
- The **request URL** with all parameters expanded
- The **response body** as formatted JSON
- The **response headers** including rate limit information
- The **HTTP status code**

## ReDoc

An alternative documentation interface is available through **ReDoc**, which provides a cleaner three-panel reading experience:

**ReDoc:** [https://api.analytics.gnosis.io/redoc](https://api.analytics.gnosis.io/redoc){ .md-button }

ReDoc is optimized for reference and reading, with features including:

- **Three-panel layout** -- Navigation on the left, documentation in the center, request/response examples on the right
- **Search** -- Full-text search across all endpoints and their descriptions
- **Nested schema display** -- Expandable request and response schemas with type information
- **Downloadable spec** -- Download the full OpenAPI specification directly from the ReDoc interface

!!! tip "When to use which"
    Use **Swagger UI** when you want to interactively test endpoints and experiment with parameters. Use **ReDoc** when you want a clean, printable reference for the full API surface.

## OpenAPI Specification

The raw OpenAPI JSON specification is available at:

```
https://api.analytics.gnosis.io/openapi.json
```

You can use this specification with any OpenAPI-compatible tool:

| Tool | Use Case |
|------|----------|
| [Swagger Codegen](https://swagger.io/tools/swagger-codegen/) | Generate client SDKs in multiple languages |
| [OpenAPI Generator](https://openapi-generator.tech/) | Generate client libraries, server stubs, and documentation |
| [Postman](https://www.postman.com/) | Import as a collection for API testing |
| [Insomnia](https://insomnia.rest/) | Import for REST API development and debugging |
| [Stoplight](https://stoplight.io/) | API design and documentation platform |

### Importing into Postman

1. Open Postman and go to **File > Import**
2. Select **Link** and paste: `https://api.analytics.gnosis.io/openapi.json`
3. Click **Import** -- all endpoints will be created as a Postman collection
4. Set the `X-API-Key` variable in the collection settings for authenticated requests

### Fetching the Spec Programmatically

```bash
curl -s "https://api.analytics.gnosis.io/openapi.json" | python -m json.tool > openapi.json
```

## Embedding in Your Own Site

You can embed the Swagger UI in your own documentation or internal tools using an iframe:

```html
<iframe
  src="https://api.analytics.gnosis.io/docs"
  width="100%"
  height="800px"
  style="border: none;"
  loading="lazy"
  title="Gnosis Analytics API Documentation">
</iframe>
```

Or render the OpenAPI spec with your own Swagger UI instance:

```html
<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist/swagger-ui.css" />
</head>
<body>
  <div id="swagger-ui"></div>
  <script src="https://unpkg.com/swagger-ui-dist/swagger-ui-bundle.js"></script>
  <script>
    SwaggerUIBundle({
      url: "https://api.analytics.gnosis.io/openapi.json",
      dom_id: "#swagger-ui",
      presets: [SwaggerUIBundle.presets.apis],
      layout: "BaseLayout",
    });
  </script>
</body>
</html>
```

## Local Development

When running the API locally, the interactive docs are available at:

| Interface | URL |
|-----------|-----|
| Swagger UI | `http://127.0.0.1:8000/docs` |
| ReDoc | `http://127.0.0.1:8000/redoc` |
| OpenAPI JSON | `http://127.0.0.1:8000/openapi.json` |

The local docs reflect whatever dbt manifest is configured via `DBT_MANIFEST_URL` or `DBT_MANIFEST_PATH` in your environment.

## Next Steps

- [Endpoints](endpoints.md) -- Understand the URL structure and how endpoints are generated.
- [Filtering & Pagination](filtering.md) -- Learn how to construct queries with filters, pagination, and sort.
- [Authentication](authentication.md) -- Set up API key authentication for testing protected endpoints.
