---
title: Consumers Showing Stale Data
description: Tracing a stale or wrong number on the API, MCP server, dashboard or docs back to its cause, in the right order
---

# A consumer shows stale or wrong data

Trace it back in this order. Do not start at the consumer.

1. **Is the warehouse right?** Query the mart directly. If it is wrong there, this is not a serving problem → [dbt reprocess](dbt-reprocess.md).
2. **Is it a cache?** Only the dashboard caches. See below.
3. **Is it the contract between dbt and the consumer?** A renamed or retired model breaks three surfaces dbt does not know about: the semantic layer, cerebro-api's dynamic routes, and the dashboard's own SQL.

## cerebro-api

```bash
curl -s https://api.analytics.gnosis.io/health          # {"status":"ok","clickhouse_connected":true}
curl -s https://api.analytics.gnosis.io/v1/⟨route⟩
```

Routes are **generated from the dbt manifest**, refreshed every 300 s. A model tagged `production` + `api:⟨resource⟩` becomes an endpoint with no code change; a renamed model removes one the same way.

Force a manifest reload without a restart (needs a tier-3 key):

```bash
curl -X POST https://api.analytics.gnosis.io/v1/system/manifest/refresh -H 'X-API-Key: ⟨key⟩'
```

API keys are read at **startup**, so a key change needs a workload restart. ClickHouse credential changes do not.

`/health` asserts `clickhouse_connected`, so every replica goes unready during a warehouse outage. That is deliberate.

If it looks down from your laptop, check DNS first — the VPN client overrides this hostname to `0.0.0.0` while connected. `dig @8.8.8.8 api.analytics.gnosis.io` before declaring an outage.

## cerebro-mcp

The server exposes `/health` (probes ClickHouse; 503 when unreachable) and `/livez` (process only).

!!! warning "Liveness is `/livez`, never `/health`"
    `/health` 503s during every warehouse blip. Wiring liveness to it would restart the server during every one.

One replica, always. Session state is a module-level singleton and the internal gateway has no session affinity; two replicas corrupt multi-step analysis.

**Adding a database to the allowlist** — the most common request. `ALLOWED_DATABASES` **replaces** the default list entirely:

- Never set it to only the new database.
- Never drop `dbt` — `/health` validates it, so every replica would go unready.
- `scratch` is not on the list; the RPC-scan auto-append that would add it is disabled.

The edit is a configuration change followed by a restart. Expect a short MCP outage.

## metrics-dashboard

Deployed on Vercel, outside the cluster.

**Cache first** — results cache for 24 h by default:

```bash
curl -s 'https://metrics.gnosischain.com/api/test' -H 'X-API-Key: ⟨key⟩'      # cache status
curl -s 'https://metrics.gnosischain.com/api/metrics?metricId=⟨id⟩&refreshCache=true'
```

!!! warning "Never `refreshCache=true` without a `metricId`"
    That is a ~600-query fan-out inside a 60-second function.

A card showing a calm em-dash with no error and no retry button is the **designed** empty state for `UNKNOWN_TABLE`. It means the model the card reads was renamed or retired, not that the dashboard broke.

**If the metric itself is wrong,** the likely cause is export drift: each metric's SQL exists twice, and `api/queries/⟨id⟩.json` is what runs. `pnpm run export-queries` is a manual step, not part of the build.

!!! warning "`export-queries` is a write with no dry-run"
    It rewrites `api/queries/*.json` and unlinks orphans. Do not run it as a diagnostic. And never hand-edit `api/queries/*.json` to make production behave — the next export reverts you and the repo's source of truth stays wrong.

Redeploy is `git push origin main`. Not `vercel --prod` from a working tree — that ships uncommitted local state to production with no CI gate.

Do not answer "who reads this model?" from metric ids or filenames; several ids do not name the table they read. Grep the query strings.

## cerebro-docs

```bash
curl -sI https://docs.analytics.gnosis.io/
curl -sI https://docs.analytics.gnosis.io/llms.txt
curl -sI https://docs.analytics.gnosis.io/llms-ctx.txt
curl -sI https://docs.analytics.gnosis.io/search/search_index.json
```

cerebro-mcp loads three of these over the public hostname at startup, so a docs deploy that drops one breaks **the MCP server's docs tools**, not anything visible on the site. Check all four after every docs deploy.

!!! info "Internal runbook"
    [runbooks/40-consumers-stale.md](https://github.com/gnosisdevops/infrastructure-gnosis-analytics/blob/main/runbooks/40-consumers-stale.md) — private repository; carries the cluster-specific commands for this page.
