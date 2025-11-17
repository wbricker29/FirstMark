---
version: "1.0-minimal"
created: "2025-01-16"
updated: "2025-01-17"
project: "Talent Signal Agent"
context: "FirstMark Capital AI Lead Case Study"
---

# Technical Specification: Talent Signal Agent (v1.0-Minimal)

Engineering contract for Python implementation of AI-powered executive matching system

## Architecture

### System Overview

The Talent Signal Agent is a demo-quality Python application that uses AI agents to research and evaluate executive candidates against role specifications. The system integrates with Airtable for data storage and UI, uses OpenAI's Deep Research API for candidate research, and employs structured LLM outputs for evidence-aware assessments.

**Key Design Principles:**

- **Evidence-Aware Scoring:** Explicit handling of "Unknown" when public data is insufficient (using `None`/`null`, not 0 or NaN)
- **Quality-Gated Research:** Optional single incremental search agent step when initial research has quality issues
- **Minimal Audit Trail:** Airtable fields + terminal logs (no separate event DB for v1)
- **Deep Research Primary:** v1 uses o4-mini-deep-research as default; fast mode is Phase 2+

### Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      AIRTABLE DATABASE                       │
│  People (64) | Portco (4) | Portco_Roles (4) | Role_Specs (6)│
│  Searches (4) | Screens (4) | Assessments (research+scores)│
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
    │    └─ o4-mini-deep-research  │
    │                              │
    │  Step 2: Quality Check       │
    │    └─ Simple sufficiency     │
    │                              │
    │  Step 3: Conditional Branch  │
    │    ├─ Incremental Search     │
    │    │   (optional, single)    │
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
    │  - Research        │
    │  - Assessments     │
    │  - Status fields   │
    └────────────────────┘

    ┌────────────────────┐
    │  OPENAI APIS       │
    │                    │
    │  - Deep Research   │
    │  - GPT-5-mini      │
    │  - Web Search      │
    └────────────────────┘
```

### Technology Stack

- **Language:** Python 3.11+
- **Framework:** Flask (webhook server), Agno (agent orchestration)
- **LLM Provider:** OpenAI (o4-mini-deep-research, gpt-5-mini)
- **Database:** Airtable (primary storage), Agno SqliteDb for session state (tmp/agno_sessions.db, no custom event tables)
- **Validation:** Pydantic (structured outputs)
- **Package Manager:** UV
- **Tunnel:** ngrok (local demo)

### Project Structure

**v1.0-Minimal Layout (5 files):**

```
demo/
├── app.py              # Flask app + webhook entrypoints
├── agents.py           # research + assessment agent creation + runners
├── models.py           # Pydantic models (research + assessment)
├── airtable_client.py  # Thin Airtable wrapper
└── settings.py         # Config/env loading (optional)

tmp/
└── agno_sessions.db    # Agno workflow session state (gitignored, SqliteDb only)

tests/
├── test_scoring.py         # calculate_overall_score tests
├── test_quality_check.py   # quality check heuristics
└── test_workflow_smoke.py  # happy-path /screen flow with mocks (optional)

spec/                   # Documentation
├── constitution.md     # Project governance
├── prd.md              # Product requirements
├── spec.md             # This file
└── v1_minimal_spec.md  # Minimal scope definition

.python-version         # Python 3.11
pyproject.toml          # Dependencies
.env.example            # Environment variables template
README.md               # Implementation guide
```

**Phase 2+ Enhancements:**

- Further decomposition into subpackages (`agents/`, `models/`, `workflows/`)
- CLI interface
- SQLite workflow event storage
- Async orchestration
- Production deployment configuration

---

## Interfaces

### Research Agent Interface

**Purpose:** Conduct comprehensive executive research using OpenAI Deep Research.

**⚠️ IMPORTANT - Deep Research API Limitations:**

- **Deep Research models (o4-mini-deep-research) do NOT support structured outputs (`output_schema`)**
- Returns markdown text via `result.content` (not Pydantic model)
- Citations available via `result.citations` (built-in API feature)
- See `spec/dev_reference/implementation_guide.md` Section 2 for complete Deep Research patterns

**Signature:**

```python
from pathlib import Path
from typing import Optional
from agno import Agent, OpenAIResponses
from models import ExecutiveResearchResult

