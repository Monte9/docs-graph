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
<root>/data/competitors/<slug>.md
```

where `<root>` is the folder the user mounted (in Cowork) or the current working directory (in a terminal). Resolve `<root>` at runtime — do not hardcode a machine-specific path in the skill. If `<root>/data/competitors/` does not exist yet, create it.

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

Follow the Recommended Doc Structure section in the reference doc for the body. Every factual claim must be verifiable against the "References & Sources" section at the bottom of the body.

## Step 5: Report

Summarize to the user:

- Competitor researched
- Path to the new doc: `<root>/data/competitors/<slug>.md`
- Any dimensions where data was unavailable (noted as "unknown" or "N/A")
- Any follow-ups (e.g., manual product screenshots)

## Done checklist

The skill's deliverable is local-only. A run is considered done when `<root>/data/competitors/<slug>.md` exists and meets the Done check in the reference doc.

**Do not push the doc to Notion as part of this skill.** If the frontmatter
includes a `notion_id`, the user (or a separate sync skill) may later push
the doc upstream; this skill does not. If no `notion_id` is present, any
Notion sync is a manual follow-up and not part of this skill's contract.

## Incremental runs

If `<root>/data/competitors/<slug>.md` already exists, ask the user whether to refresh it or leave it alone. Do not silently overwrite.

## Parallel runs

This skill is safe to run in parallel across multiple sessions. Each run writes to a different `<slug>.md` file, so there is no contention on the filesystem. Any post-processing that touches shared state (e.g., rebuilding a graph index, syncing to Notion, updating aggregate reports) is intentionally out of scope for this skill and must be run once, serially, after the batch of parallel research runs has finished.

## Principle

Everything about *what* and *how* to research lives in the reference doc. This skill only handles *when* and *where*. If the research approach needs to change, update the reference doc, not this skill.
