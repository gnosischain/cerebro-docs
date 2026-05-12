# Research Projects

End-to-end multi-phase analysis with durable state, evidence attachments, and peer-review gating.

## What it is

A research project is a workflow scoped to a single hypothesis. It walks through five canonical phases — `mapping`, `hypothesis`, `execution`, `verification`, `publication` — with a peer-review gate before publication. Every phase, every recorded finding, every attached chart, and every executed query lands in the [event log](../advanced/memory-and-resume.md), so a crash mid-phase loses no progress.

## When to use it

- The deliverable is a long-form research report (essay or whitepaper).
- The work spans more than one chat session.
- Multiple findings need to be assembled with evidence cross-references.
- A peer reviewer must sign off before publication.
- You want the work to be resumable from any point.

For one-off analytical reports use [`generate_report`](../reports.md) directly. For narrative-first deliverables (memos, pitches), use [Storyteller](storyteller.md).

## Step-by-step tutorial

### 1. Start the project

```text
start_research_project(
  question="Why did Gnosis Pay payment volume drop 22% in February?",
  hypothesis="A single-cohort onboarding campaign ended in late January.",
  scope="Payment volume Jan–Mar 2026 by cohort, segment, geography.",
)
# → returns research_project_id (e.g. rp_009c4ade8d6e)
```

This emits `workflow_started`, creates the workflow row, and returns a `research_project_id` you'll thread through every later call.

### 2. Pin schemas (recommended)

```text
capture_schema_snapshot(
  research_project_id="rp_009c4ade8d6e",
  tables=["fct_execution_gpay_kpi_daily", "dim_token", "dim_address_labels"],
)
```

Locks column definitions for the lifetime of the project so column drift later doesn't invalidate findings.

### 3. For each phase: plan → execute → verify

```text
plan_research_phase(
  research_project_id="rp_009c4ade8d6e",
  phase="mapping",
  plan_markdown="""
  1. Identify all upstream models touching gpay payment volume.
  2. Map cohort definitions (onboarding date, source, geography).
  3. Confirm aggregator dedup is correct.
  """,
)

# inside execute_research_phase, call data tools:
execute_research_phase(
  research_project_id="rp_009c4ade8d6e",
  phase="mapping",
)

# during execution, record findings/memories as they emerge:
record_research_memory(
  research_project_id="rp_009c4ade8d6e",
  kind="observation",
  statement="cohort_2025_q4 contains 78% of Feb volume — single-cohort risk confirmed",
  confidence=0.85,
)

record_research_finding(
  research_project_id="rp_009c4ade8d6e",
  title="Volume concentration in 2025-Q4 cohort",
  confidence=0.9,
)

attach_research_evidence(
  research_project_id="rp_009c4ade8d6e",
  finding_id="finding_xxx",
  ref_kind="chart",
  ref_id="chart_3",
  title="Volume share by cohort, Jan–Mar",
)

# finally:
verify_research_phase(
  research_project_id="rp_009c4ade8d6e",
  phase="mapping",
  passed=True,
  summary="3 candidate cohorts identified; volume concentration confirmed.",
)
```

Repeat for `hypothesis`, `execution`, `verification`. Each phase emits its own events; resume always knows the phase you're in.

### 4. Peer review gate

```text
prepare_peer_review(research_project_id="rp_009c4ade8d6e")

# reviewer reads findings, evidence, and runs their own checks…

record_peer_review(
  research_project_id="rp_009c4ade8d6e",
  status="approved",   # or "rejected"
  summary="Cohort dedup verified; conclusions hold.",
)
```

If `status="rejected"`, the workflow is marked `failed` and the resume handler will surface the reviewer summary on the next interaction.

### 5. Publish

```text
publish_research_report(
  research_project_id="rp_009c4ade8d6e",
  title="Gnosis Pay Q1 Volume Drop: Cohort Concentration",
  format="research",   # uses generate_research_report under the hood
)
# → returns file:// link, marks workflow complete
```

