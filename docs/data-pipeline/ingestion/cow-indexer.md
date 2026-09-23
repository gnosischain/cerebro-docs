# CoW Protocol Indexer (cow-indexer)

[cow-indexer](https://github.com/gnosischain/cow-indexer) is a standalone, multi-chain indexer for CoW Protocol. It reads canonical contract events directly from EVM JSON-RPC, enriches discovered orders and settlements through the public CoW API, and optionally imports authoritative off-chain history bundles. It does not depend on dbt or any existing ingestion pipeline.

## Overview

The indexer covers every chain CoW Protocol is deployed on -- mainnet, Gnosis, Arbitrum One, Base, BNB, Polygon, Avalanche, Linea, Ink, and Plasma, plus the Sepolia testnet -- each with its own API base URL, deployment file, and finality window configured in `config/chains.yaml`. Chains without an available RPC can be disabled individually.

Three properties define the data model:

- Every identity includes `environment` and `chain_id`, so multiple chains coexist in one schema.
- Addresses and hashes are stored lowercase, and raw RPC, API, and export payloads are retained alongside decoded rows.
- Token amounts use ClickHouse `UInt256`, avoiding precision loss on settlement values.

Archive state and traces are not required from the RPC provider, but it must serve historical `eth_getLogs` calls back to each configured deployment block.

## Architecture

```mermaid
graph LR
    subgraph Sources
        RPC[EVM JSON-RPC<br/>logs and blocks]
        API[CoW API<br/>orders, trades, competitions]
        EXP[Export bundle<br/>Parquet]
    end

    DEC[Decoders]

    subgraph CH[ClickHouse]
        CAN[(Canonical tables<br/>orders, trades, competitions)]
        CKPT[Checkpoints and<br/>reorg reconciliation]
        WQ[Durable API enrichment<br/>work queue]
    end

    RPC --> DEC
    API --> DEC
    EXP --> DEC
    DEC --> CAN
    CAN --- CKPT
    CAN --- WQ
```

The indexer owns its ClickHouse schema through numbered migrations covering indexing state, raw sources, orders, trades, solver competitions, metadata, and the committed `*_canonical` views. The target database is set via `CLICKHOUSE_DATABASE` (repository default `cow_indexer`; the Cerebro deployment uses `cow_db`).

## Coverage model

The mandatory RPC and API path provides complete indexed history for the configured on-chain contracts, and the maximum order-book history that is publicly discoverable from order UIDs, owners, transactions, and competitions. It cannot discover an off-chain order that never executes when neither its UID nor its owner is otherwise known.

The optional Parquet export interface closes that gap when an authorized CoW order-book database export is available.

!!! note
    "Complete off-chain history" may only be claimed when a validated export manifest declares the required historical boundary. Without a bundle, off-chain coverage is discoverable-only by design.

## Running modes

Each mode is a subcommand of the same binary. They share the ClickHouse schema and the durable checkpoints, so they interleave safely.

| Mode | Command | Purpose |
|------|---------|---------|
| Preflight | `preflight --chain <all\|key>` | Read-only readiness check: RPC head, historical `eth_getLogs` at the deployment block, and CoW API reachability per chain |
| Migrate | `migrate` | Apply idempotent `migrations/*.sql`; run before any ingestion |
| Backfill | `backfill --chain <sel> [--from-block N] [--to-block M]` | One-shot forward scan from the checkpoint (or a bound) up to the safe head |
| Repair | `repair --chain <key> --from-block N --to-block M` | Rescan a bounded range and reconcile reorgs and gaps without moving the forward checkpoint backward |
| Continuous | `continuous --chain <all\|key>` | Long-running service: forward scan, finality-window rescan, competitions, active orders, enrichment, and token prices per chain |
| Inspect | `status`, `coverage --chain <sel>`, `validate --chain <sel>` | Report per-chain checkpoints, historical coverage, and reconciliation checks |
| Export import | `inspect-export`, `import-export`, `validate-export` | Optional authoritative off-chain Parquet bundle import |
| Orderbook backfill | `backfill-orderbook <probe\|seed-orders\|seed-owners\|drain\|status>` | Replay historical off-chain orders through the public API into `orders` (`source='backfill'`) |

The typical lifecycle is `preflight` -> `migrate` -> `continuous`; the continuous service backfills each chain from its pinned deployment block up to the tip and then tracks the head. Every chain runs independently -- a failing chain retries in isolation and does not stop the others.

!!! warning
    A fresh chain with no checkpoint starts at the earliest pinned `from_block` in its `deployments/*.json`. Pin those blocks (not `0`) to avoid scanning from genesis.

## Log scanning and reorg handling

The scanner starts with 5,000-block `eth_getLogs` requests. Successful ranges grow to 50,000 blocks; provider range or response-limit errors halve the request down to a 50-block minimum. Limit errors are recognized by JSON-RPC code and message (`-32005`, "too many logs", "block range") even when the provider returns them with a non-200 HTTP status, so they trigger adaptive halving (logged as `rpc_range_reduced`) rather than aborting the scan. Every RPC call has a hard request timeout, so a hung provider raises a retryable error instead of parking the scan.

Writes are committed in a fixed order per range: raw logs, block headers, decoded events, then the checkpoint.

Reorg handling is non-destructive:

- Continuous ingestion stores canonical block hashes throughout the finality window and rescans that window on every cycle.
- A replacement block hash makes logs from the abandoned block non-canonical at query time; the reorg-aware `*_canonical` views drop orphaned-hash rows without mutating data.
- The `*_canonical` views are additionally bounded to the committed checkpoint, so they never expose partially-processed rows.
- Checkpoints never move backward: `repair` rescans a bounded range while leaving the durable forward checkpoint in place.

## API enrichment

Event discovery creates deterministic work identities for order UIDs, owners, settlement transaction hashes, app-data hashes, and token addresses. Order lookups are batched into the documented maximum of 128 UIDs per call; account orders and trades paginate in 1,000-row pages.

The client uses `curl_cffi` browser TLS impersonation because CoW's edge distinguishes -- and blocks -- ordinary Python TLS clients by their TLS/JA3 fingerprint. This is required even with an API key, which is sent as `X-API-Key` and raises the allowance to roughly 30 RPS. A single adaptive rate limiter is shared across all chains (they hit the same host and key); it applies bounded exponential backoff on retryable statuses and backs the global rate off toward `COW_API_MAX_INTERVAL_SECONDS` on `429`/`403`, recovering as requests succeed.

The work queue is an append-only, restart-safe ClickHouse table. Terminal revisions (`done`, `dead`, `unavailable_from_public_api`) dominate the ReplacingMergeTree merge, so replayed chain ranges do not revive completed work while those rows exist. To keep the queue bounded, a scheduled maintenance task purges terminal work items older than a grace window (`COW_PURGE_GRACE_HOURS`, default 24 hours). This is finite-window deduplication: a later rediscovery after the purge re-creates a fresh pending item and re-enriches it, which is safe because handler writes are idempotent. Items that exhaust `COW_MAX_ATTEMPTS` land in `dead_letters` for inspection.

!!! warning
    Run only one enrichment worker replica per `(environment, chain_id)`. ClickHouse does not provide a transactional competing-consumer lease.

## Historical order-book backfill

Live API capture only starts at deployment time, but the chain holds years of traded order UIDs and trader addresses. `backfill-orderbook` replays that off-chain history through the public CoW API into `orders` (`source='backfill'`) using the existing work queue, without touching the live ingestion path.

The design is two-pass:

1. **Seed orders / drain** -- distinct traded UIDs missing from `orders` are batched into 128-UID work items and fetched via `POST /orders/by_uids`, recovering every executed order.
2. **Seed owners / drain** -- one work item per distinct trader, paged via `GET /account/{owner}/orders`, recovering expired and cancelled orders that never executed. Owners who never traded stay invisible.

The drain uses its own rate limiter and concurrency budget, fully separate from the live enrichment loop, so a throttled backfill never slows live ingestion and `drain` is safe to run beside `continuous`. Progress lives in the work items themselves: terminal states survive restarts and re-seeding is a no-op while items remain within the purge grace window.

!!! info "Feasibility floor"
    The public API serves full order JSON back to roughly 2022-07 (the order-book migration epoch); 2021-era UIDs return 404 and are counted as missing data, never as failures. The `probe` subcommand makes this gate repeatable. The 2021 epoch -- and authoritative fields such as cancellation timestamps -- remain reachable only via the export bundle path.

!!! note "Timestamp caveat"
    Backfilled `status:{status}` order events carry observation-time timestamps, not historical ones. Pre-capture cancelled-unfilled orders have no cancel time and are treated as open until `valid_to` by downstream reconstruction.

## Observability

The continuous service serves three endpoints on `COW_METRICS_PORT` (default 9090):

| Endpoint | Purpose |
|----------|---------|
| `/health` | Process liveness |
| `/ready` | ClickHouse connectivity |
| `/metrics` | Prometheus metrics |

Exported metric families (labeled by chain):

| Metric | Meaning |
|--------|---------|
| `cow_chain_lag_blocks{chain}` | Safe head minus the committed scan position |
| `cow_rows_written_total{chain,table}` | Rows written per table |
| `cow_rpc_requests_total{chain,method,status}` | RPC request counts |
| `cow_api_requests_total{chain,route,status}` | CoW API request counts, labeled by templated route |
| `cow_request_seconds{source,chain}` | RPC/API latency histogram |

There is deliberately no exact pending-work gauge: computing one requires a full-table `FINAL` over the append-only work queue, which is the memory risk the design removes.

!!! note
    During a backfill, `cow_chain_lag_blocks` is legitimately large until a chain catches up. Alert on "no rows written in an hour" and pod health rather than on lag thresholds; treat lag thresholds as steady-state signals to enable only after the initial backfill completes.

## Configuration

All configuration is environment-based. Key variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `CLICKHOUSE_HOST` / `CLICKHOUSE_PORT` | -- / `8443` | ClickHouse Cloud endpoint (secure native-HTTP) |
| `CLICKHOUSE_DATABASE` | `cow_indexer` | Target database (must already exist) |
| `COW_RPC_URL_<CHAIN>` | -- | Per-chain JSON-RPC endpoint (e.g. `COW_RPC_URL_GNOSIS`) |
| `COW_CHAIN` | `gnosis` | Chain selection for the Docker Compose service (`all` for every enabled chain) |
| `COW_API_KEY` | -- | CoW API key, sent as `X-API-Key`; without it the public edge throttles under load |
| `COW_API_INTERVAL_SECONDS` | `0.1` with key, `0.6` without | Global enrichment pacing shared across all chains |
| `COW_API_MAX_INTERVAL_SECONDS` | `5.0` | Adaptive backoff ceiling on `429`/`403` |
| `COW_ENRICH_CONCURRENCY` | `6` | Bounded concurrent enrichment work items |
| `COW_MAX_ATTEMPTS` | `6` | Attempts before a work item is dead-lettered |
| `COW_PURGE_ENABLED` / `COW_PURGE_GRACE_HOURS` | `true` / `24` | Scheduled retention of finished work items |
| `COW_BACKFILL_INTERVAL_SECONDS` | `0.5` | Order-book backfill pacing (separate limiter) |
| `COW_BACKFILL_CONCURRENCY` | `2` | Order-book backfill concurrency |
| `COW_METRICS_PORT` | `9090` | Health and metrics port |

See the [repository README](https://github.com/gnosischain/cow-indexer) for the full variable reference, export-bundle tooling, and failure-recovery runbook.

## Operating and recovering

### How it runs

One continuous Deployment running `continuous --chain all` — **11 chains in one process**, each with six independent loops — plus a 6-hourly sweep CronJob running `backfill-orderbook seed-orders` then `drain`. Kill-safe: checkpoints are durable, writes are idempotent by key, and commit order is raw logs → block headers → decoded events → checkpoint. `Recreate`, one replica, **never two even for a second**; run only one enrichment worker per chain — ClickHouse has no transactional competing-consumer lease.

### Health — per chain, never summed

```sql
SELECT chain_id, argMax(block_number, updated_at) AS checkpoint_block,
       dateDiff('minute', max(updated_at), now()) AS lag_min
FROM cow_db.indexing_checkpoints WHERE source = 'rpc'
GROUP BY chain_id ORDER BY lag_min DESC;
```

!!! warning "One dead chain leaves the pod green and the summed row-rate healthy"
    Verified 2026-09-22: one chain frozen for six weeks, another ~2 h behind, the other nine ≤ 6 min — and the stalled-rows alert, which sums `cow_rows_written_total` across chains, saw nothing. Alert on "no rows written in an hour" per chain and on pod health, never on lag: `cow_chain_lag_blocks` is legitimately enormous during any catch-up.

!!! warning "Do not aggregate `trades_canonical` unscoped"
    The block-hash join hits the **4 GiB per-query** limit. Read the checkpoint table instead. And never a bare `FINAL` over a data table — read the `*_canonical` views, scoped.

If you query `settlements`, drop any `environment='production'` filter or `GROUP BY environment, chain_id`: sepolia is `environment='testnet'` and invisible otherwise.

### Detecting a gap and repairing

```bash
cow-indexer status                      # takes no --chain
cow-indexer coverage --chain all
cow-indexer validate --chain all
cow-indexer repair --chain ⟨one⟩ --from-block ⟨lo⟩ --to-block ⟨hi⟩
```

`repair` never moves the forward checkpoint backward and is explicitly the deep-reorg and gap fix — safe alongside the tailing loop. Holes in `indexing_ranges` are **not** proof of missing data: its inserts ack at the async buffer and are lost on an abrupt kill. Cross-check `raw_rpc_logs` / `settlements`. A "gap" from block 1 to each chain's pinned `from_block` is normal.

!!! warning "Never delete or rewind `indexing_checkpoints` to force a rescan"
    The chain then restarts at its pinned deployment block and rescans years. `cow_db` tables are Shared\*MergeTree and **do not dedupe re-inserted rows** unless the ORDER BY key matches exactly — a re-insert is not automatically idempotent.

### Orderbook history

Off-chain orders that predate live capture: `backfill-orderbook seed-orders --chain ⟨c⟩ --limit 2000`, then `drain`, then `status`. The 6-hourly sweep is the live lane's **designed complement**, not a backfill hack — it closes the 1 h–24 h enrichment leak. A failed slot self-heals at the next slot; only act if two consecutive fail.

!!! warning "Two things never to do with the sweep"
    Never `seed-orders` without `--limit` as a way to "reprocess everything": the pre-2022-Q3 epoch is unserved by the API and the sweep is a ~900K-call operation. Never start a manual drain inside the scheduled sweep window — a hand-created Job is invisible to `concurrencyPolicy: Forbid`, and two drains race `work_items`.

### Code 241 on the lease

The `work_items` lease uses `FINAL`; too many parts pushes it over its per-query cap. It fails in isolation — RPC ingestion keeps running. `OPTIMIZE TABLE cow_db.work_items FINAL`, then lower `COW_ENRICH_BATCH` and/or raise `CLICKHOUSE_FINAL_MEMORY_MB` in the stack. Never force `lightweight_delete_mode='lightweight_update_force'` on any `cow_db` table — `work_items` has no block-number column and ClickHouse Cloud rejects the statement.

`purge-work --chain ⟨c⟩ --grace-hours 24` requires the scheduled purge **disabled** and the continuous pod **down** — never run it inside the live pod, where the purge loop is already running. Never hand-edit `work_items` rows to clear a lease: attempts are the retry budget, and burning them dead-letters work nothing ever processed.

### The shared egress identity

cow-indexer and click-runner's `cow-fees` leave the cluster from **one** NAT address, which is CoW's rate-limit identity. A 403 storm on one affects the other. **Never retry inside the cooldown** (~1 h): retrying prolongs it for everything sharing the address. Re-allowlisting is a conversation with CoW. Never move the indexer to a public node to get off the shared address — an Autopilot public node's IP is ephemeral and can never be allowlisted.

### Then dbt

**Nothing to rebuild.** dbt does not read `cow_db` at all — the CoW models read the on-chain decode from `execution`, so a `cow_db` repair has no dbt consequence. The canonical views are computed at read time, so consumers see corrected data immediately.

!!! note "Expected noise"
    - `rpc_range_reduced` warnings — the scanner starts at 5,000 blocks, grows to 50,000, and halves to 50 on the provider's result cap.
    - "No Jobs listed" for the sweep — finished Jobs are deleted after 24 h and only three of each outcome are kept.
    - Huge `cow_chain_lag_blocks` during catch-up.

!!! info "Internal runbook"
    [runbooks/24-cow-indexer.md](https://github.com/gnosisdevops/infrastructure-gnosis-analytics/blob/main/runbooks/24-cow-indexer.md) — private repository; carries the cluster-specific commands for this page.

### Redeploying

On an image roll the scanner restarts; the sweep CronJob changes at its next slot. Apply outside 00:15-00:45 and 02:45-05:00 UTC and never during an API 403 storm. The decisive proof is every live chain advances, no unexplained empty log bucket, no new dead letters. Procedure: [Redeploying a service](../../operations/deployment.md#redeploying-a-service).

## Downstream consumers

The indexed database backs the [CoW Explorer](../../mcp/mini-apps/cow-explorer.md) MCP mini-app, a read-only data explorer over the canonical order, trade, and competition tables. Because the indexer is independent of dbt, its tables are also available as an upstream source for dbt models in the transformation layer.
