# Technical Implementation Specification V2

> Detailed technical design, architecture, data models, and implementation guide for the Talent Signal Agent demo

---

## 1. Overview & Key Decisions

### Technology Stack

**Framework & Models:**
- **Framework:** AGNO (agent framework)
- **LLM Models:**
  - Person Research: OpenAI Deep Research API (`o4-mini-deep-research`)
  - Assessment: GPT-5 or GPT-5-mini (`gpt-5`, `gpt-5-mini`)
  - Web Search: OpenAI native web search (`web_search_preview` builtin tool)
  - Reference: `reference/docs_and_examples/agno/agno_openai_itegration.md`

**Infrastructure:**
- **DB & UI:** Airtable
- **Backend:** Python script with Flask webhook server
- **Tunnel:** ngrok (for local demo)
- **APIs:** OpenAI Deep Research API, OpenAI API, OpenAI Web Search
- **Libraries:** pyairtable, Flask, python-dotenv

### Demo Scope

**All 4 modules in scope:**
1. Module 1 (Data Upload) - ✅ CSV ingestion via webhook
2. Module 2 (New Open Role) - ✅ Airtable-only (no Python)
3. Module 3 (New Search) - ✅ Airtable-only (no Python)
4. Module 4 (New Screen) - ✅ Primary workflow (webhook + Python)

**Demo Execution Strategy:**
- **3 portcos:** Pre-run results ready (Pigment CFO, Mockingbird CFO, Synthesia CTO)
- **1 portco:** Live execution during demo (Estuary CTO)
- **Candidates:** Sourced from `reference/guildmember_scrape.csv` (64 executives)

### Design Principles

- **Recall over Precision:** "Rather not miss a great match vs see some duds"
- **Filter, Don't Decide:** Goal is to focus review, not replace human judgment
- **Augmentation, Not Replacement:** Enhance talent team capabilities
- **Success Metric:** "Evaluators should say 'I'd actually use this ranking'"

### Research & Assessment Strategy

**Research Execution:**
- **Primary Method:** OpenAI Deep Research API (`o4-mini-deep-research`)
  - Comprehensive executive research with multi-step reasoning
  - Built-in citation extraction and source tracking
  - Returns markdown content + citations (no structured JSON)
  - ~2-5 minutes per candidate
- **Parser Step (Structured Output):** `gpt-5-mini` (or `gpt-5`) parser agent
  - Consumes Deep Research markdown + citations (or fast web search results)
  - Produces structured `ExecutiveResearchResult` Pydantic objects
  - Written to Airtable `Research_Results.research_json` as JSON
- **Supplemental Method:** OpenAI Web Search Builtin (`web_search_preview`)
  - Assessment agent can verify claims and look up context
  - Person researcher can use for quick fact-checks
  - Real-time search capability during evaluation
- **Flexible Mode:** Can switch to web-search-only for faster demos (~30-60 sec/candidate)

**Assessment Approach:**
- **Single Evaluation (Spec-Guided):** LLM guided via role spec with evidence-aware scoring
- **Evidence-Aware Scoring:** Uses `None`/`null` for insufficient evidence (no forced guessing)
- **Confidence Tracking:** High/Medium/Low based on evidence quality and LLM self-assessment
- **Model-Generated Rubric:** Explicitly deferred to Phase 2+ (not in demo)

### Planning Document Map

This technical spec is supported by more detailed planning docs:
- **Data Models / Pydantic Schemas:** `demo_planning/data_design.md`
- **Airtable Schema & Field Definitions:** `demo_planning/airtable_schema.md`
- **Role Spec System & Templates:** `demo_planning/role_spec_design.md`
- **Research Pipeline Details:** `demo_planning/deep_research_findings.md`
- **Alignment Review & Fix Log:** `demo_planning/alignment_issues_and_fixes.md`

For schema changes, update `data_design.md` first, then sync `airtable_schema.md` and this technical spec.

### Role Spec Design

- **Structure:** Fully defined in `demo_planning/role_spec_design.md`
- **Format:** Markdown-based specs stored in Airtable Long Text field
- **Dimensions:** 6 weighted dimensions per spec (CFO and CTO templates)
- **Evidence Levels:** High/Medium/Low for each dimension
- **Storage:** Individual records with template vs customized versions

---

## 2. Architecture

### Webhook Architecture (Flask + ngrok)

**Design:**
- Single Python codebase (webhook receiver + AI workflow + Airtable writes)
- Flask-based webhook receiver with ngrok tunnel for local demo
- Simple setup (~15 min), full automation, no cloud deployment needed

**Flow:**
```
Airtable Trigger (Button click OR Status field change)
  → Airtable Automation (webhook trigger)
  → ngrok public URL (tunnel to localhost)
  → Flask server on localhost:5000
  → Python matching workflow (research + assessment)
  → Write results back to Airtable
  → Update status field
```

**Benefits:**
- All logic in one place
- Real-time visibility (terminal logs during execution)
- Local hosting OK for demo
- Full automation (button click → results)

### Workflow Architecture

**Complete Specification:**
- **See:** `demo_planning/screening_workflow_spec.md` for full implementation details
- **Pattern:** Research → Quality Gate → Conditional Supplemental Search (Loop) → Assessment
- **Execution:** Synchronous for demo (async optimization post-demo)
- **Key Features:**
  - Intelligent research quality checks
  - Bounded iteration (max 3 supplemental searches)
  - Full audit trail via event streaming
  - Error handling with exponential backoff

#### Research Quality Gate (Step 2)

The workflow includes an explicit sufficiency check immediately after the deep research agent. This prevents unnecessary supplemental searches and makes the behavior predictable for the demo.

