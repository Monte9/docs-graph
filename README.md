# Docs Graph

A Claude Cowork plugin that turns a folder of markdown documents into an interactive visual graph. See how your documents connect to each other — rendered as a single HTML file you can open in any browser.

## Install

**Option A — From GitHub (recommended):**
1. In Claude Cowork, open the sidebar and click **Customize**
2. Click the **+** button next to "Personal plugins"
3. Select **Add marketplace**
4. Enter `Monte9/docs-graph` and click **Sync**
5. Go to **Plugins** in the Directory, switch to the **Personal** tab
6. Find "Docs graph" and click to install it

**Option B — Manual upload:**
1. [Download docs-graph.zip](https://github.com/Monte9/docs-graph/releases/latest/download/docs-graph.zip)
2. In Claude Cowork, open the sidebar and click **Customize**
3. Click the **+** button next to "Personal plugins"
4. Select **Upload plugin** and upload the `.zip` file

## Usage

1. Select a folder for your project (e.g. "Rosebud", "Q2 Planning", anything)
2. Ask Claude to "set up the graph viewer"
3. Write docs or ask Claude to create them for you
4. Open `_graph/index.html` in your browser

Ask Claude to "rebuild the graph" after adding or editing documents.

## How it's organized

```
your-folder/
├── _graph/           ← the viewer lives here (auto-generated)
└── docs/             ← your documents go here
    ├── 2026-03-01/
    │   └── synthesis-kickoff.md
    └── 2026-04-10/
        └── analysis-review.md
```

## Document format

Each markdown file starts with a metadata block:

```markdown
---
name: My Document Title
date: 2026-04-10
type: synthesis
description: A one-sentence summary
references:
  - https://notion.so/some-page
  - 2026-04-02/other-doc.md
---

Your content here...
```

Types: `synthesis`, `analysis`, `comments`, `brief`, `draft`, `note`. References create edges between documents in the graph.

## Packaging

```bash
./build.sh
```

Creates `docs-graph.zip` for sharing. Also auto-built on every push to `main` via GitHub Actions.

## Requirements

Python 3 and a modern web browser.

## License

MIT
