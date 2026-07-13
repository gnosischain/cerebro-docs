/* Interactive API metrics catalog explorer.
 *
 * Mounts on the `#api-catalog` div emitted into docs/api/explorer.md,
 * fetching the companion catalog_data.json sidecar (generated from the dbt
 * manifest). The "Browse by category" list below the explorer is the
 * no-JavaScript fallback.
 *
 * MkDocs Material swaps page content via `document$` (instant nav), so we
 * (re)initialise on every emission — the same pattern as
 * javascripts/semantic-graph.js. A dataset flag guards against double
 * initialisation of the same mount element, and the fetched JSON is cached
 * per data-src so instant-nav revisits don't refetch.
 *
 * SECURITY: every piece of data-derived text (dbt descriptions, column
 * names, filter names, …) is rendered via textContent / createTextNode —
 * never innerHTML.
 */
(function () {
  "use strict";

  var SWAGGER_URL = "https://api.analytics.gnosis.io/docs";
  var DEFAULT_BASE_URL = "https://api.analytics.gnosis.io";
  var CHUNK_SIZE = 100;
  var DEBOUNCE_MS = 150;

  // data-src -> Promise resolving to the parsed catalog JSON.
  var dataCache = {};

  var GRANULARITY_ORDER = [
    "hourly", "daily", "weekly", "monthly", "quarterly", "yearly", "latest",
  ];

  // Facet groups: OR within a group, AND across groups.
  var GROUPS = [
    {
      id: "category",
      label: "Category",
      vals: function (ep) { return ep.category ? [ep.category] : []; },
    },
    {
      id: "tier",
      label: "Tier",
      vals: function (ep) { return ep.tier ? [ep.tier] : []; },
    },
    {
      id: "granularity",
      label: "Granularity",
      vals: function (ep) { return ep.granularity ? [ep.granularity] : []; },
    },
    {
      id: "method",
      label: "Method",
      vals: function (ep) { return ep.methods || []; },
    },
    {
      id: "type",
      label: "Type",
      vals: function (ep) { return [ep.legacy ? "legacy" : "filtered"]; },
    },
  ];

  /* ---------- data loading ---------- */

  function loadData(src) {
    if (!dataCache[src]) {
      dataCache[src] = fetch(src).then(function (r) {
        if (!r.ok) throw new Error("HTTP " + r.status);
        return r.json();
      });
      dataCache[src].catch(function () {
        // Drop the failed promise so the next visit retries the fetch.
        delete dataCache[src];
      });
    }
    return dataCache[src];
  }

  /* ---------- DOM helpers (textContent only — data is untrusted) ---------- */

  function el(tag, className, text) {
    var node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined && text !== null) node.textContent = String(text);
    return node;
  }

  // rows: array of arrays of { text, code } cells.
  function buildTable(headers, rows) {
    var wrap = el("div", "ac-table-wrap");
    var table = document.createElement("table");
    var thead = document.createElement("thead");
    var headRow = document.createElement("tr");
    headers.forEach(function (h) {
      headRow.appendChild(el("th", null, h));
    });
    thead.appendChild(headRow);
    table.appendChild(thead);
    var tbody = document.createElement("tbody");
    rows.forEach(function (cells) {
      var tr = document.createElement("tr");
      cells.forEach(function (cell) {
        var td = document.createElement("td");
        if (cell && cell.code && cell.text) {
          var codeEl = document.createElement("code");
          codeEl.textContent = cell.text;
          td.appendChild(codeEl);
        } else {
          td.textContent = cell && cell.text ? cell.text : "";
        }
        tr.appendChild(td);
      });
      tbody.appendChild(tr);
    });
    table.appendChild(tbody);
    wrap.appendChild(table);
    return wrap;
  }

  function metaLine(label, text) {
    var p = el("p", "ac-detail-meta");
    p.appendChild(el("strong", null, label + ": "));
    p.appendChild(document.createTextNode(text));
    return p;
  }

  /* ---------- search / facet plumbing ---------- */

  function buildHaystack(ep) {
    var parts = [ep.path, ep.resource, ep.model, ep.description];
    (ep.columns || []).forEach(function (c) {
      if (c && c.name) parts.push(c.name);
    });
    (ep.filters || []).forEach(function (f) {
      if (f && f.name) parts.push(f.name);
    });
    return parts
      .filter(function (p) { return !!p; })
      .join(" ")
      .toLowerCase();
  }

  function collectValues(endpoints, group) {
    var seen = {};
    var out = [];
    endpoints.forEach(function (ep) {
      group.vals(ep).forEach(function (v) {
        if (v && !seen[v]) {
          seen[v] = true;
          out.push(v);
        }
      });
    });
    if (group.id === "tier" || group.id === "method") {
      out.sort();
    } else if (group.id === "granularity") {
      out.sort(function (a, b) {
        var ia = GRANULARITY_ORDER.indexOf(a);
        var ib = GRANULARITY_ORDER.indexOf(b);
        if (ia === -1 && ib === -1) return a < b ? -1 : a > b ? 1 : 0;
        if (ia === -1) return 1;
        if (ib === -1) return -1;
        return ia - ib;
      });
    }
    return out;
  }

  /* ---------- detail-panel content ---------- */

  function filterNotes(f) {
    var notes = [];
    if (f.desc) notes.push(f.desc);
    if (f.case) notes.push("case: " + f.case);
    if (f.max_items) notes.push("max items: " + f.max_items);
    return notes.join("; ");
  }

  function policyLine(ep) {
    var text = ep.allow_unfiltered
      ? "unfiltered queries allowed"
      : "at least one filter is required";
    if (ep.require_any_of && ep.require_any_of.length) {
      text += " — must include one of: " + ep.require_any_of.join(", ");
    }
    return metaLine("Filter policy", text);
  }

  function paginationLine(ep) {
    var pg = ep.pagination || {};
    var text;
    if (pg.enabled) {
      text =
        "limit/offset, default " + pg.default_limit + ", max " + pg.max_limit;
      text +=
        pg.response === "envelope"
          ? " — envelope response {items, pagination}"
          : " — bare JSON array";
    } else {
      text = "none — bare JSON array";
    }
    return metaLine("Pagination", text);
  }

  function sortLine(ep) {
    var parts = [];
    if (ep.sort && ep.sort.length) {
      var fixed = ep.sort
        .map(function (s) { return s.column + " " + s.dir; })
        .join(", ");
      parts.push("default " + fixed);
    }
    if (ep.sortable_fields && ep.sortable_fields.length) {
      parts.push("user-sortable fields: " + ep.sortable_fields.join(", "));
    }
    return metaLine("Sort", parts.length ? parts.join(" — ") : "none");
  }

  /* ---------- curl generation ---------- */

  function pickFilter(ep) {
    var filters = ep.filters || [];
    for (var i = 0; i < filters.length; i++) {
      var t = (filters[i].type || "").toLowerCase();
      if (t.indexOf("date") !== -1) return filters[i];
    }
    return filters.length ? filters[0] : null;
  }

  function placeholderFor(f) {
    var t = (f.type || "").toLowerCase();
    if (t.indexOf("date") !== -1) return "2025-01-01";
    if (
      t.indexOf("int") !== -1 ||
      t.indexOf("num") !== -1 ||
      t.indexOf("float") !== -1 ||
      t.indexOf("decimal") !== -1
    ) {
      return "100";
    }
    if (t.indexOf("bool") !== -1) return "true";
    return "value";
  }

  function buildCurl(ep, baseUrl) {
    var url = baseUrl + ep.path;
    var filter = ep.legacy ? null : pickFilter(ep);
    var methods = ep.methods || [];
    var postOnly =
      methods.length > 0 &&
      methods.indexOf("GET") === -1 &&
      methods.indexOf("POST") !== -1;
    var needsKey = !!ep.tier && ep.tier !== "tier0";
    var lines = [];

    if (postOnly) {
      lines.push('curl -X POST "' + url + '"');
      lines.push('  -H "Content-Type: application/json"');
      if (needsKey) lines.push('  -H "X-API-Key: YOUR_API_KEY"');
      var body = filter
        ? '{"' + filter.name + '": "' + placeholderFor(filter) + '"}'
        : "{}";
      lines.push("  -d '" + body + "'");
    } else {
      var query = filter
        ? "?" + filter.name + "=" + placeholderFor(filter)
        : "";
      lines.push('curl "' + url + query + '"');
      if (needsKey) lines.push('  -H "X-API-Key: YOUR_API_KEY"');
    }
    return lines.join(" \\\n");
  }

  /* ---------- detail panel ---------- */

  function buildDetail(ep, baseUrl) {
    var box = el("div", "ac-detail");

    if (ep.description) {
      box.appendChild(el("p", "ac-detail-desc", ep.description));
    }

    if (ep.columns && ep.columns.length) {
      box.appendChild(el("h5", "ac-detail-h", "Columns"));
      box.appendChild(
        buildTable(
          ["Column", "Type", "Description"],
          ep.columns.map(function (c) {
            return [
              { text: c.name, code: true },
              { text: c.type, code: true },
              { text: c.desc },
            ];
          })
        )
      );
    }

    if (ep.legacy) {
      box.appendChild(
        el(
          "p",
          "ac-note",
          "Legacy endpoint — GET only, no parameters, returns the full table."
        )
      );
    } else {
      if (ep.filters && ep.filters.length) {
        box.appendChild(el("h5", "ac-detail-h", "Filters"));
        box.appendChild(
          buildTable(
            ["Param", "Operator", "Column", "Type", "Notes"],
            ep.filters.map(function (f) {
              return [
                { text: f.name, code: true },
                { text: f.op, code: true },
                { text: f.column, code: true },
                { text: f.type },
                { text: filterNotes(f) },
              ];
            })
          )
        );
      }
      box.appendChild(policyLine(ep));
      box.appendChild(paginationLine(ep));
      box.appendChild(sortLine(ep));
    }

    box.appendChild(el("h5", "ac-detail-h", "Example request"));
    var pre = el("pre", "ac-curl");
    var code = document.createElement("code");
    code.textContent = buildCurl(ep, baseUrl);
    pre.appendChild(code);
    box.appendChild(pre);

    var links = el("div", "ac-links");
    if (ep.doc) {
      var docLink = el("a", "ac-link", "Full docs →");
      // `doc` is relative to docs/api/ (e.g. "catalog/execution/#anchor");
      // the explorer page lives at /api/explorer/, one directory-URL deeper.
      docLink.href = "../" + ep.doc;
      links.appendChild(docLink);
    }
    var swaggerLink = el("a", "ac-link", "Swagger UI →");
    swaggerLink.href = SWAGGER_URL;
    swaggerLink.target = "_blank";
    swaggerLink.rel = "noopener";
    links.appendChild(swaggerLink);
    box.appendChild(links);

    return box;
  }

  /* ---------- main setup (runs once per mount element) ---------- */

  function setup(mount, data) {
    var root = mount.closest(".api-catalog-explorer");
    var scope = root || document;
    var searchInput = scope.querySelector("#ac-search");
    var facetsBox = scope.querySelector("#ac-facets");
    var countBox = scope.querySelector("#ac-count");

    var baseUrl = data.base_url || DEFAULT_BASE_URL;
    var endpoints = data.endpoints || [];
    endpoints.forEach(function (ep) {
      if (!ep._hay) ep._hay = buildHaystack(ep);
    });

    var state = { query: "", active: {} };
    GROUPS.forEach(function (g) {
      state.active[g.id] = {};
    });

    var groupValues = {};
    GROUPS.forEach(function (g) {
      groupValues[g.id] = collectValues(endpoints, g);
    });
    // Prefer the catalog's own category ordering when provided.
    if (data.categories && data.categories.length) {
      var catOrder = data.categories.map(function (c) { return c.id; });
      groupValues.category.sort(function (a, b) {
        var ia = catOrder.indexOf(a);
        var ib = catOrder.indexOf(b);
        if (ia === -1) ia = catOrder.length;
        if (ib === -1) ib = catOrder.length;
        return ia - ib;
      });
    }

    mount.textContent = "";
    var listBox = el("div", "ac-list");
    var moreBox = el("div", "ac-more");
    mount.appendChild(listBox);
    mount.appendChild(moreBox);

    var currentMatches = [];
    var renderedCount = 0;

    function tokens() {
      return state.query.toLowerCase().split(/\s+/).filter(function (t) {
        return t.length > 0;
      });
    }

    function matchesSearch(ep, toks) {
      for (var i = 0; i < toks.length; i++) {
        if (ep._hay.indexOf(toks[i]) === -1) return false;
      }
      return true;
    }

    function matchesGroup(ep, group) {
      var set = state.active[group.id];
      var keys = Object.keys(set);
      if (keys.length === 0) return true;
      var vals = group.vals(ep);
      for (var i = 0; i < vals.length; i++) {
        if (set[vals[i]]) return true;
      }
      return false;
    }

    // skipGroupId: exclude one group from the AND — used for chip counts.
    function matches(ep, toks, skipGroupId) {
      if (!matchesSearch(ep, toks)) return false;
      for (var i = 0; i < GROUPS.length; i++) {
        if (GROUPS[i].id === skipGroupId) continue;
        if (!matchesGroup(ep, GROUPS[i])) return false;
      }
      return true;
    }

    function anyFilterActive() {
      if (state.query.replace(/\s+/g, "") !== "") return true;
      for (var i = 0; i < GROUPS.length; i++) {
        if (Object.keys(state.active[GROUPS[i].id]).length > 0) return true;
      }
      return false;
    }

    function renderFacets() {
      if (!facetsBox) return;
      facetsBox.textContent = "";
      var toks = tokens();

      GROUPS.forEach(function (group) {
        var values = groupValues[group.id];
        if (!values.length) return;
        var groupEl = el("div", "ac-facet-group");
        groupEl.appendChild(el("span", "ac-facet-label", group.label));
        values.forEach(function (value) {
          var count = 0;
          endpoints.forEach(function (ep) {
            if (!matches(ep, toks, group.id)) return;
            if (group.vals(ep).indexOf(value) !== -1) count++;
          });
          var chip = el("button", "ac-chip");
          chip.type = "button";
          if (state.active[group.id][value]) chip.classList.add("ac-chip--on");
          chip.appendChild(el("span", "ac-chip-label", value));
          chip.appendChild(el("span", "ac-chip-count", String(count)));
          chip.addEventListener("click", function () {
            if (state.active[group.id][value]) {
              delete state.active[group.id][value];
            } else {
              state.active[group.id][value] = true;
            }
            update();
          });
          groupEl.appendChild(chip);
        });
        facetsBox.appendChild(groupEl);
      });

      if (anyFilterActive()) {
        var clearWrap = el("div", "ac-facet-group");
        var clearChip = el("button", "ac-chip ac-chip--clear", "Clear");
        clearChip.type = "button";
        clearChip.addEventListener("click", function () {
          state.query = "";
          if (searchInput) searchInput.value = "";
          GROUPS.forEach(function (g) {
            state.active[g.id] = {};
          });
          update();
        });
        clearWrap.appendChild(clearChip);
        facetsBox.appendChild(clearWrap);
      }
    }

    function buildItem(ep) {
      var item = el("div", "ac-item");
      var row = el("button", "ac-row");
      row.type = "button";

      (ep.methods || []).forEach(function (m) {
        row.appendChild(el("span", "ac-badge ac-badge--" + m.toLowerCase(), m));
      });
      row.appendChild(el("code", "ac-path", ep.path));
      if (ep.tier) {
        row.appendChild(el("span", "ac-tier ac-tier--" + ep.tier, ep.tier));
      }
      row.appendChild(el("span", "ac-desc", ep.description || ""));

      var detail = null;
      row.addEventListener("click", function () {
        if (!detail) {
          detail = buildDetail(ep, baseUrl);
          item.appendChild(detail);
          item.classList.add("ac-item--open");
          return;
        }
        detail.hidden = !detail.hidden;
        item.classList.toggle("ac-item--open", !detail.hidden);
      });

      item.appendChild(row);
      return item;
    }

    function appendChunk() {
      var next = currentMatches.slice(
        renderedCount,
        renderedCount + CHUNK_SIZE
      );
      next.forEach(function (ep) {
        listBox.appendChild(buildItem(ep));
      });
      renderedCount += next.length;

      moreBox.textContent = "";
      var remaining = currentMatches.length - renderedCount;
      if (remaining > 0) {
        var btn = el("button", "ac-show-more", "Show " + remaining + " more");
        btn.type = "button";
        btn.addEventListener("click", appendChunk);
        moreBox.appendChild(btn);
      }
    }

    function renderResults() {
      var toks = tokens();
      currentMatches = endpoints.filter(function (ep) {
        return matches(ep, toks, null);
      });
      if (countBox) {
        countBox.textContent =
          currentMatches.length + " of " + endpoints.length + " endpoints";
      }
      listBox.textContent = "";
      moreBox.textContent = "";
      renderedCount = 0;
      if (!currentMatches.length) {
        listBox.appendChild(
          el(
            "div",
            "ac-empty",
            "No endpoints match the current search and filters."
          )
        );
        return;
      }
      appendChunk();
    }

    function update() {
      renderFacets();
      renderResults();
    }

    if (searchInput) {
      var debounceTimer = null;
      searchInput.addEventListener("input", function () {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(function () {
          state.query = searchInput.value || "";
          update();
        }, DEBOUNCE_MS);
      });
    }

    update();
  }

  /* ---------- init / re-init on Material instant navigation ---------- */

  function init() {
    var mount = document.getElementById("api-catalog");
    if (!mount) return;
    // Guard against double-init of the same element (document$ replays the
    // current page on subscribe, and the DOMContentLoaded fallback may also
    // have fired).
    if (mount.dataset.acInit === "1") return;
    mount.dataset.acInit = "1";

    var src = mount.getAttribute("data-src");
    if (!src) return;

    mount.textContent = "";
    mount.appendChild(el("div", "ac-loading", "Loading endpoint catalog…"));

    loadData(src)
      .then(function (data) {
        // The mount may have been swapped out while fetching (instant nav).
        if (!mount.isConnected) return;
        setup(mount, data);
      })
      .catch(function (err) {
        delete mount.dataset.acInit; // let a revisit retry
        mount.textContent = "";
        mount.setAttribute("data-error", String(err));
        console.warn("api-catalog: failed to load", err);
      });
  }

  if (typeof window.document$ !== "undefined" && window.document$.subscribe) {
    window.document$.subscribe(function () {
      init();
    });
  } else if (typeof document$ !== "undefined" && document$.subscribe) {
    // Material exposes `document$` as a bare global in some builds.
    document$.subscribe(function () {
      init();
    });
  } else {
    document.addEventListener("DOMContentLoaded", init);
  }
})();
