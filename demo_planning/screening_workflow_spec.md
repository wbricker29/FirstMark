# Candidate Screening Workflow Specification

> Detailed specification for the Agno-based candidate screening workflow with conditional research supplementation

**Created:** 2025-01-16
**Status:** Implementation Ready

---

## Overview

The candidate screening workflow implements an intelligent research-then-evaluate pattern with a quality gate that triggers supplemental research only when needed. This ensures high-quality assessments while optimizing for execution time.

## Workflow Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   CANDIDATE SCREENING WORKFLOW               │
└─────────────────────────────────────────────────────────────┘

Step 1: Deep Research Agent
├─ Model: o4-mini-deep-research (always-on)
├─ Output: ExecutiveResearchResult (structured)
├─ Duration: 2-6 minutes (Deep Research latency)
└─ Captures: Experiences, expertise, leadership, citations, confidence, gaps

                            ↓

Step 2: Research Quality Check (pure function)
├─ Evaluates: Sufficiency of research for assessment
├─ Criteria (example heuristics):
│   • ≥3 citations
│   • Non-empty summary + ≥3 key experiences
│   • Research confidence != Low
├─ Output: `(research, is_sufficient)`
└─ Decision: Proceed directly to assessment OR run a single incremental search pass

                            ↓

Step 3 (Optional): Incremental Search Agent
├─ Triggered only when Step 2 deems research insufficient
├─ Agent: gpt-5-mini + `web_search_preview`
├─ Constraint: ≤2 tool calls total
├─ Output: ResearchAddendum (new findings + citations)
└─ Merge: Combine Deep Research + addendum into final ExecutiveResearchResult

                            ↓

Step 4: Assessment Agent (ReasoningTools-enabled)
├─ Model: gpt-5-mini
├─ Tools: `ReasoningTools(add_instructions=True)` (required)
├─ Input: Final research + role spec markdown
├─ Output: AssessmentResult (structured JSON + reasoning trace)
└─ Duration: 30-60 sec

                            ↓

FINAL RESULT → Persisted on Assessments table (research_structured_json,
research_markdown_raw, assessment_json, summary fields, status updates)
```

---

## Agents Specification

### 1. Deep Research Agent

**Purpose:** Comprehensive executive research using OpenAI's Deep Research API (no fast-mode toggle in v1).

**Configuration:**
```python
deep_research_agent = Agent(
    name="Deep Research Agent",
    model=OpenAIResponses(id="o4-mini-deep-research", max_tool_calls=1),
    instructions="""
        Research this executive comprehensively for talent evaluation.

        Focus on:
        - Career trajectory: roles, companies, tenure, progression
        - Leadership experience: team sizes, scope of responsibility
        - Domain expertise: technical/functional areas, industry sectors
        - Company stage experience: startup, growth, scale, public
        - Notable achievements: exits, fundraising, product launches
        - Public evidence: LinkedIn, company sites, news articles

        Be explicit about:
        - What you found with supporting citations
        - What you couldn't find (gaps)
        - Confidence level based on evidence quality/quantity

        Return the ExecutiveResearchResult schema directly (no parser step).
    """,
    output_schema=ExecutiveResearchResult,
    exponential_backoff=True,
    retries=2,
    retry_delay=1,
)
```

**Output Schema:**
```python
# NOTE: Canonical research schema (with full fields) is defined in
# demo_planning/data_design.md. This simplified version highlights
# the fields most relevant to the screening workflow quality gate.

class Citation(BaseModel):
    url: str
    quote: str
    relevance: str = Field(description="Why this source is relevant")

