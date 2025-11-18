# FirstMark Talent Signal Agent - Current Workflow Implementation Analysis

**Date**: November 16, 2025  
**Repository Branch**: claude/airtable-workflow-integration-01RK76tfNrr5errZpCEjiW75  
**Status**: Planning Phase (No Active Python Implementation Yet)

---

## Executive Summary

The FirstMark Talent Signal Agent case is currently in the **planning and design phase**. While comprehensive architectural documentation and design decisions have been created, **no working Python implementation or workflow orchestration system exists yet**. 

The repository contains:
- Detailed case requirements and specifications
- Architectural planning documents with design decisions
- Mock data schemas (defined but not generated)
- JavaScript portfolio scraping utilities (data prep only)
- No active workflow execution, API endpoints, or agent implementation

**Time Constraint**: Presentation scheduled for 5 PM on 11/19 (3 days from repository snapshot date)

---

## 1. Current Workflows (Conceptual, Not Implemented)

### Planned Workflow Components

The system is designed to have 4 main workflow stages:

#### A. **Data Ingestion Workflow**
**Status**: NOT IMPLEMENTED
- **Input**: CSV files (Mock_Guilds.csv, Exec_Network.csv) + text files (bios, job descriptions)
- **Process**: 
  - Normalize CSV headers and field values
  - Store structured data in database
  - Embed unstructured text (bios) for semantic search
- **Output**: Ingested and indexed data in database
- **Planned Tool**: Python script + SQLite/Supabase
- **Notes**: Design decision made to keep ingestion simple (not using LLM for this, just basic CSV parsing)

#### B. **Role Specification Generation Workflow**
**Status**: PLANNED, NOT IMPLEMENTED
- **Input**: Open role description (text or user input)
- **Process**:
  - Generate/refine role specification using LLM
  - Structure spec with dimensions: Values, Abilities, Skills, Experience, Seniority
  - Create assessment rubric with weights
- **Output**: Standardized Role Spec JSON
- **Planned Tool**: LLM (Claude) with structured output format
- **Storage**: Role specs stored as JSON artifacts

#### C. **Candidate Research & Assessment Workflow**
**Status**: PLANNED, NOT IMPLEMENTED
- **Input**: Candidate profile (structured data) + Role spec
- **Process** (Two parallel research paths):
  1. **Research Path**: Use OpenAI Deep Research API to enrich candidate info
  2. **Assessment Path**: Evaluate candidate against role spec rubric
- **Output**: 
  - Research findings with source citations
  - Assessment scorecard with confidence levels
  - Justification/reasoning for each dimension
- **Planned Tools**:
  - OpenAI Deep Research API (preferred for research)
  - GPT-4.5 for assessment
  - Structured output format for consistent scoring
- **Mock Data**: Fake Apollo enrichment responses (not real API)

#### D. **Ranking & Reporting Workflow**
**Status**: PLANNED, NOT IMPLEMENTED
- **Input**: Assessment results for candidate pool
- **Process**:
  - Aggregate scores across candidates
  - Generate ranked list with confidence intervals
  - Create detailed reasoning trails
  - Surface top matches with actionable insights
