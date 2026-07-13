# Simulation Sandboxes

DuckDB + Parquet sandboxes for counterfactual SQL — UPDATE, INSERT, DELETE — without ever touching production ClickHouse.

## What it is

ClickHouse is `readonly=1` for analyst safety. That's the right default but it leaves simulator agents with nothing but prose for "what if we boosted cashback 30%?" questions. Sandboxes solve this:

1. Cerebro exports a CH `SELECT` to `~/.cerebro/sandboxes/<id>/snapshot.parquet`.
2. An in-memory DuckDB connection mounts the parquet as a regular table.
3. The agent runs **any** SQL inside DuckDB — read or write — until the question is answered.
4. The sandbox is destroyed (or evicted by TTL/LRU).

Production CH never sees a write. The parquet is auditable and replayable.

The sandbox tools are registered only when `SANDBOX_ENABLED=true` (off by default — enable it for local use; the deployed instance keeps it off to avoid provisioning persistent storage).

## When to use it

- Counterfactuals that touch >10 rows or >2 dimensions ("what if cashback was +30% across all February?").
- Forecasting experiments with synthetic future rows.
- Multi-step UPDATE/INSERT chains that build a hypothetical state.
- MMM simulator (`mmm_simulator` persona) and forecasting analyst flows.

For pure-formula deltas (single multiplier on a single aggregate) skip the sandbox and compute in raw CH SQL.

## Step-by-step tutorial

### 1. Fork the relevant CH slice

```text
create_simulation_sandbox(
  sandbox_id="gpay_q2_baseline",
  source_query='''
    SELECT day,
           sum(payment_volume_usd) AS volume,
           sum(cashback_usd)        AS cashback,
           count(distinct user_id)  AS active_users
    FROM dbt.fct_execution_gpay_kpi_daily
    WHERE day >= today() - 90
    GROUP BY day
  ''',
  table_name="baseline",
)
# → returns {sandbox_id, table, row_count, bytes, parquet_path}
```

The export is bounded by `SANDBOX_MAX_BYTES_PER_EXPORT` (default 2 GB).

### 2. Mutate the snapshot

```text
query_sandbox(
  sandbox_id="gpay_q2_baseline",
  sql="UPDATE baseline SET cashback = cashback * 1.3",
)
# → {rows_affected: 90}
```

### 3. Re-aggregate / compare

```text
query_sandbox(
  sandbox_id="gpay_q2_baseline",
  sql='''
    SELECT
      sum(cashback)                              AS new_cashback_total,
      (sum(cashback) - sum(cashback) / 1.3)      AS cashback_delta_usd,
      sum(cashback) / nullif(sum(volume), 0) * 100 AS new_cashback_pct
    FROM baseline
  ''',
)
```

### 4. Tear down

```text
destroy_sandbox("gpay_q2_baseline")
# Idempotent. Returns False if not found.
```

## Worked example: forecasting with synthetic rows

```text
create_simulation_sandbox(
  sandbox_id="validators_zerogrowth_q3",
  source_query='''
    SELECT day, count(*) AS active_validators
    FROM dbt.api_consensus_validators_active_daily
    WHERE day >= today() - 365
    GROUP BY day
  ''',
  table_name="series",
)

query_sandbox(
  sandbox_id="validators_zerogrowth_q3",
  sql='''
    INSERT INTO series
    SELECT t.day, last_value(active_validators)
    FROM (SELECT * FROM series ORDER BY day DESC LIMIT 1) AS last_row
    CROSS JOIN UNNEST(generate_series(today() + 1, today() + 90, INTERVAL 1 DAY)) AS t(day)
  ''',
)

# now run the same forecasting SQL you'd run on CH against `series`
query_sandbox(
  sandbox_id="validators_zerogrowth_q3",
  sql="SELECT … FROM series",
)

destroy_sandbox("validators_zerogrowth_q3")
```

## Tool reference

