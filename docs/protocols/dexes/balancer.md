# Balancer

## Protocol Overview

Balancer is a generalized AMM allowing pools with 2–8 tokens at arbitrary weights. The key innovation is a **single Vault contract** that holds all token balances; pool contracts contain only pricing logic.

V2 has been deployed on Gnosis Chain since **2021**; V3 launched in **2024** with further architectural improvements.

## Contracts on Gnosis Chain

| Version | Contract | Address |
|---------|----------|---------|
| V2 | Vault | `0xBA12222222228d8Ba445958a75a0704d566BF2C8` |
| V2 | Authorizer | Governance contract |
| V3 | Vault | `0xba1333333333a1ba1108e8412f11850a5c319ba9` |

## dbt Models

- **`contracts_BalancerV2_Vault_events`** — all Vault events, start **2021-01-01**, monthly batches
- **`contracts_BalancerV3_Vault_events`** — all V3 Vault events, start **2024-01-01**

## Architecture: The Vault

- All tokens for all pools live in the single Vault address
- Pools register with the Vault and receive a unique `poolId` (`bytes32`)
- `poolId` = first 20 bytes are the pool contract address + 2 bytes specialization + 10 bytes nonce
- Swaps route through the Vault which handles token custody; pools only compute prices
- Gas savings: "internal balances" — the Vault can net token transfers across multiple pools in one transaction

## Pool Types (V2)

| Type | Invariant | Use Case |
|------|-----------|----------|
| Weighted | $\prod B_i^{w_i} = k$ | General multi-token pools (e.g., 80/20 GNO/WETH) |
| Composable Stable | StableSwap invariant | Stablecoins, correlated assets (e.g., USDC/USDT/DAI) |
| Boosted | Wraps yield-bearing tokens | USDC → Aave aUSDC internally for yield |
| LBP (Liquidity Bootstrapping) | Time-varying weights | Token launches with decreasing sell pressure |
| Managed | Owner-controlled weights | Portfolio management |

## Key Events and `decoded_params` (V2)

### `PoolRegistered`

| `decoded_params` key | Description |
|---------------------|-------------|
| `poolId` | Unique pool identifier (`bytes32`) |
| `poolAddress` | Pool contract address |
| `specialization` | Pool type enum (0=GENERAL, 1=MINIMAL_SWAP_INFO, 2=TWO_TOKEN) |

### `TokensRegistered`

| `decoded_params` key | Description |
|---------------------|-------------|
| `poolId` | Pool identifier |
| `tokens` | Array of token addresses |
| `assetManagers` | Array of asset manager addresses |

### `Swap`

| `decoded_params` key | Type | Description |
|---------------------|------|-------------|
| `poolId` | bytes32 | Pool where swap occurred |
| `tokenIn` | address | Token sold to pool |
| `tokenOut` | address | Token bought from pool |
| `amountIn` | uint256 | Amount of tokenIn |
| `amountOut` | uint256 | Amount of tokenOut |

### `PoolBalanceChanged` (add/remove liquidity)

| `decoded_params` key | Type | Description |
|---------------------|------|-------------|
| `poolId` | bytes32 | Pool identifier |
| `liquidityProvider` | address | LP address |
| `tokens` | address[] | Token addresses |
| `deltas` | int256[] | Token amount changes (positive = deposit, negative = withdrawal) |
| `protocolFeeAmounts` | uint256[] | Fee taken by protocol |

## Example Query: Swap Volume Per Pool (V2)

```sql
SELECT
    decoded_params['poolId']                         AS pool_id,
    decoded_params['tokenIn']                        AS token_in,
    decoded_params['tokenOut']                       AS token_out,
    count()                                          AS swap_count,
    sum(toUInt256OrZero(decoded_params['amountIn']))  AS total_amount_in
FROM contracts_BalancerV2_Vault_events
WHERE event_name = 'Swap'
AND block_timestamp >= now() - INTERVAL 30 DAY
GROUP BY pool_id, token_in, token_out
ORDER BY swap_count DESC
LIMIT 20
```

## See Also

- [DEX Protocols Overview](index.md) — AMM mechanics, Balancer weighted pool invariant
- [dbt Model Catalog — Contracts](../../models/contracts.md)
