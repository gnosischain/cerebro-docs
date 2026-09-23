---
title: Operations
description: Triage order, the rules that apply to every procedure, and the index of runbooks for the Gnosis Analytics platform
---

# Operations

This section is written for the person on call. It answers four questions in order: is everything running, is the data fresh, did the nightly transformation succeed, and — when something is wrong — what to type.

The platform runs on **GKE Autopilot** with all workloads deployed by Terraform, data in **ClickHouse Cloud** reached over a private endpoint, and images built by **GitHub Actions** into GHCR. The procedures here are complete; the cluster-specific commands (resource names, secret names, the copy-pasteable job recipes) live in a private companion repository that every page links to.

## Triage order

**Raw freshness → coverage → dbt → consumer.** Starting at the model is the most common way to lose an afternoon: a stale dashboard card is usually a stale raw table four steps upstream.

Start at [Morning Check & Triage](troubleshooting.md). It routes you to the right page.

## The five rules

**1. Plan → classify → apply the plan file.** Every deployment change is Terraform. A bare `apply` in a scraper stack can destroy a running backfill Job or re-execute production ingestion. See [Deployment](deployment.md).

**2. One writer per database or chain.** Enforced differently per app, so check the right thing:

| App | Enforcement | What a violation looks like |
|---|---|---|
| cryo | Convention only. `maintain` selects **every** non-completed range (`processing` included), DELETEs it and re-extracts with **no claim** — stop the writer first. Only `auto-maintain` claims | Silent duplication or deleted rows |
| rpc-state | A writer lease with a 120 s stale window and **no override flag** | The new pod exits 1 and crash-loops until the lease goes stale |
| rpc-log, cow | The checkpoint itself | Checkpoint regression, not row duplication |
| beacon, envio, dbt live loop | `Recreate` strategy + single replica | Duplicate rows (the targets do not dedupe) |

**3. The warehouse memory cap is a total, not per-query.** One unscoped query starves every other job. Scope every query to one database and a bounded window. See [Warehouse out of memory](runbooks/warehouse-oom.md).

**4. A hand-created Job is invisible to `concurrencyPolicy: Forbid`.** Before creating one, check nothing is already running. See [One-shot jobs](runbooks/one-shot-jobs.md).

**5. A green job is not fresh data.** Several ingesters exit 0 on partial failure. The only real "did data arrive" signal is a freshness query against the warehouse.

## `FINAL`, per database

Four repos give four different answers and all four are right. Generalising any one of them is wrong about the other three.

| Database | Rule |
|---|---|
| `consensus` (`load_state_chunks`, `transformer_progress`) | **`FINAL` required** — they keep every status transition |
| `rpc_state_indexer` (`writer_heartbeats`, `discovery_ranges`) | **`FINAL` required**, and scope by recency — old `failed` rows survive forever |
| `envio_ga` | **Never `FINAL`** — it OOMs the instance. Use `argMax(col, insert_version) … GROUP BY id HAVING argMax(_deleted, insert_version) = 0` |
| `execution*` (`indexing_state`) | **`FINAL` does not collapse across months** — the table is partitioned by `toYYYYMM(created_at)`, so a range that failed in one month and completed in the next keeps both rows. Resolve a range with `argMax(status, (created_at, insert_version)) … GROUP BY dataset, start_block, end_block`; never `FINAL` + `GROUP BY argMax` |
| `cow_db` | Never a bare `FINAL` over a data table. Read the `*_canonical` views, scoped |
| `dbt` marts | Read as published. Marts read ReplacingMergeTree **without** `FINAL`, which is why a duplicate row counts twice |

## Index

| When | Page |
|---|---|
| Daily, and whenever something looks wrong | [Morning Check & Triage](troubleshooting.md) |
| How changes reach the cluster; pause, resume, scale | [Deployment](deployment.md) |
| What the signals are, what is absent by design, which workloads have no alerts | [Monitoring & Detection](monitoring.md) |
| `Code: 241` across unrelated jobs | [Warehouse out of memory](runbooks/warehouse-oom.md) |
| The 06:00 dbt run failed or stalled | [dbt daily run failed](runbooks/dbt-daily-run-failed.md) |
| An indexer was repaired; fix dbt without a full refresh | [dbt reprocess](runbooks/dbt-reprocess.md) |
| The Dune prices source skipped a day | [Recovering from a prices gap](prices-gap-recovery.md) |
| API, MCP, dashboard or docs showing stale data | [Consumers showing stale data](runbooks/consumers-stale.md) |
| How to run any repair command on Autopilot | [One-shot jobs](runbooks/one-shot-jobs.md) |
| Rotating a credential | [Secret rotation](runbooks/secret-rotation.md) |

Each ingestor's own page carries its **Operating and recovering** section — stopped, gap, corrupt range, restart: [cryo-indexer](../data-pipeline/ingestion/cryo-indexer.md), [beacon-indexer](../data-pipeline/ingestion/beacon-indexer.md), [rpc-state-indexer](../data-pipeline/ingestion/rpc-state-indexer.md), [rpc-log-indexer](../data-pipeline/ingestion/rpc-log-indexer.md), [cow-indexer](../data-pipeline/ingestion/cow-indexer.md), [envio-ga-indexer](../data-pipeline/ingestion/envio-ga-indexer.md), [click-runner](../data-pipeline/ingestion/click-runner.md), [nebula](../data-pipeline/crawlers/nebula.md), [ip-crawler](../data-pipeline/crawlers/ip-crawler.md).

## Conventions

- `⟨FILL⟩` marks a value you must supply.
- **`[drift]`** marks a live change made directly on the cluster that Terraform does not know about. It survives until the next apply, then vanishes silently. If a change must outlive an apply, change the stack instead.
- Every procedure page ends with a link to its internal runbook, which holds the identifiers and copy-pasteable recipes.

## Key contacts

| Area | Team |
|------|------|
| API and dbt models | Gnosis Analytics engineering |
| Infrastructure and Kubernetes | Gnosis DevOps |
| ClickHouse Cloud | Managed by ClickHouse (external) |
