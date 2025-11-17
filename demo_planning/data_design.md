# Data Design Reference

> Data models, schemas, and design decisions for the Talent Signal Agent demo

---

## Decisions & Status

### Data Sources (CONFIRMED)
- **Primary Source:** `reference/guildmember_scrape.csv` (64 executives from FirstMark guilds)
  - Fields: full_name, title_raw, company, misc_liheadline, source
  - Mix of CFO, CTO, CPO, CRO, CEO, Founders
  - Real people with LinkedIn profiles
- **Mock Data:** NOT creating Mock_Guilds.csv or Exec_Network.csv
  - Using actual scraped data instead
- **Enrichment:** Stub/mock Apollo API responses (not real API calls)

### Airtable Schema (IN PROGRESS - See Outstanding Decisions in technical_spec.md)

**Key Decisions Made:**
- Demo: Only upload people (no company/role uploads via Module 1)
- Title Table: NOT in demo - using standard dropdowns instead
- Role specs: Markdown-based, stored in Long Text field (see role_spec_design.md)

**Key Decisions Needed:**
- Complete field definitions for all tables
- Storage format for research results, assessments, citations
- Dimension score storage: individual fields vs JSON

---

## Data Models

### Normalized Title Taxonomy

**C-Level Functions:**
- Chief Executive Officer (CEO)
- Chief Financial Officer (CFO)
- Chief Technical Officer (CTO)
- Chief Product Officer (CPO)
- Chief People Officer (CPO)
- Chief Revenue Officer (CRO)
- Chief Operating Officer (COO)
- Chief Marketing Officer (CMO)
- Chief Design Officer (CDO)
- Chief Development Officer (CDO)

**Executive Functions (Non-C-Level):**
- Exec_Finance (VP Finance, Head of Finance, etc.)
- Exec_Tech (VP Engineering, Head of Engineering, etc.)
- Exec_Product (VP Product, Head of Product, etc.)
- Exec_People (VP People, Head of People, etc.)
- Exec_Sales-Revenue (VP Sales, Head of Revenue, etc.)
- Exec_Operations (VP Operations, Head of Operations, etc.)
- Exec_Marketing (VP Marketing, Head of Marketing, etc.)
- Exec_Design (VP Design, Head of Design, etc.)
- Exec_Other (Other executive roles)

**Seniority Levels:**
- C-Level
- VP (Vice President)
- SVP (Senior Vice President)
- Head
- Director
- Senior Director

---

## Input Data Schema

### Source: guildmember_scrape.csv (ACTUAL DATA)

**CSV Structure:**
- `full_name` (string) - Executive name
- `title_raw` (string) - Raw job title (non-normalized)
- `company` (string) - Current company
- `misc_liheadline` (string, optional) - LinkedIn headline with additional context
- `source` (string) - Source of record (FMLinkedIN, FMGuildPage, FMCFO, FMCTOSummit, FMFounder, FMProduct)

**Sample Records:**
- Jonathan Carr, CFO, Armis
- Ben Kus, CTO, Box
- Isabelle Winkles, CFO, Braze
- Deb Schwartz, CFO, Cameo
- Brendan Humphreys, CTO, Canva

**Data Characteristics:**
- 64 total records
- Mix of CFO, CTO, CPO, CRO, CEO, Founders
- Real companies (mix of FirstMark portfolio and others)
- Some records have LinkedIn headlines, some don't
- Non-normalized titles (will require mapping)

---

## Airtable Database Schema

### People Table

**Status:** Field definitions in progress

**Confirmed Fields:**
- Name (string)
- Current Title (string) - from title_raw
- Current Company (string)
- LinkedIn Headline (Long Text, optional) - from misc_liheadline
- Source (Single Select) - from source field

**Pending Decisions:**
- LinkedIn URL (string) - need to add or derive
- Bio (Long Text or Rich Text?) - where does this come from?
- Normalized Function (Single Select: CFO, CTO, CPO, etc.)
- Location (string) - not in guildmember_scrape.csv, need enrichment?
- Company Stage (Single Select) - not in scrape, need enrichment?
- Sector (Single Select) - not in scrape, need enrichment?

