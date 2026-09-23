---
title: Warehouse Out of Memory
description: Recognising and recovering from a ClickHouse Code 241 storm that hits unrelated jobs at once
---

# Warehouse out of memory (Code 241)

**Recognise it:** `Code: 241 … (total) memory limit exceeded … maximum: ⟨N⟩ GiB … OvercommitTracker decision` hitting **unrelated** jobs in one window — indexers, the dbt cron and the CoW sweep all failing within the same half hour.

That is a server-wide condition. Your query was the victim, not the cause.

**Not the same thing:** `Query memory limit exceeded … maximum: 4.00 GiB`. That is a per-query limit and it *is* your query. Scope it — bound the window, drop `FINAL`, read the checkpoint table instead of aggregating a fat view.

!!! warning "The cap is a total, not per-query"
    The warehouse idles near its memory ceiling. One unscoped analytical query starves every other job on the platform. Scope every query to one database and a bounded window; never combine `FINAL` with `GROUP BY argMax`; push predicates into each `UNION` branch as constants.

## 1. Read the ceiling out of the error

The `maximum:` figure in any 241 tells you the service tier the warehouse is currently running at. Compare it to what the tier is *supposed* to be. A service that has silently scaled back down to a smaller tier produces exactly this storm, and the fix is the autoscaling floor, not the queries.

From inside the cluster (the MCP tool refuses `system.*` queries), on both replicas:

```sql
SELECT hostName(), metric, round(value / pow(2, 30), 2) AS gib
FROM clusterAllReplicas(default, system.asynchronous_metrics)
WHERE metric IN ('CGroupMemoryTotal', 'jemalloc.resident', 'jemalloc.allocated')
ORDER BY 1, 2;
```

**Check `CGroupMemoryTotal` on both replicas before launching any backfill.**

Raising the autoscaling **minimum** is a ClickHouse Cloud console action. Relying on the maximum alone has proven insufficient: a service set only at the top of its range scaled back overnight and the storm returned the next morning.

## 2. Emergency relief

```sql
SYSTEM JEMALLOC PURGE;    -- per replica
```

Measured effect: tracked memory dropped roughly 11 → 7.5 GB, then eroded again within ~2.5 h under cron load. It buys a window; it does not fix anything.

!!! warning "\"Wait for a quiet window\" stopped working"
    When this is chronic, the windows are rare and short — a tiny model once failed 13 times in 3 hours. Do not plan on one.

## 3. Find the structural cause

The measured driver is **allocator residency plus active-part metadata**, not fat queries. A baseline that idles near the cap with tens of thousands of active parts leaves nothing for real work.

```sql
SELECT table, count() AS parts FROM system.parts WHERE active
GROUP BY table ORDER BY parts DESC LIMIT 20;
```

Reducing part counts — batching per-target inserts, off-hours `OPTIMIZE` — is the durable fix. Without it, residency creeps back silently.

## 4. Restart the victims, in order

1. **Indexers self-heal.** cryo, rpc-log, cow and envio all resume from durable checkpoints. Nothing to do unless a pod is crash-looping.
2. **rpc-state** may have failed a backfill Job. Check coverage before re-running — an already-complete range exits non-zero ([RPC State Indexer](../../data-pipeline/ingestion/rpc-state-indexer.md)).
3. **The CoW sweep** self-heals at its next 6-hourly slot. Act only if two consecutive slots fail.
4. **dbt** needs a deliberate rerun → [dbt daily run failed](dbt-daily-run-failed.md). Do this **last**: it is the heaviest consumer, and restarting it into an unresolved memory condition just reproduces the failure.

## What not to do

- Do not add per-model memory knobs. The limit is server-wide and the compiled SQL carries no settings.
- Do not throttle one indexer and call it fixed — the baseline is resident even with a given job idle.
- Do not diagnose a `(total)` 241 with `allocate chunk 0.00 B` as a model-size problem. That shape means the server was saturated and your query was selected to stop.

!!! info "Internal runbook"
    [runbooks/10-warehouse-oom.md](https://github.com/gnosisdevops/infrastructure-gnosis-analytics/blob/main/runbooks/10-warehouse-oom.md) — private repository; carries the cluster-specific commands for this page.
