# Agave

## Protocol Overview

Agave is an **Aave V2 fork** deployed on Gnosis Chain by the [1Hive](https://1hive.org/) community. It is governed by the AGVE token and supports GNO, WETH, WBTC, USDC, wxDAI, and LINK as collateral and borrow assets.

## Contracts on Gnosis Chain

| Contract | Address |
|----------|---------|
| LendingPool | `0x5E15d5E33d318dCEd84Bfe3F4EACe07909bE6d9c` |

## dbt Model

**`contracts_agave_LendingPool_events`** — incremental, partitioned by month, start **2022-04-19**

Output columns: `block_number`, `block_timestamp`, `transaction_hash`, `transaction_index`, `log_index`, `contract_address`, `event_name`, `decoded_params` `Map(String, String)`

## Decoded Event Signatures

Full ABI signatures (these generate the `topic0` hashes the decoder matches against):

```
Deposit(address indexed reserve, address user, address indexed onBehalfOf, uint256 amount, uint16 indexed referralCode)

Withdraw(address indexed reserve, address indexed user, address indexed to, uint256 amount)

Borrow(address indexed reserve, address user, address indexed onBehalfOf, uint256 amount, uint256 interestRateMode, uint256 borrowRate, uint16 indexed referralCode)

Repay(address indexed reserve, address indexed user, address indexed repayer, uint256 amount)

LiquidationCall(address indexed collateralAsset, address indexed debtAsset, address indexed user, uint256 debtToCover, uint256 liquidatedCollateralAmount, address liquidator, bool receiveAToken)

ReserveDataUpdated(address indexed reserve, uint256 liquidityRate, uint256 stableBorrowRate, uint256 variableBorrowRate, uint256 liquidityIndex, uint256 variableBorrowIndex)
```

## `decoded_params` Keys Per Event

| `event_name` | `decoded_params` keys |
|-------------|----------------------|
| `Deposit` | `reserve`, `user`, `onBehalfOf`, `amount`, `referralCode` |
| `Withdraw` | `reserve`, `user`, `to`, `amount` |
| `Borrow` | `reserve`, `user`, `onBehalfOf`, `amount`, `interestRateMode`, `borrowRate`, `referralCode` |
| `Repay` | `reserve`, `user`, `repayer`, `amount` |
| `LiquidationCall` | `collateralAsset`, `debtAsset`, `user`, `debtToCover`, `liquidatedCollateralAmount`, `liquidator`, `receiveAToken` |
| `ReserveDataUpdated` | `reserve`, `liquidityRate`, `stableBorrowRate`, `variableBorrowRate`, `liquidityIndex`, `variableBorrowIndex` |

## Example Queries

### APY Over Time for wxDAI

```sql
SELECT
    toStartOfDay(block_timestamp)                                    AS day,
    decoded_params['reserve']                                        AS reserve,
    avg(toFloat64(decoded_params['liquidityRate'])) / 1e27           AS avg_supply_apr,
    avg(toFloat64(decoded_params['variableBorrowRate'])) / 1e27      AS avg_variable_borrow_apr
FROM contracts_agave_LendingPool_events
WHERE event_name = 'ReserveDataUpdated'
AND lower(decoded_params['reserve']) = '0xe91d153e0b41518a2ce8dd3d7944fa863463a97d'  -- wxDAI
GROUP BY day, reserve
ORDER BY day DESC
```

### Deposit Volume Per Asset

```sql
SELECT
    toStartOfWeek(block_timestamp)                   AS week,
    decoded_params['reserve']                        AS reserve,
    sum(toFloat64(decoded_params['amount'])) / 1e18  AS total_deposited  -- adjust decimals per asset
FROM contracts_agave_LendingPool_events
WHERE event_name = 'Deposit'
GROUP BY week, reserve
ORDER BY week DESC
```

## See Also

- [Lending Protocols Overview](index.md) — shared mechanics, interest rate model, units
- [dbt Model Catalog — Contracts](../../models/contracts.md)