def create_research_agent(use_deep_research: bool = True) -> Agent:
    """Create research agent with flexible execution mode.

    Args:
        use_deep_research: If True, use o4-mini-deep-research.
                          For v1.0-minimal, only True is required.
                          False (fast mode) is Phase 2+.

    Returns:
        Configured Agno Agent instance.

    Notes:
        - v1 implementation only requires use_deep_research=True
        - Fast mode (gpt-5 + web_search) is future enhancement
        - Deep Research returns markdown (NOT structured output)
        - DO NOT use output_schema with Deep Research models
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
        use_deep_research: Toggle between deep and fast modes (v1: True only)

    Returns:
        ExecutiveResearchResult with career timeline, expertise, citations

    Raises:
        RuntimeError: If research agent execution fails after retries

    Notes:
        - Uses Agno's built-in retry with exponential_backoff=True
        - Deep Research returns markdown via result.content (NOT structured output)
        - Citations extracted from result.citations (built-in API feature)
        - No separate parser agent needed
    """
    pass
```

**Examples:**

```python
# Deep research mode (v1.0-minimal required path)
result = run_research(
    candidate_name="Jonathan Carr",
    current_title="CFO",
    current_company="Armis",
    linkedin_url="https://linkedin.com/in/jonathan-carr",
    use_deep_research=True
)
assert result.research_confidence in ["High", "Medium", "Low"]
assert len(result.citations) >= 3
```

### Assessment Agent Interface

**Purpose:** Evaluate candidate against role specification using provided research.

**Signature:**

```python
from models import AssessmentResult, ExecutiveResearchResult

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
        - Overall score calculated in Python using simple average algorithm
        - Uses gpt-5-mini with Agno's native structured outputs
        - No separate parser needed
    """
    pass
```

### Quality Check Interface

**Purpose:** Evaluate research sufficiency and determine if incremental search is needed.

**Signature:**

```python
from models import ExecutiveResearchResult

def check_research_quality(research: ExecutiveResearchResult) -> bool:
    """Evaluate if research is sufficient for assessment.

    Simple Sufficiency Criteria (v1.0-minimal):
    - ≥3 citations
    - Non-empty research summary

    Args:
        research: ExecutiveResearchResult to evaluate

    Returns:
        True if sufficient (skip incremental search)
        False if insufficient (trigger single incremental search agent step)

    Notes:
        - v1 uses minimal criteria
        - Phase 2+ can add: experience count, expertise areas, confidence level
        - This is a pure function, no complex workflow types needed
    """
    pass
```

### Score Calculation Interface

**Purpose:** Calculate overall score from dimension scores using simple average.

**Signature:**

```python
from typing import Optional
from models import DimensionScore

def calculate_overall_score(dimension_scores: list[DimensionScore]) -> Optional[float]:
    """Calculate simple average score from dimensions with scores.

    Simple Average Algorithm (v1.0-minimal):
    1. Filter to scored dimensions (score is not None)
    2. If no dimensions scored, return None
    3. Compute average on 1-5 scale
    4. Scale to 0-100 (multiply by 20)

    Args:
        dimension_scores: List of DimensionScore objects from assessment

    Returns:
        Overall score (0-100) or None if no dimensions scored

    Example:
        >>> scores = [
        ...     DimensionScore(dimension="Fundraising", score=4, ...),
        ...     DimensionScore(dimension="Operations", score=3, ...),
        ...     DimensionScore(dimension="Strategy", score=None, ...),  # Unknown
        ... ]
        >>> calculate_overall_score(scores)
        70.0  # (4 + 3) / 2 * 20

    Notes:
        - v1 uses simple average (no weights)
        - Spec-defined weights remain in AssessmentResult for reference
        - Phase 2+ can implement weighted algorithm if needed
        - Demonstrates evidence-aware concept without complexity
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

    def write_assessment(
        self,
        screen_id: str,
        candidate_id: str,
        assessment: AssessmentResult,
        research: Optional[ExecutiveResearchResult] = None
    ) -> str:
        """Write assessment results to Airtable.

        Args:
            screen_id: Parent screen record ID
            candidate_id: Candidate being evaluated
            assessment: Assessment result from agent
            research: Optional research result for audit trail

        Returns:
            Created assessment record ID

        Notes:
            - Writes assessment JSON
            - Writes key summary fields (overall_score, confidence, summary)
            - Optionally writes research JSON if provided
            - Updates status field on success/failure
        """
        pass

    def update_screen_status(
        self,
        screen_id: str,
        status: str,
        error_message: Optional[str] = None
    ) -> None:
        """Update screen status field.

        Args:
            screen_id: Screen record ID
            status: New status (e.g., "Processing", "Complete", "Failed")
            error_message: Optional error message if status is "Failed"
        """
        pass
