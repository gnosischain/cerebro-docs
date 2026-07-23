# MTA API Endpoints

<!-- BEGIN AUTO-GENERATED: api-catalog-mta -->
<!-- generated: 2026-07-23 -->
_7 endpoints across 3 resources. Generated from the dbt manifest — edits inside this block will be overwritten. Regenerate with `python scripts/update_docs.py --only api`._

## gnosis_app_attribution

API view passthrough over `fct_execution_gnosis_app_attribution_30d`. Tier1 endpoint (`api:gnosis_app_attribution_30d`), requires `X-API-Key`. Granularity tag `granularity:rolling_180d` documents that the underlying mart aggregates over the trailing 180 days of conversions.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/mta/gnosis_app_attribution/rolling_180d/30d` | GET | tier1 | -- | -- | -- |
| `/v1/mta/gnosis_app_attribution/rolling_180d/60d` | GET | tier1 | -- | -- | -- |
| `/v1/mta/gnosis_app_attribution/rolling_180d/7d` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/mta/gnosis_app_attribution/rolling_180d/30d`"
    API view passthrough over `fct_execution_gnosis_app_attribution_30d`. Tier1 endpoint (`api:gnosis_app_attribution_30d`), requires `X-API-Key`. Granularity tag `granularity:rolling_180d` documents that the underlying mart aggregates over the trailing 180 days of conversions.

    Model: `api_execution_gnosis_app_attribution_30d` — table `dbt.api_execution_gnosis_app_attribution_30d`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `conversion_kind` | `LowCardinality(String)` | Conversion target. |
    | `event_kind` | `LowCardinality(String)` | Touchpoint kind being credited. |
    | `conversions_with_touch` | `UInt64` | Distinct conversions that saw this `event_kind` in their journey. |
    | `first_touch` | `Float64` | Sum of first-touch credits. |
    | `last_touch` | `Float64` | Sum of last-touch credits. |
    | `linear` | `Float64` | Sum of linear credits. |
    | `time_decay_hl_7d` | `Float64` | Sum of time-decay credits (HL=7d). |
    | `total_conversions` | `UInt64` | Total conversions of this kind in the 180-day window. |
    | `computed_at` | `DateTime` | Materialisation timestamp. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/mta/gnosis_app_attribution/rolling_180d/30d" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/mta/gnosis_app_attribution/rolling_180d/60d`"
    API view passthrough over `fct_execution_gnosis_app_attribution_60d`. Tier1 endpoint (`api:gnosis_app_attribution_60d`), requires `X-API-Key`. Granularity tag `granularity:rolling_180d` documents that the underlying mart aggregates over the trailing 180 days of conversions.

    Model: `api_execution_gnosis_app_attribution_60d` — table `dbt.api_execution_gnosis_app_attribution_60d`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `conversion_kind` | `LowCardinality(String)` | Conversion target. |
    | `event_kind` | `LowCardinality(String)` | Touchpoint kind being credited. |
    | `conversions_with_touch` | `UInt64` | Distinct conversions that saw this `event_kind` in their journey. |
    | `first_touch` | `Float64` | Sum of first-touch credits. |
    | `last_touch` | `Float64` | Sum of last-touch credits. |
    | `linear` | `Float64` | Sum of linear credits. |
    | `time_decay_hl_7d` | `Float64` | Sum of time-decay credits (HL=7d). |
    | `total_conversions` | `UInt64` | Total conversions of this kind in the 180-day window. |
    | `computed_at` | `DateTime` | Materialisation timestamp. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/mta/gnosis_app_attribution/rolling_180d/60d" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/mta/gnosis_app_attribution/rolling_180d/7d`"
    API view passthrough over `fct_execution_gnosis_app_attribution_7d`. Tier1 endpoint (`api:gnosis_app_attribution_7d`), requires `X-API-Key`. Granularity tag `granularity:rolling_180d` documents that the underlying mart aggregates over the trailing 180 days of conversions.

    Model: `api_execution_gnosis_app_attribution_7d` — table `dbt.api_execution_gnosis_app_attribution_7d`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `conversion_kind` | `LowCardinality(String)` | Conversion target. |
    | `event_kind` | `LowCardinality(String)` | Touchpoint kind being credited. |
    | `conversions_with_touch` | `UInt64` | Distinct conversions that saw this `event_kind` in their journey. |
    | `first_touch` | `Float64` | Sum of first-touch credits. |
    | `last_touch` | `Float64` | Sum of last-touch credits. |
    | `linear` | `Float64` | Sum of linear credits. |
    | `time_decay_hl_7d` | `Float64` | Sum of time-decay credits (HL=7d). |
    | `total_conversions` | `UInt64` | Total conversions of this kind in the 180-day window. |
    | `computed_at` | `DateTime` | Materialisation timestamp. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/mta/gnosis_app_attribution/rolling_180d/7d" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gnosis_app_funnel_summary

