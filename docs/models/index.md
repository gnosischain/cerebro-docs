# dbt Model Catalog

The Gnosis Analytics data platform is powered by **dbt-cerebro**, a dbt project that transforms raw Gnosis Chain data into approximately **400 curated models** organized across 8 thematic modules. These models are materialized in a ClickHouse Cloud warehouse and serve as the backbone for both the Cerebro MCP server and the metrics dashboard.

## Naming Convention

All models follow a structured naming pattern:

```
{layer}_{module}_{resource}_{granularity}
```

For example:

- `api_execution_transactions_daily` -- API-layer, execution module, transaction data, daily granularity
- `int_consensus_validators_status_daily` -- Intermediate-layer, consensus module, validator status, daily granularity
- `stg_execution__blocks` -- Staging-layer, execution module, blocks (double underscore indicates direct source mapping)

## Model Layers

Models are organized into four layers, each building on the previous one. Always prefer higher-tier models for query performance.

| Layer | Prefix | Purpose | Performance |
|-------|--------|---------|-------------|
| **API** | `api_*` | Pre-aggregated daily/weekly views designed for fast reads | Fastest |
| **Fact** | `fct_*` | Immutable event records with business-level grain | Fast |
| **Intermediate** | `int_*` | Business logic joins, enrichment, deduplication | Moderate |
| **Staging** | `stg_*` | Minimal cleaning and type casting of raw source tables | Slowest (raw scans) |

!!! tip "Query Performance"
    When using Cerebro MCP or the dashboard API, always query `api_*` models first. Fall back to `fct_*` or `int_*` only when the API layer does not expose the fields you need. Avoid `stg_*` models for ad-hoc analytics unless you need raw-level granularity.

## Module Overview

<!-- BEGIN AUTO-GENERATED: models-summary -->
| Module | Models | Description |
|--------|:------:|-------------|
| [Bridges](bridges.md) | ~17 | -- |
| [Consensus](consensus.md) | ~53 | -- |
| [Contracts](contracts.md) | ~14 | -- |
| [Crawlers](crawlers.md) | ~13 | -- |
| [ESG](esg.md) | ~16 | -- |
| [Execution](execution.md) | ~176 | -- |
| [P2P Network](p2p.md) | ~25 | -- |
| [ProbeLab](probelab.md) | ~5 | -- |
<!-- END AUTO-GENERATED: models-summary -->

## Source Databases

Models are built from raw data stored across multiple ClickHouse databases:

| Database | Content |
|----------|---------|
| `execution` | Blocks, transactions, logs, traces, contracts, transfers |
| `consensus` | Validators, attestations, rewards, deposits, blobs, specs |
| `crawlers_data` | Dune labels, Dune prices, bridge flows, GNO supply, Gnosis Pay wallets |
| `nebula` | P2P network crawls and visit records |
| `nebula_discv4` | Discovery v4 protocol data (variant schema) |
| `dbt` | Materialized dbt models (~400 tables) |

## Using Models with Cerebro MCP

To explore models programmatically through the MCP server:

```
search_models("transactions daily")         -- Find models by keyword
search_models(module="execution")            -- Filter by module
get_model_details("api_execution_transactions_daily")  -- Full schema + SQL
describe_table("api_execution_transactions_daily")     -- Column types + descriptions
```

See the [MCP Tools Reference](../mcp/tools.md) for the complete tool catalog.
