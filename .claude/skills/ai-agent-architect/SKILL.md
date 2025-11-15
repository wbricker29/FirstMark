---
name: ai-agent-architect
description: Framework-agnostic methodology for designing and building efficient Python LLM applications and AI agents. Emphasizes KISS and YAGNI principles, lean development cycles, and iterative complexity. This skill should be used when designing LLM systems, building AI agents, architecting RAG pipelines, or working on Python-based AI projects. Provides decision frameworks, design patterns (simple to complex), and development processes that prioritize working prototypes over premature optimization.
---

# AI Agent Architect

## Overview

This skill provides a principled, framework-agnostic approach to designing and building Python LLM applications and AI agents. Instead of prescribing specific frameworks or tools, it teaches design principles, decision-making frameworks, and iterative development patterns that lead to efficient, maintainable systems.

**Core Philosophy:** Start simple, validate, then expand. Build the minimal viable solution first, prove it works, then add complexity only when needed.

## Core Principles

### 1. KISS (Keep It Simple, Stupid)
**Simple solutions first, always.**

- Start with the most straightforward approach that could work
- Use plain Python and OpenAI/Anthropic APIs before adding frameworks
- Add abstractions only when you're repeating yourself (DRY principle triggers complexity)
- Question every dependency: "Do I actually need this?"

**Example:**
```python
# KISS: Start here
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}]
)

# NOT THIS (premature framework adoption)
agent = LangChainAgent(
    llm=ChatOpenAI(),
    tools=[Tool1(), Tool2()],
    memory=ConversationMemory(),
    callbacks=[CustomCallback()]
)
```

### 2. YAGNI (You Aren't Gonna Need It)
**Don't build for imaginary future requirements.**

- Build only what you need right now
- Resist the urge to make it "production-ready" on day one
- No complex pipelines until simple scripts prove the concept
- No vector databases until you've proven retrieval is actually needed

**Decision Test:** "If I delete this, would the core functionality break today?" If no, delete it.

### 3. Lean Development Cycles
**Build → Validate → Expand (repeat)**

1. **Build:** Minimal implementation that demonstrates core value
2. **Validate:** Test with real data, measure actual performance
3. **Expand:** Add complexity only where validation showed it's needed

**Anti-pattern:** Building the entire architecture before running a single example.

### 4. Iterative Complexity
**Complexity ladder: climb only as high as you must.**

```
Simple Prompt → Few-Shot Prompt → Prompt Chain → Tool Use → Agent → Multi-Agent
```

Start at the bottom. Move up only when the current level fails to meet requirements.

## Development Workflow

### Phase 1: Define & Validate Core Value (30% of effort)

**Goal:** Prove the concept works with the simplest possible implementation.

**Steps:**

1. **Define Success Criteria**
   - What does "working" mean? (Be specific and measurable)
   - What's the minimum output quality to be useful?
   - What's the maximum acceptable latency/cost?

2. **Build Minimal Prototype**
   - Single Python script (< 100 lines)
   - Hardcoded examples or minimal test data
   - Direct API calls, no frameworks
   - Print results to console

3. **Validate Value**
   - Does it produce useful output?
   - Is the approach fundamentally sound?
   - What's the actual cost/latency?

**Exit Criteria:** You have a working script that demonstrates the core value proposition.

**Example (Talent Matching):**
```python
# minimal_matcher.py - ~50 lines
import anthropic

client = anthropic.Anthropic()

# Hardcoded test data
role = {"title": "CTO", "requirements": "15+ years, Python, ML"}
candidate = {"name": "Alice", "bio": "VP Eng at Series B, 18 years Python/ML"}

prompt = f"""
Role: {role}
Candidate: {candidate}

Rate match quality (0-100) and explain why.
"""

response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[{"role": "user", "content": prompt}]
)

print(response.content[0].text)
```

**Validation:** Run with 5-10 examples. Does it work? Great, move to Phase 2.

### Phase 2: Scale to Real Data (30% of effort)

**Goal:** Handle actual data sources and volumes.

**Steps:**

1. **Data Integration (Simple First)**
   - CSV files → pandas DataFrames
   - JSON files → Python dicts
   - Plain text → string processing
   - No databases yet, just files

2. **Batch Processing**
   - Loop over real data
   - Collect results
   - Basic error handling (try/except)

