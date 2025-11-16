# Solution Strategy

> WB's strategic thinking, approach, and key decisions for the FirstMark Talent Signal Agent case study

## Core Understanding

**Problem:**

FirstMark's talent team manually searches their network (Guild members, portfolio executives, partner connections) to match open roles at portfolio companies. This is:
- **Time-intensive:** Research per candidate takes hours
- **Inconsistent:** Different team members use different evaluation criteria
- **Incomplete:** Hard to surface non-obvious matches (e.g., adjacent sector experience)
- **Unscalable:** Can't systematically leverage 1000+ person network

**Core Requirements:**

1. **Match:** Identify and rank potential CTO/CFO candidates for open roles
2. **Explain:** Provide clear reasoning trails for why candidates match (or don't)
3. **Investigate:** Enable drill-down into specific dimensions of fit

**Success Definition:**

System should filter the network to 5-10 high-quality candidates per role, with sufficient reasoning for talent team to prioritize outreach. Augmentation, not replacement.

**Core Items:**

- Ingest, Match, Explain

---

## Response Guiding Principles

- Emphasize the quality of thinking
- Make basic assumptions, and err on the side of KISS where possible
- Demo must be functional
- Most important demo component is the screening workflow

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
  - OpenAI Deep Research API
  - Other deep research API
  - Hugging Face Model
- Open Source Approach/Framework
  - Open Deep research
  - Caml
  - owl
- Custom Agentic

**Decision:** OpenAI Deep Research API + ability to do incremental search via Tavily

**Rationale:** Selected Deep Research API for three reasons:
1. **Speed:** Proven capability to generate comprehensive reports in 3-6 minutes vs days of custom development
2. **Quality:** Demonstrates state-of-the-art research synthesis while allowing focus on assessment logic (the differentiating value)
3. **Integration showcase:** Shows ability to leverage best-in-class external tools rather than NIH syndrome

**Tradeoffs:** Less transparency into research process vs custom agent, but acceptable for demo timeframe. Production would evaluate cost/quality tradeoff (Deep Research ~$0.50-2/candidate vs custom agent ~$0.05-0.20).

**Alternatives Considered:**
- Custom Agentic (Tavily + web scraping): Too time-intensive for 48-hour demo, would shift focus from assessment logic to plumbing
- Open source frameworks: Insufficient maturity/documentation for reliable demo execution

### Granularity & Transparency

**Considerations:**
- Do we need granularity in seeing all sources (aka scraping all source content)
- Are we ok with synthesized report and sources or need to see how put together (aka full internal agent)
- Do we want AI to generate its own non-deterministic grade and pair it with a deterministic hybrid?
  - AKA have 2 assessments - via provided rubric; via own rubric and high level orientation, then match

**Decision:** Hybrid approach - synthesized reports with citations + structured evidence extraction

**Rationale:**
1. **Transparency without overwhelming:** Deep Research provides synthesized narrative with citations; our assessment agent extracts structured evidence against role requirements
2. **Auditability:** Can trace from final score → evidence → source without requiring evaluators to read 20+ web pages
3. **Scalability:** Structured outputs enable systematic comparison across candidates

**Tradeoffs:** Some loss of granular source content vs full scraping, but structured evidence extraction provides sufficient transparency for talent team decision-making.

### Ingestion Method

**Options:**
- Use LLM or code or both for ingestion?

**Decision:** Basic CSV Ingest Via Python

**Rationale:**
1. **Not differentiating:** Data ingestion isn't the value proposition; matching/assessment is
2. **Production reality:** Real system would use Affinity API or Apollo webhooks, not CSV parsing
3. **Time efficiency:** Don't spend demo hours on commodity functionality

**Tradeoffs:** Minimal data validation vs production-grade ETL, but acceptable for demo with controlled mock data.

### LLM Responsibilities

**Options:**
- Research
- Enrichment
- Assessment
- Reporting

**Decision:**
- **Enrichment:** Stub/mock (would be Apollo API in production)
- **Research:** Deep Research API for comprehensive candidate background
- **Assessment:** Dedicated Agno agent with structured outputs for evidence-aware scoring
- **Reporting:** LLM-generated narrative summaries with citations

**Rationale:**
1. **LLM where it adds value:** Research synthesis and assessment reasoning are LLM strengths
2. **Mock where it's commodity:** Apollo enrichment is API call, not LLM problem
3. **Structured where it matters:** Assessment uses structured outputs to ensure consistent, auditable scoring

**Tradeoffs:** Mocking enrichment means demo doesn't show real-time data integration, but avoids Apollo API learning curve with no evaluation benefit.

### UI Platform

**Options:**
- If use deep agents, they have ui
- Streamlit
- Jupyter notebook?

**Decision:** AIRTABLE

**Rationale:**
1. **Meet them where they are:** FirstMark already uses Airtable for talent workflows
2. **Integration story:** Demonstrates ability to augment existing stack vs requiring new tool adoption
3. **Credibility:** Ryan's beautiful tools see low adoption; show pragmatic integration instead
4. **Speed:** Airtable UI + webhooks faster than building Streamlit app

**Tradeoffs:** Less custom UI control vs Streamlit, but higher stakeholder alignment and faster time-to-value.

**Alternatives Considered:**
- Streamlit: Beautiful custom UI but requires new tool in stack, lower adoption likelihood
- Jupyter: Good for technical demo but not usable by talent team in production

### Agent Framework

**Options:**
- Agno
- LangChain
- OpenAI SDK

**Decision:** Agno

**Rationale:**
1. **Built-in patterns:** Agno provides agent patterns (ReActAgent, structured outputs) reducing boilerplate for 48-hour demo
2. **Domain examples:** Strong recruiter/candidate evaluation examples in documentation (`agno_recruiter.md`, `candidate_analyser/`)
3. **Clean integration:** Native support for OpenAI models and structured outputs (Pydantic models)

**Tradeoffs:** Smaller community/ecosystem vs LangChain, but sufficient for demo scope. Production would re-evaluate based on firm-wide standards.

**Alternatives Considered:**
- LangChain: Mature ecosystem but heavier framework, more boilerplate for simple agents
- OpenAI SDK: Too low-level, would require building agent patterns from scratch

### Demo DB Platform

**Options:**
- Local sqlite or supabase
- Airtable

**Decision:** AIRTABLE

**Rationale:**
1. **DB + UI combo:** Single platform provides data storage, UI, and webhooks
2. **Meet them in their stack:** Same rationale as UI platform - integration over innovation
3. **Speed:** Faster than Supabase + separate frontend

**Tradeoffs:** Less query flexibility vs SQL database, but sufficient for demo data volumes and queries.

### Enrichment

**Options:**
- Bright data
- Firecrawl
- Apollo

**Decision:** For now, nothing - Enrichment tool will be stub
- Will mock API response data from Apollo
- Backup: Can use crawl4ai if needed

**Rationale:**
1. **Not differentiating:** Enrichment API calls don't demonstrate AI/agent value
2. **Time efficiency:** Learning Apollo API provides zero evaluation benefit
3. **Production clarity:** Explicitly calling out as "would be Apollo" shows production thinking

**Tradeoffs:** No real-time enrichment demo, but allows focus on assessment logic (the actual AI value).

### Mock Data

**Mock People:**
- Real people for candidates?
- If real, are they portco members? people in the room?
- **Decision:** REAL PEOPLE, Part from scrape, others we can search

**Rationale:** Real profiles create more realistic demo narrative and enable evaluators to verify research quality against their own knowledge.

**Mock Companies:**
- Real companies?
- **Decision:** Yes, subset of portcos

**Rationale:** Using actual FirstMark portfolio companies demonstrates domain knowledge and makes demo relatable to evaluators.

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

**Rationale:**
1. **Incremental value delivery:** Candidate profiles would be a central platform feature (Tier 1 vision), not demo requirement
2. **Time efficiency:** Building standardized profiles requires more refinement on schema, refresh cadence, etc.
3. **Sufficient for demo:** Bespoke research per role-match shows the value; standardized profiles are optimization

**Tradeoffs:** Repeated research vs cached profiles, but acceptable for 4-role demo scope.

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
- OpenAI deep research is a sufficient base when paired with subagents

**Trades:**
- Cheap - GPT for basic LLM usage, Fake Apollo

---

## Success Metrics

**Demo succeeds if:**

1. **Usability test:** Evaluators say "I'd actually use this ranking" (primary metric)
2. **Transparency test:** Can trace reasoning for why #1 candidate beat #2
3. **Product thinking test:** Clear path from demo → MVP → production is evident
4. **Technical credibility test:** Architecture choices defensible under Q&A

**Evaluation criteria alignment:**

- **Product Thinking (25%):** Demonstrated via 3-tier framework, FMC-specific customization (Airtable integration), stakeholder calibration ("meet them where they are")
- **Technical Design (25%):** Shown through Agno framework selection, structured outputs with Pydantic models, evidence-aware scoring methodology
- **Data Integration (20%):** Evidenced by structured (CSV) + unstructured (web research via Deep Research API) synthesis
- **Insight Generation (20%):** Proven via ranked outputs with reasoning trails, evidence extraction against role requirements, counterfactuals ("why not candidate X")
- **Communication (10%):** Delivered through clear presentation mapping and demo narrative

---

## Key Risks & Mitigations

### Technical Risks

**Risk:** Live demo timing (Deep Research = 3-6 min/candidate)
- **Mitigation:** 3 pre-run scenarios + 1 live execution OR toggle to Web Search mode (1-2 min/candidate)
- **Contingency:** If live fails, pre-run results show full functionality; live execution is additive, not critical path

**Risk:** API rate limits or failures during demo
- **Mitigation:** Pre-run results as primary demo content; live execution demonstrates real-time capability but isn't required for evaluation
- **Contingency:** Have API keys with sufficient rate limits; test thoroughly pre-demo

**Risk:** Webhook/ngrok instability for Airtable integration
- **Mitigation:** Test thoroughly pre-demo; have markdown/JSON exports showing full audit trail as backup
- **Contingency:** Can show integration architecture via code walkthrough if live webhook fails

**Risk:** Assessment reasoning appears opaque or AI-generated fluff
- **Mitigation:** Structured outputs with citations, evidence-aware scoring (None for insufficient data), counterfactuals ("why this candidate beats alternatives")
- **Validation:** Pre-demo review of reasoning quality; ensure traces from score → evidence → source

### Strategic Risks

**Risk:** Evaluators question lack of real data integration (Apollo, Affinity)
- **Mitigation:** Explicitly position as demo limitation; production roadmap addresses in MVP tier (Tier 2)
- **Communication:** "In production, this would be Apollo API call returning: [show mock data structure]"

**Risk:** Demo appears over-engineered for simple matching problem
- **Mitigation:** 3-tier framework shows demo as simplified version; emphasize incremental value delivery
- **Communication:** "Demo proves value before infrastructure investment; MVP would add X, Y, Z"

**Risk:** Unclear differentiation from "just use ChatGPT to search candidates"
- **Mitigation:** Emphasize systematic process, structured outputs, auditability, integration with existing workflow
- **Communication:** "Ad-hoc ChatGPT requires manual synthesis; this provides consistent, auditable, integrated workflow"

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
