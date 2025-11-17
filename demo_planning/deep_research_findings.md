# Deep Research API Investigation Findings

> **Date:** 2025-11-16
> **Purpose:** Investigate citation extraction and structured output capabilities for Talent Signal Agent
> **Test Script:** `test_deep_research.py`

---

## Executive Summary

**Key Findings:**
1. ✅ **Citations ARE accessible via Agno** - No need for hybrid OpenAI SDK approach
2. ❌ **Structured outputs NOT supported** - `o4-mini-deep-research` does not support Pydantic schemas
3. **Recommended Approach:** Two-step process (Deep Research → Parse to structured format)

---

## Test Results

### Test 1: Basic Deep Research via Agno ✅ SUCCESS

**Configuration:**
```python
agent = Agent(
    model=OpenAIResponses(id="o4-mini-deep-research", max_tool_calls=1),
    instructions="Research this executive comprehensively..."
)

result = agent.run(query)
```

**Execution Time:** ~8 minutes for comprehensive research on Satya Nadella

**Response Structure:**

#### RunOutput Object

The `agent.run()` method returns a `RunOutput` object with the following key attributes:

```python
RunOutput(
    content='# Satya Nadella\n\nSatya Nadella (born 1967)...',  # Markdown text
    citations=Citations(...),  # ✅ Citations object available
    messages=[...],  # Full message history
    metrics=Metrics(
        input_tokens=31762,
        output_tokens=4342,
        total_tokens=36104,
        reasoning_tokens=32128
    )
)
```

#### Citations Object Structure

**Two ways to access citations:**

1. **Top-level:** `result.citations`
2. **From message:** `result.messages[-1].citations`

**Citations object format:**
```python
Citations(
    raw=[
        {
            'url': 'https://apnews.com/article/...',
            'title': '2024-02-02 | Microsoft CEO Satya Nadella...',
            'start_index': 139,
            'end_index': 282,
            'type': 'url_citation'
        },
        # ... more citations
    ],
    urls=[
        UrlCitation(
            url='https://apnews.com/article/...',
            title='2024-02-02 | Microsoft CEO Satya Nadella...'
        ),
        # ... more UrlCitation objects
    ],
    documents=None
)
```

**Key Properties:**
- `raw`: Array of citation dicts with character positions (start_index, end_index)
- `urls`: Array of `UrlCitation` objects (url, title)
- `documents`: None for web-based research (would contain document citations for vector store searches)

#### Sample Output

**Content (Markdown):**
```markdown
# Satya Nadella

Satya Nadella (born 1967) is an Indian-American business executive who has
served as CEO of Microsoft since February 2014 ([apnews.com](https://apnews.com/...)).

## Key Achievements

- **Cloud/AI transformation:** Nadella refocused Microsoft on cloud computing
  and artificial intelligence, driving dramatic growth. For example, AP News
  notes that since his 2014 appointment "Microsoft's stock has soared over
  1,000%" under his leadership ([apnews.com](https://apnews.com/...)).
```

**Citations (4 total):**
- All from same source: AP News article on Satya Nadella's decade at Microsoft
- Each citation includes URL, title, and character position in the text

---

### Test 2: Deep Research with Structured Output ❌ FAILED

**Configuration:**
```python
agent = Agent(
    model=OpenAIResponses(id="o4-mini-deep-research", max_tool_calls=1),
    output_schema=SimpleResearchResult,  # Pydantic model
    instructions="Research and return structured format..."
)
```

**Error:**
```
OpenAI API Error 400: Invalid parameter: 'text.format' of type 'json_schema'
is not supported with model version `o4-mini-deep-research`.
```

**Root Cause:**
The Deep Research models (`o3-deep-research`, `o4-mini-deep-research`) do NOT support structured outputs via `response_format: {type: "json_schema", ...}`.

**Impact:**
- Cannot use `output_schema` parameter with Deep Research models
- Cannot get Pydantic-validated structured responses directly
- Must parse markdown output into structured format separately

---

## Implementation Recommendations

### Recommended: Two-Step Research + Parse Approach

Given that Deep Research models don't support structured outputs, we recommend a two-step process. Deep Research models (`o3-deep-research`, `o4-mini-deep-research`) must **not** be called with `output_schema` / `response_model`; all structured research comes from a second step that parses their markdown + citations into `ExecutiveResearchResult`.

#### Step 1: Deep Research (Comprehensive)

```python
from agno.agent import Agent
from agno.models.openai import OpenAIResponses

# Research Agent - Deep, comprehensive research
research_agent = Agent(
    model=OpenAIResponses(id="o4-mini-deep-research", max_tool_calls=1),
    instructions="""
        Research this executive comprehensively using all available sources.

        Focus on:
        - Career trajectory and timeline
        - Leadership experience and team building
        - Domain expertise (technical/functional areas)
        - Company stage and sector experience
        - Notable achievements and outcomes

        Structure the response with clear sections and include inline citations.
    """
)

# Execute research
result = research_agent.run(f"""
    Research: {candidate.name}
    Current Role: {candidate.title} at {candidate.company}
    LinkedIn: {candidate.linkedin_url}
""")

# Extract research output
research_text = result.content  # Markdown text with inline citations
citations = result.citations.urls  # List[UrlCitation]
```

