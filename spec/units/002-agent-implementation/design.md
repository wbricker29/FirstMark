---
unit_id: "002-agent-implementation"
title: "Agent Implementation - Research, Assessment, and Incremental Search"
version: "1.0"
created: "2025-01-16"
updated: "2025-11-19"
status: "complete"
---

# Unit Design: Agent Implementation

Stable intent and acceptance criteria for core AI agent implementation

## Objective

**Summary:** Implement the three core AI agents (research, assessment, incremental search) using Agno framework with structured outputs, built-in retry/backoff, and evidence-aware scoring capabilities.

**Success Metrics:**

- All three agents (research, assessment, incremental search) fully implemented and functional
- Research agent two-agent pattern (Deep Research + parser) produces structured ExecutiveResearchResult with normalized citations
- Assessment agent uses direct structured outputs via Agno's output_schema
- Evidence-aware scoring uses None for Unknown dimensions (never 0 or NaN)
- Built-in retry/backoff handles transient API failures gracefully

## Behavior

**Description:** This unit implements the three core AI agents that power the Talent Signal Agent workflow. The research agent conducts comprehensive executive research using OpenAI's Deep Research API (o4-mini-deep-research) paired with a parser agent to convert markdown output into structured ExecutiveResearchResult payloads. The assessment agent evaluates candidates against role specifications with evidence-aware scoring. The incremental search agent performs optional supplemental research when initial quality is insufficient.

**Research Agent Pattern:** Deep Research returns markdown via `result.content` and citations via `result.citations`. A dedicated parser agent (`gpt-5-mini` + `output_schema=ExecutiveResearchResult`) normalizes API responses, merges citations, recomputes confidence/gaps, and produces the canonical structured output with raw markdown preserved in `research_markdown_raw` field for Airtable storage.

### Inputs

#### Research Agent Inputs

- **Type:** `str` (candidate_name, current_title, current_company), `Optional[str]` (linkedin_url), `bool` (use_deep_research)
- **Description:** Candidate information for research
- **Examples:**
  - `candidate_name="Jonathan Carr"`, `current_title="CFO"`, `current_company="Armis"`, `linkedin_url="https://linkedin.com/in/jonathan-carr"`, `use_deep_research=True`

#### Assessment Agent Inputs

- **Type:** `ExecutiveResearchResult` (research), `str` (role_spec_markdown), `str` (custom_instructions)
- **Description:** Research results and role specification for evaluation
- **Examples:**
  - `research=<ExecutiveResearchResult>`, `role_spec_markdown="# CFO Role Spec..."`, `custom_instructions=""`

#### Incremental Search Agent Inputs

- **Type:** `str` (candidate_name), `ExecutiveResearchResult` (initial_research), `str` (quality_gaps)
- **Description:** Candidate name, initial research, and identified quality gaps
- **Examples:**
  - `candidate_name="Jane Smith"`, `initial_research=<ExecutiveResearchResult>`, `quality_gaps="Missing fundraising experience details"`

### Outputs

#### Research Agent Output

- **Type:** `ExecutiveResearchResult`
- **Description:** Structured research with career timeline, expertise areas, citations, confidence metadata
- **Examples:**
  - ExecutiveResearchResult with research_summary, career_timeline (list of CareerEntry), expertise_areas, citations (≥3), research_confidence="High"

#### Assessment Agent Output

- **Type:** `AssessmentResult`
- **Description:** Evidence-aware dimension scores, overall score, must-haves checks, flags, counterfactuals
- **Examples:**
  - AssessmentResult with dimension_scores (DimensionScore with score=4 or None), overall_score=70.0, assessment_confidence="High"

#### Incremental Search Agent Output

- **Type:** `ExecutiveResearchResult`
- **Description:** Merged research combining initial and supplemental findings
- **Examples:**
  - ExecutiveResearchResult with updated citations count, enriched career_timeline

### Edge Cases

- **Scenario:** Deep Research API returns markdown instead of structured output
  - **Expected behavior:** Parser agent (`gpt-5-mini` + `output_schema=ExecutiveResearchResult`) converts markdown + citations into structured payload with normalized citation format (handles both list and object citation formats from Deep Research API)

- **Scenario:** Parser agent fails to structure Deep Research output
  - **Expected behavior:** Error propagates with raw markdown preserved; incremental search agent can be triggered as fallback to regenerate structured data

- **Scenario:** Candidate has insufficient public information
  - **Expected behavior:** Assessment agent returns None for unknown dimensions, not 0 or NaN

- **Scenario:** API call fails with transient error
  - **Expected behavior:** Agno's built-in retry with exponential_backoff handles retry automatically (max 2 retries)

- **Scenario:** Quality check determines research is insufficient
  - **Expected behavior:** Incremental search agent performs single-pass supplemental research (max 2 web/search calls)

## Interfaces Touched

- `create_research_agent()` - Creates research agent with Deep Research mode
- `run_research()` - Executes research and returns ExecutiveResearchResult
- `assess_candidate()` - Evaluates candidate against role spec
- `check_research_quality()` - Validates research sufficiency
- `calculate_overall_score()` - Computes simple average score from dimensions

