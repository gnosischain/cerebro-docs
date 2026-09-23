---
title: One-Shot Jobs
description: How repair and maintenance commands actually run on GKE Autopilot, now that the old one-shot Jobs are gone
---

# Running a one-shot repair on Autopilot

Every repair command in these runbooks needs somewhere to run. The one-shot Jobs that ran them on the old cluster (`maintain`, `historical`, `validate`, `repair`, `migrate`) were deliberately **not** ported. This page is what replaced them.

## The mechanism

Clone the app's existing CronJob template into a fresh Job, injecting the change **while rendering** (a Job's pod template is immutable once created), then apply it. The clone inherits the secrets, volumes, resource requests and — where it matters — the protective environment the CronJob already carries.

| App | Clone source | What is overridden |
|---|---|---|
| cryo (Gnosis, Celo) | the auto-maintain CronJob | **env only** — `OPERATION`, plus `START_BLOCK` / `END_BLOCK`. cryo takes no `command`; its entrypoint dispatches on env, so a `command` override would bypass it |
| beacon | the daily validators CronJob | `command`, **and `ENABLED_LOADERS`** (see the trap below) |
| envio | the reconcile CronJob | `args`, with a memory bump — the reconcile template is sized for an id-diff sweep, not for `fix` |
| dbt | the daily CronJob | `args` |
| click-runner, ip-crawler | the specific ingestor's CronJob | nothing, or `args` for one leg |
| rpc-log | **no CronJob exists** — a fresh pod from the deployment's image with the same secrets | `args` |
| rpc-state | **the Terraform-gated backfill Job** — never clone; the writer lease forbids a second writer | see [RPC State Indexer](../../data-pipeline/ingestion/rpc-state-indexer.md) |

Two universal caveats:

!!! warning "A hand-created Job is invisible to `concurrencyPolicy: Forbid`"
    It carries no ownerReference, so it never appears in `.status.active`. Check nothing is already running before creating one.

!!! warning "You must delete it"
    A cloned Job sets no `ttlSecondsAfterFinished`.

## Per-app preconditions

**cryo `maintain`** claims all non-completed ranges and DELETEs each range *before* it claims it. The stop sequence first: scale the continuous writer to zero, suspend the auto-maintain cron, wait for the pod to be gone, **and confirm no auto-maintain pod is still running** — suspending a cron does not stop an in-flight Job. All of that is `[drift]` that the next apply reverts. Chunk to a few hundred thousand blocks per Job: ephemeral storage is capped at **10 Gi**, an Autopilot hard ceiling. Cloning the auto-maintain cron inherits its `MODE=custom` + explicit `DATASETS`, which is what keeps `MODE=full` from expanding to a 41.9M-block backfill; a hand-rolled pod would not.

**cryo `validate`** writes nothing, so it can simply be exec'd in the running continuous pod with `OPERATION=validate` and a block range. It exits non-zero when gaps exist.

**beacon** — a `--loaders` name that is **not** in the pod's `ENABLED_LOADERS` is dropped from the filter entirely, and selection falls open to **every** loader in the range. The validators cron ships `ENABLED_LOADERS=validators`, so every clone must override that variable to a superset of the loaders you name. `check` and `--dry-run` are read-only and safe beside realtime; `fix` reloads and re-transforms, so pause realtime and transform for overlapping slot ranges. Never run a `--force` fix from the transform workload: it has no beacon credentials, so it deletes and then fails.

**envio** — never run `fix` or `reprocess` by exec'ing into the realtime pod; that pod is 1 Gi and the 4-worker backfill `fix` can launch will OOM it. If an entity the realtime loop is actively writing must be repaired, pause the loop first (`[drift]`; it is otherwise never to be scaled).

**dbt** — five things:

- Only `dbt_incremental_runner.py` accepts `--project-dir` / `--profiles-dir`. `refresh.py` and `gap_window_refresh.py` reject them and exit 2 at argparse.
- `--resume` is inert in a clone: `backoffLimit 0` + `restartPolicy: Never` means exactly one attempt, and `target/refresh_state/` lives on the pod's ephemeral volume.
- Overriding `args` **drops the publish step**, so artifacts never reach the bucket and the pod log is the only record. Read it before deleting the Job.
- There is no lock against the 06:00 cron, and `Forbid` cannot see your Job. Run in a quiet window.
- The pre-flight (`context.py`) must run inside the Job or on the live-loop pod, never on the static server: the server's `/data` is a read-only bucket mount and `context.py` writes its artifact.

**rpc-log** — the live pod's 512 Mi limit makes a wide `exec` repair an OOM that restarts `continuous`. Use the fresh-pod form. `CHAIN` must name one chain; `repair` with `CHAIN=all` aborts. The pod's range and concurrency env can be omitted — the app defaults are identical to the deployment's.

## What was rejected, and why

**Running dbt in the idle static-server pod.** Its `/data` is a read-only bucket mount and `/app/target` symlinks into it, so dbt cannot write artifacts at all.

**Running from a laptop against the warehouse.** The private-endpoint hostname resolves inside the VPC only. The public hostname exists but would send every write over the internet, which is the cost the private endpoint exists to avoid, and nothing would alert on it.

**A Terraform-gated Job** (the rpc-state pattern) for one-off repairs. Roughly six variables and a `kubernetes_job_v1` per operation — worth it for a repeated multi-hour backfill, strictly more machinery than a clone for a one-off.

!!! info "Internal runbook"
    [runbooks/60-gke-one-shot-jobs.md](https://github.com/gnosisdevops/infrastructure-gnosis-analytics/blob/main/runbooks/60-gke-one-shot-jobs.md) — private repository; carries the copy-pasteable render-and-apply recipe for each app, the fresh-pod spec, and the stop sequence.