- **Output**: 
  - Ranked candidate list (Markdown + JSON)
  - Individual candidate scorecards
  - Comparative analysis (why #1 beats #2)
  - Investigation trails (how to drill down into matches)

---

## 2. Current Architecture

### Technology Stack (Planned vs. Actual)

#### Data Infrastructure
- **Structured Data Storage**: SQLite (demo), Supabase (future consideration)
- **Vector Storage**: NOT YET SELECTED (options: Pinecone, Supabase pgvector, others)
- **Mock Data**: CSV files + plain text files

#### AI/Agent Framework
- **Primary Research Tool**: OpenAI Deep Research API
- **Assessment Agent**: Custom LLM-based evaluation (likely Claude)
- **Framework**: NOT FINALIZED (considering LangChain, Agno, custom Python)

#### Data Processing
- **Node.js Scripts**: Portfolio scraping utilities (existing)
  - `scrape_companies.js` - Scrapes FirstMark portfolio company pages
  - `process_portfolio.js` - Transforms raw portfolio data
  - `create_summary.js` - Generates CSV/MD summaries
- **Python**: NOT YET IN USE (will be primary for case implementation)

### Data Flow Diagram (Conceptual)

```
INPUTS
├── Structured Data
│   ├── Mock_Guilds.csv (guild members, roles, companies)
│   └── Exec_Network.csv (executives, titles, network connections)
├── Unstructured Data
│   ├── Executive Bios (text files, ~10-20 profiles)
│   └── Job Descriptions (text files, 3-5 open roles)
└── FirstMark Portfolio Data
    └── Via scrape_companies.js (already extracted)

PROCESSING LAYER
├── Data Ingestion
│   └── Python: CSV normalization + database storage
├── Role Spec Generation
│   └── LLM: Create standardized role specifications
├── Candidate Research
│   ├── OpenAI Deep Research API
│   └── Mock Apollo enrichment
├── Assessment
│   └── Structured LLM evaluation against rubric
└── Ranking
    └── Score aggregation + reasoning trails

OUTPUTS
├── Ranked Candidates (JSON + Markdown)
├── Assessment Scorecards (per candidate)
├── Research Trails (sources + citations)
└── Investigation Interface (TBD - Streamlit/UI/Notebook)
```

### Database Schema (Planned)

Based on `data_schema.md`:

#### Mock_Guilds Table
```
- guild_member_id (PK)
- guild_name (CTO Guild, CFO Guild, etc.)
- exec_id (FK to executives)
- exec_name
- company_name
- company_domain
- role_title (raw: "SVP Engineering", "CFO")
- function (enum: CTO, CFO, CPO, CRO)
- seniority_level (enum: C-Level, VP, Head, Director)
- location
- company_stage (Seed, A, B, C, Growth)
- sector (SaaS, Consumer, Fintech, etc.)
- is_portfolio_company (bool)
```

#### Exec_Network Table
```
- exec_id (PK)
- exec_name
- current_title
- current_company_name
- current_company_domain
- role_type (CTO, CFO, CRO, etc.)
- primary_function (Engineering, Finance, Revenue)
- location
- company_stage
- sector
- recent_exit_experience (bool)
- prior_companies (semicolon-separated)
- linkedin_url
- relationship_type (Guild, Portfolio Exec, Partner 1st-degree, Event)
- source_partner
```

#### Role Spec (Artifact - JSON)
```
{
  "role_id": "...",
  "role_title": "CFO",
  "company_name": "...",
  "company_stage": "B",
  "specifications": {
    "values": {...},
    "abilities": {...},
    "skills": {...},
    "experience": {...},
    "seniority": "C-Level"
  },
  "assessment_rubric": {
    "dimensions": [...],
    "weights": {...},
    "scale": "1-5"
  }
}
```

#### Assessment Result
```
{
  "assessment_id": "...",
  "candidate_id": "...",
  "role_id": "...",
  "scores": {
    "dimension_1": {
      "score": 4,
      "confidence": "HIGH",
      "reasoning": "..."
    }
  },
  "overall_score": 3.8,
  "overall_confidence": "MEDIUM",
  "research_sources": [...],
  "justification": "...",
  "counterfactuals": [...]
}
```

---

## 3. Existing Integrations & APIs

### Implemented
- None for the Talent Signal Agent (too early in development)

### Planned/Evaluated
- **OpenAI Deep Research API** - SELECTED for candidate research
  - Reason: "Good enough" balance of cost and performance
  - Fallback options: Hugging Face models, Open Deep Research (open-source)
  
- **Apollo API** - STUB IMPLEMENTATION ONLY
  - For enriching person/company data
  - Currently mocked (fake response data) - not connecting to real API
  - Real implementation deferred for MVP validation
  
- **Alternative Enrichment Tools** (evaluated but not selected):
  - Bright Data
  - Firecrawl
  - People Data Labs
  - Harmonic
  - Exa
  - Perplexity
  
- **Database Options** (under consideration):
  - SQLite (demo/local)
  - Supabase (with pgvector for embeddings)
  
- **Vector Store** - NOT YET SELECTED
  - Options considered: Pinecone, Supabase pgvector, others
  - Decision: Defer until MVP phase

---

## 4. Workflow Management & Orchestration

### Current State: NONE IMPLEMENTED

### Planned Approaches (Evaluated in case notes)

#### Option 1: Custom Python Script with LLM Agents
- **Status**: Preferred for 48-hour demo
- **Tools**: Python + LangChain/custom agent loop
- **Orchestration**: Sequential execution with state management
- **Trigger**: Command-line or notebook execution

#### Option 2: Full Agent Framework
- **Status**: Considered but deferred
- **Tools**: Agno or Deep Agents framework
- **Features**: Built-in UI, state management, worker allocation
- **Drawback**: Higher setup complexity for 48-hour timeframe

#### Option 3: Open Source Deep Research
- **Status**: Evaluated, deferred to MVP
- **Project**: Open Deep Research framework
- **Features**: Full agent orchestration, research pipeline
- **Issue**: Learning curve, not necessary for demo

### Key Design Decisions on Orchestration

1. **Research Method**:
   - Use OpenAI Deep Research API (not building custom research agent)
   - Reason: Faster to implement, sufficient quality for demo

2. **Enrichment**:
   - Do NOT implement real Apollo integration (too much scope)
   - Instead: Stub function with mock Apollo responses
   - Future: Real API integration in MVP phase

3. **Candidate Profile**:
   - SKIP standardized candidate profile creation
   - Reason: Not mission-critical for 48-hour demo
   - Future: Can extend if needed

4. **Assessment Method**:
   - Two-evaluation approach:
     1. LLM-guided evaluation using spec rubric
     2. LLM self-generated rubric evaluation
   - Compare results for robustness

---

## 5. Main Workflow Files & Their Purposes

### Current Repository Structure

```
/home/user/FirstMark/
├── case/                          # CASE DELIVERABLES & SPECS
│   ├── case_brief.md              # Official case requirements
│   ├── wbcasenotes_v1.md          # DETAILED PLANNING (656 lines)
│   ├── data_schema.md             # Database schema definitions
│   └── archive/                   # Previous iterations
│
├── scripts/                       # DATA PREPARATION (Node.js)
│   ├── scrape_companies.js        # Portfolio scraping (uses Puppeteer)
│   ├── process_portfolio.js       # Data transformation
│   ├── create_summary.js          # CSV/MD export
│   └── README.md                  # Script documentation
│
├── research/                      # RESEARCH & DATA OUTPUTS
│   ├── Firm_DeepResearch.md       # FirstMark firm analysis
│   ├── interviewprompt.md         # Interview prep
│   ├── member_research/           # Partner/team member deep dives
│   └── interview_research/        # Role & interview context
│
├── AGENTS.md                      # ARCHITECTURE GUIDELINES
├── REQUIREMENTS.md                # PROJECT REQUIREMENTS
├── CLAUDE.md                      # CLAUDE CODE INSTRUCTIONS
└── README.md                      # Project overview
```

### Key Documentation Files (Non-Code)

| File | Lines | Purpose | Status |
|------|-------|---------|--------|
| `case/wbcasenotes_v1.md` | 674 | Master planning document with all decisions, architectures, and design rationale | Complete |
| `case/data_schema.md` | 40 | Database schema definitions for inputs and outputs | Complete |
| `case/case_brief.md` | 76 | Official case requirements from FirstMark | Complete |
| `REQUIREMENTS.md` | 51 | Project development guidelines and constraints | Complete |
| `AGENTS.md` | (duplicate of REQUIREMENTS.md) | Architecture and deployment guidelines | Complete |

### Data Preparation Scripts (Existing)

| Script | Purpose | Input | Output | Status |
|--------|---------|-------|--------|--------|
| `scrape_companies.js` | Scrape FirstMark portfolio from website | FirstMark website | `research/portfolio_raw.json`, `portfolio_detailed.json` | Functional |
| `process_portfolio.js` | Transform raw portfolio to clean data | `portfolio_raw.json` | `research/portfolio_table.md` | Functional |
| `create_summary.js` | Generate CSV and summary | `portfolio_*.json` | `research/portfolio_export.csv`, `portfolio_summary.md` | Functional |

### Missing Implementation Files (To Be Created)

**Python Agent Scripts (NOT YET CREATED)**:
1. `data_ingestion.py` - CSV loading, normalization, DB storage
2. `role_spec_generator.py` - LLM-based role spec creation
3. `candidate_researcher.py` - OpenAI Deep Research API wrapper
4. `candidate_assessor.py` - Evaluation against rubric
5. `ranking_engine.py` - Score aggregation and ranking
6. `main.py` or `agent.py` - Orchestration entry point
7. `utils.py` - Shared utilities (prompts, schemas, helpers)

**Mock Data Files (NOT YET CREATED)**:
1. `Mock_Guilds.csv` - Guild member executive data
2. `Exec_Network.csv` - Extended network executives
3. `bios/` directory - Executive biography text files
4. `job_descriptions/` directory - Open role descriptions

---

## 6. API & Integration Points (Conceptual)

### External APIs (Planned)

#### OpenAI Deep Research API
```
Endpoint: TBD (via OpenAI SDK)
Method: async call
Input: Candidate name + context + research query
Output: Research report + citations
Status: To be implemented as wrapper function
Mock Status: Will test with real API if available
```

#### Apollo API (MOCKED)
```
Endpoint: N/A - Using stub function
Input: Person name/company
Output: Enriched person data (fake/mock responses)
Status: Stub only - no real API integration
Future: Real integration in MVP phase
```

### Internal API Points (Planned)

#### Role Spec API (LLM-based)
```
Input: Role description (string) + company context
Output: Structured Role Spec (JSON)
Implementation: Direct LLM call with structured output
```

#### Assessment API (LLM-based)
```
Input: Candidate data + Role Spec + Rubric
Output: Assessment Result (JSON with scores + reasoning)
Implementation: LLM agent loop
```

#### Ranking API
```
Input: List of Assessment Results
Output: Ranked candidates + comparisons
Implementation: Python logic (no LLM needed)
```

---

## 7. Key Design Decisions & Trade-offs

### Completed Decisions (from wbcasenotes_v1.md)

| Decision | Options Considered | Selection | Rationale |
|----------|------------------|-----------|-----------|
| **Research Method** | Deep Research API, Open-source agent, Custom | OpenAI Deep Research API | Fast, sufficient quality, cost-effective |
| **Enrichment** | Real Apollo, Bright Data, Firecrawl | Mock/Stub Apollo | Time constraint; avoid setup complexity |
| **Candidate Profile** | Standardized profiles, Bespoke per-role | Skip for demo | Not critical path; can extend later |
| **Ingestion** | LLM-based, Code-based | Basic Python CSV | Simple, sufficient for mock data |
| **Assessment** | Single LLM rubric, Dual evaluation | Dual evaluation (rubric + self-generated) | Validate robustness |
| **Mock Data** | Fully synthetic, Mix of real/synthetic | Real people (researched) + synthetic companies | More convincing, realistic demo |
| **Demo Database** | SQLite, Supabase | SQLite for simplicity | Demo-only; upgrade in production |
| **UI** | Streamlit, Jupyter, None | Markdown + JSON outputs + optional UI | Focus on reasoning trails; UI secondary |

### Open Decisions (from case notes)

1. **Agent Framework Selection**: LangChain vs. Agno vs. Custom
   - Current lean: Custom Python (KISS principle for 48 hours)
   
2. **Investigation Interface**: How users drill down into matches
   - Options: CLI, Web UI, Notebook, Markdown
   - Current: Not finalized
   
3. **Confidence Scoring**: How to express confidence alongside scores
   - Planned: H/M/L + percentage alongside numeric scores
   
4. **Counterfactuals**: How to generate and present alternative explanations
   - Planned: Include but exact mechanism TBD

---

## 8. Current Implementation Status

### Completed
- ✅ Case requirements specification
- ✅ Architecture planning and design
- ✅ Data schema definitions
- ✅ Design decision documentation
- ✅ Portfolio scraping utilities (Node.js)
- ✅ Firm and team member research
- ✅ Mock data schema design

### In Progress / Next Phase
- ⏳ Mock data generation (CSV + text files)
- ⏳ Python project setup (dependencies, structure)
- ⏳ Data ingestion pipeline
- ⏳ Role spec generation logic
- ⏳ Candidate research integration
- ⏳ Assessment and ranking engines
- ⏳ Output formatting and visualization

### Not Started
- ❌ Working Python implementation
- ❌ Database initialization
- ❌ API integrations
- ❌ Real workflow orchestration
- ❌ Testing and validation
- ❌ User interface (if planned)
- ❌ Documentation/README for implementation

---

## 9. Critical Path to Implementation

Based on case notes and 48-hour constraint:

### Phase 1: Setup & Data (4-6 hours)
1. Create mock data files (CSVs + bios + JDs)
2. Set up Python project structure
3. Initialize SQLite database
4. Create data ingestion script

### Phase 2: Core Logic (12-16 hours)
1. Role spec generator (LLM-based)
2. Candidate researcher (OpenAI API wrapper)
3. Assessment engine (LLM with structured output)
4. Ranking and aggregation logic

### Phase 3: Integration & Demo (8-10 hours)
1. Main orchestration script
2. End-to-end workflow execution
3. Output formatting (JSON + Markdown)
4. Example run with pre-populated demo data

### Phase 4: Documentation & Presentation (4-6 hours)
1. Architecture write-up (1-2 pages)
2. README with usage instructions
3. Pre-run example walkthrough (for presentation)
4. Presentation slides/talking points

---

## 10. Recommendations for Next Steps

### Immediate Priority (Next 2 hours)
1. **Generate mock data files**:
   - `Mock_Guilds.csv`: 8-12 fictional but realistic guild members
   - `Exec_Network.csv`: Additional network executives
   - `bios/`: 10-15 executive bio text files
   - `job_descriptions/`: 3-5 open role descriptions

2. **Set up Python project**:
   ```
   case/
   ├── data/
   │   ├── mock_guilds.csv
   │   ├── exec_network.csv
   │   └── (bios and JDs as text files)
   ├── src/
   │   ├── data_ingestion.py
   │   ├── role_spec_gen.py
   │   ├── researcher.py
   │   ├── assessor.py
   │   └── main.py
   └── outputs/
   ```

### Short Term (Next 4-6 hours)
1. **Implement data ingestion** - Load and normalize CSVs
2. **Implement role spec generator** - LLM call with structured output
3. **Implement candidate researcher** - Wrapper around research API

### Medium Term (Next 6-8 hours)
1. **Implement assessor** - Structured evaluation logic
2. **Implement ranking** - Aggregation and comparison
3. **Create end-to-end pipeline** - Wire everything together

### Before Presentation
1. Run full pipeline on mock data
2. Prepare output examples
3. Create presentation write-up
4. Test research API integration (or finalize mock responses)

---

## Summary Table: Workflow Components Status

| Component | Type | Status | Location | Dependencies |
|-----------|------|--------|----------|--------------|
| Case Requirements | Spec | ✅ Complete | `case/case_brief.md` | None |
| Architecture Plan | Design | ✅ Complete | `case/wbcasenotes_v1.md` | None |
| Data Schema | Design | ✅ Complete | `case/data_schema.md` | None |
| Mock Data | Data | ❌ Not created | `case/data/` | None |
| Python Setup | Infrastructure | ❌ Not started | `case/src/` | Python 3.10+ |
| Data Ingestion | Workflow | ❌ Not implemented | `case/src/data_ingestion.py` | Mock data |
| Role Spec Gen | Workflow | ❌ Not implemented | `case/src/role_spec_gen.py` | OpenAI API key |
| Research Integration | Workflow | ❌ Not implemented | `case/src/researcher.py` | OpenAI API key |
| Assessment Engine | Workflow | ❌ Not implemented | `case/src/assessor.py` | Role specs |
| Ranking Engine | Workflow | ❌ Not implemented | `case/src/main.py` | All above |
| Outputs | Artifact | ❌ Not implemented | `case/outputs/` | Ranking engine |
| Documentation | Deliverable | ⏳ In progress | `case/DESIGN.md` | Architecture |

---

**Last Updated**: November 16, 2025
**Next Action**: Begin mock data generation and Python project setup
