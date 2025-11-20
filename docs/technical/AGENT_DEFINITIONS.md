# AGENT DEFINITIONS - Talent Signal Agent

**Version:** 1.0
**Last Updated:** 2025-01-18
**System:** FirstMark Talent Signal Agent (Agno Framework)

---

## Overview

The Talent Signal Agent implements a **4-agent linear workflow** with quality-gated architecture for AI-powered executive matching. The system performs OSINT research, structured data extraction, conditional supplemental research, and evidence-aware assessment against role specifications.

### Execution Flow

```
┌──────────────────────┐
│  1. Deep Research    │  o4-mini-deep-research (2-6 min)
│  OSINT Profiling     │  → Markdown + citations
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│  2. Research Parser  │  gpt-5-mini (10-30 sec)
│  Structure Data      │  → ExecutiveResearchResult
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│  3. Quality Gate     │  Python function (<1 sec)
│  Check Citations     │  → Pass: Skip to Step 4
│                      │  → Fail: Run Incremental Search
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│  3a. Incremental     │  gpt-5 (1-2 min, conditional)
│  Supplemental Search │  → Merged ExecutiveResearchResult
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│  4. Assessment       │  gpt-5-mini (30-60 sec)
│  Evidence Scoring    │  → AssessmentResult (1-5 scale)
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│  5. Score Calc       │  Python function (<5 sec)
│  1-5 → 0-100 scale   │  → Final assessment + Airtable write
└──────────────────────┘
```

**Total Time per Candidate:** ~3-8 minutes (Deep Research dominates at 2-6 min)

---

## Agent 1: Deep Research Agent

### Role
Performs comprehensive OSINT profiling of executive candidates to gather verifiable career history, achievements, and professional context from public sources.

### Objectives
- Locate and synthesize information from LinkedIn, company websites, news articles, funding databases, podcasts, and conference talks
- Extract verifiable facts (roles, dates, companies, deals) with citations
- Identify patterns and observations about leadership style, decision-making, and team-building
- Surface gaps and low-confidence areas explicitly
- Provide structured markdown output with evidence taxonomy

### Methods

**LLM Model:** `o4-mini-deep-research` (OpenAI Deep Research API)

**Configuration:**
```python
model="o4-mini-deep-research"
max_tool_calls=1                     # Single research pass
timeout=600                          # 10-minute timeout
add_datetime_to_context=True         # Temporal awareness
exponential_backoff=True
retries=2
delay_between_retries=1
```

**Key Constraints:**
- NO `output_schema` parameter (API returns markdown only, not structured JSON)
- Built-in web search and citation extraction (no separate tools needed)
- Returns raw markdown + citations array (parsed by Agent 2)

**Input:**
```python
candidate_name: str                  # "Jane Smith"
current_title: str                   # "CFO"
current_company: str                 # "Acme Corp"
linkedin_url: Optional[str]          # "https://linkedin.com/in/janesmith"
```

**Output:**
```python
research_markdown: str               # Raw markdown (5 sections)
citations: List[dict]                # Extracted by API [{url, title, snippet}]
```

**Prompt Source:** `demo/prompts/catalog.yaml` (key: `deep_research`)

**Prompt Features (Enhanced v1.0, January 2025):**
- **Evidence Taxonomy:**
  - `[FACT]` – Verifiable roles, dates, companies, deals, quotes with citations (high/medium/low)
  - `[OBSERVATION]` – Patterns inferred from multiple facts (leadership style, decision-making, communication)
  - `[HYPOTHESIS]` – Supported but unconfirmed inferences; always low confidence and explicitly caveated
- **Output Structure (5 Parts):**
  1. **Candidate Information** – Basic info, career timeline, expertise, achievements (with citations + confidence)
  2. **Candidate Insights & Observations** – Strengths, patterns, values, behavioral observations
  3. **Relevant Role Information** – Information specifically tied to the role being screened
  4. **Research Process & Findings** – Narrative summary, citation list with reliability notes, overall research confidence
  5. **Research Confidence & Limitations** – Confidence rationale and explicit limitations/gaps to probe in follow-up
- **Source Reliability Hierarchy (5-point scale):**
  - **Reliability 5:** First-party sources (official bios, LinkedIn, company websites, press releases)
  - **Reliability 4:** Major reputable sources (WSJ, NYT, TechCrunch, Forbes, Bloomberg)
  - **Reliability 3:** Trade press (industry publications, conference proceedings, podcast transcripts)
  - **Reliability 2:** Aggregators (Crunchbase, PitchBook, news aggregators)
  - **Reliability 1:** Unknown/Low-reliability (social media, forums, unverified blogs)
