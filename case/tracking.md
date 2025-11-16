# Implementation Tracking

> Task checklist and progress tracking for FirstMark Talent Signal Agent case study
> **Presentation:** 5 PM 11/19/2025 (Tuesday)
> **Last Updated:** 2025-01-16

---

## Quick Status Summary

**Current Phase:** Planning Complete → Ready to Begin Implementation
**Last Updated:** 2025-01-16

### 📊 Current Implementation Status

**Planning & Design:** ✅ COMPLETE (100%)
- All architectural decisions finalized
- Complete Airtable schema designed (9 tables, all fields defined)
- Complete Pydantic data models designed
- Role spec templates created
- Demo scenarios planned (4 portcos, 3 pre-run + 1 live)

**Python Implementation:** ⚠️ NOT STARTED (0%)
- Basic project structure only (`main.py` stub, `pyproject.toml`)
- No dependencies installed yet
- No agents implemented
- No webhook server implemented
- No Airtable integration implemented

**Airtable Setup:** ⚠️ NOT STARTED (0%)
- Base not created
- Tables not created
- People data (64 executives) not loaded
- Role specs not created
- Demo scenarios not set up

**Demo Pre-Runs:** ⚠️ NOT STARTED (0%)
- No pre-run screening data generated yet
- Dependent on completing Python implementation + Airtable setup

**Estimated Remaining Work:** 34-38 hours
- Python implementation: 20-24 hours
- Airtable setup: 7 hours
- Pre-run execution: 4-6 hours
- Testing & polish: 3-4 hours

### ✅ Resolved Decisions (Updated 2025-01-16)

**Technology & Architecture:**
- Framework: AGNO
- LLM: GPT-5, GPT-5-mini, o4-mini-deep-research
- Research: OpenAI Deep Research API + Web Search (no separate LinkedIn scraping, no third-party APIs)
- Infrastructure: Flask + ngrok webhook required
- Candidate Profiles: OUT OF SCOPE (bespoke research per role instead)

**Assessment Approach:**
- Single evaluation (Spec-guided): Evidence-aware scoring with confidence levels
- AI-generated rubric: Explicitly deferred to Phase 2+ (not in demo v1)
- Role specs: Fully defined in `demo_planning/role_spec_design.md`

**Demo Strategy:**
- All 4 modules in scope (1-4)
- 3 portcos pre-run (Pigment, Mockingbird, Synthesia)
- 1 portco live (Estuary)
- Candidates from `reference/guildmember_scrape.csv`

**Simplifications:**
- Deduplication: Skip (assume clean data)
- Enrichment: Stub/mock (no real Apollo)
- Citation storage: URLs + quotes from API (no scraping)
- Modules 1-3: Pre-populate data (build Module 4 only)

### 🚧 Critical Items Still Needed (Before Build)

1. ✅ **Confidence calculation logic** - APPROVED
   - Decision: LLM self-assessment + evidence count threshold
2. ✅ **Counterfactuals definition** - APPROVED
   - Decision: "Key reasons candidate might NOT be ideal fit despite high score + Assumptions or evaluation results that are most important/must be true"
3. ✅ **Execution times** - RESOLVED
   - Deep Research: 3-6 min/candidate (~30-60 min for 10 sequential)
   - Web Search fallback: 1-2 min/candidate (~10-20 min for 10 sequential)
4. ✅ **Airtable schema details** - COMPLETED
   - Complete field definitions documented in `demo_planning/airtable_schema.md`
   - All 9 tables designed with full JSON schemas
   - Setup instructions and pre-population checklist included
5. [ ] **OpenAI API integration review** (1 hour) - Understand response format, structured outputs, web search tool usage

**Total Time to Unblock Build: ~1 hour** (down from 3 hours)

---

## High Priority - Critical Decisions First

### Outstanding Decisions (Must Resolve Before Build)

#### Assessment Scoring Mechanics ✅ RESOLVED
- [x] ~~Define confidence calculation method~~ → **APPROVED**
  - **Decision:** LLM self-assessment + evidence count threshold
  - Implementation: LLM evaluates own certainty per dimension; evidence count validates
