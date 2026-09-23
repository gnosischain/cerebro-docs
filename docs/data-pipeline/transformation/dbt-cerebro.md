# dbt-cerebro

dbt-cerebro is the core data transformation project for the Gnosis Analytics platform. It is a [dbt](https://www.getdbt.com/) project containing about 1,370 SQL models (roughly 1,250 tagged `production`) across 15 modules that transform raw blockchain data from ClickHouse into analytics-ready datasets.

## Overview

dbt-cerebro transforms Gnosis Chain data across four domains:

- **Execution Layer** -- Transaction analysis, smart contract interactions, DeFi protocols, gas usage
- **Consensus Layer** -- Validator activity, block proposals, attestations, sync committee participation
- **P2P Network** -- Peer-to-peer interactions, client distributions, network topology
- **ESG / Sustainability** -- Environmental metrics including power consumption and carbon emissions

All data is unified in ClickHouse Cloud for high-performance analytics.

## Architecture

```
Data Sources                  dbt Transformation Pipeline                Output
─────────────                 ──────────────────────────                 ──────

execution.blocks       -->    stg_execution__blocks                \
execution.transactions -->    stg_execution__transactions           |
execution.logs         -->    stg_execution__logs                   |
consensus.blocks       -->    stg_consensus__blocks                 |--> int_* models
nebula.visits          -->    stg_p2p__visits                       |     (incremental)
crawlers_data.*        -->    stg_crawlers__*                      /
                                      |
                                      v
                              int_execution_blocks_clients_daily    \
                              int_consensus_validators_active_daily  |
                              int_p2p_peers_geo_daily                |--> fct_* models
                              int_bridges_transfers_daily           /     (views)
                                      |
                                      v
                              fct_execution_gas_daily               \
                              fct_consensus_attestation_rates        |--> api_* models
                              fct_p2p_client_diversity              /     (views)
                                      |
                                      v
                              api_execution_transactions_daily       --> REST API
                              api_consensus_validators_active_daily  --> REST API
                              api_p2p_client_distribution_daily      --> REST API
```

## Model Organization

Models are organized by domain module, each with its own staging, intermediate, and marts subdirectories:

```
models/
├── execution/           # Execution layer (blocks, txs, contracts)
│   ├── staging/         # stg_execution__*
│   ├── intermediate/    # int_execution_*
│   └── marts/           # fct_execution_*, api_execution_*
├── consensus/           # Consensus layer (validators, attestations)
│   ├── staging/
│   ├── intermediate/
│   └── marts/
├── contracts/           # Decoded smart contract data
│   └── {protocol}/      # One subdirectory per protocol
├── p2p/                 # P2P network analysis
├── ESG/                 # Environmental sustainability
├── bridges/             # Cross-chain bridge activity
├── probelab/            # ProbeLab network metrics
└── crawlers/            # Crawler data transformations
```

## Incremental Processing

Most intermediate models are incrementally materialized. The same model SQL supports four distinct invocation modes — daily catch-up, microbatch slicing, full-refresh batching, and refill recovery — selected by which dbt vars are set when the model runs.

A typical incremental config:

```sql
{{
  config(
    materialized='incremental',
    incremental_strategy=(
      'append'
      if (var('start_month', none) or var('incremental_end_date', none))
      else 'delete+insert'
    ),
    engine='ReplacingMergeTree()',
    order_by='(block_timestamp, transaction_hash)',
    unique_key='(block_timestamp, transaction_hash)',
    partition_by='toStartOfMonth(block_timestamp)'
  )
}}

SELECT ...
FROM {{ source('execution', 'transactions') }}
{% if var('start_month', none) and var('end_month', none) %}
WHERE toStartOfMonth(block_timestamp) >= toDate('{{ var("start_month") }}')
  AND toStartOfMonth(block_timestamp) <= toDate('{{ var("end_month") }}')
{% else %}
{{ apply_monthly_incremental_filter('block_timestamp', 'date', false) }}
{% endif %}
```

Key building blocks:

- **`delete+insert`** for daily runs (no vars set) — delete the affected window, insert fresh rows. Cheap on small windows.
- **`append`** when either `start_month` (full-refresh / refill) or `incremental_end_date` (microbatch) is set — no mutation. RMT collapses duplicates on background merges or via on-demand `OPTIMIZE`.
- **`ReplacingMergeTree`** handles deduplication on `unique_key` so re-runs are idempotent.
- **Monthly partitioning** on `toStartOfMonth(...)` enables efficient partition-level deletes, queries, and `OPTIMIZE` operations.
- **`apply_monthly_incremental_filter`** produces the WHERE clause for the daily and microbatch paths; the `start_month` branch is written inline because it filters source rows.

For the full picture see:

- [Incremental Strategies](incremental-strategies.md) — the invocation modes, the macro routing logic, and the `refill_append` tag for heavy aggregates
- [Running Models](running-models.md) — the production runners with end-to-end examples
- [The dbt daily run failed](../../operations/runbooks/dbt-daily-run-failed.md) — reading last night's failure and rerunning only what failed
- [dbt reprocess after upstream repair](../../operations/runbooks/dbt-reprocess.md) — the decision tree for fixing dbt after an indexer repair, without a full refresh
- [Recovering from a Prices Gap](../../operations/prices-gap-recovery.md) — incident response when a prices source skips a day

## Contract ABI Decoding

dbt-cerebro includes a system for decoding raw blockchain transaction data into human-readable function calls and events. See [ABI Decoding](abi-decoding.md) for the full workflow.

## Macros

The project includes custom macros in the `macros/` directory:

| Category | Key Macros | Purpose |
|----------|-----------|---------|
| `db/` | `apply_monthly_incremental_filter` | Monthly incremental processing — see [Incremental Strategies](incremental-strategies.md) |
| `db/` | `refill_safe_pre_hook` / `refill_safe_post_hook` | Memory contract for `tag:refill_append` models — caps memory at 8 GiB and enables disk spill |
| `db/` | `optimize_partition_final` | `OPTIMIZE TABLE … PARTITION '<m>' FINAL DEDUPLICATE` — used by the refill script |
| `db/` | `kill_failed_mutations` | Cleanup poisoned mutations from killed `delete+insert` runs |
| `decoding/` | `decode_calls`, `decode_logs` | Contract ABI decoding |
| `execution/` | Various helpers | Execution layer utilities |

## Seeds

Static reference data is loaded via dbt seeds:

| Seed File | Description |
|-----------|-------------|
| `contracts_abi.csv` | Contract ABIs fetched from Blockscout |
| `event_signatures.csv` | Event topic signatures generated from ABIs |
| `function_signatures.csv` | Function selector signatures generated from ABIs |

!!! warning "Deploy seeds only from the merged tip, and verify the `chain` column"
    A `dbt seed` run from a stale checkout once wiped the `chain` column on the signature and ABI seeds. Because `decode_logs` filters `WHERE chain = 'gnosis'`, the entire decode fleet appended zero rows for days while every run stayed green. After any seed deploy, check row counts **and** the `chain` distribution; the symptom to recognise is decode models appending 0 rows with no error.

## Configuration

### Environment Variables

| Variable | Description |
|----------|-------------|
| `CLICKHOUSE_URL` | ClickHouse Cloud hostname |
| `CLICKHOUSE_PORT` | HTTP port (typically 8443) |
| `CLICKHOUSE_USER` | Username (typically `default`) |
| `CLICKHOUSE_PASSWORD` | Authentication password |
| `CLICKHOUSE_SECURE` | Use HTTPS (`True`) |
| `CLICKHOUSE_DATABASE` | Target database for dbt models |

### ClickHouse Requirements

- ClickHouse version 24.1 or later
- Permissions to create/drop tables, read source schemas, and write to target schemas

## Running in production

dbt-cerebro runs on the platform's Kubernetes cluster as three workloads from one image:

| Workload | What | Notes |
|---|---|---|
| Daily CronJob, **06:00 UTC** | `cron_preview.sh` → `scripts/run_dbt_observability.sh` | ~3h40m. `concurrencyPolicy: Forbid`, one attempt, no Kubernetes retries; the orchestrator retries transients internally. Only `dbt-run` is mandatory — `source-freshness` failing nightly is expected |
| Live-loop Deployment | `dbt run --select tag:live` every 45 s | 19 models. One replica, `Recreate`, never scaled |
| Static-server Deployment | serves `/logs/`, `/reports/`, `/health`, `/metrics` | The route to last night's published artifacts, via a port-forward. Its data volume is a read-only bucket mount, so dbt cannot run there |

The published artifacts (`dbt.log`, run results, reports) go to a bucket only the cron and server service accounts can read; the orchestrator's step summary and its `TRANSIENT=` / `PERMANENT=` classification go to the pod's **stdout only**. Three job records are kept per outcome.

Repairs and backfills run inside a one-shot clone of the daily CronJob — see [One-shot jobs](../../operations/runbooks/one-shot-jobs.md). Overriding the Job's `args` drops the publish step, so the pod log is the only record of such a run.

Elementary is switched off; nothing writes `elementary.*`, and `dbt docs generate` writing a catalog with 0 model nodes is known dbt-clickhouse behaviour.

For the full set of runners (daily cron, live loop, microbatch catch-up, full-refresh batched, gap-window refresh, refill recovery) see [Running Models](running-models.md).

### Local development

The repository ships a Compose file with the same image:

```bash
docker-compose up -d           # start the container (documentation server on port 8080)
docker exec -it dbt /bin/bash  # enter it
dbt debug                      # test the connection
dbt run --select execution     # run a module
dbt build --select +api_execution_transactions_daily
```

## Development Workflow

1. **Choose the appropriate layer** based on the type of transformation needed
2. **Follow naming conventions**: `stg_{source}__{table}`, `int_{domain}_{metric}_{grain}`, `fct_{domain}_{metric}_{grain}`, `api_{domain}_{metric}_{grain}`
3. **Configure materialization** appropriately (views for staging/facts/API, incremental for intermediate)
4. **Add tests** using dbt's built-in testing framework
5. **Generate documentation** with `dbt docs generate`

See [Model Layers](model-layers.md) for detailed guidance on each layer.
