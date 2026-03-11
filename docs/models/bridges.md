# Bridges Module

The Bridges module contains approximately **18 models** focused on cross-chain bridge analytics between Gnosis Chain and other networks, primarily Ethereum. It tracks token flows, bridge volumes, netflow direction, and provides visualization-ready data for sankey diagrams.

## Data Sources

Bridge flow data is sourced from the `crawlers_data` ClickHouse database, specifically tables tracking token movements across bridge contracts. The module also joins with execution layer transaction and log data to enrich flow records with block timestamps, token metadata, and USD valuations.

## Bridge Types

The module tracks several bridge protocols that connect Gnosis Chain to other networks:

### xDai Bridge

The native bridge for moving DAI/xDAI between Ethereum and Gnosis Chain. DAI deposited on Ethereum is locked in the bridge contract, and an equivalent amount of xDAI is minted on Gnosis Chain. This is the primary bridge for the network's native gas token.

- **Direction**: Ethereum <-> Gnosis Chain
- **Supported tokens**: DAI / xDAI only
- **Contract**: Ethereum-side deposit contract and Gnosis-side mint/burn contract

### OmniBridge

A generalized token bridge supporting arbitrary ERC-20 transfers between Ethereum and Gnosis Chain. Tokens are locked on the source chain, and wrapped representations are minted on the destination chain.

- **Direction**: Ethereum <-> Gnosis Chain
- **Supported tokens**: Any ERC-20 token
- **Notable tokens**: GNO, USDC, USDT, WETH, WBTC

### Layer 2 Bridges

The module also tracks bridges connecting Gnosis Chain to Layer 2 networks:

- **Arbitrum Bridge** -- Tracks token flows between Gnosis Chain and Arbitrum via third-party bridging infrastructure
- **Optimism Bridge** -- Tracks token flows between Gnosis Chain and Optimism
- **Other bridges** -- Additional bridge protocols are added as they gain adoption

!!! info "Bridge Data Coverage"
    Bridge flow records are sourced from external monitoring crawlers and may not capture 100% of all bridge transactions. Coverage is highest for the native xDai Bridge and OmniBridge, which represent the majority of cross-chain volume on Gnosis Chain.

## Model Categories

<!-- BEGIN AUTO-GENERATED: models-bridges -->
**Cum**

| Model | Layer | Description |
|-------|-------|-------------|
| `api_bridges_cum_netflow_weekly_by_bridge` | API | This view aggregates cumulative net flow in USD per bridge on a weekly basis, supporting trend analysis and reporting... |

**Flows**

| Model | Layer | Description |
|-------|-------|-------------|
| `int_bridges_flows_daily` | Intermediate | The int_bridges_flows_daily model aggregates daily bridge transfer data, providing insights into token volumes, trans... |

**Kpi**

| Model | Layer | Description |
|-------|-------|-------------|
| `api_bridges_kpi_distinct_bridges_all_time` | API | This model provides the most recent count of distinct bridges tracked over time, serving as a key performance indicat... |
| `api_bridges_kpi_distinct_chains_all_time` | API | This dbt view provides the most recent count of distinct API bridge chains, serving as a key performance indicator fo... |
| `api_bridges_kpi_netflow_7d` | API | The api_bridges_kpi_netflow_7d model provides a snapshot of net flow metrics over the last 7 days, enabling trend ana... |
| `api_bridges_kpi_total_netflow_all_time` | API | This dbt view aggregates the total net flow in USD over all time periods, providing a comprehensive KPI snapshot for ... |
| `api_bridges_kpi_total_volume_all_time` | API | The `api_bridges_kpi_total_volume_all_time` model provides the most recent total volume in USD across all bridges, se... |
| `api_bridges_kpi_volume_7d` | API | The api_bridges_kpi_volume_7d model provides a snapshot of API volume metrics over the last 7 days, enabling trend an... |

**Kpis**

| Model | Layer | Description |
|-------|-------|-------------|
| `fct_bridges_kpis_snapshot` | Fact | The fct_bridges_kpis_snapshot model provides a consolidated snapshot of bridge transaction metrics, including volume,... |

**Netflow**

