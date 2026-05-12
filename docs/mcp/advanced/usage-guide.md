# Usage Guide

A comprehensive end-to-end guide: setup, recipes, recovery, best practices, and pitfalls.

> Companion pages:
> - [Setup](../setup.md) — install + connect Claude Desktop / VS Code / Claude Code
> - [Tools](../tools.md) — categorised tool reference
> - [Workflows](../workflows/index.md) — research / QBR / storyteller / sandbox flows
> - [Mini-Apps](../mini-apps/index.md) — interactive UI surfaces
> - [Memory & Resume](memory-and-resume.md), [Quality Gates](quality-gates.md), [Multi-Tenant](multi-tenant.md), [Semantic Metrics](semantic-metrics.md)

---

## Table of contents

1. [Quick start](#1-quick-start)
2. [Connection setup](#2-connection-setup)
3. [Mental model: the dispatcher pattern](#3-mental-model-the-dispatcher-pattern)
4. [Tool reference by category](#4-tool-reference-by-category)
5. [Workflow recipes](#5-workflow-recipes)
6. [Resume & recovery](#6-resume-recovery)
7. [Multi-tenant setup](#7-multi-tenant-setup)
8. [Best practices](#8-best-practices)
9. [Common pitfalls](#9-common-pitfalls)
10. [Tips, tricks, power patterns](#10-tips-tricks-power-patterns)
11. [Troubleshooting](#11-troubleshooting)

---

## 1. Quick start

The 30-second tour. Everything else elaborates on this.

```text
1. get_agent_persona("cerebro_dispatcher")        # always start here for non-trivial tasks
2. preflight_analytics_request(...)               # dispatcher emits this — gates the request
3. search_models / discover_models                # find dbt models across all tiers
4. get_model_details / describe_table             # exact columns + lineage
5. start_query / execute_query                    # SQL with date filter + LIMIT
6. generate_charts(specs=[...])                   # BATCH — minimum 3 charts, single call
7. generate_report(markdown="...")                # assembles the dashboard
   → returns file:// link. Show it. Don't paste markdown back.
```

For research projects, QBRs, or storyteller sessions, swap step 7 for the appropriate `publish_*` / `storyteller_generate_story_report` tool.

---

## 2. Connection setup

### Local stdio (default)

Add this to your MCP config (e.g. `~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "cerebro": {
      "command": "uv",
      "args": ["--directory", "/path/to/cerebro-mcp", "run", "cerebro-mcp"],
      "env": {
        "CEREBRO_OWNER": "alice@gnosis.io",
        "CEREBRO_OWNER_HASH_SALT": "rotate-me-quarterly",
        "CLICKHOUSE_PASSWORD": "..."
      }
    }
  }
}
```

`CEREBRO_OWNER` tags every workflow / event / report with a SHA-256 hash of your identity (salted by `CEREBRO_OWNER_HASH_SALT`). See [Multi-Tenant](multi-tenant.md).

### SSE / remote

```json
{
  "mcpServers": {
    "cerebro": {
      "url": "https://mcp.analytics.gnosis.io/sse",
      "headers": {
        "Authorization": "Bearer <token>",
        "X-Cerebro-Owner": "alice@gnosis.io"
      }
    }
  }
}
```

### Verifying the connection

```text
system_status()      # health + version
list_custom_tools()  # what's available in this build
get_help()           # top-level navigation
```

---

## 3. Mental model: the dispatcher pattern

The dispatcher is the front door. **Always start there for non-trivial requests.**

```text
get_agent_persona("cerebro_dispatcher")
```

The dispatcher:

1. Classifies intent (analytics report? MMM? research? case study?)
2. Runs `preflight_analytics_request` to gate the request
3. Names the specialist chain (e.g. `mmm_analyst → mmm_causal_reviewer → generate_report`)
4. Emits a binding **dispatch manifest**

**Skip the dispatcher only for:**

- Trivial turns ("hi", "list reports", "open report 3")
- Explicit specialist invocation ("use mmm_analyst on DEXes")
- Follow-up turns inside an already-dispatched workflow

The dispatcher is a router. It does not query the DB or write SQL. See [Cerebro Dispatcher](../dispatcher.md).

---

## 4. Tool reference by category

(Mirrors [Available Tools](../tools.md). Quick links.)

| Category | Anchor |
|---|---|
| Discovery & schema | [Tools §1](../tools.md#1-discovery-schema) |
| Query execution | [Tools §2](../tools.md#2-query-execution) |
| Visualisation & reporting | [Tools §3](../tools.md#3-visualisation-reporting) |
| Research workflow | [Tools §4](../tools.md#4-research-workflow) |
| Storyteller | [Tools §5](../tools.md#5-storyteller-narrative-pipeline) |
| Mini-apps | [Tools §6](../tools.md#6-mini-apps-live-ui-surfaces) |
| On-chain RPC & contract | [Tools §7](../tools.md#7-on-chain-rpc-contract-tools) |
| Simulation sandbox | [Tools §8](../tools.md#8-simulation-sandbox-duckdb-parquet) |
| Resume & state | [Tools §9](../tools.md#9-resume-state-inspection) |
| Bridges, validators, on-chain | [Tools §10](../tools.md#10-bridges-validators-on-chain-helpers) |
| Documentation & reasoning | [Tools §11](../tools.md#11-documentation-reasoning) |
| Agent personas | [Tools §12](../tools.md#12-agent-personas) |

---

## 5. Workflow recipes

### 5.1 "Show me a report on X" (standard analytical request)

```text
1. get_agent_persona("cerebro_dispatcher")
2. preflight_analytics_request(question="...", domain=...)
3. search_models("X")                              # exhaust — don't stop at first match
4. get_model_details(top 3-5 candidates)
5. describe_table(chosen tables)
6. start_query(EDA: quantiles, stddev, count)      # quick distribution
7. execute_query(...)                              # main queries with LIMIT + dates
                                                   # ≥1 statistical, ≥1 correlation
8. generate_charts(specs=[≥3 charts])              # BATCH
                                                   # ≥1 series_field/pie/treemap/heatmap/sankey
                                                   # ≥1 scatter/heatmap
9. generate_report(markdown="""
   ... {{chart:CHART_ID_1}} ...
   ## Key Takeaways
   | Takeaway | Evidence | Why it matters |
   |---|---|---|
   | ... | ... | ... |
   """)
10. Return file:// link. Ask about export.
```

### 5.2 Long-form research project

See [Research Projects](../workflows/research-projects.md) for the full walk-through. Compressed:

```text
1. start_research_project(question, hypothesis, scope)  # → rp_xxx
2. For each phase (mapping → hypothesis → execution → verification):
   a. plan_research_phase(rp_xxx, phase, plan)
   b. execute_research_phase(rp_xxx, phase)
      - record_research_finding/memory as they emerge
      - attach_research_evidence(rp_xxx, chart_id)
   c. verify_research_phase(rp_xxx, phase, passed=True, summary=...)
3. prepare_peer_review(rp_xxx)
4. record_peer_review(rp_xxx, status="approved" | "rejected", summary=...)
5. publish_research_report(rp_xxx, ...)             # terminal
```

### 5.3 Storyteller (memo / pitch / brief)

See [Storyteller](../workflows/storyteller.md):

```text
1. storyteller_start_session(session_id, deliverable_kind="memo")
2. storyteller_record_context_brief(audience, mechanism, required_action)
3. storyteller_record_big_idea(sentence, stakes)
4. storyteller_record_storyboard(scene_count, narrative_order, rationale)
5. for i in range(scene_count):
     storyteller_record_visual_spec(scene_index=i, chart_family=..., relationship=..., action_title=...)
6. storyteller_record_final_story(title, content_length)
7. storyteller_run_clarity_checks()
8. storyteller_record_accessibility_pass()
9. storyteller_generate_story_report(style="research" | "scrollytelling" | "dashboard")
```

### 5.4 MMM (sector contribution / ROI)

See [MMM](../mmm.md):

```text
1. get_agent_persona("mmm_analyst")
2. Synthesize a markdown DAG table (vars, edges, co-launched flags)
3. get_agent_persona("mmm_causal_reviewer")     # pass the DAG verbatim
4. If verdict=BLOCK: apply prescribed fix, re-submit
5. If verdict=PASS: generate_report(...)
6. Optionally: get_agent_persona("mmm_simulator") with (β, r, λ, current_spend, baseline_kpi)
```

**Do not call `generate_report` until reviewer verdict = PASS.**

### 5.5 What-if simulation

See [Simulation Sandboxes](../workflows/simulation-sandboxes.md):

```text
1. create_simulation_sandbox(name, source_query, table_name)
2. query_sandbox(name, "UPDATE ... SET ... = ... * 1.3")
3. query_sandbox(name, "SELECT ... aggregate the deltas ...")
4. destroy_sandbox(name)
```

---

## 6. Resume & recovery

If the chat dies, the agent loses context, or you `/clear`:

```text
1. list_resumable_workflows()
   → returns [{workflow_id, kind, last_event_at, action, summary}, ...]
2. get_workflow_resume_hint(workflow_id)
   → full hint with work / content / notes blocks + next_action
3. Call the next_action tool with next_action_args
```

See [Resumable Workflows](../workflows/resumable-workflows.md) for hint payload shapes by kind.

### What survives

- Everything in `cerebro_state.db`: workflows, events, gates, hints
- All findings, memories, evidence, notes, content recordings
- All generated reports (file:// paths)

### What does NOT survive

- Claude's in-conversation reasoning
- Untyped scratch ("I was thinking...") that wasn't saved via `record_research_memory` or `log_reasoning`

**Lesson:** save early, save often. Prefer `record_*` calls over inline prose.

---

## 7. Multi-tenant setup

See [Multi-Tenant](multi-tenant.md) for the full design. The summary:

- `CEREBRO_OWNER` (env or header) → SHA-256 hash → stamps every workflow.
- `list_resumable_workflows`, `get_workflow_resume_hint`, `list_reports` filter by owner.
- Single-token shared SSE = no isolation; per-user JWT validation upstream is required for real authz.

---

## 8. Best practices

### Discovery discipline

- Run `search_models` once per major entity in the question. Exhaust the catalogue.
- For each candidate, call `get_model_details`. Skip a candidate? `record_model_exclusion(name, reason)` — `generate_report` enforces this.
- Use `get_relevant_columns(query, table)` for wide tables (50+ columns).

### Query hygiene

- Always include a date filter — even `WHERE date >= today() - 90`.
- Always include `LIMIT` for EDA. Drop it only for charts.
- Use `argMax(col, date)` for stock measures (TVL, balance, supply). Never `SUM(stock_col)` over a range.
- Use `quantile(0.5)` (median) before `avg` — Gnosis Chain data is heavy-tailed.
- For correlations over time: first-difference or use `lagInFrame`. Plain `corr()` over levels is non-stationary.
- Deduplicate aggregator volume — `fct_execution_pools_daily` etc. need a CTE or first-hop-only filter.

### Reporting

- **One `generate_charts` batch call.** Multiple single calls slow the run and break gate counting.
- Minimum 3 charts. Include dimensional breakdown + scatter/heatmap + statistical summary.
- Key takeaways = 3-column markdown table (Takeaway / Evidence / Why it matters). Never bullets.
- After `generate_report`, return the file:// link. Do not paste markdown back.
- Acknowledge residual buckets in chart subtitle when filtering `WHERE label != ''`.

### Workflow durability

- Save findings the moment you have them — don't wait until "the end."
- Use `record_research_memory` for working notes. They survive chat wipes; inline prose doesn't.
- For long sessions: `record_research_memory` every ~5 minutes of substantive work.

### Performance

- Prefer `start_query` + `get_query_results` over `execute_query` for queries > 10s.
- Use `explain_query` before running heavy SQL.
- Sandboxes are cheap — spin one up for any iterative what-if.

---

## 9. Common pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Querying `execution.logs` directly for transfers | Slow, wrong amounts | Use `fct_token_transfers` or related dbt models |
| `SUM(tvl_usd)` over date range | `stock_flow_discipline` gate rejects | Use `argMax(tvl_usd, date)` |
| Plain `corr(x,y)` over time series | `stationarity_on_correlations` rejects | First-difference, Spearman, or note ADF |
| Single `generate_chart` calls | Slow, gate counts wrong | One `generate_charts(specs=[...])` batch |
| Pasting markdown back as a reply | User sees raw `{{chart:ID}}` | Show only the file:// link + summary |
| Hardcoding columns without `describe_table` | `Code 47` UNKNOWN_IDENTIFIER | `describe_table` first |
| Stopping search at first model match | Missed dimensions | Exhaust `search_models`, log exclusions |
| `generate_report` before MMM reviewer PASS | Causal review missing | Wait for reviewer verdict |
| Saving findings only at the end | Lost on chat wipe | Save immediately, every memory/finding |
| `min_idle_seconds=86400` on resume | Resume list empty after sweep | Use default 0 |
| Forgetting `research_project_id` on charts/queries | Evidence not linked to project | Always pass it |

---

## 10. Tips, tricks, power patterns

### Inspect raw state

```bash
sqlite3 ~/.cerebro/cerebro_state.db
.tables
SELECT id, kind, status, updated_at FROM workflows ORDER BY updated_at DESC LIMIT 10;
SELECT seq, kind, json_extract(payload, '$.preview')
  FROM events WHERE workflow_id = 'research_rp_abc' ORDER BY seq;
```

### Reopen a buried report

```text
list_reports()        # filter by kind
open_report(id=42)
```

### Hot-swap a chart in a published report

Reports embed SQL — click `</>` in the UI, copy, modify, then:

```text
generate_chart(spec={...})        # new chart_id
# Re-emit the report with the new placeholder
```

### Use the metric layer when available

`query_metrics` / `quick_metric_chart` are safer than raw SQL — semantics pre-validated, no column hallucination. See [Semantic Metrics](semantic-metrics.md).

### Pin schemas for research

```text
capture_schema_snapshot(research_project_id, tables=[...])
```

Locks the schema for the project's lifetime so column drift doesn't invalidate findings.

### Trust but verify

```text
verify_numbers(claim="DEX volume grew 12% MoM in Q1", sql="SELECT ...")
```

Returns a pass/fail + the actual number.

### Thinking mode for hard reasoning

```text
set_thinking_mode("high")
```

Longer scratchpad — useful before complex MMM / causal-review steps.

---

## 11. Troubleshooting

### `manifest_hash_mismatch`

Known platform bug. Fall back to raw SQL via `execute_query`. The metric layer recovers after the next dbt build.

### `Workflow not found` on resume

The workflow exists but was created under a different `CEREBRO_OWNER`. Check `owner_hash` in `cerebro_state.db`. Cross-tenant access is blocked by design.

### `aiosqlite: threads can only be started once`

Stale connection in the pool. Restart the MCP server.

### Charts render but report rejects them

Check the gate output. Most common: missing `series_field` (no dimensional breakdown), or no scatter/heatmap. Add a chart that satisfies the gate. See [Quality Gates](quality-gates.md).

### Resume hint shows old next_action

```text
recompute_workflow_resume_hint(workflow_id)
```

Forces a fresh scan over the full event log.

### "Chat cleared completely on crash"

This is upstream of cerebro (Claude conversation buffer). The cerebro event log still has everything — use [§6 Resume](#6-resume-recovery) to recover. Save memories more frequently to minimise loss.

---

## See also

- [Memory & Resume](memory-and-resume.md) — event log internals
- [Hybrid Search](hybrid-search.md) — `search_models` ranking
- [Quality Gates](quality-gates.md) — report enforcement
- [Multi-Tenant](multi-tenant.md) — owner identity
- [Semantic Metrics](semantic-metrics.md) — when to use the registry
