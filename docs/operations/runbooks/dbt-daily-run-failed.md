---
title: dbt Daily Run Failed
description: Reading last night's dbt failure, classifying it, rerunning only what failed, and the refusal triage
---

# The dbt daily run failed

The daily run is a Kubernetes CronJob at **06:00 UTC**, ~3h40m, with `concurrencyPolicy: Forbid`, `backoffLimit: 0` and `restartPolicy: Never` — **one attempt, no Kubernetes retries**. That is deliberate: the orchestrator owns retries internally.

It runs `cron_preview.sh` → `scripts/run_dbt_observability.sh`, whose only mandatory step is `dbt-run`. `source-freshness` failing every night is expected and non-mandatory.

Separately, a **live loop** Deployment runs `dbt run --select tag:live` (19 models) every 45 s, and a static server Deployment serves the published logs and metrics.

## 1. Read the failure

Find the failed job's pod and grep its log:

```text
MANDATORY STEP FAILED | ] Failed: | Code: [0-9]+ | REFUSED | TRANSIENT= | PERMANENT=
```

Only three job records are kept per outcome, so a pod older than ~3 runs is gone. After that, the published artifacts are served by the static server under `/logs/` and `/reports/` — reach it with a port-forward.

!!! warning "Not the storage bucket"
    Operators have no grant on the artifact bucket; only the cron and server service accounts do. The port-forward to the server is the route.

!!! warning "No `clickhouse-client` in the image"
    Warehouse checks go through the MCP tool, the console, or the in-image Python client.

The orchestrator's step summary, the `TRANSIENT=` / `PERMANENT=` lines and the retry outcome go to **stdout only** — they are not in the published `dbt.log`.

## 2. Classify

Transient: `Code: 159 | 209 | 210 | 394`, `QUERY_WAS_CANCELLED`, `TIMEOUT_EXCEEDED`, `SOCKET_TIMEOUT`, `NETWORK_ERROR`, `SSLError`, `UNEXPECTED_EOF_WHILE_READING`, `HTTPSConnectionPool`, `RemoteDisconnected`, `ConnectionResetError`, `Broken pipe`.

!!! warning "`Code: 241` is PERMANENT unless the message also says `OvercommitTracker`"
    With it, you were a cross-tenant victim, not the cause. Several unrelated steps failing on 241 in one window → [Warehouse out of memory](warehouse-oom.md) first; nothing here will help.

`Code: 341` on a daily run means a mutation OOMed — the model needs the microbatch path, not a retry. `Code: 388` means the merge pool is full; wait, do not loop-retry.

The cron already retried transients once at `--threads 1`, so what you see failed twice.

## 3. Is it failed, or still running?

A job past ~3h40m may be stalled rather than failed: check whether it is still active, whether the last log line is moving, and its resource usage.

!!! warning "Before re-running anything on a `delete+insert` model"
    ```sql
    SELECT * FROM system.mutations WHERE is_done = 0 AND is_killed = 0 ORDER BY create_time DESC LIMIT 20;
    ```
    `is_done=0, is_killed=0` is not dead. With `mutations_sync: 0` the lightweight DELETE keeps executing server-side after dbt reports failure — the DELETE lands, the INSERT never runs, and months vanish with no error. `KILL MUTATION` it first.

## 4. Rerun only what failed

The failed node ids are in the per-batch stash:

```bash
python /app/scripts/refresh/classify_failed_nodes.py --stash-dir /app/target/failed_batches
# prints TRANSIENT=<ids> and PERMANENT=<ids>
dbt run --select ⟨node⟩+ --threads 1
```

Run these inside a one-shot dbt job ([how](one-shot-jobs.md)). The flag is `--stash-dir`, not `--dir`.

!!! warning "The stash dies with the pod"
    It lives on the pod's ephemeral volume and is not published. If the pod is gone, rebuild the failed set from the model-status metric or the log. A one-shot job gets exactly one attempt, so `--resume` is inert across pods. And `Forbid` cannot see a hand-created job — never launch one while the 06:00 pod is running, or two pods rebuild `tag:production` and duplicate rows.

