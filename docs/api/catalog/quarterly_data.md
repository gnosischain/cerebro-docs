# Quarterly Data API Endpoints

<!-- BEGIN AUTO-GENERATED: api-catalog-quarterly_data -->
_24 endpoints across 24 resources. Generated from the dbt manifest — edits inside this block will be overwritten. Regenerate with `python scripts/update_docs.py --only api`._

## carbon_emissions

Quarterly annualised CO2 emissions (tonnes/yr) from end-of-quarter snapshot, with estimation flag for periods using forward-filled carbon intensity.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/quarterly_data/carbon_emissions/quarterly` | GET, POST | tier0 | `quarter_from`, `quarter_to` | limit/offset (envelope) | quarter DESC |

??? info "`GET/POST /v1/quarterly_data/carbon_emissions/quarterly`"
    Quarterly annualised CO2 emissions (tonnes/yr) from end-of-quarter snapshot, with estimation flag for periods using forward-filled carbon intensity.

    Model: `api_quarterly_data_carbon_emissions` — table `dbt.api_quarterly_data_carbon_emissions`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `quarter_from` | `>=` | `quarter` | date | Inclusive lower bound on quarter start date (e.g. 2024-01-01 for 2024-Q1) |
    | `quarter_to` | `<=` | `quarter` | date | Inclusive upper bound on quarter start date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** `limit`/`offset` — default 200, max 1000; response: envelope `{items, pagination}`

    **Sort:** `quarter DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `quarter` | `Date` | Quarter start date. |
    | `co2_tonnes_yr` | `Float64` | Annualised CO2 emissions in tonnes per year at end of quarter. |
    | `is_estimated` | `Bool` | True if the quarter's value uses forward-filled carbon intensity data. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/quarterly_data/carbon_emissions/quarterly?quarter_from=2026-01-01"
    ```

## circles_active_minters

Quarterly peak of blacklist-excluded Circles v2 Active Minters (the +80% mint-coverage cohort). Matches the Dune circles-v2-kpis active-minters peak.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/quarterly_data/circles_active_minters/quarterly` | GET, POST | tier0 | `quarter_from`, `quarter_to` | limit/offset (envelope) | quarter DESC |

??? info "`GET/POST /v1/quarterly_data/circles_active_minters/quarterly`"
    Quarterly peak of blacklist-excluded Circles v2 Active Minters (the +80% mint-coverage cohort). Matches the Dune circles-v2-kpis active-minters peak.

    Model: `api_quarterly_data_circles_active_minters` — table `dbt.api_quarterly_data_circles_active_minters`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `quarter_from` | `>=` | `quarter` | date | Inclusive lower bound on quarter start date (e.g. 2024-01-01 for 2024-Q1) |
    | `quarter_to` | `<=` | `quarter` | date | Inclusive upper bound on quarter start date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** `limit`/`offset` — default 200, max 1000; response: envelope `{items, pagination}`

    **Sort:** `quarter DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `quarter` | `Date` | Quarter start date. |
    | `active_minters_peak` | `UInt64` | Highest daily blacklist-excluded active-minter count within the quarter. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/quarterly_data/circles_active_minters/quarterly?quarter_from=2026-01-01"
    ```

## circles_active_trusts

End-of-quarter active trust links in Circles v2.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/quarterly_data/circles_active_trusts/quarterly` | GET, POST | tier0 | `quarter_from`, `quarter_to` | limit/offset (envelope) | quarter DESC |

??? info "`GET/POST /v1/quarterly_data/circles_active_trusts/quarterly`"
    End-of-quarter active trust links in Circles v2.

    Model: `api_quarterly_data_circles_active_trusts` — table `dbt.api_quarterly_data_circles_active_trusts`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `quarter_from` | `>=` | `quarter` | date | Inclusive lower bound on quarter start date (e.g. 2024-01-01 for 2024-Q1) |
    | `quarter_to` | `<=` | `quarter` | date | Inclusive upper bound on quarter start date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** `limit`/`offset` — default 200, max 1000; response: envelope `{items, pagination}`

    **Sort:** `quarter DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `quarter` | `Date` | Quarter start date. |
    | `active_trusts` | `UInt64` | Total active trust links at end of quarter. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/quarterly_data/circles_active_trusts/quarterly?quarter_from=2026-01-01"
    ```

## circles_backers

Quarterly currently-trusted Circles backers, as of quarter end (revocation-aware). A backer is an address currently trusted by the backers group avatar var('circles_target_group_address'); trust is revocable, so this count can fall. Distinct from the ever-backed cumulative series (api:circles_v2_...

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/quarterly_data/circles_backers/quarterly` | GET, POST | tier0 | `quarter_from`, `quarter_to` | limit/offset (envelope) | quarter DESC |

