# Maintenance & invariants

The semantic-layer registry is a stable contract that downstream
consumers (AI agents, dashboards, BI tools) rely on. Keeping that
contract honest requires disciplined authoring and an understanding of
the invariants the build enforces — and the ones it doesn't.

This page is the operational playbook.

## The five invariants

These hold across the project. Breaking any one is a bug.

### 1. Measure names are globally unique

Every `name:` under a `measures:` block must be unique across the
entire `semantic/authoring/` tree. The build collects all measure names
into a `measure_name → [model_names]` map; when a metric's
`type_params.measure` resolves to two or more models, the binding is
ambiguous and the validator emits `ambiguous_measure_binding`.

Convention: `<column>_value`, or `<semantic_model_name>__<measure>`
when that collides. Two same-named measures across semantic_models is
only a build error *once a metric references them*
(`ambiguous_measure_binding`).

The build picks a deterministic winner (`sorted(candidates)[0]`) so
the registry is reproducible even when collisions exist. But the
validator will flag every *bound* collision as an error if you run with
`--validate`.

**Let the scaffolder enforce this.**
`scripts/semantic/scaffold_metrics.py` is the source of truth for
measure uniqueness: it rewrites only the collided names to
`<semantic_model_name>__<measure>` (already-unique names — including
every name an existing metric binds to — are left untouched, so churn
is minimal) and emits one candidate metric per eligible measure. The
result is the property that makes "a metric for every measure" possible
in the first place: no measure is left without a globally-unique name
and a metric. Re-run it whenever you add measures (`--target-dir target
--write`) rather than hand-editing the `metrics:` block.

### 2. Root semantic_model's `quality_tier` matches the metric's

If a metric is `approved` but its root semantic_model is `candidate`,
the metric appears in the registry but **fails at execution time**:
`_metric_is_executable` checks both. Common gotcha when authors
promote a metric without realising the root model also needs
promotion.

