# Solution Strategy – Reviewer-Augmented Draft (v2)

> Refined, reviewer-aligned strategy for the Talent Signal Agent demo. This version tightens the original `solution_strategy_v2.md` with clearer flows, scoring, and data integration, while keeping the same core bets and architecture.

---

## 1. Core Understanding

**Problem.** FirstMark’s talent team manually searches their network (Guilds, portfolio execs, partner connections) to match open roles at portfolio companies. Today this is:
- **Time‑intensive:** Research per candidate can take hours.
- **Inconsistent:** Different people apply different criteria and heuristics.
- **Incomplete:** Non‑obvious matches (adjacent sectors, stage transitions) are easy to miss.
- **Unscalable:** The network is large (1000+ executives); the process is bespoke.

**What we’re building.** A “Talent Signal Agent” that:
1. Ingests small but realistic **structured** data (Guilds, exec network) + **unstructured** data (bios, articles, LinkedIn‑style text, JDs).
2. **Identifies and ranks** potential CTO/CFO candidates for a given open role.
3. Produces a **transparent reasoning trail** for each recommendation.

**Success definition.** For a single search (e.g., CTO @ Estuary), the system should:
- Narrow the universe to **5–10 prioritized candidates**.
- Provide **evidence‑backed reasoning** that a recruiter would actually use.
- Integrate into the existing **Airtable‑centric workflow** (no net‑new tool adoption).

---

## 2. Guiding Principles

- **Meet you where you are.** Design around Airtable as DB + UI, with minimal, well‑scoped Python.
- **Screening over infra.** Focus on the Module 4 screening workflow, not generic data platform work.
- **Spec‑guided, not free‑form.** Use a single, role‑spec‑guided evaluation; defer model‑generated rubrics to later phases.
- **Evidence‑aware, not overconfident.** Never force scores; allow `Unknown` when public data is thin.
- **Demo ≠ production.** Be explicit about what’s demo‑only vs what would harden in a 1–3 month MVP.

---

## 3. Solution Tiers (Context)

These tiers are primarily for framing during the presentation; the demo itself is Tier 0.

### 3.1 Ideal Production System (Tier 1 – 12–18 months)

- Centralized talent intelligence layer (Affinity + Apollo/Harmonic) with:
  - Immutable events for people, roles, companies, relationships.
  - Standardized enrichment + search operations.
  - Canonical schemas and title/role normalization.
- Rich investigation flows (historical roles, mock interviews, longitudinal performance signals).

### 3.2 MVP for Hypothesis Validation (Tier 2 – 1 month)

- Real integrations (Apollo/Harmonic/Affinity), productionized agents, better caching.
- Wider role coverage (beyond CTO/CFO) and more flexible role spec templates.
- Stronger investigation and iteration tools for talent partners.

### 3.3 Demo Implementation (Tier 0 – This Case)

- **Airtable** as both DB and UI.
- **Flask + ngrok** webhook server with two endpoints (`/upload`, `/screen`).
- **AGNO** agents:
  - Research via `o4-mini-deep-research` (Deep Research API).
  - Assessment via `gpt-5-mini` with structured outputs.
- **Spec‑guided evaluation only,** against a small number of CTO/CFO roles and candidates.

---

## 4. Key Strategic Decisions (Tightened)

### 4.1 Research Method

**Options considered**
- Deep Research‑style APIs (OpenAI Deep Research, others).
- Open‑source agents (Caml, OpenDeepResearch, Owl, custom Tavily stack).
- Fully custom agentic research.

**Decision.** Use **OpenAI Deep Research API (`o4-mini-deep-research`)** as the primary research engine, optionally backed by OpenAI web search (`web_search_preview`) for faster runs.

**Why.**
1. **Time‑boxed quality.** Deep Research reliably returns 2–5 minute executive research reports with citations, which is appropriate for a live demo and resembles a real recruiter workflow.
2. **Keeps the “interesting” part in assessment.** The differentiation here is how we structure, score, and explain matches — not whether we can orchestrate our own crawler.
3. **Reasoning & citations built in.** We can lean on the API’s multi‑step reasoning and citation support, then post‑process into our own structured schema (`ExecutiveResearchResult`).

