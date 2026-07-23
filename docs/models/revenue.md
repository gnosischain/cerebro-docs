# Revenue Module

<!-- BEGIN AUTO-GENERATED: models-revenue -->
<!-- generated: 2026-07-23 -->
**Active**

| Model | Layer | Description |
|-------|-------|-------------|
| `fct_revenue_active_users_cohorts_monthly` | Fact | HEADLINE — cross-stream unique-active-user cohort (monthly grain).
Same logic as the weekly variant: per-user fees su... |
| `fct_revenue_active_users_cohorts_weekly` | Fact | HEADLINE — cross-stream unique-active-user cohort (rolling 52-week).
For each user, fees across ALL streams (holdings... |
| `fct_revenue_active_users_totals_monthly` | Fact | Monthly cross-stream active-user totals (no cohort split).
Threshold is $0.50/month — the month-scaled equivalent of ... |
| `fct_revenue_active_users_totals_weekly` | Fact | Weekly cross-stream active-user totals (no cohort split).
A user is counted once per week if their trailing-52w fees ... |
| `api_revenue_active_users_cohorts_monthly` | API | API view over fct_revenue_active_users_cohorts_monthly. |
| `api_revenue_active_users_cohorts_weekly` | API | API view over fct_revenue_active_users_cohorts_weekly. |
| `api_revenue_active_users_totals_monthly` | API | API view over fct_revenue_active_users_totals_monthly. |
| `api_revenue_active_users_totals_weekly` | API | API view over fct_revenue_active_users_totals_weekly. |

**Fees**

| Model | Layer | Description |
|-------|-------|-------------|
| `int_revenue_fees_monthly_per_user` | Intermediate | Monthly per-user fees per stream/symbol. Simple calendar-month
aggregation (no rolling window). The current (incomple... |
| `int_revenue_fees_unified_daily` | Intermediate | Unified daily per-user revenue fees across all streams.
UNION ALL of the per-stream daily fee intermediates with a
st... |
| `int_revenue_fees_weekly_per_user` | Intermediate | Weekly per-user fees per stream/symbol with trailing 52-calendar-week
rolling total (`annual_rolling_fees`). The week... |

**Gnosis**

| Model | Layer | Description |
|-------|-------|-------------|
| `int_revenue_gnosis_app_fees_daily` | Intermediate | Daily per-user Gnosis App (Metri) fees denominated in USD.
Users pay a CRC ERC-1155 fee to the Metri fee receiver add... |
| `fct_revenue_gnosis_app_cohorts_monthly` | Fact | Gnosis App stream — monthly Metri CRC fee "potential" revenue by user
$-cohort bucket. Same source as the weekly tabl... |
| `fct_revenue_gnosis_app_cohorts_weekly` | Fact | Gnosis App stream — rolling-52-week Metri CRC fee "potential" revenue
by user $-cohort bucket. Each user's cumulative... |
| `api_revenue_gnosis_app_cohorts_monthly` | API | API view over fct_revenue_gnosis_app_cohorts_monthly. |
| `api_revenue_gnosis_app_cohorts_weekly` | API | API view over fct_revenue_gnosis_app_cohorts_weekly. |

**Gpay**

| Model | Layer | Description |
|-------|-------|-------------|
| `int_revenue_gpay_fees_daily` | Intermediate | Daily per-user Gnosis Pay fees. Each ERC20 transfer to the GP settlement
address is treated as a payment; the per-pay... |
| `fct_revenue_gpay_cohorts_monthly` | Fact | Gnosis Pay stream — monthly per-payment fee "potential" revenue by
symbol and user $-cohort bucket. Same source as th... |
| `fct_revenue_gpay_cohorts_weekly` | Fact | Gnosis Pay stream — rolling-52-week per-payment fee "potential" revenue
by payment token and user $-cohort bucket. Ea... |
| `api_revenue_gpay_cohorts_monthly` | API | API view over fct_revenue_gpay_cohorts_monthly. |
| `api_revenue_gpay_cohorts_weekly` | API | API view over fct_revenue_gpay_cohorts_weekly. |
| `api_revenue_gpay_eure_cohorts_monthly` | API | EURe Gnosis Pay monthly cohort API view. |
| `api_revenue_gpay_eure_cohorts_weekly` | API | EURe Gnosis Pay rolling-52w cohort API view. |
| `api_revenue_gpay_gbpe_cohorts_monthly` | API | GBPe Gnosis Pay monthly cohort API view. |
| `api_revenue_gpay_gbpe_cohorts_weekly` | API | GBPe Gnosis Pay rolling-52w cohort API view. |
| `api_revenue_gpay_usdce_cohorts_monthly` | API | USDC.e Gnosis Pay monthly cohort API view. |
| `api_revenue_gpay_usdce_cohorts_weekly` | API | USDC.e Gnosis Pay rolling-52w cohort API view. |

**Holdings**

| Model | Layer | Description |
|-------|-------|-------------|
| `int_revenue_holdings_fees_daily` | Intermediate | Daily per-user imputed holdings fees for EURe, USDC.e, BRLA, ZCHF.
`fees = balance_usd * daily_rate_for_symbol`, wher... |
| `fct_revenue_holdings_cohorts_monthly` | Fact | Holdings stream — monthly imputed-interest "potential" revenue by
symbol and user $-cohort bucket. Same source stream... |
| `fct_revenue_holdings_cohorts_weekly` | Fact | Holdings stream — rolling-52-week imputed-interest "potential" revenue
by token symbol and user $-cohort bucket. Each... |
| `api_revenue_holdings_brla_cohorts_monthly` | API | BRLA holdings monthly cohort API view. |
| `api_revenue_holdings_brla_cohorts_weekly` | API | BRLA holdings rolling-52w cohort API view. |
| `api_revenue_holdings_cohorts_monthly` | API | API view over fct_revenue_holdings_cohorts_monthly. |
| `api_revenue_holdings_cohorts_weekly` | API | API view over fct_revenue_holdings_cohorts_weekly. |
| `api_revenue_holdings_eure_cohorts_monthly` | API | EURe holdings monthly cohort API view. |
| `api_revenue_holdings_eure_cohorts_weekly` | API | EURe holdings rolling-52w cohort API view. |
| `api_revenue_holdings_usdce_cohorts_monthly` | API | USDC.e holdings monthly cohort API view. |
| `api_revenue_holdings_usdce_cohorts_weekly` | API | USDC.e holdings rolling-52w cohort API view. |
| `api_revenue_holdings_zchf_cohorts_monthly` | API | ZCHF holdings monthly cohort API view. |
| `api_revenue_holdings_zchf_cohorts_weekly` | API | ZCHF holdings rolling-52w cohort API view. |

**Ocsdai**

| Model | Layer | Description |
|-------|-------|-------------|
| `int_revenue_ocsdai_user_balances_daily` | Intermediate | OpenCover OC-sDAI ERC-4626 vault look-through for the sDAI revenue stream.
Per (date, user) USD value of the sDAI und... |

**Per**

| Model | Layer | Description |
|-------|-------|-------------|
| `fct_revenue_per_user_monthly` | Fact | Monthly per-user revenue. Same shape as the weekly variant but at
calendar-month grain with `month_fees_total` (no ro... |
| `fct_revenue_per_user_weekly` | Fact | One row per (week, user_pseudonym). Sums `annual_rolling_fees` across
all streams (holdings + sDAI + gpay) for each u... |
| `api_revenue_per_user_monthly` | API | API view over fct_revenue_per_user_monthly. Per-user monthly revenue
keyed on `user_pseudonym`. Filterable by month r... |
| `api_revenue_per_user_weekly` | API | API view over fct_revenue_per_user_weekly. Per-user weekly revenue
keyed on `user_pseudonym` — the canonical join key... |

**Sdai**

| Model | Layer | Description |
|-------|-------|-------------|
| `int_revenue_sdai_fees_daily` | Intermediate | Daily per-user sDAI revenue accruing to the DAO.
Methodology: `fees = balance_usd * sdai_daily_rate * dao_share_pct`,... |
| `fct_revenue_sdai_cohorts_monthly` | Fact | sDAI / Savings xDAI stream — monthly imputed-yield "potential" revenue
by user $-cohort bucket. Same source as the we... |
| `fct_revenue_sdai_cohorts_weekly` | Fact | sDAI / Savings xDAI stream — rolling-52-week imputed-yield "potential"
revenue by user $-cohort bucket. Each user's i... |
| `api_revenue_sdai_cohorts_monthly` | API | API view over fct_revenue_sdai_cohorts_monthly. |
| `api_revenue_sdai_cohorts_weekly` | API | API view over fct_revenue_sdai_cohorts_weekly. |

<!-- END AUTO-GENERATED: models-revenue -->
