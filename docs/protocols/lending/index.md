# Lending Protocols

All three lending protocols on Gnosis Chain (Agave, Aave V3, SparkLend) share the same core mechanics derived from the Aave codebase. This page covers the shared concepts; individual protocol pages detail contract addresses, dbt models, and specific features.

## Protocol-aware lending stack

The intermediate / mart layer was widened so every `int_execution_lending_aave_*` model is **protocol-aware**: raw Pool events from Aave V3 and SparkLend are combined via `UNION ALL` with a `protocol` literal, and reserves are resolved through [`seeds/lending_market_mapping.csv`](https://github.com/gnosischain/dbt-cerebro/blob/main/seeds/lending_market_mapping.csv) (15 `(protocol, reserve)` rows). Unique keys and window `PARTITION BY` clauses always include `protocol`, so Aave V3 and SparkLend can be sliced independently or unioned at the mart layer. See [Aave V3](aave-v3.md) and [SparkLend](spark.md) for the protocol-specific details.

## How Lending Pools Work

1. **Supply** — Users deposit assets into the pool and receive **aTokens** (interest-bearing ERC-20 tokens whose balance grows over time).
2. **Borrow** — Users borrow against their collateral up to the **Loan-to-Value (LTV)** ratio. Outstanding borrows are tracked via **variableDebtTokens**.
3. **Repay** — Borrowers repay debt plus accrued interest.
4. **Withdraw** — Suppliers redeem aTokens for the underlying asset plus earned interest.
5. **Liquidation** — If a borrower's health factor drops below 1, anyone can repay part of their debt and seize collateral at a discount.

## Health Factor

$$
\text{Health Factor} = \frac{\sum(\text{collateral}_i \times \text{liquidation threshold}_i)}{\text{total debt in base currency}}
$$

- **HF > 1**: Position is safe
- **HF < 1**: Position is liquidatable

The liquidation threshold is per-asset (e.g., WETH might be 82.5%).

## Interest Rate Model

All three protocols use a **piecewise linear ("kink") model**:

$$
U = \frac{\text{total borrows}}{\text{total liquidity}}
$$

If $U \leq U_{opt}$:

$$
\text{variableBorrowRate} = \text{baseRate} + \text{slope}_1 \times \frac{U}{U_{opt}}
$$

If $U > U_{opt}$:

$$
\text{variableBorrowRate} = \text{baseRate} + \text{slope}_1 + \text{slope}_2 \times \frac{U - U_{opt}}{1 - U_{opt}}
$$

$$
\text{liquidityRate} = \text{variableBorrowRate} \times U \times (1 - \text{reserveFactor})
$$

**Typical parameters:** $U_{opt} = 80\%$, $\text{slope}_1 = 4\%$, $\text{slope}_2 = 100\%$, $\text{baseRate} = 0\text{–}2\%$

The steep $\text{slope}_2$ intentionally punishes over-utilization to protect liquidity providers. The `reserveFactor` is the fraction of interest revenue sent to the protocol treasury.

## Units and Conversions

| Value | Storage Format | Conversion |
|-------|---------------|------------|
| Rates (`liquidityRate`, `variableBorrowRate`, `stableBorrowRate`) | RAY = 1e27 | APR = `rate / 1e27` |
| RAY APR → APY | — | $(1 + \text{rate} / 1e27 / \text{seconds per year})^{\text{seconds per year}} - 1$ |
| Indexes (`liquidityIndex`, `variableBorrowIndex`) | RAY = 1e27 | Divide by 1e27 |
| Token amounts | Token wei | Divide by $10^{\text{decimals}}$ for human-readable |

## Key Event Types

All three lending protocols emit these core events (Agave uses `Deposit`, Aave V3/Spark use `Supply`):

| Event | Description | Key `decoded_params` Fields |
|-------|-------------|----------------------------|
| `Deposit` / `Supply` | User supplies assets | `reserve`, `user`, `onBehalfOf`, `amount` |
| `Withdraw` | User redeems supply | `reserve`, `user`, `to`, `amount` |
| `Borrow` | User opens a borrow | `reserve`, `user`, `amount`, `borrowRateMode`, `borrowRate` |
| `Repay` | User repays debt | `reserve`, `user`, `repayer`, `amount` |
| `LiquidationCall` | Position liquidated | `collateralAsset`, `debtAsset`, `user`, `debtToCover`, `liquidatedCollateralAmount`, `liquidator` |
| `ReserveDataUpdated` | Interest rates updated | `reserve`, `liquidityRate`, `stableBorrowRate`, `variableBorrowRate`, `liquidityIndex`, `variableBorrowIndex` |

## Protocol Pages

- [Agave](agave.md) — Aave V2 fork by 1Hive
- [Aave V3](aave-v3.md) — Aave V3 with E-Mode, Isolation Mode, Siloed Borrowing
- [SparkLend](spark.md) — Aave V3 fork by MakerDAO/Sky
- [Rate Analytics](analytics.md) — How daily supply APY, borrow APY, utilization, and per-user balances are derived from raw events
- [Savings xDAI](../savings/index.md) — ERC-4626 vault whose `SXDAI` token is listed as a SparkLend reserve

## See Also

- [Contract ABI Decoding](../../data-pipeline/transformation/abi-decoding.md)
- [dbt Model Catalog — Contracts](../../models/contracts.md)
