# Celo API Endpoints

<!-- BEGIN AUTO-GENERATED: api-catalog-celo -->
<!-- generated: 2026-07-23 -->
_33 endpoints across 24 resources. Generated from the dbt manifest — edits inside this block will be overwritten. Regenerate with `python scripts/update_docs.py --only api`._

## celo_gpay_active_users

Trailing-7D distinct paying Safes with WoW change_pct. Counter tile.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/celo/celo_gpay_active_users/last_7d` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/celo/celo_gpay_active_users/last_7d`"
    Trailing-7D distinct paying Safes with WoW change_pct. Counter tile.

    Model: `api_celo_gpay_active_users_7d` — table `dbt.api_celo_gpay_active_users_7d`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `value` | `Nullable(Float64)` | The number of active users in the last 7 days. |
    | `change_pct` | `Nullable(Float64)` | The percentage change compared to the previous 7-day period. |
    | `as_of_date` | `Nullable(Date)` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/celo/celo_gpay_active_users/last_7d"
    ```

## celo_gpay_activity_by_action

Daily count/USD/native volume per action (Payment, Top-up, Withdrawal, Reversal).

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/celo/celo_gpay_activity_by_action/daily` | GET | tier1 | `action`, `start_date`, `end_date` | -- | date DESC |
| `/v1/celo/celo_gpay_activity_by_action/weekly` | GET | tier1 | `action`, `start_date`, `end_date` | -- | week DESC |
| `/v1/celo/celo_gpay_activity_by_action/monthly` | GET | tier1 | `action`, `start_date`, `end_date` | -- | month DESC |

??? info "`GET /v1/celo/celo_gpay_activity_by_action/daily`"
    Daily count/USD/native volume per action (Payment, Top-up, Withdrawal, Reversal).

    Model: `api_celo_gpay_activity_by_action_daily` — table `dbt.api_celo_gpay_activity_by_action_daily`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `action` | `=` | `action` | string | Action type (Payment, Top-up, Withdrawal, Reversal) |
    | `start_date` | `>=` | `date` | date | Inclusive start date |
    | `end_date` | `<=` | `date` | date | Inclusive end date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `date DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The calendar date. |
    | `action` | `Nullable(String)` | The activity type (e.g., Payment, Deposit, Withdrawal, Cashback). |
    | `activity_count` | `UInt64` | The number of transactions for this action on this date. |
    | `volume_usd` | `Nullable(Float64)` | The total USD volume for this action on this date. |
    | `volume_native` | `Float64` | The total native token volume for this action on this date. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/celo/celo_gpay_activity_by_action/daily?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/celo/celo_gpay_activity_by_action/weekly`"
    Weekly count/USD/native volume per action.

    Model: `api_celo_gpay_activity_by_action_weekly` — table `dbt.api_celo_gpay_activity_by_action_weekly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `action` | `=` | `action` | string | Action type (Payment, Top-up, Withdrawal, Reversal) |
    | `start_date` | `>=` | `week` | date | Inclusive start date |
    | `end_date` | `<=` | `week` | date | Inclusive end date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `week DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `week` | `Date` | The first day of the ISO week. |
    | `action` | `Nullable(String)` | The activity type (e.g., Payment, Deposit, Withdrawal, Cashback). |
    | `activity_count` | `UInt64` | The number of transactions for this action in this week. |
    | `volume_usd` | `Nullable(Float64)` | The total USD volume for this action in this week. |
    | `volume_native` | `Float64` | The total native token volume for this action in this week. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/celo/celo_gpay_activity_by_action/weekly?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/celo/celo_gpay_activity_by_action/monthly`"
    Monthly count/USD/native volume per action.

    Model: `api_celo_gpay_activity_by_action_monthly` — table `dbt.api_celo_gpay_activity_by_action_monthly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `action` | `=` | `action` | string | Action type (Payment, Top-up, Withdrawal, Reversal) |
    | `start_date` | `>=` | `month` | date | Inclusive start date |
    | `end_date` | `<=` | `month` | date | Inclusive end date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `month DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `month` | `Date` | The first day of the month. |
    | `action` | `Nullable(String)` | The activity type (e.g., Payment, Deposit, Withdrawal, Cashback). |
    | `activity_count` | `UInt64` | The number of transactions for this action in this month. |
    | `volume_usd` | `Nullable(Float64)` | The total USD volume for this action in this month. |
    | `volume_native` | `Float64` | The total native token volume for this action in this month. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/celo/celo_gpay_activity_by_action/monthly?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## celo_gpay_balance_cohorts_holders

Daily holder counts per balance bucket, by token and unit (usd/native).

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/celo/celo_gpay_balance_cohorts_holders/daily` | GET | tier1 | `token`, `start_date`, `end_date` | -- | date DESC |