- **Query Seed Templates (17 concrete patterns):**
  - Identity & Basic Info (4 templates): LinkedIn, company bios, resume searches
  - Expertise & Thought Leadership (4 templates): Speaking, publications, podcasts, conferences
  - Career & Achievements (3 templates): Funding rounds, acquisitions, awards
  - Communication Patterns (3 templates): Transcripts, videos, social media
  - Network & Context (3 templates): Panels, team references, topic-specific
  - *See `docs/prompt_system_summary.md` for complete template list*
- **Sparse-Data Handling Policy:**
  - Expand source types: local news, university pages, GitHub, Google Scholar, Archive.org, niche podcasts
  - Use name variants and multilingual search for international candidates
  - Document "Limited Public Presence" explicitly and downgrade confidence when evidence remains thin
  - Apply specific strategies when <3 citations or <500 words of content

**Enhancement Details:** See `docs/prompt_system_summary.md` for full prompt enhancement features

**Execution Time:** 2-6 minutes (depends on candidate profile depth)

**Implementation Reference:**
- **Factory:** `demo/agents.py:40-89` (`create_research_agent()`)
- **Invocation:** `demo/screening_service.py:153-165`
- **Prompt:** `demo/prompts/catalog.yaml:6-96`

---

## Agent 2: Research Parser Agent

### Role
Converts unstructured markdown research into a structured `ExecutiveResearchResult` schema suitable for programmatic processing and assessment.

### Objectives
- Parse Deep Research markdown into typed Pydantic model
- Extract career timeline entries (role, company, dates, scope)
- Categorize sector expertise and stage exposure
- Preserve narrative summary and raw markdown
- Map citations to structured format
- Surface research gaps and confidence levels
- Respect evidence taxonomy ([FACT] → structured fields, [OBSERVATION] → narrative)

### Methods

**LLM Model:** `gpt-5-mini`

**Configuration:**
```python
model="gpt-5-mini"
output_schema=ExecutiveResearchResult  # Structured output enabled
num_history_runs=3                     # Context from recent runs
exponential_backoff=True
retries=2
delay_between_retries=1
```

**Input:**
```python
research_markdown: str                # Output from Agent 1
candidate_name: str
current_title: str
current_company: str
citations: List[dict]                 # From Agent 1 API
```

**Output:** `ExecutiveResearchResult` (Pydantic model)
```python
exec_name: str
current_role: str
current_company: str
career_timeline: List[CareerEntry]    # [{role, company, start_year, end_year, scope}]
total_years_experience: Optional[int]
fundraising_experience: Optional[str] # Role-specific dimension
operational_finance_experience: Optional[str]
technical_leadership_experience: Optional[str]
team_building_experience: Optional[str]
sector_expertise: List[str]           # ["fintech", "b2b saas"]
stage_exposure: List[str]             # ["series-a", "growth"]
research_summary: str                 # 3-5 paragraph narrative
research_markdown_raw: str            # Preserved original
key_achievements: List[str]           # Bulleted highlights
notable_companies: List[str]          # Name recognition
citations: List[Citation]             # [{url, title, snippet, accessed_date}]
research_confidence: Literal["High", "Medium", "Low"]
gaps: List[str]                       # Explicit missing information
research_timestamp: datetime
research_model: str                   # "o4-mini-deep-research"
```

**Prompt Source:** `demo/prompts/catalog.yaml` (key: `research_parser`)

**Prompt Features (Enhanced v1.0, January 2025):**
- **Evidence Classification Handling:**
  - Treats `[FACT]` statements as primary evidence for structured fields
  - Uses `[OBSERVATION]` to enrich narrative fields (not hard facts)
  - Treats `[HYPOTHESIS]` as speculative (adds to gaps, not structured fields)
- **Malformed Markdown Handling:**
  - Robust extraction from both well-structured and partial markdown
  - Citation URL fallback for missing structured fields
  - Context-based inference for missing data (current role, sector expertise, stage exposure)
  - Explicit gap documentation when fields cannot be extracted
- **Citation Extraction (4 source types):**
  - Structured citation lists, inline citations, citation dicts, URL patterns
  - Creates Citation objects with url, title, snippet, relevance_note
