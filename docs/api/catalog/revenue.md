# Revenue API Endpoints

<!-- BEGIN AUTO-GENERATED: api-catalog-revenue -->
<!-- generated: 2026-07-23 -->
_28 endpoints across 14 resources. Generated from the dbt manifest — edits inside this block will be overwritten. Regenerate with `python scripts/update_docs.py --only api`._

## revenue_active_users_cohorts

API view over fct_revenue_active_users_cohorts_weekly.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/revenue/revenue_active_users_cohorts/weekly` | GET | tier1 | `cohort`, `start_date`, `end_date` | -- | week DESC |
| `/v1/revenue/revenue_active_users_cohorts/monthly` | GET | tier1 | `cohort`, `start_date`, `end_date` | -- | month DESC |

??? info "`GET /v1/revenue/revenue_active_users_cohorts/weekly`"
    API view over fct_revenue_active_users_cohorts_weekly.

    Model: `api_revenue_active_users_cohorts_weekly` — table `dbt.api_revenue_active_users_cohorts_weekly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `cohort` | `=` | `cohort` | string | Cohort bucket |
    | `start_date` | `>=` | `week` | date | Inclusive start week |
    | `end_date` | `<=` | `week` | date | Inclusive end week |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `week DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `week` | `Date` | Week start. |
    | `cohort` | `String` | Annualised $-bucket (includes `<1`). |
    | `annual_rolling_fees_total` | `Float64` | Sum of rolling-52w fees across all streams for users in this cohort. |
    | `users_cnt` | `UInt64` | Unique users in this cohort. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/revenue/revenue_active_users_cohorts/weekly?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/revenue/revenue_active_users_cohorts/monthly`"
    API view over fct_revenue_active_users_cohorts_monthly.

    Model: `api_revenue_active_users_cohorts_monthly` — table `dbt.api_revenue_active_users_cohorts_monthly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `cohort` | `=` | `cohort` | string | Cohort bucket |
    | `start_date` | `>=` | `month` | date | Inclusive start month |
    | `end_date` | `<=` | `month` | date | Inclusive end month |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `month DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `month` | `Date` | First day of the month. |
    | `cohort` | `String` | Monthly $-bucket. |
    | `fees_total` | `Float64` | Sum of monthly fees across all streams. |
    | `users_cnt` | `UInt64` | Unique users in this cohort. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/revenue/revenue_active_users_cohorts/monthly?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## revenue_active_users_totals

API view over fct_revenue_active_users_totals_weekly.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/revenue/revenue_active_users_totals/weekly` | GET | tier1 | `start_date`, `end_date` | -- | week DESC |
| `/v1/revenue/revenue_active_users_totals/monthly` | GET | tier1 | `start_date`, `end_date` | -- | month DESC |

??? info "`GET /v1/revenue/revenue_active_users_totals/weekly`"
    API view over fct_revenue_active_users_totals_weekly.

    Model: `api_revenue_active_users_totals_weekly` — table `dbt.api_revenue_active_users_totals_weekly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `start_date` | `>=` | `week` | date | Inclusive start week |
    | `end_date` | `<=` | `week` | date | Inclusive end week |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `week DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `week` | `Date` | Week start. |
    | `users_cnt` | `UInt64` | Unique users above the $6/year threshold. |
    | `annual_rolling_fees_total` | `Float64` | Sum of rolling-52w fees from qualifying users. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/revenue/revenue_active_users_totals/weekly?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/revenue/revenue_active_users_totals/monthly`"
    API view over fct_revenue_active_users_totals_monthly.

    Model: `api_revenue_active_users_totals_monthly` — table `dbt.api_revenue_active_users_totals_monthly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `start_date` | `>=` | `month` | date | Inclusive start month |
    | `end_date` | `<=` | `month` | date | Inclusive end month |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `month DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `month` | `Date` | First day of the month. |
    | `users_cnt` | `UInt64` | Unique users above the $0.50/month threshold. |
    | `fees_total` | `Float64` | Sum of monthly fees from qualifying users. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/revenue/revenue_active_users_totals/monthly?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## revenue_gnosis_app_cohorts

