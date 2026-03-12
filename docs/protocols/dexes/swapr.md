# Swapr

## Protocol Overview

Swapr is a Gnosis-chain-native DEX using the **Algebra V3 protocol** (a Uniswap V3 fork with improvements).

Key differences from Uniswap V3:

- **Dynamic fees:** fee tier adapts to volatility rather than being fixed at pool creation
- **Farming:** built-in liquidity mining support
- **Single pool per pair:** one pool per token pair (no multiple fee tiers)
- **Different naming:** `bottomTick`/`topTick` instead of `tickLower`/`tickUpper`, `price` instead of `sqrtPriceX96`

## Contracts on Gnosis Chain

| Contract | Address |
|----------|---------|
| AlgebraFactory | `0xa0864cca6e114013ab0e27cbd5b6f4c8947da766` |
| AlgebraPools | Dynamic — selected from `contracts_whitelist` (type = `SwaprPool`) |

## dbt Models

- **`contracts_Swapr_v3_AlgebraFactory_events`** — pool creation events, start **2022-03-01**
- **`contracts_Swapr_v3_AlgebraFactory_calls`** — factory function calls, start **2022-03-01**
- **`contracts_Swapr_v3_AlgebraPool_events`** — all pool events, start **2022-03-01**
- **`contracts_Swapr_v3_AlgebraPool_calls`** — pool function calls, start **2022-03-01**
    - Pool models include `contract_address` column = specific pool address

## Key Events and `decoded_params`

### `Pool` (PoolCreated, from Factory)

| `decoded_params` key | Description |
|---------------------|-------------|
| `token0` | First token address |
| `token1` | Second token address |
| `pool` | New pool address |

### `Initialize`

| `decoded_params` key | Type | Description |
|---------------------|------|-------------|
| `price` | uint160 | Initial `sqrtPriceX96` |
| `tick` | int24 | Initial tick |

### `Swap`

| `decoded_params` key | Type | Description |
|---------------------|------|-------------|
| `sender` | address | Caller |
| `recipient` | address | Token recipient |
| `amount0` | int256 | token0 delta |
| `amount1` | int256 | token1 delta |
| `price` | uint160 | New `sqrtPriceX96` after swap (**note:** Algebra calls it `price`, not `sqrtPriceX96`) |
| `liquidity` | uint128 | Pool liquidity |
| `tick` | int24 | New tick |

### `Mint`

`sender`, `owner`, `bottomTick`, `topTick`, `liquidityAmount`, `amount0`, `amount1`

### `Burn`

`owner`, `bottomTick`, `topTick`, `liquidityAmount`, `amount0`, `amount1`

### `Collect`

`owner`, `recipient`, `bottomTick`, `topTick`, `amount0`, `amount1`

!!! note "Naming Differences from Uniswap V3"
    Algebra uses `bottomTick`/`topTick` instead of `tickLower`/`tickUpper`, and `price` instead of `sqrtPriceX96` in Swap events. The underlying representation (`sqrtPriceX96` as `uint160`) is the same.

## Example Query: Compare Swapr vs Uniswap V3 Swap Volume

```sql
SELECT
    toStartOfWeek(block_timestamp)   AS week,
    'swapr'                          AS dex,
    count()                          AS swap_count
FROM contracts_Swapr_v3_AlgebraPool_events
WHERE event_name = 'Swap'
GROUP BY week

UNION ALL

SELECT
    toStartOfWeek(block_timestamp),
    'uniswap_v3',
    count()
FROM contracts_UniswapV3_Pool_events
WHERE event_name = 'Swap'
GROUP BY week
ORDER BY week DESC, dex
```

## See Also

- [DEX Protocols Overview](index.md) — AMM mechanics, concentrated liquidity, sqrtPriceX96
- [Uniswap V3](uniswap-v3.md) — the base protocol Swapr/Algebra is forked from
- [dbt Model Catalog — Contracts](../../models/contracts.md)