- [x] ~~Define what "counterfactuals" means~~ → **APPROVED**
  - **Decision:** "Key reasons candidate might NOT be ideal fit despite high score + Assumptions or evaluation results that are most important/must be true"
  - Implementation: LLM generates critical caveats and key assumptions for each assessment
- [x] ~~Decide on evaluation approach~~ → **RESOLVED**
  - **Decision:** Single evaluation (spec-guided) with evidence-aware scoring for demo v1
  - **Future:** AI-generated rubric / alternative evaluation deferred to Phase 2+ (post-demo)

#### Airtable Schema Details ✅ COMPLETED
- [x] Define complete field list for People Table
  - [x] Map fields from guildmember_scrape.csv to People table
  - [x] Bio field: Using linkedin_headline (Long Text)
- [x] Define complete field list for Screens Table (renamed from "Platform - Hiring - Screen")
  - [x] Status enum values: Draft, Ready to Screen, Processing, Complete, Failed
  - [x] Custom instructions field: Optional Long Text field
- [x] Define complete field list for Workflows Table (renamed from "Operations - Workflows")
  - [x] Audit trail fields: Multiple timestamp fields (research_started, research_completed, etc.)
  - [x] Research results storage: Linked to Research_Results table
  - [x] Assessment results storage: Linked to Assessments table
  - [x] Execution logs format: JSON array in execution_log field
- [x] Define complete field list for Assessments Table (renamed from "Role Eval Table")
  - [x] Dimension scores: JSON array in dimension_scores_json field
  - [x] Evidence quotes storage: Embedded in DimensionScore JSON objects
  - [x] Citation links storage: URLs array in DimensionScore JSON objects
- [x] Define complete field list for Research_Results Table
  - [x] Full research text: ExecutiveResearchResult JSON in research_json field
  - [x] Citation structure: Full Citation objects with URL, title, snippet, relevance_note

**See:** `demo_planning/airtable_schema.md` for complete documentation

#### Research Execution Strategy ✅ RESOLVED
- [x] ~~Decide research approach~~ → **RESOLVED**
  - **Decision:** OpenAI Deep Research API (primary) + Web Search builtin (supplemental)
  - **Rationale:** Native OpenAI capabilities only - no third-party search APIs needed
  - **Strategy:** Hybrid approach with flexible execution modes, 3 pre-run + 1 live during demo
  - [ ] Review API docs to determine execution times (1 hour)
- [x] ~~Decide on LinkedIn scraping~~ → **RESOLVED**
  - **Decision:** No separate LinkedIn scraping - Deep Research API handles web research
  - Citation storage: URLs + key quotes from API response (no additional scraping)

#### Technical Execution Parameters ✅ RESOLVED
- [x] ~~Determine expected execution times~~ → **RESOLVED**
  - **Deep Research Mode (Primary):**
    - Research phase: 2-5 minutes per candidate (o4-mini-deep-research)
    - Assessment phase: 30-60 seconds per candidate (gpt-5-mini)
    - Total per candidate: ~3-6 minutes
    - Full screen (10 candidates sequential): ~30-60 minutes
  - **Web Search Mode (Fallback/Fast):**
    - Research phase: 30-60 seconds per candidate (gpt-5 + web search)
    - Assessment phase: 30-60 seconds per candidate
    - Total per candidate: ~1-2 minutes
    - Full screen (10 candidates sequential): ~10-20 minutes
- [x] ~~Plan demo execution strategy based on timing~~ → **RESOLVED**
  - **Decision:** Use Deep Research for 3 pre-run scenarios; use Web Search mode or smaller candidate set for live demo if time-constrained
  - Synchronous implementation (sequential processing) for demo simplicity and reliability

### MVP Simplifications ✅ RESOLVED
- [x] Module 1 (Upload): Pre-populate data manually
  - **Decision:** Focus on Module 4 (Screen workflow) for demo
  - **Rationale:** CSV upload is commodity; screening/assessment is the value demonstration
- [x] Module 2 (New Role): Create records manually in Airtable
  - **Decision:** Manual Airtable data entry for demo scenarios
  - **Rationale:** Role creation is one-time setup, not core workflow
- [x] Module 3 (New Search): Create records manually in Airtable
  - **Decision:** Manual Airtable data entry linking roles to specs
  - **Rationale:** Search setup is straightforward, automation not needed for demo
