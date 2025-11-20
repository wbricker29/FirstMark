# Design Synthesis: Talent Signal Agent

**Generated:** 2025-01-17  
**Version:** 1.0-minimal  
**Scope:** Complete architectural analysis of `demo/` implementation

---

## Executive Summary

The Talent Signal Agent is a Python-based AI system that automates executive candidate screening for FirstMark Capital portfolio companies. The system integrates with Airtable for data management, uses OpenAI's Deep Research API for candidate investigation, and employs structured LLM outputs for evidence-aware assessment scoring.

**Core Purpose:** Transform manual executive screening workflows into an automated, evidence-backed ranking system that integrates seamlessly with existing Airtable-based processes.

**Key Technologies:**
- **Runtime:** FastAPI + AgentOS (webhook server with control plane UI)
- **Orchestration:** Agno framework (workflow management + session persistence)
- **LLM Provider:** OpenAI (o4-mini-deep-research, gpt-5-mini)
- **Data Storage:** Airtable (primary), SqliteDb (session state)
- **Validation:** Pydantic (structured outputs)
- **Prompt Management:** YAML catalog (`demo/prompts/catalog.yaml`)

**Architecture Philosophy:**
- Evidence-aware scoring (explicit `None` for unknown, never 0 or NaN)
- Quality-gated research (conditional incremental search)
- Centralized prompt management (code-free prompt iteration)
- Session state persistence (audit trail via SqliteDb)
- Separation of concerns (thin wrappers, focused modules)

---

## Architecture Overview

### System Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    AIRTABLE DATABASE                         │
│  People | Portcos | Role_Specs | Searches | Screens |       │
│  Assessments | Automation_Log                                 │
└────────────────────┬──────────────────────────────────────────┘
                     │
                     │ Automation Trigger (Status = "Ready to Screen")
                     │ POST ScreenWebhookPayload (screen_slug + candidates)
                     │ Python sets Status → "Processing" on receipt
                     ▼
         ┌───────────────────────────┐
         │   NGROK TUNNEL (Demo)     │
         └───────────┬───────────────┘
                     │ HTTPS
                     ▼
    ┌────────────────────────────────────┐
    │   AGENTOS FASTAPI RUNTIME          │
    │   (:5001)                          │
    │   - POST /screen                   │
    │   - GET /healthz                  │
    │   - AgentOS Control Plane UI      │
    └───────────┬────────────────────────┘
                │
                ▼
    ┌────────────────────────────────────┐
    │   SCREENING_SERVICE                │
    │   (process_screen_direct)          │
    │   - Validates structured payload   │
    │   - Orchestrates candidate loop    │
    │   - Status + automation logging    │
    └───────────┬────────────────────────┘
                │
                ▼
    ┌────────────────────────────────────┐
    │   AGENTOS CANDIDATE WORKFLOW       │
    │   (4-step linear pipeline)          │
    │                                     │
    │   Step 1: Deep Research            │
    │     └─ o4-mini-deep-research       │
    │     └─ Research Parser Agent       │
    │                                     │
    │   Step 2: Quality Check            │
    │     └─ ≥3 citations + non-empty    │
    │                                     │
    │   Step 3: Incremental Search      │
    │     └─ Conditional (if quality fails)│
    │     └─ gpt-5 + web_search (max 2)  │
    │                                     │
    │   Step 4: Assessment               │
    │     └─ gpt-5-mini + ReasoningTools│
    │     └─ Evidence-aware scoring      │
    └───────────┬────────────────────────┘
                │
                │ Session State (SqliteDb)
                │ tmp/agno_sessions.db
                │
                ▼
    ┌────────────────────────────────────┐
    │   AIRTABLE CLIENT                  │
    │   - write_assessment()             │
    │   - update_screen_status()         │
    │   - log_automation_event()         │
    └────────────────────────────────────┘