**Tradeoffs.**
- Less control over the underlying multi‑step plan than a custom agent; acceptable for a 48‑hour demo.
- In production we would benchmark Deep Research vs an in‑house agent on:
  - Cost per candidate.
  - Coverage of key dimensions.
  - Stability/latency.

---

### 4.2 Granularity & Transparency

**Decision.** Use **synthesized reports + structured evidence extraction** instead of raw page‑level scraping.

- Deep Research returns a structured understanding of the executive + citations.
- Our **assessment agent** extracts dimension‑level evidence and scores against the role spec using `ExecutiveResearchResult` as input.

**Why this is sufficient.**
- **Traceability.** We can go: overall score → dimension score → evidence quotes → citation URLs, without dumping every web page.
- **Cognitive load.** Recruiters don’t want 20 tabs; they want 1–2 paragraphs per candidate plus an at‑a‑glance scorecard.

---

### 4.3 Ingestion & Data Shape

**Decision.** Use **CSV ingest via Python** for demo data, with schemas aligned to `Mock_Guilds.csv` and `Exec_Network.csv`.

- `/upload` endpoint:
  - Accepts an Airtable attachment (CSV).
  - Normalizes into the Airtable People table (and optionally related tables).
  - Handles simple cleaning only (types, enums, whitespace).

**Rationale.**
- The differentiator is not ETL; it’s matching and assessment.
- In production we would pivot to APIs (Affinity, Apollo, Harmonic) and treat CSV upload as a fallback.

---

### 4.4 LLM Responsibilities

**Final split.**
- **Research:** Deep Research → `ExecutiveResearchResult`.
- **Assessment:** `gpt-5-mini` → `AssessmentResult` (spec‑guided).
- **Reporting:** `gpt-5-mini` generates a short narrative summary per candidate.
- **Enrichment:** Stub/mock Apollo response (explicitly demo‑only).

This keeps LLMs focused on **reasoning and explanation**, not on boilerplate enrichment or ingestion.

---

### 4.5 UI & DB Platform

**Decision.** Use **Airtable as both UI and DB**, with:
- Tables for People, Roles, Searches, Screens, Role Specs, and Operations/Workflows (per `technical_spec_V2.md`).
- Role and search management (Modules 2 and 3) as **Airtable‑only flows.**

**Why.**
- You already live in Airtable for talent workflows.
- Low setup friction; no new UI surface.
- We can demonstrate a real “click button → see candidates ranked” flow.

---

### 4.6 Agent Framework

**Decision.** Use **AGNO** as the agent framework for:
- Research agent (`create_research_agent`), wrapping `o4-mini-deep-research`.
- Assessment agent (`create_assessment_agent`), wrapping `gpt-5-mini` with Pydantic outputs.

**Reasons.**
- Good fit with structured outputs and agent patterns.
- Existing recruiter/candidate evaluation examples.
- Cleaner than building from scratch on the raw OpenAI SDK for a 48‑hour demo.

---

### 4.7 Mock Data Strategy

- **People.** Real executives (where appropriate) plus synthetic entries, drawn from:
  - Guild member scrapes (`reference/guildmember_scrape.csv`).
  - Manually curated network entries.
- **Companies.** Real FirstMark portfolio companies for 3–4 searches (Pigment, Mockingbird, Synthesia, Estuary).
- **Roles.** 4 roles in scope:
  - 2x CFO (e.g., Pigment, Mockingbird).
  - 2x CTO (e.g., Synthesia, Estuary).

---

## 5. End‑to‑End Demo Flow (Module 4)

This is the story we will tell live. It uses the Flask `/screen` endpoint and Airtable as the only UI the evaluators touch.

### 5.1 Single Search Walkthrough (CTO @ Estuary)

