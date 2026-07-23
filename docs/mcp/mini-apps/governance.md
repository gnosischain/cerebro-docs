# Governance Explorer

Read-only analyst surface over the `governance_db` ClickHouse database: GnosisDAO Snapshot proposals, votes, voters, and followers plus the Discourse forum (topics, posts, contributors, categories), cross-linked between the two sources.

- **Resource URI:** `ui://cerebro/governance`
- **Entry tool:** `open_governance(section?, query?, entity_type?, identifier?)`
- **Backed by:** `src/cerebro_mcp/tools/visualization/governance_explorer.py`, reading `governance_db` (ingested daily by [click-runner](../../data-pipeline/ingestion/click-runner.md))

!!! warning "Everything here is off-chain signaling"
    Every dataset in this app is **Snapshot off-chain signaling and forum activity — never binding on-chain execution**. A passed proposal is a signal, not an executed transaction. There is no treasury, execution, or delegation data in v1. Each dataset carries a provenance label ("Snapshot off-chain signaling", "Forum activity", or "Snapshot signaling + forum activity") so the plane is always disclosed.

## What it is

Four sections plus entity drill-downs:

| Section | Focus |
|---|---|
| `overview` | Space summary, source freshness, governance activity, proposal types, quorum distribution, voting-power concentration, latest activity, forum category activity |
| `proposals` | Filterable proposal list + creation activity |
| `voters` | Voter leaderboard, concentration, activity |
| `forum` | Categories, topics, contributor leaderboard, posting activity |

Entity drill-downs exist for `proposal` (detail, choices, votes, forum links), `voter` (profile, votes, participation), `forum_topic` (detail, posts, proposal links), and `forum_user` (profile, posts, activity).

### Proposal ↔ forum-topic linking is two-tier, never fuzzy

Cross-source links between a Snapshot proposal and its forum discussion are resolved by exactly two tiers:

1. **Primary — the author-declared `discussion` URL.** The topic id is extracted from the proposal's discussion link (`forum.gnosis.io/t/<slug>/<id>`), reported as `link_source = 'discussion'`.
2. **Secondary — exact GIP-number equality.** A shared `GIP-N` number extracted with one regex (word boundary before `GIP`, so `AGIP-5` never matches), reported as `link_source = 'gip'`.

There are no fuzzy or free-text joins, ever. A proposal without a discussion URL or a GIP number simply has no forum link.

### Consistent reads: FINAL everywhere

All eight `governance_db` tables are `ReplacingMergeTree(ingested_at)`, and the daily ingesters routinely re-insert rows (all proposals, the whole user directory, every bumped topic with all its posts). Un-merged duplicates would double-count aggregates, so **every table read in this app uses `FINAL`** — no carve-outs, enforced by a lexical test in the module.

## When to use it

- "What proposals are active / recently closed, and did they meet quorum?"
- Voter analysis: leaderboard, voting-power concentration, participation over time.
- Forum health: category activity, top contributors, topic engagement.
- Tracing a GIP from forum discussion to Snapshot vote (or the reverse).
- Drilling into one proposal, voter address, topic, or forum contributor.

Quorum is described as **met / missed / unspecified** (proposals with no quorum set), never pass/fail language.

## How to open it

```text
open_governance()                                # overview
open_governance(section="proposals")
open_governance(query="GIP-121")                 # resolve a GIP, id, address, or title text
open_governance(entity_type="voter", identifier="0xabc…")
```

- `section` — `overview` (default), `proposals`, `voters`, or `forum`.
- `query` — resolves a proposal id (`0x…64`), voter address, GIP number, topic/user id, or title text. A single match deep-links to the entity; multiple matches render a candidate list.
- `entity_type` + `identifier` — direct entity load (`proposal`, `voter`, `forum_topic`, `forum_user`); must be provided together.

The default open path runs **zero ClickHouse queries** — every dataset group is deferred and streamed by the frontend through `load_governance_datasets`.

### Time ranges: the `start_at` token encoding

Section loads have **no `window_days` parameter**. The range is encoded entirely in `start_at` / `end_at`:

| `start_at` | `end_at` | Meaning |
|---|---|---|
| `""` | `""` | All history |
| `"90d"` or `"1y"` | must be empty | Relative preset anchored to `now()` UTC |
| ISO-8601 timestamp | ISO-8601 timestamp | Custom range (both required; `start_at` must be earlier than `end_at`) |

Start-only or end-only custom ranges are rejected, as is a preset with a non-empty `end_at`. Tokens are stored verbatim so the scope fingerprint stays deterministic and presets survive a zero-query tab return. For proposals, a range matches when the proposal's `[start_at, end_at]` voting window *intersects* the requested range, not just when it was created inside it.

## Tool reference

`open_governance` is the only agent-visible tool. The other four are registered with `APP_ONLY_META` and marked `app_only` — called by the React frontend, hidden from the model-facing tool list.

### Entry point (agent-visible)

| Tool | Purpose | Key parameters |
|---|---|---|
| `open_governance` | Open the explorer on a section, search result, or entity | `section`, `query`, `entity_type`, `identifier` |

### App-internal loaders

| Tool | Purpose | Key parameters |
|---|---|---|
| `load_governance_section` | Atomically load one section with its filter scope | `view_id`, `request_id`, `section`, `query`, `start_at`, `end_at`, `proposal_state`, `proposal_type`, `quorum_status`, `category_id`, `forum_status`, `sort_by`, `force_refresh` |
| `load_governance_datasets` | Load one deferred dataset group (additive) | `view_id`, `request_id`, `section`, `group`, `scope_id`, `force_refresh` |
| `search_governance` | Resolve a proposal, voter, GIP, topic, or contributor | `view_id`, `request_id`, `query` |
| `load_governance_entity` | Load a resolved entity bundle | `view_id`, `request_id`, `entity_type`, `identifier` |

Filter vocabularies (validated before any SQL): `proposal_state` ∈ active/pending/closed; `proposal_type` ∈ the full Snapshot voting-system set (basic, single-choice, approval, ranked-choice, quadratic, weighted); `quorum_status` ∈ met/missed/unspecified; `forum_status` ∈ open/closed/archived. Sorts are per-section whitelists mapping to fixed `ORDER BY` fragments.

## Best practices

- **Lead with the provenance label** when reporting numbers — "Snapshot signaling" vs "forum activity" is a meaningful distinction to a governance audience.
- **Use `query` with a GIP number** (`GIP-121`, `gip 121`) — it resolves across both sources via the same regex the SQL uses.
- **Prefer presets** (`"90d"` / `"1y"`) over hand-built ISO ranges when the user asks for "recent" activity; all-history is the empty-token default.

## Pitfalls

- **Reading vote outcomes as execution.** Nothing in this app is binding; do not phrase results as "the DAO did X" based on a Snapshot vote alone.
- **Expecting delegation or treasury data.** Not in v1.
- **Inventing links between proposals and topics.** If neither the discussion URL nor an exact GIP number matches, there is no link — do not bridge the gap editorially.
- **Mixing the token grammar.** `start_at="90d"` with a non-empty `end_at` is rejected, as is a lone ISO `start_at`.

## See also

- [Mini-Apps overview](index.md)
- [click-runner](../../data-pipeline/ingestion/click-runner.md) — the ingestion service that populates `governance_db`
- [CoW Explorer](cow-explorer.md) — sibling read-only explorer over `cow_db`
