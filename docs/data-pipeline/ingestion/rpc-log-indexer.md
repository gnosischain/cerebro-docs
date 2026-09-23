# RPC Log Indexer (rpc-log-indexer)

[rpc-log-indexer](https://github.com/gnosischain/rpc-log-indexer) is a small, durable event indexer: `eth_getLogs` → ABI-decode by `topic0` → append to ClickHouse, with adaptive range sizing, per-chain checkpoints and reorg-safe canonical views. It is the **event** sibling of [rpc-state-indexer](rpc-state-indexer.md), which snapshots **state**, and shares none of its census machinery.

## Purpose

Today it tracks one contract on two chains: the Snapshot **DelegateRegistry** on Ethereum mainnet and on Gnosis, events `SetDelegate` / `ClearDelegate`, scoped server-side to the `gnosis.eth` space via a topic filter. This is the on-chain source behind the governance delegation models in dbt (the data Dune publishes as `snapshot_ethereum.delegateregistry_evt_*`).

It makes **no `eth_call`** at all — events carry every field — so one archive RPC per chain is sufficient; historical ranges do require archive log access.

## Data

Database `rpc_log_indexer`. Every row keys on `(environment, chain_id)`.

| Table | Role |
|---|---|
| `raw_rpc_logs` | Logs exactly as fetched. **The reprocessable source of truth** — decoding is derived and rebuildable from here |
| `decoded_events` | ABI-decoded; fields in a canonical JSON `args` column |
| `chain_blocks` | One row per block number converging to the latest-observed hash — the reorg mechanism |
| `indexing_checkpoints` | **Per `(environment, chain_id)` — not per contract.** The committed forward position |
| `indexing_ranges` | Per-window audit trail. Records only `complete`; the `error` column is never populated |

**Consumers must read the `*_canonical` views** (`raw_rpc_logs_canonical`, `decoded_events_canonical`, and on top of them `v_delegate_events`, `v_delegate_events_gnosis`). Each inner-joins block hashes and bounds to the committed checkpoint, so a reorged or uncommitted row never reaches them. A chain with no committed checkpoint exposes no canonical rows at all.

## Operating and recovering

### How it runs

One continuous Deployment, `CHAIN=all` — both chains in one process, each with its own RPC client and checkpoint. `continuous` loops: forward-scan to the safe head → a **finality rescan** of the last `finality_blocks` (which does not move the checkpoint) → sleep `POLL_SECONDS` → repeat. Range sizing starts at `INITIAL_RANGE` (5000), halves on a provider range-limit error down to `MIN_RANGE` (50), doubles on success up to `MAX_RANGE` (50000).

Single writer per chain, `Recreate`, one replica. The hazard for this service is **checkpoint contention and regression**, not row duplication: re-scanning the same range writes identical ORDER BY keys, which collapse under `FINAL`. `backfill` and `continuous` must never run together on one chain.

No CronJob and no Job exist in the stack. The migration Job was deliberately not ported — the schema already exists in the shared warehouse, and re-running it there is not a no-op.

### Health — checkpoint age, not data age

```sql
SELECT chain_id, argMax(block_number, updated_at) AS checkpoint_block,
       dateDiff('minute', max(updated_at), now()) AS lag_min
FROM rpc_log_indexer.indexing_checkpoints WHERE source = 'rpc'
GROUP BY chain_id ORDER BY chain_id;
```

!!! warning "`max(block_timestamp)` on the data tables is meaningless here"
    The contract emits a handful of events a month, so `decoded_events_canonical` can read weeks stale while the service is perfectly healthy. Verified 2026-09-22: last on-chain event 08-30 09:19, captured by the indexer 08-30 09:38, checkpoint at the chain head every minute since. Any freshness alert for this service must be written on checkpoint age.

**Normal behaviour that looks like a stall:** each cycle re-scans and re-logs the same window — ~64 blocks on ethereum, ~200 on gnosis. Steps are small and regular (ethereum ~32 blocks every ~6.4 min, gnosis ~16 every ~1.4 min) because that is head pace. Ethereum sitting on one window for several minutes, re-emitting it every ~13 s, is the finality rescan. **Verify both chains advance — gnosis alone is not proof.**

`indexing_ranges` is not a failure log; the pod log line is the sole record. A checkpoint that stops advancing → `scan_cycle_failed` in the log.

### Detecting a gap

The common cause is structural: **the checkpoint is per chain, not per contract.** Adding a contract to a running chain indexes it forward only; everything between its deployment block and the current checkpoint is silently skipped.

```sql
SELECT chain_id, min(from_block), max(to_block) FROM rpc_log_indexer.indexing_ranges
WHERE chain_id = ⟨id⟩ GROUP BY chain_id;
```

Compare against the contract's `from_block` in `config/deployments/<chain>.json`.

### Repairing

```bash
rpc-log-indexer repair --from-block ⟨lo⟩ --to-block ⟨hi⟩      # CHAIN must name ONE chain
```

`repair` passes `update_checkpoint=False`: it only inserts idempotent rows and never moves the forward checkpoint, so it is safe beside the running loop. Run it in a fresh pod ([one-shot jobs](../../operations/runbooks/one-shot-jobs.md)) — exec'ing into the live pod works for a narrow range, but its 512 Mi limit makes a wide repair an OOM that restarts `continuous`.

!!! warning "`backfill` is not `repair`"
    `backfill` **advances** the checkpoint and collides with the live `continuous`. Never use it to fill a gap below the checkpoint. And never repair a range you have not bounded first: a blind full-history repair issues one block RPC per block at concurrency 10.

**Deep reorg** — the same command. `repair` re-observes every block header in the range, so `chain_blocks` converges to the new canonical hashes and the orphaned-hash logs drop out of the canonical inner join automatically. **There is nothing to delete.**

!!! warning "Never `DELETE` from `chain_blocks`"
    The canonical views inner-join it, so removing headers erases *correct* logs from every consumer, with no error.

!!! warning "Never rewind the checkpoint near 06:00"
    While that gap is open the canonical views are truncated, and `dbt.int_governance_current_delegations` is a plain `table` rebuilt wholesale from them by any `dbt run` — including the unattended 06:00 cron, against which there is no lock.

### Restart

Kill and restart at any moment. The checkpoint advances only after a window's logs **and** block headers are written, and the canonical views expose nothing above it. Never scale above 1, never switch to `RollingUpdate`.

### Then dbt

`int_governance_current_delegations` is materialized `table` — a plain `dbt run -s` rebuilds it wholesale; no incremental lever applies. See [dbt reprocess](../../operations/runbooks/dbt-reprocess.md).

!!! note "Expected noise"
    - The same ~64 / ~200-block window re-scanned every cycle — the finality rescan.
    - `rpc_log_indexer_chain_lag_blocks` going flat rather than climbing when the RPC is down — the gauge needs the chain head, so it goes stale rather than growing.
    - A provider error mentioning a result or range cap (`-32602 "query exceeds max results"`, `-32005`) — handled by halving the window, logged as a range reduction. If the phrasing is one the classifier does not recognise, the scan **wedges** instead: add the phrase to the limit markers and probe every new provider against a dense range first.

!!! info "Internal runbook"
    [runbooks/23-rpc-log-indexer.md](https://github.com/gnosisdevops/infrastructure-gnosis-analytics/blob/main/runbooks/23-rpc-log-indexer.md) — private repository; carries the fresh-pod spec and the cluster-specific commands for this page.

### Redeploying

On an image roll the scanner restarts. Apply any time, never while a repair pod exists. The decisive proof is both checkpoints continue from checkpoint+1 with no range gap. Procedure: [Redeploying a service](../../operations/deployment.md#redeploying-a-service).

