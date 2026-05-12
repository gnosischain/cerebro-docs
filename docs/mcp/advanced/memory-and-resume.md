# Memory & Resume

How Cerebro remembers things across crashes, restarts, and conversations.

> **TL;DR.** Cerebro has **four** persistence layers: a SQLite event log (`~/.cerebro/cerebro_state.db`), durable JSON state for research projects, DuckDB sandboxes for what-if simulations, and per-process in-memory state for storyteller and session counters.

## The four memory layers

```text
┌───────────────────────────────────────────────────────────────────────┐
│ Cerebro MCP — Persistence layers                                      │
├───────────────────────────────────────────────────────────────────────┤
│ 1. Workflow event log     ~/.cerebro/cerebro_state.db (SQLite, WAL)   │
│    workflows + events + gates tables                                  │
│ 2. Research store         ~/.cerebro/research_projects/<id>/          │
│    project.json + evidence.json + memory.json + findings.json + ...   │
│ 3. Sandbox snapshots      ~/.cerebro/sandboxes/<id>/snapshot.parquet  │
│    DuckDB :memory: instances mounted from parquet                     │
│ 4. In-memory singletons (process lifetime only)                       │
│    storyteller_state, session counters, runtime_state                 │
└───────────────────────────────────────────────────────────────────────┘
```

| Layer | Format | Survives kill -9? | Survives box restart? | Used for |
|---|---|---|---|---|
| Event log | SQLite WAL | ✅ | ✅ | Crash recovery, resume hints, audit trail |
| Research store | JSON files | ✅ (atomic writes) | ✅ | Authoritative project state |
| Sandbox snapshots | parquet + DuckDB | ✅ parquet | ❌ DuckDB connection dies | Counterfactual simulations |
| In-memory state | Python dicts | ❌ | ❌ | Live storyteller phase, session counters |

## SQLite event log

**File:** `~/.cerebro/cerebro_state.db` (path overridable via `EVENT_STORE_PATH`).
**Pragmas:** `journal_mode=WAL`, `synchronous=NORMAL`, `foreign_keys=ON`.

### Schema

```sql
CREATE TABLE workflows (
  id            TEXT PRIMARY KEY,
  kind          TEXT NOT NULL,        -- "research_project" | "storyteller_session"
  status        TEXT NOT NULL,        -- "running" | "waiting_gate" | "completed" | "failed" | "orphaned"
  created_at    REAL NOT NULL,
  updated_at    REAL NOT NULL,        -- bumped by every event append
  metadata_json TEXT NOT NULL DEFAULT '{}',
  owner         TEXT                  -- SHA-256 hash of caller, NULL for legacy
);
CREATE INDEX idx_workflows_owner_status ON workflows(owner, status);

CREATE TABLE events (
  workflow_id        TEXT NOT NULL,
  seq                INTEGER NOT NULL,    -- monotonic per-workflow
  kind               TEXT NOT NULL,
  payload_json       BLOB NOT NULL,
  ts                 REAL NOT NULL,
  payload_compressed INTEGER NOT NULL DEFAULT 0,    -- gzip flag
  PRIMARY KEY (workflow_id, seq),
  FOREIGN KEY (workflow_id) REFERENCES workflows(id)
);
CREATE INDEX idx_events_workflow_seq ON events(workflow_id, seq);

CREATE TABLE gates (
  workflow_id  TEXT NOT NULL,
  gate_name    TEXT NOT NULL,
  status       TEXT NOT NULL,        -- "pending" | "ready" | "passed" | "failed"
  payload_json TEXT NOT NULL DEFAULT '{}',
  updated_at   REAL NOT NULL,
  PRIMARY KEY (workflow_id, gate_name)
);
```

### Why these design choices

- **Per-workflow seq** — concurrent workflows can write without contention beyond SQLite's writer lock.
- **`payload_json` as BLOB with gzip flag** — payloads >4 KB (LLM message histories) are gzipped before insert.
- **`updated_at` bumped on every append** — enables cheap "stale workflow" filtering. Subtlety: writing a `workflow_resume_hint` event refreshes `updated_at`, which is why `list_resumable_workflows` defaults to `min_idle_seconds=0`.
- **Two parallel APIs** — async `EventStore` (aiosqlite) and sync `event_store_sync` (stdlib sqlite3). Same file, same schema. Sync API is for sync MCP tools; async API for the parallel-fan-out runner and resume handlers.

### Self-bootstrapping

The sync path creates the schema on first connection if absent. So you can `rm ~/.cerebro/cerebro_state.db*` at any time and the next tool call recreates it cleanly.

## Event kinds