class ExecutiveResearchResult(BaseModel):
    exec_id: str
    exec_name: str
    summary: str = Field(description="2-3 sentence executive summary")
    key_experiences: List[str] = Field(description="Notable roles and achievements")
    domain_expertise: List[str] = Field(description="Technical/functional domains")
    leadership_evidence: List[str] = Field(description="Team building and leadership examples")
    stage_experience: List[str] = Field(description="Company stages worked at")
    sector_experience: List[str] = Field(description="Industry sectors")
    citations: List[Citation] = Field(description="Source URLs and quotes")
    research_confidence: str = Field(description="High/Medium/Low based on evidence quality and quantity")
    gaps: List[str] = Field(description="Information not found or unclear from public sources")
```

**Execution Mode:**
- Always use o4-mini-deep-research for comprehensive analysis (2-6 minutes). Optional incremental search is handled as a separate step, not as a global “fast mode”.

---

### 2. Incremental Search Agent (Optional)

**Purpose:** Single-pass supplemental research when Deep Research quality heuristics fail. Limited to **two** tool calls to keep latency predictable.

**Configuration:**
```python
incremental_search_agent = Agent(
    name="Incremental Search Agent",
    model=OpenAIResponses(id="gpt-5-mini"),
    tools=[{"type": "web_search_preview"}],
    max_tool_calls=2,
    instructions="""
        You are a single-pass supplemental researcher. Only run when Deep Research results
        lack sufficient citations or key evidence. Perform at most two targeted searches
        to address the supplied gaps, then stop.

        Return only NEW information plus the citations that support it. If gaps remain,
        document them explicitly.
    """,
    output_schema=ResearchAddendum,
    exponential_backoff=True,
    retries=1,
)
```

**Output Schema:**
```python
class ResearchAddendum(BaseModel):
    """Single-pass supplemental research from incremental search."""
    new_findings: List[str] = Field(description="Additional discoveries not in original research")
    filled_gaps: List[str] = Field(description="Which specific gaps were addressed")
    citations: List[Citation] = Field(description="New sources")
    confidence: str = Field(description="High/Medium/Low for new findings")
    remaining_gaps: List[str] = Field(description="Gaps still not filled")
```

---

### 3. Assessment Agent

**Purpose:** Evaluate candidate against role specification using complete research.

**Configuration:**
```python
assessment_agent = Agent(
    name="Assessment Agent",
    model=OpenAIResponses(id="gpt-5-mini"),
    tools=[{"type": "web_search_preview"}],  # Optional context verification
    instructions="""
        Evaluate candidate against role specification using provided research.

        You will receive:
        - Complete executive research (original + supplements if applicable)
        - Role specification with weighted dimensions

        Your evaluation process:
        1. For each dimension in the role spec:
           - Score 1-5 (1 = weakest, 5 = strongest)
           - If there is Unknown/No Evidence, leave the score as null/None
           - Assign confidence (High/Medium/Low)
           - Provide evidence-based reasoning with quotes
           - Cite specific sources

        2. Generate overall assessment:
           - Top 3-5 reasons FOR this candidate
           - Top 3-5 reasons AGAINST or concerns
           - Critical assumptions (counterfactuals)

        3. Use web search ONLY if you need to:
            - Verify specific claims about companies/roles
            - Look up industry context (e.g., typical metrics for stage/sector)
            - Validate assumptions critical to assessment

        Be explicit when evidence is insufficient - leave the score as null/None
        for that dimension instead of guessing.
        Minimize searches - rely primarily on research results provided.
    """,
    output_schema=AssessmentResult,
    exponential_backoff=True,
    retries=2,
)
```

**Output Schema:**
```python
class DimensionScore(BaseModel):
    # NOTE: Canonical DimensionScore / AssessmentResult definitions live in
    # demo_planning/data_design.md. This version adds optional fields that are
    # convenient for the screening workflow implementation.

    dimension: str
    weight: float = Field(description="From role spec (0-1, used in Python weighting)")
    evidence_level: str = Field(description="High/Medium/Low from role spec (expected observability)")
    score: Optional[int] = Field(
        default=None,
        ge=1,
        le=5,
        description="1-5 = strength level; None = Unknown/Insufficient evidence",
    )
    confidence: str = Field(description="High/Medium/Low")
    evidence: List[str] = Field(description="Specific evidence supporting this score")
    reasoning: str = Field(description="Why this score was assigned")

