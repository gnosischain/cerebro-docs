# Execution Module

The Execution module is the largest module in dbt-cerebro with approximately **208 models**. It covers all data produced by the Gnosis Chain execution layer (EVM), including blocks, transactions, logs, traces, contract deployments, native transfers, balance diffs, gas metrics, and DeFi yield tracking.

## Data Sources

Raw data is sourced from the `execution` ClickHouse database, which contains:

- **blocks** -- Block headers with timestamps, gas limits, base fees, and miner/proposer info
- **transactions** -- All on-chain transactions with input data, gas usage, and receipt status
- **logs** -- EVM event logs emitted by smart contracts
- **traces** -- Internal transaction traces (call, create, suicide, reward)
- **contracts** -- Deployed contract metadata and bytecodes
- **native_transfers** -- xDAI (native token) transfers extracted from traces
- **balance_diffs** -- State-level balance changes per block

## Model Categories

<!-- BEGIN AUTO-GENERATED: models-execution -->
**Blocks**

| Model | Layer | Description |
|-------|-------|-------------|
| `int_execution_blocks_clients_version_daily` | Intermediate | The model aggregates daily counts of execution blocks grouped by client and version, supporting incremental updates f... |
| `int_execution_blocks_gas_usage_daily` | Intermediate | This model aggregates daily gas usage and limits from execution blocks to monitor gas consumption efficiency over time. |
| `fct_execution_blocks_clients_daily` | Fact | The fct_execution_blocks_clients_daily model aggregates daily execution block counts per client, providing insights i... |
| `fct_execution_blocks_gas_usage_monthly` | Fact | The fct_execution_blocks_gas_usage_monthly model aggregates monthly gas usage and limits for execution blocks to supp... |
| `api_execution_blocks_clients_cnt_daily` | API | The api_execution_blocks_clients_cnt_daily model provides daily aggregated counts of API execution blocks per client,... |
| `api_execution_blocks_clients_pct_daily` | API | The api_execution_blocks_clients_pct_daily model provides daily percentage metrics of API execution blocks per client... |
| `api_execution_blocks_gas_usage_pct_daily` | API | The api_execution_blocks_gas_usage_pct_daily model provides daily insights into the percentage of gas used by API exe... |
| `api_execution_blocks_gas_usage_pct_monthly` | API | This model provides a monthly percentage of gas usage for execution blocks, enabling analysis of gas consumption tren... |

**Circles**

| Model | Layer | Description |
|-------|-------|-------------|
| `int_execution_circles_backing` | Intermediate | The `int_execution_circles_backing` model aggregates daily counts of completed circles backing events to monitor exec... |
| `int_execution_circles_transitive_transfers` | Intermediate | The model calculates daily transitive transfer volumes between avatars involved in circle-based contracts, aggregatin... |
| `int_execution_circles_v2_avatars` | Intermediate | This model aggregates daily counts of avatar registrations by type (Human, Group, Organization) to monitor user onboa... |
| `fct_execution_circles_avatars` | Fact | The fct_execution_circles_avatars model provides a daily time series of avatar type counts within execution circles, ... |
| `fct_execution_circles_backing` | Fact | The fct_execution_circles_backing model provides a daily cumulative count of execution circle backing events, facilit... |
| `api_execution_circles_avatars` | API | The api_execution_circles_avatars view aggregates daily counts of avatar types used in API executions within circles,... |
| `api_execution_circles_backers_cnt_latest` | API | This view provides the latest count of backers for API executions and the percentage change compared to the count fro... |
| `api_execution_circles_groups_cnt_latest` | API | This view provides the latest total count of group avatars and the percentage change compared to the count from seven... |
| `api_execution_circles_humans_cnt_latest` | API | This view provides the latest count of human avatars and the percentage change compared to the count from seven days ... |
| `api_execution_circles_orgs_cnt_latest` | API | This view provides the latest count of organization avatars and the percentage change compared to the count from seve... |

**Data**