**Sufficiency Criteria:**
- ≥3 key experiences captured
- ≥2 domain expertise areas identified
- ≥3 distinct citations
- Research confidence is High or Medium
- ≤2 information gaps remain

**Outputs:**
- Enriched `ExecutiveResearchResult` plus `quality_metrics`
- Boolean `is_sufficient`
- `gaps_to_fill` list for supplemental search instructions

**Decision:** If `is_sufficient = True`, the workflow proceeds directly to assessment. Otherwise the supplemental search branch is invoked.

#### Conditional Supplemental Search (Step 3)

- Triggered only when the quality gate returns `is_sufficient = False`
- **Step 3a – Prep:** Build targeted prompts/queries anchored to `gaps_to_fill`
- **Step 3b – Loop:** Web-search agent executes up to **3 iterations**; each iteration receives prior findings to avoid duplication
- **Step 3c – Merge:** Supplemental findings combine with the original research before assessment

**Loop Mechanics (Step 3b):**
The loop exits early when both conditions are met:
1. ≥2 new findings are surfaced during the latest iteration, and
2. Either (a) the supplemental output’s confidence is High **or** (b) there are no remaining gaps.

If the break condition is never satisfied, the loop halts automatically after the third iteration to preserve deterministic timing for the demo.

### Flask Endpoints & Trigger Options

**Endpoints:**
- `/upload` - Data ingestion (CSV → clean → load → People table)
- `/screen` - Run candidate screening workflow (Module 4)

**Modules 2 & 3:** Airtable-only (no Python endpoints needed)
- Keeps Python surface area small
- Single codebase with only automation-needed endpoints
- Can extend with additional endpoints later

**Trigger Options:**
- **Button:** Explicit action button in record (e.g., "Start Screening")
- **Status Field:** Automation triggers when field changes (e.g., Status → "Ready to Screen")
- **Recommended:** Status field triggers for natural workflow and state management

### Demo Flow (Status Field Trigger)

1. Create Screen record, link candidates and search
2. Change Status field to "Ready to Screen"
3. Automation fires → Terminal shows live progress with emoji indicators
4. Status auto-updates: Draft → Processing → Complete
5. Refresh Airtable to see populated Assessment results
6. Show ranked candidates view with reasoning and drill-down

### Setup

```bash
# Install dependencies
pip install flask pyairtable python-dotenv

# Start Flask server
python webhook_server.py

# Start ngrok (separate terminal)
ngrok http 5000

# Configure Airtable automation with ngrok URL
```

---

## 3. Data Design

### Input Data Schemas

#### Structured: Mock_Guilds.csv
(One row per guild member seat)

- `guild_member_id` (string) – unique row id
- `guild_name` (string) – e.g., CTO Guild, CFO Guild
- `exec_id` (string) – stable id used across all tables
- `exec_name` (string)
- `company_name` (string)
- `company_domain` (string, optional) – acmeco.com
- `role_title` (string) – raw title (SVP Engineering, CFO)
- `function` (enum) – CTO, CFO, CPO, etc.
- `seniority_level` (enum) – C-Level, VP, Head, Director
- `location` (string) – city/region; can normalize to country
- `company_stage` (enum, optional) – Seed, A, B, C, Growth
- `sector` (enum, optional) – SaaS, Consumer, Fintech, etc.
- `is_portfolio_company` (bool) – whether it's FirstMark portfolio

#### Structured: Exec_Network.csv
(One row per known executive in the wider network)

- `exec_id` (string) – primary key; matches Mock_Guilds.csv
- `exec_name` (string)
- `current_title` (string)
- `current_company_name` (string)
- `current_company_domain` (string, optional)
- `role_type` (enum) – normalized function: CTO, CFO, CRO, etc.
- `primary_function` (enum, optional) – broader grouping: Engineering, Finance, Revenue
- `location` (string)
- `company_stage` (enum, optional) – current company stage
- `sector` (enum, optional)
- `recent_exit_experience` (bool, optional) – IPO/M&A in last X years
- `prior_companies` (string, optional) – semi-colon separated list
- `linkedin_url` (string)
- `relationship_type` (enum, optional) – Guild, Portfolio Exec, Partner 1st-degree, Event
- `source_partner` (string, optional) – which partner/guild list

#### Unstructured: Executive bios and Job descriptions
Bios and job descriptions will come via txt files.

### Output Artifacts

**Search - Config & Trail:**
- Logging of Search
  - All agent steps, messages, reasoning
  - OpenAI Deep research full response and parsing
  - Response citation source links
- Storage of All logs and intermediate parts

**Assessment Results:**
- Assessment results Overview
- Individual assessment results
  - Result Scorecard
  - Result Justification
  - Individual component drill down of some type
- Everything needs to have a markdown copy, since some people will not care about UI

### Airtable Database Design

**Tables:**

- **People Table:** Needs bio field + other normal descriptors
- **Company Table:** Standard company information
- **Portco Table:** Portfolio company specific information
- **Platform - Hiring - Portco Roles:** Where all open roles live
- **Platform - Hiring - Search:** Roles where we are actively assisting with the search
  - Contains Search Custom Info
  - Allows for tracking of work and status
  - Contains spec info that can then be used for Eval
- **Platform - Hiring - Screen:** Batch of screens done
- **Operations - Audit & Logging:** Audit trail for all operations
- **Operations - Workflows:** Standardized set of fields containing execution trail and reporting info that can be linked to other items like Screen
- **Role Spec Table:** Standard role specifications
- **Research Table:** Holds all granular research sprint info (could fold into role eval temporarily)
- **Role Eval Table:** Holds all Assessments (linked to Operation, Role, People)

