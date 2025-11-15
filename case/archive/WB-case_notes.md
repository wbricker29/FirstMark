# WB Case Working Document

## 1. CASE OVERVIEW

### Deliverables
1. **Write-up or slide deck (1-2 pages)**
   - Overview of problem framing and agent design
   - Description of data sources and architecture
   - Key design decisions and tradeoffs
   - How to extend this in production

2. **Lightweight Python prototype**
   - Ingests mock structured + unstructured data
   - Identifies potential matches
   - Outputs ranked recommendations with reasoning
   - Example: "Jane Doe → strong fit for CFO @ AcmeCo because of prior Series B fundraising experience at consumer startup"

3. **README or Loom video (optional)**
   - Explain what's implemented vs. conceptual

### Assessment Details
**WHO:** Beth Viner, Shilpa Nayyar, Matt Turck, Adam Nelson (optional)
**WHEN:** 5 PM 11/19

### Evaluation Rubric

| Category | Weight | Excellence Criteria |
|----------|--------|-------------------|
| **Product Thinking** | 25% | Clear understanding of VC and talent workflows. Scopes an agent that actually fits how the firm works. Communicates assumptions and value. |
| **Technical Design** | 25% | Uses modern LLM/agent frameworks logically; modular design; thoughtful about retrieval, context, and prompting. |
| **Data Integration** | 20% | Handles structured + unstructured data elegantly (e.g., vector store, metadata joins). Sensible about what's automatable. |
| **Insight Generation** | 20% | Produces useful, explainable, ranked outputs — not just text dumps. Demonstrates reasoning or scoring logic. |
| **Communication & Clarity** | 10% | Clean, clear explanation of what was done, why, and next steps. No jargon for the sake of it. |

### Core Requirement
**Ingest → Match → Explain**
- Match executives (CFO/CTO) to roles
- Ability to diagnose/investigate the 'match'

---

## 2. STRATEGIC APPROACH

### My Perspective: AI Transformation in Venture
- How I think about attacking transformation in venture
- How it applies to talent matching
- The approach I'm taking:
  - Breakdown components
  - Identify complexity and requirements
  - Focus on quality of thinking over perfect execution

### Three-Tier Solution Framework

#### **Ideal Solution**
What this would look like in an ideal state, both for this feature and the surrounding ecosystem:

**Centralized Data Platform:**
- Central table storing core information for all use cases
  - People, roles (title + company), companies, relationships
  - Canonical title mapping table and mechanism
- Standardized ETL pipelines for ingestion
  - Extract, Normalize, Reconcile Entity (Person, Company, etc) with existing data
  - Append new records
- Immutable system design
  - Ability only to add new records and identify/relate active items
- Parallel operations storage system
  - Standardized logging of all events
- Standardized evergreen operations on records
  - Enriching people/companies via Apollo
  - Return raw enrichment request response, cleaned response content, and enrichment data
  - Store enrichment results (before and after)
- Smart ingestion with HITL
  - When mapping is unclear, trigger human-in-the-loop

**Guild Model:**
- Forward-deployed development use cases
- Centralized foundation and standards building

#### **MVP Solution**
If asked to develop my first cut for actual use and evaluation:
- Use existing APIs (Harmonic, Apollo, etc.)
- Focused on core matching workflow
- Basic but robust data handling
- Clear evaluation framework

#### **Demo Solution** (48-hour constraint)
The demo that is illustrative in 2 days:
- Real people + some fake data to demonstrate normalization challenges
- Mock API responses (stubbed enrichment)
- Focus on showcasing thinking and architecture
- Working prototype demonstrating key concepts

### Market Analysis Approach
Before building, would identify:

**E2E Solutions:**
- Cost and performance analysis
- Existing talent matching platforms

**Partial Solutions:**
- Enrichment: Apollo, People Data Labs
- Candidate AI Evaluation tools
- Network matching tools

**Development Options:**
- General Python frameworks & LLM frameworks (ideally firm standard)
- Research approaches:
  - Research-as-API (OpenAI Deep Research, Perplexity, Exa)
  - Open source approaches
  - Custom agentic systems

### Key Principles
- **Emphasize quality of thinking** over perfect implementation
- **KISS principle:** Make basic assumptions, err on the side of simplicity
- **Context-aware design:** Ultimate design depends on Time, Value, and Security concerns
  - Security is a firm-level decision and needs to be clear