**Questions:**
- Which fields from guildmember_scrape.csv map to People table?
- Do we enrich with mock Apollo data to add missing fields?
- What's the primary key? (auto-generated ID or full_name?)

### Company Table

**Status:** Field definitions needed

**Questions:**
- Do we need a separate Company table for demo?
- Or just store company name as text in People table?

### Portco Table

**Status:** Field definitions needed

**Confirmed Portcos for Demo:**
1. Pigment (B2B SaaS, enterprise, international)
2. Mockingbird (Consumer DTC, physical product)
3. Synthesia (AI/ML SaaS, global scale)
4. Estuary (Data infrastructure, developer tools)

**Pending Decisions:**
- What fields are needed? (name, stage, sector, description, website)
- Pre-populate or create during demo?

### Platform - Hiring - Portco Roles

**Status:** Field definitions needed

**Questions:**
- Fields: role_id, portco_link, role_type (CFO/CTO), status, description?
- Will have 4 records for demo (one per portco scenario)

### Platform - Hiring - Search

**Status:** Field definitions needed

**Purpose:** Active searches where FirstMark is assisting

**Questions:**
- Fields: search_id, role_link, spec_link, notes, timeline, status?
- How does this differ from Portco Roles table?

### Platform - Hiring - Screen

**Status:** Partial field definitions in technical_spec.md

**Fields (Confirmed):**
- screen_id (auto-generated)
- search_link (Link to Search table)
- candidates_links (Multiple links to People table)
- status (Single Select)
- created_date (Date)

**Fields (Pending):**
- Status enum values: Draft, Ready to Screen, Processing, Complete, Failed?
- Custom instructions field (Long Text)?
- Results summary field?

### Operations - Workflows

**Status:** Field definitions needed

**Purpose:** Audit trail and execution logs for all operations

**Questions:**
- What fields are needed for audit trail?
- How are research results stored?
- How are assessment results stored?
- Execution logs format (JSON? Long Text?)?
- Link to Screen, People, and Role Eval tables?

### Role Spec Table

**Status:** Fully defined in role_spec_design.md

**Fields:**
- spec_id (auto-generated)
- spec_name (string) - e.g., "CFO - Series B SaaS"
- role_type (Single Select: CFO, CTO)
- is_template (checkbox) - true for base templates
- spec_content (Long Text) - Markdown-formatted spec
- created_date (Date)
- modified_date (Date)

**Will have 6 records for demo:**
- CFO Template (base)
- CTO Template (base)
- Pigment CFO Spec (customized from template)
- Mockingbird CFO Spec (customized from template)
- Synthesia CTO Spec (customized from template)
- Estuary CTO Spec (customized from template)

### Role Eval / Assessments Table (v1 storage of research + assessment)

**Status:** See finalized `Assessments` table definition in `demo_planning/airtable_schema.md`.

**Purpose:** Stores assessment results for candidate-role pairs.

**Key Fields (summary – see `airtable_schema.md` for canonical list):**
- `assessment_id` (Auto ID)
- `screen` (Link to Screens)
- `candidate` (Link to People)
- `role` (Link to Portco_Roles)
- `role_spec` (Link to Role_Specs)
- `status` (Single Select: Pending → Processing → Complete/Failed)
- `overall_score` (Number, 0–100, nullable)
- `overall_confidence` (Single Select: High, Medium, Low)
- `topline_summary` (Long Text)
- `dimension_scores_json` (Long Text) – JSON array of `DimensionScore` objects:
  - `dimension`
  - `score` (1–5 or `null`, where `null` = Unknown / Insufficient public evidence)
  - `evidence_level`
  - `confidence`
  - `reasoning`
  - `evidence_quotes` (array of strings)
  - `citation_urls` (array of URLs)