```

### Data Flow

**Request Flow:**
1. User sets Screen status to "Ready to Screen" (triggers Airtable automation)
2. Automation POSTs structured `ScreenWebhookPayload` to `/screen` endpoint
   - Payload contains `screen_slug` with nested `role_spec_slug` (spec snapshot), `search_slug` (role info), and `candidate_slugs[]` array
   - All data pre-assembled by Airtable formulas - zero API traversal needed
3. FastAPI endpoint validates payload using `ScreenWebhookPayload` Pydantic model
4. `screening_service.process_screen_direct()` extracts spec markdown and candidates from payload (no Airtable reads)
5. For each candidate: `AgentOSCandidateWorkflow.run_candidate_workflow()` executes 4-step pipeline
6. Assessment results written to Airtable `Assessments` table via write-only client
7. Screen status updated to "Complete"

**State Management:**
- Workflow state persisted in `tmp/agno_sessions.db` (SqliteDb)
- Session ID format: `screen_{screen_id}_{candidate_id}`
- State structure: `session_state["workflow_data"]` dict containing research, assessment, metadata
- Pydantic models serialized to dict for JSON persistence

**Error Handling:**
- Validation errors → 400 with field-level details
- Runtime errors → 500 with error logging to Airtable
- Partial failures → Continue processing remaining candidates, return summary

---

## Core Components

### 1. `agentos_app.py` (~318 lines)

**Purpose:** AgentOS-backed FastAPI runtime serving as the canonical webhook entrypoint.

**Key Classes & Dependencies:**

- **`ScreenWebhookPayload`** (`demo/models.py`)
  - Nested payload schema (screen slug, role spec slug, search slug, candidate slugs)
  - Ensures FastAPI receives structured objects (no JSON strings to parse)
- **`verify_bearer_token()`** (optional FastAPI dependency)
  - Enforces `AGENTOS_SECURITY_KEY` when configured
  - Returns 401 with WWW-Authenticate header on failure

**Key Functions:**

- **`screen_endpoint()`** (lines 194-271)
  - FastAPI POST handler for `/screen`
  - Validates payload, enqueues `process_screen_direct()` via `BackgroundTasks`
  - Returns `202 Accepted` payload with `screen_id` + `candidates_queued`
  - Handles validation/server errors with consistent JSON responses (400/500)

- **`health_check()`** (lines 164-168)
  - FastAPI GET handler for `/healthz`
  - Simple health endpoint returning `{"status": "ok"}`
  - Used for monitoring and smoke tests

- **`_init_airtable_client()`** (lines 61-82)
  - Bootstraps AirtableClient with environment variables
  - Validates required credentials at startup

**Design Patterns:**
- **Facade Pattern:** FastAPI endpoint provides simplified interface to screening service
- **Dependency Injection:** `candidate_runner` parameter allows testability
- **Factory Pattern:** AgentOS instance created with registered agents and workflows

**Dependencies:**
- `demo.airtable_client.AirtableClient`
- `demo.screening_service.process_screen_direct`
- `demo.agents` (agent factories)
- `demo.models.AssessmentResult`
- `demo.settings.settings`

---

### 2. `workflow.py` (~467 lines)

**Purpose:** AgentOS-aware workflow orchestration for candidate screening.

**Key Classes:**

- **`AgentOSCandidateWorkflow`** (lines 32-441)
  - Wraps Agno `Workflow` with AgentOS-aware session tracking
  - Defines 4-step workflow with step executors
  - Manages session state serialization (Pydantic → dict for SqliteDb)
  - Handles AgentOS workflow registration for control plane visibility

**Key Methods:**

- **`run_candidate_workflow()`** (lines 73-441)
  - Primary execution path for candidate screening
  - Coordinates 4-step pipeline: research → quality check → incremental search → assessment
  - Returns `AssessmentResult` with evidence-aware scores

**Design Patterns:**
- **Facade Pattern:** `AgentOSCandidateWorkflow` provides simplified interface to Agno workflow complexity
- **Session Management:** SqliteDb persistence for audit trails and AgentOS tracking

**Dependencies:**
- `demo.agents` (run_research, run_incremental_search, assess_candidate)
- `demo.screening_helpers` (check_research_quality)
- `demo.models.AssessmentResult`
- `agno.workflow.Workflow`, `agno.os.AgentOS`

---

### 3. `screening_helpers.py` (~427 lines)

**Purpose:** Business logic helpers for candidate screening workflow, including quality checks, scoring, candidate context extraction, and markdown report generation.

**Key Functions:**

- **`check_research_quality()`** (lines 42-77)
  - Simple sufficiency check: ≥3 citations + non-empty summary
  - Returns boolean for conditional incremental search
  - Counts unique citations by URL (stricter quality gate)

- **`calculate_overall_score()`** (lines 80-118)
  - **Evidence-aware:** Filters out `None` scores
  - Formula: `(sum(scored) / len(scored)) * 20`
  - Returns `None` if no dimensions scored

- **`reconstruct_research()`** (lines 20-39)
  - Converts dict representation to `ExecutiveResearchResult` Pydantic model
  - Handles both dict and instance inputs for flexibility

- **`validate_candidates()`** (lines 121-131)
  - Validates that candidates list is non-empty
  - Raises `ValueError` if empty

- **`extract_candidate_context()`** (lines 134-221)
  - Extracts candidate context from standardized webhook payload
  - Supports both new webhook format (direct keys) and legacy format (nested fields)
  - Returns dict with candidate_id, candidate_name, current_title, current_company, linkedin_url

- **`render_assessment_markdown_inline()`** (lines 250-292)
  - Renders concise markdown summary for Airtable inline field display
  - Includes candidate name, role, overall score, summary, dimension snapshot, must-haves
  - Truncates research summary to 240 characters

- **`render_screen_report()`** (lines 295-427)
  - Creates comprehensive markdown report combining assessment + research
  - Includes candidate snapshot, assessment summary, dimension details, must-haves, red/green flags, counterfactuals
  - Includes research summary, key achievements, career timeline, citations
  - Optionally includes role spec snapshot

**Dependencies:**
- `demo.models.AssessmentResult`, `DimensionScore`, `ExecutiveResearchResult`, `CandidateDict`, `MustHaveCheck`
- `demo.settings.settings` (for quality check configuration)

---

### 4. `agents.py` (~864 lines)

**Purpose:** Agent creation factories and workflow execution logic.

**Key Functions:**

**Agent Factories:**
- **`create_research_agent()`** (lines 107-156)
  - Returns Deep Research agent (`o4-mini-deep-research`)
  - **Critical:** No `output_schema` (Deep Research API returns markdown)
  - Loads prompt from YAML catalog via `get_prompt("deep_research")`

- **`create_research_parser_agent()`** (lines 159-174)
  - Converts markdown → `ExecutiveResearchResult`
  - Uses `gpt-5-mini` with `output_schema=ExecutiveResearchResult`
  - Respects evidence taxonomy ([FACT]/[OBSERVATION]/[HYPOTHESIS])

- **`create_incremental_search_agent()`** (lines 177-205)
  - Single-pass supplemental research
  - `gpt-5` with `max_tool_calls=2` (web_search tool)
  - Returns structured `ExecutiveResearchResult`

- **`create_assessment_agent()`** (lines 208-234)
  - Evaluates candidate against role spec
  - Uses `ReasoningTools` for explicit reasoning
  - Returns `AssessmentResult` with evidence-aware scores

**Workflow Execution:**
- **`run_research()`** (lines 237-341)
  - Two-agent pattern: Deep Research → Parser
  - Extracts citations from Deep Research API response
  - Merges parser output with raw citations
  - Computes confidence and gaps heuristics

- **`run_incremental_search()`** (lines 344-399)
  - Conditional supplemental research
  - Merges results with `merge_research_results()`
  - URL-based citation deduplication

- **`assess_candidate()`** (lines 486-537)
  - Formats research for assessment prompt
  - Computes overall score via `calculate_overall_score()` from `screening_helpers`
  - Stores role spec markdown for audit trail

**Design Patterns:**
- **Factory Pattern:** Agent creation functions return configured `Agent` instances
- **Strategy Pattern:** `use_deep_research` parameter (v1 only supports `True`)
- **Template Method:** Prompt building functions (`_build_parser_prompt`, `_build_assessment_prompt`)
- **Merger Pattern:** `merge_research_results()` combines original + supplemental with deduplication

**Dependencies:**
- `demo.models` (Pydantic schemas)
- `demo.prompts.get_prompt` (YAML catalog loader)
- `demo.settings.settings` (OpenAI timeout config)

---

### 5. `screening_service.py` (~462 lines)

**Purpose:** Shared workflow orchestration logic for processing screen records, including batch candidate processing, error handling, status updates, and markdown report generation.

**Key Classes:**

- **`LogSymbols`** (lines 24-30)
  - Dataclass for emoji logging glyphs (🔍, ✅, ❌)
  - Ensures consistent console output

- **`ScreenValidationError`** (lines 33-43)
  - Custom exception for Airtable payload validation failures
  - Includes field-level error details

**Key Functions:**

- **`process_screen_direct()`** (lines 381-463)
  - Canonical orchestration function invoked from FastAPI
  - Validates structured payload (no Airtable reads)
  - Loops through candidates, executes workflow, writes assessments
  - Handles partial failures gracefully and propagates `ScreenValidationError`
  - Coordinates with helper functions:
    - `_update_screen_status_and_log_webhook()` – status flip + automation log entry
    - `_process_candidate_batch()` – iterates candidates, catches per-candidate failures
    - `_log_completion_event()` – writes completion metadata back to Airtable
    - `_format_response_payload()` – consistent response contract for FastAPI

- **`_process_candidate_batch()`** (lines 153-308)
  - Processes each candidate in the batch
  - Generates markdown reports (assessment and research) via `screening_helpers`
  - Writes reports to `tmp/screen_reports/` directory temporarily
  - Uploads reports as attachments to Airtable assessment records
  - Cleans up temporary report files after upload
  - Handles per-candidate errors without stopping batch processing

- **`_write_report_file()`** (lines 35-52)
  - Persists markdown report to disk for Airtable attachment uploads
  - Creates `tmp/screen_reports/` directory if needed
  - Returns file path or None on failure

- **`_build_research_report_content()`** (lines 55-100)
  - Creates markdown content for research attachment file
  - Includes candidate snapshot, research summary, detailed markdown, key achievements, citations

**Report Generation:**
- Assessment reports: Generated via `screening_helpers.render_screen_report()`
- Research reports: Generated via `_build_research_report_content()`
- Inline markdown: Generated via `screening_helpers.render_assessment_markdown_inline()`
- Reports written to `tmp/screen_reports/` with format: `{screen_id}_{candidate_id}_{label}.md`
- Reports uploaded to Airtable as attachments, then cleaned up

**Design Patterns:**
- **Template Method:** Candidate processing loop with error isolation
- **Dependency Injection:** `candidate_runner` parameter allows AgentOS workflow injection
- **Error Isolation:** Individual candidate failures don't stop batch processing

**Dependencies:**
- `demo.airtable_client.AirtableClient`
- `demo.workflow.AgentOSCandidateWorkflow`
- `demo.models.AssessmentResult`, `ExecutiveResearchResult`, `CandidateDict`
- `demo.screening_helpers` (render functions, extract_candidate_context, validate_candidates)

---

### 6. `airtable_client.py` (~290 lines)

**Purpose:** Thin wrapper around pyairtable for Talent Signal schema.

**Key Class:**

- **`AirtableClient`** (lines 27-258)
  - Write-only client (no read/traversal methods)
  - Pre-initialized table handles for write operations only (screens, assessments, automation_log)
  - Handles base ID normalization (strips `/table` suffix)
  - **Architecture:** All read operations handled by Airtable formulas; Python receives complete payloads via webhook

**Key Methods:**

- **`write_assessment()`** (lines 73-132)
  - Persists `AssessmentResult` and `ExecutiveResearchResult` to Platform-Assessments table
  - **Writes consolidated JSON blobs:** Full `AssessmentResult` → "Assessment JSON" field, full `ExecutiveResearchResult` → "Research JSON" field
  - **Extracts key fields:** Overall Score, Overall Confidence, Topline Summary, Assessment Model, Assessment Timestamp, Research Model
  - **Conditionally writes:** Research Markdown Report (if `research.research_markdown_raw` exists)
  - Links to screen and candidate records
  - **Note:** Granular JSON fields (Dimension Scores JSON, Red Flags JSON, etc.) exist in schema but are NOT populated - all data stored in consolidated blobs

- **`update_screen_status()`** (lines 357-399)
  - Updates screen status field
  - Optionally logs errors to `Automation_Log` table

- **`log_automation_event()`** (lines 295-355)
  - Writes audit trail entries
  - Links to screens and assessments
  - Captures webhook payloads and error messages

**Design Patterns:**
- **Write-Only Pattern:** Zero traversal API calls - all data arrives via structured webhook payloads
- **Facade Pattern:** Simplifies pyairtable API surface for write operations
- **Repository Pattern:** Encapsulates Airtable table writes only

**Dependencies:**
- `pyairtable.Api` and `pyairtable.Table`
- `demo.models.AssessmentResult`, `ExecutiveResearchResult`

---

### 7. `models.py` (~304 lines)

**Purpose:** Pydantic schemas for structured outputs.

**Key Models:**

- **`Citation`** (lines 13-19)
  - URL, title, snippet, optional relevance note

- **`CareerEntry`** (lines 22-29)
  - Company, role, dates, achievements

- **`ExecutiveResearchResult`** (lines 32-65)
  - Comprehensive research artifact
  - Career timeline, expertise, citations
  - Confidence levels and gaps
  - Raw markdown preserved for audit

- **`DimensionScore`** (lines 67-85)
  - **Evidence-aware scoring:** `score: Optional[int]` (None = Unknown)
  - Evidence level, confidence, reasoning, citations
  - **Critical:** Never use 0 or NaN for missing scores

- **`AssessmentResult`** (lines 95-118)
  - Overall score (computed), dimension scores
  - Must-haves, red flags, green flags
  - Summary, counterfactuals
  - Metadata (timestamp, model, role spec used)

**Design Patterns:**
- **Data Transfer Object (DTO):** Pydantic models for API boundaries
- **Validation:** Field constraints (`ge=1, le=5` for scores)
- **Serialization:** `model_dump_json()` for Airtable storage

---

### 8. `settings.py` (~120 lines)

**Purpose:** Environment variable loading and typed configuration.

**Key Classes:**

- **`AppConfig`:** Application-level settings (name, env, log level)
- **`OpenAIConfig`:** API key, timeout, deep research toggle
- **`AirtableConfig`:** API key, base ID (with normalization)
- **`ServerConfig`:** Host, port (FastAPI/AgentOS configuration)
- **`AgentOSConfig`:** Security key (optional)
- **`QualityCheckConfig`:** Quality thresholds (min citations)

- **`Settings`:** Container class aggregating all config sections

**Design Patterns:**
- **Configuration Object:** Centralized settings with type safety
- **Environment Variable Mapping:** Pydantic Settings with aliases
- **Singleton Pattern:** Global `settings` instance

---

### 7. `prompts/` Directory

**Purpose:** Centralized YAML prompt catalog for code-free prompt iteration.

**Files:**

- **`catalog.yaml`** (139 lines)
  - 4 prompt definitions: `deep_research`, `research_parser`, `incremental_search`, `assessment`
  - Structured fields: `description`, `instructions`, `markdown` flag
  - Evidence taxonomy encoded in Deep Research prompt ([FACT]/[OBSERVATION]/[HYPOTHESIS])

- **`library.py`** (81 lines)
  - **`PromptContext`** dataclass: Materialized prompt values
  - **`get_prompt(name, **kwargs)`**: Loader with placeholder support
  - **`as_agent_kwargs()`**: Converts to Agno `Agent` constructor kwargs

**Design Patterns:**
- **Catalog Pattern:** Externalized prompts in version-controlled YAML
- **Factory Pattern:** `get_prompt()` creates `PromptContext` instances
- **Adapter Pattern:** `as_agent_kwargs()` bridges catalog → Agno API

**Benefits:**
- Prompts editable without code changes
- Version control for prompt evolution
- Placeholder support for dynamic content
- Type-safe integration with agent factories

---

## Design Patterns & Decisions

### 1. Evidence-Aware Scoring

**Principle:** Explicitly handle "Unknown" when public data is insufficient.

**Implementation:**

```67:85:demo/models.py
class DimensionScore(BaseModel):
    """Evidence-aware dimension score for a single evaluation criterion."""

    dimension: str

    # Scoring (1-5 scale with None for Unknown)
    score: Optional[int] = Field(None, ge=1, le=5)
    # None (Python) / null (JSON) = Unknown / Insufficient evidence
    # DO NOT use NaN or 0 - always use None for missing scores

    # Evidence Quality
    evidence_level: Literal["High", "Medium", "Low"]  # From role spec
    confidence: Literal["High", "Medium", "Low"]  # LLM self-assessment

    # Reasoning & Evidence
    reasoning: str  # 1-3 sentences explaining the score
    evidence_quotes: list[str] = Field(default_factory=list)
    citation_urls: list[str] = Field(default_factory=list)
