# Storyteller

Eight-step pipeline for narrative-first deliverables: memos, decision briefs, pitches, customer stories, investor updates.

## What it is

The storyteller workflow forces a structured discipline before any prose is written:

1. **Context brief** — who is the audience, what mechanism (memo / pitch / brief), what action.
2. **Big idea** — one sentence. The thesis.
3. **Storyboard** — N scenes in a chosen narrative order.
4. **Visual specs** — per scene, the chart family + relationship + action title.
5. **Final story** — the drafted prose.
6. **Clarity gate** — language passes a clarity check.
7. **Accessibility gate** — colour, contrast, alt-text pass.
8. **Generate report** — emits the final layout (research / scrollytelling / dashboard).

Each step records an event. If the agent skips a step, the next call raises. The state machine lives in memory; observability events go to the [event log](../advanced/memory-and-resume.md).

## When to use it

- The deliverable's primary function is to **persuade** or **explain**, not catalogue.
- Memos, decision briefs, internal pitches, investor updates, customer success stories.
- The audience is non-technical or executive.
- You want a one-sentence "big idea" forced before any chart is drawn.

For analytical reports use [`generate_report`](../reports.md). For long-form research use [Research Projects](research-projects.md).

## Step-by-step tutorial

### 1. Start the session

```text
storyteller_start_session(
  session_id="memo_q1_retention",
  deliverable_kind="memo",
)
```

### 2. Record the context brief

```text
storyteller_record_context_brief(
  audience="VPs and engineering leadership",
  mechanism="memo",                       # or decision_brief / pitch / customer_story / investor_update
  required_action="approve Q1 budget reallocation",
)
```

### 3. Lock the big idea (single sentence)

```text
storyteller_record_big_idea(
  sentence="Q3 retention is up 8% MoM but driven entirely by a single onboarding cohort.",
  stakes="Without diversifying the cohort, growth stalls in Q4.",
)
```

The big-idea sentence is preserved verbatim in the event log (≤500 chars, no truncation marker).

### 4. Storyboard

```text
storyteller_record_storyboard(
  scene_count=5,
  narrative_order="chronological",       # or "lead_with_ending" / "build_to_climax"
  rationale="Build trust with familiar metrics, then reveal the cohort dependency.",
)
```

### 5. Visual spec per scene

```text
for i in range(5):
  storyteller_record_visual_spec(
    scene_index=i,
    chart_family="line",                 # or bar_vertical / scatter / heatmap / sankey / …
    relationship="trend",                # or category_comparison / correlation / part_to_whole / …
    action_title=f"Scene {i}: retention trajectory by month",
  )
```

Re-recording a `scene_index` is fine — the resume handler dedupes by index, keeping the latest spec.

### 6. Final story (prose)

```text
storyteller_record_final_story(
  title="Q3 Retention Brief",
  content_length=4823,
)
```

### 7. Gates

```text
storyteller_run_clarity_checks()
storyteller_record_accessibility_pass()
```

If a gate fails, the state machine rolls back to a `blocking_phase`. The resume hint surfaces the failed gate name so the next session knows which step to redo.

### 8. Generate the report

```text
storyteller_generate_story_report(
  style="research",   # or "scrollytelling" / "dashboard"
)
# → emits handoff_completed; returns file:// link
```

## Picking a `style`

| `style` | Layout | Natural fit | Required mechanism |
|---|---|---|---|
| `research` (default) | Research-essay (Anthropic-style). | Whitepapers, theses, narrative analyses. | memo / decision_brief |
| `scrollytelling` | Scroll-triggered visuals + reveals. | Pitches, customer stories, growth pitches, investor updates. | pitch / customer_story / investor_update |
| `dashboard` | Standard dashboard. | Backwards-compat / unsure. | any |

The mapping the storyteller uses:

- `mechanism=pitch \| customer_story \| investor_update` → `style="scrollytelling"` is a good default.
- `mechanism=memo \| decision_brief` → `style="research"` is a good default.

