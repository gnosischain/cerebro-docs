---
title: Metrics Explorer
description: Search and filter every REST API endpoint in the Gnosis Analytics catalog
---

# Metrics Explorer

Search every REST endpoint in the Gnosis Analytics API by name, description, or column, and expand any endpoint to see its columns, declared filters, and a ready-to-run `curl` example. The explorer is generated from the same dbt manifest that powers the API, so it always reflects the live catalog.

<div class="api-catalog-explorer">
  <div class="ac-toolbar">
    <input type="search" id="ac-search" placeholder="Search endpoints — name, description, column…" autocomplete="off" />
    <span class="ac-count" id="ac-count"></span>
  </div>
  <div id="api-catalog" data-src="/api/catalog_data.json"></div>
</div>

## Browse by category

The full endpoint catalog is also available as static reference pages, one per category:

- [Endpoint catalog overview](catalog/index.md)
- [Execution](catalog/execution.md)
- [Consensus](catalog/consensus.md)
- [Celo (Gnosis Pay)](catalog/celo.md)
- [Revenue](catalog/revenue.md)
- [Quarterly Data](catalog/quarterly_data.md)
- [Bridges](catalog/bridges.md)
- [P2P](catalog/p2p.md)
- [ESG](catalog/esg.md)
- [MTA](catalog/mta.md)
- [MMM](catalog/mmm.md)
- [Crawlers Data](catalog/crawlers_data.md)
