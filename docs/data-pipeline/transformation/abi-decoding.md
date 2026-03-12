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

---

## EVM ABI Encoding — The Byte Layout

Understanding the raw byte layout is essential for decoding any log or call manually.

### Type Categories

**Static types** are encoded inline in their 32-byte head slot:

| Solidity Type | Encoding |
|--------------|----------|
| `address` | Zero-padded to 32 bytes on the left; actual 20-byte address in the last 40 hex chars |
| `uint256` / `int256` | Big-endian 32-byte integer |
| `uint8`–`uint128` | Same as `uint256` (padded to 32 bytes) |
| `bytes32` | Stored as-is (right-padded if < 32 bytes) |
| `bool` | 1 byte value padded to 32 bytes (`0x00..01` or `0x00..00`) |

**Dynamic types** have a head slot storing a byte-offset pointing to the tail:

| Solidity Type | Head |
|--------------|------|
| `string` | byte offset (32 bytes) |
| `bytes` | byte offset (32 bytes) |
| `uint256[]` | byte offset (32 bytes) |
| `address[]` | byte offset (32 bytes) |

### Head/Tail Layout

For N parameters, the ABI encoding is:

```
[word 0: head slot for param 0]   ← 32 bytes
[word 1: head slot for param 1]   ← 32 bytes
...
[word N-1: head slot for param N-1]
[tail data for dynamic params...]  ← variable length
```

Static params store their value directly in the head slot. Dynamic params store a byte offset (relative to the start of the encoding) pointing to their data in the tail section.

**Example:** `transfer(address to, uint256 amount)` — both static, so calldata is:

```
[4 bytes: selector a9059cbb]
[32 bytes: to address, zero-padded]
[32 bytes: amount, big-endian uint256]
```

### Function Selectors

- `keccak256` of canonical signature `"functionName(type1,type2,...)"` (no spaces, canonical types)
- Take first 4 bytes = first 8 hex chars
- Example: `transfer(address,uint256)` → `a9059cbb`
- In `execution.transactions`: `input` has no `0x` prefix, so selector = `substring(input, 1, 8)`

### Event Topics

- `topic0` = full 32-byte keccak256 of `"EventName(type1,type2,...)"` — the event signature hash
- **Indexed** parameters (max 3) go into `topic1`, `topic2`, `topic3` — each padded to 32 bytes
- **Non-indexed** parameters ABI-encoded together in the `data` field
- In `execution.logs`: topics and data stored **without `0x` prefix**

### Worked Example: Decoding a Transfer

`Transfer(address indexed from, address indexed to, uint256 value)`:

```
topic0 = ddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef
topic1 = 000000000000000000000000AAAA...AAAA   (from address, 32 bytes)
topic2 = 000000000000000000000000BBBB...BBBB   (to address)
data   = 00000000000000000000000000000000000000000000152D02C7E14AF6800000
         (1000 tokens × 1e18)
```

Decoding:

- `from` = `right(topic1, 40)` = `aaaa...aaaa`
- `to` = `right(topic2, 40)` = `bbbb...bbbb`
- `value` = `reinterpretAsUInt256(reverse(unhex(substring(data, 1, 64))))` = `1000000000000000000000`

---

## How the Macros Work Internally

### `decode_logs` — Step by Step

1. **Address normalization** — Input address(es) lowercased and `0x` stripped defensively:
    ```sql
    lower(replaceAll(address_column, '0x', ''))
    ```
    Supports: single address string, array of addresses, or `contract_address_ref` (JOIN to `contracts_whitelist` filtered by `contract_type_filter`).

2. **Event signature lookup** — JOIN `event_signatures` table:
    ```sql
    JOIN event_signatures es
    ON lower(replaceAll(l.topic0, '0x', '')) = es.signature
    ```
    Retrieves: `event_name`, `names` (array of param names), `types` (array of Solidity types), `indexed_flags` (array of bools).

3. **Log deduplication** — `execution.logs` can have multiple insert versions for the same log entry (due to reorgs or re-indexing). Keep the latest:
    ```sql
    ROW_NUMBER() OVER (
        PARTITION BY block_number, transaction_index, log_index
        ORDER BY insert_version DESC
    ) = 1
    ```

