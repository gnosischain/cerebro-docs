# Cross-sector examples

Three worked patterns showing what the semantic layer was built for.
Each example pairs the **intent** with the **MCP call** and the
**emitted SQL**, so you can see exactly what work the layer does on
your behalf.

## Example 1 — Time-spine cross-grain composition

**Intent**: weekly overlay of CoW Protocol DEX volume, lending deposits,
and revenue active users. The cow data is daily-grain natively; lending
and revenue are already weekly. We want all three aligned on Monday
weeks.

**MCP call**:

```python
mcp__cerebro-dev__query_metrics(
    metrics=[
        "cow_volume_usd",
        "lending_deposits_volume_weekly",
        "revenue_active_users_weekly",
    ],
    dimensions=["week"],
    order_by=["week DESC"],
    limit=5,
)
```

**What the planner does**:

1.  Recognises three metrics with three different roots → engages
    `multi_branch_aggregate_join` mode.
2.  For each branch, resolves the `week` dimension:
    - cow's root has a `date` (day-grain) column → synthesises
      `toMonday(b1_root.date) AS week`.
    - lending's root has a native `week` column → uses it directly.
    - revenue's root has a native `week` column → uses it directly.
3.  Builds a `keys` CTE as `UNION DISTINCT` of all branches' weeks.
4.  Joins each branch back to `keys` on the shared `week`.

**Emitted SQL** (abbreviated):

```sql
WITH
  branch_1 AS (
    SELECT toMonday(b1_root.date) AS week,
           sum(coalesce(volume_usd, 0)) AS cow_volume_usd
    FROM dbt.fct_execution_cow_daily AS b1_root
    GROUP BY toMonday(b1_root.date)
  ),
  branch_2 AS (
    SELECT week,
           sum(deposits_volume_weekly) AS lending_deposits_volume_weekly
    FROM dbt.fct_execution_lending_weekly AS b2_root
    GROUP BY week
  ),
  branch_3 AS (
    SELECT week,
           sum(users_cnt) AS revenue_active_users_weekly
    FROM dbt.api_revenue_active_users_totals_weekly AS b3_root
    GROUP BY week
  ),
  keys AS (
    SELECT week FROM branch_1
    UNION DISTINCT SELECT week FROM branch_2
    UNION DISTINCT SELECT week FROM branch_3
  )
SELECT keys.week, branch_1.cow_volume_usd,
       branch_2.lending_deposits_volume_weekly,
       branch_3.revenue_active_users_weekly
FROM keys
LEFT JOIN branch_1 ON keys.week = branch_1.week
LEFT JOIN branch_2 ON keys.week = branch_2.week
LEFT JOIN branch_3 ON keys.week = branch_3.week
ORDER BY week DESC
LIMIT 5
```

**Sample output**:

| Week | cow_volume_usd | lending_deposits | revenue_active_users |
| --- | ---: | ---: | ---: |
| 2026-05-04 | $0 (partial) | $1.34M | 10,807 |
| 2026-04-27 | $521K | $3.21M | 10,683 |
| 2026-04-20 | $2.71M | $2.78M | 10,555 |
| 2026-04-13 | $4.26M | $1.35M | 10,446 |
| 2026-04-06 | $1.51M | $1.73M | 10,328 |

**Value contributed by the semantic layer**: this is **8 lines of MCP
call** instead of **30+ lines of hand-written SQL with three CTEs**.
The `toMonday(date)` upcast for the cow side is invisible to the
caller — the planner synthesises it because (a) cow's root has a
day-grain time column, (b) `dim_time_spine_weekly` is registered, and
(c) a relationship from cow to the weekly spine exists.

---

## Example 2 — Web vs on-chain Gnosis App parity

**Intent**: compare the web-side Mixpanel DAU sum-per-week with the
on-chain Gnosis App activity user count for the same weeks. Two metrics
from completely different data domains (Mixpanel vs execution layer
heuristics), unified by the project's Monday-anchored weekly spine.

**MCP call**:

```python
mcp__cerebro-dev__query_metrics(
    metrics=["gnosis_app_mixpanel_dau", "gnosis_app_activity_users_daily"],
    dimensions=["week"],
    order_by=["week DESC"],
    limit=5,
)
```

**What the planner does**:

- Both metric roots are at day-grain (`date` column). Both need the
  `toMonday(date)` upcast to reach the `week` dimension.
- The planner emits the same `multi_branch_aggregate_join` shape, with
  upcast synthesised on **both** branches.

**Emitted SQL** (abbreviated):

```sql
WITH
  branch_1 AS (
    SELECT toMonday(b1_root.date) AS week,
           sum(dau) AS gnosis_app_mixpanel_dau
    FROM dbt.api_mixpanel_ga_overview_daily AS b1_root
    GROUP BY toMonday(b1_root.date)
  ),
  branch_2 AS (
    SELECT toMonday(b2_root.date) AS week,
           sum(n_users) AS gnosis_app_activity_users_daily
    FROM dbt.api_execution_gnosis_app_activity_by_action_daily AS b2_root
    GROUP BY toMonday(b2_root.date)
  ),
  ...
```