| Model | Layer | Description |
|-------|-------|-------------|
| `fct_crawlers_data_distinct_projects_sectors` | Fact | This model identifies unique combinations of projects and sectors from crawler data, supporting analysis of project-s... |
| `api_crawlers_data_distinct_projects_sectors_totals` | API | This view aggregates the total number of distinct projects and sectors crawled, providing a high-level overview of da... |

**Deposists**

| Model | Layer | Description |
|-------|-------|-------------|
| `int_GBCDeposit_deposists_daily` | Intermediate | The `int_GBCDeposit_deposists_daily` view aggregates daily deposit amounts and withdrawal credentials from GBC deposi... |

**Gpay**

| Model | Layer | Description |
|-------|-------|-------------|
| `int_execution_gpay_activity` | Intermediate | Incremental model that captures individual Gnosis Pay wallet transactions including payments, deposits, withdrawals, ... |
| `int_execution_gpay_activity_daily` | Intermediate | Incremental model that aggregates Gnosis Pay wallet activity at the daily level, grouped by wallet, action, direction... |
| `int_execution_gpay_balances_daily` | Intermediate | Incremental model that tracks daily token balances for each Gnosis Pay wallet address, with both native and USD values. |
| `int_execution_gpay_wallet_owners` | Intermediate | Incremental model that maps Gnosis Pay wallet addresses to their owner addresses and safe thresholds. |
| `fct_execution_gpay_actions_by_token_daily` | Fact | Daily aggregation of Gnosis Pay activity metrics broken down by action type and token, with cumulative totals. |
| `fct_execution_gpay_actions_by_token_monthly` | Fact | Monthly aggregation of Gnosis Pay activity metrics broken down by action type and token, with cumulative totals. |
| `fct_execution_gpay_actions_by_token_weekly` | Fact | Weekly aggregation of Gnosis Pay activity metrics broken down by action type and token, with cumulative totals. |
| `fct_execution_gpay_activity_daily` | Fact | Daily summary of Gnosis Pay ecosystem activity including active users, payments, volume, and funded wallet counts. |
| `fct_execution_gpay_activity_monthly` | Fact | Monthly summary of Gnosis Pay ecosystem activity including active users, payments, volume, and funded wallet counts. |
| `fct_execution_gpay_activity_weekly` | Fact | Weekly summary of Gnosis Pay ecosystem activity including active users, payments, volume, and funded wallet counts. |
| `fct_execution_gpay_balance_cohorts_daily` | Fact | Daily distribution of Gnosis Pay wallet balances segmented into cohort buckets by token, showing holder counts and va... |
| `fct_execution_gpay_balances_by_token_daily` | Fact | Daily aggregate token balances across all Gnosis Pay wallets, in both native and USD values. |
| `fct_execution_gpay_cashback_cohort_retention_monthly` | Fact | Monthly cohort retention analysis for Gnosis Pay cashback recipients, tracking user counts and retention percentages ... |
| `fct_execution_gpay_cashback_dist_weekly` | Fact | Weekly distribution of Gnosis Pay cashback amounts using percentile statistics. |
| `fct_execution_gpay_cashback_impact_monthly` | Fact | Monthly analysis of cashback impact on Gnosis Pay user segments, comparing payment behavior between cashback and non-... |
| `fct_execution_gpay_cashback_recipients_weekly` | Fact | Weekly count of unique Gnosis Pay cashback recipients. |
| `fct_execution_gpay_churn_monthly` | Fact | Monthly user churn and retention analysis for Gnosis Pay, breaking down users into new, retained, returning, and chur... |
| `fct_execution_gpay_flows_snapshot` | Fact | Snapshot of token flow patterns between Gnosis Pay wallet labels across different time windows. |
| `fct_execution_gpay_kpi_monthly` | Fact | Monthly key performance indicators for Gnosis Pay including MAU, payment volume, deposits, withdrawals, cashback, and... |
| `fct_execution_gpay_owner_balances_by_token_daily` | Fact | Daily aggregate token balances across Gnosis Pay wallet owners (as opposed to wallet addresses), in both native and U... |
| `fct_execution_gpay_payments_hourly` | Fact | Hourly payment counts for Gnosis Pay broken down by token symbol. |
| `fct_execution_gpay_retention_by_action_monthly` | Fact | Monthly cohort retention analysis for Gnosis Pay users broken down by action type, tracking user counts and retention... |
| `fct_execution_gpay_retention_monthly` | Fact | Monthly cohort retention analysis for all Gnosis Pay activity, tracking user counts and retention percentages over time. |
| `fct_execution_gpay_snapshots` | Fact | Summary snapshot metrics for Gnosis Pay across different time windows (All, 7D), providing headline KPIs with percent... |
| `fct_execution_gpay_user_lifetime_metrics` | Fact | Lifetime metrics for each Gnosis Pay wallet, including tenure, activity counts, payment volumes, and cashback totals. |
| `api_execution_gpay_active_users_7d` | API | 7-day active user count with period-over-period change percentage for Gnosis Pay. |
| `api_execution_gpay_active_users_weekly` | API | Weekly time series of Gnosis Pay active user counts. |
| `api_execution_gpay_activity_by_action_daily` | API | Daily Gnosis Pay activity metrics broken down by action type, with counts and volumes. |
| `api_execution_gpay_activity_by_action_monthly` | API | Monthly Gnosis Pay activity metrics broken down by action type, with counts and volumes. |
| `api_execution_gpay_activity_by_action_weekly` | API | Weekly Gnosis Pay activity metrics broken down by action type, with counts and volumes. |
| `api_execution_gpay_balance_cohorts_holders_daily` | API | Daily count of Gnosis Pay wallet holders in each balance cohort bucket by token. |
| `api_execution_gpay_balance_cohorts_value_daily` | API | Daily total value held in each balance cohort bucket by token, in native and USD. |
| `api_execution_gpay_balances_by_token_daily` | API | Daily total Gnosis Pay wallet balances by token in USD. |
| `api_execution_gpay_balances_native_daily` | API | Daily total Gnosis Pay wallet balances by token in native units. |
| `api_execution_gpay_balances_usd_daily` | API | Daily total Gnosis Pay wallet balances by token in USD. |
| `api_execution_gpay_cashback_7d` | API | 7-day cashback summary with unit breakdown and period-over-period change percentage. |
| `api_execution_gpay_cashback_cohort_retention_monthly` | API | Monthly cashback cohort retention heatmap data showing retention and amount percentages across cohorts. |
| `api_execution_gpay_cashback_cohort_retention_users_monthly` | API | Monthly cashback cohort sizes over time, formatted for time series visualization. |
| `api_execution_gpay_cashback_cumulative` | API | Cumulative cashback distributed over time by unit. |
| `api_execution_gpay_cashback_dist_weekly` | API | Weekly cashback distribution percentiles for Gnosis Pay users. |
| `api_execution_gpay_cashback_impact_monthly` | API | Monthly cashback impact analysis comparing payment behavior between user segments. Passes through all columns from th... |
| `api_execution_gpay_cashback_recipients_7d` | API | 7-day unique cashback recipient count with period-over-period change percentage. |
| `api_execution_gpay_cashback_recipients_total` | API | All-time total count of unique Gnosis Pay cashback recipients. |
| `api_execution_gpay_cashback_recipients_weekly` | API | Weekly time series of unique Gnosis Pay cashback recipient counts. |
| `api_execution_gpay_cashback_total` | API | All-time total cashback distributed by unit. |
| `api_execution_gpay_cashback_weekly` | API | Weekly cashback amounts distributed by unit. |
| `api_execution_gpay_churn_monthly` | API | Monthly user churn breakdown for Gnosis Pay showing user segments and rates by activity scope. |
| `api_execution_gpay_churn_rates_monthly` | API | Monthly churn and retention rates for Gnosis Pay by activity scope. |
| `api_execution_gpay_flows_snapshot` | API | Token flow patterns between Gnosis Pay wallet labels for API consumption. |
| `api_execution_gpay_funded_addresses_daily` | API | Daily time series of cumulative funded Gnosis Pay wallet addresses. |
| `api_execution_gpay_funded_addresses_monthly` | API | Monthly time series of cumulative funded Gnosis Pay wallet addresses. |
| `api_execution_gpay_funded_addresses_weekly` | API | Weekly time series of cumulative funded Gnosis Pay wallet addresses. |
| `api_execution_gpay_gno_balance_daily` | API | Daily total GNO token balance across all Gnosis Pay wallets. |
| `api_execution_gpay_gno_total_balance` | API | Current total GNO token balance across all Gnosis Pay wallets. |
| `api_execution_gpay_kpi_monthly` | API | Monthly KPIs for Gnosis Pay, passing through all columns from the fact model. |
| `api_execution_gpay_owner_balances_by_token_daily` | API | Daily total Gnosis Pay owner balances by token in USD. |
| `api_execution_gpay_owner_total_balance` | API | Current total balance across all Gnosis Pay wallet owners in USD. |
| `api_execution_gpay_payments_7d` | API | 7-day payment count with period-over-period change percentage. |
| `api_execution_gpay_payments_by_token_daily` | API | Daily payment counts by token for Gnosis Pay. |
| `api_execution_gpay_payments_by_token_monthly` | API | Monthly payment counts by token for Gnosis Pay. |
| `api_execution_gpay_payments_by_token_weekly` | API | Weekly payment counts by token for Gnosis Pay. |
| `api_execution_gpay_payments_hourly` | API | Hourly payment counts by token for Gnosis Pay. |
| `api_execution_gpay_retention_by_action_monthly` | API | Monthly cohort retention heatmap data for Gnosis Pay broken down by action type. |
| `api_execution_gpay_retention_by_action_users_monthly` | API | Monthly cohort user counts over time by action type, formatted for time series visualization. |
| `api_execution_gpay_retention_monthly` | API | Monthly cohort user counts over time, formatted for time series visualization. |
| `api_execution_gpay_retention_pct_monthly` | API | Monthly cohort retention heatmap data for all Gnosis Pay activity. |
| `api_execution_gpay_retention_volume_monthly` | API | Monthly cohort volume retention over time, formatted for time series visualization. |
| `api_execution_gpay_total_balance` | API | Current total balance across all Gnosis Pay wallets in USD. |
| `api_execution_gpay_total_funded` | API | All-time total count of funded Gnosis Pay wallets (users who made at least one payment). |
| `api_execution_gpay_total_payments` | API | All-time total count of Gnosis Pay payments. |
| `api_execution_gpay_total_volume` | API | All-time total payment volume for Gnosis Pay in USD. |
| `api_execution_gpay_user_activity` | API | Individual transaction-level activity for a specific Gnosis Pay user, filtered by wallet address. |
| `api_execution_gpay_user_balances_daily` | API | Daily token balances for a specific Gnosis Pay user in native and USD values. |
| `api_execution_gpay_user_cashback_daily` | API | Daily cashback amounts for a specific Gnosis Pay user. |
| `api_execution_gpay_user_lifetime_metrics` | API | Lifetime metrics for a specific Gnosis Pay user, passing through all columns from the fact model. |
| `api_execution_gpay_user_payments_daily` | API | Daily payment amounts by token for a specific Gnosis Pay user. |
| `api_execution_gpay_user_total_cashback` | API | All-time total cashback for a specific Gnosis Pay user. |
| `api_execution_gpay_user_total_payments` | API | All-time total payment count for a specific Gnosis Pay user. |
| `api_execution_gpay_user_total_volume` | API | All-time total payment volume for a specific Gnosis Pay user. |
| `api_execution_gpay_volume_7d` | API | 7-day payment volume with period-over-period change percentage. |
| `api_execution_gpay_volume_payments_by_token_daily` | API | Daily payment volume by token in USD for Gnosis Pay. |
| `api_execution_gpay_volume_payments_by_token_monthly` | API | Monthly payment volume by token in USD for Gnosis Pay. |
| `api_execution_gpay_volume_payments_by_token_weekly` | API | Weekly payment volume by token in USD for Gnosis Pay. |
| `api_execution_gpay_wallet_balance_composition` | API | Current balance composition of a Gnosis Pay wallet by token. |

