---
unit_id: "002-agent-implementation"
version: "1.0"
created: "2025-01-16"
updated: "2025-01-16"
status: "planning"
---

# Unit Plan: Agent Implementation

Volatile task breakdown and verification plan for implementing core AI agents

## Tasks

### TK-01

- **Title:** Implement Pydantic data models for agent outputs
- **Description:** Create all Pydantic models in `demo/models.py` including ExecutiveResearchResult, AssessmentResult, DimensionScore, Citation, CareerEntry, and MustHaveCheck. Ensure evidence-aware scoring with Optional[int] for scores (None for Unknown, never 0 or NaN). Follow spec/dev_reference/implementation_guide.md for complete field definitions.
- **Files:** `demo/models.py`
- **Status:** done
- **Priority:** high
- **Estimate:** 1.5 hours
- **Dependencies:** None
- **Note:** Foundation for all agent structured outputs. Critical: Use Optional[int] for DimensionScore.score field.
- **Completed:** 2025-01-16T23:45:00Z

### TK-02

- **Title:** Implement research agent with Deep Research mode
- **Description:** Create `create_research_agent()` and `run_research()` functions in `demo/agents.py`. Configure Agno Agent with OpenAIResponses(id="o4-mini-deep-research"), exponential_backoff=True, retries=2. Handle markdown output from Deep Research API (NOT structured output). Extract citations from result.citations. Return ExecutiveResearchResult.
- **Files:** `demo/agents.py`
- **Status:** ready
- **Priority:** high
- **Estimate:** 2 hours
- **Dependencies:** TK-01
- **Note:** Deep Research does NOT support output_schema. Must parse markdown manually or use incremental search agent.
- **Completed:** null

### TK-03

- **Title:** Implement quality check function
- **Description:** Create `check_research_quality()` function in `demo/agents.py`. Implement simple sufficiency criteria: ≥3 citations AND non-empty research_summary. Return bool (True if sufficient, False if incremental search needed). Pure function, no complex workflow types.
- **Files:** `demo/agents.py`
- **Status:** ready
- **Priority:** medium
- **Estimate:** 0.5 hours
- **Dependencies:** TK-01
- **Note:** Simple heuristics for v1. Phase 2+ can add: experience count, expertise areas, confidence level.
- **Completed:** null

### TK-04

- **Title:** Implement overall score calculation function
- **Description:** Create `calculate_overall_score()` function in `demo/agents.py`. Filter dimension_scores to scored only (score is not None). If no scored dimensions, return None. Compute simple average on 1-5 scale, multiply by 20 to scale to 0-100. Return Optional[float].
- **Files:** `demo/agents.py`
- **Status:** ready
- **Priority:** medium
- **Estimate:** 0.5 hours
- **Dependencies:** TK-01
- **Note:** Python implementation, NOT LLM calculation. Demonstrates evidence-aware concept.
- **Completed:** null

### TK-05

- **Title:** Implement assessment agent with evidence-aware scoring
- **Description:** Create `assess_candidate()` function in `demo/agents.py`. Configure Agno Agent with OpenAIResponses(id="gpt-5-mini"), tools=[ReasoningTools(add_instructions=True)], output_schema=AssessmentResult, exponential_backoff=True, retries=2. Evaluate candidate against role_spec_markdown. Use custom_instructions if provided. Return AssessmentResult with dimension scores (1-5 or None for Unknown).
- **Files:** `demo/agents.py`
- **Status:** ready
- **Priority:** high
- **Estimate:** 2 hours
- **Dependencies:** TK-01, TK-04
- **Note:** ReasoningTools required for v1 (PRD AC-PRD-04). Use Agno's native structured outputs.
- **Completed:** null

### TK-06

- **Title:** Implement incremental search agent
- **Description:** Create incremental search agent in `demo/agents.py` for optional single-pass supplemental research. Configure Agno Agent with OpenAIResponses(id="gpt-5"), tools=[web_search], output_schema=ExecutiveResearchResult. Execute single-pass search (max 2 web/search calls) when quality check fails. Merge results with initial research. Return merged ExecutiveResearchResult.
- **Files:** `demo/agents.py`
- **Status:** ready
- **Priority:** medium
- **Estimate:** 1.5 hours
- **Dependencies:** TK-01, TK-02, TK-03
- **Note:** Single-pass only (no multi-iteration loops in v1). Uses Agno's built-in web_search tool.
- **Completed:** null