```

**Scoring Logic:**

```754:792:demo/agents.py
def calculate_overall_score(
    dimension_scores: list[DimensionScore],
) -> Optional[float]:
    """Calculate a candidate's overall score based on scored dimensions.

    Args:
        dimension_scores: Dimension-level outputs from ``AssessmentResult``.

    Returns:
        Optional[float]: Score on a 0-100 scale or ``None`` if no dimensions
        were scorable.

    Example:
        >>> scores = [
        ...     DimensionScore(
        ...         dimension="Leadership",
        ...         score=4,
        ...         evidence_level="High",
        ...         confidence="Medium",
        ...         reasoning="",
        ...     ),
        ...     DimensionScore(
        ...         dimension="Strategy",
        ...         score=None,
        ...         evidence_level="Medium",
        ...         confidence="Low",
        ...         reasoning="",
        ...     ),
        ... ]
        >>> calculate_overall_score(scores)
        80.0
    """

    scored = [score.score for score in dimension_scores if score.score is not None]

    if not scored:
        return None

    return (sum(scored) / len(scored)) * 20
```

**Rationale:**
- Prevents false confidence from forced scores
- Distinguishes "no evidence" from "negative evidence"
- Enables downstream filtering of incomplete assessments
- Aligns with investor/board decision-making (explicit uncertainty)

---

### 2. Quality-Gated Research

**Principle:** Conditional incremental search only when initial research is insufficient.

**Implementation:**

```723:751:demo/agents.py
def check_research_quality(research: ExecutiveResearchResult) -> bool:
    """Determine if research meets the minimum sufficiency threshold.

    Args:
        research: Research payload to evaluate.

    Returns:
        bool: ``True`` if there are ≥3 unique citations and a non-empty summary.

    Example:
        >>> research = ExecutiveResearchResult(
        ...     exec_name="Jamie",
        ...     current_role="COO",
        ...     current_company="Acme",
        ...     research_summary="Summary",
        ...     citations=[
        ...         Citation(url="https://1", title="One", snippet=""),
        ...         Citation(url="https://2", title="Two", snippet=""),
        ...         Citation(url="https://3", title="Three", snippet=""),
        ...     ],
        ... )
        >>> check_research_quality(research)
        True
    """

    summary_present = bool(research.research_summary.strip())
    unique_citations = {citation.url for citation in research.citations if citation.url}

    return summary_present and len(unique_citations) >= 3
```

**Workflow Integration:**

```401:450:demo/agentos_app.py
    def _incremental_search_step(
        self, step_input: StepInput, run_context: RunContext
    ) -> StepOutput:
        if run_context.session_state is None:
            run_context.session_state = {}

        state = run_context.session_state.get("workflow_data", {})
        research_data = state.get("research")
        if research_data is None:
            raise RuntimeError("Missing research payload before incremental search")
        if state.get("quality_ok"):
            self.logger.info(
                "%s Skipping incremental search for %s (quality threshold met)",
                LOG_SUCCESS,
                state.get("candidate_name", "candidate"),
            )
            return StepOutput(
                step_name="incremental_search",
                executor_name="run_incremental_search",
                success=True,
                content={"skipped": True},
            )

        self.logger.info(
            "%s Running incremental search for %s",
            LOG_SEARCH,
            state.get("candidate_name", "candidate"),
        )
        # Reconstruct research object from dict if needed
        if isinstance(research_data, dict):
            from demo.models import ExecutiveResearchResult

            research = ExecutiveResearchResult.model_validate(research_data)
        else:
            research = research_data

        merged_research = run_incremental_search(
            candidate_name=state.get("candidate_name", "candidate"),
            initial_research=research,
            quality_gaps=research.gaps,
            role_spec_markdown=state.get("role_spec_markdown", ""),
        )
        # Store as dict for JSON serialization (SqliteDb persistence)
        state["research"] = merged_research.model_dump()
        return StepOutput(
            step_name="incremental_search",
            executor_name="run_incremental_search",
            success=True,
            content={"citations": len(merged_research.citations)},
        )
