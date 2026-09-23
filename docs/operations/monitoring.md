---
title: Monitoring & Detection
description: What the observability signals are, what is absent by design, which workloads have no alert coverage, and how to know your detection is working
---

# Monitoring and detection

Run this page's checks before concluding "nothing alerted, so nothing is wrong". Several of the signals the runbooks rely on can be silently absent.

## The stack

| Layer | How |
|---|---|
| Metrics | A Prometheus **agent** in the cluster remote-writes to a shared Thanos. It evaluates no rules and serves no queries. |
| Logs | Grafana Alloy reads pod logs through the Kubernetes API and ships to Loki. (Not Promtail — Autopilot refuses the host-path mount it needs.) |
| Alerts | **Grafana-managed**, provisioned as code, evaluated against Thanos, Loki and ClickHouse, routed per rule to Slack. There is no Alertmanager. |
| Dashboards | Twelve Grafana dashboards, one per service. Not Terraform-managed, so drift against live Grafana is invisible — but they are the best source of working LogQL and SLA thresholds. |

## Absent by design

Autopilot blocks node-exporter and the kubelet scrape, so **`node_*`, `container_*` and `kubelet_*` are absent from Thanos.** Those families are collected by GKE's managed pipeline into Cloud Monitoring instead. A dashboard panel using them is blank, not broken. No alert rule depends on any of them.

## Log-based detection

Every log-based check — the per-query `dune-query-failed` rule, envio's `Realtime tick error` grep, dbt's stdout-only `TRANSIENT=` / `PERMANENT=` lines — depends on Alloy shipping to Loki. Prove it end to end in Grafana Explore, against Loki:

```logql
{namespace="analytics", pod=~"⟨dbt cron pod prefix⟩.*"}
```

If that returns no streams, **every Loki-based alert is blind** and so is half of [dbt daily run failed](runbooks/dbt-daily-run-failed.md). Fall back to pod logs directly — but only while the pod exists (three job records per CronJob outcome).

## Workloads with no coverage at all

| Workload | Coverage |
|---|---|
| nebula (both crawlers) | **none** |
| ip-crawler | **none**, and no cron-miss rule |
| rpc-log-indexer | **none** |
| the rpc-state **ethereum** daemon | every rule selects the Gnosis deployment name, so the mainnet daemon matches nothing |
| onchain-alerter | 11 rules, all paused, for a workload that is not deployed |

No `cron-miss-*` rule exists for the HOPR crons, the governance ingestors, DefiLlama, CoinGecko, ip-crawler, or the CoW 6-hourly sweep. The `*-stale` ClickHouse rules partly compensate, but at 30–60 h instead of 26 h.

For these, **the data query is the detection.** That is what the [morning check](troubleshooting.md) is for.

## Green but wrong — the four recognisers

**Checkpoint age, not data age, for sparse indexers.** `rpc_log_indexer.decoded_events_canonical` can read weeks stale while the service is perfectly healthy: it watches one Snapshot DelegateRegistry space, which emits a handful of events a month. Judge it by the checkpoint.

**Per chain, not summed.** `cow_db` runs 11 chains in one pod. A single dead chain leaves the pod green and the summed row-rate healthy. Only the per-chain checkpoint query shows it.

**A uniform ~80 s `cryo-*-auto-maintain` runtime means "nothing in window", not "healthy".**

**Thousands of nebula restarts are by design** — a max-uptime liveness watchdog, and the only thing that catches a hung crawl.

## Three structural blind spots

- **Nothing alerts on "has a `blocks` row but no `transactions` row."** Only the per-dataset coverage query on the [cryo page](../data-pipeline/ingestion/cryo-indexer.md) finds it.
- **Chain-lag metrics cannot fire during an RPC outage.** They need the indexer to fetch the chain head, so they go *stale* rather than growing. Absence of a lag alert is not evidence of health.
- **Three dbt alert rules query `elementary.model_run_results`.** Elementary is switched off and writes nothing, so those rules ship paused and cannot be unpaused as written.

## The alerting stack's own rules

Rules are provisioned read-only in the UI (`provenance: api`). Change them in YAML and apply.

!!! warning "Never add a `grafana_notification_policy` resource"
    It replaces the *entire* org routing tree on a shared Grafana and would hijack every other team's alerting. Route per-rule via `notification_settings`.

!!! warning "Never use `pause_all` to silence one rule"
    Flipping it back un-mutes everything else too. Pause the single rule with `paused: true` and apply.

**`kind: state` vs `kind: event` changes what "Resolved" means.** A `state` rule measures a current condition, so resolved means it cleared. An `event` rule counts failures in a rolling window, so resolved only means the window aged out. Pair event rules with a state rule (`dune-query-failed` is the fast notice; `crawlers-data-stale` is the ground truth).

And the governing lesson from the alerting work: **an alert that exists only in git is a diagram.** It is not done until it is applied and has been seen to evaluate.

## Health endpoints

| Service | Endpoint | Note |
|---|---|---|
| cerebro-api | `/health` | asserts ClickHouse connectivity — every replica goes unready in a warehouse outage, deliberately |
| cerebro-mcp | `/health`, `/livez` | liveness is `/livez`; `/health` 503s during warehouse blips |
| indexers | `/health`, `/ready`, `/metrics` on 9090 | rpc-state `/ready` 503 = startup incomplete or its own heartbeat loop died, **not** "another writer holds the lock" |
| dbt static server | `/health`, `/metrics`, `/logs/`, `/reports/` | the route to last night's artifacts |

!!! info "Internal runbook"
    [runbooks/70-is-my-detection-dead.md](https://github.com/gnosisdevops/infrastructure-gnosis-analytics/blob/main/runbooks/70-is-my-detection-dead.md) — private repository; carries the cluster-specific commands for this page.