**Design Notes:**
- Demo: Only upload people (no company/role uploads via Module 1)
- Title Table: NOT in demo - using standard dropdowns instead
- Role Spec Structure: See `demo_planning/role_spec_design.md` for full details
- Specs include custom instructions field for additional guidance
- Generalized search rules may include tenure-based scoring adjustments

### Structured Output Schemas

All LLM interactions use structured outputs via Pydantic models for type safety and consistent parsing.

**📋 Complete schema definitions are in:** `demo_planning/data_design.md` (lines 256-448)

#### Schema Overview

The following Pydantic models are used throughout the system:

**Research Output (from o4-mini-deep-research):**
- `Citation` - Source citation with URL, title, snippet, relevance note
- `CareerEntry` - Timeline entry for career history with achievements
- `ExecutiveResearchResult` - Complete research output including:
  - Career timeline and total years experience
  - Dimension-aligned fields (fundraising, technical leadership, team building, etc.)
  - Sector expertise and stage exposure
  - Research summary, key achievements, notable companies
  - Citations with full source tracking
  - **Audit metadata:** research_timestamp, research_model

**Assessment Output (from gpt-5-mini):**
- `DimensionScore` - Evidence-aware dimension score (1-5 or None for unknown)
  - Includes evidence level (from spec), confidence (LLM assessment)
  - Reasoning, evidence quotes, citation URLs
- `MustHaveCheck` - Must-have requirement evaluation with evidence
- `AssessmentResult` - Complete assessment including:
  - Overall score and confidence
  - Dimension-level scores with evidence
  - Must-haves check, red flags, green flags
  - Summary and counterfactuals
  - **Audit metadata:** assessment_timestamp, assessment_model, role_spec_used

**Workflow Schemas:**
- `ResearchSupplement` - Supplemental search findings from iterative web search (Step 3b)
  - Iteration number, new findings, filled gaps, remaining gaps
  - See `demo_planning/screening_workflow_spec.md` (lines 187-196)
- Quality check output structures (enriched research + is_sufficient flag)
- Merged research structures (original + all supplemental findings)

**Alternative Evaluation (Phase 2+):**
- `ModelGeneratedDimension` - Model-created evaluation dimension
- `AlternativeAssessment` - Alternative evaluation using model-generated rubric
  - **Note:** Out of scope for demo v1

#### Key Design Principles

**Evidence-Aware Scoring:**
- `score: Optional[int]` with range 1-5, where `None` (Python) / `null` (JSON) = Unknown/Insufficient Evidence
- **DO NOT use:** NaN, 0, or empty values - use `None`/`null` exclusively
- Prevents forced guessing when public data is thin
- Explicitly surfaces data gaps for human reviewers
- Example: `{"dimension": "Fundraising Experience", "score": null, "reasoning": "No public data found"}`

**Confidence vs Evidence Level:**
- `evidence_level` (from spec): How observable this dimension typically is from public data
- `confidence` (from LLM): Self-assessed certainty given actual evidence found
- These two signals combine to inform overall confidence calculation

**Audit Metadata (Critical for Compliance):**
- All research outputs include: `research_timestamp`, `research_model`
- All assessment outputs include: `assessment_timestamp`, `assessment_model`, `role_spec_used`
- Enables full audit trail and model tracking

**Overall Score Calculation:**
Computed in Python using an evidence-aware weighting algorithm over dimension scores:

1. Filter to scored dimensions: `scored_dims = [d for d in dimension_scores if d.score is not None]`.
2. If fewer than 2 dimensions are scored, return `overall_score = None` (insufficient information).
3. Take human-designed weights from the role spec for each dimension.
4. Restrict and renormalize weights to the scored dimensions only so they sum to 1.0.
5. Compute a weighted average on the 1–5 scale:
   - `weighted_avg = sum(d.score * w[d.dimension] for d in scored_dims) / sum(w[d.dimension] for d in scored_dims)`.
6. Optionally apply a modest boost to dimensions whose `evidence_level` is High (implementation detail).
7. Convert to 0–100 scale: `overall_score = (weighted_avg - 1) * 25`, then round to 1 decimal place.

**Model Usage (demo v1):**
- Research (Deep Mode): `o4-mini-deep-research` → markdown + citations → `gpt-5-mini` parser → `ExecutiveResearchResult`
- Research (Fast Mode): `gpt-5` + `web_search_preview` → `ExecutiveResearchResult` directly
- Assessment: `gpt-5-mini` → `AssessmentResult` (spec-guided evaluation only)

**📖 See for complete details:**
- **Full Pydantic model definitions:** `demo_planning/data_design.md` (lines 266-387)
- **Usage examples:** `demo_planning/data_design.md` (lines 389-408)
- **Schema design notes:** `demo_planning/data_design.md` (lines 410-448)
- **Evidence-aware scoring patterns and None/null handling**

---

## 4. Core Components

### Person Researcher

**Implementation:**
- **Primary Agent:** Agno Agent with OpenAIResponses(id="o4-mini-deep-research")
  - Comprehensive multi-step executive research
  - Custom instructions for executive evaluation context
  - Returns markdown content with inline citations (no structured JSON)
  - Built-in citation tracking and source extraction
- **Supplemental Tool:** Web search (`{"type": "web_search_preview"}`)
  - Quick fact-checks for missing details
  - Company context lookups
  - Recent news or role changes