class AssessmentResult(BaseModel):
    candidate_id: str
    role_id: str
    overall_score: Optional[float] = Field(
        default=None,
        ge=0,
        le=100,
        description="Calculated in Python, not by LLM",
    )
    overall_confidence: str = Field(description="High/Medium/Low")
    dimension_scores: List[DimensionScore]
    top_reasons_for: List[str] = Field(description="3-5 key strengths for this role")
    top_reasons_against: List[str] = Field(description="3-5 key concerns or gaps")
    counterfactuals: List[str] = Field(description="Critical assumptions that must be true for this match to work")
    relationship_type: str = Field(description="Guild/Portfolio Exec/Partner 1st-degree/Event")
    assessment_method: str = Field(description="spec-guided or model-generated")
```

---

## Workflow Steps Specification

### Step 1: Deep Research

**Type:** Agent Step
**Executor:** `deep_research_agent`

**Input:**
```python
prompt = f"""
Candidate: {candidate.name}
Current Title: {candidate.current_title} at {candidate.current_company}
LinkedIn: {candidate.linkedin_url}

Research this executive comprehensively.
"""
```

**Output:** `ExecutiveResearchResult` (Pydantic model)

**Expected Duration:**
- Deep Research mode: 2-5 minutes
- Fast mode: 30-60 seconds

---

### Step 2: Research Quality Check

**Type:** Custom Function Step
**Executor:** `check_research_quality()`

**Purpose:** Evaluate if research is sufficient to proceed to assessment.

**Implementation:**
```python
def check_research_quality(step_input: StepInput) -> StepOutput:
    """
    Evaluate if research is sufficient for assessment.

    Returns StepOutput with:
    - content: enriched research result
    - success: True if sufficient, False if needs supplemental search
    """
    research: ExecutiveResearchResult = step_input.previous_step_content

    # Sufficiency criteria
    has_enough_experiences = len(research.key_experiences) >= 3
    has_enough_expertise = len(research.domain_expertise) >= 2
    has_enough_citations = len(research.citations) >= 3
    confidence_acceptable = research.research_confidence in ["High", "Medium"]
    few_gaps = len(research.gaps) <= 2

    sufficient = all([
        has_enough_experiences,
        has_enough_expertise,
        has_enough_citations,
        confidence_acceptable,
        few_gaps,
    ])

    # Calculate quality score
    quality_score = (
        (len(research.key_experiences) * 10) +
        (len(research.domain_expertise) * 15) +
        (len(research.citations) * 5) +
        (30 if confidence_acceptable else 0) +
        (20 if few_gaps else 0)
    )

    enriched = {
        "research": research,
        "is_sufficient": sufficient,
        "gaps_to_fill": research.gaps if not sufficient else [],
        "quality_score": quality_score,
        "criteria_met": {
            "experiences": has_enough_experiences,
            "expertise": has_enough_expertise,
            "citations": has_enough_citations,
            "confidence": confidence_acceptable,
            "gaps": few_gaps,
        }
    }

    return StepOutput(
        content=enriched,
        success=sufficient,  # Determines if condition executes
    )
