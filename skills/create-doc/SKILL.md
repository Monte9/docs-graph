---
name: create-doc
description: "Create a new document in the user's doc folder with the right format for the graph viewer. Use when the user asks to write a doc, add a synthesis/analysis/comments/note, capture notes, or otherwise add a markdown file to their folder. Also use when the user says 'create a doc', 'write a note', 'add a synthesis', 'capture this', or wants to save any structured markdown document. Regenerates the graph index after creation."
---

# Create Doc

Create a new markdown document in the user's folder and regenerate the graph index so it shows up in the viewer.

## Where docs live

The doc folder is whichever folder the user has mounted as their workspace. If it's not obvious which folder is the root (e.g., the mounted folder is a parent repo), ask the user to confirm the path. The general layout is:

```
<doc-root>/
├── _graph/              # graph viewer — do not put docs here
│   ├── build.py         # rebuilds graph.json + index.html
│   ├── graph.json
│   └── index.html
└── YYYY-MM-DD/          # one folder per day docs were written
    └── <type>-<slug>.md
```

Docs are grouped by date. Inside a date folder, files are named `<type>-<short-slug>.md` — for example `synthesis-q2-strategy.md`, `analysis-pricing-review.md`, `comments-okr-feedback.md`.

## Requirements

Before creating the file, make sure you know:

1. **Date** — today's date in `YYYY-MM-DD`. Use `date +%Y-%m-%d` via Bash if needed.
2. **Type** — one of `synthesis`, `analysis`, `comments`, `brief`, `draft`, `note`, or another short type that fits. This drives both the filename prefix and the frontmatter `type` field.
3. **Slug** — short kebab-case description of the topic (e.g. `q2-strategy`, `pricing-review`).
4. **Name** — human-readable title.
5. **Description** — one-sentence summary.
6. **References** — optional list of URLs (Notion pages, etc.) or relative paths to other docs that this doc relates to. These become edges in the graph.

If any of these are missing and can't be inferred from context, ask the user.

## Create the file

Path: `<doc-root>/<YYYY-MM-DD>/<type>-<slug>.md`

Create the date folder if it doesn't already exist.

The file MUST start with YAML frontmatter in this exact shape so `build.py` can parse it:

```markdown
---
name: <Human readable title>
description: <One-sentence summary>
date: <YYYY-MM-DD>
type: <synthesis|analysis|comments|brief|draft|note|...>
references:
  - <url or relative path>
  - <url or relative path>
---

# <Title>

<body content in markdown>
```

Notes on frontmatter:
- `references` must be a YAML list with `- ` items, one per line. Omit the list entirely (or leave empty) if there are no references.
- Keep keys flat — `build.py` uses a simple line-based parser and does not handle nested YAML.
- Do not add keys other than `name`, `description`, `date`, `type`, `references` unless the user asks; extras are ignored.

Write the body in normal markdown — headings, paragraphs, bullets are all fine.

## Regenerate the graph

After the file is written, check if `_graph/build.py` exists in the doc root. If it does, run:

```bash
cd <doc-root> && python3 _graph/build.py
```

This rewrites `_graph/graph.json` and re-embeds the graph data into `_graph/index.html`. Confirm the output shows the expected doc count went up by one.

If `_graph/` doesn't exist yet, let the user know they can set it up using the **build-graph** skill to get an interactive visualization of their documents.

## Done when

- New `.md` file exists at the right path with valid frontmatter.
- `python3 _graph/build.py` ran successfully and reported the new doc (if `_graph/` exists).
- Share the path to the new file with the user.