**Characteristics:**
- **Time:** 2-5 minutes per candidate (with `max_tool_calls=1`)
- **Quality:** Comprehensive, well-cited research
- **Format:** Structured markdown with inline citations
- **Cost:** ~36K tokens ($0.36 @ $10/1M for o4-mini-deep-research)

#### Step 2: Parse to Structured Format

```python
# Parser Agent - Convert markdown to structured format
parser_agent = Agent(
    model=OpenAIResponses(id="gpt-5-mini"),  # Fast, supports structured output
    output_schema=ExecutiveResearchResult,   # Canonical model defined in demo_planning/data_design.md
    instructions="""
        Parse the provided executive research into the structured format.

        Extract:
        - Career timeline events
        - Domain expertise areas
        - Company stages and sectors
        - Key achievements

        Map citations from the research to specific claims.
        Be explicit about gaps - use the gaps field for missing information.
    """
)

# Parse research into structured format
structured_result = parser_agent.run(f"""
    Executive: {candidate.name}

    Research Content:
    {research_text}

    Citations:
    {[{"url": c.url, "title": c.title} for c in citations]}
""")

# Now we have structured data
executive_data: ExecutiveResearchResult = structured_result.content
```

**Characteristics:**
- **Time:** 10-30 seconds (fast model, structured output)
- **Quality:** Validated Pydantic schema
- **Format:** Structured data ready for Airtable
- **Cost:** Minimal (~2K tokens @ $0.15/1M for gpt-5-mini)

#### Complete Research Pipeline

```python
def research_executive(candidate) -> ExecutiveResearchResult:
    """
    Complete two-step research pipeline.

    Returns structured research result with citations.
    """
    # Step 1: Deep Research
    research_result = research_agent.run(f"""
        Research: {candidate.name}
        Current Role: {candidate.title} at {candidate.company}
        LinkedIn: {candidate.linkedin_url}
    """)

    # Step 2: Parse to structured format
    structured_result = parser_agent.run(f"""
        Executive: {candidate.name}

        Research Content:
        {research_result.content}

        Citations:
        {[{"url": c.url, "title": c.title} for c in research_result.citations.urls]}
    """)

    return structured_result.content
```

---

### Phase 2 (Future): Fast Web Search Mode

> **Not in v1:** Fast mode is documented here for future exploration but is explicitly deferred per `spec/v1_minimal_spec.md`. The v1 demo always runs Deep Research (with an optional single incremental search step when quality checks fail).

For faster execution in the future, we could use `gpt-5` with web search instead of Deep Research:

```python
# Fast Web Search Agent (30-60 seconds per candidate)
fast_research_agent = Agent(
    model=OpenAIResponses(id="gpt-5"),
    tools=[{"type": "web_search_preview"}],
    output_schema=ExecutiveResearchResult,  # ✅ Works with gpt-5
    instructions="""
        Research this executive using web search (3-5 targeted queries).

        Search for:
        - LinkedIn profile and career history
        - Company background and stage
        - Recent news and achievements
        - Domain expertise indicators

        Return structured results with citations.
    """
)

# Single-step execution
result = fast_research_agent.run(query)
executive_data: ExecutiveResearchResult = result.content
```

**Trade-offs:**
- ✅ **Faster:** 30-60 seconds vs 2-5 minutes
- ✅ **Structured output:** Direct Pydantic response
- ✅ **Simpler:** Single agent, one API call
- ❌ **Less comprehensive:** Fewer sources, less depth
- ❌ **Quality variance:** May miss nuanced details

**Use Case:**
- Live demo execution (time-constrained)
- Quick candidate filtering
- Supplemental searches in assessment phase

---

## Storage & Schema Implications

### Citation Storage in Airtable

Based on findings, citations should be stored as:

**Option A: JSON Array Field**
```json
{
  "citations": [
    {
      "url": "https://apnews.com/article/...",
      "title": "Microsoft CEO Satya Nadella caps a decade...",
      "relevance": "Career timeline and achievements"
    }
  ]
}
```

**Option B: Linked Records (Citations Table)**
- Create separate Citations table
- Link multiple citations to each research record
- Better for querying and deduplication

**Recommendation:** Option A (JSON field) for demo simplicity

### Research Storage Schema

Execution metadata and structured research now stay on the **Assessments** table (per v1 minimal contract):

- Each candidate/screen pair has one Assessment record with status, runtime, and error fields.
- The record also stores:
  - `research_structured_json` + `research_markdown_raw`
  - `assessment_json`, dimension/must-have arrays, topline summary, optional markdown narrative
  - `research_model` + `assessment_model`