Cumulative conversion funnel per funnel/step: the number of distinct users who reached at least each step. Point-in-time snapshot backing the "Conversion Funnel" chart.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/mta/gnosis_app_funnel_summary/latest` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/mta/gnosis_app_funnel_summary/latest`"
    Cumulative conversion funnel per funnel/step: the number of distinct users who reached at least each step. Point-in-time snapshot backing the "Conversion Funnel" chart.

    Model: `api_execution_gnosis_app_funnel_summary` — table `dbt.api_execution_gnosis_app_funnel_summary`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `as_of_date` | `Date` | Snapshot date the funnel counts were computed (today, UTC). |
    | `funnel_name` | `String` | Name of the conversion funnel. |
    | `level` | `UInt8` | Funnel step index (0-based windowFunnel level). |
    | `step_label` | `String` | Human-readable step label (e.g. 'Step 1'). |
    | `n_users` | `UInt64` | Distinct users who reached at least this step. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/mta/gnosis_app_funnel_summary/latest" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gpay_attribution

API view passthrough over `fct_execution_gpay_attribution_30d`. Tier1 endpoint (`api:gpay_attribution_30d`), requires `X-API-Key`. `granularity:rolling_180d` documents the underlying window. The `identity_role` column lets API callers filter to owner-grain, treasury-grain, or delegate-grain at qu...

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/mta/gpay_attribution/rolling_180d/30d` | GET | tier1 | -- | -- | -- |
| `/v1/mta/gpay_attribution/rolling_180d/60d` | GET | tier1 | -- | -- | -- |
| `/v1/mta/gpay_attribution/rolling_180d/7d` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/mta/gpay_attribution/rolling_180d/30d`"
    API view passthrough over `fct_execution_gpay_attribution_30d`. Tier1 endpoint (`api:gpay_attribution_30d`), requires `X-API-Key`. `granularity:rolling_180d` documents the underlying window. The `identity_role` column lets API callers filter to owner-grain, treasury-grain, or delegate-grain at qu...

    Model: `api_execution_gpay_attribution_30d` — table `dbt.api_execution_gpay_attribution_30d`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `conversion_kind` | `LowCardinality(String)` | Conversion target. |
    | `identity_role` | `LowCardinality(String)` | Role grain. |
    | `event_kind` | `LowCardinality(String)` | Touchpoint kind being credited. |
    | `conversions_with_touch` | `UInt64` | Distinct conversions that saw this `event_kind` in their journey. |
    | `first_touch` | `Float64` | Sum of first-touch credits. |
    | `last_touch` | `Float64` | Sum of last-touch credits. |
    | `linear` | `Float64` | Sum of linear credits. |
    | `time_decay_hl_7d` | `Float64` | Sum of time-decay credits (HL=7d). |
    | `total_conversions` | `UInt64` | Total conversions of this (kind, role) in the 180-day window. |
    | `computed_at` | `DateTime` | Materialisation timestamp. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/mta/gpay_attribution/rolling_180d/30d" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/mta/gpay_attribution/rolling_180d/60d`"
    API view passthrough over `fct_execution_gpay_attribution_60d`. Tier1 endpoint (`api:gpay_attribution_60d`), requires `X-API-Key`. `granularity:rolling_180d` documents the underlying window.

    Model: `api_execution_gpay_attribution_60d` — table `dbt.api_execution_gpay_attribution_60d`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `conversion_kind` | `LowCardinality(String)` | Conversion target. |
    | `identity_role` | `LowCardinality(String)` | Role grain. |
    | `event_kind` | `LowCardinality(String)` | Touchpoint kind being credited. |
    | `conversions_with_touch` | `UInt64` | Distinct conversions that saw this `event_kind` in their journey. |
    | `first_touch` | `Float64` | Sum of first-touch credits. |
    | `last_touch` | `Float64` | Sum of last-touch credits. |
    | `linear` | `Float64` | Sum of linear credits. |
    | `time_decay_hl_7d` | `Float64` | Sum of time-decay credits (HL=7d). |
    | `total_conversions` | `UInt64` | Total conversions of this (kind, role) in the 180-day window. |
    | `computed_at` | `DateTime` | Materialisation timestamp. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/mta/gpay_attribution/rolling_180d/60d" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/mta/gpay_attribution/rolling_180d/7d`"
    API view passthrough over `fct_execution_gpay_attribution_7d`. Tier1 endpoint (`api:gpay_attribution_7d`), requires `X-API-Key`. `granularity:rolling_180d` documents the underlying window. The `identity_role` column lets API callers filter to owner-grain, treasury-grain, or delegate-grain at quer...

    Model: `api_execution_gpay_attribution_7d` — table `dbt.api_execution_gpay_attribution_7d`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `conversion_kind` | `LowCardinality(String)` | Conversion target. |
    | `identity_role` | `LowCardinality(String)` | Role grain. |
    | `event_kind` | `LowCardinality(String)` | Touchpoint kind being credited. |
    | `conversions_with_touch` | `UInt64` | Distinct conversions that saw this `event_kind` in their journey. |
    | `first_touch` | `Float64` | Sum of first-touch credits. |
    | `last_touch` | `Float64` | Sum of last-touch credits. |
    | `linear` | `Float64` | Sum of linear credits. |
    | `time_decay_hl_7d` | `Float64` | Sum of time-decay credits (HL=7d). |
    | `total_conversions` | `UInt64` | Total conversions of this (kind, role) in the 180-day window. |
    | `computed_at` | `DateTime` | Materialisation timestamp. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/mta/gpay_attribution/rolling_180d/7d" \
      -H "X-API-Key: YOUR_API_KEY"
    ```
<!-- END AUTO-GENERATED: api-catalog-mta -->
