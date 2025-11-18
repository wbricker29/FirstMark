---
version: "1.0-minimal"
created: "2025-01-16"
updated: "2025-01-17"
project: "Talent Signal Agent"
context: "FirstMark Capital AI Lead Case Study"
implementation_status: "Stages 1-4 Complete (Airtable + Agents + Workflow + Flask Integration), Stage 5-6 Pending (Testing + Demo Prep)"
---

# Technical Specification: Talent Signal Agent (v1.0-Minimal)

Engineering contract for Python implementation of AI-powered executive matching system

## Current Implementation Status (2025-01-17)

**Stage 1 (Airtable Foundation): ✅ COMPLETE**
- 8 tables configured (6 core + 1 helper + 1 audit bonus)
- Base ID: appeY64iIwU5CEna7
- 2/4 demo scenarios seeded (Pigment CFO complete, Estuary CTO in processing)
- 2/64 executives loaded, 2 role spec templates ready
- Schema 95% aligned with spec (minor cosmetic deviations documented below)
- **Phase 0 data loading:** Using `talent-signal-candidate-loader` Claude skill for automated CSV import

**Stage 2 (Agent Implementation): ✅ COMPLETE**
- ✅ demo/models.py - All Pydantic models implemented
- ✅ demo/prompts/catalog.yaml + library.py - Centralized YAML prompt catalog with loader
- ✅ demo/agents.py - Research, Assessment, Incremental Search agents consume catalog templates
- ✅ tests/test_prompts.py - Loader regression protection
- ✅ tests/test_scoring.py - 7 test cases with fixtures (all passing)
- ✅ tests/test_quality_check.py - 9 test cases with fixtures (all passing)
- ✅ tests/test_research_agent.py - 21 test cases (all passing)
- ✅ 58 total tests passing, 75% coverage (exceeds 50% constitution target)
- ✅ Type hints and docstrings on all public functions

**Stage 3 (Workflow Orchestration): ✅ COMPLETE**
- ✅ Linear workflow with 4-step pipeline (Deep Research → Quality Check → Incremental Search → Assessment)
- ✅ SqliteDb session state management at tmp/agno_sessions.db
- ✅ Agno UI Dashboard - Real-time workflow monitoring and session inspection validated
- ✅ screen_single_candidate() orchestration helper
- ✅ Event streaming with emoji indicators (🔍, ✅, ❌, 🔄) + UI visualization
- ✅ Quality gate triggering conditional incremental search
- ✅ tests/test_workflow.py - 9 test cases covering all 5 acceptance criteria (all passing)
- ✅ 75% coverage (exceeds 50% constitution target)
- ✅ Workflow architecture + Agno UI usage documented in README.md

**Stage 4 (Webhook Integration): ✅ COMPLETE**
- ✅ AirtableClient with full CRUD operations (`demo/airtable_client.py`)
- ✅ Legacy Flask webhook server with POST `/screen` endpoint (`demo/app.py`) retained for compatibility
- ✅ Shared screening workflow logic (`demo/screening_service.py`)
- ✅ tests/test_airtable_client.py - 37 tests, 100% coverage (all passing)
- ✅ tests/test_app.py - 21 tests, 90% coverage (legacy suite, skipped in default CI)
- ✅ Comprehensive README documentation with ngrok setup (AgentOS instructions front-and-center; Flask documented as legacy)

**Stage 4.5 (Prompt Templating & AgentOS Runtime): ✅ COMPLETE / CUTOVER IN PROGRESS**
- ✅ **Centralized Prompt Catalog** (`demo/prompts/catalog.yaml`)
  - Canonical YAML prompt definitions for all 4 agents (deep_research, research_parser, incremental_search, assessment)
  - Structured prompt contexts: `description`, `instructions`, `expected_output`, `additional_context`
  - Version-controlled prompts (no hardcoded Python strings)
- ✅ **Prompt Library** (`demo/prompts/library.py` + `__init__.py`)
  - `get_prompt(name, **placeholders)` loader returning `PromptContext` dataclass
  - `PromptContext.as_agent_kwargs()` for direct Agno Agent integration
  - Placeholder support via Python `str.format` syntax
- ✅ **Agent Integration** (`demo/agents.py`)
  - All agent factories now use `get_prompt()` for prompt loading
  - Temporal awareness with `add_datetime_to_context=True` on research/assessment agents
  - Context engineering aligned with Agno best practices
- ✅ **Prompt Tests** (`tests/test_prompts.py`)
  - Catalog validation and regression protection
  - Missing key error handling verification
- ✅ **AgentOS Runtime** (`demo/agentos_app.py`)
  - FastAPI entrypoint now canonical `/screen` implementation
  - Control plane UI validated + `/docs` contract codified in spec
  - Shared workflow orchestration via `demo/screening_service.py`
  - README/runbooks updated to use AgentOS + ngrok; Flask instructions moved to legacy appendix
  - FastAPI-specific regression tests (`tests/test_agentos_app.py`)
- ⬜ **Outstanding Cutover Tasks**
  - ✅ Update CI to treat `demo/app.py` tests as legacy (pyproject defaults `-m 'not legacy'`; run `pytest -m legacy` when needed)
  - ⬜ Ensure all Airtable automations/scripts use the AgentOS URL + optional bearer auth (helper scripts + runbooks now reference AgentOS; confirm Airtable automations next)
  - ⬜ Document/postpone deletion of `demo/app.py` after validation (see `docs/agent_os_integration_spec.md` for hand-off checklist)
