# CoW Protocol

## Protocol Overview

CoW Protocol (formerly CowSwap) is an **intent-based batch auction DEX**. Users sign trade intents (not executable transactions); off-chain solvers compete to find the best execution. The winning solver settles all matched orders in a single on-chain transaction.

**"CoW" = Coincidence of Wants:** orders matched peer-to-peer without an AMM — no slippage, no MEV. All orders in a batch for the same token pair execute at the same **uniform clearing price**.

## Contracts on Gnosis Chain

| Contract | Address |
|----------|---------|
| GPv2Settlement | `0x9008D19f58AAbD9eD0D60971565AA8510560ab41` |
| GPv2VaultRelayer | `0xC92E8bdf79f0507f65a392b0ab4667716BFE0110` |
| GPv2AllowlistAuthentication | `0x2c4c28DDBdAc9C5E7055b4C863b72eA0149D8aFE` |

!!! warning "No dbt model yet"
    Use the raw logs approach below until a model is added.

## Fee Mechanics

- **Network fee:** estimated gas cost, deducted in sell token
- **Protocol fee:** basis points applied to the surplus (buy token for sell orders)
- **Partner fee:** optional integrator fee (0–1%), calculated against spot prices
- **Net effect:** users always receive at least their signed limit price (or better)

## Key Event: `Trade`

`topic0` (no 0x): `a07a543ab8a018198e99ca0184c93fe9050a79040a0a5d93dca47196b9b940e`

```
Trade(
    address indexed owner,      -- order signer (in topic1)
    address sellToken,          -- token being sold
    address buyToken,           -- token being bought
    uint256 sellAmount,         -- actual sell amount (after fees)
    uint256 buyAmount,          -- actual buy amount
    uint256 feeAmount,          -- network fee taken in sell token
    bytes orderUid              -- 56-byte unique order identifier
)
```

## Key Call: `settle`

```
settle(
    address[] tokens,                         -- token address array for this batch
    uint256[] clearingPrices,                 -- uniform prices per token
    GPv2Trade.Data[] trades,                  -- per-order execution data
    GPv2Interaction.Data[][3] interactions    -- [pre, intra, post] AMM interactions
)
```

## On-the-Fly SQL: Decode `Trade` Events Without a dbt Model

```sql
-- CoW Protocol Trade events from raw execution.logs
-- topic0 (no 0x) for Trade event:
-- a07a543ab8a018198e99ca0184c93fe9050a79040a0a5d93dca47196b9b940e
-- topic1 = owner (indexed address, padded to 32 bytes)
-- Non-indexed params decoded from data (all without 0x):
-- word 0: sellToken (address, padded to 32 bytes)
-- word 1: buyToken
-- word 2: sellAmount
-- word 3: buyAmount
-- word 4: feeAmount

SELECT
    block_timestamp,
    transaction_hash,
    log_index,
    '0x' || lower(right(topic1, 40))                                   AS owner,
    '0x' || lower(right(substring(data, 1, 64), 40))                   AS sell_token,
    '0x' || lower(right(substring(data, 65, 64), 40))                  AS buy_token,
    toString(reinterpretAsUInt256(reverse(unhex(substring(data, 129, 64))))) AS sell_amount,
    toString(reinterpretAsUInt256(reverse(unhex(substring(data, 193, 64))))) AS buy_amount,
    toString(reinterpretAsUInt256(reverse(unhex(substring(data, 257, 64))))) AS fee_amount
FROM execution.logs
WHERE lower(topic0) = 'a07a543ab8a018198e99ca0184c93fe9050a79040a0a5d93dca47196b9b940e'
AND lower(address) = '9008d19f58aabd9ed0d60971565aa8510560ab41'  -- GPv2Settlement, no 0x
ORDER BY block_timestamp DESC
LIMIT 100
```

## Template: How to Add a CoW dbt Model

When ready to add a proper dbt model:

```sql
-- models/contracts/CowProtocol/contracts_CowProtocol_GPv2Settlement_events.sql
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
        contract_address='0x9008D19f58AAbD9eD0D60971565AA8510560ab41',
        output_json_type=true,
        incremental_column='block_timestamp',
        start_blocktime='2021-04-01'
    )
}}
```

## See Also

- [DEX Protocols Overview](index.md) — AMM mechanics overview
- [On-the-Fly Decoding](../../data-pipeline/transformation/abi-decoding.md#on-the-fly-decoding-without-dbt-models) — general approach for raw log decoding
- [dbt Model Catalog — Contracts](../../models/contracts.md)
