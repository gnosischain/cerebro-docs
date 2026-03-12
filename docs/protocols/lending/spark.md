# Spark

## Protocol Overview

Spark Protocol is a **fork of Aave V3**, deployed by MakerDAO (now Sky) to provide lending infrastructure for DAI/USDS. It launched on Gnosis Chain in **September 2023** and focuses on DAI/USDS, WETH, wstETH, and WBTC as key assets. Risk parameters are set by MakerDAO governance (SparkDAO subDAO).

## Contracts on Gnosis Chain

| Contract | Address |
|----------|---------|
| Pool | `0x2Dae5307c5E3FD1CF5A72Cb6F698f915860607e0` |

## dbt Model

**`contracts_spark_Pool_events`** — incremental, monthly partitions, start **2023-09-05**

`decoded_params` is `Map(String, Nullable(String))` — same query syntax as Aave V3.

### Verified `decoded_params` Keys for `ReserveDataUpdated`

From `schema.yml`: `reserve`, `liquidityRate`, `stableBorrowRate`, `variableBorrowRate`, `liquidityIndex`, `variableBorrowIndex`

## Decoded Event Signatures

Same event ABI as Aave V3 — all `Supply`/`Withdraw`/`Borrow`/`Repay`/`LiquidationCall`/`ReserveDataUpdated` events have identical signatures and `decoded_params` keys. See [Aave V3](aave-v3.md) for the full list.

## Example Query

### Spark Supply APR for WXDAI/DAI

```sql
SELECT
    toStartOfDay(block_timestamp)                                AS day,
    decoded_params['reserve']                                    AS reserve,
    avg(toFloat64(decoded_params['liquidityRate'])) / 1e27       AS supply_apr,
    avg(toFloat64(decoded_params['variableBorrowRate'])) / 1e27  AS variable_borrow_apr
FROM contracts_spark_Pool_events
WHERE event_name = 'ReserveDataUpdated'
GROUP BY day, reserve
ORDER BY day DESC
```

## See Also

- [Lending Protocols Overview](index.md) — shared mechanics, interest rate model, units
- [Aave V3](aave-v3.md) — identical event signatures and V3-specific features
- [dbt Model Catalog — Contracts](../../models/contracts.md)