```

**Rationale:**
- Cost optimization (avoid unnecessary API calls)
- Speed (skip incremental search when quality threshold met)
- Focused remediation (target specific gaps, not blanket re-research)

---

### 3. Workflow Orchestration

**Principle:** AgentOS-aware workflow with proper session tracking and state persistence.

**Architecture:**

```88:127:demo/agentos_app.py
class AgentOSCandidateWorkflow:
    """AgentOS-aware workflow that runs the four candidate screening steps."""

    def __init__(self, log: logging.Logger, agent_os: AgentOS | None = None) -> None:
        self.logger = log
        self.agent_os = agent_os
        db_path = Path("tmp") / "agno_sessions.db"
        db_path.parent.mkdir(parents=True, exist_ok=True)
        self.workflow = Workflow(
            id="talent-signal-candidate-workflow",
            name="Talent Signal Candidate Workflow",
            description="Deep research → quality check → optional incremental search → assessment",
            db=SqliteDb(
                db_file=str(db_path),
                session_table="agno_sessions",  # Explicit table name for AgentOS tracking
            ),
            stream_events=True,
            steps=[
                Step(
                    name="deep_research",
                    description="Run Deep Research agent",
                    executor=self._deep_research_step,
                ),
                Step(
                    name="quality_check",
                    description="Evaluate research sufficiency",
                    executor=self._quality_check_step,
                ),
                Step(
                    name="incremental_search",
                    description="Run incremental search when the quality gate fails",
                    executor=self._incremental_search_step,
                ),
                Step(
                    name="assessment",
                    description="Score the candidate against the role spec",
                    executor=self._assessment_step,
                ),
            ],
        )
```

**Session State Management:**

```324:365:demo/agentos_app.py
    def _deep_research_step(
        self, step_input: StepInput, run_context: RunContext
    ) -> StepOutput:
        # Initialize session state if needed
        if run_context.session_state is None:
            run_context.session_state = {}

        # Initialize workflow state structure
        if "workflow_data" not in run_context.session_state:
            run_context.session_state["workflow_data"] = {}

        state = run_context.session_state["workflow_data"]

        # Extract input data
        input_data = step_input.input if isinstance(step_input.input, dict) else {}
        candidate = input_data.get("candidate", {})
        context = self._extract_candidate_context(candidate)

        # Store initial state
        state.setdefault("screen_id", input_data.get("screen_id"))
        state.setdefault("candidate", candidate)
        state.setdefault("role_spec_markdown", input_data.get("role_spec_markdown", ""))
        state.update(context)

        self.logger.info(
            "%s Starting deep research for %s (%s at %s)",
            LOG_SEARCH,
            context["candidate_name"],
            context["current_title"],
            context["current_company"],
        )
        research = run_research(
            candidate_name=context["candidate_name"],
            current_title=context["current_title"],
            current_company=context["current_company"],
            linkedin_url=context["linkedin_url"],
        )
        # Store as dict for JSON serialization (SqliteDb persistence)
        state["research"] = research.model_dump()
        return StepOutput(
            step_name="deep_research",
            executor_name="run_research",
            success=True,
            content={"citations": len(research.citations)},
        )
```

**Rationale:**
- **SqliteDb Persistence:** Audit trail for debugging and compliance
- **Pydantic → Dict Serialization:** JSON-compatible state for database storage
- **AgentOS Integration:** Workflow visible in control plane UI for monitoring
- **Step Executors:** Clear separation of workflow definition vs. execution logic

---

### 4. Prompt Management System

**Principle:** Centralized YAML catalog enables code-free prompt iteration.

**Catalog Structure:**

```6:45:demo/prompts/catalog.yaml
deep_research:
  description: >
    You are the Talent Signal Deep Research agent, an evidence-first OSINT profiler
    for executive screening.
  instructions: |
    You investigate executive candidates for FirstMark Capital portfolio searches.

    Your goals:
    - Build an evidence-backed dossier of the executive's background and track record.
    - Surface patterns in how they lead, communicate, and make decisions.
    - Explicitly document remaining unknowns and low-confidence areas.

    Distinguish clearly between:
    - [FACT – high/medium/low]: Verifiable roles, dates, companies, deals, quotes with citations.
    - [OBSERVATION – high/medium/low]: Patterns inferred from multiple facts (leadership style,
      decision-making, communication).
    - [HYPOTHESIS – low]: Supported but not directly confirmed inferences; use sparingly and
      clearly caveat.

    Research process (do not show your queries):
    - Prioritize LinkedIn, company sites, reputable news, funding databases, conference talks,
      and podcasts.
    - Note recency in brackets (e.g., "[FACT – medium, based on 2021 interview]").
    - If evidence is thin, say so and lower your confidence rather than guessing.

    Structure your response with these markdown sections:
    - Executive Summary
    - Career Timeline
    - Leadership & Operating Style
    - Domain Expertise
    - Stage & Sector Experience
    - Key Achievements
    - Public Presence
    - Gaps in Public Evidence (include what you looked for but did not find)

    In every section:
    - Tie statements to specific citations where possible.
    - Prefer fewer, higher-quality [HYPOTHESIS] items over speculation.
    - Do not output JSON; return a readable markdown report only.
  markdown: true
```

**Loader Implementation:**

```63:80:demo/prompts/library.py
def get_prompt(name: str, **format_kwargs: Any) -> PromptContext:
    """Return prompt context for ``name`` with optional placeholder values."""

    try:
        entry = _CATALOG_DATA[name]
    except KeyError as exc:  # pragma: no cover - developer error path
        raise KeyError(f"Prompt '{name}' not found in catalog {_CATALOG_PATH}") from exc

    return PromptContext(
        name=name,
        description=_format_value(entry.get("description"), format_kwargs),
        instructions=_format_value(entry.get("instructions"), format_kwargs),
        expected_output=_format_value(entry.get("expected_output"), format_kwargs),
        additional_context=_format_value(
            entry.get("additional_context"), format_kwargs
        ),
        markdown=entry.get("markdown"),
    )
```

**Agent Integration:**

```107:156:demo/agents.py
def create_research_agent(use_deep_research: bool = True) -> Agent:
    """Create research agent with flexible execution mode.

    Args:
        use_deep_research: When ``True``, configure the agent with
            ``o4-mini-deep-research``. Fast mode (``False``) is deferred to
            Phase 2.

    Returns:
        Agent: Configured Deep Research agent instance.

    Raises:
        NotImplementedError: If ``use_deep_research`` is ``False`` during the
            minimal v1 implementation.

    Example:
        >>> agent = create_research_agent()
        >>> agent.model.id
        'o4-mini-deep-research'

    Notes:
        - v1 implementation only requires ``use_deep_research=True``
        - Fast mode (gpt-5 + web_search) is future enhancement
        - Deep Research returns markdown (NOT structured output)
        - DO NOT use ``output_schema`` with Deep Research models
    """
    if not use_deep_research:
        raise NotImplementedError(
            "Fast mode (gpt-5 + web_search) is Phase 2+. "
            "v1.0-minimal only supports Deep Research mode."
        )

    from demo.settings import settings

    prompt = get_prompt("deep_research")

    return Agent(
        name="Deep Research Agent",
        model=OpenAIResponses(
            id="o4-mini-deep-research",
            max_tool_calls=1,
            timeout=settings.openai.timeout,
        ),
        # CRITICAL: NO output_schema - Deep Research API doesn't support structured outputs
        **prompt.as_agent_kwargs(),
        add_datetime_to_context=True,
        exponential_backoff=True,
        retries=2,
        delay_between_retries=1,
    )
