# Solution Strategy

> WB's strategic thinking, approach, and key decisions for the FirstMark Talent Signal Agent case study

## Core Understanding

**Key Requirements:**

- Needs to match the candidate
- Roles - CFO and CTO
- Ability to Diagnose/investigate 'match'

**Core Items:**

- Ingest, Match, Explain

---

## Response Guiding Principles

- Emphasize the quality of thinking
- Make basic assumptions, and err on the side of KISS where possible
- Demo must be functional
- Most important demo compoennt is the screening workflow

---

## Strategic Approach Context

Top-level approach breakdown to show thinking and contextualize the demo

### Distinction and Articulation of Three Solution Tiers

#### Ideal Solution

What this would look like in an ideal state, both in terms of this feature and the surrounding ecosystem:

- Some centralization exists or is incorporated into it
- Would be modular to lift and shift new methods and capabilities and use elsewhere
- Model Agnostic

#### MVP Solution

If asked to develop my first cut of this for use and evaluation, what it would look like:

- Actual ROI discussion and roadmapping
- Some standard framework (but def just some)
- Ideally leveraging central tools
- Post real market research (timeboxed) of at least providers
- Option for consensus
- With Anthropic

#### Demo Solution

The demo I think is illustrative in 2 days

---

## Key Strategic Decisions

### Research Method

**Options:**
- Out of the box API
  - OpenAI Deepresearch API
  - Other deep research API
  - Hugging Face Model
- Open Source Approach/Framework
  - Open Deep research
  - Caml
  - owl
- Custom Agentic

**Decision:** OpenAI Deep research API + ability to do incremental search via Tavily

**Reason:** Good enough for demo purposes; demonstrates integration capability

### Granularity & Transparency

**Considerations:**
- Do we need granularity in seeing all sources (aka scraping all source content)
- Are we ok with synthesized report and sources or need to see how put together (aka full internal agent)
- Do we want AI to generate its own non-deterministic grade and pair it with a deterministic hybrid?
  - AKA have 2 assessments - via provided rubric; via own rubric and high level orientation, then match

### Ingestion Method

**Options:**
- Use LLM or code or both for ingestion?

**Decision:** Basic CSV Ingest Via Python

**Reason:** Wouldn't be part of this in reality, and pretty basic

### LLM Responsibilities

**Options:**
- Research
- Enrichment
- Assessment
- Reporting

**Decision:**
- Enrichment is going to be fake (because will be Apollo anyway)
  - Not doing real apollo because haven't used it
  - Other options could have used
- Research
  - API Tool
  - Subagent for search and extract
- Distinct Agent for assessment and reporting

### UI Platform

**Options:**
- If use deep agents, they have ui
- Streamlit
- Jupyter notebook?

**Decision:** AIRTABLE

**Reason:** Meet FirstMark where they are; demonstrate ability to integrate with existing stack

### Agent Framework

**Options:**
- Agno
- LangChain
- OpenAI SDK

**Decision:** Agno

### Demo DB Platform

**Options:**
- Local sqlite or supabase
- Airtable

**Decision:** AIRTABLE

**Reason:** DB & UI features quickly; meet them in their stack

### Enrichment

**Options:**
- Bright data
- Firecrawl
- Apollo

**Decision:** For now, nothing - Enrichment tool will be stub
- Will mock API response data from Apollo
- Backup: Can use crawl4ai if needed

### Mock Data

**Mock People:**
- Real people for candidates?
- If real, are they portco members? people in the room?
- **Decision:** REAL PEOPLE, Part from scrape, others we can search

**Mock Companies:**
- Real companies?
- **Decision:** Yes, subset of portcos

**Mock Roles:**
- 4 roles, 2 CTO + 2 CFO
- Real portcos
- Series A - D
- Easy portcos to characterize and find CTO and CFO for
- **Decision:** Done

**Data Edge Cases:**
- Non-normalized names, field names
- Bios just one text file

### Candidate Profile

**Question:** Do we skip creating profile and just have bespoke research anchored on spec for now?

**Decision:** Yes, skip

**Reason:** "Probably takes some more refinement on what a profile is, if we keep standardized profiles or auto-gen when create new person (of x y z type)"

---

## Demo Method & Bets

### What I Know About FMC

- I know you use Airtable
- I know when I ask about data, you don't say a lot
- I know that I need to demonstrate value quick
  - Add functionality, get buy in, inform the roadmap
- I know that I need to start by meeting you where you are
  - Adding to your stack needs critical mass and value
  - Ryan is adding value but no one is using it
  - Can build the beautiful thing, but without cred, it's not going to get used
- We have to prototype quick to get to value

### My Process and Decisions

**Bets:**
- I can meet you in Airtable
- OpenAI deepresearch is a sufficient base when paired with subagents

**Trades:**
- Cheap - GPT for basic LLM usage, Fake Apollo

---

## Talking Points (Items to Cover in Presentation)

### General Context

Ultimate design depends on Time, Value, and security concerns

- Security is a firm-level decision and it needs to be clear

