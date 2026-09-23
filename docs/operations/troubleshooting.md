---
title: Morning Check & Triage
description: The five-minute daily check, the freshness baselines that decide whether last night's data is trustworthy, and where each symptom routes
---

# Morning check and triage

Five minutes. Run it daily, and run it first whenever something looks wrong.

## 1. Is everything running?

Three reads against the cluster: every CronJob's `SUSPEND` flag and last schedule time; every Deployment's ready vs desired replicas; any pod not `Running` or `Succeeded`.

Expected: 17 Deployments at desired replicas. Every CronJob with a last schedule inside its interval. Exactly two suspended by design — `dune-execute-only-daily-ingestor` and `probelab-ingestor-latest`. Any other `SUSPEND=true` is drift or an unfinished pause: check it against the stack before assuming it is intentional.

A pod in `Error` is a finished Job that failed — the name tells you which page.

## 2. Is the data fresh?

One query per source. **The healthy value is not zero for most of them, and the reason matters** — an operator who does not know why `execution.blocks` is an hour behind will chase it.

| Source | Signal | Healthy | Why that number |
|---|---|---|---|
| `execution.blocks` | `max(block_timestamp)` | ~66 min | `CONFIRMATION_BLOCKS=720` at 5 s/block |
| `execution_live.blocks` | `max(block_timestamp)` | ~1 min | `CONFIRMATION_BLOCKS=6` |
| `consensus.blocks` | `max(slot_timestamp)` | ~67 min | `REALTIME_SLOT_DELAY=700` slots |
| `rpc_log_indexer` | **checkpoint** age, per chain | < 1 h | data age is meaningless here — the contract is sparse |
| `cow_db` | **checkpoint** age, **per chain** | ≤ ~6 min | a summed check hides one dead chain |
| `rpc_state_indexer` | `max(snapshot_date)` per job | yesterday | published overnight, 00:19–03:11 |
| `crawlers_data` | per-table SLA ratio | < 1 | Dune lands T-2, the rest T-1 |

```sql
-- chain data
SELECT 'execution' AS src, dateDiff('minute', max(block_timestamp), now()) AS lag_min FROM execution.blocks
UNION ALL SELECT 'execution_live', dateDiff('minute', max(block_timestamp), now()) FROM execution_live.blocks
UNION ALL SELECT 'consensus', dateDiff('minute', max(slot_timestamp), now()) FROM consensus.blocks;

-- rpc-log and cow: checkpoint age, per chain
SELECT chain_id, dateDiff('minute', max(updated_at), now()) AS lag_min
FROM rpc_log_indexer.indexing_checkpoints WHERE source = 'rpc' GROUP BY chain_id ORDER BY chain_id;

SELECT chain_id, dateDiff('minute', max(updated_at), now()) AS lag_min
FROM cow_db.indexing_checkpoints WHERE source = 'rpc' GROUP BY chain_id ORDER BY lag_min DESC;

-- rpc-state: every job should carry yesterday
SELECT chain_id, job_name, max(snapshot_date) AS latest_day
FROM rpc_state_indexer.census_publications
WHERE published_at >= now() - INTERVAL 3 DAY
GROUP BY chain_id, job_name ORDER BY chain_id, job_name;

-- click-runner outputs, as a ratio against each table's SLA
SELECT tbl, dateDiff('hour', latest_data, now()) / threshold_h AS staleness_ratio
FROM (
  SELECT 'dune_labels' AS tbl, toDateTime(max(introduced_at)) AS latest_data, 60 AS threshold_h FROM crawlers_data.dune_labels
  UNION ALL SELECT 'dune_prices', toDateTime(max(block_date)), 60 FROM crawlers_data.dune_prices
  UNION ALL SELECT 'dune_bridge_flows', toDateTime(max(timestamp)), 60 FROM crawlers_data.dune_bridge_flows
  UNION ALL SELECT 'coingecko_prices', toDateTime(max(ingested_at)), 30 FROM crawlers_data.coingecko_prices
  UNION ALL SELECT 'defillama_prices', toDateTime(max(ingested_at)), 30 FROM crawlers_data.defillama_prices
  UNION ALL SELECT 'circles_blacklisted', toDateTime(max(ingested_at)), 30 FROM crawlers_data.circles_blacklisted
  UNION ALL SELECT 'cow_api_trade_fees', toDateTime(max(ingested_at)), 30 FROM crawlers_data.cow_api_trade_fees
);
```

`envio_ga` and `celo_execution` are readable through the Cerebro MCP since 2026-09-23; the same checks are `maintain check` ([envio](../data-pipeline/ingestion/envio-ga-indexer.md)) and the cryo coverage query ([cryo](../data-pipeline/ingestion/cryo-indexer.md)) when the MCP is unavailable.

## 3. Did the 06:00 dbt run succeed?

List the dbt jobs by start time; grep the newest one's log for `MANDATORY STEP FAILED`, `] Failed:`, `Code: 241`, `REFUSED`. Only three job records are kept per outcome, so a pod older than ~3 runs is gone.

If the run failed → [dbt daily run failed](runbooks/dbt-daily-run-failed.md). If the failures are `Code: 241` across several unrelated steps → [Warehouse out of memory](runbooks/warehouse-oom.md) first.

## 4. Did yesterday land before 06:00?

The most frequent daily decision, and the one that decides whether last night's dbt output is trustworthy. The dbt cron rebuilds from whatever the raw layer held at 06:00; **it does not wait**.

