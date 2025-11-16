---
version: "1.0"
created: "2025-01-16"
updated: "2025-01-16"
project: "Talent Signal Agent"
context: "FirstMark Capital AI Lead Case Study"
---

# Technical Specification: Talent Signal Agent

Engineering contract for Python implementation of AI-powered executive matching system

## Architecture

### System Overview

The Talent Signal Agent is a demo-quality Python application that uses AI agents to research and evaluate executive candidates against role specifications. The system integrates with Airtable for data storage and UI, uses OpenAI's Deep Research API for candidate research, and employs structured LLM outputs for evidence-aware assessments.

**Key Design Principles:**
- **Evidence-Aware Scoring:** Explicit handling of "Unknown" when public data is insufficient (using `None`/`null`, not 0 or NaN)
- **Quality-Gated Research:** Conditional supplemental search triggered only when initial research is insufficient
- **Audit Trail:** Complete event logging for transparency and debugging
- **Flexible Execution:** Toggle between deep research (comprehensive) and fast mode (quick turnaround)

### Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      AIRTABLE DATABASE                       │
│  People (64) | Portcos (4) | Roles (4) | Specs (6)         │
│  Searches (4) | Screens (4) | Workflows | Research | Assess │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ Automation Trigger (Status Change)
                     ▼
            ┌─────────────────┐
            │  NGROK TUNNEL    │ (Demo Only)
            └────────┬─────────┘
                     │
                     ▼
         ┌──────────────────────┐
         │   FLASK WEBHOOK      │  (:5000)
         │   SERVER             │
         └────────┬─────────────┘
                  │
                  ▼
    ┌─────────────────────────────┐
    │  AGNO WORKFLOW ORCHESTRATOR  │
    │                              │
    │  Step 1: Deep Research Agent │
    │    ├─ o4-mini-deep-research  │
    │    └─ OR gpt-5 + web_search  │
    │                              │
    │  Step 2: Quality Gate        │
    │    └─ Check research quality │
    │                              │
    │  Step 3: Conditional Branch  │
    │    ├─ Supplemental Search    │
    │    │   └─ gpt-5 + web_search │
    │    └─ Merge Research         │
    │                              │
    │  Step 4: Assessment Agent    │
    │    └─ gpt-5-mini + spec      │
    └────────┬────────────────────┘
             │
             │ Write Results
             ▼
    ┌────────────────────┐
    │  AIRTABLE API      │
    │  (pyairtable)      │
    │                    │
    │  - Workflows       │
    │  - Research        │
    │  - Assessments     │
    └────────────────────┘

    ┌────────────────────┐
    │  OPENAI APIS       │
    │                    │
    │  - Deep Research   │
    │  - GPT-5 / GPT-5-mini │
    │  - Web Search      │
    └────────────────────┘

    ┌────────────────────┐
    │  SQLITE DB         │
    │  (Workflow Events) │
    └────────────────────┘
```

### Technology Stack

- **Language:** Python 3.11+
- **Framework:** Flask (webhook server), Agno (agent orchestration)
- **LLM Provider:** OpenAI (o4-mini-deep-research, gpt-5-mini, gpt-5)
- **Database:** Airtable (primary), SQLite (workflow events)
- **Validation:** Pydantic (structured outputs)
- **Package Manager:** UV
- **Tunnel:** ngrok (local demo)

### Project Structure

```
demo_files/
├── __init__.py
├── agents/                    # Agent configurations
│   ├── __init__.py
│   ├── research_agent.py      # Deep research + web search modes
│   ├── assessment_agent.py    # Spec-guided evaluation
│   └── web_search_agent.py    # Supplemental search
├── models/                    # Pydantic data models
│   ├── __init__.py
│   ├── research.py            # ExecutiveResearchResult, Citation
│   ├── assessment.py          # AssessmentResult, DimensionScore
│   └── workflow.py            # ResearchSupplement, quality metrics
├── workflows/                 # Agno workflow definitions
│   ├── __init__.py
│   ├── screening_workflow.py  # Main candidate screening workflow
│   └── workflow_functions.py  # Custom step functions
├── integrations/              # External service clients
│   ├── __init__.py
│   ├── airtable_client.py     # Airtable read/write operations
│   └── openai_client.py       # OpenAI API wrapper (if needed)
├── utils/                     # Helper functions
│   ├── __init__.py
│   ├── scoring.py             # Overall score calculation
│   ├── spec_parser.py         # Role spec markdown parser
│   └── logger.py              # Structured logging setup
├── webhook_server.py          # Flask app with /screen endpoint
└── config.py                  # Environment variables and config