- **Parser Agent:** `gpt-5-mini` (or `gpt-5`) with `ExecutiveResearchResult` Pydantic schema
  - Parses Deep Research markdown + citations (or fast web-search results)
  - Produces structured research objects used by assessment and Airtable
- **Flexible Mode:** Can switch to web-search-only agent for faster execution
  - Uses GPT-5 with web search tool instead of Deep Research API
  - Reduces per-candidate time from 2–5 min to 30–60 sec
  - Controlled via environment flag for demo flexibility

**Research Storage:**
- Execution metadata and logs:
  - Stored in `Operations - Workflows` table (status, timestamps, `execution_log`, errors).
- Structured research:
  - Stored in `Research_Results` table using `ExecutiveResearchResult` JSON (`research_json`).
  - Citations stored as JSON array of citation objects (`citations` field).
- Web search queries logged separately for transparency.
- All intermediate steps and reasoning captured in audit trail.

**Workflow Integration:** The `ExecutiveResearchResult` feeds directly into the Step 2 quality gate before any supplemental search decisions are made. See `demo_planning/screening_workflow_spec.md` (Quality Gate section) for end-to-end orchestration.

**Implementation Example (synchronous for demo):**

```python
import os
from agno.agent import Agent
from agno.models.openai import OpenAIResponses

# Environment flag for demo flexibility
USE_DEEP_RESEARCH = os.getenv('USE_DEEP_RESEARCH', 'true').lower() == 'true'

def create_research_agent() -> Agent:
    """Create research agent with flexible execution mode and error handling."""

    if USE_DEEP_RESEARCH:
        # Comprehensive research mode (slower, higher quality)
        return Agent(
            model=OpenAIResponses(id="o4-mini-deep-research", max_tool_calls=1),
            instructions="""
                Research this executive comprehensively using all available sources.
                Focus on: career trajectory, leadership experience, domain expertise,
                company stage/sector experience, notable achievements.
                Return structured results with citations.
            """,
            output_schema=ExecutiveResearchResult,
            exponential_backoff=True,  # Auto-retry on provider errors
            retries=2,
            retry_delay=1,
        )
    else:
        # Fast web search mode (faster, good quality)
        return Agent(
            model=OpenAIResponses(id="gpt-5"),
            tools=[{"type": "web_search_preview"}],
            instructions="""
                Research this executive using web search (3-5 targeted queries).
                Search for: LinkedIn profile, company background, recent news,
                career highlights, domain expertise indicators.
                Synthesize findings into structured output with citations.
            """,
            output_schema=ExecutiveResearchResult,
            exponential_backoff=True,
            retries=2,
            retry_delay=1,
        )

def run_deep_research(candidate):
    """Run research on candidate with full audit trail (synchronous)."""
    from agno.run import RunEvent

    agent = create_research_agent()
    prompt = f"""
    Research executive: {candidate.name}
    Current Role: {candidate.current_title} at {candidate.current_company}
    LinkedIn: {candidate.linkedin_url}
    """

    # Synchronous streaming for audit trail
    response = agent.run(prompt, stream=True, stream_events=True)

    # Capture all events for logging
    events = []
    final_response = None
    for event in response:
        events.append(event)

        # Log tool calls for transparency
        if event.event == RunEvent.tool_call_started:
            print(f"🔧 {event.tool.tool_name}: {event.tool.tool_args}")

        final_response = event

    # Store events in Operations - Workflows table
    store_workflow_events(candidate.id, events)

    return final_response.content  # Returns ExecutiveResearchResult
```

### Assessment Agent

**Configuration:**

```python
assessment_agent = Agent(
    model=OpenAIResponses(id="gpt-5-mini"),
    tools=[{"type": "web_search_preview"}],  # Can search during assessment
    instructions="""
        Evaluate candidate against role spec using provided research.

        Use web search ONLY if you need to:
        - Verify specific claims about companies/roles
        - Look up industry context (e.g., typical metrics for stage/sector)
        - Validate assumptions critical to assessment

        Minimize searches - rely primarily on research results provided.
        Be explicit when evidence is insufficient - return score = null (None) for Unknown.
    """,
    output_schema=AssessmentResult,  # Pydantic model for structured output
    exponential_backoff=True,  # Auto-retry on provider errors
    retries=2,
    retry_delay=1,
)
```

**Benefits:**
- Assessment agent can validate critical assumptions independently
- Reduces "low confidence" scores by allowing context lookups
- Demonstrates agentic autonomy (agent decides when additional search is needed)
- All searches logged for transparency and reasoning trail

### Agno Implementation Patterns

**Agent Instantiation:**
- Agents created per-request (safe pattern for demo)
- Can also be module-level for performance optimization
- State managed through session and database, not agent objects
- Pattern: Create agents inside request handlers or workflow functions

**Event Streaming & Audit Trails:**
- Use `stream=True, stream_events=True` for full observability
- Synchronous iteration with regular `for` loop (demo implementation)
- Captured events: `run_started`, `run_completed`, `tool_call_started`, `tool_call_completed`, `run_content`
- Store all events in Operations - Workflows table for complete audit trail

**Streaming + Structured Outputs:**
- Structured outputs work seamlessly with streaming
- Final event in stream contains the Pydantic model instance
- Pattern:
  ```python
  response = agent.run(prompt, stream=True, stream_events=True)
  events = []
  final_response = None
  for event in response:
      events.append(event)
      final_response = event

  result: ExecutiveResearchResult = final_response.content
  ```