3. **Measure Performance**
   - Count API calls and costs
   - Measure latency (time.time())
   - Identify bottlenecks (is it data loading? API calls? parsing?)

**Exit Criteria:** The script processes your full dataset and produces results.

**Example (Scaling Matcher):**
```python
# matcher_v2.py - ~150 lines
import anthropic
import pandas as pd
import json
from pathlib import Path

def load_data():
    """Load from CSVs and JSON - simple file I/O"""
    roles = pd.read_csv("data/roles.csv")
    candidates = pd.read_csv("data/candidates.csv")
    bios = json.loads(Path("data/bios.json").read_text())
    return roles, candidates, bios

def match_candidate_to_role(role, candidate, bio):
    """Single match - same logic as Phase 1"""
    # ... (previous prompt logic)
    return {"score": score, "reasoning": reasoning}

def main():
    roles, candidates, bios = load_data()
    results = []

    for _, role in roles.iterrows():
        for _, candidate in candidates.iterrows():
            bio = bios.get(candidate["id"], "")
            result = match_candidate_to_role(role, candidate, bio)
            results.append(result)

    # Save results
    pd.DataFrame(results).to_csv("matches.csv", index=False)

if __name__ == "__main__":
    main()
```

### Phase 3: Optimize Based on Evidence (30% of effort)

**Goal:** Address bottlenecks identified in Phase 2.

**Only add complexity for proven problems:**

**Problem: Too many API calls (high cost)**
→ Solution: Add retrieval/filtering before LLM (now you need vector search)

**Problem: Responses inconsistent**
→ Solution: Add structured output, few-shot examples, or fine-tuning

**Problem: Need multi-step reasoning**
→ Solution: Upgrade from single prompt to agentic pattern

**Problem: Slow sequential processing**
→ Solution: Add async/parallel execution

**Key:** Don't solve problems you don't have. Measure first, optimize second.

### Phase 4: Polish & Production-ize (10% of effort)

**Goal:** Make it maintainable and robust.

**Only after core functionality is validated:**

- Proper error handling and logging
- Configuration management (env vars, config files)
- Documentation (README, docstrings)
- Tests (at least smoke tests)
- Deployment considerations (if needed)

**Anti-pattern:** Starting with Phase 4 before Phase 1 works.

## LLM & Agent Design Patterns

### Complexity Ladder (climb only as needed)

#### Level 0: Single Prompt (Start Here)
**When to use:** Most tasks, most of the time.

**Pattern:**
```python
response = llm.generate(f"Task: {task}\nContext: {context}\nOutput:")
```

**Strengths:** Fast, cheap, simple, easy to debug.

**When to upgrade:** When single prompt consistently fails to produce good results.

---

#### Level 1: Few-Shot Prompting
**When to use:** Single prompt works but output format/style is inconsistent.

**Pattern:**
```python
examples = """
Example 1: {input1} → {output1}
Example 2: {input2} → {output2}
Example 3: {input3} → {output3}
"""

prompt = f"{examples}\n\nNow solve: {new_input}"
```

**Strengths:** Improves consistency without complexity.

**When to upgrade:** When examples don't help or task requires multiple steps.

---

#### Level 2: Prompt Chains
**When to use:** Task naturally decomposes into sequential steps.

**Pattern:**
```python
# Step 1: Extract requirements
requirements = llm.generate(f"Extract requirements from: {job_description}")

# Step 2: Score match
score = llm.generate(f"Score match:\nRequirements: {requirements}\nCandidate: {candidate}")

# Step 3: Generate explanation
explanation = llm.generate(f"Explain score {score} for: {candidate}")
```

**Strengths:** Each step is simple, debuggable, and can be optimized independently.

**When to upgrade:** When the chain needs dynamic branching or decision-making.

---

#### Level 3: Retrieval-Augmented Generation (RAG)
**When to use:** Need to search/filter large datasets before LLM processing.

**Simple RAG (no vector DB):**
```python
def simple_rag(query, documents):
    # Filter by keyword matching
    relevant = [doc for doc in documents if keyword_match(query, doc)]

    # Rank by simple heuristic (e.g., keyword count)
    ranked = sorted(relevant, key=lambda d: relevance_score(query, d), reverse=True)[:5]

    # Pass to LLM
    context = "\n\n".join(ranked)
    return llm.generate(f"Context: {context}\n\nQuestion: {query}")
```

