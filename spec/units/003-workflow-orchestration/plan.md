---
unit_id: "003-workflow-orchestration"
version: "1.0"
created: "2025-01-17"
updated: "2025-11-17"
---

# Unit Plan: Workflow Orchestration

Volatile task breakdown and verification plan for implementing linear Agno workflow orchestration.

## Tasks

### TK-01

- **Title:** Create Workflow with SqliteDb Configuration
- **Description:** Implement `create_screening_workflow()` function in `demo/agents.py` that creates an Agno Workflow instance with SqliteDb at `tmp/agno_sessions.db`, session state initialization, and event streaming enabled. Configure workflow with 4-step linear execution pattern (no teams, no nested workflows).
- **Files:** `demo/agents.py`
- **Status:** complete
- **Priority:** high
- **Estimate:** 2 hours
- **Dependencies:** None
- **Note:** Must use SqliteDb (not InMemoryDb) per constitution and spec lines 1033-1065. Enable `stream_events=True` for stdout logging. ✅ Implemented via `create_screening_workflow()` factory pointing to `tmp/agno_sessions.db`.
- **Completed:** 2025-11-17

### TK-02

- **Title:** Implement Research Merging Logic
- **Description:** Create `merge_research_results()` helper function that combines original Deep Research result with incremental search results. Merge citations (deduplicate by URL), combine summaries, preserve career timeline from original, and update research_confidence based on combined data quality.
- **Files:** `demo/agents.py`
- **Status:** complete
- **Priority:** high
- **Estimate:** 1.5 hours
- **Dependencies:** None
- **Note:** Used by conditional incremental search step when quality check fails. Must handle ExecutiveResearchResult Pydantic models. ✅ `merge_research_results()` now dedupes by URL, preserves timelines, and recalculates confidence.
- **Completed:** 2025-11-17

### TK-03

- **Title:** Implement screen_single_candidate() Helper
- **Description:** Create `screen_single_candidate()` function that orchestrates the full 4-step workflow: (1) Run Deep Research agent, (2) Execute quality check via `check_research_quality()`, (3) Conditionally run incremental search and merge if needed, (4) Run assessment agent with merged/original research. Function takes candidate_data dict, role_spec_markdown str, and screen_id str, returns AssessmentResult.
- **Files:** `demo/agents.py`
- **Status:** complete
- **Priority:** high
- **Estimate:** 3 hours
- **Dependencies:** TK-01, TK-02
- **Note:** This is the main integration function called by Flask webhook. Must handle all error scenarios gracefully and preserve session state in SqliteDb. ✅ `screen_single_candidate()` now orchestrates research, quality gate, incremental search, and assessment with state tracking.
- **Completed:** 2025-11-17

### TK-04

- **Title:** Add Logging with Emoji Indicators
- **Description:** Configure Python standard library logging in `demo/agents.py` with INFO level and emoji indicators (🔍 for research, ✅ for success, ❌ for errors, 🔄 for incremental search). Add strategic log statements throughout workflow execution to show progress.
- **Files:** `demo/agents.py`
- **Status:** complete
- **Priority:** medium
- **Estimate:** 1 hour
- **Dependencies:** TK-03
- **Note:** Use standard Python logging module (not structlog). Log at key workflow steps: research start/complete, quality check result, incremental search trigger, assessment start/complete. ✅ INFO-level logger with emoji cues now wraps workflow steps.
- **Completed:** 2025-11-17

### TK-05

- **Title:** Create Workflow Integration Tests
- **Description:** Implement `tests/test_workflow.py` with unit tests for: (1) Happy path workflow execution with mocked agents (AC-WF-01), (2) Quality gate triggering incremental search with low-quality fixture (AC-WF-02), (3) Session state persistence verification (AC-WF-03), (4) Event streaming to stdout (AC-WF-04), (5) Error handling with retry behavior (AC-WF-05). Use pytest fixtures for test data and mocks.
- **Files:** `tests/test_workflow.py`
- **Status:** complete
- **Priority:** high
- **Estimate:** 2.5 hours
- **Dependencies:** TK-03, TK-04
- **Note:** Target 50% coverage per constitution. Mock agent responses to avoid real API calls. Verify SqliteDb file creation and session data persistence. ✅ Implemented 9 test cases (5 AC tests + 4 helper tests). Coverage: 75% (exceeds 50% target). All 5 acceptance criteria verified.
- **Completed:** 2025-11-17