- **Field Population Rules:**
  - Required fields: exec_name, current_role, current_company, research_summary
  - Optional fields: career_timeline, achievements, sector/stage exposure, notable companies
  - Confidence estimation: High (≥5 citations, ≥2000 chars), Medium (3-4 citations, 500-2000 chars), Low (<3 citations, <500 chars)

**Enhancement Details:** See `docs/prompt_system_summary.md` for full prompt enhancement features

**Execution Time:** 10-30 seconds

**Implementation Reference:**
- **Factory:** `demo/agents.py:92-107` (`create_research_parser_agent()`)
- **Invocation:** `demo/screening_service.py:168-179`
- **Prompt:** `demo/prompts/catalog.yaml:98-120`
- **Model:** `demo/models.py:45-80` (`ExecutiveResearchResult`)

---

## Agent 3: Incremental Search Agent (Conditional)

### Role
Provides targeted supplemental research when initial Deep Research lacks sufficient quality (citations or content depth), focusing on specific gaps rather than repeating full research.

### Objectives
- **Conditional Trigger:** Only runs if `check_research_quality()` returns False
  - Quality gate: <3 citations OR empty summary
- Perform max 2 targeted web searches to fill identified gaps
- Focus on LinkedIn/biography details, leadership scope, fundraising evidence, low-confidence areas
- Return only new information (avoid duplicating Agent 1 findings)
- Merge supplemental data with original research
- Document remaining gaps after supplemental effort

### Methods

**LLM Model:** `gpt-5`

**Configuration:**
```python
model="gpt-5"
tools=[{"type": "web_search_preview"}]  # OpenAI web search
max_tool_calls=2                        # Hard constraint: ≤2 searches
output_schema=ExecutiveResearchResult   # Same structure as Agent 2
add_datetime_to_context=True
exponential_backoff=True
retries=1                               # Fast-fail for supplemental
delay_between_retries=1
```

**Trigger Condition:** `check_research_quality()` at `demo/agents.py:268-273`
```python
# Quality gate checks:
# 1. len(citations) >= 3
# 2. len(research_summary) > 0 (non-empty)
# If either fails → run Incremental Search
```

**Input:**
```python
candidate_name: str
initial_research: ExecutiveResearchResult  # From Agent 2
quality_gaps: Optional[List[str]]          # Identified gaps
role_spec_markdown: Optional[str]          # For targeted searches
```

**Output:** `ExecutiveResearchResult` (supplemental, merged with original via `merge_research_results()`)

**Prompt Source:** `demo/prompts/catalog.yaml` (key: `incremental_search`)

**Prompt Features (Enhanced v1.0, January 2025):**
- **Gap-Type → Query Mapping (5 categories):**
  - LinkedIn/Biography Details → `"{NAME}" site:linkedin.com OR "{NAME}" "{COMPANY}" bio`
  - Leadership Scope → `"{NAME}" "{COMPANY}" (team size OR headcount OR "managed" OR "led")`
  - Fundraising Evidence (CFO) → `"{NAME}" "{COMPANY}" (funding OR raised OR Series OR IPO)`
  - Product/Technical Evidence (CTO) → `"{NAME}" "{COMPANY}" (product OR launch OR "built" OR technology)`
  - Low-Confidence Area Upgrades → `"{NAME}" "{SPECIFIC_TOPIC}"` (use exact gap text)
- **Search Execution Strategy:**
  - Prioritize role-spec-critical gaps first (fundraising for CFO, product for CTO)
  - Then address general gaps (LinkedIn details, leadership scope)
  - Finally address low-confidence upgrades
  - Stop early when gap is closed with high-confidence evidence
- **Stopping Criteria:**
  - Max 2 searches (hard constraint in prompt and config)
  - Early stop when gap is closed
  - Document gaps when no relevant results found
- **Output Constraints:**
  - Return only NEW information with citations (no duplication)
  - Structured markdown: New Findings, New Citations, Remaining Gaps, Confidence
  - Explicitly document unresolved gaps after supplemental effort

**Enhancement Details:** See `docs/prompt_system_summary.md` for full prompt enhancement features

**Merge Logic:** `demo/agents.py:335-416` (`merge_research_results()`)
```python
# Combines original + supplemental:
- Narrative summaries: "Supplemental Research:" prefix added
- Citations: Deduplicates by URL, preserves order
- Career timeline: Appends new entries
- Achievements/companies/expertise: Merges without duplicates
- Confidence: Updates to reflect merged artifact
- Gaps: Combines and deduplicates
```

