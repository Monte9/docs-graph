# Competitive Landscape Dimensions

## Overview

This document is the single source of truth for how we research and evaluate
competitors in the O3 "Who Can Use It" analysis. It defines 19 dimensions
across three categories (strategic, product, content), a recommended doc
structure, and the writing rules we follow.

**The mental model is simple**: one doc per competitor. Each doc is
structured around these 19 dimensions and serves as both the qualitative
writeup and the structured data. Comparison tables, clusters, and landscape
charts can be generated from the docs on demand — no separate facts database
to maintain in parallel.

The goal is normalization: when two people research two different
competitors, they collect the same types of information using the same
vocabulary. Values are open-ended (not 1-5 scores). Record what you find, and
we cluster and compare across the full dataset later.

---

## Where Competitor Docs Live

Every competitor doc lives at:

```
data/competitors/<slug>.md
```

Use a kebab-case slug based on the competitor name (e.g., `wysa`,
`simple-practice`, `spring-health`). One file per competitor. No subfolders,
no per-competitor folders, no separate sources file.

The `data/competitors/` folder is rendered as a single `research` node in the
graph. Synthesis docs reference it via `data: competitors` in their
frontmatter.

Each doc must have this frontmatter:

```yaml
---
name: <Competitor Display Name>
date: <YYYY-MM-DD>
type: research
description: <one-sentence summary>
references:
  - <any notion URLs or external sources cited in the body>
---
```

---

## Competitor List

The authoritative list of competitors to research lives in Notion:
[Competitor list — defined](https://www.notion.so/rosebudjournal/Competitor-list-defined-33d328e8e3f780e0aa7fd1c0a42b73d4).
Pull from that list when deciding what to work on.

---

## How to Use This Document

1. When writing a competitor's doc, use this as a checklist. Every dimension
   should have enough detail in the writeup to support comparison later.
2. Use the exact field names listed here as section markers or tags inside
   each competitor doc, so facts can be extracted programmatically.
3. If a dimension is not applicable or data is unavailable, record that
   explicitly (e.g., "none", "unknown", "N/A") rather than leaving it blank.

---

## Writing Guide

**Voice & tone**
- Plain, direct language. Short sentences. No filler.
- No em-dashes. Use commas, periods, or parentheses instead.
- Avoid inflated modifiers: "essentially", "notably", "significantly",
  "comprehensive", "robust".
- Avoid hedging ("it appears that", "it seems"). State what the evidence shows.
- No comparative framing against Rosebud. Each doc is a standalone analysis.

**Data integrity**
- Every factual claim must trace to a URL in the References section.
- Pricing must come from the product's site or a verified aggregator
  (Capterra, G2, SaaSWorthy).
- Review quotes must be verbatim from the source. Do not reword.
- If data is unavailable, say so. Do not fill gaps with inference.

---

## Recommended Doc Structure

Each competitor doc should follow this structure. Sections map to one or more
dimensions defined below.

1. **Executive Summary** — one paragraph under 120 words. What the product is,
   who it serves, pricing range, review ratings, top 2-3 features, compliance
   posture. A reader should get the full picture here without scrolling.
2. **Market Positioning & Reviews** — overall ratings, verbatim quotes with
   attribution, strengths and weaknesses drawn from real reviews.
3. **Practice Setting Fit** — two subsections only: Direct to Practitioner
   (solo and group) and Institutional / Platform-Employed.
4. **Modality Fit** — modality orientation, explicitly supported modalities,
   gaps.
5. **Pricing** — tiers, plans, trial info.
6. **Key Features** — single combined section with four subsections:
   Assignment & Content Delivery, Client-Facing Experience, Therapist
   Visibility & Between-Session Data, Automation & Workflows.
7. **Compliance & Security** — HIPAA, GDPR, encryption, BAA availability,
   SOC 2 status. Separate line for EHR integrations.
8. **Content & Distribution** — channels, topics, practitioner resources,
   community (maps to the four Content dimensions).
9. **References & Sources** — numbered list with URLs and access dates.

---

# Strategic Dimensions

These dimensions define a competitor's market position, accessibility, and how
the competitor positions itself to our target buyer (independent practitioners).

---

## 1. Access Model

**Field**: `access_model` | **Category**: `strategic`

**Definition**: How does a practitioner get access to this product? Can an
independent solo therapist sign up on their own, or does it require an
organizational contract, marketplace membership, or employer relationship?

**What to look for**: Signup flow, pricing page availability, enterprise-only
gating, marketplace requirements, credentialing requirements.

**Doc section**: Practice Setting Fit

---

## 2. Business Model

**Field**: `business_model` | **Category**: `strategic`

**Definition**: What is the revenue and go-to-market structure? This is
separate from access model because two companies can both be "direct-to-
practitioner" but have completely different business models (SaaS subscription
vs. marketplace revenue split vs. dual-surface consumer + practitioner).

