# OpenAI Reference Materials

This directory contains curated OpenAI documentation and examples that complement the Agno framework for building the Talent Signal Agent.

## Structure

```
openai_reference/
├── deep_research_api/        # Deep Research API docs and examples
│   ├── OAI_deepresearchapi.md
│   ├── OAI_mcp_deepresearch.md
│   ├── oai_introduction_to_deep_research_api.ipynb
│   ├── oaisdk_introduction_to_deep_research_api_agents.ipynb
│   └── oaisdk_agents-deep-research-main/
│
├── research_patterns/        # Research workflow patterns
│   └── oaisdk_research_bot/
│
└── guides/                   # General guides and documentation
    ├── A Deep Dive Into The OpenAI Agents SDK.md
    └── gpt-5-1_prompting_guide.ipynb
```

## How to Use

### 1. Deep Research API Integration

Use patterns from `deep_research_api/` when calling OpenAI's Deep Research API from Agno agents:

```python
from openai import OpenAI
from agno.agent import Agent

client = OpenAI()

def deep_research_candidate(candidate_name: str) -> dict:
    """Deep dive on finalist candidates"""
    response = client.responses.create(
        model="o3-deep-research",
        input=f"Comprehensive evaluation of {candidate_name}...",
        background=True,
        tools=[{"type": "web_search_preview"}]
    )
    return response.output_text
```

### 2. Research Workflow Patterns

Reference `research_patterns/oaisdk_research_bot/` for:

- Breaking research into planning → execution → synthesis
- Prompt engineering for high-quality research outputs
- Structured output schemas (Pydantic models)

### 3. GPT-5 Prompting

See `guides/gpt-5-1_prompting_guide.ipynb` for:

- Best practices with GPT-5
- Reasoning and structured outputs
- Cost optimization strategies

## Archived Materials

Less relevant materials have been moved to `_oai_archive/` and can be deleted if not needed.