API view over fct_revenue_gnosis_app_cohorts_weekly.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/revenue/revenue_gnosis_app_cohorts/weekly` | GET | tier1 | `cohort`, `start_date`, `end_date` | -- | week DESC |
| `/v1/revenue/revenue_gnosis_app_cohorts/monthly` | GET | tier1 | `cohort`, `start_date`, `end_date` | -- | month DESC |

??? info "`GET /v1/revenue/revenue_gnosis_app_cohorts/weekly`"
    API view over fct_revenue_gnosis_app_cohorts_weekly.

    Model: `api_revenue_gnosis_app_cohorts_weekly` — table `dbt.api_revenue_gnosis_app_cohorts_weekly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `cohort` | `=` | `cohort` | string | Cohort bucket |
    | `start_date` | `>=` | `week` | date | Inclusive start week |
    | `end_date` | `<=` | `week` | date | Inclusive end week |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `week DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `week` | `Date` | Week start. |
    | `cohort` | `String` | Annualised $-bucket. |
    | `annual_rolling_fees_total` | `Float64` | Sum of rolling-52w fees for users in this cohort. |
    | `users_cnt` | `UInt64` | Users with >$0 rolling fees. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/revenue/revenue_gnosis_app_cohorts/weekly?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/revenue/revenue_gnosis_app_cohorts/monthly`"
    API view over fct_revenue_gnosis_app_cohorts_monthly.

    Model: `api_revenue_gnosis_app_cohorts_monthly` — table `dbt.api_revenue_gnosis_app_cohorts_monthly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `cohort` | `=` | `cohort` | string | Cohort bucket |
    | `start_date` | `>=` | `month` | date | Inclusive start month |
    | `end_date` | `<=` | `month` | date | Inclusive end month |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `month DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `month` | `Date` | First day of the month. |
    | `cohort` | `String` | Monthly $-bucket. |
    | `fees_total` | `Float64` | Sum of monthly fees. |
    | `users_cnt` | `UInt64` | Users with >$0 monthly fees. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/revenue/revenue_gnosis_app_cohorts/monthly?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## revenue_gpay_cohorts

API view over fct_revenue_gpay_cohorts_weekly.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/revenue/revenue_gpay_cohorts/weekly` | GET | tier1 | `symbol`, `cohort`, `start_date`, `end_date` | -- | week DESC |
| `/v1/revenue/revenue_gpay_cohorts/monthly` | GET | tier1 | `symbol`, `cohort`, `start_date`, `end_date` | -- | month DESC |

??? info "`GET /v1/revenue/revenue_gpay_cohorts/weekly`"
    API view over fct_revenue_gpay_cohorts_weekly.

    Model: `api_revenue_gpay_cohorts_weekly` — table `dbt.api_revenue_gpay_cohorts_weekly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `symbol` | `=` | `symbol` | string | Token symbol (EURe, GBPe, USDC.e) |
    | `cohort` | `=` | `cohort` | string | Cohort bucket |
    | `start_date` | `>=` | `week` | date | Inclusive start week |
    | `end_date` | `<=` | `week` | date | Inclusive end week |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `week DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `week` | `Date` | Week start. |
    | `symbol` | `String` | Payment token (EURe, GBPe, USDC.e). |
    | `cohort` | `String` | Annualised $-bucket. |
    | `annual_rolling_fees_total` | `Float64` | Sum of rolling-52w fees for users in this cohort. |
    | `users_cnt` | `UInt64` | Users with >$0 rolling fees. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/revenue/revenue_gpay_cohorts/weekly?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/revenue/revenue_gpay_cohorts/monthly`"
    API view over fct_revenue_gpay_cohorts_monthly.

    Model: `api_revenue_gpay_cohorts_monthly` — table `dbt.api_revenue_gpay_cohorts_monthly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `symbol` | `=` | `symbol` | string | Token symbol (EURe, GBPe, USDC.e) |
    | `cohort` | `=` | `cohort` | string | Cohort bucket |
    | `start_date` | `>=` | `month` | date | Inclusive start month |
    | `end_date` | `<=` | `month` | date | Inclusive end month |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `month DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `month` | `Date` | First day of the month. |
    | `symbol` | `String` | Payment token. |
    | `cohort` | `String` | Monthly $-bucket. |
    | `fees_total` | `Float64` | Sum of monthly fees. |
    | `users_cnt` | `UInt64` | Users with >$0 monthly fees. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/revenue/revenue_gpay_cohorts/monthly?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## revenue_gpay_eure_cohorts