**Execution Time:** 1-2 minutes (if triggered)

**Implementation Reference:**
- **Factory:** `demo/agents.py:110-138` (`create_incremental_search_agent()`)
- **Quality Check:** `demo/agents.py:268-273` (`check_research_quality()`)
- **Merge Function:** `demo/agents.py:335-416` (`merge_research_results()`)
- **Invocation:** `demo/screening_service.py:182-205`
- **Prompt:** `demo/prompts/catalog.yaml:122-139`

---

## Agent 4: Assessment Agent

### Role
Performs evidence-aware evaluation of candidates against role specifications, producing structured scores with explicit confidence levels and board-ready insights.

### Objectives
- Score candidates on evaluation dimensions (1-5 scale) with evidence-based reasoning
- Assign `None` (not 0 or NaN) to dimensions lacking sufficient evidence
- Provide dimension-level confidence assessments (High/Medium/Low)
- Check must-have requirements against available evidence
- Identify red flags (3-5 board-ready risk bullets)
- Identify green flags (3-5 strength bullets)
- Generate 2-3 sentence topline verdict
- Produce counterfactuals as concrete follow-up questions
- Respect evidence hierarchy: [FACT] (strongest) > [OBSERVATION] > [HYPOTHESIS] (speculative)

### Methods

**LLM Model:** `gpt-5-mini`

**Configuration:**
```python
model="gpt-5-mini"
tools=[ReasoningTools(add_instructions=True)]  # Structured reasoning
output_schema=AssessmentResult                 # Structured output
add_datetime_to_context=True                   # Temporal awareness
num_history_runs=3                             # Context from recent runs
exponential_backoff=True
retries=2
delay_between_retries=1
```

**Input:**
```python
research: ExecutiveResearchResult      # Final (post-merge from Agent 3 if triggered)
role_spec_markdown: str                # Evaluation rubric
custom_instructions: Optional[str]     # Recruiter overrides
```

**Output:** `AssessmentResult` (Pydantic model)
```python
overall_score: Optional[float]         # 0-100 scale (computed in Python, not by LLM)
overall_confidence: Literal["High", "Medium", "Low"]

dimension_scores: List[DimensionScore]
  - dimension: str                     # "Fundraising Experience"
  - score: Optional[int]               # 1-5 scale, None for Unknown/Insufficient
  - evidence_level: Literal["High", "Medium", "Low"]
  - confidence: Literal["High", "Medium", "Low"]
  - reasoning: str                     # 1-3 sentences
  - evidence_quotes: List[str]         # Direct quotes from research
  - citation_urls: List[str]           # Supporting URLs

must_haves_check: List[MustHaveCheck]
  - requirement: str
  - met: bool
  - evidence: str

red_flags_detected: List[str]          # 3-5 board-ready risk bullets
green_flags: List[str]                 # 3-5 strength bullets
summary: str                           # 2-3 sentence headline verdict
counterfactuals: List[str]             # Concrete follow-up questions

assessment_timestamp: datetime
assessment_model: str                  # "gpt-5-mini"
role_spec_used: Optional[str]          # Role spec title
```

**Prompt Source:** `demo/prompts/catalog.yaml` (key: `assessment`)

**Prompt Features (Enhanced v1.0, January 2025):**
- **Evidence Weighting Rules (4 factors):**
  1. **Source Reliability (Highest Weight):** First-party > Major reputable > Trade press > Aggregators > Unknown
  2. **Recency (High Weight):** Last 2 years > 3-5 years > >5 years (except IPO/major funding remains relevant)
  3. **Citation Count (Medium Weight):** Multiple citations > Single citation > No citations (null/None)
  4. **Confidence Tags (Medium Weight):** [FACT – high] > [FACT – medium] > [FACT – low] > [OBSERVATION] > [HYPOTHESIS] (null/None)
- **Conflict Resolution (5 strategies):**
  - Prefer more recent evidence when sources conflict
  - Prefer higher reliability sources
  - Prefer consensus when multiple sources agree vs. one disagrees
  - Document conflicts in reasoning and use conservative score
  - Mark as null/None when conflict is fundamental and cannot be resolved
- **1-5 Scale Semantics:**
  - `5` = Strong positive / clear strength on this dimension
  - `4` = Solid / generally strong with minor caveats
  - `3` = Mixed / partial fit with notable gaps
  - `2` = Weak / meaningfully below expectations
  - `1` = Strong negative / clearly misaligned with the dimension
  - `null/None` = Insufficient evidence (NOT 0, NaN, or empty values)