1. **Define role & search (Airtable).**
   - In `Role Spec` table, select or lightly customize a **CTO template** for Estuary:
     - Dimensions (e.g., Stage fit, Sector fit, Technical leadership, Team‑building, Scale/SaaS experience, Context fit).
     - Weights and evidence expectations per dimension (from `technical_spec_V2.md`).
   - In `Search` table, create a new search linked to:
     - The Estuary role record.
     - The chosen role spec.

2. **Select candidate batch (Airtable).**
   - In `Screen` table, create a new Screen record:
     - Link to the Estuary search.
     - Link 5–15 candidate records from the People table (Guild members + exec network).
     - Optionally add custom guidance (e.g., “prior data infra experience preferred”).

3. **Trigger screening (Airtable → Flask).**
   - Click a **“Start Screening”** button or set Status to `Ready to Screen`.
   - Airtable Automation posts to `/screen` with:
     - `screen_id`.
     - Linked candidate IDs.
     - Linked role_spec_id.

4. **Run research for each candidate (Flask + AGNO).**
   - For each candidate:
     - Create a Workflow record in `Operations - Workflows`.
     - Call the **Research agent**:
       - Uses `o4-mini-deep-research` with a structured prompt (see §6.1).
       - Writes an `ExecutiveResearchResult` JSON into the Workflow record.
       - Logs citations and any gaps (missing data) explicitly.

5. **Run assessment (Flask + AGNO).**
   - The **Assessment agent** consumes:
     - The role spec (dimensions, weights, must‑haves).
     - The `ExecutiveResearchResult` struct.
   - It returns an `AssessmentResult`:
     - Dimension scores (1–5 or `null` for unknown).
     - Must‑haves check.
     - Overall score (0–100).
     - Summary and counterfactuals.

6. **Write results back to Airtable.**
   - Store:
     - **Per‑candidate assessment** in `Role Eval` table (linked to Search, Screen, Person).
     - **Aggregated Screen view** (sorted by overall score) via Airtable views.
   - Update Screen `Status` from `Draft → Processing → Complete`.