??? info "`GET /v1/celo/celo_gpay_balance_cohorts_holders/daily`"
    Daily holder counts per balance bucket, by token and unit (usd/native).

    Model: `api_celo_gpay_balance_cohorts_holders_daily` — table `dbt.api_celo_gpay_balance_cohorts_holders_daily`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `token` | `=` | `token` | string | Token symbol |
    | `start_date` | `>=` | `date` | date | Inclusive start date |
    | `end_date` | `<=` | `date` | date | Inclusive end date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `date DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Nullable(Date)` | The calendar date of the balance snapshot. |
    | `token` | `LowCardinality(String)` | The token symbol. |
    | `cohort_unit` | `String` | The unit used for cohort bucketing (e.g., USD, native). |
    | `label` | `String` | The balance range bucket label. |
    | `value` | `UInt64` | The number of holders in this cohort bucket. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/celo/celo_gpay_balance_cohorts_holders/daily?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## celo_gpay_balance_cohorts_value

Daily summed balance (native + USD) per balance bucket, by token and unit.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/celo/celo_gpay_balance_cohorts_value/daily` | GET | tier1 | `token`, `start_date`, `end_date` | -- | date DESC |

??? info "`GET /v1/celo/celo_gpay_balance_cohorts_value/daily`"
    Daily summed balance (native + USD) per balance bucket, by token and unit.

    Model: `api_celo_gpay_balance_cohorts_value_daily` — table `dbt.api_celo_gpay_balance_cohorts_value_daily`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `token` | `=` | `token` | string | Token symbol |
    | `start_date` | `>=` | `date` | date | Inclusive start date |
    | `end_date` | `<=` | `date` | date | Inclusive end date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `date DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Nullable(Date)` | The calendar date of the balance snapshot. |
    | `token` | `LowCardinality(String)` | The token symbol. |
    | `cohort_unit` | `String` | The unit used for cohort bucketing. |
    | `label` | `String` | The balance range bucket label. |
    | `value_native` | `Float64` | The total native token value in this bucket. |
    | `value_usd` | `Float64` | The total USD value in this bucket. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/celo/celo_gpay_balance_cohorts_value/daily?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## celo_gpay_balances_native

Daily total net-flow balance (native units) by token. USDC/USDT only.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/celo/celo_gpay_balances_native/daily` | GET | tier1 | `token`, `start_date`, `end_date` | -- | date DESC |

??? info "`GET /v1/celo/celo_gpay_balances_native/daily`"
    Daily total net-flow balance (native units) by token. USDC/USDT only.

    Model: `api_celo_gpay_balances_native_daily` — table `dbt.api_celo_gpay_balances_native_daily`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `token` | `=` | `label` | string | Token symbol |
    | `start_date` | `>=` | `date` | date | Inclusive start date |
    | `end_date` | `<=` | `date` | date | Inclusive end date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `date DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Nullable(Date)` | The calendar date of the balance snapshot. |
    | `label` | `LowCardinality(String)` | The token symbol. |
    | `value` | `Float64` | The total balance in native token units. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/celo/celo_gpay_balances_native/daily?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## celo_gpay_balances_usd