```

**Rationale:**
- **Version Control:** Prompts tracked in git, enabling A/B testing and rollback
- **Non-Developers:** Product/design can iterate prompts without code changes
- **Consistency:** Single source of truth for prompt definitions
- **Evidence Taxonomy:** Encoded in Deep Research prompt ([FACT]/[OBSERVATION]/[HYPOTHESIS])

---

### 5. Error Handling Strategy

**Principle:** Graceful degradation with detailed error logging and partial failure support.

**Validation Errors:**

```573:593:demo/agentos_app.py
@fastapi_app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Normalize FastAPI validation errors to match expected error response schema."""

    field_errors: dict[str, str] = {}
    for error in exc.errors():
        loc = error.get("loc", [])
        field_name = next(
            (item for item in reversed(loc) if isinstance(item, str)),
            "body",
        )
        field_errors[str(field_name)] = error.get("msg", "Invalid value")

    payload = {
        "error": "validation_error",
        "message": "Invalid request payload.",
        "fields": field_errors or None,
    }
    return JSONResponse(status_code=400, content=payload)
```

**Runtime Errors:**

```538:556:demo/agentos_app.py
def _server_error_response(screen_id: str, exc: Exception) -> JSONResponse:
    """Format a consistent JSON error response for server errors."""

    error_message = str(exc) or exc.__class__.__name__
    logger.exception(
        "%s Critical failure while processing screen %s",
        LOG_ERROR,
        screen_id,
    )
    _mark_screen_failed(screen_id, error_message)
    return JSONResponse(
        status_code=500,
        content={
            "error": "server_error",
            "message": "Unexpected server error while processing screen.",
            "screen_id": screen_id,
            "details": error_message,
        },
    )
```

**Partial Failures:**

```137:221:demo/screening_service.py
    results: list[dict[str, Any]] = []
    errors: list[dict[str, str]] = []

    for candidate in candidate_records:
        candidate_id = (
            candidate.get("id")
            or candidate.get("record_id")
            or candidate.get("fields", {}).get("id")
        )
        if candidate_id is None:
            logger.error(
                "%s Candidate record missing Airtable ID; skipping record.",
                glyphs.error,
            )
            errors.append(
                {
                    "candidate_id": "unknown",
                    "error": "Candidate record missing Airtable ID.",
                }
            )
            continue

        candidate_id_str = str(candidate_id)
        candidate_name = (
            candidate.get("fields", {}).get("Full Name")
            or candidate.get("fields", {}).get("Name")
            or candidate_id_str
        )

        # Inject company name from Screen's rollup field
        # (People.Current Company is a record link, not useful for prompts)
        candidate_company = screen_record.get("fields", {}).get("Candidate Company", "")
        if candidate_company and "fields" in candidate:
            candidate["fields"]["Company"] = candidate_company

        logger.debug(
            "📦 PROCESSING CANDIDATE (ID: %s, Name: %s):\n%s",
            candidate_id_str,
            candidate_name,
            json.dumps(candidate, indent=2, default=str),
        )

        try:
            assessment = run_candidate(
                candidate_data=candidate,
                role_spec_markdown=str(role_spec_markdown),
                screen_id=screen_id,
            )
            assessment_record_id = airtable.write_assessment(
                screen_id=screen_id,
                candidate_id=candidate_id_str,
                assessment=assessment,
                role_spec_markdown=str(
                    role_spec_markdown
                ),  # NEW: Capture Spec for audit
            )
            results.append(
                {
                    "candidate_id": candidate_id_str,
                    "assessment_id": assessment_record_id,
                    "overall_score": assessment.overall_score,
                    "confidence": assessment.overall_confidence,
                    "summary": assessment.summary,
                    "assessed_at": assessment.assessment_timestamp.isoformat(),
                }
            )
            logger.info(
                "%s Candidate %s screened successfully (score=%s)",
                glyphs.success,
                candidate_name,
                assessment.overall_score,
            )
        except Exception as exc:  # pragma: no cover - depends on downstream errors
            logger.error(
                "%s Candidate %s failed during screening: %s",
                glyphs.error,
                candidate_name,
                exc,
            )
            errors.append(
                {
                    "candidate_id": candidate_id_str,
                    "error": str(exc),
                }
            )
```

**Rationale:**
- **Field-Level Validation:** Clear error messages for Airtable automation debugging
- **Error Isolation:** Individual candidate failures don't stop batch processing
- **Audit Trail:** Errors logged to Airtable `Automation_Log` table
- **Status Updates:** Screen status updated to "Complete" even with partial failures

---

## Data Models

### Model Hierarchy

```
Citation
  └─ Used by: ExecutiveResearchResult.citations

CareerEntry
  └─ Used by: ExecutiveResearchResult.career_timeline

ExecutiveResearchResult
  ├─ Citations: list[Citation]
  ├─ Career Timeline: list[CareerEntry]
  ├─ Metadata: research_timestamp, research_model, research_confidence
  └─ Gaps: list[str]

DimensionScore
  ├─ score: Optional[int] (1-5, None = Unknown)
  ├─ evidence_level: Literal["High", "Medium", "Low"]
  ├─ confidence: Literal["High", "Medium", "Low"]
  └─ Evidence: reasoning, evidence_quotes, citation_urls

MustHaveCheck
  ├─ requirement: str
  ├─ met: bool
  └─ evidence: Optional[str]

AssessmentResult
  ├─ Overall: overall_score (Optional[float]), overall_confidence
  ├─ Dimensions: list[DimensionScore]
  ├─ Requirements: list[MustHaveCheck]
  ├─ Flags: red_flags_detected, green_flags
  ├─ Qualitative: summary, counterfactuals
  └─ Metadata: assessment_timestamp, assessment_model, role_spec_used
```

### Key Validation Rules

**DimensionScore:**
- `score` must be `None` or `1 <= score <= 5`
- `None` explicitly represents "Unknown / Insufficient evidence"
- Never use `0` or `NaN` for missing scores

**AssessmentResult:**
- `overall_score` computed from dimension scores (filtering `None`)
- Formula: `(sum(scored) / len(scored)) * 20` (0-100 scale)
- Returns `None` if no dimensions scored

**ExecutiveResearchResult:**
- `research_summary` required (non-empty string)
- `citations` list may be empty but should have ≥3 for quality threshold
- `gaps` list documents missing information explicitly

---

## Workflow Execution

### Step-by-Step Flow

**Step 1: Deep Research**

```324:365:demo/agentos_app.py
    def _deep_research_step(
        self, step_input: StepInput, run_context: RunContext
    ) -> StepOutput:
        # Initialize session state if needed
        if run_context.session_state is None:
            run_context.session_state = {}

        # Initialize workflow state structure
        if "workflow_data" not in run_context.session_state:
            run_context.session_state["workflow_data"] = {}

        state = run_context.session_state["workflow_data"]

        # Extract input data
        input_data = step_input.input if isinstance(step_input.input, dict) else {}
        candidate = input_data.get("candidate", {})
        context = self._extract_candidate_context(candidate)

        # Store initial state
        state.setdefault("screen_id", input_data.get("screen_id"))
        state.setdefault("candidate", candidate)
        state.setdefault("role_spec_markdown", input_data.get("role_spec_markdown", ""))
        state.update(context)

        self.logger.info(
            "%s Starting deep research for %s (%s at %s)",
            LOG_SEARCH,
            context["candidate_name"],
            context["current_title"],
            context["current_company"],
        )
        research = run_research(
            candidate_name=context["candidate_name"],
            current_title=context["current_title"],
            current_company=context["current_company"],
            linkedin_url=context["linkedin_url"],
        )
        # Store as dict for JSON serialization (SqliteDb persistence)
        state["research"] = research.model_dump()
        return StepOutput(
            step_name="deep_research",
            executor_name="run_research",
            success=True,
            content={"citations": len(research.citations)},
        )
```

- Executes `run_research()` which calls Deep Research API + Parser Agent
- Stores research as dict in session state for persistence
- Returns citation count for logging

**Step 2: Quality Check**

```367:399:demo/agentos_app.py
    def _quality_check_step(
        self, step_input: StepInput, run_context: RunContext
    ) -> StepOutput:
        if run_context.session_state is None:
            run_context.session_state = {}

        state = run_context.session_state.get("workflow_data", {})
        research_data = state.get("research")
        if research_data is None:
            raise RuntimeError("Deep research step must run before quality check")

        # Reconstruct research object from dict if needed
        if isinstance(research_data, dict):
            from demo.models import ExecutiveResearchResult

            research = ExecutiveResearchResult.model_validate(research_data)
        else:
            research = research_data

        quality_ok = check_research_quality(research)
        state["quality_ok"] = quality_ok
        self.logger.info(
            "%s Research quality check for %s → %s",
            LOG_SEARCH,
            state.get("candidate_name", "candidate"),
            "pass" if quality_ok else "fail",
        )
        return StepOutput(
            step_name="quality_check",
            executor_name="check_research_quality",
            success=True,
            content={"quality_ok": quality_ok},
        )
```

- Validates research sufficiency (≥3 citations + non-empty summary)
- Stores `quality_ok` boolean for conditional step execution

**Step 3: Incremental Search (Conditional)**

```401:450:demo/agentos_app.py
    def _incremental_search_step(
        self, step_input: StepInput, run_context: RunContext
    ) -> StepOutput:
        if run_context.session_state is None:
            run_context.session_state = {}

        state = run_context.session_state.get("workflow_data", {})
        research_data = state.get("research")
        if research_data is None:
            raise RuntimeError("Missing research payload before incremental search")
        if state.get("quality_ok"):
            self.logger.info(
                "%s Skipping incremental search for %s (quality threshold met)",
                LOG_SUCCESS,
                state.get("candidate_name", "candidate"),
            )
            return StepOutput(
                step_name="incremental_search",
                executor_name="run_incremental_search",
                success=True,
                content={"skipped": True},
            )

        self.logger.info(
            "%s Running incremental search for %s",
            LOG_SEARCH,
            state.get("candidate_name", "candidate"),
        )
        # Reconstruct research object from dict if needed
        if isinstance(research_data, dict):
            from demo.models import ExecutiveResearchResult

            research = ExecutiveResearchResult.model_validate(research_data)
        else:
            research = research_data

        merged_research = run_incremental_search(
            candidate_name=state.get("candidate_name", "candidate"),
            initial_research=research,
            quality_gaps=research.gaps,
            role_spec_markdown=state.get("role_spec_markdown", ""),
        )
        # Store as dict for JSON serialization (SqliteDb persistence)
        state["research"] = merged_research.model_dump()
        return StepOutput(
            step_name="incremental_search",
            executor_name="run_incremental_search",
            success=True,
            content={"citations": len(merged_research.citations)},
        )
```

- Skips if `quality_ok = True`
- Otherwise executes `run_incremental_search()` with gap-targeted queries
- Merges results and updates session state

**Step 4: Assessment**

```452:493:demo/agentos_app.py
    def _assessment_step(
        self, step_input: StepInput, run_context: RunContext
    ) -> StepOutput:
        if run_context.session_state is None:
            run_context.session_state = {}

        state = run_context.session_state.get("workflow_data", {})
        research_data = state.get("research")
        if research_data is None:
            raise RuntimeError("Missing research payload before assessment")

        # Reconstruct research object from dict if needed
        if isinstance(research_data, dict):
            from demo.models import ExecutiveResearchResult

            research = ExecutiveResearchResult.model_validate(research_data)
        else:
            research = research_data

        self.logger.info(
            "%s Starting assessment for %s",
            LOG_SEARCH,
            state.get("candidate_name", "candidate"),
        )
        assessment = assess_candidate(
            research=research,
            role_spec_markdown=state.get("role_spec_markdown", ""),
        )
        # Store as dict for JSON serialization (SqliteDb persistence)
        state["assessment"] = assessment.model_dump()
        self.logger.info(
            "%s Assessment complete for %s (overall_score=%s)",
            LOG_SUCCESS,
            state.get("candidate_name", "candidate"),
            assessment.overall_score,
        )
        return StepOutput(
            step_name="assessment",
            executor_name="assess_candidate",
            success=True,
            content={"assessment": assessment.model_dump()},
        )
```

- Executes `assess_candidate()` with research + role spec
- Computes overall score from dimension scores
- Returns assessment in StepOutput content

### State Management

**Session State Structure:**

```python
session_state = {
    "workflow_data": {
        "screen_id": "recXXXX",
        "candidate": {...},
        "candidate_name": "Jane Doe",
        "current_title": "CFO",
        "current_company": "Acme Corp",
        "role_spec_markdown": "# Role Spec\n...",
        "research": {...},  # ExecutiveResearchResult as dict
        "quality_ok": True,
        "assessment": {...}  # AssessmentResult as dict
    }
}
```

**Persistence:**
- SqliteDb at `tmp/agno_sessions.db`
- Session table: `agno_sessions`
- Pydantic models serialized to dict for JSON compatibility
- Reconstructed via `model_validate()` when reading from state

---

## Integration Architecture

### Airtable Integration

**Client Design:**

```27:77:demo/airtable_client.py
class AirtableClient:
    """Typed wrapper around pyairtable for the demo's Airtable schema."""

    SCREENS_TABLE: Final[str] = "Platform-Screens"
    PEOPLE_TABLE: Final[str] = "People"
    ROLE_SPECS_TABLE: Final[str] = "Platform-Role_Specs"
    ASSESSMENTS_TABLE: Final[str] = "Platform-Assessments"
    SEARCHES_TABLE: Final[str] = "Platform-Searches"
    PORTCOS_TABLE: Final[str] = "Portcos"
    PORTCO_ROLES_TABLE: Final[str] = "Platform-Portco_Roles"
    AUTOMATION_LOG_TABLE: Final[str] = "Operations-Automation_Log"

    def __init__(self, api_key: str, base_id: str) -> None:
        """Instantiate the Airtable client and table handles.

        Args:
            api_key: Airtable personal access token with base permissions.
            base_id: Base identifier (``appXXXX``) optionally containing a
                trailing ``/table`` suffix from Airtable's UI URLs.

        Raises:
            ValueError: If either credential is blank.
        """

        api_key = api_key.strip()
        base_id = base_id.strip()
        if not api_key:
            raise ValueError("Airtable API key is required")
        if not base_id:
            raise ValueError("Airtable base ID is required")

        # Airtable often appends the table ID to the base ID in URLs such as
        # ``appXXXXXXXX/tblYYYYYYYY``; only the base prefix is needed here.
        clean_base_id = base_id.split("/")[0]

        self.api_key: str = api_key
        self.base_id: str = clean_base_id
        self.api: Api = Api(api_key)

        # Precompute table handles for the main workflow tables so downstream
        # CRUD methods can reuse them without recreating Table instances.
        self.screens: Table = self.api.table(self.base_id, self.SCREENS_TABLE)
        self.people: Table = self.api.table(self.base_id, self.PEOPLE_TABLE)
        self.role_specs: Table = self.api.table(self.base_id, self.ROLE_SPECS_TABLE)
        self.assessments: Table = self.api.table(self.base_id, self.ASSESSMENTS_TABLE)
        self.searches: Table = self.api.table(self.base_id, self.SEARCHES_TABLE)
        self.portcos: Table = self.api.table(self.base_id, self.PORTCOS_TABLE)
        self.portco_roles: Table = self.api.table(self.base_id, self.PORTCO_ROLES_TABLE)
        self.automation_log: Table = self.api.table(
            self.base_id, self.AUTOMATION_LOG_TABLE
        )