### Distinguish Demo from Other Scenarios

- Ideal would already have x, and would approach by doing y
- MVP Would have x, would spend more time to do

### Framework Philosophy

We are creating frameworks to help guide LLM and standardize and compound what we do

The ideal model for FirstMark AI path is a guild:
- There are forward-deployed development use cases
- Centralized foundation and standards building

### Market Research Approach

In ideal and MVP, would start by identifying what solutions are in the market:

**Are there solutions that can perform this e2e?**
- Cost, performance

**Are there solutions that can perform parts?**
- EG enrichment - Apollo, People data labs
- Candidate AI Eval
- Networking Matching

**What are the development options?**
- General python Frameworks & LLM frameworks (Ideally firm standard)
- Research approaches
  - Research as API
  - Open source approaches
  - Custom

### Decision to Skip Candidate Profile

There is a world where we have a standardized set of information that we collect, synthesize and maintain for certain people:
- Trade is always keep all data just in case, and not reinvesting the full wheel vs data storage problems
- I don't think it's mission critical
- I think we can do it as an extension if we want

### Business Context Points

**Differentiation:**
- Differentiation helps, have guild, use it
- Case of thing that is done many times in peoples minds in different ways --> Get value from rationalizing and augmenting
- People evaluation is a fundamental pillar of VC, especially early stage

**Requirements and Components:**
- Recall over precision
  - Rather not miss a great match vs see some dudes
- The goal is not to make the decision, it's to filter and focus review
  - Needs to sufficiently filter who is reviewed
  - Needs to inform review of an individual (pop key info, enable quick action)
  - Needs to enable investigation
- The target is augmentation, not replacement
- The goal is to:
  - Validate the quality of research methods
  - Validate the quality of the evaluation and traces
  - Cut operational cost
  - Optimize execution time
- Our future cases for extension are:
  - Other people enrichment and research use cases - founders, LPs, hires
  - Applications could be current and or retroactive

**Key Complexity Points and Decisions:**

Boundaries:
- What parts of this are central and universal
  - EG. Person intake and normalization
- What parts of this are standard practices beyond this use case
  - Is enrichment on all People?
  - What is the cadence of
- What do we keep+Maintain vs Keep+Redo vs toss
  - Do we try to define refresh process?

Technical considerations:
- Where do we need LLM
- What is the balance of enabling vs confining the LLM
- How we guardrail LLM
- How do we optimize human engagement?
- Where do we build vs buy?
  - And where start from scratch vs leverage existing methods

Known messy corners:
- Titles will be non-normalized
- There will be a need for disambiguation
- This happens too often to be centralized

---

## Future State Vision

### TIER 1: Target Production System (12-18 month vision)

**TLDR:** Rationalized Schema, Central Storage, Standard Operation and orchestration

#### Data Platform (Conceptual - Not Building)

**Scope:** Enterprise-grade talent intelligence platform

Ideally, have centralized and universal foundation:

- Centralized data platform (Affinity integration, immutable event log)
- Real-time enrichment (Apollo, Harmonic) for people and companies as necessary
- Standardized LLM Web search
- Foundational Artifact pieces (Role spec, Assessment method)

In an ideal scenario, data ingestion and storage is a distinct evergreen component of the broader system:

**Central Data Store:**
- Central table storing core information for all use cases
  - Including people, roles (title + company), companies, relationships
  - Also Canonical title mapping table and mechanism
- Standardized ETL pipelines for ingestion
  - Extract, Normalize, Reconcile Entity (Person, Company, etc) with existing data and appends new records
- Ideally, the system is immutable
  - Ability only to add new records and identify and relate active items
- Parallel operations storage system
  - Standardized logging of all events

**Standard Operations:**
- Standardized operations that can be run on records that are also evergreen
  - Including enriching people/companies via Apollo
  - That return the raw enrichment request response, the cleaned response content, and the enrichment data
  - Enrich the record
  - Store enrichment results, before and after
- When new people need to be added, they are imported, cleaned, mapped
  - Where mapping is unclear, HITL loop

**Additional Platform Features:**
- Storage and maintenance process for open roles (maybe just active searches)

**Open Questions:**
- Would we decompose down to role name table?
- How handle location? Is both person and role based, and subject to change
- Can we use Affinity as Central source of people truth? What does Affinity design look like

### TIER 2: MVP for Hypothesis Validation (1-month sprint)

**Scope:** Prove value before infrastructure investment

- Use whatever APIs you have - harmonic, apollo, etc
- Standard Python frameworks
- Standard LLM Framework (ADK maybe?)
- Research via
  - External Provider(s)
  - In-house agent (either via framework or full custom build)
- Would store content from all cited items
- Would want better investigation capability

### Future Ideas to Potentially Cover

- Mock interview
- Generalized enrichment
- Historical Role analysis (profiling, fit estimate)

### Future Questions

- What does Affinity API look like? What is data schema like?
- What is current hygiene
- Who are biggest slackers
- What does Apollo API look like?
- Would Affinity be ideal source of truth?
- Where and how is guild managed now?