```

**Input:** `ExecutiveResearchResult` from Step 1
**Output:** Enriched research dict with `is_sufficient` flag
**Success Flag:** `True` = sufficient (skip to assessment), `False` = insufficient (trigger supplemental search)

---

### Step 3: Conditional Supplemental Search

**Type:** Condition Step
**Evaluator:** `lambda step_input: step_input.previous_step_content["is_sufficient"]`

**Executes only if:** Research is NOT sufficient (evaluator returns `False`)

#### Step 3a: Prepare Supplemental Search

**Type:** Custom Function Step
**Executor:** `coordinate_supplemental_search()`

**Implementation:**
```python
def coordinate_supplemental_search(step_input: StepInput) -> StepOutput:
    """
    Prepare targeted search queries based on research gaps.
    """
    quality_check = step_input.previous_step_content
    gaps = quality_check.get("gaps_to_fill", [])
    original_research = quality_check["research"]

    # Generate targeted search prompts
    search_prompt = f"""
    ORIGINAL RESEARCH SUMMARY:
    {original_research.summary}

    IDENTIFIED GAPS:
    {chr(10).join(f'- {gap}' for gap in gaps)}

    MISSING INFORMATION:
    - Experiences: {3 - len(original_research.key_experiences)} more needed
    - Expertise: {2 - len(original_research.domain_expertise)} more needed
    - Citations: {3 - len(original_research.citations)} more needed

    YOUR TASK:
    Conduct targeted web searches to fill these specific gaps.
    Focus on: LinkedIn profile details, recent company news, domain expertise evidence.
    Be specific and cite sources.
    """

    return StepOutput(content=search_prompt)
```

**Output:** Search prompt for web search agent

#### Step 3: Incremental Search (Optional)

**Type:** Conditional Agent Step (executed when quality check fails)

**Implementation:**
```python
def run_incremental_search(step_input: StepInput) -> StepOutput:
    prompt = step_input.previous_step_content["search_prompt"]
    addendum: ResearchAddendum = incremental_search_agent.run(prompt).content
    return StepOutput(content={
        "research": step_input.previous_step_content["research"],
        "addendum": addendum,
    })
```

#### Step 4: Merge Research

**Type:** Custom Function Step
**Executor:** `merge_research()`

**Implementation:**
```python
def merge_research(step_input: StepInput) -> StepOutput:
    """
    Merge original research with all supplemental findings.
    """
    # Access workflow history to get original research
    quality_check_output = step_input.previous_step_content  # From loop

    addendum: Optional[ResearchAddendum] = quality_check_output.get("addendum")
    original_research: ExecutiveResearchResult = quality_check_output["research"]

    if not addendum:
        return StepOutput(content=original_research)

    all_new_findings = addendum.new_findings
    all_new_citations = addendum.citations
    all_filled_gaps = addendum.filled_gaps

    for supplement in supplements:
        all_new_findings.extend(supplement.new_findings)
        all_new_citations.extend(supplement.citations)
        all_filled_gaps.extend(supplement.filled_gaps)

    # Create merged research result
    merged = ExecutiveResearchResult(
        exec_id=original_research.exec_id,
        exec_name=original_research.exec_name,
        summary=f"{original_research.summary} (Enhanced with supplemental research)",
        key_experiences=original_research.key_experiences + [
            f for f in all_new_findings if "experience" in f.lower() or "role" in f.lower()
        ],
        domain_expertise=original_research.domain_expertise + [
            f for f in all_new_findings if "expertise" in f.lower() or "domain" in f.lower()
        ],
        leadership_evidence=original_research.leadership_evidence + [
            f for f in all_new_findings if "leadership" in f.lower() or "team" in f.lower()
        ],
        stage_experience=original_research.stage_experience,
        sector_experience=original_research.sector_experience,
        citations=original_research.citations + all_new_citations,
        research_confidence="High",  # Upgraded after supplemental research
        gaps=[g for g in original_research.gaps if g not in all_filled_gaps],
    )

    return StepOutput(content=merged)
```

**Input:** Original research (+ optional addendum)
**Output:** Final `ExecutiveResearchResult`

---

### Step 4: Assessment

**Type:** Agent Step
**Executor:** `assessment_agent`

**Input:**
```python
assessment_prompt = f"""
ROLE SPECIFICATION:
{role_spec.markdown_content}

CANDIDATE RESEARCH:
{research_result}

EVALUATION TASK:
Evaluate this candidate against the role specification.
Provide dimension-level scores, overall assessment, and reasoning.
"""
```

**Input Source:**
- If research was sufficient: Original research from Step 1
- If supplemental search occurred: `merge_research` output (Deep Research + single addendum)

**Output:** `AssessmentResult` (Pydantic model)

---

## Complete Workflow Definition

```python
from agno.workflow import Workflow, Step, Condition, StepInput, StepOutput
from agno.db.sqlite import SqliteDb