tests/
├── __init__.py
├── test_agents/               # Agent unit tests
├── test_models/               # Pydantic model tests
├── test_workflows/            # Workflow integration tests
├── test_utils/                # Utility function tests
├── fixtures/                  # Test data
│   ├── mock_research.json
│   ├── mock_assessment.json
│   └── sample_specs/
└── conftest.py                # Pytest configuration

spec/                          # Documentation
├── constitution.md            # Project governance
├── prd.md                     # Product requirements
└── spec.md                    # This file

.python-version                # Python 3.11
pyproject.toml                 # Dependencies
.env.example                   # Environment variables template
README.md                      # Implementation guide
```

---

## Interfaces

### Research Agent Interface

**Purpose:** Conduct comprehensive executive research using OpenAI Deep Research or fast web search mode.

**Signature:**
```python
from pathlib import Path
from typing import Optional
from agno import Agent, OpenAIResponses
from models.research import ExecutiveResearchResult

def create_research_agent(use_deep_research: bool = True) -> Agent:
    """Create research agent with flexible execution mode.

    Args:
        use_deep_research: If True, use o4-mini-deep-research (2-5 min).
                          If False, use gpt-5 + web_search (30-60 sec).

    Returns:
        Configured Agno Agent instance.
    """
    pass

def run_research(
    candidate_name: str,
    current_title: str,
    current_company: str,
    linkedin_url: Optional[str] = None,
    use_deep_research: bool = True
) -> ExecutiveResearchResult:
    """Execute research on candidate and return structured results.

    Args:
        candidate_name: Executive full name
        current_title: Current job title
        current_company: Current company name
        linkedin_url: LinkedIn profile URL (optional)
        use_deep_research: Toggle between deep and fast modes

    Returns:
        ExecutiveResearchResult with career timeline, expertise, citations

    Raises:
        RuntimeError: If research agent execution fails after retries
    """
    pass
```

**Examples:**
```python
# Deep research mode (comprehensive)
result = run_research(
    candidate_name="Jonathan Carr",
    current_title="CFO",
    current_company="Armis",
    linkedin_url="https://linkedin.com/in/jonathan-carr",
    use_deep_research=True
)
assert result.research_confidence in ["High", "Medium", "Low"]
assert len(result.citations) >= 3

# Fast mode (quick turnaround)
result = run_research(
    candidate_name="Jane Doe",
    current_title="CTO",
    current_company="Acme Corp",
    use_deep_research=False
)
assert result.research_model == "gpt-5+web_search"
```

### Assessment Agent Interface

**Purpose:** Evaluate candidate against role specification using provided research.

**Signature:**
```python
from models.assessment import AssessmentResult
from models.research import ExecutiveResearchResult

def assess_candidate(
    research: ExecutiveResearchResult,
    role_spec_markdown: str,
    custom_instructions: str = ""
) -> AssessmentResult:
    """Evaluate candidate against role spec with evidence-aware scoring.

    Args:
        research: Structured research result (original or merged)
        role_spec_markdown: Full role specification in markdown format
        custom_instructions: Additional evaluation guidance (optional)

    Returns:
        AssessmentResult with dimension scores, overall score, reasoning

    Notes:
        - Dimension scores use 1-5 scale with None for Unknown
        - Overall score calculated in Python (not by LLM)
        - Uses gpt-5-mini with optional web_search for verification
    """
    pass
```

### Quality Check Interface

**Purpose:** Evaluate research sufficiency and determine if supplemental search is needed.

**Signature:**
```python
from typing import TypedDict
from agno.workflow import StepInput, StepOutput

class QualityMetrics(TypedDict):
    """Research quality assessment metrics."""
    has_enough_experiences: bool
    has_enough_expertise: bool
    has_enough_citations: bool
    confidence_acceptable: bool
    few_gaps: bool
    quality_score: int

class QualityCheckResult(TypedDict):
    """Quality check output with sufficiency determination."""
    research: ExecutiveResearchResult
    is_sufficient: bool
    gaps_to_fill: list[str]
    quality_score: int
    criteria_met: QualityMetrics

def check_research_quality(step_input: StepInput) -> StepOutput:
    """Evaluate if research is sufficient for assessment.

    Sufficiency Criteria:
    - ≥3 key experiences captured
    - ≥2 domain expertise areas identified
    - ≥3 distinct citations
    - Research confidence is High or Medium
    - ≤2 information gaps remain

    Args:
        step_input: Agno StepInput containing previous step content

    Returns:
        StepOutput with enriched research + is_sufficient flag
        success=True if sufficient (skip supplemental search)
        success=False if insufficient (trigger supplemental search)
    """
    pass