## Data Shapes

- `ExecutiveResearchResult` - Structured research output with career timeline, expertise, citations
- `AssessmentResult` - Evidence-aware assessment with dimension scores and overall score
- `DimensionScore` - Individual dimension evaluation with score (1-5 or None)
- `Citation` - Source citation with URL, title, snippet
- `CareerEntry` - Timeline entry for career history
- `MustHaveCheck` - Must-have requirement evaluation

## Constraints

### Functional

- Deep Research models (o4-mini-deep-research) do NOT support structured outputs (output_schema) - requires parser agent
- Research uses two-agent pattern: Deep Research (markdown + citations) → Parser agent (structured ExecutiveResearchResult)
- Parser agent normalizes citation formats (list vs object), merges citations, recomputes confidence/gaps
- Assessment agent uses gpt-5-mini with structured outputs (output_schema supported directly)
- Incremental search is single-pass only (no multi-iteration loops in v1)
- Overall score calculated in Python using simple average algorithm (not by LLM)

### Non-Functional

- Deep Research: 2-6 minutes per candidate
- Assessment: 30-60 seconds per candidate
- Quality check: <1 second
- Incremental search: 30-60 seconds (max 2 web/search calls)
- Memory usage: <512MB per Flask worker
- Synchronous execution only (v1.0-minimal)

## Acceptance Criteria

### AC-002-01

- **Given:** Valid candidate information (name, title, company, optional LinkedIn URL)
- **When:** Research agent executes with use_deep_research=True (Deep Research + parser agent handshake)
- **Then:** Returns ExecutiveResearchResult with ≥3 citations, non-empty research summary, normalized citation format, and raw markdown preserved in research_markdown_raw field
- **Testable:** ✅

### AC-002-02

- **Given:** ExecutiveResearchResult and role specification markdown
- **When:** Assessment agent evaluates candidate
- **Then:** Produces dimension scores with None for Unknown (never 0 or NaN)
- **Testable:** ✅

### AC-002-03

- **Given:** List of DimensionScore objects from assessment
- **When:** calculate_overall_score() is called
- **Then:** Overall score calculated in Python using simple average algorithm ((sum of scored dimensions / count) * 20), not by LLM
- **Testable:** ✅

### AC-002-04

- **Given:** Initial research with quality issues (e.g., <3 citations)
- **When:** Incremental search agent is triggered
- **Then:** Performs single-pass supplemental research with max 2 web/search calls and returns merged ExecutiveResearchResult
- **Testable:** ✅

### AC-002-05

- **Given:** Assessment agent configured with output_schema=AssessmentResult
- **When:** Agent executes evaluation
- **Then:** Returns Pydantic model directly without parser agent
- **Testable:** ✅

### AC-002-06

- **Given:** Transient API failure during agent execution
- **When:** Agent configured with exponential_backoff=True, retries=2
- **Then:** Built-in retry handles failure automatically with exponential backoff
- **Testable:** ✅

## Dependencies

**Blocks:** 003-workflow-implementation

**Blocked by:** 001-phase-1 (Airtable setup, Pydantic models)

## Notes

**Implementation Notes:**

- Deep Research API limitation: Returns markdown (not structured output), requires parser agent to convert to ExecutiveResearchResult
- Research agent uses two-agent pattern: o4-mini-deep-research (Deep Research) + gpt-5-mini (parser with output_schema)
- Parser agent normalizes citations (handles list vs object formats), preserves raw markdown in research_markdown_raw field
- Assessment agent uses ReasoningTools(add_instructions=True) for explicit reasoning trails (PRD AC-PRD-04)
- Assessment agent uses direct structured outputs via output_schema (no parser needed for gpt-5-mini)
- Quality check uses simple sufficiency criteria: ≥3 citations + non-empty summary
- See spec/dev_reference/implementation_guide.md for complete data model definitions and reference/deep_research_test_results.md for parser agent pattern

**Centralized Prompt System:**

- All agent prompts defined in `demo/prompts/catalog.yaml` (4 agents: deep_research, research_parser, incremental_search, assessment)
- Dynamic loading via `demo/prompts/library.py` using `get_prompt(name)` function
- Prompts injected using `**prompt.as_agent_kwargs()` pattern (provides description, instructions, markdown settings)
- Enables code-free prompt editing and consistent structure across agents
- Follows Agno context engineering best practices from `reference/docs_and_examples/agno/agno_contextmanagement.md`

**Context Management Features:**

- `add_datetime_to_context=True` enabled on Deep Research, Incremental Search, and Assessment agents (NOT parser agent)
- Provides temporal awareness for understanding "recent", "current", "latest" in executive research
- System messages include current timestamp for recency signals
- ReasoningTools uses `add_instructions=True` to inject tool usage guidance into system prompt

**Key Design Patterns:**

- Evidence-aware scoring: Use None/null for unknown dimensions (never 0 or NaN)
- Overall score calculated in Python, not by LLM
- Type safety via Pydantic for all structured outputs
- Built-in retry/backoff for resilience
- Deep Research + parser handshake: Markdown → structured output with citation normalization