EURe Gnosis Pay rolling-52w cohort API view.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/revenue/revenue_gpay_eure_cohorts/weekly` | GET | tier1 | `cohort`, `start_date`, `end_date` | -- | week DESC |
| `/v1/revenue/revenue_gpay_eure_cohorts/monthly` | GET | tier1 | `cohort`, `start_date`, `end_date` | -- | month DESC |

??? info "`GET /v1/revenue/revenue_gpay_eure_cohorts/weekly`"
    EURe Gnosis Pay rolling-52w cohort API view.

    Model: `api_revenue_gpay_eure_cohorts_weekly` — table `dbt.api_revenue_gpay_eure_cohorts_weekly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `cohort` | `=` | `cohort` | string | Cohort bucket |
    | `start_date` | `>=` | `week` | date | Inclusive start week |
    | `end_date` | `<=` | `week` | date | Inclusive end week |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `week DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `week` | `Date` | Week start. |
    | `cohort` | `String` | Annualised $-bucket. |
    | `annual_rolling_fees_total` | `Float64` | Sum of rolling-52w fees for users in this cohort. |
    | `users_cnt` | `UInt64` | Users with >$0 rolling fees. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/revenue/revenue_gpay_eure_cohorts/weekly?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/revenue/revenue_gpay_eure_cohorts/monthly`"
    EURe Gnosis Pay monthly cohort API view.

    Model: `api_revenue_gpay_eure_cohorts_monthly` — table `dbt.api_revenue_gpay_eure_cohorts_monthly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `cohort` | `=` | `cohort` | string | Cohort bucket |
    | `start_date` | `>=` | `month` | date | Inclusive start month |
    | `end_date` | `<=` | `month` | date | Inclusive end month |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `month DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `month` | `Date` | First day of the month. |
    | `cohort` | `String` | Monthly $-bucket. |
    | `fees_total` | `Float64` | Sum of monthly fees. |
    | `users_cnt` | `UInt64` | Users with >$0 monthly fees. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/revenue/revenue_gpay_eure_cohorts/monthly?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## revenue_gpay_gbpe_cohorts

GBPe Gnosis Pay rolling-52w cohort API view.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/revenue/revenue_gpay_gbpe_cohorts/weekly` | GET | tier1 | `cohort`, `start_date`, `end_date` | -- | week DESC |
| `/v1/revenue/revenue_gpay_gbpe_cohorts/monthly` | GET | tier1 | `cohort`, `start_date`, `end_date` | -- | month DESC |

??? info "`GET /v1/revenue/revenue_gpay_gbpe_cohorts/weekly`"
    GBPe Gnosis Pay rolling-52w cohort API view.

    Model: `api_revenue_gpay_gbpe_cohorts_weekly` — table `dbt.api_revenue_gpay_gbpe_cohorts_weekly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `cohort` | `=` | `cohort` | string | Cohort bucket |
    | `start_date` | `>=` | `week` | date | Inclusive start week |
    | `end_date` | `<=` | `week` | date | Inclusive end week |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `week DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `week` | `Date` | Week start. |
    | `cohort` | `String` | Annualised $-bucket. |
    | `annual_rolling_fees_total` | `Float64` | Sum of rolling-52w fees for users in this cohort. |
    | `users_cnt` | `UInt64` | Users with >$0 rolling fees. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/revenue/revenue_gpay_gbpe_cohorts/weekly?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/revenue/revenue_gpay_gbpe_cohorts/monthly`"
    GBPe Gnosis Pay monthly cohort API view.

    Model: `api_revenue_gpay_gbpe_cohorts_monthly` — table `dbt.api_revenue_gpay_gbpe_cohorts_monthly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `cohort` | `=` | `cohort` | string | Cohort bucket |
    | `start_date` | `>=` | `month` | date | Inclusive start month |
    | `end_date` | `<=` | `month` | date | Inclusive end month |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `month DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `month` | `Date` | First day of the month. |
    | `cohort` | `String` | Monthly $-bucket. |
    | `fees_total` | `Float64` | Sum of monthly fees. |
    | `users_cnt` | `UInt64` | Users with >$0 monthly fees. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/revenue/revenue_gpay_gbpe_cohorts/monthly?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## revenue_gpay_usdce_cohorts