**Rwa**

| Model | Layer | Description |
|-------|-------|-------------|
| `int_execution_rwa_backedfi_prices` | Intermediate | The model aggregates daily closing prices for various backed financial instruments from Oracle event data, supporting... |
| `fct_execution_rwa_backedfi_prices_daily` | Fact | The fct_execution_rwa_backedfi_prices_daily view consolidates daily price data for various backed finance instruments... |
| `api_execution_rwa_backedfi_prices_daily` | API | The api_execution_rwa_backedfi_prices_daily model provides daily pricing data for RWA-backed financial instruments to... |

**State**

| Model | Layer | Description |
|-------|-------|-------------|
| `int_execution_state_size_full_diff_daily` | Intermediate | This model calculates the daily net change in storage size for execution states by aggregating storage diffs, support... |
| `fct_execution_state_full_size_daily` | Fact | The fct_execution_state_full_size_daily model aggregates daily cumulative bytes of execution state data, providing in... |
| `api_execution_state_full_size_daily` | API | The api_execution_state_full_size_daily model provides daily aggregated data on the size of API execution states, fac... |

**Storage**

| Model | Layer | Description |
|-------|-------|-------------|
| `stg_execution__storage_diffs` | Staging | The stg_execution__storage_diffs model captures storage difference events from blockchain execution transactions, ena... |

