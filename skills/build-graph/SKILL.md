---
name: build-graph
description: "Set up and build an interactive graph visualization for a folder of markdown files. Use this skill whenever the user wants to visualize relationships between documents, build or rebuild the doc graph, set up the graph viewer, or see how their documents reference each other. Also use when the user mentions 'build the graph', 'rebuild the graph', 'update the graph', 'graph viewer', 'doc graph', 'knowledge map', or wants to explore connections between notes, docs, or any collection of interlinked markdown files."
---

# Build Graph

Build and maintain an interactive graph visualization for interlinked markdown documents. The viewer renders documents as nodes on a timeline, with edges showing how documents reference each other (via a `references` field in YAML frontmatter). External URLs referenced by documents appear as separate nodes.

The result is a single `index.html` file that can be opened in any browser — no server required.

## Folder layout

The graph viewer (`_graph/`) lives at the root of the user's mounted folder. Documents live in `docs/`, and optional research data lives in `data/`:

```
<root>/                    ← the folder the user mounted
├── _graph/                ← graph viewer lives here
│   ├── build.py
│   ├── index.html
│   └── graph.json
├── docs/                  ← all documents go here
│   ├── 2026-03-01/
│   │   └── doc-kickoff.md
│   └── 2026-04-02/
│       └── review-proposal.md
└── data/                  ← research data folders (optional)
    └── product-competitors/
        ├── source1.md
        ├── source2.md
        └── facts.csv
```

`build.py` scans `docs/` for documents and `data/` for research nodes. Directories starting with `_` or `.` are skipped.

## When to use this skill

- User wants to visualize their documents as a graph
- User wants to set up the graph viewer for the first time
- User says "rebuild the graph" or "update the graph"
- User asks to see how their docs connect or reference each other

## Bootstrapping into a new folder

The plugin expects three sibling directories at the root of the user's mounted folder: `_graph/`, `docs/`, and `data/`. If any are missing, create them before building. This layout is a hard requirement — documents outside `docs/` and research folders outside `data/` will not be picked up.

### Step 1: Create the directories

```bash
mkdir -p <root>/_graph <root>/docs <root>/data
```

`data/` is created even if empty so the user has a clear place to drop research folders later.

### Step 2: Copy the scripts

This skill bundles two files:

- `scripts/build.py` — copy to `<root>/_graph/build.py`
- `scripts/index.html` — copy to `<root>/_graph/index.html`

Use the Read tool to read each file from this skill's `scripts/` directory, then use Write to place them in the target `_graph/` folder.

### Step 3: Run the initial build

```bash
cd <root> && python3 _graph/build.py
```

This scans all `.md` files under `docs/`, extracts frontmatter, and embeds the graph data directly into `index.html`. The output tells you how many docs and references it found.

### Step 4: Open it

The user can open `_graph/index.html` directly in a browser. No server needed.

## Rebuilding after changes

Whenever documents are added, edited, or their frontmatter changes:

```bash
cd <root> && python3 _graph/build.py
```

The build is fast (pure Python, no dependencies) and idempotent.

## The frontmatter contract

For a markdown file to appear in the graph, it should have YAML frontmatter:

```yaml
---
name: Human Readable Title
description: One-sentence summary
date: YYYY-MM-DD
type: doc
references:
  - https://example.com/some-page
  - 2026-04-02/other-doc.md
data: product-competitors
notion_id: 330328e8e3f78043ba1fed7955d00b11
---
```

Field details:

- **name** (recommended): Display label in the graph. Falls back to the filename if missing.
- **date** (recommended): Determines which timeline lane the node appears in. Documents with the same date share a lane.
- **type** (optional): Drives the node's color and icon. Six recognized types:
  - `doc` (default, blue) — dated timeline entry. Analysis, synthesis, brief, draft, working notes all collapse here.
  - `review` (amber) — critique or review of another doc or page. Never synced to Notion.
  - `guide` (rose) — how-to / process / style. Pinned in the top strip.
  - `ref` (bronze) — what-is / canonical domain context. Pinned in the top strip, often Notion-synced.
  - `chart` (teal) — visualization paired with a parent doc via the `chart:` key. Opens in a full-screen overlay.
  - `research` (red) — auto-generated from each folder under `data/`, not usually set by hand.

  Unknown types get default gray.
- **description** (optional): Shown in the side panel.
- **references** (optional): A YAML list of URLs or relative file paths. Each becomes a directed edge. External URLs are rendered as "external" nodes. Relative paths are matched by suffix.
- **data** (optional): Links the doc to a research folder in `data/<value>/`. Creates an edge to the research node in the graph. The research node shows source file count and facts from `facts.csv`.
- **notion_id** (optional): 32-char hex ID (or dashed UUID) of the Notion page this doc mirrors. Adds a Notion-sync indicator to the node and a "Synced" section in its panel. Use on `ref` and `guide` when the doc is the local copy of a Notion page; never on `review`.
- **chart** (required on `type: chart`): Filename of the HTML chart in the same date folder (e.g. `chart: competitive-landscape.html`).

Files without frontmatter are still included as type `doc`.

## Multi-project support

The viewer handles two layouts automatically:

**Single-project** (date folders directly under `docs/`):
```
docs/
├── 2026-03-01/
│   └── doc-kickoff.md
└── 2026-04-02/
    └── review-proposal.md
```

**Multi-project** (project folders containing date folders):
```
docs/
├── project-alpha/
│   └── 2026-03-01/
│       └── doc-alpha-kickoff.md
└── project-beta/
    └── 2026-03-15/
        └── doc-beta-audit.md
```

## Customization

- **Add a document type**: Find the `TYPE_STYLES` object in index.html
- **Change colors**: CSS variables in the `<style>` block
- **Adjust spacing**: Layout constants at the top of the `<script>` block

## Troubleshooting

- **"No docs/ folder found"**: Create `docs/` or pass a path: `python3 _graph/build.py /path/to/docs`
- **"0 docs found"**: Make sure markdown files are inside `docs/`, not at the root level
- **Documents not linking**: References use suffix matching — check that reference paths match actual file paths
- **Blank viewer**: Check browser console for JS errors, then rerun `python3 _graph/build.py`