USDC.e Gnosis Pay rolling-52w cohort API view.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/revenue/revenue_gpay_usdce_cohorts/weekly` | GET | tier1 | `cohort`, `start_date`, `end_date` | -- | week DESC |
| `/v1/revenue/revenue_gpay_usdce_cohorts/monthly` | GET | tier1 | `cohort`, `start_date`, `end_date` | -- | month DESC |

??? info "`GET /v1/revenue/revenue_gpay_usdce_cohorts/weekly`"
    USDC.e Gnosis Pay rolling-52w cohort API view.

    Model: `api_revenue_gpay_usdce_cohorts_weekly` — table `dbt.api_revenue_gpay_usdce_cohorts_weekly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `cohort` | `=` | `cohort` | string | Cohort bucket |
    | `start_date` | `>=` | `week` | date | Inclusive start week |
    | `end_date` | `<=` | `week` | date | Inclusive end week |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `week DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `week` | `Date` | Week start. |
    | `cohort` | `String` | Annualised $-bucket. |
    | `annual_rolling_fees_total` | `Float64` | Sum of rolling-52w fees for users in this cohort. |
    | `users_cnt` | `UInt64` | Users with >$0 rolling fees. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/revenue/revenue_gpay_usdce_cohorts/weekly?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/revenue/revenue_gpay_usdce_cohorts/monthly`"
    USDC.e Gnosis Pay monthly cohort API view.

    Model: `api_revenue_gpay_usdce_cohorts_monthly` — table `dbt.api_revenue_gpay_usdce_cohorts_monthly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `cohort` | `=` | `cohort` | string | Cohort bucket |
    | `start_date` | `>=` | `month` | date | Inclusive start month |
    | `end_date` | `<=` | `month` | date | Inclusive end month |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `month DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `month` | `Date` | First day of the month. |
    | `cohort` | `String` | Monthly $-bucket. |
    | `fees_total` | `Float64` | Sum of monthly fees. |
    | `users_cnt` | `UInt64` | Users with >$0 monthly fees. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/revenue/revenue_gpay_usdce_cohorts/monthly?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## revenue_holdings_brla_cohorts

