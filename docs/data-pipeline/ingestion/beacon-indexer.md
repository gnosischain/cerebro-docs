# beacon-indexer

The beacon-indexer is a consensus layer indexer that fetches data from a beacon node REST API and stores it in ClickHouse or Parquet files. It follows an ELT (Extract, Load, Transform) pattern with fork-aware parsing and automatic network detection.

## Purpose

beacon-indexer handles the acquisition of all consensus layer data:

- Validator sets, balances, and status changes
- Block proposals and attestations
- Sync committee participation
- Rewards and penalties
- Deposits, withdrawals, and voluntary exits

## Architecture

The indexer operates in two distinct phases:

```
Phase 1: Load (Extract + Load)
    Beacon Node REST API --> Raw JSON --> ClickHouse raw_* tables

Phase 2: Transform
    raw_* tables --> Fork-aware parsing --> Structured tables
```

This ELT separation means raw data is preserved exactly as received from the beacon API. Transformation logic can be updated and re-run independently without re-fetching data from the beacon node.

## Storage Backends

beacon-indexer supports two storage backends, selected via the `STORAGE_BACKEND` environment variable:

| Backend | Best For | Setup Required |
|---------|----------|----------------|
| **ClickHouse** | Production systems, real-time analytics, complex queries | Database migration |
| **Parquet** | Data analysis, ETL pipelines, archival storage, development | None |

The ClickHouse backend provides fork-aware chunk-based processing with concurrent access and monitoring. The Parquet backend produces portable columnar files compatible with pandas, DuckDB, and Spark.

## Fork Awareness

The beacon chain has undergone multiple protocol upgrades (forks), each introducing new data fields and structures. beacon-indexer automatically detects the fork version for each slot and applies the appropriate parser.

| Fork | Key Changes for Indexing |
|------|--------------------------|
| **Phase 0** | Base beacon chain: blocks, attestations, deposits, voluntary exits |
| **Altair** | Sync committee data, participation metrics |
| **Bellatrix** | Execution payloads (The Merge) |
| **Capella** | Validator withdrawals, BLS-to-execution changes |
| **Deneb** | Blob KZG commitments, blob sidecar data |
| **Electra** | Execution layer requests (deposit, withdrawal, consolidation) |

## Supported Networks

| Network | Slot Time | Slots per Epoch | Detection |
|---------|-----------|-----------------|-----------|
| **Mainnet** | 12 seconds | 32 | Automatic |
| **Gnosis Chain** | 5 seconds | 16 | Automatic |
| **Holesky** | 12 seconds | 32 | Automatic |
| **Sepolia** | 12 seconds | 32 | Automatic |

Network parameters are auto-detected from the beacon chain genesis data. No manual configuration is required.

## Operating and recovering

### How it runs

Three workloads, one image, all writing `consensus`:

| Workload | Runs | Loaders | Beacon credentials |
|---|---|---|---|
| realtime Deployment | `load realtime` | blocks, rewards, data_column_sidecars | yes |
| transform Deployment | `transform run --continuous` | derives the transformed tables | **no** |
| validators CronJob, **02:00 UTC** | `load backfill` | validators | yes |

State is two tables and nothing in the pod: `consensus.load_state_chunks` (per loader: `pending | claimed | completed | failed`) and `consensus.transformer_progress`. **Always query both with `FINAL`** — they keep every status transition, so without it you read history, not state.

The 02:00 Job takes **~4h11m**; incomplete until ~06:15 is normal. Single writer per loader, `Recreate`, one replica.

### Health

The Deployments carry **no liveness or readiness probes** by design, so a `Running` pod is not proof of progress. Ground truth is the raw frontier:

```sql
SELECT 'raw_blocks' AS t, max(slot) AS max_slot, max(slot_timestamp) AS latest FROM consensus.raw_blocks
UNION ALL SELECT 'raw_rewards', max(slot), max(slot_timestamp) FROM consensus.raw_rewards
UNION ALL SELECT 'raw_data_column_sidecars', max(slot), max(slot_timestamp) FROM consensus.raw_data_column_sidecars
UNION ALL SELECT 'raw_validators', max(slot), max(slot_timestamp) FROM consensus.raw_validators;
```