```

### Score Calculation Interface

**Purpose:** Calculate overall score from dimension scores using evidence-aware weighting.

**Signature:**
```python
from typing import Optional
from models.assessment import DimensionScore

def calculate_overall_score(
    dimension_scores: list[DimensionScore],
    spec_weights: dict[str, float]
) -> Optional[float]:
    """Calculate weighted overall score (0-100 scale) from dimension scores.

    Evidence-Aware Algorithm:
    1. Filter to scored dimensions (score is not None)
    2. If fewer than 2 dimensions scored, return None
    3. Restrict and renormalize weights to scored dimensions only
    4. Compute weighted average on 1-5 scale
    5. Optionally boost High evidence dimensions
    6. Scale to 0-100 and round to 1 decimal

    Args:
        dimension_scores: List of DimensionScore objects from assessment
        spec_weights: Human-designed weights from role spec (dimension -> weight)

    Returns:
        Overall score (0-100) or None if insufficient scoreable dimensions

    Example:
        >>> scores = [
        ...     DimensionScore(dimension="Fundraising", score=4, weight=0.25, ...),
        ...     DimensionScore(dimension="Operations", score=3, weight=0.20, ...),
        ...     DimensionScore(dimension="Strategy", score=None, weight=0.15, ...),
        ... ]
        >>> weights = {"Fundraising": 0.25, "Operations": 0.20, "Strategy": 0.15, ...}
        >>> calculate_overall_score(scores, weights)
        73.3  # Only Fundraising and Operations scored
    """
    pass
```

### Airtable Integration Interface

**Purpose:** Read and write data to Airtable database.

**Signature:**
```python
from typing import Optional, Any

class AirtableClient:
    """Client for Airtable API operations using pyairtable."""

    def __init__(self, api_key: str, base_id: str):
        """Initialize Airtable client.

        Args:
            api_key: Airtable personal access token
            base_id: Airtable base identifier
        """
        pass

    def get_screen(self, screen_id: str) -> dict[str, Any]:
        """Fetch Screen record with linked relationships.

        Args:
            screen_id: Airtable record ID

        Returns:
            Screen record with search, candidates, status fields
        """
        pass

    def get_role_spec(self, spec_id: str) -> dict[str, Any]:
        """Fetch Role Spec with markdown content.

        Args:
            spec_id: Airtable record ID

        Returns:
            Role spec record with structured_spec_markdown
        """
        pass

    def create_workflow_record(
        self,
        screen_id: str,
        candidate_id: str,
        status: str = "Queued"
    ) -> str:
        """Create workflow audit trail record.

        Args:
            screen_id: Parent screen record ID
            candidate_id: Candidate being evaluated
            status: Initial workflow status

        Returns:
            Created workflow record ID
        """
        pass

    def write_assessment(
        self,
        workflow_id: str,
        assessment: AssessmentResult,
        role_id: str,
        spec_id: str
    ) -> str:
        """Write assessment results to Airtable.

        Args:
            workflow_id: Parent workflow record ID
            assessment: Assessment result from agent
            role_id: Role being evaluated for
            spec_id: Spec used for evaluation

        Returns:
            Created assessment record ID
        """
        pass
```

---

## Data Models

All data models use Pydantic for validation and structured outputs. Complete definitions are in `demo_planning/data_design.md`.

### Entity: ExecutiveResearchResult

```python
from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime

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
    """Structured research output from parser agent.

    This model is produced by a parser agent (gpt-5-mini or gpt-5) that
    processes Deep Research markdown + citations or fast web-search results
    into a structured format for downstream assessment.
    """
    exec_name: str
    current_role: str
    current_company: str

    # Career & Experience
    career_timeline: list[CareerEntry] = Field(default_factory=list)
    total_years_experience: Optional[int] = None

    # Dimension-Aligned Fields (CFO)
    fundraising_experience: Optional[str] = None
    operational_finance_experience: Optional[str] = None

    # Dimension-Aligned Fields (CTO)
    technical_leadership_experience: Optional[str] = None

    # Universal Fields
    team_building_experience: Optional[str] = None
    sector_expertise: list[str] = Field(default_factory=list)
    stage_exposure: list[str] = Field(default_factory=list)

    # Summary & Evidence
    research_summary: str
    key_achievements: list[str] = Field(default_factory=list)
    notable_companies: list[str] = Field(default_factory=list)
    citations: list[Citation] = Field(default_factory=list)

    # Quality Metadata
    research_confidence: Literal["High", "Medium", "Low"] = "Medium"
    gaps: list[str] = Field(default_factory=list)

    # Audit Metadata
    research_timestamp: datetime = Field(default_factory=datetime.now)
    research_model: str = "o4-mini-deep-research"