```

**Spec Resolution:**

```134:146:demo/airtable_client.py
        # Spec content resolution:
        # - Master Role Spec Content: Formula field that resolves to the active Spec
        # - Admin-Automation Spec Content Snapshot: Immutable snapshot captured at screening start
        #
        # Workflow: Automation copies Master Role Spec Content → Admin-Automation Spec Content Snapshot
        # when Status changes to "Processing", then code reads the snapshot.
        #
        # Priority:
        # 1. Admin-Automation Spec Content Snapshot (if populated by automation)
        # 2. Master Role Spec Content (fallback if snapshot not yet populated)
        role_spec_markdown: Optional[str] = fields.get(
            "Admin-Automation Spec Content Snapshot"
        ) or fields.get("Master Role Spec Content")
```

**Rationale:**
- **Immutable Specs:** Snapshot ensures spec doesn't change mid-screening
- **Backward Compatibility:** Falls back to formula field or linked Role_Spec
- **Pre-initialized Tables:** Performance optimization (reuse Table instances)

---

### AgentOS Runtime Integration

**Registration:**

```622:655:demo/agentos_app.py
# Register AgentOS runtime with existing workflow + agents.
agent_os = AgentOS(
    id="talent-signal-os",
    description="FirstMark Talent Signal AgentOS runtime",
    agents=[
        create_research_agent(),
        create_research_parser_agent(),
        create_incremental_search_agent(),
        create_assessment_agent(),
    ],
    workflows=[candidate_workflow_runner.workflow],
    base_app=fastapi_app,
)