- **Confidence scoring:** Must have confidence alongside any evaluation

### Key Tradeoffs
- **Complexity vs. Time:** Balancing sophisticated matching with 48-hour constraint
- **Automation vs. Explainability:** AI-generated scores vs. transparent reasoning
- **Breadth vs. Depth:** Comprehensive data gathering vs. focused quality research
- **Real vs. Mock:** Using real portfolio data vs. creating illustrative examples

---

## 3. DECISION LOG

### ✅ Decided

**Mock Data Approach:**
- Real people + maybe fake
- Data will show normalization issues (non-standard conventions, names, etc.)

**Enrichment:**
- Enrichment tool will be stub
- Will mock API response data from Apollo

### ❓ Open Decisions

**Research Method:**
- [ ] OpenAI Deep Research API
- [ ] Other deep research API (Exa, Perplexity)
- [ ] Custom agentic approach

**Data Ingestion:**
- [ ] LLM-based ingestion
- [x] Code-based ingestion (basic CSV ingest)
- [ ] Hybrid approach

**LLM Responsibility Decomposition:**
- [ ] Research
- [ ] Enrichment
- [ ] Assessment
- [ ] Reporting

**Framework Choice:**
- [ ] Agno
- [ ] LangChain/LangGraph
- [ ] Other

**Database Platform:**
- [ ] Local SQLite
- [ ] Supabase

**UI:**
- [ ] Include UI
- [ ] CLI/Script only
- [ ] Jupyter notebook interface

**Mock Data Fidelity:**
- [ ] Totally fake
- [ ] Some reality (leaning this way)

**Data Scraper:**
- [ ] BrightData
- [ ] Firecrawl

**Database Granularity:**
- [ ] Full entity decomposition (role name table, etc.)
- [ ] Simpler schema for demo

**Research Methodology:**
- [ ] Synthesized and granular methods?
- [ ] Store full source citation content?
- [ ] AI-generated non-deterministic grade + deterministic hybrid?
- [ ] Does candidate profile include assessment or separate?


### FUTURE QUESTIONS AND CONSIDERATIONS
**Location Handling:**
- [ ] Person-based vs. role-based
- [ ] How to handle changes over time

**Data Source Integration:**
- [ ] Can we use Affinity as central source of people truth?
- [ ] What does Affinity integration look like?

**Additional Options:**
- [ ] Assessment of previous people in role (profiling them, input of fit)

---

## 4. TECHNICAL DESIGN

### Data Design

#### Input Schemas

| Type | Example | Description |
|------|---------|-------------|
| **Structured** | Mock_Guilds.csv | Two FirstMark Guilds. Columns: company, role title, location, seniority, function |
| **Structured** | Exec_Network.csv | Partner's connections. Columns: name, current title, company, role type (CTO, CRO, etc.), location, LinkedIn URL |
| **Unstructured** | Executive bios | ~10-20 bios (mock or real) in text format |
| **Unstructured** | Job descriptions | Text of 3-5 open portfolio roles for CFO and CTO |

#### Storage Model

**Core Entities:**
- People table
- Roles table (title + company)
- Companies table
- Relationships table

**Operational Data:**
- Research logs
- Enrichment results (raw + cleaned)
- Assessment scores and reasoning
- Source citations

**Company Table Requirements:**
- Review startup taxonomy
- Include stage information

#### Output Schemas

**Assessment Results Overview:**
- Ranked list of candidates per role
- Summary statistics

**Individual Assessment Results:**
- Result scorecard
- Result justification
- Individual component drill-down
- Confidence scores

### Component Architecture

#### 1. Data Ingestion & Normalization
**Inputs:** CSV files, text documents
**Process:**
- Read CSV
- Normalize headers
- Extract and normalize entities and values
- Handle non-standard conventions

**Ideal:** Centralized platform
**Demo:** Python script to ingest, normalize, and store

#### 2. Person Enrichment
**Method:** Stubbed with mock Apollo data
**Future:** Firecrawl or similar for real implementation
**Storage:**
- Raw API responses
- Cleaned/normalized data
- Enrichment metadata

#### 3. Person Research
**Components:**
- Web and API researcher
- Research synthesis storage
- Research run log
- Research source storage

#### 4. Role Spec Generator
**Framework Definition:**
- Components: Values, Abilities, Skills, Experience
- Grading scale
- Standards for specs