- 📋 Reference: `docs/agent_os_integration_spec.md` (migration plan + deployment checklist)
- 📋 Reference: `spec/dev_reference/prompt_system_summary.md`

**Next Steps:**
1. End-to-end integration testing with full workflow (2 hours) - Stage 5
2. Seed remaining demo data: 62 executives + 2 scenarios (2-4 hours) - Stage 6
3. Execute pre-runs (Mockingbird CFO, Synthesia CTO) + live demo prep (3 hours) - Stage 6

See "Implementation Roadmap" section (line 1201) for detailed breakdown.

### AgentOS Integration Status

**Prototype Complete:** An alternative FastAPI-based runtime using the AgentOS framework has been implemented in `demo/agentos_app.py`, running the same screening workflow as the Flask implementation via shared `demo/screening_service.py`.

**Current Architecture (Dual Entrypoints):**
- **Flask (`demo/app.py`)**: Production webhook entrypoint for Airtable automation
- **AgentOS (`demo/agentos_app.py`)**: Prototype entrypoint with enhanced observability and control plane
- **Shared Logic**: Both use `demo/screening_service.py` for workflow orchestration

**AgentOS Benefits:**
- **Runtime + Control Plane**: SSE-compatible FastAPI app with built-in UI for stakeholder demos
- **Deployment Flexibility**: Docker Compose templates for ECS/GCE/Azure/on-prem
- **Enhanced Observability**: Metrics, eval hooks, RBAC, session management
- **MCP Integration**: Optional MCP server via `enable_mcp_server=True`
- **Production Path**: Sqlite (dev) → Postgres (production) with managed templates

**Migration Roadmap:**
Stage 4 polish work is complete. Stage 4.5 introduced centralized prompt templating (enabling code-free prompt iteration) and the AgentOS prototype runtime. Stage 5 will focus on multi-candidate orchestration, metrics, and evals on the AgentOS runtime. Complete migration plan: `docs/agent_os_integration_spec.md`

## Architecture

### System Overview

The Talent Signal Agent is a demo-quality Python application that uses AI agents to research and evaluate executive candidates against role specifications. The system integrates with Airtable for data storage and UI, uses OpenAI's Deep Research API for candidate research, and employs structured LLM outputs for evidence-aware assessments.

**Key Design Principles:**

- **Evidence-Aware Scoring:** Explicit handling of "Unknown" when public data is insufficient (using `None`/`null`, not 0 or NaN)
- **Quality-Gated Research:** Optional single incremental search agent step when initial research has quality issues
- **Agno-Managed Observability:** Agno UI dashboard for workflow monitoring; no custom event DB for v1
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
- **Framework:** FastAPI + AgentOS (canonical webhook server), Flask (legacy compatibility), Agno (agent orchestration + UI dashboard)
- **LLM Provider:** OpenAI (o4-mini-deep-research, gpt-5-mini)
- **Database:** Airtable (primary storage), Agno SqliteDb for session state (tmp/agno_sessions.db, no custom event tables)
- **Validation:** Pydantic (structured outputs)
- **Package Manager:** UV
- **Tunnel:** ngrok (local demo)
- **UI/Monitoring:** Agno built-in UI dashboard (browser-accessible), AgentOS control plane (prototype)
- **Prompt Management:** YAML prompt catalog (`demo/prompts/catalog.yaml`) + loader (`demo/prompts/library.py`)

### Project Structure

**v1.0-Minimal Layout (core modules + prompt catalog):**