`raw_blocks` should advance ~100 slots every ~8–10 min and sit ~700–800 slots behind head (`REALTIME_SLOT_DELAY=700`, about **67 minutes** at 5 s slots).

!!! warning "Realtime does not self-heal an outage"
    On restart it sets its resume point to `max(slot)` **across all four raw tables**, then rounds **up** to the next 100-slot boundary. Because the 02:00 validators cron keeps writing near-head snapshots into `raw_validators` while realtime is down, the resume point is dragged forward to near head and **the entire outage window is skipped with no error**. This is the single most common way a beacon gap appears while everything looks green. After any realtime outage longer than a few minutes, run the gap check over `[frontier_before_outage, current_head]` before declaring recovery.

### Detecting a gap

Every 100-slot chunk on the grid with no completed row, **per loader**:

```sql
SELECT loader, expected_start, expected_start + 99 AS expected_end
FROM (
  SELECT arrayJoin(['blocks','rewards','data_column_sidecars']) AS loader,
         ⟨LO⟩ + number * 100 AS expected_start
  FROM numbers(⟨window_width/100⟩)
) AS e
LEFT ANTI JOIN (
  SELECT loader_name AS loader, start_slot AS expected_start
  FROM consensus.load_state_chunks FINAL
  WHERE status = 'completed' AND start_slot >= ⟨LO⟩ AND start_slot < ⟨HI⟩
) AS c USING (loader, expected_start)
ORDER BY loader, expected_start;
```

`⟨LO⟩` must be a multiple of 100. The **last chunk of any backfill is truncated** to `end_slot - 1`, so a single non-grid chunk at a previous backfill's boundary can show as a false positive — check it against `load_state_chunks` before repairing.

Chunks that exist but are not completed — the status tells you which repair applies:

```sql
SELECT loader_name, status, count() AS chunks, min(start_slot), max(end_slot)
FROM consensus.load_state_chunks FINAL
WHERE start_slot >= ⟨LO⟩ AND end_slot < ⟨HI⟩
GROUP BY loader_name, status ORDER BY loader_name, status;
```

Validators are one snapshot at the last slot of each UTC day, so a missing date is a gap:

```sql
SELECT toDate(slot_timestamp) AS d, count() AS snapshots
FROM consensus.raw_validators FINAL
WHERE slot_timestamp >= now() - INTERVAL 45 DAY GROUP BY d ORDER BY d;
```

`maintain check --start-slot ⟨LO⟩ --end-slot ⟨HI⟩ --detailed` finds failed and completed-but-untransformed chunks. It does **not** detect missing chunk rows — only the SQL above does.

### Repairing

| Chunk state | Repair |
|---|---|
| `failed` | `maintain fix --start-slot ⟨LO⟩ --end-slot ⟨HI⟩` (`--dry-run` first) |
| missing / `pending` / `claimed` | `load backfill --start-slot ⟨LO⟩ --end-slot ⟨HI⟩` — `maintain fix` only ever selects `failed` |
| validators | trigger the cron; it re-scans 0→head and skips what is complete |

Run these as one-shot jobs cloned from the validators CronJob ([how](../../operations/runbooks/one-shot-jobs.md)). Both slot arguments are required on every verb. `--end-slot` is **exclusive**, and chunk selection is `start_slot >= LO AND end_slot <= HI`, so a partially overlapping chunk is silently skipped. Keep both on 100-slot boundaries, strictly behind the live frontier.

!!! warning "A `--loaders` value not in the pod's `ENABLED_LOADERS` widens the repair to every loader"
    It does not narrow anything — it removes the loader filter entirely. The validators cron ships `ENABLED_LOADERS=validators`, so `--loaders blocks` from a clone of it repairs **everything** in the range. Always override `ENABLED_LOADERS` to a superset of the loaders you name.

### Corrupt range