```

---

## Data Models

**All Pydantic models are defined in `spec/dev_reference/implementation_guide.md` (canonical source).**

### Key Models

**ExecutiveResearchResult** - Structured research output from Deep Research agent

- **Note:** Deep Research returns markdown (not structured output); must parse manually or use incremental search agent
- Contains career timeline, expertise areas, citations, confidence metadata
- Citations extracted from `result.citations` (built-in Deep Research API feature)
- See `spec/dev_reference/implementation_guide.md` lines 113-162 for complete definition and Deep Research patterns

**AssessmentResult** - Structured assessment from evaluation agent

- Evidence-aware dimension scores (1-5 scale with `None` for Unknown)
- Overall score computed in Python from dimension scores
- Must-haves checks, red/green flags, counterfactuals
- See `spec/dev_reference/implementation_guide.md` lines 358-382 for complete definition

**DimensionScore** - Evidence-aware scoring for evaluation dimensions

- `score: Optional[int]` - Uses `None` (not 0, NaN, or empty) for Unknown/Insufficient Evidence
- Includes reasoning, evidence quotes, citation URLs
- See `spec/dev_reference/implementation_guide.md` lines 334-350 for complete definition

**Supporting Models:**

- `Citation` - Source citation with URL, title, snippet
- `CareerEntry` - Timeline entry for career history
- `MustHaveCheck` - Must-have requirement evaluation

**Important Design Patterns:**

- Evidence-aware scoring: Use `None`/`null` for unknown dimensions (never 0 or NaN)
- Overall score calculated in Python, not by LLM
- Type safety via Pydantic for all structured outputs

**For complete field definitions, constraints, and usage examples, see `spec/dev_reference/implementation_guide.md`.**

### Entity: WorkflowEvent (Phase 2+)

**Note:** WorkflowEvent entity and custom SQLite event tables are **Phase 2+ enhancements**, not required for v1.0-minimal.

For v1.0-minimal:

- Use Agno's `SqliteDb` at `tmp/agno_sessions.db` for workflow session state (Agno-managed tables only)
- Rely on Airtable fields for final results (status, error messages, assessment JSON)
- Use terminal logs (Python `logging` module) for execution visibility
- Enable Agno's event streaming for stdout logging (`stream_events=True`)
- No custom WorkflowEvent model or event logging tables

**Phase 2+ WorkflowEvent Model:**

```python
from pydantic import BaseModel
from typing import Literal, Optional, Any
from datetime import datetime

class WorkflowEvent(BaseModel):
    """Single event in workflow execution audit trail (Phase 2+)."""
    timestamp: datetime
    event: Literal[
        "workflow_started",
        "workflow_completed",
        "step_started",
        "step_completed",
        "tool_call_started",
        "tool_call_completed",
    ]
    step_name: Optional[str] = None
    message: str
    metadata: Optional[dict[str, Any]] = None