```

**Fields:**
- `exec_name`: Full name
- `current_role`: Current job title
- `current_company`: Current company
- `career_timeline`: Structured work history
- `total_years_experience`: Total career years
- `fundraising_experience`: CFO dimension (nullable)
- `operational_finance_experience`: CFO dimension (nullable)
- `technical_leadership_experience`: CTO dimension (nullable)
- `team_building_experience`: Universal leadership dimension
- `sector_expertise`: List of industry sectors (e.g., ["B2B SaaS", "Fintech"])
- `stage_exposure`: Company stages (e.g., ["Series A", "Series B", "Growth"])
- `research_summary`: 2-3 sentence executive summary
- `key_achievements`: Notable accomplishments with evidence
- `notable_companies`: Recognized companies worked at
- `citations`: Source citations with URLs and quotes
- `research_confidence`: Overall confidence (High/Medium/Low)
- `gaps`: Information not found or unclear
- `research_timestamp`: When research was conducted
- `research_model`: Model used (e.g., "o4-mini-deep-research", "gpt-5+web_search")

**Constraints:**
- `exec_name` must be non-empty
- `research_confidence` must be one of: High, Medium, Low
- `citations` should have ≥3 entries for High confidence
- `gaps` should be ≤2 entries for High confidence

### Entity: AssessmentResult

```python
from pydantic import BaseModel, Field
from typing import Optional, Literal

class DimensionScore(BaseModel):
    """Evidence-aware dimension score.

    Uses Optional[int] with None to represent Unknown/Insufficient Evidence.
    DO NOT use NaN, 0, or empty values - use None exclusively.
    """
    dimension: str
    score: Optional[int] = Field(None, ge=1, le=5)
    evidence_level: Literal["High", "Medium", "Low"]
    confidence: Literal["High", "Medium", "Low"]
    reasoning: str
    evidence_quotes: list[str] = Field(default_factory=list)
    citation_urls: list[str] = Field(default_factory=list)

class MustHaveCheck(BaseModel):
    """Must-have requirement evaluation."""
    requirement: str
    met: bool
    evidence: Optional[str] = None

class AssessmentResult(BaseModel):
    """Structured assessment from gpt-5-mini agent."""

    # Overall Assessment
    overall_score: Optional[float] = Field(None, ge=0, le=100)
    overall_confidence: Literal["High", "Medium", "Low"]

    # Dimension-Level Scores
    dimension_scores: list[DimensionScore]

    # Requirements Checking
    must_haves_check: list[MustHaveCheck] = Field(default_factory=list)
    red_flags_detected: list[str] = Field(default_factory=list)
    green_flags: list[str] = Field(default_factory=list)

    # Qualitative Assessment
    summary: str
    counterfactuals: list[str] = Field(default_factory=list)

    # Audit Metadata
    assessment_timestamp: datetime = Field(default_factory=datetime.now)
    assessment_model: str = "gpt-5-mini"
    role_spec_used: Optional[str] = None
```

**Fields:**
- `overall_score`: 0-100 scale (nullable, computed in Python)
- `overall_confidence`: Combined confidence level
- `dimension_scores`: List of DimensionScore objects (4-6 dimensions)
- `must_haves_check`: Boolean checks for hard requirements
- `red_flags_detected`: Disqualifying factors found
- `green_flags`: Positive signals worth highlighting
- `summary`: 2-3 sentence topline assessment
- `counterfactuals`: Critical assumptions that must be true
- `assessment_timestamp`: When assessment ran
- `assessment_model`: Model used (e.g., "gpt-5-mini")
- `role_spec_used`: Spec identifier for audit trail

**Constraints:**
- `overall_score` is nullable (None if <2 dimensions scored)
- `dimension_scores.score` uses None for Unknown (not 0, NaN, or empty)
- `summary` should be 2-3 sentences

### Entity: WorkflowEvent

```python
from pydantic import BaseModel
from typing import Literal, Optional, Any
from datetime import datetime

