# Resumable Workflows

How to recover a workflow that was interrupted by a crash, network blip, server restart, or chat wipe.

## What it is

Every workflow in Cerebro (research / storyteller / sandbox) writes structured events to `~/.cerebro/cerebro_state.db`. On every server start, a `WorkflowRegistry` walks each open workflow's event stream and computes a `ResumeOutcome` — a structured advice payload that the agent reads on the next user interaction.

The registry **never** auto-acts. It only emits a hint. The agent decides whether and how to resume.

## When to use it

- After an Anthropic 529 / rate limit interrupted a long workflow.
- After Claude Code wiped the conversation buffer.
- After `kill -9` on the MCP server.
- When picking up someone else's in-progress research project.
- When you want to know "did I publish that report?" without re-deriving it.

## The three resume tools

```text
list_resumable_workflows(min_idle_seconds=0)
  → markdown summary of every running / waiting_gate workflow with its latest hint

get_workflow_resume_hint(workflow_id)
  → JSON payload of the latest hint for one workflow

recompute_workflow_resume_hint(workflow_id)
  → re-runs the registered handler over the full event log,
    appends a fresh hint, flips terminal status if applicable
```

All three are read-only (apart from `recompute`, which appends one event).

## Step-by-step recovery

### 1. Find what's resumable

```text
list_resumable_workflows()
```

Output:

```text
| workflow_id                | kind                | status        | summary                                                    |
|----------------------------|---------------------|---------------|------------------------------------------------------------|
| research_rp_8f2a…          | research_project    | running       | hypothesis phase, 9 queries, 3 mem, 1 finding              |
| storyteller_vp_brief_q1    | storyteller_session | running       | big_idea recorded. storyboard has 3 scenes (0 specs done). |
```

### 2. Read the full hint

```text
get_workflow_resume_hint("research_rp_8f2a…")
```

Returns a structured payload with `next_action` + `next_action_args` pre-computed. The agent calls that tool to continue.

### 3. (Optional) recompute

If state has progressed since the bootstrap-time scan and the cached hint is stale:

```text
recompute_workflow_resume_hint("research_rp_8f2a…")
```

Walks the full event log fresh and writes a new hint. Status is flipped to `complete` / `failed` / `orphan` if the log shows a terminal event.

## Resume hint shapes

### Research project

```json
{
  "research_project_id": "rp_xxx",
  "current_phase": "execution",
  "completed_phases": ["mapping", "hypothesis"],
  "next_action": "execute_research_phase",
  "next_action_args": {"research_project_id": "rp_xxx", "phase": "execution"},
  "verification_gate": "passed",
  "peer_review_gate": null,
  "work": {
    "queries_run": 12,
    "queries_failed": 1,
    "error_classes": {"clickhouse_code_47": 1},
    "recent_memories": [{"statement_preview": "...", "confidence": 0.85}, ...],
    "recent_findings": [...],
    "evidence_by_phase": {"mapping": 1, "hypothesis": 2}
  }
}
```

### Storyteller

```json
{
  "session_id": "vp_brief_q1",
  "current_phase": "visual_design",
  "next_action": "storyteller_record_visual_spec",
  "content": {
    "audience": "Executive team",
    "mechanism": "decision_brief",
    "big_idea_sentence": "Q4 reorg unlocks 15% velocity at the cost of 2 senior departures.",
    "storyboard_scene_count": 3,
    "visual_specs_recorded": [],
    "visual_spec_chart_families": null,
    "final_story_title": null,
    "final_story_length": 0
  }
}
```

## Resume actions

| `action` | Meaning | Status flip |
|---|---|---|
| `ready_to_resume` | Workflow has more work; hint contains `next_action` | none |
| `complete` | Terminal success detected (`report_published` / `handoff_completed`) | → `completed` |
| `failed` | Terminal failure detected (rejected peer review, gate failure) | → `failed` |
| `orphan` | Stale beyond TTL OR handler can't make sense of state | → `orphaned` |
| `no_handler` | `kind` has no registered handler | → `orphaned` |

## Bootstrap-time sweep

On every server start, `bootstrap.init_event_store_async()`:

1. Initializes the event store schema (idempotent).
2. Registers all known resume handlers (research, storyteller).
3. Calls `registry.resume_all_running(max_age_seconds=24h)` — finds every workflow last touched > 24h ago.
4. For each, writes a `workflow_resume_hint` event with the outcome.
5. Logs a one-line summary: `Workflow resume sweep on startup: ready_to_resume=2, complete=1, orphaned=1`.

The 24h threshold is `WORKFLOW_ORPHAN_AGE_SECONDS`. Lower it to be more aggressive.

## Best practices

- **Default to `min_idle_seconds=0`** in `list_resumable_workflows` — otherwise the boot sweep's hint refresh hides the workflow it was written for (because writing a hint bumps `updated_at`).
- **Recompute when in doubt.** A cached hint can be hours old; `recompute_workflow_resume_hint` is cheap.
- **Treat `orphan` as final.** If a workflow is orphaned, restart from a new project — don't try to revive it.
- **Use a fresh chat per resume.** Old conversation context biases the agent toward re-running already-done steps.

## Pitfalls

- **Resume hint missing `next_action`.** Means the workflow is in an unrecognised state. Read the event log directly (`sqlite3 .cerebro/cerebro_state.db ...`) to figure out what happened.
- **`unfinished_llm_calls` field populated but agent ignores it.** Only an LLM-runner that emits `llm_call_started` events sees these. Most cerebro tools don't — they just record their inputs/outputs.
- **Trying to resume a workflow you don't own** (multi-tenant). The registry filters by owner; cross-tenant workflows are invisible.
- **Pulling resume across MCP server upgrades that change schema.** The schema is local and can be deleted/recreated; old workflows will not resume against new code.

## Live state inspection

```bash
# Schema sanity check
sqlite3 ~/.cerebro/cerebro_state.db ".schema"

# All workflows by status
sqlite3 ~/.cerebro/cerebro_state.db \
  "SELECT kind, status, count(*) FROM workflows GROUP BY kind, status"

# Most recent events on a specific workflow
sqlite3 ~/.cerebro/cerebro_state.db "
  SELECT seq, kind, datetime(ts,'unixepoch') AS ts
  FROM events WHERE workflow_id = 'research_rp_xxx' ORDER BY seq"

# Owner distribution (multi-tenant audit)
sqlite3 ~/.cerebro/cerebro_state.db \
  "SELECT substr(owner,1,12), count(*) FROM workflows GROUP BY 1 ORDER BY 2 DESC"
```

## See also

- [Memory & Resume](../advanced/memory-and-resume.md) — full event-log internals
- [Multi-Tenant](../advanced/multi-tenant.md) — owner filtering on resume
- [Research Projects](research-projects.md) / [Storyteller](storyteller.md) — workflow shapes