- [x] Airtable Interface: Standard grid views + basic filtering
  - **Decision:** Use default Airtable views, no custom interfaces
  - **Rationale:** Custom interfaces add development time without demonstrating AI capability
- [x] File upload deduplication: Skip for demo
  - **Decision:** Assume clean data (no duplicate detection logic)
  - **Rationale:** Data quality is pre-ensured, not a demo focus
- [x] Citation handling: Store URLs + key quotes from API
  - **Decision:** No additional web scraping beyond what Deep Research API provides
  - **Rationale:** API citations sufficient for evidence trail

**Implementation Scope for Demo v1.0:** Module 4 (Screen workflow) only - Research + Assessment agents with Airtable integration

---

## High Priority - Foundation

### Mock Data Generation
- [x] Design and generate mock data
  - [x] Use existing guildmember_scrape.csv (64 executives - already available in `reference/`)
  - [x] Create job descriptions for 4 demo portcos
    - [x] Pigment - CFO Role (B2B SaaS, enterprise, international)
    - [x] Mockingbird - CFO Role (Consumer DTC, physical product)
    - [x] Synthesia - CTO Role (AI/ML SaaS, global scale)
    - [x] Estuary - CTO Role (Data infrastructure, developer tools)
  - [ ] Generate mock research data for 3 pre-run scenarios (Pigment, Mockingbird, Synthesia) - **DEFERRED** to after Python implementation
  - [x] Mock Apollo enrichment data (stub function) - **DECISION:** Not needed, research comes from Deep Research API

**Status:** Mock data design complete in `demo_planning/data_design.md`, actual data generation will happen during pre-run phase

### Data Schemas ✅ COMPLETED
- [x] Design and generate data schemas
  - [x] Input schemas (CSV structure) - Documented in `airtable_schema.md`
  - [x] Storage schemas (Airtable tables/fields) - Complete 9-table schema in `airtable_schema.md`
  - [x] Output schemas (assessment results, reports) - Pydantic models documented in `data_design.md`

### Framework Elements
- [x] Role spec framework and template (COMPLETED - see demo_planning/role_spec_design.md)
  - [x] CFO template (6 dimensions with weights)
  - [x] CTO template (6 dimensions with weights)
  - [x] Must-haves, nice-to-haves, red flags structure
  - [ ] Create role specs for 4 demo scenarios
    - [ ] Pigment CFO spec (customize from CFO template)
    - [ ] Mockingbird CFO spec (customize from CFO template)
    - [ ] Synthesia CTO spec (customize from CTO template)
    - [ ] Estuary CTO spec (customize from CTO template)

- [ ] Assessment framework
  - [ ] Assessment rubric (uses role spec dimensions)
  - [ ] Assessment scoring logic (score + confidence + reasoning)
  - [ ] Structured output schema for assessment results

- [ ] Design and generate prompts
  - [ ] Research prompt template (for OpenAI Deep Research API)
  - [ ] Assessment prompt template (with role spec injection)
  - [ ] Report generation prompt

## High Priority - Infrastructure

### Python Project Setup
- [x] Set up Python project structure
  - [x] Created `pyproject.toml` with project metadata
  - [x] Created basic `main.py` stub
  - [x] Python 3.11+ environment configured via `.python-version`
  - [x] Virtual environment at `.venv/`
- [ ] Install dependencies (flask, pyairtable, openai, python-dotenv)
  - **STATUS:** Not yet added to `pyproject.toml`
  - **NEXT:** Add dependencies and run `uv pip install -e .`
- [ ] Set up environment variables and API key management (.env file)
  - **STATUS:** Not yet created
  - **REQUIRED:** OpenAI API key, Airtable API key, Airtable base ID
- [ ] Create requirements.txt
  - **NOTE:** Using `pyproject.toml` instead (modern Python packaging)
  - Will auto-generate from `pyproject.toml` if needed

### Airtable Configuration
- [ ] Create Airtable base
- [ ] Set up all tables:
  - [ ] People Table (with bio field, LinkedIn, etc.)
  - [ ] Company Table
  - [ ] Portco Table (pre-enriched with demo portcos)
  - [ ] Platform - Hiring - Portco Roles
  - [ ] Platform - Hiring - Search
  - [ ] Platform - Hiring - Screen
  - [ ] Operations - Workflows (execution trail, audit log)
  - [ ] Role Spec Table
  - [ ] Research Table
  - [ ] Role Eval Table
