---
title: Data Dictionary
description: ClickHouse database schemas, table definitions, and partitioning strategies
---

# Data Dictionary

The Gnosis Analytics platform stores all data in a ClickHouse Cloud cluster organized into five databases. This page documents the key tables in each database, their columns, data types, and partitioning strategies.

## Database Overview

| Database | Purpose | Primary Sources | Approx. Tables |
|----------|---------|-----------------|----------------|
| `execution` | Raw execution layer data | cryo-indexer | ~15 |
| `consensus` | Raw consensus layer data | beacon-indexer, era-parser | ~10 |
| `crawlers_data` | External data from third-party sources | click-runner, ip-crawler | ~10 |
| `nebula` | P2P network crawl data | nebula | ~5 |
| `dbt` | Transformed and modeled data | dbt-cerebro | ~400 |

---

## execution Database

Raw execution layer data indexed from Gnosis Chain EL nodes by cryo-indexer. Tables contain block-level, transaction-level, and event-level data.

### execution.blocks

Block header information for every execution layer block.

| Column | Type | Description |
|--------|------|-------------|
| `block_number` | `UInt64` | Block height (primary key) |
| `block_hash` | `String` | Block hash (hex) |
| `parent_hash` | `String` | Parent block hash |
| `author` | `String` | Block proposer address (hex) |
| `state_root` | `String` | State trie root hash |
| `transactions_root` | `String` | Transaction trie root hash |
| `receipts_root` | `String` | Receipt trie root hash |
| `gas_used` | `UInt64` | Total gas consumed by transactions in this block |
| `gas_limit` | `UInt64` | Maximum gas allowed in this block |
| `base_fee_per_gas` | `Nullable(UInt64)` | EIP-1559 base fee (null for pre-London blocks) |
| `extra_data` | `String` | Extra data field (often contains client identifier) |
| `block_timestamp` | `DateTime` | Block timestamp (UTC) |
| `blob_gas_used` | `Nullable(UInt64)` | EIP-4844 blob gas consumed |
| `excess_blob_gas` | `Nullable(UInt64)` | EIP-4844 excess blob gas |

**Engine:** `ReplacingMergeTree()` | **Order by:** `block_number` | **Partition by:** `toStartOfMonth(block_timestamp)`

---

### execution.transactions

Individual transactions within execution layer blocks.

| Column | Type | Description |
|--------|------|-------------|
| `block_number` | `UInt64` | Block containing this transaction |
| `transaction_index` | `UInt32` | Position within the block |
| `transaction_hash` | `String` | Transaction hash (hex) |
| `from_address` | `String` | Sender address |
| `to_address` | `Nullable(String)` | Recipient address (null for contract creation) |
| `value` | `UInt256` | Transfer value in wei |
| `gas_price` | `Nullable(UInt64)` | Gas price in wei |
| `gas_used` | `UInt64` | Actual gas consumed |
| `input` | `String` | Transaction input data (calldata) |
| `nonce` | `UInt64` | Sender nonce |
| `transaction_type` | `UInt8` | Transaction type (0=legacy, 1=access list, 2=EIP-1559, 3=blob) |
| `max_fee_per_gas` | `Nullable(UInt64)` | EIP-1559 max fee per gas |
| `max_priority_fee_per_gas` | `Nullable(UInt64)` | EIP-1559 max priority fee |
| `max_fee_per_blob_gas` | `Nullable(UInt64)` | EIP-4844 max blob gas fee |
| `block_timestamp` | `DateTime` | Block timestamp (UTC) |
| `success` | `Bool` | Whether the transaction succeeded |

**Engine:** `ReplacingMergeTree()` | **Order by:** `(block_number, transaction_index)` | **Partition by:** `toStartOfMonth(block_timestamp)`

---

### execution.logs

Event logs emitted by smart contract execution.

| Column | Type | Description |
|--------|------|-------------|
| `block_number` | `UInt64` | Block number |
| `transaction_index` | `UInt32` | Transaction position in block |
| `log_index` | `UInt32` | Log position within transaction |
| `transaction_hash` | `String` | Transaction hash |
| `address` | `String` | Contract address that emitted the log |
| `topic0` | `Nullable(String)` | First topic (event signature hash) |
| `topic1` | `Nullable(String)` | Second topic (indexed parameter) |
| `topic2` | `Nullable(String)` | Third topic (indexed parameter) |
| `topic3` | `Nullable(String)` | Fourth topic (indexed parameter) |
| `data` | `String` | Non-indexed event data (hex) |
| `block_timestamp` | `DateTime` | Block timestamp |

