# Execution Module

The Execution module is the largest module in dbt-cerebro. It covers all data produced by the Gnosis Chain execution layer (EVM), including blocks, transactions, logs, traces, contract deployments, native transfers, balance diffs, gas metrics, tokens, DeFi yield tracking, Gnosis Pay, and Circles.

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
<!-- generated: 2026-07-23 -->
**Account**

| Model | Layer | Description |
|-------|-------|-------------|
| `int_execution_account_balance_history_daily` | Intermediate | Address × date daily portfolio balance aggregate. Heavy GROUP BY over
int_execution_tokens_balances_daily lives in it... |
| `int_execution_account_token_movements_in_daily` | Intermediate | Inbound leg of token movements (to_address = address) aggregated by
(date, token_address, address, counterparty). Spl... |
| `int_execution_account_token_movements_out_daily` | Intermediate | Outbound leg of token movements (from_address = address) aggregated by
(date, token_address, address, counterparty). ... |
| `fct_execution_account_counterparty_edges_daily` | Fact | Daily directed account-counterparty graph edges from production movement and GPay activity facts. |
| `fct_execution_account_counterparty_edges_latest` | Fact | Latest bounded graph edge source for Account Portfolio interactions and relationships. |
| `fct_execution_account_linked_entities_latest` | Fact | Direct entity links for selected and linked-group Account Portfolio navigation. |
| `fct_execution_account_profile_latest` | Fact | Complete latest account profile for the Account Portfolio hero and routing layer. |
| `fct_execution_account_safes_latest` | Fact | One row per current (owner, Safe) pair, enriched with that Safe's threshold,
current owner count, version, and deploy... |
| `fct_execution_account_search_index` | Fact | Search index for address, Circles, Safe, GPay, Gnosis App, validator, and withdrawal credential lookup. |
| `fct_execution_account_token_balances_latest` | Fact | Latest non-zero token balances by address, optimized for account lookup. |
| `fct_execution_account_token_movements_daily` | Fact | Daily token movement legs by address, counterparty, token, and direction from production whitelisted daily transfers. |
| `fct_execution_account_transaction_summary_latest` | Fact | Latest address-grain activity summary derived from production token movement facts. |
| `api_execution_account_balance_history_daily` | API | Simple API view for Account Portfolio balance history. |
| `api_execution_account_counterparty_graph` | API | Simple API view for Account Portfolio counterparty graph rows. |
| `api_execution_account_linked_entities_latest` | API | Simple API view for direct linked entities. |
| `api_execution_account_profile_latest` | API | Simple API view over the latest Account Portfolio profile fact. |
| `api_execution_account_recent_transactions` | API | Recent production-backed token movement rows for Account Portfolio transaction tables. |
| `api_execution_account_safes_latest` | API | Reverse lookup — given an address, list every Safe it currently owns,
enriched with that Safe's threshold, current ow... |
| `api_execution_account_search_index` | API | Simple API view over Account Portfolio search index. |
| `api_execution_account_token_balances_latest` | API | Simple API view for latest Account Portfolio token balances. |
| `api_execution_account_token_movements_daily` | API | Simple API view for Account Portfolio token movements. |
| `api_execution_account_transaction_summary_latest` | API | Simple API view for Account Portfolio transaction/activity summary. |
| `api_execution_account_validators_latest` | API | Account-facing validator member view filterable by withdrawal address or credential. |

**Accounts**