Daily total net-flow balance (USD) by token. USDC/USDT only.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/celo/celo_gpay_balances_usd/daily` | GET | tier1 | `token`, `start_date`, `end_date` | -- | date DESC |

??? info "`GET /v1/celo/celo_gpay_balances_usd/daily`"
    Daily total net-flow balance (USD) by token. USDC/USDT only.

    Model: `api_celo_gpay_balances_usd_daily` — table `dbt.api_celo_gpay_balances_usd_daily`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `token` | `=` | `label` | string | Token symbol |
    | `start_date` | `>=` | `date` | date | Inclusive start date |
    | `end_date` | `<=` | `date` | date | Inclusive end date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `date DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Nullable(Date)` | The calendar date of the balance snapshot. |
    | `label` | `LowCardinality(String)` | The token symbol. |
    | `value` | `Float64` | The total balance in USD for this token. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/celo/celo_gpay_balances_usd/daily?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## celo_gpay_churn

Monthly new/retained/returning/churned segmentation by scope (Payment, Any).

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/celo/celo_gpay_churn/monthly` | GET | tier1 | `scope`, `start_date`, `end_date` | -- | month DESC |

??? info "`GET /v1/celo/celo_gpay_churn/monthly`"
    Monthly new/retained/returning/churned segmentation by scope (Payment, Any).

    Model: `api_celo_gpay_churn_monthly` — table `dbt.api_celo_gpay_churn_monthly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `scope` | `=` | `scope` | string | Churn scope |
    | `start_date` | `>=` | `month` | date | Inclusive start month |
    | `end_date` | `<=` | `month` | date | Inclusive end month |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `month DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `scope` | `String` | The activity scope for churn calculation (e.g., all, payment). |
    | `month` | `String` | The first day of the month. |
    | `new_users` | `UInt64` | Users active for the first time this month. |
    | `retained_users` | `UInt64` | Users active in both this and the previous month. |
    | `returning_users` | `UInt64` | Users returning after a period of inactivity. |
    | `churned_users` | `UInt64` | Users active last month but not this month. |
    | `total_active` | `UInt64` | Total active users this month. |
    | `churn_rate` | `Float64` | The percentage of last month's users who churned. |
    | `retention_rate` | `Float64` | The percentage of last month's users who were retained. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/celo/celo_gpay_churn/monthly?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## celo_gpay_churn_rates

Monthly churn and retention rates by scope (Payment, Any).

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/celo/celo_gpay_churn_rates/monthly` | GET | tier1 | `scope`, `start_date`, `end_date` | -- | month DESC |

??? info "`GET /v1/celo/celo_gpay_churn_rates/monthly`"
    Monthly churn and retention rates by scope (Payment, Any).

    Model: `api_celo_gpay_churn_rates_monthly` — table `dbt.api_celo_gpay_churn_rates_monthly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `scope` | `=` | `scope` | string | Churn scope |
    | `start_date` | `>=` | `month` | date | Inclusive start month |
    | `end_date` | `<=` | `month` | date | Inclusive end month |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `month DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `scope` | `String` | The activity scope (e.g., all, payment). |
    | `month` | `String` | The first day of the month. |
    | `churn_rate` | `Float64` | The churn rate for the month. |
    | `retention_rate` | `Float64` | The retention rate for the month. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/celo/celo_gpay_churn_rates/monthly?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## celo_gpay_funded_addresses

Cumulative funded (ever-paid) Safes by day.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/celo/celo_gpay_funded_addresses/daily` | GET | tier1 | -- | -- | -- |
| `/v1/celo/celo_gpay_funded_addresses/weekly` | GET | tier1 | -- | -- | -- |
| `/v1/celo/celo_gpay_funded_addresses/monthly` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/celo/celo_gpay_funded_addresses/daily`"
    Cumulative funded (ever-paid) Safes by day.

    Model: `api_celo_gpay_funded_addresses_daily` — table `dbt.api_celo_gpay_funded_addresses_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The calendar date. |
    | `value` | `UInt64` | The cumulative number of funded wallet addresses. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/celo/celo_gpay_funded_addresses/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/celo/celo_gpay_funded_addresses/weekly`"
    Cumulative funded Safes by week.

    Model: `api_celo_gpay_funded_addresses_weekly` — table `dbt.api_celo_gpay_funded_addresses_weekly`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The first day of the ISO week. |
    | `value` | `UInt64` | The cumulative number of funded wallet addresses. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/celo/celo_gpay_funded_addresses/weekly" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/celo/celo_gpay_funded_addresses/monthly`"
    Cumulative funded Safes by month.

    Model: `api_celo_gpay_funded_addresses_monthly` — table `dbt.api_celo_gpay_funded_addresses_monthly`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The first day of the month. |
    | `value` | `UInt64` | The cumulative number of funded wallet addresses. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/celo/celo_gpay_funded_addresses/monthly" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## celo_gpay_kpi

