# Two-Skill Approach: Design & Implementation Plan
## FirstMark Case Study Skill Ecosystem

**Created:** 2025-11-14
**Purpose:** Design document for building reusable AI skills to accelerate FirstMark case study completion while creating long-term value

---

## Executive Summary

### The Approach
Build **two complementary skills** that work together to accelerate the FirstMark Talent Signal Agent case study while maximizing long-term reusability:

1. **`ai-agent-architect`** - Reusable AI agent design expertise (90% long-term value)
2. **`firstmark-case-context`** - Case-specific context and requirements (10% long-term value)

### Why This Design?
- **Efficient:** 2 skills vs 5 = faster to build, easier to maintain
- **Reusable:** The ai-agent-architect skill is valuable beyond this case (useful for the actual role)
- **Practical:** Provides both deep technical guidance and specific case context
- **Balanced:** Frameworks + specifics without being overly prescriptive

---

## Architecture Overview

### Skill Interaction Model

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INVOKES SKILLS                       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ├─────────────────┬──────────────┤
                              ▼                 ▼              ▼
                    ┌──────────────────┐ ┌─────────────┐ ┌────────┐
                    │ ai-agent-architect│ │  firstmark- │ │ Skills │
                    │  (Technical Core) │ │case-context │ │Work    │
                    │                   │ │ (Case Spec) │ │Together│
                    └──────────────────┘ └─────────────┘ └────────┘
                              │                 │              │
                    ┌─────────┴─────────────────┴──────────────┘
                    │     Combined Context & Guidance
                    ▼
        ┌──────────────────────────────────────┐
        │  DELIVERABLES GENERATION             │
        │  • Architecture design               │
        │  • Python prototype                  │
        │  • Technical writeup                 │
        │  • Documentation                     │
        └──────────────────────────────────────┘
