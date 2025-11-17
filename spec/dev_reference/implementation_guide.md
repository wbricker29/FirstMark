# Talent Signal Agent - V1 Implementation Guide

**Version:** 1.0
**Created:** 2025-01-19
**Status:** Implementation Ready

---

## Authority & Cross-References

**This document implements the scope defined in `spec/v1_minimal_spec.md`.**
When conflicts arise, `spec/v1_minimal_spec.md` takes precedence.

**Purpose:** Practical implementation guide consolidating Pydantic models, agent configurations, workflow orchestration, and Deep Research API limitations for the v1.0-minimal prototype.

**Related Documents:**
- **Authoritative scope**: `spec/v1_minimal_spec.md` (v1 contract)
- **Product requirements**: `spec/prd.md`
- **Technical specification**: `spec/spec.md`
- **Airtable schema**: `airtable_ai_spec.md`
- **Role templates**: `role_spec_design.md`

---

## Table of Contents

1. [V1 Scope Summary](#v1-scope-summary)
2. [Deep Research API Limitations](#deep-research-api-limitations)
3. [Pydantic Models](#pydantic-models)
4. [Agent Configurations](#agent-configurations)
5. [Workflow Implementation](#workflow-implementation)
6. [Quality Check Logic](#quality-check-logic)
7. [Airtable Integration](#airtable-integration)
8. [Score Calculation](#score-calculation)
9. [Error Handling](#error-handling)
10. [Quick Reference](#quick-reference)

---

## V1 Scope Summary

### Core Contract (from spec/v1_minimal_spec.md)

**Functional Scope:**
- **One primary workflow:** Module 4 (Screen) - sequential candidate processing
- **Research mode:** Deep Research (`o4-mini-deep-research`) only - no fast mode
- **Optional enhancement:** Single incremental search pass (≤2 web tool calls) when quality check fails
- **Assessment:** ReasoningTools-enabled gpt-5-mini agent
- **UI:** Airtable-only (no custom interfaces)

**Technical Constraints:**
- **Execution:** Synchronous, single-process (no async/concurrent processing)
- **Database:** Agno's `SqliteDb(db_file="tmp/agno_sessions.db")` for session state only
- **No custom tables:** No WorkflowEvent model, no custom event logging tables
- **Airtable storage:** All research + assessment data in Assessments table (7 tables total: 6 core + 1 helper)
- **Audit trail:** Airtable status fields + terminal logs (no separate Workflows/Research_Results tables)

**Phase 2+ (NOT in v1):**
- Fast mode (gpt-5 + web search)
- Multi-iteration supplemental search loops
- Async/concurrent candidate processing
- Custom SQLite event tables
- Separate Workflows or Research_Results tables
- Parser agents (Deep Research returns markdown)

---

## Deep Research API Limitations

### Critical Constraint

**The Deep Research models (`o3-deep-research`, `o4-mini-deep-research`) do NOT support structured outputs.**

```python
# ❌ THIS WILL FAIL
deep_research_agent = Agent(
    model=OpenAIResponses(id="o4-mini-deep-research"),
    output_schema=ExecutiveResearchResult,  # ERROR: json_schema not supported
)
```

**Error Message:**
```
OpenAI API Error 400: Invalid parameter: 'text.format' of type 'json_schema'
is not supported with model version `o4-mini-deep-research`.
```

### V1 Implementation Approach

**Deep Research returns markdown** with inline citations. Structure the data through:
1. **Prompting**: Request well-organized markdown sections
2. **Lightweight parsing**: Extract citations from RunOutput object
3. **Direct storage**: Save markdown blob + metadata to Airtable

**What IS accessible:**
- ✅ `result.content` - Markdown research text with inline citations
- ✅ `result.citations.urls` - List of UrlCitation objects (url, title)
- ✅ `result.metrics` - Token usage and cost data

**Characteristics:**
- **Time:** 2-6 minutes per candidate (with `max_tool_calls=1`)
- **Cost:** ~$0.36 per candidate (~36K tokens @ $10/1M)
- **Quality:** Comprehensive, well-cited research
- **Format:** Structured markdown with inline citations

---

## Pydantic Models

### Research Output Models

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
    """Structured research output."""
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
    stage_exposure: list[str] = Field(default_factory=list)

    # Summary & Evidence
    research_summary: str
    key_achievements: list[str] = Field(default_factory=list)
    notable_companies: list[str] = Field(default_factory=list)
    citations: list[Citation] = Field(default_factory=list)

    # Confidence & Gaps
    research_confidence: Literal["High", "Medium", "Low"] = "Medium"
    gaps: list[str] = Field(default_factory=list)

    # Metadata
    research_timestamp: datetime = Field(default_factory=datetime.now)
    research_model: str = "o4-mini-deep-research"
```

### Assessment Output Models

```python
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

class MustHaveCheck(BaseModel):
    """Evaluation of must-have requirements."""
    requirement: str
    met: bool
    evidence: Optional[str] = None

class AssessmentResult(BaseModel):
    """Structured assessment output from gpt-5-mini."""

    # Overall Assessment
    overall_score: Optional[float] = Field(None, ge=0, le=100)
    # Computed in Python from dimension scores
    overall_confidence: Literal["High", "Medium", "Low"]

    # Dimension-Level Scores
    dimension_scores: list[DimensionScore]

    # Requirements Checking
    must_haves_check: list[MustHaveCheck] = Field(default_factory=list)
    red_flags_detected: list[str] = Field(default_factory=list)
    green_flags: list[str] = Field(default_factory=list)

    # Qualitative Assessment
    summary: str  # 2-3 sentence topline
    counterfactuals: list[str] = Field(default_factory=list)

    # Metadata
    assessment_timestamp: datetime = Field(default_factory=datetime.now)
    assessment_model: str = "gpt-5-mini"
    role_spec_used: Optional[str] = None
```

### Evidence-Aware Scoring Notes

**Critical Design Principle:**
- Use `None` (Python) / `null` (JSON) for "Unknown/Insufficient Evidence"
- **Never use:** NaN, 0, or empty string for missing scores
- Prevents forced guessing when public data is thin

**Example:**
```python
# Checking for unknown scores
if dimension.score is None:
    print(f"{dimension.dimension}: Insufficient evidence")

# Filtering scored dimensions for overall score calculation
scored_dims = [d for d in assessment.dimension_scores if d.score is not None]
```

---

## Agent Configurations

### 1. Deep Research Agent

```python
from agno import Agent
from agno.models.openai import OpenAIResponses

# Deep Research Agent - Returns markdown (NO structured output support)
deep_research_agent = Agent(
    name="Deep Research Agent",
    model=OpenAIResponses(id="o4-mini-deep-research", max_tool_calls=1),
    # NO output_schema - API doesn't support structured outputs
    instructions="""
        Research this executive comprehensively using all available sources.

        Focus on:
        - Career trajectory: roles, companies, tenure, progression
        - Leadership experience: team sizes, scope of responsibility
        - Domain expertise: technical/functional areas, industry sectors
        - Company stage experience: startup, growth, scale, public
        - Notable achievements: exits, fundraising, product launches
        - Public evidence: LinkedIn, company sites, news articles

        Structure your response with clear sections:
        - Executive Summary
        - Career Timeline
        - Leadership & Team Building
        - Domain Expertise
        - Stage & Sector Experience
        - Key Achievements
        - Gaps in Public Evidence

        Include inline citations with URLs and relevant quotes.

        Be explicit about:
        - What you found with supporting citations
        - What you couldn't find (gaps)
        - Confidence level based on evidence quality/quantity
    """,
    exponential_backoff=True,
    retries=2,
    retry_delay=1,
)

# Usage
result = deep_research_agent.run(f"""
    Candidate: {candidate.name}
    Current Title: {candidate.current_title} at {candidate.current_company}
    LinkedIn: {candidate.linkedin_url}

    Research this executive comprehensively.
""")

# Extract outputs
research_markdown = result.content  # Markdown text
citations = result.citations.urls  # List[UrlCitation]
```

### 2. Incremental Search Agent (Optional)

```python
# Incremental Search Agent - Single pass, ≤2 web tool calls
incremental_search_agent = Agent(
    name="Incremental Search Agent",
    model=OpenAIResponses(id="gpt-5-mini"),
    tools=[{"type": "web_search_preview"}],
    max_tool_calls=2,  # Hard limit: 2 tool calls maximum
    output_schema=ExecutiveResearchResult,  # gpt-5-mini DOES support structured outputs
    instructions="""
        You are a single-pass supplemental researcher. Only run when Deep Research
        results lack sufficient citations or key evidence.

        Perform at most TWO targeted web searches to address the supplied gaps,
        then stop.

        Return only NEW information plus the citations that support it.
        If gaps remain, document them explicitly in the gaps field.
    """,
    exponential_backoff=True,
    retries=1,
)
```

### 3. Assessment Agent (ReasoningTools Required)

```python
from agno.tools.reasoning import ReasoningTools

# Assessment Agent - ReasoningTools enabled (REQUIRED for v1)
assessment_agent = Agent(
    name="Assessment Agent",
    model=OpenAIResponses(id="gpt-5-mini"),
    tools=[ReasoningTools(add_instructions=True)],  # REQUIRED
    output_schema=AssessmentResult,
    instructions="""
        Evaluate candidate against role specification using provided research.

        You will receive:
        - Complete executive research (original + supplements if applicable)
        - Role specification with weighted dimensions

        Your evaluation process:
        1. For each dimension in the role spec:
           - Score 1-5 (1 = weakest, 5 = strongest)
           - If Unknown/No Evidence, set score to null/None
           - Assign confidence (High/Medium/Low)
           - Provide evidence-based reasoning with quotes
           - Cite specific sources

        2. Generate overall assessment:
           - Top 3-5 reasons FOR this candidate
           - Top 3-5 reasons AGAINST or concerns
           - Critical assumptions (counterfactuals)

        Be explicit when evidence is insufficient - use null/None for scores
        instead of guessing.
    """,
    exponential_backoff=True,
    retries=2,
)
```

---

## Workflow Implementation

### Complete Workflow Definition

```python
from agno.workflow import Workflow, Step, Condition, StepInput, StepOutput
from agno.db.sqlite import SqliteDb

candidate_screening_workflow = Workflow(
    name="Candidate Screening Workflow",
    description="Deep research → quality check → optional incremental search → assessment",
    db=SqliteDb(db_file="tmp/agno_sessions.db"),  # Required for session state
    stream_events=True,  # Log to stdout
    steps=[
        Step(
            name="deep_research",
            description="Comprehensive executive research",
            agent=deep_research_agent,
        ),
        Step(
            name="quality_check",
            description="Evaluate research sufficiency",
            executor=check_research_quality,
        ),
        Condition(
            name="incremental_search",
            description="Run incremental search only when research is insufficient",
            evaluator=lambda step_input: not step_input.previous_step_content["is_sufficient"],
            steps=[
                Step(
                    name="prepare_incremental",
                    description="Prepare targeted search prompt",
                    executor=coordinate_supplemental_search,
                ),
                Step(
                    name="run_incremental_search",
                    description="Single-pass incremental search",
                    executor=run_incremental_search,
                ),
                Step(
                    name="merge_research",
                    description="Merge deep research with incremental findings",
                    executor=merge_research,
                ),
            ],
        ),
        Step(
            name="assessment",
            description="Evaluate candidate against role specification",
            agent=assessment_agent,
        ),
    ],
)
```

### Step Implementations

#### Step 1: Deep Research

```python
# Input is prepared by Flask endpoint
prompt = f"""
Candidate: {candidate.name}
Current Title: {candidate.current_title} at {candidate.current_company}
LinkedIn: {candidate.linkedin_url}

Research this executive comprehensively.
"""

# Workflow handles execution
# Output: RunOutput with .content (markdown) and .citations
```

#### Step 2: Quality Check

```python
def check_research_quality(step_input: StepInput) -> StepOutput:
    """
    Evaluate if research is sufficient for assessment.

    Returns StepOutput with:
    - content: enriched research result
    - success: True if sufficient, False if needs supplemental search
    """
    research_result = step_input.previous_step_content  # RunOutput from deep_research

    # Extract markdown and citations
    research_markdown = research_result.content
    citations = research_result.citations.urls if research_result.citations else []

    # Sufficiency criteria (simple heuristics)
    has_enough_citations = len(citations) >= 3
    has_content = len(research_markdown) > 500  # Meaningful content

    # Simple quality score
    quality_score = (
        (len(citations) * 20) +  # Citations are valuable
        (50 if has_content else 0)
    )

    sufficient = has_enough_citations and has_content

    enriched = {
        "research_markdown": research_markdown,
        "citations": citations,
        "is_sufficient": sufficient,
        "quality_score": quality_score,
        "criteria_met": {
            "citations": has_enough_citations,
            "content": has_content,
        }
    }

    return StepOutput(
        content=enriched,
        success=sufficient,  # Determines if condition executes
    )
```

#### Step 3: Conditional Incremental Search

```python
def coordinate_supplemental_search(step_input: StepInput) -> StepOutput:
    """Prepare targeted search queries based on research gaps."""
    quality_check = step_input.previous_step_content

    search_prompt = f"""
    ORIGINAL RESEARCH SUMMARY:
    {quality_check["research_markdown"][:500]}...

    ISSUE: Research lacks sufficient citations or depth.

    YOUR TASK:
    Conduct TWO targeted web searches to enhance this research.
    Focus on: LinkedIn profile details, recent company news, domain expertise evidence.
    Be specific and cite sources.
    """

    return StepOutput(content={"search_prompt": search_prompt})

def run_incremental_search(step_input: StepInput) -> StepOutput:
    """Execute incremental search agent."""
    prompt = step_input.previous_step_content["search_prompt"]
    addendum: ExecutiveResearchResult = incremental_search_agent.run(prompt).content

    return StepOutput(content={
        "addendum": addendum,
    })

def merge_research(step_input: StepInput) -> StepOutput:
    """Merge original research with single incremental search addendum (v1: no loops)."""
    # Get original research from earlier step
    quality_check_output = step_input.previous_step_content
    addendum = quality_check_output.get("addendum")

    if not addendum:
        # No addendum, return original
        return StepOutput(content=quality_check_output["research_markdown"])

    # Create enhanced markdown combining both
    merged_markdown = f"""
{quality_check_output["research_markdown"]}

## Supplemental Research

{addendum.research_summary}

### Additional Citations
{[c.url for c in addendum.citations]}
"""

    return StepOutput(content=merged_markdown)
```

#### Step 4: Assessment

```python
# Input is prepared by workflow
assessment_prompt = f"""
ROLE SPECIFICATION:
{role_spec.markdown_content}

CANDIDATE RESEARCH:
{research_markdown}  # From merge_research or original deep_research

EVALUATION TASK:
Evaluate this candidate against the role specification.
Provide dimension-level scores, overall assessment, and reasoning.
"""

# Agent runs and returns AssessmentResult
```

### Single Candidate Execution

```python
def screen_candidate(candidate, role_spec):
    """Screen a single candidate through the workflow (synchronous)."""

    # Prepare input prompt
    prompt = f"""
    Candidate: {candidate.name}
    Current Title: {candidate.current_title} at {candidate.current_company}
    LinkedIn: {candidate.linkedin_url}

    Role Specification:
    {role_spec.markdown_content}
    """

    # Run workflow with event streaming (synchronous)
    result_stream = candidate_screening_workflow.run(
        input=prompt,
        stream=True,
        stream_events=True,
    )

    # Collect events and final result
    events = []
    final_result = None

    for event in result_stream:
        events.append(event)

        # Log progress
        if hasattr(event, 'event'):
            if event.event == 'step_started':
                logger.info(f"Started: {event.step_name}")
            elif event.event == 'step_completed':
                logger.info(f"Completed: {event.step_name}")

        final_result = event

    # Extract assessment from final output
    assessment: AssessmentResult = final_result.content

    # Calculate overall score in Python (not by LLM)
    overall_score = calculate_weighted_score(
        dimension_scores=assessment.dimension_scores,
    )

    assessment.overall_score = overall_score

    # Save to Airtable
    workflow_record = save_workflow_to_airtable(
        candidate_id=candidate.id,
        role_id=role_spec.id,
        assessment=assessment,
        events=events,
        workflow_run_id=final_result.run_id,
        execution_time=calculate_duration(events),
    )

    return assessment, workflow_record
```

### Batch Processing (Sequential)

```python
@app.route('/screen', methods=['POST'])
def run_screening():
    """Flask endpoint for batch candidate screening.

    V1 implementation processes candidates sequentially. Concurrent/async
    processing is deferred to Phase 2+.
    """
    screen_id = request.json['screen_id']

    # Get screen details
    screen = airtable.get_screen(screen_id)
    candidates = airtable.get_linked_candidates(screen)
    role_spec = airtable.get_role_spec(screen.role_spec_id)

    # Update screen status
    airtable.update_screen(screen_id, status="Processing")

    # Process all candidates sequentially (v1 approach)
    results = []
    for candidate in candidates:
        assessment, workflow_record = screen_candidate(candidate, role_spec)
        results.append((assessment, workflow_record))

    # Update screen with results
    airtable.update_screen(
        screen_id,
        status="Complete",
        candidates_processed=len(results),
        completed_at=datetime.utcnow(),
    )

    return {
        'status': 'success',
        'screen_id': screen_id,
        'candidates_processed': len(results),
        'results': [
            {
                'candidate_id': r[0].candidate_id,
                'overall_score': r[0].overall_score,
                'confidence': r[0].overall_confidence,
            }
            for r in results
        ]
    }
```

---

## Quality Check Logic

### Simple Heuristics (V1)

```python
def check_research_quality_logic(research_markdown: str, citations: list) -> dict:
    """
    V1 quality check: simple heuristics for research sufficiency.

    Args:
        research_markdown: Markdown text from deep research
        citations: List of citation objects

    Returns:
        Dict with is_sufficient flag and quality metrics
    """
    # Sufficiency criteria
    has_enough_citations = len(citations) >= 3
    has_content = len(research_markdown) > 500
    has_multiple_sources = len(set(c.url for c in citations)) >= 2

    # Calculate quality score
    quality_score = (
        (len(citations) * 20) +  # 20 points per citation
        (50 if has_content else 0) +  # 50 for meaningful content
        (30 if has_multiple_sources else 0)  # 30 for source diversity
    )

    sufficient = all([
        has_enough_citations,
        has_content,
    ])

    return {
        "is_sufficient": sufficient,
        "quality_score": quality_score,
        "criteria_met": {
            "citations": has_enough_citations,
            "content": has_content,
            "sources": has_multiple_sources,
        },
        "gaps": [] if sufficient else ["Insufficient citations or content depth"]
    }
```

---

## Airtable Integration

### Assessments Table Storage

**All research and assessment data goes into the Assessments table:**

```python
def save_workflow_to_airtable(
    candidate_id: str,
    role_id: str,
    research_markdown: str,
    research_citations: list,
    assessment: AssessmentResult,
    events: list,
    workflow_run_id: str,
    execution_time: float,
):
    """
    Save complete workflow results to Assessments table.

    V1 stores everything in Assessments table - no separate
    Workflows or Research_Results tables.
    """
    # Prepare research structured JSON
    research_structured = {
        "exec_name": assessment.candidate_name,
        "research_summary": research_markdown[:500],  # Truncated summary
        "citations": [
            {
                "url": c.url,
                "title": c.title,
            }
            for c in research_citations
        ],
        "research_timestamp": datetime.now().isoformat(),
        "research_model": "o4-mini-deep-research",
    }

    # Create assessment record
    assessment_record = {
        "candidate": [candidate_id],  # Link to People
        "role": [role_id],  # Link to Portco_Roles
        "status": "Complete",

        # Research data (all on Assessments table)
        "research_structured_json": json.dumps(research_structured),
        "research_markdown_raw": research_markdown,

        # Assessment data
        "assessment_json": assessment.json(),
        "assessment_markdown_report": generate_markdown_report(assessment),  # Optional

        # Summary fields for Airtable views
        "overall_score": assessment.overall_score,
        "overall_confidence": assessment.overall_confidence,
        "topline_summary": assessment.summary,

        # Execution metadata
        "runtime_seconds": execution_time,
        "assessment_timestamp": assessment.assessment_timestamp.isoformat(),
        "research_model": "o4-mini-deep-research",
        "assessment_model": "gpt-5-mini",
    }

    # Write to Airtable
    return airtable.assessments.create(assessment_record)
```

### Error Handling

```python
try:
    result = candidate_screening_workflow.run(input=prompt, stream=True)
    for event in result:
        # Process events
        pass
except Exception as e:
    logger.error(f"Workflow failed for candidate {candidate.id}: {e}")

    # Save partial results if available
    save_failed_workflow(
        candidate_id=candidate.id,
        error=str(e),
        partial_events=collected_events,
    )

    # Mark in Airtable
    airtable.update_assessment_status(
        assessment_id=assessment_record_id,
        status="Failed",
        error_message=str(e),
    )

    raise
```

---

## Score Calculation

### V1 Simple Average Algorithm

```python
def calculate_weighted_score(dimension_scores: list[DimensionScore]) -> Optional[float]:
    """
    Calculate simple average score from dimensions with scores.

    V1 uses simple average × 20 (ignores weights in AssessmentResult).
    Weights are preserved for Phase 2+ weighted calculation.

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
        >>> calculate_weighted_score(scores)
        70.0  # (4 + 3) / 2 * 20
    """
    scored = [d.score for d in dimension_scores if d.score is not None]

    if not scored:
        return None

    return (sum(scored) / len(scored)) * 20
```

---

## Error Handling

### Agent-Level Retries

All agents configured with:
```python
exponential_backoff=True,
retries=2,  # or 1 for incremental search
retry_delay=1,
```

**Behavior:**
- Retries on model provider errors (rate limits, timeouts)
- Exponential backoff between retries
- Max 2 retry attempts per agent call

### Workflow-Level Error Handling

```python
from agno.exceptions import RetryAgentRun, StopAgentRun

# In custom functions or tools
def check_research_quality(step_input: StepInput) -> StepOutput:
    research = step_input.previous_step_content

    if research is None or not hasattr(research, 'content'):
        raise RetryAgentRun(
            "Research step did not return valid output. "
            "Retrying with stronger validation."
        )

    # Continue with quality check...
```

---

## Quick Reference

### Key Technical Decisions

| Decision | V1 Implementation | Phase 2+ |
|----------|------------------|----------|
| **Research Mode** | Deep Research only (o4-mini-deep-research) | + Fast mode (gpt-5 + web search) |
| **Supplemental Search** | Single optional pass (≤2 tool calls) | Multi-iteration loops |
| **Execution** | Sequential, synchronous | Async, concurrent |
| **Database** | Agno SqliteDb (session state only) | + Custom event tables |
| **Airtable Tables** | 7 tables (6 core + 1 helper) | + Workflows, Research_Results |
| **Parser Agent** | NO (Deep Research → markdown) | Optional two-step parse |
| **Assessment Tools** | ReasoningTools (required) | + Additional tools |
| **Score Calculation** | Simple average × 20 | Weighted algorithm |

### Execution Time Estimates

**Per Candidate:**
- Deep Research: 2-6 minutes
- Quality Check: <1 second
- Incremental Search (if triggered): 30-90 seconds
- Assessment: 30-60 seconds
- **Total:** 3-7 minutes per candidate

**Batch Processing (10 Candidates, Sequential):**
- Best case: 30-60 minutes
- Worst case: 40-70 minutes

### Cost Estimates

**Per Candidate:**
- Deep Research: ~$0.36 (dominant cost)
- Incremental Search (if triggered): ~$0.01-0.02
- Assessment: <$0.01
- **Total:** ~$0.37 per candidate

**10 Candidates:** ~$3.70

### File Structure

```text
demo/
├── app.py              # Flask app + /screen endpoint
├── agents.py           # Agent creation functions
├── models.py           # Pydantic models
├── workflow.py         # Workflow definition + step executors
├── airtable_client.py  # Thin Airtable wrapper
├── settings.py         # Config/env loading
└── tmp/                # Gitignored (agno_sessions.db)
```

### Environment Variables

```bash
# Required
OPENAI_API_KEY=sk-...
AIRTABLE_API_KEY=key...
AIRTABLE_BASE_ID=app...

# Quality gate thresholds (optional overrides)
MIN_CITATIONS=3
MIN_CONTENT_LENGTH=500
```

---

## Implementation Checklist

Before starting implementation, verify:

- [ ] spec/v1_minimal_spec.md reviewed and understood
- [ ] Airtable base created with 7 tables (see airtable_ai_spec.md)
- [ ] Assessments table includes: research_structured_json, research_markdown_raw, assessment_json, assessment_markdown_report
- [ ] Deep Research agent configured WITHOUT output_schema
- [ ] Assessment agent configured WITH ReasoningTools(add_instructions=True)
- [ ] Workflow uses SqliteDb(db_file="tmp/agno_sessions.db")
- [ ] No custom WorkflowEvent model or event tables
- [ ] Sequential processing only (no async/concurrent)
- [ ] Simple average × 20 score calculation
- [ ] Error handling captures to Airtable status fields

---

**Document Version:** 1.0
**Last Updated:** 2025-01-19
**Status:** Implementation Ready
**Authority:** Implements spec/v1_minimal_spec.md