Raw tables are `ReplacingMergeTree ORDER BY (slot, payload_hash)`, so two *different* payloads for one slot coexist — they are not deduped against each other. That is the bad-RPC signature:

```sql
SELECT slot, count() AS payload_variants FROM consensus.raw_blocks
WHERE slot BETWEEN ⟨LO⟩ AND ⟨HI⟩ GROUP BY slot HAVING payload_variants > 1 ORDER BY slot LIMIT 50;
```

Repair is `maintain fix … --force --loaders blocks`, always `--dry-run` first.

!!! warning "`--force` deletes first"
    It deletes the raw rows and every mapped transformed table for the range before reloading — for `blocks` that is 14 tables. If the beacon node is unreachable you are left with a hole, not the old data. Never widen the range "to be safe".

!!! warning "Never run a `--force` fix from the transform workload"
    It has no beacon credentials, so `BEACON_NODE_URL` falls back to localhost — it deletes first, then every reload fails, leaving the range empty and marked failed. `maintain check` and `maintain reset` are ClickHouse-only and safe there.

Verifying a repair: a duplicate scan right after a reload gives false positives, because the raw tables dedupe only at merge time. Judge by chunk status instead:

```sql
SELECT loader_name, status, count() FROM consensus.load_state_chunks FINAL
WHERE start_slot >= ⟨LO⟩ AND end_slot < ⟨HI⟩ AND loader_name = 'blocks'
GROUP BY loader_name, status;    -- want: all 'completed'
```

### Re-deriving transformed tables without refetching

!!! warning "Do not use `transform reprocess`"
    It is wired into the CLI but the implementation is a stub that logs "not implemented yet" and returns. It looks successful and changes nothing.

The real procedure is two statements; the third step is nothing, because the running transformer picks the chunks up on its next 10-second poll:

```sql
-- 1. delete the wrong rows from ONLY the affected transformed tables, one statement each
ALTER TABLE consensus.blocks DELETE WHERE slot BETWEEN ⟨LO⟩ AND ⟨HI⟩;

-- 2. un-complete the transform bookkeeping for exactly those chunks
INSERT INTO consensus.transformer_progress
  (raw_table_name, start_slot, end_slot, status, processed_count, failed_count, error_message, processed_at)
SELECT 'raw_blocks', start_slot, end_slot, 'failed', 0, 0, 'manual scoped reprocess', now()
FROM consensus.load_state_chunks FINAL
WHERE loader_name = 'blocks' AND status = 'completed'
  AND start_slot >= ⟨LO⟩ AND end_slot <= ⟨HI⟩;
```

`TRANSFORM_CHUNKS_PER_BATCH` is pinned to **1** — that is memory protection, not a tuning oversight, so a large range re-derives slowly. Each validators chunk parses a full ~400k-entry beacon state. Never `TRUNCATE transformer_progress` to force a re-derive; that is a full refresh of all history.

### Transform lagging behind raw

```sql
SELECT
  (SELECT max(end_slot) FROM consensus.load_state_chunks FINAL WHERE loader_name='blocks' AND status='completed') AS raw_frontier,
  (SELECT max(end_slot) FROM consensus.transformer_progress FINAL WHERE raw_table_name='raw_blocks' AND status='completed') AS transform_frontier;
```

Swap the loader to find **which** one is lagging — the Prometheus alert takes `max()` across all table labels and hides exactly this.

`OOMKilled` on the transform workload is the classic stall. Restarting self-heals: on startup it resets any `processing` row older than 30 minutes back to `failed`, making those chunks eligible again. Check nobody raised `TRANSFORM_CHUNKS_PER_BATCH` above 1 before restarting.

### Restart — the mandatory reset

An unclean kill leaves chunks in `claimed`, and **nothing reaps them**. `maintain fix` cannot see them (it selects `failed`). After any unclean kill:

```bash
# both slot arguments are REQUIRED
python -m src.main maintain reset --start-slot 0 --end-slot 999999999 --status claimed
```