### TK-07

- **Title:** Write unit tests for scoring and quality check
- **Description:** Create `tests/test_scoring.py` for calculate_overall_score() tests (all scored, partial scored, no scored, None handling). Create `tests/test_quality_check.py` for check_research_quality() tests (sufficient, insufficient citations, empty summary). Use pytest with fixtures for ExecutiveResearchResult and DimensionScore test data.
- **Files:** `tests/test_scoring.py`, `tests/test_quality_check.py`
- **Status:** ready
- **Priority:** high
- **Estimate:** 1.5 hours
- **Dependencies:** TK-01, TK-03, TK-04
- **Note:** Core logic tests required by constitution. Focus on happy paths + evidence-aware None handling.
- **Completed:** null

### TK-08

- **Title:** Add type hints and docstrings to all agent functions
- **Description:** Add comprehensive type hints (PEP 484) and Google-style docstrings to all public functions in `demo/agents.py`: create_research_agent(), run_research(), assess_candidate(), check_research_quality(), calculate_overall_score(). Document args, returns, raises, examples. Ensure mypy compliance.
- **Files:** `demo/agents.py`
- **Status:** ready
- **Priority:** medium
- **Estimate:** 1 hour
- **Dependencies:** TK-02, TK-03, TK-04, TK-05, TK-06
- **Note:** Constitution requirement: all public functions must have type hints and docstrings.
- **Completed:** null

### TK-09

- **Title:** Integration smoke test (optional)
- **Description:** Create `tests/test_workflow_smoke.py` for happy-path /screen flow with mocks. Test research → quality check → assessment pipeline with mock candidate data. Verify structured outputs, None handling, overall score calculation. Use pytest mocks for Agno agents.
- **Files:** `tests/test_workflow_smoke.py`
- **Status:** ready
- **Priority:** low
- **Estimate:** 1.5 hours
- **Dependencies:** TK-02, TK-03, TK-04, TK-05, TK-06
- **Note:** Optional for v1. Provides confidence in agent integration before workflow implementation.
- **Completed:** null

## Verification

### Commands