- Every `rpc_state_indexer` job shows `snapshot_date = yesterday` (query above)?
- `execution` / `consensus` past midnight UTC?
- `crawlers_data` within SLA — remembering Dune is legitimately T-2?

**If the rpc-state daemon missed a day**, that day needs a one-day all-jobs recovery Job (~25 min, and it also runs curated balances) → [rpc-state-indexer](../data-pipeline/ingestion/rpc-state-indexer.md).

**If dbt already ran against a stale source**, do not rebuild everything. Get the scoped re-run list from [dbt reprocess](runbooks/dbt-reprocess.md).

## Green but wrong — the four recognisers

**Checkpoint age, not data age, for sparse indexers.** `rpc_log_indexer.decoded_events_canonical` can read weeks stale while the service is perfectly healthy: it watches one Snapshot DelegateRegistry space, which emits a handful of events a month. Judge it by the checkpoint.

**Per chain, not summed.** `cow_db` runs 11 chains in one pod. A single dead chain leaves the pod green and the summed row-rate healthy.

**A uniform ~80 s `cryo-*-auto-maintain` runtime means "nothing in window", not "healthy".**

**Thousands of nebula restarts are by design** — a max-uptime liveness watchdog, and the only thing that catches a hung crawl.

## Where to go

| Symptom | Page |
|---|---|
| `Code: 241` in several unrelated places | [Warehouse out of memory](runbooks/warehouse-oom.md) |
| One chain or dataset behind | that ingestor's page, "Operating and recovering" |
| dbt cron failed or stalled | [dbt daily run failed](runbooks/dbt-daily-run-failed.md) |
| Upstream was repaired, dbt still wrong | [dbt reprocess](runbooks/dbt-reprocess.md) |
| Dashboard or API stale, warehouse fine | [Consumers showing stale data](runbooks/consumers-stale.md) |
| Nothing alerted and you do not trust that | [Monitoring & Detection](monitoring.md) |

---

## Missing API Endpoints

**Symptoms:** Expected API endpoints return 404, new dbt models do not appear in the Swagger UI.

### Step 1: Check Manifest Refresh

Look for manifest refresh logs:

Read the API workload's recent logs and filter for `manifest`:

Expected logs when manifest refreshes successfully:

```
Fetching manifest from https://gnosischain.github.io/dbt-cerebro/manifest.json...
Manifest downloaded successfully.
Loaded 412 models from dbt manifest.
```

If you see errors:

- **HTTP errors** -- The manifest URL may be unreachable or returning errors
- **Parse errors** -- The manifest JSON may be malformed
- **"Manifest not modified (304)"** -- The manifest has not changed since the last fetch

### Step 2: Force a Manifest Refresh

With a tier3 API key, trigger an immediate refresh:

```bash
curl -X POST "https://api.analytics.gnosis.io/v1/system/manifest/refresh" \
  -H "X-API-Key: YOUR_TIER3_KEY"
```

### Step 3: Verify dbt Tags

The model must have both `production` and an `api:{name}` tag to be registered. Check the model's configuration in dbt-cerebro:

```sql
-- Required tags for API exposure
tags=['production', 'consensus', 'api:blob_commitments', 'granularity:daily']
```

Common tagging mistakes:

- Missing `production` tag
- Misspelled `api:` prefix (e.g., `Api:`, `API:`)
- Missing category tag (the URL prefix)

### Step 4: Check for meta.api Validation Errors

If the model has a `meta.api` block with invalid configuration, it will be skipped during manifest loading. Check API logs for validation errors:

Read the API workload's recent logs and filter for `error` lines mentioning the upstream API.

Common validation issues:

- `parameters[].column` references a column not in the model's SELECT
- `sort[].column` references a column not in the model's SELECT
- `require_any_of` references undeclared parameter names
- `allow_unfiltered=false` with no declared parameters

### Step 5: Verify dbt Model Deployment

Confirm the model was deployed successfully in dbt-cerebro:

```bash
# In the dbt-cerebro container
dbt ls --select api_consensus_blob_commitments_daily
dbt run --select api_consensus_blob_commitments_daily
```

Check that the manifest was regenerated and published after the latest dbt run.

---

---

## Rate Limiting Issues

**Symptoms:** Receiving 429 (Too Many Requests) responses.

### Check Your Current Tier

The 429 response includes the `X-RateLimit-Limit` header showing your current limit:

```bash
curl -v "https://api.analytics.gnosis.io/v1/consensus/blob_commitments/latest"
```

Look for response headers:

```
X-RateLimit-Limit: 20
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1710500400
Retry-After: 42
```

### Per-Tier Limits

| Tier | Rate Limit |
|------|-----------|
| tier0 (no key) | 100 requests/min per IP |
| tier1 (partner) | 500 requests/min per key |
| tier2 (premium) | 1,000 requests/min per key |
| tier3 (internal) | 10,000 requests/min per key |

### Resolution Steps

1. **Wait for the window to reset** -- The `Retry-After` header tells you how long
2. **Add caching** -- Cache responses for `daily` and `all_time` endpoints
3. **Use pagination wisely** -- Fetch larger pages with higher `limit` values instead of many small requests
4. **Use POST with list filters** -- Batch multiple filter values into a single request instead of making separate requests
5. **Upgrade your tier** -- Contact the Gnosis Analytics team if you need higher limits

---

!!! info "Internal runbook"
    [runbooks/00-morning-check.md](https://github.com/gnosisdevops/infrastructure-gnosis-analytics/blob/main/runbooks/00-morning-check.md) — private repository; carries the exact cluster commands and the cron-log grep.
