---
title: API Changelog
description: Notable changes to the Gnosis Analytics API surface
---

# API Changelog

Notable changes to the public API surface, most recent first. The OpenAPI specification at [`/openapi.json`](https://api.analytics.gnosis.io/openapi.json) always reflects the **live** endpoint catalog, so it is the authoritative reference at any point in time.

## 2026-06-09 -- Path restructure

**About 130 endpoint paths changed.** The `api:` resource id no longer embeds the time grain or metric window -- both moved into dedicated path segments of the URL contract:

```
/v1/{category}/{resource}/{granularity}[/{window}]
```

- **Time grain** (`daily`/`weekly`/`monthly`/`hourly`/`latest`) moved out of the resource name into the `granularity` path segment. Daily/weekly/monthly variants that used to be separate resources are now **one resource** selected by the granularity segment.
- **Metric windows** (`7d`/`30d`/`60d`) moved out of the resource name into a new trailing `window` path segment.

### Example Migrations

| Old path | New path |
|----------|----------|
| `/v1/execution/gpay_activity_by_action_daily/daily` | `/v1/execution/gpay_activity_by_action/daily` |
| `/v1/execution/circles_v2_kpi_mints_7d/last_7d` | `/v1/execution/circles_v2_kpi_mints/last_7d/7d` |
| `/v1/mta/gpay_attribution_30d/rolling_180d` | `/v1/mta/gpay_attribution/rolling_180d/30d` |
| `/v1/consensus/forks_info` | `/v1/consensus/forks_info/latest` |

The full old-to-new mapping table for all changed paths is in the [API migration document](https://github.com/gnosischain/cerebro-api/blob/main/docs/API_MIGRATION_2026-06-09.md) in the cerebro-api repository.

!!! warning "Older integrations should update their paths"
    Clients built against the pre-2026-06-09 paths must update to the new URL structure. If you are unsure which paths your integration uses, compare them against the live [OpenAPI spec](https://api.analytics.gnosis.io/openapi.json) or the migration mapping table linked above.

## Next Steps

- [Endpoints](endpoints.md) -- The current URL contract and how routes are generated.
- [Metrics Explorer](explorer.md) -- Searchable catalog of every endpoint.
- [Endpoint Catalog](catalog/index.md) -- Per-category reference with columns and filters.
