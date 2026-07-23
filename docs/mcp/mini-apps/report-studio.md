# Report Studio

Browse, preview, and manage the report archive, and compose new dashboard reports from recent chart records — without going through the agent's report pipeline.

- **Resource URI:** `ui://cerebro/report_studio`
- **Entry tool:** `open_report_studio(query?, kind?, report?)`
- **Backed by:** `src/cerebro_mcp/tools/visualization/report_studio.py`, over the flat HTML files in `CEREBRO_REPORT_DIR` (default `~/.cerebro/reports`)

## What it is

Report Studio is the management surface for the reports the [Report Renderer](../reports.md) produces. The relationship is deliberate:

- **Report Renderer** (`generate_report`, `generate_research_report`, `generate_case_study_report`) *generates* reports — agent-driven, with the full [quality-gate](../advanced/quality-gates.md) enforcement.
- **Report Studio** *manages and composes* — it lists the archive, previews any report natively in-app, renames and deletes entries, and lets a human assemble a new report from existing chart records, with the agent quality gates bypassed by construction (chart existence and layout rules still apply).

The archive's source of truth is the flat HTML files in the report directory. The gallery lists filename-derived metadata only (id, kind, size, mtime, a lossy title hint) — cheap, no multi-MB HTML reads. Opening an entry extracts the embedded `<script id="report-data">` payload for a native preview: title, charts as ECharts options, sections HTML, and the queries behind each chart. Reports created in the composer also carry their raw composition inputs, enabling "Duplicate to composer"; agent-generated reports do not.

!!! warning "Trust model: gate mutations on shared deployments"
    Report files and the chart-record registry are **process-global with no per-user owner**. Mutations (delete / rename / compose / studio chart creation) *and* chart-record reads are gated by `REPORT_STUDIO_ALLOW_MUTATIONS` — on shared SSE deployments this should be **off**, leaving Report Studio a read-only archive browser. When disabled, the composer surface is omitted from the UI entirely and every gated tool returns an explanatory error.

## When to use it

- "Show me my reports" / "what did we generate last week?" — interactive archive browsing.
- Re-opening a past report with its charts and queries, without regenerating anything.
- Renaming or deleting archive entries.
- Human-driven composition: picking from recent chart records (server-wide registry, 2-hour TTL) and arranging them with markdown into a new report, research essay, or case study.

For agent-driven report generation with quality gates, use the generators on the [Reports](../reports.md) page. `list_reports()` / `open_report(id)` remain the lightweight non-interactive alternatives.

## How to open it

```text
open_report_studio()                       # archive gallery
open_report_studio(query="gnosis pay")     # filtered archive (matches filename slug/id)
open_report_studio(kind="research")        # report | research | case_study
open_report_studio(report="a1b2c3d4")      # straight into a preview (UUID or 8+ hex prefix)
```

## Walkthrough: compose a report

With mutations enabled, the composer flow inside the app is:

1. **Pick charts.** The composer lists recent chart records (without their heavy ECharts options; thumbnails hydrate lazily per chart). Records come from the same server-wide registry the agent's `generate_charts` fills, and expire after 2 hours.
2. **Optionally create a chart in-app.** The studio chart form runs SELECT/WITH-only SQL through the full ClickHouse guard stack (allowed databases, readonly session) and registers the result as a new chart record.
3. **Arrange sections.** A composition is an ordered list of sections, each *exactly one of* `{"markdown": "..."}` or `{"charts": ["chart_1", ...]}`. Limits: 40 sections, 20,000 chars of markdown per section, 30 charts per report.
4. **Compose.** Three kinds map to the three renderer layouts — dashboard report (optional subtitle and up to 12 summary numbers; KPI `numberDisplay` charts are auto-arranged into `{{grid:N}}` blocks), research essay (`deck` up to 240 chars, 3-6 `key_takeaways`, authored `{{figure}}` / `{{pullquote}}` / `{{callout}}` directives pass through), and case study (`deck`, 3-6 `key_points`, optional hero chart and CTA, `{{scene}}` / `{{step}}` / `{{reveal}}` directives pass through).