BRLA holdings rolling-52w cohort API view.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/revenue/revenue_holdings_brla_cohorts/weekly` | GET | tier1 | `cohort`, `start_date`, `end_date` | -- | week DESC |
| `/v1/revenue/revenue_holdings_brla_cohorts/monthly` | GET | tier1 | `cohort`, `start_date`, `end_date` | -- | month DESC |

??? info "`GET /v1/revenue/revenue_holdings_brla_cohorts/weekly`"
    BRLA holdings rolling-52w cohort API view.

    Model: `api_revenue_holdings_brla_cohorts_weekly` — table `dbt.api_revenue_holdings_brla_cohorts_weekly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `cohort` | `=` | `cohort` | string | Cohort bucket |
    | `start_date` | `>=` | `week` | date | Inclusive start week |
    | `end_date` | `<=` | `week` | date | Inclusive end week |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `week DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `week` | `Date` | Week start. |
    | `cohort` | `String` | Annualised $-bucket for user's rolling fees. |
    | `annual_rolling_fees_total` | `Float64` | Sum of rolling-52w fees for users in this cohort. |
    | `users_cnt` | `UInt64` | Number of users with >$0 rolling fees in cohort. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/revenue/revenue_holdings_brla_cohorts/weekly?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/revenue/revenue_holdings_brla_cohorts/monthly`"
    BRLA holdings monthly cohort API view.

    Model: `api_revenue_holdings_brla_cohorts_monthly` — table `dbt.api_revenue_holdings_brla_cohorts_monthly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `cohort` | `=` | `cohort` | string | Cohort bucket |
    | `start_date` | `>=` | `month` | date | Inclusive start month |
    | `end_date` | `<=` | `month` | date | Inclusive end month |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `month DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `month` | `Date` | First day of the month. |
    | `cohort` | `String` | Monthly $-bucket for user's monthly fees. |
    | `fees_total` | `Float64` | Sum of monthly fees for users in this cohort. |
    | `users_cnt` | `UInt64` | Number of users with >$0 monthly fees in cohort. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/revenue/revenue_holdings_brla_cohorts/monthly?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## revenue_holdings_cohorts

API view over fct_revenue_holdings_cohorts_weekly.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/revenue/revenue_holdings_cohorts/weekly` | GET | tier1 | `symbol`, `cohort`, `start_date`, `end_date` | -- | week DESC |
| `/v1/revenue/revenue_holdings_cohorts/monthly` | GET | tier1 | `symbol`, `cohort`, `start_date`, `end_date` | -- | month DESC |

??? info "`GET /v1/revenue/revenue_holdings_cohorts/weekly`"
    API view over fct_revenue_holdings_cohorts_weekly.

    Model: `api_revenue_holdings_cohorts_weekly` — table `dbt.api_revenue_holdings_cohorts_weekly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `symbol` | `=` | `symbol` | string | Token symbol (EURe, USDC.e, BRLA, ZCHF) |
    | `cohort` | `=` | `cohort` | string | Cohort bucket |
    | `start_date` | `>=` | `week` | date | Inclusive start week |
    | `end_date` | `<=` | `week` | date | Inclusive end week |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `week DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `week` | `Date` | Week start. |
    | `symbol` | `String` | Canonical token symbol. |
    | `cohort` | `String` | Annualised $-bucket for user's rolling fees. |
    | `annual_rolling_fees_total` | `Float64` | Sum of rolling-52w fees for users in this cohort. |
    | `users_cnt` | `UInt64` | Number of users with >$0 rolling fees in cohort. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/revenue/revenue_holdings_cohorts/weekly?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/revenue/revenue_holdings_cohorts/monthly`"
    API view over fct_revenue_holdings_cohorts_monthly.

    Model: `api_revenue_holdings_cohorts_monthly` — table `dbt.api_revenue_holdings_cohorts_monthly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `symbol` | `=` | `symbol` | string | Token symbol (EURe, USDC.e, BRLA, ZCHF) |
    | `cohort` | `=` | `cohort` | string | Cohort bucket |
    | `start_date` | `>=` | `month` | date | Inclusive start month |
    | `end_date` | `<=` | `month` | date | Inclusive end month |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `month DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `month` | `Date` | First day of the month. |
    | `symbol` | `String` | Canonical token symbol. |
    | `cohort` | `String` | Monthly $-bucket for user's monthly fees. |
    | `fees_total` | `Float64` | Sum of monthly fees for users in this cohort. |
    | `users_cnt` | `UInt64` | Number of users with >$0 monthly fees in cohort. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/revenue/revenue_holdings_cohorts/monthly?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## revenue_holdings_eure_cohorts