**Error Handling:**
- Built-in retry with `exponential_backoff=True`
- Configure retries with `retries=2, retry_delay=1`
- Automatic handling of provider errors (rate limits, timeouts)
- Custom error handling via `RetryAgentRun` and `StopAgentRun` exceptions (if needed)
- If a research or assessment step fails after retries:
  - Mark the corresponding Workflow record as `Failed`
  - Populate `error_message` with a concise error summary
  - Do not crash the entire Flask process; return a 200/OK with `"status": "failed"` so Airtable reflects the failure state.

**Implementation Notes:**
- All agents configured with basic retry/error handling suitable for the demo.
- Event streaming provides full transparency for demo and debugging.
- Synchronous execution keeps implementation simple for the 48-hour constraint.
- Async optimization deferred to post-demo phase.

### Matching & Ranking Logic (Evidence-Aware)

**Pre-filtering (Deterministic):**
- Filter candidates by:
  - Role type (CTO vs CFO)
  - Basic stage/sector alignment with the role (exact or "stretch" match)
  - Optional geography if required by the role
- Goal: keep LLM work focused on plausible candidates.

**Dimension-Level Scoring:**
- For each candidate-role pair, the assessment LLM call returns:
  - Dimension scores on a 1–5 scale with `None` for Unknown:
    - `5–1` = strength based on observable evidence
    - `None` (Python) / `null` (JSON) = Unknown / Insufficient public evidence
    - **DO NOT use:** NaN, 0, or empty values - use `None`/`null` exclusively
  - Evidence Level (High/Medium/Low) copied from the spec
  - Confidence (High/Medium/Low)
  - Evidence-based reasoning + quotes + citations
- The LLM is explicitly instructed:
  - Not to guess when evidence is missing.
  - To return `null` and a short "insufficient evidence" explanation when it cannot support a score.

**Overall Score Calculation:**
- Per-candidate overall score is computed in Python (not by the LLM):
  - Start from human-designed dimension weights from the spec.
  - For each dimension:
    - Ignore or heavily down-weight dimensions with `score = None` (Unknown).
    - Optionally apply a modest boost to **High** evidence dimensions to reflect data quality.
  - Compute a weighted average over non-None dimensions only.
  - Scale to 0–100 for Airtable display (`overall_score`).
- Overall confidence combines:
  - LLM's self-reported confidence across dimensions.
  - The proportion of dimensions with non-None scores (more None values → lower overall confidence).

**Implementation Note:**

```python
def calculate_overall_score(dimension_scores, spec_weights) -> Optional[float]:
    # Filter scored dimensions
    scored = [d for d in dimension_scores if d.score is not None]
    if len(scored) < 2:
        return None

    # Restrict and renormalize weights to scored dimensions
    raw_weights = {d.dimension: spec_weights[d.dimension] for d in scored}
    total = sum(raw_weights.values())
    norm_weights = {dim: w / total for dim, w in raw_weights.items()}

    # Weighted average on 1–5 scale
    weighted_avg = sum(d.score * norm_weights[d.dimension] for d in scored)

    # Scale to 0–100
    return round((weighted_avg - 1) * 25, 1)
```

**Ranking:**
- Candidates are ranked for a given role by:
  1. `overall_score` (descending)
  2. `overall_confidence` (High > Medium > Low)
  3. Relationship heuristic (e.g., Guild > Portfolio Exec > Partner 1st-degree > Event)
- Candidates below a configurable minimum score threshold are explicitly labeled as "Not Recommended" (rather than hidden).

**Single Evaluation (Spec-Guided for Demo v1):**
- **Primary (and only) evaluation:** Spec-guided, evidence-aware scoring as described above. This is the main ranking shown in Airtable.
- Model-generated rubric / alternative evaluation is a **future experiment**, not implemented for the initial demo.

#### Research Merging (Step 3c)

When supplemental search runs, its outputs are merged back into the original `ExecutiveResearchResult` before assessment so downstream scoring sees a single, enriched object.

- **Experiences & Expertise:** Append `new_findings` that map to key experiences, domain expertise, or leadership evidence.
- **Citations:** Combine all primary + supplemental citations for transparent sourcing.
- **Gaps:** Remove any gaps covered in `filled_gaps`; carry forward only unresolved items from `remaining_gaps`.
- **Confidence:** Upgrade research confidence to "High" once supplemental search finishes (either by meeting the break condition or exhausting 3 iterations).

This merged artifact is the only research object passed into the assessment agent, ensuring the scoring step always consumes the most complete view available. Detailed merge pseudo-code lives in `demo_planning/screening_workflow_spec.md` (Step 3c).

#### Evidence Quote Extraction

Dimension-level reasoning can optionally include short evidence quotes drawn from the research text:

- **Input:** Full `ExecutiveResearchResult` (including `research_summary`, `career_timeline`, and citations) plus the dimension name.
- **Process:** Call a lightweight `gpt-5-mini` helper with a structured output schema like:
  - `QuoteExtractionResult = { quotes: list[str] }`
- **Prompt:** "Extract 1–3 short quotes (1–2 sentences each) from the research that most directly support the score for `<dimension>`."
- **Output:** A small list of concrete excerpts stored in `DimensionScore.evidence_quotes` (may be empty if nothing is clearly supportive).

This helper is optional for the demo; it can be added as a follow-up enhancement if time permits.

### Person Enrichment

**Implementation:** Stub function that looks up mock Apollo data (fake for demo)

### Portco Components

**Standardized storage of portco information:**
- Basic Portco Info Define subset
- Review Startup Taxonomy
- Includes stage

**Demo:**
- Cut-through portco table pre-enriched
- Maybe add startup taxonomy
- Maybe do research
- Need to select subset

### Role Spec Components

**Full specification defined in:** `demo_planning/role_spec_design.md`

