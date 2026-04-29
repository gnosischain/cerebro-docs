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
### Overview

| Metric | Chart Type | Description |
|--------|-----------|-------------|
| `overview_active_accounts` | number | -- |
| `overview_esg` | number | -- |
| `overview_gno_supply_daily` | area | Daily GNO supply components by source category. Stacked view shows how each source contributes to... |
| `overview_payments` | number | -- |
| `overview_stablecoins_supply_latest` | pie | Latest stablecoin supply split in USD (excluding sDAI and WxDAI). Pie shares are relative to the ... |
| `overview_stablecoins_supply_total` | number | -- |
| `overview_stake_api` | number | -- |
| `overview_stake_gno` | number | -- |
| `overview_transactions` | number | -- |
| `overview_validators` | number | -- |

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
| `api_execution_gpay_kpi_arpu_latest` | numberDisplay | Latest month (USD) |
| `api_execution_gpay_kpi_flows_monthly` | line | Payments, deposits, withdrawals, net flow |
| `api_execution_gpay_kpi_mau_latest` | numberDisplay | Distinct wallets with any Gnosis Pay activity (payments, deposits, withdrawals, cashback) in the ... |
| `api_execution_gpay_kpi_payment_volume_latest` | numberDisplay | Latest month (USD) |
| `api_execution_gpay_kpi_repeat_purchase_rate_latest` | numberDisplay | Latest month |
| `api_execution_gpay_payments_7d` | numberDisplay | Last 7 days |
| `api_execution_gpay_payments_by_token_weekly` | bar | Weekly payment count split by token. Stacked bars show token mix and overall payment activity. |
| `api_execution_gpay_payments_hourly` | bar | Payment counts per hour over the last 14 complete days, broken down by token. Useful for spotting... |
| `api_execution_gpay_retention_by_action_monthly` | heatmap | Cohort retention heatmap by action type. Filter action and switch between users/volume views. |
| `api_execution_gpay_retention_by_action_users_monthly` | bar | Stacked cohort user activity over time. Filter by action type. |
| `api_execution_gpay_retention_monthly` | bar | By activation cohort |
| `api_execution_gpay_retention_pct_monthly` | heatmap | By activation cohort |
| `api_execution_gpay_retention_volume_monthly` | bar | By activation cohort, in USD |
| `api_execution_gpay_total_balance` | numberDisplay | EURe, GBPe, USDC.e |
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
| `api_execution_gpay_user_total_cashback` | numberDisplay | Lifetime cashback earned (GNO) |
| `api_execution_gpay_user_total_volume` | numberDisplay | Lifetime payment volume (USD) |
| `api_execution_gpay_volume_7d` | numberDisplay | Last 7 days |
| `api_execution_gpay_volume_payments_by_token_weekly` | bar | Weekly payment volume in USD split by token. Stacked bars show token contribution to total proces... |
| `api_execution_gpay_wallet_balance_composition` | pie | Current balance distribution across all tokens in Gnosis Pay wallets. Tokens below 1% of total ar... |
| `text_gpay_glossary` | text | Definitions of key concepts, KPIs, and action types used across the Gnosis Pay dashboard |

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
| `api_consensus_attestations_daily` | area | Daily attestation counts by inclusion-delay bucket. Lower delay buckets indicate faster inclusion... |
| `api_consensus_blob_commitments_daily` | bar | Daily number of blob commitments included by execution payloads. This tracks EIP-4844 data-availa... |
| `api_consensus_blocks_daily` | area | Daily produced versus missed blocks from consensus data. Divergence between series highlights val... |
| `api_consensus_credentials_latest` | pie | Current validator withdrawal credential split (0x00, 0x01, 0x02). Shares reflect migration from l... |
| `api_consensus_deposits_withdrawls_cnt_daily` | bar | Daily count of validator deposits and withdrawals. Compare both series to monitor validator-set e... |
| `api_consensus_deposits_withdrawls_volume_daily` | bar | Daily deposit and withdrawal volume in mGNO. Volume captures stake movement magnitude, not just e... |
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
| `api_consensus_validators_balances_dist_daily` | quantileBands | Daily validator effective-balance quantiles. Bands reveal concentration and spread across the val... |
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
| `api_esg_carbon_emissions_annualised_latest` | numberDisplay | Estimated annualised CO2e (in tCO2e) |
| `api_esg_carbon_emissions_daily` | quantileBands | Daily network CO2e estimate with uncertainty bands from model simulations. The central line is th... |
| `api_esg_cif_network_vs_countries_daily` | line | Compares Gnosis network carbon intensity (gCO2e/kWh) against selected country benchmarks. Values ... |
| `api_esg_energy_consumption_annualised_latest` | numberDisplay | Estimated annualised consumption (in MWh) |
| `api_esg_estimated_nodes_daily` | quantileBands | Estimated network node count per day with uncertainty bands. Estimation uses crawler-observed pee... |
| `api_esg_info_annual_daily` | quantileBands | Annualized emissions and energy projections derived from daily estimates. Bands communicate uncer... |
| `api_esg_info_category_daily` | bar | Daily emissions and energy estimates by node-category segment. Category filter shows which node g... |
| `esg_methodology` | text | Environmental, Social, and Governance methodology overview |
| `text_esg_methodology` | text | How we calculate and analyze the Gnosis network carbon emissions |