Promotion sequence:
1. Set the semantic_model's `config.meta.cerebro.quality_tier:
   approved`.
2. Set every metric pointing at it to `approved` as well.
3. Validate that `target/semantic_registry.json` shows both as
   approved and the metric resolves to an `approved` root.

### 3. Monday-anchored weeks everywhere

`dim_time_spine_weekly` uses `toMonday(day)`. Every weekly mart must
use `toStartOfWeek(date, 1)` or `toMonday(date)` to match. Bare
`toStartOfWeek(date)` (default Sunday) silently produces misaligned
data; cross-sector composition through `dim_time_spine_weekly` will
join the wrong 7-day windows.

This invariant is not yet enforced by validation. Adding a check that
scans every `*_weekly.sql` for `toStartOfWeek(*, *)` without `, 1` is
on the open-improvements list.

### 4. `user_pseudonym` hash space is project-wide

The `pseudonymize_address` macro hashes lowercased addresses with a
secret `CEREBRO_PII_SALT`. Every model that joins on `user_pseudonym`
implicitly trusts that this salt has been stable forever. Rotating
the salt is *theoretically possible* but *practically catastrophic*:
every materialised pseudonym in every mart would need a full refresh,
and every relationship in the user-pseudonym graph would point at
mismatched IDs in the interim.

Authoring rules:
- Never call `sipHash64(...)` directly on an address — always go
  through `{{ pseudonymize_address('col') }}`.
- Never store raw addresses in a model that also stores
  `user_pseudonym`. (Use the identity-bridge pattern: raw + pseudonym
  in an internal-only mart, with a pseudonym-only mart-tier
  projection.)
- See [Privacy & Pseudonyms](../privacy-pseudonyms.md).

### 5. Relationships only reference materialised models

A relationship in `semantic/relationships/*.yml` is a CI-checked claim
that both `left_model` and `right_model` exist in `target/manifest.json`.
Renaming a dbt model without updating its relationship references
emits `unknown_left_model` / `unknown_right_model` errors.

This is why relationships are kept in `semantic/relationships/` rather
than scattered inside individual `semantic_models.yml` blocks — they
need a holistic refresh whenever models are renamed.

## Privacy gates

The semantic-layer `quality_tier` is **NOT** the same as the
cerebro-api `exclude_from_api` flag or the MCP `expose_to_mcp` flag.
These are three independent gates:

| Gate | Where | What it blocks |
| --- | --- | --- |
| `quality_tier: blocked` | `semantic_models.yml` | The metric never enters the registry. Both `discover_metrics` and `query_metrics` can't reach it. |
| `meta.expose_to_mcp: false` | `models/**/schema.yml` (or `dbt_project.yml`) | The MCP `execute_query` tool refuses to query this model directly. Raw SQL access is blocked. |
| `meta.api.exclude_from_api: true` | `models/**/schema.yml` (or `dbt_project.yml`) | cerebro-api refuses to expose the model as a REST endpoint. |

The Mixpanel privacy policy uses all three together:

- **All** Mixpanel marts: `meta.api.exclude_from_api: true` — no cerebro-api exposure.
- **Per-user grain** (`api_mixpanel_ga_users_daily`): also
  `meta.expose_to_mcp: false` AND not registered in
  `semantic/authoring/mixpanel_ga/semantic_models.yml` — completely
  invisible to MCP consumers.
- **Aggregate Mixpanel views** (overview, modals, funnel, etc.):
  MCP-accessible, registered as `quality_tier: approved` for the few
  promoted entries.

See [Privacy & Pseudonyms](../privacy-pseudonyms.md) for the full
policy.

## Authoring checklist

When adding a new metric:

- [ ] dbt model exists and is materialised. `dbt build --select <model>`
      passes.
- [ ] Schema doc in `models/<module>/marts/schema.yml` covers every
      column the metric will surface.
- [ ] Semantic_model entry in `semantic/authoring/<module>/semantic_models.yml`:
    - [ ] `model: ref('<the_dbt_model>')` matches an actual model
    - [ ] Dimensions enumerated (every column the metric exposes for
          grouping or filtering)
    - [ ] Measures have **globally-unique names** (convention:
          `<metric_name>_value`)
    - [ ] `config.meta.cerebro.quality_tier` matches the intended
          metric tier (or is `candidate` if you're still iterating)
    - [ ] `question_synonyms` populated — these drive
          `discover_metrics`
- [ ] Metric entry in the same file's `metrics:` block:
    - [ ] `type_params.measure` matches one of the measure names you
          declared
    - [ ] `allowed_dimensions` enumerates every dimension a caller may
          pass
    - [ ] `supported_time_grains` lists the natural time grains
          (`day`, `week`, `month` typically)
    - [ ] `quality_tier` matches the root semantic_model's tier
- [ ] If cross-sector: relationship declared in
      `semantic/relationships/*.yml` (`user_pseudonym.yml`,
      `time_spines.yml`, or `execution_graph.yml`)
- [ ] Build + validate:
      ```bash
      python3 scripts/semantic/build_registry.py --target-dir target --validate
      ```
      Zero `error_count` for the new metric.
- [ ] Force-reload the MCP runtime cache:
      ```python
      mcp__cerebro-dev__reload_semantic_registry()
      ```
- [ ] Sanity-check via `discover_metrics` and `query_metrics`.

## Promotion checklist (candidate → approved) { #promotion-checklist }

- [ ] Underlying SQL is stable; no known data-quality issues open.
- [ ] Column types are stable (no in-flight migration).
- [ ] Cross-sector relationships referencing this metric's root are
      approved (`quality_tier: approved`).
- [ ] Real-world test query via `query_metrics` returns sensible data.
- [ ] If this metric will be composed cross-grain: time-spine
      relationship in place.
- [ ] Documentation updated — at minimum a 1-line description on the
      metric, ideally a short paragraph on the dbt model's
      `description` field.
- [ ] Flip `quality_tier: candidate` → `approved` on **both** the
      semantic_model and the metric. Rebuild + reload.
- [ ] Verify with `discover_metrics`: the metric shows up.
- [ ] Verify with `query_metrics`: real data comes back (no
      "not approved" error).

## Drift modes — what to watch for

| Drift mode | How it presents | Mitigation |
| --- | --- | --- |
| Measure-name collision | New metric resolves to wrong root_model; `discover_metrics` returns confusing scores. | `validate_registry` catches at build time. Re-run `scaffold_metrics.py` to uniquify + (re)bind. |
| Root semantic_model still candidate | Metric appears in `discover_metrics` but `query_metrics` rejects with "not approved". | Promotion checklist above — promote both. |
| Week-anchor outlier | Cross-sector joins return misaligned rows; counts look weirdly low. | Audit `*_weekly.sql` for bare `toStartOfWeek(date)`. CI check pending. |
| Renamed dbt model | `unknown_left_model` validation error. | Update every `semantic/relationships/*.yml` that referenced the old name. |
| Stale registry on MCP side | `query_metrics` returns "metric not found" or pre-promotion state. | Call `reload_semantic_registry`. The force path now reloads all four artifacts (registry + docs + manifest + catalog) atomically, so a single call clears a post-deploy `manifest_hash_mismatch` and the first query after a deploy self-heals. If still stale, check CDN cache headers on the GitHub Pages publish, and confirm the MCP isn't pinned to a stale local artifact path. |
| Salt rotation (hypothetical) | All `user_pseudonym` joins return empty. | **Don't rotate.** If absolutely necessary, full refresh of every pseudonymized mart in a single transaction. |

## Ongoing-maintenance time budget

Realistic projection based on the current shape (~1,037 metrics — ~72
approved, ~965 auto-generated candidates — 51 relationships, ~1,095
semantic-mapped models):

- **New cross-sector metric**: 30 min (write YAML + validate + smoke
  test).
- **New user-keyed mart**: 1-2 h (write SQL + schema doc + semantic_model
  + relationships + build/test cycle).
- **Renaming a dbt model**: 15-30 min depending on how many
  relationships reference it.
- **Failed validation in CI**: 5-15 min to fix per error code (most are
  YAML typos or stale references).
- **MCP planner bug surfacing in production**: variable; expect 1-4 h
  including PR review on cerebro-mcp.

**Recurring time**: ~1-2 hours / month if the team scopes properly —
i.e. doesn't register every new mart, only the analyst-facing ones.

## Tooling

| Tool | Purpose | Where |
| --- | --- | --- |
| `scripts/semantic/build_registry.py` | Compile `semantic/authoring/` + dbt artifacts into `target/semantic_registry.json`. | dbt-cerebro |
| `scripts/semantic/build_registry.py --validate` | Add invariant checks (measure uniqueness, missing measures, unknown relationship models, etc.). | dbt-cerebro |
| `scripts/semantic/build_semantic_docs.py` | Generate `semantic_docs_index.json` for MCP's `gnosis://semantic-model/{name}` resource. | dbt-cerebro |
| `scripts/semantic/scaffold_candidates.py` | Auto-generate candidate `semantic_models` from new dbt models (rough starting point only — review before committing). | dbt-cerebro |
| `scripts/semantic/scaffold_metrics.py` | Uniquify collided measure names and emit one candidate metric per eligible measure across all domains. Idempotent; re-run after adding measures. Skips blocked/internal/`expose_to_mcp: false` models and id-like measures. | dbt-cerebro |
| `scripts/semantic/generate_graph_diagram.py` | Auto-generate [graph.md](graph.md) (static Mermaid) **and** the `graph_data.json` sidecar that powers the interactive cytoscape explorer. | dbt-cerebro |
| `mcp__cerebro-dev__reload_semantic_registry` | Force MCP runtime refresh, bypassing the 300s poll. | cerebro-mcp MCP tool |
| `tests/test_semantic_registry.py` | pytest suite for `build_registry.py` + validation. | dbt-cerebro |

## Open improvements (CI / tooling) { #open-improvements-ci-tooling }

Tracked here so authoring debt stays visible:

1. **Week-anchor enforcement** — scan every `*_weekly.sql` for
   `toStartOfWeek(*)` without explicit `, 1` mode. Currently a
   convention; should be a build check.
2. **Hash-space rotation guard** — alert if `CEREBRO_PII_SALT` is set
   to a different value than the one used by any existing
   pseudonymized mart. Currently nothing prevents an accidental
   rotation in a non-prod environment.
3. **Auto-published `graph.md`** — partly done. The generator now emits
   both the static Mermaid `graph.md` and the `graph_data.json` sidecar
   behind the interactive cytoscape explorer. Remaining: wire
   `scripts/semantic/generate_graph_diagram.py` into the registry-build
   CI step (with `--json-output`) so both stay current automatically.
4. **Cross-grain enforcement** — flag a metric in `discover_metrics`
   results when its `supported_time_grains` declare a grain that's not
   reachable from its root model (i.e. no spine bridge or upcast
   template exists). Currently surfaces as a runtime error.
5. **Set-intersection metric type** — planner enhancement to support
   `query_metrics([userX_metric, userY_metric])` with no shared
   dimensions, returning intersection cardinalities. Today this is a
   raw-query pattern.