class WorkflowEvent(BaseModel):
    """Single event in workflow execution audit trail."""
    timestamp: datetime
    event: Literal[
        "workflow_started",
        "workflow_completed",
        "step_started",
        "step_completed",
        "tool_call_started",
        "tool_call_completed",
        "condition_execution_started",
        "condition_execution_completed",
        "loop_iteration_started",
        "loop_iteration_completed",
    ]
    step_name: Optional[str] = None
    message: str
    metadata: Optional[dict[str, Any]] = None
```

**Fields:**
- `timestamp`: Event timestamp
- `event`: Event type from Agno workflow
- `step_name`: Step identifier (if applicable)
- `message`: Human-readable event description
- `metadata`: Additional context (tool args, results, etc.)

---

## Non-Functional Requirements

### Performance

- **Research Phase:**
  - Deep Research mode: 2-5 minutes per candidate
  - Fast mode: 30-60 seconds per candidate
  - Quality check: <1 second
  - Supplemental search iteration: 30-60 seconds
- **Assessment Phase:**
  - Assessment agent: 30-60 seconds per candidate
- **Full Workflow:** <10 minutes per candidate (including LLM API calls)
- **Memory Usage:** <512MB per Flask worker
- **Database Writes:** <5 seconds per Airtable operation

### Scalability

**For Demo (v1.0):**
- **Concurrency:** Synchronous execution (one candidate at a time)
- **Throughput:** 1 screen request per Flask worker
- **Workers:** Single Flask process sufficient for demo

**For Production (v2.0+):**
- **Horizontal Scaling:** Multiple Flask workers (3-5 per server)
- **Async Processing:** asyncio.gather() for concurrent candidate screening
- **Queue-Based:** Celery/RQ for long-running workflows
- **Caching:** Research result caching by candidate ID

### Security

- **API Keys:** Environment variables only (never in code)
- **Input Validation:** Pydantic models for all webhook inputs
- **Secrets Management:**
  - `.env` file for local development
  - `.env` in `.gitignore`
  - No secrets in Airtable automations
- **No SQL Injection Risk:** Using Airtable API and SQLite (workflow events only)

### Reliability

- **Uptime:** Not applicable (local demo server)
- **Error Handling:**
  - Agent-level retries: exponential_backoff=True, retries=2
  - Workflow failures: Mark Workflow record as "Failed" with error message
  - Graceful degradation: Continue processing other candidates if one fails
- **Recovery:** Manual restart of Flask server if needed
- **Monitoring:** Terminal logs with emoji indicators (🔍, ✅, ❌)

### Testing

- **Unit Tests:** pytest (50%+ coverage target)
- **Coverage Scope:** Core matching logic, scoring, quality checks
- **Integration Tests:** End-to-end workflow execution with mock data
- **Type Checking:** mypy (standard mode, not strict)
- **Formatting:** ruff format (black-compatible)
- **Linting:** ruff check

### Deployment

- **Environment:** Local development (Mac/Linux)
- **Server:** Flask on localhost:5000
- **Tunnel:** ngrok for webhook connectivity
- **Configuration:** Environment variables via `.env` file
- **Dependencies:** uv for package management
- **Database:** Airtable (primary), SQLite (workflow events)

---

## Dependencies

### Core Dependencies

```toml
[project]
name = "talent-signal-agent"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "agno-ai>=0.1.0",           # Agent framework
    "pydantic>=2.5.0",          # Data validation
    "flask>=3.0.0",             # Webhook server
    "pyairtable>=2.0.0",        # Airtable API client
    "python-dotenv>=1.0.0",     # Environment variables
]
```

### Development Dependencies

```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",            # Testing framework
    "pytest-cov>=4.1.0",        # Coverage reporting
    "ruff>=0.1.0",              # Formatting + linting
    "mypy>=1.7.0",              # Type checking
]
```

### Optional Dependencies

```toml
[project.optional-dependencies]
observability = [
    "structlog>=23.1.0",        # Structured logging (if time permits)
]
```

---

## API Specification

### Flask Webhook Endpoints

#### POST /screen

**Purpose:** Execute candidate screening workflow for a batch of candidates.

**Trigger:** Airtable automation when Screen.status changes to "Ready to Screen"

**Request:**
```json
{
    "screen_id": "recABC123"
}
```

**Request Headers:**
```
Content-Type: application/json
```

**Response (200 - Success):**
```json
{
    "status": "success",
    "screen_id": "recABC123",
    "candidates_processed": 3,
    "execution_time_seconds": 342.5,
    "results": [
        {
            "candidate_id": "recXYZ1",
            "workflow_id": "recWF1",
            "overall_score": 78.0,
            "confidence": "High"
        },
        {
            "candidate_id": "recXYZ2",
            "workflow_id": "recWF2",
            "overall_score": 65.3,
            "confidence": "Medium"
        }
    ]
}
```

**Response (200 - Partial Failure):**
```json
{
    "status": "partial",
    "screen_id": "recABC123",
    "candidates_processed": 2,
    "candidates_failed": 1,
    "results": [...],
    "errors": [
        {
            "candidate_id": "recXYZ3",
            "error": "Research agent failed after 2 retries",
            "workflow_id": "recWF3"
        }
    ]
}
```

**Response (400 - Bad Request):**
```json
{
    "error": "ValidationError",
    "message": "Invalid request payload",
    "details": {
        "field": "screen_id",
        "constraint": "must be valid Airtable record ID"
    }
}
```

**Response (500 - Server Error):**
```json
{
    "error": "InternalError",
    "message": "Workflow execution failed",
    "details": {
        "screen_id": "recABC123",
        "error": "Airtable API connection timeout"
    }
}
```

**Implementation:**
```python
@app.route('/screen', methods=['POST'])
def run_screening():
    """Execute screening workflow for all candidates in a screen."""
    try:
        # Validate request
        data = request.json
        screen_id = data.get('screen_id')
        if not screen_id:
            return {"error": "screen_id required"}, 400

        # Update screen status to Processing
        airtable.update_screen(screen_id, status="Processing")

        # Get screen details
        screen = airtable.get_screen(screen_id)
        candidates = airtable.get_linked_candidates(screen)
        role_spec = airtable.get_role_spec(screen['role_spec_id'])

        # Process candidates (synchronous for demo)
        results = []
        errors = []

        for candidate in candidates:
            try:
                result = screen_single_candidate(
                    candidate=candidate,
                    role_spec=role_spec,
                    screen_id=screen_id
                )
                results.append(result)
            except Exception as e:
                errors.append({
                    "candidate_id": candidate['id'],
                    "error": str(e)
                })

        # Update screen status
        final_status = "Complete" if not errors else "Partial"
        airtable.update_screen(screen_id, status=final_status)

        return {
            "status": "success" if not errors else "partial",
            "screen_id": screen_id,
            "candidates_processed": len(results),
            "candidates_failed": len(errors),
            "results": results,
            "errors": errors
        }

    except Exception as e:
        logger.error("screening_failed", screen_id=screen_id, error=str(e))
        airtable.update_screen(screen_id, status="Failed", error=str(e))
        return {"error": str(e)}, 500
