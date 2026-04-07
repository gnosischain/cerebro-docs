# Protocol Analytics

This section provides deep dives into the DeFi protocols tracked by the Gnosis Chain analytics platform. While the [dbt Model Catalog — Contracts](../models/contracts.md) lists all auto-generated decoded models, this section explains **how each protocol works**, what the decoded data means, and how to query it effectively.

All protocol models use the [`decode_logs`](../data-pipeline/transformation/abi-decoding.md) and [`decode_calls`](../data-pipeline/transformation/abi-decoding.md) macros to produce a `decoded_params` column of type `Map(String, String)`. Access individual fields with:

```sql
decoded_params['reserve']       -- address of the reserve asset
decoded_params['amount']        -- raw token amount (divide by 10^decimals)
decoded_params['liquidityRate'] -- interest rate in RAY (divide by 1e27)
```

## Lending Protocols

| Protocol | Contract Address | dbt Model | Live Since |
|----------|-----------------|-----------|------------|
| [Agave](lending/agave.md) | `0x5E15d5E33d318dCEd84Bfe3F4EACe07909bE6d9c` | `contracts_agave_LendingPool_events` | 2022-04-19 |
| [Aave V3](lending/aave-v3.md) | `0xb50201558B00496A145fE76f7424749556E326D8` | `contracts_aaveV3_PoolInstance_events` | 2023-10-04 |
| [Spark](lending/spark.md) | `0x2Dae5307c5E3FD1CF5A72Cb6F698f915860607e0` | `contracts_spark_Pool_events` | 2023-09-05 |

## DEX Protocols

| Protocol | Contract Address | dbt Model | Live Since |
|----------|-----------------|-----------|------------|
| [Uniswap V3](dexes/uniswap-v3.md) | Dynamic (whitelist) | `contracts_UniswapV3_Pool_events` | 2022-04-22 |
| [Balancer V2](dexes/balancer.md) | `0xBA12222222228d8Ba445958a75a0704d566BF2C8` | `contracts_BalancerV2_Vault_events` | 2021-01-01 |
| [Balancer V3](dexes/balancer.md) | `0xba1333333333a1ba1108e8412f11850a5c319ba9` | `contracts_BalancerV3_Vault_events` | 2024-01-01 |
| [CoW Protocol](dexes/cowswap.md) | `0x9008D19f58AAbD9eD0D60971565AA8510560ab41` | *(no model yet)* | — |
| [Swapr](dexes/swapr.md) | Dynamic (whitelist) | `contracts_Swapr_v3_AlgebraPool_events` | 2022-03-01 |

## Circles Protocol

| Protocol | Contract Address | dbt Model | Live Since |
|----------|-----------------|-----------|------------|
| [Circles V2](circles/index.md) | `0xc12C1E50ABB450d6205Ea2C3Fa861b3B834d13e8` | `contracts_circles_v2_Hub_events` | 2024-10-15 |

## See Also

- [Contract ABI Decoding](../data-pipeline/transformation/abi-decoding.md) — how the decoding pipeline works
- [dbt Model Catalog — Contracts](../models/contracts.md) — full list of decoded contract models