**When to add vector search:** When keyword matching fails to find relevant docs.

**Vector RAG:**
```python
from sentence_transformers import SentenceTransformer
import numpy as np

# One-time: Create embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')
doc_embeddings = model.encode(documents)

# Query-time: Find similar docs
query_embedding = model.encode([query])[0]
similarities = np.dot(doc_embeddings, query_embedding)
top_k_indices = np.argsort(similarities)[-5:][::-1]
relevant_docs = [documents[i] for i in top_k_indices]

# Pass to LLM
context = "\n\n".join(relevant_docs)
return llm.generate(f"Context: {context}\n\nQuestion: {query}")
```

**When to upgrade:** When you need dynamic decision-making about what to retrieve.

---

#### Level 4: Tool-Using Agent (ReAct Pattern)
**When to use:** LLM needs to decide which tools to use and when.

**Simple ReAct:**
```python
def react_agent(task, tools, max_iterations=5):
    """
    ReAct: Reason + Act in a loop

    Tools: {
        "search_candidates": function,
        "get_candidate_bio": function,
        "score_match": function
    }
    """
    context = f"Task: {task}\nAvailable tools: {list(tools.keys())}"

    for i in range(max_iterations):
        # Thought: Let LLM decide what to do
        thought = llm.generate(f"{context}\n\nWhat should I do next? (Think step-by-step)")

        # Action: Let LLM choose a tool
        action = llm.generate(f"{thought}\n\nWhich tool should I use? Output: tool_name(args)")

        # Execute tool
        tool_name, args = parse_action(action)
        observation = tools[tool_name](**args)

        # Update context
        context += f"\n\nThought: {thought}\nAction: {action}\nObservation: {observation}"

        # Check if done
        done = llm.generate(f"{context}\n\nAm I done? (yes/no)")
        if "yes" in done.lower():
            break

    # Final answer
    return llm.generate(f"{context}\n\nProvide final answer:")
```

**When to upgrade:** When single agent can't handle task complexity.

---

#### Level 5: Multi-Agent Systems
**When to use:** Task requires specialized sub-agents with different roles.

**Only use when Level 4 proves insufficient.** Multi-agent systems are complex and hard to debug.

**Simple Multi-Agent:**
```python
def multi_agent_system(task):
    # Agent 1: Researcher
    research = researcher_agent.run(f"Research candidates for: {task}")

    # Agent 2: Analyzer
    analysis = analyzer_agent.run(f"Analyze these candidates: {research}")

    # Agent 3: Ranker
    ranking = ranker_agent.run(f"Rank candidates: {analysis}")

    return ranking
```

**When to upgrade:** Rarely. Multi-agent is often over-engineering.

## Decision Frameworks

### Framework Selection Decision Tree

```
START: Need to build an LLM application

Q: Have you proven the concept with a single script?
   NO → Go write a 50-line script first
   YES ↓

Q: Is your current code becoming unmaintainable (>500 lines, lots of duplication)?
   NO → Keep using plain Python + OpenAI/Anthropic SDK
   YES ↓

Q: Do you need RAG/vector search?
   YES → Consider LlamaIndex (RAG-focused)
   NO ↓

Q: Do you need complex multi-step agents with tools?
   YES → Consider LangChain or CrewAI
   NO ↓

Q: Do you have very specific orchestration needs?
   YES → Build custom with plain Python
   NO → You probably don't need a framework yet
```

**Key Insight:** Most projects never need frameworks. Start without them.

### RAG Strategy Decision Tree

```
START: Need to retrieve information for LLM

Q: How many documents?
   < 10 → Just pass all as context (no RAG needed)
   < 1000 → Keyword/metadata filtering + simple ranking
   > 1000 ↓

Q: Can you filter by metadata (dates, categories, tags)?
   YES → Start with metadata filtering + keyword search
   NO ↓

Q: Are keyword matches finding the right docs?
   YES → Stick with keyword-based retrieval
   NO → Now add vector embeddings

Q: Which embedding model?
   Start: sentence-transformers/all-MiniLM-L6-v2 (fast, free, local)
   If insufficient: OpenAI text-embedding-3-small
   If still insufficient: OpenAI text-embedding-3-large

Q: Need a vector database?
   < 100K docs → Use FAISS (local, simple)
   > 100K docs → Consider Pinecone/Weaviate (if you must)
```

