---
name: do-research
description: "Research a topic by gathering sources and structured facts from the web. Creates a data/<topic>/ folder with per-subject source files and a shared facts.csv. Auto-creates an analysis doc if one doesn't exist. Use when the user says 'do research', 'research this', 'gather data on', 'competitive research', 'analyze competitors', or wants to build a structured research folder for any topic."
---

# Do Research

Gather web sources and structured facts for a research topic. Creates a `data/<topic>/` folder with per-subject source files and a shared `facts.csv`. If no analysis doc exists for the topic, creates one via the create-doc skill.

## Folder layout

```
<root>/
├── docs/
│   └── YYYY-MM-DD/
│       └── analysis-<topic>.md          ← auto-created, used to synthesize findings
├── data/
│   └── <topic>/
│       ├── <subject-1>.md               ← sources for subject 1
│       ├── <subject-2>.md               ← sources for subject 2
│       └── facts.csv                    ← shared structured data across all subjects
└── _graph/
```

## When to use this skill

- User asks to research a topic, gather competitive intel, or build a research folder
- User says "do research on X", "research competitors", "gather data for Y"
- User wants structured source files and a facts CSV for later analysis

## Step 1: Gather inputs interactively

Ask the user:

1. **Topic slug** — kebab-case folder name (e.g. `product-competitors`, `pricing-models`)
2. **Subjects** — who/what to research. Accept either:
   - A comma-separated list (e.g. "wysa, evolve, jimini")
   - A Notion URL — fetch the page and extract subjects from tables or lists
3. **Search context** — optional keywords to focus web searches (e.g. "therapist between-session AI product")

If the user provides all of this upfront, skip the questions and proceed.

## Step 2: Create folder structure

```bash
mkdir -p <root>/data/<topic>
```

If `facts.csv` doesn't exist yet, create it with headers:

```csv
subject,category,key,value,detail,source_id
```

**Category values:**
- `primitive` — product capability or feature
- `pricing` — pricing model, tiers, who pays
- `compliance` — HIPAA, SOC 2, certifications, claims
- `segment_fit` — target audience, practice setting, modality fit
- `meta` — founding year, funding, team size, stage, other background

These categories are defaults for competitive research. For other research types, use categories that fit the domain. The skill should adapt.

## Step 3: Research each subject

For each subject that does NOT already have a `<subject-slug>.md` file in `data/<topic>/`:

### 3a. Web search

Run 2-3 web searches per subject to cover different angles:
- `"<subject> <search context>"` — primary product/topic search
- `"<subject> pricing plans"` or `"<subject> features"` — specifics
- `"<subject> reviews"` or `"<subject> comparison"` — third-party perspective

### 3b. Web fetch

Fetch the top 3-5 most relevant URLs from search results. Extract:
- Product features and capabilities
- Pricing information
- Compliance claims
- Target audience
- Any structured data (tables, specs, comparisons)

### 3c. Create source file

Write `data/<topic>/<subject-slug>.md`:

```markdown
# Sources — <Subject Name>

### <slug>-1. <Source Title>
- **URL:** <url>
- **Key data:** <2-3 bullet points of important facts>
- **Relevance:** <why this source matters for the research>

### <slug>-2. <Source Title>
- **URL:** <url>
- **Key data:** ...
- **Relevance:** ...
```

Source IDs follow the pattern `<subject-slug>-<n>` (e.g. `wysa-1`, `wysa-2`). These are referenced from facts.csv.

### 3d. Append to facts.csv

For each fact discovered, append a row to `data/<topic>/facts.csv`:

```csv
wysa,primitive,pre_session_report,yes,"AI-generated summary sent to clinician before session",wysa-1
wysa,pricing,model,per_client,"$15/client/month for clinician tier",wysa-1
wysa,compliance,hipaa,claimed,"BAA available for enterprise tier",wysa-3
```

**Rules for facts.csv:**
- One fact per row. Be specific.
- `value` should be machine-readable when possible: `yes`, `no`, `partial`, `claimed`, a number, or a short string.
- `detail` is the human-readable explanation. Quote it if it contains commas.
- `source_id` must reference a numbered source in the subject's source file.
- Never fabricate data. If something is unclear, use `value=unclear` and explain in `detail`.

## Step 4: Create or find the analysis doc

Check if an analysis doc already exists for this topic. Look for files matching `analysis-<topic>*.md` in `docs/`.

**If no doc exists:** use the create-doc skill to create one:
- **Type:** `analysis`
- **Slug:** `<topic>`
- **Name:** `<Topic Human Readable> — Analysis`
- **Description:** derived from the research context
- **Frontmatter must include:** `data: <topic>` (this creates the graph edge to the research node)
- **References:** include any Notion URLs the user provided as context
- **Body:** list the subjects researched, link to the data folder, and leave a `## Findings` section for synthesis

**If doc exists:** update its frontmatter to include `data: <topic>` if not already present.

## Step 5: Rebuild the graph

If `_graph/build.py` exists:

```bash
cd <root> && python3 _graph/build.py
```

Confirm the research node appears in the output.

## Step 6: Report

Summarize what was done:

```
Researched N subjects for "<topic>":
- <subject-1>: M sources, K facts
- <subject-2>: M sources, K facts
- ...

Data: data/<topic>/
Doc:  docs/YYYY-MM-DD/analysis-<topic>.md

Subjects not yet researched: <list any remaining>
```

## Incremental runs

The skill is designed for incremental use. On subsequent runs:
- Subjects with existing source files are skipped (unless user asks to refresh)
- New subjects are appended to the existing facts.csv
- The analysis doc is reused, not recreated

## Done when

- `data/<topic>/` exists with source files for each researched subject
- `facts.csv` has rows for all discovered facts
- An analysis doc exists with `data: <topic>` in frontmatter
- Graph rebuilt (if `_graph/` exists)
- Summary reported to user
