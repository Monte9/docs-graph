# Agents

This file is for AI agents working on this repo. If you're a human, see README.md.

## What this is

A Claude Cowork plugin called **docs-graph**. It has three skills:

- **create-doc** (`skills/create-doc/SKILL.md`) — creates markdown documents with YAML frontmatter in the right format for the graph viewer
- **build-graph** (`skills/build-graph/SKILL.md`) — sets up and rebuilds an interactive HTML graph viewer that visualizes documents and their references
- **rosebud-competitor-research** (`skills/rosebud-competitor-research/SKILL.md`) — researches competitors following the Rosebud competitive research system. Deliberately Rosebud-specific (mental-health practitioner tools); not intended for general-purpose competitor research

## Repo structure

```
docs-graph/
├── .claude-plugin/
│   ├── plugin.json              # plugin manifest (name, version, description)
│   └── marketplace.json         # marketplace entry (keep version in sync with plugin.json)
├── skills/
│   ├── create-doc/
│   │   └── SKILL.md             # instructions for creating docs
│   ├── build-graph/
│   │   ├── SKILL.md             # instructions for setting up/rebuilding the graph
│   │   └── scripts/
│   │       ├── build.py         # Python script that scans docs/ and generates graph data
│   │       └── index.html       # D3.js viewer template (data gets embedded by build.py)
│   └── rosebud-competitor-research/
│       ├── SKILL.md             # thin executor for Rosebud competitor research
│       └── dimensions.md        # reference doc: 19 dimensions, doc structure, writing rules
├── README.md                    # human-facing docs
├── AGENTS.md                    # this file
├── setup.sh                     # LOCAL DEV ONLY — symlinks ~/docs, ~/data into repo
├── build.sh                     # packages the plugin into a .zip file
└── .gitignore                   # excludes .plugin files, .zip, and local dev output
```

## How the folder layout works when installed

When a user installs this plugin and mounts a folder, the expected layout is:

```
<root>/                    ← whatever folder the user mounts
├── _graph/                ← graph viewer at the root level
│   ├── build.py
│   ├── index.html
│   └── graph.json
├── docs/                  ← all documents go in here
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

`_graph/`, `docs/`, and `data/` are siblings at the root. `build.py` scans `docs/` for documents and `data/` for research nodes.

## How the graph viewer works

`build.py` walks `docs/`, parses YAML frontmatter (name, date, type, references, data), and embeds the resulting JSON into `index.html` between `// __GRAPH_DATA_START__` and `// __GRAPH_DATA_END__` markers. It also scans `data/` for research folders — each subfolder becomes a `research` node that counts its source `.md` files and `facts.csv` rows. The HTML file uses D3.js to render a horizontal timeline with nodes per document and edges per reference.

The viewer is entirely self-contained — one HTML file, no server, no build tools. It persists the open side panel via URL hash, so refreshing the page retains the current panel.

## Frontmatter format

Every markdown doc should start with:

```yaml
---
name: Title
date: YYYY-MM-DD
type: synthesis|analysis|comments|brief|draft|note|research
description: One-sentence summary
references:
  - https://external-url.com
  - YYYY-MM-DD/other-doc.md
data: folder-name
---
```

`build.py` uses a simple line-based YAML parser (no PyYAML dependency). Keep frontmatter flat — no nested objects.

The `data` field is optional — it links a doc to a research folder in `data/<value>/`, creating an edge to the corresponding research node in the graph. The `research` type is automatically assigned to nodes created from `data/` folders.

## Local development

For local dev, mount **THIS repo folder** (`~/Projects/docs-graph`) in Cowork. The skills are picked up directly from `skills/` — no need to install the plugin. Edits take effect immediately.

### Prerequisites

- Python 3 (no pip deps — `build.py` is stdlib only)
- A folder of your real docs somewhere on disk (default `~/docs`); optionally a `~/data` folder for research data

### One-time setup

From the repo root:

```bash
./setup.sh                              # docs/ → ~/docs, data/ → ~/data
./setup.sh ~/other/docs                 # docs/ → custom path, data/ → ~/data
./setup.sh ~/other/docs ~/other/data    # both custom
```

`setup.sh` symlinks your real `docs/` and `data/` into the repo so you can develop against real content. Both symlinks are gitignored.

### Initial build

Bootstrap `_graph/` the same way end users do — via the `build-graph` skill, or manually:

```bash
# Manual equivalent of what the build-graph skill does:
mkdir -p _graph
cp skills/build-graph/scripts/build.py   _graph/build.py
cp skills/build-graph/scripts/index.html _graph/index.html
python3 _graph/build.py
```

