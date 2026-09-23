---
title: Secret Rotation
description: Rotating one credential, and the all-consumers order for rotating the ClickHouse password
---

# Rotating a secret

Secrets live in Google Secret Manager and reach pods through the External Secrets Operator on a 3-minute sync. Rotation is three steps, and skipping any one of them has caused an incident.

## One secret

1. **Write a new version of the whole JSON blob.** Author it with `jq` and pass it by file — inline quoting is the usual cause of "invalid character" errors from the operator.
2. **Force the ExternalSecret to sync** and confirm it reports `SecretSynced=True`.
3. **Restart the consuming workload.** The process read its environment at startup; syncing the Kubernetes Secret is not enough.

!!! warning "The value is one JSON blob, replaced wholesale"
    Read the existing keys and rewrite all of them. Dropping one puts the consuming pods into `CreateContainerConfigError`. This has happened.

!!! warning "The secret-name prefix is load-bearing"
    Access is granted by an IAM condition on the namespace prefix, so a misnamed secret is invisible to the namespace and fails at *sync* time as `SecretSyncedError`, not in review.

The operator role can write a new version without being able to read the current one. Rebuild the payload from the live Kubernetes Secret if you need the other keys.

RPC endpoints live in a separate `⟨service⟩-rpc` secret deliberately, so they rotate without touching database credentials.

## Rotating the ClickHouse password — all consumers

This is not one secret. Miss a consumer and it fails silently, often days later.

| Tier | Consumer | What breaks if missed |
|---|---|---|
| 1 | The ~11 in-cluster secrets that carry warehouse credentials — every indexer, click-runner, dbt, cerebro-api, cerebro-mcp | The workload crash-loops or serves 503 |
| 2 | **metrics-dashboard's Vercel environment** — it connects to ClickHouse directly, with credentials held as Vercel project variables, not in Secret Manager | Every dashboard card goes to its empty state; nothing in the cluster tells you |
| 3 | **Grafana's ClickHouse datasource** — every `*-stale` alert rule queries through it | All those rules go to NoData, which reads as "no alerts firing" |
| 4 | **dbt-cerebro's CI secret** `CLICKHOUSE_URL` | The docs-publish job fails; it has broken this way before |

Rotate in that order, and **verify each tier** before moving on: workloads running and synced; one dashboard card loading; one alert rule evaluating to OK rather than NoData; the CI docs job green.

!!! info "Internal runbook"
    [runbooks/50-secret-rotation.md](https://github.com/gnosisdevops/infrastructure-gnosis-analytics/blob/main/runbooks/50-secret-rotation.md) — private repository; carries the secret names and the exact commands.
