# beacon-indexer

The beacon-indexer is a consensus layer indexer that fetches data from a beacon node REST API and stores it in ClickHouse or Parquet files. It follows an ELT (Extract, Load, Transform) pattern with fork-aware parsing and automatic network detection.

## Purpose

beacon-indexer handles the acquisition of all consensus layer data:

- Validator sets, balances, and status changes
- Block proposals and attestations
- Sync committee participation
- Rewards and penalties
- Deposits, withdrawals, and voluntary exits

## Architecture

The indexer operates in two distinct phases:

```
Phase 1: Load (Extract + Load)
    Beacon Node REST API --> Raw JSON --> ClickHouse raw_* tables

Phase 2: Transform
    raw_* tables --> Fork-aware parsing --> Structured tables
```

This ELT separation means raw data is preserved exactly as received from the beacon API. Transformation logic can be updated and re-run independently without re-fetching data from the beacon node.

## Storage Backends

beacon-indexer supports two storage backends, selected via the `STORAGE_BACKEND` environment variable:

| Backend | Best For | Setup Required |
|---------|----------|----------------|
| **ClickHouse** | Production systems, real-time analytics, complex queries | Database migration |
| **Parquet** | Data analysis, ETL pipelines, archival storage, development | None |

The ClickHouse backend provides fork-aware chunk-based processing with concurrent access and monitoring. The Parquet backend produces portable columnar files compatible with pandas, DuckDB, and Spark.

## Fork Awareness

The beacon chain has undergone multiple protocol upgrades (forks), each introducing new data fields and structures. beacon-indexer automatically detects the fork version for each slot and applies the appropriate parser.

| Fork | Key Changes for Indexing |
|------|--------------------------|
| **Phase 0** | Base beacon chain: blocks, attestations, deposits, voluntary exits |
| **Altair** | Sync committee data, participation metrics |
| **Bellatrix** | Execution payloads (The Merge) |
| **Capella** | Validator withdrawals, BLS-to-execution changes |
| **Deneb** | Blob KZG commitments, blob sidecar data |
| **Electra** | Execution layer requests (deposit, withdrawal, consolidation) |

## Supported Networks

| Network | Slot Time | Slots per Epoch | Detection |
|---------|-----------|-----------------|-----------|
| **Mainnet** | 12 seconds | 32 | Automatic |
| **Gnosis Chain** | 5 seconds | 16 | Automatic |
| **Holesky** | 12 seconds | 32 | Automatic |
| **Sepolia** | 12 seconds | 32 | Automatic |

Network parameters are auto-detected from the beacon chain genesis data. No manual configuration is required.

## Operations

### Migration

Creates the database schema (ClickHouse backend only):

```bash
make migration
```

### Backfill

Loads historical raw data from the beacon API for a specified slot range:

```bash
make backfill
```

### Transform

Parses raw data into structured tables with fork-appropriate field extraction:

```bash
make transform
```

### Real-time

Continuously follows the chain head, loading new slots as they are produced:

```bash
make realtime
```

### Maintenance

The maintenance system provides tools for data integrity checking and recovery:

```bash
# Check system health
make maintenance-status

# Find and fix failed chunks
make maintenance-fix

# Fix recent failures (last week)
make maintenance-fix-recent

# Analyze data gaps
make maintenance-gaps
```

Maintenance supports dry-run mode (`--dry-run`) to preview what would be changed without modifying data.

## Configuration

### Required Settings

| Variable | Description |
|----------|-------------|
| `BEACON_NODE_URL` | Beacon node REST API endpoint |
| `STORAGE_BACKEND` | `clickhouse` or `parquet` |

### ClickHouse Settings (when using ClickHouse backend)

| Variable | Default | Description |
|----------|---------|-------------|
| `CLICKHOUSE_HOST` | -- | ClickHouse server hostname |
| `CLICKHOUSE_PASSWORD` | -- | Authentication password |
| `CLICKHOUSE_PORT` | `8443` | HTTP port |
| `CLICKHOUSE_USER` | `default` | Username |
| `CLICKHOUSE_DATABASE` | `consensus` | Target database |
| `CLICKHOUSE_SECURE` | `true` | Use HTTPS |

### Parquet Settings (when using Parquet backend)

| Variable | Default | Description |
|----------|---------|-------------|
| `PARQUET_OUTPUT_DIR` | `./parquet_data` | Output directory for Parquet files |

### Processing Settings

| Variable | Description |
|----------|-------------|
| `ENABLED_LOADERS` | Comma-separated list of data loaders to enable (blocks, validators, rewards, etc.) |
| `CHUNK_SIZE` | Number of slots per processing chunk |

## Data Flow

1. **Load phase** -- The backfill or realtime command fetches raw beacon API responses and stores them in `raw_*` tables (ClickHouse) or raw Parquet files.
2. **Transform phase** -- The transform command reads raw data, detects the fork version for each slot, and writes parsed data into structured tables (blocks, validators, attestations, etc.).
3. **State tracking** -- Chunk-based state tracking records which slot ranges have been loaded and transformed, enabling resumability.

## Docker Deployment

