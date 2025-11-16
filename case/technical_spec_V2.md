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
  - Structured output support via Pydantic schemas
  - ~2-5 minutes per candidate
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

**Complete schema definitions are in:** `demo_planning/data_design.md` (lines 256-427)

#### ExecutiveResearchResult (Deep Research Output)

```python
from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime

class Citation(BaseModel):
    url: str
    quote: str
    relevance: str = Field(description="Why this source is relevant")

class CareerEntry(BaseModel):
    company: str
    title: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    achievements: list[str]

class ExecutiveResearchResult(BaseModel):
    """Structured output from o4-mini-deep-research."""
    exec_name: str
    current_role: str
    current_company: str
    career_timeline: list[CareerEntry]

    # Dimension-aligned fields
    fundraising_experience: Optional[str] = None  # CFO
    operational_finance_experience: Optional[str] = None  # CFO
    technical_leadership_experience: Optional[str] = None  # CTO
    team_building_experience: Optional[str] = None
    sector_expertise: list[str]
    stage_exposure: list[str]

    research_summary: str
    key_achievements: list[str]
    citations: list[Citation]
    research_confidence: str = Field(description="High/Medium/Low based on evidence quality")
    gaps: list[str] = Field(description="Information not found or unclear")
```

#### AssessmentResult (Evaluation Output)

```python
class DimensionScore(BaseModel):
    """Evidence-aware dimension score."""
    dimension: str
    score: Optional[int] = Field(None, ge=1, le=5)  # None = Unknown
    evidence_level: Literal["High", "Medium", "Low"]  # From spec
    confidence: Literal["High", "Medium", "Low"]  # LLM assessment
    reasoning: str
    evidence_quotes: list[str]
    citation_urls: list[str]

class MustHaveCheck(BaseModel):
    requirement: str
    met: bool
    evidence: str

class AssessmentResult(BaseModel):
    """Structured assessment from gpt-5-mini."""
    overall_score: Optional[float] = Field(None, ge=0, le=100)
    overall_confidence: Literal["High", "Medium", "Low"]
    dimension_scores: list[DimensionScore]
    must_haves_check: list[MustHaveCheck]
    red_flags_detected: list[str]
    green_flags: list[str]
    summary: str
    counterfactuals: list[str]
```

#### Schema Design Principles

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

**Overall Score Calculation:**
- Computed in Python using evidence-aware weighting (see Matching & Ranking Logic section)
- Dimensions with `score = None` are ignored or down-weighted
- Optional boost for High evidence level dimensions
- Result scaled to 0-100 for Airtable display

**Model Usage (demo v1):**
- Research: `o4-mini-deep-research` → `ExecutiveResearchResult`
- Assessment: `gpt-5-mini` → `AssessmentResult` (spec-guided evaluation only)
  - Model-generated rubric / `AlternativeAssessment` is explicitly out of scope for the initial demo

**See full schema definitions with usage examples in:** `demo_planning/data_design.md`

---

## 4. Core Components

### Person Researcher

**Implementation:**
- **Primary Agent:** Agno Agent with OpenAIResponses(id="o4-mini-deep-research")
  - Comprehensive multi-step executive research
  - Custom instructions for executive evaluation context
  - Structured output using ExecutiveResearchResult Pydantic schema
  - Built-in citation tracking and source extraction
- **Supplemental Tool:** Web search (`{"type": "web_search_preview"}`)
  - Quick fact-checks for missing details
  - Company context lookups
  - Recent news or role changes
- **Flexible Mode:** Can switch to web-search-only agent for faster execution
  - Uses GPT-5 with web search tool instead of Deep Research API
  - Reduces per-candidate time from 2-5 min to 30-60 sec
  - Controlled via environment flag for demo flexibility

**Research Storage:**
- Research Run log in Operations - Workflows table
- Structured research results using Pydantic schema
- Citations automatically included from Deep Research API response (URLs + quotes)
- Web search queries logged separately for transparency
- All intermediate steps and reasoning captured in audit trail

**Implementation Example (synchronous for demo):**

```python
import os
from agno.agent import Agent
from agno.models.openai import OpenAIResponses

# Environment flag for demo flexibility
USE_DEEP_RESEARCH = os.getenv('USE_DEEP_RESEARCH', 'true').lower() == 'true'

def create_research_agent() -> Agent:
    """Create research agent with flexible execution mode."""

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
        )

def run_deep_research(candidate):
    """Run research on candidate using configured mode."""
    agent = create_research_agent()
    prompt = f"""
    Research executive: {candidate.name}
    Current Role: {candidate.current_title} at {candidate.current_company}
    LinkedIn: {candidate.linkedin_url}
    """
    result = agent.run(prompt)
    return result.content  # Returns ExecutiveResearchResult
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
        Be explicit when evidence is insufficient - use score 0 for Unknown.
    """,
    output_schema=AssessmentResult,  # Pydantic model for structured output
)
```

**Benefits:**
- Assessment agent can validate critical assumptions independently
- Reduces "low confidence" scores by allowing context lookups
- Demonstrates agentic autonomy (agent decides when additional search is needed)
- All searches logged for transparency and reasoning trail

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
# Filter scored dimensions
scored_dims = [d for d in dimension_scores if d.score is not None]

# Calculate weighted average (only non-None scores)
if scored_dims:
    weighted_sum = sum(d.score * weights[d.dimension] for d in scored_dims)
    total_weight = sum(weights[d.dimension] for d in scored_dims)
    overall_score = (weighted_sum / total_weight) * 20  # Scale to 0-100
else:
    overall_score = None  # No scoreable dimensions
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
  - **Observable, evidence-based scale** (5–1) plus `0 = Unknown / Not enough public evidence`
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
    # Load to appropriate table
    # Return status
```

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
    screen_id = request.json['screen_id']

    # Get screen details + linked candidates
    screen = get_screen(screen_id)
    candidates = get_linked_candidates(screen)

    # Process candidates sequentially (simple, reliable for demo)
    results = []
    for candidate in candidates:
        workflow = create_workflow_record(screen_id, candidate.id)
        research = run_deep_research(candidate)
        assessment = run_assessment(candidate, research, screen.role_spec)
        write_results_to_airtable(workflow, research, assessment)
        results.append(assessment)

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