```

### Division of Responsibilities

| Aspect | ai-agent-architect | firstmark-case-context |
|--------|-------------------|------------------------|
| **Scope** | Any AI agent project | This specific case only |
| **Longevity** | Permanent (keep forever) | Temporary (delete after case) |
| **Content Type** | Patterns, frameworks, principles | Requirements, context, constraints |
| **Reusability** | Very High | None |
| **Size** | Large (~3-5k words + resources) | Small (~1k words + data) |
| **Trigger** | Auto (keywords) | Explicit only |

---

## Skill 1: `ai-agent-architect`

### Purpose
Expert system for designing and building production-quality LLM agent applications. Provides architectural patterns, implementation strategies, and best practices for agentic AI systems.

### Metadata

```yaml
---
name: ai-agent-architect
description: Expert in designing and building LLM agent systems including RAG pipelines, multi-agent architectures, and agentic workflows. This skill should be used when building AI agents, designing RAG systems, implementing LLM applications, or working with agent frameworks like LangChain, LlamaIndex, or CrewAI. Covers architecture patterns (ReAct, Plan-and-Execute, Reflexion), retrieval strategies, data integration (structured + unstructured), prompt engineering for agents, and production considerations.
---
```

### SKILL.md Structure

**1. Overview & When to Use** (~200 words)
- What this skill provides
- When to invoke it
- What it doesn't cover

**2. Agent Architecture Patterns** (~800 words)
- ReAct (Reasoning + Acting)
- Plan-and-Execute
- Reflexion (Self-Reflection)
- Tool-Using Agents
- Multi-Agent Systems
- When to use each pattern

**3. RAG System Design** (~600 words)
- Naive RAG (single-shot retrieval)
- Hierarchical RAG (multi-level indexing)
- Agentic RAG (agent-driven retrieval)
- Query transformation strategies
- Retrieval strategies (vector, hybrid, metadata filtering)

**4. Data Integration Patterns** (~400 words)
- Structured data handling (CSVs, databases, APIs)
- Unstructured data processing (PDFs, bios, text)
- Hybrid approaches (combining structured + unstructured)
- Vector store design patterns
- Metadata enrichment strategies

**5. Framework Selection Guide** (~300 words)
- LangChain: When to use, strengths, gotchas
- LlamaIndex: When to use, strengths, gotchas
- CrewAI: When to use, strengths, gotchas
- Custom: When to build from scratch
- Decision tree for framework selection

**6. Prompt Engineering for Agents** (~400 words)
- System prompts for agentic behavior
- Reasoning chain design
- Tool descriptions and instructions
- Output formatting and parsing
- Few-shot examples for agents

**7. Production Considerations** (~300 words)
- Evaluation strategies (accuracy, relevance, cost)
- Latency optimization
- Cost management
- Error handling and fallbacks
- Observability and debugging

### References Directory

**`references/agent_patterns_deep_dive.md`** (~2k words)
- Detailed implementations of each agent pattern
- Code examples and pseudocode
- Comparisons and trade-offs
- When each pattern fails

**`references/rag_architecture_guide.md`** (~1.5k words)
- Advanced RAG techniques
- Indexing strategies
- Chunk size optimization
- Embedding model selection
- Reranking and filtering

**`references/production_playbook.md`** (~1k words)
- Deployment patterns
- Monitoring and logging
- A/B testing frameworks
- Cost optimization techniques
- Security considerations

### Assets Directory

**`assets/agent_boilerplate/`**
- `langchain_agent_template.py` - Basic LangChain agent setup
- `llamaindex_rag_template.py` - LlamaIndex RAG boilerplate
- `requirements.txt` - Common dependencies
- `config.yaml` - Configuration template
- `.env.example` - Environment variables

**`assets/architecture_diagrams/`**
- `react_pattern.mmd` - Mermaid diagram of ReAct pattern
- `rag_pipeline.mmd` - RAG architecture visualization
- `multi_agent_system.mmd` - Multi-agent interaction diagram

### Scripts Directory

**`scripts/setup_agent_env.py`**
- Sets up Python virtual environment
- Installs required dependencies
- Validates API keys
- Creates project structure

**`scripts/generate_mock_embeddings.py`**
- Generates synthetic embeddings for testing
- Creates mock vector store
- Useful for prototyping without API costs

---

## Skill 2: `firstmark-case-context`

### Purpose
Provides all context, requirements, and constraints specific to the FirstMark Talent Signal Agent case study. Temporary skill to be deleted after case completion.

### Metadata

```yaml
---
name: firstmark-case-context
description: Context and requirements for the FirstMark Capital Talent Signal Agent case study. Includes case specifications, evaluation rubric, FirstMark background, portfolio insights, and mock data structures. This skill should only be invoked explicitly when working on the FirstMark case study deliverables.
---
```

### SKILL.md Structure

**1. Case Study Overview** (~150 words)
- Problem statement: Match executives to portfolio company roles
- Key challenge: Structured + unstructured data integration
- Target roles: CTO, CFO candidates
- Mock data requirement

**2. Deliverables Checklist** (~200 words)
- [ ] 1-2 page write-up OR slide deck
  - Problem framing
  - Agent design
  - Architecture
  - Production considerations
- [ ] Lightweight Python prototype
  - Data ingestion
  - Matching logic
  - Ranked recommendations with reasoning
- [ ] README or Loom video
  - Implementation explanation
  - How to run the code

**3. Evaluation Rubric** (~300 words)

| Criterion | Weight | What They're Looking For |
|-----------|--------|-------------------------|
| **Product Thinking** | 25% | Understanding VC/talent workflows, user needs, problem framing |
| **Technical Design** | 25% | Modern LLM/agent frameworks, modular architecture, retrieval/prompting |
| **Data Integration** | 20% | Handling structured + unstructured data, vector stores, metadata joins |
| **Insight Generation** | 20% | Useful, explainable, ranked outputs with clear reasoning trails |
| **Communication** | 10% | Clear explanation of approach, decisions, and next steps |

**4. FirstMark Context** (~250 words)
- Platform team structure
- Talent network (portfolio companies, guilds, LinkedIn)
- Current manual process pain points
- Typical use cases and workflows

**5. Implementation Guidance** (~200 words)
- How to map rubric to technical decisions
- What to prioritize for each criterion
- Common pitfalls to avoid
- How to demonstrate thinking

### References Directory

**`references/case_brief.md`**
- Full case study requirements (extracted from PDF)
- Exact wording of deliverable requirements
- Timeline and submission details

**`references/firstmark_research.md`**
- Firm overview and history
- Portfolio companies list
- Platform team structure
- Recent investments and focus areas

**`references/role_context.md`**
- AI Builder role description
- What they're looking for in candidates
- Team structure and reporting
- Key initiatives for the role

### Assets Directory

**`assets/mock_data/`**
- `companies.csv` - Portfolio company data structure
  ```csv
  company_id,name,stage,industry,headcount,location,open_roles
  ```
- `roles.csv` - Open role specifications
  ```csv
  role_id,company_id,title,level,requirements,nice_to_haves
  ```
- `candidates.csv` - Executive candidate pool
  ```csv
  candidate_id,name,current_role,years_experience,skills,location
  ```
- `bios.json` - Unstructured biographical text
  ```json
  [{"candidate_id": "...", "bio": "...", "linkedin_summary": "..."}]
  ```

**`assets/writeup_template.md`**
```markdown
# Talent Signal Agent: FirstMark Case Study