**Engine:** `ReplacingMergeTree()` | **Order by:** `(block_number, transaction_index, log_index)` | **Partition by:** `toStartOfMonth(block_timestamp)`

---

### execution.traces

Internal call traces for transaction execution (call tree).

| Column | Type | Description |
|--------|------|-------------|
| `block_number` | `UInt64` | Block number |
| `transaction_index` | `UInt32` | Transaction position |
| `transaction_hash` | `String` | Transaction hash |
| `trace_address` | `String` | Position in the call tree (e.g., `0.1.2`) |
| `from_address` | `String` | Caller address |
| `to_address` | `Nullable(String)` | Callee address |
| `value` | `UInt256` | Value transferred in wei |
| `input` | `String` | Call input data |
| `output` | `String` | Call output data |
| `call_type` | `String` | Trace type: `call`, `staticcall`, `delegatecall`, `create`, `create2` |
| `gas_used` | `UInt64` | Gas consumed by this trace |
| `error` | `Nullable(String)` | Revert reason if call failed |
| `block_timestamp` | `DateTime` | Block timestamp |

**Engine:** `ReplacingMergeTree()` | **Order by:** `(block_number, transaction_index, trace_address)` | **Partition by:** `toStartOfMonth(block_timestamp)`

---

### execution.contracts

Deployed smart contract metadata.

| Column | Type | Description |
|--------|------|-------------|
| `block_number` | `UInt64` | Block where the contract was deployed |
| `transaction_hash` | `String` | Deployment transaction hash |
| `contract_address` | `String` | Deployed contract address |
| `deployer` | `String` | Address that deployed the contract |
| `bytecode` | `String` | Contract creation bytecode |
| `block_timestamp` | `DateTime` | Deployment timestamp |

**Engine:** `ReplacingMergeTree()` | **Order by:** `(contract_address)` | **Partition by:** `toStartOfMonth(block_timestamp)`

---

### execution.native_transfers

Native token (xDai) transfers extracted from traces.

| Column | Type | Description |
|--------|------|-------------|
| `block_number` | `UInt64` | Block number |
| `transaction_hash` | `String` | Transaction hash |
| `from_address` | `String` | Sender address |
| `to_address` | `String` | Recipient address |
| `value` | `UInt256` | Transfer amount in wei |
| `block_timestamp` | `DateTime` | Block timestamp |

**Engine:** `ReplacingMergeTree()` | **Order by:** `(block_number, transaction_hash)` | **Partition by:** `toStartOfMonth(block_timestamp)`

---

### execution.erc20_transfers

ERC-20 token transfer events decoded from logs.

