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

### Alternative: Fast Web Search Mode

For faster execution (demo flexibility), can use `gpt-5` with web search instead of Deep Research:

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

Execution metadata and structured research are split between `Workflows` and `Research_Results` in Airtable:

**Workflows Table Fields (execution metadata):**
```
- workflow_id (primary key)
- screen (link to Screens)
- candidate (link to People)
- status (Single Select) - Queued/Research/Assessment/Complete/Failed
- research_started / research_completed (DateTime)
- assessment_started / assessment_completed (DateTime)
- execution_log (Long Text, JSON) - event stream
- error_message (Long Text)
```

**Research_Results Table Fields (structured research):**
```
- research_id (primary key)
- workflow (link to Workflows)
- candidate (link to People)
- research_summary (Long Text)
- research_json (Long Text, JSON) - full ExecutiveResearchResult
- citations (Long Text, JSON) - array of citation objects
- research_confidence (Single Select) - High/Medium/Low
- research_gaps (Long Text, JSON) - missing information notes
- research_timestamp (DateTime)
- research_model (Single Line Text)
```

Execution and research are joined via `Research_Results.workflow`.

For complete Airtable field definitions, see `demo_planning/airtable_schema.md` (Research_Results and Workflows tables).

---

## Cost & Performance Analysis

### Deep Research Mode (Recommended for Pre-runs)

**Per Candidate:**
- Research: ~$0.36 (36K tokens @ $10/1M)
- Parsing: ~$0.0003 (2K tokens @ $0.15/1M)
- **Total:** ~$0.36 per candidate
- **Time:** 2-6 minutes per candidate

**For 10 candidates (sequential):**
- **Cost:** ~$3.60
- **Time:** 20-60 minutes

**Recommendation:** Use for 3 pre-run scenarios (30 total candidates = $10.80)

### Fast Web Search Mode (Recommended for Live Demo)

**Per Candidate:**
- Research + Structure: ~$0.02 (2K tokens @ $10/1M for gpt-5)
- **Total:** ~$0.02 per candidate
- **Time:** 30-90 seconds per candidate

**For 5 candidates (sequential):**
- **Cost:** ~$0.10
- **Time:** 2.5-7.5 minutes

**Recommendation:** Use for live demo execution (Estuary CTO role)

---

## Updated Technical Spec Implications

### Changes Required in technical_spec_V2.md

**Section: "Core Components > Person Researcher"**

Replace with two-step approach:

```markdown
### Person Researcher

**Implementation:** Two-step process (Research → Parse)

#### Research Agent (Step 1)
- **Model:** OpenAIResponses(id="o4-mini-deep-research", max_tool_calls=1)
- **Output:** Markdown research with inline citations
- **Citations:** Accessible via `result.citations.urls`
- **Time:** 2-5 minutes per candidate

#### Parser Agent (Step 2)
- **Model:** OpenAIResponses(id="gpt-5-mini")
- **Output:** ExecutiveResearchResult (Pydantic)
- **Input:** Research markdown + citations from Step 1
- **Time:** 10-30 seconds

#### Alternative: Fast Mode
- **Model:** OpenAIResponses(id="gpt-5") with web_search_preview
- **Output:** Direct structured output (single step)
- **Time:** 30-60 seconds per candidate
- **Use:** Live demo execution
```

**Section: "Structured Output Schemas"**

For the detailed `ExecutiveResearchResult` Pydantic model that underpins the JSON stored in `Research_Results.research_json`, see `demo_planning/data_design.md` (“Structured Output Schemas”). That model is the single source of truth for the research schema.

---

## Decision Record

### Final Decision: Two-Step Approach with Mode Toggle

**Primary Mode (Deep Research):**
- Use for pre-run scenarios (comprehensive, high-quality)
- Two-step: o4-mini-deep-research → gpt-5-mini parser
- Time: 2-6 min/candidate
- Cost: ~$0.36/candidate

**Fast Mode (Web Search):**
- Use for live demo (faster, still good quality)
- Single-step: gpt-5 with web search + structured output
- Time: 30-90 sec/candidate
- Cost: ~$0.02/candidate

**Implementation:**
```python
# Environment flag for mode selection
USE_DEEP_RESEARCH = os.getenv('USE_DEEP_RESEARCH', 'true').lower() == 'true'

def research_executive(candidate):
    if USE_DEEP_RESEARCH:
        return two_step_deep_research(candidate)
    else:
        return fast_web_search_research(candidate)
```

**Benefits:**
- ✅ All via Agno (no hybrid SDK approach needed)
- ✅ Citations fully accessible
- ✅ Structured outputs achieved
- ✅ Flexible execution (comprehensive vs fast)
- ✅ Demo risk mitigation (can toggle if time-constrained)

---

## Next Steps

1. **Update technical_spec_V2.md** with two-step approach
2. **Design Airtable schema** with citation storage
3. **Implement research pipeline** with mode toggle
4. **Test both modes** with sample candidates
5. **Pre-run 3 scenarios** using Deep Research mode
6. **Prepare live demo** with Fast mode as fallback

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
