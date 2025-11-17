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
