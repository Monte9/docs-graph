# Agents

This file is for AI agents working on this repo. If you're a human, see README.md.

## What this is

A Claude Cowork plugin called **docs-graph**. It has two skills:

- **create-doc** (`skills/create-doc/SKILL.md`) — creates markdown documents with YAML frontmatter in the right format for the graph viewer
- **build-graph** (`skills/build-graph/SKILL.md`) — sets up and rebuilds an interactive HTML graph viewer that visualizes documents and their references

## Repo structure

```
docs-graph/
├── .claude-plugin/plugin.json   # plugin manifest (name, version, description)
├── skills/
│   ├── create-doc/
│   │   └── SKILL.md             # instructions for creating docs
│   └── build-graph/
│       ├── SKILL.md             # instructions for setting up/rebuilding the graph
│       └── scripts/
│           ├── build.py         # Python script that scans docs/ and generates graph data
│           └── index.html       # D3.js viewer template (data gets embedded by build.py)
├── README.md                    # human-facing docs
├── AGENTS.md                    # this file
├── build.sh                     # packages the plugin into a .plugin file
└── .gitignore                   # excludes .plugin files and .DS_Store
```

## How the folder layout works when installed

When a user installs this plugin and mounts a folder, the expected layout is:

```
<root>/                    ← whatever folder the user mounts (e.g. "Rosebud")
├── _graph/                ← graph viewer at the root level
│   ├── build.py
│   ├── index.html
│   └── graph.json
└── docs/                  ← all documents go in here
    ├── 2026-03-01/
    │   └── synthesis-kickoff.md
    └── 2026-04-02/
        └── analysis-review.md
```

`_graph/` and `docs/` are siblings at the root. `build.py` scans `docs/` by default (the sibling directory).

## How the graph viewer works

`build.py` walks `docs/`, parses YAML frontmatter (name, date, type, references), and embeds the resulting JSON into `index.html` between `// __GRAPH_DATA_START__` and `// __GRAPH_DATA_END__` markers. The HTML file uses D3.js to render a horizontal timeline with nodes per document and edges per reference.

The viewer is entirely self-contained — one HTML file, no server, no build tools.

## Frontmatter format

Every markdown doc should start with:

```yaml
---
name: Title
date: YYYY-MM-DD
type: synthesis|analysis|comments|brief|draft|note
description: One-sentence summary
references:
  - https://external-url.com
  - YYYY-MM-DD/other-doc.md
---
```

`build.py` uses a simple line-based YAML parser (no PyYAML dependency). Keep frontmatter flat — no nested objects.

## Development workflow

1. Edit skill files or viewer code
2. Test by running `python3 skills/build-graph/scripts/build.py /path/to/some/docs` against a folder with markdown files
3. Run `./build.sh` to package into `docs-graph.plugin`
4. The `.plugin` file is a zip — open it in Cowork to install

## Packaging

```bash
./build.sh
```

Creates `docs-graph.plugin` at the repo root. The `.plugin` file is gitignored.

## Key files to know when making changes

- **Viewer layout/styling**: `skills/build-graph/scripts/index.html` — CSS is in the `<style>` block, layout constants (COL_WIDTH, ROW_SPACING, etc.) are at the top of the `<script>` block, type colors are in the `TYPE_STYLES` object
- **Data pipeline**: `skills/build-graph/scripts/build.py` — `parse_frontmatter()` handles YAML, `scan_folder()` walks the tree, `main()` embeds into HTML
- **Skill triggers**: the `description` field in each SKILL.md frontmatter controls when Cowork activates the skill — edit these if the skill isn't triggering when it should