**Base Role Specs:**
- Standard spec for given title
- Title + company archetype variants

**Company-Specific Enrichment:**
- Plain text job description → structured spec
- Manual editing capabilities

#### 5. Candidate Profile Generator
**Framework:**
- Standardized way to describe a candidate for a role
- Components, definitions, requirements, standards

#### 6. Candidate Assessment Engine
**Definition:** Standardized framework and process for evaluating candidates
**Dual Process:**
1. General process for human execution
2. LLM agent execution process

**Outputs:**
- Topline assessment
- Individual component assessment scores
- Reasoning for each score
- Confidence levels

#### 7. Report Generation
**Outputs:**
- Ranked recommendations
- Reasoning trails
- Scorecard visualizations

### Tech Stack

**Data Processing:**
- Python
- Pandas for CSV handling

**Database:**
- SQLite or Supabase (TBD)

**LLM Framework:**
- Agno or LangChain/LangGraph (TBD)

**Research Tools:**
- OpenAI Deep Research API or
- Exa/Firecrawl or
- Custom agentic system

**Scraping:**
- BrightData or Firecrawl (TBD)

### System Gates

1. **Data Ingestion and Normalization** ✓
2. **Enrichment** ✓
3. **Frameworks:**
   - Role spec ✓
   - Candidate profile ✓
   - Assessment methodology ✓
4. **Presentation** ✓

---

## 5. EXECUTION CHECKLIST

### High Priority

- [ ] **Design and generate data schemas**
  - [ ] Input schemas
  - [ ] Storage schemas
  - [ ] Output schemas

- [ ] **Design and generate key framework elements**
  - [ ] Role spec framework
  - [ ] Candidate profile framework
  - [ ] Assessment/match score framework

- [ ] **Design and generate prompts**
  - [ ] Research prompts
  - [ ] Assessment prompts
  - [ ] Report generation prompts

- [ ] **Identify and setup platform**
  - [ ] Agno or LangChain/LangGraph
  - [ ] Firecrawl or BrightData
  - [ ] Database (SQLite or Supabase)

- [ ] **Design and generate mock data**
  - [ ] Mock_Guilds.csv
  - [ ] Exec_Network.csv
  - [ ] Executive bios
  - [ ] Job descriptions

### Mid Priority

- [ ] Apollo API schema and logistics (if time permits)

### Optional

- [ ] Review the existing company finder skill
- [ ] Mock interview preparation
- [ ] Generalized enrichment capabilities

---

## 6. REFERENCE MATERIALS

### APIs & Research Tools

**Deep Research APIs:**
- EXA
- FIRECRAWL
- OpenAI
- Perplexity
- [Parallel AI](https://parallel.ai/)
- [DeepLookup](https://deeplookup.com/welcome/)
- [BrightData Web Scraper](https://brightdata.com/products/web-scraper)

**Open Source Models:**
- [Tongyi-DeepResearch-30B](https://huggingface.co/Alibaba-NLP/Tongyi-DeepResearch-30B-A3B)
  - [GitHub Repo](https://github.com/Alibaba-NLP/DeepResearch)
- [Provider Showcase](https://medium.com/@leucopsis/open-source-deep-research-ai-assistants-157462a59c14)

### Example Implementations

**Agent Examples:**
- [Deep Researcher Agent](https://github.com/Arindam200/awesome-ai-apps/tree/main/advance_ai_agents/deep_researcher_agent)
- [Candidate Analyser](https://github.com/Arindam200/awesome-ai-apps/tree/main/advance_ai_agents/candidate_analyser)

**Reference Repos:**
- [MCP Deep Orchestrator](https://github.com/lastmile-ai/mcp-agent/tree/main/src/mcp_agent/workflows/deep_orchestrator)
- [Agent Skill Creator](https://github.com/FrancyJGLisboa/agent-skill-creator)

**Tools:**
- [HuggingFace Web Spaces](https://huggingface.co/spaces?q=Web&sort=likes)
- [Another Wrapper - Open Deep Research](https://anotherwrapper.com/open-deep-research)
- [CAMEL AI](https://github.com/camel-ai/camel)

### Future Extensions

- Mock interview capabilities
- Generalized enrichment pipelines
- Integration with existing tools/APIs

---

## 7. NOTES & MISC

- Note: Tamar Yehoshua is listed as fslack on one page (verify)
- A2a reference
