# RPC Scans

Bulk on-chain data collection: sweep logs, batched view calls, storage slots, bytecode, and traces across block windows or address sets of any size, streaming the rows into ClickHouse **scratch tables** that you then analyse with ordinary SQL — joins against dbt models included.

This is the counterpart to the single-call tools in `src/cerebro_mcp/tools/web3/rpc.py` (`contract_explore`, `contract_call_function`, `contract_decode_transaction_input`, `contract_decode_receipt_logs`): use those for **one contract, current state**; use the scan family (`src/cerebro_mcp/tools/web3/rpc_scan.py`) when the job is **thousands of addresses or a block window** — e.g. incident forensics, holder sweeps, or verifying a pipeline independently of dbt. The `chain_forensics` persona ([Agent Fleet](../agents.md)) is built around this toolkit.

## Enabling

The family is registered only when `RPC_SCAN_ENABLED=true` (default off). Because the engine **writes** into ClickHouse, the deployment's ClickHouse user needs grants a read-only user usually lacks:

```sql
GRANT CREATE DATABASE, CREATE TABLE, INSERT, DROP TABLE, SELECT
ON scratch.* TO <CLICKHOUSE_USER>;
```

The scratch database name defaults to `scratch` (`RPC_SCAN_SCRATCH_DATABASE`) and is automatically added to `ALLOWED_DATABASES` so `execute_query` can read the results. Additional prerequisites:

- **Pinned-block reads** (any non-`latest` `block` argument) require `GNOSIS_ARCHIVE_RPC_URL`.
- **Trace scans** additionally require a trace-capable archive node (Erigon, or Nethermind with the Trace module).

## How jobs work

Every scan tool starts an engine job, waits up to `sync_wait_seconds` (capped server-side), and returns either the finished counts-first summary or a running snapshot — same shape either way. Key properties:

- **Partial rows are queryable mid-scan.** The scratch table exists from the start; you can run SQL against it while the job runs.
- **Results land in `scratch.rpc_*` tables** — one per job, e.g. `scratch.rpc_logs_<id>`, `scratch.rpc_calls_<id>`, `scratch.rpc_traces_<id>`, `scratch.rpc_blocks_<id>`. Tables expire after `RPC_SCAN_SCRATCH_TTL_DAYS` (default 7).
- **Jobs are resumable.** The engine checkpoints a cursor; a cancelled, failed, or restart-orphaned job continues into the *same* table via `rpc_scan_resume`. Tables are `ReplacingMergeTree`, so the one-unit overlap dedups on merge (count with `uniqExact` or `FINAL`).
- **Auto-chunking.** Log scans halve the block range on provider "range too large" errors and grow back after success — never pre-chunk manually. Trace scans chunk around the node's ~100-blocks-per-call `trace_filter` cap.
- **Address sets come inline or from SQL.** Small sets pass as a list; any size passes as `address_sql="SELECT safe_address FROM dbt.<model>"` — which also lets you chain scans (feed one scan's scratch table into the next).

## The scan family

| Tool | What it sweeps |
|---|---|
| `rpc_scan_logs(from_block, to_block, contracts?, event?, …)` | `eth_getLogs` over any block window. Decode via an event signature (typed `arg_*` columns), a contract's full ABI, or raw topics; filter a decoded argument against an address set (indexed args server-side at any set size). |
| `rpc_batch_call(calls, addresses?/address_sql?, block?)` | View-function reads across thousands of addresses via Multicall3 `aggregate3` (~600 reads per round trip; one reverting target never aborts a batch). Wide output: one row per address with typed `<alias>_out_N` columns. |
| `rpc_read_storage(slots, addresses?/address_sql?, block?)` | Raw `eth_getStorageAt` across an address set at one pinned block. Each value stored as hex, `value_uint`, and `value_address` for one-line SQL classification. |
| `rpc_get_code(addresses?/address_sql?, detect_proxies?)` | Classify every address by bytecode: EOA vs contract, `code_hash` clustering, EIP-1167 minimal-proxy detection, EIP-1967 implementation/admin/beacon slots. |
| `rpc_scan_traces(from_block, to_block, from/to filters, min_value_wei?)` | `trace_filter` sweep for **native xDAI value flows** and internal calls — the blind spot of every Transfer-log method. |
| `rpc_trace_transaction(tx_hash, max_depth?, store?)` | One transaction's full execution as an indented call tree (`debug_traceTransaction`), with net native-value movement per address; `store=true` persists frames to a scratch table. |
| `rpc_find_block(kind, …)` | Binary-search block finders: first block at/after a timestamp, first block where an address has code (deployment), or first block where a storage slot changed. The anchor-pinning primitive — resolve your incident window to blocks before any scan. |

## Job control

| Tool | Purpose |
|---|---|
| `rpc_scan_status(job_id)` | Progress (blocks/addresses done, rows written, ETA) for running jobs; full counts-first summary for terminal ones. |
| `rpc_scan_cancel(job_id)` | Stop a running scan. Partial rows are kept and the cursor recorded. |
| `rpc_scan_resume(job_id)` | Continue a partial/cancelled/orphaned scan from its persisted cursor into the same table. |
| `rpc_list_scans(limit)` | All jobs — in-memory plus the persisted registry (survives server restarts). |

## Typical forensics flow

```text
rpc_find_block(kind="timestamp", timestamp="2026-06-01T00:00:00Z")   # pin the window
rpc_scan_logs(from_block=…, to_block=…, contracts=[token],
              event="Transfer(address indexed from, address indexed to, uint256 value)")
execute_query("SELECT arg_to, uniqExact((block_number, log_index)) AS n
               FROM scratch.rpc_logs_<id> GROUP BY arg_to ORDER BY n DESC", database="scratch")
rpc_get_code(address_sql="SELECT DISTINCT arg_to FROM scratch.rpc_logs_<id>")   # classify recipients
rpc_scan_traces(from_block=…, to_block=…, to_addresses=[suspect])               # native-value residuals
```

## Guardrails

Selected limits from `config.py` (all overridable by env): `RPC_SCAN_MAX_CONCURRENT_JOBS=2`, `RPC_SCAN_MAX_ROWS_PER_JOB=5,000,000`, `RPC_SCAN_MAX_ADDRESSES=500,000` per resolved set, `RPC_SCAN_MAX_INLINE_ADDRESSES=500` (larger sets must come via `address_sql`), `RPC_SCAN_TRACE_MAX_RANGE_BLOCKS=200,000`, and non-indexed log filtering requires a window ≤ `RPC_SCAN_UNINDEXED_FILTER_MAX_BLOCKS=250,000`.

## When *not* to scan

For long-history aggregates that dbt already models, use `execute_query` directly — a scan re-collects what the warehouse already has. The scan engine shines when the window is recent (not yet in dbt), the event isn't decoded by any model, or you need pipeline-independent verification.

## See also

- [Tools — Web3](../tools.md#web3) — the full tool reference
- [Contract Explorer](../mini-apps/contract-explorer.md) — single-contract interactive surface
- [Setup — Feature flags](../setup.md#feature-flags) — `RPC_SCAN_ENABLED` and friends
