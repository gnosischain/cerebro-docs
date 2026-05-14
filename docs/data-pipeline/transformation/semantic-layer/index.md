# Semantic Layer

The semantic layer is the *metric-and-relationship registry* on top of the
dbt warehouse. It is the surface every non-SQL consumer of Gnosis Analytics
talks to: AI chat agents, dashboards, BI tools, and any downstream caller
that needs a stable, named contract rather than a SQL query against a
specific table.

This section explains **what the semantic layer is, what it isn't, and
when to use it**. Subsequent pages dive into each component.

## What's in the box

The "semantic layer" bundles five distinct things — each with its own ROI
profile. Knowing which one you're touching matters.

| Component | What it is | Files | Audience |
| --- | --- | --- | --- |
| **User-keyed marts** | Per-user-pseudonym projections of each sector (revenue, gpay, gnosis_app, circles). Stable contracts for cross-sector overlap. | `models/**/fct_*_users_distinct.sql`, `fct_revenue_per_user_*.sql` | Anyone running cross-sector analytics. |
| **Time spines** | `dim_time_spine_{daily,weekly,monthly}` reference dimensions. The Monday-anchored join axis for time-series cross-sector composition. | `models/shared/marts/dim_time_spine_*.sql` | Anyone composing metrics across grains. |
| **Schema docs** | Column-level descriptions on every analyst-facing api_ / fct_ model. Powers `describe_table` and `get_model_details` in the MCP. | `models/**/schema.yml` | LLMs, analysts navigating the model space. |
| **Semantic models** | `semantic_models:` blocks in `semantic/authoring/`. Declare which dimensions and measures a model exposes, plus its `quality_tier` and `question_synonyms`. | `semantic/authoring/<module>/semantic_models.yml` | The `discover_metrics` and `query_metrics` MCP tools. |
| **Metric registry** | Named metrics (e.g. `cow_volume_usd`, `revenue_active_users_weekly`) bound to measures. Compiled into `target/semantic_registry.json`. | `semantic/authoring/<module>/semantic_models.yml` (the `metrics:` block); build script `scripts/semantic/build_registry.py` | AI agents, dashboard tools, anyone calling `query_metrics`. |

The first three are **infrastructure** — small, durable, broadly useful.
The last two are **interfaces** — only worth their weight when there's
something querying them.

## Why we built it

Three concrete pain points motivated the work, in priority order:

1.  **Cross-sector user analysis is hard without standardization.** Pre-
    semantic-layer, asking "how many revenue-active users hold a Gnosis
    Pay Safe?" required hand-joining intermediates and re-applying
    `pseudonymize_address()` correctly each time. The user-keyed marts
    make this a one-line `INNER JOIN ... USING (user_pseudonym)`.
2.  **AI agents and dashboards need a stable, named contract.** When the
    underlying mart is renamed or its columns change, downstream
    consumers shouldn't break. A metric ID like `cow_volume_usd` is the
    contract. The mart can move; the metric persists.
3.  **Cross-grain composition was lossy.** Monday-vs-Sunday week
    anchoring, day-vs-week-vs-month aggregation conventions — these
    diverged across modules and bit analysts silently. The time spines
    and the planner-side upcast logic (see [time spines](time-spines.md))
    fix this.

## Who actually uses it (honest audience breakdown)

| Audience | Primary tool | Semantic-layer ROI |
| --- | --- | --- |
| **SQL-fluent analyst writing a one-off report** | `execute_query` (raw SQL via the MCP) | ~20% — the marts help; the metric registry is bypassed for ad-hoc work. |
| **AI chat agent answering analytics questions** | `discover_metrics` → `query_metrics` | ~80% — can't easily compose raw SQL across 1000+ dbt models. Metric names and `question_synonyms` are essential. |
| **Dashboard / BI tool consumers** | Stable metric IDs (`cow_volume_usd`, etc.) | ~90% — needs the contract more than the SQL. |

Most teams underestimate that the registry's value is **concentrated in
the second and third audiences**. If you're a power analyst writing a
report, expect to use it lightly. The metric registry shines in
downstream consumers — every dashboard that renders `revenue_active_users_weekly`
benefits from the stable name + the underlying maintenance discipline.

## Structure of this section

- **[Architecture](architecture.md)** — file layout, naming conventions,
  what the registry-build does, and how `semantic/authoring/`,
  `semantic/relationships/`, and `target/semantic_registry.json` fit
  together.
- **[User-pseudonym graph](user-pseudonym-graph.md)** — cross-sector user
  overlap analysis. The 5-node graph (revenue × gpay × gnosis_app × circles
  × ...) and how to compose joins through it.
- **[Time spines](time-spines.md)** — cross-grain composition. How
  `dim_time_spine_{daily,weekly,monthly}` enable daily metrics to compose
  with weekly metrics and beyond.
- **[Metric registry](metric-registry.md)** — `discover_metrics`,
  `query_metrics`, quality tiers, the `allow_candidate` opt-in, and the
  scalar-KPI distinction.
- **[Maintenance](maintenance.md)** — the invariants that keep the
  registry trustworthy, the drift modes you'll hit, and the
  authoring checklist for new metrics.
- **[Cross-sector examples](cross-sector-examples.md)** — three worked
  examples (cow × lending × revenue weekly overlay, Gnosis App on-chain
  vs web parity, 4-way user-pseudonym intersection).
- **[Semantic graph](graph.md)** — auto-generated Mermaid diagram of the
  current cross-sector graph, regenerated by
  `scripts/semantic/generate_graph_diagram.py`.

## Related reading

- **[Privacy & Pseudonyms](../privacy-pseudonyms.md)** — the
  `pseudonymize_address` macro and `CEREBRO_PII_SALT` are the foundation
  of every `user_pseudonym` join in the semantic layer.
- **[Model Layers](../model-layers.md)** — where the user-keyed marts
  fit (always `fct_` / `api_` mart-tier).
- **[meta.api Contract](../../../developer/meta-api-contract.md)** —
  the related contract for cerebro-api exposure. `meta.api.exclude_from_api`
  and `expose_to_mcp` are *not* the same gate as the semantic-layer
  `quality_tier`; see [maintenance](maintenance.md#privacy-gates).
