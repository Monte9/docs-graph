---
name: rosebud-competitor-research
description: "Research a competitor following the Rosebud competitive research system (mental-health practitioner tools). Use when a Rosebud team member says 'research <competitor>', 'analyze <competitor>', 'competitive research on X', 'research wysa', 'research quenza', or similar. Delegates to the dimensions reference doc — all research instructions (what to measure, how to structure the writeup, voice rules) live there. Rosebud-specific: not intended for general-purpose competitor research."
---

# Rosebud Competitor Research

This skill is a thin executor. The knowledge lives in the reference doc.

## Step 1: Read the reference doc

Read `dimensions.md` in this skill's folder. It is the single source of truth for:

- What to research (19 dimensions across strategic, product, content categories)
- How to structure each competitor doc
- Voice and data-integrity rules

## Step 2: Identify the competitor

Ask the user which competitor to research, or accept one from the request (e.g., "research wysa"). If the user is unsure, point them to the [Competitor list in Notion](https://www.notion.so/rosebudjournal/Competitor-list-defined-33d328e8e3f780e0aa7fd1c0a42b73d4) referenced in the dimensions doc.

Use a kebab-case slug for the competitor (e.g., `wysa`, `simple-practice`, `spring-health`).

## Step 3: Research the competitor

Do the web research per the rules in the reference doc. Follow the Research Checklist at the bottom of that doc (practitioner subdomain check, app store check, review site check, PubMed check, AI safety page check).

## Step 4: Write the doc

Write the competitor writeup to:

```
data/competitors/<slug>.md
```

Frontmatter (keep minimal — do NOT add a `references:` key; URLs live in the body's "References & Sources" section only):

```yaml
---
name: <Competitor Display Name>
date: <YYYY-MM-DD>
type: research
description: <one-sentence summary>
# Optional — only if a corresponding Notion page already exists and the user
# wants to enable future sync. Leave out otherwise.
# notion_id: <notion-page-id>
---
```

Follow the Recommended Doc Structure section in the reference doc for the body. Every factual claim must trace to a numbered entry in the "References & Sources" section at the bottom of the body.

## Step 5: Rebuild the graph

If `_graph/build.py` exists, rebuild so the new competitor doc shows up as a node:

```bash
python3 _graph/build.py
```

## Step 6: Report

Summarize to the user:

- Competitor researched
- Path to the new doc: `data/competitors/<slug>.md`
- Any dimensions where data was unavailable (noted as "unknown" or "N/A")
- Any follow-ups (e.g., manual product screenshots)

## Done checklist

The skill's deliverable is local-only. A run is considered done when:

1. `data/competitors/<slug>.md` exists and meets the Done check in the reference doc.
2. `python3 _graph/build.py` has been re-run and the new doc shows up as a node.

**Do not push the doc to Notion as part of this skill.** If the frontmatter
includes a `notion_id`, the user (or a separate sync skill) may later push
the doc upstream; this skill does not. If no `notion_id` is present, any
Notion sync is a manual follow-up and not part of this skill's contract.

## Incremental runs

If `data/competitors/<slug>.md` already exists, ask the user whether to refresh it or leave it alone. Do not silently overwrite.

## Principle

Everything about *what* and *how* to research lives in the reference doc. This skill only handles *when* and *where*. If the research approach needs to change, update the reference doc, not this skill.