Monthly KPI table (MAU, volumes, net flow, ARPU, repeat rate). Backs the KPI tiles and monthly KPI charts. USDC/USDT only.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/celo/celo_gpay_kpi/monthly` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/celo/celo_gpay_kpi/monthly`"
    Monthly KPI table (MAU, volumes, net flow, ARPU, repeat rate). Backs the KPI tiles and monthly KPI charts. USDC/USDT only.

    Model: `api_celo_gpay_kpi_monthly` — table `dbt.api_celo_gpay_kpi_monthly`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `month` | `Date` | The first day of the month. |
    | `mau` | `UInt64` | Monthly active users across all activity types. |
    | `payment_mau` | `UInt64` | Monthly active users who made payments. |
    | `deposit_mau` | `UInt64` | Monthly active users who made deposits. |
    | `withdrawal_mau` | `UInt64` | Monthly active users who made withdrawals. |
    | `total_payment_volume_usd` | `Nullable(Float64)` | Total payment volume in USD for the month. |
    | `total_payment_count` | `UInt64` | Total number of payments in the month. |
    | `total_deposit_volume_usd` | `Nullable(Float64)` | Total deposit volume in USD for the month. |
    | `total_withdrawal_volume_usd` | `Nullable(Float64)` | Total withdrawal volume in USD for the month. |
    | `net_flow_usd` | `Nullable(Float64)` | Net flow (deposits minus withdrawals) in USD for the month. |
    | `reversal_total_usd` | `Nullable(Float64)` | Total reversal value in USD for the month. |
    | `arpu` | `Nullable(Float64)` | Average revenue per user in USD. |
    | `avg_tx_per_user` | `Float64` | Average number of transactions per active user. |
    | `repeat_purchase_rate` | `Float64` | Percentage of users who made more than one payment. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/celo/celo_gpay_kpi/monthly" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## celo_gpay_payments

Trailing-7D payment count with WoW change_pct. Counter tile.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/celo/celo_gpay_payments/last_7d` | GET | tier0 | -- | -- | -- |
| `/v1/celo/celo_gpay_payments/hourly` | GET | tier1 | `token`, `start_date`, `end_date` | -- | date DESC |

??? info "`GET /v1/celo/celo_gpay_payments/last_7d`"
    Trailing-7D payment count with WoW change_pct. Counter tile.

    Model: `api_celo_gpay_payments_7d` — table `dbt.api_celo_gpay_payments_7d`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `value` | `Nullable(Float64)` | The total number of payments in the last 7 days. |
    | `change_pct` | `Nullable(Float64)` | The percentage change compared to the previous 7-day period. |
    | `as_of_date` | `Nullable(Date)` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/celo/celo_gpay_payments/last_7d"
    ```

??? info "`GET /v1/celo/celo_gpay_payments/hourly`"
    Hourly payment counts by token over the trailing 14 days.

    Model: `api_celo_gpay_payments_hourly` — table `dbt.api_celo_gpay_payments_hourly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `token` | `=` | `label` | string | Token symbol |
    | `start_date` | `>=` | `date` | date | Inclusive start date |
    | `end_date` | `<=` | `date` | date | Inclusive end date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `date DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `DateTime` | The hour timestamp of the payment activity. |
    | `label` | `String` | The token symbol. |
    | `value` | `UInt64` | The number of payments in this hour for this token. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/celo/celo_gpay_payments/hourly?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## celo_gpay_payments_by_token