### TK-06

- **Title:** Document Workflow Architecture
- **Description:** Add workflow orchestration section to `README.md` explaining: (1) 4-step linear execution flow, (2) Quality gate logic and thresholds, (3) Session state persistence with SqliteDb, (4) Event streaming and logging, (5) Error handling and retry behavior. Include code examples for calling `screen_single_candidate()`.
- **Files:** `README.md`
- **Status:** complete
- **Priority:** medium
- **Estimate:** 1 hour
- **Dependencies:** TK-05
- **Note:** Focus on explaining design decisions (why SqliteDb, why linear, why quality gate). Include example usage with sample inputs/outputs. ✅ Added "Workflow Orchestration" section with 6 subsections: Execution Flow, Session State Persistence, Event Streaming & Logging, Error Handling, Usage Example, Design Decisions. Covers all 5 requirements plus rationale.
- **Completed:** 2025-11-17

## Verification

### Commands

1. **pytest tests/test_workflow.py -v** - Run workflow integration tests (must pass: ✅)
2. **pytest tests/ --cov=demo --cov-report=term-missing** - Check coverage (must meet target: ✅)
3. **mypy demo/agents.py** - Type checking (must pass: ✅)
4. **ruff format demo/ tests/** - Auto-format code (must pass: ✅)
5. **ruff check demo/ tests/** - Linting (must pass: ✅)

### Gates

- **tests:** must pass ✅ (all 5 acceptance criteria covered)
- **type_check:** must pass ✅ (mypy standard mode)
- **coverage:** must pass ✅ (≥50% per constitution)
- **format:** must pass ✅ (ruff format)
- **lint:** must pass ✅ (ruff check)

### Coverage Target

50% (0.50) - Per constitution quality bar for case study

### Acceptance References

From `design.md`:

- **AC-WF-01:** Linear Workflow Execution - Verified by TK-05 test case 1
- **AC-WF-02:** Quality Gate Triggers Incremental Search - Verified by TK-05 test case 2
- **AC-WF-03:** Session State Persistence - Verified by TK-05 test case 3
- **AC-WF-04:** Event Streaming for Visibility - Verified by TK-05 test case 4
- **AC-WF-05:** Error Handling with Graceful Degradation - Verified by TK-05 test case 5

## Status

- **Progress:** 100% (6/6 tasks completed)
- **Created:** 2025-01-17
- **Status:** complete
- **Next Action:** Unit complete. Proceed to Stage 4 (Flask Webhook Integration).

## Implementation Notes

### Critical Design Constraints

1. **SqliteDb Required:** Must use SqliteDb at `tmp/agno_sessions.db` for session state (NOT InMemoryDb) - per spec lines 1033-1065
2. **Linear Execution Only:** No teams, no nested workflows, sequential steps - v1 simplification
3. **Single Incremental Search:** Quality gate triggers at most one additional search step (not a loop)
4. **No Custom Event Tables:** Use Agno-managed session tables only, no WorkflowEvent model
5. **Synchronous Processing:** No async/await, one candidate at a time

### Key Interfaces

From `demo/agents.py` (Stage 2 - already implemented):

- `run_research()` - Deep Research agent execution
- `assess_candidate()` - Assessment agent execution
- `check_research_quality()` - Quality gate heuristics
- `calculate_overall_score()` - Score computation

### Testing Strategy

- Mock all agent responses to avoid real OpenAI API calls
- Create fixtures for ExecutiveResearchResult with varying quality levels
- Verify SqliteDb file creation and session data persistence
- Capture stdout to verify event streaming
- Test error scenarios with mocked API failures

### Phase 2+ Exclusions

Do NOT implement in this unit (Phase 2+ only):

- Async execution or concurrent candidate processing
- InMemoryDb fallback mode
- Custom WorkflowEvent model or event database tables
- Multi-iteration incremental search loops
- Team coordination or nested workflows