**Summary:**
- Markdown-based role evaluation frameworks
- Template library (CFO, CTO base templates)
- 4–6 weighted dimensions per spec, each with:
  - **Weight** (for human-designed importance)
  - **Evidence Level** (High/Medium/Low – how reliably this can be assessed from public/web data)
  - **Observable, evidence-based scale** (5–1) plus `None/null = Unknown / Not enough public evidence`
- CFO and CTO templates include:
  - High-evidence dimensions (e.g., fundraising track record, sector/domain expertise, stage exposure)
  - Medium-/low-evidence dimensions (e.g., culture, product partnership) that are primarily for qualitative commentary
- Must-haves, nice-to-haves, red flags
- Customization via duplication and editing
- Python parser module for LLM consumption
- Structured output schema for assessments that respects evidence levels

### Candidate Profiles

**OUT OF SCOPE FOR DEMO**
- Standardized Candidate Profile Definition: Components, definitions, requirements, standards for a spec
- Goal is to have standard way we describe a candidate generally, and then how we translate and populate for a given spec

---

## 5. Demo Modules

### Module 1: Data Uploading

**Pattern:** Airtable Button → Webhook → Flask `/upload` endpoint

**Flow (via Airtable Interface UI):**
- Upload file via Airtable attachment field
- Select File type dropdown (person, company)
  - No role uploads for demo
- Click "Process Upload" button
  - Can either be webflow trigger button if UI allows, or can be an action that changes a field value to trigger webhook
- **Webhook triggers Flask `/upload` endpoint**
  - Python: Download file from Airtable
  - Python: Clean, normalize, dedupe
  - Python: Load into proper table
  - Python: Update status field with results

**Demo:**
- Add new people CSV
  - Could add bios in text field too

**Implementation:**

```python
@app.route('/upload', methods=['POST'])
def process_upload():
    # Get file from Airtable
    # Clean and normalize
    # Deduplicate rows (see deduplication strategy below)
    # Load to appropriate table
    # Return status
```

**Deduplication Strategy (Demo-Scoped):**
- Primary key for people imported via CSV:
  - Use a normalized combination of `full_name` + `current_company` (case-insensitive) as a soft key.
- Before inserting a new person:
  - Search the People table for an existing record with the same normalized name + company.
  - If found, skip insert and attach any additional CSV metadata as an update rather than a new row.
- This keeps the demo data clean without heavy-weight fuzzy matching.

### Module 2: New Open Role

**ALL IN AIRTABLE (no Python)**

**Definitions and Notes:**
- Open roles exist for many portcos. Not all of them we will be actively assisting with
- Portcos can provide us open roles that we provide in careers portal externally
- Note: Can have portcos submit + Aging mechanism

**Flow (via Airtable Interface UI):**
- Select Portco
- Select Role type
- Optional notes for candidate parameters
- Optional add spec
  - Select Existing
    - Ability to add bespoke requirements
  - Create Own
  - Maybe create new version of existing

**Demo:**
- Create new Role live

### Module 3: New Search

**ALL IN AIRTABLE (no Python)**

**Definitions and Notes:**
- Search is a role we are actively assisting with. Will have role spec
- Have as distinct item so we can attach other items to it (like notes)

**Flow (via Airtable Interface UI):**
- Link Role
- Link spec?
- Add notes
- Add timeline date

**Demo:**
- Create new search live

### Module 4: New Screen

**Pattern:** Airtable Button → Webhook → Flask `/screen` endpoint

**Definition:**
- Perform screening on a set of people for a search
- Main demo workflow for talent matching

**Requirements:**
- Process one or more candidates at a time
- Bulk selection via linked records
- Multiple screens per search allowed
- Can redo evals with new guidance

**Flow (via Airtable Interface UI):**
- Create new Screen record in Airtable
- Link to Search (which links to Role + Spec)
- Add custom guidance/specifications (optional)
- Link one or more candidates from People table
  - Use Airtable multi-select
- Click "Start Screening" button
  - Can either be webflow trigger button if UI allows, or can be an action that changes a field value to trigger webhook
- **Webhook triggers Flask `/screen` endpoint**
  - For each linked candidate:
    - Create Workflow record (audit trail)
    - Run Deep Research via OpenAI API
    - Store research results in Workflow record
    - Run Assessment against role spec
    - Store assessment in Workflow record
      - Overall score + confidence
      - Dimension-level scores
      - Reasoning + counterfactuals
    - Update candidate status
    - Mark Workflow as complete
  - Update Screen status to "Complete"
  - Terminal shows real-time progress

**Implementation (synchronous for demo):**

```python
@app.route('/screen', methods=['POST'])
def run_screening():
    """Synchronous screening with full event capture for audit trail."""
    screen_id = request.json['screen_id']

    # Get screen details + linked candidates
    screen = get_screen(screen_id)
    candidates = get_linked_candidates(screen)

    # Process candidates sequentially (simple, reliable for demo)
    results = []
    for candidate in candidates:
        print(f"📋 Processing: {candidate.name}")

        # Create workflow record for audit trail
        workflow = create_workflow_record(screen_id, candidate.id)

        # Research with event capture (returns ExecutiveResearchResult + events)
        research = run_deep_research(candidate)

        # Assessment with event capture
        assessment = run_assessment(candidate, research, screen.role_spec)

        # Write results to Airtable
        write_results_to_airtable(workflow, research, assessment)

        results.append(assessment)
        print(f"✅ Completed: {candidate.name}")

    # Update screen status
    update_screen_status(screen_id, 'Complete')

    return {'status': 'success', 'candidates_processed': len(results)}
```

