# cryo-indexer

The cryo-indexer is the primary execution layer indexer for the Gnosis Analytics pipeline. It extracts blockchain data from an RPC node using the [Cryo](https://github.com/paradigmxyz/cryo) binary (a high-performance Rust data extraction tool) and loads it into ClickHouse.

## Purpose

cryo-indexer handles the full lifecycle of execution layer data acquisition:

- Real-time indexing of new blocks as they are produced
- Historical bulk loading of past block ranges
- Automatic recovery from failures and incomplete ranges
- Validation of data integrity

## Architecture

```
Blockchain RPC --> Cryo Binary --> Parquet Files --> ClickHouse
                                        |
                                  Worker Process
                                        |
                                  State Manager
                                        |
                                indexing_state table
```

The indexer orchestrates the Cryo binary to extract data from the RPC node into intermediate Parquet files, which are then loaded into ClickHouse. A single `indexing_state` table in ClickHouse serves as the source of truth for all processing state.

### Key Design Decisions

- **Blocks first** -- Block headers are always processed before other datasets, because downstream datasets require valid block timestamps.
- **1000-block chunks** -- All processing uses fixed 1000-block ranges for predictable resource usage.
- **Atomic ranges** -- A range is either fully completed or marked as failed. No partial writes.
- **Single state table** -- The `indexing_state` table tracks all datasets and ranges in one place.

## Datasets

cryo-indexer supports 11 datasets organized into four indexing modes:

### Indexing Modes

| Mode | Datasets Included | Use Case | Approx. Storage per 1M Blocks |
|------|-------------------|----------|-------------------------------|
| **minimal** (default) | blocks, transactions, logs | Standard DeFi/DApp analysis | ~50 GB |
| **extra** | contracts, native_transfers, traces | Contract and trace analysis | ~100 GB |
| **diffs** | balance_diffs, code_diffs, nonce_diffs, storage_diffs | State change tracking | ~200 GB |
| **full** | All 11 datasets | Complete blockchain analysis | ~500 GB |
| **custom** | User-defined | Tailored to specific needs | Variable |

### Dataset Reference

| Dataset | Description | ClickHouse Table |
|---------|-------------|-----------------|
| `blocks` | Block headers, timestamps, gas, withdrawals root | `blocks` |
| `transactions` | Transaction data including gas, value, status, input | `transactions` |
| `logs` | Smart contract event log emissions | `logs` |
| `contracts` | Contract creation events | `contracts` |
| `native_transfers` | xDAI/ETH native token transfers | `native_transfers` |
| `traces` | Internal transaction execution traces | `traces` |
| `balance_diffs` | Account balance state changes per block | `balance_diffs` |
| `code_diffs` | Smart contract bytecode changes | `code_diffs` |
| `nonce_diffs` | Account nonce changes | `nonce_diffs` |
| `storage_diffs` | Contract storage slot changes | `storage_diffs` |
| `withdrawals` | Validator withdrawals (auto-populated with blocks) | `withdrawals` |

!!! note
    The `withdrawals` dataset is automatically populated whenever blocks are processed. It does not require a separate extraction step.

## Operation Modes

### Continuous (Default)

Real-time blockchain following for production deployments.

- Polls the chain tip every 10 seconds (configurable via `POLL_INTERVAL`)
- Waits for 12 block confirmations before indexing (configurable via `CONFIRMATION_BLOCKS`) to avoid reorg issues
- Processes in small batches (default 100 blocks) for low latency
- Single-threaded for stability
- Automatically resumes from the last indexed block on restart
- Resets stale processing jobs on startup

```bash
make continuous
# Or with custom settings:
make continuous MODE=full START_BLOCK=18000000
```

### Historical

Fast bulk indexing for initial sync or backfilling specific block ranges.

- Supports parallel processing with multiple workers
- Automatically divides work into 1000-block chunks
- Built-in progress tracking with ETA calculations
- Strict timestamp validation at each step

```bash
make historical START_BLOCK=1000000 END_BLOCK=2000000 WORKERS=8
```

### Maintain

Processes failed and pending ranges from the state table.

- Scans `indexing_state` for ranges marked as `failed` or `pending`
- Re-attempts each range with proper error handling
- Reports what was fixed and any remaining issues

```bash
make maintain
# Or for a specific range:
make maintain START_BLOCK=1000000 END_BLOCK=2000000 WORKERS=4
```

### Validate (Read-Only)

Checks indexing progress and data integrity without modifying data.

```bash
make status
```

## Configuration

### Required Settings

| Variable | Description |
|----------|-------------|
| `ETH_RPC_URL` | Blockchain RPC endpoint URL |
| `CLICKHOUSE_HOST` | ClickHouse server hostname |
| `CLICKHOUSE_PASSWORD` | ClickHouse authentication password |

### Core Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `NETWORK_NAME` | `ethereum` | Network name passed to Cryo |
| `CLICKHOUSE_USER` | `default` | ClickHouse username |
| `CLICKHOUSE_DATABASE` | `blockchain` | Target database name (auto-created) |
| `CLICKHOUSE_PORT` | `8443` | ClickHouse HTTP port |
| `CLICKHOUSE_SECURE` | `true` | Use HTTPS for ClickHouse connection |

### Operation Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `OPERATION` | `continuous` | Operation mode: `continuous`, `historical`, `maintain`, `validate` |
| `MODE` | `minimal` | Indexing mode: `minimal`, `extra`, `diffs`, `full`, `custom` |
| `DATASETS` | (derived from MODE) | Comma-separated dataset list (for custom mode) |
| `START_BLOCK` | `0` | Starting block number |
| `END_BLOCK` | `0` | Ending block number (0 = chain tip) |

### Performance Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `WORKERS` | `1` | Number of parallel workers (use 4-16 for historical) |
| `BATCH_SIZE` | `100` | Blocks per processing batch |
| `MAX_RETRIES` | `3` | Maximum retry attempts with exponential backoff |
| `REQUESTS_PER_SECOND` | `20` | RPC request rate limit |
| `MAX_CONCURRENT_REQUESTS` | `2` | Maximum concurrent RPC requests |
| `CRYO_TIMEOUT` | `600` | Cryo command timeout in seconds |
| `CONFIRMATION_BLOCKS` | `12` | Blocks to wait before indexing (reorg safety) |
| `POLL_INTERVAL` | `10` | Seconds between chain tip polls |

## State Management

All indexing state is tracked in the `indexing_state` table:

```sql
-- Composite key: (mode, dataset, start_block, end_block)
-- Status flow: pending -> processing -> completed | failed
```

| Field | Description |
|-------|-------------|
| `mode` | Indexing mode that created this range |
| `dataset` | Dataset name (blocks, transactions, etc.) |
| `start_block`, `end_block` | Block range boundaries |
| `status` | Current state: `pending`, `processing`, `completed`, `failed` |
| `worker_id` | ID of the worker processing this range |
| `attempt_count` | Number of processing attempts |
| `rows_indexed` | Number of rows inserted |
| `error_message` | Error details if status is `failed` |

On startup, all ranges stuck in `processing` state are automatically reset to `pending`, enabling self-healing after crashes.

## Docker Deployment

```bash
# Build
docker-compose build

# Run migrations
docker-compose --profile migrations up migrations

# Start continuous indexing (minimal mode)
docker-compose up cryo-indexer-minimal

# Historical backfill
OPERATION=historical START_BLOCK=18000000 END_BLOCK=18100000 \
  docker-compose --profile historical up historical-job
```

## Typical Deployment Workflow

1. **Initial setup** -- Build the image and run database migrations
2. **Historical sync** -- Bulk-load the desired block range with multiple workers
3. **Maintenance pass** -- Run `maintain` to retry any failed ranges
4. **Switch to continuous** -- Start following the chain tip in real time
5. **Periodic maintenance** -- Occasionally run `maintain` to clear any accumulated failures

## ClickHouse Table Schemas

All tables are stored in the `execution` database.

??? note "Table: `execution.blocks`"
    **Engine:** ReplacingMergeTree(insert_version)
    **PARTITION BY:** toStartOfMonth(block_timestamp)
    **ORDER BY:** (block_number)

    | Column | Type | Notes |
    |--------|------|-------|
    | `block_number` | UInt32 (Nullable) | Block height |
    | `block_hash` | String (Nullable) | Block hash |
    | `parent_hash` | String (Nullable) | Parent block hash |
    | `author` | String (Nullable) | Block author / miner |
    | `state_root` | String (Nullable) | State trie root hash |
    | `gas_used` | UInt64 (Nullable) | Total gas used in block |
    | `gas_limit` | UInt64 (Nullable) | Block gas limit |
    | `timestamp` | UInt32 (Nullable) | Unix timestamp |
    | `size` | UInt64 (Nullable) | Block size in bytes |
    | `base_fee_per_gas` | UInt64 (Nullable) | EIP-1559 base fee |
    | `withdrawals_root` | String (Nullable) | Withdrawals trie root |
    | `chain_id` | UInt64 (Nullable) | Chain identifier |
    | `block_timestamp` | DateTime | Materialized from `timestamp` |
    | `insert_version` | UInt64 | Materialized; deduplication version |

??? note "Table: `execution.transactions`"
    **Engine:** ReplacingMergeTree(insert_version)
    **PARTITION BY:** toStartOfMonth(block_timestamp)
    **ORDER BY:** (block_number, transaction_index)

    | Column | Type | Notes |
    |--------|------|-------|
    | `block_number` | UInt32 (Nullable) | Block height |
    | `transaction_index` | UInt64 (Nullable) | Position within the block |
    | `transaction_hash` | String (Nullable) | Transaction hash |
    | `nonce` | UInt64 (Nullable) | Sender nonce |
    | `from_address` | String (Nullable) | Sender address |
    | `to_address` | String (Nullable) | Recipient address |
    | `value_string` | String (Nullable) | Transfer value (string) |
    | `value_f64` | Float64 (Nullable) | Transfer value (float) |
    | `input` | String (Nullable) | Calldata |
    | `gas_limit` | UInt64 (Nullable) | Gas limit |
    | `gas_used` | UInt64 (Nullable) | Gas consumed |
    | `gas_price` | UInt64 (Nullable) | Gas price in wei |
    | `transaction_type` | UInt32 (Nullable) | EIP-2718 transaction type |
    | `max_priority_fee_per_gas` | UInt64 (Nullable) | EIP-1559 priority fee |
    | `max_fee_per_gas` | UInt64 (Nullable) | EIP-1559 max fee |
    | `success` | UInt8 (Nullable) | 1 = success, 0 = revert |
    | `chain_id` | UInt64 (Nullable) | Chain identifier |
    | `block_timestamp` | DateTime64(0, 'UTC') | Block timestamp |
    | `insert_version` | UInt64 | Materialized; deduplication version |

??? note "Table: `execution.logs`"
    **Engine:** ReplacingMergeTree(insert_version)
    **ORDER BY:** (block_number, transaction_index, log_index)

    | Column | Type | Notes |
    |--------|------|-------|
    | `block_number` | UInt32 (Nullable) | Block height |
    | `log_index` | UInt32 (Nullable) | Log position within the block |
    | `transaction_hash` | String (Nullable) | Parent transaction hash |
    | `address` | String (Nullable) | Emitting contract address |
    | `topic0` | String (Nullable) | Event signature hash |
    | `topic1` | String (Nullable) | Indexed parameter 1 |
    | `topic2` | String (Nullable) | Indexed parameter 2 |
    | `topic3` | String (Nullable) | Indexed parameter 3 |
    | `data` | String (Nullable) | Non-indexed event data |
    | `chain_id` | UInt64 (Nullable) | Chain identifier |
    | `block_timestamp` | DateTime64(0, 'UTC') | Block timestamp |
    | `insert_version` | UInt64 | Materialized; deduplication version |

??? note "Table: `execution.traces`"
    **Engine:** ReplacingMergeTree(insert_version)
    **ORDER BY:** (block_number, transaction_index, trace_address)

    | Column | Type | Notes |
    |--------|------|-------|
    | `action_from` | String (Nullable) | Caller address |
    | `action_to` | String (Nullable) | Callee address |
    | `action_value` | String (Nullable) | Value transferred |
    | `action_gas` | String (Nullable) | Gas provided |
    | `action_input` | String (Nullable) | Input data |
    | `action_call_type` | String (Nullable) | Call type (call, delegatecall, etc.) |
    | `action_type` | String (Nullable) | Trace action type |
    | `result_gas_used` | UInt32 (Nullable) | Gas consumed by trace |
    | `result_output` | String (Nullable) | Return data |
    | `result_code` | String (Nullable) | Deployed bytecode (create traces) |
    | `result_address` | String (Nullable) | Created contract address |
    | `trace_address` | String (Nullable) | Position in the trace tree |
    | `subtraces` | UInt32 (Nullable) | Number of child traces |
    | `transaction_index` | UInt32 (Nullable) | Transaction position in block |
    | `block_number` | UInt32 (Nullable) | Block height |
    | `error` | String (Nullable) | Error message if trace reverted |
    | `chain_id` | UInt64 (Nullable) | Chain identifier |
    | `block_timestamp` | DateTime64 | Block timestamp |
    | `insert_version` | UInt64 | Materialized; deduplication version |

??? note "Table: `execution.contracts`"
    **Engine:** ReplacingMergeTree(insert_version)
    **ORDER BY:** (block_number, create_index)

    | Column | Type | Notes |
    |--------|------|-------|
    | `block_number` | UInt32 (Nullable) | Block height |
    | `contract_address` | String (Nullable) | Deployed contract address |
    | `deployer` | String (Nullable) | EOA that initiated the deploy |
    | `factory` | String (Nullable) | Factory contract (if created via CREATE2) |
    | `code` | String (Nullable) | Deployed bytecode |
    | `code_hash` | String (Nullable) | Keccak256 of bytecode |
    | `chain_id` | UInt64 (Nullable) | Chain identifier |
    | `block_timestamp` | DateTime64 | Block timestamp |
    | `insert_version` | UInt64 | Materialized; deduplication version |

??? note "Table: `execution.native_transfers`"
    **Engine:** ReplacingMergeTree(insert_version)
    **ORDER BY:** (block_number, transfer_index)

    | Column | Type | Notes |
    |--------|------|-------|
    | `block_number` | UInt32 (Nullable) | Block height |
    | `transfer_index` | UInt32 (Nullable) | Transfer position in block |
    | `transaction_hash` | String (Nullable) | Parent transaction hash |
    | `from_address` | String (Nullable) | Sender address |
    | `to_address` | String (Nullable) | Recipient address |
    | `value_string` | String (Nullable) | Transfer value (string) |
    | `value_f64` | Float64 (Nullable) | Transfer value (float) |
    | `chain_id` | UInt64 | Chain identifier |
    | `block_timestamp` | DateTime64 | Block timestamp |
    | `insert_version` | UInt64 | Materialized; deduplication version |

??? note "Table: `execution.balance_diffs`"
    **Engine:** ReplacingMergeTree(insert_version)
    **ORDER BY:** (block_number, transaction_index, address)

    | Column | Type | Notes |
    |--------|------|-------|
    | `block_number` | UInt32 | Block height |
    | `transaction_index` | UInt32 | Transaction position in block |
    | `address` | String | Account address |
    | `from_value_f64` | Float64 | Balance before the change |
    | `to_value_f64` | Float64 | Balance after the change |
    | `block_timestamp` | DateTime64 | Block timestamp |
    | `insert_version` | UInt64 | Materialized; deduplication version |

??? note "Table: `execution.withdrawals`"
    **Engine:** ReplacingMergeTree(insert_version)
    **ORDER BY:** (block_number, withdrawal_index)

    | Column | Type | Notes |
    |--------|------|-------|
    | `block_number` | UInt32 | Block height |
    | `withdrawal_index` | String | Withdrawal sequence index |
    | `validator_index` | String | Validator that triggered the withdrawal |
    | `address` | String | Recipient address |
    | `amount` | String | Withdrawal amount |
    | `block_timestamp` | DateTime64 | Block timestamp |
    | `insert_version` | UInt64 | Materialized; deduplication version |

??? note "Table: `execution.indexing_state`"
    **Engine:** ReplacingMergeTree(insert_version)
    **ORDER BY:** (mode, dataset, start_block)

    | Column | Type | Notes |
    |--------|------|-------|
    | `mode` | String | Indexing mode (minimal, extra, etc.) |
    | `dataset` | String | Dataset name (blocks, transactions, etc.) |
    | `start_block` | UInt32 | Range start block |
    | `end_block` | UInt32 | Range end block |
    | `status` | String | pending / processing / completed / failed |
    | `worker_id` | String | ID of the processing worker |
    | `attempt_count` | UInt8 | Number of processing attempts |
    | `created_at` | DateTime | Range creation timestamp |
    | `completed_at` | DateTime (Nullable) | Completion timestamp |
    | `rows_indexed` | UInt64 (Nullable) | Number of rows inserted |
    | `error_message` | String (Nullable) | Error details if failed |