| Model | Layer | Description |
|-------|-------|-------------|
| `fct_bridges_netflow_weekly_by_bridge` | Fact | This model aggregates weekly net flow data for each bridge, providing a time-series view of net USD transactions to s... |

**Sankey**

| Model | Layer | Description |
|-------|-------|-------------|
| `fct_bridges_sankey_edges_token_daily` | Fact | The fct_bridges_sankey_edges_token_daily model captures daily token transfer volumes across bridges, illustrating flo... |
| `api_bridges_sankey_gnosis_in_by_token_7d` | API | This model aggregates inbound transfer values for each token over the last 7 days, facilitating analysis of token inf... |
| `api_bridges_sankey_gnosis_in_ranges` | API | This view aggregates inbound token transfer flows between sources and targets over specified time ranges, supporting ... |
| `api_bridges_sankey_gnosis_out_by_token_7d` | API | This view aggregates the total outflow values of tokens between sources and targets over the last 7 days, providing i... |
| `api_bridges_sankey_gnosis_out_ranges` | API | This view aggregates outflow token transfer data across different time ranges for API bridges, supporting analysis of... |

**Token**

| Model | Layer | Description |
|-------|-------|-------------|
| `fct_bridges_token_netflow_daily_by_bridge` | Fact | The model aggregates daily net USD flow values for each bridge and token, enabling analysis of token transfer volumes... |
| `api_bridges_token_netflow_daily_by_bridge` | API | This view aggregates daily net flow values for each token across individual bridges and provides a combined total for... |

<!-- END AUTO-GENERATED: models-bridges -->

## Key Concepts

**Inflow vs. Outflow**

: Inflow represents tokens bridged _to_ Gnosis Chain from another network. Outflow represents tokens bridged _from_ Gnosis Chain to another network. Netflow is the difference (inflow - outflow); positive values indicate net capital entering Gnosis Chain.

**USD Valuation**

: All volume and netflow figures are available in both native token amounts and USD equivalents. USD values are computed using daily closing prices from the crawlers price feed, joined by token address and date.

**Sankey Data**

: The sankey models produce source-target-value triples suitable for direct rendering in ECharts or D3 sankey diagrams. Source and target represent chain names (e.g., "Ethereum", "Gnosis Chain"), and value represents the USD flow amount.

## Key Models Reference

| Model | Description | Key Columns |
|-------|-------------|-------------|
| `api_bridges_netflow_daily` | Daily net capital flow by bridge | `dt`, `bridge`, `inflow_usd`, `outflow_usd`, `netflow_usd` |
| `api_bridges_volume_daily` | Daily gross bridge volume | `dt`, `bridge`, `volume_usd` |
| `api_bridges_sankey_daily` | Sankey flow pairs for visualization | `dt`, `source`, `target`, `value_usd` |
| `int_bridges_volume_by_token_daily` | Volume by individual token | `dt`, `token_symbol`, `token_address`, `volume_usd` |

## Query Examples

Retrieve daily bridge netflow for the past 30 days:

```sql
SELECT dt, bridge, inflow_usd, outflow_usd, netflow_usd
FROM dbt.api_bridges_netflow_daily
WHERE dt >= today() - 30
ORDER BY dt
```

Get volume breakdown by token:

```sql
SELECT dt, token_symbol, volume_usd
FROM dbt.int_bridges_volume_by_token_daily
WHERE dt >= today() - 7
ORDER BY dt, volume_usd DESC
```

Check net capital direction over the past quarter:

```sql
SELECT
    toStartOfWeek(dt) AS week,
    sum(inflow_usd) AS total_inflow,
    sum(outflow_usd) AS total_outflow,
    sum(netflow_usd) AS net
FROM dbt.api_bridges_netflow_daily
WHERE dt >= today() - 90
GROUP BY week
ORDER BY week
```

Compare bridge volume by bridge type:

```sql
SELECT bridge, sum(volume_usd) AS total_volume
FROM dbt.api_bridges_volume_daily
WHERE dt >= today() - 30
GROUP BY bridge
ORDER BY total_volume DESC
```

## Related Modules

- [Execution](execution.md) -- Raw transaction and log data from which bridge events are decoded
- [Contracts](contracts.md) -- ABI-decoded bridge contract events
- [Crawlers](crawlers.md) -- External bridge flow data feeds from crawlers_data
