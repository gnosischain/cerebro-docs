# Consensus Module

The Consensus module covers all data from the Gnosis Chain Beacon Chain (consensus layer). This includes validator lifecycle management, attestation performance, sync committee participation, proposer duties, rewards and penalties, deposits, withdrawals, slashings, blob commitments, client distribution, and epoch/slot metadata.

## Data Sources

Raw data is sourced from the `consensus` ClickHouse database, which contains:

- **validators** -- Validator registry with pubkeys, activation/exit epochs, and balances
- **attestations** -- Attestation records including source, target, and head votes
- **rewards** -- Per-validator reward and penalty breakdowns by epoch
- **deposits** -- Beacon chain deposit events
- **withdrawals** -- Processed withdrawal records (post-Shapella)
- **blobs** -- Blob sidecar commitments (post-Dencun/Pectra)
- **sync_committees** -- Sync committee assignments and participation
- **proposer_duties** -- Block proposal assignments and execution
- **specs** -- Chain specification parameters (slots per epoch, etc.)

## Gnosis Chain Consensus Parameters

Gnosis Chain shares the Ethereum Beacon Chain specification with several key differences:

| Parameter | Value |
|-----------|-------|
| Slots per epoch | 16 |
| Block time | 5 seconds |
| Epoch duration | 80 seconds |
| Staking requirement | 1 GNO per validator |
| Gas token | xDAI (18 decimals) |
| Withdrawal prefix | `0x01` |
| Max validators per epoch churn | 4 |

!!! info "Low Barrier to Entry"
    Unlike Ethereum's 32 ETH requirement, Gnosis Chain requires only 1 GNO to run a validator. This design choice promotes decentralization by lowering the financial barrier to participation, resulting in a larger and more distributed validator set.

## Model Categories

<!-- BEGIN AUTO-GENERATED: models-consensus -->
**Attestations**

| Model | Layer | Description |
|-------|-------|-------------|
| `stg_consensus__attestations` | Staging | The stg_consensus__attestations model consolidates attestation data from the consensus layer, enabling analysis of va... |
| `int_consensus_attestations_daily` | Intermediate | The int_consensus_attestations_daily model aggregates daily consensus attestations, providing insights into attestati... |
| `fct_consensus_attestations_performance_daily` | Fact | Network-wide daily attestation KPI fact derived from int_consensus_attestations_daily. One row per day. |
| `api_consensus_attestations_daily` | API | The api_consensus_attestations_daily model provides a daily summary of consensus attestations, capturing key metrics ... |
| `api_consensus_attestations_performance_daily` | API | Public API view over fct_consensus_attestations_performance_daily. Network-wide daily attestation KPIs. |

**Blob**

| Model | Layer | Description |
|-------|-------|-------------|
| `stg_consensus__blob_commitments` | Staging | This model aggregates blob commitment data from the consensus layer, providing a view of commitment details associate... |
| `int_consensus_blob_commitments_daily` | Intermediate | The `int_consensus_blob_commitments_daily` model aggregates daily counts of blob commitments from the consensus layer... |
| `api_consensus_blob_commitments_daily` | API | The api_consensus_blob_commitments_daily model provides a daily overview of total blob commitments within the consens... |

**Blocks**

| Model | Layer | Description |
|-------|-------|-------------|
| `stg_consensus__blocks` | Staging | The stg_consensus__blocks model provides a structured view of blockchain block data, capturing key consensus layer at... |
| `int_consensus_blocks_daily` | Intermediate | The int_consensus_blocks_daily model aggregates daily consensus block production metrics, including counts of blocks ... |
| `api_consensus_blocks_daily` | API | The api_consensus_blocks_daily model aggregates daily consensus block data, providing insights into blocks produced a... |

**Consolidations**

| Model | Layer | Description |
|-------|-------|-------------|
| `fct_consensus_consolidations_daily` | Fact | Daily EIP-7251 consolidation event counts and transferred amounts stacked by role
('self', 'source', 'target'). Mater... |
| `api_consensus_consolidations_daily` | API | Public API view — SELECT * FROM fct_consensus_consolidations_daily. Filter/pagination metadata in model config. |