| Model | Layer | Description |
|-------|-------|-------------|
| `int_execution_accounts_label_contracts` | Intermediate | Protocol / token / infra contract addresses identified from Dune labels (int_crawlers_data_labels), restricted to non... |
| `int_execution_accounts_non_user_contracts` | Intermediate | Deployed contracts that are NOT Safe proxies: the exclusion set that
defines the per-user "user" universe (users = EO... |

**Address**

| Model | Layer | Description |
|-------|-------|-------------|
| `int_execution_address_roles_current` | Intermediate | Identity-role pivot: one row per on-chain address with boolean flags
for every role it plays across the sectors we tr... |
| `fct_execution_address_resolver` | Fact | Per-(address × source) domain resolver rows. The cross-source merge
happens at query time inside `api_execution_addre... |
| `fct_ubo_address_classification` | Fact | Maps every labeled address to its UBO terminal classification. Filters to the six sectors relevant for UBO coverage a... |
| `api_execution_address_resolver` | API | Per-address merge view over `fct_execution_address_resolver`. Collapses
the per-source rows into a single row per add... |
| `api_execution_address_search` | API | Lightweight dropdown source for the Account Portfolio tab's global
filter. Two columns (address + display_name), `all... |

**Auto**

| Model | Layer | Description |
|-------|-------|-------------|
| `stg_envio_ga__auto_topups` | Staging | Circles auto-topup CONFIG event ledger from the envio_ga indexer (source envio_ga.auto_topup), materialized as a view... |

**Avatars**

| Model | Layer | Description |
|-------|-------|-------------|
| `stg_envio_ga__avatars` | Staging | Circles avatar state — the active-user spine (composite-version dedup). INTERNAL. |

**Balancer**

| Model | Layer | Description |
|-------|-------|-------------|
| `stg_pools__balancer_v2_events` | Staging | Normalized signed token deltas for Balancer V2 pools, decoded from Vault events
(PoolBalanceChanged, PoolBalanceManag... |
| `stg_pools__balancer_v2_pool_registry` | Staging | Mapping of Balancer V2 poolId (bytes32) to pool contract address, built from
PoolRegistered events emitted once per p... |
| `stg_pools__balancer_v3_events` | Staging | Unified Balancer V3 Vault event stream normalized into a single
row-shape: (pool_address | wrapped_token_address, blo... |
| `stg_pools__balancer_v3_token_map` | Staging | Balancer V3 ERC4626 wrapper → underlying token mapping. Used to resolve wrapped Aave tokens (waGno*) to their underly... |

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

**Bridges**

| Model | Layer | Description |
|-------|-------|-------------|
| `int_execution_bridges_address_flows_daily` | Intermediate | Address-grain bridge flows. Joins whitelisted transfers against the
dune labels set filtered on bridge projects to ex... |

**Cashback**

| Model | Layer | Description |
|-------|-------|-------------|
| `stg_envio_ga__cashback_status_history` | Staging | Staging view over the envio_ga indexer's `cashback_status_history` source: one row per cashback-NFT status-transition... |

**Cashbacks**

| Model | Layer | Description |
|-------|-------|-------------|
| `stg_envio_ga__cashbacks` | Staging | Gnosis Pay cashback NFT mints (grain = mint id). INTERNAL. |

**Circles**

| Model | Layer | Description |
|-------|-------|-------------|
| `int_execution_circles_v2_active_avatars_weekly` | Intermediate | Week-bucketed Circles v2 activity (one row per (week, address)) covering human registrations, trust events, and perso... |
| `int_execution_circles_v2_avatar_metadata` | Intermediate | Current parsed IPFS metadata for every Circles v2 avatar. Joins each
avatar's latest (avatar, metadata_digest) pair f... |
| `int_execution_circles_v2_avatar_metadata_history` | Intermediate | SCD-style historical view of every Circles v2 avatar metadata change.
One row per (avatar, metadata_digest) ever anno... |
| `int_execution_circles_v2_avatar_metadata_targets` | Intermediate | Deterministic queue of every (avatar, metadata_digest) pair the Circles v2
NameRegistry has ever announced. Built as ... |
| `int_execution_circles_v2_avatars` | Intermediate | Circles v2 avatar registration events (Human, Group, Org) normalized for downstream analytics. |
| `int_execution_circles_v2_backers_current` | Intermediate | Trust-defined backers snapshot. One row per address ever trusted by the backers group avatar (var('circles_target_gro... |
| `int_execution_circles_v2_backing` | Intermediate | Captures Circles backing lifecycle events with decoded participants and metadata for downstream analytics. |
| `int_execution_circles_v2_backing_depositors_current` | Intermediate | Current snapshot of distinct depositor addresses with lifecycle counts. |
| `int_execution_circles_v2_backing_events_daily` | Intermediate | Daily Circles v2 backing-lifecycle event counts. Tracks the "depositors" set — addresses that emit a backing event. N... |
| `int_execution_circles_v2_balance_cohorts_daily` | Intermediate | Daily distribution of CRC holders across balance buckets, aggregated from daily balances. |
| `int_execution_circles_v2_balance_diffs_daily` | Intermediate | Daily aggregated per-account balance deltas derived from unified v2 transfers. One row per (date, account, token_addr... |
| `int_execution_circles_v2_balances_daily` | Intermediate | Daily end-of-day token balances per account for Circles v2 tokens with demurrage adjustment. |
| `int_execution_circles_v2_crc20_pools` | Intermediate | View of all Uniswap V3 and Swapr V3 pools that contain at least one CRC20 wrapper token. Combines the dynamic pool re... |
| `int_execution_circles_v2_crc20_prices_raw` | Intermediate | Trade-level executed prices for CRC20 wrapper tokens across all supported DEX protocols. Filters int_execution_pools_... |
| `int_execution_circles_v2_economically_active_avatars_weekly` | Intermediate | Circles-first ECONOMICALLY ACTIVE avatars, ecosystem-wide — one row per (week, avatar, earning_kind) where the avatar... |
| `int_execution_circles_v2_gcrc_cashback_recipients_weekly` | Intermediate | Weekly gCRC cashback recipients — addresses that received >= 1 gCRC (group token 0x548c…4bc1) from the Circles cashba... |
| `int_execution_circles_v2_group_collateral_balances_daily` | Intermediate | Daily end-of-day group collateral balances per token, derived from cumulative collateral diffs. |
| `int_execution_circles_v2_group_collateral_diffs` | Intermediate | Per-group collateral deltas from StandardTreasury lock, burn, and return events. |
| `int_execution_circles_v2_group_settings_updates` | Intermediate | Group configuration changes from BaseGroupFactory, CMGroupDeployer, and BaseGroup runtime events. |
| `int_execution_circles_v2_group_size_daily` | Intermediate | Per-group member count over time (one row per group_address per day). Members are the trustees on the group's outgoin... |
| `int_execution_circles_v2_groups_overview_daily` | Intermediate | Network-level daily group metrics — new groups + collateral activity. |
| `int_execution_circles_v2_hub_events_daily` | Intermediate | Daily count of every Circles v2 Hub event, broken down by event_name. Per (date, event_name): n_events, n_tx, n_disti... |
| `int_execution_circles_v2_hub_transfers` | Intermediate | Circles v2 ERC-1155 TransferSingle and TransferBatch events from the Hub, exploded into individual rows. |
| `int_execution_circles_v2_invite_funnel` | Intermediate | One row per invited human, carrying the mint-cadence signals for the five-stage funnel (Invited → ≥2 days → ≥7 days →... |
| `int_execution_circles_v2_inviter_canonical` | Intermediate | Canonical inviter per Circles v2 Human avatar, resolving the
invitation-at-scale "farm". Hub.RegisterHuman records in... |
| `int_execution_circles_v2_inviter_fees` | Intermediate | Per-event Circles v2 inviter-fee transfers — wrapped-CRC ERC-20 Transfer events in the same tx as a Hub.PersonalMint,... |
| `int_execution_circles_v2_mint_activity_daily` | Intermediate | Densified per-(avatar, date) personal-mint activity with 14-day rolling window. Replaces Dune's gnosis_circlesv2_mint... |
| `int_execution_circles_v2_mint_events` | Intermediate | One row per protocol mint, tagged with `mint_kind`. Sourced from the DECODED Hub events in contracts_circles_v2_Hub_e... |
| `int_execution_circles_v2_mints_daily` | Intermediate | Network-level daily mint summary broken down by mint_kind: total mint events, distinct recipient addresses, and total... |
| `int_execution_circles_v2_offer_cycles` | Intermediate | ERC20TokenOfferCycle events capturing configuration, creation, deposits, claims, and withdrawals. |
| `int_execution_circles_v2_payments` | Intermediate | Payment events from the PaymentGatewayFactory with decoded payer, payee, and amount. |
| `int_execution_circles_v2_referrers` | Intermediate | "Users who start referring" — one row per inviter, i.e. each address that appears as invited_by on a Circles v2 Human... |
| `int_execution_circles_v2_score_mints` | Intermediate | Per-mint fact for the OffchainScoreBasedMintPolicy PersonalMinted event — one row per score-based personal mint. `col... |
| `int_execution_circles_v2_tokens_supply_daily` | Intermediate | Per-token Circles v2 daily supply derived from the zero-address balance in `int_execution_circles_v2_balances_daily`.... |
| `int_execution_circles_v2_transfers` | Intermediate | Unified Circles v2 transfers combining Hub ERC-1155 and ERC-20 wrapper transfers. Static wrapper amounts are converte... |
| `int_execution_circles_v2_transfers_categorised` | Intermediate | Per-transfer categorisation of int_execution_circles_v2_transfers into one of mint / burn / wrap / unwrap / p2p. (Mat... |
| `int_execution_circles_v2_transfers_daily` | Intermediate | Daily transfer counts + volume per category. |
| `int_execution_circles_v2_trust_pair_ranges` | Intermediate | Validity ranges for Circles v2 trust relations. One row per (truster, trustee) pair, with parallel arrays valid_from_... |
| `int_execution_circles_v2_trust_updates` | Intermediate | Raw trust update events from Circles v2 Trust events, normalized into a common schema. |
| `int_execution_circles_v2_trusts_daily` | Intermediate | Event-grain daily trust activity: total trust events, new trusts (expiry > block_timestamp), revoked trusts (expiry <... |
| `int_execution_circles_v2_wrapper_supply_daily` | Intermediate | Daily wrapped-supply delta per ERC-20 wrapper token. |
| `int_execution_circles_v2_wrapper_tokens` | Intermediate | Reference table mapping Circles V2 ERC-20 wrapper addresses to their on-chain token symbol. Rebuilt daily. Symbol is ... |
| `int_execution_circles_v2_wrapper_transfers` | Intermediate | ERC20 Transfer events for Circles v2 wrapper tokens parsed from raw logs. |
| `int_execution_circles_v2_wrappers` | Intermediate | ERC20 wrapper deployments from the ERC20Lift contract, mapping avatars to their wrapper token addresses. |
| `fct_execution_circles_human_avatars_distinct` | Fact | One row per `user_pseudonym` for Circles v2 HUMAN avatars
(Groups and Orgs excluded — those aren't user-grain entitie... |
| `fct_execution_circles_v2_active_minters_daily` | Fact | Per-day count of Circles v2 "Active Minters" — avatars that minted on each of the last 14 days AND whose 14-day mint ... |
| `fct_execution_circles_v2_active_trusts_daily` | Fact | Dense daily time series of network-wide active trust relationships. |
| `fct_execution_circles_v2_avatar_balances_daily` | Fact | Materialized daily avatar token balances with dust filtering (> 0.001 CRC). Derived from int_execution_circles_v2_bal... |
| `fct_execution_circles_v2_avatar_balances_latest` | Fact | Latest per-(avatar, token) CRC balance snapshot with an is_wrapped flag
indicating whether the token_address is an ER... |
| `fct_execution_circles_v2_avatar_personal_token_supply_latest` | Fact | One-row-per-avatar summary of a Circles v2 avatar's own personal CRC
token: total circulating supply, how much is wra... |
| `fct_execution_circles_v2_avatar_token_distribution` | Fact | Per-avatar distribution of holders of a Circles v2 personal CRC token
(the ERC-1155 token whose token_address equals ... |
| `fct_execution_circles_v2_avatar_tokens_held_count` | Fact | Per-avatar count of distinct CRC tokens currently held with a balance
above the 0.001 CRC dust threshold (1e15 raw we... |
| `fct_execution_circles_v2_avatar_trusts_daily` | Fact | Daily cumulative trust statistics per avatar (trusts given and received). |
| `fct_execution_circles_v2_avatar_trusts_summary` | Fact | Latest per-avatar trust summary: trusts given and trusts received as of
the last complete day. Materialised daily fro... |
| `fct_execution_circles_v2_avatars` | Fact | Dense daily time series of avatar type counts with cumulative totals. |
| `fct_execution_circles_v2_backers_cumulative_daily` | Fact | Daily EVER-BACKED cumulative count of trust-defined backers (addresses ever trusted by the backers group avatar var('... |
| `fct_execution_circles_v2_backers_current_daily` | Fact | Daily count of CURRENTLY-TRUSTED backers: addresses whose trust interval from the backers group avatar var('circles_t... |
| `fct_execution_circles_v2_crc20_prices_daily` | Fact | Daily aggregated executed prices for CRC20 wrapper tokens, one row per (date, crc20_token, backing_token, pool_addres... |
| `fct_execution_circles_v2_economically_active_avatars_weekly` | Fact | Weekly counts of economically active Circles avatars, ecosystem-wide (circles-first layer; NOT app-filtered). Rows pe... |
| `fct_execution_circles_v2_group_size_current` | Fact | Current size of every Circles v2 group, where size = distinct trustees in the group's outgoing trust list. Includes g... |
| `fct_execution_circles_v2_group_token_supply_current` | Fact | Per-group personal-token supply snapshot. One row per Group avatar with supply / wrapped / unwrapped / wrapped_pct an... |
| `fct_execution_circles_v2_group_token_supply_daily` | Fact | Daily aggregate of Circles v2 group-token supply, split between native ERC-1155 and wrapped ERC-20 forms. Aggregated ... |
| `fct_execution_circles_v2_inviter_farm_quota` | Fact | Per-inviter Circles-v2 InvitationFarm ("invitation-at-scale") state: invites claimed from the farm and latest granted... |
| `fct_execution_circles_v2_inviters_ranking` | Fact | Leaderboard of top inviters by number of human avatars invited. |
| `fct_execution_circles_v2_minter_cohort_daily` | Fact | Daily cohort distribution of Circles v2 minters bucketed by 14-day mint coverage (mint_14dw / 336). Six buckets: <1%,... |
| `fct_execution_circles_v2_stats_current` | Fact | Current aggregate statistics for Circles v2 (avatar, trust, token, wrapper counts). |
| `fct_execution_circles_v2_supply_by_holder_type_daily` | Fact | Daily CRC supply breakdown by holder type (avatar type or Dune label sector). |
| `fct_execution_circles_v2_tokens_supply_daily` | Fact | Compatibility view over `int_execution_circles_v2_tokens_supply_daily`. Column-level tests and shape live on the inte... |
| `fct_execution_circles_v2_total_supply_daily` | Fact | Network-wide daily total CRC supply aggregated across all tokens. |
| `fct_execution_circles_v2_trust_relations_current` | Fact | Current active trust relations for Circles v2, derived from trust_pair_ranges. |
| `fct_execution_circles_v2_trusts_distribution` | Fact | Distribution histogram of trust degree (given/received) across avatars. |
| `api_execution_circles_v2_active_minters_daily` | API | Time-series view over fct_execution_circles_v2_active_minters_daily; latest day excluded. |
| `api_execution_circles_v2_active_trusts_cnt_latest` | API | Latest active trust count with 7-day change percentage. |
| `api_execution_circles_v2_active_trusts_daily` | API | API view of daily active trust count time series. |
| `api_execution_circles_v2_avatar_balances_daily` | API | Daily CRC balance per avatar broken down by token (one row per avatar/date/token). |
| `api_execution_circles_v2_avatar_balances_latest` | API | Latest per-(avatar, token) CRC balance snapshot with an is_wrapped flag
indicating whether the token_address is an ER... |
| `api_execution_circles_v2_avatar_metadata` | API | Per-avatar identity for Circles v2: on-chain registration metadata
(avatar type, on-chain name, inviter, token_id, re... |
| `api_execution_circles_v2_avatar_metadata_history` | API | Historical timeline of every Circles v2 avatar metadata change. Thin
passthrough over int_execution_circles_v2_avatar... |
| `api_execution_circles_v2_avatar_mint_activity_daily` | API | Daily personal-mint activity per Circles v2 avatar.

A Circles v2 personal mint is a Hub TransferSingle event where
f... |
| `api_execution_circles_v2_avatar_personal_token_supply_latest` | API | One-row-per-avatar summary of a Circles v2 avatar's own personal CRC
token: total circulating supply, how much is wra... |
| `api_execution_circles_v2_avatar_search` | API | Lightweight (avatar, display_name) lookup used by the dashboard global
filter to support searching avatars by display... |
| `api_execution_circles_v2_avatar_token_distribution` | API | Per-avatar distribution of holders of a Circles v2 personal CRC token
(the ERC-1155 token whose token_address equals ... |
| `api_execution_circles_v2_avatar_tokens_held_count` | API | Per-avatar count of distinct CRC tokens currently held with a balance
above the 0.001 CRC dust threshold (1e15 raw we... |
| `api_execution_circles_v2_avatar_trust_network` | API | Trust-network edge list for the Circles v2 Avatar Trust Network panel.

One row per directed trust edge from the pers... |
| `api_execution_circles_v2_avatar_trust_relations` | API | Current active trust relations pivoted to one row per (avatar, counterparty) pair with direction (outgoing, incoming,... |
| `api_execution_circles_v2_avatar_trusts_daily` | API | Daily cumulative trusts given and received per avatar. |
| `api_execution_circles_v2_avatar_trusts_summary` | API | Latest snapshot of cumulative trusts given and received per avatar. |
| `api_execution_circles_v2_avatars` | API | API view of daily avatar type counts and cumulative totals. |
| `api_execution_circles_v2_avatars_current` | API | API view of current Circles v2 avatar registrations. |
| `api_execution_circles_v2_backers_cumulative_daily` | API | Time-series view of trust-defined EVER-BACKED cumulative backers (ignores revocation); latest day excluded. For the r... |
| `api_execution_circles_v2_backers_current_daily` | API | Time-series of currently-trusted (revocation-aware) backers; latest day excluded. Distinct from api:circles_v2_backer... |
| `api_execution_circles_v2_backing_depositors_current` | API | Snapshot of distinct depositor addresses. |
| `api_execution_circles_v2_backing_events_daily` | API | Time-series of Circles v2 backing-lifecycle events, by stage. |
| `api_execution_circles_v2_balance_cohorts_daily` | API | Daily wealth distribution: distinct CRC holders bucketed by balance tier (0-1 / 1-10 / 10-100 / 100-1k / 1k-10k / 10k... |
| `api_execution_circles_v2_crc20_prices_daily` | API | Public daily price view for CRC20 wrapper tokens, consolidated across all pools. One row per (date, crc20_token) with... |
| `api_execution_circles_v2_economically_active_avatars_weekly` | API | Weekly economically active Circles avatars (ecosystem-wide, circles-first definition) by earning_kind, with the in-ap... |
| `api_execution_circles_v2_gcrc_cashback_cumulative` | API | Cumulative Circles v2 gCRC cashback over time, one row per week: the running total gCRC distributed and the running c... |
| `api_execution_circles_v2_gcrc_cashback_recipients_ranking` | API | Top 100 lifetime recipients of Circles v2 gCRC cashback, ranked by total amount received, enriched with each recipien... |
| `api_execution_circles_v2_gcrc_cashback_total` | API | Lifetime (single-row) Circles v2 gCRC cashback totals for KPI tiles: the cumulative cashback amount distributed and t... |
| `api_execution_circles_v2_gcrc_cashback_weekly` | API | Weekly Circles v2 gCRC cashback distribution: distinct recipient count and total gCRC amount sent from the cashback w... |
| `api_execution_circles_v2_group_collateral_daily` | API | Per-group daily member-CRC collateral (native units). |
| `api_execution_circles_v2_group_explorer_profile` | API | One row per Circles v2 group: identity, on-chain handlers, and snapshot KPIs (members, supply, wrapped %, collateral,... |
| `api_execution_circles_v2_group_holders` | API | Holders of a group's token, resolving both native ERC-1155 and ERC-20 wrapper legs (wrapper mapped back to group via ... |
| `api_execution_circles_v2_group_member_scores` | API | Latest on-chain score per (score-based group, member), from the OffchainScoreBasedMintPolicy PersonalMinted event. On... |
| `api_execution_circles_v2_group_members` | API | Members of a group (trustees on its outgoing trust list) with profile and join date; is_mutual flags reciprocal trust. |
| `api_execution_circles_v2_group_mints_daily` | API | Per-group daily group-token mints vs collateral redemptions (distinct tokens/units, labelled in the kind column). |
| `api_execution_circles_v2_group_score_distribution` | API | Count of members per score bucket, per score-based group. Buckets carry a bucket_rank for stable ordering in charts. |
| `api_execution_circles_v2_group_search` | API | (group_address, display_name) lookup backing the Group Explorer global filter. One row per Circles v2 Group avatar. |
| `api_execution_circles_v2_group_size_daily` | API | Per-group daily member count, from historical trust intervals. |
| `api_execution_circles_v2_group_size_distribution` | API | Histogram of Circles v2 group sizes (members per group). |
| `api_execution_circles_v2_group_supply_daily` | API | Per-group daily token supply, split native ERC-1155 vs ERC-20 wrapper (wrapper level = prefix-sum of wrapper supply d... |
| `api_execution_circles_v2_group_token_supply_daily` | API | Long-format time-series view (one row per (date, label)) over fct_execution_circles_v2_group_token_supply_daily, read... |
| `api_execution_circles_v2_group_token_supply_top_latest` | API | Top 100 Circles v2 groups by personal-token supply (leaderboard view). |
| `api_execution_circles_v2_groups_cnt_latest` | API | Latest count of group avatars and 7-day percentage change. |
| `api_execution_circles_v2_groups_overview_daily` | API | Daily group registrations + collateral activity, with cumulative group total. |
| `api_execution_circles_v2_hub_events_daily` | API | Time-series view over int_execution_circles_v2_hub_events_daily; latest day excluded. |
| `api_execution_circles_v2_humans_cnt_latest` | API | Latest count of human avatars and 7-day percentage change. |
| `api_execution_circles_v2_invite_funnel_cohort_monthly` | API | Invitee cohort by month, with the five-stage mint-cadence funnel (Invited → ≥2 days → ≥7 days → ≥14 days → Active Min... |
| `api_execution_circles_v2_inviter_farm_quota` | API | Inviter InvitationFarm leaderboard (invites claimed + current quota), ordered by invites_claimed. Passthrough over fc... |
| `api_execution_circles_v2_inviters_ranking` | API | Top-N inviters leaderboard ordered by number of human avatars invited. Pre-joins the inviter's display name, preview ... |
| `api_execution_circles_v2_kpi_active_minters_latest` | API | KPI: yesterday's Active Minters count with WoW pct change. |
| `api_execution_circles_v2_kpi_avg_members_per_group_latest` | API | KPI: average and median members per group. |
| `api_execution_circles_v2_kpi_avg_trusts_per_avatar_latest` | API | KPI: average trusts per human avatar = active_trusts / humans. Network-density indicator. |
| `api_execution_circles_v2_kpi_depositors_in_backers_pct_latest` | API | KPI: % of depositors that ended up trusted by the backers group. |
| `api_execution_circles_v2_kpi_group_token_supply_latest` | API | KPI: aggregate group-token supply with 7d change. |
| `api_execution_circles_v2_kpi_group_wrapped_pct_latest` | API | KPI: share of group-token supply held as ERC-20 wrappers, with 7d delta. |
| `api_execution_circles_v2_kpi_mints_7d` | API | KPI: total mints in the last 7 full days with WoW pct change. |
| `api_execution_circles_v2_kpi_new_backers_7d` | API | KPI: backers newly trusted in the last 7 days with WoW change. |
| `api_execution_circles_v2_kpi_new_groups_7d` | API | KPI: groups registered in the last 7 days with WoW change. |
| `api_execution_circles_v2_kpi_new_trusts_7d` | API | KPI: new trusts granted in the last 7 full days with WoW pct change. |
| `api_execution_circles_v2_kpi_total_backers_latest` | API | KPI: backers currently trusted by the backers group (revocation-aware), with 7d change. |
| `api_execution_circles_v2_kpi_total_depositors_latest` | API | KPI: total distinct depositors with 7d-new and WoW change. |
| `api_execution_circles_v2_kpi_total_supply_latest` | API | KPI: latest network-wide CRC supply with 7-day pct change. |
| `api_execution_circles_v2_minter_cohort_daily` | API | Time-series view over fct_execution_circles_v2_minter_cohort_daily; latest day excluded. |
| `api_execution_circles_v2_mints_daily` | API | Time-series view over int_execution_circles_v2_mints_daily; latest day excluded. One row per (date, mint_kind) — mint... |
| `api_execution_circles_v2_orgs_cnt_latest` | API | Latest count of organization avatars and 7-day percentage change. |
| `api_execution_circles_v2_p2p_velocity_daily` | API | Peer-to-peer transfer velocity (mint/burn/wrap/unwrap excluded). |
| `api_execution_circles_v2_pool_explorer_liquidity_daily` | API | Daily count of liquidity events (Mint = 'Add', Burn = 'Remove') per Uniswap V3 Circles pool, deduped on (transaction_... |
| `api_execution_circles_v2_pool_explorer_liquidity_events` | API | Individual liquidity events (Mint mapped to Add, Burn to Remove) for the main Uniswap V3 Circles pools, one row per e... |
| `api_execution_circles_v2_pool_explorer_swaps` | API | Individual recent swaps executed on the main Circles v2 DEX pools, scoped to the curated liquidity pools for the Pool... |
| `api_execution_circles_v2_pool_explorer_swaps_daily` | API | Daily swap activity per main Circles DEX pool tracked in the Pool Explorer: number of swaps, total USD volume, and di... |
| `api_execution_circles_v2_pool_search` | API | Point-in-time (pool_address, display_name) lookup of Circles v2 liquidity pools that backs the Pool Explorer filter d... |
| `api_execution_circles_v2_pools_daily` | API | Daily liquidity/market metrics for the main Circles DEX pools (seed circles_liquidity_pools), one row per (date, pool... |
| `api_execution_circles_v2_pools_latest` | API | One row per main Circles DEX pool: latest TVL plus trailing-7d volume, trades, distinct traders and fees. Backs the L... |
| `api_execution_circles_v2_pools_reserves_daily` | API | Daily USD total value locked (TVL) per main Circles DEX pool, computed as the sum of both token legs' USD value. Back... |
| `api_execution_circles_v2_pools_reserves_latest` | API | Latest per-(pool, token) reserve, token USD price and TVL for the main Circles DEX pools. Emits two rows per pool (on... |
| `api_execution_circles_v2_pools_reserves_token_daily` | API | Daily per-(pool, token) reserve balance and USD valuation for the main Circles DEX pools (Uniswap V3 and Balancer V3)... |
| `api_execution_circles_v2_pools_traders_daily` | API | Daily distinct traders and trade count per main Circles DEX pool. A trader is the swap taker (Swap recipient), fallin... |
| `api_execution_circles_v2_score_mints_daily` | API | Daily score-based mint activity per group: mint count, distinct minters, average member score at mint, and total grou... |
| `api_execution_circles_v2_stats_current` | API | Snapshot of network-level Circles v2 counts (avatars total + by type, active trusts, tokens, wrappers). One row per m... |
| `api_execution_circles_v2_supply_by_holder_type_daily` | API | API view of daily CRC supply breakdown by holder type (avatar type or Dune label sector). |
| `api_execution_circles_v2_total_supply_daily` | API | API view of daily network-wide CRC supply. |
| `api_execution_circles_v2_transfers_daily` | API | Time-series of Circles v2 transfers by category. |
| `api_execution_circles_v2_trust_relations_current` | API | API view of current active Circles v2 trust relations. |
| `api_execution_circles_v2_trusts_daily` | API | Time-series view over int_execution_circles_v2_trusts_daily; latest day excluded. |
| `api_execution_circles_v2_trusts_distribution` | API | Distribution histogram of trust degree (given / received) across avatars. Each row is a (direction, bucket) cell with... |
| `api_execution_circles_v2_wrapper_share_daily` | API | Network wrapped vs unwrapped supply share over time. |

**Claims**

| Model | Layer | Description |
|-------|-------|-------------|
| `int_ubo_claims_aave_daily` | Intermediate | Per-protocol UBO supply claims for Aave V3 + SparkLend. Standardized shape: one row per (date, protocol, container_ad... |
| `int_ubo_claims_balancer_v2_daily` | Intermediate | Per-protocol UBO supply claims for Balancer V2. Standardized shape: one row per (date, container_address, ubo_address... |
| `int_ubo_claims_curve_daily` | Intermediate | Per-protocol UBO supply claims for Curve 3pool (0x7f90122bf0700f9e7e1f688fe926940e8839f353) on Gnosis Chain. Unwinds ... |
| `int_ubo_claims_sdai_daily` | Intermediate | Per-protocol UBO supply claims for the sDAI ERC4626 vault (0xaf204776c7245bf4147c2612bf6e5972ee483701) on Gnosis Chai... |
| `int_ubo_claims_swapr_v3_daily` | Intermediate | Per-user UBO supply claims for Swapr V3 (Algebra). Standardized shape: one row per (date, container_address, ubo_addr... |
| `int_ubo_claims_uniswap_v3_daily` | Intermediate | Per-user UBO supply claims for Uniswap V3. Standardized shape: one row per (date, container_address, ubo_address, tok... |

**Coordinator**

| Model | Layer | Description |
|-------|-------|-------------|
| `stg_envio_ga__coordinator_states` | Staging | Current-state (grain = one row per coordinator address) view of Circles auto-topup coordinators, sourced from the env... |

**Cow**

| Model | Layer | Description |
|-------|-------|-------------|
| `int_execution_cow_batches` | Intermediate | Batch-level aggregates for CoW Protocol settlements. One row per settlement transaction with trade counts, interactio... |
| `int_execution_cow_trades` | Intermediate | Pure on-chain CoW Protocol trades enriched with token metadata (symbol, decimals), USD prices (ASOF daily), and the s... |
| `fct_execution_cow_daily` | Fact | Daily CoW Protocol metrics: volume, trades, unique traders, fees, batch counts, CoW ratio (peer-to-peer matching shar... |
| `fct_execution_cow_solvers` | Fact | Solver registry built from SolverAdded/SolverRemoved events. Shows the latest status (active/inactive) of each solver. |
| `fct_execution_cow_solvers_daily` | Fact | Daily per-solver performance metrics: trades, volume, fees, batches, CoW batches, and gas costs. |
| `fct_execution_cow_trades` | Fact | Canonical CoW Protocol trades table. Joins on-chain trade data from int_execution_cow_trades with off-chain protocol ... |
| `api_execution_cow_batch_metrics_ts` | API | Daily average number of trades settled per CoW Protocol batch. Values above 1.0 indicate days where the solver matche... |
| `api_execution_cow_batch_routing_ts` | API | Daily share of CoW Protocol settlement batches by routing type, as percentages of total daily batches. Three labels: ... |
| `api_execution_cow_fees_ts` | API | Daily CoW Protocol revenue (USD) on Gnosis Chain. Filtered to fee_source = 'api' — surplus-based fees introduced Sep ... |
| `api_execution_cow_kpi_active_solvers` | API | Number of distinct solvers that settled at least one batch in the last 7 complete days, with week-over-week change. R... |
| `api_execution_cow_kpi_fees_7d` | API | 7-day CoW Protocol revenue (USD) with week-over-week change. Reflects surplus-based fees (fee_source = 'api', Sep 202... |
| `api_execution_cow_kpi_solver_value_7d` | API | 7-day gross solver value (USD) with week-over-week change. Covers priceImprovement and surplus fee policies (Sep 2024+). |
| `api_execution_cow_kpi_traders_7d` | API | 7-day unique trader count (exact) with week-over-week change. Uses fct_execution_cow_trades directly for exact uniqEx... |
| `api_execution_cow_kpi_trades_7d` | API | 7-day CoW Protocol trade count with week-over-week change. |
| `api_execution_cow_kpi_volume_7d` | API | 7-day CoW Protocol trading volume with week-over-week change. |
| `api_execution_cow_solver_value_ts` | API | Daily gross value generated by CoW solvers on Gnosis Chain (USD). For each trade with a priceImprovement or surplus f... |
| `api_execution_cow_solvers_volume_ts` | API | Daily volume by solver, top 6 by recent (180d) volume plus an "Other" bucket. Solver labels come from the cow_solvers... |
| `api_execution_cow_top_pairs_weekly` | API | Weekly volume by top 8 directional token pairs (sold → bought), with remaining pairs grouped as "Other". Pair ranking... |
| `api_execution_cow_trades_ts` | API | Daily CoW Protocol trade count. |
| `api_execution_cow_volume_ts` | API | Daily CoW Protocol trading volume. Client-side time-range filtering applies via the dashboard's global selector. |

**Data**

| Model | Layer | Description |
|-------|-------|-------------|
| `fct_crawlers_data_distinct_projects_sectors` | Fact | This model identifies unique combinations of projects and sectors from crawler data, supporting analysis of project-s... |
| `api_crawlers_data_distinct_projects_sectors_totals` | API | This view aggregates the total number of distinct projects and sectors crawled, providing a high-level overview of da... |

**Deposists**

| Model | Layer | Description |
|-------|-------|-------------|
| `int_GBCDeposit_deposists_daily` | Intermediate | The `int_GBCDeposit_deposists_daily` view aggregates daily deposit amounts and withdrawal credentials from GBC deposi... |

**Dex**

| Model | Layer | Description |
|-------|-------|-------------|
| `stg_live__dex_trades_balancer_v2` | Staging | Normalized Balancer V2 Swap events from the Vault contract (execution_live). PoolId → pool_address is resolved via th... |
| `stg_live__dex_trades_balancer_v3` | Staging | Normalized Balancer V3 Swap events from the Vault contract (execution_live). Applies the wrapped-token map (`stg_pool... |
| `stg_live__dex_trades_swapr_v3` | Staging | Normalized Swapr V3 (Algebra) Swap events from execution_live logs. Same schema/logic as Uniswap V3 — Algebra uses th... |
| `stg_live__dex_trades_uniswap_v3` | Staging | Normalized Uniswap V3 Swap events from execution_live logs. Derives bought/sold token & amounts from the signed `amou... |
| `int_live__dex_trades_raw` | Intermediate | Cached, rolling 48h window of unified DEX swaps across all supported protocols (Uniswap V3, Swapr V3, Balancer V2, Ba... |

**Earned**

| Model | Layer | Description |
|-------|-------|-------------|
| `stg_envio_ga__earned_from_invite` | Staging | GA-native invite-reward ledger (grain = event id). INTERNAL. |

**Gnosis**

| Model | Layer | Description |
|-------|-------|-------------|
| `int_execution_gnosis_app_bundlers` | Intermediate | Dynamic Cometh ERC-4337 bundler allowlist for Gnosis App attribution.
Supersedes the hand-maintained seeds/gnosis_app... |
| `int_execution_gnosis_app_first_conversion` | Intermediate | One row per Gnosis App user (the onboard cohort) with the date of their
first event in each conversion kind. Feeds th... |
| `int_execution_gnosis_app_gp_card_ga_link` | Intermediate | Authoritative, MODULE-AGNOSTIC Gnosis Pay card -> Gnosis App LINK, one row per CANONICAL card.
Union of the Mixpanel ... |
| `int_execution_gnosis_app_gpay_topups` | Intermediate | Gnosis App → Gnosis Pay top-ups.

A top-up = a Gnosis Pay "Crypto Deposit" into a GP wallet that is currently
GA-owne... |
| `int_execution_gnosis_app_gpay_txns` | Intermediate | Any USER-INITIATED Gnosis Pay card-wallet transaction (Payment = card spend,
Crypto Withdrawal, Fiat Off-ramp, Fiat T... |
| `int_execution_gnosis_app_gpay_wallets` | Intermediate | Gnosis Pay wallets (Safes) that have been or currently are controlled
by a Gnosis App user, via the Safe's Zodiac **D... |
| `int_execution_gnosis_app_gt_card_owner` | Intermediate | Reusable GP card (Safe) -> Gnosis App account bridge — the UNION of three on-chain signals gated to the envio_ga regi... |
| `int_execution_gnosis_app_gt_pay_wallets` | Intermediate | Guardian-module MEMBERSHIP (netted Enabled-Disabled). GA-ownership is GT-unavailable and stays on the heuristic. is_g... |
| `int_execution_gnosis_app_gt_user_activity` | Intermediate | Canonical per-identity ACTIVITY model (grain = registry UNION avatar). Records
every action signal — app-feature (swa... |
| `int_execution_gnosis_app_gt_user_dim` | Intermediate | Ground-truth registered-identity dimension (= dim_circles_identity, ~301k).
Registry LEFT JOIN avatar (active spine) ... |
| `int_execution_gnosis_app_gt_user_identity_bridge` | Intermediate | Internal registry address -> pseudonym bridge (shared CEREBRO_PII_SALT). INTERNAL. |
| `int_execution_gnosis_app_gt_user_reconciliation` | Intermediate | Aggregate-only reconciliation snapshot (public). registered (GT registry) vs active (heuristic) containment; cutover ... |
| `int_execution_gnosis_app_gt_wallet_metrics` | Intermediate | Per-wallet analytical rollup (one row per registry-or-avatar identity): lifecycle (tenure/recency/cohort), engagement... |
| `int_execution_gnosis_app_marketplace_offers` | Intermediate | Gnosis App marketplace offers — one row per non-excluded PaymentGateway
created via Circles v2 PaymentGatewayFactory.... |
| `int_execution_gnosis_app_marketplace_payments` | Intermediate | Gnosis App marketplace payments — one row per PaymentReceived event
from Circles v2 PaymentGatewayFactory that satisf... |
| `int_execution_gnosis_app_swap_fees_daily` | Intermediate | Daily aggregated CoW protocol fee revenue from Gnosis App swaps. `fee_usd` is derived from `fee_amount` (sold-token n... |
| `int_execution_gnosis_app_swap_fees_monthly` | Intermediate | Monthly rollup of swap_fees_daily. |
| `int_execution_gnosis_app_swap_fees_weekly` | Intermediate | Weekly rollup of swap_fees_daily. |
| `int_execution_gnosis_app_swaps` | Intermediate | Gnosis App swaps — one row per CoW order pre-signed by a GA user through
the Cometh ERC-4337 bundler. Matches the Dun... |
| `int_execution_gnosis_app_token_offer_claim_funnel_daily` | Intermediate | Daily per-offer token-offer claim conversion. Eligible-pool denominator is the rolling 30-day active GA users (proxy ... |
| `int_execution_gnosis_app_token_offer_claims` | Intermediate | Gnosis App token-offer claims — one row per `OfferClaimed` event emitted
by any ERC20TokenOfferCycle where the claim ... |
| `int_execution_gnosis_app_token_offers` | Intermediate | Gnosis App token-offer registry — one row per `NextOffer` instance emitted
by the Circles v2 ERC20TokenOfferCycle con... |
| `int_execution_gnosis_app_user_activity_daily` | Intermediate | Foundation table for all Gnosis App user-activity analytics — one row
per (date, address, activity_kind). Every downs... |
| `int_execution_gnosis_app_user_activity_daily_incl_gpay` | Intermediate | The composite Gnosis App activity feed (int_execution_gnosis_app_user_activity_daily)
EXTENDED with a `gpay_txn` acti... |
| `int_execution_gnosis_app_user_events` | Intermediate | Long-form heuristic event log for Gnosis App user identification.

Seven rules, all keyed off the same chokepoint: a ... |
| `int_execution_gnosis_app_user_identities` | Intermediate | Pseudonymization boundary for the Gnosis App sector.

Every address from the snapshot is hashed via pseudonymize_addr... |
| `int_execution_gnosis_app_user_identity_bridge` | Intermediate | INTERNAL ONLY — holds raw `address` and `user_pseudonym` together for
every known Gnosis App user. The only place in ... |
| `int_execution_gnosis_app_user_purchase_freq_30d` | Intermediate | Rolling 30-day per-user purchase-event count (swap_filled + marketplace_buy). Full rebuild on every run; size bounded... |
| `int_execution_gnosis_app_users_current` | Intermediate | Snapshot of the Gnosis App sector. One row per address that triggered
any heuristic, with derived confidence proxy `n... |
| `int_execution_gnosis_app_weekly_earners` | Intermediate | Weekly "economic earners" set for the WEAU metric, scoped to the Gnosis App: addresses that earned >= 1 gCRC cashback... |
| `int_execution_gnosis_app_weekly_signals` | Intermediate | Composite weekly activity for the Gnosis App WAU metric. UNION of Circles v2 active avatars (humans/trusts/mints), fi... |
| `int_execution_gnosis_app_weekly_signals_in_app` | Intermediate | IN-APP-ONLY weekly activity signal — companion to int_execution_gnosis_app_weekly_signals (the ecosystem-wide WAU fee... |
| `fct_execution_gnosis_app_activity_by_action_daily` | Fact | Daily activity counts, unique users, and USD by activity_kind. Feeds the Activity tab's stacked bar. |
| `fct_execution_gnosis_app_activity_by_action_monthly` | Fact | Monthly activity-by-action. |
| `fct_execution_gnosis_app_activity_by_action_weekly` | Fact | Weekly activity-by-action. |
| `fct_execution_gnosis_app_churn_monthly` | Fact | Monthly churn & retention segments. Two scopes — 'Any' (any non-onboard
activity) and 'Swap' (swap_signed/swap_filled... |
| `fct_execution_gnosis_app_gp_card_ga_link_daily` | Fact | Daily + cumulative count of Gnosis Pay cards LINKED to a Gnosis App account,
split by link_source. Backing fact for a... |
| `fct_execution_gnosis_app_gp_card_ga_volume_daily` | Fact | GA-LINKED Gnosis Pay funding & spend volume, daily, split by link_source. Module-agnostic,
correctly-timed successor ... |
| `fct_execution_gnosis_app_gpay_migration_daily` | Fact | Daily Gnosis Pay exploit -> Safe migration recovery time-series (June-2026 incident). One row per calendar date from ... |
| `fct_execution_gnosis_app_gpay_topups_by_token_daily` | Fact | Daily Gnosis App → Gnosis Pay top-up activity, derived from
int_execution_gnosis_app_gpay_topups (top-up = a GP "Cryp... |
| `fct_execution_gnosis_app_gpay_topups_cohort_monthly` | Fact | First-top-up cohort × subsequent-top-up retention.

Top-up definition is owned by int_execution_gnosis_app_gpay_topup... |
| `fct_execution_gnosis_app_gpay_topups_monthly` | Fact | Monthly top-up counts and USD volume (aggregated across tokens). Top-up = a GP Crypto Deposit into a currently-GA-own... |
| `fct_execution_gnosis_app_gpay_topups_weekly` | Fact | Weekly top-up counts and USD volume (aggregated across tokens). Top-up = a GP Crypto Deposit into a currently-GA-owne... |
| `fct_execution_gnosis_app_gpay_volume_daily` | Fact | Gnosis-App-scoped Gnosis Pay funding & spend volume, daily, split by
onboarding class. Backing fact table for api_exe... |
| `fct_execution_gnosis_app_gpay_wallets_daily` | Fact | Daily cumulative count of Gnosis Pay wallets controlled by a Gnosis App
user, split by onboarding class. Backing fact... |
| `fct_execution_gnosis_app_gt_active_wallets` | Fact | Active-wallet time-series (DAU/WAU/MAU) from real transaction_action.timestamp, scoped to app-engaged wallets. One ta... |
| `fct_execution_gnosis_app_gt_cashback_nft` | Fact | Gnosis Pay cashback NFT-mint program — daily mint series x status. A SEPARATE
family from gpay_cashback_* (gCRC trans... |
| `fct_execution_gnosis_app_gt_investments` | Fact | Metri auto-invest accounts by active flag (GT-only; no Gnosis Pay analogue). Owner-keyed. |
| `fct_execution_gnosis_app_gt_referrals` | Fact | Two DISTINCT referral metrics side by side: `earned` (GA-native paid-reward
ledger) and `full_invite_graph` (every ac... |
| `fct_execution_gnosis_app_gt_registrations_monthly` | Fact | New identity/profile REGISTRATIONS per month (avatar.created_at = account/profile creation; 100% of avatars have a pr... |
| `fct_execution_gnosis_app_gt_swaps_by_pair` | Fact | FILLED swaps by app_scope x token pair. gnosis_app = CURRENT Gnosis App,
metri = LEGACY Gnosis App (both roll up to G... |
| `fct_execution_gnosis_app_gt_swaps_summary` | Fact | Swap counts by app_scope x real CoW status enum. app_scope separates the Gnosis App VERSIONS sharing the Circles inde... |
| `fct_execution_gnosis_app_gt_user_identities_public` | Fact | PUBLIC identity boundary — pseudonym-only registry attributes. Join surface to mixpanel/gpay/circles (shared CEREBRO_... |
| `fct_execution_gnosis_app_gt_wallet_cohort_retention_monthly` | Fact | Acquisition-cohort retention: retained wallets / cohort size at month_index N after first activity. Denominator = coh... |
| `fct_execution_gnosis_app_gt_wallet_metrics_public` | Fact | PUBLIC per-wallet rollup — pseudonym-only mirror of int_execution_gnosis_app_gt_wallet_metrics (raw address dropped; ... |
| `fct_execution_gnosis_app_marketplace_buys_cumulative_daily` | Fact | Cumulative marketplace buys and distinct payers per offer, computed as
running window sums over a dense (offer × date... |
| `fct_execution_gnosis_app_marketplace_buys_daily` | Fact | Daily marketplace buys per offer, derived from
int_execution_gnosis_app_marketplace_payments. Grain (date, offer_name). |
| `fct_execution_gnosis_app_marketplace_offers_latest` | Fact | Latest per-offer totals — one row per curated offer with lifetime
n_buys, distinct payers, and first/last buy timesta... |
| `fct_execution_gnosis_app_retention_by_action_monthly` | Fact | Cohort retention split by activity_kind (swap_filled / swap_signed / topup /
marketplace_buy / token_offer_claim / ci... |
| `fct_execution_gnosis_app_retention_monthly` | Fact | Cohort retention grid for the Gnosis App onboard cohort.

Modeling assumptions:
  * cohort_month = month of the user'... |
| `fct_execution_gnosis_app_swaps_by_pair_daily` | Fact | Daily swap activity sliced by token pair (sold_symbol → bought_symbol).
pair is a pre-joined label for dashboard use;... |
| `fct_execution_gnosis_app_swaps_by_solver_daily` | Fact | Daily swap activity sliced by solver (filled trades only). |
| `fct_execution_gnosis_app_swaps_daily` | Fact | Daily Gnosis App swap activity, derived from int_execution_gnosis_app_swaps.
Backing fact for api_execution_gnosis_ap... |
| `fct_execution_gnosis_app_swaps_monthly` | Fact | Monthly swap counts and filled USD volume. |
| `fct_execution_gnosis_app_swaps_weekly` | Fact | Weekly swap counts and filled USD volume (bucket = ISO Mon-start). |
| `fct_execution_gnosis_app_token_offer_claims_by_offer_daily` | Fact | Daily token-offer claims sliced by specific offer (nextOffer address).
offer_token_symbol surfaces which token was so... |
| `fct_execution_gnosis_app_token_offer_claims_cohort_monthly` | Fact | First-claim cohort × subsequent-claim activity retention. cohort_month
= month of user's first token-offer claim. ret... |
| `fct_execution_gnosis_app_token_offer_claims_daily` | Fact | Daily Gnosis App token-offer claim activity, derived from
int_execution_gnosis_app_token_offer_claims. One row per da... |
| `fct_execution_gnosis_app_token_offer_claims_monthly` | Fact | Monthly token-offer claim activity. |
| `fct_execution_gnosis_app_token_offer_claims_weekly` | Fact | Weekly token-offer claim activity. |
| `fct_execution_gnosis_app_user_profile_latest` | Fact | Account-facing Gnosis App profile fact from production current-user and GPay wallet ownership models. |
| `fct_execution_gnosis_app_users_daily` | Fact | Daily user counts. new_users = distinct addresses whose first-ever
activity hit was on this date; active_users = dist... |
| `fct_execution_gnosis_app_users_daily_incl_gpay` | Fact | "Incl. Gnosis Pay" twin of fct_execution_gnosis_app_users_daily: identical New / Returning /
Reactivated / Active log... |
| `fct_execution_gnosis_app_users_distinct` | Fact | One row per Gnosis App on-chain user_pseudonym, with boolean flags
indicating which identification heuristic(s) fired... |
| `fct_execution_gnosis_app_users_monthly` | Fact | Monthly cohort of users. Returning = active this month AND previous month. Reactivated = active this month, inactive ... |
| `fct_execution_gnosis_app_users_monthly_incl_gpay` | Fact | "Incl. Gnosis Pay" twin of fct_execution_gnosis_app_users_monthly: identical New / Returning /
Reactivated / Active l... |
| `fct_execution_gnosis_app_users_weekly` | Fact | Weekly cohort of users (ISO Mon-start). Returning = active this week AND previous week. Reactivated = active this wee... |
| `fct_execution_gnosis_app_users_weekly_incl_gpay` | Fact | "Incl. Gnosis Pay" twin of fct_execution_gnosis_app_users_weekly — identical New/Returning/Reactivated/Active logic, ... |
| `fct_execution_gnosis_app_weekly_active_users_circles_ecosystem` | Fact | Circles-ecosystem weekly active reach — NOT a Gnosis App growth metric. Distinct addresses active that week across th... |
| `fct_execution_gnosis_app_weekly_economically_active_users` | Fact | Weekly Economically Active Users — intersection of the Gnosis-App-only (in-app) weekly active users and weekly Circle... |
| `api_execution_gnosis_app_active_users_incl_gpay_daily` | API | Gnosis App Daily Active Users (DAU), Gnosis-Pay-inclusive variant over fct_execution_gnosis_app_users_daily_incl_gpay... |
| `api_execution_gnosis_app_active_users_incl_gpay_monthly` | API | Gnosis App Monthly Active Users (MAU), Gnosis-Pay-inclusive variant over fct_execution_gnosis_app_users_monthly_incl_... |
| `api_execution_gnosis_app_active_users_incl_gpay_weekly` | API | Gnosis App Weekly Active Users (WAU), Gnosis-Pay-inclusive variant over fct_execution_gnosis_app_users_weekly_incl_gp... |
| `api_execution_gnosis_app_activity_by_action_daily` | API | FastAPI view over fct_execution_gnosis_app_activity_by_action_daily. Params: activity_kind, start_date, end_date. |
| `api_execution_gnosis_app_activity_by_action_monthly` | API | FastAPI view over fct_execution_gnosis_app_activity_by_action_monthly. |
| `api_execution_gnosis_app_activity_by_action_weekly` | API | FastAPI view over fct_execution_gnosis_app_activity_by_action_weekly. |
| `api_execution_gnosis_app_churn_monthly` | API | FastAPI view over fct_execution_gnosis_app_churn_monthly. Params: scope, start_month, end_month. |
| `api_execution_gnosis_app_circles_ecosystem_weekly_active_users` | API | Whole-Circles-network weekly active reach (NOT Gnosis App growth; that is api:gnosis_app_users weekly / api:gnosis_ap... |
| `api_execution_gnosis_app_gp_card_ga_link_daily` | API | Dashboard view of fct_execution_gnosis_app_gp_card_ga_link_daily: daily + cumulative
count of GA-linked Gnosis Pay ca... |
| `api_execution_gnosis_app_gp_card_ga_volume_daily` | API | Dashboard view of fct_execution_gnosis_app_gp_card_ga_volume_daily: GA-linked GP-card funding &
spend per day by link... |
| `api_execution_gnosis_app_gpay_topups_by_token_daily` | API | FastAPI endpoint view of fct_execution_gnosis_app_gpay_topups_by_token_daily.
Supports query params: token_bought_sym... |
| `api_execution_gnosis_app_gpay_topups_cohort_monthly` | API | FastAPI view over fct_execution_gnosis_app_gpay_topups_cohort_monthly. Params: start_month, end_month. |
| `api_execution_gnosis_app_gpay_topups_monthly` | API | FastAPI view over fct_execution_gnosis_app_gpay_topups_monthly. |
| `api_execution_gnosis_app_gpay_topups_weekly` | API | FastAPI view over fct_execution_gnosis_app_gpay_topups_weekly. |
| `api_execution_gnosis_app_gpay_volume_daily` | API | FastAPI endpoint view of fct_execution_gnosis_app_gpay_volume_daily.
GA-controlled Gnosis Pay funding (funded_volume_... |
| `api_execution_gnosis_app_gpay_wallets_daily` | API | FastAPI endpoint view of fct_execution_gnosis_app_gpay_wallets_daily.
Supports query params: onboarding_class, start_... |
| `api_execution_gnosis_app_gt_active_wallets` | API | Public DAU series (active app-engaged wallets per day). WAU/MAU in the underlying fct. |
| `api_execution_gnosis_app_gt_referrals` | API | Public referral metrics — earned ledger vs full invite graph. |
| `api_execution_gnosis_app_gt_swaps` | API | Public swap counts by scope x CoW status enum. |
| `api_execution_gnosis_app_gt_user_reconciliation` | API | Public reconciliation snapshot — registered (GT registry) vs active (heuristic) containment. |
| `api_execution_gnosis_app_gt_wallet_cohort_retention` | API | Public acquisition-cohort retention matrix (point-in-time; as_of_date). |
| `api_execution_gnosis_app_gt_wallet_metrics` | API | Public per-wallet metric endpoint (pseudonym-only; curated lifecycle/engagement/trust/segment surface). Point-in-time... |
| `api_execution_gnosis_app_kpi_churn_rate_latest` | API | KPI: latest-month 'Any'-scope churn rate. |
| `api_execution_gnosis_app_kpi_dau_latest` | API | KPI: DAU yesterday with pct change vs the day before. |
| `api_execution_gnosis_app_kpi_gp_wallets_imported` | API | KPI: cumulative GP wallets imported (pre-existing GP users who added GA). |
| `api_execution_gnosis_app_kpi_gp_wallets_latest` | API | KPI: count of GP wallets currently GA-owned. |
| `api_execution_gnosis_app_kpi_gp_wallets_onboarded` | API | KPI: cumulative GP wallets onboarded via Gnosis App. |
| `api_execution_gnosis_app_kpi_marketplace_buys_7d` | API | KPI: marketplace buys in the last 7 full days. |
| `api_execution_gnosis_app_kpi_marketplace_buys_total` | API | KPI: lifetime marketplace buys across all curated offers. |
| `api_execution_gnosis_app_kpi_marketplace_payers_7d` | API | KPI: distinct marketplace payers in the last 7 full days. |
| `api_execution_gnosis_app_kpi_mau_latest` | API | KPI: MAU for the latest complete month with pct change vs prior. |
| `api_execution_gnosis_app_kpi_new_users_7d` | API | KPI: new users in the last 7 full days with pct change vs prior 7d. |
| `api_execution_gnosis_app_kpi_repeat_purchase_rate_latest` | API | KPI: share of last-30d active users with ≥2 swap_filled or marketplace_buy events. |
| `api_execution_gnosis_app_kpi_retention_pct_latest` | API | KPI: latest-cohort M1 retention %. |
| `api_execution_gnosis_app_kpi_swap_fees_7d` | API | KPI: protocol fee revenue (USD) from filled swaps in last 7 full days with WoW pct change. |
| `api_execution_gnosis_app_kpi_swap_volume_7d` | API | KPI: filled-swap USD volume in the last 7 full days. |
| `api_execution_gnosis_app_kpi_swaps_7d` | API | KPI: signed swap count in the last 7 full days. |
| `api_execution_gnosis_app_kpi_token_offer_claimers_7d` | API | KPI: distinct token-offer claimers in the last 7 full days. |
| `api_execution_gnosis_app_kpi_token_offer_claims_7d` | API | KPI: token-offer claim count in the last 7 full days with pct change vs prior 7d. |
| `api_execution_gnosis_app_kpi_token_offer_volume_7d` | API | KPI: token-offer received-side USD volume in the last 7 full days. |
| `api_execution_gnosis_app_kpi_topup_volume_7d` | API | KPI: topup USD volume in the last 7 full days. |
| `api_execution_gnosis_app_kpi_topups_7d` | API | KPI: topup count in the last 7 full days. |
| `api_execution_gnosis_app_kpi_total_users` | API | KPI: total distinct GA users to date. Returns (value, change_pct). |
| `api_execution_gnosis_app_kpi_wau_latest` | API | KPI: WAU for the latest complete week with pct change vs prior. |
| `api_execution_gnosis_app_kpi_weekly_active_users_latest` | API | KPI: latest complete week's Gnosis App WAU (Lineage A, fct_execution_gnosis_app_users_weekly.active_users — same popu... |
| `api_execution_gnosis_app_kpi_weekly_economically_active_users_latest` | API | KPI: latest complete week's WEAU (non-blacklisted only) with WoW pct change. |
| `api_execution_gnosis_app_marketplace_buys_cumulative_daily` | API | FastAPI endpoint view of
fct_execution_gnosis_app_marketplace_buys_cumulative_daily. Supports
query params: offer_nam... |
| `api_execution_gnosis_app_marketplace_buys_daily` | API | FastAPI endpoint view of fct_execution_gnosis_app_marketplace_buys_daily.
Supports query params: offer_name, start_da... |
| `api_execution_gnosis_app_marketplace_offers_latest` | API | FastAPI endpoint view of fct_execution_gnosis_app_marketplace_offers_latest.
Supports query param: offer_name. |
| `api_execution_gnosis_app_purchase_freq_distribution_latest` | API | Distribution histogram of last-30d purchase counts per user (buckets 1/2/3/4-5/6-10/11+). |
| `api_execution_gnosis_app_retention_by_action_monthly` | API | FastAPI view over fct_execution_gnosis_app_retention_by_action_monthly. Params: activity_kind, start_month, end_month. |
| `api_execution_gnosis_app_retention_monthly` | API | FastAPI view over fct_execution_gnosis_app_retention_monthly. Params: start_month, end_month. |
| `api_execution_gnosis_app_swap_fees_daily` | API | Daily CoW protocol fee revenue from GA swaps (filled trades, pro-rated to USD). |
| `api_execution_gnosis_app_swap_fees_monthly` | API | Monthly rollup of swap_fees_daily. |
| `api_execution_gnosis_app_swap_fees_weekly` | API | Weekly rollup of swap_fees_daily. |
| `api_execution_gnosis_app_swaps_by_pair_daily` | API | FastAPI view over fct_execution_gnosis_app_swaps_by_pair_daily. Params: pair, start_date, end_date. |
| `api_execution_gnosis_app_swaps_by_solver_daily` | API | FastAPI view over fct_execution_gnosis_app_swaps_by_solver_daily. Params: solver, start_date, end_date. |
| `api_execution_gnosis_app_swaps_daily` | API | FastAPI endpoint view of fct_execution_gnosis_app_swaps_daily. Supports
query params: start_date, end_date. |
| `api_execution_gnosis_app_swaps_monthly` | API | FastAPI view over fct_execution_gnosis_app_swaps_monthly. |
| `api_execution_gnosis_app_swaps_weekly` | API | FastAPI view over fct_execution_gnosis_app_swaps_weekly. |
| `api_execution_gnosis_app_time_to_first_conversion_cohort_monthly` | API | Time from onboard to a user's FIRST event of each conversion kind, bucketed
by onboard-month cohort. Long format: one... |
| `api_execution_gnosis_app_token_offer_claim_funnel_daily` | API | Daily per-offer token-offer claim conversion (claims, claimers, USD received, claim_rate_pct). |
| `api_execution_gnosis_app_token_offer_claims_by_offer_daily` | API | FastAPI view over fct_execution_gnosis_app_token_offer_claims_by_offer_daily. Params: offer_address, cycle_address, o... |
| `api_execution_gnosis_app_token_offer_claims_cohort_monthly` | API | FastAPI view over fct_execution_gnosis_app_token_offer_claims_cohort_monthly. Params: start_month, end_month. |
| `api_execution_gnosis_app_token_offer_claims_daily` | API | FastAPI view over fct_execution_gnosis_app_token_offer_claims_daily. Params: start_date, end_date. |
| `api_execution_gnosis_app_token_offer_claims_monthly` | API | FastAPI view over fct_execution_gnosis_app_token_offer_claims_monthly. Params: start_date, end_date. |
| `api_execution_gnosis_app_token_offer_claims_weekly` | API | FastAPI view over fct_execution_gnosis_app_token_offer_claims_weekly. Params: start_date, end_date. |
| `api_execution_gnosis_app_user_activity_daily` | API | Account-facing Gnosis App activity view. |
| `api_execution_gnosis_app_user_profile_latest` | API | Account-facing Gnosis App profile view from production current-user models. |
| `api_execution_gnosis_app_users_daily` | API | FastAPI view over fct_execution_gnosis_app_users_daily. Params: start_date, end_date. |
| `api_execution_gnosis_app_users_monthly` | API | FastAPI view over fct_execution_gnosis_app_users_monthly. Params: start_month, end_month. |
| `api_execution_gnosis_app_users_weekly` | API | FastAPI view over fct_execution_gnosis_app_users_weekly. Params: start_date, end_date. |
| `api_execution_gnosis_app_weekly_active_users` | API | Gnosis App Weekly Active Users (WAU) time-series over fct_execution_gnosis_app_users_weekly.active_users (in-app acti... |
| `api_execution_gnosis_app_weekly_active_users_incl_gpay` | API | Gnosis App Weekly Active Users (WAU), Gnosis-Pay-inclusive variant of api_execution_gnosis_app_weekly_active_users: '... |
| `api_execution_gnosis_app_weekly_economically_active_users` | API | Time-series view over fct_execution_gnosis_app_weekly_economically_active_users (latest week excluded). |

**Gpay**

| Model | Layer | Description |
|-------|-------|-------------|
| `int_celo_gpay_activity` | Intermediate | Per-transfer classified Celo GP activity. Classification happens HERE,
not upstream in Dune — Dune only supplies raw ... |
| `int_celo_gpay_activity_daily` | Intermediate | Daily aggregation of int_celo_gpay_activity by Safe/action/token.
Incremental (insert_overwrite + apply_monthly_incre... |
| `int_celo_gpay_balances_daily` | Intermediate | Cumulative net-flow balance per Safe/token ((Top-up + Reversal) minus
(Payment + Withdrawal), running total since the... |
| `int_celo_gpay_safe_current_owners` | Intermediate | Current owner set per Safe, folded directly from
int_celo_gpay_wallet_events. Mirrors Gnosis Chain's
int_execution_sa... |
| `int_celo_gpay_wallet_events` | Intermediate | Thin pass-through of the unified, append-only wallet-lifecycle event
log (issued_at + add_owner + remove_owner) — see... |
| `int_celo_gpay_wallets` | Intermediate | Canonical Celo GP card Safe list, reconstructed from
int_celo_gpay_wallet_events (action='issued_at') rather than rea... |
| `int_execution_gpay_accounts_deployed` | Intermediate | True Gnosis Pay account universe, one row per deployed account. Unlike
int_execution_gpay_wallets (payment-gated), ac... |
| `int_execution_gpay_activity` | Intermediate | Incremental model that captures individual Gnosis Pay wallet transactions including payments, deposits, withdrawals, ... |
| `int_execution_gpay_activity_daily` | Intermediate | Incremental model that aggregates Gnosis Pay wallet activity at the daily level, grouped by wallet, action, direction... |
| `int_execution_gpay_allowances_current` | Intermediate | Current allowance state per Gnosis Pay Safe.

Replays SetAllowance events from int_execution_gpay_roles_events and
ke... |
| `int_execution_gpay_balances_daily` | Intermediate | Incremental model that tracks daily token balances for each Gnosis Pay wallet address, with both native and USD values. |
| `int_execution_gpay_balances_user_daily` | Intermediate | User-holdings view over int_execution_gpay_balances_daily that is
safe to aggregate across the June 2026 Safe migrati... |
| `int_execution_gpay_delay_activity_daily` | Intermediate | Daily count of TransactionAdded events per GP Safe — the
privacy-respecting "user did something admin-y today" signal... |
| `int_execution_gpay_delay_events` | Intermediate | Decoded events emitted by the Zodiac Delay Module proxies attached to
GP Safes. Includes:

  DelaySetup       — modul... |
| `int_execution_gpay_refunds` | Intermediate | Exploit-recovery refunds credited to migrated NEW Safes by the
distributor wallets in the gpay_refund_distributors se... |
| `int_execution_gpay_roles_events` | Intermediate | Decoded events from the Zodiac Roles v2 module proxies attached to GP
Safes. Includes the events Gnosis Pay actually ... |
| `int_execution_gpay_safe_canonical` | Intermediate | Canonical resolution for the June 2026 post-exploit Safe migration
(gp_migrated_safes seed). One row per OLD Safe wit... |
| `int_execution_gpay_safe_identities` | Intermediate | PURPOSE
-------
This model is the privacy boundary for the Gnosis Pay ↔ Mixpanel
bridge. It produces a lookup table f... |
| `int_execution_gpay_safe_modules` | Intermediate | Current module topology per Gnosis Pay Safe.

Replays int_execution_safes_module_events filtered to GP Safes, keeps
t... |
| `int_execution_gpay_safe_switchover` | Intermediate | One row per June 2026 migrated pair. Refunded (is_lost) pairs are
excluded from user holdings from first_refund_at (t... |
| `int_execution_gpay_spend_activity_daily` | Intermediate | Daily card-spend activity per GP Safe.

Source: int_execution_gpay_spender_events filtered to event_name='Spend'.
The... |
| `int_execution_gpay_spender_delegates_current` | Intermediate | Current spender-delegate set per Gnosis Pay Safe.

Replays AssignRoles events from int_execution_gpay_roles_events wi... |
| `int_execution_gpay_spender_events` | Intermediate | Decoded events from the Gnosis Pay Spender module proxies attached to
GP Safes. The Spender is GP's custom final gate... |
| `int_execution_gpay_user_identity_bridge` | Intermediate | INTERNAL ONLY — GP-side analogue of `int_execution_gnosis_app_user_identity_bridge`.
Holds raw GP addresses (Safe con... |
| `int_execution_gpay_wallet_owners` | Intermediate | Current owner snapshot for Gnosis Pay Safes. Thin filter over int_execution_safes_current_owners (the generic Safe ow... |
| `int_execution_gpay_wallets` | Intermediate | Gnosis Pay Safes derived from on-chain events. A Safe qualifies if it
has emitted SafeSetup (so it exists on-chain) A... |
| `fct_execution_gpay_actions_by_token_daily` | Fact | Daily aggregation of Gnosis Pay activity metrics broken down by action type and token, with cumulative totals. |
| `fct_execution_gpay_actions_by_token_monthly` | Fact | Monthly aggregation of Gnosis Pay activity metrics broken down by action type and token, with cumulative totals. |
| `fct_execution_gpay_actions_by_token_weekly` | Fact | Weekly aggregation of Gnosis Pay activity metrics broken down by action type and token, with cumulative totals. |
| `fct_execution_gpay_activity_daily` | Fact | Daily summary of Gnosis Pay ecosystem activity including active users, payments, volume, and funded wallet counts. |
| `fct_execution_gpay_activity_monthly` | Fact | Monthly summary of Gnosis Pay ecosystem activity including active users, payments, volume, and funded wallet counts. |
| `fct_execution_gpay_activity_weekly` | Fact | Weekly summary of Gnosis Pay ecosystem activity including active users, payments, volume, and funded wallet counts. N... |
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
| `fct_execution_gpay_user_balances_latest` | Fact | Latest Gnosis Pay wallet balances by token for portfolio lookups.
User-holdings semantics: reads int_execution_gpay_b... |
| `fct_execution_gpay_user_lifetime_metrics` | Fact | Lifetime metrics for each Gnosis Pay wallet, including tenure, activity counts, payment volumes, and cashback totals. |
| `fct_execution_gpay_users_distinct` | Fact | Deduplicated Gnosis Pay user projection for the semantic layer's cross-sector user-overlap path. One row per user_pse... |
| `api_execution_gpay_accounts_daily` | API | Daily time series of the cumulative number of deployed Gnosis Pay accounts. |
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
| `api_execution_gpay_total_accounts` | API | All-time total count of deployed Gnosis Pay accounts (Safes that enabled a Gnosis Pay Zodiac module - Delay / Roles /... |
| `api_execution_gpay_total_balance` | API | Current total balance across all Gnosis Pay wallets in USD. |
| `api_execution_gpay_total_funded` | API | All-time total count of funded Gnosis Pay wallets (users who made at least one payment). |
| `api_execution_gpay_total_payments` | API | All-time total count of Gnosis Pay payments. |
| `api_execution_gpay_total_volume` | API | All-time total payment volume for Gnosis Pay in USD. |
| `api_execution_gpay_user_activity` | API | Individual transaction-level activity for a specific Gnosis Pay user, filtered by wallet address. |
| `api_execution_gpay_user_balances_daily` | API | Daily token balances for a specific Gnosis Pay user in native and USD values. |
| `api_execution_gpay_user_balances_latest` | API | Simple API view over latest Gnosis Pay wallet balances. |
| `api_execution_gpay_user_cashback_daily` | API | Daily cashback amounts for a specific Gnosis Pay user. |
| `api_execution_gpay_user_lifetime_metrics` | API | Lifetime metrics for a specific Gnosis Pay user, passing through all columns from the fact model. |
| `api_execution_gpay_user_payments_daily` | API | Daily payment amounts by token for a specific Gnosis Pay user. |
| `api_execution_gpay_user_top_wallets` | API | API view of the top 50 Gnosis Pay wallets by lifetime payment volume. One row per wallet_address, selected from fct_e... |
| `api_execution_gpay_user_total_cashback` | API | All-time total cashback for a specific Gnosis Pay user. |
| `api_execution_gpay_user_total_payments` | API | All-time total payment count for a specific Gnosis Pay user. |
| `api_execution_gpay_user_total_volume` | API | All-time total payment volume for a specific Gnosis Pay user. |
| `api_execution_gpay_volume_7d` | API | 7-day payment volume with period-over-period change percentage. |
| `api_execution_gpay_volume_payments_by_token_daily` | API | Daily payment volume by token in USD for Gnosis Pay. |
| `api_execution_gpay_volume_payments_by_token_monthly` | API | Monthly payment volume by token in USD for Gnosis Pay. |
| `api_execution_gpay_volume_payments_by_token_weekly` | API | Weekly payment volume by token in USD for Gnosis Pay. |
| `api_execution_gpay_wallet_balance_composition` | API | Current balance composition of a Gnosis Pay wallet by token. |

**Guardian**

| Model | Layer | Description |
|-------|-------|-------------|
| `stg_envio_ga__guardian_module` | Staging | Append-only module Enabled/Disabled events (grain = event id). INTERNAL. |

**Interactions**

| Model | Layer | Description |
|-------|-------|-------------|
| `stg_cow__interactions` | Staging | Staging view of Interaction events from GPv2Settlement. Each row is one external contract call (AMM swap, approval, e... |

**Investment**

| Model | Layer | Description |
|-------|-------|-------------|
| `stg_envio_ga__investment_accounts` | Staging | Metri auto-invest accounts (grain = account address). INTERNAL. |

**Known**

| Model | Layer | Description |
|-------|-------|-------------|
| `fct_ubo_known_containers_daily` | Fact | Distinct (date, container_address, token_address) tuples for which we have UBO-level supply claims. Derived directly ... |

**Lending**

| Model | Layer | Description |
|-------|-------|-------------|
| `int_execution_lending_aave_balance_cohorts_daily` | Intermediate | Daily lender balance cohort distributions per (protocol, reserve) across Aave V3 and SparkLend on Gnosis. Buckets use... |
| `int_execution_lending_aave_daily` | Intermediate | Daily lending metrics per (protocol, reserve) on Gnosis Chain, covering both Aave V3 and SparkLend. Includes supply/b... |
| `int_execution_lending_aave_diffs_daily` | Intermediate | Daily per-user scaled balance deltas for Gnosis lending markets (Aave V3
and SparkLend). Computes scaled deltas from ... |
| `int_execution_lending_aave_user_balances_daily` | Intermediate | Daily per-user aToken balances across Gnosis lending markets (Aave V3 and
SparkLend). Reads scaled deltas from int_ex... |
| `int_execution_lending_aave_utilization_daily` | Intermediate | Daily utilization rate per (protocol, reserve) across Aave V3 and SparkLend.
Computes cumulative scaled supply/borrow... |
| `fct_execution_lending_latest` | Fact | Lender / borrower counts per (window, protocol, token) plus protocol-scoped
'ALL'-tokens rows and an all-protocols 'A... |
| `fct_execution_lending_weekly` | Fact | Weekly fact aggregating lending activity per (week, protocol, token) across
Aave V3 and SparkLend on Gnosis. Built fr... |
| `api_execution_lending_activity_counts_weekly` | API | Weekly lender/borrower distinct user counts pivoted into long format for
stacked-bar activity charts. One row per (we... |
| `api_execution_lending_activity_volumes_weekly` | API | Weekly deposit/borrow volumes pivoted into long format for stacked-bar
volume charts. One row per (week, token, proto... |
| `api_execution_lending_balance_cohorts_holders_daily` | API | Daily lender count by balance cohort per (protocol, token) across Aave V3 and SparkLend. Stacked bar chart data showi... |
| `api_execution_lending_balance_cohorts_value_daily` | API | Daily lender balance cohort values per (protocol, token) across Aave V3 and SparkLend. Stacked bar chart data showing... |
| `api_execution_lending_borrowers_count_7d` | API | KPI view of recently-active borrowers on Gnosis (Aave V3, SparkLend).
IMPORTANT — this is a 7-day FLOW, not a stock: ... |
| `api_execution_lending_daily` | API | Long-format daily APY series per (token, protocol) across Aave V3 and
SparkLend. Each row pivots into one of two apy_... |
| `api_execution_lending_lenders_count_7d` | API | KPI view of currently-active lenders on Gnosis (Aave V3, SparkLend).
"Active lenders" is a STOCK measure — unique wal... |
| `api_execution_lending_tvl_by_token_latest` | API | Latest lending TVL per reserve token on Gnosis (aggregated across Aave V3 and SparkLend) for pie chart display. Each ... |

**Live**

| Model | Layer | Description |
|-------|-------|-------------|
| `api_execution_live_trades` | API | Dashboard-facing feed of recent DEX trades on Gnosis Chain. Reads from the cached `int_live__dex_trades_raw` table, s... |
| `api_execution_live_trades_freshness` | API | One-row freshness indicator for the live-trades tab. Shows the newest ingested block timestamp in `execution_live.log... |
| `api_execution_live_trades_hourly_48h` | API | Hourly USD volume over the live window (up to 48h), stacked by protocol. Feeds the "last 48h volume" chart on the Liv... |
| `api_execution_live_trades_stats` | API | One-row summary for the live-trades tab header tiles. Counts trades, sums USD volume, counts unique traders, and comp... |

**Modules**

| Model | Layer | Description |
|-------|-------|-------------|
| `contracts_gpay_modules_registry` | CONTRACTS | Cross-referenced registry of every Zodiac module proxy that is currently
or was ever enabled on a Gnosis Pay Safe.

T... |
| `contracts_zodiac_modules_registry` | CONTRACTS | ABI-resolution registry for Zodiac Modifier proxies (Delay + Roles) on
Gnosis Chain, chain-wide (NOT GP-scoped).

Mir... |

**Network**

| Model | Layer | Description |
|-------|-------|-------------|
| `fct_execution_network_retention_monthly` | Fact | Per-cohort monthly network retention. A cohort is the set of addresses
whose first successful transaction landed in a... |

**Ocsdai**

| Model | Layer | Description |
|-------|-------|-------------|
| `int_yields_ocsdai_share_price_daily` | Intermediate | Daily share price (sDAI per OC-sDAI share) for the OpenCover OC-sDAI vault
("Covered Savings xDAI", 0x0ac34fe133bde3a... |

**Pay**

| Model | Layer | Description |
|-------|-------|-------------|
| `stg_envio_ga__pay_topups` | Staging | STRETCH — distinct (card, funder) pairs for app-initiated top-ups (PayTopUp / AutoTopup) from ONE full scan of envio_... |

**Pools**

| Model | Layer | Description |
|-------|-------|-------------|
| `int_execution_pools_balancer_v2_daily` | Intermediate | Daily Balancer V2 pool token balances with oracle price enrichment. Built from delta events (PoolBalanceChanged, Swap... |
| `int_execution_pools_balancer_v3_daily` | Intermediate | Daily Balancer V3 pool token balances with oracle price enrichment.
Built from delta events (LiquidityAdded, Liquidit... |
| `int_execution_pools_balances_daily` | Intermediate | Combined daily pool token balances across all DEX protocols. Thin UNION ALL of the four protocol-level models (Uniswa... |
| `int_execution_pools_dex_liquidity_events` | Intermediate | Individual LP add/remove/collect events across all protocols on Gnosis Chain. One row per (event, token) — not pivote... |
| `int_execution_pools_dex_trades` | Intermediate | DEX swap events enriched with USD prices and transaction context. Source of truth for trade-level analytics with USD ... |
| `int_execution_pools_dex_trades_raw` | Intermediate | Raw DEX swap events across all protocols on Gnosis Chain. One row per swap with token metadata (symbol, decimals, hum... |
| `int_execution_pools_dex_trades_tx_context` | Intermediate | Thin lookup mapping swap transaction hashes to sender (tx_from) and recipient (tx_to). Only contains transactions tha... |
| `int_execution_pools_fees_daily` | Intermediate | Daily accrued pool fees and trading volume at pool x token grain for Uniswap V3,
Swapr V3, and Balancer V3 pools, com... |
| `int_execution_pools_il_swap_flows_daily` | Intermediate | Daily pool-level base data for LVR computation. Combines swap flows (signed int256 token amounts), fees, TVL, and per... |
| `int_execution_pools_lps_daily` | Intermediate | Daily LP provider activity from Mint and Burn events on Uniswap V3 and Swapr V3 pools. Tracks event counts, daily uni... |
| `int_execution_pools_metrics_daily` | Intermediate | Pool-level daily metrics: TVL, fees, volume, swap count, and 7D trailing fee APR. Aggregates token-level TVL from the... |
| `int_execution_pools_swapr_v3_daily` | Intermediate | Daily Swapr V3 pool token balances with oracle price enrichment.
Built from event deltas (Mint, Burn, Swap, Collect, ... |
| `int_execution_pools_uniswap_v3_daily` | Intermediate | Daily Uniswap V3 pool token balances with oracle price enrichment. Built from event deltas (Mint, Burn, Swap, Collect... |
| `fct_execution_pools_daily` | Fact | Daily pool-level metrics for top Uniswap V3, Swapr V3, and Balancer V3 pools on
Gnosis Chain, including TVL (USD), ac... |
| `fct_execution_pools_il_daily` | Fact | Pool-level Loss Versus Rebalancing (LVR) from actual swap flows. LVR measures the cost LPs pay to arbitrageurs — the ... |
| `fct_execution_pools_lps_latest` | Fact | Unique LP provider counts per token over rolling time windows with change_pct vs prior window. Mirrors the lending pa... |
| `fct_execution_pools_snapshots` | Fact | Snapshot KPI table for pool yields. Each row is a (token, metric) pair with the latest value and 7-day percentage cha... |
| `fct_execution_pools_tvl_token_daily` | Fact | Per-token TVL composition within pools with server-side denomination. Three TVL columns are pre-computed: tvl_usd (co... |
| `api_execution_pools_fee_apr_7d_daily` | API | API view for fee APR (7D trailing) time series by token and pool label (Uniswap V3/Swapr V3 only). Uses accrued fees ... |
| `api_execution_pools_fees_7d` | API | Per-token total LP fees over the last 7 days (snapshot) with 7-day-prior change. Sourced from fct_execution_pools_sna... |
| `api_execution_pools_fees_usd_daily` | API | API view for daily fee revenue (USD) by token and pool, sourced from fct_execution_pools_daily. |
| `api_execution_pools_lp_activity_daily` | API | API view for daily LP activity (Mint/Burn event counts) per pool per token, unpivoted into one row per event type for... |
| `api_execution_pools_lps_count_7d` | API | API view for unique LP provider count over the last 7 days per token. |
| `api_execution_pools_net_apr_daily` | API | API view for net APR (fee APR plus LVR) time series by token and pool label, with fee APR and LVR components. |
| `api_execution_pools_swap_count_daily` | API | API view for daily swap event count by token and pool, sourced from fct_execution_pools_daily. |
| `api_execution_pools_tvl_by_pool_latest` | API | Latest-day TVL breakdown per (token, pool) for the pools dashboard's
drill-down chart. One row per pool with positive... |
| `api_execution_pools_tvl_daily` | API | API view for pool TVL (USD) time series by token and pool label. |
| `api_execution_pools_tvl_latest` | API | Latest TVL snapshot per token across all tracked DEX pools with 7-day change. Sourced from fct_execution_pools_snapsh... |
| `api_execution_pools_tvl_token_daily` | API | Daily TVL time series per (token, pool) decomposed into the contribution
of each pool side. Sourced from fct_executio... |
| `api_execution_pools_volume_7d` | API | API view for 7-day total trading volume per token (snapshot from fct_execution_pools_snapshots). |
| `api_execution_pools_volume_daily` | API | API view for daily trading volume (USD) by token and pool, sourced from fct_execution_pools_daily. |

**Prices**

| Model | Layer | Description |
|-------|-------|-------------|
| `int_execution_prices_dex_ratios` | Intermediate | Daily DEX-derived USD prices for whitelist tokens that have no Gnosis Chainlink feed (GBPe, BRLA, BRZ, COW, SAFE). Me... |
| `int_execution_prices_native_daily` | Intermediate | Native daily USD price series for whitelist base tokens, assembled from on-chain data to replace the Dune feed: Chain... |
| `int_execution_prices_oracle_daily` | Intermediate | Daily native USD prices derived from Chainlink on-chain oracle feeds (AnswerUpdated events) for whitelisted tokens. O... |

**Profiles**

| Model | Layer | Description |
|-------|-------|-------------|
| `stg_envio_ga__profiles` | Staging | Circles profile per identity (dedup required — version-superseding dup ids). INTERNAL. |

**Registry**

| Model | Layer | Description |
|-------|-------|-------------|
| `contracts_safe_registry` | CONTRACTS | Registry consumed by decode_logs(contract_address_ref=ref('contracts_safe_registry')).
Maps each Safe proxy → the sin... |

**Rwa**

| Model | Layer | Description |
|-------|-------|-------------|
| `int_execution_rwa_backedfi_prices` | Intermediate | The model aggregates daily closing prices for various backed financial instruments from Oracle event data, supporting... |
| `fct_execution_rwa_backedfi_prices_daily` | Fact | The fct_execution_rwa_backedfi_prices_daily view consolidates daily price data for various backed finance instruments... |
| `api_execution_rwa_backedfi_prices_daily` | API | The api_execution_rwa_backedfi_prices_daily model provides daily pricing data for RWA-backed financial instruments to... |

**Safe**

| Model | Layer | Description |
|-------|-------|-------------|
| `fct_execution_safe_owner_pseudonyms` | Fact | Chain-wide Safe → owner pseudonym bridge. One row per current
(safe_address, owner) pair, hashed into the project-wid... |
| `api_execution_safe_details_latest` | API | One row per Safe contract with deployment metadata + current-owner-count
+ current-threshold. Powers the Safe-section... |

**Safes**

| Model | Layer | Description |
|-------|-------|-------------|
| `int_execution_safes` | Intermediate | Gnosis Safe deployments on Gnosis Chain.

A Safe is deployed by the SafeProxyFactory as a minimal proxy that
delegate... |
| `int_execution_safes_current_owners` | Intermediate | Current owner set per Safe.

For each (safe_address, owner) pair, take the latest event by
(block_number, log_index).... |
| `int_execution_safes_module_events` | Intermediate | Long-form log of module-state and guard-state mutations on every Safe
in contracts_safe_registry.

event_kind ∈ (enab... |
| `int_execution_safes_module_events_v2` | Intermediate | Validation copy of int_execution_safes_module_events that uses the
decode_logs event_name_filter (topic0 pre-filter) ... |
| `int_execution_safes_owner_events` | Intermediate | Long-form ownership-event log for every Safe in contracts_safe_registry.

All ABI decoding is delegated to decode_log... |
| `api_execution_safes_current_owners` | API | Per-Safe owner list (add-only snapshot). One row per (safe, owner) pair
where the last observed event for that pair i... |

**Savings**

| Model | Layer | Description |
|-------|-------|-------------|
| `int_yields_savings_xdai_rate_daily` | Intermediate | Canonical daily Savings xDAI vault rate for the Gnosis Savings xDAI vault
(0xaf204776c7245bF4147c2612BF6e5972Ee483701... |
| `fct_yields_savings_xdai_apy_daily` | Fact | Canonical Savings xDAI APY mart. Long-format output with one row per
(date, label) where label ∈ {'Daily','7DMA','30D... |

**Sdai**

| Model | Layer | Description |
|-------|-------|-------------|
| `int_yields_sdai_rate_daily` | Intermediate | Legacy compatibility wrapper over int_yields_savings_xdai_rate_daily.
Preserves the historical (date, sdai_conversion... |
| `fct_yields_sdai_apy_daily` | Fact | Legacy compatibility wrapper over fct_yields_savings_xdai_apy_daily.
Preserves the historical (date, apy, label) shap... |

**Second**

| Model | Layer | Description |
|-------|-------|-------------|
| `int_ubo_second_level_daily` | Intermediate | Rows from fct_ubo_supply_claims_daily where ubo_address is itself a known container for the bridge token (container_a... |

**Settlements**

| Model | Layer | Description |
|-------|-------|-------------|
| `stg_cow__settlements` | Staging | Staging view of Settlement events from GPv2Settlement. One row per batch settlement, linking transaction_hash to the ... |

**Solvers**

| Model | Layer | Description |
|-------|-------|-------------|
| `stg_cow__solvers` | Staging | Staging view of SolverAdded and SolverRemoved events from the GPv2AllowListAuthentication contract. Used to build the... |

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

**Supply**

| Model | Layer | Description |
|-------|-------|-------------|
| `fct_ubo_supply_claims_daily` | Fact | THE reusable UBO supply-claims surface. One row per (date, protocol, container_address, ubo_address) — for each conta... |
| `fct_ubo_supply_claims_resolved_daily` | Fact | One-pass second-level-container resolution over fct_ubo_supply_claims_daily. Identical schema and unique key. For any... |

**Swapr**

| Model | Layer | Description |
|-------|-------|-------------|
| `stg_pools__swapr_v3_events` | Staging | Normalized event deltas for Swapr V3 (Algebra) pools. Same structure as stg_pools__uniswap_v3_events. |

**Swaps**

| Model | Layer | Description |
|-------|-------|-------------|
| `stg_envio_ga__swaps` | Staging | CoW order records (grain = order id). No fill timestamp; status is a real enum. INTERNAL. |

**Token**

| Model | Layer | Description |
|-------|-------|-------------|
| `int_execution_token_prices_daily` | Intermediate | The `int_execution_token_prices_daily` view consolidates daily price data for various tokens and stablecoins used in ... |

**Tokens**

| Model | Layer | Description |
|-------|-------|-------------|
| `stg_pools__tokens_meta` | Staging | Normalized token metadata from the tokens_whitelist seed. Provides lowercase address, uppercase symbol (nullable via ... |
| `int_execution_tokens_address_diffs_daily` | Intermediate | This model calculates daily net address-level token transfer deltas, capturing inflows and outflows for each address ... |
| `int_execution_tokens_balance_cohorts_daily` | Intermediate | Daily token balance cohort distributions, segmenting holders into balance buckets. |
| `int_execution_tokens_balances_by_sector_daily` | Intermediate | Daily balances aggregated by sector labels for each token. |
| `int_execution_tokens_balances_daily` | Intermediate | Daily token balances per address with USD valuation. Reads native balances from int_execution_tokens_balances_native_... |
| `int_execution_tokens_balances_native_daily` | Intermediate | Daily cumulative native-token balances per address. Holds the heavy running-sum compute; does not include USD pricing... |
| `int_execution_tokens_supply_holders_daily` | Intermediate | Daily supply and holder counts aggregated by token. |
| `int_execution_tokens_transfers_daily` | Intermediate | The int_execution_tokens_transfers_daily model aggregates daily transfer metrics for tokens, providing insights into ... |
| `fct_execution_tokens_metrics_daily` | Fact | Daily per-token fact joining supply/holders (from
int_execution_tokens_supply_holders_daily), transfer volume/counts/... |
| `fct_execution_tokens_overview_by_class_latest` | Fact | Token-class-level overview KPIs (supply_total, holders_total) on the
latest available date with 7-day change percent.... |
| `fct_execution_tokens_supply_by_sector_latest` | Fact | Latest-day supply breakdown per (token_class, sector). Sector classification
comes from int_execution_tokens_balances... |
| `fct_execution_tokens_supply_distribution_latest` | Fact | Latest-day supply distribution per (token_class, token symbol). Each row
is a token's share within its class. Sourced... |
| `fct_execution_tokens_top_holders_latest` | Fact | Latest-day snapshot of token holders ranked by USD balance, with concentration metrics (pct_of_total, cumulative_pct)... |
| `fct_execution_tokens_top_holders_ranked` | Fact | Latest-day snapshot of top-500 token holders per token ranked by USD balance. Combines int_execution_tokens_balances_... |
| `fct_execution_tokens_ubo_coverage_latest` | Fact | Per-token diagnostic of how much of the supply has been resolved to a real end-holder (UBO) versus still sitting in a... |
| `fct_execution_tokens_ubo_venue_breakdown_latest` | Fact | Latest-snapshot split of each token's positive-balance supply across UBO venues. One row per (token_address, venue): ... |
| `api_execution_tokens_active_senders_daily` | API | This view provides daily counts of active senders per API token, enabling analysis of token engagement over time. |
| `api_execution_tokens_balance_cohorts_holders_daily` | API | This view provides daily snapshots of token balance cohort distributions among holders, enabling analysis of holder s... |
| `api_execution_tokens_balance_cohorts_value_daily` | API | This view aggregates daily token balance cohort values, segmented by balance buckets, to support analysis of token ho... |
| `api_execution_tokens_balances_daily` | API | Daily per-wallet token balance feed for downstream API consumers.
Sourced from int_execution_tokens_balances_daily. T... |
| `api_execution_tokens_holders_daily` | API | The api_execution_tokens_holders_daily model provides daily aggregated data on the number of unique token holders for... |
| `api_execution_tokens_holders_latest_by_token` | API | This model provides the latest snapshot of the number of holders for each API token, aggregated by token symbol, to s... |
| `api_execution_tokens_overview_latest` | API | Thin API view over fct_execution_tokens_overview_by_class_latest — supply/holders KPI cards per token class with 7-da... |
| `api_execution_tokens_supply_by_sector_latest` | API | Thin API view over fct_execution_tokens_supply_by_sector_latest — supply distribution by holder sector for the latest... |
| `api_execution_tokens_supply_daily` | API | The api_execution_tokens_supply_daily model provides daily aggregated data on the supply of different API tokens, sup... |
| `api_execution_tokens_supply_distribution_latest` | API | Thin API view over fct_execution_tokens_supply_distribution_latest — per-token share of supply within token class on ... |
| `api_execution_tokens_supply_latest_by_token` | API | This model provides the latest supply values for each API token based on daily recorded data, enabling tracking of to... |
| `api_execution_tokens_top_holders_latest` | API | Thin API view over fct_execution_tokens_top_holders_latest. Returns all holders ranked by balance, with concentration... |
| `api_execution_tokens_ubo_coverage_latest` | API | Thin API view over fct_execution_tokens_ubo_coverage_latest. |
| `api_execution_tokens_ubo_venue_breakdown_latest` | API | Thin API view over fct_execution_tokens_ubo_venue_breakdown_latest. One row per (token_address, venue), ordered by to... |
| `api_execution_tokens_volume_daily` | API | The api_execution_tokens_volume_daily model provides daily aggregated data on the trading volume of different tokens ... |

**Trades**

| Model | Layer | Description |
|-------|-------|-------------|
| `stg_cow__trades` | Staging | Staging view decoding CoW Protocol Trade events from the GPv2Settlement contract. Each row is one trade fill: token p... |
| `int_execution_trades_by_tx` | Intermediate | Transaction-grain collapse of `int_execution_pools_dex_trades` — one row per (date, transaction_hash). Runs the expen... |
| `fct_execution_trades_by_aggregator_daily` | Fact | Daily per-aggregator share of trades. Reads from `int_execution_trades_by_tx` (tx grain). share_pct is pre-computed s... |
| `fct_execution_trades_by_protocol_daily` | Fact | Daily per-protocol DEX activity. Aggregated from `int_execution_pools_dex_trades` at the swap (hop) grain — so multi-... |
| `fct_execution_trades_by_token_daily` | Fact | Daily per-token DEX activity. Each swap contributes to BOTH its sold and bought side, so `combined_usd` across all to... |
| `fct_execution_trades_lifetime` | Fact | One-row lifetime summary of DEX trading on Gnosis Chain. Materialized as a table, full rebuild on every dbt run. Feed... |
| `api_execution_trades_stats_aggregator_share_ts` | API | Dashboard view — daily aggregator share. Pure SELECT from fct_execution_trades_by_aggregator_daily. Each date's value... |
| `api_execution_trades_stats_hop_distribution` | API | Dashboard view — hop-count distribution per time window. Percentages are computed within each window (1m/3m/6m/1y) of... |
| `api_execution_trades_stats_lifetime` | API | Dashboard view — lifetime scalar totals. Pure SELECT from fct_execution_trades_lifetime. |
| `api_execution_trades_stats_net_flow` | API | Dashboard view — top 10 tokens by absolute net USD flow per time window (1m/3m/6m/1y), ranked independently within ea... |
| `api_execution_trades_stats_size_distribution` | API | Dashboard view — trade-size distribution per time window. Percentages are computed within each window (1m/3m/6m/1y) o... |
| `api_execution_trades_stats_top_tokens_weekly` | API | Dashboard view — weekly top-8 token activity + Other. Aggregates from fct_execution_trades_by_token_daily to the week... |
| `api_execution_trades_stats_traders_weekly` | API | Dashboard view — weekly unique traders. Distinct `tx_from` per week (Monday start, UTC) from `int_execution_trades_by... |
| `api_execution_trades_stats_trades_ts` | API | Dashboard view — daily protocol swap counts. Pure SELECT from fct_execution_trades_by_protocol_daily. |
| `api_execution_trades_stats_volume_ts` | API | Dashboard view — daily protocol volume. Pure SELECT from fct_execution_trades_by_protocol_daily. |

**Transaction**

| Model | Layer | Description |
|-------|-------|-------------|
| `stg_envio_ga__transaction_actions` | Staging | STRETCH — per-identity first/last action timestamp + count from ONE full scan of envio_ga.transaction_action (208M, n... |

**Transactions**

| Model | Layer | Description |
|-------|-------|-------------|
| `int_execution_transactions_by_project_alltime_state` | Intermediate | This model aggregates execution transaction data by project and month, providing insights into transaction volume, fe... |
| `int_execution_transactions_by_project_daily` | Intermediate | This model aggregates daily execution transaction data by project, providing insights into transaction volume, user e... |
| `int_execution_transactions_by_project_hourly_recent` | Intermediate | This model aggregates hourly execution transaction data by project for the recent two-day period, providing insights ... |
| `int_execution_transactions_cumulative_daily` | Intermediate | Daily time series of new and cumulative unique active accounts. Derived from the unique addresses table, provides exa... |
| `int_execution_transactions_daily_active_addresses` | Intermediate | Daily active address hashes — one row per unique sender address per active day. Used for memory-efficient windowed ac... |
| `int_execution_transactions_info_daily` | Intermediate | The `int_execution_transactions_info_daily` model aggregates daily transaction data from the execution layer, providi... |
| `int_execution_transactions_unique_addresses` | Intermediate | Incremental table of every unique transaction sender address hash with the date it was first seen. Used to compute ex... |
| `fct_execution_transactions_active_accounts_daily` | Fact | Daily unique active accounts (transaction initiators) on Gnosis Chain, using bitmap merge across all projects for acc... |
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
| `api_execution_transactions_active_accounts_daily` | API | Daily unique initiator accounts on Gnosis Chain. Uses bitmap merge for accurate deduplication — no double-counting ac... |
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

**Transfer**

| Model | Layer | Description |
|-------|-------|-------------|
| `stg_envio_ga__transfer_actions` | Staging | STRETCH — compact per-(participant, transfer_type) aggregate from ONE full scan of envio_ga.transfer (108M, no prunin... |

**Transfers**

| Model | Layer | Description |
|-------|-------|-------------|
| `int_execution_transfers_whitelisted_daily` | Intermediate | The `int_execution_transfers_whitelisted_daily` model aggregates daily whitelisted token transfer data, including dep... |

**Uniswap**

| Model | Layer | Description |
|-------|-------|-------------|
| `stg_pools__uniswap_v3_events` | Staging | Normalized event deltas for Uniswap V3 pools. Parses Mint, Burn, Swap, Collect, Flash events into signed token deltas... |

**Users**

| Model | Layer | Description |
|-------|-------|-------------|
| `stg_envio_ga__users` | Staging | Registered Circles identity universe (dedup via envio_latest). INTERNAL (raw address). |

**V3**

| Model | Layer | Description |
|-------|-------|-------------|
| `stg_pools__v3_current_tick` | Staging | Latest tick per V3 pool derived from the most recent Swap event. Used to determine whether concentrated-liquidity LP ... |
| `stg_pools__v3_pool_registry` | Staging | Complete registry of Uniswap V3 and Swapr V3 (Algebra) pools on Gnosis Chain.
Combines factory creation events (PoolC... |

**Wallet**

| Model | Layer | Description |
|-------|-------|-------------|
| `stg_envio_ga__wallet_activity_daily` | Staging | STRETCH — distinct (app-active wallet, calendar-day) from ONE full scan of envio_ga.transaction_action (209M). The DA... |

**Yields**

| Model | Layer | Description |
|-------|-------|-------------|
| `int_execution_yields_balancer_lp_fees` | Intermediate | True Balancer (V2/V3) LP swap fees per (provider, pool), used by int_execution_yields_user_lp_positions to replace th... |
| `int_execution_yields_user_activity` | Intermediate | Unified yield activity feed combining LP events (Add/Remove Liquidity, Collect Fees) from the pools pipeline and lend... |
| `int_execution_yields_user_lp_positions` | Intermediate | Per-user LP position summary across all DEX protocols. One row per (provider, pool_address, tick_lower, tick_upper). ... |
| `fct_execution_yields_opportunities_latest` | Fact | Combined yield opportunities table for LP pools and lending markets. Ranked by yield for quick comparison. |
| `fct_execution_yields_overview_snapshot` | Fact | Long-format KPI snapshot table for the yields overview dashboard. One row
per metric, with the latest value, 7-day ch... |
| `fct_execution_yields_user_fee_collections_daily` | Fact | Daily fee collection amounts per user per pool from V3 Collect events. Feeds the fee income chart in the user portfol... |
| `fct_execution_yields_user_lending_positions_latest` | Fact | Current Aave V3 lending positions per user with supply APY from the yields opportunities table. One row per (user, re... |
| `fct_execution_yields_user_lifetime_metrics` | Fact | Per-wallet lifetime KPI metrics for the yields user portfolio. Aggregates across LP positions (fees, active/in-range ... |
| `api_execution_yields_opportunities_latest` | API | Thin API view over fct_execution_yields_opportunities_latest, sorted by
yield_apr/yield_apy descending. Powers the yi... |
| `api_execution_yields_overview_lending_best_apy` | API | Overview KPI card for the best lending supply APY currently available (with the token symbol as label) and 7-day change. |
| `api_execution_yields_overview_lending_lenders` | API | Overview KPI card for total distinct Aave V3 lenders on Gnosis with 7-day change percentage. |
| `api_execution_yields_overview_lending_tvl` | API | Overview KPI card for total Aave V3 lending TVL with 7-day change percentage. |
| `api_execution_yields_overview_lp_best_apr` | API | Overview KPI card for the best LP fee APR currently available (with the pool name as label) and 7-day change. |
| `api_execution_yields_overview_lp_tvl` | API | Overview KPI card for total LP TVL across Uniswap V3, Swapr V3, Balancer V2/V3 on Gnosis with 7-day change. |
| `api_execution_yields_overview_sdai_apy` | API | Overview KPI card for Savings xDAI (sDAI) APY with 7-day change percentage. |
| `api_execution_yields_overview_sdai_supply` | API | Overview KPI card for total sDAI supply with 7-day change percentage. |
| `api_execution_yields_user_activity` | API | Per-event user activity feed across LP and lending positions (deposits,
withdrawals, fee collections, supply/repay, e... |
| `api_execution_yields_user_fee_collections_daily` | API | Thin API view over fct_execution_yields_user_fee_collections_daily — per-day, per-pool LP fee collection amounts for ... |
| `api_execution_yields_user_kpis` | API | Thin API view over fct_execution_yields_user_lifetime_metrics for the
"user portfolio KPIs" widget. One row per walle... |
| `api_execution_yields_user_lending_balances_daily` | API | Daily supply balance series per (user, reserve) across Aave V3. Rounded
to 6 native decimals and 2 USD decimals for d... |
| `api_execution_yields_user_lending_positions` | API | Thin API view over fct_execution_yields_user_lending_positions_latest — current Aave V3 lending positions per user wi... |
| `api_execution_yields_user_lp_positions` | API | Current LP positions per wallet across Uniswap V3, Swapr V3, and Balancer
V2/V3. One row per (provider, pool_address[... |
| `api_execution_yields_user_top_wallets` | API | Allow-list of ~50 wallet addresses surfaced as "top wallets" on the user
portfolio landing dashboard. Combines top Un... |

**Zodiac**

| Model | Layer | Description |
|-------|-------|-------------|
| `int_execution_zodiac_modifier_module_events` | Intermediate | Long-form append log of every EnabledModule / DisabledModule event
emitted BY a Zodiac Modifier proxy (Delay / Roles)... |
| `int_execution_zodiac_modifier_submodules_latest` | Intermediate | Latest-state snapshot of which sub-modules are currently enabled on each
Zodiac Modifier, derived from int_execution_... |
| `int_execution_zodiac_module_proxies` | Intermediate | Catalogue of every Zodiac module proxy ever deployed on Gnosis Chain.

Decoded directly from the canonical Zodiac Mod... |

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