4. **Incremental filter** — For incremental dbt runs, filters new data only:
    ```sql
    WHERE block_timestamp > (SELECT max(block_timestamp) - INTERVAL 1 HOUR FROM this)
    ```

5. **Data word extraction** — Split `data` field into 32-byte chunks:
    ```sql
    splitByLength(unhex(data), 32)
    ```
    Assumes no `0x` prefix — confirmed true for `execution.logs`.

6. **Indexed parameter decoding** (from `topic1`/`topic2`/`topic3`):
    - `address` type: `'0x' || lower(right(topic_n, 40))` — last 20 bytes
    - `uint*` / `int*`: `toString(reinterpretAsUInt256(reverse(unhex(topic_n))))`
    - `bytes32`: `'0x' || lower(topic_n)` — full 32 bytes

7. **Non-indexed parameter decoding** (from data words array):
    - **Static** (`address`, `uint*`, `int*`, `bytes32`): read `word[i]` directly, same conversions as above
    - **Dynamic** (`string`, `bytes`): `word[i]` = byte offset → convert to word index → read length word → read data bytes → convert hex to UTF-8 (for `string`) or add `0x` prefix (for `bytes`)
    - **Arrays** (`address[]`, `uint256[]`): `word[i]` = offset → word at offset = element count → read N elements

8. **String finalization**:
    ```sql
    replaceRegexpAll(reinterpretAsString(unhex(hex_data)), '\0', '')
    ```
    Removes null padding bytes from UTF-8 strings.

9. **Map assembly** — Interleave indexed and non-indexed decoded values back into their original ABI position order using the `indexed_flags` array to route each param to the right slot.

10. **Output** — Depending on `output_json_type` flag:
    - `true` → native ClickHouse `Map(String, String)` (enables `decoded_params['key']` syntax)
    - `false` → JSON string via `toJSONString(map(...))`
    - Final columns: `block_number`, `block_timestamp`, `transaction_hash`, `transaction_index`, `log_index`, `contract_address`, `event_name`, `decoded_params`

### `decode_calls` — Step by Step

1. **Transaction filtering** — Filter to transactions where `to_address` matches the contract (normalized, lowercase, no `0x`).

2. **Selector extraction** — `input` column has **no `0x` prefix**:
    ```sql
    lower(substring(input, 1, 8))
    ```
    = first 4 bytes = function selector.

3. **Function signature lookup**:
    ```sql
    JOIN function_signatures fs
    ON selector = lower(substring(input, 1, 8))
    ```
    Retrieves: `function_name`, `names`, `types`.

4. **Deduplication**:
    ```sql
    PARTITION BY block_number, transaction_index ORDER BY insert_version DESC
    ```

5. **Arg extraction** — Everything after the 4-byte selector:
    ```sql
    substring(input, 9)
    ```
    = ABI-encoded arguments (no `0x` prefix).

6. **Arg decoding** — Same head/tail logic as non-indexed log params (steps 5–8 from `decode_logs`).

7. **Output** — `block_number`, `block_timestamp`, `transaction_hash`, `nonce`, `gas_price`, `value`, `function_name`, `decoded_input` `Map(String, String)`

---

## On-the-Fly Decoding (Without dbt Models)

This section enables agents to decode any contract's events or calls using only raw SQL, without waiting for a dbt model to be built.

### Column Format Reference

!!! warning "No `0x` prefix in execution tables"
    The following columns are stored **without** the `0x` prefix (lowercase hex):

    - `execution.logs`: `address`, `topic0`, `topic1`, `topic2`, `topic3`, `data`
    - `execution.transactions`: `input`, `to`, `from`, `hash`

    But `event_signatures.contract_address` and `function_signatures.contract_address` are stored **with `0x`**.

### Signature Lookup

```sql
-- Find event name and parameter layout from a topic0 value
SELECT
    signature,          -- 64-char hex, no 0x
    event_name,
    names,              -- Array(String) of param names
    types,              -- Array(String) of Solidity types
    indexed_flags       -- Array(UInt8): 1 = indexed (in topics), 0 = non-indexed (in data)
FROM event_signatures
WHERE signature = 'ddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'
-- Optionally filter to a specific contract:
-- AND lower(contract_address) = lower('0xContractAddress')   ← contract_address HAS 0x
```