EURe holdings rolling-52w cohort API view.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/revenue/revenue_holdings_eure_cohorts/weekly` | GET | tier1 | `cohort`, `start_date`, `end_date` | -- | week DESC |
| `/v1/revenue/revenue_holdings_eure_cohorts/monthly` | GET | tier1 | `cohort`, `start_date`, `end_date` | -- | month DESC |

??? info "`GET /v1/revenue/revenue_holdings_eure_cohorts/weekly`"
    EURe holdings rolling-52w cohort API view.

    Model: `api_revenue_holdings_eure_cohorts_weekly` — table `dbt.api_revenue_holdings_eure_cohorts_weekly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `cohort` | `=` | `cohort` | string | Cohort bucket |
    | `start_date` | `>=` | `week` | date | Inclusive start week |
    | `end_date` | `<=` | `week` | date | Inclusive end week |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `week DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `week` | `Date` | Week start. |
    | `cohort` | `String` | Annualised $-bucket for user's rolling fees. |
    | `annual_rolling_fees_total` | `Float64` | Sum of rolling-52w fees for users in this cohort. |
    | `users_cnt` | `UInt64` | Number of users with >$0 rolling fees in cohort. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/revenue/revenue_holdings_eure_cohorts/weekly?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/revenue/revenue_holdings_eure_cohorts/monthly`"
    EURe holdings monthly cohort API view.

    Model: `api_revenue_holdings_eure_cohorts_monthly` — table `dbt.api_revenue_holdings_eure_cohorts_monthly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `cohort` | `=` | `cohort` | string | Cohort bucket |
    | `start_date` | `>=` | `month` | date | Inclusive start month |
    | `end_date` | `<=` | `month` | date | Inclusive end month |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `month DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `month` | `Date` | First day of the month. |
    | `cohort` | `String` | Monthly $-bucket for user's monthly fees. |
    | `fees_total` | `Float64` | Sum of monthly fees for users in this cohort. |
    | `users_cnt` | `UInt64` | Number of users with >$0 monthly fees in cohort. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/revenue/revenue_holdings_eure_cohorts/monthly?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## revenue_holdings_usdce_cohorts

USDC.e holdings rolling-52w cohort API view.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/revenue/revenue_holdings_usdce_cohorts/weekly` | GET | tier1 | `cohort`, `start_date`, `end_date` | -- | week DESC |
| `/v1/revenue/revenue_holdings_usdce_cohorts/monthly` | GET | tier1 | `cohort`, `start_date`, `end_date` | -- | month DESC |

??? info "`GET /v1/revenue/revenue_holdings_usdce_cohorts/weekly`"
    USDC.e holdings rolling-52w cohort API view.

    Model: `api_revenue_holdings_usdce_cohorts_weekly` — table `dbt.api_revenue_holdings_usdce_cohorts_weekly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `cohort` | `=` | `cohort` | string | Cohort bucket |
    | `start_date` | `>=` | `week` | date | Inclusive start week |
    | `end_date` | `<=` | `week` | date | Inclusive end week |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `week DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `week` | `Date` | Week start. |
    | `cohort` | `String` | Annualised $-bucket for user's rolling fees. |
    | `annual_rolling_fees_total` | `Float64` | Sum of rolling-52w fees for users in this cohort. |
    | `users_cnt` | `UInt64` | Number of users with >$0 rolling fees in cohort. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/revenue/revenue_holdings_usdce_cohorts/weekly?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/revenue/revenue_holdings_usdce_cohorts/monthly`"
    USDC.e holdings monthly cohort API view.

    Model: `api_revenue_holdings_usdce_cohorts_monthly` — table `dbt.api_revenue_holdings_usdce_cohorts_monthly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `cohort` | `=` | `cohort` | string | Cohort bucket |
    | `start_date` | `>=` | `month` | date | Inclusive start month |
    | `end_date` | `<=` | `month` | date | Inclusive end month |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `month DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `month` | `Date` | First day of the month. |
    | `cohort` | `String` | Monthly $-bucket for user's monthly fees. |
    | `fees_total` | `Float64` | Sum of monthly fees for users in this cohort. |
    | `users_cnt` | `UInt64` | Number of users with >$0 monthly fees in cohort. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/revenue/revenue_holdings_usdce_cohorts/monthly?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## revenue_holdings_zchf_cohorts