**Credentials**

| Model | Layer | Description |
|-------|-------|-------------|
| `int_consensus_credentials_daily` | Intermediate | The int_consensus_credentials_daily model tracks the daily count of validator credentials by type, supporting analysi... |
| `api_consensus_credentials_daily` | API | The api_consensus_credentials_daily model provides daily aggregated counts and percentage shares of different credent... |
| `api_consensus_credentials_latest` | API | The api_consensus_credentials_latest model provides a snapshot of the most recent count of different credential types... |

**Deposits**

| Model | Layer | Description |
|-------|-------|-------------|
| `stg_consensus__deposits` | Staging | This model captures deposit transactions from the consensus layer, providing details necessary for analyzing deposit ... |
| `int_consensus_deposits_withdrawals_daily` | Intermediate | This model aggregates daily consensus deposit and withdrawal data, providing insights into the total amounts and tran... |
| `api_consensus_deposits_withdrawls_cnt_daily` | API | The model aggregates daily counts of consensus deposits and withdrawals to monitor transaction activity trends over t... |
| `api_consensus_deposits_withdrawls_volume_daily` | API | The api_consensus_deposits_withdrawls_volume_daily model provides a daily summary of deposit and withdrawal volumes f... |

**Entry**

| Model | Layer | Description |
|-------|-------|-------------|
| `int_consensus_entry_queue_daily` | Intermediate | This model provides daily aggregated insights into validator activation times within the consensus protocol, enabling... |
| `api_consensus_entry_queue_daily` | API | The api_consensus_entry_queue_daily model provides daily aggregated statistics on the validator entry queue, enabling... |

**Execution**

| Model | Layer | Description |
|-------|-------|-------------|
| `stg_consensus__execution_requests` | Staging | This view aggregates execution request data from the consensus layer, providing insights into various transaction typ... |

**Forks**

| Model | Layer | Description |
|-------|-------|-------------|
| `fct_consensus_forks` | Fact | The fct_consensus_forks model provides a consolidated view of consensus fork details, including their identifiers, ve... |
| `api_consensus_forks` | API | The api_consensus_forks model provides a consolidated view of consensus fork information used in the blockchain netwo... |

**Graffiti**

| Model | Layer | Description |
|-------|-------|-------------|
| `int_consensus_graffiti_daily` | Intermediate | This model aggregates daily counts of graffiti entries on the blockchain, categorizing them by detected brands and cl... |
| `fct_consensus_graffiti_cloud` | Fact | The fct_consensus_graffiti_cloud model aggregates graffiti-related consensus data over various timeframes to support ... |
| `api_consensus_graffiti_cloud` | API | The api_consensus_graffiti_cloud model aggregates consensus data related to graffiti labels and their associated valu... |
| `api_consensus_graffiti_label_daily` | API | The api_consensus_graffiti_label_daily model aggregates daily counts of graffiti labels to support trend analysis and... |

**Info**

| Model | Layer | Description |
|-------|-------|-------------|
| `fct_consensus_info_latest` | Fact | The fct_consensus_info_latest model aggregates the most recent and 7-day summary metrics related to deposits, withdra... |
| `api_consensus_info_active_ongoing_latest` | API | The model provides the latest consensus information on active and ongoing items, serving as a key reference for monit... |
| `api_consensus_info_apy_latest` | API | The api_consensus_info_apy_latest model provides the most recent annual percentage yield (APY) data from consensus so... |
| `api_consensus_info_deposits_cnt_latest` | API | The model provides the latest consensus information on the total number of deposits, serving as a key metric for moni... |
| `api_consensus_info_staked_latest` | API | The api_consensus_info_staked_latest model provides the most recent total staked GNO value and its percentage change,... |
| `api_consensus_info_withdrawls_cnt_latest` | API | This view provides the latest count of withdrawal events from the consensus API, enabling monitoring of withdrawal ac... |

**Rewards**

| Model | Layer | Description |
|-------|-------|-------------|
| `stg_consensus__rewards` | Staging | The stg_consensus__rewards model aggregates consensus layer reward-related metrics per slot to support analysis of va... |

