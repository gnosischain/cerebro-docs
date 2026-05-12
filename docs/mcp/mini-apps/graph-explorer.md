# Graph Explorer

Cross-sector force graph of every graph-capable semantic model in dbt-cerebro. Trust relations, ownership, LP positions, validator control, bridge flows — all in one canvas.

## What it is

Graph Explorer renders an ECharts force graph centered on a seed (typically an EVM address). Nodes come from the semantic registry; edges are fetched per query. Every graph-capable dbt model contributes a **profile**; chip toggles on the strip below the graph let you mix profiles in/out.

Resource URI: `ui://cerebro/graph_explorer`.

## When to use it

- "Who owns this Safe and what else do they control?"
- "Which validators are funded by which deposit address?"
- "Which DEX pools share LPs with this one?"
- Sector-spanning investigations (Circles + Safe + GPay + DeFi all on one canvas).

## Two screens

1. **Catalog (empty state)** — lists every profile by sector. Primary action: paste an EVM address; the backend auto-detects which profiles apply via `int_execution_address_roles_current`.
2. **Graph screen** — force-directed canvas with topbar (window, max neighbors, layout), chip strip (per-profile toggles), and side panel (node metadata, role badges, semantic provenance, suggested next hops).

## Step-by-step tutorial

### 1. Seed from an address

```text
open_graph_explorer()
load_graph_explorer_seed(address="0xabc…")
# Auto-detects roles, picks default profiles, renders 1-hop subgraph.
```

### 2. Expand a node

```text
expand_graph_explorer_node(node_id="address:0xdef…")
# One additional hop, capped at MAX_HOPS = 5.
```

### 3. Update focus

```text
update_graph_explorer_focus(
  window_days=30,
  max_neighbors=50,
  layout="circle",                 # or "force"
  status_filter="approved",        # or "candidate" / "all"
  active_profiles=["circles_trust", "lp_in_pool", "lending_user_to_reserve"],
)
```

## Tool reference

| Tool | Purpose |
|---|---|
| `open_graph_explorer()` | Open the panel (catalog screen if no seed) |
| `load_graph_explorer_seed(address)` | Seed the graph on an address |
| `expand_graph_explorer_node(node_id)` | One-hop expansion (cap MAX_HOPS=5) |
| `update_graph_explorer_focus(...)` | Window, neighbors, layout, status filter, profiles |

## Profiles (initial release)

| Profile | Source → Target | Quality |
|---|---|---|
| `circles_trust` | circles_avatar → circles_avatar | approved |
| `circles_trust_history` | circles_avatar → circles_avatar | candidate |
| `circles_avatar_balances` | circles_avatar → token | approved |
| `safe_ownership` | address → safe | candidate |
| `gpay_ownership` | address → gpay_wallet | candidate |
| `token_transfers` | address → address | candidate |
| `lp_in_pool` | address → pool | approved |
| `pool_contains_token` | pool → token | approved |
| `lending_user_to_reserve` | address → token | approved |
| `validator_controlled_by` | address → validator | approved |
| `deposit_to_validator` | address → validator | approved |
| `bridge_user_flows` | address → bridge | candidate |
| `address_labeled_as` | address → project_label | approved |

## Cross-sector relationships

These edges drive the "suggested next hops" chips in the side panel:

- `gpay_wallet_is_safe` — GPay Safes are Safes.
- `ga_user_controls_gpay` — **canonical** EOA → GP Safe binding via the Delay Module. **Do NOT** use `safes_current_owners.owner` (returns sentinel `0x…0002`).
- `circles_avatar_is_address` — avatars are addresses.
- `deposit_to_validator_identity` — `withdrawal_credentials` joins GBCDeposit and consensus.
- `validator_address_is_safe` — the 20-byte withdrawal address is often a Safe.
- `address_labeled_as_project` — universal Dune-label enrichment.

## Worked example

```text
# Triaging a suspicious deposit address
> open_graph_explorer()
> load_graph_explorer_seed(address="0xdep…")
< 1-hop subgraph: 12 validators funded, 3 token transfers, 1 Safe ownership

> expand_graph_explorer_node(node_id="safe:0xs…")
< Safe owners: 5 EOAs

> update_graph_explorer_focus(active_profiles=["lp_in_pool", "bridge_user_flows"], window_days=30)
< Adds LP positions and bridge flows for every node in current view

# Click a node → side panel shows role badges, semantic provenance, and "next hops"
```

## Knobs

| Setting | Default | Where |
|---|---|---|
| `MAX_HOPS` | 5 | `tools/graph_explorer.py` |
| `DEFAULT_WINDOW_DAYS` | 90 | same |
| `DEFAULT_MAX_NEIGHBORS` | 25 | same |

## Best practices

- **Start with `approved` status filter.** Candidate profiles are useful but noisier.
- **Don't expand past 3 hops** without a reason — the graph becomes illegible fast.
- **Use `Recenter` from the side panel** to reseed cleanly on a new focal node — beats expanding outward forever.
- **The `Ask` button** pushes the current view state into model context and asks the LLM to summarise the subgraph — useful for narrative wrap-up.

## Pitfalls

- **Treating `safe_ownership` as full-fidelity Safe lineage.** Source is `int_execution_safes_current_owners` (current snapshot only). Use historical Safe queries for time-series analysis.
- **Mixing too many profiles.** Three to five active profiles is usually the legibility sweet spot.
- **Following `gpay_ownership` instead of `ga_user_controls_gpay`.** The former is the Safe-owner relationship (sentinel-poisoned for GPay Safes); the latter is the canonical EOA-to-GP-Safe binding.

## See also

- [Mini-Apps overview](index.md)
- [Portfolio](portfolio.md) — single-address counterpart
- [Contract Explorer](contract-explorer.md) — single-contract counterpart
- [Cross-sector models](https://github.com/gnosis-org/dbt-cerebro/blob/main/semantic/relationships/execution_graph.yml) — where the relationship graph is authored
