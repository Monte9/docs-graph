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

Before looking at chart shapes, write down the **one question** this dimension's chart should answer in plain English. A dimension is a topic (e.g. "access model"); a question is a read (e.g. "can a solo therapist sign up today?"). Without a crisp question, the chart becomes a 24-row data table disguised as a visualization. With one, the chart shape usually picks itself. See the "Anchor on the question first" section in `create-chart/SKILL.md` for the full rationale.

Proven examples from this system:

- Compliance → "Who holds third-party-audited HIPAA?" → 4-tier heatmap.
- Pricing → "How much does it cost to get started?" → log-axis dot strip with segment bands.
- Access Model → "Can a solo therapist sign up today?" → binary two-column split.

With the question pinned down, read the extracted data and look for the shape that fits:

- **Binary / two-column** — if the question is a yes/no and the secondary texture (why, how much) can live in a hover tooltip. Simplest and most legible.
- **Discrete states or tiers** — does the data split into 2-5 natural clusters (audited / self-attested / none; free / per-seat / per-session; heavy / moderate / light)? A heatmap or tier-coded matrix reads naturally.
- **Continuous axes** — are there one or two things varying at once that plot as a scatter or dot strip (price on a log axis, ai-usage × clinical-visibility)?
- **Count or breadth** — does the dimension reduce to "how much of X" per competitor (library size, feature count)? A bar chart or ranked list is clearest.
- **Flow / process** — is the dimension actually a sequence or workflow? A process diagram, not a matrix.
- **Flat / thin signal** — if 20 of 24 competitors have basically the same value, the chart might be a small outlier callout instead of a full matrix. Don't manufacture structure that isn't there.
- **Named evidence** — which 2-3 specific competitors anchor each cluster? Those names go straight into the key-insight bullets.
- **Outliers / whitespace** — anyone unusual in a way that's competitively relevant for Rosebud.

The shape should fall out of the question + data, not get imposed. Compliance landed on a 4-tier heatmap because the data bifurcated into audited/self-attested/inherited/none. Access model landed on a binary split because the question was literally "can they sign up today?" — yes or no. Let each dimension produce its own shape.

**Resist over-encoding.** When the data has many attributes, the instinct is to encode them all (position + color + glyph + band + label). The result reads like a spreadsheet. Pick the single attribute that answers the one question; everything else goes in the hover or the analysis doc.

**Don't default to chip clusters.** A multi-column layout of chips (one column per category, chips inside) is easy to produce and almost always wrong when the data has continuous or quantitative attributes (funding amounts, counts, ratings, years, prices). Chip clusters only earn their keep when the answer is *purely categorical* and the categories themselves are the read (e.g. "which of 5 messaging buckets do they sit in"). If the data has numbers, the chart wants an axis — use a dot strip, bar, or scatter, not chips.

### When a dimension is composite (multiple charts)

The default is **one chart per dimension**. This keeps the one-question discipline intact and the final report scannable.

A **second chart** is justified only when both of these hold:

1. The second question is **orthogonal** to the first — it can't be collapsed into a hover tooltip or a column on the primary chart.
2. The second question is **competitively meaningful** — a distinct strategic read, not additional texture.

Examples where a second chart earns its keep:

- **Pricing** — "How much to get started?" (entry-price dot strip) is orthogonal to "Who offers a meaningful free tier?" (9 advertise free, only 2 let you run a real practice for free). Different reads, different implications.
- **How AI Is Used (#11)** — client-facing AI and back-office AI are structurally different products. One chart per axis is honest; forcing both into one visual loses the distinction.
- **Customer Pain Points (#16)** — average rating (reception signal) and thematic complaint clustering (product-gap signal) are independent reads that drive different conclusions.

When shipping two charts:

- **Primary**: `<dimension>-landscape.html` — the headline read.
- **Secondary**: `<dimension>-<question-slug>.html` (e.g. `pricing-free-tier.html`, `ai-capabilities-back-office.html`). Each needs its own `chart-<slug>.md` doc.
- The **analysis doc** references both and labels which answers which question.
- The **report doc** dimension section has one image block per chart, in primary-then-secondary order.

If you find yourself reaching for a **third chart**, stop. Three usually means one of two things: the dimension is too broad and should be split, or two of the three questions collapse into each other under closer inspection. Force the discipline; don't ship three.

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

<1-2 sentence synthesis of the dominant pattern. Name the pattern directly — don't hedge. If the data splits into two groups, say so. If it's flat, say that too. Do NOT prefix this paragraph with "Overview:" or a "## Overview" header — the dimension title is already the orientation.>

- <Key insight #1, with 2-3 named competitors as evidence>
- <Key insight #2, with 2-3 named competitors as evidence>

## The 24-competitor matrix

<The full 24-row data table. Columns reflect the attributes the dimension actually breaks into — don't pad columns for symmetry. Keep coding consistent and legend-able.>

## <Optional: Tier / cluster breakdown>

<Include only if the data warrants grouped tiers. For each cluster, name the members and the one or two things that justify grouping them.>

## <Optional: Patterns and whitespace>

<What does the pattern imply? Where's the Rosebud whitespace, if any? Skip this section if nothing substantive surfaced.>
```

**Style rules for the overview + bullets — follow Start Simple:**

The overview and bullets are the part of the report people actually read. Write them at the speed of the reader, not the speed of the LLM. See `docs/2026-04-09/note-start-simple.md` (Notion: [Start Simple](https://www.notion.so/rosebudjournal/Start-Simple-33d328e8e3f780778745e432e6c21de7)) for the full framing. Applied here:

- **No "Overview:" label.** The dimension heading is the orientation; don't preface the synthesis paragraph with `**Overview**:`, `## Overview`, or similar. Just write the sentence.
- **Each dimension has one point.** The synthesis paragraph states it in plain English. If you're stating two things, pick one.
- **Plain words, not LLM words.** Ban: "bifurcates", "structurally", "landscape", "posture", "watershed", "proxy for value", "monetization shape", "GTM", "procurement", "axes", "pervasive but shallow", "uniformly sales-gated", "inventory matched to", "consumer-acquires / enterprise-monetizes", and anything that reads like a McKinsey slide. Say "splits into two", "most", "real audits", "who you sell to decides", "small slice", "all need a sales call".
- **Shorter is better.** Overview = 1-2 short sentences. Bullets = 1-2 short sentences each with a bolded one-line headline. If you can cut a word, cut it. If you can cut a clause, cut it.
- **Name the evidence.** Bullets name specific companies. "Most competitors do X" is weaker than "Healthie, Lyra, and SimplePractice do X; the other 21 don't." Keep the list short — three names is usually enough.
- **3 bullets is the target, 4 is the ceiling.** If you need 5, one is filler — cut or merge.
- **Don't pad with "Rosebud positioning"** unless the implication is sharp. A paragraph that hedges is worse than no paragraph.

**Bad vs. good phrasing:**

| Avoid (LLM-ish) | Prefer (plain) |
| --- | --- |
| "Access mode bifurcates on one practitioner-relevant question" | "10 of 24 let a solo therapist sign up today." |
| "Enterprise is uniformly sales-gated" | "Enterprise plays all need a sales call." |
| "Third-party audit is the watershed" | "Real audits are rare." |
| "Entry price is not a proxy for value" | "Headline price isn't where the value sits." |
| "GTM dictates posture" | "Who you sell to decides what audits you get." |
| "Dual-surface is usually consumer-acquires, enterprise-monetizes" | "The consumer app draws users; the enterprise contract pays the bills." |
| "Marketplace is the rarest model and the heaviest gate" | "Marketplaces treat therapists as supply — heaviest credentialing in the set." |

**The detailed tier breakdown section can stay precise and technical** — that's where numbers, SKU names, auditor names, and full company lists live. Start Simple applies to the overview and bullets, not the underlying matrix.

## Step 4 — Create the chart

Use the **create-chart** skill. The handoff contract: **name the chart type explicitly** and pass the decision, not the ambiguity. `create-chart` is a faithful renderer — it builds what you ask for. If you don't name a specific shape, it has no way to push back on a bad choice.

Pass it:

- The dimension slug and title
- The **named chart type** — one of: `binary two-column`, `matrix/heatmap`, `dot strip` (with axis: linear or log), `positioning scatter` (with both axes named), `bar / ranked list`, `process/flow`, `landscape map`, or `chip cluster` (only if the data is purely categorical — see the "Don't default to chip clusters" rule in step 2)
- The **one question** the chart answers, stated in plain English (same phrasing you anchored on in step 2)
- The data you extracted (or the synthesized tier/cluster structure if that's what the chart encodes)
- A brief note on what hover/tooltip should reveal per cell or point

If you can't name the chart type in one of the categories above, go back to step 2 — the shape hasn't fallen out of the data yet.

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