```
demo/
├── app.py               # Flask app + webhook entrypoints (legacy compatibility)
├── agentos_app.py       # AgentOS/FastAPI entrypoint (canonical runtime)
├── screening_service.py # Shared workflow orchestration logic
├── agents.py            # Research + assessment agent creation + runners
├── models.py            # Pydantic models (research + assessment)
├── airtable_client.py   # Thin Airtable wrapper
├── settings.py          # Config/env loading (optional)
└── prompts/
    ├── catalog.yaml     # Canonical prompt definitions (YAML)
    └── library.py       # Loader that materializes PromptContext objects

tmp/
└── agno_sessions.db    # Agno workflow session state (gitignored, SqliteDb only)

tests/
├── test_scoring.py         # calculate_overall_score tests
├── test_quality_check.py   # quality check heuristics
├── test_prompts.py         # prompt catalog loader tests
└── test_workflow_smoke.py  # happy-path /screen flow with mocks (optional)

spec/                   # Documentation
├── constitution.md     # Project governance
├── prd.md              # Product requirements
├── spec.md             # This file
└── v1_minimal_spec.md  # Minimal scope definition

docs/                   # Integration specifications
└── agent_os_integration_spec.md  # AgentOS migration roadmap

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

### v1.0-Minimal Scope Contract

**What v1 INCLUDES:**
- ✅ Single Flask endpoint (`POST /screen`)
- ✅ Deep Research API (o4-mini-deep-research) as primary research mode
- ✅ Optional single incremental search step (max 2 web/search calls) when quality is low
- ✅ Spec-guided assessment with evidence-aware scoring (None for Unknown)
- ✅ Agno workflow with SqliteDb at tmp/agno_sessions.db (session state only)
- ✅ **Agno UI Dashboard** for real-time workflow monitoring and session inspection
- ✅ **Centralized Prompt Templates** (`demo/prompts/catalog.yaml` + loader)
- ✅ ReasoningTools enabled for all assessment agents
- ✅ Airtable-only storage (research + assessment data in Assessments table)
- ✅ Terminal logs + Airtable status fields + Agno UI (comprehensive observability)
- ✅ Synchronous, sequential processing (one candidate at a time)

**What v1 EXCLUDES (Phase 2+):**
- ❌ Fast Mode (web search fallback optimization)
- ❌ Multi-iteration supplemental search loops
- ❌ Custom SQLite WorkflowEvent tables or audit database
- ❌ Separate Research_Results or Workflows tables in Airtable
- ❌ Concurrent workers or async processing
- ❌ Parser agent layer (using Agno native structured outputs)
- ❌ Production deployment (Docker, cloud hosting, monitoring)
- ❌ Agno Teams, memory persistence, or multi-agent coordination

**Critical Design Decisions:**
- Simple average scoring (no weighted algorithm in v1)
- Direct structured outputs via `output_schema` (no parser needed)
- All user-facing data in Airtable (4 JSON fields in Assessments table)
- SqliteDb required for v1 (InMemoryDb is Phase 2+ fallback only)

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
- **UI Dashboard:** Agno UI (browser-accessible, workflow monitoring)
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
        final_status = "Complete" if not errors else "Failed"
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
- Update Screen status to "Failed" if any candidates failed

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

- **Primary:** Agno UI Dashboard - Real-time workflow monitoring, session inspection, reasoning traces
- **Secondary:** Airtable fields (status, error messages, assessment JSON, research JSON)
- **Tertiary:** Terminal logs during execution
- **Agno Events:** Enable `stream_events=True` for stdout logging + UI visualization

**Phase 2+ Enhancements:**

- SQLite database for workflow events (`tmp/screening_workflows.db`)
- Full event capture and persistence
- Event replay capability
- Detailed audit queries
- Advanced Agno UI customization (custom dashboards, alerts)

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

   **Critical Distinctions:**

   - ✅ **v1.0-minimal REQUIRES SqliteDb** - File persists locally at `tmp/agno_sessions.db` for reviewable session history
   - ✅ **Agno-managed tables ONLY** - No custom schema, no WorkflowEvent model, no event logging tables
   - ❌ **InMemoryDb is Phase 2+ fallback** - NOT used in v1; stateless execution deferred
   - ❌ **Custom event persistence is Phase 2+** - No SQLite audit database beyond Agno's internal session state

   **v1 Audit Trail Contract:**
   - Airtable: Final results (assessment_json, research_structured_json, status, error messages)
   - SqliteDb: Agno workflow sessions (agent transcripts, tool calls, retries)
   - Stdout: Streaming events via `stream_events=True`
   - No separate events database or custom workflow event capture

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

7. **Agno UI Dashboard (Required for v1):**

   ```python
   from agno import Workflow

   # UI automatically available when workflow runs
   workflow = Workflow(
       name="screening",
       db=SqliteDb(db_file="tmp/agno_sessions.db"),
       stream_events=True,  # Enables UI visualization
   )

   # Access UI at: http://localhost:7777 (or configured port)
   # - Real-time workflow execution monitoring
   # - Session history and inspection
   # - Agent inputs/outputs and reasoning traces
   # - Prompt template viewing
   ```

   - Zero-configuration UI for local development
   - Browser-accessible workflow monitoring
   - Session replay and debugging capabilities
   - Required for v1 demo (showcase modern agent tooling)

8. **Centralized Prompt Templates (Required for v1):**

   ```python
   from agno import Agent
   from pathlib import Path

   # Option 1: Load from YAML/JSON file
   assessment_agent = Agent(
       name="assessment",
       model=OpenAIResponses(id="gpt-5-mini"),
       instructions=Path("demo/prompts/assessment.yaml").read_text(),
       output_schema=AssessmentResult,
   )

   # Option 2: Use Agno's template system (if available)
   # Check Agno docs for native template loading patterns
   ```

   **Template Structure (demo/prompts/assessment.yaml):**

   ```yaml
   system_prompt: |
     You are an expert executive recruiter evaluating candidates for senior leadership roles.

     Evaluate the candidate against the provided role specification using evidence-based reasoning.

     Scoring Guidelines:
     - Use 1-5 scale for each dimension
     - Return null/None for dimensions with insufficient evidence
     - Cite specific evidence for all scored dimensions
     - Provide confidence levels (High/Medium/Low) for each score

   user_prompt_template: |
     Role Specification:
     {role_spec_markdown}

     Candidate Research:
     {research_summary}

     Evaluate this candidate against the role specification above.
   ```

   - Version-controlled prompts (not hardcoded in Python)
   - Easy iteration without code changes
   - Clear separation of logic and instructions
   - Required for v1 demo (showcase prompt management)

**Do NOT Use in v1.0-Minimal:**

- AGNO memory / Postgres DB (`enable_user_memories`, `enable_agentic_memory`)
- AGNO Teams or multi-agent coordination
- Large toolkits unrelated to core functionality (Notion, Slack, etc.)
- Nested workflows or complex state machines
- Event persistence to databases (stream to stdout only)

---

## Airtable Schema Reference

**Complete Airtable schema is in `spec/dev_reference/airtable_ai_spec.md` (canonical source).**

### V1 Tables Overview (8 tables: 6 core + 1 helper + 1 audit)

**Core Tables (v1):**

1. **People (2/64 records seeded)** - Executive candidates from guildmember_scrape.csv
   - Current: 2 demo executives (Alex Rivera - CFO, Nia Patel - CTO)
   - Target: 64 total from reference/guildmember_scrape.csv
2. **Portcos (2/4 records seeded)** - Portfolio companies for demo scenarios
   - Current: Pigment (Series B), Estuary (Series C)
   - Target: 4 companies for full demo scenarios
3. **Portco Roles (2/4 records seeded)** - Open roles at portfolio companies
   - Current: Pigment CFO, Estuary CTO
   - Target: 4 roles (add Mockingbird CFO, Synthesia CTO)
4. **Searches (2/4 records seeded)** - Active talent searches linking roles to specs
   - Current: Pigment CFO Search (Active), Estuary CTO Search (Planning)
   - Target: 4 searches for full demo
5. **Screens (2/4 records seeded)** - Screening batches (webhook trigger table)
   - Current: Screen #1 (Pigment CFO - Complete), Screen #2 (Estuary CTO - Processing)
   - Target: 4 screens for pre-runs + live demo
6. **Assessments (1/~12-15 records seeded)** - Assessment results with all research data
   - Current: 1 complete (Alex Rivera for Pigment CFO, score: 86.5)
   - Fields: research_structured_json, research_markdown_raw, assessment_json, assessment_markdown_report
   - **Note:** Table contains duplicate JSON fields (both singleLineText "(text)" and multilineText versions)

**Helper Table (v1):**

7. **Role Specs (2/6 records seeded)** - Role evaluation templates and customized specs
   - Current: 2 templates (Series B SaaS CFO, Growth Infra CTO)
   - Target: 2 templates + 4 customized specs (referenced by Searches)

**Audit Table (v1 bonus):**

8. **Audit Logs** - Change tracking and compliance monitoring (not in original spec)
   - Tracks state changes, webhook events, manual edits, system updates
   - AI-powered change summaries and compliance risk detection

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

### Current Implementation Notes

**Field Type Deviations (cosmetic, non-blocking):**

- **Screen ID:** Implemented as `number` instead of `auto-number` (manual assignment for demo control)
- **Assessment ID:** Implemented as `singleLineText` instead of `auto-number` (allows custom ID format)
- **URL Fields:** LinkedIn URL, Website using `singleLineText` instead of `url` type (sufficient for demo)

**Duplicate JSON Fields in Assessments Table:**

The Assessments table currently contains both `singleLineText` "(text)" versions AND `multilineText` versions of JSON fields:
- Dimension Scores JSON (text) + Dimension Scores JSON
- Must Haves Check JSON (text) + Must Haves Check JSON
- Red Flags JSON (text) + Red Flags JSON
- Green Flags JSON (text) + Green Flags JSON
- Counterfactuals JSON (text) + Counterfactuals JSON
- Research Structured JSON (text) + Research Structured JSON
- Assessment JSON (text) + Assessment JSON

**Recommendation:** Use multilineText versions for implementation, remove singleLineText "(text)" duplicates in cleanup phase.

**Demo-Scoped Single Select Options:**

To simplify the demo, several single-select fields have reduced option sets:
- **People.Normalized Function:** CFO, CTO only (spec defines 8 options including CEO, CPO, CRO, COO, CMO)
- **People.Source:** FMGuildPage, FMLinkedIN only (spec defines 6 sources)
- **Portcos.Stage:** Series B, Series C only (spec defines 6 stages from Seed to Public)
- **Portcos.Sector:** B2B SaaS, Infrastructure only (spec defines 7 sectors)
- **Portco Roles.Role Type:** CFO, CTO only (spec defines 5 types)
- **Portco Roles.Status:** Open only (spec defines: Open, On Hold, Filled, Cancelled)
- **Portco Roles.Priority:** Critical, High only (spec defines: Critical, High, Medium, Low)
- **Searches.Status:** Active, Planning only (spec defines: Planning, Active, Paused, Completed)
- **Screens.Status:** Draft, Processing, Complete, Failed (demo uses: Processing, Complete, Failed)
- **Assessments.Status:** Pending, Processing, Complete, Failed (demo uses: Pending, Complete, Failed)

**Phase 2+ Enhancement:** Expand single-select options to full spec when supporting broader use cases beyond CFO/CTO demo scenarios.

**For complete field definitions, types, options, and setup instructions, see `spec/dev_reference/airtable_ai_spec.md`.**

---

## Implementation Roadmap

**Progress Tracking:** See `spec/units/` for detailed phase plans with task statuses.

**Single Developer:** Follow stages 1-6 sequentially (~21 hours total)
**Two Developers:** See parallel track breakdown below (~20 hours per developer)

### High-Level Stages

1. **Stage 1: Setup** (2 hours) ✅ COMPLETE (2025-01-16)
   - Airtable base configured (8 tables)
   - 2/4 demo scenarios seeded (Pigment CFO, Estuary CTO)
   - 2/64 executives loaded
   - 2 role spec templates created
   - Project structure and dependencies configured
   - Agno UI dashboard setup and validation
   - Prompt template directory structure created
2. **Stage 2: Agent Implementation** (6 hours) ✅ COMPLETE (2025-11-17)
   - ✅ demo/models.py - All Pydantic models
   - ✅ demo/prompts/ - Centralized prompt templates for research and assessment
   - ✅ demo/agents.py - Research, Assessment, Incremental Search agents with template loading
   - ✅ tests/test_scoring.py + tests/test_quality_check.py + tests/test_research_agent.py (37 tests)
   - ✅ Type hints, docstrings, 75% coverage
   - ✅ All acceptance criteria validated
   - ✅ Agno UI dashboard tested for agent monitoring
3. **Stage 3: Workflow Orchestration** (4 hours) ✅ COMPLETE (2025-11-17)
   - ✅ Linear workflow with quality gate
   - ✅ SqliteDb session state management (tmp/agno_sessions.db)
   - ✅ screen_single_candidate() helper
   - ✅ Event streaming with emoji indicators + Agno UI visualization
   - ✅ Agno UI dashboard validated for real-time workflow monitoring
   - ✅ 9 workflow integration tests (all passing)
   - ✅ Documentation in README.md
4. **Stage 4: Flask Integration** (4 hours) ✅ COMPLETE (2025-11-17)
   - ✅ AirtableClient implementation (demo/airtable_client.py)
   - ✅ Flask webhook server (demo/app.py)
   - ✅ Error handling and logging with emoji indicators
   - ✅ 118 tests passing, 82% coverage
4.5. **Stage 4.5: Prompt Templating & AgentOS Runtime** (2 hours) ✅ COMPLETE (2025-11-17)
   - ✅ Centralized YAML prompt catalog (demo/prompts/catalog.yaml) for all 4 agents
   - ✅ Prompt library loader (demo/prompts/library.py) with get_prompt() interface
   - ✅ Agent integration refactor - all factories use prompt templates
   - ✅ Prompt validation tests (tests/test_prompts.py)
   - ✅ Context engineering alignment (temporal awareness, Agno best practices)
   - ✅ AgentOS/FastAPI entrypoint (demo/agentos_app.py)
   - ✅ Shared workflow orchestration (demo/screening_service.py)
   - ✅ Dual runtime architecture (Flask production + AgentOS prototype)
   - ✅ Control plane UI validation
   - ✅ Migration roadmap documented (docs/agent_os_integration_spec.md)
   - 📋 Reference: spec/dev_reference/prompt_system_summary.md
5. **Stage 5: Testing** (2 hours) ⏸️ PENDING
   - Integration tests + validation
   - Manual webhook testing
6. **Stage 6: Demo Preparation** (3 hours) ⏸️ PENDING
   - Complete data seeding (62 executives, 2 scenarios)
   - Pre-runs (Mockingbird CFO, Synthesia CTO)
   - Live scenario setup (Estuary CTO)

---

## 2-Developer Parallel Implementation Track

### **Stage 1: Foundation Setup** (2 hours parallel) ✅ COMPLETE

**Developer A (Data Layer):**
- [x] Create project structure (5 files + prompts/: models.py, agents.py, airtable_client.py, app.py, settings.py)
- [x] Implement **models.py** - All Pydantic models
  - ExecutiveResearchResult, AssessmentResult, DimensionScore
  - Citation, CareerEntry, MustHaveCheck
- [x] Create **demo/prompts/** directory with template structure
  - research.yaml (Deep Research agent prompt)
  - assessment.yaml (Assessment agent prompt)
- [x] Create **settings.py** - Config/env loading
- [x] Set up **.env** from .env.example
- [x] Validate Agno UI dashboard accessibility

**Developer B (Infrastructure):**
- [x] Configure **pyproject.toml** with dependencies
- [x] Set up Python 3.11 environment (uv)
- [x] Install dependencies (`uv pip install`)
- [x] Implement **tests/test_scoring.py** skeleton
- [x] Set up Airtable base (8 tables including Audit Logs) from `spec/dev_reference/airtable_ai_spec.md`
- [x] Seed initial demo data (2/4 scenarios, 2/64 executives, 2 role spec templates)

**Sync Point:** ✅ Both complete → models.py merged

**Current State (2025-11-17):**
- ✅ Airtable base accessible (base ID: appeY64iIwU5CEna7)
- ✅ 8 tables configured with correct schemas
- ✅ 2 demo scenarios operational (Pigment CFO complete with assessment, Estuary CTO in processing)
- ✅ Stage 2 (Agent Implementation) complete - all agents and tests implemented

### **Stage 2: Core Components** (6 hours parallel) ✅ COMPLETE

**Developer A (Agents):**
- [x] Create **Prompt Templates** (`demo/prompts/`)
  - research.yaml - Deep Research agent instructions
  - assessment.yaml - Assessment agent evaluation guidelines
- [x] Implement **Research Agent** (`agents.py`)
  - `create_research_agent()` with Deep Research mode
  - Load instructions from prompt templates
  - `run_research()` with retry/backoff
  - Handle markdown output (NOT structured output for Deep Research)
  - Extract citations from `result.citations`
- [x] Implement **Assessment Agent** (`agents.py`)
  - `assess_candidate()` with gpt-5-mini
  - Load instructions from prompt templates
  - ReasoningTools integration
  - Structured outputs via `output_schema=AssessmentResult`
- [x] Implement **Incremental Search Agent** (`agents.py`)
  - Optional single-step search with web_search tool
  - Research merging logic
- [x] Test agents via Agno UI dashboard

**Developer B (Integration + Logic):**
- [x] Implement **scoring logic**
  - `calculate_overall_score()` - simple average × 20
  - `check_research_quality()` - ≥3 citations heuristic
- [x] Complete **tests/test_scoring.py** (7 test cases)
- [x] Create **tests/test_quality_check.py** (9 test cases)
- [x] Implement **airtable_client.py** - Complete client (completed in Stage 4)
  - `get_screen()`, `get_role_spec()`
  - `write_assessment()`, `update_screen_status()`
  - Error handling

**Sync Point:** ✅ Review agent interfaces complete - all agents functional with 75% test coverage

### **Stage 3: Workflow Orchestration** (4 hours paired/sequential) ✅ COMPLETE

**Developer A + B (Collaborative):**
- [x] Implement **Workflow** in `agents.py`
  - Step 1: Deep Research Agent (with template-loaded prompts)
  - Step 2: Quality Check (function call)
  - Step 3: Conditional Incremental Search
  - Step 4: Assessment Agent (with template-loaded prompts)
- [x] Configure **SqliteDb** at `tmp/agno_sessions.db`
  - Session state management
  - NO custom WorkflowEvent tables
- [x] Implement **screen_single_candidate()** helper
- [x] Add event streaming (`stream_events=True`)
- [x] Validate **Agno UI Dashboard** for workflow monitoring
  - Real-time execution visibility
  - Session inspection and replay
  - Prompt template viewing
- [x] Implement **tests/test_workflow.py** with 9 test cases
  - AC-WF-01: Linear workflow execution
  - AC-WF-02: Quality gate triggers incremental search
  - AC-WF-03: Session state persistence
  - AC-WF-04: Event streaming to stdout + UI
  - AC-WF-05: Error handling with retry
- [x] Document workflow architecture + Agno UI usage in README.md

**Testing Results:**
- Developer A: Workflow tested with mock agents (9/9 passing)
- Developer B: All acceptance criteria verified
- Coverage: 75% (exceeds 50% target)

**Sync Point:** ✅ Complete - End-to-end workflow validated with comprehensive test coverage

### **Stage 4: Flask Webhook** (3 hours parallel) ✅ COMPLETE

**Developer A (Endpoint Implementation):**
- [x] Implement **app.py** - Flask server
- [x] Implement **/screen endpoint**
  - Request validation
  - Screen status updates
  - Candidate iteration (synchronous)
  - Error handling (partial failures)
- [x] Add logging with emoji indicators (🔍, ✅, ❌)

**Developer B (Infrastructure):**
- [x] Set up **ngrok tunnel**
- [x] Configure **Airtable automation**
  - Trigger: Screen.status → "Ready to Screen"
  - Action: POST to Flask /screen with {screen_id}
- [x] Test webhook connectivity
- [x] Create error handling test cases

**Testing Results:**
- ✅ 37 AirtableClient tests (100% coverage of demo/airtable_client.py)
- ✅ 21 Flask endpoint tests (90% coverage of demo/app.py)
- ✅ 118 total tests passing
- ✅ 82% overall coverage (exceeds 50% target)
- ✅ Basic webhook connectivity verified
- ✅ Comprehensive README documentation with ngrok setup

**Sync Point:** ✅ Complete - Full webhook → workflow → Airtable write plumbing validated

### **Stage 4.5: Prompt Templating & AgentOS Runtime** (2 hours parallel) ✅ COMPLETE

**Developer A (Prompt System):**
- [x] Create **demo/prompts/catalog.yaml** - Centralized prompt definitions
  - Define structured prompts for all 4 agents (deep_research, research_parser, incremental_search, assessment)
  - Structure: `description`, `instructions`, `expected_output`, `additional_context`
  - Support placeholder syntax for dynamic content (e.g., `{role_title}`)
- [x] Implement **demo/prompts/library.py** - Prompt loader
  - `get_prompt(name, **placeholders)` function returning `PromptContext` dataclass
  - `PromptContext.as_agent_kwargs()` for Agno Agent integration
  - YAML parsing and validation with clear error messages
- [x] Create **demo/prompts/__init__.py** - Clean import interface
- [x] Refactor **demo/agents.py** - Use prompt templates
  - Update all agent factories to call `get_prompt()`
  - Add temporal awareness (`add_datetime_to_context=True`)
  - Remove hardcoded prompt strings
- [x] Implement **tests/test_prompts.py** - Catalog validation
  - Test all catalog entries load correctly
  - Verify missing key error handling
  - Test placeholder substitution

**Developer B (AgentOS Runtime):**
- [x] Implement **agentos_app.py** - FastAPI entrypoint with AgentOS
  - Configure AgentOS runtime with existing agents/workflows
  - Enable control plane UI for observability
  - Set up bearer token authentication (optional for demo)
  - Validate /screen endpoint compatibility
- [x] Extract **screening_service.py** - Shared workflow orchestration
  - Move `process_screen()` logic from app.py to shared module
  - Ensure both Flask and AgentOS can use common workflow
  - Maintain Airtable client integration pattern
- [x] Document **docs/agent_os_integration_spec.md**
  - Capture current findings and design decisions
  - Define migration roadmap for Stage 5+
  - Document deployment paths (Docker/ECS/Postgres)

**Testing Results:**
- ✅ All 4 agent prompt templates loading correctly from catalog
- ✅ Prompt tests passing (catalog validation + error handling)
- ✅ Agents successfully using prompt templates via get_prompt()
- ✅ Context engineering improvements validated (temporal awareness)
- ✅ AgentOS prototype running locally (demo/agentos_app.py)
- ✅ Both Flask and AgentOS routes functional with shared logic
- ✅ Control plane UI accessible for workflow monitoring
- ✅ Migration roadmap documented for future production deployment

**Sync Point:** ✅ Complete - Prompt templating system operational, dual runtime architecture validated, production migration path documented

**References:**
- Prompt system design: `spec/dev_reference/prompt_system_summary.md`
- Context engineering patterns: `reference/docs_and_examples/agno/agno_contextmanagement.md`
- AgentOS integration: `docs/agent_os_integration_spec.md`

### **Stage 5: Testing & Validation** (2 hours parallel) ⏸️ PENDING

**Developer A (Test Execution):**
- [ ] Run **test_scoring.py** suite
- [ ] Run **test_quality_check.py** suite
- [ ] Run **test_workflow_smoke.py** (if created)
- [ ] Fix any failing tests
- [ ] Verify type hints (mypy check - optional)

**Developer B (Integration Testing):**
- [ ] Manual test: Full /screen endpoint with 1 candidate
- [ ] Verify Airtable writes
- [ ] Check SqliteDb session state
- [ ] Review logs for completeness
- [ ] Test error scenarios (API failures, bad data)

**Sync Point:** All tests passing + manual validation complete

### **Stage 6: Demo Preparation** (3 hours parallel)

**Developer A (Pre-runs 1 & 2):**
- [ ] **Pre-run 1: Pigment CFO**
  - Execute via webhook
  - Verify results in Airtable
  - Document execution time
- [ ] **Pre-run 2: Mockingbird CFO**
  - Execute via webhook
  - Verify results in Airtable
  - Compare assessment quality

**Developer B (Pre-run 3 & Live Prep):**
- [ ] **Pre-run 3: Synthesia CTO**
  - Execute via webhook
  - Verify results in Airtable
- [ ] **Live Demo Prep: Estuary CTO**
  - Set up Screen record (status: "Draft")
  - Verify role spec + candidates loaded
  - Test webhook trigger (dry run)
- [ ] Create **demo script** with timing estimates

**Sync Point:** Review all 3 pre-runs + live demo readiness

### Timeline Summary

| Stage | Developer A | Developer B | Duration | Cumulative | Status |
|-------|-------------|-------------|----------|------------|--------|
| 1 | Data Layer | Infrastructure | 2h | 2h | ✅ Complete |
| 2 | Agents | Integration + Logic | 6h | 8h | ✅ Complete |
| 3 | Workflow (paired) | Workflow (paired) | 4h | 12h | ✅ Complete |
| 4 | Flask Endpoint | Webhook Setup | 3h | 15h | ✅ Complete |
| 4.5 | Prompt Templates + AgentOS | Shared Logic + Prompt System | 2h | 17h | ✅ Complete |
| 5 | Test Execution | Integration Testing | 2h | 19h | ⏸️ Pending |
| 6 | Pre-runs 1-2 | Pre-run 3 + Live Prep | 3h | 22h | ⏸️ Pending |

**Total: 22 hours per developer (adjusted for AgentOS prototype)**
**Completed: 17 hours (77%)** | **Remaining: 5 hours (23%)**

### Daily Sync Schedule (for 2.5 day sprint)

**Day 1 (8 hours):** ✅ COMPLETE
- ✅ Morning: Stages 1-2 (8h parallel)
- ✅ End of Day: Sync Point - merge models + review interfaces

**Day 2 (8 hours):** ✅ COMPLETE
- ✅ Morning: Stage 3 (4h collaborative)
- ✅ Afternoon: Stage 4 (3h parallel) → Sync webhook test
- ✅ Evening: Stage 4.5 (2h parallel) → Prompt templating system + AgentOS prototype

**Day 3 (5 hours):** ⏸️ PENDING
- Stage 5: Integration testing (2h)
- Stage 6: Demo preparation and pre-runs (3h)
- Final: Demo rehearsal together

### Critical Handoffs

1. **Stage 1 → 2:** Developer A provides models.py to Developer B
2. **Stage 2 → 3:** Both review agent interfaces + Airtable client before workflow
3. **Stage 3 → 4:** Workflow tested before Flask integration
4. **Stage 4 → 4.5:** Flask working before prompt templating refactor + AgentOS prototype
5. **Stage 4.5 → 5:** Prompt system + both runtimes validated before comprehensive testing
6. **Stage 5 → 6:** All tests green before pre-runs

### Risk Mitigation

- **Blocker in Stage 2?** Other developer can assist (agents are independent)
- **Workflow issues in Stage 3?** Fall back to manual step execution for testing
- **Webhook connectivity issues?** Use direct Python calls for pre-runs, fix automation later

---

## Success Criteria

This specification succeeds if:

### ✅ Completed (Stages 1-4.5)

1. ✅ **Working Prototype:** Demonstrates end-to-end candidate screening
2. ✅ **Evidence-Aware Scoring:** Handles Unknown dimensions with None/null (not 0 or NaN)
3. ✅ **Quality-Gated Research:** Optional incremental search triggered when quality is low
4. ✅ **Minimal Implementation:** 5-file structure + prompt templates, simple algorithms, basic logging
5. ✅ **Type Safety:** Type hints on public functions (mypy as goal, not gate)
6. ✅ **Basic Tests:** Core logic tested (scoring, quality check) - 118 tests passing, 82% coverage
7. ✅ **Clear Documentation:** This spec + README explain implementation
8. ✅ **Agno UI Dashboard:** Real-time workflow monitoring, session inspection operational
9. ✅ **Prompt Templates:** Centralized, version-controlled prompts for research and assessment agents

### ⏸️ Pending (Stages 5-6)

10. ⏸️ **Demo Ready:** 3 pre-run scenarios complete, 1 ready for live execution (Stage 6 pending)

**Remember:** The goal is demonstrating quality of thinking through minimal, working code—not building production infrastructure. Agno UI and prompt templates showcase modern agent development best practices.

---

## Document Control

**Related Documents:**

- `spec/constitution.md` - Project governance and principles
- `spec/prd.md` - Product requirements document
- `spec/v1_minimal_spec.md` - Minimal scope definition (this document's basis)
- `docs/agent_os_integration_spec.md` - **AgentOS migration roadmap and implementation plan**
- `case/technical_spec_V2.md` - Detailed technical architecture
- `spec/dev_reference/implementation_guide.md` - Data models and schemas
- `spec/dev_reference/role_spec_design.md` - Role specification framework

**Approval:**

- Created: 2025-01-16
- Updated: 2025-01-17 (v1.0-minimal refactor)
- Updated: 2025-01-17 (Added Agno UI dashboard, centralized prompt templates, and AgentOS prototype to v1.0-minimal scope)
- Status: Ready for Implementation (Stages 1-4 complete, AgentOS prototype complete)
- Next Review: Post-implementation retrospective
### Screening API (AgentOS `/screen` Endpoint)

**Purpose:** Canonical HTTP interface for Airtable automations and manual demo triggers. Hosted by `demo/agentos_app.py` (FastAPI + AgentOS).

**Endpoint:**

- Method: `POST`
- URL: `<AGENTOS_BASE_URL>/screen` (e.g., `http://localhost:5000/screen` or the ngrok URL)
- Headers:
  - `Content-Type: application/json`
  - `Authorization: Bearer <AGENTOS_SECURITY_KEY>` (optional — only required if configured in settings)