ZCHF holdings rolling-52w cohort API view.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/revenue/revenue_holdings_zchf_cohorts/weekly` | GET | tier1 | `cohort`, `start_date`, `end_date` | -- | week DESC |
| `/v1/revenue/revenue_holdings_zchf_cohorts/monthly` | GET | tier1 | `cohort`, `start_date`, `end_date` | -- | month DESC |

??? info "`GET /v1/revenue/revenue_holdings_zchf_cohorts/weekly`"
    ZCHF holdings rolling-52w cohort API view.

    Model: `api_revenue_holdings_zchf_cohorts_weekly` — table `dbt.api_revenue_holdings_zchf_cohorts_weekly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `cohort` | `=` | `cohort` | string | Cohort bucket |
    | `start_date` | `>=` | `week` | date | Inclusive start week |
    | `end_date` | `<=` | `week` | date | Inclusive end week |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `week DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `week` | `Date` | Week start. |
    | `cohort` | `String` | Annualised $-bucket for user's rolling fees. |
    | `annual_rolling_fees_total` | `Float64` | Sum of rolling-52w fees for users in this cohort. |
    | `users_cnt` | `UInt64` | Number of users with >$0 rolling fees in cohort. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/revenue/revenue_holdings_zchf_cohorts/weekly?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/revenue/revenue_holdings_zchf_cohorts/monthly`"
    ZCHF holdings monthly cohort API view.

    Model: `api_revenue_holdings_zchf_cohorts_monthly` — table `dbt.api_revenue_holdings_zchf_cohorts_monthly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `cohort` | `=` | `cohort` | string | Cohort bucket |
    | `start_date` | `>=` | `month` | date | Inclusive start month |
    | `end_date` | `<=` | `month` | date | Inclusive end month |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `month DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `month` | `Date` | First day of the month. |
    | `cohort` | `String` | Monthly $-bucket for user's monthly fees. |
    | `fees_total` | `Float64` | Sum of monthly fees for users in this cohort. |
    | `users_cnt` | `UInt64` | Number of users with >$0 monthly fees in cohort. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/revenue/revenue_holdings_zchf_cohorts/monthly?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## revenue_per_user