## Worked example

Concrete log of a session that survived a crash:

```text
> start_research_project(question="...", hypothesis="...")
< rp_8f2a... created. workflow_id=research_rp_8f2a...

> plan_research_phase("rp_8f2a...", "mapping", "...")
> execute_research_phase("rp_8f2a...", "mapping")
> [9 search_models / get_model_details / execute_query calls — all logged]
> record_research_memory(...)   # x3
> record_research_finding(...)  # x1
> verify_research_phase(..., passed=True)

> plan_research_phase(..., phase="hypothesis", ...)
> execute_research_phase(..., phase="hypothesis")
< [LLM session crashes here — Anthropic 529]

# Server restart, fresh chat session
> list_resumable_workflows()
< | id | kind | status | last_event |
  | research_rp_8f2a... | research_project | running | hypothesis phase, 3 mem, 1 finding |

> get_workflow_resume_hint("research_rp_8f2a...")
< {
    "current_phase": "hypothesis",
    "completed_phases": ["mapping"],
    "next_action": "execute_research_phase",
    "next_action_args": {"research_project_id": "rp_8f2a...", "phase": "hypothesis"},
    "verification_gate": null,
    "peer_review_gate": null,
    "work": {
      "queries_run": 9, "queries_failed": 0,
      "recent_memories": [{"statement_preview": "...", "confidence": 0.85}, …],
      "recent_findings": [{"title": "Volume concentration in 2025-Q4 cohort", …}],
      "evidence_by_phase": {"mapping": 1}
    }
  }

> execute_research_phase("rp_8f2a...", "hypothesis")
# resumes cleanly from where it died — no re-running of mapping queries
```

## Tool reference

| Tool | Phase | Notes |
|---|---|---|
| `start_research_project` | bootstrap | emits `workflow_started` |
| `capture_schema_snapshot` | bootstrap | one-time, optional |
| `plan_research_phase` | per phase | emits `phase_planned` |
| `execute_research_phase` | per phase | emits `phase_completed` on advance |
| `verify_research_phase` | per phase | flips `verification:<phase>` gate |
| `record_research_memory` | any | emits `memory_recorded` |
| `record_research_finding` | any | emits `finding_recorded` |
| `attach_research_evidence` | any | emits `evidence_attached` |
| `prepare_peer_review` | gate | sets up the review payload |
| `record_peer_review` | gate | flips `peer_review` gate |
| `publish_research_report` | terminal | emits `report_published`, status → completed |
| `get_research_project` / `_findings` / `_memory` / `_evidence` | read | accessors |

## Best practices

- **Save findings the moment you have them.** Don't wait until "the end" — chat wipes are real.
- **Always thread `research_project_id` through `execute_query`** so the work-event capture associates queries with the project.
- **One project per hypothesis.** A scope creep should fork into a new project.
- **Use `record_research_memory` every ~5 minutes** of substantive work. The memory survives chat wipes; inline prose doesn't.
- **Pin schemas at the top.** A two-week project on a model whose columns drift mid-flight creates ghost findings.
- **Treat peer review as a real gate.** A `status="rejected"` is the correct outcome when assumptions don't hold — don't push through.

## Pitfalls

- **Forgetting `research_project_id` on `execute_query`.** The query runs but isn't logged to the event stream, so resume can't see it.
- **Calling `publish_research_report` without peer review.** Tool will succeed but the workflow shows ungated publication — fine occasionally, not the norm.
- **Re-using a project_id across hypotheses.** The event log gets mixed; resume hints become misleading.
- **Discarding findings on `failed` peer review.** The findings are still in the JSON store — re-open, address feedback, start a new project that cites them.

## See also

- [Memory & Resume](../advanced/memory-and-resume.md) — event-log internals
- [Resumable Workflows](resumable-workflows.md) — recovery commands
- [Reports](../reports.md) — `generate_research_report` layout details
- [Quality Gates](../advanced/quality-gates.md) — what `publish_research_report` enforces