### Yields

The Yields sector provides a unified view of DeFi yield opportunities on Gnosis Chain across lending protocols, DEX liquidity pools, and the Savings xDAI vault. It is organized into five tabs.

**Overview tab** — headline KPIs and a cross-asset comparison table.

| Metric | Chart Type | Description |
|--------|-----------|-------------|
| `api_execution_yields_overview_lending_tvl` | numberDisplay | -- |
| `api_execution_yields_overview_lending_lenders` | numberDisplay | Current |
| `api_execution_yields_overview_lp_tvl` | numberDisplay | -- |
| `api_execution_yields_overview_lending_best_apy` | numberDisplay | -- |
| `api_execution_yields_overview_lp_best_apr` | numberDisplay | Last 7 days |
| `api_execution_yields_opportunities_latest` | table | Pools & lending ranked by yield |

**Savings xDAI tab** — Savings vault APY and supply tracking.

| Metric | Chart Type | Description |
|--------|-----------|-------------|
| `api_execution_yields_overview_sdai_apy` | numberDisplay | Current |
| `api_execution_yields_overview_sdai_supply` | numberDisplay | -- |
| `historical_yield_sdai` | line | APY for Savings xDAI (formerly sDAI) on rolling Moving Median (MM) |

**Lending tab** — per-token and per-protocol lending analytics with token/protocol filters and time range controls.

| Metric | Chart Type | Description |
|--------|-----------|-------------|
| `api_execution_yields_lending_lenders_count_7d` | numberDisplay | Current |
| `api_execution_yields_lending_borrowers_count_7d` | numberDisplay | Last 7 days |
| `api_execution_yields_lending_tvl_by_token_latest` | pie | Current distribution |
| `api_execution_yields_lending_balance_cohorts_holders_daily` | bar | Lender count by balance cohort |
| `api_execution_yields_lending_balance_cohorts_value_daily` | bar | Total value by balance cohort |
| `api_execution_yields_lending_daily` | line | Daily rates by token, split by lending protocol |
| `api_execution_yields_lending_activity_counts_weekly` | bar | Weekly unique count |
| `api_execution_yields_lending_activity_volumes_weekly` | bar | Weekly in USD |

**Pools tab** — DEX pool performance with token/pool filters and time range controls.

| Metric | Chart Type | Description |
|--------|-----------|-------------|
| `api_execution_yields_pools_tvl_latest` | numberDisplay | -- |
| `api_execution_yields_pools_volume_7d` | numberDisplay | Last 7 days |
| `api_execution_yields_pools_fees_7d` | numberDisplay | Last 7 days |
| `api_execution_yields_pools_lps_count_7d` | numberDisplay | Last 7 days |
| `api_execution_yields_pools_tvl_by_pool_latest` | pie | Current distribution |
| `api_execution_yields_pools_tvl_token_daily` | area | Daily by token |
| `api_execution_yields_pools_net_apr_daily` | line | 7-day trailing by pool |
| `api_execution_yields_pools_lp_activity_daily` | bar | Daily by pool |
| `api_execution_yields_pools_fees_usd_daily` | bar | Daily by pool |
| `api_execution_yields_pools_swap_count_daily` | bar | Daily by pool |
| `api_execution_yields_pools_volume_daily` | bar | Daily by pool |

**User Portfolio tab** — per-wallet yield analytics with wallet search. Requires explicit wallet address input.

| Metric | Chart Type | Description |
|--------|-----------|-------------|
| `api_execution_yields_user_top_wallets` | table | Top wallets by LP and lending activity for the User Portfolio dropdown. |
| `api_execution_yields_user_kpi_total_lp_fees` | numberDisplay | Lifetime (USD) |
| `api_execution_yields_user_kpi_lending_balance` | numberDisplay | Current (USD) |
| `api_execution_yields_user_kpi_active_lp_positions` | numberDisplay | -- |
| `api_execution_yields_user_kpi_active_lending_positions` | numberDisplay | Active reserves |
| `api_execution_yields_user_lp_positions` | table | Active and historical positions |
| `api_execution_yields_user_lending_positions` | table | Lending supply balances on Gnosis (Aave V3 & SparkLend) |
| `api_execution_yields_user_fee_collections_daily` | bar | Daily fees collected by pool |
| `api_execution_yields_user_lending_balances_daily` | bar | Daily supply balance by token |
| `api_execution_yields_user_activity` | table | LP & lending actions |

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