**What to look for**: Revenue source (practitioner subscription, per-session
fee, enterprise contract, marketplace spread, consumer subscription, ad-
supported), who pays (practitioner, employer, payor, consumer), whether there
is a consumer product alongside the practitioner product.

**Doc section**: Practice Setting Fit, Pricing

---

## 3. Pricing

**Field**: `pricing` | **Category**: `strategic`

**Definition**: What does it cost for a solo practitioner to use this product?
This is about accessibility for our target buyer, not enterprise pricing.

**What to look for**: Monthly price for solo practitioner, per-clinician add-on
cost for groups, free tier or trial availability, annual discount, whether
pricing is public or requires a sales call.

**Doc section**: Pricing

---

## 4. Compliance & Security

**Field**: `compliance` | **Category**: `strategic`

**Definition**: What is the compliance and security posture? This matters for
practitioner adoption (HIPAA is table stakes in the US) and for institutional
buyers who require SOC 2 or GDPR.

**What to look for**: HIPAA compliance and BAA availability, GDPR compliance,
SOC 2 Type I or Type II, encryption standards (at rest, in transit), data
residency, third-party audits, published security documentation.

**Doc section**: Compliance & Security

---

## 5. Modality Fit

**Field**: `modality_fit` | **Category**: `strategic`

**Definition**: Which therapeutic modalities does this product support well, and
which are underserved? Most tools are biased toward structured approaches (CBT,
DBT, ACT). Rosebud's opportunity is strongest in modalities that current tools
ignore.

**What to look for**: Explicitly supported modalities (with evidence), modality
limitations or biases in the product design, whether the tool is
modality-agnostic infrastructure or modality-specific.

**Modalities to check for specifically**: CBT, DBT, ACT, EMDR, IFS, narrative,
psychodynamic, somatic, solution-focused, motivational interviewing, mindfulness,
relational/humanistic, coaching.

**Doc section**: Modality Fit

---

## 6. Practitioner Messaging

**Field**: `practitioner_messaging` | **Category**: `strategic`

**Definition**: How does the competitor position itself to practitioners? What
is the core value proposition and framing? This reveals what benefits resonate
in the market and where there are messaging gaps we can exploit.

**What to look for**: Headline copy on practitioner-facing pages, key benefits
emphasized (flexibility, admin relief, outcomes, income, community), AI stance
(augmentation vs. replacement), what practitioner segments they target vs.
ignore.

**Doc section**: Market Positioning & Reviews (plus web research on
practitioner-facing landing pages).

---

# Product Dimensions

These dimensions capture what the product actually does. Rather than a single
subjective "between-session depth" score, we break the product surface into
specific, observable features that can be compared across competitors.

---

## 7. Between-Session Features

**Field**: `between_session_features` | **Category**: `product`

**Definition**: What specific features does the product offer for client
engagement between live sessions? This is a checklist of discrete capabilities,
not a subjective rating.

**What to look for**: Check for each of these capabilities and record which
ones the product supports.

**Feature checklist**:
- **Homework/assignments**: Can the therapist assign structured tasks?
- **Journaling**: Can the client journal or do free-text reflection?
- **Mood/emotion tracking**: Does the client log mood, emotions, or symptoms?
- **Outcome measures**: Are standardized assessments available (PHQ-9, GAD-7)?
- **Automated pathways**: Can activities be sequenced and auto-delivered?
- **AI companion**: Is there an AI chatbot or interactive agent for the client?
- **Secure messaging**: Can client and therapist message between sessions?
- **Push notifications/reminders**: Does the product nudge the client?

