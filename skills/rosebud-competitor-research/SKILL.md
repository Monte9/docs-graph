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
docs/competitors/<slug>.md
```

Frontmatter:

```yaml
---
name: <Competitor Display Name>
date: <YYYY-MM-DD>
type: research
description: <one-sentence summary>
references:
  - <any notion URLs or external sources>
---
```

Follow the Recommended Doc Structure section in the reference doc for the body. Every factual claim must trace to a URL in the References section.

## Step 5: Rebuild the graph

If `_graph/build.py` exists, rebuild so the new competitor doc shows up as a node:

```bash
python3 _graph/build.py
```

## Step 6: Report

Summarize to the user:

- Competitor researched
- Path to the new doc: `docs/competitors/<slug>.md`
- Any dimensions where data was unavailable (noted as "unknown" or "N/A")
- Any follow-ups (e.g., manual product screenshots)

## Incremental runs

If `docs/competitors/<slug>.md` already exists, ask the user whether to refresh it or leave it alone. Do not silently overwrite.

## Principle

Everything about *what* and *how* to research lives in the reference doc. This skill only handles *when* and *where*. If the research approach needs to change, update the reference doc, not this skill.
