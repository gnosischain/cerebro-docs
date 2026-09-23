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