**Doc section**: Key Features

---

## 8. Platforms

**Field**: `platforms` | **Category**: `product`

**Definition**: What platforms and interfaces does the product run on? This
covers both the client-facing side and the practitioner-facing side.

**What to look for**: Native iOS app, native Android app, web app (responsive
or desktop-only), practitioner dashboard/portal, app store presence and ratings.

**Doc section**: Key Features > Client-Facing Experience (plus app store
research).

---

## 9. Data Sharing

**Field**: `data_sharing` | **Category**: `product`

**Definition**: What data flows between the client and the therapist, and in
what direction? This is about visibility and control: does the therapist see
client between-session activity? Does the client see therapist notes? Is AI
interaction data shared or hidden?

**What to look for**: Whether therapist sees client homework responses, journal
entries, mood data, or AI conversation logs. Whether there are dashboards,
alerts, or session prep summaries. Whether sharing is on by default or opt-in.
Whether AI interactions are visible to the therapist.

**Doc section**: Key Features > Therapist Visibility & Between-Session Data

---

## 10. AI Capabilities

**Field**: `ai_capabilities` | **Category**: `product`

**Definition**: How is AI/ML used in the product? This is a spectrum from "no
AI at all" to "AI is the core product." Important for understanding where
Rosebud's AI-native approach is differentiated vs. where competitors are catching
up.

**What to look for**: AI-generated content or activities, AI chatbot/companion
for clients, AI clinical notes or documentation, AI-powered matching or
recommendations, ML-based outcome prediction, NLP sentiment analysis, human
escalation pathways for AI interactions.

**Doc section**: Key Features (any subsection), plus any AI-specific mentions
in Executive Summary or Market Positioning.

---

## 11. EHR Integration

**Field**: `ehr_integration` | **Category**: `product`

**Definition**: Does this product integrate with existing practice management
tools, or is it a standalone silo? Practitioners rarely want to replace their
entire stack. A tool that plays nicely with SimplePractice or TherapyNotes has
a lower adoption barrier.

**What to look for**: Native integrations (which EHRs?), API availability,
Zapier/webhook support, is the product itself an EHR (making this N/A), data
import/export capabilities.

**Doc section**: Compliance & Security, Key Features

---

## 12. In-Product Content Library

**Field**: `in_product_content` | **Category**: `product`

**Definition**: What pre-built content does the product offer inside the app
for clients or practitioners to use? This is distinct from marketing content
(blog posts, webinars). It captures the depth and breadth of clinical or
wellness content that ships with the product itself.

**What to look for**: Number and type of exercises, meditations, worksheets,
psychoeducation modules, or activity templates available in-app. Whether
content is own-produced or licensed from third parties. Whether content is
therapist-assignable or client-self-serve only. Named content creators or
clinical authors.

**Doc section**: Key Features > Assignment & Content Delivery and
Client-Facing Experience (plus app store descriptions).

---

## 13. Content Sourcing

**Field**: `content_sourcing` | **Category**: `product`

**Definition**: Where does the in-product content come from? Own-produced at
scale, crowdsourced from practitioners, licensed from publishers, or generated
by AI? This reveals the content moat: a company with 1,000 own-produced
exercises has a different defensibility profile than one using a generic CBT
worksheet library.

**What to look for**: Whether content is proprietary or third-party, named
authors or clinical teams, content partnerships, practitioner-contributed
content, AI-generated content, content update cadence.

**Doc section**: Key Features, plus marketing pages and press coverage.

---

## 14. Clinical Evidence

**Field**: `clinical_evidence` | **Category**: `product`

**Definition**: What published clinical evidence supports this product? This is
a real differentiator axis: some competitors have multiple peer-reviewed RCTs,
others make claims without citations. For a landscape visualization, this
separates evidence-backed products from marketing-backed ones.

**What to look for**: Published RCTs (journal, sample size, outcomes), peer-
reviewed studies, white papers with methodology, aggregate outcome data with
sample sizes, clinical advisory board, university research partnerships,
FDA clearance or breakthrough device designation.