candidate_screening_workflow = Workflow(
    name="Candidate Screening Workflow",
    description="Deep research → quality check → optional incremental search → assessment",
    db=SqliteDb(db_file="tmp/agno_sessions.db"),
    stream_events=True,
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

---

## Usage Pattern

### Single Candidate Screening

```python
async def screen_candidate(candidate, role_spec):
    """Screen a single candidate through the workflow."""

    # Prepare input prompt
    prompt = f"""
    Candidate: {candidate.name}
    Current Title: {candidate.current_title} at {candidate.current_company}
    LinkedIn: {candidate.linkedin_url}

    Role Specification:
    {role_spec.markdown_content}
    """

    # Run workflow with event streaming
    result_stream = candidate_screening_workflow.arun(
        input=prompt,
        stream=True,
        stream_events=True,
    )

    # Collect events and final result
    events = []
    final_result = None

    async for event in result_stream:
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
        ignore_unknown=True,
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

### Batch Processing (Multiple Candidates)

```python
@app.route('/screen', methods=['POST'])
async def run_screening():
    """Flask endpoint for batch candidate screening.

    NOTE: This async pattern is a Phase 2 optimization. For the initial
    demo, a simpler synchronous endpoint that processes candidates one
    at a time (as described in case/technical_spec_V2.md) is sufficient.
    """
    screen_id = request.json['screen_id']

    # Get screen details
    screen = airtable.get_screen(screen_id)
    candidates = airtable.get_linked_candidates(screen)
    role_spec = airtable.get_role_spec(screen.role_spec_id)

    # Update screen status
    airtable.update_screen(screen_id, status="Processing")

    # Process all candidates concurrently
    tasks = [
        screen_candidate(candidate, role_spec)
        for candidate in candidates
    ]

    results = await asyncio.gather(*tasks)

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

## Event Logging & Audit Trail

### Events Captured

The workflow captures all events with `store_events=True`:

1. **Workflow Events:**
   - `workflow_started`
   - `workflow_completed`

2. **Step Events:**
   - `step_started` (for each step)
   - `step_completed` (for each step)
   - Step name, duration, executor type

3. **Condition Events:**
   - `condition_execution_started`
   - `condition_execution_completed`
   - Evaluator result (True/False)

4. **Agent Events:**
   - `run_started`, `run_completed`
   - `tool_call_started`, `tool_call_completed`
   - Tool names, arguments, results
   - Token usage, model info

### Event Storage

**Database:** Agno `SqliteDb(db_file="tmp/agno_sessions.db")` (demo default). No custom Workflows table for v1; we rely on Assessments status/error fields for the user-facing audit trail.

**Access:**
```python
workflow_run_output = await candidate_screening_workflow.arun(...)
events = workflow_run_output.events  # Inspect locally via SqliteDb viewer
```

**Airtable Storage:**
- Screens table: `status`, `last_run_timestamp`, `error_message`
- Assessments table: `status`, `runtime_seconds`, `error_message`, `research_structured_json`, `assessment_json`
- `events_json` (full event log as JSON)
- `duration` (total execution time)
- `steps_executed` (list of step names)
- `supplemental_search_triggered` (boolean)
- `supplemental_iterations` (0-3)

---

## Execution Time Estimates

### Best Case (Sufficient Research)
- Step 1 (Deep Research): 2-5 min
- Step 2 (Quality Check): <1 sec
- Step 3 (Condition): Skipped
- Step 4 (Assessment): 30-60 sec
- **Total:** ~3-6 minutes per candidate

### Worst Case (Insufficient Research → Incremental Search)
- Step 1 (Deep Research): 2-5 min
- Step 2 (Quality Check): <1 sec
- Step 3a (Prepare incremental search): <1 sec
- Step 3b (Incremental search, ≤2 tool calls): 30-90 sec
- Step 3c (Merge): <1 sec
- Step 4 (Assessment): 30-60 sec
- **Total:** ~4-7 minutes per candidate

### Batch Processing (10 Candidates, Async)
- **Best case:** 3-6 minutes (all parallel)
- **Worst case:** 5-9 minutes (all parallel)
- **Mixed:** ~4-8 minutes (some trigger supplemental, some don't)

---

## Configuration & Toggles

### Environment Variables

```bash
# Quality gate thresholds (optional overrides)
MIN_EXPERIENCES=3
MIN_EXPERTISE=2
MIN_CITATIONS=3
MAX_GAPS=2
```

### Runtime Configuration

```python
# Pass additional data to workflow
workflow.arun(
    input=prompt,
    additional_data={
        "min_experiences": 3,
        "min_expertise": 2,
    }
)

# Access in custom functions
def check_research_quality(step_input: StepInput) -> StepOutput:
    config = step_input.additional_data or {}
    min_experiences = config.get("min_experiences", 3)
    # ... use config values
```

---

## Error Handling & Retries

### Agent-Level Retries

All agents configured with:
```python
exponential_backoff=True,
retries=2,
retry_delay=1,
```

**Behavior:**
- Retries on model provider errors (rate limits, timeouts)
- Exponential backoff between retries
- Max 2 retry attempts per agent call

### Workflow-Level Error Handling

```python
try:
    result = await candidate_screening_workflow.arun(input=prompt, stream=True)
    async for event in result:
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
    airtable.update_workflow_status(
        workflow_id=workflow_record_id,
        status="Failed",
        error_message=str(e),
    )

    raise
```

### Custom Exception Handling

```python
from agno.exceptions import RetryAgentRun, StopAgentRun

# In custom functions or tools
def check_research_quality(step_input: StepInput) -> StepOutput:
    research = step_input.previous_step_content

    if research is None or not isinstance(research, ExecutiveResearchResult):
        raise RetryAgentRun(
            "Research step did not return valid ExecutiveResearchResult. "
            "Please re-run research with stricter output schema validation."
        )

    # Continue with quality check...
```

---

## Testing Strategy

### Unit Tests

```python
# Test quality check logic
def test_quality_check_sufficient():
    research = ExecutiveResearchResult(
        exec_id="test_001",
        key_experiences=["A", "B", "C"],
        domain_expertise=["X", "Y"],
        citations=[...],  # 3 citations
        research_confidence="High",
        gaps=[],
    )

    result = check_research_quality_logic(research)
    assert result["is_sufficient"] == True

def test_quality_check_insufficient():
    research = ExecutiveResearchResult(
        exec_id="test_002",
        key_experiences=["A"],  # Only 1
        domain_expertise=["X"],
        citations=[...],  # Only 1
        research_confidence="Low",
        gaps=["Missing career history", "No leadership examples", "Limited expertise"],
    )

    result = check_research_quality_logic(research)
    assert result["is_sufficient"] == False
    assert len(result["gaps_to_fill"]) == 3
```

### Integration Tests

```python
# Test full workflow with mock candidate
async def test_workflow_sufficient_research():
    """Test workflow when initial research is sufficient."""

    mock_candidate = create_mock_candidate()
    mock_role_spec = create_mock_role_spec()

    result = await screen_candidate(mock_candidate, mock_role_spec)

    # Verify no supplemental search was triggered
    assert "supplemental_search_loop" not in [e.step_name for e in result.events]
    assert isinstance(result.assessment, AssessmentResult)
    assert result.assessment.overall_score > 0

async def test_workflow_insufficient_research():
    """Test workflow when supplemental search is needed."""

    # Use a candidate with minimal public info
    sparse_candidate = create_sparse_candidate()
    mock_role_spec = create_mock_role_spec()

    result = await screen_candidate(sparse_candidate, mock_role_spec)

    # Verify supplemental search was triggered
    loop_events = [e for e in result.events if "loop" in e.event]
    assert len(loop_events) > 0
    assert isinstance(result.assessment, AssessmentResult)
```

---

## Production Considerations

### Scalability

**Current Design:** Single workflow instance, sequential candidate processing within workflow

**Scaling Options:**
1. **Horizontal:** Multiple Flask workers processing different screens concurrently
2. **Concurrent Candidates:** `asyncio.gather()` for batch processing within screen
3. **Queue-Based:** Background job queue (Celery, RQ) for long-running workflows

### Cost Optimization

**Estimated API Costs per Candidate (v1):**
- Deep Research: ~$0.36 (dominant cost)
- Incremental search (when triggered): ~$0.01-0.02 (two gpt-5-mini tool calls)
- Assessment: marginal (<$0.01)

**Optimization Strategies:**
1. Reduce candidate batch size for live demos rather than switching models
2. Cache research/assessment artifacts for candidates who appear in multiple screens
3. Reuse incremental search prompts when evaluating multiple candidates for the same role (shared gaps)

### Monitoring & Observability

**Metrics to Track:**
1. Workflow execution time (p50, p95, p99)
2. Supplemental search trigger rate
3. Quality check pass/fail rate
4. Agent error rates
5. Token usage and costs

**Logging:**
```python
import structlog

logger = structlog.get_logger()

# Log workflow start
logger.info("workflow_started",
    candidate_id=candidate.id,
    role_id=role_spec.id,
    mode="deep_research")

# Log quality check decision
logger.info("quality_check_complete",
    candidate_id=candidate.id,
    is_sufficient=result["is_sufficient"],
    quality_score=result["quality_score"])

# Log supplemental search
logger.info("supplemental_search_triggered",
    candidate_id=candidate.id,
    gaps_count=len(result["gaps_to_fill"]))
```

---

## Future Enhancements

### Phase 2 Improvements

1. **Adaptive Quality Thresholds:** Adjust sufficiency criteria based on role seniority.
2. **Smarter Incremental Search Decisions:** Learn when incremental search is likely to help vs. when to skip entirely.
3. **Research Caching:** Cache research results by candidate ID and invalidate on profile updates/time.
4. **Parallel Supplemental Search:** If incremental search remains helpful, explore parallelizing the two tool calls or adding curated sources.
5. **Custom Quality Metrics:** Role-specific quality gates + domain-aware sufficiency criteria.

---

## References

- **Agno Workflows Documentation:** `reference/docs_and_examples/agno/agno_workflows.md`
- **Agno Workflow Patterns:** `reference/docs_and_examples/agno/agno_workflowpatterns.md`
- **OpenAI Integration:** `reference/docs_and_examples/agno/agno_openai_itegration.md`
- **Technical Specification:** `case/technical_spec_V2.md`
- **Role Spec Design:** `demo_planning/role_spec_design.md`
- **Data Design:** `demo_planning/data_design.md`

---

## Changelog

- **2025-11-16**
  - Fixed conditional supplemental-search logic to only run when research is insufficient (`supplemental_search_condition` evaluator now negates `is_sufficient`).
  - Corrected loop end-condition semantics to align with Agno (`search_complete` now returns `True` to break the loop).
  - Updated assessment scoring guidance and `DimensionScore` schema to use evidence-aware `None` for Unknown, consistent with `demo_planning/data_design.md`.
  - Added notes pointing to canonical schema definitions in `demo_planning/data_design.md`.
  - Clarified that the async batch `/screen` endpoint is a Phase 2 optimization and that v1 can use a simpler synchronous implementation.
  - Updated technical spec reference to `case/technical_spec_V2.md`.

**Document Status:** Implementation Ready
**Last Updated:** 2025-11-16
**Next Steps:** Begin implementation in `demo_files/` directory