## Worked example

```text
> storyteller_start_session(session_id="vp_brief_q1", deliverable_kind="decision_brief")
> storyteller_record_context_brief(
    audience="Executive team",
    mechanism="decision_brief",
    required_action="Approve Q4 reorg",
  )
> storyteller_record_big_idea(
    sentence="Q4 reorg unlocks 15% velocity at the cost of 2 senior departures.",
    stakes="Without it, ship dates slip 6 weeks.",
  )
> storyteller_record_storyboard(scene_count=3, narrative_order="chronological")

# [chat dies]

> list_resumable_workflows()
< storyteller_vp_brief_q1 | storyteller_session | running |
  big_idea recorded. storyboard has 3 scenes (0 visual specs done).

> get_workflow_resume_hint("storyteller_vp_brief_q1")
< {
    "session_id": "vp_brief_q1",
    "current_phase": "visual_design",
    "next_action": "storyteller_record_visual_spec",
    "content": {
      "audience": "Executive team",
      "mechanism": "decision_brief",
      "big_idea_sentence": "Q4 reorg unlocks 15% velocity at the cost of 2 senior departures.",
      "storyboard_scene_count": 3,
      "visual_specs_recorded": [],
      "final_story_title": null
    }
  }

# Resume — agent picks up at visual_design phase
> storyteller_record_visual_spec(scene_index=0, chart_family="bar_vertical", ...)
> storyteller_record_visual_spec(scene_index=1, ...)
> storyteller_record_visual_spec(scene_index=2, ...)
> storyteller_record_final_story(title="Q4 Reorg Brief", content_length=2900)
> storyteller_run_clarity_checks()
> storyteller_record_accessibility_pass()
> storyteller_generate_story_report(style="research")
< file:///…/reports/storyteller_vp_brief_q1.html
```

## Tool reference

| Tool | Phase | Notes |
|---|---|---|
| `storyteller_start_session` | bootstrap | sets active singleton |
| `storyteller_record_context_brief` | context | emits `context_brief_recorded` |
| `storyteller_record_big_idea` | narrative | emits `big_idea_recorded` |
| `storyteller_record_storyboard` | storyboard | emits `storyboard_recorded` |
| `storyteller_record_visual_spec` | visual_design | one event per scene; dedup by `scene_index` |
| `storyteller_record_final_story` | write | emits `final_story_recorded` |
| `storyteller_run_clarity_checks` | critique | gate; on fail emits `gate_failed` |
| `storyteller_record_accessibility_pass` | accessibility | gate |
| `storyteller_generate_story_report` | handoff | terminal — emits `handoff_completed` |
| `storyteller_status` | any | inspect current phase / content |
| `storyteller_end_session` | any | clear singleton |

## Best practices

- **Don't skip the big idea.** A storyteller deliverable without a single-sentence thesis is a dashboard with prose around it.
- **One scene per beat.** If a scene tries to make two points, split it.
- **Action titles, not chart names.** "Scene 3: retention is concentrated in one cohort" beats "Scene 3: retention chart".
- **Re-record visual specs freely.** The handler dedupes by scene_index — last write wins.
- **Pick the layout style early.** Tells you what voice to draft in.

## Pitfalls

- **Trying to start two sessions at once.** Only one active session per process — calling `start_session` again clears any prior state.
- **Calling `generate_story_report` before gates pass.** Will raise. Run clarity + accessibility first.
- **Treating final_story `content_length` as a limit.** It's a recorded measurement, not a budget — but if the resume hint shows 80 chars where you wrote 8000, something dropped the prose.
- **Using `style="dashboard"` for a memo.** Works but loses the narrative pacing the layout was designed for.

## See also

- [Resumable Workflows](resumable-workflows.md) — recovery
- [Reports](../reports.md) — `style` layouts under the hood
- [Memory & Resume](../advanced/memory-and-resume.md) — event-log internals
- [Storyteller agent personas](../agents.md) — the underlying persona library
