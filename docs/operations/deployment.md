---
title: Deployment
description: How changes reach the GKE Autopilot cluster — the release chain, the apply ritual, and pause/resume/scale
---

# Deployment

There is **no CI deploy and no GitOps reconcile loop.** Every change reaches the cluster through a Terraform apply run by a person, and a live edit made directly on the cluster persists until someone applies over it — then vanishes without warning.

## The platform

| | |
|---|---|
| Cluster | GKE **Autopilot**, one region, private nodes, IAM-only control plane |
| Workloads | 17 Deployments and ~19 CronJobs, one Terraform root stack per service |
| Warehouse | ClickHouse Cloud, reached over a **Private Service Connect** endpoint — never the public hostname |
| Secrets | Google Secret Manager → External Secrets Operator (3-minute sync) → Kubernetes Secrets |
| Images | `ghcr.io/gnosischain/<name>`, multi-arch, built on push to `main` |
| Ingress | One shared external Gateway for the public API and these docs; the MCP server is on an internal gateway behind the VPN |

Two Autopilot constraints shape everything operational: **ephemeral storage is capped at 10 Gi per pod**, and node-level metrics (`node_*`, `container_*`) are not scrapeable — see [Monitoring](monitoring.md).

## The release chain

1. Merge to `main` in the app repository → GitHub Actions builds a multi-arch image.
2. It lands in GHCR as `:latest` and `:<short-sha>`.
3. An operator pins `tag@digest` in that stack's `locals.tf`.
4. Plan → classify → apply.

!!! warning "Pin the multi-arch index digest, never a per-arch child"
    Five workloads have hit this: an arm64 child pulls fine on Autopilot and then dies `exec format error` in CrashLoopBackOff, with nothing in the message about architecture. Resolve the index digest with `docker buildx imagetools inspect <image>:<tag>`.

`locals.tf` is authoritative for image pins. Several stack READMEs quote older digests; treat them as narrative. The `locals.tf` comment blocks are, in practice, the real changelog — they record why each pin was chosen.

## The apply ritual — never skip it

1. **Plan into a file.** A saved plan is the only way what you reviewed is what runs.
2. **Classify it** by piping the plan's JSON through `ops/verdict.py --live`. Always `--live`: without it a routine re-run and real lost work look identical.
3. **Run every CHECK it prints**, and read the output.
4. **Apply that plan file** — never a fresh apply, never auto-approve.

`verdict.py` holds no facts about any stack, so it stays correct for stacks written long after it. Verdicts, most severe first:

| Verdict | Meaning | Do |
|---|---|---|
| `DATA_AT_RISK` | a volume is destroyed or replaced | **Stop.** Most volumes have no backups. |
| `JOB_WILL_DIE` | a Job is destroyed and `--live` confirmed it is running | **Stop.** That work is lost; re-applying does not resume it. |
| `WORKLOAD_WILL_VANISH` | a Deployment or CronJob is destroyed | Stop unless that is the intent. |
| `JOB_WILL_RUN` | a Job is created and will execute | Confirm running it now is intended and idempotent. |
| `WORKLOAD_WILL_START` | a workload absent from the cluster is created | **Ask why it is absent** — it may be paused deliberately. |
| `JOB_WILL_RERUN` | a Job is replaced but its prior run finished | Usually fine. |
| `WORKLOAD_WILL_RESTART` | pods roll | Routine. |
| `MUTUAL EXCLUSION` | the plan starts a workload **and** destroys a Job | **Stop.** Single-writer collision. |

Exit 0 = nothing destroys running work. Exit 2 = something does. Nothing blocks a command; the verdict is advice to a human. Delete the plan file afterwards — a stale plan applied later is a plan nobody reviewed.

Two plan-time gotchas: Kubernetes-manifest resources server-side dry-run, so a plan needs cluster connectivity and the CRDs already installed; and **never init with `-upgrade`** — it rewrites the tracked provider lockfile.

## Redeploying a service

A redeploy is an image pin change on one stack, applied with the ritual above, plus a **baseline before** and a **proof after** that nothing was lost. It is done one service at a time: two services may sit in their verification windows together, but only one apply runs at a time.

1. **Check the window.** Every service has slots to avoid (table below) and an idle-gap rule: apply between two units of work, never in the middle of one.
2. **Baseline, read-only, within 10 minutes of the apply.** Record the workload's generation and image, the writer's frontier or checkpoint, a fixed window of already-final rows, and the app's own coverage or backlog query. For a crawler, record the visit counts of the sweeps that are open, not only the sealed ones.
3. **Validate and apply the saved plan file.** Expected: an in-place update of the image on the workloads that share the pin, nothing added, nothing destroyed, verdict `WORKLOAD_WILL_RESTART` (a CronJob-only stack carries the same label even though nothing restarts).
4. **Verify immediately.** One pod per workload on the new digest with 0 restarts (the state daemons are the exception: 3-5 lease-refusal exits before Ready are normal, more or a different exit reason is not), the resume line at the baseline frontier, the first unit of work completed.
5. **Verify the data** after 10 to 30 minutes: frontier past the baseline, the coverage query clean across the restart window, the fixed window unchanged, no duplicates, no new dead letters or orphaned ranges.
6. **Nothing-lost checklist**, then commit the one pinned file. The next [morning check](troubleshooting.md) is the final confirmation for anything rolled the day before.