| Column | Type | Description |
|--------|------|-------------|
| `block_number` | `UInt64` | Block number |
| `transaction_hash` | `String` | Transaction hash |
| `log_index` | `UInt32` | Log position |
| `token_address` | `String` | ERC-20 contract address |
| `from_address` | `String` | Sender address |
| `to_address` | `String` | Recipient address |
| `value` | `UInt256` | Transfer amount (in token's smallest unit) |
| `block_timestamp` | `DateTime` | Block timestamp |

**Engine:** `ReplacingMergeTree()` | **Order by:** `(block_number, log_index)` | **Partition by:** `toStartOfMonth(block_timestamp)`

---

### execution.erc721_transfers

ERC-721 (NFT) transfer events decoded from logs.

| Column | Type | Description |
|--------|------|-------------|
| `block_number` | `UInt64` | Block number |
| `transaction_hash` | `String` | Transaction hash |
| `log_index` | `UInt32` | Log position |
| `token_address` | `String` | ERC-721 contract address |
| `from_address` | `String` | Sender address |
| `to_address` | `String` | Recipient address |
| `token_id` | `UInt256` | NFT token ID |
| `block_timestamp` | `DateTime` | Block timestamp |

**Engine:** `ReplacingMergeTree()` | **Order by:** `(block_number, log_index)` | **Partition by:** `toStartOfMonth(block_timestamp)`

---

### execution.state_diffs

Account state changes per transaction.

| Column | Type | Description |
|--------|------|-------------|
| `block_number` | `UInt64` | Block number |
| `transaction_index` | `UInt32` | Transaction position |
| `transaction_hash` | `String` | Transaction hash |
| `address` | `String` | Account address |
| `slot` | `String` | Storage slot (for storage diffs) |
| `from_value` | `String` | Previous value |
| `to_value` | `String` | New value |
| `block_timestamp` | `DateTime` | Block timestamp |

**Engine:** `ReplacingMergeTree()` | **Order by:** `(block_number, transaction_index, address, slot)` | **Partition by:** `toStartOfMonth(block_timestamp)`

---

## consensus Database

Raw consensus layer data from beacon-indexer and era-parser. Contains validator lifecycle, attestation, and block proposal data.

### consensus.blocks

Beacon chain block (slot) data.

| Column | Type | Description |
|--------|------|-------------|
| `slot` | `UInt64` | Slot number (primary key) |
| `epoch` | `UInt64` | Epoch number (`slot / 16` on Gnosis) |
| `block_root` | `String` | Block root hash |
| `parent_root` | `String` | Parent block root |
| `state_root` | `String` | Beacon state root |
| `proposer_index` | `UInt64` | Validator index of the block proposer |
| `graffiti` | `String` | Proposer graffiti (UTF-8 string) |
| `attestation_count` | `UInt32` | Number of attestations in this block |
| `deposit_count` | `UInt32` | Number of deposits in this block |
| `exit_count` | `UInt32` | Number of voluntary exits |
| `slot_timestamp` | `DateTime` | Slot timestamp (UTC) |

**Engine:** `ReplacingMergeTree()` | **Order by:** `slot` | **Partition by:** `toStartOfMonth(slot_timestamp)`

---

### consensus.attestations

Validator attestation data per slot.

| Column | Type | Description |
|--------|------|-------------|
| `slot` | `UInt64` | Slot being attested to |
| `committee_index` | `UInt32` | Committee index |
| `aggregation_bits` | `String` | Bitfield of participating validators |
| `beacon_block_root` | `String` | Attested block root |
| `source_epoch` | `UInt64` | Source checkpoint epoch |
| `target_epoch` | `UInt64` | Target checkpoint epoch |
| `slot_timestamp` | `DateTime` | Slot timestamp |

**Engine:** `ReplacingMergeTree()` | **Order by:** `(slot, committee_index)` | **Partition by:** `toStartOfMonth(slot_timestamp)`

---

### consensus.validators

Validator registry snapshots.

| Column | Type | Description |
|--------|------|-------------|
| `validator_index` | `UInt64` | Validator index |
| `pubkey` | `String` | Validator public key (hex) |
| `withdrawal_credentials` | `String` | Withdrawal credentials |
| `effective_balance` | `UInt64` | Effective balance in Gwei |
| `slashed` | `Bool` | Whether the validator has been slashed |
| `activation_epoch` | `UInt64` | Epoch when the validator was activated |
| `exit_epoch` | `UInt64` | Epoch when the validator exited (max value if still active) |
| `withdrawable_epoch` | `UInt64` | Epoch when funds become withdrawable |
| `status` | `String` | Current status: `active_ongoing`, `active_exiting`, `exited_unslashed`, etc. |
| `snapshot_epoch` | `UInt64` | Epoch when this snapshot was taken |

**Engine:** `ReplacingMergeTree()` | **Order by:** `(validator_index, snapshot_epoch)` | **Partition by:** `toStartOfMonth(toDateTime(snapshot_epoch * 80))`

---

### consensus.sync_committees

Sync committee participation data.

| Column | Type | Description |
|--------|------|-------------|
| `slot` | `UInt64` | Slot number |
| `period` | `UInt64` | Sync committee period |
| `sync_committee_bits` | `String` | Bitfield of participating committee members |
| `participant_count` | `UInt32` | Number of participants |
| `slot_timestamp` | `DateTime` | Slot timestamp |

**Engine:** `ReplacingMergeTree()` | **Order by:** `slot` | **Partition by:** `toStartOfMonth(slot_timestamp)`

---

### consensus.blob_sidecars

EIP-4844 blob sidecar data.

| Column | Type | Description |
|--------|------|-------------|
| `slot` | `UInt64` | Slot number |
| `blob_index` | `UInt32` | Blob index within the slot |
| `block_root` | `String` | Associated block root |
| `kzg_commitment` | `String` | KZG commitment (hex) |
| `kzg_proof` | `String` | KZG proof (hex) |
| `blob_size` | `UInt32` | Blob data size in bytes |
| `slot_timestamp` | `DateTime` | Slot timestamp |

**Engine:** `ReplacingMergeTree()` | **Order by:** `(slot, blob_index)` | **Partition by:** `toStartOfMonth(slot_timestamp)`

---

### consensus.proposer_duties

Block proposer assignments per epoch.

| Column | Type | Description |
|--------|------|-------------|
| `epoch` | `UInt64` | Epoch number |
| `slot` | `UInt64` | Slot number |
| `validator_index` | `UInt64` | Assigned proposer's validator index |
| `proposed` | `Bool` | Whether the assigned proposer actually proposed a block |

**Engine:** `ReplacingMergeTree()` | **Order by:** `(epoch, slot)` | **Partition by:** `toStartOfMonth(toDateTime(slot * 5))`

---

## crawlers_data Database

External data imported via click-runner and ip-crawler. Contains third-party datasets used for ESG, network performance, and geolocation analytics.

### crawlers_data.ipinfo

IP geolocation data enriched by ip-crawler from ipinfo.io.

| Column | Type | Description |
|--------|------|-------------|
| `ip` | `String` | IP address (primary key component) |
| `hostname` | `String` | Reverse DNS hostname |
| `city` | `String` | City name |
| `region` | `String` | Region/state name |
| `country` | `String` | ISO country code |
| `loc` | `String` | Latitude,longitude coordinates |
| `org` | `String` | Organization name |
| `postal` | `String` | Postal/ZIP code |
| `timezone` | `String` | IANA timezone identifier |
| `asn` | `String` | Autonomous System Number |
| `company` | `String` | Company name |
| `is_bogon` | `Bool` | Whether the IP is a bogon (private/reserved) |
| `is_mobile` | `Bool` | Whether the IP is a mobile connection |
| `success` | `Bool` | Whether the lookup succeeded |
| `created_at` | `DateTime` | First lookup timestamp |
| `updated_at` | `DateTime` | Most recent lookup timestamp |

**Engine:** `ReplacingMergeTree()` | **Order by:** `ip`

---

### crawlers_data.ember_electricity_generation

Global electricity generation data from the Ember Climate project. Used for ESG carbon footprint calculations.

| Column | Type | Description |
|--------|------|-------------|
| `country` | `String` | Country name |
| `country_code` | `String` | ISO country code |
| `year` | `UInt16` | Data year |
| `category` | `String` | Generation category (e.g., `Coal`, `Gas`, `Solar`, `Wind`) |
| `subcategory` | `String` | Subcategory detail |
| `value` | `Float64` | Generation amount (TWh or other unit) |
| `unit` | `String` | Unit of measurement |

**Engine:** `ReplacingMergeTree()` | **Order by:** `(country_code, year, category)`

---

### crawlers_data.probelab_agent_semvers_avg_1d

Daily ProbeLab network metrics on agent version distribution.

| Column | Type | Description |
|--------|------|-------------|
| `date` | `Date` | Observation date |
| `agent_name` | `String` | Client software name |
| `agent_semver` | `String` | Semantic version string |
| `count` | `Float64` | Average peer count observed |
| `percentage` | `Float64` | Percentage of total peers |

**Engine:** `ReplacingMergeTree()` | **Order by:** `(date, agent_name, agent_semver)` | **Partition by:** `toStartOfMonth(date)`

---

## nebula Database

P2P network crawl data from the nebula DHT crawler. Contains peer discovery results, visit records, and session data.

### nebula.visits

Records of each peer visit during a crawl session.

| Column | Type | Description |
|--------|------|-------------|
| `id` | `UInt64` | Visit identifier |
| `peer_id` | `String` | Unique peer identifier |
| `crawl_id` | `UInt64` | Crawl session identifier |
| `peer_properties` | `String` | JSON object with IP, agent version, fork digest, protocols |
| `visit_started_at` | `DateTime` | Visit start timestamp |
| `visit_ended_at` | `DateTime` | Visit end timestamp |
| `connect_error` | `Nullable(String)` | Error details if connection failed |
| `agent_version` | `Nullable(String)` | Extracted agent version string |
| `protocols` | `Nullable(String)` | Supported protocol list |

**Engine:** `MergeTree()` | **Order by:** `(visit_started_at, peer_id)` | **Partition by:** `toStartOfMonth(visit_started_at)`

!!! info "JSON extraction"
    The `peer_properties` field contains a JSON object. Downstream dbt models extract individual fields (IP address, agent version, fork digest) from this JSON for analytics.

---

### nebula.peers

Aggregated peer records with the latest known state for each discovered peer.

| Column | Type | Description |
|--------|------|-------------|
| `peer_id` | `String` | Unique peer identifier |
| `multi_hash` | `String` | Multihash representation |
| `agent_version` | `Nullable(String)` | Last known agent version |
| `protocols` | `Nullable(String)` | Last known supported protocols |
| `first_seen_at` | `DateTime` | When this peer was first discovered |
| `last_seen_at` | `DateTime` | Most recent visit |

**Engine:** `ReplacingMergeTree(last_seen_at)` | **Order by:** `peer_id`

---

## dbt Database

Transformed and modeled data produced by dbt-cerebro. Contains approximately 400 models organized by layer and module.

### Model Naming Pattern

```
{layer}_{module}_{entity}_{granularity}
```

### Layer Distribution

| Layer | Prefix | Materialization | Approx. Count | Description |
|-------|--------|-----------------|---------------|-------------|
| Staging | `stg_` | View | ~40 | Clean interfaces over raw source tables |
| Intermediate | `int_` | Incremental table | ~200 | Business logic, joins, aggregations |
| Facts | `fct_` | View | ~50 | Business-ready metrics and KPIs |
| API | `api_` | View | ~100 | REST API endpoint projections |

### Key API Models by Module

#### Execution Module

| Model | Description | Granularity |
|-------|-------------|-------------|
| `api_execution_transactions_daily` | Daily transaction counts, unique senders/receivers | Daily |
| `api_execution_gas_daily` | Gas usage statistics, fees, avg gas price | Daily |
| `api_execution_blocks_clients_version_daily` | Block proposer client distribution | Daily |
| `api_execution_token_balances_daily` | Token balance snapshots | Daily |
| `api_execution_contract_deployments_daily` | New contract deployment counts | Daily |

#### Consensus Module

| Model | Description | Granularity |
|-------|-------------|-------------|
| `api_consensus_validators_active_daily` | Active validator count over time | Daily |
| `api_consensus_attestation_participation_daily` | Attestation participation rates | Daily |
| `api_consensus_blob_commitments_daily` | Blob commitment volumes | Daily |
| `api_consensus_blob_commitments_latest` | Most recent blob commitment data | Latest |
| `api_consensus_proposer_duties_daily` | Block proposal statistics | Daily |

#### Bridges Module

| Model | Description | Granularity |
|-------|-------------|-------------|
| `api_bridges_transfers_daily` | Cross-chain bridge transfer volume | Daily |
| `api_bridges_transfers_weekly` | Weekly bridge volume summary | Weekly |

#### P2P Module

| Model | Description | Granularity |
|-------|-------------|-------------|
| `api_p2p_client_distribution_daily` | Client software distribution | Daily |
| `api_p2p_client_diversity_latest` | Current client diversity snapshot | Latest |
| `api_p2p_peers_geo_daily` | Geographic distribution of peers | Daily |

#### ESG Module

| Model | Description | Granularity |
|-------|-------------|-------------|
| `api_esg_energy_consumption_daily` | Network energy consumption estimates | Daily |
| `api_esg_carbon_footprint_monthly` | Monthly carbon footprint calculations | Monthly |

#### Contracts Module

| Model | Description | Granularity |
|-------|-------------|-------------|
| `api_contracts_deployments_daily` | Smart contract deployment analytics | Daily |
| `api_contracts_decoded_events` | Decoded smart contract events | -- |

### Partitioning Strategy

All intermediate (`int_*`) models are partitioned by month using `toStartOfMonth(date)`. This enables:

- **Efficient incremental processing** -- The `delete+insert` strategy operates on monthly partitions
- **Fast date range queries** -- ClickHouse can skip entire partitions for date-filtered queries
- **Manageable partition sizes** -- Monthly partitions balance between too many small partitions and too few large ones

### Row Count Estimates

!!! note "Approximate values"
    These are approximate row counts to give a sense of scale. Actual values grow over time as new blockchain data is indexed.

| Table | Approximate Rows | Growth Rate |
|-------|-------------------|-------------|
| `execution.blocks` | ~40M | ~17K/day |
| `execution.transactions` | ~500M | ~150K/day |
| `execution.logs` | ~2B | ~1M/day |
| `execution.traces` | ~3B | ~2M/day |
| `consensus.blocks` | ~40M (slots) | ~17K/day |
| `consensus.attestations` | ~500M | ~300K/day |
| `consensus.validators` | ~200K (latest snapshot) | Slow growth |
| `nebula.visits` | ~100M | ~500K/day |
| `crawlers_data.ipinfo` | ~500K | ~1K/day |

## Next Steps

- [Model Catalog](../models/index.md) -- Browse all dbt models by module
- [Environment Variables](env-vars.md) -- Database connection configuration
- [Glossary](glossary.md) -- Term definitions
