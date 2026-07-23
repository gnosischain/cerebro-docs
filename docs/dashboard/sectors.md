# Dashboard Sectors

The metrics dashboard is organized into **9 active sectors**, each covering a distinct area of Gnosis Chain analytics. Sectors are defined in `public/dashboard.yml` and rendered as top-level navigation items in the dashboard sidebar.

## Sector Overview

| Order | Sector | Description |
|-------|--------|-------------|
| 1 | [Overview](#overview) | High-level network health KPIs and summary charts |
| 2 | [Gnosis Pay](#gnosis-pay) | Gnosis Pay card transaction volume, wallet counts, and spend analytics |
| 3 | [OnChain Activity](#onchain-activity) | Transaction volume, gas usage, active addresses, contract deployments |
| 4 | [Consensus](#consensus) | Validator counts, attestation performance, rewards, deposits, withdrawals |
| 5 | [Network](#network) | P2P network size, client distribution, geographic node spread |
| 6 | [Bridges](#bridges) | Bridge volume, netflow, token flow breakdowns, sankey visualizations |
| 7 | [Tokens](#tokens) | Token transfers, supply metrics, price trends for major Gnosis Chain tokens |
| 8 | [ESG](#esg) | Carbon emissions, power consumption, energy mix, node infrastructure |
| 9 | [Yields](#yields) | DeFi yield analytics: lending APY, LP fee APR, savings rates, user portfolio |

## Sector Details

<!-- BEGIN AUTO-GENERATED: dashboard-sectors -->
<!-- generated: 2026-07-23 -->
### Overview

| Metric | Chart Type | Description |
|--------|-----------|-------------|
| `overview_active_accounts` | number | -- |
| `overview_bridges_total_volume` | number | Cumulative all-time volume bridged into and out of Gnosis Chain. |
| `overview_esg` | number | Projected annual carbon emissions of Gnosis Chain, in tonnes of CO₂-equivalent. |
| `overview_gno_supply_daily` | area | Daily GNO supply components by source category. Stacked view shows how each source contributes to... |
| `overview_kpi_active_accounts` | kpi | Unique addresses that sent at least one transaction on Gnosis Chain on the most recent complete day. |
| `overview_kpi_circles_minters` | kpi | Circles v2 active minters (avatars whose personal CRC minting over the last 14 days is at least 8... |
| `overview_kpi_dex_volume` | kpi | Daily DEX trading volume across all protocols (Uniswap V3, Balancer, Swapr) on Gnosis Chain, on t... |
| `overview_kpi_gpay_active_users` | kpi | Distinct Gnosis Pay wallets that made at least one card payment on the most recent complete day. |
| `overview_kpi_gpay_volume` | kpi | Total USD value of Gnosis Pay card payments on the most recent complete day. |
| `overview_kpi_stablecoin_supply` | kpi | Total USD value of stablecoins circulating on Gnosis Chain, excluding sDAI, WxDAI and BRZ (BRZ ha... |
| `overview_kpi_staked_gno` | kpi | Total GNO staked in the Gnosis Chain consensus layer. |
| `overview_kpi_transactions` | kpi | All successful transactions on Gnosis Chain on the most recent complete day. |
| `overview_kpi_validators` | kpi | Number of validators in active_ongoing status on Gnosis Chain. Post-Pectra, validator count has d... |
| `overview_payments` | number | -- |
| `overview_stablecoins_supply_daily` | area | Daily circulating USD supply of stablecoins on Gnosis Chain (excluding sDAI, WxDAI and BRZ), stac... |
| `overview_stablecoins_supply_total` | number | -- |
| `overview_stake_api` | number | -- |
| `overview_stake_gno` | number | -- |
| `overview_transactions` | number | -- |
| `overview_transactions_daily` | area | All successful transactions on Gnosis Chain per day. |
| `overview_validators` | number | -- |
| `overview_yields_lending_tvl` | number | Total value locked across lending markets on Gnosis Chain. |

### Account Portfolio

*No query files found for Account Portfolio.*

### Gnosis Pay

| Metric | Chart Type | Description |
|--------|-----------|-------------|
| `api_execution_gpay_active_users_7d` | numberDisplay | Last 7 days |
| `api_execution_gpay_activity_by_action_weekly` | bar | Weekly Gnosis Pay activity segmented by action type. Toggle between action counts and USD volume. |
| `api_execution_gpay_balance_cohorts_holders_daily` | area | Daily wallet count grouped by balance cohort (e.g. 0–10, 10–100, 100–1K). Use the token dropdown ... |
| `api_execution_gpay_balance_cohorts_value_daily` | area | Daily aggregate balance grouped by balance cohort. Use the token dropdown and Native/USD toggle t... |
| `api_execution_gpay_balances_native_daily` | area | Daily aggregate balance in native token units. Use the dropdown to switch between EURe, GBPe, USD... |
| `api_execution_gpay_balances_usd_daily` | area | Daily aggregate wallet balances in USD, stacked by token (EURe, GBPe, USDC.e, GNO). The total lin... |
| `api_execution_gpay_cashback_7d` | numberDisplay | Last 7 days |
| `api_execution_gpay_cashback_cohort_retention_monthly` | heatmap | Payment retention after first cashback |
| `api_execution_gpay_cashback_cohort_retention_users_monthly` | bar | Stacked cohort user activity over time for first-cashback cohorts. |
| `api_execution_gpay_cashback_cumulative` | area | Cumulative GNO cashback distributed over time. Toggle between native GNO and USD. This curve is m... |
| `api_execution_gpay_cashback_dist_weekly` | quantileBands | Percentile bands of weekly per-user GNO cashback on a log scale. The median line (q50) shows the ... |
| `api_execution_gpay_cashback_impact_monthly` | bar | Compares payer behavior by dynamic cashback segments over time. |
| `api_execution_gpay_cashback_recipients_7d` | numberDisplay | Last 7 days |
| `api_execution_gpay_cashback_recipients_total` | numberDisplay | Total unique wallets that have received at least one GNO cashback reward from Gnosis Pay. |
| `api_execution_gpay_cashback_recipients_weekly` | bar | Weekly count of unique wallets that received at least one GNO cashback transfer. A wallet is coun... |
| `api_execution_gpay_cashback_total` | numberDisplay | All-time |
| `api_execution_gpay_cashback_weekly` | bar | Weekly GNO cashback distributed to Gnosis Pay users. Toggle between native GNO and USD value to c... |
| `api_execution_gpay_churn_monthly` | bar | New, retained, returning, churned |
| `api_execution_gpay_churn_rates_monthly` | line | Monthly lifecycle rates |
| `api_execution_gpay_flows_inout_by_label_snapshot` | bar | Signed inflow/outflow by counterparty label for the selected window and symbol. Inflow is positiv... |
| `api_execution_gpay_flows_snapshot` | graph | Explore directed flows between labels. Select a window and value mode, then inspect edge thicknes... |
| `api_execution_gpay_flows_total_volume_1d` | numberDisplay | Total flow |
| `api_execution_gpay_flows_total_volume_30d` | numberDisplay | Total flow |
| `api_execution_gpay_flows_total_volume_7d` | numberDisplay | Total flow |
| `api_execution_gpay_flows_total_volume_90d` | numberDisplay | Total flow |
| `api_execution_gpay_funded_addresses_weekly` | bar | Running total of wallets that have made their first Gnosis Pay card payment. Each bar shows the a... |
| `api_execution_gpay_gno_total_balance` | numberDisplay | Total GNO held across all Gnosis Pay wallets at the latest date. |
| `api_execution_gpay_kpi_activity_monthly` | line | MAU by activity type |
| `api_execution_gpay_kpi_arpu_latest` | numberDisplay | Latest month |
| `api_execution_gpay_kpi_flows_monthly` | line | Payments, deposits, withdrawals, net flow |
| `api_execution_gpay_kpi_mau_latest` | numberDisplay | Distinct wallets with any Gnosis Pay activity (payments, deposits, withdrawals, cashback) in the ... |
| `api_execution_gpay_kpi_payment_volume_latest` | numberDisplay | Latest month |
| `api_execution_gpay_kpi_repeat_purchase_rate_latest` | numberDisplay | Latest month |
| `api_execution_gpay_payments_7d` | numberDisplay | Last 7 days |
| `api_execution_gpay_payments_by_token_weekly` | bar | Weekly payment count split by token. Stacked bars show token mix and overall payment activity. |
| `api_execution_gpay_payments_hourly` | bar | Payment counts per hour over the last 14 complete days, broken down by token. Useful for spotting... |
| `api_execution_gpay_retention_by_action_monthly` | heatmap | Cohort retention heatmap by action type. Filter action and switch between users/volume views. |
| `api_execution_gpay_retention_by_action_users_monthly` | bar | Stacked cohort user activity over time. Filter by action type. |
| `api_execution_gpay_retention_monthly` | bar | By activation cohort |
| `api_execution_gpay_retention_pct_monthly` | heatmap | By activation cohort |
| `api_execution_gpay_retention_volume_monthly` | bar | By activation cohort, in USD |
| `api_execution_gpay_total_balance` | numberDisplay | Current |
| `api_execution_gpay_total_funded` | numberDisplay | All-time |
| `api_execution_gpay_total_payments` | numberDisplay | All-time |
| `api_execution_gpay_total_volume` | numberDisplay | All-time |
| `api_execution_gpay_user_actions_radar` | radar | Radar profile of lifetime action counts for the selected wallet across all supported Gnosis Pay a... |
| `api_execution_gpay_user_activity` | table | Actions include: Payment (card spend at merchant), Cashback (GNO reward), Fiat Top Up (bank trans... |
| `api_execution_gpay_user_balances_daily` | bar | Daily wallet balance by token |
| `api_execution_gpay_user_balances_latest` | pie | Latest USD balance by token |
| `api_execution_gpay_user_cashback_daily` | bar | Daily cashback received (GNO) |
| `api_execution_gpay_user_lifetime_avg_monthly_payment_volume_usd` | numberDisplay | Average monthly payment volume for months in which the selected wallet was active. |
| `api_execution_gpay_user_lifetime_inactivity_days` | numberDisplay | Days since the selected wallet last recorded Gnosis Pay activity. |
| `api_execution_gpay_user_lifetime_tenure_days` | numberDisplay | Days between first and last recorded Gnosis Pay activity for the selected wallet. |
| `api_execution_gpay_user_lifetime_total_cashback_usd` | numberDisplay | Total cashback received in USD by the selected wallet. |
| `api_execution_gpay_user_lifetime_total_deposit_volume_usd` | numberDisplay | Total lifetime deposit volume (fiat top-ups + crypto deposits) for the selected wallet. |
| `api_execution_gpay_user_lifetime_total_withdrawal_volume_usd` | numberDisplay | Total lifetime withdrawal volume (fiat off-ramps + crypto withdrawals) for the selected wallet. |
| `api_execution_gpay_user_payments_daily` | bar | Daily payment volume by token (USD) |
| `api_execution_gpay_user_total_cashback` | numberDisplay | Lifetime |
| `api_execution_gpay_user_total_volume` | numberDisplay | Lifetime |
| `api_execution_gpay_volume_7d` | numberDisplay | Last 7 days |
| `api_execution_gpay_volume_payments_by_token_weekly` | bar | Weekly payment volume in USD split by token. Stacked bars show token contribution to total proces... |
| `api_execution_gpay_wallet_balance_composition` | pie | Current balance distribution across all tokens in Gnosis Pay wallets. Tokens below 1% of total ar... |
| `text_gpay_glossary` | text | Definitions of key concepts, KPIs, and action types used across the Gnosis Pay dashboard |

### Gnosis App

| Metric | Chart Type | Description |
|--------|-----------|-------------|
| `api_execution_gnosis_app_active_users_incl_gpay_weekly` | bar | Activity by behavioral cohort. |
| `api_execution_gnosis_app_activity_by_action_weekly` | bar | Weekly actions by kind |
| `api_execution_gnosis_app_attribution_30d` | bar | Conversion credit by touchpoint |
| `api_execution_gnosis_app_churn_monthly_chart` | bar | Monthly — new / retained / returning / churned |
| `api_execution_gnosis_app_cumulative_users_weekly` | area | Weekly |
| `api_execution_gnosis_app_funnel_summary` | bar | Users reaching each funnel step |
| `api_execution_gnosis_app_gp_card_ga_link_daily` | area | Daily cumulative GA↔GP-card links by signal |
| `api_execution_gnosis_app_gpay_migration_card_spend_weekly_usd` | -- | -- |
| `api_execution_gnosis_app_gpay_migration_funded_cards` | -- | -- |
| `api_execution_gnosis_app_gpay_migration_migrated_cards` | -- | -- |
| `api_execution_gnosis_app_gpay_migration_money_daily_usd` | -- | -- |
| `api_execution_gnosis_app_gpay_migration_reactivated_any` | -- | -- |
| `api_execution_gnosis_app_gpay_migration_reactivated_spend` | -- | -- |
| `api_execution_gnosis_app_gpay_migration_reactivation_rate_funded` | -- | -- |
| `api_execution_gnosis_app_gpay_migration_reactivation_weekly` | -- | -- |
| `api_execution_gnosis_app_gpay_migration_refunded_cards` | -- | -- |
| `api_execution_gnosis_app_gpay_migration_refunds_daily_safes` | -- | -- |
| `api_execution_gnosis_app_gpay_migration_stranded_old_safes` | table | Migrated users who have not moved funds to their new card (outreach list) |
| `api_execution_gnosis_app_gpay_migration_usd_in_new_safes` | -- | -- |
| `api_execution_gnosis_app_gpay_migration_usd_stranded_old_safes` | -- | -- |
| `api_execution_gnosis_app_gpay_topups_by_token_weekly` | bar | Weekly — deposited token breakdown |
| `api_execution_gnosis_app_gpay_topups_cohort_monthly` | heatmap | First-topup cohort × subsequent activity |
| `api_execution_gnosis_app_gpay_topups_weekly_chart` | bar | Weekly count and USD volume |
| `api_execution_gnosis_app_gpay_wallets_cumulative_daily` | area | Daily cumulative by onboarding class |
| `api_execution_gnosis_app_gt_active_wallets_weekly` | -- | -- |
| `api_execution_gnosis_app_gt_app_generation` | -- | -- |
| `api_execution_gnosis_app_gt_engagement_tiers` | -- | -- |
| `api_execution_gnosis_app_gt_kpi_active_wallets_30d` | -- | -- |
| `api_execution_gnosis_app_gt_kpi_gp_card_users` | -- | -- |
| `api_execution_gnosis_app_gt_kpi_new_registrations` | -- | -- |
| `api_execution_gnosis_app_gt_kpi_power_users` | -- | -- |
| `api_execution_gnosis_app_gt_kpi_retention_1m` | -- | -- |
| `api_execution_gnosis_app_gt_referrals` | table | Earned rewards vs full invite graph |
| `api_execution_gnosis_app_gt_registrations_monthly` | -- | -- |
| `api_execution_gnosis_app_gt_retention_cohort_heatmap` | -- | -- |
| `api_execution_gnosis_app_gt_swaps` | bar | CoW swaps by app scope and status |
| `api_execution_gnosis_app_kpi_dau_latest` | numberDisplay | Latest day |
| `api_execution_gnosis_app_kpi_gp_wallets_latest` | numberDisplay | Legacy DelayModule-only on-chain count |
| `api_execution_gnosis_app_kpi_marketplace_buys_7d` | numberDisplay | Last 7 days |
| `api_execution_gnosis_app_kpi_marketplace_buys_total` | numberDisplay | All time |
| `api_execution_gnosis_app_kpi_marketplace_payers_7d` | numberDisplay | Last 7 days |
| `api_execution_gnosis_app_kpi_mau_latest` | numberDisplay | Latest month |
| `api_execution_gnosis_app_kpi_new_users_7d` | numberDisplay | Last 7 days |
| `api_execution_gnosis_app_kpi_repeat_purchase_rate_latest` | numberDisplay | Last 30 days |
| `api_execution_gnosis_app_kpi_swap_fees_7d` | numberDisplay | CoW protocol fee revenue (USD) from filled Gnosis App swaps in the last 7 full days, with WoW pct... |
| `api_execution_gnosis_app_kpi_swap_volume_7d` | numberDisplay | Last 7 days |
| `api_execution_gnosis_app_kpi_swaps_7d` | numberDisplay | Last 7 days |
| `api_execution_gnosis_app_kpi_token_offer_claimers_7d` | numberDisplay | Last 7 days |
| `api_execution_gnosis_app_kpi_token_offer_claims_7d` | numberDisplay | Last 7 days |
| `api_execution_gnosis_app_kpi_token_offer_volume_7d` | numberDisplay | Last 7 days |
| `api_execution_gnosis_app_kpi_topup_volume_7d` | numberDisplay | Last 7 days |
| `api_execution_gnosis_app_kpi_topups_7d` | numberDisplay | Last 7 days |
| `api_execution_gnosis_app_kpi_total_users` | numberDisplay | Lifetime |
| `api_execution_gnosis_app_kpi_weekly_active_users_latest` | numberDisplay | Latest week |
| `api_execution_gnosis_app_kpi_weekly_economically_active_users_latest` | numberDisplay | Latest week |
| `api_execution_gnosis_app_marketplace_buys_daily_chart` | bar | Daily buys — stacked by offer |
| `api_execution_gnosis_app_marketplace_cumulative_buys_chart` | area | Daily cumulative — per offer |
| `api_execution_gnosis_app_marketplace_cumulative_payers_chart` | area | Daily cumulative distinct payers per offer |
| `api_execution_gnosis_app_marketplace_offers_leaderboard` | table | Lifetime totals per curated offer |
| `api_execution_gnosis_app_purchase_freq_distribution_latest` | bar | Users by # of purchases in last 30 days |
| `api_execution_gnosis_app_swap_fees_weekly` | bar | Weekly CoW protocol fee revenue from filled Gnosis App swaps. fee_usd is pro-rated from fee_amoun... |
| `api_execution_gnosis_app_swaps_by_pair_weekly` | bar | Weekly filled swaps by token pair (top 10) |
| `api_execution_gnosis_app_swaps_by_solver_weekly` | bar | Weekly filled trades by solver |
| `api_execution_gnosis_app_swaps_weekly_chart` | bar | Weekly count and filled USD volume |
| `api_execution_gnosis_app_time_to_first_conversion_cohort_monthly` | line | Median days from onboard to first conversion, by cohort |
| `api_execution_gnosis_app_token_offer_claims_by_offer_weekly` | bar | Weekly — claims stacked by offer instance |
| `api_execution_gnosis_app_token_offer_claims_cohort_monthly` | heatmap | First-claim cohort × subsequent activity |
| `api_execution_gnosis_app_token_offer_claims_weekly` | bar | Claims, claimers and USD volume — daily or weekly |
| `api_execution_gnosis_app_token_offer_offers_leaderboard` | table | Lifetime totals per offer instance |
| `api_execution_gnosis_app_weekly_economically_active_users` | bar | WAU ∩ Circles reward earners |
| `growth_app_topup_by_campaign_weekly` | -- | -- |
| `growth_ga_card_funded_usd_weekly` | -- | -- |
| `growth_ga_card_spend_total_usd` | -- | -- |
| `growth_ga_card_spend_usd_weekly` | -- | -- |
| `growth_ga_linked_cards_total` | -- | -- |
| `growth_ga_wau_weau_weekly` | -- | -- |
| `growth_kpi_attributed_conversion_pct` | -- | -- |
| `growth_kpi_ga_wau_latest` | -- | -- |
| `growth_kpi_ga_weau_latest` | -- | -- |
| `growth_starts_referring_by_campaign_weekly` | -- | -- |

### Circles

| Metric | Chart Type | Description |
|--------|-----------|-------------|
| `api_execution_circles_v2_active_minters_daily` | area | Daily Active Minters (14d sustained mint) |
| `api_execution_circles_v2_active_trusts_cnt_latest` | numberDisplay | Live directed trust edges |
| `api_execution_circles_v2_active_trusts_daily` | area | Cumulative active trust relationships |
| `api_execution_circles_v2_avatar_balances_daily` | area | Daily CRC balance for the selected avatar, broken down by Circles token. Toggle between static an... |
| `api_execution_circles_v2_avatar_holdings_by_token` | table | Per-token CRC balance held by the selected Circles v2 avatar. Sorted by demurrage-adjusted balanc... |
| `api_execution_circles_v2_avatar_metadata` | table | Static registration facts for the selected Circles v2 avatar — type, who invited them, and when t... |
| `api_execution_circles_v2_avatar_metadata_history` | table | Full timeline of metadata updates for the selected Circles v2 avatar. Each row is one UpdateMetad... |
| `api_execution_circles_v2_avatar_mint_activity_daily` | bar | Daily personal-mint activity for the selected Circles v2 avatar. Each Circles human can mint up t... |
| `api_execution_circles_v2_avatar_personal_token_supply_latest` | numberDisplay | Total supply of the selected avatar\ |
| `api_execution_circles_v2_avatar_personal_token_wrapped_latest` | numberDisplay | Amount of the selected avatar\ |
| `api_execution_circles_v2_avatar_token_distribution` | pie | For the selected Circles v2 avatar\ |
| `api_execution_circles_v2_avatar_tokens_held_count` | numberDisplay | Number of distinct Circles v2 CRC tokens the selected avatar currently holds with a balance above... |
| `api_execution_circles_v2_avatar_total_balance_latest` | numberDisplay | Sum of all CRC tokens held by the avatar, with the Circles demurrage applied. |
| `api_execution_circles_v2_avatar_trust_network` | graph | Trust network for the selected Circles v2 avatar, laid out as concentric rings around the focal n... |
| `api_execution_circles_v2_avatar_trust_relations` | table | Each row is one counterparty. Direction is outgoing if the avatar trusts the counterparty, incomi... |
| `api_execution_circles_v2_avatar_trusts_daily` | line | Daily cumulative trusts given and received by the selected avatar. |
| `api_execution_circles_v2_avatar_trusts_given_latest` | numberDisplay | Outgoing trust relationships the avatar has extended to other Circles avatars. |
| `api_execution_circles_v2_avatar_trusts_received_latest` | numberDisplay | Incoming trust relationships the avatar has received from other Circles avatars. |
| `api_execution_circles_v2_avatars` | bar | Daily new avatar registrations by type |
| `api_execution_circles_v2_avatars_cumulative` | area | Cumulative avatars by type over time |
| `api_execution_circles_v2_backers_cumulative_daily` | area | Addresses trusted by the backers group over time |
| `api_execution_circles_v2_backing_depositors_current` | table | Addresses that pledged backing collateral |
| `api_execution_circles_v2_backing_events_daily` | bar | Daily backing-lifecycle events by stage |
| `api_execution_circles_v2_balance_cohorts_daily` | area | CRC holders split into balance tiers over time |
| `api_execution_circles_v2_crc20_price_daily` | bar | Daily CRC20 trading volume, swaps and USD price |
| `api_execution_circles_v2_gcrc_cashback_cumulative` | area | Total gCRC distributed and lifetime recipients |
| `api_execution_circles_v2_gcrc_cashback_recipients_ranking` | table | Largest lifetime gCRC cashback recipients |
| `api_execution_circles_v2_gcrc_cashback_weekly` | bar | gCRC distributed and recipients per week |
| `api_execution_circles_v2_group_explorer_avg_score_latest` | numberDisplay | Mean member mint score (score-based groups) |
| `api_execution_circles_v2_group_explorer_collateral_daily` | area | End-of-day member CRC collateral |
| `api_execution_circles_v2_group_explorer_collateral_latest` | numberDisplay | Member CRC locked as backing (latest) |
| `api_execution_circles_v2_group_explorer_holders_breakdown` | table | Largest holders of the group token |
| `api_execution_circles_v2_group_explorer_holders_count_latest` | numberDisplay | Distinct wallets holding the group token |
| `api_execution_circles_v2_group_explorer_members` | table | Accounts the group trusts |
| `api_execution_circles_v2_group_explorer_members_latest` | numberDisplay | Addresses on the group |
| `api_execution_circles_v2_group_explorer_metadata` | table | Registration, profile and on-chain handlers for the selected group |
| `api_execution_circles_v2_group_explorer_mints_7d` | numberDisplay | Group token minted in the last 7 days (CRC) |
| `api_execution_circles_v2_group_explorer_mints_redemptions_daily` | bar | Daily group mints vs collateral redemptions |
| `api_execution_circles_v2_group_explorer_score_distribution` | bar | Members bucketed by on-chain trust score |
| `api_execution_circles_v2_group_explorer_score_mints_daily` | line | Daily score-based minting activity |
| `api_execution_circles_v2_group_explorer_size_daily` | area | Members (outgoing trust) per day |
| `api_execution_circles_v2_group_explorer_supply_latest` | numberDisplay | Total circulating supply of the group token (CRC) |
| `api_execution_circles_v2_group_explorer_token_supply_daily` | area | Circulating group-token supply over time (CRC) |
| `api_execution_circles_v2_group_explorer_trust_network` | graph | The group at the centre, members on the surrounding rings |
| `api_execution_circles_v2_group_explorer_wrapped_pct_latest` | numberDisplay | Share of supply held in the ERC-20 wrapper |
| `api_execution_circles_v2_group_size_distribution` | bar | Groups bucketed by member count |
| `api_execution_circles_v2_group_token_supply_daily` | area | Native ERC-1155 vs wrapped ERC-20 supply across all groups |
| `api_execution_circles_v2_group_token_supply_top_latest` | table | Leaderboard of Circles v2 groups by personal-token supply |
| `api_execution_circles_v2_groups_cnt_latest` | numberDisplay | Registered group avatars (cumulative) |
| `api_execution_circles_v2_groups_overview_daily` | area | Total registered Circles v2 groups over time |
| `api_execution_circles_v2_holder_count_by_type_daily` | line | Daily distinct holder count per category |
| `api_execution_circles_v2_hub_events_addresses_daily` | bar | Daily distinct addresses per Hub event |
| `api_execution_circles_v2_hub_events_daily` | bar | Daily Circles v2 Hub event mix |
| `api_execution_circles_v2_humans_cnt_latest` | numberDisplay | Registered human avatars (cumulative) |
| `api_execution_circles_v2_invite_funnel_cohort_monthly` | bar | Invitee cohort cadence drop-off |
| `api_execution_circles_v2_inviter_farm_quota` | table | Inviters ranked by invites claimed from the farm |
| `api_execution_circles_v2_inviters_ranking` | table | Leaderboard of top inviters by humans invited |
| `api_execution_circles_v2_kpi_active_minters_latest` | numberDisplay | Consistent minters (14d, >=80% of max) |
| `api_execution_circles_v2_kpi_avg_members_per_group_latest` | numberDisplay | Mean group size (members per group) |
| `api_execution_circles_v2_kpi_avg_trusts_per_avatar_latest` | numberDisplay | Active trusts ÷ humans |
| `api_execution_circles_v2_kpi_depositors_in_backers_pct_latest` | numberDisplay | % of depositors that became trust-defined backers |
| `api_execution_circles_v2_kpi_gcrc_cashback_last_week` | numberDisplay | Most recent complete week (gCRC) |
| `api_execution_circles_v2_kpi_gcrc_cashback_last_week_recipients` | numberDisplay | Most recent complete week |
| `api_execution_circles_v2_kpi_gcrc_cashback_recipients` | numberDisplay | Lifetime distinct recipients |
| `api_execution_circles_v2_kpi_gcrc_cashback_total` | numberDisplay | Lifetime · complete weeks (gCRC) |
| `api_execution_circles_v2_kpi_group_token_supply_latest` | numberDisplay | Total CRC across all group personal tokens |
| `api_execution_circles_v2_kpi_group_wrapped_pct_latest` | numberDisplay | Share of group-token supply held as ERC-20 wrappers |
| `api_execution_circles_v2_kpi_mints_7d` | numberDisplay | Mint events in last 7 days |
| `api_execution_circles_v2_kpi_new_backers_7d` | numberDisplay | Backers newly trusted in the last 7 days |
| `api_execution_circles_v2_kpi_new_groups_7d` | numberDisplay | New groups registered in the last 7 days |
| `api_execution_circles_v2_kpi_total_backers_latest` | numberDisplay | Addresses trusted by the backers group |
| `api_execution_circles_v2_kpi_total_depositors_latest` | numberDisplay | Addresses that have pledged collateral |
| `api_execution_circles_v2_kpi_total_supply_latest` | numberDisplay | Network-wide CRC supply |
| `api_execution_circles_v2_minter_cohort_daily` | area | Avatars by 14-day mint coverage cohort |
| `api_execution_circles_v2_mints_daily` | area | Mints per day: events, minters, volume |
| `api_execution_circles_v2_orgs_cnt_latest` | numberDisplay | Registered organization avatars (cumulative) |
| `api_execution_circles_v2_p2p_velocity_daily` | area | Daily wallet-to-wallet CRC activity |
| `api_execution_circles_v2_pool_explorer_activity_daily` | bar | Trading and liquidity activity for the selected pool over time |
| `api_execution_circles_v2_pool_explorer_liquidity_events` | table | Individual add/remove liquidity events for the selected pool |
| `api_execution_circles_v2_pool_explorer_metadata` | table | Pair, protocol and headline liquidity/activity for the selected pool |
| `api_execution_circles_v2_pool_explorer_reserves` | table | Both token reserves of the selected pool |
| `api_execution_circles_v2_pool_explorer_reserves_daily` | area | USD value of each token reserve over time |
| `api_execution_circles_v2_pool_explorer_swaps` | table | Most recent swaps through the selected pool |
| `api_execution_circles_v2_pools_activity_daily` | bar | Volume, swaps or traders per pool over time |
| `api_execution_circles_v2_pools_latest` | table | The main Circles DEX pools at a glance |
| `api_execution_circles_v2_pools_reserves_latest` | table | Both token reserves of each pool |
| `api_execution_circles_v2_pools_traders_7d` | numberDisplay | Trailing 7-day distinct traders (per-pool, summed) |
| `api_execution_circles_v2_pools_trades_7d` | numberDisplay | Trailing 7-day swap count, all tracked pools |
| `api_execution_circles_v2_pools_tvl_daily` | area | USD value locked per pool over time |
| `api_execution_circles_v2_pools_tvl_total` | numberDisplay | USD value locked across the tracked Circles DEX pools |
| `api_execution_circles_v2_pools_volume_7d` | numberDisplay | Trailing 7-day swap volume, all tracked pools |
| `api_execution_circles_v2_supply_by_holder_type_daily` | area | Daily CRC supply broken down by holder category |
| `api_execution_circles_v2_token_count_daily` | area | Daily count of distinct CRC tokens with non-zero supply |
| `api_execution_circles_v2_total_supply_daily` | area | Network-wide CRC supply (nominal and demurraged) |
| `api_execution_circles_v2_transfers_daily` | bar | Daily transfers by category |
| `api_execution_circles_v2_trust_flow_daily` | bar | Daily new vs revoked trust relationships |
| `api_execution_circles_v2_trusts_daily` | area | Trust event activity |
| `api_execution_circles_v2_trusts_distribution` | bar | Avatars grouped by trust degree, given vs received |
| `api_execution_circles_v2_weau_weekly` | bar | Weekly avatars earning CRC rewards (ecosystem-wide) |
| `api_execution_circles_v2_wrapper_share_daily` | area | ERC-20 wrapped vs unwrapped CRC supply |

### Trades

| Metric | Chart Type | Description |
|--------|-----------|-------------|
| `api_execution_cow_batch_routing_ts` | bar | Daily percentage of CoW Protocol settlement batches by routing type.  |
| `api_execution_cow_fees_ts` | area | Daily CoW Protocol revenue on Gnosis Chain — surplus-based fees collected since Sep 2024. Pre-Sep... |
| `api_execution_cow_kpi_active_solvers` | numberDisplay | Number of distinct solvers that settled at least one batch in the last 7 complete days. Reflects ... |
| `api_execution_cow_kpi_fees_7d` | numberDisplay | Total CoW Protocol fees (USD) collected on Gnosis Chain in the last 7 complete days. Reflects the... |
| `api_execution_cow_kpi_solver_value_7d` | numberDisplay | Total gross value generated by CoW solvers on Gnosis Chain in the last 7 complete days — the full... |
| `api_execution_cow_kpi_traders_7d` | numberDisplay | Distinct trader addresses (order owners) that executed at least one CoW Protocol trade in the las... |
| `api_execution_cow_kpi_trades_7d` | numberDisplay | Number of CoW Protocol trades on Gnosis Chain in the last 7 complete days. Each Trade event in th... |
| `api_execution_cow_kpi_volume_7d` | numberDisplay | Total CoW Protocol trading volume (USD) on Gnosis Chain in the last 7 complete days. |
| `api_execution_cow_solver_value_ts` | area | Daily gross value generated by CoW solvers on Gnosis Chain — the full amount found beyond the ref... |
| `api_execution_cow_solvers_volume_ts` | area | Daily trading volume attributed to each solver, based on which solver settled the batch containin... |
| `api_execution_cow_top_pairs_weekly` | bar | Weekly USD trading volume for the top 8 directional token pairs (sold → bought) by lifetime volum... |
| `api_execution_cow_trades_ts` | area | Daily number of individual trades (Trade events) settled through CoW Protocol on Gnosis Chain. |
| `api_execution_cow_volume_ts` | area | Daily total trading volume (USD) routed through CoW Protocol on Gnosis Chain. Priced using the be... |
| `api_execution_live_trades` | table | DEX swaps from the last 30 minutes of cached data across Uniswap V3, Swapr V3, Balancer V2 and Ba... |
| `api_execution_live_trades_freshness` | numberDisplay | Seconds behind Gnosis Chain — difference between the newest ingested log in execution_live.logs a... |
| `api_execution_live_trades_hourly_48h` | bar | Hourly USD volume across Uniswap V3, Swapr V3, Balancer V2 and Balancer V3 over the last 48 hours... |
| `api_execution_live_trades_stats_aggregator` | numberDisplay | Share of feed trades routed through an aggregator — where tx.to_address matches a labeled aggrega... |
| `api_execution_live_trades_stats_count` | numberDisplay | Number of DEX transactions in the feed window (last 30 minutes of cached data, after the 60s reor... |
| `api_execution_live_trades_stats_multihop` | numberDisplay | Share of trades in the feed window that route through more than one pool — i.e. the transaction c... |
| `api_execution_live_trades_stats_traders` | numberDisplay | Distinct tx.from_address values across the feed window. This is the EOA that initiated the swap, ... |
| `api_execution_live_trades_stats_volume` | numberDisplay | Sum of per-trade USD notionals in the feed window. Uses a conservative pricing: for trades where ... |
| `api_execution_trades_stats_aggregator_share_ts` | area | Daily share of trades by router/aggregator. A trade is assigned to its transaction-level `tx_to` ... |
| `api_execution_trades_stats_hop_distribution` | bar | Share of DEX trades by hop count — 1 hop (direct pool swaps), 2/3 hops (short routes), 4+ hops (c... |
| `api_execution_trades_stats_lifetime_traders` | numberDisplay | All-time distinct count of trader addresses (`tx_from`) across indexed DEX trades on Gnosis Chain... |
| `api_execution_trades_stats_lifetime_trades` | numberDisplay | All-time distinct transaction count of indexed DEX trades on Gnosis Chain. Multi-hop router swaps... |
| `api_execution_trades_stats_lifetime_volume` | numberDisplay | All-time sum of per-swap USD notional across indexed DEX trades on Gnosis Chain. Multi-hop routes... |
| `api_execution_trades_stats_net_flow` | bar | Top 10 tokens by absolute net USD flow. Positive = net accumulation (more USD bought into the tok... |
| `api_execution_trades_stats_size_distribution` | bar | Share of DEX trades by USD notional size bucket, computed as the max per-hop amount_usd within a ... |
| `api_execution_trades_stats_top_tokens_weekly` | bar | Weekly USD trading volume for the top 8 tokens by lifetime volume (sold + bought side combined), ... |
| `api_execution_trades_stats_traders_weekly` | area | Number of distinct wallet addresses that executed at least one DEX trade on Gnosis Chain in a giv... |
| `api_execution_trades_stats_trades_ts` | area | Daily number of distinct DEX trades on Gnosis Chain, stacked by protocol. Each transaction is cou... |
| `api_execution_trades_stats_volume_ts` | area | Daily DEX trading volume on Gnosis Chain, stacked by protocol (Uniswap V3, Balancer V2, Balancer ... |

### Tokens

| Metric | Chart Type | Description |
|--------|-----------|-------------|
| `api_execution_tokens_active_senders_daily` | bar | Daily unique sending addresses per token. Token filter isolates sender activity for a specific as... |
| `api_execution_tokens_balance_cohorts_holders_daily` | bar | Daily holder counts by token balance cohort, with token and unit filters. Cohort buckets can be n... |
| `api_execution_tokens_balance_cohorts_value_daily` | bar | Daily aggregate balances by token cohort, with token and unit filters. Unit toggle switches betwe... |
| `api_execution_tokens_holders_total` | numberDisplay | -- |
| `api_execution_tokens_supply_by_class_daily` | bar | Daily token market cap (USD) by token, filtered by token class. Stacked view shows class composit... |
| `api_execution_tokens_supply_by_sector_latest` | pie | Latest-day token supply in USD grouped by sector for the selected token class. Sector percentages... |
| `api_execution_tokens_supply_distribution_latest` | pie | Latest token supply distribution in USD for the selected token class. Pie shares are computed wit... |
| `api_execution_tokens_supply_total` | numberDisplay | -- |
| `api_execution_tokens_top_holders_latest` | table | Top holders ranked by USD balance for the selected token.  |
| `api_execution_tokens_volume_daily` | bar | Daily transfer volume per token with token filter and unit toggle. Compare native token flow vers... |

### OnChain Activity

| Metric | Chart Type | Description |
|--------|-----------|-------------|
| `api_crawlers_data_distinct_projects_total` | numberDisplay | All-time |
| `api_crawlers_data_distinct_sectors_total` | numberDisplay | All-time |
| `api_execution_transactions_7d` | numberDisplay | Last 7 days |
| `api_execution_transactions_active_accounts_7d` | numberDisplay | Last 7 days |
| `api_execution_transactions_active_accounts_by_project_monthly_top5` | bar | Monthly unique initiator accounts for the top 5 projects. Focuses on dominant projects rather tha... |
| `api_execution_transactions_active_accounts_by_project_ranges_top20` | pie | Select a window (All, 7D, 30D, 90D) to recompute the top 20 projects by unique initiator accounts... |
| `api_execution_transactions_active_accounts_by_sector_hourly` | bar | Hourly unique initiator accounts by sector for the recent 48-hour window. Useful for short-term a... |
| `api_execution_transactions_active_accounts_by_sector_weekly` | bar | Weekly unique initiator accounts by sector. Compare sector participation trends at a smoother cad... |
| `api_execution_transactions_active_accounts_total` | numberDisplay | All-time |
| `api_execution_transactions_by_project_monthly_top5` | bar | Monthly transaction counts for the top 5 projects. Useful for tracking leading project throughput... |
| `api_execution_transactions_by_project_ranges_top20` | pie | Select a window (All, 7D, 30D, 90D) to recompute the top 20 projects by transaction count. Projec... |
| `api_execution_transactions_by_sector_hourly` | bar | Hourly transaction counts by sector for the recent 48-hour window. Captures near-real-time sector... |
| `api_execution_transactions_by_sector_weekly` | bar | Weekly transaction counts by sector. Smooths daily noise to highlight medium-term activity trends. |
| `api_execution_transactions_fees_native_7d` | numberDisplay | Last 7 days |
| `api_execution_transactions_fees_native_by_project_monthly_top5` | bar | Monthly transaction fees (xDAI) for the top 5 projects. Shows which projects drive fee generation. |
| `api_execution_transactions_fees_native_by_project_ranges_top20` | pie | Select a window (All, 7D, 30D, 90D) to recompute the top 20 projects by total fees in xDAI. Proje... |
| `api_execution_transactions_fees_native_by_sector_hourly` | bar | Hourly transaction fees in xDAI by sector for the recent 48-hour window. Good for spotting short-... |
| `api_execution_transactions_fees_native_by_sector_weekly` | bar | Weekly transaction fees in xDAI by sector. Highlights sustained fee contribution by sector. |
| `api_execution_transactions_fees_native_total` | numberDisplay | All-time |
| `api_execution_transactions_gas_used_weekly` | area | Weekly execution-layer gas used by transaction type. Compare structural shifts in demand across t... |
| `api_execution_transactions_total` | numberDisplay | All-time |
| `text_onchain_projects_sectors_glossary` | text | Representative project examples by sector |
| `text_onchain_projects_sectors_overview_info` | text | Definitions used in metrics |

### Consensus

| Metric | Chart Type | Description |
|--------|-----------|-------------|
| `api_consensus_attestations_avg_inclusion_delay_daily` | line | Average number of slots between attestation slot and inclusion slot, weighted by attestation coun... |
| `api_consensus_attestations_daily` | area | Daily attestation counts by inclusion-delay bucket. Lower delay buckets indicate faster inclusion... |
| `api_consensus_attestations_p50_inclusion_delay_daily` | line | Weighted median of attestation inclusion delay. Typically 1 on healthy network days — values > 1 ... |
| `api_consensus_attestations_pct_distance_1_daily` | line | Fraction of attestations included in the very next slot (inclusion_delay = 1). This is the upper ... |
| `api_consensus_blob_commitments_daily` | bar | Daily number of blob commitments included by execution payloads. This tracks EIP-4844 data-availa... |
| `api_consensus_blocks_daily` | area | Daily produced versus missed blocks from consensus data. Divergence between series highlights val... |
| `api_consensus_consolidations_daily` | bar | Count of consolidation events per day, split into self (credential switch 0x01→0x02), source (val... |
| `api_consensus_credentials_latest` | pie | Current validator withdrawal credential split (0x00, 0x01, 0x02). Shares reflect migration from l... |
| `api_consensus_deposits_withdrawals_cumulative_daily` | line | Cumulative sum (from genesis) of daily deposit and withdrawal volumes. Deposits include both the ... |
| `api_consensus_deposits_withdrawls_cnt_daily` | bar | Daily count of validator deposits and withdrawals. Compare both series to monitor validator-set e... |
| `api_consensus_deposits_withdrawls_volume_daily` | bar | Daily deposit and withdrawal volume in GNO. Volume captures stake movement magnitude, not just ev... |
| `api_consensus_entry_queue_daily` | bar | Daily average estimated time (days) to enter the validator set. Rising values indicate queue pres... |
| `api_consensus_graffiti` | wordcloud | Top validator graffiti messages weighted by frequency. Use the label filter to isolate message so... |
| `api_consensus_graffiti_label_daily` | area | Daily graffiti counts by keyword/category label. Trends help identify operator branding and campa... |
| `api_consensus_info_active_ongoing_latest` | numberDisplay | -- |
| `api_consensus_info_active_stake_latest` | numberDisplay | -- |
| `api_consensus_info_apy_latest` | numberDisplay | -- |
| `api_consensus_info_deposits_cnt_latest` | numberDisplay | -- |
| `api_consensus_info_staked_latest` | numberDisplay | -- |
| `api_consensus_info_withdrawls_cnt_latest` | numberDisplay | -- |
| `api_consensus_staked_daily` | area | Daily total staked GNO on the consensus layer. Reflects aggregate validator effective stake over ... |
| `api_consensus_validators_active_daily` | area | Daily count of active validators participating in consensus. Useful for tracking validator set gr... |
| `api_consensus_validators_apy_dist` | boxplot | Boxplots summarize daily validator APY dispersion over the last 30 days. Whiskers use the 10th an... |
| `api_consensus_validators_apy_dist_daily` | quantileBands | Daily APY quantiles for validator rewards. Shaded bands show dispersion while the median tracks c... |
| `api_consensus_validators_apy_mean_daily` | quantileBands | Shaded bands are T-Digest quantiles of per-validator APY across the active validator set each day... |
| `api_consensus_validators_balances_dist_daily` | quantileBands | Daily validator effective-balance quantiles. Bands reveal concentration and spread across the val... |
| `api_consensus_validators_explorer_active_count` | numberDisplay | Validators currently active under this credential. Count of validators with status in (active_ong... |
| `api_consensus_validators_explorer_apy_daily` | quantileBands | For multi-validator credentials, shaded bands are T-Digest quantiles of per-validator APY on each... |
| `api_consensus_validators_explorer_apy_latest` | numberDisplay | Per-credential balance-weighted APY = SUM(30d consensus income) / AVG(30d effective balance) × 36... |
| `api_consensus_validators_explorer_balance_daily` | area | Sum of balance_gno across every validator sharing the selected withdrawal_credentials, day by day... |
| `api_consensus_validators_explorer_balance_dist` | bar | Bucketed histogram of effective balance across every validator sharing the selected withdrawal cr... |
| `api_consensus_validators_explorer_balance_latest` | numberDisplay | -- |
| `api_consensus_validators_explorer_count_latest` | numberDisplay | -- |
| `api_consensus_validators_explorer_deposits_withdrawals_daily` | bar | Pivoted view of the four flow columns from api_consensus_validators_explorer_daily. Deposits and ... |
| `api_consensus_validators_explorer_exited_count` | numberDisplay | Validators that have exited under this credential. Count of validators with status starting exite... |
| `api_consensus_validators_explorer_income_30d` | numberDisplay | -- |
| `api_consensus_validators_explorer_income_daily` | bar | Sum of consensus_income_amount_gno across every validator sharing the selected withdrawal_credent... |
| `api_consensus_validators_explorer_members_table` | table | One row per validator sharing the selected withdrawal_credentials. Default sort is balance (desc)... |
| `api_consensus_validators_explorer_proposed_blocks_lifetime` | numberDisplay | -- |
| `api_consensus_validators_explorer_proposer_rewards_daily` | bar | Sum of proposer_reward_total_gno for the selected withdrawal_credentials, by day. Bars only appea... |
| `api_consensus_validators_explorer_slashed_count` | numberDisplay | Validators slashed under this credential. Count of validators with slashed=true on the latest bea... |
| `api_consensus_validators_income_total_daily` | area | Sum of consensus_income_amount_gno per day across the full validator set (including exited and ze... |
| `api_consensus_validators_status_daily` | bar | Daily validator counts by lifecycle status (active, pending, exited, and related states). Status ... |
| `api_consensus_withdrawal_credentials_freq_daily` | area | Daily count of distinct withdrawal credentials by type. Tracks adoption of credential formats acr... |
| `api_consensus_zero_blob_commitments_daily` | area | Daily split of blocks with versus without blob commitments. Use it to monitor blob adoption relat... |
| `text_consensus_validators_status` | text | A reference table of validator lifecycle states in the Beacon Chain |

### Network

| Metric | Chart Type | Description |
|--------|-----------|-------------|
| `api_p2p_clients_latest_discv4` | numberDisplay | -- |
| `api_p2p_clients_latest_discv5` | numberDisplay | -- |
| `api_p2p_crawls_latest_discv4` | numberDisplay | -- |
| `api_p2p_crawls_latest_discv5` | numberDisplay | -- |
| `api_p2p_discv4_clients_daily` | bar | Distribution of peers dialable in DiscV4 protocol |
| `api_p2p_discv4_clients_latest` | pie | Last day clients distribution |
| `api_p2p_discv5_clients_daily` | bar | Distribution of peers dialable in DiscV5 protocol |
| `api_p2p_discv5_clients_latest` | pie | Last day clients distribution |
| `api_p2p_discv5_current_fork_daily` | bar | Distribution for forks across the network (Consensus Layer) |
| `api_p2p_discv5_next_fork_daily` | bar | Distribution for Broadcasted next forks (Consensus Layer) |
| `api_p2p_topology_latest` | map | Geographic visualization of peer-to-peer network connections |
| `api_p2p_visits_latest_discv4` | numberDisplay | -- |
| `api_p2p_visits_latest_discv5` | numberDisplay | -- |
| `api_probelab_clients_cloud_daily` | bar | Clients per cloud provider |
| `api_probelab_clients_country_daily` | bar | Client per country |
| `api_probelab_clients_daily` | bar | Daily consensus clients |
| `api_probelab_clients_quic_daily` | bar | 7DMA distribution |
| `api_probelab_clients_version_daily` | bar | Versions per client distribution |
| `network_client_distribution` | network | Network visualization of client implementations and their connections |
| `network_validator_connections` | network | Network connections and relationships between validators |
| `text_gnosis_chain_forks_history` | text | A timeline of major milestones, forks, and protocol upgrades on Gnosis Chain |
| `text_gnosis_chain_history` | text | Definitions, Naming Conventions, and Fork Version History |
| `text_network_clients` | text | -- |
| `text_network_glossary` | text | Definitions of key concepts, protocols, and terminology used across the Network dashboard |
| `text_network_methodology` | text | How we measure and analyze network health metrics |
| `text_network_overview` | text | All crawl data is filtered for Gnosis Network |
| `text_network_protocols_overview` | text | Understanding discv4 and discv5 protocols |
| `text_probelab` | text | Curated Analytics & Expert Insights on P2P Matters |

### Bridges

| Metric | Chart Type | Description |
|--------|-----------|-------------|
| `api_bridges_cum_netflow_weekly_by_bridge` | area | Weekly cumulative netflow in USD by bridge (inflow minus outflow). Positive values indicate net i... |
| `api_bridges_kpi_distinct_bridges_all_time` | numberDisplay | All time |
| `api_bridges_kpi_distinct_chains_all_time` | numberDisplay | All time |
| `api_bridges_kpi_netflow_7d` | numberDisplay | Last 7 days |
| `api_bridges_kpi_total_netflow_all_time` | numberDisplay | All time |
| `api_bridges_kpi_total_volume_all_time` | numberDisplay | All time |
| `api_bridges_kpi_volume_7d` | numberDisplay | Last 7 days |
| `api_bridges_sankey_gnosis_in_by_token_7d` | sankey | Token-level inbound bridge flows into Gnosis over the last 7 days. Link width represents USD volu... |
| `api_bridges_sankey_gnosis_in_ranges` | sankey | Inbound bridge flows into Gnosis split by selected time window. Use the range filter to compare r... |
| `api_bridges_sankey_gnosis_out_by_token_7d` | sankey | Token-level outbound bridge flows from Gnosis over the last 7 days. Link width represents USD vol... |
| `api_bridges_sankey_gnosis_out_ranges` | sankey | Outbound bridge flows from Gnosis split by selected time window. Use the range filter to compare ... |
| `api_bridges_token_netflow_daily_by_bridge` | bar | Daily net token flow in USD by bridge and token. Negative values mean net outflow from Gnosis for... |

### ESG

| Metric | Chart Type | Description |
|--------|-----------|-------------|
| `api_esg_carbon_emissions_annualised_latest` | numberDisplay | Estimated annualised CO2e emissions for Gnosis Chain, reported in tCO2e. |
| `api_esg_carbon_emissions_daily` | quantileBands | Daily network CO2e estimate with uncertainty bands from model simulations. The central line is th... |
| `api_esg_cif_network_vs_countries_daily` | line | Compares Gnosis network carbon intensity (gCO2e/kWh) against selected country benchmarks. Values ... |
| `api_esg_energy_consumption_annualised_latest` | numberDisplay | Estimated annualised energy consumption for Gnosis Chain, reported in MWh. |
| `api_esg_estimated_nodes_daily` | quantileBands | Estimated network node count per day with uncertainty bands. Estimation uses crawler-observed pee... |
| `api_esg_info_annual_daily` | quantileBands | Annualized emissions and energy projections derived from daily estimates. Bands communicate uncer... |
| `api_esg_info_category_daily` | bar | Daily emissions and energy estimates by node-category segment. Category filter shows which node g... |
| `esg_methodology` | text | Environmental, Social, and Governance methodology overview |
| `text_esg_methodology` | text | How we calculate and analyze the Gnosis network carbon emissions |

### Yields

| Metric | Chart Type | Description |
|--------|-----------|-------------|
| `api_execution_yields_lending_activity_counts_weekly` | bar | Weekly unique lender and borrower counts across Gnosis lending markets (Aave V3 and SparkLend) by... |
| `api_execution_yields_lending_activity_volumes_weekly` | bar | Weekly deposit and borrow volumes across Gnosis lending markets (Aave V3 and SparkLend) by token.... |
| `api_execution_yields_lending_balance_cohorts_holders_daily` | bar | Daily unique-lender counts by balance cohort across Gnosis lending markets  |
| `api_execution_yields_lending_balance_cohorts_value_daily` | bar | Daily aggregate balances by lender cohort across Gnosis lending markets  |
| `api_execution_yields_lending_borrowers_count_7d` | numberDisplay | Unique wallets that borrowed at least one asset across Gnosis lending markets (Aave V3 and SparkL... |
| `api_execution_yields_lending_daily` | line | Daily supply APY and variable borrow APY for each lending reserve on  |
| `api_execution_yields_lending_lenders_count_7d` | numberDisplay | Unique wallets currently holding a supply balance worth more than $0.01 (sub-cent dust excluded) ... |
| `api_execution_yields_lending_top_lenders_latest` | table | Top lending suppliers ranked by USD balance for the selected token and protocol.  |
| `api_execution_yields_lending_tvl_by_token_latest` | pie | Latest TVL distribution across Gnosis lending reserves (Aave V3 and SparkLend combined). Each sli... |
| `api_execution_yields_opportunities_latest` | table | Current yield opportunities across LP pools and lending markets on Gnosis Chain. Rows are ranked ... |
| `api_execution_yields_overview_lending_best_apy` | numberDisplay | Highest supply APY currently available across Gnosis lending markets (Aave V3 and SparkLend). The... |
| `api_execution_yields_overview_lending_lenders` | numberDisplay | Unique wallets currently holding a supply balance worth more than $0.01 (sub-cent dust excluded) ... |
| `api_execution_yields_overview_lending_tvl` | numberDisplay | Total value locked across all lending reserves on Gnosis Chain (Aave V3 and SparkLend). Change co... |
| `api_execution_yields_overview_lp_best_apr` | numberDisplay | Highest 7-day trailing fee APR among tracked Uniswap V3 and Swapr V3 pools. Annualised from recen... |
| `api_execution_yields_overview_lp_tvl` | numberDisplay | Total value locked across all tracked Uniswap V3 and Swapr V3 liquidity pools. Change compares to... |
| `api_execution_yields_overview_sdai_apy` | numberDisplay | Current annual percentage yield on the Savings xDAI vault on Gnosis Chain.  |
| `api_execution_yields_overview_sdai_supply` | numberDisplay | Total value locked in the Savings xDAI vault (0xaf20…3701). Not all bridged  |
| `api_execution_yields_pools_fees_7d` | numberDisplay | Total fees accrued across all tracked pools for the selected token. Change compares to the prior ... |
| `api_execution_yields_pools_fees_usd_daily` | bar | Daily gross fee revenue in USD broken down by pool for the selected token. Derived from Swap and ... |
| `api_execution_yields_pools_lp_activity_daily` | bar | Daily by pool |
| `api_execution_yields_pools_lps_count_7d` | numberDisplay | Unique wallet addresses that provided liquidity (Mint events) on Uniswap V3 or Swapr V3 pools in ... |
| `api_execution_yields_pools_net_apr_daily` | line | Annualised fee revenue earned by LPs, computed from a 7-day trailing window of fees divided by av... |
| `api_execution_yields_pools_swap_count_daily` | bar | Daily number of swap transactions per pool for the selected token. Counts individual Swap events ... |
| `api_execution_yields_pools_tvl_by_pool_latest` | pie | Latest TVL distribution across pools for the selected token. Pie shares show within-token liquidi... |
| `api_execution_yields_pools_tvl_latest` | numberDisplay | Total value locked across all tracked pools for the selected token. Change compares to 7 days ago. |
| `api_execution_yields_pools_tvl_token_daily` | area | Stacked area showing each token\ |
| `api_execution_yields_pools_volume_7d` | numberDisplay | Total gross trading volume across all tracked pools for the selected token. Change compares to th... |
| `api_execution_yields_pools_volume_daily` | bar | Daily gross trading volume in USD broken down by pool for the selected token. Derived from Swap e... |
| `api_execution_yields_user_activity` | table | Unified activity feed showing all LP actions (Add/Remove Liquidity, Collect Fees) and lending act... |
| `api_execution_yields_user_fee_collections_daily` | bar | Daily LP fee income from Collect events across V3 pools (Uniswap/Swapr) for the selected wallet. ... |
| `api_execution_yields_user_kpi_active_lending_positions` | numberDisplay | Number of (protocol, reserve) combinations where the selected wallet currently has a supply balan... |
| `api_execution_yields_user_kpi_active_lp_positions` | numberDisplay | Count of LP positions with remaining liquidity — shown broken down by in-range vs out-of-range fo... |
| `api_execution_yields_user_kpi_lending_balance` | numberDisplay | Current total supply balance across all Gnosis lending markets (Aave V3 and SparkLend) for the se... |
| `api_execution_yields_user_kpi_total_lp_fees` | numberDisplay | Total LP swap fees for the selected wallet. Uniswap/Swapr V3: fees from Collect events. Balancer ... |
| `api_execution_yields_user_lending_balances_daily` | bar | Daily supply balance history for the selected wallet across Gnosis lending markets (Aave V3 and S... |
| `api_execution_yields_user_lending_positions` | table | Current supply positions (value above $0.01) across Gnosis lending markets (Aave V3 and SparkLend)  |
| `api_execution_yields_user_lp_positions` | table | LP positions across Uniswap V3, Swapr V3, Balancer V2, and Balancer V3. Shows capital invested, w... |
| `historical_yield_sdai` | line | Historical APY for the Savings xDAI vault (0xaf20…3701) on Gnosis Chain.  |

### Gnosis Revenue

| Metric | Chart Type | Description |
|--------|-----------|-------------|
| `api_revenue_active_users_totals_monthly` | bar | For each user, calendar-month fees are summed across **all** streams (holdings + sDAI + GPay) **b... |
| `api_revenue_active_users_totals_weekly` | bar | For each user, trailing-52-week fees are summed across **all** streams (holdings + sDAI + GPay) *... |
| `api_revenue_gnosis_app_cohorts_monthly` | bar | When a user transacts via Gnosis App (Cometh ERC-4337), a CRC ERC-1155 fee is paid to the Metri f... |
| `api_revenue_gnosis_app_cohorts_weekly` | bar | When a user transacts via Gnosis App (Cometh ERC-4337), a CRC ERC-1155 fee is paid to the Metri f... |
| `api_revenue_gpay_eure_cohorts_monthly` | bar | EURe transfers to the GP settlement address × **20 bps**, priced to USD. Fees summed per calendar... |
| `api_revenue_gpay_eure_cohorts_weekly` | bar | Each ERC-20 EURe transfer to the Gnosis Pay settlement address (`0x4822…172EE`) is a payment. Fee... |
| `api_revenue_gpay_gbpe_cohorts_monthly` | bar | GBPe transfers to the GP settlement address × **20 bps**, priced to USD. Fees summed per calendar... |
| `api_revenue_gpay_gbpe_cohorts_weekly` | bar | GBPe transfers to the GP settlement address (`0x4822…172EE`) × **20 bps (0.20%)**, priced to USD.... |
| `api_revenue_gpay_usdce_cohorts_monthly` | bar | USDC.e transfers to the GP settlement address × **100 bps**, priced to USD. Fees summed per calen... |
| `api_revenue_gpay_usdce_cohorts_weekly` | bar | USDC.e transfers to the GP settlement address (`0x4822…172EE`) × **100 bps (1.00%)**, priced to U... |
| `api_revenue_holdings_brla_cohorts_monthly` | bar | Per user per day we compute **balance_usd × 5.61349e-5** (2.07% APY). Fees summed over one calend... |
| `api_revenue_holdings_brla_cohorts_weekly` | bar | Per user per day we compute **balance_usd × 5.61349e-5** (2.07% APY expressed per-day). Daily fee... |
| `api_revenue_holdings_eure_cohorts_monthly` | bar | Per user per day we compute **balance_usd × 9.6e-6** (0.351% APY expressed per-day). Fees are sum... |
| `api_revenue_holdings_eure_cohorts_weekly` | bar | Per user per day we compute **balance_usd × 9.6e-6** (0.351% APY expressed per-day). Daily fees a... |
| `api_revenue_holdings_usdce_cohorts_monthly` | bar | Per user per day we compute **balance_usd × 9.6e-6** (0.351% APY). Fees summed over one calendar ... |
| `api_revenue_holdings_usdce_cohorts_weekly` | bar | Per user per day we compute **balance_usd × 9.6e-6** (0.351% APY expressed per-day). Daily fees s... |
| `api_revenue_holdings_zchf_cohorts_monthly` | bar | Per user per day we compute **balance_usd × 1.36646e-5** (0.5% APY). Fees summed over one calenda... |
| `api_revenue_holdings_zchf_cohorts_weekly` | bar | Per user per day we compute **balance_usd × 1.36646e-5** (0.5% APY expressed per-day). Daily fees... |
| `api_revenue_sdai_cohorts_monthly` | bar | Per day we compute `balance_usd × sdai_daily_rate × 10%`. The daily rate comes from on-chain sDAI... |
| `api_revenue_sdai_cohorts_weekly` | bar | Per day we compute `balance_usd × sdai_daily_rate × 10%`. The daily rate comes from on-chain sDAI... |
| `text_revenue_methodology` | text | Assumptions, data flow, and how active users are computed across sectors. |

### DAO Treasury

| Metric | Chart Type | Description |
|--------|-----------|-------------|
| `api_dao_treasury_allocation_latest` | pie | Current GnosisDAO holdings breakdown on Gnosis Chain by token. Shows each asset individually — GN... |
| `api_dao_treasury_holdings_by_class_ts` | area | Daily total GnosisDAO holdings on Gnosis Chain (wallet + lending), stacked by asset class: GNO, S... |
| `api_dao_treasury_holdings_detail_latest` | table | Detailed breakdown of all GnosisDAO positions on Gnosis Chain — token balances and lending supply... |
| `api_dao_treasury_kpi_gno_held` | numberDisplay | Total GNO and GNO derivatives (sGNO, spGNO, aGnoGNO) held by GnosisDAO wallets on Gnosis Chain, e... |
| `api_dao_treasury_kpi_lending_total` | numberDisplay | Total USD value of GnosisDAO lending supply positions on Gnosis Chain across Aave V3 and SparkLen... |
| `api_dao_treasury_kpi_non_gno_holdings` | numberDisplay | Total USD value of GnosisDAO non-GNO assets on Gnosis Chain. Excludes GNO and GNO derivatives (sG... |
| `api_dao_treasury_kpi_total_holdings` | numberDisplay | Total USD value of GnosisDAO holdings on Gnosis Chain, including wallet token balances and lendin... |

<!-- END AUTO-GENERATED: dashboard-sectors -->

## Sector Configuration

Each sector is defined in `public/dashboard.yml`:

```yaml
Overview:
  name: Overview
  order: 1
  icon: "chart-icon"
  iconClass: "chart-line"
  source: /dashboards/overview.yml

GnosisPay:
  name: Gnosis Pay
  order: 10
  icon: "card-icon"
  iconClass: credit-card
  palette: gnosis-pay
  source: /dashboards/gnosis-pay.yml
```

The `source` field points to a sector-specific YAML file in `public/dashboards/` that defines the metric grid layout. See [Configuration](configuration.md) for details on the layout format and how to add new sectors.