- `must_haves_check_json` (Long Text) – JSON array of `MustHaveCheck` objects
- `red_flags_json` / `green_flags_json` (Long Text, JSON arrays)
- `counterfactuals_json` (Long Text, JSON array)
- `research_structured_json` (Long Text) – entire `ExecutiveResearchResult`
- `research_markdown_raw` (Long Text) – Deep Research markdown blob w/ inline citations
- `assessment_json` (Long Text) – entire `AssessmentResult` (with reasoning trace captured via Agno `ReasoningTools`)
- `assessment_markdown_report` (Long Text) – optional formatted narrative
- `runtime_seconds` (Number) + `error_message` (Long Text) for operational visibility
- `assessment_timestamp`, `research_model`, `assessment_model`

**Design Notes:**
- Dimension scores are stored as JSON to avoid constantly changing Airtable fields when specs evolve.
- The 1–5 scale (with `null` for Unknown) matches the updated role spec design and allows the system to be explicit when the web data is insufficient.
- **Important:** Use `null` in JSON (or `None` in Python), NOT NaN or 0, to represent unknown/unscored dimensions.
- Overall score is calculated in Python using the v1 simple-average × 20 algorithm (see `spec/v1_minimal_spec.md`) and written back as a single number for easy sorting.
- Research and assessment artifacts share the same record to keep Airtable as the single source of truth (no `Research_Results` or `Workflows` tables in v1).

---

## Structured Output Schemas

### Pydantic Models for LLM Outputs

All structured LLM interactions (parsing, assessment, fast web-search mode) use Pydantic models to ensure type safety and consistent parsing. Deep Research itself returns markdown + citations, which are parsed into these models.

#### Core Models

```python
from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime

# ============================================================================
# Research Output Models (from research pipeline)
# ============================================================================

class Citation(BaseModel):
    """Source citation from research."""
    url: str
    title: str
    snippet: str
    relevance_note: Optional[str] = None

class CareerEntry(BaseModel):
    """Timeline entry for career history."""
    company: str
    role: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    key_achievements: list[str] = Field(default_factory=list)

class ExecutiveResearchResult(BaseModel):
    """Structured research output produced directly via Deep Research (structured responses) with optional incremental search blending."""
    exec_name: str
    current_role: str
    current_company: str

    # Career & Experience
    career_timeline: list[CareerEntry] = Field(default_factory=list)
    total_years_experience: Optional[int] = None

    # Key Areas (aligned with role spec dimensions)
    fundraising_experience: Optional[str] = None  # CFO-specific
    operational_finance_experience: Optional[str] = None  # CFO-specific
    technical_leadership_experience: Optional[str] = None  # CTO-specific
    team_building_experience: Optional[str] = None
    sector_expertise: list[str] = Field(default_factory=list)
    stage_exposure: list[str] = Field(default_factory=list)  # e.g., ["Series A", "Series B", "Growth"]

    # Summary & Evidence
    research_summary: str
    key_achievements: list[str] = Field(default_factory=list)
    notable_companies: list[str] = Field(default_factory=list)
    citations: list[Citation] = Field(default_factory=list)

    # Confidence & Gaps (stored on Assessments table)
    research_confidence: Literal["High", "Medium", "Low"] = "Medium"
    gaps: list[str] = Field(default_factory=list)

    # Metadata
    research_timestamp: datetime = Field(default_factory=datetime.now)
    research_model: str = "o4-mini-deep-research"

# ============================================================================
# Assessment Output Models (from gpt-5-mini)
# ============================================================================

class DimensionScore(BaseModel):
    """Evidence-aware dimension score for a single evaluation criterion."""
    dimension: str

    # Scoring (1-5 scale with None for Unknown)
    score: Optional[int] = Field(None, ge=1, le=5)
    # None (Python) / null (JSON) = Unknown / Insufficient public evidence to score
    # DO NOT use NaN or 0 - use None to represent missing/unknown scores

    # Evidence Quality
    evidence_level: Literal["High", "Medium", "Low"]  # From role spec
    confidence: Literal["High", "Medium", "Low"]  # LLM self-assessment

    # Reasoning & Evidence
    reasoning: str  # 1-3 sentences explaining the score
    evidence_quotes: list[str] = Field(default_factory=list)  # Key supporting quotes
    citation_urls: list[str] = Field(default_factory=list)  # Source URLs

class MustHaveCheck(BaseModel):
    """Evaluation of must-have requirements."""
    requirement: str
    met: bool
    evidence: Optional[str] = None

class AssessmentResult(BaseModel):
    """Structured assessment output (from gpt-5-mini)."""

    # Overall Assessment
    overall_score: Optional[float] = Field(None, ge=0, le=100)
    # Computed in Python from dimension scores using evidence-aware weighting
    overall_confidence: Literal["High", "Medium", "Low"]

    # Dimension-Level Scores
    dimension_scores: list[DimensionScore]

    # Requirements Checking
    must_haves_check: list[MustHaveCheck] = Field(default_factory=list)
    red_flags_detected: list[str] = Field(default_factory=list)
    green_flags: list[str] = Field(default_factory=list)

    # Qualitative Assessment
    summary: str  # 2-3 sentence topline assessment
    counterfactuals: list[str] = Field(default_factory=list)
    # Key assumptions or what would most change the recommendation

    # Metadata
    assessment_timestamp: datetime = Field(default_factory=datetime.now)
    assessment_model: str = "gpt-5-mini"
    role_spec_used: Optional[str] = None  # spec_id or spec_name

# ============================================================================
# Alternative Assessment (Model-Generated Rubric)
# ============================================================================

class ModelGeneratedDimension(BaseModel):
    """Dimension created by the model (Evaluation B)."""
    dimension_name: str
    definition: str
    score: int = Field(ge=1, le=5)
    reasoning: str

class AlternativeAssessment(BaseModel):
    """Assessment using model-generated rubric (exploratory evaluation)."""
    generated_dimensions: list[ModelGeneratedDimension]
    overall_assessment: str
    comparison_notes: Optional[str] = None  # How this differs from spec-based eval
```