# Update workflow runner with AgentOS reference for proper session tracking
# This ensures workflows executed through run_candidate_workflow are tracked by AgentOS
# and visible in the AgentOS control plane UI
candidate_workflow_runner.agent_os = agent_os

logger.info(
    "%s AgentOS initialized with workflow %s (id: %s)",
    LOG_SUCCESS,
    candidate_workflow_runner.workflow.name,
    candidate_workflow_runner.workflow.id,
)

# Log security key status (security is handled via middleware/environment, not constructor)
if settings.agentos.security_key:
    logger.info(
        "%s AgentOS security key configured (use middleware for bearer token auth)",
        LOG_SEARCH,
    )

app = agent_os.get_app()
```

**Benefits:**
- **Control Plane UI:** Real-time workflow monitoring and session inspection
- **Agent Registration:** All agents visible in AgentOS dashboard
- **Session Tracking:** Workflow runs tracked with proper session IDs
- **FastAPI Integration:** Base app extended with AgentOS routes

---

### Webhook Endpoint Design

**Request Validation:**

```202:271:demo/models.py
class ScreenWebhookPayload(BaseModel):
    """Complete screening payload from Airtable with structured nested objects."""

    screen_slug: ScreenSlugData = Field(..., description="Screen record data")

    @property
    def screen_id(self) -> str:
        return self.screen_slug.screen_id

    @property
    def spec_markdown(self) -> str:
        return self.screen_slug.role_spec_slug.role_spec.role_spec_content

    def get_candidates(self) -> list[CandidateDict]:
        """Returns normalized candidate dicts with guaranteed keys."""
        ...
```

**Endpoint Handler:**

```196:252:demo/agentos_app.py
@fastapi_app.post("/screen", response_model=None, status_code=202)
def screen_endpoint(
    payload: ScreenWebhookPayload,
    background_tasks: BackgroundTasks,
    _auth: None = Depends(verify_bearer_token),
) -> dict[str, Any] | JSONResponse:
    """FastAPI implementation of the Airtable webhook entrypoint.

    Processes screening webhook with pre-assembled Airtable data.
    Returns 202 Accepted immediately and processes workflow in background.
    """

    try:
        candidates = payload.get_candidates()
        background_tasks.add_task(
            process_screen_direct,
            screen_id=payload.screen_id,
            role_spec_markdown=payload.spec_markdown,
            candidates=candidates,
            custom_instructions=payload.custom_instructions,
            airtable=airtable_client,
            logger=logger,
            symbols=SCREEN_LOG_SYMBOLS,
            candidate_runner=candidate_workflow_runner.run_candidate_workflow,
        )
        return {
            "status": "accepted",
            "message": "Screen workflow started",
            "screen_id": payload.screen_id,
            "candidates_queued": len(candidates),
        }
    except ValueError as exc:
        return JSONResponse(
            status_code=400,
            content={
                "error": "validation_error",
                "message": str(exc),
                "fields": None,
            },
        )
    except ScreenValidationError as exc:
        return JSONResponse(
            status_code=400,
            content={
                "error": "validation_error",
                "message": exc.message,
                "fields": exc.field_errors or None,
            },
        )
    except Exception as exc:  # pragma: no cover - runtime error path
        return _server_error_response(payload.screen_id, exc)
```

**Response Format & Background Execution:**

- FastAPI responds immediately with `{"status": "accepted", ...}` and HTTP 202.
- Candidate processing happens asynchronously inside `process_screen_direct()`; `_format_response_payload()` formats completion logs for observability but is **not** returned to Airtable.
- Airtable automation reads success/failure from the HTTP status only; all assessment details arrive via write operations in `demo/airtable_client.py`.

**Rationale:**
- **Structured Payload Validation:** All role spec + candidate context arrives via `ScreenWebhookPayload`, eliminating Airtable reads.
- **Delegation:** Endpoint delegates to `screening_service.process_screen_direct()` for determinism and testability.
- **Non-Blocking Webhook:** Background tasks prevent Airtable timeouts even when research takes several minutes.
- **Consistent Responses:** Standardized JSON error format for Airtable automation
- **Partial Success:** Returns summary even when some candidates fail

---

## Key Implementation Details

### 1. Two-Agent Research Pattern

**Deep Research → Parser:**

```237:341:demo/agents.py
def run_research(
    candidate_name: str,
    current_title: str,
    current_company: str,
    linkedin_url: Optional[str] = None,
    use_deep_research: bool = True,
) -> ExecutiveResearchResult:
    """Execute research on candidate and return structured results.

    Args:
        candidate_name: Executive full name.
        current_title: Current job title.
        current_company: Current company name.
        linkedin_url: LinkedIn profile URL (optional).
        use_deep_research: Toggle between deep and fast modes (v1: ``True``
            only).

    Returns:
        ExecutiveResearchResult: Parsed research output.

    Raises:
        RuntimeError: If the research agent fails after the configured retries.

    Example:
        >>> result = run_research(
        ...     candidate_name="Jane Doe",
        ...     current_title="CTO",
        ...     current_company="Acme Corp",
        ... )
        >>> result.exec_name
        'Jane Doe'

    Notes:
        - Uses Agno's built-in retry with ``exponential_backoff=True``
        - Deep Research returns markdown via ``result.content``
        - Citations extracted from ``result.citations``
        - No separate parser agent needed
    """
    # Create agent
    agent = create_research_agent(use_deep_research=use_deep_research)

    # Build prompt
    linkedin_section = (
        f"\nLinkedIn: {linkedin_url}" if linkedin_url else "\nLinkedIn: Not provided"
    )

    prompt = f"""
Candidate: {candidate_name}
Current Title: {current_title} at {current_company}{linkedin_section}

Research this executive comprehensively.
    """.strip()

    # Execute research
    try:
        result = agent.run(prompt)
    except Exception as e:
        raise RuntimeError(
            f"Research agent failed for {candidate_name} after retries: {e}"
        ) from e

    research_markdown: str = str(result.content) if hasattr(result, "content") else ""
    citation_dicts = _extract_citation_dicts(result)
    fallback_citations = _convert_dicts_to_citations(citation_dicts)

    parser_agent = create_research_parser_agent()
    parser_prompt = _build_parser_prompt(
        candidate_name=candidate_name,
        current_title=current_title,
        current_company=current_company,
        research_markdown=research_markdown,
        citations=citation_dicts,
    )

    try:
        parser_output = parser_agent.run(parser_prompt)
    except Exception as exc:  # pragma: no cover - API failure path
        raise RuntimeError(
            f"Research parser failed for {candidate_name} after Deep Research: {exc}"
        ) from exc

    structured = _coerce_model(parser_output, ExecutiveResearchResult)

    structured.research_markdown_raw = research_markdown
    structured.citations = _merge_citation_models(
        structured.citations,
        fallback_citations,
    )
    structured.research_summary = (
        structured.research_summary.strip()
        if structured.research_summary.strip()
        else _extract_summary(research_markdown)
    )
    structured.research_confidence = _estimate_confidence(
        structured.citations,
        research_markdown,
    )
    structured.gaps = structured.gaps or _identify_gaps(
        research_markdown,
        structured.citations,
    )
    structured.research_timestamp = datetime.now()
    structured.research_model = "o4-mini-deep-research"

    return structured
