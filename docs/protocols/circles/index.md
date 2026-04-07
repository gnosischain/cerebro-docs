# Circles V2

## Protocol Overview

Circles V2 is a decentralized universal basic income (UBI) currency protocol deployed on **Gnosis Chain** in **October 2024**. Built on the ERC-1155 standard, it allows every human participant to mint their own personal CRC tokens at a rate of 1 CRC per hour. A trust-based social graph enables transitive transfers between users who are not directly connected, creating a quasi-fungible currency backed by social relations rather than centralized institutions.

Circles is defined by five simple rules:

1. **Universal access** — anyone can create an account without centralized gatekeeping.
2. **Distributed issuance** — each account creates 1 CRC per hour.
3. **Demurrage** — every CRC loses 7% nominal value per year.
4. **Rule of Trust** — if account A trusts account B, anyone holding B-CRC can swap them for any CRC held by A, at a 1:1 rate.
5. **Groups** — anyone can create a group; group CRC are minted from and redeemed against member CRC at 1:1.

## Contracts on Gnosis Chain

| Contract | Address | dbt Model |
|----------|---------|-----------|
| Hub V2 | `0xc12C1E50ABB450d6205Ea2C3Fa861b3B834d13e8` | `contracts_circles_v2_Hub_events` |
| ERC20Lift | `0x5F99a795dD2743C36D63511f0D4bc667e6d3cDB5` | `contracts_circles_v2_ERC20Lift_events` |
| NameRegistry | `0xA27566fD89162cC3D40Cb59c87AAaA49B85F3474` | — |
| Migration | `0xD44B8dcFBaDfC78EA64c55B705BFc68199B56376` | — |
| Base Mint Policy | `0xcCa27c26CF7BAC2a9928f42201d48220F0e3a549` | — |

## dbt Models

- **`contracts_circles_v2_Hub_events`** — all Hub events (transfers, trust, registrations, collateral), start **2024-10-15**
- **`contracts_circles_v2_ERC20Lift_events`** — wrapper deployment events, start **2024-10-15**
- **`int_execution_circles_v2_transfers`** — unified transfer table (hub + wrapper), start **2024-10-15**
- **`int_execution_circles_v2_balances_daily`** — daily EOD balances with demurrage, start **2024-10-15**

See [Data Models](data-models.md) for the full pipeline reference.

## Avatar Types

Circles defines three kinds of accounts (avatars):

- **Human** — mints personal CRC at 1 CRC/hour. Minting is capped at a 14-day backlog. Must be invited by an existing human. Event: `RegisterHuman(avatar, inviter)`.
- **Group** — does **not** mint CRC from time. Issues group-CRC in exchange for member personal CRC deposited as collateral. Has a vault (treasury) and a configurable mint policy. Event: `RegisterGroup(group, mint, treasury, name, symbol)`.
- **Organization** — cannot mint any CRC. Used by shops, vendors, and services to send and receive CRC. Participates in the trust graph only. Event: `RegisterOrganization(organization, name)`.

## Trust System & Transitive Transfers

The trust graph is a **directed** social network. When Alice trusts Bob, two things happen:

1. Alice commits to accepting Bob-CRC as payment for goods and services.
2. Alice's CRC holdings become swappable for Bob-CRC by anyone in the network.

!!! warning "Trusting is a responsibility"
    If Bob turns out to be dishonest, Alice's CRC can be depleted via the swap rule. Users should only trust accounts they are confident are honest.

### Transitive Transfers

Payments route through chains of trust, like water through a network of pipes. Even if Carol and Bob don't trust each other directly, Carol can pay Bob if a trust path exists:

1. Carol swaps Carol-CRC for Alice-CRC at Alice (because Alice trusts Carol)
2. Carol sends Alice-CRC to Bob (because Bob trusts Alice)

Key properties:

- **Conservation of trusted balance**: each intermediate party's total trusted CRC holdings remain unchanged during a transitive transfer.
- **Social network connectivity**: the "six degrees of separation" property of social graphs ensures most honest users can transact with each other.
- **Pathfinder**: an off-chain service computes optimal transfer paths through the trust graph.
- **Trust expiry**: trust relations carry a Unix timestamp expiry (`0` = no expiry).

### Sybil Resistance

The trust system provides **relative Sybil resistance**: a malicious actor controlling multiple accounts can only influence the broader economy to the extent that honest "boundary" accounts trust them. The damage is bounded by the trusted CRC holdings of these boundary accounts.

## Demurrage (Daily Burn)

All CRC balances lose **7% nominal value per year** through a continuous daily decay. This is paired with 1 CRC/hour minting to create a fair distribution of purchasing power.

### Parameters

| Parameter | Value |
|-----------|-------|
| Annual rate | 7% |
| Daily decay factor (γ) | $(1 - 0.07)^{1/365.25} \approx 0.9998013320085989$ |
| Inflation day zero | October 15, 2020, 00:00 UTC |
| Inflation day zero (Unix) | `1602720000` |
| Equilibrium balance | ~120,804 CRC |

