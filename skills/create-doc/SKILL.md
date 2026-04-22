---
name: create-doc
description: "Create a new document in the user's docs folder with the right format for the graph viewer. Use when the user asks to write a doc, add a guide, capture a reference, save a review/critique, add a review of a Notion page, or otherwise add a markdown file to their folder. Also use when the user says 'create a doc', 'write a note', 'capture this', 'add a guide', 'add a ref', 'review this page', or wants to save any structured markdown document. Regenerates the graph index after creation."
---

# Create Doc

Create a new markdown document in the user's `docs/` folder and regenerate the graph index so it shows up in the viewer.

## Folder layout

Documents live in a `docs/` subdirectory of the user's mounted folder:

```
<root>/                    ← the folder the user mounted
├── _graph/                ← graph viewer (don't put docs here)
└── docs/                  ← all documents go here
    └── YYYY-MM-DD/
        └── <type>-<slug>.md
```

If `docs/` doesn't exist yet, create it.

Docs are grouped by date. Inside a date folder, files are named `<type>-<short-slug>.md` — for example `doc-q2-strategy.md`, `review-pricing-proposal.md`, `guide-tone-and-style.md`.

## Types — pick the right one

The graph recognizes six doc types. Most new docs are `doc`. Use the others only when they genuinely fit.

| Type | When to use | Notion sync | Where it appears |
|---|---|---|---|
| **doc** | Default. Dated timeline entry — analysis, synthesis, brief, draft, working notes. | Optional | Timeline |
| **review** | A critique or review of another doc, page, or proposal. Explicitly NOT synced to Notion — this is our take on something, not a canonical artifact. | Never | Timeline |
| **guide** | How-to, process, or style. Canonical, reusable across many docs (e.g. tone guide, a research process, a scope-discipline writeup). | Optional | Pinned in top strip |
| **ref** | What-is / reference material. Canonical domain context that other docs link to (e.g. product overview, segmentation definitions, kickoff-level framing). | Usually | Pinned in top strip |
| **chart** | A visualization paired with a parent doc. The parent doc gets a chart badge; the chart opens in full-screen overlay. | Never | Paired to parent |

Quick decision rules:
- If the user says "review this Notion page about X" or "critique this proposal" → **review**.
- If the user says "add a guide on how we write / do X" → **guide**.
- If the user says "add a ref for what X is" / "capture the definition of X" → **ref**.
- If the user is dropping in a data visualization meant to accompany another doc → **chart**.
- Everything else (analysis, synthesis, working brief, draft, meeting notes) → **doc**.

When in doubt, default to `doc`. The old taxonomy (synthesis, analysis, comments, brief, draft, note) all collapses into `doc`.

## Requirements

Before creating the file, make sure you know:

1. **Date** — today's date in `YYYY-MM-DD`. Use `date +%Y-%m-%d` via Bash if needed.
2. **Type** — one of `doc`, `review`, `guide`, `ref`, `chart` (see the table above).
3. **Slug** — short kebab-case description of the topic (e.g. `q2-strategy`, `pricing-review`).
4. **Name** — human-readable title.
5. **Description** — one-sentence summary.
6. **References** — optional list of URLs (Notion pages, etc.) or relative paths to other docs that this doc relates to. These become edges in the graph.
7. **Notion sync target** (optional) — if this doc is the local copy of a specific Notion page, capture its `notion_id`. See "Notion sync" below.

If any of these are missing and can't be inferred from context, ask the user.

## Default guide references

Every new doc should reference the two foundational guides so every piece of writing inherits the shared scope and voice:

- `2026-04-09/guide-start-simple.md` — scope discipline (one point, one page, MVP over perfection)
- `2026-04-22/guide-tone-and-style.md` — voice rules (no em-dashes, no filler, plain words, short sentences)

Add both to the `references:` list by default. The only exception is when writing one of the guides themselves (to avoid a self-reference). The user can remove them after the fact if a specific doc should stand outside the shared style, but the default is to include them.

## Reviews — extra rules

A `review` is our critique of another artifact (a Notion page, a proposal, a competitor doc, another markdown doc). Keep these rules in mind:

- **Never** set a `notion_id` on a review. A review is our take, not the thing being reviewed.
- The thing being reviewed belongs in `references:`. If the user gave you a Notion URL, add that URL as a reference. If it's another local doc, use the relative path.
- The slug should name what's being reviewed, not the act of reviewing (e.g. `review-pseudonymization-proposal.md`, not `review-my-thoughts.md`).
- The body should lead with the specific claim or document being reviewed, then move into what holds up, what doesn't, and what would change your mind.

## Notion sync (ref and guide only)

If the doc is the local copy of a Notion page — meaning the Notion page and this doc are kept in sync — add a `notion_id:` frontmatter field. The graph will show a Notion-sync indicator on the node and a "Synced" section in its panel.

- Extract the 32-character hex ID from a Notion URL (e.g. `https://www.notion.so/workspace/Title-330328e8e3f78043ba1fed7955d00b11` → `notion_id: 330328e8e3f78043ba1fed7955d00b11`).
- Only set `notion_id` when the user confirms this doc mirrors that page.
- Regular Notion links that just appear as references (not sync targets) stay in the `references:` list.

## Create the file

Path: `<root>/docs/<YYYY-MM-DD>/<type>-<slug>.md`

Create the date folder if it doesn't already exist.

The file MUST start with YAML frontmatter in this exact shape so `build.py` can parse it:

```markdown
---
name: <Human readable title>
description: <One-sentence summary>
date: <YYYY-MM-DD>
type: <doc|review|guide|ref|chart>
references:
  - 2026-04-09/guide-start-simple.md
  - 2026-04-22/guide-tone-and-style.md
  - <any additional urls or relative paths>
---

# <Title>

<body content in markdown>
```

The first two references are the default foundational guides (see "Default guide references"). Skip them only when writing one of the guides itself.

Notes on frontmatter:
- `references` must be a YAML list with `- ` items, one per line. Omit the list entirely (or leave empty) if there are no references.
- `data:` is an optional field that links the doc to a research folder in `data/<value>/`. This creates an edge to the research node in the graph. Example: `data: product-competitors` links to `data/product-competitors/`.
- `notion_id:` is an optional field that marks this doc as synced to a specific Notion page (see "Notion sync" above). Use on `ref` and `guide` types; never on `review`.
- `chart:` is required on `type: chart` docs and points to the chart HTML file (e.g. `chart: 2026-04-12/chart-competitive-landscape.html`).
- Keep keys flat — `build.py` uses a simple line-based parser and does not handle nested YAML.
- Do not add keys other than `name`, `description`, `date`, `type`, `references`, `data`, `notion_id`, `chart` unless the user asks; extras are ignored.

Write the body in normal markdown — headings, paragraphs, bullets are all fine.

## Regenerate the graph

After the file is written, check if `_graph/build.py` exists at the root. If it does, run:

```bash
cd <root> && python3 _graph/build.py
```

This rewrites `_graph/graph.json` and re-embeds the graph data into `_graph/index.html`. Confirm the output shows the expected doc count went up by one.

If `_graph/` doesn't exist yet, let the user know they can set it up using the **build-graph** skill to get an interactive visualization of their documents.

## Done when

- New `.md` file exists at the right path with valid frontmatter.
- `python3 _graph/build.py` ran successfully and reported the new doc (if `_graph/` exists).
- Share the path to the new file with the user.
