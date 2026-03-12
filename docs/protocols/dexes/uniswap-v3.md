# Uniswap V3

## Protocol Overview

Uniswap V3 was deployed on Gnosis Chain in **April 2022**. It is a concentrated liquidity AMM with multiple fee tiers. A Factory contract creates new pools for any token pair + fee tier combination.

## Contracts on Gnosis Chain

| Contract | Address |
|----------|---------|
| Factory | `0xe32F7dD7e3f098D518ff19A22d5f028e076489B1` |
| Pools | Dynamic — selected from `contracts_whitelist` (type = `UniswapV3Pool`) |

## dbt Models

- **`contracts_UniswapV3_Factory_events`** — pool creation events, start **2022-04-22**
- **`contracts_UniswapV3_Pool_events`** — all pool events (swap/mint/burn/collect), start **2022-04-22**
    - Pools dynamically selected: both `token0` and `token1` must be in `contracts_whitelist`
    - `contract_address` column = pool address

## Key Events and `decoded_params`

### `PoolCreated` (from Factory)

| `decoded_params` key | Type | Description |
|---------------------|------|-------------|
| `token0` | address | Lower-address token |
| `token1` | address | Higher-address token |
| `fee` | uint24 | Fee in hundredths of a bip (e.g., 3000 = 0.3%) |
| `tickSpacing` | int24 | Minimum tick separation |
| `pool` | address | Newly deployed pool address |

### `Initialize`

| `decoded_params` key | Type | Description |
|---------------------|------|-------------|
| `sqrtPriceX96` | uint160 | Initial sqrt price × 2^96 |
| `tick` | int24 | Initial tick |

### `Mint` (add liquidity)

| `decoded_params` key | Type | Description |
|---------------------|------|-------------|
| `sender` | address | Caller |
| `owner` | address | NFT position owner |
| `tickLower` | int24 | Lower tick of position |
| `tickUpper` | int24 | Upper tick of position |
| `amount` | uint128 | Liquidity units added |
| `amount0` | uint256 | token0 deposited |
| `amount1` | uint256 | token1 deposited |

### `Burn` (remove liquidity)

Same fields as `Mint`.

### `Swap`

| `decoded_params` key | Type | Description |
|---------------------|------|-------------|
| `sender` | address | Caller (usually a router) |
| `recipient` | address | Token recipient |
| `amount0` | int256 | token0 delta (negative = out of pool) |
| `amount1` | int256 | token1 delta (negative = out of pool) |
| `sqrtPriceX96` | uint160 | New sqrt price after swap |
| `liquidity` | uint128 | Pool liquidity at time of swap |
| `tick` | int24 | New current tick after swap |

### `Collect` (fee collection)

| `decoded_params` key | Type | Description |
|---------------------|------|-------------|
| `owner` | address | Position owner |
| `recipient` | address | Fee recipient |
| `tickLower` / `tickUpper` | int24 | Position bounds |
| `amount0` / `amount1` | uint128 | Fees collected |

## Price Derivation from `sqrtPriceX96`

```sql
-- Human-readable price (token1 per token0) from a Swap event
-- Adjust decimal_diff = decimal0 - decimal1 for the specific token pair
SELECT
    block_timestamp,
    contract_address                                                    AS pool,
    pow(toFloat64(decoded_params['sqrtPriceX96']) / pow(2, 96), 2)
        * pow(10, 18 - 6)                                              AS price_usdc_per_weth,
        -- where token0=WETH(18 decimals), token1=USDC(6 decimals)
    toInt256OrZero(decoded_params['amount0']) / -1e18                   AS weth_in,
    toInt256OrZero(decoded_params['amount1']) / 1e6                     AS usdc_out
FROM contracts_UniswapV3_Pool_events
WHERE event_name = 'Swap'
AND lower(contract_address) = '0x...'  -- specific pool address
ORDER BY block_timestamp DESC
LIMIT 100
```

## Example Query: Swap Volume by Pool (Last 7 Days)

```sql
SELECT
    contract_address                                AS pool,
    count()                                         AS swap_count,
    sum(abs(toInt256OrZero(decoded_params['amount0']))) / 1e18 AS vol_token0
FROM contracts_UniswapV3_Pool_events
WHERE event_name = 'Swap'
AND block_timestamp >= now() - INTERVAL 7 DAY
GROUP BY pool
ORDER BY swap_count DESC
```

## See Also

- [DEX Protocols Overview](index.md) — AMM mechanics, sqrtPriceX96, ticks
- [dbt Model Catalog — Contracts](../../models/contracts.md)