- **Evidence Hierarchy:**
  - `[FACT]` - Strongest: roles, dates, companies, deals with citations
  - `[OBSERVATION]` - Medium: patterns inferred from multiple facts
  - `[HYPOTHESIS]` - Speculative: do not use for scoring (treat as null/None)
- **Output Structure:**
  - Headline verdict: "[Overall: Strong/Moderate/Weak] [Role] fit; strongest on [dimension], risks around [dimension]"
  - Board-ready language: Red/green flags as concise, actionable bullets
  - Counterfactuals: Concrete follow-up questions ("If they led 300+ person org post-Series D, Leadership score 3→4")

**Enhancement Details:** See `docs/prompt_system_summary.md` for full prompt enhancement features

**Score Calculation:** `demo/screening_helpers.py:5-19` (`calculate_overall_score()`)
```python
# Computed in Python (not by LLM):
# 1. Filter out None dimension scores
# 2. Average remaining scores: sum / count
# 3. Scale to 0-100: average * 20
# 4. Return None if no dimensions scored
```

**Execution Time:** 30-60 seconds

**Implementation Reference:**
- **Factory:** `demo/agents.py:141-167` (`create_assessment_agent()`)
- **Invocation:** `demo/screening_service.py:208-227`
- **Score Calculation:** `demo/screening_helpers.py:5-19`
- **Prompt:** `demo/prompts/catalog.yaml:141-189`
- **Model:** `demo/models.py:94-116` (`AssessmentResult`)

---

## Workflow Sequence

### Step-by-Step Execution

**Trigger:** AgentOS webhook receives `POST /screen` with a structured `ScreenWebhookPayload` (`screen_slug` containing the Screen record, linked role spec/search, and `candidate_slugs[]`)

**Orchestration:** `demo/screening_service.py` (`process_screen_direct()` plus helper functions for status updates, batch execution, and completion logging)

#### Step 1: Deep Research (2-6 minutes)
```python
# Agent 1: o4-mini-deep-research
result = research_agent.run(
    f"Research: {candidate.name}, {candidate.title} @ {candidate.company}. "
    f"LinkedIn: {candidate.linkedin_url or 'Not provided'}"
)
# Output: markdown + citations
```

#### Step 2: Parse to Structured Data (10-30 seconds)
```python
# Agent 2: gpt-5-mini with structured output
research_result = parser_agent.run(
    f"Parse this research for {candidate.name}...\n\n{markdown}"
)
# Output: ExecutiveResearchResult (Pydantic model)
```

#### Step 3: Quality Gate & Conditional Branch (<1 second check)
```python
# Python function: check_research_quality()
is_sufficient = (
    len(research_result.citations) >= 3 and
    len(research_result.research_summary) > 0
)

if not is_sufficient:
    # Agent 3: gpt-5 with web search, max 2 calls (1-2 minutes)
    supplemental = incremental_agent.run(
        f"Supplemental research for {candidate.name}..."
    )
    # Merge original + supplemental via merge_research_results()
    research_result = merge_research_results(original, supplemental)
else:
    # Skip to assessment
    pass
```

#### Step 4: Assessment (30-60 seconds)
```python
# Agent 4: gpt-5-mini with ReasoningTools
assessment = assessment_agent.run(
    f"Assess {candidate.name} for {role_spec.title}...\n\n"
    f"Research:\n{research_result.research_summary}"
)
# Output: AssessmentResult (dimension scores, red/green flags, verdict)
```

#### Step 5: Score Calculation & Airtable Write (<5 seconds)
```python
# Python calculation (not LLM)
assessment.overall_score = calculate_overall_score(assessment.dimension_scores)
# Formula: (sum of scored dimensions / count) * 20

# Write to Airtable Assessments table
airtable_client.assessments.create({
    "screen_id": screen.id,
    "candidate_id": candidate.id,
    "overall_score": assessment.overall_score,
    "dimension_scores_json": json.dumps(assessment.dimension_scores),
    "red_flags": assessment.red_flags_detected,
    "green_flags": assessment.green_flags,
    "summary": assessment.summary,
    # ... additional fields
})
```

### Error Handling
- **Exponential Backoff:** All agents retry with exponential delay
- **Session State:** Persisted to `SqliteDb` at `tmp/agno_sessions.db`
- **Airtable Updates:** Status tracking in Platform-Screens table
- **AgentOS Dashboard:** Real-time monitoring and session inspection

