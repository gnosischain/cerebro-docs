# Contracts Module

The Contracts module contains approximately **44 models** that provide protocol-specific decoded event and function call data. Unlike the Execution module which handles raw EVM data, the Contracts module uses ABI decoding to transform opaque log topics and calldata into human-readable, typed columns for specific protocols deployed on Gnosis Chain.

## Data Sources

The Contracts module draws from two sources:

1. **execution** database -- Raw logs and traces containing encoded event/function data
2. **contracts_whitelist / contracts_abi** -- ABI registry that maps contract addresses to their interface definitions, enabling automatic decoding

The ABI decoding system matches log topics and function selectors against known ABIs to produce decoded columns with meaningful names (e.g., `sender`, `amount`, `pool_id`) rather than raw hex data.

## ABI Decoding System

The decoding pipeline works as follows:

1. Contracts are registered in a whitelist with their addresses, names, and protocol tags
2. ABI JSON is stored and indexed by contract address
3. During dbt model execution, logs and traces are joined with ABI data
4. Event topics and function selectors are matched to decode parameters into typed columns

This approach avoids the need to write custom parsers for each contract -- any contract with a registered ABI is automatically decoded.

```
Raw Logs (execution.logs)
    |
    +-- JOIN contracts_whitelist (by address)
    +-- JOIN contracts_abi (by address + event signature)
    |
    v
Decoded Events (typed columns: sender, amount, pool_id, ...)
    |
    v
Protocol-Specific Models (int_contracts_balancer_swaps_daily, etc.)
```

## Model Categories

<!-- BEGIN AUTO-GENERATED: models-contracts -->
**Tslax**

| Model | Layer | Description |
|-------|-------|-------------|
| `contracts_backedfi_TSLAx_Oracle_events` | CONTRACTS | The `contracts_backedfi_TSLAx_Oracle_events` model captures and processes blockchain event logs related to the TSLAx ... |

**Bc3M**

| Model | Layer | Description |
|-------|-------|-------------|
| `contracts_backedfi_bC3M_Oracle_events` | CONTRACTS | This model captures and processes blockchain event logs related to the BackedFi contracts from the Oracle source, ena... |

**Bcoin**

| Model | Layer | Description |
|-------|-------|-------------|
| `contracts_backedfi_bCOIN_Oracle_events` | CONTRACTS | This model captures and stores Oracle event logs related to the BackedFi platform, enabling analysis of contract inte... |

**Bcspx**

| Model | Layer | Description |
|-------|-------|-------------|
| `contracts_backedfi_bCSPX_Oracle_events` | CONTRACTS | The `contracts_backedfi_bCSPX_Oracle_events` model captures and processes blockchain event logs related to the Backed... |

**Bhigh**

| Model | Layer | Description |
|-------|-------|-------------|
| `contracts_backedfi_bHIGH_Oracle_events` | CONTRACTS | The `contracts_backedfi_bHIGH_Oracle_events` model captures and processes blockchain event logs related to the Backed... |

**Bib01**

| Model | Layer | Description |
|-------|-------|-------------|
| `contracts_backedfi_bIB01_Oracle_events` | CONTRACTS | The `contracts_backedfi_bIB01_Oracle_events` model captures and processes blockchain event logs related to the Backed... |

**Bibta**

| Model | Layer | Description |
|-------|-------|-------------|
| `contracts_backedfi_bIBTA_Oracle_events` | CONTRACTS | The `contracts_backedfi_bIBTA_Oracle_events` model captures and processes blockchain event logs related to the Backed... |

**Bmstr**

| Model | Layer | Description |
|-------|-------|-------------|
| `contracts_backedfi_bMSTR_Oracle_events` | CONTRACTS | The `contracts_backedfi_bMSTR_Oracle_events` model captures and processes blockchain event logs related to BackedFi's... |

**Bnvda**

| Model | Layer | Description |
|-------|-------|-------------|
| `contracts_backedfi_bNVDA_Oracle_events` | CONTRACTS | This model captures and processes Oracle event logs related to the BackedFi protocol, enabling analysis of contract i... |

**Calls**

| Model | Layer | Description |
|-------|-------|-------------|
| `contracts_GBCDeposit_calls` | CONTRACTS | The `contracts_GBCDeposit_calls` model captures and decodes call data related to GBCDeposit contract interactions, fa... |
| `contracts_wxdai_calls` | CONTRACTS | The `contracts_wxdai_calls` model captures and decodes call interactions with the specified wxDai contract, providing... |

**Events**

| Model | Layer | Description |
|-------|-------|-------------|
| `contracts_GBCDeposit_events` | CONTRACTS | The contracts_GBCDeposit_events model captures and processes deposit event logs related to the GBC Deposit contract, ... |
| `contracts_sdai_events` | CONTRACTS | The `contracts_sdai_events` model captures and processes event logs related to the specified smart contract, enabling... |
| `contracts_wxdai_events` | CONTRACTS | The `contracts_wxdai_events` model captures and processes event logs related to the specified contract address, enabl... |