```

---

## Configuration

### Environment Variables

```bash
# Application
APP_NAME=talent-signal-agent
APP_ENV=development
DEBUG=true
LOG_LEVEL=INFO

# OpenAI
OPENAI_API_KEY=sk-...
USE_DEEP_RESEARCH=true  # Toggle research mode (true=deep, false=fast)

# Airtable
AIRTABLE_API_KEY=pat...
AIRTABLE_BASE_ID=app...

# Flask
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
FLASK_DEBUG=true

# Workflow
MIN_EXPERIENCES=3
MIN_EXPERTISE=2
MIN_CITATIONS=3
MAX_GAPS=2
MAX_SUPPLEMENTAL_ITERATIONS=3

# SQLite (workflow events)
WORKFLOW_DB_PATH=tmp/screening_workflows.db
```

### Configuration Files

- `pyproject.toml`: Package metadata and dependencies
- `.python-version`: Python version (3.11)
- `.env`: Environment variables (local dev, not committed)
- `.env.example`: Template for environment variables
- `ruff.toml`: Linter configuration (if needed)
- `mypy.ini`: Type checker configuration (if needed)

---

## Error Handling

### Error Hierarchy

```python
class TalentSignalError(Exception):
    """Base exception for Talent Signal Agent."""
    pass

class AirtableError(TalentSignalError):
    """Airtable API operation failed."""
    pass

class ResearchError(TalentSignalError):
    """Research agent execution failed."""
    pass

class AssessmentError(TalentSignalError):
    """Assessment agent execution failed."""
    pass

class WorkflowError(TalentSignalError):
    """Workflow execution failed."""
    pass

class ValidationError(TalentSignalError):
    """Input validation failed."""
    pass