Daily payment count split by token (USDC/USDT).

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/celo/celo_gpay_payments_by_token/daily` | GET | tier1 | `token`, `start_date`, `end_date` | -- | date DESC |
| `/v1/celo/celo_gpay_payments_by_token/weekly` | GET | tier1 | `token`, `start_date`, `end_date` | -- | date DESC |
| `/v1/celo/celo_gpay_payments_by_token/monthly` | GET | tier1 | `token`, `start_date`, `end_date` | -- | date DESC |

??? info "`GET /v1/celo/celo_gpay_payments_by_token/daily`"
    Daily payment count split by token (USDC/USDT).

    Model: `api_celo_gpay_payments_by_token_daily` — table `dbt.api_celo_gpay_payments_by_token_daily`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `token` | `=` | `label` | string | Token symbol |
    | `start_date` | `>=` | `date` | date | Inclusive start date |
    | `end_date` | `<=` | `date` | date | Inclusive end date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `date DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The calendar date. |
    | `label` | `LowCardinality(String)` | The token symbol. |
    | `value` | `UInt64` | The number of payments for this token on this date. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/celo/celo_gpay_payments_by_token/daily?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/celo/celo_gpay_payments_by_token/weekly`"
    Weekly payment count split by token (USDC/USDT).

    Model: `api_celo_gpay_payments_by_token_weekly` — table `dbt.api_celo_gpay_payments_by_token_weekly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `token` | `=` | `label` | string | Token symbol |
    | `start_date` | `>=` | `date` | date | Inclusive start date |
    | `end_date` | `<=` | `date` | date | Inclusive end date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `date DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The first day of the ISO week. |
    | `label` | `LowCardinality(String)` | The token symbol. |
    | `value` | `UInt64` | The number of payments for this token in this week. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/celo/celo_gpay_payments_by_token/weekly?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/celo/celo_gpay_payments_by_token/monthly`"
    Monthly payment count split by token (USDC/USDT).

    Model: `api_celo_gpay_payments_by_token_monthly` — table `dbt.api_celo_gpay_payments_by_token_monthly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `token` | `=` | `label` | string | Token symbol |
    | `start_date` | `>=` | `date` | date | Inclusive start date |
    | `end_date` | `<=` | `date` | date | Inclusive end date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `date DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The first day of the month. |
    | `label` | `LowCardinality(String)` | The token symbol. |
    | `value` | `UInt64` | The number of payments for this token in this month. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/celo/celo_gpay_payments_by_token/monthly?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## celo_gpay_retention

Monthly payment-cohort retention (absolute users) in date/label/value shape.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/celo/celo_gpay_retention/monthly` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/celo/celo_gpay_retention/monthly`"
    Monthly payment-cohort retention (absolute users) in date/label/value shape.

    Model: `api_celo_gpay_retention_monthly` — table `dbt.api_celo_gpay_retention_monthly`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `String` | The activity month. |
    | `label` | `String` | The cohort month label. |
    | `value` | `UInt64` | The number of active users from this cohort. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/celo/celo_gpay_retention/monthly" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## celo_gpay_retention_by_action

Per-action monthly cohort retention heatmap.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/celo/celo_gpay_retention_by_action/monthly` | GET | tier1 | `action` | -- | -- |

??? info "`GET /v1/celo/celo_gpay_retention_by_action/monthly`"
    Per-action monthly cohort retention heatmap.

    Model: `api_celo_gpay_retention_by_action_monthly` — table `dbt.api_celo_gpay_retention_by_action_monthly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `action` | `=` | `action` | string | Action type |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `x` | `String` | The activity month (x-axis of the heatmap). |
    | `y` | `String` | The cohort month (y-axis of the heatmap). |
    | `action` | `Nullable(String)` | The activity type (e.g., Payment, Deposit, Withdrawal). |
    | `retention_pct` | `Float64` | The user retention percentage. |
    | `value_abs` | `UInt64` | The absolute number of retained users. |
    | `amount_retention_pct` | `Nullable(Float64)` | The amount retention percentage. |
    | `value_usd` | `Nullable(Float64)` | The total USD amount for the cohort in this month. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/celo/celo_gpay_retention_by_action/monthly?action=VALUE" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## celo_gpay_retention_by_action_users

Per-action monthly cohort retention (absolute users).

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/celo/celo_gpay_retention_by_action_users/monthly` | GET | tier1 | `action` | -- | -- |

??? info "`GET /v1/celo/celo_gpay_retention_by_action_users/monthly`"
    Per-action monthly cohort retention (absolute users).

    Model: `api_celo_gpay_retention_by_action_users_monthly` — table `dbt.api_celo_gpay_retention_by_action_users_monthly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `action` | `=` | `action` | string | Action type |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `action` | `Nullable(String)` | The activity type (e.g., Payment, Deposit, Withdrawal). |
    | `date` | `String` | The activity month. |
    | `label` | `String` | The cohort month label. |
    | `value` | `UInt64` | The number of active users from this cohort. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/celo/celo_gpay_retention_by_action_users/monthly?action=VALUE" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## celo_gpay_retention_pct

