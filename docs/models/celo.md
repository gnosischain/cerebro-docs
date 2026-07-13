# Celo (Gnosis Pay) Module

<!-- BEGIN AUTO-GENERATED: models-celo -->
**Gpay**

| Model | Layer | Description |
|-------|-------|-------------|
| `fct_celo_gpay_actions_by_token_daily` | Fact | Daily volume (native + USD) and count per action x token, with running cumulatives. Actions - Payment, Top-up, Withdr... |
| `fct_celo_gpay_actions_by_token_monthly` | Fact | Monthly rollup of fct_celo_gpay_actions_by_token_daily. USDC/USDT only. |
| `fct_celo_gpay_actions_by_token_weekly` | Fact | Weekly rollup of fct_celo_gpay_actions_by_token_daily. USDC/USDT only. |
| `fct_celo_gpay_activity_daily` | Fact | Daily card-payment activity (active Safes, payment count, USD volume) plus
newly-funded and cumulative-funded card co... |
| `fct_celo_gpay_activity_monthly` | Fact | Monthly rollup of fct_celo_gpay_activity_daily. Partial current month excluded. USDC/USDT only. |
| `fct_celo_gpay_activity_weekly` | Fact | Weekly rollup of fct_celo_gpay_activity_daily. Partial current week excluded. USDC/USDT only. |
| `fct_celo_gpay_balance_cohorts_daily` | Fact | Per-day holder distribution across balance buckets, by token, in USD and native units. Zero/negative balances exclude... |
| `fct_celo_gpay_balances_by_token_daily` | Fact | Total net-flow balance across all Safes, per day per token. Built from the dense per-Safe base. USDC/USDT only. |
| `fct_celo_gpay_balances_safe_daily` | Fact | DENSE per-Safe/token/day net-flow balance (Celo analog of Gnosis Chain's
int_execution_gpay_balances_user_daily). Den... |
| `fct_celo_gpay_churn_monthly` | Fact | Monthly new/retained/returning/churned Safe segmentation and churn/retention
rates, for two scopes - Payment (card sp... |
| `fct_celo_gpay_kpi_monthly` | Fact | Monthly KPIs - MAU (and per-action MAU), payment/deposit/withdrawal USD
volumes, net flow (deposits minus withdrawals... |
| `fct_celo_gpay_payments_hourly` | Fact | Hourly payment counts by token over the trailing 14 days. Serves the time-of-day distribution panel. USDC/USDT only. |
| `fct_celo_gpay_retention_by_action_monthly` | Fact | Per-action monthly cohort retention. Cohort = month a Safe first performed the action. Actions - Payment, Top-up, Wit... |
| `fct_celo_gpay_retention_monthly` | Fact | Monthly payment-cohort retention (users + USD). Cohort = month of a Safe's first Payment. USDC/USDT only. |
| `fct_celo_gpay_snapshots` | Fact | All-time and trailing-7D headline snapshots per action (Volume/Count/Users),
plus TotalBalance. Feeds the counter til... |
| `api_celo_gpay_active_users_7d` | API | Trailing-7D distinct paying Safes with WoW change_pct. Counter tile. |
| `api_celo_gpay_activity_by_action_daily` | API | Daily count/USD/native volume per action (Payment, Top-up, Withdrawal, Reversal). |
| `api_celo_gpay_activity_by_action_monthly` | API | Monthly count/USD/native volume per action. |
| `api_celo_gpay_activity_by_action_weekly` | API | Weekly count/USD/native volume per action. |
| `api_celo_gpay_balance_cohorts_holders_daily` | API | Daily holder counts per balance bucket, by token and unit (usd/native). |
| `api_celo_gpay_balance_cohorts_value_daily` | API | Daily summed balance (native + USD) per balance bucket, by token and unit. |
| `api_celo_gpay_balances_native_daily` | API | Daily total net-flow balance (native units) by token. USDC/USDT only. |
| `api_celo_gpay_balances_usd_daily` | API | Daily total net-flow balance (USD) by token. USDC/USDT only. |
| `api_celo_gpay_churn_monthly` | API | Monthly new/retained/returning/churned segmentation by scope (Payment, Any). |
| `api_celo_gpay_churn_rates_monthly` | API | Monthly churn and retention rates by scope (Payment, Any). |
| `api_celo_gpay_funded_addresses_daily` | API | Cumulative funded (ever-paid) Safes by day. |
| `api_celo_gpay_funded_addresses_monthly` | API | Cumulative funded Safes by month. |
| `api_celo_gpay_funded_addresses_weekly` | API | Cumulative funded Safes by week. |
| `api_celo_gpay_kpi_monthly` | API | Monthly KPI table (MAU, volumes, net flow, ARPU, repeat rate). Backs the KPI tiles and monthly KPI charts. USDC/USDT ... |
| `api_celo_gpay_payments_7d` | API | Trailing-7D payment count with WoW change_pct. Counter tile. |
| `api_celo_gpay_payments_by_token_daily` | API | Daily payment count split by token (USDC/USDT). |
| `api_celo_gpay_payments_by_token_monthly` | API | Monthly payment count split by token (USDC/USDT). |
| `api_celo_gpay_payments_by_token_weekly` | API | Weekly payment count split by token (USDC/USDT). |
| `api_celo_gpay_payments_hourly` | API | Hourly payment counts by token over the trailing 14 days. |
| `api_celo_gpay_retention_by_action_monthly` | API | Per-action monthly cohort retention heatmap. |
| `api_celo_gpay_retention_by_action_users_monthly` | API | Per-action monthly cohort retention (absolute users). |
| `api_celo_gpay_retention_monthly` | API | Monthly payment-cohort retention (absolute users) in date/label/value shape. |
| `api_celo_gpay_retention_pct_monthly` | API | Monthly payment-cohort retention heatmap (x/y/retention_pct/value_abs/value_usd). |
| `api_celo_gpay_retention_volume_monthly` | API | Monthly payment-cohort retention by USD volume. |
| `api_celo_gpay_total_balance` | API | Latest-day net-flow USDC+USDT float held across all GP Safes. Counter tile. |
| `api_celo_gpay_total_funded` | API | All-time distinct funded (ever-paid) Safes. Counter tile. |
| `api_celo_gpay_total_payments` | API | All-time payment count. Counter tile. |
| `api_celo_gpay_total_volume` | API | All-time card payment volume in USD (USDC + USDT). Counter tile. |
| `api_celo_gpay_volume_7d` | API | Trailing-7D payment volume (USD) with WoW change_pct. Counter tile. |
| `api_celo_gpay_volume_payments_by_token_daily` | API | Daily payment volume (USD) split by token (USDC/USDT). |
| `api_celo_gpay_volume_payments_by_token_monthly` | API | Monthly payment volume (USD) split by token (USDC/USDT). |
| `api_celo_gpay_volume_payments_by_token_weekly` | API | Weekly payment volume (USD) split by token (USDC/USDT). |
| `api_celo_gpay_wallet_balance_composition` | API | Latest-day USD balance composition across tokens (USDC/USDT); sub-1% folded into Other. |

<!-- END AUTO-GENERATED: models-celo -->