**Request Schema (`ScreenRequest`):**

```json
{
  "screen_id": "recXXXXXXXXXXXXXX"
}
```

- `screen_id` (string, required): Airtable record identifier for `Platform-Screens`. Must be non-empty and begin with `rec`.

**Successful Response (`200 OK`):**

```json
{
  "status": "success",
  "screen_id": "recScreen123",
  "candidates_total": 2,
  "candidates_processed": 2,
  "candidates_failed": 0,
  "execution_time_seconds": 18.42,
  "results": [
    {
      "candidate_id": "recCandidate123",
      "assessment_id": "recAssessment123",
      "overall_score": 78.5,
      "confidence": "High",
      "summary": "Topline summary...",
      "assessed_at": "2025-01-18T12:34:56.000000"
    }
  ]
}
```

- `status`: `"success"` when no candidate failures, `"partial"` when at least one candidate fails.
- `results`: One entry per successful candidate including Airtable Assessment record ID, score, confidence, summary, and timestamp.
- `errors` (optional): Present only when failures occur; mirrors Flask behavior.

**Error Responses:**

- `400 Bad Request` (`validation_error`): Returned when the payload is missing/invalid. Includes `message` and optional `fields` map.
- `500 Server Error` (`server_error`): Returned when downstream processing fails unexpectedly. Includes `screen_id` and `details`. The screen is marked `Complete` in Airtable with the failure noted via logging.

**Airtable Automation Contract:**

- Trigger: `Screens.status == "Ready to Screen"` automation sends `{ "screen_id": "{RECORD_ID}" }` to the AgentOS `/screen` endpoint (via ngrok or intranet URL).
- Auth: None by default. If `AGENTOS_SECURITY_KEY` is set, Airtable must include the `Authorization` header.
- Idempotency: Endpoint is stateless per request. Airtable should avoid duplicate triggers; reruns simply overwrite assessment records per candidate.

**Manual Testing:**

```bash
curl -X POST http://localhost:5000/screen \
  -H "Content-Type: application/json" \
  -d '{"screen_id": "recScreen123"}'
```

Add `-H "Authorization: Bearer $AGENTOS_SECURITY_KEY"` when security is enabled.
