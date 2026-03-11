# Contract ABI Decoding

dbt-cerebro includes a system for decoding raw blockchain transaction data into human-readable function calls and events. This enables analysis of specific smart contract interactions without requiring custom parsing for each contract.

## Overview

On the blockchain, transaction input data and event logs are encoded as raw hex bytes. To understand what function was called or what event was emitted, you need the contract's ABI (Application Binary Interface), which describes the structure of each function and event.

The decoding system works in two phases:

1. **Preparation** -- Fetch the contract ABI, generate function/event signatures, and load them as dbt seeds
2. **Runtime** -- Use dbt macros (`decode_calls`, `decode_logs`) to match raw hex data against signatures and extract typed parameters

## Decoding Workflow

```
Step 1: Fetch ABI
    Blockscout API --> contracts_abi table in ClickHouse

Step 2: Export & Generate Signatures
    contracts_abi table --> contracts_abi.csv (seed)
    contracts_abi.csv --> signature_generator.py
    signature_generator.py --> event_signatures.csv (seed)
    signature_generator.py --> function_signatures.csv (seed)

Step 3: Load Seeds
    dbt seed --> function_signatures table
    dbt seed --> event_signatures table

Step 4: Create Decoding Models
    raw transactions + function_signatures --> decode_calls macro --> decoded calls
    raw logs + event_signatures --> decode_logs macro --> decoded events
```

## Step-by-Step Guide

### Step 1: Fetch Contract ABI

Use the `fetch_and_insert_abi` dbt operation to retrieve a contract's ABI from the Blockscout API and store it in the `contracts_abi` table:

```bash
docker exec -it dbt /bin/bash

# Fetch ABI for a single contract
dbt run-operation fetch_and_insert_abi \
  --args '{"address": "0xe91d153e0b41518a2ce8dd3d7944fa863463a97d"}'

# Repeat for additional contracts
dbt run-operation fetch_and_insert_abi \
  --args '{"address": "0xAnotherContractAddress"}'
```

The operation queries the Blockscout API for the contract's verified ABI JSON and inserts it into ClickHouse.

### Step 2: Export ABIs and Generate Signatures

!!! warning
    Always export ABIs before running `dbt seed`. The seed command overwrites the `contracts_abi` table with the contents of the CSV file. If you skip the export step, newly fetched ABIs will be lost.

```bash
# Export current ABIs from ClickHouse to CSV
python scripts/abi/export_contracts_abi.py

# Generate signature files from the exported ABIs
python scripts/signatures/signature_generator.py
```

The signature generator parses each ABI and produces:

- **`seeds/function_signatures.csv`** -- Maps 4-byte function selectors to function names and parameter types
- **`seeds/event_signatures.csv`** -- Maps 32-byte event topic hashes to event names and parameter types

### Step 3: Load Seeds into ClickHouse

```bash
# Load all seed files
dbt seed

# Or load specific seeds
dbt seed --select contracts_abi
dbt seed --select event_signatures
dbt seed --select function_signatures
```

### Step 4: Create Decoding Models

Create dbt models that use the `decode_calls` or `decode_logs` macros to decode raw data for a specific contract.

#### Decoding Event Logs

```sql
-- models/contracts/your_protocol/your_contract_events.sql
{{
    config(
        materialized='incremental',
        incremental_strategy='delete+insert',
        engine='ReplacingMergeTree()',
        order_by='(block_timestamp, log_index)',
        partition_by='toStartOfMonth(block_timestamp)',
        pre_hook=["SET allow_experimental_json_type = 1"]
    )
}}

{{
    decode_logs(
        source_table=source('execution', 'logs'),
        contract_address='0xYourContractAddress',
        output_json_type=true,
        incremental_column='block_timestamp'
    )
}}
```

#### Decoding Function Calls

```sql
-- models/contracts/your_protocol/your_contract_calls.sql
{{
    config(
        materialized='incremental',
        incremental_strategy='delete+insert',
        engine='ReplacingMergeTree()',
        order_by='(block_timestamp, transaction_hash)',
        partition_by='toStartOfMonth(block_timestamp)',
        pre_hook=["SET allow_experimental_json_type = 1"]
    )
}}

{{
    decode_calls(
        source_table=source('execution', 'transactions'),
        contract_address='0xYourContractAddress',
        output_json_type=true,
        incremental_column='block_timestamp'
    )
}}
```

### Step 5: Run the Models

```bash
# Run specific contract models
dbt run --select your_contract_events your_contract_calls

# Or run all contract models
dbt run --select contracts
```

## How the Macros Work

### `decode_logs` Macro

1. Filters the source `logs` table for the specified contract address
2. Extracts `topic0` (the event signature hash) from each log entry
3. Joins against the `event_signatures` seed table to find matching event definitions
4. Parses the remaining topics and `data` field according to the ABI parameter types
5. Outputs decoded event name and typed parameters

### `decode_calls` Macro

1. Filters the source `transactions` table for transactions sent to the specified contract address
2. Extracts the first 4 bytes of `input` data (the function selector)
3. Joins against the `function_signatures` seed table to find matching function definitions
4. Parses the remaining input data according to the ABI parameter types
5. Outputs decoded function name and typed parameters

## Seed Files

| Seed File | Contents | Key Columns |
|-----------|----------|-------------|
| `contracts_abi.csv` | Raw ABI JSON per contract | `contract_address`, `abi_json` |
| `event_signatures.csv` | Event topic-to-name mappings | `signature_hash`, `event_name`, `contract_address`, `inputs` |
| `function_signatures.csv` | Selector-to-name mappings | `selector`, `function_name`, `contract_address`, `inputs` |

## Safe Workflow Summary

The correct order of operations when adding new contracts:

```bash
# 1. Fetch ABI from Blockscout
dbt run-operation fetch_and_insert_abi --args '{"address": "0x..."}'

# 2. Export ABIs to CSV (prevents data loss from dbt seed)
python scripts/abi/export_contracts_abi.py

# 3. Generate signature CSVs
python scripts/signatures/signature_generator.py

# 4. Load seeds (safe now because CSVs are up to date)
dbt seed

# 5. Run decoding models
dbt run --select contracts
```

## Troubleshooting

**Empty decoded tables** -- Verify that the contract address matches exactly (case-sensitive hex), signatures were generated and seeded, and raw data exists for the target time period.

**Missing ABI after seed** -- You ran `dbt seed` without first exporting. Re-fetch the ABI and follow the safe workflow above.

**Signature generation fails** -- Check that ABIs exist in ClickHouse (`SELECT COUNT(*) FROM contracts_abi`) and that the JSON is valid (`SELECT contract_address FROM contracts_abi WHERE NOT isValidJSON(abi_json)`).