Then open `_graph/index.html` in a browser. No server needed.

### Repo layout after setup

```
docs-graph/                      ← mount this folder in Cowork
├── docs/ → ~/docs               ← symlink (gitignored)
├── data/ → ~/data               ← symlink (gitignored)
├── _graph/                      ← generated output (gitignored, safe to delete)
│   ├── build.py                 ← RUN COPY — do NOT edit here
│   ├── index.html               ← RUN COPY — do NOT edit here (data is re-embedded)
│   └── graph.json
├── skills/                      ← SOURCE OF TRUTH — edit here
│   ├── build-graph/
│   │   ├── SKILL.md
│   │   └── scripts/
│   │       ├── build.py         ← template
│   │       └── index.html       ← template
│   ├── create-doc/SKILL.md
│   └── rosebud-competitor-research/
│       ├── SKILL.md
│       └── dimensions.md
└── ...
```

**Critical distinction:** `skills/build-graph/scripts/{build.py,index.html}` are the canonical templates — what ships in the plugin. `_graph/{build.py,index.html}` are run-copies that the skill writes during bootstrap. **Edits to the viewer or build script go in `skills/build-graph/scripts/`. Never edit `_graph/` directly** — your changes get overwritten the next time the skill bootstraps, and they won't ship to users.

### Edit → test loop

For viewer/build script changes:

```bash
# 1. Edit the template
$EDITOR skills/build-graph/scripts/index.html

# 2. Copy template → run copy
cp skills/build-graph/scripts/index.html _graph/index.html

# 3. Rebuild (re-embeds GRAPH_DATA)
python3 _graph/build.py

# 4. Reload _graph/index.html in the browser
```

For doc-graph behavior changes (YAML parsing, data/ scanning, etc.):

```bash
cp skills/build-graph/scripts/build.py _graph/build.py
python3 _graph/build.py
```

For skill prompt changes (SKILL.md, dimensions.md): no rebuild needed — Cowork reads them live from `skills/`.

For adding test content:
1. Use the `create-doc` skill to add docs to `docs/` (which is your `~/docs` via symlink)
2. Run `python3 _graph/build.py` to pick them up

### Blowing away local state

`_graph/` is generated output — delete it anytime and re-bootstrap. Useful if the run copies drift from the templates:

```bash
rm -rf _graph && <rerun initial build steps above>
```

### Ship it

1. Commit edits under `skills/` (and `AGENTS.md`, `README.md`, etc.)
2. `docs/`, `data/`, and `_graph/` are gitignored — only plugin source gets committed
3. Push to main → GitHub Actions builds a release → users sync the plugin

## Packaging

```bash
./build.sh
```

Creates `docs-graph.zip` at the repo root. The `.zip` file is gitignored.

## Commits and versioning

This repo uses **conventional commits**. Every commit message must follow:

```
<type>(<scope>): <description>
```

Types:
- `fix` — bug fix → bumps **patch** (1.0.0 → 1.0.1)
- `feat` — new feature → bumps **minor** (1.0.0 → 1.1.0)
- `feat!` or `BREAKING CHANGE:` — breaking change → bumps **major** (1.0.0 → 2.0.0)
- `docs` — documentation only (no version bump)
- `chore` — maintenance, CI, tooling (no version bump)
- `refactor` — code restructuring (no version bump)
- `style` — formatting, whitespace (no version bump)

Scopes: `build-graph`, `create-doc`, `viewer`, `build`, `ci`

Examples:
```
fix(viewer): prevent node overlap on chained references
feat(create-doc): add support for custom frontmatter fields
feat(build-graph)!: change docs/ to documents/ folder name
docs: update install instructions in README
chore(ci): fix release workflow permissions
```

When a commit bumps the version (`fix` or `feat`), also update:
- `.claude-plugin/plugin.json` → `version` field
- `.claude-plugin/marketplace.json` → `version` field in the plugin entry

Users who installed via marketplace sync need to re-sync to pick up changes.

## Key files to know when making changes

- **Viewer layout/styling**: `skills/build-graph/scripts/index.html` — CSS is in the `<style>` block, layout constants (COL_WIDTH, ROW_SPACING, etc.) are at the top of the `<script>` block, type colors are in the `TYPE_STYLES` object
- **Data pipeline**: `skills/build-graph/scripts/build.py` — `parse_frontmatter()` handles YAML, `scan_folder()` walks docs/, `scan_data_folder()` walks data/ for research nodes, `main()` embeds into HTML
- **Skill triggers**: the `description` field in each SKILL.md frontmatter controls when Cowork activates the skill — edit these if the skill isn't triggering when it should