API view over fct_revenue_per_user_weekly. Per-user weekly revenue keyed on `user_pseudonym` — the canonical join key for cross-sector user-overlap queries. Filterable by week range and `is_revenue_active`.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/revenue/revenue_per_user/weekly` | GET | tier3 | `start_week`, `end_week`, `is_revenue_active` | -- | week DESC |
| `/v1/revenue/revenue_per_user/monthly` | GET | tier3 | `start_month`, `end_month`, `is_revenue_active` | -- | month DESC |

??? info "`GET /v1/revenue/revenue_per_user/weekly`"
    API view over fct_revenue_per_user_weekly. Per-user weekly revenue keyed on `user_pseudonym` — the canonical join key for cross-sector user-overlap queries. Filterable by week range and `is_revenue_active`.

    Model: `api_revenue_per_user_weekly` — table `dbt.api_revenue_per_user_weekly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `start_week` | `>=` | `week` | date | Inclusive start week |
    | `end_week` | `<=` | `week` | date | Inclusive end week |
    | `is_revenue_active` | `=` | `is_revenue_active` | string | Filter to users above the $6 / 52w threshold (1 or 0) |

    **Filter policy:** At least one filter required.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `week DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `week` | `Date` | ISO week start (Monday). |
    | `user_pseudonym` | `UInt64` | Cross-sector pseudonym (sipHash64 of lowercased address). |
    | `rolling_fees_total` | `Float64` | Sum of 52w-rolling potential revenue across all streams (USD). |
    | `has_holdings` | `UInt8` | 1 if user has any rolling fees from the holdings stream. |
    | `has_sdai` | `UInt8` | 1 if user has any rolling fees from the sDAI stream. |
    | `has_gpay` | `UInt8` | 1 if user has any rolling fees from the Gnosis Pay stream. |
    | `has_gnosis_app` | `UInt8` | 1 if user has any rolling fees from the Gnosis App stream. |
    | `n_streams` | `UInt8` | Number of distinct streams the user accrued fees in. |
    | `is_revenue_active` | `UInt8` | 1 iff rolling_fees_total >= $6 (Dune active-user threshold). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/revenue/revenue_per_user/weekly?start_week=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/revenue/revenue_per_user/monthly`"
    API view over fct_revenue_per_user_monthly. Per-user monthly revenue keyed on `user_pseudonym`. Filterable by month range and `is_revenue_active`.

    Model: `api_revenue_per_user_monthly` — table `dbt.api_revenue_per_user_monthly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `start_month` | `>=` | `month` | date | Inclusive start month |
    | `end_month` | `<=` | `month` | date | Inclusive end month |
    | `is_revenue_active` | `=` | `is_revenue_active` | string | Filter to users above the $0.50 / month threshold (1 or 0) |

    **Filter policy:** At least one filter required.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `month DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `month` | `Date` | First day of the calendar month. |
    | `user_pseudonym` | `UInt64` | Cross-sector pseudonym (sipHash64). |
    | `month_fees_total` | `Float64` | Sum of monthly potential revenue across all streams (USD). |
    | `has_holdings` | `UInt8` | 1 if user had holdings-stream fees this month. |
    | `has_sdai` | `UInt8` | 1 if user had sDAI-stream fees this month. |
    | `has_gpay` | `UInt8` | 1 if user had Gnosis Pay-stream fees this month. |
    | `has_gnosis_app` | `UInt8` | 1 if user had Gnosis App-stream fees this month. |
    | `n_streams` | `UInt8` | Number of distinct streams contributing in the month. |
    | `is_revenue_active` | `UInt8` | 1 iff month_fees_total >= $0.50 (month-scaled $6 threshold). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/revenue/revenue_per_user/monthly?start_month=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## revenue_sdai_cohorts

API view over fct_revenue_sdai_cohorts_weekly.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/revenue/revenue_sdai_cohorts/weekly` | GET | tier1 | `cohort`, `start_date`, `end_date` | -- | week DESC |
| `/v1/revenue/revenue_sdai_cohorts/monthly` | GET | tier1 | `cohort`, `start_date`, `end_date` | -- | month DESC |

??? info "`GET /v1/revenue/revenue_sdai_cohorts/weekly`"
    API view over fct_revenue_sdai_cohorts_weekly.

    Model: `api_revenue_sdai_cohorts_weekly` — table `dbt.api_revenue_sdai_cohorts_weekly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `cohort` | `=` | `cohort` | string | Cohort bucket |
    | `start_date` | `>=` | `week` | date | Inclusive start week |
    | `end_date` | `<=` | `week` | date | Inclusive end week |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `week DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `week` | `Date` | Week start. |
    | `cohort` | `String` | Annualised $-bucket. |
    | `annual_rolling_fees_total` | `Float64` | Sum of rolling-52w fees for users in this cohort. |
    | `users_cnt` | `UInt64` | Users with >$0 rolling fees. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/revenue/revenue_sdai_cohorts/weekly?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/revenue/revenue_sdai_cohorts/monthly`"
    API view over fct_revenue_sdai_cohorts_monthly.

    Model: `api_revenue_sdai_cohorts_monthly` — table `dbt.api_revenue_sdai_cohorts_monthly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `cohort` | `=` | `cohort` | string | Cohort bucket |
    | `start_date` | `>=` | `month` | date | Inclusive start month |
    | `end_date` | `<=` | `month` | date | Inclusive end month |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `month DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `month` | `Date` | First day of the month. |
    | `cohort` | `String` | Monthly $-bucket. |
    | `fees_total` | `Float64` | Sum of monthly fees for users in this cohort. |
    | `users_cnt` | `UInt64` | Users with >$0 monthly fees. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/revenue/revenue_sdai_cohorts/monthly?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```
<!-- END AUTO-GENERATED: api-catalog-revenue -->
