# MMM API Endpoints

<!-- BEGIN AUTO-GENERATED: api-catalog-mmm -->
_1 endpoints across 1 resources. Generated from the dbt manifest — edits inside this block will be overwritten. Regenerate with `python scripts/update_docs.py --only api`._

## mmm_spine

API view passthrough over `fct_execution_mmm_spine_weekly`. Tier1 endpoint (`api:mmm_spine_weekly`), requires `X-API-Key`. The MMM analyst persona reads this directly to pull a complete (kpi, media, control) weekly spine without hand-rolling the union — a single `SELECT * FROM api_execution_mmm_s...

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/mmm/mmm_spine/weekly` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/mmm/mmm_spine/weekly`"
    API view passthrough over `fct_execution_mmm_spine_weekly`. Tier1 endpoint (`api:mmm_spine_weekly`), requires `X-API-Key`. The MMM analyst persona reads this directly to pull a complete (kpi, media, control) weekly spine without hand-rolling the union — a single `SELECT * FROM api_execution_mmm_s...

    Model: `api_execution_mmm_spine_weekly` — table `dbt.api_execution_mmm_spine_weekly`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `week` | `Date` | ISO Monday-start week date. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/mmm/mmm_spine/weekly" \
      -H "X-API-Key: YOUR_API_KEY"
    ```
<!-- END AUTO-GENERATED: api-catalog-mmm -->