| Tool | Purpose |
|---|---|
| `create_simulation_sandbox(sandbox_id, source_query, table_name="data", database="dbt")` | Fork CH data into an in-memory DuckDB sandbox with a parquet snapshot on disk. |
| `query_sandbox(sandbox_id, sql, max_rows=200)` | Run any SQL (read or write) against the sandbox. |
| `list_sandboxes()` | Diagnostic listing. |
| `destroy_sandbox(sandbox_id)` | Tear down. Idempotent. |

## Operational characteristics

| Property | Value |
|---|---|
| Sandbox state | local disk (parquet) + in-memory DuckDB |
| Production CH writes | **zero** — `readonly=1` enforced at CH client level |
| Per-sandbox disk cap | `SANDBOX_MAX_BYTES_PER_EXPORT` (default 2 GB) |
| Concurrency | RLock per manager (different sandboxes parallel; same one serialized) |
| Eviction | LRU at `SANDBOX_MAX_CONCURRENT` (default 4) |
| Idle TTL | `SANDBOX_TTL_SECONDS` (default 30 min) |
| Crash safety | `atexit` teardown; parquet survives, DuckDB connection does not |

## Type sanitizer

ClickHouse → Arrow → DuckDB is not 1:1. Some CH types crash pyarrow or read back as opaque BLOBs. Cerebro wraps every export in a sanitising outer SELECT:

| ClickHouse type | Cast applied | Reason |
|---|---|---|
| `Enum8 / Enum16` | `CAST(col AS String)` | Default arrow surface is int — loses labels. |
| `UUID` | `toString(col)` | `fixed_size_binary[16]` reads as BLOB. |
| `IPv4 / IPv6` | `toString(col)` | Same BLOB problem. |
| `DateTime64(N)` for N>6 | `toDateTime64(col, 6)` | Arrow ns precision unreliable in some builds. |
| `Decimal(P, S)` for P>38 | `CAST(col AS Float64)` | Arrow `decimal128` caps at 38. |
| `Date / Date32` | `toDate32(col)` | Avoids `USMALLINT` mishap in DuckDB. |
| `Array(Tuple(...))` deeply nested | `toString(col)` | DuckDB chokes. |
| `Nullable(T)` / `LowCardinality(T)` | wrappers stripped, then re-evaluate `T` | Casts still produce nullable output. |

You don't have to think about this — it's automatic. But if a sandbox query fails with `Binder Error: No function matches…`, check whether the CH source column is one of the above types.

## Best practices

- **Source query should already aggregate/filter.** Don't fork a million-row raw table — fork the aggregate you'll mutate.
- **Use real names for sandboxes.** `gpay_q2_baseline` beats `s1`. The id appears in resume hints and audit logs.
- **Always `destroy_sandbox` when done.** TTL + LRU will clean up but explicit teardown is hygienic.
- **Test the same SQL on CH first.** A query that fails against the live data won't be fixed by sandboxing.
- **Reuse table names across sandboxes.** Each sandbox is isolated — `data`, `baseline`, `series` are fine to repeat.

## Pitfalls

- **Trying to write back to ClickHouse.** Production CH stays `readonly=1`. The sandbox is the only mutable surface.
- **Expecting persistence across server restart.** DuckDB is in-memory. The parquet survives but auto-remount is not implemented — re-create the sandbox on the next session.
- **Multi-table joins inside a sandbox.** Each `create_simulation_sandbox` produces one parquet → one DuckDB table. Multi-table mounts are not yet exposed; combine them into the source query if needed.
- **Hitting the 2 GB cap.** Bump `SANDBOX_MAX_BYTES_PER_EXPORT` if your source query needs more, or aggregate first.

## See also

- [Memory & Resume](../advanced/memory-and-resume.md) — sandbox lifecycle hooks
- [Phase 2 design doc (cerebro-mcp repo)](https://github.com/gnosischain/cerebro-mcp/blob/main/docs/phase2_simulation_sandbox.md) — the original sprint write-up
- [MMM](../mmm.md) — the simulator persona that drives this most heavily