Monthly payment-cohort retention heatmap (x/y/retention_pct/value_abs/value_usd).

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/celo/celo_gpay_retention_pct/monthly` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/celo/celo_gpay_retention_pct/monthly`"
    Monthly payment-cohort retention heatmap (x/y/retention_pct/value_abs/value_usd).

    Model: `api_celo_gpay_retention_pct_monthly` — table `dbt.api_celo_gpay_retention_pct_monthly`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `x` | `String` | The activity month (x-axis of the heatmap). |
    | `y` | `String` | The cohort month (y-axis of the heatmap). |
    | `retention_pct` | `Float64` | The user retention percentage. |
    | `value_abs` | `UInt64` | The absolute number of retained users. |
    | `amount_retention_pct` | `Nullable(Float64)` | The amount retention percentage. |
    | `value_usd` | `Nullable(Float64)` | The total USD amount for the cohort in this month. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/celo/celo_gpay_retention_pct/monthly" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## celo_gpay_retention_volume

Monthly payment-cohort retention by USD volume.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/celo/celo_gpay_retention_volume/monthly` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/celo/celo_gpay_retention_volume/monthly`"
    Monthly payment-cohort retention by USD volume.

    Model: `api_celo_gpay_retention_volume_monthly` — table `dbt.api_celo_gpay_retention_volume_monthly`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `String` | The activity month. |
    | `label` | `String` | The cohort month label. |
    | `value` | `Nullable(Float64)` | The total USD volume for this cohort in this month. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/celo/celo_gpay_retention_volume/monthly" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## celo_gpay_total_balance

Latest-day net-flow USDC+USDT float held across all GP Safes. Counter tile.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/celo/celo_gpay_total_balance/all_time` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/celo/celo_gpay_total_balance/all_time`"
    Latest-day net-flow USDC+USDT float held across all GP Safes. Counter tile.

    Model: `api_celo_gpay_total_balance` — table `dbt.api_celo_gpay_total_balance`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `value` | `Nullable(Float64)` | The total balance in USD. |
    | `as_of_date` | `Nullable(Date)` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/celo/celo_gpay_total_balance/all_time"
    ```

## celo_gpay_total_funded

All-time distinct funded (ever-paid) Safes. Counter tile.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/celo/celo_gpay_total_funded/all_time` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/celo/celo_gpay_total_funded/all_time`"
    All-time distinct funded (ever-paid) Safes. Counter tile.

    Model: `api_celo_gpay_total_funded` — table `dbt.api_celo_gpay_total_funded`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `value` | `Nullable(Float64)` | The total number of funded wallets. |
    | `as_of_date` | `Nullable(Date)` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/celo/celo_gpay_total_funded/all_time"
    ```

## celo_gpay_total_payments

All-time payment count. Counter tile.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/celo/celo_gpay_total_payments/all_time` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/celo/celo_gpay_total_payments/all_time`"
    All-time payment count. Counter tile.

    Model: `api_celo_gpay_total_payments` — table `dbt.api_celo_gpay_total_payments`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `value` | `Nullable(Float64)` | The total number of payments. |
    | `as_of_date` | `Nullable(Date)` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/celo/celo_gpay_total_payments/all_time"
    ```

## celo_gpay_total_volume

All-time card payment volume in USD (USDC + USDT). Counter tile.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/celo/celo_gpay_total_volume/all_time` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/celo/celo_gpay_total_volume/all_time`"
    All-time card payment volume in USD (USDC + USDT). Counter tile.

    Model: `api_celo_gpay_total_volume` — table `dbt.api_celo_gpay_total_volume`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `value` | `Nullable(Float64)` | The total payment volume in USD. |
    | `as_of_date` | `Nullable(Date)` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/celo/celo_gpay_total_volume/all_time"
    ```

## celo_gpay_volume

