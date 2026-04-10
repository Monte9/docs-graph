---
name: build-graph
description: "Set up and build an interactive graph visualization for a folder of markdown files. Use this skill whenever the user wants to visualize relationships between documents, build or rebuild the doc graph, set up the graph viewer, or see how their documents reference each other. Also use when the user mentions 'build the graph', 'rebuild the graph', 'update the graph', 'graph viewer', 'doc graph', 'knowledge map', or wants to explore connections between notes, docs, or any collection of interlinked markdown files."
---

# Build Graph

Build and maintain an interactive graph visualization for any folder of interlinked markdown documents. The viewer renders documents as nodes on a timeline, with edges showing how documents reference each other (via a `references` field in YAML frontmatter). External URLs referenced by documents appear as separate nodes.

The result is a single `index.html` file that can be opened in any browser — no server required.

## When to use this skill

- User wants to visualize a folder of markdown files as a graph
- User wants to set up or rebuild the graph viewer (`_graph/`)
- User asks to see how their docs connect or reference each other
- User mentions "rebuild the graph" or "update the graph"

## How it works

The system has two parts:

1. **`build.py`** — a Python script that walks a folder tree, parses YAML frontmatter from every `.md` file, extracts references, and writes the data into `index.html`.
2. **`index.html`** — a self-contained D3.js-powered viewer with a horizontal timeline layout, clickable nodes, a side panel with rendered markdown content, and zoom/pan navigation.

Both files live in a `_graph/` subdirectory inside the target markdown folder. The build script treats its parent directory as the document root.

## The frontmatter contract

For a markdown file to appear in the graph, it should have YAML frontmatter at the top of the file. The frontmatter fields the graph understands are:

```yaml
---
name: Human Readable Title
description: One-sentence summary
date: YYYY-MM-DD
type: synthesis
references:
  - https://example.com/some-page
  - 2026-04-02/other-doc.md
---
```

Field details:

- **name** (recommended): Display label in the graph. Falls back to the filename if missing.
- **date** (recommended): Determines which timeline lane the node appears in. Documents with the same date share a lane. If missing, the document still appears but won't be placed on the timeline cleanly.
- **type** (optional): Drives the node's color and icon. Built-in types and their colors: `synthesis` (blue), `analysis` (purple), `comments` (amber), `brief` (teal), `draft` (olive), `note` (gray). Any unknown type gets a default gray style. You can extend the type palette by editing the `TYPE_STYLES` object in index.html.
- **description** (optional): Shown in tooltips and the side panel.
- **references** (optional): A YAML list of URLs or relative file paths. Each reference becomes a directed edge in the graph. External URLs (http/https) are rendered as separate "external" nodes. Relative paths are matched against other documents in the folder by suffix (so `2026-04-02/my-doc.md` matches `project/2026-04-02/my-doc.md`).

Files without frontmatter are still included — they're treated as type `note` with the filename as the name.

## Bootstrapping the viewer into a new folder

If the target folder doesn't have a `_graph/` directory yet, you need to create it from the bundled scripts in this skill.

### Step 1: Create the directory

```bash
mkdir -p <target-folder>/_graph
```

### Step 2: Copy the scripts

This skill bundles two files:

- `scripts/build.py` — copy to `<target-folder>/_graph/build.py`
- `scripts/index.html` — copy to `<target-folder>/_graph/index.html`

Use the Read tool to read each file from this skill's `scripts/` directory, then use Write to place them in the target `_graph/` folder.

### Step 3: Run the initial build

```bash
cd <target-folder> && python3 _graph/build.py
```

This scans all `.md` files, extracts frontmatter, and embeds the graph data directly into `index.html`. The output tells you how many docs and references it found.

### Step 4: Open it

The user can open `_graph/index.html` directly in a browser. No server needed — everything is self-contained in that one file.

## Rebuilding after changes

Whenever documents are added, edited, or their frontmatter changes, rebuild:

```bash
cd <target-folder> && python3 _graph/build.py
```

The build is fast (pure Python, no dependencies) and idempotent — it overwrites the embedded data in index.html each time.

## Folder structure

The viewer expects markdown files organized under the target folder. It handles two layouts automatically:

**Single-project** (date folders at the top level):
```
my-docs/
├── _graph/
│   ├── build.py
│   ├── index.html
│   └── graph.json
├── 2026-03-01/
│   └── synthesis-kickoff.md
├── 2026-04-02/
│   └── analysis-review.md
└── README.md          ← ignored (no frontmatter with date)
```

**Multi-project** (project folders containing date folders):
```
strategy/
├── _graph/
├── project-alpha/
│   ├── 2026-03-01/
│   │   └── brief-alpha-kickoff.md
│   └── 2026-04-01/
│       └── synthesis-alpha-q2.md
└── project-beta/
    └── 2026-03-15/
        └── analysis-beta-audit.md
```

The build script detects which layout you have automatically. Directories starting with `_` or `.` are always skipped.

## Customization notes

The viewer is a single HTML file with inline CSS and JS. Common things people want to change:

- **Add a new document type**: Find the `TYPE_STYLES` object in index.html and add an entry with `color`, `icon` (SVG path), and `label`.
- **Change colors**: The CSS variables at the top of the `<style>` block control the overall palette (background, card colors, borders).
- **Adjust spacing**: Layout constants like `COL_WIDTH`, `ROW_SPACING`, `EXT_NODE_W`, etc. are defined at the top of the `<script>` block.

## Troubleshooting

- **"0 docs found"**: The build script skips directories starting with `_` or `.`. Make sure your markdown files are in regular subdirectories.
- **Documents not linking**: References use suffix matching. A reference to `foo/bar.md` matches a node whose ID ends with `foo/bar.md`. Check that the reference path in frontmatter matches the actual file's relative path from the root.
- **Blank viewer**: Open browser dev tools console. If there's a JS error about `GRAPH_DATA`, the build script didn't embed the data — rerun `python3 _graph/build.py`.