Rollback always has the same shape: restore the previous image line, plan to a file, classify, apply that file, then repeat steps 4 and 5 on the old image. Only an image or runtime fault justifies it; a rollback is a second restart with the same timing rules.

| Service | What restarts | Avoid | Decisive proof |
|---|---|---|---|
| cryo indexer (Gnosis and Celo) | the continuous writers; auto-maintain picks the image up at its next slot | the two hours before an auto-maintain slot, and the slot itself | grid coverage over the restart window whole, no orphan range |
| beacon indexer | realtime and transform | 02:00-06:15 UTC; apply in the idle gap between chunks (about 8.5 minutes apart) | no chunk hole across the restart, transform caught up |
| rpc-state indexer (both chains) | the census daemon; the CronJobs at their next slot | 00:00-03:30 UTC; the archive endpoint healthy for an hour, proven from inside the cluster | one active lease, the last three days' publications identical, yesterday published before 06:00 |
| rpc-log indexer | the scanner | none, but never while a repair pod exists | both checkpoints continue from checkpoint+1, no range gap |
| cow indexer | the scanner; the sweep CronJob at its next slot | 00:15-00:45 and 02:45-05:00 UTC, and during an API 403 storm | every live chain's checkpoint advances, no unexplained empty log bucket, no new dead letters |
| envio-ga indexer | realtime; reconcile at its 03:00 slot | 02:50-03:15 and 05:30-06:30 UTC | watermarks continue past the baseline, no duplicate raw versions |
| nebula | both crawlers | 01:50-02:10 UTC; apply right after both crawlers have restarted at their own sweep boundaries | interrupted crawls sealed `cancelled`, the first new sweeps sealed `succeeded` inside the normal size band |
| ip-crawler and click-runner | nothing; only the CronJob templates change | 01:55-02:10 UTC for ip-crawler, 03:00-05:10 UTC for click-runner, never while a Job is active | the first run on the new image succeeds at its next slot |

What a full pass over every service taught:

- Verification queries share the warehouse memory cap with the writers. Run them one statement at a time and bounded; one "memory limit exceeded" retry inside a writer during verification is noise, a repeating one means stop querying.
- A graceful stop seals an interrupted nebula crawl as `cancelled`; only an out-of-memory or watchdog kill leaves it `started`. Judge sweeps by visits counted per crawl id, not by the crawl's own peer counter.
- The CoW chain-1 "leak band" (fills without an order row) grows between the six-hourly sweeps by design; read it by fill age and re-check after the next sweep instead of expecting it flat.
- Envio's state table keeps only merged rows, so the pre-roll watermark comes from the raw entity table.
- An empty log bucket after a cow restart is checked against the execution indexer's independent copy of the same blocks before it is called a hole.

!!! info "Internal runbook"
    The deployments repository's `runbooks/80-redeploy-a-service.md` holds the full procedure per service: the exact commands, baseline and verification queries, timing rules, rollback and the abort-versus-noise lists.

## Pause, resume, scale

The on/off levers are per-stack `locals.tf` values — `replicas`, `cron_suspended`, and for a few stacks a single `cutover_complete` line that drives both. There is no root kill switch.

!!! warning "Three workloads are correctness-bound to one replica"
    The MCP server (module-level session singleton, no session affinity), the dbt live loop (`Recreate`, and two pods would run the same incremental models against the same tables), and the envio realtime loop (no lease: a second instance permanently duplicates `raw_entities` versions and doubles the upstream load). Never scale them, including "temporarily".

Every indexer uses `strategy = Recreate`, not `RollingUpdate`. The target tables are SharedMergeTree and **do not dedupe re-inserted rows**, so a two-pod overlap duplicates data rather than resolving it. For rpc-state a rolling update also deadlocks: the new pod cannot take the writer lease while the old one holds it.

A temporary pause set directly on the CronJob object works but is **`[drift]`** — the next apply silently resumes it. If a pause must outlive the next apply, change `locals.tf`.

## Restart without changing config

A `rollout restart` is safe and Terraform-invisible: it changes only an annotation. Use it after a secret rotation; an apply is not needed for that. Then confirm the workload is back at its desired replica count and, for anything that writes, that its checkpoint is advancing again.

!!! info "Internal runbook"
    The deployments repository (private) holds the stacks, `ops/verdict.py`, and the per-scenario runbooks with cluster-specific commands.
