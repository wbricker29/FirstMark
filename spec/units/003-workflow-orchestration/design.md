---
unit_id: "003-workflow-orchestration"
title: "Workflow Orchestration - Linear Research to Assessment Pipeline"
version: "1.0"
created: "2025-01-17"
updated: "2025-11-17"
status: "complete"
---

# Unit Design: Workflow Orchestration

Stable intent and acceptance criteria for implementing the Agno workflow that orchestrates candidate screening from research through assessment.

## Objective

**Summary:** Implement a linear Agno workflow that connects Deep Research → Quality Check → Optional Incremental Search → Assessment agents into a cohesive screening pipeline with session state persistence and stdout event streaming.

**Success Metrics:**

- Single workflow executes all 4 steps sequentially for one candidate
- Session state persisted to SqliteDb at `tmp/agno_sessions.db` for review
- Workflow callable via `screen_single_candidate()` helper for Flask integration
- Terminal logs show execution progress with event streaming

## Behavior

**Description:** This unit creates the orchestration layer that coordinates the research and assessment agents implemented in Stage 2. The workflow executes a 4-step linear process: (1) Deep Research Agent conducts comprehensive research, (2) Quality Check evaluates research sufficiency, (3) Conditional Incremental Search supplements if quality is low, and (4) Assessment Agent evaluates candidate against role spec. The workflow uses Agno's SqliteDb for session state management and streams events to stdout for visibility.

### Inputs

#### candidate_data
- **Type:** `dict[str, Any]` (from Airtable People record)
- **Description:** Executive candidate information including name, title, company, LinkedIn URL
- **Examples:**
  - `{"name": "Alex Rivera", "current_title": "CFO", "current_company": "Armis", "linkedin_url": "https://linkedin.com/in/alex-rivera"}`
  - `{"name": "Nia Patel", "current_title": "CTO", "current_company": "DataBricks", "linkedin_url": "https://linkedin.com/in/nia-patel"}`

#### role_spec_markdown
- **Type:** `str`
- **Description:** Full role specification in markdown format (from Role_Specs table)
- **Examples:**
  - Multi-paragraph markdown with role context, must-haves, evaluation dimensions, company context

#### screen_id
- **Type:** `str`
- **Description:** Airtable record ID for the Screen record (for audit trail and status updates)
- **Examples:**
  - `"recABC123"`
  - `"recXYZ789"`

### Outputs

#### AssessmentResult
- **Type:** `AssessmentResult` (Pydantic model)
- **Description:** Complete assessment with dimension scores, overall score, confidence, reasoning
- **Examples:**
  - Assessment with overall_score=86.5, confidence="High", 4 dimension scores, must-haves checks

### Edge Cases

- **Scenario:** Research quality check fails (insufficient citations)
  - **Expected behavior:** Trigger single incremental search agent step, merge results, proceed to assessment

- **Scenario:** Deep Research API returns no citations
  - **Expected behavior:** Quality check fails, incremental search triggered, workflow continues

- **Scenario:** All dimension scores return None (insufficient evidence)
  - **Expected behavior:** calculate_overall_score() returns None, assessment completes with confidence="Low"

- **Scenario:** Workflow interrupted mid-execution
  - **Expected behavior:** Session state preserved in SqliteDb, can review partial execution

## Interfaces Touched

From `spec/spec.md`:

- **Research Agent Interface** (lines 170-236) - `run_research()` function
- **Assessment Agent Interface** (lines 254-284) - `assess_candidate()` function
- **Quality Check Interface** (lines 289-315) - `check_research_quality()` function
- **Score Calculation Interface** (lines 319-358) - `calculate_overall_score()` function
- **Agno Workflow** (lines 987-1065) - Workflow class with SqliteDb configuration

## Data Shapes

From `spec/spec.md`:

- **ExecutiveResearchResult** (lines 453-459) - Structured research output
- **AssessmentResult** (lines 461-467) - Structured assessment output
- **DimensionScore** (lines 469-472) - Evidence-aware scoring model