#### Usage Examples

```python
from agno import Agent, OpenAIResponses
from agno.tools.reasoning import ReasoningTools

# Deep Research Agent (structured output directly)
deep_research_agent = Agent(
    model=OpenAIResponses(id="o4-mini-deep-research", max_tool_calls=1),
    output_schema=ExecutiveResearchResult,
    instructions=[
        "Run comprehensive executive research with inline citations.",
        "Return the ExecutiveResearchResult schema directly (no downstream parser)."
    ],
    retries=2,
    exponential_backoff=True,
)

# Optional incremental search agent (single pass, max two web calls)
incremental_search_agent = Agent(
    model=OpenAIResponses(id="gpt-5-mini"),
    tools=[{"type": "web_search_preview", "max_results": 5}],
    max_tool_calls=2,
    output_schema=ExecutiveResearchResult,
    instructions=[
        "Only run when quality heuristics flag missing evidence (e.g., <3 citations).",
        "Perform at most two focused searches to fill the gaps, then emit an updated ExecutiveResearchResult."
    ],
)

# Assessment Agent (spec-guided, ReasoningTools required)
assessment_agent = Agent(
    model=OpenAIResponses(id="gpt-5-mini"),
    tools=[ReasoningTools(add_instructions=True)],
    instructions="Evaluate the candidate against the linked role spec. Provide explicit reasoning for each dimension and overall recommendation.",
    output_schema=AssessmentResult,
)
```

#### Schema Design Notes

**Evidence-Aware Scoring:**
- `score: Optional[int]` allows `None` (Python) / `null` (JSON) for "Unknown/Insufficient Evidence"
- Range 1-5 when evidence exists, `None` when it doesn't
- **DO NOT use:** NaN, 0, or empty string - always use `None` for missing scores
- Prevents forced guessing when public data is thin
- Example: `{"score": null, "reasoning": "No public data on fundraising experience"}`

