# Portfolio

Address-centric mini-app that unifies an address's presence across Circles, Gnosis Pay, Safe, DeFi, and yields.

## What it is

Portfolio gives a single address a five-section profile:

- **Overview** — summary card with role flags (is_safe, is_gpay_wallet, is_circles_avatar, …).
- **Relationships** — graph-like neighborhood (Safe owners, GPay owner events, trust relations).
- **Yields** — active LP and lending positions.
- **GPay** — Gnosis Pay Safe events, modules, spender history.
- **Circles** — avatar profile, trust relations, CRC balances, wrappers.

Resource URI: `ui://cerebro/portfolio`. Built on `int_execution_address_roles_current` (the same auto-detection [Graph Explorer](graph-explorer.md) uses).

## When to use it

- Investigating a specific address: "who is `0xabc…` and what do they do on-chain?"
- Verifying multisig ownership before a security review.
- Triaging a customer support ticket where the user supplied an address.
- Composing reports about specific accounts (validators, treasury, partner addresses).

## Step-by-step tutorial

### 1. Open with an address

```text
open_portfolio(address="0xabc…")
```

The auto-detector classifies the address (Safe / GPay / Circles avatar / EOA / …) and seeds the relevant tabs.

### 2. Lazy-load a specific section

Sections load on demand to keep the initial render fast:

```text
load_portfolio_section(section="circles")
load_portfolio_section(section="yields")
```

### 3. Navigate to a related address

```text
navigate_portfolio_relation(target_address="0xdef…", relation="safe_owner")
# Reseeds the panel on the new address, preserving the active tab.
```

### 4. Update focus

```text
update_portfolio_focus(active_tab="yields", window_days=180)
```

## Worked example

```text
# A customer reported a missing GPay payment.
> open_portfolio(address="0xabc…")
< INITIAL_LOAD: roles=[gpay_wallet], gpay events: 142

> load_portfolio_section(section="gpay")
< [GPay events table renders]

# Their controlling EOA via the GA Delay Module
> navigate_portfolio_relation(target_address="0xeoa…", relation="ga_user_controls_gpay")
< [Panel reseeds on the EOA]

> load_portfolio_section(section="circles")
< [Circles trust relations + CRC balances]
```

## Tool reference

| Tool | Purpose |
|---|---|
| `open_portfolio(address)` | Open the panel; auto-detect roles |
| `load_portfolio_address(address)` | Reseed the open panel on a new address |
| `load_portfolio_section(section)` | Lazy-load Overview / Relationships / Yields / GPay / Circles |
| `update_portfolio_focus(...)` | Change tab, window, threshold |
| `navigate_portfolio_relation(target_address, relation)` | Follow a graph edge to another address |

## Best practices

- **Always resolve labels first** with `resolve_address(...)` if the user gave you a name (ENS, Safe, label).
- **Use `navigate_portfolio_relation`, not `load_portfolio_address`,** when following a relationship — it preserves audit trail in the resume hint.
- **Pair with Graph Explorer** for visual context — Portfolio shows the address; Graph Explorer shows its network.

## Pitfalls

- **Querying `safes_current_owners.owner` for GPay control.** Returns the sentinel `0x…0002`. Use `ga_user_controls_gpay` (Delay Module-based) instead — Graph Explorer encodes this canonically.
- **Treating the Yields tab as historical.** It shows current open positions only. For history, query `fct_execution_yields_user_lending_positions` directly.

## See also

- [Mini-Apps overview](index.md)
- [Graph Explorer](graph-explorer.md) — visual network view
- [Contract Explorer](contract-explorer.md) — single-contract RPC view
- [Tools §6](../tools.md#6-mini-apps-live-ui-surfaces)