<!-- END AUTO-GENERATED: models-contracts -->

## Covered Protocols

The following protocols have dedicated decoded models:

### DEX Protocols

| Protocol | Type | Key Events | Key Contracts |
|----------|------|------------|---------------|
| **Balancer** | Batch swap DEX | Swap, Join, Exit, FlashLoan | Vault (`0xBA12...`), WeightedPool, StablePool |
| **CoW Protocol** | Batch auction DEX | Trade, Settlement, Interaction | Settlement contract, GPv2AllowanceManager |
| **SushiSwap** | AMM DEX | Swap, Mint, Burn, Sync | SushiSwap Router, Factory, Pair contracts |
| **Curve** | Stableswap DEX | TokenExchange, AddLiquidity, RemoveLiquidity | StableSwap pools, CryptoSwap pools |
| **Uniswap** | Concentrated liquidity DEX | Swap, Mint, Burn, Collect | UniswapV3Factory, UniswapV3Pool |

### Lending Protocols

| Protocol | Type | Key Events | Key Contracts |
|----------|------|------------|---------------|
| **Aave / Agave** | Lending pool | Supply, Borrow, Repay, Liquidation, FlashLoan | LendingPool, aTokens, VariableDebtToken |
| **Spark** | Lending pool (MakerDAO) | Supply, Borrow, Repay, Liquidation | SparkLend Pool, spTokens |

### Other Protocols

| Protocol | Type | Key Events | Key Contracts |
|----------|------|------------|---------------|
| **Circles** | UBI / Social currency | Trust, Transfer, Signup, OrganizationSignup | Hub, Token contracts |
| **Gnosis Pay** | Payments | Card transactions, settlements | Payment processor contracts |
| **Gnosis Safe** | Multisig wallet | ExecTransaction, AddOwner, RemoveOwner, EnableModule | Safe proxy, SafeModuleTransaction |

!!! tip "Adding New Protocols"
    To add decoded event data for a new protocol, register its contract addresses in the whitelist and upload the ABI JSON. The decoding pipeline will automatically produce typed columns for all matching events. See the [Contract ABI Decoding](../data-pipeline/transformation/abi-decoding.md) guide for details.

## Using `search_models_by_address`

The MCP server provides a dedicated tool to find dbt models related to a specific contract address:

```
search_models_by_address("0xba12222222228d8ba445958a75a0704d566bf2c8")
```

This searches the contracts whitelist, ABI registry, and model SQL to find all models that reference the given address. It is the fastest way to discover what decoded data is available for a specific contract.

## Key Models Reference

| Model | Description | Key Columns |
|-------|-------------|-------------|
| `api_contracts_protocol_activity_daily` | Cross-protocol daily activity | `dt`, `protocol`, `event_count`, `unique_users` |
| `api_contracts_events_daily` | Decoded event volume | `dt`, `protocol`, `event_name`, `count` |
| `int_contracts_balancer_swaps_daily` | Balancer swap data | `dt`, `pool_name`, `swap_count`, `volume_usd` |
| `int_contracts_cow_settlements_daily` | CoW Protocol batches | `dt`, `settlement_count`, `trade_count`, `volume_usd` |
| `int_contracts_aave_events_daily` | Aave/Agave lending | `dt`, `event_type`, `asset`, `amount_usd` |

## Query Examples

Get daily Balancer swap volume:

```sql
SELECT dt, pool_name, swap_count, volume_usd
FROM dbt.int_contracts_balancer_swaps_daily
WHERE dt >= today() - 7
ORDER BY dt, volume_usd DESC
```

Check Circles protocol growth:

```sql
SELECT dt, new_signups, total_users
FROM dbt.int_contracts_circles_signups_daily
WHERE dt >= today() - 30
ORDER BY dt
```

Compare DEX volume across protocols:

```sql
SELECT
    protocol,
    sum(volume_usd) AS total_volume,
    sum(swap_count) AS total_swaps
FROM dbt.api_contracts_protocol_activity_daily
WHERE dt >= today() - 30
  AND protocol IN ('Balancer', 'CoW Protocol', 'SushiSwap', 'Curve', 'Uniswap')
GROUP BY protocol
ORDER BY total_volume DESC
```

Track Gnosis Safe module transactions:

```sql
SELECT dt, module_type, tx_count
FROM dbt.int_contracts_safe_module_txs_daily
WHERE dt >= today() - 30
ORDER BY dt
```

## Related Modules

- [Execution](execution.md) -- Raw logs and traces that serve as input to ABI decoding
- [Bridges](bridges.md) -- Bridge contracts are a subset of decoded contract data
- [Crawlers](crawlers.md) -- Dune labels provide additional contract name resolution
