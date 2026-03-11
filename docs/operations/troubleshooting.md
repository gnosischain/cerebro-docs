---
title: Troubleshooting
description: Common issues and resolution steps for the Gnosis Analytics platform
---

# Troubleshooting

This page covers common issues encountered when operating the Gnosis Analytics platform and provides step-by-step resolution procedures.

## API Not Responding

**Symptoms:** HTTP requests to `api.analytics.gnosis.io` return connection errors, timeouts, or 502/503 status codes.

### Step 1: Check Pod Status

```bash
kubectl get pods -n cerebro -l app=cerebro-api
```

| Pod Status | Meaning | Action |
|-----------|---------|--------|
| `Running` | Pod is running but may be unhealthy | Check logs and probes |
| `CrashLoopBackOff` | Pod is crashing and restarting repeatedly | Check logs for startup errors |
| `Pending` | Pod cannot be scheduled | Check node resources and events |
| `ImagePullBackOff` | Cannot pull Docker image | Check GHCR credentials and image tag |

### Step 2: Check Pod Logs

```bash
kubectl logs -n cerebro deployment/cerebro-api --tail=100
```

Look for:

- ClickHouse connection errors on startup
- Manifest loading failures
- Python stack traces indicating application errors

### Step 3: Check Readiness Probe

```bash
kubectl describe pod -n cerebro -l app=cerebro-api | grep -A 5 "Readiness"
```

If the readiness probe is failing, the pod is not receiving traffic even though it is running. Common causes:

- Application has not finished starting (increase `initialDelaySeconds`)
- Application is stuck on a long-running startup task (manifest download)
- Port mismatch between probe and application

### Step 4: Check ClickHouse Connectivity

From inside the pod:

```bash
kubectl exec -n cerebro deployment/cerebro-api -- \
  curl -s "https://${CLICKHOUSE_URL}:8443/ping"
```

If this fails, check:

- ClickHouse Cloud service status
- Network security group rules
- ClickHouse credentials in Kubernetes secrets

### Step 5: Check ALB and Ingress

```bash
kubectl get ingress -n cerebro
kubectl describe ingress cerebro-api -n cerebro
```

Verify:

- ALB is provisioned and has a DNS name
- Target group health checks are passing
- TLS certificate is valid and not expired

---

## Missing API Endpoints

**Symptoms:** Expected API endpoints return 404, new dbt models do not appear in the Swagger UI.

### Step 1: Check Manifest Refresh

Look for manifest refresh logs:

```bash
kubectl logs -n cerebro deployment/cerebro-api --tail=200 | grep -i "manifest"
```

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

```bash
kubectl logs -n cerebro deployment/cerebro-api | grep -i "error" | grep -i "api"
```

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
| tier0 (no key) | 20 requests/min per IP |
| tier1 (partner) | 100 requests/min per key |
| tier2 (premium) | 500 requests/min per key |
| tier3 (internal) | 10,000 requests/min per key |

### Resolution Steps

1. **Wait for the window to reset** -- The `Retry-After` header tells you how long
2. **Add caching** -- Cache responses for `daily` and `all_time` endpoints
3. **Use pagination wisely** -- Fetch larger pages with higher `limit` values instead of many small requests
4. **Use POST with list filters** -- Batch multiple filter values into a single request instead of making separate requests
5. **Upgrade your tier** -- Contact the Gnosis Analytics team if you need higher limits

---

## ClickHouse Connection Errors

**Symptoms:** API returns 500 errors, logs show ClickHouse connection failures.

### Step 1: Verify ClickHouse Cloud Status

Check if ClickHouse Cloud is operational. Connection errors during planned maintenance windows are expected.

### Step 2: Check Credentials

Verify the Kubernetes secret contains correct credentials:

```bash
kubectl get secret cerebro-api-secrets -n cerebro -o jsonpath='{.data.CLICKHOUSE_URL}' | base64 -d
kubectl get secret cerebro-api-secrets -n cerebro -o jsonpath='{.data.CLICKHOUSE_USER}' | base64 -d
```

Compare with the expected values in AWS SSM Parameter Store.

### Step 3: Test Connectivity from Pod

```bash
kubectl exec -n cerebro deployment/cerebro-api -- \
  curl -s "https://${CLICKHOUSE_URL}:8443/?query=SELECT+1"
```

### Step 4: Check Network / Firewall

- Verify the EKS cluster's security group allows outbound HTTPS (443) and ClickHouse (8443)
- Check if ClickHouse Cloud's IP allowlist includes the cluster's NAT gateway IP
- Verify DNS resolution of the ClickHouse hostname from within the pod

### Step 5: Check External Secrets Sync

```bash
kubectl get externalsecret cerebro-api-secrets -n cerebro
```

If the status shows `SecretSyncedError`, the secret sync from SSM has failed. Check:

- ESO pod logs: `kubectl logs -n external-secrets deployment/external-secrets`
- IAM permissions for the ESO service account
- SSM parameter paths in the ExternalSecret resource

---

## Indexer Lag

**Symptoms:** Indexed data is behind the current chain head. API shows stale data.

### Step 1: Check Indexer Status

```bash
# cryo-indexer
kubectl logs -n indexers deployment/cryo-indexer --tail=50

# beacon-indexer
kubectl logs -n indexers deployment/beacon-indexer --tail=50
```

Look for:

- Current block/slot being processed
- Processing rate (blocks per second)
- Any error messages

