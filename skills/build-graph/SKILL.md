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
│   │   └── synthesis-kickoff.md
│   └── 2026-04-02/
│       └── analysis-review.md
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

If the user's folder doesn't have `_graph/` and `docs/` yet, create them from the bundled scripts in this skill.

### Step 1: Create the directories

```bash
mkdir -p <root>/_graph <root>/docs
```

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
type: synthesis
references:
  - https://example.com/some-page
  - 2026-04-02/other-doc.md
data: product-competitors
---
```

Field details:

- **name** (recommended): Display label in the graph. Falls back to the filename if missing.
- **date** (recommended): Determines which timeline lane the node appears in. Documents with the same date share a lane.
- **type** (optional): Drives the node's color and icon. Built-in types: `synthesis` (blue), `analysis` (purple), `comments` (amber), `brief` (teal), `draft` (olive), `note` (gray), `research` (red). Unknown types get default gray.
- **description** (optional): Shown in the side panel.
- **references** (optional): A YAML list of URLs or relative file paths. Each becomes a directed edge. External URLs are rendered as "external" nodes. Relative paths are matched by suffix.
- **data** (optional): Links the doc to a research folder in `data/<value>/`. Creates an edge to the research node in the graph. The research node shows source file count and facts from `facts.csv`.

Files without frontmatter are still included as type `note`.

## Multi-project support

The viewer handles two layouts automatically:

**Single-project** (date folders directly under `docs/`):
```
docs/
├── 2026-03-01/
│   └── synthesis-kickoff.md
└── 2026-04-02/
    └── analysis-review.md
```

**Multi-project** (project folders containing date folders):
```
docs/
├── project-alpha/
│   └── 2026-03-01/
│       └── brief-alpha-kickoff.md
└── project-beta/
    └── 2026-03-15/
        └── analysis-beta-audit.md
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