7. **Review and drill down (live demo).**
   - In the `Screen` interface:
     - Show ranked candidates with:
       - Overall score and confidence.
       - Top 2–3 dimensions driving the score.
       - Short summary (“why this candidate beats #2”).
     - For any candidate:
       - Open the Workflow record to see:
         - Short research summary.
         - Evidence quotes + citation URLs.

---

## 6. Scoring & Data Integration

### 6.1 Research Prompt Shape (Deep Research)

For each executive, we give `o4-mini-deep-research`:
- **Inputs:**
  - Name, current title, current company (from People table).
  - LinkedIn URL if available.
  - Optional hints (e.g., “this person is in the FirstMark CTO Guild”).
- **Instructional goals:**
  - Produce a concise narrative suitable for **CTO/CFO evaluation.**
  - Return:
    - Career timeline (companies, roles, dates, achievements).
    - Sector and stage exposure (Seed → Growth).
    - Functional scope and team size.
    - Notable achievements (fundraising, exits, major launches).
    - Gaps: what we could not find.
  - Include **citations** (URLs + short quotes).
- **Output mapping:**
  - The response is parsed into `ExecutiveResearchResult`:
    - `career_timeline`, `sector_expertise`, `stage_exposure`, narrative summary, `citations`, and `gaps`.

This keeps research **repeatable and schema‑aligned** while still leveraging Deep Research’s reasoning.

---

### 6.2 Scoring Model (`AssessmentResult`)

The assessment is **spec‑guided** and **evidence‑aware**. At a high level:

- Each role spec defines 5–7 **dimensions**, e.g. (for CTO):
  - Stage fit (has operated at similar stage).
  - Sector fit (relevant or adjacent domains).
  - Technical leadership (scope of engineering org, architecture leadership).
  - Team building & recruiting.
  - Scale / complexity experience.
  - Context fit (geo, business model, founder profile).
- Each dimension has:
  - Weight (e.g., 0.1–0.3).
  - Evidence expectancy (how observable from public data).

**Per‑dimension scoring.**
- The assessment agent produces a `DimensionScore`:
  - `score`: integer 1–5, or `null` if insufficient public evidence.
  - `evidence_level`: High/Medium/Low (from the spec’s guidance).
  - `confidence`: High/Medium/Low (LLM’s self‑assessment).
  - `reasoning`: 2–4 sentences referencing research findings.
  - `evidence_quotes` and `citation_urls`: pulled directly from `ExecutiveResearchResult.citations`.

**Must‑haves.**
- Role specs declare a small set of **must‑have requirements** (e.g., “Has led engineering at Series B+ SaaS company”).
- `must_haves_check` encodes:
  - `requirement`, `met: bool`, `evidence`.
- A candidate failing a hard must‑have can:
  - Have their overall score capped.
  - Be flagged in `red_flags_detected`.

**Overall score calculation.**
- Implemented in Python, not inside the LLM:
  - Filter out dimensions where `score is None`.
  - Weighted average of remaining dimensions.
  - Optional small boost for:
    - High evidence‑level dimensions.
    - High confidence.
  - Scale to **0–100** for Airtable display.

This gives a **simple, explainable scoring model** that directly supports the “I’d actually use this ranking” test.

---

### 6.3 Structured + Unstructured Data Integration

**Structured fields** (from CSV/Airtable):
- Function (CTO vs CFO).
- Stage, sector, geography, current company size.
- Relationship metadata (Guild vs portfolio vs network).

**Unstructured signals** (from research):
- Narrative evidence of:
  - Stage transitions (Seed → Series B → Growth).
  - Domain depth (data infra vs dev tools vs consumer).
  - Scope (org size, global vs regional).
  - Notable achievements.

**Integration pattern.**
- Structured fields:
  - Used as **filters** (e.g., only CTOs for CTO role).
  - Provide initial priors (e.g., exact stage, sector).
- Unstructured fields:
  - Flow through `ExecutiveResearchResult` into `DimensionScore.reasoning`.
  - Fill gaps where structured data is missing or noisy.

The result is a rank that is **more than a filter** but still grounded in the explicit, structured data the team already tracks.

---

## 7. Risks & Mitigations (Summarized)

**Deep Research latency.**
- Mitigation: Pre‑run 3 scenarios; run 1 live with smaller candidate set.
- Fallback: Switch `USE_DEEP_RESEARCH=false` to use web search mode (1–2 minutes per candidate).

**Webhook / ngrok fragility.**
- Mitigation: Dry‑run automations pre‑demo; keep ngrok and Flask logs visible.
- Fallback: Walk through the workflow using pre‑populated Workflow/Role Eval records.

**Perceived “black box” behavior.**
- Mitigation: Emphasize:
  - Pydantic schemas.
  - Evidence‑aware scoring (nulls allowed).
  - Direct citation links and `gaps` field.

**“Why not just ChatGPT?” question.**
- Answer: This solution:
  - Operates on **your Airtable data** and work views.
  - Produces **consistent, comparable scores** aligned to explicit role specs.
  - Leaves a durable **audit trail** for future searches.

---

## 8. How This Maps to the Case Rubric

- **Product Thinking (25%).**
  - Airtable‑first UX, clear module separation, explicit demo vs MVP vs ideal.
  - Focus on screening workflow and recruiter usability.
- **Technical Design (25%).**
  - AGNO agents with structured outputs, clear scoring model, and simple webhook architecture.
- **Data Integration (20%).**
  - Joins structured CSV/Airtable data with unstructured Deep Research outputs via explicit schemas.
- **Insight Generation (20%).**
  - Ranked, explainable outputs with per‑dimension reasoning and citations.
- **Communication & Clarity (10%).**
  - End‑to‑end flow that can be walked in 3–5 minutes, with clear tradeoffs and future extensions.