- [ ] Define fields for each table
- [ ] Set up Airtable automations/webhooks
- [ ] Design Airtable interfaces/views for demo

### Webhook Server
- [ ] Flask webhook server implementation
  - [ ] `/upload` endpoint (CSV ingestion)
  - [ ] `/screen` endpoint (main screening workflow)
  - [ ] `/new-role` endpoint (optional for demo)
  - [ ] `/research` endpoint (optional for demo)
- [ ] ngrok setup and configuration
- [ ] Test webhook connectivity with Airtable

## High Priority - Core Functions

### Data Ingestion Module
- [ ] Build CSV processing logic
- [ ] Implement data normalization
- [ ] Create deduplication logic
- [ ] Load data to Airtable via pyairtable

### Mock Enrichment
- [ ] Create Apollo API stub/mock
- [ ] Generate mock enrichment response data

### Research Module
- [ ] OpenAI Deep Research API integration
- [ ] Research prompt engineering
- [ ] Citation extraction and storage
- [ ] Research result parsing and storage

### Assessment Module
- [ ] Build assessment/evaluation logic
- [ ] Implement rubric-based scoring
- [ ] Generate confidence levels (H/M/L)
- [ ] Create reasoning/justification generation
- [ ] Add counterfactuals

### Report Generation
- [ ] Create assessment report templates
- [ ] Generate markdown outputs
- [ ] Store results in Airtable

## High Priority - API Integrations

- [ ] OpenAI API setup and testing
  - [ ] Deep Research API (o4-mini-deep-research)
  - [ ] Standard API (gpt-5, gpt-5-mini)
  - [ ] Web Search builtin tool (web_search_preview)
- [ ] pyairtable integration and CRUD operations testing
- [ ] Verify API rate limits and error handling

## High Priority - Testing & Demo Prep

### Testing
- [ ] Test data ingestion workflow end-to-end
- [ ] Test research workflow with 2-3 candidates
- [ ] Test assessment workflow
- [ ] Test full screening workflow
- [ ] Verify all audit trails and logging work
- [ ] Test webhook connectivity (ngrok + Airtable)
- [ ] Verify error handling and rate limiting
- [ ] Test structured output schema validation

### Demo Preparation - Pre-Run Scenarios (3 portcos)
- [ ] Pigment CFO - Pre-run complete screening
  - [ ] Select 3-5 candidate profiles from guildmember_scrape.csv
  - [ ] Run research + assessment workflow
  - [ ] Generate complete audit trails
  - [ ] Create markdown reports
- [ ] Mockingbird CFO - Pre-run complete screening
  - [ ] Select 3-5 candidate profiles
  - [ ] Run research + assessment workflow
  - [ ] Generate complete audit trails
  - [ ] Create markdown reports
- [ ] Synthesia CTO - Pre-run complete screening
  - [ ] Select 3-5 candidate profiles
  - [ ] Run research + assessment workflow
  - [ ] Generate complete audit trails
  - [ ] Create markdown reports