---

## Key Design Patterns

### 1. Quality-Gated Architecture
**Pattern:** Conditional execution based on research quality heuristics

**Implementation:**
```python
def check_research_quality(result: ExecutiveResearchResult) -> bool:
    """Quality gate: ≥3 citations + non-empty summary"""
    return (
        len(result.citations) >= 3 and
        len(result.research_summary) > 0
    )
```

**Benefit:**
- Saves 1-2 minutes per candidate when quality is high (~60% of cases)
- Targets supplemental research only where needed
- Prevents redundant searches

**Location:** `demo/agents.py:268-273`

---

### 2. Evidence Taxonomy
**Pattern:** Explicit evidence levels in prompts and reasoning

**Implementation:**
- **[FACT]:** Verifiable roles, dates, companies, deals, quotes with citations
- **[OBSERVATION]:** Patterns inferred from multiple facts
- **[HYPOTHESIS]:** Supported but unconfirmed inferences

**Usage:**
- **Deep Research Prompt:** Instructs model to label evidence explicitly
- **Research Parser:** Maps [FACT] → structured fields, [OBSERVATION] → narrative
- **Assessment Prompt:** Treats [FACT] as strongest evidence, [HYPOTHESIS] as speculative

**Benefit:**
- Clear separation of verifiable facts vs. inferences
- Enables downstream confidence scoring
- Supports evidence-aware assessment

**Location:** `demo/prompts/catalog.yaml` (all 4 prompts use taxonomy)

---

### 3. Evidence-Aware Scoring
**Pattern:** Explicit handling of "Unknown" using `None` (not 0 or NaN)

**Implementation:**
```python
# In Pydantic model:
score: Optional[int]  # 1-5 scale, None for Unknown/Insufficient

# In prompt:
"Use null (not 0 or NaN) for dimensions lacking sufficient evidence"

# In Python calculation:
def calculate_overall_score(dimensions: List[DimensionScore]) -> Optional[float]:
    scored = [d.score for d in dimensions if d.score is not None]
    if not scored:
        return None
    return (sum(scored) / len(scored)) * 20  # 1-5 → 0-100 scale
```

**Benefit:**
- Distinguishes "Unknown" from "Poor" (0 would falsely lower overall score)
- Maintains assessment integrity when evidence is sparse
- Supports confidence-weighted evaluation

**Location:**
- Model: `demo/models.py:94-116`
- Calculation: `demo/screening_helpers.py:5-19`
- Prompt: `demo/prompts/catalog.yaml:141-189`

---

### 4. Centralized Prompt Management
**Pattern:** YAML prompt catalog with code-free iteration

**Structure:**
```yaml
# demo/prompts/catalog.yaml
agents:
  deep_research:
    description: "Comprehensive OSINT profiling"
    instructions: |
      You are an expert executive researcher...
    markdown: true

  research_parser:
    description: "Parse research to structured format"
    instructions: |
      Parse the following research...
```

**Loader:**
```python
# demo/prompts/library.py
def get_prompt(name: str) -> PromptContext:
    """Load prompt from YAML catalog"""
    with open("demo/prompts/catalog.yaml") as f:
        catalog = yaml.safe_load(f)
    return PromptContext(**catalog["agents"][name])

# Usage in agent factory:
prompt = get_prompt("deep_research")
agent = Agent(
    name=prompt.description,
    instructions=prompt.instructions,
    ...
)
```

**Benefit:**
- Version-controlled prompts (git tracked)
- No hardcoded strings in Python code
- Fast iteration without code changes
- Centralized template management

**Location:**
- Catalog: `demo/prompts/catalog.yaml` (190 lines)
- Loader: `demo/prompts/library.py` (~40 lines)
- Usage: All 4 agent factories in `demo/agents.py`

---

### 5. Two-Phase Research Pattern
**Pattern:** Deep Research (markdown) → Parser (structured output)

**Rationale:**
- OpenAI Deep Research API doesn't support `output_schema` parameter
- Separation of concerns: research quality vs. data extraction
- Allows flexible markdown structure while ensuring typed output

**Flow:**
```
Agent 1 (o4-mini-deep-research)
  → Markdown + citations (unstructured)

Agent 2 (gpt-5-mini)
  → ExecutiveResearchResult (Pydantic, structured)
```

**Benefit:**
- Leverages o4-mini's research strengths without schema constraints
- gpt-5-mini handles fast, reliable parsing
- Type safety for downstream assessment