**Token**

| Model | Layer | Description |
|-------|-------|-------------|
| `int_execution_token_prices_daily` | Intermediate | The `int_execution_token_prices_daily` view consolidates daily price data for various tokens and stablecoins used in ... |

**Tokens**

| Model | Layer | Description |
|-------|-------|-------------|
| `int_execution_tokens_address_diffs_daily` | Intermediate | This model calculates daily net address-level token transfer deltas, capturing inflows and outflows for each address ... |
| `int_execution_tokens_balance_cohorts_daily` | Intermediate | Daily token balance cohort distributions, segmenting holders into balance buckets. |
| `int_execution_tokens_balances_by_sector_daily` | Intermediate | Daily balances aggregated by sector labels for each token. |
| `int_execution_tokens_balances_daily` | Intermediate | The int_execution_tokens_balances_daily model tracks the daily balances of tokens for various addresses, incorporatin... |
| `int_execution_tokens_supply_holders_daily` | Intermediate | Daily supply and holder counts aggregated by token. |
| `int_execution_tokens_transfers_daily` | Intermediate | The int_execution_tokens_transfers_daily model aggregates daily transfer metrics for tokens, providing insights into ... |
| `fct_execution_tokens_metrics_daily` | Fact | -- |
| `fct_execution_tokens_overview_by_class_latest` | Fact | -- |
| `fct_execution_tokens_supply_by_sector_latest` | Fact | -- |
| `fct_execution_tokens_supply_distribution_latest` | Fact | -- |
| `api_execution_tokens_active_senders_daily` | API | This view provides daily counts of active senders per API token, enabling analysis of token engagement over time. |
| `api_execution_tokens_balance_cohorts_holders_daily` | API | This view provides daily snapshots of token balance cohort distributions among holders, enabling analysis of holder s... |
| `api_execution_tokens_balance_cohorts_value_daily` | API | This view aggregates daily token balance cohort values, segmented by balance buckets, to support analysis of token ho... |
| `api_execution_tokens_balances_daily` | API | -- |
| `api_execution_tokens_holders_daily` | API | The api_execution_tokens_holders_daily model provides daily aggregated data on the number of unique token holders for... |
| `api_execution_tokens_holders_latest_by_token` | API | This model provides the latest snapshot of the number of holders for each API token, aggregated by token symbol, to s... |
| `api_execution_tokens_overview_latest` | API | -- |
| `api_execution_tokens_supply_by_sector_latest` | API | -- |
| `api_execution_tokens_supply_daily` | API | The api_execution_tokens_supply_daily model provides daily aggregated data on the supply of different API tokens, sup... |
| `api_execution_tokens_supply_distribution_latest` | API | -- |
| `api_execution_tokens_supply_latest_by_token` | API | This model provides the latest supply values for each API token based on daily recorded data, enabling tracking of to... |
| `api_execution_tokens_volume_daily` | API | The api_execution_tokens_volume_daily model provides daily aggregated data on the trading volume of different tokens ... |