```

### Error Response Format

```json
{
    "error": "ResearchError",
    "message": "Deep Research API failed after 2 retries",
    "details": {
        "candidate_id": "recXYZ",
        "research_model": "o4-mini-deep-research",
        "attempts": 2,
        "last_error": "Rate limit exceeded"
    },
    "workflow_id": "recWF123",
    "timestamp": "2025-01-16T10:30:00Z"
}
```

### Error Handling Strategy

**Agent-Level (Agno built-in):**
```python
agent = Agent(
    model=OpenAIResponses(id="o4-mini-deep-research"),
    exponential_backoff=True,  # Auto-retry with backoff
    retries=2,                  # Max 2 retry attempts
    retry_delay=1,              # Initial delay in seconds
)
```

**Workflow-Level (Custom):**
```python
try:
    result = await workflow.arun(input=prompt)
except Exception as e:
    logger.error("workflow_failed", error=str(e))
    airtable.update_workflow(workflow_id, status="Failed", error=str(e))
    raise WorkflowError(f"Workflow execution failed: {e}")
```

**Graceful Degradation:**
- If one candidate fails, continue processing others
- Mark failed workflows individually
- Return partial results with error details
- Update Screen status to "Partial" if any candidates failed

---

## Observability

### Logging

**Setup (using standard logging for demo):**
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
```

**Usage:**
```python
logger.info(f"🔍 Starting research for {candidate.name}")
logger.info(f"✅ Research complete - {len(citations)} citations found")
logger.error(f"❌ Assessment failed: {error}")
```

**Optional: Structured Logging (if time permits):**
```python
import structlog

logger = structlog.get_logger()
logger.info("research_started", candidate_id="recXYZ", mode="deep_research")
logger.info("research_completed", candidate_id="recXYZ", citations=12, confidence="High")
```

### Metrics (Terminal Output)

- Workflow execution time (per candidate)
- Supplemental search trigger rate
- Quality check pass/fail rate
- Overall score distribution
- Token usage (from OpenAI API responses)

### Audit Trail

**Storage:** SQLite database (`tmp/screening_workflows.db`)

**Captured Events:**
- All Agno workflow events (via `store_events=True`)
- Step execution timestamps and durations
- Tool calls (web searches, API calls)
- Condition evaluations (quality gate, loop end condition)
- Loop iterations (supplemental search)

**Access:**
```python
workflow_run = await workflow.arun(input=prompt)
events = workflow_run.events  # List of WorkflowEvent objects

# Store in Airtable for persistence
airtable.update_workflow(
    workflow_id=workflow_id,
    execution_log=json.dumps([e.dict() for e in events])
)
```

---

## Workflow Specification Reference

Complete workflow implementation details are in `demo_planning/screening_workflow_spec.md`.

**Key Components:**
- Step 1: Deep Research Agent (o4-mini-deep-research or gpt-5 + web_search)
- Step 2: Quality Check (custom function, sufficiency criteria)
- Step 3: Conditional Supplemental Search (gpt-5 + web_search, max 3 iterations)
- Step 4: Assessment Agent (gpt-5-mini with role spec)

**Execution Modes:**
- Synchronous (demo v1.0): Process candidates sequentially
- Async (future v2.0): Process candidates concurrently with asyncio.gather()

**Event Streaming:**
- All workflow steps captured with `stream=True, stream_events=True`
- Events logged to terminal and stored in SQLite
- Full audit trail for transparency and debugging

---

## Airtable Schema Reference

Complete Airtable schema is in `demo_planning/airtable_schema.md`.

**Key Tables:**
- **People (64 records):** Executive candidates from guildmember_scrape.csv
- **Portcos (4 records):** Portfolio companies (Pigment, Mockingbird, Synthesia, Estuary)
- **Portco_Roles (4 records):** Open roles at portfolio companies
- **Role_Specs (6 records):** 2 templates + 4 customized specs
- **Searches (4 records):** Active talent searches linking roles to specs
- **Screens (4 records):** Screening batches (3 pre-run + 1 live demo)
- **Workflows (~12-15 records):** Execution audit trail (one per candidate-screen pair)
- **Research_Results (~12-15 records):** Structured research outputs
- **Assessments (~12-15 records):** Assessment results with dimension scores

**Webhook Trigger:**
- Table: Screens
- Trigger Field: `status`
- Trigger Value: "Ready to Screen" (change from "Draft")
- Action: POST to Flask `/screen` endpoint with `screen_id`

---

## Implementation Checklist