Three workflow kinds, each with their own event vocabulary. All events carry `kind`, `seq`, `ts`, and a workflow-specific `payload`.

### Universal

| Kind | When | Payload |
|---|---|---|
| `workflow_started` | Workflow row first created | `{project_id?, hypothesis?, scope?}` |
| `workflow_resume_hint` | Registry computes a resume outcome | `{kind, action, summary, resume_hint, unfinished_llm_call_count}` |
| `llm_call_started` / `llm_call_completed` / `llm_call_failed` | An agent runner brackets each LLM call | `LLMCallEvent` (subtask, call_id, system_prompt, full message history, tool_schemas, response, elapsed_seconds) |

### `research_project`

| Kind | When | Payload |
|---|---|---|
| `phase_planned` | `plan_research_phase` | `{phase, plan_preview}` |
| `phase_completed` | `execute_research_phase` advances | `{phase, advanced_to}` |
| `verification_completed` | `verify_research_phase` | `{phase, passed, summary_preview}` |
| `peer_review_recorded` | `record_peer_review` | `{status, summary_preview}` |
| `report_published` | `publish_research_report` | `{report_id, title}` |
| `query_executed` | `execute_query(... research_project_id=)` | `{sql_preview, sql_full_len, database, row_count, elapsed_seconds, evidence_title, artifact_ref_id, error_class}` |
| `memory_recorded` | `record_research_memory` | `{memory_id, kind, statement_preview, statement_full_len, confidence}` |
| `finding_recorded` | `record_research_finding` | `{finding_id, title, confidence, evidence_count}` |
| `evidence_attached` | `attach_research_evidence` / `capture_schema_snapshot` | `{kind, ref_id, phase, title}` |

### `storyteller_session`

| Kind | When | Payload |
|---|---|---|
| `workflow_started` | `storyteller_start_session` | `{session_id}` |
| `phase_advanced` | Any state-machine forward move | `{from, to}` |
| `gate_failed` | Clarity / accessibility check rolls back | `{gate, blocking_phase, reason}` |
| `handoff_completed` | `storyteller_generate_story_report` | `{report_id, style}` |
| `context_brief_recorded` | `storyteller_record_context_brief` | `{audience, mechanism, required_action}` |
| `big_idea_recorded` | `storyteller_record_big_idea` | `{sentence, stakes}` (verbatim ≤500 chars) |
| `storyboard_recorded` | `storyteller_record_storyboard` | `{scene_count, narrative_order, rationale_preview}` |
| `visual_spec_recorded` | `storyteller_record_visual_spec` | `{scene_index, chart_family, relationship, action_title}` |
| `final_story_recorded` | `storyteller_record_final_story` | `{title, content_length}` |

### Payload size budgets

Long-form text is truncated and a `*_full_len` paired so the resume hint can tell the agent "this preview is 800 of 4,200 chars; pull the full version from the JSON store if you need it."

| Field | Cap |
|---|---|
| `sql_preview` | 1500 chars |
| `statement_preview` (memory) | 800 chars |
| `plan_preview` | 500 chars |
| `summary_preview` | 500 chars |
| `title` | 300 chars |
| `audience` | 200 chars |
| `sentence` (big_idea, verbatim) | 500 chars |

## WorkflowRegistry and resume handlers

`workflow_registry.py` maps each `kind` to a pure async function: `(workflow_id, workflow_row, events) → ResumeOutcome`.

### `ResumeOutcome` shape

```python
@dataclass
class ResumeOutcome:
    workflow_id: str
    kind: str
    action: str               # "ready_to_resume" | "complete" | "failed" | "orphan" | "no_handler"
    summary: str
    resume_hint: dict
    unfinished_llm_calls: list[LLMCallEvent]
```

### Action vocabulary

| Action | Status side-effect |
|---|---|
| `ready_to_resume` | none |
| `complete` | row → `completed` |
| `failed` | row → `failed` |
| `orphan` | row → `orphaned` |
| `no_handler` | row → `orphaned` |

### Registered handlers

| Kind | Module | What's in the hint |
|---|---|---|
| `research_project` | `research_resume.py` | current_phase, completed_phases, next_action, gates, work block |
| `storyteller_session` | `storyteller_resume.py` | current_phase, next_action, content block |

## How writes flow

### Sync tool path (most research / storyteller tools)

```text
agent calls @mcp.tool() def some_tool(...)
  ↓
tool body runs (validates, mutates research_store / sandbox / etc.)
  ↓
tool calls a `record_*` helper from event_store_sync.py
  ↓
helper opens fresh sqlite3 connection, applies WAL+NORMAL pragmas,
  begins IMMEDIATE transaction, computes seq via SELECT MAX(seq)+1,
  inserts event, commits
  ↓
tool returns success
```