**Doc section**: Executive Summary, Compliance & Security, References. Also
check PubMed/PMC directly.

---

## 15. Safety and Crisis Handling

**Field**: `safety` | **Category**: `product`

**Definition**: How does the product handle crisis situations, suicidal
ideation, or clinical escalation? For any product with an AI component or
between-session client interaction, safety protocols are a critical product
surface. This dimension captures both the technical safeguards and the
published stance on AI safety.

**What to look for**: Crisis detection and escalation pathways (hotline
routing, therapist alerts, emergency contacts), AI safety guardrails and
published AI principles, human-in-the-loop requirements, content moderation,
suicide/self-harm protocols, published safety documentation.

**Doc section**: Key Features > Automation & Workflows, Compliance & Security,
and any AI principles or safety pages.

---

# Content Dimensions

These dimensions capture how the competitor reaches, engages, and retains
practitioners through content, community, and education.

---

## 16. Channels & Distribution

**Field**: `channels` | **Category**: `content`

**Definition**: Map of every channel a competitor uses to reach practitioners.
Lets us build a radar chart per company to see who has broad coverage across
social networks and content channels vs. single-channel bets.

**What to look for**: Blog (practitioner-specific feed?), LinkedIn, Instagram,
X/Twitter, TikTok, YouTube, podcast, email newsletter, webinars, conferences,
practitioner-specific landing pages, founder/leadership thought leadership.

**Doc section**: Content & Distribution

---

## 17. Content Topics

**Field**: `content_topics` | **Category**: `content`

**Definition**: What subjects is each competitor publishing about? Clustering
topics across companies reveals white space and common themes. Tells us where
the conversation is and where nobody is talking.

**What to look for**: Blog post categories, webinar topics, social media themes,
newsletter content, educational resource topics. Look for both clinical topics
(modalities, outcomes, evidence) and business topics (billing, marketing,
practice growth, burnout).

**Doc section**: Content & Distribution

---

## 18. Practitioner Resources

**Field**: `practitioner_resources` | **Category**: `content`

**Definition**: What educational content, tools, and materials does the company
provide to practitioners? This goes beyond just CEUs to include any resource
that helps practitioners do their job better. Tells us who is investing in
practitioner enablement vs. just selling a product.

**What to look for**: CEU/CE credit courses, webinars, accreditation (APA,
NBCC, etc.), product training, clinical best practice guides, downloadable
templates or frameworks, research libraries, case studies, cost (free vs. paid).

**Doc section**: Content & Distribution

---

## 19. Community

**Field**: `community` | **Category**: `content`

**Definition**: Does the competitor foster a practitioner community? Community
increases switching costs and creates a moat beyond the product itself.

**What to look for**: Online forums, peer consultation groups, case conferences,
Slack/Discord communities, in-person events, user conferences, mentorship
programs, practitioner advisory boards. Also capture any CTAs to join
practitioner-specific newsletters or groups (signup URLs, where they appear,
what's promised).

**Doc section**: Content & Distribution

---

# Research Checklist

Before concluding research on any competitor, verify these steps:

1. **Practitioner subdomain check**: Search for `therapist`, `clinician`,
   `provider`, `practice`, or `care` subdomains and landing pages. Many
   competitors run a practitioner product on a separate subdomain from the
   consumer marketing site (e.g., `therapyassist.evolveinc.io`,
   `provider.growtherapy.com`, `organizations.headspace.com/providers`).
2. **Content doc check**: If a Content report exists in the Competitor
   Analyses DB for this company, fetch it first and treat its findings as
   authoritative for the Content dimensions.
3. **App store check**: Search iOS App Store and Google Play for the product.
   Record ratings, review count, and any practitioner-relevant reviews.
4. **Review site check**: Search Capterra, G2, Trustpilot, and Choosing
   Therapy for the product. Record ratings and verbatim quotes.
5. **PubMed/PMC check**: Search for published studies referencing the product
   name. Record any RCTs or peer-reviewed outcomes data for `clinical_evidence`.
6. **AI safety page check**: Look for a dedicated AI principles, safety, or
   trust page on the competitor's site. Record for `safety`.