**Demo:**
- Demo UI and kick off flow
- Use pre-run example for discussion and can check in periodically to see the live run is progressing

---

## 6. Demo Configuration

### Candidates
- **Source:** `reference/guildmember_scrape.csv` (64 executives from FirstMark guilds)
- **Roles:** Mix of CFOs, CTOs, CPOs, CROs across various companies
- **Demo Scope:** Execute evaluations for 10-15 candidates
- **Enrichment:** Basic profiles + LinkedIn URLs (mock research data for demo)

### Portco + Role Scenarios

**4 total scenarios:**

1. **Pigment - CFO Role** (B2B SaaS, enterprise, international)
   - Status: Pre-run ✅

2. **Mockingbird - CFO Role** (Consumer DTC, physical product)
   - Status: Pre-run ✅

3. **Synthesia - CTO Role** (AI/ML SaaS, global scale)
   - Status: Pre-run ✅

4. **Estuary - CTO Role** (Data infrastructure, developer tools)
   - Status: **LIVE EXECUTION** during demo 🔴

**Demo Strategy:**
- Show pre-run results for 3 scenarios (full data, insights, rankings ready)
- Kick off live screening for 1 scenario to demonstrate real-time workflow
- Toggle between completed results and in-progress execution
- Highlight different assessment patterns across CFO vs CTO roles

---

## 7. Implementation Planning

### Technical Implementation Notes

**Core Requirements:**
- Must have confidence alongside any evaluation score
- Rubrics are dimensions, weights, definition, and scale
- Need quotation level detail somewhere
- Counterfactuals
- All ins and outs will use structured outputs (Pydantic models)
- Demo db schemas will be MVP, not beautiful thing
- Will do a single evaluation path for the demo (LLM guided via spec and rubric)
- Data schema: People will always have LinkedIn associated with them

**Airtable Requirements:**
- DB & UI features quickly
- Meet them in their stack
- Requirements:
  - Ability to kickoff workflow from Airtable
  - Ability to use Python for Data ops and Agent work

### Outstanding Decisions Needed

#### 1. Assessment Scoring Mechanics

**Confidence Calculation:** How is confidence (High/Medium/Low) determined?
- Based on amount of evidence found?
- Based on directness of evidence match?
- LLM self-assessment of certainty?
- Combination approach?
- **Recommendation:** Use LLM self-assessment + evidence quantity (simple heuristic)
- **Status:** APPROVED ✅

**Counterfactuals Definition:** What does "counterfactuals" mean in this context?
- "What if" scenarios? (e.g., "If candidate had X experience, score would be Y")
- Alternative interpretations of ambiguous evidence?
- Reasons candidate might NOT be a good fit despite high score?
- **Recommendation:** "Key reasons candidate might NOT be ideal fit despite high score + Assumptions or evaluation results that are most important/must be true"
- **Status:** APPROVED ✅

**Two Evaluation Comparison:** How do we present both evaluation results?
- Side-by-side comparison in UI?
- Separate sections in markdown report?
- Highlight where they agree vs disagree?
- Use spec-based as primary, AI-generated as validation?
- **Note:** Only relevant if we later add model-generated rubric path (not in demo v1)

#### 2. Airtable Schema Details

Need complete field definitions for these tables:

**People Table:**
- Standard fields: name, current_title, current_company, location, linkedin_url
- Bio field: Long Text? Rich Text?
- Which fields from guildmember_scrape.csv map to People table?

**Platform - Hiring - Screen:**
- Fields: screen_id, search_link, candidates_links, status, created_date
- Status enum values: Draft, Ready to Screen, Processing, Complete, Failed?
- Custom instructions field?

**Operations - Workflows:**
- Fields needed for audit trail?
- Research results storage structure?
- Assessment results storage structure?
- Execution logs format?

**Role Eval Table:**
- How are dimension scores stored? Individual fields vs JSON?
- Evidence quotes storage?
- Citation links storage?

**Research Table:**
- Full research text field?
- Citation structure: URLs only or full content snapshots?
- OpenAI Deep Research API response format?

#### 3. Data Ingestion & Processing

**File Upload Deduplication:**
- Do we implement dedupe logic for demo? (checking exec_id or name+company?)
- **Recommendation:** Skip for demo - assume clean uploads only
- **Status:** RESOLVED ✅ - Skipping dedupe for demo

**OpenAI Deep Research API Integration:**
- Expected response format and structure?
- How are citations returned in the API response?
- Rate limits and cost implications?
- **Need to review:** `reference/docs_and_examples/openai_reference/deep_research_api/OAI_deepresearchapi.md`

**Citation Storage:**
- Store URLs only (from Deep Research API response)?
- Or also store citation snippets/quotes provided by API?
- **Recommendation:** URLs + key quotes provided in API response (no additional scraping)

#### 4. Technical Robustness

**Error Handling:**
- Rate limiting strategy for OpenAI API calls?
- Retry logic for failed research/assessment calls?
- Fallback behavior if API fails during demo?

**Execution Time:**
- **Deep Research Mode (Primary):**
  - Research phase: 2-5 minutes per candidate (o4-mini-deep-research)
  - Assessment phase: 30-60 seconds per candidate (gpt-5-mini)
  - Total per candidate (sequential demo implementation): ~3-6 minutes
  - Running 10 candidates sequentially would take ~30-60 minutes, so the demo relies on pre-run scenarios rather than full 10-candidate live runs.
