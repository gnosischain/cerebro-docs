/* Interactive semantic-layer graph explorer (cytoscape.js + fcose).
 *
 * Mounts on the `#sg-canvas` div emitted into graph.md by
 * dbt-cerebro's scripts/semantic/generate_graph_diagram.py, fetching the
 * companion graph_data.json sidecar. The static Mermaid diagram in the
 * <details> below is the no-JavaScript fallback.
 *
 * MkDocs Material swaps page content via `document$` (instant nav), so we
 * (re)initialise on every emission and tear down any prior instance — the
 * same pattern as javascripts/mathjax.js.
 */
(function () {
  "use strict";

  var cyInstance = null;
  var fcoseRegistered = false;

  // Edge-type palette mirrors the Mermaid legend in graph.md.
  var EDGE_STYLE = {
    pseudo: { color: "#2e7d32", width: 3, style: "solid" },
    spine: { color: "#e65100", width: 2, style: "dashed" },
    other: { color: "#607d8b", width: 1.5, style: "solid" },
  };

  // Soft per-sector tints for the compound (group) backgrounds.
  var SECTOR_PALETTE = [
    "#fff8e1", "#e3f2fd", "#f3e5f5", "#fce4ec", "#e0f7fa",
    "#f1f8e9", "#fff3e0", "#ede7f6", "#efebe9", "#fafafa",
  ];

  function registerFcose() {
    if (fcoseRegistered) return;
    if (window.cytoscape && window.cytoscapeFcose) {
      try {
        window.cytoscape.use(window.cytoscapeFcose);
        fcoseRegistered = true;
      } catch (e) {
        /* already registered across navigations — harmless */
        fcoseRegistered = true;
      }
    }
  }

  function sectorColorMap(sectors) {
    var map = {};
    sectors.forEach(function (s, i) {
      map[s] = SECTOR_PALETTE[i % SECTOR_PALETTE.length];
    });
    return map;
  }

  function buildElements(data) {
    var nodes = data.nodes || [];
    var edges = data.edges || [];

    // Nodes that touch a user_pseudonym edge get the green treatment even
    // when their `kind` is a plain model (matches the Mermaid styling).
    var pseudoNodes = {};
    edges.forEach(function (e) {
      if (e.type === "pseudo") {
        pseudoNodes[e.source] = true;
        pseudoNodes[e.target] = true;
      }
    });

    var sectors = [];
    var seenSector = {};
    nodes.forEach(function (n) {
      if (!seenSector[n.sector]) {
        seenSector[n.sector] = true;
        sectors.push(n.sector);
      }
    });
    sectors.sort();
    var sectorColors = sectorColorMap(sectors);

    var els = [];

    // Compound parent per sector.
    sectors.forEach(function (s) {
      els.push({
        group: "nodes",
        data: { id: "sector::" + s, label: s, isSector: 1 },
        classes: "sector",
        selectable: false,
        style: { "background-color": sectorColors[s] },
      });
    });

    nodes.forEach(function (n) {
      var nodeClass = "model";
      if (n.kind === "spine") {
        nodeClass = "spine";
      } else if (pseudoNodes[n.id]) {
        nodeClass = "pseudo";
      }
      var badge = n.metric_count
        ? n.metric_count + (n.metric_count === 1 ? " metric" : " metrics")
        : "";
      els.push({
        group: "nodes",
        data: {
          id: n.id,
          parent: "sector::" + n.sector,
          label: n.label,
          fullName: n.name,
          sector: n.sector,
          kind: n.kind,
          metricCount: n.metric_count || 0,
          tier: n.quality_tier || "",
          badge: badge,
        },
        classes: nodeClass,
      });
    });

    edges.forEach(function (e, i) {
      els.push({
        group: "edges",
        data: {
          id: "e" + i,
          source: e.source,
          target: e.target,
          etype: e.type,
          axis: e.axis,
        },
        classes: e.type,
      });
    });

    return { elements: els, sectors: sectors, sectorColors: sectorColors };
  }

  function styleSheet() {
    return [
      {
        selector: "node",
        style: {
          label: "data(label)",
          "font-size": "11px",
          "font-family": "-apple-system,Segoe UI,Roboto,sans-serif",
          "text-valign": "center",
          "text-halign": "center",
          "text-wrap": "wrap",
          "text-max-width": "120px",
          width: "label",
          height: "label",
          padding: "8px",
          shape: "round-rectangle",
          "border-width": 1,
          color: "#263238",
        },
      },
      {
        selector: "node.model",
        style: {
          "background-color": "#eceff1",
          "border-color": "#455a64",
        },
      },
      {
        selector: "node.pseudo",
        style: {
          "background-color": "#e8f5e9",
          "border-color": "#2e7d32",
          "border-width": 1.5,
          color: "#1b5e20",
        },
      },
      {
        selector: "node.spine",
        style: {
          "background-color": "#fff3e0",
          "border-color": "#e65100",
          "border-width": 2,
          shape: "round-pill",
          color: "#bf360c",
        },
      },
      {
        selector: "node.sector",
        style: {
          label: "data(label)",
          "font-size": "13px",
          "font-weight": "bold",
          "text-valign": "top",
          "text-halign": "center",
          color: "#37474f",
          "background-opacity": 0.45,
          "border-width": 1,
          "border-color": "#90a4ae",
          shape: "round-rectangle",
          padding: "12px",
        },
      },
      {
        selector: "edge",
        style: {
          "curve-style": "bezier",
          "target-arrow-shape": "none",
          width: 1.5,
          "line-color": "#607d8b",
          opacity: 0.7,
        },
      },
      {
        selector: "edge.pseudo",
        style: {
          "line-color": EDGE_STYLE.pseudo.color,
          width: EDGE_STYLE.pseudo.width,
        },
      },
      {
        selector: "edge.spine",
        style: {
          "line-color": EDGE_STYLE.spine.color,
          width: EDGE_STYLE.spine.width,
          "line-style": "dashed",
          "target-arrow-shape": "triangle",
          "target-arrow-color": EDGE_STYLE.spine.color,
        },
      },
      {
        selector: "edge.other",
        style: {
          "line-color": EDGE_STYLE.other.color,
          width: EDGE_STYLE.other.width,
        },
      },
      { selector: ".dimmed", style: { opacity: 0.12 } },
      {
        selector: "node:selected",
        style: { "border-width": 3, "border-color": "#d84315" },
      },
    ];
  }

  function buildFilters(container, cy, sectors, sectorColors) {
    if (!container) return;
    container.innerHTML = "";
    var active = {};
    sectors.forEach(function (s) {
      active[s] = true;
      var chip = document.createElement("button");
      chip.type = "button";
      chip.className = "sg-chip sg-chip--on";
      chip.textContent = s;
      chip.style.borderColor = sectorColors[s];
      chip.addEventListener("click", function () {
        active[s] = !active[s];
        chip.classList.toggle("sg-chip--on", active[s]);
        chip.classList.toggle("sg-chip--off", !active[s]);
        var sel = cy.nodes('[sector = "' + s + '"]');
        if (active[s]) {
          sel.style("display", "element");
        } else {
          sel.style("display", "none");
        }
      });
      container.appendChild(chip);
    });
  }

  function wireInteractions(cy) {
    cy.on("tap", "node", function (evt) {
      var node = evt.target;
      if (node.data("isSector")) return;
      var hood = node.closedNeighborhood();
      cy.elements().addClass("dimmed");
      hood.removeClass("dimmed");
      node.removeClass("dimmed");
    });
    cy.on("tap", function (evt) {
      if (evt.target === cy) {
        cy.elements().removeClass("dimmed");
      }
    });
  }

  function runLayout(cy) {
    registerFcose();
    var name = fcoseRegistered ? "fcose" : "cose";
    var opts = { name: name, animate: false, fit: true, padding: 30 };
    if (name === "fcose") {
      opts.quality = "default";
      opts.nodeSeparation = 90;
      opts.idealEdgeLength = 90;
      opts.nodeRepulsion = 6000;
      opts.packComponents = true;
    }
    cy.layout(opts).run();
  }

  function initGraph() {
    var container = document.getElementById("sg-canvas");
    if (!container) return;
    if (!window.cytoscape) return;

    // Tear down any instance from a previous page (Material instant nav).
    if (cyInstance) {
      try {
        cyInstance.destroy();
      } catch (e) {
        /* ignore */
      }
      cyInstance = null;
    }

    var src = container.getAttribute("data-src");
    if (!src) return;

    fetch(src)
      .then(function (r) {
        if (!r.ok) throw new Error("HTTP " + r.status);
        return r.json();
      })
      .then(function (data) {
        // Container may have been swapped out while fetching.
        var live = document.getElementById("sg-canvas");
        if (!live) return;

        var built = buildElements(data);
        registerFcose();

        cyInstance = window.cytoscape({
          container: live,
          elements: built.elements,
          style: styleSheet(),
          wheelSensitivity: 0.2,
          minZoom: 0.1,
          maxZoom: 3,
        });

        runLayout(cyInstance);
        wireInteractions(cyInstance);
        buildFilters(
          document.getElementById("semantic-graph-filters"),
          cyInstance,
          built.sectors,
          built.sectorColors
        );

        var reset = document.getElementById("semantic-graph-reset");
        if (reset) {
          reset.onclick = function () {
            cyInstance.elements().removeClass("dimmed");
            cyInstance.nodes().style("display", "element");
            var chips = document.querySelectorAll("#semantic-graph-filters .sg-chip");
            chips.forEach(function (c) {
              c.classList.add("sg-chip--on");
              c.classList.remove("sg-chip--off");
            });
            runLayout(cyInstance);
          };
        }
      })
      .catch(function (err) {
        container.setAttribute("data-error", String(err));
        // Fallback Mermaid diagram below remains visible.
        console.warn("semantic-graph: failed to load", err);
      });
  }

  if (typeof window.document$ !== "undefined" && window.document$.subscribe) {
    window.document$.subscribe(function () {
      initGraph();
    });
  } else if (typeof document$ !== "undefined" && document$.subscribe) {
    // Material exposes `document$` as a bare global in some builds.
    document$.subscribe(function () {
      initGraph();
    });
  } else {
    document.addEventListener("DOMContentLoaded", initGraph);
  }
})();