### Phase 1: Setup (4 hours)
- [x] Create project structure
- [x] Set up Python environment (uv, .python-version)
- [ ] Install dependencies (pyproject.toml)
- [ ] Configure environment variables (.env)
- [ ] Create Pydantic models (models/)
- [ ] Validate against data_design.md schemas

### Phase 2: Agent Implementation (8 hours)
- [ ] Implement research agent (agents/research_agent.py)
  - [ ] Deep Research mode (o4-mini-deep-research)
  - [ ] Fast mode (gpt-5 + web_search)
  - [ ] Environment toggle (USE_DEEP_RESEARCH)
- [ ] Implement assessment agent (agents/assessment_agent.py)
  - [ ] Spec-guided evaluation
  - [ ] Evidence-aware scoring (None for Unknown)
  - [ ] Web search capability for verification
- [ ] Implement web search agent (agents/web_search_agent.py)
  - [ ] Supplemental search for gaps
  - [ ] Targeted query generation

### Phase 3: Workflow Implementation (6 hours)
- [ ] Create workflow definition (workflows/screening_workflow.py)
  - [ ] Step 1: Deep Research
  - [ ] Step 2: Quality Check (custom function)
  - [ ] Step 3: Conditional Supplemental Search (with loop)
  - [ ] Step 4: Assessment
- [ ] Implement custom workflow functions (workflows/workflow_functions.py)
  - [ ] check_research_quality()
  - [ ] coordinate_supplemental_search()
  - [ ] search_complete() (loop end condition)
  - [ ] merge_research()
- [ ] Test workflow end-to-end with mock data

### Phase 4: Integrations (6 hours)
- [ ] Implement Airtable client (integrations/airtable_client.py)
  - [ ] Read operations (get_screen, get_role_spec, etc.)
  - [ ] Write operations (create_workflow, write_assessment, etc.)
  - [ ] Status updates (update_screen_status)
- [ ] Implement Flask webhook server (webhook_server.py)
  - [ ] /screen endpoint
  - [ ] Request validation
  - [ ] Error handling
- [ ] Set up ngrok tunnel

### Phase 5: Utilities (2 hours)
- [ ] Implement scoring utilities (utils/scoring.py)
  - [ ] calculate_overall_score() with evidence-aware weighting
- [ ] Implement spec parser (utils/spec_parser.py)
  - [ ] Parse markdown role specs
  - [ ] Extract dimensions, weights, evidence levels
- [ ] Set up logging (utils/logger.py)

### Phase 6: Testing (4 hours)
- [ ] Unit tests for core logic
  - [ ] Quality check logic
  - [ ] Score calculation
  - [ ] Spec parsing
- [ ] Integration tests
  - [ ] End-to-end workflow execution
  - [ ] Airtable read/write operations
- [ ] Achieve 50%+ coverage on core logic

### Phase 7: Demo Preparation (4 hours)
- [ ] Pre-run 3 scenarios (Pigment CFO, Mockingbird CFO, Synthesia CTO)
- [ ] Verify results in Airtable
- [ ] Prepare Estuary CTO for live demo
- [ ] Test webhook trigger automation
- [ ] Create demo script with timing estimates

**Total Estimated Time:** 34 hours (includes buffer)

---

## Success Criteria

This specification succeeds if:

1. ✅ **Working Prototype:** Demonstrates end-to-end candidate screening
2. ✅ **Evidence-Aware Scoring:** Handles Unknown dimensions with None/null (not 0 or NaN)
3. ✅ **Quality-Gated Research:** Conditional supplemental search works correctly
4. ✅ **Type Safety:** All public functions have type hints, mypy passes
5. ✅ **Test Coverage:** Core logic achieves 50%+ coverage
6. ✅ **Audit Trail:** Full event logging captured and stored
7. ✅ **Demo Ready:** 3 pre-run scenarios complete, 1 ready for live execution
8. ✅ **Clear Documentation:** This spec + README explain implementation

**Remember:** The goal is demonstrating quality of thinking through minimal, working code—not building production infrastructure.

---

## Document Control

**Related Documents:**
- `spec/constitution.md` - Project governance and principles
- `spec/prd.md` - Product requirements document
- `case/technical_spec_V2.md` - Detailed technical architecture
- `demo_planning/data_design.md` - Data models and schemas
- `demo_planning/screening_workflow_spec.md` - Workflow implementation details
- `demo_planning/airtable_schema.md` - Airtable database schema
- `demo_planning/role_spec_design.md` - Role specification framework

**Approval:**
- Created: 2025-01-16
- Status: Ready for Implementation
- Next Review: Post-implementation retrospective
