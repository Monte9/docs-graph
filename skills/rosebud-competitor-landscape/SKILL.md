---
name: rosebud-competitor-landscape
description: "Produce a single-dimension landscape analysis across the 24 Rosebud competitors in data/competitors/ — an analysis doc with a tight overview + named-evidence bullets, paired with a chart that renders the pattern. Use whenever the user says things like 'analyze the X dimension', 'do the next dimension', 'compile trends for X across competitors', 'build the landscape for Y', 'what does the landscape look like for Z', or 'let's do <dimension_name> next'. Also use iteratively — one dimension at a time — when building toward the full landscape report. Chart type is a deliberate judgment call based on the shape of the data, not a fixed template. Delegates file creation to create-doc and create-chart; this skill owns the data extraction and the pattern synthesis."
---

# Rosebud Competitor Landscape

For a single dimension of the Rosebud competitive research system, produce an analysis doc + chart pair that shows how the 24 competitors compare. The skill does three things: extracts the dimension data, synthesizes the pattern, and produces the paired output files via `create-doc` + `create-chart`. The chart shape is a judgment call based on what the data actually looks like — resist forcing a template onto data that doesn't want it.

## Inputs

- **Dimension** — one `field_name` from the 20 dimensions defined in `skills/rosebud-competitor-research/dimensions.md` (e.g. `compliance`, `pricing_model`, `how_ai_is_used`, `in_product_content`). Ask the user if they haven't picked one.
- **Source data** — the 24 research files under `data/competitors/*.md`. Each file has:
  - A snapshot table near the top with rows like `| <field_name> | <short value> |`
  - A fuller section further down titled `### <Dimension Title>` with the bullet-level detail

## Step 1 — Extract the raw data

Pull the dimension's snapshot row from every competitor in a single bash pass:

```bash
cd <root>/data/competitors && for f in *.md; do
  echo "=== ${f%.md} ==="
  grep -E "^\| <field_name> " "$f" | head -1
done
```

If a snapshot is thin on detail, pull the fuller section for that competitor:

```bash
awk '/^### <Dimension Title>/,/^### [^<]|^## /' <slug>.md
```

The goal is a structured list of `competitor → value(s)` — typically 1-4 attributes per competitor. Don't over-extract; too many attributes make the chart noisy and the bullets unfocusable.

## Step 2 — Synthesize (this is the judgment step)

Read the extracted data and look for the shape that's actually there:

- **Discrete states or tiers** — does the data split into 2-5 natural clusters (audited / self-attested / none; free / per-seat / per-session; heavy / moderate / light)? If yes, a heatmap or tier-coded matrix will read naturally.
- **Continuous axes** — are there two things varying at once that plot as a scatter (price × target user, ai-usage-intensity × clinical-visibility)?
- **Count or breadth** — does the dimension reduce to "how much of X" per competitor (library size, feature count)? A bar chart or simple ranked list is clearest.
- **Flow / process** — is the dimension actually a sequence or workflow? A process diagram, not a matrix.
- **Flat / thin signal** — if 20 of 24 competitors have basically the same value, the chart might be a small outlier callout instead of a full matrix. Don't manufacture structure that isn't there.
- **Named evidence** — which 2-3 specific competitors anchor each cluster? Those names go straight into the key-insight bullets.
- **Outliers / whitespace** — anyone unusual in a way that's competitively relevant for Rosebud.

The compliance pilot landed on a 4-tier heatmap because the data cleanly bifurcated into audited/self-attested/inherited/none. That pattern fell out of the data; it wasn't imposed. Let each dimension produce its own shape.

## Step 3 — Create the analysis doc

Use the **create-doc** skill (or follow its frontmatter contract) to write:

```
docs/<YYYY-MM-DD>/analysis-<dimension-slug>-landscape.md
```

The doc shape is prescriptive — this part stays stable across dimensions so the eventual full report reads consistently:

```markdown
---
name: <Dimension Title> Landscape
description: <one-line summary of what this landscape shows>
date: <YYYY-MM-DD>
type: analysis
chart: <dimension-slug>-landscape.html
data: competitors
references:
  - <YYYY-MM-DD>/chart-<dimension-slug>-landscape.md
---

# <Dimension Title> Landscape

## Overview

<1-2 sentence synthesis of the dominant pattern. Name the pattern directly — don't hedge. If the data bifurcates, say so. If it's flat, say that too.>

- <Key insight #1, with 2-3 named competitors as evidence>
- <Key insight #2, with 2-3 named competitors as evidence>

## The 24-competitor matrix

<The full 24-row data table. Columns reflect the attributes the dimension actually breaks into — don't pad columns for symmetry. Keep coding consistent and legend-able.>

## <Optional: Tier / cluster breakdown>

<Include only if the data warrants grouped tiers. For each cluster, name the members and the one or two things that justify grouping them.>

## <Optional: Patterns and whitespace>

<What does the pattern imply? Where's the Rosebud whitespace, if any? Skip this section if nothing substantive surfaced.>
```

**Style rules for the overview + bullets:**

- Overview is 1-2 sentences. If you need three, one of them is filler — delete it.
- Bullets name specific companies. "Most competitors do X" is weaker than "Healthie, Lyra, and SimplePractice do X; the other 21 don't."
- Don't pad with "Rosebud positioning" sections unless the implication is sharp. A paragraph that hedges is worse than no paragraph.

## Step 4 — Create the chart

Use the **create-chart** skill. Pass it:

- The dimension slug and title
- The data you extracted (or the synthesized tier/cluster structure if that's what the chart encodes)
- Your judgment on chart type (heatmap, scatter, bar, flow, landscape map — whatever the data shape called for in step 2)
- A brief note on what hover/tooltip should reveal per cell or point

`create-chart` handles the template, the visual vocabulary, the iframe postMessage download listener, and the paired `chart-<slug>-landscape.md` doc. This skill stays out of chart mechanics — trust the lower-level skill to do its job.

## Step 5 — Rebuild the graph

```bash
cd <root> && python3 _graph/build.py
```

Confirm two new nodes appeared (`analysis-<slug>-landscape.md` and `chart-<slug>-landscape.md`), both edge-linked to the `competitors` research node via the `data:` key, and that `Copied N chart(s)` went up by one.

## Done when

- `docs/<date>/analysis-<slug>-landscape.md` exists with overview + named-evidence bullets + data table.
- `docs/<date>/chart-<slug>-landscape.md` and its `.html` exist via create-chart, with a working download button.
- `python3 _graph/build.py` ran and the new nodes show up in the viewer.
- Share both file paths with the user plus a one-sentence summary of the pattern found (so they can eyeball before moving on).

## Scaling to the full landscape report

Once each of the 20 dimensions has its own analysis + chart pair, the full report becomes a synthesis across them. Things to watch for as the set fills in:

- **Dimensions that correlate** — e.g. compliance tier ↔ pricing tier ↔ target buyer. When correlation shows up, the final report can collapse two dimensions into one combined view.
- **Repeat-outlier competitors** — same 2-3 names surfacing as outliers across many dimensions usually means they're a distinct strategic cluster worth naming.
- **Flat dimensions** — if a dimension produced a thin chart and a one-bullet analysis, consider merging it into an adjacent dimension in the final report rather than giving it its own section.

A cross-dimension synthesis doc (`type: synthesis`) can reference all 20 analysis docs once they exist. That's where the "whole report" comes together.

## References

- **Dimension list and field_names**: `skills/rosebud-competitor-research/dimensions.md`
- **Proven pattern example** (compliance pilot): `docs/2026-04-17/analysis-compliance-landscape.md` + `chart-compliance-landscape.md` + `compliance-landscape.html`
- **Lower-level skills this calls into**: `create-doc`, `create-chart`
