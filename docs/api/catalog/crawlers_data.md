# Crawlers Data API Endpoints

<!-- BEGIN AUTO-GENERATED: api-catalog-crawlers_data -->
<!-- generated: 2026-07-23 -->
_1 endpoints across 1 resources. Generated from the dbt manifest — edits inside this block will be overwritten. Regenerate with `python scripts/update_docs.py --only api`._

## gno_supply

The api_crawlers_data_gno_supply_daily model aggregates daily GNO supply data from crawler sources to support trend analysis and reporting.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/crawlers_data/gno_supply/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/crawlers_data/gno_supply/daily`"
    The api_crawlers_data_gno_supply_daily model aggregates daily GNO supply data from crawler sources to support trend analysis and reporting.

    Model: `api_crawlers_data_gno_supply_daily` — table `dbt.api_crawlers_data_gno_supply_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `label` | `String` | Identifier for the specific GNO supply data source or category. |
    | `date` | `Date` | The date corresponding to the supply data, formatted as YYYY-MM-DD. |
    | `supply` | `Float64` | The amount of GNO supply recorded on the given date, measured in units consistent with blockchain token quantities. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/crawlers_data/gno_supply/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```
<!-- END AUTO-GENERATED: api-catalog-crawlers_data -->
