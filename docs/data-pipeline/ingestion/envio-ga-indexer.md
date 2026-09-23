# Envio GA Indexer (envio_ga-indexer)

[envio_ga-indexer](https://github.com/gnosischain/envio_ga-indexer) mirrors a Hasura / Envio HyperIndex GraphQL API for Gnosis Chain (Circles, Metri, Metri Pay, Gnosis Pay / Cashback, Investment) into ClickHouse so its 28 entities are queryable alongside dbt models. `chain_id = 100`.

## Purpose

The design is dictated by three verified source constraints: the source is **mutable in place, can delete rows, and exposes no change cursor, no row counts and no delete signal**. A hard 1000-row page cap forces keyset pagination by `id`; ids are opaque, case-sensitive strings, not time- or block-ordered.

Each entity is assigned a sync tier in `config/entities.yaml`: `block_cursor` (immutable, append-only — only `transfer` and `transaction`), `field_cursor` (a monotonic update field), `dual` (block discovery plus a periodic full rescan), or `full_rescan` (no usable cursor).

## Data

Database `envio_ga`.

| Table | Role |
|---|---|
| `ga_index_state` | All progress, append-only ReplacingMergeTree: `entity`, `partition_key` (`''` keyset walk, `block:lo-hi`, `realtime`, `rescan`), `cursor_end` (the resume key), `status`, `backfill_complete` |
| `raw_entities` | Full JSON payload per observation with a hash; **no TTL** — it is the mutation history the API destroys on in-place update |
| 28 typed tables | `transfer`, `transaction`, `transaction_action`, `avatar`, `token`, `trust_relation`, `cashback`, `profile`, … each ReplacingMergeTree keyed by `id` with `_deleted`, `_synced_block`, `insert_version` |

`transaction_action` is ~200M rows and unpartitioned; `transfer` ~108M.

!!! warning "Never `FINAL` on any `envio_ga` table"
    It OOMs the instance. Always:
    ```sql
    SELECT id, argMax(value, insert_version) AS value
    FROM envio_ga.transfer GROUP BY id
    HAVING argMax(_deleted, insert_version) = 0;
    ```

## Operating and recovering

### How it runs

A realtime Deployment (`load realtime`, one replica, `Recreate`, entity-sharded — **never scale it**) and a daily reconcile CronJob at **03:00 UTC** (`reconcile`) that diffs the live id set to find upstream deletes. All checkpoints are durable and every write is id-keyed ReplacingMergeTree, so kill, restart and rollout are safe at any moment.

`envio_ga` is not on the MCP allowlist, so its checks run from a pod or the console.

### Health — is it us, or is the source halted?

Ask this **first**. The upstream API has halted table-by-table before (2026-07-27 to 09-10), leaving 55 production dbt models stale while our indexer was fine.

- Chain head **not** advancing → the **source** stopped. Nothing to fix here.
- Chain head advancing, entity watermark flat → **us**.

The `envio-ga-head-stalled` alert (head not advanced in 30 min) fires for the *source* stopping, not only for our indexer. Read it that way.

A healthy pod logs **nothing** on a tick where no rows changed — the block-sync and field-sync lines are gated on there being work (the rescan line logs unconditionally). Only 14 of the 28 entities ever write a `partition_key='realtime'` state row; the 14 `full_rescan` entities write `'rescan'`, once per interval. Do not expect every entity to tick.

### Detecting a gap

```bash
python -m src.main maintain check
```

**This is the only honest completeness signal.** It computes completeness as the **minimum over block sub-chunks** — a single chunk's flag once reported COMPLETE while the data was short. Two caveats on its output: only `transfer` and `transaction` ever get block chunks, and the "stuck pages" section is always empty because that claim path is dead code.

Never judge completeness from row counts, and never run `maintain fix` or `load backfill` without `--entities` — both default to all 28.

### Repairing

```bash
python -m src.main maintain fix --entities ⟨X⟩ --block-range ⟨LO⟩:⟨HI⟩
```

Run it as a one-shot job cloned from the reconcile CronJob with a memory bump ([how](../../operations/runbooks/one-shot-jobs.md)) — never by exec'ing into the realtime pod.

!!! warning "`maintain fix --entities X` without a range can launch a 4-worker backfill"
    It does so silently if any failed or dead page exists — inside a 1 Gi pod that is the OOM.

!!! warning "The `--block-range` path can turn a corrupt range into an empty one"
    It deletes the window and re-fetches, but **skips writes whose payload hash is unchanged**. If the upstream payload did *not* change, the range ends up empty. Record the window's live row count first, and confirm the upstream payload actually changed. It also writes no `ga_index_state` row, so the chunk's own flag is unchanged by the repair.

**Re-deriving typed tables with zero API calls:**

```bash
python -m src.main maintain reprocess --entities ⟨X⟩
```

Rebuilds the typed tables from `raw_entities` — the reason that table has no TTL. It has **no range flag** (it walks the entity's entire raw history), and on a non-deletable entity it resets every `_deleted=0` permanently.

### Reconcile

`Reconcile walk incomplete; skipping tombstone` is **the safety mechanism working**. Never force it — a partial walk would tombstone live rows. Never `reconcile --entities transfer` (or `transaction`, `transaction_action`): those are `deletable: false` precisely because a full id-walk of a 100M+ row entity is not viable. 18 entities are deletable.

### Restart

Safe at any point; re-run the same command and it resumes from the furthest completed `cursor_end`.

!!! warning "Never run `python -m src.main status` against production"
    It executes an unscoped `count()` over a `GROUP BY id` subquery for **every** one of the 28 entities.

### Then dbt

Fix the mirror first with `maintain reprocess`, then use the scoped dbt lever from [dbt reprocess](../../operations/runbooks/dbt-reprocess.md). Never reach for a dbt full refresh to fix envio-derived models.

!!! note "Expected noise"
    - Silence on a no-change tick.
    - `maintain check` reporting zero stuck pages, always.
    - A `full_rescan` entity with no `realtime` state row.

!!! info "Internal runbook"
    [runbooks/25-envio-ga-indexer.md](https://github.com/gnosisdevops/infrastructure-gnosis-analytics/blob/main/runbooks/25-envio-ga-indexer.md) — private repository; carries the cluster-specific commands for this page.
