# Modules Reference

dbt-cerebro organizes its approximately 400 models into eight domain modules. Each module has its own directory under `models/` and covers a distinct analytical domain.

## Module Summary

| Module | Directory | Approx. Models | Source Database | Description |
|--------|-----------|-----------------|-----------------|-------------|
| [Execution](#execution) | `models/execution/` | ~208 | `execution` | Blocks, transactions, gas, contracts |
| [Consensus](#consensus) | `models/consensus/` | ~54 | `consensus` | Validators, attestations, sync committees |
| [Contracts](#contracts) | `models/contracts/` | ~44 | `execution` | ABI-decoded smart contract calls and events |
| [P2P](#p2p) | `models/p2p/` | ~27 | `nebula` | Peer discovery, client distribution, geography |
| [Bridges](#bridges) | `models/bridges/` | ~18 | `execution` | Cross-chain bridge transfers and volumes |
| [ESG](#esg) | `models/ESG/` | ~18 | Multiple | Power consumption, carbon emissions |
| [ProbeLab](#probelab) | `models/probelab/` | ~9 | `crawlers_data` | P2P network crawl metrics from ProbeLab |
| [Crawlers](#crawlers) | `models/crawlers/` | ~9 | `crawlers_data` | IP geolocation and network metadata |

## Execution

The execution module is the largest, covering all execution layer blockchain data. It transforms raw blocks, transactions, logs, and traces into analytics-ready datasets.

**Key staging models:**

- `stg_execution__blocks` -- Block headers with timestamps, gas, and proposer
- `stg_execution__transactions` -- Full transaction data
- `stg_execution__logs` -- Smart contract event emissions
- `stg_execution__traces` -- Internal transaction traces

**Key intermediate models:**

- `int_execution_blocks_clients_version_daily` -- Block proposer client distribution over time
- `int_execution_transactions_gas_daily` -- Gas usage trends and fee analytics
- `int_execution_transactions_daily` -- Daily transaction counts and unique addresses
- `int_execution_native_transfers_daily` -- xDAI transfer volume

**Key API models:**

- `api_execution_transactions_daily` -- Transaction statistics endpoint
- `api_execution_transactions_7d` -- Rolling 7-day transaction data
- `api_execution_blocks_daily` -- Block production metrics

## Consensus

The consensus module handles validator lifecycle, attestation participation, and beacon chain events.

**Key staging models:**

- `stg_consensus__blocks` -- Beacon chain blocks with fork version
- `stg_consensus__validators` -- Validator set and balances
- `stg_consensus__attestations` -- Attestation records

**Key intermediate models:**

- `int_consensus_validators_active_daily` -- Active validator count over time
- `int_consensus_attestation_participation_daily` -- Attestation inclusion rates
- `int_consensus_blocks_proposed_daily` -- Block proposal success rates
- `int_consensus_sync_committee_daily` -- Sync committee participation

**Key API models:**

- `api_consensus_validators_active_daily` -- Validator count endpoint
- `api_consensus_attestation_rates_daily` -- Attestation performance

## Contracts

The contracts module contains ABI-decoded smart contract interactions. Each protocol gets its own subdirectory with models for decoded function calls and event logs.

**Structure:**

```
models/contracts/
├── wxdai/                    # Wrapped xDAI contract
├── gnosis_bridge/            # AMB/Omni bridge contracts
├── deposit_contract/         # Validator deposit contract
└── ...                       # Additional protocols
```

**Key capabilities:**

- Decoded function calls from raw transaction input data
- Decoded event logs from raw log topics and data
- Protocol-specific metrics (volume, users, fees)

See [ABI Decoding](abi-decoding.md) for the full workflow.

## P2P

The P2P module analyzes the peer-to-peer network topology using data from the nebula DHT crawler and ip-crawler geolocation enrichment.

**Key intermediate models:**

- `int_p2p_peers_geo_daily` -- Peer geographic distribution
- `int_p2p_client_distribution_daily` -- Client software version distribution
- `int_p2p_peer_count_daily` -- Total reachable peer count

**Key API models:**

- `api_p2p_client_distribution_daily` -- Client diversity endpoint
- `api_p2p_geo_distribution_daily` -- Geographic distribution endpoint

## Bridges

The bridges module tracks cross-chain bridge activity between Gnosis Chain and other networks (primarily Ethereum mainnet).

**Key intermediate models:**

- `int_bridges_transfers_daily` -- Daily bridge transfer counts and volumes
- `int_bridges_unique_users_daily` -- Unique bridge users over time

**Key API models:**

- `api_bridges_transfers_daily` -- Bridge activity endpoint

## ESG

The ESG (Environmental, Social, Governance) module calculates sustainability metrics for the Gnosis Chain network, including power consumption and carbon emissions estimates.

**Data sources:**

- Validator count from the consensus module
- Hardware power consumption estimates
- Electricity carbon intensity data from Ember (via click-runner)

**Key intermediate models:**

- `int_esg_power_consumption_daily` -- Estimated network power usage
- `int_esg_carbon_emissions_daily` -- Carbon footprint calculations

**Key API models:**

- `api_esg_power_consumption_daily` -- Power usage endpoint
- `api_esg_carbon_emissions_daily` -- Carbon emissions endpoint

## ProbeLab

The ProbeLab module transforms daily P2P network metrics provided by [ProbeLab](https://probelab.io/), an external research team that performs independent network measurements.

**Data source:** ProbeLab Parquet files ingested via click-runner from S3.

**Key models:**

- `stg_crawlers__probelab_agent_semvers_avg_1d` -- Agent version statistics
- `stg_crawlers__probelab_agent_types_avg_1d` -- Agent type distribution

## Crawlers

The crawlers module transforms IP geolocation and network metadata data collected by the ip-crawler service.

**Key models:**

- `stg_crawlers__ipinfo` -- Enriched IP geolocation data
- `int_crawlers_geo_distribution_daily` -- Geographic distribution of enriched peers

## Running Specific Modules

```bash
# Run all models in a module
dbt run --select execution
dbt run --select consensus
dbt run --select contracts

# Run a specific model with its upstream dependencies
dbt build --select +api_execution_transactions_daily

# Run all API models across all modules
dbt run --select tag:api

# Run staging models only for a module
dbt run --select execution.staging
```