```

---

## Non-Functional Requirements

### Performance

- **Research Phase:**
  - Deep Research mode: 2-6 minutes per candidate
  - Quality check: <1 second
  - Optional incremental search: 30-60 seconds (single agent step, up to 2 web/search calls)
- **Assessment Phase:**
  - Assessment agent: 30-60 seconds per candidate
- **Full Workflow:** <10 minutes per candidate (including LLM API calls)
- **Memory Usage:** <512MB per Flask worker
- **Database Writes:** <5 seconds per Airtable operation

### Scalability

**For Demo (v1.0-minimal):**

- **Concurrency:** Synchronous execution (one candidate at a time)
- **Throughput:** 1 screen request per Flask worker
- **Workers:** Single Flask process sufficient for demo
- **Candidates:** Up to ~10 candidates per Screen

**For Production (Phase 2+):**

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
- **No SQL Injection Risk:** Using Airtable API (no SQL database in v1)

### Reliability

- **Uptime:** Not applicable (local demo server)
- **Error Handling:**
  - Agent-level retries: exponential_backoff=True, retries=2 (Agno built-in)
  - Workflow failures: Update Airtable status to "Failed" with error message
  - Graceful degradation: Continue processing other candidates if one fails
- **Recovery:** Manual restart of Flask server if needed
- **Monitoring:** Terminal logs with emoji indicators (🔍, ✅, ❌)

### Testing

**v1.0-minimal Testing Scope:**

- **Core Logic Tests:** Basic tests for scoring and quality check
- **Test Files:**
  - `test_scoring.py` - calculate_overall_score, etc.
  - `test_quality_check.py` - quality check heuristics
  - `test_workflow_smoke.py` - happy-path /screen flow with mocks (optional)
- **Coverage:** No strict percentage requirement; focus on correctness
- **Type Checking:** Type hints on public functions (mypy as goal, not gate)
- **Formatting:** ruff format (black-compatible)
- **Linting:** ruff check

**Phase 2+ Testing Enhancements:**

- 50%+ coverage target
- Comprehensive integration tests
- Strict mypy mode
- CI/CD pipeline

### Deployment

- **Environment:** Local development (Mac/Linux)
- **Server:** Flask on localhost:5000
- **Tunnel:** ngrok for webhook connectivity
- **Configuration:** Environment variables via `.env` file
- **Dependencies:** uv for package management
- **Database:** Airtable (primary storage), Agno SqliteDb at tmp/agno_sessions.db (session state only, no custom event tables)

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
    "ruff>=0.1.0",              # Formatting + linting
    "mypy>=1.7.0",              # Type checking (optional)
]
```