1. **pytest tests/** - Run all unit tests (must pass: ✅)
2. **pytest --cov=demo --cov-report=term-missing tests/** - Check coverage (must pass: ✅)
3. **mypy demo/** - Type checking (must pass: ✅)
4. **ruff check demo/ tests/** - Linting (must pass: ✅)
5. **ruff format demo/ tests/** - Formatting (must pass: ✅)

### Gates

- **tests:** must pass ✅ (all tests passing)
- **type_check:** must pass ✅ (mypy with standard settings)
- **coverage:** must pass ✅ (≥50% for core logic)
- **linting:** must pass ✅ (ruff check)
- **formatting:** must pass ✅ (ruff format)

### Coverage Target

50% (0.50) - Core logic only per constitution

### Acceptance References

- AC-002-01: Research agent returns ExecutiveResearchResult with ≥3 citations
- AC-002-02: Assessment agent produces dimension scores with None for Unknown
- AC-002-03: Overall score calculated in Python using simple average algorithm
- AC-002-04: Incremental search performs single-pass supplemental research
- AC-002-05: Assessment agent uses output_schema for structured outputs
- AC-002-06: Built-in retry handles API failures with exponential backoff

## Progress

- **Status:** in_progress
- **Created:** 2025-01-16
- **Tasks Total:** 9
- **Tasks Completed:** 1
- **Progress:** 11%

## 2-Developer Parallel Execution Plan

### Developer A (Agents Track) - 6 hours

**Focus:** Core agent implementation

1. **TK-02: Research Agent** (2 hours)
   - Deep Research mode with o4-mini-deep-research
   - Markdown output handling (NOT structured output)
   - Citation extraction from result.citations
   - Built-in retry/backoff

2. **TK-05: Assessment Agent** (2 hours)
   - gpt-5-mini with ReasoningTools
   - Evidence-aware scoring (None for Unknown)
   - Structured outputs via output_schema
   - Built-in retry/backoff

3. **TK-06: Incremental Search Agent** (1.5 hours)
   - Single-pass supplemental research
   - web_search tool integration
   - Research merging logic

4. **TK-08: Type Hints & Docstrings** (0.5 hours)
   - Document all agent functions
   - Google-style docstrings
   - Mypy compliance

**Dependencies:** TK-01 (completed in Phase 1)

### Developer B (Logic + Testing Track) - 6 hours

**Focus:** Supporting logic and test coverage

1. **TK-03: Quality Check Function** (0.5 hours)
   - Simple sufficiency criteria (≥3 citations, non-empty summary)
   - Pure function implementation
   - Return bool for workflow branching

2. **TK-04: Overall Score Calculation** (0.5 hours)
   - Simple average algorithm
   - Evidence-aware None handling
   - Scale to 0-100 (multiply by 20)

3. **TK-07: Unit Tests** (1.5 hours)
   - tests/test_scoring.py (calculate_overall_score)
   - tests/test_quality_check.py (check_research_quality)
   - Pytest fixtures for test data
   - Focus on None handling + edge cases

4. **TK-09: Integration Smoke Test** (1.5 hours) - OPTIONAL
   - tests/test_workflow_smoke.py
   - Happy-path /screen flow with mocks
   - End-to-end pipeline verification

5. **TK-08: Type Hints & Docstrings** (0.5 hours) - SHARED
   - Review and validate Developer A's docstrings
   - Add type hints to scoring/quality functions
   - Cross-check for consistency

6. **Buffer Time** (1.5 hours)
   - Test execution and debugging
   - Coverage validation (≥50%)
   - Ruff linting/formatting
   - Mypy type checking

**Dependencies:** TK-01 (completed in Phase 1)

### Sync Points

1. **After TK-02, TK-03, TK-04** (Mid-point)
   - Developer A: Research agent complete
   - Developer B: Quality check + scoring complete
   - Review: Interface contracts between research and quality check

2. **After TK-05, TK-06, TK-07** (Near-end)
   - Developer A: All agents complete
   - Developer B: Core tests complete
   - Review: Agent outputs match test expectations

3. **After TK-08** (Final)
   - Both: Type hints and docstrings complete
   - Run all verification commands together
   - Validate all acceptance criteria

### Parallel Execution Timeline

**Hours 0-2:**
- Developer A: TK-02 (Research Agent)
- Developer B: TK-03 + TK-04 (Quality Check + Scoring)

**Hours 2-4:**
- Developer A: TK-05 (Assessment Agent)
- Developer B: TK-07 (Unit Tests)

**Hours 4-5.5:**
- Developer A: TK-06 (Incremental Search)
- Developer B: TK-09 (Integration Test - optional)

**Hours 5.5-6:**
- Developer A: TK-08 (Docstrings for agents)
- Developer B: TK-08 (Docstrings for logic) + verification runs

### Critical Path

**TK-01 → TK-02 → TK-05 → TK-06 → TK-08** (Developer A)

Developer B's work can proceed in parallel with minimal blocking.

## Notes

**Implementation Order Rationale:**

1. **TK-01 (Models):** Foundation for all structured outputs
2. **TK-02 (Research):** Core research capability with Deep Research API
3. **TK-03, TK-04 (Quality/Scoring):** Supporting functions for workflow
4. **TK-05 (Assessment):** Core evaluation capability
5. **TK-06 (Incremental):** Optional enhancement for low-quality research
6. **TK-07 (Tests):** Verify core logic correctness
7. **TK-08 (Docs):** Constitution compliance (type hints, docstrings)
8. **TK-09 (Integration):** Optional confidence check

**Key Constraints:**

- Deep Research models do NOT support output_schema (returns markdown)
- Assessment agent uses gpt-5-mini with structured outputs
- ReasoningTools required for assessment agent (v1 requirement)
- Incremental search is single-pass only (no loops)
- Overall score calculated in Python (not by LLM)
- Synchronous execution only (v1.0-minimal)

**Estimated Total Time:** 11.5 hours (excluding optional TK-09)

**Dependencies Graph (DAG Validated):**

```
TK-01 (Models)
├── TK-02 (Research) → TK-06 (Incremental)
├── TK-03 (Quality) → TK-06, TK-07
├── TK-04 (Scoring) → TK-05, TK-07
└── TK-05 (Assessment) → TK-08

TK-06 → TK-08
TK-02, TK-03, TK-04, TK-05, TK-06 → TK-09 (optional)
```

No circular dependencies detected. All tasks have clear predecessors.