## Problem Framing
[How you understand the problem and user needs]

## Agent Design
[Your approach and why you chose it]

## Architecture
[Technical design and data flow]

## Production Considerations
[Scaling, evaluation, iteration]

---
🤖 Generated with Claude Code
```

### Scripts Directory

**`scripts/generate_talent_data.py`**
- Generates realistic synthetic talent data
- Creates companies, roles, candidates, bios
- Ensures data consistency across files
- Configurable size and complexity

**`scripts/validate_deliverables.py`**
- Checks that all required deliverables exist
- Validates data structures
- Ensures rubric coverage
- Pre-submission checklist

---

## Implementation Plan

### Phase 1: Setup & Initialization (30 mins)

**Tasks:**
1. Initialize both skills using `init_skill.py`
2. Set up directory structure
3. Create placeholder files
4. Validate YAML frontmatter

**Commands:**
```bash
cd /path/to/firstmark/.claude/skills/

# Initialize ai-agent-architect
python scripts/init_skill.py ai-agent-architect --path wai-agent-architect

# Initialize firstmark-case-context
python scripts/init_skill.py firstmark-case-context --path wfirstmark-case-context
```

**Deliverables:**
- [ ] Two skill directories with proper structure
- [ ] Valid SKILL.md templates
- [ ] Empty resource directories ready to populate

---

### Phase 2: Build `ai-agent-architect` (2-3 hours)

**Priority Order:**

**2.1 Core SKILL.md Content** (60 mins)
- Write Overview & When to Use
- Document Agent Architecture Patterns (focus on ReAct + Plan-and-Execute)
- RAG System Design section
- Framework Selection Guide

**2.2 Reference Files** (45 mins)
- Create `references/agent_patterns_deep_dive.md`
- Create `references/rag_architecture_guide.md`
- Focus on practical patterns, not exhaustive coverage

**2.3 Assets** (30 mins)
- Create `assets/agent_boilerplate/langchain_agent_template.py`
- Create `assets/agent_boilerplate/requirements.txt`
- Create basic Mermaid diagrams

**2.4 Scripts** (30 mins)
- Create `scripts/setup_agent_env.py`
- Create `scripts/generate_mock_embeddings.py`

**2.5 Validation** (15 mins)
- Run `scripts/quick_validate.py`
- Test skill invocation
- Verify all references work

---

### Phase 3: Build `firstmark-case-context` (1-2 hours)

**Priority Order:**

**3.1 Core SKILL.md Content** (30 mins)
- Case Study Overview
- Deliverables Checklist
- Evaluation Rubric table
- Implementation Guidance

**3.2 Reference Files** (20 mins)
- Extract case brief details to `references/case_brief.md`
- Compile FirstMark research to `references/firstmark_research.md`
- Copy role context to `references/role_context.md`

**3.3 Mock Data Generation** (45 mins)
- Write `scripts/generate_talent_data.py`
- Create realistic synthetic data
- Generate example CSVs and JSON
- Validate data structures

**3.4 Assets** (20 mins)
- Create `assets/writeup_template.md`
- Add example mock data files to `assets/mock_data/`

**3.5 Validation** (15 mins)
- Run `scripts/quick_validate.py`
- Test data generation script
- Verify template formatting

---

### Phase 4: Integration & Testing (45 mins)

**4.1 Skills Working Together** (20 mins)
- Test invoking both skills simultaneously
- Verify they complement each other
- Check for context conflicts or duplication

**4.2 End-to-End Workflow Test** (25 mins)
- Test workflow: "Design the Talent Signal Agent architecture"
  - Should pull from ai-agent-architect for patterns
  - Should reference firstmark-case-context for requirements
- Test workflow: "Generate the prototype code"
  - Should use boilerplate from ai-agent-architect
  - Should use mock data from firstmark-case-context

---

### Phase 5: Packaging & Documentation (30 mins)

**5.1 Package Skills** (15 mins)
```bash
scripts/package_skill.py wai-agent-architect ./dist
scripts/package_skill.py wfirstmark-case-context ./dist
```

**5.2 Create Usage Guide** (15 mins)
- Document how to invoke each skill
- Provide example workflows
- Note what to delete after case completion

---

## Total Time Estimate

| Phase | Time | Priority |
|-------|------|----------|
| Phase 1: Setup | 30 mins | Must Have |
| Phase 2: ai-agent-architect | 2-3 hours | Must Have |
| Phase 3: firstmark-case-context | 1-2 hours | Must Have |
| Phase 4: Integration & Testing | 45 mins | Should Have |
| Phase 5: Packaging | 30 mins | Nice to Have |
| **TOTAL** | **5-7 hours** | |

**Fast Track (3-4 hours):**
- Skip detailed reference files
- Minimal assets (just templates)
- Basic scripts only
- Skip formal packaging

---

## Usage Examples

### Example 1: Architecture Design

```
User: "Help me design the Talent Signal Agent architecture using modern LLM patterns"