Trailing-7D payment volume (USD) with WoW change_pct. Counter tile.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/celo/celo_gpay_volume/last_7d` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/celo/celo_gpay_volume/last_7d`"
    Trailing-7D payment volume (USD) with WoW change_pct. Counter tile.

    Model: `api_celo_gpay_volume_7d` — table `dbt.api_celo_gpay_volume_7d`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `value` | `Nullable(Float64)` | The total payment volume in USD in the last 7 days. |
    | `change_pct` | `Nullable(Float64)` | The percentage change compared to the previous 7-day period. |
    | `as_of_date` | `Nullable(Date)` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/celo/celo_gpay_volume/last_7d"
    ```

## celo_gpay_volume_payments_by_token

Daily payment volume (USD) split by token (USDC/USDT).

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/celo/celo_gpay_volume_payments_by_token/daily` | GET | tier1 | `token`, `start_date`, `end_date` | -- | date DESC |
| `/v1/celo/celo_gpay_volume_payments_by_token/weekly` | GET | tier1 | `token`, `start_date`, `end_date` | -- | date DESC |
| `/v1/celo/celo_gpay_volume_payments_by_token/monthly` | GET | tier1 | `token`, `start_date`, `end_date` | -- | date DESC |

??? info "`GET /v1/celo/celo_gpay_volume_payments_by_token/daily`"
    Daily payment volume (USD) split by token (USDC/USDT).

    Model: `api_celo_gpay_volume_payments_by_token_daily` — table `dbt.api_celo_gpay_volume_payments_by_token_daily`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `token` | `=` | `label` | string | Token symbol |
    | `start_date` | `>=` | `date` | date | Inclusive start date |
    | `end_date` | `<=` | `date` | date | Inclusive end date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `date DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The calendar date. |
    | `label` | `LowCardinality(String)` | The token symbol. |
    | `value` | `Nullable(Float64)` | The payment volume in USD for this token on this date. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/celo/celo_gpay_volume_payments_by_token/daily?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/celo/celo_gpay_volume_payments_by_token/weekly`"
    Weekly payment volume (USD) split by token (USDC/USDT).

    Model: `api_celo_gpay_volume_payments_by_token_weekly` — table `dbt.api_celo_gpay_volume_payments_by_token_weekly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `token` | `=` | `label` | string | Token symbol |
    | `start_date` | `>=` | `date` | date | Inclusive start date |
    | `end_date` | `<=` | `date` | date | Inclusive end date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `date DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The first day of the ISO week. |
    | `label` | `LowCardinality(String)` | The token symbol. |
    | `value` | `Nullable(Float64)` | The payment volume in USD for this token in this week. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/celo/celo_gpay_volume_payments_by_token/weekly?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/celo/celo_gpay_volume_payments_by_token/monthly`"
    Monthly payment volume (USD) split by token (USDC/USDT).

    Model: `api_celo_gpay_volume_payments_by_token_monthly` — table `dbt.api_celo_gpay_volume_payments_by_token_monthly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `token` | `=` | `label` | string | Token symbol |
    | `start_date` | `>=` | `date` | date | Inclusive start date |
    | `end_date` | `<=` | `date` | date | Inclusive end date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `date DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The first day of the month. |
    | `label` | `LowCardinality(String)` | The token symbol. |
    | `value` | `Nullable(Float64)` | The payment volume in USD for this token in this month. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/celo/celo_gpay_volume_payments_by_token/monthly?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## celo_gpay_wallet_balance_composition

Latest-day USD balance composition across tokens (USDC/USDT); sub-1% folded into Other.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/celo/celo_gpay_wallet_balance_composition/latest` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/celo/celo_gpay_wallet_balance_composition/latest`"
    Latest-day USD balance composition across tokens (USDC/USDT); sub-1% folded into Other.

    Model: `api_celo_gpay_wallet_balance_composition` — table `dbt.api_celo_gpay_wallet_balance_composition`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `name` | `String` | The token symbol or name. |
    | `value` | `Float64` | The balance amount in USD. |
    | `as_of_date` | `Nullable(Date)` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/celo/celo_gpay_wallet_balance_composition/latest" \
      -H "X-API-Key: YOUR_API_KEY"
    ```
<!-- END AUTO-GENERATED: api-catalog-celo -->