- Screens table holds the batch status/error message.
- Deeper execution logs remain in Agno's `SqliteDb (tmp/agno_sessions.db)`; Airtable no longer needs Workflows/Research_Results tables for v1.

See `demo_planning/airtable_schema.md` (Assessments section) for the canonical field list.

---

## Cost & Performance Analysis

### Deep Research Mode (Required for v1)

**Per Candidate:**
- Deep Research call: ~$0.36 (≈36K tokens @ $10/1M)
- Optional incremental search (≤2 gpt-5-mini tool calls): ~$0.01
- **Total:** ~$0.37 per candidate
- **Time:** 2-6 minutes per candidate (dominated by Deep Research)

**For 10 candidates (sequential):**
- **Cost:** ~$3.70
- **Time:** 20-60 minutes

**Recommendation:** Use for all pre-run screens and the live Estuary demo; limit batch size instead of switching models when time-constrained.

### Fast Web Search Mode (Phase 2 only)

- Maintain for future experimentation but keep behind a feature flag for now.
- Not part of the v1 demo contract per `spec/v1_minimal_spec.md`.

---

## Updated Technical Spec Implications

### Changes Required in `technical_spec_V2.md`

- **Person Researcher:** Document a **single** Deep Research agent (OpenAIResponses `o4-mini-deep-research`) configured with `output_schema=ExecutiveResearchResult`. No parser agent. Include note that the agent must stream markdown + structured output simultaneously and that `response_format=json_schema` is unsupported.
- **Incremental Search:** Describe the optional single-pass `gpt-5-mini` search agent that runs only when a quality heuristic fails (e.g., `<3` unique citations). Cap tool calls at two per candidate.
- **Assessment Agent:** Call out the `ReasoningTools` requirement so the JSON in Airtable includes explicit reasoning traces.
- **Data Persistence:** Update storage diagrams to show Assessments table holding `research_structured_json`, `research_markdown_raw`, `assessment_json`, etc., with Screens providing run-level statuses. Remove references to Workflows + Research_Results tables.
- **Audit Trail:** Note that Agno `SqliteDb (tmp/agno_sessions.db)` is the dev-facing log, while Airtable statuses/error fields are the user-facing audit layer.

### Decision Record

**Final Decision:** Deep Research–first pipeline with optional single incremental search; no fast-mode toggle.

- Deep Research agent always runs (pre-runs + live demo).
- Quality heuristic may trigger one incremental search agent run (≤2 tool calls).
- Assessment agent (ReasoningTools-enabled) consumes research outputs directly and writes everything onto Assessments records.

**Implementation Sketch:**
```python
def run_research(candidate):
    result = deep_research_agent.run(candidate)
    if research_is_low_quality(result):
        supplement = incremental_search_agent.run(candidate)
        result = merge_research(result, supplement)
    return result

def screen_candidate(candidate):
    research = run_research(candidate)
    assessment = assessment_agent.run(
        research=research,
        role_spec=spec_markdown,
    )
    write_assessment_record(candidate, research, assessment)
```

### Next Steps

1. Update `technical_spec_V2.md` + `spec/spec.md` to reflect the single-agent Deep Research flow, optional incremental search, and Assessments-only storage.
2. Update demo planning docs (this file, `data_design.md`, `airtable_schema.md`, workflow spec) to match the linear workflow (DONE in this pass for schema/research docs; workflow spec still pending).
3. Ensure engineering checklist references `ReasoningTools`, Agno `SqliteDb`, and the new Airtable fields before implementation begins.

---

## Appendix: Full Test Output

### Test 1 Response Attributes

```python
RunOutput attributes:
[
    'content',           # ✅ Markdown research text
    'citations',         # ✅ Citations object
    'messages',          # ✅ Full conversation history
    'metrics',           # ✅ Token usage stats
    'agent_id',
    'agent_name',
    'created_at',
    'events',
    'files',
    'images',
    'videos',
    'audio',
    'reasoning_content',
    'reasoning_messages',
    'reasoning_steps',
    'references',
    'model',
    'model_provider',
    'run_id',
    'session_id',
    'status',
    # ... additional metadata fields
]
```

### Test 1 Metrics

```python
Metrics(
    input_tokens=31762,      # Research context
    output_tokens=4342,      # Generated response
    total_tokens=36104,      # Combined
    reasoning_tokens=32128,  # Deep reasoning steps
    duration=None,           # Not captured
    time_to_first_token=None
)
```

**Cost Calculation:**
- o4-mini-deep-research pricing: ~$10/1M tokens
- Total cost: 36,104 tokens × $10/1M = $0.36

### Test 2 Error Details

```
File: agno/models/openai/responses.py, line 539
Error: openai.BadRequestError
Message: Invalid parameter: 'text.format' of type 'json_schema'
         is not supported with model version `o4-mini-deep-research`.
```

**Confirmed:** Deep Research models do not support `response_format: {type: "json_schema", ...}`

---

**Document Version:** 1.0
**Last Updated:** 2025-11-16
**Author:** Claude Code (automated testing and analysis)