### Demo Preparation - Live Execution (1 portco)
- [ ] Estuary CTO - Prepare for live demo
  - [ ] Select 2-3 candidate profiles for live screening
  - [ ] Pre-load candidates and role spec into Airtable
  - [ ] Test live execution flow (don't save results)
  - [ ] Prepare talking points for live demo portion

### Demo Logistics
- [ ] Prepare ranked candidate views in Airtable
- [ ] Test drill-down into reasoning ("why #1 beat #2")
- [ ] Create demo script with timing
- [ ] Test ngrok stability
- [ ] Prepare backup plan if webhook fails
- [ ] Verify markdown exports are generated
- [ ] Practice full demo presentation flow

## High Priority - Deliverables

- [ ] Write 1-2 page write-up or slide deck
  - [ ] Problem framing and agent design
  - [ ] Data sources and architecture
  - [ ] Key design decisions and tradeoffs
  - [ ] Production extension plan
- [ ] Create README with setup instructions
- [ ] Prepare demo script
- [ ] Optional: Record Loom video walkthrough

## Mid Priority

- [ ] Implement second evaluation method (LLM generating own rubric) - explicitly deferred to Phase 2+ (post-demo)
- [ ] Add LinkedIn scraping capability (if needed beyond Deep Research)
- [ ] Enhanced investigation/drill-down UI in Airtable
- [ ] Apollo API schema and logistics (for future real implementation discussion)

## Optional / Out of Scope for Demo

- [ ] Review the existing company finder skill
- [ ] Note - Tamar Yehoshua is fslack on one page
- [ ] Add role spec customization UI flow (manual for demo)
- [ ] Create standardized title mapping table (dropdowns for demo)
- [ ] Build candidate profile component (explicitly out of scope)
- [ ] File upload deduplication logic (pre-populate for demo)
- [ ] Custom Airtable Interfaces (standard views for demo)

---

## Implementation Phase Recommendations

### Phase 0: Immediate Pre-Build Tasks ✅ COMPLETE
**Time: Originally 3 hours | Status: DONE**
1. [x] ~~Document confidence calculation logic~~ ✅ APPROVED
2. [x] ~~Document counterfactuals definition~~ ✅ APPROVED
3. [ ] Review OpenAI Deep Research API documentation (1 hour) - **REMAINING**
   - File: `reference/docs_and_examples/agno/agno_openai_itegration.md`
   - Understand: response format, citation structure, rate limits, execution time
   - Confirm: Structured output support, web_search_preview tool usage
   - **NOTE:** Can be done concurrently with Phase 1 setup work
4. [x] ~~Create detailed Airtable schema document~~ ✅ COMPLETED
   - File: `demo_planning/airtable_schema.md` (created 2025-01-16)
   - Complete 9-table schema with all field definitions
   - JSON schemas for all complex data structures
   - Setup instructions and pre-population checklist

**Current Blocker Status:** ✅ UNBLOCKED - Ready to begin implementation

---

## 🚀 Next Steps - Immediate Actions

### Critical Path to Demo (in priority order)

**1. Airtable Base Setup (7 hours) - DO FIRST**
   - Create new Airtable base: "FirstMark Talent Signal Agent Demo"
   - Create all 9 tables with field definitions from `airtable_schema.md`
   - Import 64 executives from `reference/guildmember_scrape.csv` to People table
   - Create 4 portco records (Pigment, Mockingbird, Synthesia, Estuary)
   - Create 4 role records (2 CFO, 2 CTO)
   - Create 6 role specs (2 templates + 4 customized from `role_spec_design.md`)
   - Create 4 search records linking roles to specs
   - Create 4 screen records (3 Draft for pre-run, 1 Draft for live demo)
   - **Why first:** Airtable setup is independent work and unblocks API key setup

**2. Python Dependencies & Environment (1 hour)**
   - Add dependencies to `pyproject.toml`: `flask`, `pyairtable`, `openai`, `python-dotenv`, `pydantic`
   - Run `uv pip install -e .`
   - Create `.env` file with API keys (OpenAI, Airtable base ID, Airtable API token)
   - Test basic OpenAI API connectivity
   - Test basic Airtable API connectivity (read from People table)

**3. Core Python Implementation (20-24 hours)**
   - Create Pydantic models (ExecutiveResearchResult, AssessmentResult, etc.)
   - Implement research agent (Deep Research API + parser agent)
   - Implement assessment agent (spec-guided evaluation)
   - Implement Flask webhook server with `/screen` endpoint
   - Implement Airtable integration (read screens, write results)
   - End-to-end testing with 1 candidate

**4. Webhook & Automation Setup (1 hour)**
   - Start Flask server
   - Start ngrok tunnel
   - Create Airtable automation: "When Screen.status → Ready to Screen, POST to webhook"
   - Test automation with dummy screen

**5. Pre-Run Executions (4-6 hours)**
   - Run Pigment CFO screening (3-4 candidates)
   - Run Mockingbird CFO screening (3-4 candidates)
   - Run Synthesia CTO screening (4-5 candidates)
   - Verify all results populated correctly in Workflows, Research_Results, Assessments

**6. Demo Preparation & Polish (3-4 hours)**
   - Test Estuary CTO live demo flow (don't save results)
   - Create Airtable views for demo (ranked candidates, drill-down into reasoning)
   - Practice demo presentation flow
   - Create backup plan if webhook fails
   - Write 1-2 page write-up or slide deck

**Total Estimated Time:** 36-43 hours

---

### Phase 1: Foundation (Core Infrastructure) ✅ Partially Resolved
1. ✅ Technology stack decided (AGNO, GPT-5, Flask, Airtable)
2. ✅ Research strategy decided (OpenAI Deep Research API)
3. ✅ Role spec framework completed
4. [ ] Python project setup + dependencies
5. [ ] Airtable base creation + table setup
6. [ ] Flask webhook server skeleton
7. Expected: 3-4 hours

### Phase 2: Core Workflow (Minimum Viable Demo)
1. Research module (OpenAI Deep Research API + Web Search integration)
   - Implement ExecutiveResearchResult Pydantic schema
   - Create research agent with flexible execution modes (Deep Research vs Web Search)
   - Environment flag for demo flexibility
2. Assessment module (spec-guided evaluation with evidence-aware scoring)
   - Implement AssessmentResult Pydantic schema
   - Create assessment agent with web search capability
   - Evidence-aware scoring with confidence levels (None/null for insufficient evidence)
3. Module 4 (Screen workflow) - end-to-end
   - Synchronous endpoint implementation (sequential processing)
   - Full event streaming for audit trail capture
   - Real-time status updates via console logs
4. Expected: 8-10 hours

### Phase 3: Demo Data & Pre-Runs
1. Create 4 role specs for demo portcos (using templates from role_spec_design.md)
2. Pre-populate Airtable with candidates from guildmember_scrape.csv
3. Run research + assessment for 3 pre-run scenarios (Pigment, Mockingbird, Synthesia)
4. Create markdown reports
5. Expected: 6-8 hours

### Phase 4: Supporting Modules (OPTIONAL - If Time Permits)
**Recommendation: SKIP these - pre-populate data manually instead**
1. Module 1 (Upload) - skip, pre-populate data
2. Module 2 (New Role) - skip, create records manually
3. Module 3 (New Search) - skip, create records manually
4. Expected: 0 hours (skipped)

### Phase 5: Testing & Polish
1. End-to-end testing of Module 4 workflow
2. Test live execution for Estuary scenario (don't save)
3. Demo rehearsal
4. Backup plans (if webhook fails)
5. Write-up completion (1-2 pages)
6. Expected: 4-6 hours

**Total Estimated: 20-28 hours** (leaves buffer within 48-hour window)
**Simplified from original:** Skipped Modules 1-3 automation saves ~4-6 hours
**Implementation Notes:**
- Implement both Deep Research and Web Search modes with environment flag toggle
- Synchronous implementation keeps demo simple and reliable (sequential processing)
- Execution mode flexibility provides demo options: comprehensive results (Deep Research) or faster live execution (Web Search)
- Async optimization deferred to post-demo phase

---

## Reference Items

### Research APIs & Tools

**Deep Research APIs:**
- EXA
- FIRECRAWL
- OPENAI
- Perplexity
- https://parallel.ai/
- https://deeplookup.com/welcome/
- https://brightdata.com/products/web-scraper
- https://huggingface.co/Alibaba-NLP/Tongyi-DeepResearch-30B-A3B
  - https://github.com/Alibaba-NLP/DeepResearch
- Provider Showcase - https://medium.com/@leucopsis/open-source-deep-research-ai-assistants-157462a59c14

**Deep Research Agent Examples:**
- https://github.com/Arindam200/awesome-ai-apps/tree/main/advance_ai_agents/deep_researcher_agent
- https://github.com/Arindam200/awesome-ai-apps/tree/main/advance_ai_agents/candidate_analyser

**Tools:**
- https://github.com/Alibaba-NLP/DeepResearch
- https://huggingface.co/spaces?q=Web&sort=likes
- https://anotherwrapper.com/open-deep-research
- https://github.com/camel-ai/camel

**Framework References:**
- https://github.com/lastmile-ai/mcp-agent/tree/main/src/mcp_agent/workflows/deep_orchestrator
- https://github.com/FrancyJGLisboa/agent-skill-creator