- **Web Search Mode (Fallback/Fast):**
  - Research phase: 30-60 seconds per candidate (gpt-5 + web search, agent makes 3-5 queries)
  - Assessment phase: 30-60 seconds per candidate (+ occasional search)
  - Total per candidate (sequential demo implementation): ~1-2 minutes
  - Suitable for shorter live runs (e.g., 3-5 candidates) if time-constrained.
- **Demo Strategy:** Use Deep Research for 3 pre-run scenarios; use Web Search mode or a smaller candidate set for the live demo if time-constrained

**Structured Outputs:**
- All API calls use structured outputs (confirmed)
- Schema validation: strict or permissive?
- Handling of schema mismatches?

#### 5. Demo Logistics

**Airtable Setup Scope:**
- Which Interface views are needed for demo?
- Are automations essential or can we trigger webhooks manually?
- Pre-populated test data requirements?

**Webhook Testing:**
- Can we test webhook locally before demo?
- Ngrok stability concerns for live demo?
- Backup plan if webhook fails?

**Output Artifacts:**
- Markdown export of all assessment results (confirmed requirement)
- Where are markdown files stored? (Airtable attachment? Local folder?)
- Format template for markdown reports?

#### 6. MVP Simplifications (Given 48-Hour Constraint)

**Resolved Simplifications:**
- Person enrichment: **Stub function** (no real Apollo API) ✅
- Research: **Real OpenAI Deep Research API** (not mock data) ✅
- Candidate profiles: **Skip entirely** ✅
- Deduplication: **Skip** (assume clean data) ✅

**Still Need to Decide:**
- Module 1 (Upload): Build full CSV processing webhook or pre-populate data manually?
- Module 2 (New Role): Airtable-only UI flow (no Python) vs fully manual record creation?
- Module 3 (New Search): Airtable-only UI flow (no Python) vs fully manual record creation?
- Airtable Interface: Custom interfaces or standard grid views?
- **Recommendation:** Pre-populate data for Modules 1-3 and/or use Airtable-only flows; focus dev time on Module 4 (screening)

### Prioritization Recommendation

**Must Have Before Build:**
1. ✅ Research execution strategy → **RESOLVED:** OpenAI Deep Research API + Web Search (hybrid approach, no Tavily)
2. ✅ Expected execution times → **RESOLVED:** 3-6 min/candidate (Deep Research) or 1-2 min/candidate (Web Search)
3. ✅ Model selection → **RESOLVED:** o4-mini-deep-research (research), gpt-5-mini (assessment)
4. ✅ Structured outputs → **RESOLVED:** Pydantic schemas defined
5. **Confidence calculation methodology** → Define H/M/L logic (Status: APPROVED ✅)
6. **Counterfactuals operational definition** → What does this mean in practice? (Status: APPROVED ✅)
7. **Airtable schema details** → Complete field definitions for core tables

**Can Decide During Build:**
1. ✅ Deduplication approach → **RESOLVED:** Skip for demo
2. Citation storage details (review Deep Research API docs for format)
3. Error handling specifics (retry logic, fallbacks)
4. Two evaluation comparison presentation (future only; relevant if we later add model-generated rubric path)
5. Markdown export format (can use simple template)

**Recommended Simplifications for Demo:**
1. **Modules 1-3:** Pre-populate data manually (no webhook automation needed)
2. **Module 4:** Build full webhook + automation (this is the core demo)
3. **Airtable UI:** Standard grid views + basic filtering (no custom interfaces)
4. **3 portcos pre-run, 1 live** → Manage execution time risk

### Next Steps

**Immediate Decisions Needed (Before Build):**

1. **Define confidence calculation logic** (30 min)
   - Propose simple heuristic: LLM self-assessment + evidence count threshold
   - Document in assessment schema
   - Status: APPROVED ✅

2. **Define counterfactuals** (30 min)
   - Operational definition for demo
   - Recommendation: "Key reasons candidate might NOT be ideal fit despite high score + Assumptions or evaluation results that are most important/must be true"
   - Status: APPROVED ✅

3. **Review OpenAI Deep Research API docs** (1 hour)
   - Understand response format, citation structure, rate limits
   - File: `reference/docs_and_examples/openai_reference/deep_research_api/OAI_deepresearchapi.md`
   - Determine expected execution time per candidate

4. **Create detailed Airtable schema** (2 hours)
   - Complete field definitions for: People, Screen, Workflows, Role Eval tables
   - Create new document: `demo_planning/airtable_schema.md`

**Implementation Sequence:**

1. **Phase 1:** Airtable setup + manual data population (4 hours)
2. **Phase 2:** Core assessment logic + prompts + Pydantic models (6 hours)
   - Implement ExecutiveResearchResult and AssessmentResult schemas
   - Create research agent (Deep Research + Web Search modes)
   - Create assessment agent with web search capability
   - Implement flexible mode switching via environment flag
3. **Phase 3:** Flask webhook + Module 4 integration (synchronous) (4 hours)
   - Simple synchronous endpoint implementation
   - Sequential candidate processing
   - Real-time status updates via status fields and console logs
4. **Phase 4:** Pre-run 3 scenarios + generate results (4 hours)
   - Use Deep Research mode for comprehensive results
   - Generate markdown exports
5. **Phase 5:** Testing + demo rehearsal (2 hours)
   - Test Deep Research and (optionally) Web Search modes
   - Verify synchronous execution and timing
   - Practice demo flow

**Total Estimated: 20 hours** (leaves buffer within 48-hour window)

**Implementation Notes:**
- Implement both Deep Research and Web Search modes with environment flag toggle
- This provides demo flexibility: comprehensive results (Deep Research) or faster live execution (Web Search)
- Keep implementation synchronous for the initial demo; add async/concurrency later only if needed