**Sample output**:

| Week | Mixpanel weekly DAU sum | on-chain weekly activity users |
| --- | ---: | ---: |
| 2026-05-04 | 9,118 | 8,616 |
| 2026-04-27 | 7,970 | 7,614 |
| 2026-04-20 | 7,649 | 8,093 |
| 2026-04-13 | 7,717 | 8,063 |

**Value contributed by the semantic layer**: the two views of "Gnosis
App users" — one from product analytics, one from on-chain heuristics
— are *automatically* aligned on Monday weeks even though they come
from completely different source systems. Without the semantic layer
this would be a hand-rolled join with two `toMonday(date)` calls and
hopeful agreement on week-anchor conventions.

---

## Example 3 — User-pseudonym 4-way intersection (raw, planner-gapped)

**Intent**: count users who appear in all four user-keyed sectors —
revenue (active), Gpay, Circles humans, and Gnosis App on-chain.

**Why this is currently raw**: the planner's
`multi_branch_aggregate_join` mode requires a shared dimension to join
on. With no time grain and no shared categorical dimension, the
"intersection cardinality" pattern isn't expressible via
`query_metrics`. See [maintenance](maintenance.md#open-improvements-ci-tooling)
for the planned `set_intersection` metric type.

**MCP call** (raw):

```python
mcp__cerebro-dev__execute_query(sql="""
WITH revenue_active AS (
  SELECT DISTINCT user_pseudonym
  FROM dbt.fct_revenue_per_user_weekly
  WHERE week = (SELECT max(week) FROM dbt.fct_revenue_per_user_weekly)
    AND is_revenue_active = 1
)
SELECT
  count() AS revenue_active_total,
  countIf(g.user_pseudonym IS NOT NULL)  AS also_in_gpay,
  countIf(c.user_pseudonym IS NOT NULL)  AS also_in_circles,
  countIf(ga.user_pseudonym IS NOT NULL) AS also_in_gnosis_app,
  countIf(g.user_pseudonym IS NOT NULL
       AND c.user_pseudonym IS NOT NULL
       AND ga.user_pseudonym IS NOT NULL) AS in_all_four
FROM revenue_active r
LEFT JOIN dbt.fct_execution_gpay_users_distinct g USING (user_pseudonym)
LEFT JOIN dbt.fct_execution_circles_human_avatars_distinct c USING (user_pseudonym)
LEFT JOIN dbt.fct_execution_gnosis_app_users_distinct ga USING (user_pseudonym)
""")
```

**Sample output** (May 2026):

| Cohort | Count | % of revenue-active |
| --- | ---: | ---: |
| Revenue-active total | 10,807 | 100% |
| Also in Gpay | 8,623 | 80% |
| Also in Circles humans | 2 | <0.1% |
| Also in Gnosis App on-chain | 2 | <0.1% |
| **In all four** | **0** | **0%** |

**Value contributed by the semantic layer** (despite being raw SQL):

- The four `fct_*_users_distinct` marts the join touches are *all*
  outputs of the semantic-layer work. Pre-layer, this query would
  involve hand-joining intermediates and recomputing pseudonyms.
- `USING (user_pseudonym)` works because every mart computes the same
  hash with the same salt — the project-wide invariant the layer
  documents and enforces.
- The "real" answer ("0 in all four") is a product insight that comes
  out of having the marts standardized. Without the layer, this
  question would be too painful to ask iteratively.

This is a good illustration of the **infrastructure vs interface**
distinction in the [index](index.md): the user-keyed marts (infrastructure)
delivered all the value here even though `query_metrics` (interface)
wasn't reachable.

---

## What these three patterns cover

| Pattern | Planner mode | Difficulty without semantic layer |
| --- | --- | --- |
| Cross-grain composition (Ex. 1) | `multi_branch_aggregate_join` + time-spine upcast | High — three CTEs, `toMonday()` x N, manual key UNION |
| Same-grain cross-domain (Ex. 2) | `multi_branch_aggregate_join` + time-spine upcasts on both branches | Medium — two CTEs, both with `toMonday()` |
| Multi-set intersection (Ex. 3) | (not yet supported) — raw SQL | High — but the underlying marts make it feasible |

If your analytics question fits Ex. 1 or Ex. 2 shape, `query_metrics`
is the right tool. If it fits Ex. 3, raw `execute_query` with the
user-keyed marts is the right tool.

The fourth common shape — **single-metric trends** (one root, one
dimension) — is handled by the `single_model` planner mode and isn't
exemplified here because it's trivial: any approved metric, any
allowed dimension, `query_metrics` works.