The composed file lands in the same archive, indistinguishable from generated reports apart from its stored composition inputs. Export/conversion (docx / pdf / pptx) stays agent-side: the export panel surfaces a copyable path plus a hint to ask the agent for `export_report`.

## Tool reference

`open_report_studio` is the only agent-visible tool. The other eleven are registered with `APP_ONLY_META` and marked `app_only` — called by the React frontend, hidden from the model-facing tool list. Tools marked *gated* additionally require `REPORT_STUDIO_ALLOW_MUTATIONS=true`.

### Entry point (agent-visible)

| Tool | Purpose | Key parameters |
|---|---|---|
| `open_report_studio` | Open the studio on the archive or straight into a preview | `query`, `kind` (report / research / case_study), `report` (UUID or 8+ hex prefix) |

### App-internal: archive reads

| Tool | Purpose | Key parameters |
|---|---|---|
| `list_report_archive` | Page of the archive (filename metadata only) | `query`, `kind`, `sort` (newest / oldest / title), `offset`, `limit` (max 200) |
| `get_report_archive_entry` | Full structured payload of one report for the native preview | `report_ref` |
| `get_report_export_info` | Paths / download URL for exporting; conversion itself is agent-side | `report_ref` |

### App-internal: mutations (gated)

| Tool | Purpose | Key parameters |
|---|---|---|
| `delete_report_archive_entry` | Delete a report file — two-step confirm (first call returns the full id + filename for the dialog) | `report_ref`, `confirm` |
| `rename_report_archive_entry` | Retitle: rewrites the embedded report-data title and the filename slug atomically; UUID and mtime preserved | `report_ref`, `title` (max 200 chars) |

### App-internal: composer (gated, including reads)

| Tool | Purpose | Key parameters |
|---|---|---|
| `list_session_charts` | Recent chart records without heavy ECharts options | — |
| `get_session_chart` | One chart record including its ECharts option | `chart_id` |
| `create_studio_chart` | Run SQL and register a chart record for the composer | `sql` (SELECT/WITH only), `chart_type`, `x_field`, `y_field`, `series_field`, `change_field`, `title`, `database` (default `dbt`), `max_rows` (default 500) |
| `compose_report` | Assemble a dashboard report | `title`, `sections`, `subtitle`, `summary_numbers` (max 12) |
| `compose_research_report` | Assemble a long-form research essay | `title`, `deck`, `sections`, `key_takeaways` (3-6), `authors`, `category`, `footnotes` |
| `compose_case_study_report` | Assemble a scrollytelling case study | `title`, `deck`, `sections`, `key_points` (3-6), `authors`, `category`, `hero_chart_id`, `cta` |

All three composers validate every chart id against the live registry before writing anything — expired or unknown ids are rejected with the list of currently available ids.

## Best practices

- **Compose soon after charting.** Chart records expire 2 hours after creation; a composition referencing an expired id fails validation up front rather than producing a broken report.
- **Batch KPIs.** In dashboard compositions, two or more `numberDisplay` charts are automatically gathered into grid blocks (sizes 2-4); putting related KPIs in the same section keeps them in one row.
- **Treat the archive as append-mostly.** Rename preserves the report UUID, so existing links keep resolving; delete is the only destructive operation and requires the two-step confirm.

## Pitfalls

- **Expecting the studio on shared servers.** With `REPORT_STUDIO_ALLOW_MUTATIONS=false` (the right setting for shared SSE deployments), the composer and chart-record tools are disabled and only archive browsing works.
- **Searching by full title.** Archive search matches the filename slug, filename, and id — titles in the gallery are lossy filename hints; the full title only arrives with the preview.
- **Assuming composed reports passed the quality gates.** They did not — human-composed reports bypass the agent gates by construction. Do not cite them as gate-compliant analysis.
- **Manually editing files in `CEREBRO_REPORT_DIR`.** Only managed report files are listed and mutated; hand-renamed or foreign files may stop resolving.

## See also

- [Reports](../reports.md) — the Report Renderer: agent-driven generation, quality gates, `export_report`
- [Mini-Apps overview](index.md)
- [Metric Lab](metric-lab.md) — prototyping the charts that become composer inputs