??? info "`GET/POST /v1/quarterly_data/circles_backers/quarterly`"
    Quarterly currently-trusted Circles backers, as of quarter end (revocation-aware). A backer is an address currently trusted by the backers group avatar var('circles_target_group_address'); trust is revocable, so this count can fall. Distinct from the ever-backed cumulative series (api:circles_v2_...

    Model: `api_quarterly_data_circles_backers` — table `dbt.api_quarterly_data_circles_backers`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `quarter_from` | `>=` | `quarter` | date | Inclusive lower bound on quarter start date (e.g. 2024-01-01 for 2024-Q1) |
    | `quarter_to` | `<=` | `quarter` | date | Inclusive upper bound on quarter start date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** `limit`/`offset` — default 200, max 1000; response: envelope `{items, pagination}`

    **Sort:** `quarter DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `quarter` | `Date` | Quarter start date. |
    | `total_backers` | `UInt64` | Distinct backers currently trusted by the backers group as of the quarter's last day. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/quarterly_data/circles_backers/quarterly?quarter_from=2026-01-01"
    ```

## circles_humans

End-of-quarter total registered human avatars in Circles v2.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/quarterly_data/circles_humans/quarterly` | GET, POST | tier0 | `quarter_from`, `quarter_to` | limit/offset (envelope) | quarter DESC |

??? info "`GET/POST /v1/quarterly_data/circles_humans/quarterly`"
    End-of-quarter total registered human avatars in Circles v2.

    Model: `api_quarterly_data_circles_humans` — table `dbt.api_quarterly_data_circles_humans`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `quarter_from` | `>=` | `quarter` | date | Inclusive lower bound on quarter start date (e.g. 2024-01-01 for 2024-Q1) |
    | `quarter_to` | `<=` | `quarter` | date | Inclusive upper bound on quarter start date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** `limit`/`offset` — default 200, max 1000; response: envelope `{items, pagination}`

    **Sort:** `quarter DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `quarter` | `Date` | Quarter start date. |
    | `registered_humans` | `UInt64` | Cumulative count of registered human avatars at end of quarter. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/quarterly_data/circles_humans/quarterly?quarter_from=2026-01-01"
    ```

## circles_total_supply

End-of-quarter Circles v2 token supply (raw and demurraged).

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/quarterly_data/circles_total_supply/quarterly` | GET, POST | tier0 | `quarter_from`, `quarter_to` | limit/offset (envelope) | quarter DESC |

??? info "`GET/POST /v1/quarterly_data/circles_total_supply/quarterly`"
    End-of-quarter Circles v2 token supply (raw and demurraged).

    Model: `api_quarterly_data_circles_total_supply` — table `dbt.api_quarterly_data_circles_total_supply`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `quarter_from` | `>=` | `quarter` | date | Inclusive lower bound on quarter start date (e.g. 2024-01-01 for 2024-Q1) |
    | `quarter_to` | `<=` | `quarter` | date | Inclusive upper bound on quarter start date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** `limit`/`offset` — default 200, max 1000; response: envelope `{items, pagination}`

    **Sort:** `quarter DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `quarter` | `Date` | Quarter start date. |
    | `total_supply` | `Float64` | Total CRC token supply at end of quarter. |
    | `total_supply_demurraged` | `Float64` | Total CRC token supply after demurrage at end of quarter. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/quarterly_data/circles_total_supply/quarterly?quarter_from=2026-01-01"
    ```

## energy_consumption

Quarterly annualised energy consumption (MWh/yr) from end-of-quarter snapshot, with estimation flag for periods using forward-filled carbon intensity.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/quarterly_data/energy_consumption/quarterly` | GET, POST | tier0 | `quarter_from`, `quarter_to` | limit/offset (envelope) | quarter DESC |

??? info "`GET/POST /v1/quarterly_data/energy_consumption/quarterly`"
    Quarterly annualised energy consumption (MWh/yr) from end-of-quarter snapshot, with estimation flag for periods using forward-filled carbon intensity.

    Model: `api_quarterly_data_energy_consumption` — table `dbt.api_quarterly_data_energy_consumption`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `quarter_from` | `>=` | `quarter` | date | Inclusive lower bound on quarter start date (e.g. 2024-01-01 for 2024-Q1) |
    | `quarter_to` | `<=` | `quarter` | date | Inclusive upper bound on quarter start date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** `limit`/`offset` — default 200, max 1000; response: envelope `{items, pagination}`

    **Sort:** `quarter DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `quarter` | `Date` | Quarter start date. |
    | `energy_mwh_yr` | `Float64` | Annualised energy consumption in MWh per year at end of quarter. |
    | `is_estimated` | `Bool` | True if the quarter's value uses forward-filled carbon intensity data. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/quarterly_data/energy_consumption/quarterly?quarter_from=2026-01-01"
    ```

## gnosis_app_peak_swappers

Peak daily unique swappers on Gnosis App within the quarter.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/quarterly_data/gnosis_app_peak_swappers/quarterly` | GET, POST | tier0 | `quarter_from`, `quarter_to` | limit/offset (envelope) | quarter DESC |

??? info "`GET/POST /v1/quarterly_data/gnosis_app_peak_swappers/quarterly`"
    Peak daily unique swappers on Gnosis App within the quarter.

    Model: `api_quarterly_data_gnosis_app_peak_swappers` — table `dbt.api_quarterly_data_gnosis_app_peak_swappers`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `quarter_from` | `>=` | `quarter` | date | Inclusive lower bound on quarter start date (e.g. 2024-01-01 for 2024-Q1) |
    | `quarter_to` | `<=` | `quarter` | date | Inclusive upper bound on quarter start date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** `limit`/`offset` — default 200, max 1000; response: envelope `{items, pagination}`

    **Sort:** `quarter DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `quarter` | `Date` | Quarter start date. |
    | `peak_daily_swappers` | `UInt64` | Highest daily count of unique swap users in the quarter. |
    | `peak_date` | `Date` | Calendar day (UTC) on which the peak daily swapper count occurred. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/quarterly_data/gnosis_app_peak_swappers/quarterly?quarter_from=2026-01-01"
    ```

## gnosis_app_swap_volume

Total swap volume in USD on Gnosis App per quarter.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/quarterly_data/gnosis_app_swap_volume/quarterly` | GET, POST | tier0 | `quarter_from`, `quarter_to` | limit/offset (envelope) | quarter DESC |

??? info "`GET/POST /v1/quarterly_data/gnosis_app_swap_volume/quarterly`"
    Total swap volume in USD on Gnosis App per quarter.

    Model: `api_quarterly_data_gnosis_app_swap_volume` — table `dbt.api_quarterly_data_gnosis_app_swap_volume`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `quarter_from` | `>=` | `quarter` | date | Inclusive lower bound on quarter start date (e.g. 2024-01-01 for 2024-Q1) |
    | `quarter_to` | `<=` | `quarter` | date | Inclusive upper bound on quarter start date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** `limit`/`offset` — default 200, max 1000; response: envelope `{items, pagination}`

    **Sort:** `quarter DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `quarter` | `Date` | Quarter start date. |
    | `volume_usd` | `Float64` | Sum of filled swap volume in USD during the quarter. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/quarterly_data/gnosis_app_swap_volume/quarterly?quarter_from=2026-01-01"
    ```

## gnosis_app_swaps

Total swap transactions on Gnosis App per quarter.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/quarterly_data/gnosis_app_swaps/quarterly` | GET, POST | tier0 | `quarter_from`, `quarter_to` | limit/offset (envelope) | quarter DESC |

??? info "`GET/POST /v1/quarterly_data/gnosis_app_swaps/quarterly`"
    Total swap transactions on Gnosis App per quarter.

    Model: `api_quarterly_data_gnosis_app_swaps` — table `dbt.api_quarterly_data_gnosis_app_swaps`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `quarter_from` | `>=` | `quarter` | date | Inclusive lower bound on quarter start date (e.g. 2024-01-01 for 2024-Q1) |
    | `quarter_to` | `<=` | `quarter` | date | Inclusive upper bound on quarter start date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** `limit`/`offset` — default 200, max 1000; response: envelope `{items, pagination}`

    **Sort:** `quarter DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `quarter` | `Date` | Quarter start date. |
    | `swaps` | `UInt64` | Total number of swap transactions in the quarter. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/quarterly_data/gnosis_app_swaps/quarterly?quarter_from=2026-01-01"
    ```

## gnosis_app_swaps_filled

Total filled swap transactions on Gnosis App per quarter.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/quarterly_data/gnosis_app_swaps_filled/quarterly` | GET, POST | tier0 | `quarter_from`, `quarter_to` | limit/offset (envelope) | quarter DESC |

??? info "`GET/POST /v1/quarterly_data/gnosis_app_swaps_filled/quarterly`"
    Total filled swap transactions on Gnosis App per quarter.

    Model: `api_quarterly_data_gnosis_app_swaps_filled` — table `dbt.api_quarterly_data_gnosis_app_swaps_filled`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `quarter_from` | `>=` | `quarter` | date | Inclusive lower bound on quarter start date (e.g. 2024-01-01 for 2024-Q1) |
    | `quarter_to` | `<=` | `quarter` | date | Inclusive upper bound on quarter start date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** `limit`/`offset` — default 200, max 1000; response: envelope `{items, pagination}`

    **Sort:** `quarter DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `quarter` | `Date` | Quarter start date. |
    | `swaps_filled` | `UInt64` | Total number of filled swap transactions in the quarter. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/quarterly_data/gnosis_app_swaps_filled/quarterly?quarter_from=2026-01-01"
    ```

## gpay_active_users

Peak monthly active users for Gnosis Pay within the quarter, on two bases: all-activity (peak_monthly_active_users) and payment-only (peak_monthly_payment_users). The payment basis is the one the quarterly report uses; the all-activity basis is inflated in June 2026 by the Safe-migration deposit/...

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/quarterly_data/gpay_active_users/quarterly` | GET, POST | tier0 | `quarter_from`, `quarter_to` | limit/offset (envelope) | quarter DESC |

??? info "`GET/POST /v1/quarterly_data/gpay_active_users/quarterly`"
    Peak monthly active users for Gnosis Pay within the quarter, on two bases: all-activity (peak_monthly_active_users) and payment-only (peak_monthly_payment_users). The payment basis is the one the quarterly report uses; the all-activity basis is inflated in June 2026 by the Safe-migration deposit/...

    Model: `api_quarterly_data_gpay_active_users` — table `dbt.api_quarterly_data_gpay_active_users`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `quarter_from` | `>=` | `quarter` | date | Inclusive lower bound on quarter start date (e.g. 2024-01-01 for 2024-Q1) |
    | `quarter_to` | `<=` | `quarter` | date | Inclusive upper bound on quarter start date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** `limit`/`offset` — default 200, max 1000; response: envelope `{items, pagination}`

    **Sort:** `quarter DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `quarter` | `Date` | Quarter start date. |
    | `peak_monthly_active_users` | `UInt64` | Highest monthly all-activity active-user count across the quarter's three months (any of payment, deposit, withdrawal, cashback). |
    | `peak_monthly_payment_users` | `UInt64` | Highest monthly payment-active user count across the quarter's three months (distinct addresses making >=1 card payment; excludes deposit/withdrawal-only act... |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/quarterly_data/gpay_active_users/quarterly?quarter_from=2026-01-01"
    ```

## gpay_cashback

Total Gnosis Pay cashback in USD per quarter.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/quarterly_data/gpay_cashback/quarterly` | GET, POST | tier0 | `quarter_from`, `quarter_to` | limit/offset (envelope) | quarter DESC |

??? info "`GET/POST /v1/quarterly_data/gpay_cashback/quarterly`"
    Total Gnosis Pay cashback in USD per quarter.

    Model: `api_quarterly_data_gpay_cashback` — table `dbt.api_quarterly_data_gpay_cashback`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `quarter_from` | `>=` | `quarter` | date | Inclusive lower bound on quarter start date (e.g. 2024-01-01 for 2024-Q1) |
    | `quarter_to` | `<=` | `quarter` | date | Inclusive upper bound on quarter start date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** `limit`/`offset` — default 200, max 1000; response: envelope `{items, pagination}`

    **Sort:** `quarter DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `quarter` | `Date` | Quarter start date. |
    | `cashback_usd` | `Float64` | Sum of cashback paid in USD during the quarter. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/quarterly_data/gpay_cashback/quarterly?quarter_from=2026-01-01"
    ```

## gpay_payments

Total Gnosis Pay payment transactions per quarter.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/quarterly_data/gpay_payments/quarterly` | GET, POST | tier0 | `quarter_from`, `quarter_to` | limit/offset (envelope) | quarter DESC |

??? info "`GET/POST /v1/quarterly_data/gpay_payments/quarterly`"
    Total Gnosis Pay payment transactions per quarter.

    Model: `api_quarterly_data_gpay_payments` — table `dbt.api_quarterly_data_gpay_payments`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `quarter_from` | `>=` | `quarter` | date | Inclusive lower bound on quarter start date (e.g. 2024-01-01 for 2024-Q1) |
    | `quarter_to` | `<=` | `quarter` | date | Inclusive upper bound on quarter start date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** `limit`/`offset` — default 200, max 1000; response: envelope `{items, pagination}`

    **Sort:** `quarter DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `quarter` | `Date` | Quarter start date. |
    | `payments` | `UInt64` | Total number of payment transactions in the quarter. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/quarterly_data/gpay_payments/quarterly?quarter_from=2026-01-01"
    ```

## gpay_volume

Total Gnosis Pay payment volume in USD per quarter.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/quarterly_data/gpay_volume/quarterly` | GET, POST | tier0 | `quarter_from`, `quarter_to` | limit/offset (envelope) | quarter DESC |

??? info "`GET/POST /v1/quarterly_data/gpay_volume/quarterly`"
    Total Gnosis Pay payment volume in USD per quarter.

    Model: `api_quarterly_data_gpay_volume` — table `dbt.api_quarterly_data_gpay_volume`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `quarter_from` | `>=` | `quarter` | date | Inclusive lower bound on quarter start date (e.g. 2024-01-01 for 2024-Q1) |
    | `quarter_to` | `<=` | `quarter` | date | Inclusive upper bound on quarter start date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** `limit`/`offset` — default 200, max 1000; response: envelope `{items, pagination}`

    **Sort:** `quarter DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `quarter` | `Date` | Quarter start date. |
    | `volume_usd` | `Float64` | Sum of payment volume in USD during the quarter. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/quarterly_data/gpay_volume/quarterly?quarter_from=2026-01-01"
    ```

## nodes_estimated

Quarterly end-of-quarter estimated total node count (observed + unobserved) with 95% confidence interval, sourced from the node classification model.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/quarterly_data/nodes_estimated/quarterly` | GET, POST | tier0 | `quarter_from`, `quarter_to` | limit/offset (envelope) | quarter DESC |

??? info "`GET/POST /v1/quarterly_data/nodes_estimated/quarterly`"
    Quarterly end-of-quarter estimated total node count (observed + unobserved) with 95% confidence interval, sourced from the node classification model.

    Model: `api_quarterly_data_nodes_estimated` — table `dbt.api_quarterly_data_nodes_estimated`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `quarter_from` | `>=` | `quarter` | date | Inclusive lower bound on quarter start date (e.g. 2024-01-01 for 2024-Q1) |
    | `quarter_to` | `<=` | `quarter` | date | Inclusive upper bound on quarter start date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** `limit`/`offset` — default 200, max 1000; response: envelope `{items, pagination}`

    **Sort:** `quarter DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `quarter` | `Date` | Quarter start date. |
    | `nodes_estimated` | `UInt64` | Total estimated nodes at end of quarter (sum across all categories). |
    | `nodes_lower_95` | `UInt64` | Lower bound of 95% confidence interval for total nodes. |
    | `nodes_upper_95` | `UInt64` | Upper bound of 95% confidence interval for total nodes. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/quarterly_data/nodes_estimated/quarterly?quarter_from=2026-01-01"
    ```

## nodes_observed

Quarterly end-of-quarter observed (directly reachable) node count from the node classification model.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/quarterly_data/nodes_observed/quarterly` | GET, POST | tier0 | `quarter_from`, `quarter_to` | limit/offset (envelope) | quarter DESC |

??? info "`GET/POST /v1/quarterly_data/nodes_observed/quarterly`"
    Quarterly end-of-quarter observed (directly reachable) node count from the node classification model.

    Model: `api_quarterly_data_nodes_observed` — table `dbt.api_quarterly_data_nodes_observed`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `quarter_from` | `>=` | `quarter` | date | Inclusive lower bound on quarter start date (e.g. 2024-01-01 for 2024-Q1) |
    | `quarter_to` | `<=` | `quarter` | date | Inclusive upper bound on quarter start date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** `limit`/`offset` — default 200, max 1000; response: envelope `{items, pagination}`

    **Sort:** `quarter DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `quarter` | `Date` | Quarter start date. |
    | `nodes_observed` | `UInt64` | Total observed nodes at end of quarter. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/quarterly_data/nodes_observed/quarterly?quarter_from=2026-01-01"
    ```

## stablecoin_holder_cohorts

End-of-quarter stablecoin holder distribution by USD balance bucket, split into USD-pegged (WxDAI, sDAI, USDC, USDC.e, USDT) and non-USD (EURe, GBPe, BRLA, ZCHF, etc.). Excludes BRZ. Shows min/max/avg/median statistics for both holders and value across all days in the quarter. Reads from pre-mate...

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/quarterly_data/stablecoin_holder_cohorts/quarterly` | GET, POST | tier0 | `quarter_from`, `quarter_to`, `peg_class` | limit/offset (envelope) | quarter DESC |

??? info "`GET/POST /v1/quarterly_data/stablecoin_holder_cohorts/quarterly`"
    End-of-quarter stablecoin holder distribution by USD balance bucket, split into USD-pegged (WxDAI, sDAI, USDC, USDC.e, USDT) and non-USD (EURe, GBPe, BRLA, ZCHF, etc.). Excludes BRZ. Shows min/max/avg/median statistics for both holders and value across all days in the quarter. Reads from pre-mate...

    Model: `api_quarterly_data_stablecoin_holder_cohorts` — table `dbt.api_quarterly_data_stablecoin_holder_cohorts`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `quarter_from` | `>=` | `quarter` | date | Inclusive lower bound on quarter start date (e.g. 2024-01-01 for 2024-Q1) |
    | `quarter_to` | `<=` | `quarter` | date | Inclusive upper bound on quarter start date |
    | `peg_class` | `=` | `peg_class` | string | Filter by peg class: USD-pegged or non-USD |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** `limit`/`offset` — default 200, max 1000; response: envelope `{items, pagination}`

    **Sort:** `quarter DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `quarter` | `Date` | Quarter start date. |
    | `peg_class` | `String` | Stablecoin peg classification: 'USD-pegged' or 'non-USD'. |
    | `balance_bucket` | `String` | USD balance range bucket (e.g. '0-0.01', '1-10', '100-1k', '1M+'). |
    | `holders_min` | `UInt64` | Minimum daily holder count in this bucket across the quarter. |
    | `holders_max` | `UInt64` | Maximum daily holder count in this bucket across the quarter. |
    | `holders_avg` | `Float64` | Average daily holder count in this bucket across the quarter. |
    | `holders_median` | `Float64` | Median daily holder count in this bucket across the quarter. |
    | `value_min` | `Float64` | Minimum daily total USD value in this bucket across the quarter. |
    | `value_max` | `Float64` | Maximum daily total USD value in this bucket across the quarter. |
    | `value_avg` | `Float64` | Average daily total USD value in this bucket across the quarter. |
    | `value_median` | `Float64` | Median daily total USD value in this bucket across the quarter. |
    | `avg_balance_usd` | `Float64` | Average USD balance per holder (value_median / holders_median). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/quarterly_data/stablecoin_holder_cohorts/quarterly?quarter_from=2026-01-01"
    ```

## stablecoin_holders

Quarterly stablecoin holder statistics on Gnosis Chain, split by peg class plus a 'total' row (column-wise sum of the two classes; total holders_median is the sum of per-class medians). Shows median, max, and average of daily holder count across all days in the quarter. Note: holders are summed a...

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/quarterly_data/stablecoin_holders/quarterly` | GET, POST | tier0 | `quarter_from`, `quarter_to`, `peg_class` | limit/offset (envelope) | quarter DESC |

??? info "`GET/POST /v1/quarterly_data/stablecoin_holders/quarterly`"
    Quarterly stablecoin holder statistics on Gnosis Chain, split by peg class plus a 'total' row (column-wise sum of the two classes; total holders_median is the sum of per-class medians). Shows median, max, and average of daily holder count across all days in the quarter. Note: holders are summed a...

    Model: `api_quarterly_data_stablecoin_holders` — table `dbt.api_quarterly_data_stablecoin_holders`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `quarter_from` | `>=` | `quarter` | date | Inclusive lower bound on quarter start date (e.g. 2024-01-01 for 2024-Q1) |
    | `quarter_to` | `<=` | `quarter` | date | Inclusive upper bound on quarter start date |
    | `peg_class` | `=` | `peg_class` | string | Filter by peg class: USD-pegged or non-USD |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** `limit`/`offset` — default 200, max 1000; response: envelope `{items, pagination}`

    **Sort:** `quarter DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `quarter` | `Date` | Quarter start date. |
    | `peg_class` | `String` | Stablecoin peg classification: 'USD-pegged', 'non-USD', or 'total' (column-wise sum of the two classes). |
    | `holders_min` | `UInt64` | Minimum daily holder count observed in the quarter. |
    | `holders_max` | `UInt64` | Maximum daily holder count observed in the quarter. |
    | `holders_avg` | `Float64` | Average daily holder count across all days in the quarter. |
    | `holders_median` | `Float64` | Median daily holder count across all days in the quarter. |
    | `tokens_included` | `String` | Comma-separated list of tokens in this peg class. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/quarterly_data/stablecoin_holders/quarterly?quarter_from=2026-01-01"
    ```

## stablecoin_supply

Quarterly stablecoin supply statistics on Gnosis Chain, split by peg class (USD-pegged vs non-USD) plus a 'total' row. Shows median, max, and average of daily supply across all days in the quarter. The 'total' row is the column-wise sum of the two per-class rows, so its supply_median is the sum o...

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/quarterly_data/stablecoin_supply/quarterly` | GET, POST | tier0 | `quarter_from`, `quarter_to`, `peg_class` | limit/offset (envelope) | quarter DESC |

??? info "`GET/POST /v1/quarterly_data/stablecoin_supply/quarterly`"
    Quarterly stablecoin supply statistics on Gnosis Chain, split by peg class (USD-pegged vs non-USD) plus a 'total' row. Shows median, max, and average of daily supply across all days in the quarter. The 'total' row is the column-wise sum of the two per-class rows, so its supply_median is the sum o...

    Model: `api_quarterly_data_stablecoin_supply` — table `dbt.api_quarterly_data_stablecoin_supply`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `quarter_from` | `>=` | `quarter` | date | Inclusive lower bound on quarter start date (e.g. 2024-01-01 for 2024-Q1) |
    | `quarter_to` | `<=` | `quarter` | date | Inclusive upper bound on quarter start date |
    | `peg_class` | `=` | `peg_class` | string | Filter by peg class: USD-pegged or non-USD |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** `limit`/`offset` — default 200, max 1000; response: envelope `{items, pagination}`

    **Sort:** `quarter DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `quarter` | `Date` | Quarter start date. |
    | `peg_class` | `String` | Stablecoin peg classification: 'USD-pegged', 'non-USD', or 'total' (column-wise sum of the two classes). |
    | `supply_min` | `Float64` | Minimum daily total supply (USD) observed in the quarter. |
    | `supply_max` | `Float64` | Maximum daily total supply (USD) observed in the quarter. |
    | `supply_avg` | `Float64` | Average daily total supply (USD) across all days in the quarter. |
    | `supply_median` | `Float64` | Median daily total supply (USD) across all days in the quarter. |
    | `tokens_included` | `String` | Comma-separated list of tokens in this peg class. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/quarterly_data/stablecoin_supply/quarterly?quarter_from=2026-01-01"
    ```

## stablecoin_transfers

Quarterly stablecoin transfer count and volume on Gnosis Chain, split by peg class (USD-pegged vs non-USD) plus a 'total' row (plain sum across classes = exact grand-total transfer count and volume). Excludes BRZ.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/quarterly_data/stablecoin_transfers/quarterly` | GET, POST | tier0 | `quarter_from`, `quarter_to`, `peg_class` | limit/offset (envelope) | quarter DESC |

??? info "`GET/POST /v1/quarterly_data/stablecoin_transfers/quarterly`"
    Quarterly stablecoin transfer count and volume on Gnosis Chain, split by peg class (USD-pegged vs non-USD) plus a 'total' row (plain sum across classes = exact grand-total transfer count and volume). Excludes BRZ.

    Model: `api_quarterly_data_stablecoin_transfers` — table `dbt.api_quarterly_data_stablecoin_transfers`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `quarter_from` | `>=` | `quarter` | date | Inclusive lower bound on quarter start date (e.g. 2024-01-01 for 2024-Q1) |
    | `quarter_to` | `<=` | `quarter` | date | Inclusive upper bound on quarter start date |
    | `peg_class` | `=` | `peg_class` | string | Filter by peg class: USD-pegged or non-USD |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** `limit`/`offset` — default 200, max 1000; response: envelope `{items, pagination}`

    **Sort:** `quarter DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `quarter` | `Date` | Quarter start date. |
    | `peg_class` | `String` | Stablecoin peg classification: 'USD-pegged', 'non-USD', or 'total' (sum across both classes). |
    | `transfers` | `UInt64` | Total number of stablecoin transfers in the quarter. |
    | `volume_usd` | `Float64` | Total stablecoin transfer volume in USD for the quarter. |
    | `tokens_included` | `String` | Comma-separated list of tokens in this peg class. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/quarterly_data/stablecoin_transfers/quarterly?quarter_from=2026-01-01"
    ```

## staked_gno

End-of-quarter GNO staked on Gnosis Chain (effective balance in real GNO; mGNO->GNO conversion happens upstream in int_consensus_validators_balances_daily).

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/quarterly_data/staked_gno/quarterly` | GET, POST | tier0 | `quarter_from`, `quarter_to` | limit/offset (envelope) | quarter DESC |

??? info "`GET/POST /v1/quarterly_data/staked_gno/quarterly`"
    End-of-quarter GNO staked on Gnosis Chain (effective balance in real GNO; mGNO->GNO conversion happens upstream in int_consensus_validators_balances_daily).

    Model: `api_quarterly_data_staked_gno` — table `dbt.api_quarterly_data_staked_gno`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `quarter_from` | `>=` | `quarter` | date | Inclusive lower bound on quarter start date (e.g. 2024-01-01 for 2024-Q1) |
    | `quarter_to` | `<=` | `quarter` | date | Inclusive upper bound on quarter start date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** `limit`/`offset` — default 200, max 1000; response: envelope `{items, pagination}`

    **Sort:** `quarter DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `quarter` | `Date` | Quarter start date. |
    | `staked_gno` | `Float64` | Total GNO staked at end of quarter. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/quarterly_data/staked_gno/quarterly?quarter_from=2026-01-01"
    ```

## transactions_count

Total successful transactions per quarter on Gnosis Chain.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/quarterly_data/transactions_count/quarterly` | GET, POST | tier0 | `quarter_from`, `quarter_to` | limit/offset (envelope) | quarter DESC |

??? info "`GET/POST /v1/quarterly_data/transactions_count/quarterly`"
    Total successful transactions per quarter on Gnosis Chain.

    Model: `api_quarterly_data_transactions_count` — table `dbt.api_quarterly_data_transactions_count`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `quarter_from` | `>=` | `quarter` | date | Inclusive lower bound on quarter start date (e.g. 2024-01-01 for 2024-Q1) |
    | `quarter_to` | `<=` | `quarter` | date | Inclusive upper bound on quarter start date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** `limit`/`offset` — default 200, max 1000; response: envelope `{items, pagination}`

    **Sort:** `quarter DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `quarter` | `Date` | Quarter start date. |
    | `transactions` | `UInt64` | Total number of successful transactions in the quarter. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/quarterly_data/transactions_count/quarterly?quarter_from=2026-01-01"
    ```

## validators_active

End-of-quarter count of active validators on Gnosis Chain (the full active set = active_ongoing + active_exiting), matching public beacon explorers.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/quarterly_data/validators_active/quarterly` | GET, POST | tier0 | `quarter_from`, `quarter_to` | limit/offset (envelope) | quarter DESC |

??? info "`GET/POST /v1/quarterly_data/validators_active/quarterly`"
    End-of-quarter count of active validators on Gnosis Chain (the full active set = active_ongoing + active_exiting), matching public beacon explorers.

    Model: `api_quarterly_data_validators_active` — table `dbt.api_quarterly_data_validators_active`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `quarter_from` | `>=` | `quarter` | date | Inclusive lower bound on quarter start date (e.g. 2024-01-01 for 2024-Q1) |
    | `quarter_to` | `<=` | `quarter` | date | Inclusive upper bound on quarter start date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** `limit`/`offset` — default 200, max 1000; response: envelope `{items, pagination}`

    **Sort:** `quarter DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `quarter` | `Date` | Quarter start date. |
    | `validators_active` | `UInt64` | Number of active validators at end of quarter — active_ongoing plus active_exiting (both attest and remain staked until exit completes). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/quarterly_data/validators_active/quarterly?quarter_from=2026-01-01"
    ```
<!-- END AUTO-GENERATED: api-catalog-quarterly_data -->