### Formula

Day calculation:

$$\text{day}(t) = \left\lfloor \frac{t - 1602720000}{86400} \right\rfloor$$

Balance decay between two timestamps:

$$\text{balance}(t) = \text{balance}(t_0) \times \gamma^{\,\text{day}(t) - \text{day}(t_0)}$$

### Equilibrium Dynamics

- Below ~120,804 CRC: minting outpaces demurrage → balance grows
- Above ~120,804 CRC: demurrage outpaces minting → balance shrinks
- After ~80 years of continuous minting, accounts reach the stable equilibrium
- After minting stops, remaining CRC decay with a half-life of ~10 years

This creates an effective **progressive tax**: small balances grow, large balances shrink. The same redistribution dynamic that inflation creates in fiat currencies is made explicit and transparent in Circles.

### The Inflationary View

There is an equivalent formulation of Circles where no demurrage applies but the minting rate increases over time. Both views produce identical real economic outcomes — the same purchasing power distribution, the same equation for a user's share of the money supply. Static/inflationary ERC-20 wrappers (`circlesType = 1`) implement this alternative view.

## Static (Inflationary) vs Demurrage Units

Circles amounts can be expressed in two equivalent representations:

| Representation | Description | Used by |
|---------------|-------------|---------|
| **Demurrage** | Time-dependent. Amounts decay over time. | Hub contract (native), demurrage wrappers (`circlesType=0`) |
| **Static / Inflationary** | Time-invariant. Same purchasing power, different nominal value. | Static wrappers (`circlesType=1`), DeFi integrations |

### Conversion Formulas

At timestamp $t$:

$$\text{demurrage} = \text{static} \times \gamma^{\,\text{day}(t)}$$

$$\text{static} = \frac{\text{demurrage}}{\gamma^{\,\text{day}(t)}}$$

The Hub contract provides `convertInflationaryToDemurrageValue()` and `convertDemurrageToInflationaryValue()` for on-chain conversion.

!!! note "Analytics convention"
    In our analytics pipeline, all transfer amounts are normalized to **demurrage units**. The `unit_type` column indicates the original representation (`'demurrage'` or `'static'`), and `amount_raw_original` preserves the pre-conversion value.

## Wrapping (ERC20Lift)

Circles Hub tokens are ERC-1155 — incompatible with most DeFi protocols (DEXes, lending markets, etc.) that expect ERC-20 tokens. The **ERC20Lift** contract deploys ERC-20 wrapper contracts for individual avatar tokens.

### Wrapper Types

| `circlesType` | Name | Behavior | Use Case |
|---------------|------|----------|----------|
| `0` | Demurrage | Wrapped balance continues to decay | Preserves Circles economic incentives |
| `1` | Static / Inflationary | Balance is frozen at wrap time (no decay) | DeFi compatibility (AMMs, lending) |

### Mechanics

- **Wrapping**: burns ERC-1155 tokens → mints ERC-20 wrapper tokens
- **Unwrapping**: burns ERC-20 wrapper → re-mints ERC-1155 tokens
- Each (avatar, circlesType) pair maps to a unique ERC-20 wrapper contract address

### Event

```
ERC20WrapperDeployed(address indexed avatar, address indexed erc20Wrapper, uint8 circlesType)
```

## Token ID Encoding

ERC-1155 token IDs encode the avatar address as a uint256 (left-padded to 32 bytes).

```sql
-- token_id → avatar address
concat('0x', leftPad(lower(hex(toUInt256(token_id))), 40, '0'))

-- avatar → token_id
reinterpretAsUInt256(
  concat(
    reverse(unhex(lower(substring(avatar, 3)))),
    unhex(repeat('00', 12))
  )
)
```

## Groups — Currency for Communities

Groups enable communities to share a fungible currency backed by members' personal CRC.

### How Group Tokens Work

1. **Minting**: anyone holding CRC trusted by the group deposits them via `groupMint()` → receives group-CRC at 1:1.
2. **Collateral**: deposited personal CRC enters the group's **vault** (treasury) and is removed from circulation.
3. **Redemption**: burn group-CRC via `groupRedeem()` → receive any CRC from the vault at 1:1.

**Total supply invariant**: minting group tokens does not change the total CRC in circulation. Collateral locked always equals group tokens minted.

### Mint Policies

Groups use customizable **mint policy** smart contracts that can:

- Limit total supply of group-CRC
- Require identity verification for membership
- Add lock-in periods to restrict early redemption
- Require exogenous collateral
- Dynamically adjust supply

### Transitive Membership

If Alice is a member of Group G, and Group G is a member of Group H, then Alice can effectively mint H-CRC through G. This enables federations of groups.

### The Resilience-Efficiency Tradeoff

| Dimension | Personal CRC | Group CRC |
|-----------|-------------|-----------|
| Resilience | Maximum — revocable trust, individual control | Lower — shared trust surface |
| Efficiency | Lower — complex path routing | Maximum — immediate fungibility within group |
| Sybil resistance | Strong — per-user trust decisions | Dependent on membership policy |

