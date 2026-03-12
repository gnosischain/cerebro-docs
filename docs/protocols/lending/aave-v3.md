# Aave V3

## Protocol Overview

Aave V3 was deployed on Gnosis Chain by Aave DAO in **October 2023**. It shares the same interest rate mechanics as Agave (Aave V2) but adds V3-specific risk management features: Efficiency Mode, Isolation Mode, and Siloed Borrowing.

## Contracts on Gnosis Chain

| Contract | Address |
|----------|---------|
| Pool (PoolInstance) | `0xb50201558B00496A145fE76f7424749556E326D8` |
| PoolConfigurator | `0x7304979ec9E4EaA0273b6A037a31c4e9e5A75D16` |

## dbt Models

- **`contracts_aaveV3_PoolInstance_events`** — all supply/borrow/repay/liquidation events, start **2023-10-04**
- **`contracts_aaveV3_PoolConfigurator_events`** — governance and risk parameter change events, start **2023-10-04**

## V3-Specific Features

### Efficiency Mode (E-Mode)

Groups correlated assets (e.g., stablecoins) with higher LTV and liquidation thresholds. An E-Mode category is assigned per user, reducing the risk of liquidation between highly correlated assets.

### Isolation Mode

Newly listed volatile assets can only be used to borrow designated stablecoins. A debt ceiling caps total borrowing against the isolated asset. Detected via the `IsolationModeTotalDebtUpdated` event.

### Siloed Borrowing

High-risk assets marked as "siloed" — if borrowed, the user cannot borrow any other asset. This prevents cross-contamination of risk.

### Token Mechanics

- **Supply** → receive an aToken (e.g., `aGnoUSDC`) whose balance grows in real time
- **Borrow** → a `variableDebtToken` balance grows with accrued interest
- Both are standard ERC-20 tokens and can be transferred

## Decoded Event Signatures

Same core events as Agave, with `Deposit` renamed to `Supply` in V3:

```
Supply(address indexed reserve, address user, address indexed onBehalfOf, uint256 amount, uint16 indexed referralCode)

Withdraw(address indexed reserve, address indexed user, address indexed to, uint256 amount)

Borrow(address indexed reserve, address user, address indexed onBehalfOf, uint256 amount, uint256 interestRateMode, uint256 borrowRate, uint16 indexed referralCode)

Repay(address indexed reserve, address indexed user, address indexed repayer, uint256 amount, bool useATokens)

LiquidationCall(address indexed collateralAsset, address indexed debtAsset, address indexed user, uint256 debtToCover, uint256 liquidatedCollateralAmount, address liquidator, bool receiveAToken)

ReserveDataUpdated(address indexed reserve, uint256 liquidityRate, uint256 stableBorrowRate, uint256 variableBorrowRate, uint256 liquidityIndex, uint256 variableBorrowIndex)
```

## Example Queries

### Liquidation Events

```sql
SELECT
    block_timestamp,
    transaction_hash,
    decoded_params['collateralAsset']                                        AS collateral,
    decoded_params['debtAsset']                                              AS debt_asset,
    decoded_params['user']                                                   AS liquidated_user,
    toFloat64(decoded_params['debtToCover']) / 1e18                          AS debt_covered,
    toFloat64(decoded_params['liquidatedCollateralAmount']) / 1e18           AS collateral_seized,
    decoded_params['liquidator']                                             AS liquidator
FROM contracts_aaveV3_PoolInstance_events
WHERE event_name = 'LiquidationCall'
ORDER BY block_timestamp DESC
LIMIT 50
```

### Interest Rate Trends (Compare with Spark)

```sql
SELECT
    toStartOfDay(block_timestamp)                                    AS day,
    'aave_v3'                                                        AS protocol,
    decoded_params['reserve']                                        AS reserve,
    avg(toFloat64(decoded_params['liquidityRate'])) / 1e27           AS supply_apr
FROM contracts_aaveV3_PoolInstance_events
WHERE event_name = 'ReserveDataUpdated'
GROUP BY day, reserve

UNION ALL

SELECT
    toStartOfDay(block_timestamp),
    'spark',
    decoded_params['reserve'],
    avg(toFloat64(decoded_params['liquidityRate'])) / 1e27
FROM contracts_spark_Pool_events
WHERE event_name = 'ReserveDataUpdated'
GROUP BY day, decoded_params['reserve']
ORDER BY day DESC, reserve
```

## See Also

- [Lending Protocols Overview](index.md) — shared mechanics, interest rate model, units
- [dbt Model Catalog — Contracts](../../models/contracts.md)