**Specs**

| Model | Layer | Description |
|-------|-------|-------------|
| `stg_consensus__specs` | Staging | The stg_consensus__specs model serves as a staging view that consolidates configuration parameters and their values u... |

**Staked**

| Model | Layer | Description |
|-------|-------|-------------|
| `api_consensus_staked_daily` | API | The api_consensus_staked_daily model provides daily aggregated data on the effective staked GNO across validators, fa... |

**Time**

| Model | Layer | Description |
|-------|-------|-------------|
| `stg_consensus__time_helpers` | Staging | The stg_consensus__time_helpers model provides essential timing parameters used for consensus protocol calculations, ... |

**Validators**

| Model | Layer | Description |
|-------|-------|-------------|
| `stg_consensus__validators` | Staging | This view consolidates validator information from the consensus layer, focusing on active validators with a positive ... |
| `stg_consensus__validators_all` | Staging | Unfiltered validator snapshot view — every validator regardless of status or balance (verified: the SQL is `SELECT * ... |
| `int_consensus_validators_apy_dist_income_daily` | Intermediate | Network-wide daily APY quantile distribution, built on int_consensus_validators_income_daily
(the spec-bounded APY so... |
| `int_consensus_validators_balances_daily` | Intermediate | The `int_consensus_validators_balances_daily` model aggregates daily total and effective balances of validators from ... |
| `int_consensus_validators_consolidation_flags` | Intermediate | Small per-validator lookup: does this validator appear as the SOURCE or
TARGET of any cross-consolidation request (ev... |
| `int_consensus_validators_consolidation_requests` | Intermediate | Deduplicated EIP-7251 (MaxEB) validator consolidation requests. One row
per unique (source_pubkey, is_self_consolidat... |
| `int_consensus_validators_consolidations_daily` | Intermediate | EIP-7251 (MaxEB) consolidation events at per-(date, validator_index, role) grain. See
https://notes.ethereum.org/@fra... |
| `int_consensus_validators_deposits_daily` | Intermediate | Daily per-validator consensus-layer deposits in GNO. Combines beacon deposits (stg_consensus__deposits) with executio... |
| `int_consensus_validators_dists_daily` | Intermediate | This model aggregates daily distributions of validator balances and APY (Annual Percentage Yield) metrics to support ... |
| `int_consensus_validators_explorer_apy_dist_daily` | Intermediate | Per-(date, withdrawal_credentials) cross-sectional APY distribution plus rolling 7d/30d
medians of the credential's b... |
| `int_consensus_validators_income_daily` | Intermediate | Daily per-(date, validator_index) consensus income fact, including exited and
zero-balance validators. Amount columns... |
| `int_consensus_validators_per_index_apy_daily` | Intermediate | Per-(date, validator_index) APY for active / pending-queued validators.
Rescoped 2026-06: `apy` is now read straight ... |
| `int_consensus_validators_proposer_rewards_daily` | Intermediate | Daily per-validator proposer rewards aggregated from slot-level stg_consensus__rewards. Amounts in real GNO (source g... |
| `int_consensus_validators_snapshots_daily` | Intermediate | Last-of-day validator snapshot per (date, validator_index). Built from stg_consensus__validators_all so exited and ze... |
| `int_consensus_validators_status_daily` | Intermediate | The int_consensus_validators_status_daily model aggregates daily counts of validators' statuses to monitor network he... |
| `int_consensus_validators_withdrawal_addresses` | Intermediate | Thin projection over int_consensus_validators_labels that derives the controlling
EVM address from each validator's w... |
| `int_consensus_validators_withdrawals_daily` | Intermediate | Daily per-validator consensus-layer withdrawals in GNO, keyed by validator_index. Withdrawals only exist on Gnosis po... |
| `fct_consensus_validators_apy_mean_daily` | Fact | Network-wide daily mean APY, balance-weighted by balance_prev_gno so exited / idle
/ just-entered validators (apy=0 a... |
| `fct_consensus_validators_dists_last_30_days` | Fact | This model provides statistical summaries of validator balances and annual percentage yields (APY) over the last 30 d... |
| `fct_consensus_validators_explorer_daily` | Fact | Per-operator (withdrawal_credentials) daily roll-up feeding the five daily charts on
the Validator Explorer tab. Mate... |
| `fct_consensus_validators_explorer_latest` | Fact | Per-operator (withdrawal_credentials) latest-snapshot roll-up. Feeds the KPI cards on
the Validator Explorer tab. Rea... |
| `fct_consensus_validators_explorer_members_table` | Fact | Members table for the Validator Explorer tab: one row per validator under the
selected withdrawal credential. Reads i... |
| `fct_consensus_validators_income_total_daily` | Fact | Network-wide daily consensus income in GNO, summed across every validator (including
exited / zero-balance). Derived ... |
| `fct_consensus_validators_status_latest` | Fact | Validator-level point-in-time snapshot at the most recent slot. One row
per validator with current balance, effective... |
| `fct_consensus_validators_withdrawal_addresses_distinct` | Fact | One row per `user_pseudonym` (sipHash of validator withdrawal
address). Aggregates `n_validators_controlled` per addr... |
| `api_consensus_validators_active_daily` | API | The api_consensus_validators_active_daily model provides a daily snapshot of the number of validators that are active... |
| `api_consensus_validators_apy_dist_daily` | API | This view provides daily distribution metrics of validator APYs, enabling analysis of validator performance variabili... |
| `api_consensus_validators_apy_dist_income_daily` | API | Public API view — SELECT * FROM int_consensus_validators_apy_dist_income_daily. Filter/pagination metadata in model c... |
| `api_consensus_validators_apy_dist_last_30_days` | API | This view provides a distribution of validator APYs over the last 30 days, enabling analysis of APY variability and t... |
| `api_consensus_validators_apy_mean_daily` | API | Public API view — SELECT * FROM fct_consensus_validators_apy_mean_daily. Filter/pagination metadata in model config. |
| `api_consensus_validators_balance_dist_last_30_days` | API | This view provides the distribution of validator balances over the last 30 days, summarized through various quantiles... |
| `api_consensus_validators_balances_daily` | API | The api_consensus_validators_balances_daily model provides a daily overview of validator balances and effective balan... |
| `api_consensus_validators_balances_dist_daily` | API | This view provides daily distribution percentiles of validator balances in GNO, enabling analysis of validator balanc... |
| `api_consensus_validators_explorer_apy_dist_daily` | API | Public API view — SELECT * FROM int_consensus_validators_explorer_apy_dist_daily. Requires withdrawal_credentials fil... |
| `api_consensus_validators_explorer_balance_dist` | API | Balance-distribution histogram across co-validators sharing a withdrawal credential.
Light view over fct_consensus_va... |
| `api_consensus_validators_explorer_daily` | API | Public API view — SELECT * FROM fct_consensus_validators_explorer_daily. Requires withdrawal_credentials filter; see ... |
| `api_consensus_validators_explorer_latest` | API | Public API view — SELECT * FROM fct_consensus_validators_explorer_latest. Requires withdrawal_credentials filter; see... |
| `api_consensus_validators_explorer_members_table` | API | Public API view — SELECT * FROM fct_consensus_validators_explorer_members_table. Requires withdrawal_credentials filt... |
| `api_consensus_validators_income_total_daily` | API | Public API view — SELECT * FROM fct_consensus_validators_income_total_daily. Filter/pagination metadata in model config. |
| `api_consensus_validators_performance_daily` | API | Public API view joining daily income and proposer-reward facts at (date, validator_index). Filterable by validator_in... |
| `api_consensus_validators_performance_latest` | API | Public API view — one row per validator with latest snapshot fields plus 30-day and lifetime aggregates. |
| `api_consensus_validators_search` | API | Dropdown source for the Validator Explorer tab. Grain is one row per
WITHDRAWAL_CREDENTIALS (not per validator) — on ... |
| `api_consensus_validators_status_daily` | API | The api_consensus_validators_status_daily model provides a daily summary of validator statuses, excluding ongoing act... |
| `api_consensus_validators_status_latest` | API | The api_consensus_validators_status_latest model provides the latest validator-level consensus status snapshot and su... |

**Withdrawal**

| Model | Layer | Description |
|-------|-------|-------------|
| `int_consensus_withdrawal_credentials_daily` | Intermediate | The `int_consensus_withdrawal_credentials_daily` model aggregates daily counts of active validator withdrawal credent... |
| `fct_consensus_withdrawal_credentials_freq_daily` | Fact | This model aggregates daily withdrawal credential counts into frequency bins to analyze validator activity levels ove... |
| `api_consensus_withdrawal_credentials_freq_daily` | API | This view aggregates daily counts of validators categorized by their withdrawal credentials frequency, supporting ana... |

**Withdrawals**

| Model | Layer | Description |
|-------|-------|-------------|
| `stg_consensus__withdrawals` | Staging | The stg_consensus__withdrawals model consolidates withdrawal event data from the consensus layer, enabling analysis o... |

**Zero**

| Model | Layer | Description |
|-------|-------|-------------|
| `api_consensus_zero_blob_commitments_daily` | API | This view provides daily aggregated counts of consensus blocks with and without zero blob commitments, aiding in moni... |

<!-- END AUTO-GENERATED: models-consensus -->

## Key Models Reference

The following table summarizes the most commonly used API-layer models for the consensus module:

| Model | Description | Key Columns |
|-------|-------------|-------------|
| `api_consensus_validators_active_daily` | Active validator count over time | `dt`, `active_validators`, `total_balance` |
| `api_consensus_attestations_daily` | Attestation performance | `dt`, `participation_rate`, `avg_inclusion_distance` |
| `api_consensus_sync_committees_daily` | Sync committee participation | `dt`, `participation_rate`, `missed_signatures` |
| `api_consensus_proposer_duties_daily` | Block proposal success rate | `dt`, `proposed_blocks`, `missed_slots` |
| `api_consensus_rewards_daily` | Daily validator rewards | `dt`, `total_rewards`, `avg_reward_per_validator` |
| `api_consensus_deposits_daily` | Deposit activity | `dt`, `deposit_count`, `deposit_volume_gno` |
| `api_consensus_withdrawals_daily` | Withdrawal processing | `dt`, `withdrawal_count`, `withdrawal_volume` |
| `api_consensus_blobs_daily` | Blob usage metrics | `dt`, `blob_count`, `total_blob_size` |
| `api_consensus_blob_commitments_daily` | KZG commitments | `dt`, `commitment_count`, `unique_submitters` |

## Query Examples

Retrieve daily active validator count for the past 30 days:

```sql
SELECT dt, active_validators, total_balance
FROM dbt.api_consensus_validators_active_daily
WHERE dt >= today() - 30
ORDER BY dt
```

Check attestation performance:

```sql
SELECT dt, participation_rate, avg_inclusion_distance
FROM dbt.api_consensus_attestations_daily
WHERE dt >= today() - 7
ORDER BY dt
```

Monitor sync committee participation:

```sql
SELECT dt, participation_rate, missed_signatures
FROM dbt.api_consensus_sync_committees_daily
WHERE dt >= today() - 14
ORDER BY dt
```

Analyze blob usage trends:

```sql
SELECT dt, blob_count, commitment_count, unique_submitters
FROM dbt.api_consensus_blob_commitments_daily
WHERE dt >= today() - 30
ORDER BY dt
```

Track missed slots:

```sql
SELECT dt, proposed_blocks, missed_slots,
       round(missed_slots / (proposed_blocks + missed_slots) * 100, 2) AS miss_rate_pct
FROM dbt.api_consensus_proposer_duties_daily
WHERE dt >= today() - 30
ORDER BY dt
```

## Related Modules

- [Execution](execution.md) -- Execution layer data that includes the deposit contract logs
- [ESG](esg.md) -- Power consumption estimates tied to validator node counts
- [P2P](p2p.md) -- Peer-to-peer network data showing validator client distribution
- [Contracts](contracts.md) -- ABI-decoded deposit contract and staking-related events