Event-log writes are wrapped in try/except in every `*_safe` helper. If the event log fails, the tool body still succeeds — event-log writes are observability, never correctness.

### Per-workflow append serialization

Concurrent appends against the same workflow can race on `SELECT MAX(seq) + 1`. Async `EventStore` uses an `asyncio.Lock` per workflow_id; sync `event_store_sync` uses `BEGIN IMMEDIATE` so SQLite serializes natively.

## How resume is computed

### Trigger 1: bootstrap-time sweep

On every server start, `bootstrap.init_event_store_async`:

1. Initializes the schema (idempotent).
2. Registers all known resume handlers.
3. Calls `registry.resume_all_running(max_age_seconds=24h)`.
4. For each, dispatches to the registered handler, gets a `ResumeOutcome`, appends a `workflow_resume_hint` event, flips status if terminal.

### Trigger 2: agent-on-demand

- `list_resumable_workflows(min_idle_seconds=0)` — markdown summary
- `get_workflow_resume_hint(workflow_id)` — JSON payload
- `recompute_workflow_resume_hint(workflow_id)` — re-runs the handler, appends fresh hint

The boot sweep and `recompute` call **the same handler function** — there's no second code path.

### Inside a handler

```python
async def resume_research_project(workflow_id, workflow_row, events):
    project_id = _project_id_from_workflow(workflow_row)
    kinds = [ev["kind"] for ev in events]
    if "report_published" in kinds:
        return ResumeOutcome(action=ACTION_COMPLETE, ...)
    verification_gate, peer_review_gate = _scan_gates(events)
    if peer_review_gate == "failed":
        return ResumeOutcome(action=ACTION_FAILED, ...)
    completed, current_phase = _scan_phases(events)
    next_action, next_args = _next_action_for_phase(current_phase, completed, project_id)
    work = _scan_work(events)
    unfinished = find_unfinished_llm_calls(events)
    return ResumeOutcome(
        action=ACTION_READY_TO_RESUME,
        summary=f"Project {project_id}: ready to resume at phase {current_phase!r}.",
        resume_hint={...},
        unfinished_llm_calls=unfinished,
    )
```

Pure function over events — no I/O, no LLM calls, no ClickHouse. Safe to run before the server has even opened its transport.

## Failure modes the design protects against

| Failure | Outcome | Where Phase 3 helps |
|---|---|---|
| Server `kill -9` mid-call | Atomically committed or not | SQLite WAL + atomic JSON writes |
| Server `kill -9` mid-research | Workflow row + completed phase events survive | Boot sweep + `recompute_hint` |
| Anthropic 529 / rate limit | LLM call interrupted | `unfinished_llm_calls` surfaces it (when wrapped by an agent runner) |
| Concurrent appends from `asyncio.gather` | UNIQUE constraint race | Per-workflow `asyncio.Lock` |
| DB file deleted between calls | Schema vanished | `event_store_sync._connect` self-bootstraps |
| Resume handler raises | Bootstrap should still succeed | Registry catches, converts to `failed`, logs |
| Wrong handler kind / missing handler | Workflow looks live forever | Falls back to `orphan` |

## Failure modes still outside cerebro's control

| Failure | Why cerebro can't help |
|---|---|
| **Claude Code wipes the conversation buffer** | Conversation lives in the LLM client's process; cerebro only sees tool calls |
| Agent runs `execute_query` *without* `research_project_id` | Cerebro can't tell which active workflow a free-form query belongs to |
| Agent forgets to call `record_research_memory` | We can't intercept thoughts — only tool calls |
| Network hiccup loses an in-flight tool call | Standard MCP retry territory; not our layer |

## Inspecting live state

```bash
sqlite3 ~/.cerebro/cerebro_state.db ".schema"

sqlite3 ~/.cerebro/cerebro_state.db \
  "SELECT kind, status, count(*) FROM workflows GROUP BY kind, status"

sqlite3 ~/.cerebro/cerebro_state.db "
  SELECT seq, kind, datetime(ts,'unixepoch') AS ts
  FROM events WHERE workflow_id = 'research_rp_xxx' ORDER BY seq"
```

## See also

- [Resumable Workflows](../workflows/resumable-workflows.md) — recovery commands
- [Multi-Tenant](multi-tenant.md) — owner column
- [Phase 3 design doc (cerebro-mcp)](https://github.com/gnosischain/cerebro-mcp/blob/main/docs/phase3_resumable_workflows.md)
- [Memory & Resume design doc (cerebro-mcp)](https://github.com/gnosischain/cerebro-mcp/blob/main/docs/memory_and_resume.md)