### Group Types

Groups can serve many purposes: location-based (city currencies), identity-based (verified humans), enterprise-based (company tokens), event-based, education-based, and more.

## Liquidity Clusters & Exchange Rates

At the micro level, different users' CRC are technically non-fungible. The trust graph creates emergent **liquidity clusters** — sets of currencies that are mutually convertible at 1:1.

Key theoretical results from the whitepaper:

- **Value flows opposite to trust**: if A trusts B, then V(B-CRC) ≥ V(A-CRC) at equilibrium.
- Within a liquidity cluster, all currencies exchange at 1:1.
- Between clusters, exchange rates can differ.
- Transitive transfer capacity = **maximum flow** on the trust graph (a well-studied optimization problem).
- The transferrable trusted balance between two groups of accounts = the max-flow / min-cut of the trust graph.

## Decoded Event Signatures

### Hub Events

```
TransferSingle(address indexed operator, address indexed from, address indexed to, uint256 id, uint256 value)
TransferBatch(address indexed operator, address indexed from, address indexed to, uint256[] ids, uint256[] values)
Trust(address indexed truster, address indexed trustee, uint256 expiryTime)
RegisterHuman(address indexed avatar, address indexed inviter)
RegisterGroup(address indexed group, address indexed mint, address indexed treasury, string name, string symbol)
RegisterOrganization(address indexed organization, string name)
PersonalMint(address indexed human, uint256 amount, uint256 startPeriod, uint256 endPeriod)
CollateralLockedSingle(address indexed group, uint256 id, uint256 value)
CollateralLockedBatch(address indexed group, uint256[] ids, uint256[] values)
GroupRedeemCollateralBurn(address indexed group, uint256 id, uint256 value)
GroupRedeemCollateralReturn(address indexed group, uint256 id, uint256 value, address to)
```

### ERC20Lift Events

```
ERC20WrapperDeployed(address indexed avatar, address indexed erc20Wrapper, uint8 circlesType)
```

## `decoded_params` Reference

For Hub events (`contracts_circles_v2_Hub_events`):

| Field | Type | Description |
|-------|------|-------------|
| `operator` | address | Entity that initiated the transfer |
| `from` | address | Sender (or `0x0` for mints) |
| `to` | address | Recipient (or `0x0` for burns) |
| `id` | uint256 | ERC-1155 token ID (avatar address encoded) |
| `value` | uint256 | Transfer amount in base units (18 decimals) |
| `ids` | uint256[] | Array of token IDs (TransferBatch) |
| `values` | uint256[] | Array of amounts (TransferBatch) |
| `truster` | address | Account granting trust |
| `trustee` | address | Account receiving trust |
| `expiryTime` | uint256 | Unix timestamp when trust expires (0 = never) |
| `avatar` | address | Registered avatar address |
| `inviter` | address | Human who invited this avatar |
| `group` | address | Group address |
| `mint` | address | Mint policy contract |
| `treasury` | address | Treasury contract |

## Example Queries

### Daily Transfer Volume by Type

```sql
SELECT
    toDate(block_timestamp)        AS day,
    transfer_type,
    unit_type,
    count()                        AS transfer_count,
    sum(toFloat64(amount_raw)) / 1e18 AS volume_crc
FROM dbt.int_execution_circles_v2_transfers
GROUP BY day, transfer_type, unit_type
ORDER BY day DESC
LIMIT 30
```

### Active Trust Relationships Over Time

```sql
SELECT
    toStartOfWeek(block_timestamp) AS week,
    count()                        AS new_trust_events,
    countIf(decoded_params['expiryTime'] != '0') AS with_expiry
FROM dbt.contracts_circles_v2_Hub_events
WHERE event_name = 'Trust'
GROUP BY week
ORDER BY week DESC
```

### Top Token Holders by Demurraged Balance

```sql
SELECT
    account,
    token_address,
    toFloat64(balance_raw) / 1e18            AS balance_crc,
    toFloat64(demurraged_balance_raw) / 1e18 AS demurraged_crc
FROM dbt.int_execution_circles_v2_balances_daily
WHERE date = yesterday()
ORDER BY demurraged_balance_raw DESC
LIMIT 50
```

## See Also

- [Circles Whitepaper](https://whitepaper.aboutcircles.com/)
- [Official Docs](https://docs.aboutcircles.com/)
- [Contracts V2 Technical Reference](https://aboutcircles.github.io/circles-contracts-v2/)
- [GitHub: circles-contracts-v2](https://github.com/aboutcircles/circles-contracts-v2)
- [Data Models](data-models.md) — analytics pipeline details
- [Avatar IPFS Metadata](../../data-pipeline/crawlers/circles-avatar-ipfs.md) — how on-chain `metadataDigest` events are resolved into IPFS profile JSON and exposed via `int_execution_circles_v2_avatar_metadata`
- [Protocol Analytics Index](../index.md)
