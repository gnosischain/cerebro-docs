# Research

This section contains in-depth analytical work built on top of the Gnosis Analytics platform's decoded on-chain data. It covers three areas:

- **[Marketing Mix Modeling (MMM)](mmm/index.md)** -- Long-form reference on MMM as a method: context, data selection, response curves, adstock, Bayesian estimation, validation checkpoints, and the Chapter 3 structural considerations that distinguish working models from misleading ones. Based on the Hakuhodo DY *Marketing Mix Modeling Guidebook* (2023), with a concrete adaptation to on-chain incentive attribution on Gnosis Chain.

- **[Protocol Analytics](../protocols/index.md)** -- Deep dives into DeFi protocols on Gnosis Chain (lending and DEXes), including how each protocol works, what the decoded event data means, and ready-to-use SQL query examples. Covers Agave, Aave V3, Spark, Uniswap V3, Balancer, CoW Protocol, and Swapr.

- **[ESG Reporting](../esg-reporting/index.md)** -- Methodology for estimating the carbon footprint and energy consumption of the Gnosis Chain validator network. Includes node population estimation, hardware classification, power modeling, carbon intensity mapping, and the resulting daily emissions figures.

All research in this section relies on the [Contract ABI Decoding](../data-pipeline/transformation/abi-decoding.md) system and the [dbt Model Catalog](../models/index.md) for its underlying data.
