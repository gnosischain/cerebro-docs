# Contracts Module

The Contracts module provides protocol-specific decoded event and function call data. Unlike the Execution module which handles raw EVM data, the Contracts module uses ABI decoding to transform opaque log topics and calldata into human-readable, typed columns for specific protocols deployed on Gnosis Chain.

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
<!-- generated: 2026-07-23 -->
**Atoken**

| Model | Layer | Description |
|-------|-------|-------------|
| `contracts_aaveV3_AToken_events` | CONTRACTS | Decoded event logs from Aave V3 aToken contracts on Gnosis (aGnoGNO, aGnoWXDAI, aGnosDAI, aGnoUSDC, aGnoEURe, aGnoUSD... |
| `contracts_spark_AToken_events` | CONTRACTS | Decoded event logs from SparkLend aToken contracts on Gnosis (spGNO, spWETH, spwstETH, spWXDAI, spsDAI, spUSDC, spUSD... |

**Cowswapethflow**

| Model | Layer | Description |
|-------|-------|-------------|
| `contracts_CowProtocol_CoWSwapEthFlow_events` | CONTRACTS | Decoded event log stream from the CoW Swap EthFlow contract on Gnosis
(0xbA3cB449bD2B4ADddBc894D8697F5170800EAdeC). C... |

**Factory**

| Model | Layer | Description |
|-------|-------|-------------|
| `contracts_UniswapV3_Factory_events` | CONTRACTS | Decoded event log stream from the Uniswap V3 Factory contract on Gnosis.
The factory emits PoolCreated events when a ... |

**Gpv2Allowlistauthentication**

| Model | Layer | Description |
|-------|-------|-------------|
| `contracts_CowProtocol_GPv2AllowListAuthentication_events` | CONTRACTS | Proxy contract — implementation ABI (GPv2AllowListAuthentication) was
fetched and stored under the proxy address by f... |

**Gpv2Settlement**

| Model | Layer | Description |
|-------|-------|-------------|
| `contracts_CowProtocol_GPv2Settlement_events` | CONTRACTS | Decoded event log stream from the CoW Protocol GPv2Settlement contract
on Gnosis Chain (the main settlement contract ... |

**Marketfactory**

| Model | Layer | Description |
|-------|-------|-------------|
| `contracts_Seer_MarketFactory_calls` | CONTRACTS | The 'contracts_Seer_MarketFactory_calls' model captures and processes call data related to the Seer MarketFactory con... |
| `contracts_Seer_MarketFactory_events` | CONTRACTS | The `contracts_Seer_MarketFactory_events` model captures and stores event logs related to the Seer MarketFactory cont... |

**Nonfungiblepositionmanager**

| Model | Layer | Description |
|-------|-------|-------------|
| `contracts_UniswapV3_NonfungiblePositionManager_events` | CONTRACTS | Decoded events from the Uniswap V3 NonfungiblePositionManager contract
(0xae8fbe656a77519a7490054274910129c9244fa3) o... |

**Pool**

| Model | Layer | Description |
|-------|-------|-------------|
| `contracts_BalancerV2_Pool_events` | CONTRACTS | Pool-level Balancer V2 events decoded from execution.logs across all pools in
contracts_BalancerV2_pool_registry. Car... |
| `contracts_UniswapV3_Pool_events` | CONTRACTS | Decoded event log stream from Uniswap V3 Pool contracts on Gnosis. Pool
addresses are dynamically selected from the c... |
| `contracts_UniswapV3_Pool_events_live` | CONTRACTS | Plain view over `execution_live.logs` that decodes Uniswap V3 Pool events in near-real-time. Materialized as a view (... |
| `contracts_spark_Pool_events` | CONTRACTS | The `contracts_spark_Pool_events` model captures and processes event logs from Spark Protocol's Pool contract, enabli... |

**Poolconfigurator**

| Model | Layer | Description |
|-------|-------|-------------|
| `contracts_aaveV3_PoolConfigurator_events` | CONTRACTS | Decoded event logs from the Aave V3 PoolConfigurator contract on Gnosis (reserve and risk-parameter governance events... |
| `contracts_spark_PoolConfigurator_events` | CONTRACTS | The `contracts_spark_PoolConfigurator_events` model captures event logs from SparkLend's PoolConfigurator contract on... |

**Poolinstance**

| Model | Layer | Description |
|-------|-------|-------------|
| `contracts_aaveV3_PoolInstance_events` | CONTRACTS | Decoded event logs from the Aave V3 Pool (PoolInstance) contract on Gnosis. Thin wrapper around the decode_logs macro... |

**Tslax**

| Model | Layer | Description |
|-------|-------|-------------|
| `contracts_backedfi_TSLAx_Oracle_events` | CONTRACTS | Decoded Chainlink-compatible AnswerUpdated event logs from the BackedFi TSLAx RWA price oracle on Gnosis. Thin wrappe... |

**Vault**

| Model | Layer | Description |
|-------|-------|-------------|
| `contracts_BalancerV2_Vault_events` | CONTRACTS | Decoded event log stream from the Balancer V2 Vault contract on Gnosis
Chain. One row per emitted log; decoded_params... |
| `contracts_BalancerV2_Vault_events_live` | CONTRACTS | Plain view over `execution_live.logs` that decodes Balancer V2 Vault events in near-real-time. Same approach as `cont... |
| `contracts_BalancerV3_Vault_events` | CONTRACTS | Decoded event log stream from the Balancer V3 Vault contract on Gnosis
Chain. One row per emitted log; decoded_params... |
| `contracts_BalancerV3_Vault_events_live` | CONTRACTS | Plain view over `execution_live.logs` that decodes Balancer V3 Vault events in near-real-time. Same approach as `cont... |

**Wrapped1155Factory**

| Model | Layer | Description |
|-------|-------|-------------|
| `contracts_Seer_Wrapped1155Factory_calls` | CONTRACTS | The `contracts_Seer_Wrapped1155Factory_calls` model captures and decodes call data related to the Wrapped1155Factory ... |
| `contracts_Seer_Wrapped1155Factory_events` | CONTRACTS | The `contracts_Seer_Wrapped1155Factory_events` model captures and processes event logs related to the Wrapped1155Fact... |

**Bc3M**

| Model | Layer | Description |
|-------|-------|-------------|
| `contracts_backedfi_bC3M_Oracle_events` | CONTRACTS | Decoded Chainlink-compatible AnswerUpdated event logs from the BackedFi bC3M RWA price oracle on Gnosis. Thin wrapper... |

**Bcoin**

| Model | Layer | Description |
|-------|-------|-------------|
| `contracts_backedfi_bCOIN_Oracle_events` | CONTRACTS | Decoded Chainlink-compatible AnswerUpdated event logs from the BackedFi bCOIN RWA price oracle on Gnosis. Thin wrappe... |

**Bcspx**

| Model | Layer | Description |
|-------|-------|-------------|
| `contracts_backedfi_bCSPX_Oracle_events` | CONTRACTS | Decoded Chainlink-compatible AnswerUpdated event logs from the BackedFi bCSPX RWA price oracle on Gnosis. Thin wrappe... |

**Bhigh**

| Model | Layer | Description |
|-------|-------|-------------|
| `contracts_backedfi_bHIGH_Oracle_events` | CONTRACTS | Decoded Chainlink-compatible AnswerUpdated event logs from the BackedFi bHIGH RWA price oracle on Gnosis. Thin wrappe... |

**Bib01**

| Model | Layer | Description |
|-------|-------|-------------|
| `contracts_backedfi_bIB01_Oracle_events` | CONTRACTS | Decoded Chainlink-compatible AnswerUpdated event logs from the BackedFi bIB01 RWA price oracle on Gnosis. Thin wrappe... |

**Bibta**

| Model | Layer | Description |
|-------|-------|-------------|
| `contracts_backedfi_bIBTA_Oracle_events` | CONTRACTS | Decoded Chainlink-compatible AnswerUpdated event logs from the BackedFi bIBTA RWA price oracle on Gnosis. Thin wrappe... |

**Bmstr**

| Model | Layer | Description |
|-------|-------|-------------|
| `contracts_backedfi_bMSTR_Oracle_events` | CONTRACTS | Decoded Chainlink-compatible AnswerUpdated event logs from the BackedFi bMSTR RWA price oracle on Gnosis. Thin wrappe... |

**Bnvda**

| Model | Layer | Description |
|-------|-------|-------------|
| `contracts_backedfi_bNVDA_Oracle_events` | CONTRACTS | Decoded Chainlink-compatible AnswerUpdated event logs from the BackedFi bNVDA RWA price oracle on Gnosis. Thin wrappe... |

**Calls**

| Model | Layer | Description |
|-------|-------|-------------|
| `contracts_AgentResultMapping_calls` | CONTRACTS | The `contracts_AgentResultMapping_calls` model captures and decodes call interactions related to a specific smart con... |
| `contracts_ConditionalTokens_calls` | CONTRACTS | The `contracts_ConditionalTokens_calls` model captures and decodes call transactions related to a specific Conditiona... |
| `contracts_FPMMDeterministicFactory_calls` | CONTRACTS | The `contracts_FPMMDeterministicFactory_calls` model captures and decodes call data related to a specific smart contr... |
| `contracts_GBCDeposit_calls` | CONTRACTS | Decoded transaction-level calls to the Gnosis Beacon Chain Deposit contract. Thin wrapper around the decode_calls mac... |
| `contracts_OmenAgentResultMapping_calls` | CONTRACTS | The `contracts_OmenAgentResultMapping_calls` model captures and processes call data related to the Omen Agent contrac... |
| `contracts_wxdai_calls` | CONTRACTS | Decoded transaction-level calls to the WXDAI contract on Gnosis. Thin wrapper around the decode_calls macro; one row ... |

**Events**

| Model | Layer | Description |
|-------|-------|-------------|
| `contracts_AgentResultMapping_events` | CONTRACTS | The contracts_AgentResultMapping_events model captures and processes blockchain event logs related to agent result ma... |
| `contracts_ConditionalTokens_events` | CONTRACTS | The `contracts_ConditionalTokens_events` model captures and stores event logs related to Conditional Tokens contracts... |
| `contracts_Curve3PoolLP_events` | CONTRACTS | Decoded event log stream from the Curve 3pool LP token (x3CRV) at
0x1337BedC9D22ecbe766dF105c9623922A27963EC on Gnosi... |
| `contracts_CurveGauge_events` | CONTRACTS | Decoded event log stream from the Curve x3CRV gauge deposit contract
(0xb721cc32160ab0da2614cc6ab16ed822aeebc101, pro... |
| `contracts_FPMMDeterministicFactory_events` | CONTRACTS | The contracts_FPMMDeterministicFactory_events model captures and processes event logs related to FPMM deterministic f... |
| `contracts_GBCDeposit_events` | CONTRACTS | Decoded event logs from the Gnosis Beacon Chain Deposit contract (DepositEvent). Thin wrapper around the decode_logs ... |
| `contracts_OmenAgentResultMapping_events` | CONTRACTS | The `contracts_OmenAgentResultMapping_events` model captures and processes event logs related to Omen Agent Result Ma... |
| `contracts_ocsdai_events` | CONTRACTS | Decoded event logs for the OpenCover OC-sDAI vault ("Covered Savings xDAI",
CoveredMetavault, 0x0ac34fe133bde3a2ef589... |
| `contracts_sdai_events` | CONTRACTS | Decoded event logs from the sDAI (Savings xDAI) ERC-4626 vault contract on Gnosis. Thin wrapper around the decode_log... |
| `contracts_wxdai_events` | CONTRACTS | Decoded event logs from the WXDAI contract on Gnosis. Thin wrapper around the decode_logs macro; one row per emitted ... |

**Feeds**

| Model | Layer | Description |
|-------|-------|-------------|
| `contracts_chainlink_feeds_events` | CONTRACTS | Decoded Chainlink price-feed AnswerUpdated events for all aggregators used on Gnosis (GNO/USD, ETH/USD, WBTC/USD, EUR... |

**Pool**

| Model | Layer | Description |
|-------|-------|-------------|
| `contracts_BalancerV2_pool_registry` | CONTRACTS | Registry of all Balancer V2 pools (from the Vault PoolRegistered event),
used by contracts_BalancerV2_Pool_events to ... |

**Registry**

| Model | Layer | Description |
|-------|-------|-------------|
| `contracts_circles_registry` | CONTRACTS | Registry of all Circles protocol contracts. Unions the static
contracts_circles_registry_static seed (lower-cased add... |

**V2**

| Model | Layer | Description |
|-------|-------|-------------|
| `contracts_Realitio_v2_1_calls` | CONTRACTS | The contracts_Realitio_v2_1_calls model captures and processes call interactions from the Realitio v2.1 smart contrac... |
| `contracts_Realitio_v2_1_events` | CONTRACTS | The `contracts_Realitio_v2_1_events` model captures and processes event logs related to Realitio V2.1 contract intera... |
| `contracts_circles_v2_AffiliateGroupRegistry_calls` | CONTRACTS | Decoded function calls for the Circles v2 AffiliateGroupRegistry contract. |
| `contracts_circles_v2_AffiliateGroupRegistry_events` | CONTRACTS | Decoded event logs for the Circles v2 AffiliateGroupRegistry contract. |
| `contracts_circles_v2_BaseGroupFactory_calls` | CONTRACTS | Decoded function calls for the Circles v2 BaseGroupFactory contract. |
| `contracts_circles_v2_BaseGroupFactory_events` | CONTRACTS | Decoded event logs for the Circles v2 BaseGroupFactory contract. |
| `contracts_circles_v2_BaseGroupMintRouter_calls` | CONTRACTS | Decoded function calls for the Circles v2 BaseGroupMintRouter contract. |
| `contracts_circles_v2_BaseGroup_events` | CONTRACTS | Decoded event logs for dynamically discovered Circles v2 BaseGroup runtime contracts. |
| `contracts_circles_v2_BaseMintPolicy_calls` | CONTRACTS | Decoded function calls for the Circles v2 BaseMintPolicy contract. |
| `contracts_circles_v2_CMGroupDeployer_calls` | CONTRACTS | Decoded function calls for the Circles v2 CMGroupDeployer contract. |
| `contracts_circles_v2_CMGroupDeployer_events` | CONTRACTS | Decoded event logs for the Circles v2 CMGroupDeployer contract. |
| `contracts_circles_v2_CirclesBackingCondition_calls` | CONTRACTS | Decoded function calls for the Circles v2 CirclesBackingCondition contract. |
| `contracts_circles_v2_CirclesBackingFactory_calls` | CONTRACTS | Decoded function calls for the Circles v2 CirclesBackingFactory contract. |
| `contracts_circles_v2_CirclesBackingFactory_events` | CONTRACTS | Decoded event logs for the Circles v2 CirclesBackingFactory contract. |
| `contracts_circles_v2_ERC20Lift_calls` | CONTRACTS | Decoded function calls for the Circles v2 ERC20Lift contract. |
| `contracts_circles_v2_ERC20Lift_events` | CONTRACTS | Decoded event logs for the Circles v2 ERC20Lift contract (wrapper factory). |
| `contracts_circles_v2_ERC20TokenOfferCycle_calls` | CONTRACTS | Decoded function calls for the Circles v2 ERC20TokenOfferCycle contracts (v1, v2, v3). |
| `contracts_circles_v2_ERC20TokenOfferCycle_events` | CONTRACTS | Decoded event logs for the Circles v2 ERC20TokenOfferCycle contracts (v1, v2, v3). |
| `contracts_circles_v2_ERC20TokenOfferFactory_calls` | CONTRACTS | Decoded function calls for the Circles v2 ERC20TokenOfferFactory contract. |
| `contracts_circles_v2_ERC20TokenOfferFactory_events` | CONTRACTS | Decoded event logs for the Circles v2 ERC20TokenOfferFactory contract. |
| `contracts_circles_v2_ERC20TokenOffer_calls` | CONTRACTS | Decoded function calls for dynamically discovered Circles v2 ERC20TokenOffer runtime contracts. |
| `contracts_circles_v2_ERC20TokenOffer_events` | CONTRACTS | Decoded event logs for dynamically discovered Circles v2 ERC20TokenOffer runtime contracts. |
| `contracts_circles_v2_GroupLBPFactory_calls` | CONTRACTS | Decoded function calls for the Circles v2 GroupLBPFactory contracts (old and new). |
| `contracts_circles_v2_GroupLBPFactory_events` | CONTRACTS | Decoded event logs for the Circles v2 GroupLBPFactory contracts (old and new). |
| `contracts_circles_v2_Hub_calls` | CONTRACTS | Decoded function calls for the Circles v2 Hub contract. |
| `contracts_circles_v2_Hub_events` | CONTRACTS | Decoded event logs for the Circles v2 Hub contract. |
| `contracts_circles_v2_InvitationEscrow_calls` | CONTRACTS | Decoded function calls for the Circles v2 InvitationEscrow contract. |
| `contracts_circles_v2_InvitationEscrow_events` | CONTRACTS | Decoded event logs for the Circles v2 InvitationEscrow contract. |
| `contracts_circles_v2_InvitationFarm_calls` | CONTRACTS | Decoded function calls for the Circles v2 InvitationFarm contract. |
| `contracts_circles_v2_InvitationFarm_events` | CONTRACTS | Decoded event logs for the Circles v2 InvitationFarm contract. |
| `contracts_circles_v2_InvitationModule_calls` | CONTRACTS | Decoded function calls for the Circles v2 InvitationModule contract. |
| `contracts_circles_v2_InvitationModule_events` | CONTRACTS | Decoded event logs for the Circles v2 InvitationModule contract. |
| `contracts_circles_v2_InvitationQuotaGrantModule_calls` | CONTRACTS | Decoded function calls for the Circles v2 InvitationQuotaGrantModule contract. |
| `contracts_circles_v2_InvitationQuotaGrantModule_events` | CONTRACTS | Decoded event logs for the Circles v2 InvitationQuotaGrantModule contract. |
| `contracts_circles_v2_Migration_calls` | CONTRACTS | Decoded function calls for the Circles v2 Migration contract
(0xd44b8dcfbadfc78ea64c55b705bfc68199b56376). Dedicated ... |
| `contracts_circles_v2_NameRegistry_calls` | CONTRACTS | Decoded function calls for the Circles v2 NameRegistry contract. |
| `contracts_circles_v2_NameRegistry_events` | CONTRACTS | Decoded event logs for the Circles v2 NameRegistry contract. |
| `contracts_circles_v2_PaymentGatewayFactory_calls` | CONTRACTS | Decoded function calls for the Circles v2 PaymentGatewayFactory
contract. This model is decoded from `execution.trace... |
| `contracts_circles_v2_PaymentGatewayFactory_events` | CONTRACTS | Decoded event logs for the Circles v2 PaymentGatewayFactory contract. |
| `contracts_circles_v2_PaymentGateway_calls` | CONTRACTS | Decoded function calls for dynamically discovered Circles v2 PaymentGateway runtime contracts. |
| `contracts_circles_v2_PaymentGateway_events` | CONTRACTS | Decoded event logs for dynamically discovered Circles v2 PaymentGateway runtime contracts. |
| `contracts_circles_v2_ReferralsModule_calls` | CONTRACTS | Decoded function calls for the Circles v2 ReferralsModule contract. |
| `contracts_circles_v2_ReferralsModule_events` | CONTRACTS | Decoded event logs for the Circles v2 ReferralsModule contract. |
| `contracts_circles_v2_StandardTreasury_calls` | CONTRACTS | Decoded function calls for the Circles v2 StandardTreasury contract. |
| `contracts_circles_v2_StandardTreasury_events` | CONTRACTS | Decoded event logs for the Circles v2 StandardTreasury contract. |
| `contracts_circles_v2_score_policy_events` | CONTRACTS | Decoded events from the OffchainScoreBasedMintPolicy singleton (0x450d68272e43c4cab7cbc7faa37893a50fae9569): Personal... |

**V3**

| Model | Layer | Description |
|-------|-------|-------------|
| `contracts_Swapr_v3_AlgebraFactory_calls` | CONTRACTS | The `contracts_Swapr_v3_AlgebraFactory_calls` model captures and decodes call data related to the Swapr v3 AlgebraFac... |
| `contracts_Swapr_v3_AlgebraFactory_events` | CONTRACTS | Decoded event logs from the Swapr v3 AlgebraFactory contract on Gnosis. Thin wrapper around the decode_logs macro; on... |
| `contracts_Swapr_v3_AlgebraPool_calls` | CONTRACTS | The `contracts_Swapr_v3_AlgebraPool_calls` model captures and processes call interactions related to the Swapr v3 Alg... |
| `contracts_Swapr_v3_AlgebraPool_events` | CONTRACTS | Decoded event logs from Swapr v3 (Algebra) Pool contracts on Gnosis. Thin wrapper around the decode_logs macro; one r... |
| `contracts_Swapr_v3_AlgebraPool_events_live` | CONTRACTS | Plain view over `execution_live.logs` that decodes Swapr V3 Algebra Pool events in near-real-time. Same approach as `... |
| `contracts_Swapr_v3_NonfungiblePositionManager_events` | CONTRACTS | Decoded events from the Swapr V3 (Algebra) NonfungiblePositionManager contract
(0x91fd594c46d8b01e62dbdebed2401dde018... |

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