**Location:** `demo/agents.py:40-107`, `demo/screening_service.py:153-179`

---

### 6. Session State Persistence
**Pattern:** Agno `SqliteDb` for workflow tracking (not `InMemoryDb`)

**Configuration:**
```python
# demo/agents.py:169-174
from agno.storage.db.sqlite import SqliteDb

db = SqliteDb(
    table_name="screening_sessions",
    db_file="tmp/agno_sessions.db"
)
```

**Benefit:**
- Persistent session history across restarts
- AgentOS Dashboard access to session logs
- Audit trail for workflow debugging
- Foundation for Phase 2 async processing

**Location:** `demo/agents.py:169-174`, `tmp/agno_sessions.db`

---

## Reference Tables

### Agent → Model → Purpose

| Agent | Model | Purpose | Execution Time | Structured Output | Tools |
|-------|-------|---------|----------------|-------------------|-------|
| **Deep Research** | `o4-mini-deep-research` | OSINT profiling with web search | 2-6 min | ❌ (markdown only) | Built-in web search + citations |
| **Research Parser** | `gpt-5-mini` | Markdown → structured data | 10-30 sec | ✅ `ExecutiveResearchResult` | None |
| **Incremental Search** | `gpt-5` | Targeted supplemental research | 1-2 min (conditional) | ✅ `ExecutiveResearchResult` | `web_search_preview` (max 2 calls) |
| **Assessment** | `gpt-5-mini` | Evidence-aware scoring | 30-60 sec | ✅ `AssessmentResult` | `ReasoningTools` |

---

### File Reference Map

| Component | File | Lines | Description |
|-----------|------|-------|-------------|
| **Agent Factories** | `demo/agents.py` | 867 | 4 agent creation functions + helpers |
| **Workflow Orchestration** | `demo/screening_service.py` | 270 | `process_screen_direct()` main loop + shared helpers |
| **Prompt Catalog** | `demo/prompts/catalog.yaml` | 190 | YAML definitions for all 4 agents |
| **Prompt Loader** | `demo/prompts/library.py` | ~40 | `get_prompt()` function |
| **Data Models** | `demo/models.py` | 119 | 7 Pydantic schemas |
| **AgentOS Runtime** | `demo/agentos_app.py` | 665 | FastAPI server, `/screen` endpoint |
| **Airtable Client** | `demo/airtable_client.py` | 400 | 8 table accessors, CRUD operations |
| **Scoring Helpers** | `demo/screening_helpers.py` | ~50 | `calculate_overall_score()`, quality check |
| **Session State** | `tmp/agno_sessions.db` | N/A | SqliteDb persistence (gitignored) |

---

### Prompt Reference Table

| Agent | Prompt Key | Lines in YAML | Key Directives |
|-------|-----------|---------------|----------------|
| **Deep Research** | `deep_research` | 6-96 | [FACT/OBSERVATION/HYPOTHESIS] taxonomy, 5-section output, source prioritization |
| **Research Parser** | `research_parser` | 98-120 | Respect taxonomy, extract facts to fields, surface gaps, avoid invention |
| **Incremental Search** | `incremental_search` | 122-139 | Max 2 searches, target gaps, return new info only, document remaining gaps |
| **Assessment** | `assessment` | 141-189 | 1-5 scale semantics, null for unknown, board-ready language, counterfactuals |

---

### Test Coverage by Agent

| Agent | Test File | Tests | Coverage | Key Test Cases |
|-------|-----------|-------|----------|----------------|
| **Deep Research** | `tests/test_research_agent.py` | 21 | ~85% | Citation extraction, markdown parsing, timeout handling |
| **Research Parser** | `tests/test_models_validation.py` | 6 | 100% | Pydantic validation, required fields, confidence levels |
| **Incremental Search** | `tests/test_quality_check.py` | 9 | 100% | Quality gate logic, merge functions, gap identification |
| **Assessment** | `tests/test_scoring.py` | 7 | 100% | Dimension scoring, overall score calc, None handling |
| **Workflow** | `tests/test_workflow.py` | 9 | ~80% | End-to-end integration, error handling, session state |
| **AgentOS** | `tests/test_agentos_app.py` | 5 | ~75% | Webhook endpoint, payload validation, error responses |

**Overall Coverage:** 130 tests, 75% coverage (exceeds 50% target)

---

## Configuration & Environment

### Required Environment Variables