### Step 2: Check RPC Endpoint Health

Indexers depend on blockchain RPC endpoints. If the RPC node is slow or unreachable, indexing stalls.

```bash
# Check execution layer RPC
kubectl exec -n indexers deployment/cryo-indexer -- \
  curl -s -X POST "${RPC_URL}" \
  -H "Content-Type: application/json" \
  -d '{"method":"eth_blockNumber","params":[],"id":1,"jsonrpc":"2.0"}'

# Check consensus layer API
kubectl exec -n indexers deployment/beacon-indexer -- \
  curl -s "${BEACON_API_URL}/eth/v1/node/syncing"
```

### Step 3: Check for Processing Errors

If the indexer encounters invalid or unexpected data, it may stall on a specific block. Check logs for:

- Parse errors
- RPC timeout errors
- ClickHouse write errors

### Step 4: Resume from Last Known Position

If an indexer is stuck, restarting it will typically resume from the last successfully indexed block:

```bash
kubectl rollout restart deployment/cryo-indexer -n indexers
```

For beacon-indexer, check the `START_SLOT` environment variable to ensure it is not set to an old value.

---

## Data Freshness Issues

**Symptoms:** API returns data that is hours or days behind the current date.

### Step 1: Identify the Bottleneck

Data freshness depends on three stages:

```
Indexer --> ClickHouse --> dbt run --> API (manifest refresh)
```

Check each stage:

1. **Indexer** -- Is the indexer caught up to the chain head? (See [Indexer Lag](#indexer-lag))
2. **dbt run** -- When was the last successful dbt run?
3. **Manifest refresh** -- When did the API last refresh its manifest?

### Step 2: Check dbt Run Schedule

dbt-cerebro runs on a schedule. Verify the last run:

```bash
# In the dbt container
dbt run-results --select api_consensus_blob_commitments_daily
```

Check for:

- Run failures -- A failed dbt run means models were not updated
- Incremental model issues -- The `apply_monthly_incremental_filter` may not be picking up the latest data
- Full refresh needed -- Some models may need a `--full-refresh` to resync

### Step 3: Check Incremental Model Status

If an incremental model is not picking up new data:

```sql
-- Check the latest date in the model
SELECT max(date) FROM dbt.int_consensus_blob_commitments_daily
```

Compare with the latest date in the source:

```sql
-- Check the latest date in raw data
SELECT max(toDate(slot_timestamp)) FROM consensus.blocks
```

If there is a gap, the incremental filter may need investigation. A `--full-refresh` can resolve state issues:

```bash
dbt run --select int_consensus_blob_commitments_daily --full-refresh
```

### Step 4: Check API Manifest

Verify the API is serving the latest manifest:

```bash
curl -s "https://api.analytics.gnosis.io/" | jq .
```

If the API is running but serving stale data, the issue is upstream (dbt run or indexer).

---

## CronJob Failures

**Symptoms:** click-runner or other scheduled jobs are not completing successfully.

### Step 1: Check CronJob Status

```bash
kubectl get cronjobs -n crawlers
kubectl get jobs -n crawlers --sort-by=.metadata.creationTimestamp
```

### Step 2: Check Failed Job Logs

```bash
# Find the failed job
kubectl get jobs -n crawlers | grep -v "1/1"

# Get logs from the failed pod
kubectl logs -n crawlers job/click-runner-ember-28438400
```

### Step 3: Common CronJob Issues

| Issue | Cause | Resolution |
|-------|-------|------------|
| Job never runs | `schedule` is in UTC, not local time | Adjust cron expression |
| Job runs but fails | ClickHouse credentials expired | Update SSM parameter and restart ESO |
| Job stuck as `Active` | Previous job still running | Set `concurrencyPolicy: Forbid` |
| Job completes but no data | Source URL changed or returned empty | Check external data source |
| Job exceeds `backoffLimit` | Repeated failures | Fix the root cause and manually trigger |

### Step 4: Manually Trigger a Job

```bash
kubectl create job --from=cronjob/click-runner-ember manual-ember-run -n crawlers
```

---

## General Debugging Commands

### Pod Inspection

```bash
# List all pods across namespaces
kubectl get pods --all-namespaces

# Describe a pod (shows events, conditions, resource usage)
kubectl describe pod <pod-name> -n <namespace>

# Get pod resource usage
kubectl top pods -n cerebro

# Execute a shell in a running pod
kubectl exec -it <pod-name> -n <namespace> -- /bin/bash
```

### Log Inspection

```bash
# Recent logs from a deployment
kubectl logs -n cerebro deployment/cerebro-api --tail=200

# Follow logs in real-time
kubectl logs -n cerebro deployment/cerebro-api -f

# Logs from a previous (crashed) container
kubectl logs -n cerebro <pod-name> --previous
```

### Secret Inspection

```bash
# List secrets
kubectl get secrets -n cerebro

# Check ExternalSecret sync status
kubectl get externalsecrets -n cerebro

# Decode a secret value
kubectl get secret cerebro-api-secrets -n cerebro \
  -o jsonpath='{.data.CLICKHOUSE_URL}' | base64 -d
```

## Next Steps

- [Monitoring](monitoring.md) -- Set up proactive alerting to catch issues early
- [Deployment](deployment.md) -- Review deployment procedures
- [Infrastructure](infrastructure.md) -- Understand the platform architecture
