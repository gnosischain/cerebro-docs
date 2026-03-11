# Data Transformation

The transformation layer converts raw blockchain data in ClickHouse into analytics-ready datasets using [dbt](https://www.getdbt.com/) (data build tool). Two projects handle this:

- **dbt-cerebro** -- the core transformation project containing ~400 SQL models organized across eight domain modules
- **dbt-schema-gen** -- an LLM-powered tool that generates and maintains `schema.yml` documentation files for dbt models

## Components

| Component | Purpose |
|-----------|---------|
| [dbt-cerebro](dbt-cerebro.md) | Core dbt project: ~400 models, 8 modules, incremental processing |
| [Model Layers](model-layers.md) | Explanation of the `stg_*` / `int_*` / `fct_*` / `api_*` naming convention and materialization strategy |
| [Modules Reference](modules.md) | The 8 domain modules with model counts, key models, and descriptions |
| [ABI Decoding](abi-decoding.md) | Contract ABI decoding system for converting raw transaction data into human-readable function calls and events |
| [dbt-schema-gen](dbt-schema-gen.md) | LLM-powered schema documentation generator |

## Transformation Philosophy

The transformation layer follows several key principles:

**Layered architecture** -- Data flows through four distinct layers (staging, intermediate, facts, API), each with a clear purpose and materialization strategy. This separation enables independent testing and selective rebuilds.

**Incremental processing** -- Large tables are materialized as incremental models using ClickHouse's `ReplacingMergeTree` engine with `delete+insert` strategy and monthly partitioning. This avoids full table scans on every run.

**Source of truth** -- Raw tables in the `execution`, `consensus`, `nebula`, and `crawlers_data` databases remain untouched. All transformations produce new tables in the `dbt` database.

**Convention over configuration** -- Strict naming conventions (`stg_`, `int_`, `fct_`, `api_`) make models self-documenting and enable automation for API endpoint discovery.
