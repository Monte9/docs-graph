---
name: create-chart
description: "Create an interactive HTML chart for the graph viewer, paired with a chart-*.md doc so it wires into the graph. Use when the user asks to make a chart, build a visualization, add a heatmap/matrix/scatter, turn an analysis into a chart, or create any standalone HTML visualization that should open from a node in the graph. Also use when adding a chart to accompany an existing analysis doc (the common pattern: an analysis doc describes trends; a chart renders them). The skill covers the non-obvious iframe-download contract and the shared visual vocabulary — without these, charts render but the viewer's download button silently fails and the design drifts. Rebuilds the graph after creation so the new chart shows up immediately."
---

# Create Chart

Create an interactive HTML chart, pair it with a `chart-*.md` doc, and rebuild the graph. Charts open in a full-screen overlay inside the graph viewer's iframe and must follow two contracts — the iframe postMessage contract (so the download button works) and the shared visual vocabulary (so the look stays consistent).

## Folder layout

Charts live as two co-located files inside a date folder under `docs/`:

```
<root>/
└── docs/
    └── YYYY-MM-DD/
        ├── <name>.html            ← the chart itself
        └── chart-<name>.md        ← the doc that wires it into the graph
```

`build.py` picks up the `chart:` key in the `.md` frontmatter and copies the HTML into `_graph/charts/` so the graph viewer can iframe it.

## The two files

### 1. `chart-<name>.md` — the graph-viewer-facing doc

Same frontmatter shape as `create-doc`, plus `chart:` and `type: chart`:

```markdown
---
name: Compliance Landscape
description: 24 competitors × 8 compliance attributes — HIPAA, SOC 2, HITRUST, ISO 27001, GDPR, device/clinical, encryption, hosting.
date: 2026-04-17
type: chart
chart: compliance-landscape.html
data: competitors
references:
  - 2026-04-17/analysis-compliance-landscape.md
---

# Compliance Landscape

<short intro describing what the chart shows and how to read it>

## Attribute definitions
<one bullet per column/axis explaining what it encodes>

## <any cluster/tier/legend breakdown>
<brief explanation of how the chart is grouped or color-coded>

See `analysis-<name>.md` for the full write-up.
```

Key points:
- `chart:` must name an HTML file in the **same date folder** — `build.py` looks for it there.
- `type: chart` activates the full-screen overlay in the viewer (otherwise the doc opens as a side panel).
- `references:` typically points back to the analysis doc so the graph shows an edge between the two.
- `data:` optionally links the chart to a research folder so it edge-links to the research node.

### 2. `<name>.html` — the chart itself

Self-contained HTML file. Uses the shared visual vocabulary and implements the iframe download contract. The easiest path is to copy `templates/chart-template.html` from this skill and fill in the content. Key requirements are documented in the next two sections.

## The iframe download contract (critical)

The graph viewer wraps every chart in an iframe and puts a `⤓` download button in the overlay chrome. When clicked, the viewer posts a message to the chart iframe:

```js
chartIframe.contentWindow.postMessage({ action: 'downloadAsImage' }, '*');
```

Each chart is responsible for listening for this and rendering itself to PNG. Without this listener, the download button silently fails — no error, no feedback. This is the most common place for new charts to break.

Every chart HTML file must include:

```html
<script>
// Download as PNG when the parent graph viewer asks.
window.addEventListener('message', function(e) {
  if (e.data && e.data.action === 'downloadAsImage') {
    const el = document.getElementById('wrapper');  // ← or whatever your root element is
    import('https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/+esm').then(mod => {
      const html2canvas = mod.default;
      html2canvas(el, {
        backgroundColor: '#ffffff',
        scale: 2,
        useCORS: true,
        logging: false,
      }).then(canvas => {
        const a = document.createElement('a');
        a.download = '<name>.png';  // ← match the chart filename
        a.href = canvas.toDataURL('image/png');
        a.click();
      });
    });
  }
});
</script>
```

The html2canvas target (`#wrapper` above) is whatever DOM element wraps the visible chart content. Use `#wrapper` for card-style charts (matrices, tables); use `#chart-wrapper` or similar for full-bleed scatter/positioning charts. The ID doesn't matter as long as the download handler snapshots the right element.

## The shared visual vocabulary

All charts in this plugin share a design language so the graph feels coherent. Reuse these tokens unless you have a specific reason to deviate:

- **Font**: `-apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif`
- **Page background**: `#f4f4f0` (cream)
- **Card background**: `#ffffff` with `1px solid #e6e6dc` border, `border-radius: 12px`, and `box-shadow: 0 4px 24px rgba(0,0,0,0.06)`
- **Text primary**: `#2a2a35`
- **Text secondary / labels**: `#7a7a85` or `#8a8a98`
- **Grid/divider lines**: `#ececE2` or `#f0f0e8`
- **Accent dark (dots, active states)**: `#2a2a35`
- **Accent muted (inactive/partial)**: `#c5c5b8`
- **Swatch rounded pills**: `padding: 3px 8px; border-radius: 999px; background: #f8f8f2; border: 1px solid #eaeae2;`
- **Legend keys** as 11-13px circles (`width: 11px; height: 11px; border-radius: 50%`)

The card root (`#wrapper`, `#chart-wrapper`, whatever you name it) should be centered horizontally on the page with some padding so the download snapshot has a clean margin. Keep the chart inside a single card; nested cards fragment the snapshot.

## When to use what chart type

Pick the chart type that matches the data shape. The plugin doesn't lock you into a style, but these are the shapes the existing charts prove out:

- **Matrix / heatmap** (`compliance-landscape.html`, `feature-matrix.html`) — rows × columns of discrete categorical states (Y / partial / N, or audited / self / none). Best when there are 3-5 discrete states and the reader needs to scan patterns down columns and across rows.
- **Positioning scatter** (`competitor-positioning.html`) — 2-axis map with labeled dots. Best when two continuous dimensions matter and you want to show clustering or whitespace.
- **Process / flow** (`process-flow.html`) — directed steps with arrows. Best for workflows, not comparisons.
- **Landscape map** (`competitive-landscape-map.html`) — grouped bubbles on a canvas, often with regions shaded. Best for showing "who is where" when neither axis is strictly quantitative.

When in doubt, start with a matrix — it's the most flexible and the easiest to reason about.

## Create the files

1. **Gather inputs** — date, chart name (kebab-case slug), title, description, paired analysis doc path (if any), `data:` folder (if any).
2. **Write `docs/<date>/<name>.html`** — copy the template (`templates/chart-template.html` in this skill), swap in content, update the `a.download` filename in the postMessage handler to match. Deviate from the template only for a specific reason.
3. **Write `docs/<date>/chart-<name>.md`** — `type: chart`, `chart: <name>.html`, references to the analysis doc, optional `data:` key.
4. **Rebuild the graph**:

   ```bash
   cd <root> && python3 _graph/build.py
   ```

   Confirm the output shows `Copied N chart(s) to _graph/charts` — the count should go up by one from the last build.
5. **Verify the download button works** — open `_graph/index.html`, click the new chart node, and test the `⤓` button. If nothing downloads, the postMessage listener is missing or the element ID in `html2canvas(el, ...)` doesn't match the actual root element.

## Done when

- `docs/<date>/<name>.html` exists and includes the postMessage download listener.
- `docs/<date>/chart-<name>.md` exists with `type: chart` and a matching `chart:` key.
- `python3 _graph/build.py` ran successfully and reported the new chart was copied.
- The download button produces a PNG of the chart when clicked in the viewer.
- Share both file paths with the user.