Action: Invoke ai-agent-architect skill

Claude will:
1. Suggest appropriate agent patterns (likely Plan-and-Execute for multi-step matching)
2. Recommend RAG architecture (hybrid structured + unstructured retrieval)
3. Provide boilerplate code to start from
4. Guide framework selection (LangChain vs LlamaIndex)

Then invoke firstmark-case-context to:
1. Check architecture against evaluation rubric
2. Ensure it addresses VC talent workflows
3. Validate it meets deliverable requirements
```

### Example 2: Prototype Implementation

```
User: "Build the Python prototype for candidate matching"

Action: Invoke both skills together

ai-agent-architect provides:
- Agent implementation template
- RAG pipeline code
- Prompt engineering patterns

firstmark-case-context provides:
- Mock data generation script
- Data structures to use
- Rubric criteria to demonstrate
```

### Example 3: Deliverable Generation

```
User: "Generate the technical writeup covering all evaluation criteria"

Action: Invoke firstmark-case-context (main) + ai-agent-architect (reference)

firstmark-case-context provides:
- Writeup template structure
- Evaluation rubric to address
- Required sections

ai-agent-architect provides:
- Technical content for architecture section
- Production considerations content
- Design rationale
```

---

## Success Criteria

### For `ai-agent-architect`
- [ ] Can design an agent architecture without additional research
- [ ] Provides working code templates that run
- [ ] Covers ReAct, Plan-and-Execute, and RAG patterns
- [ ] Gives clear framework recommendations
- [ ] Includes production considerations
- [ ] Reusable for future AI agent projects

### For `firstmark-case-context`
- [ ] Contains all case requirements
- [ ] Generates realistic mock data
- [ ] Maps clearly to evaluation rubric
- [ ] Provides deliverable templates
- [ ] Includes FirstMark context

### For Integration
- [ ] Skills work together without conflicts
- [ ] Can complete case study using both skills
- [ ] Reduces implementation time by 50%+
- [ ] Provides clear reasoning trails
- [ ] Demonstrates strong product thinking

---

## Post-Case Cleanup

After case study submission:

**Keep:**
- ✅ `ai-agent-architect` skill (valuable for role + future projects)

**Delete:**
- ❌ `firstmark-case-context` skill (no longer needed)
- ❌ Mock data files (unless useful for demos)

**Archive:**
- 📦 Case deliverables to portfolio
- 📦 Implementation learnings to personal docs

---

## Next Steps

1. **Review this plan** - Confirm approach and timeline
2. **Execute Phase 1** - Initialize both skills
3. **Build Phase 2** - Complete ai-agent-architect (highest value)
4. **Build Phase 3** - Complete firstmark-case-context (case-specific)
5. **Test & Iterate** - Validate skills work together
6. **Use for case** - Apply skills to actual deliverables

---

**Ready to proceed?** Start with Phase 1 initialization.
