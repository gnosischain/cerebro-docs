# Crawlers Module

The Crawlers module contains approximately **9 models** that aggregate and enrich external reference data from third-party sources. Its primary dataset is the Dune Analytics label directory with over 5.3 million address labels, supplemented by price feeds, token supply data, and other reference datasets used to enrich on-chain analytics across the platform.

## Data Sources

All data is sourced from the `crawlers_data` ClickHouse database, which is populated by scheduled crawlers that fetch and sync external datasets:

| Dataset | Records | Description |
|---------|---------|-------------|
| `dune_labels` | ~5.3M | Address labels from Dune Analytics mapping addresses to human-readable names and categories |
| `dune_prices` | Millions | Historical token price data from Dune |
| `gno_supply` | Daily | GNO token supply tracking (circulating, staked, locked) |
| `gpay_wallets` | ~Thousands | Gnosis Pay card wallet addresses |
| `bridge_flows` | Daily | Raw bridge deposit/withdrawal records from external bridge monitoring |

## Model Categories

<!-- BEGIN AUTO-GENERATED: models-crawlers -->
**Country**

| Model | Layer | Description |
|-------|-------|-------------|
| `stg_crawlers_data__country_codes` | Staging | The stg_crawlers_data__country_codes model consolidates standardized country identifiers and regional classifications... |

**Data**

| Model | Layer | Description |
|-------|-------|-------------|
| `int_crawlers_data_labels` | Intermediate | The int_crawlers_data_labels model consolidates and categorizes crawler data labels for various blockchain projects, ... |
| `api_crawlers_data_gno_supply_daily` | API | The api_crawlers_data_gno_supply_daily model aggregates daily GNO supply data from crawler sources to support trend a... |

**Dune**

| Model | Layer | Description |
|-------|-------|-------------|
| `stg_crawlers_data__dune_bridge_flows` | Staging | This view aggregates and standardizes data on cross-chain bridge flows from Dune, enabling analysis of token movement... |
| `stg_crawlers_data__dune_gno_supply` | Staging | This model aggregates supply data from the Dune GNO crawler, providing a staging view for analysis of supply metrics ... |
| `stg_crawlers_data__dune_labels` | Staging | This staging model processes and standardizes crawler-derived labels from Dune, facilitating consistent categorizatio... |
| `stg_crawlers_data__dune_prices` | Staging | This staging model consolidates and standardizes Dune price data for various symbols, facilitating downstream analysi... |

**Ember**

| Model | Layer | Description |
|-------|-------|-------------|
| `stg_crawlers_data__ember_electricity_data` | Staging | This view aggregates and standardizes ember electricity data across various geographic and economic classifications t... |

**Ipinfo**

| Model | Layer | Description |
|-------|-------|-------------|
| `stg_crawlers_data__ipinfo` | Staging | The stg_crawlers_data__ipinfo model aggregates and standardizes IP geolocation and organization data to support analy... |

**Probelab**

| Model | Layer | Description |
|-------|-------|-------------|
| `stg_crawlers_data__probelab_agent_semvers_avg_1d` | Staging | This view aggregates daily average semantic version data of agents, providing insights into version distribution and ... |
| `stg_crawlers_data__probelab_cloud_provider_avg_1d` | Staging | This view aggregates daily average crawl data across different cloud providers, providing insights into crawler perfo... |
| `stg_crawlers_data__probelab_countries_avg_1d` | Staging | This view aggregates daily crawler data by country and agent version type, providing insights into crawling activity ... |
| `stg_crawlers_data__probelab_quic_support_over_7d` | Staging | This view aggregates crawler data to analyze the support for QUIC protocol over a 7-day period, segmented by agent ve... |

<!-- END AUTO-GENERATED: models-crawlers -->

## Using Labels via MCP

The Cerebro MCP server exposes the Dune label dataset through the `resolve_address` tool:

```
-- Look up a specific address
resolve_address("0x9c58bacc331c9aa871afd802db6379a98e80cedb")

-- Search by name
resolve_address("Uniswap")
resolve_address("Agave")
```

The `get_token_metadata` tool also leverages crawler price data:

```
get_token_metadata("GNO")
get_token_metadata("USDC")
```

## Data Freshness

Crawler datasets are refreshed on different schedules:

| Dataset | Refresh Frequency | Typical Lag |
|---------|-------------------|-------------|
| Dune labels | Weekly | 1-7 days |
| Dune prices | Daily | < 24 hours |
| GNO supply | Daily | < 24 hours |
| Bridge flows | Daily | < 24 hours |
| Gnosis Pay wallets | Daily | < 24 hours |

!!! warning "Label Coverage"
    The Dune label dataset covers a large portion of known addresses but is not exhaustive. Newly deployed contracts or addresses not yet cataloged by the Dune community will not have labels. The `int_crawlers_address_directory` model supplements Dune labels with on-chain contract metadata (name, symbol from ERC-20 events) to improve coverage.

## Key Models Reference

| Model | Description | Key Columns |
|-------|-------------|-------------|
| `int_crawlers_dune_labels_deduplicated` | Address labels | `address`, `name`, `category`, `source` |
| `int_crawlers_prices_daily` | Token prices | `dt`, `token_address`, `token_symbol`, `avg_price_usd`, `close_price_usd` |
| `int_crawlers_gno_supply_daily` | GNO supply | `dt`, `total_supply`, `circulating_supply`, `staked_supply` |
| `int_crawlers_address_directory` | Unified address lookup | `address`, `name`, `category`, `is_contract`, `token_symbol` |

## Query Examples

Look up labels for a set of addresses:

```sql
SELECT address, name, category
FROM dbt.int_crawlers_dune_labels_deduplicated
WHERE address IN ('0x...', '0x...')
```

Get daily GNO price:

```sql
SELECT dt, avg_price_usd, close_price_usd
FROM dbt.int_crawlers_prices_daily
WHERE token_symbol = 'GNO'
  AND dt >= today() - 30
ORDER BY dt
```

Track GNO staking ratio over time:

```sql
SELECT dt, total_supply, staked_supply,
       round(staked_supply / total_supply * 100, 2) AS staking_ratio_pct
FROM dbt.int_crawlers_gno_supply_daily
WHERE dt >= today() - 90
ORDER BY dt
```

Search for protocol contracts:

```sql
SELECT address, name, category
FROM dbt.int_crawlers_dune_labels_deduplicated
WHERE category = 'dex'
  AND name ILIKE '%balancer%'
```

## Related Modules

- [Execution](execution.md) -- On-chain contract data enriched with Dune labels
- [Bridges](bridges.md) -- Bridge flow data originates from crawler feeds
- [Contracts](contracts.md) -- Contract classification uses label data for protocol identification
- [ESG](esg.md) -- Ember electricity data is also ingested through the crawler pipeline