```

**Rationale:**
- Deep Research API doesn't support structured outputs (`output_schema`)
- Parser agent normalizes markdown → Pydantic model
- Citation extraction from both Deep Research API and parser output
- Confidence and gaps computed heuristically

---

### 2. Research Merging with Deduplication

**URL-Based Citation Deduplication:**

```402:483:demo/agents.py
def merge_research_results(
    original: ExecutiveResearchResult,
    supplemental: Optional[ExecutiveResearchResult],
) -> ExecutiveResearchResult:
    """Merge Deep Research output with incremental search findings.

    Args:
        original: Primary Deep Research result.
        supplemental: Incremental search addendum (may be ``None``).

    Returns:
        Combined ExecutiveResearchResult with updated citations, summary, and confidence.
    """

    if supplemental is None:
        return original

    merged = original.model_copy(deep=True)

    # Merge narrative summaries.
    summary_sections: list[str] = []
    if merged.research_summary.strip():
        summary_sections.append(merged.research_summary.strip())
    if supplemental.research_summary.strip():
        summary_sections.append(
            "Supplemental Research:\n" + supplemental.research_summary.strip()
        )
    if summary_sections:
        merged.research_summary = "\n\n".join(summary_sections).strip()

    merged.research_markdown_raw = _merge_markdown_content(
        merged.research_markdown_raw,
        supplemental.research_markdown_raw or supplemental.research_summary,
    )

    # Merge citations with URL-based deduplication.
    seen_urls = {citation.url for citation in merged.citations if citation.url}
    for citation in supplemental.citations:
        url = citation.url
        if url and url in seen_urls:
            continue
        merged.citations.append(citation)
        if url:
            seen_urls.add(url)

    # Merge list fields.
    merged.key_achievements = _merge_unique_strings(
        merged.key_achievements,
        supplemental.key_achievements,
    )
    merged.notable_companies = _merge_unique_strings(
        merged.notable_companies,
        supplemental.notable_companies,
    )
    merged.sector_expertise = _merge_unique_strings(
        merged.sector_expertise,
        supplemental.sector_expertise,
    )
    merged.stage_exposure = _merge_unique_strings(
        merged.stage_exposure,
        supplemental.stage_exposure,
    )

    # Preserve career timeline ordering while appending new entries.
    seen_roles = {
        (entry.company, entry.role, entry.start_date, entry.end_date)
        for entry in merged.career_timeline
    }
    for entry in supplemental.career_timeline:
        key = (entry.company, entry.role, entry.start_date, entry.end_date)
        if key not in seen_roles:
            merged.career_timeline.append(entry)
            seen_roles.add(key)

    merged.gaps = _merge_unique_strings(merged.gaps, supplemental.gaps)

    # Update metadata and confidence based on the combined artifact.
    merged.research_timestamp = datetime.now()
    markdown_source = merged.research_markdown_raw.strip() or merged.research_summary
    merged.research_confidence = _estimate_confidence(merged.citations, markdown_source)

    return merged
```

**Rationale:**
- Preserves original research while adding supplemental findings
- URL-based deduplication prevents citation duplication
- Career timeline deduplication by (company, role, dates) tuple
- Confidence recomputed from merged citations and content

---

### 3. Configuration Management

**Typed Settings:**

```90:104:demo/settings.py
class Settings:
    """Global settings container with all configuration sections."""

    def __init__(self):
        """Initialize all configuration sections."""
        self.app = AppConfig()
        self.openai = OpenAIConfig()
        self.airtable = AirtableConfig()
        self.server = ServerConfig()
        self.quality = QualityCheckConfig()
        self.agentos = AgentOSConfig()


# Global settings instance
settings = Settings()
```

**Environment Variable Mapping:**

```20:32:demo/settings.py
class AppConfig(BaseSettings):
    """Application-level configuration."""

    model_config = SettingsConfigDict(populate_by_name=True)

    app_name: str = Field(default="talent-signal-agent", alias="APP_NAME")
    app_env: Literal["development", "production", "test"] = Field(
        default="development", alias="APP_ENV"
    )
    debug: bool = Field(default=True, alias="DEBUG")
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO", alias="LOG_LEVEL"
    )
```

**Rationale:**
- Type-safe configuration with Pydantic validation
- Environment variable aliases for deployment flexibility
- Grouped settings (app, openai, airtable, server, quality, agentos)
- Defaults for development, overrides via `.env` file

---

### 4. Logging and Observability

**Structured Logging:**

```42:58:demo/agentos_app.py
def _configure_logging() -> logging.Logger:
    """Configure structured logging for the AgentOS FastAPI runtime."""

    level_name = settings.app.log_level.upper()
    level = getattr(logging, level_name, logging.INFO)
    logging.basicConfig(level=level, format=LOG_FORMAT)
    logger = logging.getLogger("talent-signal.agentos")
    logger.setLevel(level)
    return logger


logger = _configure_logging()
SCREEN_LOG_SYMBOLS = LogSymbols(
    search=LOG_SEARCH,
    success=LOG_SUCCESS,
    error=LOG_ERROR,
)
```

**Emoji Indicators:**

```34:39:demo/agentos_app.py
LOG_SEARCH: Final[str] = "🔍"
LOG_SUCCESS: Final[str] = "✅"
LOG_ERROR: Final[str] = "❌"
LOG_FORMAT: Final[str] = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
```

**Audit Trail:**

```295:355:demo/airtable_client.py
    def log_automation_event(
        self,
        action: str,
        event_type: str,
        related_table: str,
        related_record_ids: list[str],
        event_summary: str,
        error_message: Optional[str] = None,
        webhook_payload: Optional[dict[str, Any]] = None,
        screen_id: Optional[str] = None,
        assessment_ids: Optional[list[str]] = None,
    ) -> str:
        """Write an automation event to Operations-Automation_Log.

        Args:
            action: Action type (e.g., "Candidate Assessment", "Ingest People File")
            event_type: Event type (e.g., "State Change", "Webhook Event", "System Update")
            related_table: Table name where event occurred
            related_record_ids: List of record IDs affected
            event_summary: Description of the event
            error_message: Optional error details if event failed
            webhook_payload: Optional webhook payload JSON
            screen_id: Optional screen record ID to link
            assessment_ids: Optional list of assessment record IDs to link

        Returns:
            Created log record ID (recXXXX)

        Raises:
            RuntimeError: If log creation fails
        """
        from datetime import datetime, timezone

        payload: dict[str, Any] = {
            "Action": action,
            "Event Type": event_type,
            "Related Table": related_table,
            "Related Record ID(s)": ", ".join(related_record_ids),
            "Event Summary": event_summary,
            "Timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if error_message:
            payload["Error Message"] = error_message

        if webhook_payload:
            payload["Webhook Payload JSON"] = json.dumps(webhook_payload, indent=2)

        if screen_id:
            payload["Platform-Screens"] = [screen_id]

        if assessment_ids:
            payload["Platform-Assessments"] = assessment_ids

        try:
            record = self.automation_log.create(payload)
            logger.info(f"✅ Logged automation event: {record['id']} ({action})")
            return record["id"]
        except Exception as exc:  # pragma: no cover - API failure path
            logger.error(f"❌ Failed to log automation event: {exc}")
            raise RuntimeError(f"Failed to log automation event: {action}") from exc
```

**Rationale:**
- **Emoji Logging:** Visual indicators for quick scanning (🔍 search, ✅ success, ❌ error)
- **Structured Format:** Consistent timestamp, level, logger name, message
- **Airtable Audit Trail:** All automation events logged for compliance
- **AgentOS UI:** Real-time workflow monitoring via control plane

---

## Summary

The Talent Signal Agent demonstrates a well-architected AI system with clear separation of concerns, evidence-aware design principles, and production-ready patterns. Key strengths include:

1. **Evidence-Aware Scoring:** Explicit `None` handling prevents false confidence
2. **Quality-Gated Research:** Cost-effective conditional incremental search
3. **Centralized Prompts:** YAML catalog enables non-developer iteration
4. **Session Persistence:** SqliteDb audit trail for debugging and compliance
5. **Error Isolation:** Partial failure support for batch processing
6. **Type Safety:** Pydantic models throughout for validation and serialization
7. **AgentOS Integration:** Control plane UI for real-time monitoring

The implementation balances simplicity with sophistication, demonstrating quality thinking in domain-specific context engineering, incremental value delivery, and scalable foundation patterns.

---

**Report Generated:** 2025-01-17  
**Analysis Scope:** `demo/` directory (7 modules, ~2,500 lines of code)  
**Key Files Analyzed:** agentos_app.py, agents.py, screening_service.py, airtable_client.py, models.py, settings.py, prompts/