## Constraints

### Functional

- Linear execution only (no teams, no nested workflows) - v1 simplification
- Quality gate uses simple heuristics: ≥3 citations, non-empty summary
- Incremental search limited to single agent step (up to 2 web/search calls)
- SqliteDb must be used (no InMemoryDb in v1) - persistence required for review
- No custom WorkflowEvent model or event logging tables - use Agno-managed tables only

### Non-Functional

- Synchronous processing (no async/await in v1) - one candidate at a time
- Workflow execution time: <10 minutes per candidate (including LLM API calls)
- Session state file: `tmp/agno_sessions.db` (gitignored)
- Event streaming to stdout only (no database persistence in v1)
- Memory usage: <512MB per workflow execution

## Acceptance Criteria

### AC-WF-01: Linear Workflow Execution

- **Given:** Valid candidate data, role spec markdown, and screen_id
- **When:** `screen_single_candidate()` is called
- **Then:** Workflow executes all 4 steps sequentially (Deep Research → Quality Check → Optional Search → Assessment) and returns AssessmentResult
- **Testable:** ✅ (unit test with mocked agents)

### AC-WF-02: Quality Gate Triggers Incremental Search

- **Given:** Deep Research returns result with <3 citations
- **When:** Quality check executes
- **Then:** Incremental search agent is invoked, research results are merged, and assessment proceeds with merged data
- **Testable:** ✅ (unit test with low-quality research fixture)

### AC-WF-03: Session State Persistence

- **Given:** Workflow execution in progress
- **When:** Any workflow step completes
- **Then:** Session state is persisted to `tmp/agno_sessions.db` using SqliteDb (Agno-managed tables only)
- **Testable:** ✅ (verify db file exists and contains session data)

### AC-WF-04: Event Streaming for Visibility

- **Given:** Workflow configured with `stream_events=True`
- **When:** Workflow executes
- **Then:** Execution events are logged to stdout showing progress through each step
- **Testable:** ✅ (capture stdout and verify event messages)

### AC-WF-05: Error Handling with Graceful Degradation

- **Given:** One agent step fails (e.g., API timeout)
- **When:** Workflow executes with Agno's built-in retry (exponential_backoff=True, retries=2)
- **Then:** Agent retries up to 2 times, and if still failing, raises clear error without corrupting session state
- **Testable:** ✅ (unit test with mocked API failure)

## Dependencies

**Blocks:**
- Stage 4: Flask Webhook Integration (requires `screen_single_candidate()` helper)

**Blocked by:**
- Stage 2: Agent Implementation (requires `run_research()`, `assess_candidate()`, `check_research_quality()`, `calculate_overall_score()`)

## Notes

**Implementation File:** `demo/agents.py` (add workflow creation and orchestration functions)

**Key Design Decisions:**

1. **No InMemoryDb in v1:** SqliteDb required at `tmp/agno_sessions.db` for reviewable workflow history (per spec lines 1033-1065)
2. **No Parser Agent:** Deep Research returns markdown via `result.content`, not structured output (per spec lines 174-178 warning)
3. **Single Incremental Search Step:** Quality gate triggers at most one additional search agent step, not a loop (per spec lines 289-315)
4. **No Custom Event Tables:** Use Agno-managed session tables + terminal logs only; custom WorkflowEvent model is Phase 2+ (per spec lines 488-521)

**Testing Strategy:**

- Unit test workflow with mocked agents (test happy path)
- Unit test quality gate logic (low quality → incremental search)
- Unit test session state persistence (verify SqliteDb file)
- Integration test with real agents (test_workflow_smoke.py - optional per spec line 583)

**Phase 2+ Enhancements (NOT in v1):**

- Async execution with `asyncio.gather()` for concurrent candidates
- Complex state machines or nested workflows
- Custom WorkflowEvent model and event persistence to database
- InMemoryDb fallback mode
