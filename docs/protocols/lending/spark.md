# SparkLend

## Protocol Overview

SparkLend is a **fork of Aave v3** operated by the MakerDAO / Sky ecosystem. The Gnosis Chain deployment went live on **2023-10-06** and is administered by the MakerDAO governance system via a `DSPauseProxy` (2-day delay) bridged from Ethereum. Reserves are initialised in a single transaction per listing (rather than Aave's three-call dance), and the protocol hosts MakerDAO's D3M (Direct Deposit DAI Module) allowing DAI liquidity to be programmatically added/removed by MakerDAO.

Registry of record: [`sparkdotfi/spark-address-registry/src/Gnosis.sol`](https://github.com/sparkdotfi/spark-address-registry/blob/master/src/Gnosis.sol). Deployment verification: [ChainSecurity SparkLend Gnosis report](https://docs.spark.fi/assets/Chainsecurity-SparkLend-Deployment-Verification.pdf).

## Key Differences vs Aave V3

- **Single-tx reserve listing.** SparkLend wraps `initReserve` + risk param config into one governance action.
- **DSPauseProxy ownership.** The `PoolAdmin` / `ACLAdmin` is the MakerDAO pause proxy — changes have a 2-day delay.
- **D3M integration.** MakerDAO can mint DAI/USDS directly into the reserve as protocol-owned liquidity, which is why DAI/sDAI utilisation looks unusually "topped-up" compared to a pure user-driven market.
- **FlashLoan event density.** SparkLend's Pool emits `ReserveDataUpdated` on **every** FlashLoan. On Gnosis, WETH alone shows **54,223 FlashLoan-emitted RDUs** versus ~5k user-action RDUs. Any rank-based (`row_number()`) pairing of user actions to preceding RDUs silently mis-aligns — see the [ASOF pairing note](#asof-pairing) below.

## Reserves on Gnosis

9 reserves are listed. Launch date per reserve from [`seeds/lending_market_mapping.csv`](https://github.com/gnosischain/dbt-cerebro/blob/main/seeds/lending_market_mapping.csv):

| Symbol | Listed |
|--------|--------|
| `GNO` | 2023-10-06 |
| `WETH` | 2023-10-06 |
| `wstETH` | 2023-10-06 |
| `WXDAI` | 2023-10-06 |
| `SXDAI` | 2023-10-06 |
| `USDC` | 2024-01-22 |
| `USDC.e` | 2025-01-14 |
| `USDT` | 2024-09-05 |
| `EURe` | 2024-10-02 |

## Contracts on Gnosis Chain

| Contract | Address |
|----------|---------|
| Pool | `0x2Dae5307c5E3FD1CF5A72Cb6F698f915860607e0` |
| PoolConfigurator | `0x9b232a63516eef3d9Cf0437E08DFd9D0E7906B0c` |
| PoolAddressesProvider | `0xA98DaCB3fC964A6A0d2ce3B77294241585EAbA6d` |
| ACL Manager (DSPauseProxy) | `0x5C3255d55E93F6b23966A3f3B29A7eB4455C5D43` |
| Oracle | `0x8E1e4FE6fe8Cd44D72Fd70D9B68fbB0Ad97f76d6` |

The 9 aTokens and 9 variable-debt tokens are enumerated in [`seeds/lending_market_mapping.csv`](https://github.com/gnosischain/dbt-cerebro/blob/main/seeds/lending_market_mapping.csv) under `protocol = 'SparkLend'`.

## dbt Models

- **`contracts_spark_Pool_events`** — decoded Pool events (17 event types), incremental, monthly partitions, start **2023-09-05**
- **`contracts_spark_AToken_events`** — `BalanceTransfer`, `Mint`, `Burn`, `Transfer` across all 9 aTokens, start **2023-10-06**
- **`contracts_spark_PoolConfigurator_events`** — governance / risk parameter changes
- **`int_execution_lending_aave_*_daily`** — the Aave-named intermediate stack was **widened to be protocol-aware**; every row carries a `protocol` column derived from a `UNION ALL` of Aave and Spark raw events, joined to `lending_market_mapping` on `(protocol, token_address)`. Unique keys / window partitions always include `protocol`.

## ASOF Pairing {#asof-pairing}

For Aave v3, each user action tx emits exactly one `ReserveDataUpdated` immediately before the action, so `row_number() OVER (PARTITION BY tx, reserve ORDER BY log_index)` pairs cleanly. SparkLend breaks this assumption: FlashLoans and D3M operations insert extra RDUs into the same tx, so ranks no longer align with user actions.

The correct pattern (from [`int_execution_lending_aave_utilization_daily.sql`](https://github.com/gnosischain/dbt-cerebro/blob/main/models/execution/lending/intermediate/int_execution_lending_aave_utilization_daily.sql)):

```sql
FROM supply_events s
ASOF INNER JOIN reserve_index_by_tx r
    ON  r.protocol         = s.protocol
    AND r.transaction_hash = s.transaction_hash
    AND r.token_address    = s.token_address
    AND r.log_index        <  s.log_index
WHERE r.liquidity_index > toUInt256OrZero('0')
```

The `ASOF log_index < s.log_index` predicate selects the RDU with the largest `log_index` strictly preceding the user action — correct for both protocols regardless of how many extra RDUs interleave.

## Decoded Event Signatures

Identical ABI to Aave v3 — `Supply` / `Withdraw` / `Borrow` / `Repay` / `LiquidationCall` / `ReserveDataUpdated` all share the same signatures and `decoded_params` keys. See [Aave V3](aave-v3.md#decoded-event-signatures) for the full list.

## Example Queries

### Supply / borrow APR by token

```sql
SELECT
    toStartOfDay(block_timestamp)                                AS day,
    decoded_params['reserve']                                    AS reserve,
    avg(toFloat64(decoded_params['liquidityRate']))      / 1e27  AS supply_apr,
    avg(toFloat64(decoded_params['variableBorrowRate'])) / 1e27  AS variable_borrow_apr
FROM dbt.contracts_spark_Pool_events
WHERE event_name = 'ReserveDataUpdated'
GROUP BY day, reserve
ORDER BY day DESC
```

### Active lenders per protocol (from the widened mart)

```sql
SELECT protocol, token, value, change_pct
FROM dbt.api_execution_lending_lenders_count_7d
WHERE protocol IN ('Aave V3', 'SparkLend')
```

### Top utilisation reserves across both markets

```sql
SELECT
    protocol,
    token_address,
    argMax(utilization_rate, date) AS latest_utilization
FROM dbt.int_execution_lending_aave_utilization_daily
WHERE date >= today() - 7
GROUP BY protocol, token_address
ORDER BY latest_utilization DESC
LIMIT 20
```

### FlashLoan density (why ASOF matters)

```sql
SELECT
    event_name,
    count() AS n
FROM dbt.contracts_spark_Pool_events
WHERE decoded_params['reserve'] = '0x6a023ccd1ff6f2045c3309768ead9e68f978f6e1'  -- WETH
GROUP BY event_name
ORDER BY n DESC
```

## See Also

- [Lending Protocols Overview](index.md) — shared mechanics, interest rate model, units
- [Aave V3](aave-v3.md) — identical event signatures and V3-specific features
- [Savings xDAI](../savings/index.md) — the sDAI/sxDAI vault, whose SXDAI token is listed as a SparkLend reserve
- [Adding a New Protocol](../../developer/add-protocol.md) — step-by-step blueprint for onboarding EVM protocols