**Handling None Scores in Code:**
```python
# Checking for unknown scores
if dimension.score is None:
    print(f"{dimension.dimension}: Insufficient evidence")

# Filtering scored dimensions
scored_dims = [d for d in assessment.dimension_scores if d.score is not None]

# Converting to pandas (None → NaN automatically)
import pandas as pd
df = pd.DataFrame([d.dict() for d in assessment.dimension_scores])
# df['score'] will have NaN for None values
```

**Confidence vs Evidence Level:**
- `evidence_level` (High/Medium/Low): From role spec, indicates how observable this dimension typically is
- `confidence` (High/Medium/Low): LLM self-assessment of certainty given the actual evidence found
- Both can be present even when `score = None` (LLM can be confident that evidence is insufficient)

**Overall Score Calculation:**
- Computed in Python, not by LLM
- Uses the v1 simple-average × 20 algorithm (ignore `None` scores entirely)
- Only dimensions with non-None scores contribute to overall_score
- See `spec/v1_minimal_spec.md` / `technical_spec_V2.md` addendum for calculation logic

**ReasoningTools Requirement:**
- Assessment agent must include `ReasoningTools(add_instructions=True)` so the JSON contains explicit thinking traces satisfying PRD AC-PRD-04.
- This configuration is part of the baseline, not a future enhancement.

**Two Evaluations:**
- `AssessmentResult`: Primary (spec-based, evidence-aware)
- `AlternativeAssessment`: Secondary (model-generated rubric for comparison)

---

## Mock Data Requirements

### For 3 Pre-Run Scenarios

**Pigment CFO:**
- 3-5 candidate profiles selected from guildmember_scrape.csv
- Mock research_structured_json + research_markdown_raw blobs for each candidate
- Assessment results with full dimension scores + assessment_json payloads
- Optional assessment_markdown_report (only if time permits)

**Mockingbird CFO:**
- 3-5 candidate profiles
- Mock research_structured_json + assessment_json outputs
- Optional assessment_markdown_report

**Synthesia CTO:**
- 3-5 candidate profiles
- Mock research_structured_json + assessment_json outputs
- Optional assessment_markdown_report

### For 1 Live Scenario

**Estuary CTO:**
- 2-3 candidate profiles (will run live during demo)
- Pre-load candidates and role spec into Airtable
- Test execution but don't save results

---

## Data Flow

### Module 1: Data Upload (Optional for Demo)
```
CSV Upload → Normalize → Dedupe? → Load to People Table
```

### Module 4: Screening Workflow (Core Demo)
```
1. Screen record moves to "Ready to Screen" (automation triggers /screen endpoint)
2. For each candidate (sequential):
   a. Create/ensure Assessment record linked to Screen + Role + Spec
   b. Run Deep Research agent (structured output) → populate research_structured_json + research_markdown_raw
   c. Run quality heuristic; if low evidence, execute optional incremental search agent (max two tool calls) and merge results
   d. Run Assessment agent (ReasoningTools-enabled) → populate assessment_json + derived summary fields
   e. Update Assessment status (`Processing` → `Complete`/`Failed`), runtime_seconds, error_message (if needed)
3. Update Screen status + summary fields; rely on Airtable + Agno `SqliteDb` for audit (no Workflows table)
4. Optional: render assessment_markdown_report for shareouts (Phase 2 enhancement)
```

---

## Outstanding Questions for Schema Definition

1. **People Table:** Complete field mapping from guildmember_scrape.csv
2. **Enrichment Strategy:** Which missing fields (location, stage, sector) come from mock Apollo?
3. **Research Storage:** Full text vs summary vs citations only?
4. **Assessment Storage:** Individual fields vs JSON for dimension scores?
5. **Citation Handling:** Store URLs only or full content?
6. **Primary Keys:** Auto-generated IDs vs natural keys?
7. **Deduplication:** Needed for demo or assume clean data?

---

## Next Steps

1. Resolve Outstanding Decisions in technical_spec.md
2. Complete field definitions for all Airtable tables
3. Create structured output schemas for LLM responses
4. Map guildmember_scrape.csv fields to People table
5. Define mock Apollo enrichment data structure