**Transactions**

| Model | Layer | Description |
|-------|-------|-------------|
| `int_execution_transactions_by_project_alltime_state` | Intermediate | This model aggregates execution transaction data by project and month, providing insights into transaction volume, fe... |
| `int_execution_transactions_by_project_daily` | Intermediate | This model aggregates daily execution transaction data by project, providing insights into transaction volume, user e... |
| `int_execution_transactions_by_project_hourly_recent` | Intermediate | This model aggregates hourly execution transaction data by project for the recent two-day period, providing insights ... |
| `int_execution_transactions_info_daily` | Intermediate | The `int_execution_transactions_info_daily` model aggregates daily transaction data from the execution layer, providi... |
| `fct_execution_transactions_by_project_monthly_top5` | Fact | This model aggregates and ranks execution transactions by project on a monthly basis, highlighting the top 5 projects... |
| `fct_execution_transactions_by_project_snapshots` | Fact | This model aggregates transaction, fee, and active account data by project over various time windows, enabling compar... |
| `fct_execution_transactions_by_sector_daily` | Fact | The fct_execution_transactions_by_sector_daily model aggregates daily execution transaction data by sector to support... |
| `fct_execution_transactions_by_sector_weekly` | Fact | The fct_execution_transactions_by_sector_weekly model aggregates weekly transaction data by sector to support busines... |
| `fct_execution_transactions_snapshots` | Fact | This table provides snapshot metrics of execution transactions, including counts, fees, and active account counts ove... |
| `api_execution_transactions_7d` | API | The api_execution_transactions_7d model provides a snapshot of the total number of API execution transactions and the... |
| `api_execution_transactions_active_accounts_7d` | API | This view provides a snapshot of the number of active accounts involved in API transactions over the last 7 days, ena... |
| `api_execution_transactions_active_accounts_by_project_monthly_top5` | API | This view aggregates the number of active accounts involved in API execution transactions, focusing on the top 5 proj... |
| `api_execution_transactions_active_accounts_by_project_ranges_top20` | API | This model identifies the top 20 project ranges with the highest number of active accounts over different time window... |
| `api_execution_transactions_active_accounts_by_project_total` | API | This view provides a snapshot of the total number of active accounts involved in API execution transactions across al... |
| `api_execution_transactions_active_accounts_by_sector_daily` | API | This view provides daily counts of active accounts involved in API transaction initiations, segmented by sector, to m... |
| `api_execution_transactions_active_accounts_by_sector_hourly` | API | This view aggregates the count of active accounts involved in API execution transactions, segmented by sector and hou... |
| `api_execution_transactions_active_accounts_by_sector_weekly` | API | This view provides weekly counts of active accounts involved in API execution transactions, segmented by sector, to s... |
| `api_execution_transactions_active_accounts_total` | API | The `api_execution_transactions_active_accounts_total` model provides a snapshot of the total number of active accoun... |
| `api_execution_transactions_by_project_monthly_top5` | API | This view aggregates the top 5 projects by transaction count on a monthly basis, enabling analysis of project activit... |
| `api_execution_transactions_by_project_ranges_top20` | API | This view aggregates the top 20 API transaction counts per project within specified time ranges, providing insights i... |
| `api_execution_transactions_by_project_total` | API | This view aggregates the total number of API execution transactions across all projects over the entire time period, ... |
| `api_execution_transactions_by_sector_daily` | API | The api_execution_transactions_by_sector_daily model provides daily aggregated counts of API execution transactions c... |
| `api_execution_transactions_by_sector_hourly` | API | This view aggregates the total number of API execution transactions per sector on an hourly basis, providing insights... |
| `api_execution_transactions_by_sector_weekly` | API | The api_execution_transactions_by_sector_weekly model aggregates the number of API execution transactions per sector ... |
| `api_execution_transactions_cnt_daily` | API | The api_execution_transactions_cnt_daily model provides a daily summary of successful API transaction counts categori... |
| `api_execution_transactions_cnt_total` | API | This view aggregates the total number of successful API transactions grouped by transaction type across all time, pro... |
| `api_execution_transactions_fees_native_7d` | API | The api_execution_transactions_fees_native_7d model provides a snapshot of native transaction fees and their percenta... |
| `api_execution_transactions_fees_native_by_project_monthly_top5` | API | This view aggregates the top 5 projects by native transaction fees on a monthly basis, providing insights into fee di... |
| `api_execution_transactions_fees_native_by_project_ranges_top20` | API | This view aggregates the top 20 native API transaction fee buckets by project for different time ranges, providing in... |
| `api_execution_transactions_fees_native_by_project_total` | API | This view aggregates total native execution transaction fees per project over the entire available time span, enablin... |
| `api_execution_transactions_fees_native_by_sector_daily` | API | This view aggregates daily native transaction fees by sector, providing insights into sector-specific fee trends over... |
| `api_execution_transactions_fees_native_by_sector_hourly` | API | This view aggregates native transaction fees by sector on an hourly basis, providing insights into fee distribution a... |
| `api_execution_transactions_fees_native_by_sector_weekly` | API | This view aggregates native transaction fees by sector on a weekly basis to support analysis of fee trends across dif... |
| `api_execution_transactions_fees_native_total` | API | The `api_execution_transactions_fees_native_total` model aggregates total native execution transaction fees over all ... |
| `api_execution_transactions_gas_share_by_project_daily` | API | This view calculates the daily share of gas used by each project in relation to the total gas consumption across all ... |
| `api_execution_transactions_gas_used_daily` | API | This view aggregates daily gas consumption and pricing metrics for successful API transaction executions, facilitatin... |
| `api_execution_transactions_gas_used_weekly` | API | This view aggregates weekly gas usage for successful API transactions, categorized by transaction type, to support pe... |
| `api_execution_transactions_total` | API | The api_execution_transactions_total model provides a consolidated count of API execution transactions over the entir... |
| `api_execution_transactions_value_daily` | API | This view aggregates daily transaction values for API executions on the xDai network, providing insights into transac... |

**Transfers**

| Model | Layer | Description |
|-------|-------|-------------|
| `int_execution_transfers_whitelisted_daily` | Intermediate | The `int_execution_transfers_whitelisted_daily` model aggregates daily whitelisted token transfer data, including dep... |

**Wallets**

| Model | Layer | Description |
|-------|-------|-------------|
| `stg_gpay__wallets` | Staging | Staging model that extracts distinct Gnosis Pay wallet addresses from the crawlers data labels, filtering for the gpa... |

<!-- END AUTO-GENERATED: models-execution -->

## Query Examples

Retrieve daily transaction counts for the past 30 days:

```sql
SELECT dt, txs, gas_used, success_rate
FROM dbt.api_execution_transactions_daily
WHERE dt >= today() - 30
ORDER BY dt
```

Check gas price trends:

```sql
SELECT dt, avg_gas_price, median_gas_price, p95_gas_price
FROM dbt.api_execution_gas_daily
WHERE dt >= today() - 7
ORDER BY dt
```

## Related Modules

- [Contracts](contracts.md) -- Protocol-specific decoded event data built on top of execution logs
- [Bridges](bridges.md) -- Bridge flow analytics derived from execution transactions and logs
- [ESG](esg.md) -- Energy consumption estimates based on execution block production data
