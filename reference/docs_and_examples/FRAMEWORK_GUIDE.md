# Framework Implementation Guide

## Decision: Agno Framework ✅

After comprehensive evaluation, **Agno** was selected for the Talent Signal Agent implementation.

### Why Agno?

1. **Domain-Specific Examples** - Candilyzer and Employee Recruiter save 10-15 hours
2. **Research Flexibility** - Exa + Deep Research API + other tools
3. **Fast Setup** - 1-2 hours to working prototype
4. **Modern Architecture** - Multi-agent teams, knowledge bases, streaming
5. **Production Ready** - Memory, persistence, reasoning trails built-in

---

## Primary Resources

### 1. Agno Framework (Main Implementation)

**Location:** `agno/`

**Key Examples:**
- `candidate_analyser/main.py` ⭐⭐⭐ - Multi-candidate evaluation with scoring
- `cookbook/examples/workflows/employee_recruiter_async_stream.py` ⭐⭐ - Full hiring workflow
- `agno_deepresearch.md` ⭐⭐ - Research patterns with citations
- `agno_recruiter.md` ⭐ - Recruitment workflow overview

**Start Here:**
```python
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.exa import ExaTools

agent = Agent(
    name="Talent Signal Agent",
    model=OpenAIChat(id="gpt-4o"),
    tools=[ExaTools(research=True)],
    instructions="Match candidates to roles with reasoning"
)
```

---

### 2. OpenAI Reference (Supplementary)

**Location:** `openai_reference/`

**Use For:**
1. **Deep Research API Integration** (`deep_research_api/`)
   - Call from Agno agents for comprehensive candidate research
   - Background processing patterns
   - Citation/source tracking

2. **Prompt Engineering** (`research_patterns/oaisdk_research_bot/`)
   - Research workflow patterns
   - Structured output schemas
   - Quality control techniques

3. **GPT-5 Best Practices** (`guides/gpt-5-1_prompting_guide.ipynb`)
   - Reasoning capabilities
   - Cost optimization
   - Structured outputs

**Example Integration:**
```python
from openai import OpenAI
from agno.agent import Agent

client = OpenAI()

def deep_research_finalist(candidate: str) -> dict:
    """Use Deep Research for top 3 candidates"""
    response = client.responses.create(
        model="o3-deep-research",
        input=f"Comprehensive evaluation of {candidate}...",
        background=True,
        tools=[{"type": "web_search_preview"}]
    )
    return response.output_text

# Use in Agno agent
agent = Agent(
    tools=[deep_research_finalist],
    ...
)
```

---

## Implementation Timeline (48 Hours)

### Day 1 (24 hours)
- **Hours 1-3:** Setup + study Candilyzer example
- **Hours 4-12:** Build core matching engine (3-agent team)
- **Hours 13-18:** Data integration (CSV + vector store)
- **Hours 19-24:** Testing with mock data

### Day 2 (24 hours)
- **Hours 1-4:** Flask webhook + Airtable integration
- **Hours 5-8:** Add Deep Research for finalists
- **Hours 9-16:** Refinement (prompts, scoring, reasoning)
- **Hours 17-24:** Documentation + demo prep

---

## Key Files Reference

### Agno Examples to Adapt
```
candidate_analyser/main.py
├── Multi-candidate loop
├── GitHub/LinkedIn integration  
├── Scoring (0-100)
└── Reasoning for decisions

employee_recruiter_async_stream.py
├── Resume screening
├── Async/streaming execution
├── Structured outputs (Pydantic)
└── Email integration patterns
```

### OpenAI Patterns to Reference
```
oaisdk_research_bot/
├── Planner → Searcher → Writer
├── Parallel search execution
├── Research quality control
└── Structured schemas

deep_research_api/
├── o3-deep-research API calls
├── Background processing
├── Citation tracking
└── MCP integration
```

---

## Quick Start Commands

```bash
# 1. Install dependencies
pip install agno openai pandas pyairtable flask

# 2. Set API keys
export OPENAI_API_KEY='your_key'
export EXA_API_KEY='your_key'

# 3. Test basic agent
python -c "
from agno.agent import Agent
from agno.models.openai import OpenAIChat

agent = Agent(
    model=OpenAIChat(id='gpt-4o'),
    instructions='You are a talent matcher'
)

result = agent.run('Hello, test')
print(result.content)
"

# 4. Start with Candilyzer
# Copy and adapt: agno/candidate_analyser/main.py
```

---

## Architecture Decision Record

**Date:** 2025-11-16

**Decision:** Use Agno framework with OpenAI Deep Research API for supplementary research

**Rationale:**
- Domain examples (Candilyzer) save 10-15 hours vs. building from scratch
- Agno provides research flexibility (Exa + Deep Research + others)
- 48-hour timeline favors rapid prototyping over single-vendor simplicity
- Can still leverage OpenAI Deep Research API for comprehensive finalist evaluation
- Best of both worlds: Agno's framework + OpenAI's research capabilities

**Trade-offs Accepted:**
- Multiple vendor dependencies (Agno + Exa + OpenAI) vs. single vendor
- 45 min Exa setup vs. integrated WebSearchTool
- Smaller community vs. OpenAI/LangChain ecosystems

**Alternatives Considered:**
- OpenAI SDK: Better single-vendor integration, but lacks domain examples
- LangGraph: Excellent for complex state management, but longer learning curve

**Status:** Locked in ✅

---

## Support Resources

**Agno Documentation:**
- GitHub: github.com/agno-oss/agno
- Examples: 140+ in cookbook/
- Community: Discord, GitHub Discussions

**OpenAI Deep Research:**
- API Docs: `openai_reference/deep_research_api/OAI_deepresearchapi.md`
- Examples: `openai_reference/deep_research_api/oaisdk_agents-deep-research-main/`

**Implementation Help:**
- Start with: `agno/candidate_analyser/main.py`
- Reference: This guide + `openai_reference/README.md`

---

## Alternative Architectures (Reference Only)

### DeepResearchAgent

**Location:** `alternative_architectures/DeepResearchAgent-main/`

A hierarchical multi-agent system with a top-level planning agent coordinating specialized lower-level agents.

**When to reference:**
- Need hierarchical task planning patterns
- Want MCP integration examples  
- Considering browser automation for LinkedIn scraping
- Exploring alternative multi-agent coordination approaches

**Note:** This is for reference only. Stick with Agno for your implementation - it's the right choice for the 48-hour timeline and talent matching use case.

See `alternative_architectures/README.md` for detailed comparison.