```bash
# Build the image
make build

# Run the full pipeline
make migration       # Create schema (ClickHouse only)
make backfill        # Load historical data
make transform       # Parse raw data
make realtime        # Follow chain head

# Maintenance
make maintenance-status
make maintenance-fix
```

## ClickHouse Table Schemas

All tables are stored in the `consensus` database.

??? note "Table: `consensus.blocks`"
    **Engine:** ReplacingMergeTree(insert_version)
    **ORDER BY:** (slot)

    | Column | Type | Notes |
    |--------|------|-------|
    | `slot` | UInt64 | Beacon chain slot number |
    | `proposer_index` | UInt64 | Validator that proposed the block |
    | `parent_root` | String | Parent block root hash |
    | `state_root` | String | State root hash |
    | `signature` | String | Block signature |
    | `version` | String | Fork version (phase0, altair, etc.) |
    | `graffiti` | String | Proposer graffiti field |
    | `eth1_deposit_count` | UInt64 | Cumulative ETH1 deposit count |
    | `sync_aggregate_participation` | UInt64 | Sync committee participation bits |
    | `withdrawals_count` | UInt32 | Number of withdrawals in block |
    | `blob_kzg_commitments_count` | UInt32 | Number of blob KZG commitments |
    | `slot_timestamp` | DateTime64 | Materialized from slot and genesis time |
    | `insert_version` | UInt64 | Materialized; deduplication version |

??? note "Table: `consensus.attestations`"
    **Engine:** ReplacingMergeTree(insert_version)
    **ORDER BY:** (slot, attestation_index, committee_index)

    | Column | Type | Notes |
    |--------|------|-------|
    | `slot` | UInt64 | Slot the attestation was included in |
    | `attestation_index` | UInt64 | Position within the block |
    | `aggregation_bits` | String | Bitfield of participating validators |
    | `signature` | String | Aggregated BLS signature |
    | `attestation_slot` | UInt64 | Slot being attested to |
    | `committee_index` | UInt64 | Committee index |
    | `beacon_block_root` | String | Attested beacon block root |
    | `source_epoch` | UInt64 | Justified checkpoint epoch |
    | `target_epoch` | UInt64 | Target checkpoint epoch |
    | `source_root` | String | Justified checkpoint root |
    | `target_root` | String | Target checkpoint root |
    | `slot_timestamp` | DateTime64 | Materialized from slot |

??? note "Table: `consensus.validators`"
    **Engine:** ReplacingMergeTree(insert_version)
    **ORDER BY:** (slot, validator_index)

    | Column | Type | Notes |
    |--------|------|-------|
    | `slot` | UInt64 | Snapshot slot |
    | `validator_index` | UInt32 | Unique validator index |
    | `balance` | UInt64 | Current balance in Gwei |
    | `status` | String | Validator lifecycle status |
    | `pubkey` | String | BLS public key |
    | `effective_balance` | UInt64 | Effective balance in Gwei |
    | `slashed` | UInt8 | 1 = slashed, 0 = not slashed |
    | `activation_epoch` | UInt64 | Epoch when validator activated |
    | `exit_epoch` | UInt64 | Epoch when validator exited |
    | `withdrawable_epoch` | UInt64 | Epoch when balance is withdrawable |
    | `slot_timestamp` | DateTime64 | Materialized from slot |

??? note "Table: `consensus.rewards`"
    **Engine:** ReplacingMergeTree(insert_version)
    **ORDER BY:** (slot, proposer_index)

    | Column | Type | Notes |
    |--------|------|-------|
    | `slot` | UInt64 | Slot number |
    | `proposer_index` | UInt64 | Proposing validator index |
    | `total` | UInt64 | Total reward amount |
    | `attestations` | UInt64 | Reward from attestation inclusion |
    | `sync_aggregate` | UInt64 | Reward from sync committee |
    | `proposer_slashings` | UInt64 | Reward from proposer slashings |
    | `attester_slashings` | UInt64 | Reward from attester slashings |

??? note "Table: `consensus.raw_blocks` / `consensus.raw_validators` / `consensus.raw_rewards`"
    **Engine:** ReplacingMergeTree
    **ORDER BY:** (slot, payload_hash)

    | Column | Type | Notes |
    |--------|------|-------|
    | `slot` | UInt64 | Beacon chain slot number |
    | `payload` | String | Full JSON response from beacon API |
    | `payload_hash` | String | Hash of the payload for deduplication |
    | `retrieved_at` | DateTime | Timestamp when data was fetched |

??? note "Table: `consensus.specs`"
    **Engine:** ReplacingMergeTree(updated_at)
    **ORDER BY:** (parameter_name)

    | Column | Type | Notes |
    |--------|------|-------|
    | `parameter_name` | String | Beacon chain spec parameter name |
    | `parameter_value` | String | Parameter value |
    | `updated_at` | DateTime64 | Last update timestamp |

??? note "Table: `consensus.genesis`"
    **Engine:** ReplacingMergeTree()
    **ORDER BY:** (genesis_time)

    | Column | Type | Notes |
    |--------|------|-------|
    | `genesis_time` | DateTime64 | Chain genesis timestamp |
    | `genesis_validators_root` | String | Merkle root of genesis validators |
    | `genesis_fork_version` | String | Fork version at genesis |
