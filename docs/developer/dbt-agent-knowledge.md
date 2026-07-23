---
title: dbt Agent Knowledge System
description: How dbt-cerebro packages contracts, lesson records, and hazards so AI agents and humans can change models safely
---

# dbt Agent Knowledge System

The [dbt-cerebro](https://github.com/gnosischain/dbt-cerebro) repository ships a knowledge layer that makes dbt engineering safe for AI agents and humans alike. Before anyone touches a model, the system supplies its resolved contract (grain, invariants, known hazards), the lessons learned from past incidents, and the safe reprocess runbook -- and Cerebro MCP serves all of it to any connected agent. This page is an overview; the authoritative depth lives in the dbt-cerebro repo itself.

## What It Is

The same data-quality mistake classes kept recurring -- staged batches wiping partitions, appends doubling populated months, cumulative chains backfilled in the wrong order. Each was diagnosed at high cost and then re-committed by the next session that lacked the context. The knowledge system turns that experience into three enforceable layers:

| Layer | Artifact | Purpose |
|-------|----------|---------|
| Operating guides | `AGENTS.md` hierarchy | Workflow rules, refresh levers, non-negotiable modeling rules |
| Incident knowledge | `docs/lessons/` records | Searchable post-mortems of known mistake classes |
| Per-model contracts | `target/agent_context.json` | Resolved grain, invariants, hazards, and runbook per model |

### AGENTS.md hierarchy

The root [`AGENTS.md`](https://github.com/gnosischain/dbt-cerebro/blob/main/AGENTS.md) is the operational entry point: the required workflow for any model change, a decision table for refresh levers, the non-negotiable modeling rules (never a wide `delete+insert`, `insert_overwrite` partition grain must equal the overwrite grain, backfill cumulative chains chronologically), and the short list of ClickHouse gotchas. Scoped `AGENTS.md` files live next to the code they govern (`models/contracts/`, `models/consensus/`, `scripts/full_refresh/`, ...) and carry domain-specific invariants; domains without one follow the root rules.

### Lesson records

Each record under `docs/lessons/` captures one mistake class as a data-quality post-mortem: symptom, root cause, forbidden action, detection, and safe remediation, with evidence references (commits, query results, on-chain verification). Frontmatter carries the machine-readable fields:

| Field | Purpose |
|-------|---------|
| `id` | Stable identifier referenced by hazards and profiles |
| `status` | Lifecycle: `observed` -> `remediated` -> `enforced` |
| `title` | One-line description of the mistake class |
| `symptom` | What you observe when the bug bites |
| `scope` | Which models or patterns the lesson applies to |

The status describes the **deployed** state, never the working tree: production runs the CI-built image from merged `main`, so a fix that exists only locally is at most `observed`. `docs/lessons/INDEX.md` is the catalog -- check it before diagnosing any data-quality symptom.

### Per-model resolved contracts

Every first-party model gets a resolved contract: grain, invariants, known hazards (linked to lesson records with their status inline), lineage blast radius (direct children plus the transitive set of affected `api_` marts), and the safe reprocess runbook. Models are classified high-risk when they are incremental, live under `models/contracts/`, read `{{ this }}` (cumulative), or carry staged `meta.full_refresh` batches -- a changed high-risk model without an explicit contract fails CI.

## How It Is Built

`scripts/agent_context/build_agent_context.py` compiles the artifact from three derived inputs -- nothing is hand-enumerated:

```
target/manifest.json          model configs, lineage, checksums, raw SQL
agent_context/profiles.yml    scope profiles (class rules)
docs/lessons/*.md             lesson records (frontmatter: id/status/title/...)
        |
        v
target/agent_context.json     resolved contracts for every first-party model
```

A model's contract is resolved in layers, most specific last:

1. **Global** -- rules from the `global` block of `profiles.yml` that apply to every model.
2. **Matching profiles, in file order** -- class rules matched against manifest facts (path prefix, materialization, incremental strategy, `{{ this }}` usage, `meta.full_refresh`, tags). Profiles never enumerate model names; membership is resolved from the manifest at build time.
3. **The model's `meta.agent`** -- an explicit per-model contract in `schema.yml`, the highest-priority layer.

List fields (`rules`, `hazards`, `validation`, `invariants`) merge with de-duplication across layers; scalar fields (`grain`, `semantics`, `ground_truth`, `reprocess_runbook`) are overridden by later layers, with `meta.agent` winning. The builder validates every hazard and lesson reference, and its output is deterministic -- CI proves it by building twice and comparing.

!!! note "Public variant"
    The builder also emits a privacy-filtered `agent_context.public.json` that drops models with privacy tags or `meta.expose_to_mcp: false` and never contains raw SQL. Only this variant is published to gh-pages; the full artifact stays local/CI-only.

## How MCP Serves It

Cerebro MCP loads the published artifact and exposes two read-only tools -- they never trigger builds or warehouse mutations:

### `search_dbt_knowledge(query, model_name?, limit?)`

Keyword search over lesson records, ranked by title, symptom, scope, and body, with an exact-phrase boost. Pass `model_name` to boost lessons in that model's hazard list. The top hit returns the full record including detection and safe remediation; querying an exact lesson id returns that record in full.

```
search_dbt_knowledge(query="negative balances", model_name="int_execution_tokens_balances_native_daily")
```

### `get_dbt_change_context(models, task?, lineage_depth?)`

The change packet over MCP: resolved contract, hazards with status, transitive `api_` mart impact, reprocess runbook, and validation commands, plus task-specific guidance (`change`, `backfill`, or `review`).

```
get_dbt_change_context(models="int_consensus_validators_withdrawals_daily", task="backfill")
```

!!! warning "Stale-manifest rule"
    When the live manifest no longer matches the artifact's build input, lesson records are still served (with a warning) -- they describe the repo, not one manifest -- but per-model contract attachments are suppressed until the artifact is rebuilt. A stale contract asserting the wrong grain is worse than none.

## Workflow

### Before changing a model

Call `get_dbt_change_context` **before** changing, backfilling, or reviewing any dbt model. The packet is the contract:

- If the model is flagged **CUMULATIVE** (reads `{{ this }}`), history must be backfilled chronologically before advancing.
- If the incremental strategy is an **expression**, verify which branch a given invocation resolves to before running.
- The listed validation selectors are the definition of done.

When a symptom appears (wipes, duplicates, negative balances, stale snapshots), search the lessons first with `search_dbt_knowledge` -- the mistake class has likely been paid for already. Working directly in the dbt-cerebro checkout, the equivalent is `python scripts/agent_context/context.py --select <model> --task <build|fix|backfill|review>`.

### Adding a lesson record

When you diagnose a new mistake class, capture it so the next session does not repeat the diagnosis:

1. Create a Markdown file under `docs/lessons/` in dbt-cerebro, named after the lesson id (e.g. `staged-insert-overwrite-wipe.md`).
2. Add frontmatter with `id`, `status`, `title`, `symptom`, `scope`, and `evidence` refs, then the body sections: symptom, root cause, forbidden action, detection, safe remediation.
3. Add the lesson to `docs/lessons/INDEX.md` under the appropriate category, and wire it as a hazard (in a `profiles.yml` profile or a model's `meta.agent`).
4. Rebuild the artifact (`python scripts/agent_context/build_agent_context.py`) -- it validates every reference.

A lesson without evidence is a rumor. The full procedure, including the evidence requirements, is in dbt-cerebro's [incident workflow](https://github.com/gnosischain/dbt-cerebro/blob/main/docs/workflows/incident.md); the architecture of the whole system is documented in [docs/agents.md](https://github.com/gnosischain/dbt-cerebro/blob/main/docs/agents.md).

## See Also

- [MCP Tools Reference](../mcp/tools.md) -- the full Cerebro MCP tool catalog, including the two knowledge tools
- [Adding dbt Models](add-model.md) -- creating models that these contracts describe
- [Conventions](conventions.md) -- naming, tagging, and testing standards