```sql
-- Find function name and parameter layout from a transaction input
SELECT
    signature,          -- 8-char hex selector, no 0x
    function_name,
    names,
    types
FROM function_signatures
WHERE signature = lower(substring(input, 1, 8))
-- AND lower(contract_address) = lower('0xContractAddress')   ← contract_address HAS 0x
-- Run against: FROM execution.transactions WHERE hash = '...'
```

### ClickHouse Hex Utility Cheat Sheet

| Operation | Expression |
|-----------|-----------|
| topic/data 32-byte word → uint256 | `reinterpretAsUInt256(reverse(unhex(word_hex_64chars)))` |
| topic → address (last 20 bytes) | `'0x' \|\| lower(right(topic1, 40))` |
| data word N (0-indexed, no 0x) | `substring(data, N*64+1, 64)` |
| data word N → uint256 | `reinterpretAsUInt256(reverse(unhex(substring(data, N*64+1, 64))))` |
| data word N → address | `'0x' \|\| lower(right(substring(data, N*64+1, 64), 40))` |
| hex bytes → UTF-8 string (strip nulls) | `replaceRegexpAll(reinterpretAsString(unhex(hex_str)), '\\0', '')` |
| dynamic type byte-offset → word index | `toUInt64(reinterpretAsUInt256(reverse(unhex(word_hex)))) / 32` |
| split data into 32-byte word array | `splitByLength(unhex(data), 32)` |
| int256 from two's complement | `reinterpretAsInt256(reverse(unhex(word_hex)))` |

### Full Example: Inline Transfer Decode

```sql
-- ERC-20 Transfer(address indexed from, address indexed to, uint256 value)
-- topic0 (no 0x): ddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef
-- topic1 = from (indexed address, padded to 32 bytes)
-- topic2 = to   (indexed address, padded to 32 bytes)
-- data   = value (single uint256, 32 bytes)
-- All columns stored without 0x prefix in execution.logs

SELECT
    block_timestamp,
    transaction_hash,
    log_index,
    '0x' || lower(address)                                                   AS token_contract,
    '0x' || lower(right(topic1, 40))                                         AS from_address,
    '0x' || lower(right(topic2, 40))                                         AS to_address,
    toString(reinterpretAsUInt256(reverse(unhex(substring(data, 1, 64)))))    AS value_raw
    -- Divide by 10^decimals to get human amount (18 for most ERC-20s)
FROM execution.logs
WHERE topic0 = 'ddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'
AND address = 'e91d153e0b41518a2ce8dd3d7944fa863463a97d'   -- wxDAI on Gnosis Chain, no 0x
AND block_timestamp >= '2024-01-01'
ORDER BY block_timestamp DESC
LIMIT 100
```

### Full Example: Inline Non-Indexed Param Decode (Aave ReserveDataUpdated)

```sql
-- ReserveDataUpdated(address indexed reserve, uint256 liquidityRate,
--   uint256 stableBorrowRate, uint256 variableBorrowRate,
--   uint256 liquidityIndex, uint256 variableBorrowIndex)
-- topic0: 804c9b842b2748a22bb64b345453a3de7ca54a6ca45ce00d415894979e22897a (Aave V2)
-- topic1: reserve (indexed address)
-- data: 5 uint256 values (non-indexed), each 32 bytes

SELECT
    block_timestamp,
    '0x' || lower(right(topic1, 40))                                          AS reserve,
    reinterpretAsUInt256(reverse(unhex(substring(data, 1,   64)))) / 1e27     AS liquidity_rate_apr,
    reinterpretAsUInt256(reverse(unhex(substring(data, 65,  64)))) / 1e27     AS stable_borrow_rate_apr,
    reinterpretAsUInt256(reverse(unhex(substring(data, 129, 64)))) / 1e27     AS variable_borrow_rate_apr,
    reinterpretAsUInt256(reverse(unhex(substring(data, 193, 64)))) / 1e27     AS liquidity_index,
    reinterpretAsUInt256(reverse(unhex(substring(data, 257, 64)))) / 1e27     AS variable_borrow_index
FROM execution.logs
WHERE topic0 = '804c9b842b2748a22bb64b345453a3de7ca54a6ca45ce00d415894979e22897a'
AND address = '5e15d5e33d318dced84bfe3f4eace07909be6d9c'   -- Agave LendingPool, no 0x
AND block_timestamp >= '2024-01-01'
ORDER BY block_timestamp DESC
```