### Prompt vs Agent Decision Guide

**Use a Prompt When:**
- Task is well-defined and consistent
- Single pass can produce good results
- You can provide all necessary context upfront
- Deterministic behavior is important

**Use an Agent When:**
- Task requires dynamic decision-making
- Need to use external tools/APIs
- Multi-step reasoning with variable paths
- Context must be gathered iteratively

**Example:**
- Prompt: "Summarize this document" ✓
- Agent: "Research a topic across multiple sources and write a report" ✓

## Implementation Guidance

### Project Structure (Keep Simple)

```
project/
├── main.py              # Entry point, < 100 lines
├── data/                # Input data (CSVs, JSONs)
├── prompts/             # Prompt templates (optional)
├── utils.py             # Helper functions (only if reused 3+ times)
├── requirements.txt     # Minimal dependencies
└── README.md            # What it does, how to run
```

**Don't create:**
- `src/` directory (until you have 5+ modules)
- `config/` directory (until you have 5+ config files)
- `tests/` directory (until core logic is stable)
- Abstract base classes (until you have 3+ similar classes)

### Dependency Management

**Start with:**
```txt
# requirements.txt (minimal)
openai>=1.0.0           # or anthropic
python-dotenv>=1.0.0    # for API keys
```

**Add only when needed:**
```txt
pandas>=2.0.0           # when working with tabular data
sentence-transformers   # when adding vector search
faiss-cpu              # when vector search is proven necessary
```

**Avoid until proven necessary:**
- langchain, llamaindex (heavy frameworks)
- chromadb, pinecone (vector DBs)
- pydantic (unless validation is critical)
- Any framework with > 10 dependencies

### Code Structure Principles

**1. Flat is better than nested**
```python
# Good: Flat structure
def main():
    data = load_data()
    results = process_data(data)
    save_results(results)

# Avoid: Premature OOP
class DataLoader:
    class CSVLoader:
        class RoleLoader:  # Stop!
```

**2. Functions over classes (until you need state)**
```python
# Good: Simple functions
def match_candidate(role, candidate):
    prompt = create_prompt(role, candidate)
    return llm.generate(prompt)

# Avoid (unless you need to maintain state)
class CandidateMatcher:
    def __init__(self, llm, config):
        self.llm = llm
        self.config = config
    # ... (only if you're reusing this object many times)
```

**3. Inline first, extract later**
```python
# First iteration: Inline everything
def process():
    prompt = f"Analyze: {data}"  # Inline prompt
    result = llm.generate(prompt)
    return result

# After 3rd time you write similar prompt → extract
def create_analysis_prompt(data):
    return f"Analyze: {data}"
```

### Error Handling (Progressive)

**Phase 1: Let it crash (learn failure modes)**
```python
result = llm.generate(prompt)  # No try/except yet
```

**Phase 2: Catch and log (when errors are understood)**
```python
try:
    result = llm.generate(prompt)
except Exception as e:
    print(f"Error: {e}")  # Simple logging
    result = None
```

**Phase 3: Graceful handling (when in production)**
```python
import logging

try:
    result = llm.generate(prompt)
except RateLimitError:
    time.sleep(60)  # Retry after backoff
    result = llm.generate(prompt)
except Exception as e:
    logging.error(f"Failed: {e}", exc_info=True)
    result = {"error": str(e)}
```

**Don't start with Phase 3.** Let it crash first to understand what actually fails.

## Common Patterns

### Pattern: Structured Output

**Problem:** LLM returns inconsistent formats.

**Simple Solution: Use prompt instructions**
```python
prompt = f"""
Analyze this candidate for the role.

Output EXACTLY in this format:
Score: [0-100]
Reasoning: [explanation]
Decision: [STRONG_MATCH | WEAK_MATCH | NO_MATCH]

Candidate: {candidate}
Role: {role}
"""
```

**If that fails: Use JSON mode**
```python
response = client.chat.completions.create(
    model="gpt-4-turbo",
    response_format={"type": "json_object"},
    messages=[{
        "role": "user",
        "content": f"Return JSON with keys: score, reasoning, decision\n\n{prompt}"
    }]
)
result = json.loads(response.choices[0].message.content)
```