```bash
# .env file
OPENAI_API_KEY=sk-...                  # OpenAI API access
AIRTABLE_API_KEY=key...                # Airtable access
AIRTABLE_BASE_ID=app...                # Target base

# Optional
FASTAPI_PORT=5001                      # AgentOS server port (default: 5001)
AGENTOS_SECURITY_KEY=...               # Control plane auth (optional)
```

### Runtime Dependencies

```toml
# pyproject.toml
[dependencies]
agno = "^1.0.0"                        # Agent framework
openai = "^1.58.1"                     # LLM API
pyairtable = "^2.3.3"                  # Airtable client
pydantic = "^2.10.4"                   # Data models
fastapi = "^0.115.6"                   # AgentOS runtime
uvicorn = "^0.34.0"                    # ASGI server
python-dotenv = "^1.0.1"               # Config loading
pyyaml = "^6.0.2"                      # Prompt catalog loader
```

### Local Development Setup

**3 Terminal Workflow:**

1. **Terminal 1 - AgentOS Server:**
   ```bash
   source .venv/bin/activate
   uv run python demo/agentos_app.py
   # Starts on http://localhost:5001
   ```

2. **Terminal 2 - ngrok Tunnel:**
   ```bash
   ngrok http 5001
   # Copy HTTPS URL for Airtable automation
   ```

3. **Terminal 3 - AgentOS Control Plane (Optional):**
   ```bash
   # Open https://os.agno.com
   # Add new OS → Connect to http://localhost:5001
   # Real-time session monitoring
   ```

**Airtable Automation:**
- Trigger: Platform-Screens record status = "Ready to Screen"
- Action: Run `scripts/airtable_webhook_automation.js` (updates `WEBHOOK_URL` to `https://YOUR_NGROK_URL.ngrok.io/screen`)
- Behavior: Script fetches linked Role Spec/Search/Candidates, builds the `screen_slug` payload, and POSTs it with `Content-Type: application/json`

---

## Production Considerations

### Scalability Constraints (V1)
- **Sequential Execution:** One candidate at a time (Phase 2: async/parallel)
- **No Caching:** Research repeated for same candidate (Phase 2: cache layer)
- **Single-Pass Research:** Max 1 incremental search (Phase 2: multi-iteration)
- **Local Session State:** SqliteDb at `tmp/` (Phase 2: PostgreSQL)

### Performance Optimizations
- **Quality Gate:** Saves 1-2 min per candidate when research is sufficient
- **Model Selection:** gpt-5-mini for fast parsing/assessment (not o4-mini)
- **Max Tool Calls:** Constrained to 1-2 to prevent runaway searches
- **Timeouts:** 10-minute cap on Deep Research to prevent hangs

### Monitoring & Observability
- **AgentOS Dashboard:** Real-time workflow status at `https://os.agno.com`
- **Session Logs:** SqliteDb persistence at `tmp/agno_sessions.db`
- **Airtable Status:** Platform-Screens table tracks progress
- **Error Handling:** Exponential backoff with retries, structured logging

### Phase 2 Enhancements (Future)
- Async processing (multiple candidates in parallel)
- Research cache (avoid re-researching same candidate)
- Multi-iteration incremental search (iterative gap-filling)
- PostgreSQL session state (production-grade persistence)
- Custom event tables (fine-grained audit trail)
- Fast mode (skip incremental search, accept lower quality)

---

## Key Achievements

This agent architecture demonstrates:

1. **Modern AI Agent Design:** Quality-gated workflow, conditional branching, evidence-aware scoring
2. **Production-Quality Engineering:** 73% test coverage, type hints, structured outputs, comprehensive docs
3. **Thoughtful Context Engineering:** Evidence taxonomy, explicit unknowns, counterfactuals
4. **Scalable Foundation:** Modular prompts, session persistence, clear Phase 2 path
5. **Domain Calibration:** VC/talent workflow understanding, board-ready language, recruiter-friendly outputs

---

**Document Maintenance:**
- Update when agent configuration changes
- Reflect prompt modifications in YAML catalog
- Document new agents or workflow steps
- Keep test coverage stats current

**Related Documentation:**
- **Setup Guide:** `README.md` (765 lines)
- **Technical Spec:** `spec/spec.md` (2040+ lines)
- **Architecture Analysis:** `DESIGN_SYNTHESIS.md` (1,880 lines)
- **Progress Tracking:** `spec/dev_plan_and_checklist.md`
- **Prompt Catalog:** `demo/prompts/catalog.yaml` (190 lines)