## 5. Refused stages

```text
grep REFUSED
```

!!! warning "Grep the log, not the metric"
    `dbt_model_status{status="refused"}` can read 0 on exactly the nights it matters: refusal records carry no `results` key, and the retry-transient cleanup globs `*.json` in the stash and unlinks any file with no error results — which is every refusal record — before the metrics emitter runs.

A refusal means the model's watermark is more than `--max-slices-per-stage` (30) days behind, so the daily runner declined to catch it up one day at a time. **Three causes, three answers:**

| Cause | How to tell | Answer |
|---|---|---|
| **No consumers** | no downstream model, no semantic reference, no `api` / `expose_to_mcp` meta, no production-tagged test | Deprecate: drop the `production` tag, keep the table, put the re-enable recipe in the file header |
| **Stalled** | on-chain activity exists *after* the watermark | `full_refresh.py --select ⟨m⟩ --stage _default --incremental-only`, then rebuild its downstream chain |
| **Dormant** | last on-chain activity == the watermark | The table is complete. It needs a policy, not a backfill |

Finding consumers — the manifest closure, plus the two surfaces dbt does not know about:

```bash
dbt ls -s ⟨model⟩+ --resource-type model --output name
grep -rn "⟨model⟩" semantic/                          # semantic layer
grep -rn "dbt\.⟨model⟩" ../metrics-dashboard/src/queries/   # dashboard SQL
```

Stalled vs dormant — compare the table's max against the chain. `*_events` models read `execution.logs` by `address`; `*_calls` models read `execution.transactions` by `to_address`:

```sql
SELECT max(block_timestamp) FROM dbt.⟨model⟩;
SELECT max(block_timestamp), count() FROM execution.logs
WHERE address = '⟨addr_no_0x_prefix⟩' AND block_timestamp > ⟨watermark⟩;
```

!!! warning "The runner's printed fix omits `--incremental-only`"
    It prints a `full_refresh.py` command per refused model. Run as printed it **drops the table** and rebuilds from the model's configured start date. Always add the flag.

Never raise `--max-slices-per-stage` on the cron path. The cap exists so a multi-month gap is routed to `full_refresh.py` instead of being ground through the nightly window.

## 6. The live loop

Restart the live-loop workload. `tag:live` models freeze while it is down and catch up on restart. One replica, `Recreate` — never scale it, even temporarily: two pods would run the same incremental models against the same tables concurrently. Do not restart it twice in quick succession expecting faster catch-up; each restart is another gap.

## 7. Suspend drift, both directions

A pause set directly on the cluster vanishes at the next Terraform apply. A Terraform pause needs an apply to lift. Whichever you did, say so — there is no reconcile loop. Do not use the stack's cutover switch to pause just the cron: it zeroes the live loop and the server too.

## 8. Resuming an interrupted multi-model rebuild

A consumer rebuild stopped part-way leaves no usable resume state — `target/refresh_state/` is on the pod's ephemeral volume. Rebuild the list from each model's own watermark:

```sql
SELECT 'model_a' AS m, max(date) FROM dbt.model_a
UNION ALL SELECT 'model_b', max(date) FROM dbt.model_b;
```

Models already at the expected date are done; the rest need re-running in DAG order.

!!! note "Expected noise"
    - `source-freshness` failing nightly — non-mandatory, and the cause is upstream.
    - `dbt-run:all=FAIL(rc=2)` in an older summary that nonetheless exited 0 — the retry recovered it.
    - No Elementary output anywhere. It is switched off; three alert rules that query `elementary.model_run_results` ship paused and cannot be unpaused as written.
    - `dbt docs generate` writing a catalog with 0 model nodes — known dbt-clickhouse behaviour.

!!! info "Internal runbook"
    [runbooks/30-dbt-daily-run-failed.md](https://github.com/gnosisdevops/infrastructure-gnosis-analytics/blob/main/runbooks/30-dbt-daily-run-failed.md) — private repository; carries the cluster-specific commands for this page.
