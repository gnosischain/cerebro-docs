---
title: Measurement (MMM & MTA)
description: Hub for all marketing measurement content — methodology, implementation, data, API, and agent tooling
---

# Measurement (MMM & MTA)

The platform measures marketing effectiveness with two complementary approaches: **Marketing Mix Modeling (MMM)**, a top-down statistical view of how channel spend drives outcomes, and **Multi-Touch Attribution (MTA)**, a bottom-up view of individual user journeys. Content about them spans methodology, dbt implementation, API access, and MCP agent tooling — this page is the map.

## Methodology

<div class="grid cards" markdown>

-   **MMM Methodology**

    ---

    Long-form reference on MMM as a method: response curves, adstock, Bayesian estimation, validation checkpoints, and structural considerations.

    [:octicons-arrow-right-24: MMM Methodology](../mmm/index.md)

-   **MTA Methodology**

    ---

    Multi-touch attribution for on-chain user journeys: touchpoint definitions, attribution windows, and model comparison.

    [:octicons-arrow-right-24: MTA Methodology](../mta/index.md)

</div>

## Implementation

<div class="grid cards" markdown>

-   **Measurement Stack (dbt)**

    ---

    How the MTA + MMM pipeline is implemented in dbt-cerebro: sources, staging, feature tables, and output marts.

    [:octicons-arrow-right-24: Measurement Stack](../../data-pipeline/transformation/measurement-stack.md)

</div>

## Data & API

<div class="grid cards" markdown>

-   **MMM Models**

    ---

    The dbt model catalog for the marketing-mix module.

    [:octicons-arrow-right-24: models/mmm](../../models/mmm.md)

-   **MTA Models**

    ---

    The dbt model catalog for the attribution module.

    [:octicons-arrow-right-24: models/mta](../../models/mta.md)

-   **MMM API Endpoints**

    ---

    REST endpoints serving MMM outputs.

    [:octicons-arrow-right-24: api/catalog/mmm](../../api/catalog/mmm.md)

-   **MTA API Endpoints**

    ---

    REST endpoints serving MTA outputs.

    [:octicons-arrow-right-24: api/catalog/mta](../../api/catalog/mta.md)

</div>

## Agent Tooling (MCP)

<div class="grid cards" markdown>

-   **MMM Standard Operating Procedure**

    ---

    The MCP server's MMM workflow: gates, phases, and outputs.

    [:octicons-arrow-right-24: MCP MMM](../../mcp/mmm.md)

-   **MMM User Guide**

    ---

    Prompt recipes and end-to-end examples for running MMM through an AI assistant.

    [:octicons-arrow-right-24: MMM User Guide](../../mcp/mmm-user-guide.md)

-   **Measurement Flow**

    ---

    How MTA, MMM, and the unified measurement view fit together in agent workflows.

    [:octicons-arrow-right-24: Measurement Flow](../../mcp/measurement-flow.md)

</div>
