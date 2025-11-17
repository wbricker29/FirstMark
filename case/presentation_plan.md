# Presentation Plan

> Demo flow, presentation structure, and delivery strategy for the FirstMark case study presentation

**Format:** 1 Hour presentation

- 15 minutes: Intro about me
- 30 minutes: Presentation of case and demo
- 15 minutes: Q&A

**Logistical Note:**

- Demo will be run live on my computer
- We will need to have a pre-run example for the research section with full audit trails that I can walk them through

---

## Presentation Structure

### Intro (15 min)

**How I think about attacking transformation in venture:**

- How we would ideally get to this use case
  - Expected ROI
- Part of process
  - What do you want
  - Do we do it <-- Expected ROI
  - How do we do it
  - How do we know we are on track
- Generally looking for
  - Portfolio value - business + tech
- What I do know is that there are countless things I don't know
  - There will be nuances that matter
  - There will be failure and bumps
- I don't really know
  - Current what is, project frequency, relative trade
  - How are you using Affinity?

**The biggest determining factors will be:**

- Understanding the what is - what are current systems like, where does data live, what does it look like - and the why!
- Paying all my sponsors - investors, COO, platform
- While trying to make headway on foundation
- Organizational dynamics
  - Who do I need to convert
  - Who do I need to accommodate
- Understanding FMC
  - How do you invest
  - What are your frustrations, hills you will die on, ideas

---

### The Case (Part 1 of main presentation)

#### The business context

- Differentiation helps, have guild, use it
- Case of thing that is done many times in peoples minds in different ways --> Get value from rationalizing and augmenting
- People evaluation is a fundamental pillar of VC, especially early stage

#### The Requirements and Components

**Recall over precision:**

- Rather not miss a great match vs see some dudes

**The goal is not to make the decision, it's to filter and focus review:**

- Needs to sufficiently filter who is reviewed
- Needs to inform review of an individual (pop key info, enable quick action)
- Needs to enable investigation

**The target is augmentation, not replacement**

**The goal is to:**

- Validate the quality of research methods
- Validate the quality of the evaluation and traces
- Cut operational cost
- Optimize execution time

**Our future cases for extension are:**

- Other people enrichment and research use cases - founders, LPs, hires
- Applications could be current and or retroactive

#### The key complexity points and decisions

**Boundaries:**

- What parts of this are central and universal
  - EG. Person intake and normalization
- What parts of this are standard practices beyond this use case
  - Is enrichment on all People?
  - What is the cadence of
- What do we keep+Maintain vs Keep+Redo vs toss
  - Do we try to define refresh process?

**Technical considerations:**

- Where do we need LLM
- What is the balance of enabling vs confining the LLM
- How we guardrail LLM
- How do we optimize human engagement?
- Where do we build vs buy?
  - And where start from scratch vs leverage existing methods

**Know messy corners:**

- Titles will be non-normalized
- There will be a need for disambiguation
- This happens too often to be centralized

---

### Approach Context (Part 2 of main presentation)

Top-level approach breakdown to show thinking and contextualize the demo

**Distinction and articulation of:**

**Ideal solution** - What this would look like in an ideal state, both in terms of this feature and the surrounding ecosystem

- Some centralization exists or is incorporated into it
- Would be modular to lift and shift new methods and capabilities and use elsewhere
- Model Agnostic

**MVP Solution** - If asked to develop my first cut of this for use and evaluation, what it would look like

- Actual ROI discussion and roadmapping
- Some standard framework (but def just some)
- Ideally leveraging central tools
- Post real market research (timeboxed) of at least providers
- Option for consensus
- With Anthropic

**Demo Solution** - The demo I think is illustrative in 2 days

---

### My Demo Method (Part 3 of main presentation)

**What I know about FMC:**

- I know you use Airtable
- I know when I ask about data, you don't say a lot
- I know that I need to demonstrate value quick
  - Add functionality, get buy in, inform the roadmap
- I know that I need to start by meeting you where you are
  - Adding to your stack needs critical mass and value
  - Ryan is adding value but no one is using it
  - Can build the beautiful thing, but without cred, it's not going to get used
- We have to prototype quick to get to value

**My process and decisions:**

Bets:

- I can meet you in Airtable
- OpenAI deepresearch is a sufficient base when paired with subagents

Trades:

- Cheap - GPT for basic LLM usage, Fake Apollo

**How the process led to demo**

---

### Demo (Part 4 of main presentation)

#### The Setup

- **Portco Roles:** Have list of portco roles (company, role, optional note)
- **Open Role:** CFO for Series B SaaS company preparing for growth stage
- **Candidate Pool:** 8 executives (mix of Guild members, network connections)
- **The Challenge:** 3 look similar on paper; AI must surface differentiating signals

#### The Story Arc

1. Role spec gets generated/refined
2. Candidates get researched (show 2-3 in depth)
3. Ranking emerges with reasoning trails
4. User can "drill down" into why #1 beat #2

#### Success Metric

Evaluators should say "I'd actually use this ranking"

---

## Case Parts - Response Components

### Tech Components to Show

- People data ingestion
  - Take in CSVs
  - Normalize the headers and add to db
- People Info Enricher
  - Quick LLM-based search to enrich titles
- People researcher
  - OpenAI deep research API done via prompt template
- Role spec generator
- Candidate Evaluator
- Report generation

### Response Components

- Thinking and perspective
- Defining the problem
- The solution generation process
- The solution (demo)
  - How it works
  - What it does and doesn't address

---

## Items for Review (Sync & Clarify)

- **Implemented vs conceptual components:** Align how you talk about "Role spec generator" and "People Info Enricher" with what is actually implemented vs what is future work in `technical_spec_V2.md` / `solution_strategy_v2_reviewer_draft.md`.
- **Demo story scope:** Decide whether the primary live arc is a single search (e.g., CFO @ Series B SaaS with ~8 candidates) or the 4‑role set described in the strategy; make sure slides and demo expectations match.
- **Ingestion emphasis:** Clarify whether CSV ingestion is shown briefly as a conceptual step or as a live component; the strategy treats ingestion as commodity compared to screening/assessment.
- **Deep Research vs web‑search mode:** Make explicit in the talk track when you are using Deep Research vs a faster web‑search agent, and how that maps to the latency expectations you set.
- **Airtable‑first flow:** Ensure the on‑screen navigation (tables, views, buttons) matches the end‑to‑end flow described in the strategy: Role Spec → Search → Screen → Workflow/Role Eval drill‑downs.
