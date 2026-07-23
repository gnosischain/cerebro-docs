# Quarterly Data Module

<!-- BEGIN AUTO-GENERATED: models-quarterly_data -->
<!-- generated: 2026-07-23 -->
**Data**

| Model | Layer | Description |
|-------|-------|-------------|
| `api_quarterly_data_carbon_emissions` | API | Quarterly annualised CO2 emissions (tonnes/yr) from end-of-quarter snapshot, with estimation flag for periods using f... |
| `api_quarterly_data_circles_active_minters` | API | Quarterly peak of blacklist-excluded Circles v2 Active Minters (the +80% mint-coverage cohort). Matches the Dune circ... |
| `api_quarterly_data_circles_active_trusts` | API | End-of-quarter active trust links in Circles v2. |
| `api_quarterly_data_circles_backers` | API | Quarterly currently-trusted Circles backers, as of quarter end (revocation-aware). A backer is an address currently t... |
| `api_quarterly_data_circles_humans` | API | End-of-quarter total registered human avatars in Circles v2. |
| `api_quarterly_data_circles_total_supply` | API | End-of-quarter Circles v2 token supply (raw and demurraged). |
| `api_quarterly_data_energy_consumption` | API | Quarterly annualised energy consumption (MWh/yr) from end-of-quarter snapshot, with estimation flag for periods using... |
| `api_quarterly_data_gnosis_app_peak_swappers` | API | Peak daily unique swappers on Gnosis App within the quarter. |
| `api_quarterly_data_gnosis_app_swap_volume` | API | Total swap volume in USD on Gnosis App per quarter. |
| `api_quarterly_data_gnosis_app_swaps` | API | Total swap transactions on Gnosis App per quarter. |
| `api_quarterly_data_gnosis_app_swaps_filled` | API | Total filled swap transactions on Gnosis App per quarter. |
| `api_quarterly_data_gpay_active_users` | API | Peak monthly active users for Gnosis Pay within the quarter, on two bases: all-activity (peak_monthly_active_users) a... |
| `api_quarterly_data_gpay_cashback` | API | Total Gnosis Pay cashback in USD per quarter. |
| `api_quarterly_data_gpay_payments` | API | Total Gnosis Pay payment transactions per quarter. |
| `api_quarterly_data_gpay_volume` | API | Total Gnosis Pay payment volume in USD per quarter. |
| `api_quarterly_data_nodes_estimated` | API | Quarterly end-of-quarter estimated total node count (observed + unobserved) with 95% confidence interval, sourced fro... |
| `api_quarterly_data_nodes_observed` | API | Quarterly end-of-quarter observed (directly reachable) node count from the node classification model. |
| `api_quarterly_data_stablecoin_holder_cohorts` | API | End-of-quarter stablecoin holder distribution by USD balance bucket, split into USD-pegged (WxDAI, sDAI, USDC, USDC.e... |
| `api_quarterly_data_stablecoin_holders` | API | Quarterly stablecoin holder statistics on Gnosis Chain, split by peg class plus a 'total' row (column-wise sum of the... |
| `api_quarterly_data_stablecoin_supply` | API | Quarterly stablecoin supply statistics on Gnosis Chain, split by peg class (USD-pegged vs non-USD) plus a 'total' row... |
| `api_quarterly_data_stablecoin_transfers` | API | Quarterly stablecoin transfer count and volume on Gnosis Chain, split by peg class (USD-pegged vs non-USD) plus a 'to... |
| `api_quarterly_data_staked_gno` | API | End-of-quarter GNO staked on Gnosis Chain (effective balance in real GNO; mGNO->GNO conversion happens upstream in in... |
| `api_quarterly_data_transactions_count` | API | Total successful transactions per quarter on Gnosis Chain. |
| `api_quarterly_data_validators_active` | API | End-of-quarter count of active validators on Gnosis Chain (the full active set = active_ongoing + active_exiting), ma... |

**Esg**

| Model | Layer | Description |
|-------|-------|-------------|
| `int_quarterly_esg_carbon_footprint_with_fallback` | Intermediate | Extends fct_esg_carbon_footprint_uncertainty with estimated daily CO2 and energy values for periods where Ember carbo... |
| `int_quarterly_esg_carbon_intensity_with_fallback` | Intermediate | Forward-fills Ember carbon intensity data for periods where values are missing (Jan 2026+). Carries the last known ca... |

**Stablecoin**

| Model | Layer | Description |
|-------|-------|-------------|
| `int_quarterly_stablecoin_cohorts_stats` | Intermediate | Pre-computed quarterly statistics (min, max, avg, median) for stablecoin holder cohorts by balance bucket and peg cla... |

<!-- END AUTO-GENERATED: models-quarterly_data -->