!!! warning "That is only half the fix"
    `reset` leaves the chunks `pending`, and no running workload ever claims a pending chunk. Follow it with a `load backfill` over the same range.

### Then dbt

`consensus` is a dbt source. Check each intermediate's strategy with `context.py` first, then follow [dbt reprocess](../../operations/runbooks/dbt-reprocess.md).

!!! note "Expected noise"
    - `Waiting for complete chunk` more or less continuously — it only writes whole 100-slot chunks.
    - `transformer_progress` rows with `status='completed', processed_count=0, error_message='No data'` — a genuinely empty raw slot range.
    - `load_state_chunks` having far more rows without `FINAL` than with it — it keeps every transition.
    - The 02:00 Job incomplete for hours. Normal until ~06:15.

!!! info "Internal runbook"
    [runbooks/21-beacon-indexer.md](https://github.com/gnosisdevops/infrastructure-gnosis-analytics/blob/main/runbooks/21-beacon-indexer.md) — private repository; carries the cluster-specific commands for this page.

### Redeploying

On an image roll realtime and transform restart. Apply outside 02:00-06:15 UTC, in the idle gap between chunks. The decisive proof is no chunk hole across the restart and the transform caught up. Procedure: [Redeploying a service](../../operations/deployment.md#redeploying-a-service).

## Configuration

### Required Settings

| Variable | Description |
|----------|-------------|
| `BEACON_NODE_URL` | Beacon node REST API endpoint |
| `STORAGE_BACKEND` | `clickhouse` in production; `parquet` is a local/dev backend |

### ClickHouse Settings (when using ClickHouse backend)

| Variable | Default | Description |
|----------|---------|-------------|
| `CLICKHOUSE_HOST` | -- | ClickHouse server hostname |
| `CLICKHOUSE_PASSWORD` | -- | Authentication password |
| `CLICKHOUSE_PORT` | `8443` | HTTP port |
| `CLICKHOUSE_USER` | `default` | Username |
| `CLICKHOUSE_DATABASE` | `consensus` | Target database |
| `CLICKHOUSE_SECURE` | `true` | Use HTTPS |

### Parquet Settings (when using Parquet backend)

| Variable | Default | Description |
|----------|---------|-------------|
| `PARQUET_OUTPUT_DIR` | `./parquet_data` | Output directory for Parquet files |

### Processing Settings

| Variable | Description |
|----------|-------------|
| `ENABLED_LOADERS` | Comma-separated loaders (blocks, validators, rewards, data_column_sidecars). Also the **filter** `--loaders` is checked against — see the repair warning above |
| `CHUNK_SIZE` | Number of slots per processing chunk |

## Data Flow

1. **Load phase** -- The backfill or realtime command fetches raw beacon API responses and stores them in `raw_*` tables (ClickHouse) or raw Parquet files.
2. **Transform phase** -- The transform command reads raw data, detects the fork version for each slot, and writes parsed data into structured tables (blocks, validators, attestations, etc.).
3. **State tracking** -- Chunk-based state tracking records which slot ranges have been loaded and transformed, enabling resumability.

## ClickHouse Table Schemas

All tables are stored in the `consensus` database.

??? note "Table: `consensus.blocks`"
    **Engine:** ReplacingMergeTree(insert_version)
    **ORDER BY:** (slot)

    | Column | Type | Notes |
    |--------|------|-------|
    | `slot` | UInt64 | Beacon chain slot number |
    | `proposer_index` | UInt64 | Validator that proposed the block |
    | `parent_root` | String | Parent block root hash |
    | `state_root` | String | State root hash |
    | `signature` | String | Block signature |
    | `version` | String | Fork version (phase0, altair, etc.) |
    | `graffiti` | String | Proposer graffiti field |
    | `eth1_deposit_count` | UInt64 | Cumulative ETH1 deposit count |
    | `sync_aggregate_participation` | UInt64 | Sync committee participation bits |
    | `withdrawals_count` | UInt32 | Number of withdrawals in block |
    | `blob_kzg_commitments_count` | UInt32 | Number of blob KZG commitments |
    | `slot_timestamp` | DateTime64 | Materialized from slot and genesis time |
    | `insert_version` | UInt64 | Materialized; deduplication version |

??? note "Table: `consensus.attestations`"
    **Engine:** ReplacingMergeTree(insert_version)
    **ORDER BY:** (slot, attestation_index, committee_index)

    | Column | Type | Notes |
    |--------|------|-------|
    | `slot` | UInt64 | Slot the attestation was included in |
    | `attestation_index` | UInt64 | Position within the block |
    | `aggregation_bits` | String | Bitfield of participating validators |
    | `signature` | String | Aggregated BLS signature |
    | `attestation_slot` | UInt64 | Slot being attested to |
    | `committee_index` | UInt64 | Committee index |
    | `beacon_block_root` | String | Attested beacon block root |
    | `source_epoch` | UInt64 | Justified checkpoint epoch |
    | `target_epoch` | UInt64 | Target checkpoint epoch |
    | `source_root` | String | Justified checkpoint root |
    | `target_root` | String | Target checkpoint root |
    | `slot_timestamp` | DateTime64 | Materialized from slot |

??? note "Table: `consensus.validators`"
    **Engine:** ReplacingMergeTree(insert_version)
    **ORDER BY:** (slot, validator_index)

    | Column | Type | Notes |
    |--------|------|-------|
    | `slot` | UInt64 | Snapshot slot |
    | `validator_index` | UInt32 | Unique validator index |
    | `balance` | UInt64 | Current balance in Gwei |
    | `status` | String | Validator lifecycle status |
    | `pubkey` | String | BLS public key |
    | `effective_balance` | UInt64 | Effective balance in Gwei |
    | `slashed` | UInt8 | 1 = slashed, 0 = not slashed |
    | `activation_epoch` | UInt64 | Epoch when validator activated |
    | `exit_epoch` | UInt64 | Epoch when validator exited |
    | `withdrawable_epoch` | UInt64 | Epoch when balance is withdrawable |
    | `slot_timestamp` | DateTime64 | Materialized from slot |

??? note "Table: `consensus.rewards`"
    **Engine:** ReplacingMergeTree(insert_version)
    **ORDER BY:** (slot, proposer_index)

    | Column | Type | Notes |
    |--------|------|-------|
    | `slot` | UInt64 | Slot number |
    | `proposer_index` | UInt64 | Proposing validator index |
    | `total` | UInt64 | Total reward amount |
    | `attestations` | UInt64 | Reward from attestation inclusion |
    | `sync_aggregate` | UInt64 | Reward from sync committee |
    | `proposer_slashings` | UInt64 | Reward from proposer slashings |
    | `attester_slashings` | UInt64 | Reward from attester slashings |

??? note "Table: `consensus.raw_blocks` / `consensus.raw_validators` / `consensus.raw_rewards`"
    **Engine:** ReplacingMergeTree
    **ORDER BY:** (slot, payload_hash)

    | Column | Type | Notes |
    |--------|------|-------|
    | `slot` | UInt64 | Beacon chain slot number |
    | `payload` | String | Full JSON response from beacon API |
    | `payload_hash` | String | Hash of the payload for deduplication |
    | `retrieved_at` | DateTime | Timestamp when data was fetched |

??? note "Table: `consensus.specs`"
    **Engine:** ReplacingMergeTree(updated_at)
    **ORDER BY:** (parameter_name)

    | Column | Type | Notes |
    |--------|------|-------|
    | `parameter_name` | String | Beacon chain spec parameter name |
    | `parameter_value` | String | Parameter value |
    | `updated_at` | DateTime64 | Last update timestamp |

??? note "Table: `consensus.genesis`"
    **Engine:** ReplacingMergeTree()
    **ORDER BY:** (genesis_time)

    | Column | Type | Notes |
    |--------|------|-------|
    | `genesis_time` | DateTime64 | Chain genesis timestamp |
    | `genesis_validators_root` | String | Merkle root of genesis validators |
    | `genesis_fork_version` | String | Fork version at genesis |