**Note:** `structlog` removed from dependencies for v1.0-minimal. Standard Python `logging` is sufficient.

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
            "overall_score": 78.0,
            "confidence": "High"
        },
        {
            "candidate_id": "recXYZ2",
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
            "error": "Research agent failed after 2 retries"
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
        airtable.update_screen_status(screen_id, status="Processing")

        # Get screen details
        screen = airtable.get_screen(screen_id)
        candidates = airtable.get_linked_candidates(screen)
        role_spec = airtable.get_role_spec(screen['role_spec_id'])

        # Process candidates (synchronous for v1)
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
                logger.error(f"❌ Candidate failed: {candidate['id']} - {e}")
                errors.append({
                    "candidate_id": candidate['id'],
                    "error": str(e)
                })

        # Update screen status
        final_status = "Complete" if not errors else "Partial"
        airtable.update_screen_status(screen_id, status=final_status)

        return {
            "status": "success" if not errors else "partial",
            "screen_id": screen_id,
            "candidates_processed": len(results),
            "candidates_failed": len(errors),
            "results": results,
            "errors": errors
        }

    except Exception as e:
        logger.error(f"❌ Screening failed: {screen_id} - {e}")
        airtable.update_screen_status(screen_id, status="Failed", error_message=str(e))
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
USE_DEEP_RESEARCH=true  # v1: always true; fast mode is Phase 2+

# Airtable
AIRTABLE_API_KEY=pat...
AIRTABLE_BASE_ID=app...

# Flask
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
FLASK_DEBUG=true

# Quality Check (v1 minimal)
MIN_CITATIONS=3
```

### Configuration Files

- `pyproject.toml`: Package metadata and dependencies
- `.python-version`: Python version (3.11)
- `.env`: Environment variables (local dev, not committed)
- `.env.example`: Template for environment variables

---

## Error Handling

### Error Handling Strategy

**v1.0-minimal Error Handling:**

For v1.0-minimal, use basic Python exceptions and error logging. No custom error hierarchy needed.

**Agent-Level (Agno built-in):**

```python
agent = Agent(
    model=OpenAIResponses(id="o4-mini-deep-research"),
    exponential_backoff=True,  # Auto-retry with backoff
    retries=2,                  # Max 2 retry attempts
    retry_delay=1,              # Initial delay in seconds
)
```

**Workflow-Level (Basic Exception Handling):**

```python
try:
    result = await workflow.arun(input=prompt)
except Exception as e:
    logger.error(f"❌ Workflow failed: {e}")
    airtable.update_screen_status(screen_id, status="Failed", error_message=str(e))
    raise
```

**Graceful Degradation:**

- If one candidate fails, continue processing others
- Update Airtable status individually per candidate
- Return partial results with error details
- Update Screen status to "Partial" if any candidates failed

**Phase 2+ Enhancements:**

- Custom error hierarchy (TalentSignalError, ResearchError, etc.)
- Structured error responses
- Error recovery strategies
- Detailed error metadata

---

## Observability

### Logging

**v1.0-minimal Logging (Python standard library):**

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

**Phase 2+ Enhancements:**

- Structured logging with `structlog`
- Log aggregation
- Metrics collection
- Rich event metadata

### Metrics (Terminal Output)

For v1.0-minimal, log key metrics to terminal:

- Workflow execution time (per candidate)
- Quality check pass/fail
- Overall score distribution
- Token usage (from OpenAI API responses)

### Audit Trail

**v1.0-minimal Audit Trail:**

- **Primary:** Airtable fields (status, error messages, assessment JSON, research JSON)
- **Secondary:** Terminal logs during execution
- **Agno Events:** Enable `stream_events=True` for stdout logging only (not persisted)

**Phase 2+ Enhancements:**

- SQLite database for workflow events (`tmp/screening_workflows.db`)
- Full event capture and persistence
- Event replay capability
- Detailed audit queries

---

## Workflow Specification Reference

**Complete workflow implementation details in `spec/dev_reference/implementation_guide.md` (canonical source).**

### High-Level Flow (4 steps)

1. **Deep Research Agent** - Conduct comprehensive executive research using o4-mini-deep-research
2. **Quality Check** - Evaluate research sufficiency (simple heuristics)
3. **Conditional Incremental Search** - Optional single-pass supplement if quality is low
4. **Assessment Agent** - Evaluate candidate against role spec with evidence-aware scoring

### Key Design Patterns

- **Linear execution** - Sequential steps (no teams, no nested workflows in v1)
- **Quality-gated research** - Optional incremental search triggered by quality check
- **Evidence-aware scoring** - Explicit handling of Unknown dimensions using `None`
- **Agno native features** - Structured outputs via `output_schema`, built-in retry/backoff
- **Event streaming** - `stream_events=True` for stdout logging (no persistence in v1)

### Implementation References

- **Step-by-step execution logic:** `spec/dev_reference/implementation_guide.md`
- **Agent creation patterns:** `spec/dev_reference/AGNO_REFERENCE.md`
- **Quality gate thresholds:** `spec/dev_reference/implementation_guide.md`
- **Score calculation:** See `calculate_overall_score()` interface in this document (line 279)

**For complete workflow pseudocode, error handling, and execution patterns, see `spec/dev_reference/implementation_guide.md`.**

---

## Agno Framework Implementation Guidance

### Recommended Native Agno Features for v1.0-Minimal

**Use These Agno Patterns:**

1. **Structured Outputs (Native):**

   ```python
   from agno import Agent, OpenAIResponses
   from agno.tools.reasoning import ReasoningTools
   from models import AssessmentResult

   assessment_agent = Agent(
       name="assessment_agent",
       model=OpenAIResponses(id="gpt-5-mini"),
       tools=[ReasoningTools(add_instructions=True)],
       output_schema=AssessmentResult,  # Returns Pydantic model directly
   )
   ```

   - Applies to gpt-5-mini assessment agent (Deep Research models reject `output_schema`; see warning above)
   - No separate parser agent needed
   - No custom JSON parsing prompts

2. **Single Workflow for Orchestration:**

   ```python
   from agno import Workflow

   workflow = Workflow(
       name="screening",
       stream_events=True,  # Log to stdout
   )
   ```

   - Linear workflow (no teams, no nested workflows in v1)
   - Simple, sequential steps
   - Event streaming for visibility

3. **Built-in Retry/Backoff:**

   ```python
   agent = Agent(
       model=OpenAIResponses(id="o4-mini-deep-research"),
       exponential_backoff=True,
       retries=2,
       retry_delay=1,
   )
   ```

   - No custom retry wrappers needed
   - Handles transient API failures
   - Configurable backoff strategy

4. **OpenAI Web Search Tools:**

   ```python
   from agno.tools.openai import web_search

   agent = Agent(
       name="incremental_search",
       model=OpenAIResponses(id="gpt-5"),
       tools=[web_search],  # Built-in web search
   )
   ```

   - Use Agno's built-in OpenAI tools
   - No hand-written HTTP calls
   - Integrated with agent framework

5. **Session State Management with SqliteDb (Required for v1):**

   ```python
   from agno.db.sqlite import SqliteDb
   from agno.workflow import Workflow

   # Required for v1: Persist session state for local review
   workflow = Workflow(
       name="screening",
       db=SqliteDb(db_file="tmp/agno_sessions.db"),  # Agno-managed tables only
       session_state={
           "screen_id": None,
           "candidates_processed": [],
       },
       stream_events=True,
   )

   # Phase 2+ fallback only: Stateless execution (NOT used in v1)
   from agno.db.in_memory import InMemoryDb

   stateless_workflow = Workflow(
       name="screening",
       db=InMemoryDb(),  # Clears on restart
       session_state={"screen_id": None},
       stream_events=True,
   )
   ```

   - **v1 requires SqliteDb** for reviewable local workflow history
   - File stored at `tmp/agno_sessions.db` (gitignored)
   - Contains only Agno-managed session tables, **no custom schema**
   - InMemoryDb is Phase 2+ fallback only (not used in v1)
   - **Critical:** No custom WorkflowEvent model or event logging tables in v1

6. **ReasoningTools for Assessment Agent (Required):**

   ```python
   from agno.tools.reasoning import ReasoningTools

   assessment_agent = Agent(
       name="assessment",
       model=OpenAIResponses(id="gpt-5-mini"),
       tools=[ReasoningTools(add_instructions=True)],  # Required for v1
       output_schema=AssessmentResult,
       instructions=[
           "Use reasoning tools to think through candidate matches systematically.",
           "Evaluate candidate against role specification with explicit reasoning.",
           "Provide dimension-level scores with evidence and confidence levels."
       ]
   )
   ```

   - Enables built-in "think → analyze" pattern for assessment quality
   - Generates explicit reasoning trails (aligns with PRD AC-PRD-04)
   - Minimal implementation cost (~5 lines of code)
   - Required for all assessment agents in v1

**Do NOT Use in v1.0-Minimal:**

- AGNO memory / Postgres DB (`enable_user_memories`, `enable_agentic_memory`)
- AGNO Teams or multi-agent coordination
- Large toolkits unrelated to core functionality (Notion, Slack, etc.)
- Nested workflows or complex state machines
- Event persistence to databases (stream to stdout only)

---

## Airtable Schema Reference

**Complete Airtable schema is in `spec/dev_reference/airtable_ai_spec.md` (canonical source).**

### V1 Tables Overview (6 core + 1 helper = 7 tables)

**Core Tables (v1):**

1. **People (64 records)** - Executive candidates from guildmember_scrape.csv
2. **Portco (4 records)** - Portfolio companies for demo scenarios
3. **Portco_Roles (4 records)** - Open roles at portfolio companies
4. **Searches (4 records)** - Active talent searches linking roles to specs
5. **Screens (4 records)** - Screening batches (webhook trigger table)
6. **Assessments (~12-15 records)** - Assessment results with all research data (research_structured_json, research_markdown_raw, assessment_json, assessment_markdown_report)

**Helper Table (v1):**
7. **Role_Specs (6 records)** - 2 templates + 4 customized specs (referenced by Searches)

**Phase 2+ Tables (NOT in v1):**

- ~~**Workflows**~~ - Execution audit trail (deferred; use Agno SqliteDb + Airtable status fields)
- ~~**Research_Results**~~ - Structured research outputs (deferred; stored in Assessments table instead)

### Webhook Automation

- **Trigger Table:** Screens
- **Trigger Field:** `status` changes to "Ready to Screen"
- **Action:** POST to Flask `/screen` endpoint with `{screen_id: <record_id>}`
- **Processing:** Python sets status to "Processing" → "Complete" or "Failed"

### Data Storage Pattern

- **Complex nested data:** Stored as JSON in Long Text fields
- **Key fields extracted:** Overall score, confidence, summary for quick viewing
- **Full Pydantic models:** Stored in `*_json` fields for complete audit trail

**v1.0-minimal Changes:**

- No Workflows table (Phase 2+)
- Status and error tracking in Screens and Assessments tables
- Research and Assessment JSON stored in respective tables
- Raw research markdown stored in Assessments.research_markdown_raw
- Assessment markdown reports stored in Assessments.assessment_markdown_report
- Agno session state in tmp/agno_sessions.db (SqliteDb, not exposed in Airtable)

**For complete field definitions, types, options, and setup instructions, see `spec/dev_reference/airtable_ai_spec.md`.**

---

## Implementation Checklist

### Stage 1: Setup (2 hours)

- [x] Create minimal project structure (5 files)
- [x] Set up Python environment (uv, .python-version)
- [ ] Install dependencies (pyproject.toml)
- [ ] Configure environment variables (.env)
- [ ] Create Pydantic models (models.py)
- [ ] Validate against data_design.md schemas

### Stage 2: Agent Implementation (6 hours)

- [ ] Implement research agent (agents.py)
  - [ ] Deep Research mode (o4-mini-deep-research)
  - [ ] Agno structured outputs (output_schema)
  - [ ] Built-in retry/backoff
- [ ] Implement assessment agent (agents.py)
  - [ ] Spec-guided evaluation
  - [ ] Evidence-aware scoring (None for Unknown)
  - [ ] Agno structured outputs
- [ ] Implement incremental search agent (agents.py)
  - [ ] Optional single-step search
  - [ ] Built-in web_search tool
  - [ ] Research merging

### Stage 3: Workflow Implementation (4 hours)

- [ ] Create workflow in agents.py
  - [ ] Step 1: Deep Research
  - [ ] Step 2: Quality Check (simple function)
  - [ ] Step 3: Conditional Incremental Search
  - [ ] Step 4: Assessment
- [ ] Implement scoring logic
  - [ ] calculate_overall_score() - simple average × 20
  - [ ] check_research_quality() - minimal criteria
- [ ] Test workflow end-to-end with mock data

### Stage 4: Integrations (4 hours)

- [ ] Implement Airtable client (airtable_client.py)
  - [ ] Read operations (get_screen, get_role_spec, etc.)
  - [ ] Write operations (write_assessment, update_screen_status)
  - [ ] Error handling
- [ ] Implement Flask webhook server (app.py)
  - [ ] /screen endpoint
  - [ ] Request validation
  - [ ] Error handling
- [ ] Set up ngrok tunnel

### Stage 5: Testing (2 hours)

- [ ] Basic tests (tests/)
  - [ ] test_scoring.py - overall score calculation
  - [ ] test_quality_check.py - quality heuristics
  - [ ] test_workflow_smoke.py - happy path (optional)
- [ ] Run tests and verify core logic

### Stage 6: Demo Preparation (3 hours)

- [ ] Pre-run 3 scenarios (Pigment CFO, Mockingbird CFO, Synthesia CTO)
- [ ] Verify results in Airtable
- [ ] Prepare Estuary CTO for live demo
- [ ] Test webhook trigger automation
- [ ] Create demo script with timing estimates

**Total Estimated Time:** 21 hours (reduced from 34 hours)

---

## Success Criteria

This specification succeeds if:

1. ✅ **Working Prototype:** Demonstrates end-to-end candidate screening
2. ✅ **Evidence-Aware Scoring:** Handles Unknown dimensions with None/null (not 0 or NaN)
3. ✅ **Quality-Gated Research:** Optional incremental search triggered when quality is low
4. ✅ **Minimal Implementation:** 5-file structure, simple algorithms, basic logging
5. ✅ **Type Safety:** Type hints on public functions (mypy as goal, not gate)
6. ✅ **Basic Tests:** Core logic tested (scoring, quality check)
7. ✅ **Demo Ready:** 3 pre-run scenarios complete, 1 ready for live execution
8. ✅ **Clear Documentation:** This spec + README explain implementation

**Remember:** The goal is demonstrating quality of thinking through minimal, working code—not building production infrastructure.

---

## Document Control

**Related Documents:**

- `spec/constitution.md` - Project governance and principles
- `spec/prd.md` - Product requirements document
- `spec/v1_minimal_spec.md` - Minimal scope definition (this document's basis)
- `case/technical_spec_V2.md` - Detailed technical architecture
- `spec/dev_reference/implementation_guide.md` - Data models and schemas
- `spec/dev_reference/role_spec_design.md` - Role specification framework

**Approval:**

- Created: 2025-01-16
- Updated: 2025-01-17 (v1.0-minimal refactor)
- Status: Ready for Implementation
- Next Review: Post-implementation retrospective