**Last resort: Pydantic validation**
```python
from pydantic import BaseModel

class MatchResult(BaseModel):
    score: int
    reasoning: str
    decision: str

# Only add this if JSON mode still produces invalid schemas
```

### Pattern: Batch Processing with Progress

**Simple batch processing:**
```python
from tqdm import tqdm  # pip install tqdm

results = []
for item in tqdm(data, desc="Processing"):
    result = process_item(item)
    results.append(result)
```

**With cost tracking:**
```python
total_cost = 0
for item in tqdm(data):
    result, cost = process_item(item)
    total_cost += cost
    results.append(result)

print(f"Total cost: ${total_cost:.2f}")
```

### Pattern: Caching (for development)

**Problem:** Re-running experiments is expensive.

**Simple file-based cache:**
```python
import json
from pathlib import Path

def cached_llm_call(prompt, cache_file="cache.json"):
    cache = json.loads(Path(cache_file).read_text()) if Path(cache_file).exists() else {}

    if prompt in cache:
        return cache[prompt]

    result = llm.generate(prompt)
    cache[prompt] = result
    Path(cache_file).write_text(json.dumps(cache, indent=2))
    return result
```

**Use during development, remove in production.**

## Anti-Patterns to Avoid

### ❌ Premature Abstraction
```python
# Don't do this first
class AbstractLLMProvider:
    @abstractmethod
    def generate(self): pass

class OpenAIProvider(AbstractLLMProvider): ...
class AnthropicProvider(AbstractLLMProvider): ...
```

**Do this instead:**
```python
# Start here
def generate(prompt):
    return client.messages.create(...)

# Switch providers later if needed (takes 5 minutes)
```

### ❌ Framework-First Thinking
```python
# Don't start here
from langchain.agents import create_react_agent
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory

# Start here instead
def simple_agent(task):
    thought = llm.generate(f"Think about: {task}")
    action = llm.generate(f"Based on '{thought}', what should I do?")
    return action
```

### ❌ Premature Optimization
```python
# Don't do this on day 1
async def parallel_process(items):
    tasks = [asyncio.create_task(process(item)) for item in items]
    return await asyncio.gather(*tasks)

# Do this first
for item in items:
    process(item)

# Add async only after profiling shows it's the bottleneck
```

### ❌ Over-Engineering Data Pipelines
```python
# Don't build this before proving the concept
class DataPipeline:
    def __init__(self):
        self.extractors = []
        self.transformers = []
        self.loaders = []
    # ... 200 lines of abstraction

# Do this first
df = pd.read_csv("data.csv")
```

## When to Graduate to Complexity

**Move from script → package when:**
- Single file > 500 lines
- 3+ modules are emerging naturally
- External users need to install it

**Add a framework when:**
- You've written the same agent logic 3+ times
- Custom orchestration code > 200 lines
- You need features the framework provides that would take weeks to build

**Add a vector database when:**
- FAISS file size > 10GB
- Query latency > 5 seconds
- Need distributed search

**Add tests when:**
- Core logic is stable and won't change daily
- You're refactoring and need confidence
- Others are contributing code

**Add CI/CD when:**
- You're deploying regularly
- Multiple contributors need standardization
- Bugs are reaching production

## Resources

### scripts/
**`setup_minimal_env.py`** - Sets up a minimal Python environment with core dependencies only.

**`benchmark_llm_providers.py`** - Simple benchmarking script to compare cost/latency across providers.

### references/
**`design_patterns_deep_dive.md`** - Detailed explanations of ReAct, Plan-and-Execute, Reflexion patterns with trade-offs.

**`prompt_engineering_guide.md`** - Techniques for effective prompting: few-shot, chain-of-thought, structured output.

**`evaluation_strategies.md`** - How to measure LLM application quality: accuracy, relevance, cost, latency.

### assets/
**`minimal_project_template/`** - Bare-bones Python project structure (main.py, requirements.txt, README.md).

**`prompt_templates/`** - Reusable prompt structures for common tasks (classification, extraction, reasoning).

---

**Remember:** The best architecture is the simplest one that works. Start simple, measure, then optimize.
