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

## Local development

For local dev, mount THIS repo folder (`~/Projects/docs-graph`) in Cowork. The skills are picked up directly from `skills/` — no need to install the plugin. You can edit skill files and scripts and changes take effect immediately.

Run the setup script first to symlink your docs into the repo:

```bash
./setup.sh              # symlinks docs/ → ~/docs (default)
./setup.sh ~/other/path # symlinks docs/ → custom path
```

After setup, the repo looks like:

```
docs-graph/                      ← mount this folder
├── docs/ → ~/docs               ← symlink to your real docs (gitignored)
├── _graph/                      ← graph output goes here (gitignored)
│   ├── build.py
│   └── index.html
├── skills/                      ← edit these directly
│   ├── build-graph/...
│   └── create-doc/...
└── ...
```

This means one folder for everything: source code, real content via symlink, and graph output. `docs/` and `_graph/` are both gitignored — only the plugin source gets committed.

### Workflow

1. Edit skill files or viewer code in `skills/`
2. Use the `create-doc` skill to add test docs to `docs/`
3. Use the `build-graph` skill to rebuild `_graph/` — or run directly: `python3 skills/build-graph/scripts/build.py`
4. Open `_graph/index.html` in a browser to verify
5. Commit changes to `skills/`, `AGENTS.md`, etc. (docs/ and _graph/ are gitignored)
6. Push to main → GitHub Actions builds a release → users sync the plugin

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
- **Data pipeline**: `skills/build-graph/scripts/build.py` — `parse_frontmatter()` handles YAML, `scan_folder()` walks the tree, `main()` embeds into HTML
- **Skill triggers**: the `description` field in each SKILL.md frontmatter controls when Cowork activates the skill — edit these if the skill isn't triggering when it should
