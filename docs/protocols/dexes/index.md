# DEX Protocols

This section covers decentralized exchange protocols tracked on Gnosis Chain: their AMM mechanics, event structures, and how to query decoded data.

## AMM Mechanics Overview

### Constant Product (xy = k) — Uniswap V2 Style

- Pool holds reserves of token0 ($x$) and token1 ($y$)
- **Invariant maintained:** $x \times y = k$
- Price of token0 in terms of token1: $P = y / x$
- After swap of $\Delta x$ in: $\Delta y = y - k / (x + \Delta x)$ (minus fee)
- Capital inefficiency: liquidity spread across all prices $[0, \infty)$

### Concentrated Liquidity (Uniswap V3, Swapr/Algebra)

LPs choose a price range $[\text{tickLower}, \text{tickUpper}]$ to deploy capital:

- Within range: acts like $xy = k$ on a virtual reserve; outside range: LP earns no fees
- Real reserves:
    - $x_{\text{real}} = L \times (1/\sqrt{P_{\text{current}}} - 1/\sqrt{P_{\text{upper}}})$
    - $y_{\text{real}} = L \times (\sqrt{P_{\text{current}}} - \sqrt{P_{\text{lower}}})$
- Capital efficiency: same liquidity depth with far less capital (up to 4000x for tight ranges)

### `sqrtPriceX96` Representation

Price is stored as $\sqrt{P} \times 2^{96}$ in a `uint160` (Q64.96 fixed-point format):

$$
\text{sqrtPrice} = \text{sqrtPriceX96} / 2^{96}
$$

$$
\text{price} = \text{sqrtPrice}^2 = (\text{sqrtPriceX96} / 2^{96})^2 \quad \text{(gives token1/token0 ratio)}
$$

Adjust for decimals:

$$
\text{adjusted price} = \text{price} \times 10^{\text{decimal0}} / 10^{\text{decimal1}}
$$

In ClickHouse (using the stored `uint160` string):

```sql
pow(toFloat64(decoded_params['sqrtPriceX96']) / pow(2, 96), 2) AS price_token1_per_token0
```

### Ticks

- Discrete price points: price at tick $t$ = $1.0001^t$
- Current tick $\approx \lfloor \log(\text{price}) / \log(1.0001) \rfloor$
- Each pool has a `tickSpacing` that constrains which ticks can hold liquidity:

| Fee Tier | Tick Spacing |
|----------|-------------|
| 0.01% | 1 |
| 0.05% | 10 |
| 0.3% | 60 |
| 1% | 200 |

### Balancer Weighted Pool Invariant

Generalization of $xy = k$ allowing arbitrary token weights $w_i$ (sum to 1):

$$
\prod B_i^{w_i} = k
$$

- Standard 50/50 pool: reduces to $xy = k$
- 80/20 pool: 80% in one asset, less impermanent loss for that asset

## Key Event Types

| Event | Meaning |
|-------|---------|
| `Initialize` | Pool created, initial sqrtPrice set |
| `Mint` / `PoolBalanceChanged` | Liquidity added |
| `Burn` / `PoolBalanceChanged` | Liquidity removed |
| `Swap` | Token swap occurred |
| `Collect` | Fees collected by LP |

## Protocol Pages

- [Uniswap V3](uniswap-v3.md) — concentrated liquidity with fixed fee tiers
- [Balancer](balancer.md) — weighted pools, single Vault architecture
- [CoW Protocol](cowswap.md) — intent-based batch auction DEX
- [Swapr](swapr.md) — Algebra V3 (Uniswap V3 fork with dynamic fees)
- [Pool Fee APR Analytics](analytics.md) — How daily fees, TVL, fee APR, net APR, and per-user LP positions are derived from raw events

## See Also

- [Contract ABI Decoding](../../data-pipeline/transformation/abi-decoding.md)
- [dbt Model Catalog — Contracts](../../models/contracts.md)
