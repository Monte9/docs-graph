# Competitive Landscape Dimensions

## Overview

This document is the single source of truth for researching and evaluating
competitors in the O3 "Who Can Use It" analysis. One doc per competitor,
structured around 20 dimensions across three categories (strategic, product,
content). Each doc serves as both the qualitative writeup and the structured
data: comparison tables, clusters, and landscape charts are generated from
the docs on demand, with no separate facts database to maintain in parallel.

The goal is normalization: when two people research two different
competitors, they collect the same types of information using the same
vocabulary. Values are open-ended (not 1-5 scores). Record what you find, and
we cluster and compare across the full dataset later.

The authoritative list of competitors to research lives in Notion:
[Competitor list — defined](https://www.notion.so/rosebudjournal/Competitor-list-defined-33d328e8e3f780e0aa7fd1c0a42b73d4).

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
- Use the canonical `field_name` shown on each dimension below; non-canonical
  names (e.g., `hipaa_status` instead of `compliance`) break programmatic
  extraction for comparison charts.
- **Declare gaps, don't skip them.** If a fact is unavailable, write `unknown`
  in the snapshot cell and add a bullet in the dimension section that says
  "<fact> not confirmed in available sources." Every one of the 20 dimensions
  must appear in every doc, even when the answer is `unknown`. Do not fill
  gaps with inference.

---

## Output Doc Spec

**File location and frontmatter**

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

**Doc structure**

Each competitor doc mirrors the dimension taxonomy directly: three top-level
category sections (Strategic, Product, Content), each with one subsection per
dimension. Dimension subsection headings use the human-readable dimension name
exactly as it appears below (e.g. "Access Model", "EHR Integration",
"Channels & Distribution"). This keeps docs scannable and makes every fact
land in one obvious place.

```
1. Executive Summary       one paragraph (under 120 words) + snapshot table.
2. Strategic
   - Access Model
   - Business Model
   - Pricing
   - Compliance & Security
   - Practitioner Messaging
   - Company Stage
3. Product
   - Between-Session Features
   - Platforms
   - Therapist-in-the-Loop Model
   - Clinician Visibility
   - How is AI Used
   - EHR Integration
   - In-Product Content Library
   - Clinical Evidence (AI)
   - Safety and Crisis Handling
   - Customer Pain Points
4. Content
   - Channels & Distribution
   - Content Topics
   - Practitioner Relationship Model
   - Practitioner Resources
5. References & Sources    numbered list with URLs and access dates.
```

**Executive Summary rules**

Executive Summary starts with one paragraph under 120 words: what the product
is, who it serves, pricing range, review ratings, top 2-3 features, compliance
posture. Below the paragraph, include a **snapshot table** with all 20
dimensions. The table has two columns: `Dimension` (the canonical field_name)
and `Value` (a concise one-line summary, aim for under ~12 words per cell).
This table gives a single-screen overview of the entire competitor before the
reader dives into section details. Each `Value` is the one-line summary of
that dimension; the matching dimension section below expands it with a short
overview paragraph and 4–8 bullets of specific facts.

References & Sources is a numbered list; every factual claim in the body must
trace to a URL in this list.

**Snapshot table template**

Copy this shape into every competitor doc's Executive Summary and fill in the
Value column. Keep each cell under ~12 words. Longer context belongs in the
dimension section, not the snapshot. See the Data integrity rules above for
how to mark unknowns.

```markdown
| Dimension | Value |
|---|---|
| access_model | <direct-to-practitioner / marketplace / enterprise-only / consumer-only / hybrid> |
| business_model | <saas_subscription / marketplace_spread / enterprise_contract / dual_surface / payor_contract / ad_supported / hybrid> |
| pricing | <$X–$Y/mo; public or sales-gated; free trial y/n> |
| compliance | <HIPAA + GDPR + ...; SOC 2 status> |
| practitioner_messaging | <headline framing + dominant benefit axis> |
| company_stage | <tier; founded YEAR; funding; headcount; user base> |
| between_session_features | <top 3 features, comma-separated> |
| platforms | <iOS + Android + web + portal, checked> |
| loop_mode | <tight / loose / none / hybrid> |
| clinician_visibility | <full / opt-in / aggregate / none> |
| ai_capabilities | <client-facing and/or back-office, or none; 1-line summary of what the AI actually does> |
| ehr_integration | <native / api / zapier / none / is_an_ehr> |
| in_product_content | <count + sourcing model> |
| clinical_evidence_ai | <RCTs / white papers / none> |
| safety | <crisis detection y/n; AI principles y/n> |
| customer_pain_points | <top 2-3 themes; avg rating across sources, listed per source (e.g., "App Store 4.6, Play 4.3, G2 4.1")> |
| channels | <count + top 2-3 channels> |
| content_topics | <top 3 topic buckets> |
| practitioner_relationship | <customer / employee / marketplace_member / end_user_via_org / none> |
| practitioner_resources | <CEUs y/n + community y/n + top resource> |
```

**Dimension subsection format**

Every dimension subsection has the same shape: a short overview paragraph
followed by a bulleted list of specific facts. This lets a reader grasp the
answer in one sentence and drill into the evidence if they want more.

1. **Overview paragraph**: 2–3 sentences that expand on the snapshot table's
   one-liner and set the context. Answer: what's the headline for this
   competitor, and why does it matter? Do not paste the generic dimension
   Definition from this reference doc. The overview is competitor-specific.
2. **Bullets**: 4–8 bullets of specific, sourced facts. Each bullet is a
   complete thought carrying a concrete detail (names, numbers, URLs, dates),
   not a general observation.

No tables, no nested headings inside a subsection. Verbatim quotes (for
Customer Pain Points) appear inline in bullets with source attribution.

Example (Compliance & Security):

```markdown
### Compliance & Security

Quenza is HIPAA + GDPR + CCPA compliant with a BAA available on request, which
clears the US mental-health bar. SOC 2 is not confirmed.

- HIPAA and GDPR compliant. BAA available on request via info@quenza.com.
- SOC 2 certification status not confirmed in available sources.
- AES-256 encryption at rest and in transit. 30-minute idle-session logout.
```

The goal is to give the reader a 1-sentence answer and the evidence in the same
scroll. No prose walls, no 20-row tables per dimension.

**Done check**

A competitor doc is ready for merge when:
- All 20 dimension subsections exist, each with a snapshot-table row, an
  overview paragraph, and 4–8 bullets (or an explicit `unknown` / `not
  confirmed` declaration per the Data integrity rules).
- Every factual claim traces to a numbered entry in References & Sources, and
  the `references:` frontmatter lists every external URL cited in the body.
- The Executive Summary paragraph is under 120 words and the snapshot table
  has all 20 canonical `field_name` rows in the order shown above.

---

## Before You Start

Run these pre-research steps before writing any dimension. Together they set
the sourcing baseline for the whole doc. The 20 dimensions follow below.

Every run is a fresh research pass. Do not reuse or import prior writeups
(Notion, drafts, older competitor docs) as authoritative — if useful context
exists elsewhere, still re-verify each fact against the live source and cite
the live source, not the prior writeup.

1. **Practitioner subdomain check**: Search for `therapist`, `clinician`,
   `provider`, `practice`, or `care` subdomains and landing pages. Many
   competitors run a practitioner product on a separate subdomain from the
   consumer marketing site (e.g., `therapyassist.evolveinc.io`,
   `provider.growtherapy.com`, `organizations.headspace.com/providers`).
2. **App store check**: Search iOS App Store and Google Play for the product.
   Record ratings, review count, and any practitioner-relevant reviews.
3. **Review site check**: Search Capterra, G2, Trustpilot, and Choosing
   Therapy for the product. Record ratings and verbatim quotes.
4. **PubMed/PMC check**: Search for published studies referencing the product
   name. Record any RCTs or peer-reviewed outcomes data for `clinical_evidence_ai`.
5. **AI safety page check**: Look for a dedicated AI principles, safety, or
   trust page on the competitor's site. Record for `safety`.

---

# Strategic Dimensions

## 1. Access Model

**Field**: `access_model` | **Category**: `strategic`

**Definition**: How does a practitioner get access to this product? Can an
independent solo therapist sign up on their own, or does it require an
organizational contract, marketplace membership, or employer relationship?

*Note: Access Model captures the entry mechanism (how a practitioner gets
in). The ongoing role (what they are once in: customer, employee,
marketplace_member, etc.) is captured in Practitioner Relationship Model (#19).*

**Why it matters**: Gates adoption for Rosebud's target buyer (solo and
small-group practitioners). If access requires enterprise contracting or
marketplace membership, the product is structurally unavailable to our ICP.

**What to look for**:
- **Signup flow**: Public signup page, trial link, or sales-gated?
- **Pricing page**: Publicly visible with tiers, or "contact us"?
- **Enterprise gating**: Any features or plans reserved for orgs only?
- **Marketplace requirements**: Must the practitioner join a network or roster?
- **Credentialing**: License verification required at signup?

---

## 2. Business Model

**Field**: `business_model` | **Category**: `strategic`

**Definition**: What is the revenue and go-to-market structure?

*Note: Separate from Access Model (#1). Two companies can both be
"direct-to-practitioner" but have completely different business models (SaaS
subscription vs. marketplace revenue split vs. dual-surface consumer +
practitioner).*

**Why it matters**: Predicts who the competitor is actually optimizing for.
SaaS-to-practitioner aligns with Rosebud's motion; marketplace or enterprise
models create different incentives, price ceilings, and feature priorities.

**What to look for**:
- **Revenue source**: Practitioner subscription, per-session fee, enterprise
  contract, marketplace spread, consumer subscription, or ad-supported.
- **Who pays**: Practitioner, employer, payor, or consumer.
- **Dual surface**: Presence of a parallel consumer product alongside the
  practitioner offering.

---

## 3. Pricing

**Field**: `pricing` | **Category**: `strategic`

**Definition**: What does it cost for a solo practitioner to use this product?
This is about accessibility for our target buyer, not enterprise pricing.

**Why it matters**: Directly comparable to Rosebud's plans and a first-order
filter for solo and small-practice buyers. Price and transparency shape
whether we land in a head-to-head evaluation at all.

**What to look for**:
- **Monthly price (solo)**: Entry-tier price in USD, or "sales-gated".
- **Per-clinician add-on**: Seat pricing for group plans.
- **Free tier**: Yes/no (and limits if yes).
- **Free trial**: Yes/no (and length if yes).
- **Annual discount**: Percentage and commitment.
- **Public pricing**: Visible on site, or quote-only.
- **HSA/FSA eligibility**: Yes/no/unknown.

---

## 4. Compliance & Security

**Field**: `compliance` | **Category**: `strategic`

**Definition**: What is the compliance and security posture? Covers regulatory
status (HIPAA, GDPR, SOC 2), encryption standards, data residency, and
attestation source.

**Why it matters**: HIPAA is table stakes for any US mental-health tool;
SOC 2 and GDPR open institutional buyers; the attestation source (self vs.
audited) determines how much weight a claim actually carries.

**What to look for**:
- **HIPAA**: Compliant y/n, BAA availability.
- **GDPR**: Coverage and data-residency notes.
- **SOC 2**: Type I or Type II, report date, auditor.
- **Encryption at rest**: Standard cited (e.g., AES-256).
- **Encryption in transit**: Standard cited (e.g., TLS 1.2+).
- **Data residency**: Where client data is stored.
- **Attestation source**: Self-attested, inherited (e.g., AWS/GCP), or independently audited by a named third party. Record source URL where compliance is claimed.
- **Security/trust page**: URL.

---

## 5. Practitioner Messaging

**Field**: `practitioner_messaging` | **Category**: `strategic`

**Definition**: How does the competitor position itself to practitioners? What
is the core value proposition and framing? This reveals what benefits resonate
in the market and where there are messaging gaps we can exploit.

*Note: This dimension focuses on positioning and value proposition only.
Review ratings, verbatim quotes, and reception signals belong in Customer
Pain Points (#16).*

**Why it matters**: Reveals the benefit axis that resonates with practitioners
in the market and where messaging gaps exist for Rosebud to occupy.

**What to look for**:
- **Homepage headline**: Exact copy directed at practitioners.
- **Key benefit axis**: Flexibility, admin relief, outcomes, income, community, or other.
- **AI stance**: Augmentation, replacement, or silent.
- **Target segments**: Which practitioner types they pitch at (solo, group, enterprise; specific licenses).
- **Excluded segments**: Which practitioner types they ignore or explicitly exclude.

---

## 6. Company Stage

**Field**: `company_stage` | **Category**: `strategic`

**Definition**: What is the company's maturity, scale, and trajectory? A $3B
incumbent and a seed-stage startup operate with different constraints.

**Why it matters**: Stage determines competitive posture, buyer fit, and the
speed at which a competitor can react. Landscape visualizations need to
weight nodes by scale, not treat them identically.

**What to look for**:
- **Founded**: Year and location.
- **Funding**: Total raised, most recent round, and valuation.
- **Headcount**: Approximate team size.
- **User base**: Reported practitioners, members, or providers.
- **Geographic footprint**: Markets served.
- **Key deals**: Partnerships or acquisitions.
- **Growth signals**: Hiring, product launches, market expansion.

---

# Product Dimensions

## 7. Between-Session Features

**Field**: `between_session_features` | **Category**: `product`

**Definition**: What specific features does the product offer for client
engagement between live sessions? This is a checklist of discrete capabilities,
not a subjective rating.

*Note: This dimension captures the feature surface (what the product offers for
between-session engagement). What the therapist actually sees of client activity
is captured in Clinician Visibility (#10).*

**Why it matters**: Between-session engagement is the axis Rosebud competes
on. The feature checklist is the most direct head-to-head comparison in the
landscape.

**What to look for** (note depth where it differentiates, e.g., "journaling
with prompts and voice input" vs. "free-text journaling only"):
- **Homework/assignments**: Can the therapist assign structured tasks?
- **Journaling**: Can the client journal or do free-text reflection?
- **Mood/emotion tracking**: Does the client log mood, emotions, or symptoms?
- **Outcome measures**: Are standardized assessments available (PHQ-9, GAD-7)?
- **Automated pathways**: Can activities be sequenced and auto-delivered?
- **AI companion**: Is there an AI chatbot or interactive agent for the client?
- **Secure messaging**: Can client and therapist message between sessions?
- **Push notifications/reminders**: Does the product nudge the client?

---

## 8. Platforms

**Field**: `platforms` | **Category**: `product`

**Definition**: What platforms and interfaces does the product run on? This
covers both the client-facing side and the practitioner-facing side.

**Why it matters**: Platform coverage signals investment level and reach.
Native iOS and Android apps beat a mobile web wrapper on engagement;
a dedicated practitioner portal signals clinician-first product thinking.

**What to look for**:
- **iOS**: Native app y/n, App Store URL, rating, review count.
- **Android**: Native app y/n, Play Store URL, rating, review count.
- **Web**: Responsive, desktop-only, or absent.
- **Practitioner portal**: Presence and feature depth.

---

## 9. Therapist-in-the-Loop Model

**Field**: `loop_mode` | **Category**: `product`

**Definition**: Where does the therapist sit relative to the client's
between-session activity? Some products require a therapist to assign every
activity (tight loop); others let clients self-serve without clinician
involvement (loose loop or no loop). This dimension captures the structural
posture: is a therapist required, and who drives the activity flow?

*Note: What the therapist actually sees of between-session activity is
captured separately in Clinician Visibility (#10).*

**Why it matters**: Determines whether the product is a therapist tool, a
consumer tool, or a hybrid. This is one of the sharpest axes in the landscape
and directly shapes who the buyer is.

**What to look for**:
- **Therapist required?**: Can the client use the product without a clinician?
- **Activity assignment**: Therapist-pushed, client-pulled, or auto-sequenced?
- **Default posture**: Does the product assume a therapist is present, or is
  the therapist an optional add-on?

---

## 10. Clinician Visibility

**Field**: `clinician_visibility` | **Category**: `product`

**Definition**: What does the therapist actually see of the client's
between-session activity? This is the data-flow companion to Therapist-in-the-
Loop Model (#9), which captures the structural posture.

**Why it matters**: The data-flow signal that separates "built for clinicians"
from "sometimes used with clinicians". Directly shapes the therapist's
day-to-day workflow and the product's clinical credibility.

**What to look for**:
- **Homework/journal visibility**: Does the therapist see client entries?
- **Mood data**: Surfaced on a dashboard or hidden from the therapist?
- **AI conversation logs**: Visible to the therapist or client-private?
- **Session prep**: Automated summaries, alerts, or briefs for the therapist?
- **Sharing default**: On-by-default or opt-in per client/entry?
- **Aggregate vs. individual**: Summary metrics only, or per-entry data?

---

## 11. How is AI Used

**Field**: `ai_capabilities` | **Category**: `product`

**Definition**: Where in the product does AI actually do work, and how central
is it? The key split is client-facing AI (point-of-care: AI that interacts
directly with clients or generates clinical content) vs. back-office AI
(operational: AI that reduces therapist admin like notes, scheduling, billing).

*Note: This dimension captures where AI is deployed and what it does. Whether
AI is backed by published evidence is captured separately in Clinical Evidence
(#14).*

**Why it matters**: Rosebud is an AI-native product, so AI placement in each
competitor's value chain is the sharpest differentiation axis in the landscape.
Client-facing AI is direct competition; back-office AI is adjacent.

**What to look for**:
- **Client-facing AI (point-of-care)**: AI chatbot or companion for clients,
  AI-generated exercises or journaling prompts, AI-powered reflections or
  psychoeducation, in-session AI copilots clients interact with directly.
- **Back-office AI (operational)**: AI-generated progress notes, AI session
  summaries, AI treatment plan drafting, AI scheduling/intake, billing code
  suggestion, marketing copy generation for practitioners.
- **Other AI**: Matching and recommendations, ML outcome prediction, NLP
  sentiment analysis on client text, risk or crisis detection, anomaly flags
  for the therapist.
- **Autonomy**: Human-in-the-loop vs. autonomous. Does the therapist review
  AI output before it reaches the client?
- **Provenance**: Named models or partnerships (OpenAI, Anthropic,
  proprietary). Record where disclosed.
- **Principles & escalation**: Published AI principles and human escalation
  pathways for AI interactions.

---

## 12. EHR Integration

**Field**: `ehr_integration` | **Category**: `product`

**Definition**: Does this product integrate with existing practice management
tools, or is it a standalone silo? Practitioners rarely want to replace their
entire stack. A tool that plays nicely with SimplePractice or TherapyNotes has
a lower adoption barrier.

**Why it matters**: Lower integration friction equals lower adoption barrier.
A product that bolts into SimplePractice, TherapyNotes, or Jane has a
structural advantage over a standalone silo.

**What to look for**:
- **Native EHRs**: List each by name (SimplePractice, TherapyNotes, Jane, Osmind, etc.).
- **API**: Public API y/n, docs URL, auth model.
- **Zapier/webhooks**: Support y/n, scope.
- **Is-an-EHR**: Y/n (if yes, mark dimension N/A).
- **Import/export**: CSV, FHIR, or other portability.

---

## 13. In-Product Content Library

**Field**: `in_product_content` | **Category**: `product`

**Definition**: What pre-built content does the product offer inside the app
for clients or practitioners to use, and where does that content come from?
This is distinct from marketing content (blog posts, webinars). It captures
both the depth/breadth of clinical or wellness content shipped with the
product and the sourcing model behind it.

*Note: This dimension captures content shipped inside the product for clients
or practitioners to use. Practitioner-facing educational content around the
product (CEUs, webinars, training, community) is captured in Practitioner
Resources (#20).*

**Why it matters**: Depth plus sourcing model is a real defensibility axis.
1,000 own-produced, clinically-authored exercises is a different moat than
a generic CBT worksheet library. Sourcing signals how serious the competitor
is about content as a wedge.

**What to look for**:
- **Library depth**: Number and type of exercises, meditations, worksheets,
  psychoeducation modules, or activity templates available in-app.
- **Assignability**: Therapist-assignable, auto-sequenced into pathways, or
  client-self-serve only.
- **Sourcing**: Proprietary/own-produced, licensed from third parties,
  crowdsourced from practitioners, or AI-generated.
- **Authors**: Named content creators, clinical authors, content partnerships,
  clinical advisory input.
- **Update cadence**: How often new content ships.
- **Sample content**: 3 specific activities, exercises, or content pieces from
  the library, hyperlinked where possible. Prefer the most popular or
  prominently featured items. Grounds the dimension in concrete examples
  rather than just counts and categories.

---

## 14. Clinical Evidence (AI)

**Field**: `clinical_evidence_ai` | **Category**: `product`

**Definition**: What published evidence does the competitor cite specifically
for their AI-powered features or AI-delivered continuous care? The relevant
evidence bar is not "does the underlying modality work" (CBT efficacy is
well-established) but "does this AI touchpoint actually help clients."

**Why it matters**: Rosebud's thesis is that AI delivers clinical value
between sessions; competitors' AI evidence bar (or absence of one) is
directly comparable and a sharp credibility signal for clinical buyers.

**What to look for**:
- **Published RCTs / peer-reviewed studies**: Journal, sample size, and
  outcomes for the AI component specifically.
- **White papers**: Methodology, AI efficacy, or AI safety claims with
  supporting data.
- **Aggregate outcome data**: Tied to AI engagement specifically, not generic
  program completion.
- **Clinical advisory input**: Named advisors on AI features.
- **University partnerships**: Research collaborations evaluating AI
  touchpoints.
- **FDA clearance/designation**: Breakthrough device or 510(k) for AI
  functionality.
- **PubMed/PMC search**: Query product name + "AI" / "chatbot" /
  "conversational agent" and record any hits.

---

## 15. Safety and Crisis Handling

**Field**: `safety` | **Category**: `product`

**Definition**: How does the product handle crisis situations, suicidal
ideation, or clinical escalation? Captures both the technical safeguards
(detection, escalation, moderation) and the published stance on AI safety.

**Why it matters**: Any product with AI or between-session client interaction
has crisis exposure; safety posture is both a product surface and a
positioning signal to clinical buyers.

**What to look for**:
- **Crisis detection**: Automated flagging y/n.
- **Escalation pathways**: Hotline routing, therapist alerts, emergency contacts.
- **AI guardrails**: Published principles y/n.
- **Content moderation**: Policy and enforcement mechanisms.
- **Suicide/self-harm protocols**: Documented y/n.
- **Safety page**: URL to AI principles, safety, or trust page.

---

## 16. Customer Pain Points

**Field**: `customer_pain_points` | **Category**: `product`

**Definition**: What specific complaints, frustrations, and unmet needs do
customers (both practitioners and their clients) express about this product?
Captured from review sites, app store reviews, and community threads. This
dimension also owns review ratings and reception signals.

*Note: This dimension owns reception signals (ratings and verbatim quotes).
Headline framing and value proposition belong in Practitioner Messaging (#5).*

**Why it matters**: Pain points are the clearest read on where a competitor
is under-delivering and where Rosebud can position against them. Ratings
reveal reception signals that positioning copy alone can't.

**What to look for**:
- **Review ratings**: Capterra, G2, Trustpilot, iOS App Store, Google Play.
  Record rating and review count per source.
- **Practitioner complaints**: At least 3 verbatim quotes from Capterra, G2,
  Trustpilot, or Choosing Therapy, each with source attribution and date
  (e.g., "'A tad bit pricey' (Capterra, 2024-03-12)"). Do not paraphrase when
  the original wording is available.
- **Client complaints**: Verbatim quotes from iOS App Store and Google Play
  reviews, with source attribution and date.
- **Common themes**: Pricing friction, onboarding difficulty, missing
  features, poor mobile experience, clunky UX, support responsiveness,
  billing bugs, AI quality issues, lack of customization, missing
  integrations, client adoption struggles.
- **Wishlist signals**: Positive reviews that reveal what users wished
  existed (features requested but not present).

---

# Content Dimensions

## 17. Channels & Distribution

**Field**: `channels` | **Category**: `content`

**Definition**: What channels does the competitor use to reach practitioners?

**Why it matters**: Channel breadth signals who is diversifying distribution
vs. placing single-channel bets, and informs where Rosebud should invest
next. A radar chart per competitor makes gaps visible at a glance.

**What to look for** (record each, even if "not present"):
- **Blog**: URL, estimated post count, practitioner-specific or general.
- **LinkedIn**: Company page URL, follower count.
- **Instagram**: Handle, follower count, post count.
- **X/Twitter**: Handle, follower count, active or dormant.
- **TikTok**: Handle or "not present".
- **YouTube**: Channel URL, subscriber count, or "not present".
- **Podcast**: Name/feed or "not present".
- **Email newsletter**: Signup URL or "not confirmed".
- **Webinars/events**: Frequency, sample titles, or "not observed".
- **Community/forum**: URL, access model (free, paid, subscription-gated).
- **Practitioner-specific presence**: Does the blog or newsletter have a
  dedicated practitioner feed, or is it mixed with consumer content?
- **Sample content**: 3 specific published pieces (blog posts, videos, social
  posts) hyperlinked with titles. Choose examples that represent the spread
  of their channel strategy.

---

## 18. Content Topics

**Field**: `content_topics` | **Category**: `content`

**Definition**: What subjects is each competitor publishing about? Clustering
topics across companies reveals white space and common themes. Tells us where
the conversation is and where nobody is talking.

**Why it matters**: Topic clustering across competitors surfaces white space
and common themes, and signals where Rosebud can differentiate content
strategy. Practitioner wellbeing is a distinct bucket worth tracking; most
tools ignore it.

**What to look for**:
- **Clinical topics**: Which modalities are covered (CBT, ACT, DBT, EMDR,
  IFS, etc.)? Record named modalities with frequency.
- **Business/practice topics**: Billing, marketing, practice growth, admin,
  operations.
- **Practitioner wellbeing**: Burnout, compassion fatigue, vicarious trauma,
  work-life balance, self-care for clinicians. Present or absent as a
  content category.
- **Consumer/client education**: Self-help, condition-specific guides aimed
  at end clients.
- **Thought leadership**: Founder visibility, conference talks, media
  appearances.

---

## 19. Practitioner Relationship Model

**Field**: `practitioner_relationship` | **Category**: `content`

**Definition**: What is the practitioner's relationship to the product? This
goes beyond access model (how they get in) to capture what they *are* once
they're in. The relationship model determines who the actual user is, what
switching costs look like, and what content resonates with them. This
dimension also captures the terminology the competitor uses on landing pages,
nav, and marketing to describe the professionals they serve ("therapist" vs.
"coach" vs. "clinician" vs. "provider").

*Note: Access Model (#1) captures the entry mechanism (how a practitioner
gets in); this dimension captures the ongoing role (what they are once in).
Typical pairings: `direct-to-practitioner` ↔ `customer`; `marketplace` ↔
`marketplace_member`; `enterprise-only` ↔ `end_user_via_org`; `consumer-only`
↔ `none`. Non-canonical pairings (e.g., hybrid access with split roles)
should be spelled out in the body.*

**Why it matters**: Determines who the actual user is, what switching costs
look like, and what content resonates (all upstream of go-to-market strategy).
Terminology choice (therapist vs. clinician vs. coach) signals target segment
and regulatory posture.

**What to look for**:
- **Relationship type**: Customer (pays SaaS directly), employee (1099 or
  W2), marketplace member, end user via an org buyer, or not a user at all.
- **Terminology**: Exact terms used on homepage, practitioner/pricing nav,
  signup flows, and testimonial sections. Count frequency (which term
  dominates).
- **License types**: Specific licenses called out (LMFT, LCSW, LPC, PsyD/PhD,
  etc.).
- **Settings served**: Solo practice, group practice, clinic, enterprise.
- **Exclusions**: Any practitioner types explicitly turned away.
- **Credibility signals**: Founder credentials, prior ventures, domain
  authority, named advisors.

---

## 20. Practitioner Resources

**Field**: `practitioner_resources` | **Category**: `content`

**Definition**: What educational content, tools, materials, and community does
the company provide to practitioners? This goes beyond just CEUs to include
any resource that helps practitioners do their job better, including peer
communities and forums.

**Why it matters**: Distinguishes companies investing in practitioner
enablement from those just selling a product. Community moats raise
switching costs and create defensibility beyond the product itself.

**What to look for**:
- **CEU/CE credits**: Offered or not, accreditation body (APA, NBCC, etc.),
  cost.
- **Webinars**: Frequency, sample topics, live vs. on-demand.
- **Product training**: Formal program, knowledge base, onboarding docs.
- **Clinical guides/templates**: Downloadable resources, best-practice
  articles, case studies, research libraries.
- **Community**: Online forums, peer consultation groups, Slack/Discord,
  practitioner advisory boards, CTAs to join practitioner-specific
  newsletters. Record URLs and access model.
- **Cost**: Free, included with subscription, or paid separately.
