# Implementation Tracking

> Task checklist and progress tracking for FirstMark Talent Signal Agent case study
> **Presentation:** 5 PM 11/19/2025 (Tuesday)
> **Last Updated:** 2025-11-16

---

## Quick Status Summary

### ✅ Resolved Decisions (Updated 2025-11-16)

**Technology & Architecture:**
- Framework: AGNO
- LLM: GPT-5, GPT-5-mini, o4-mini-deep-research
- Research: OpenAI Deep Research API + Web Search (no separate LinkedIn scraping, no third-party APIs)
- Infrastructure: Flask + ngrok webhook required
- Candidate Profiles: OUT OF SCOPE (bespoke research per role instead)

**Assessment Approach:**
- Two evaluations confirmed: Spec-based + AI-generated rubric (both)
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
   - Deep Research: 3-6 min/candidate (4-8 min for 10 async)
   - Web Search fallback: 1-2 min/candidate (2-3 min for 10 async)
4. **OpenAI API integration review** (1 hour) - Understand response format, structured outputs, web search tool usage
5. **Airtable schema details** (2 hours) - Complete field definitions for all tables

**Total Time to Unblock Build: ~3 hours** (down from 4 hours)

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
- [x] ~~Decide on two evaluation approach~~ → **RESOLVED**
  - **Decision:** BOTH evaluations confirmed (rubric-based + LLM self-generated)
  - [ ] Decide how to present/compare results (can iterate during build)

#### Airtable Schema Details
- [ ] Define complete field list for People Table
  - [ ] Map fields from guildmember_scrape.csv to People table
  - [ ] Decide: Bio field Long Text or Rich Text?
- [ ] Define complete field list for Platform - Hiring - Screen
  - [ ] Status enum values (Draft, Ready to Screen, Processing, Complete, Failed?)
  - [ ] Custom instructions field details
- [ ] Define complete field list for Operations - Workflows
  - [ ] Audit trail fields
  - [ ] Research results storage structure
  - [ ] Assessment results storage structure
  - [ ] Execution logs format
- [ ] Define complete field list for Role Eval Table
  - [ ] Dimension scores: Individual fields vs JSON?
  - [ ] Evidence quotes storage format
  - [ ] Citation links storage format
- [ ] Define complete field list for Research Table
  - [ ] Full research text field structure
  - [ ] Citation structure: URLs only or full content snapshots?

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
    - Full screen (10 candidates async): ~4-8 minutes
  - **Web Search Mode (Fallback/Fast):**
    - Research phase: 30-60 seconds per candidate (gpt-5 + web search)
    - Assessment phase: 30-60 seconds per candidate
    - Total per candidate: ~1-2 minutes
    - Full screen (10 candidates async): ~2-3 minutes
- [x] ~~Plan demo execution strategy based on timing~~ → **RESOLVED**
  - **Decision:** Use Deep Research for 3 pre-run scenarios; can use Web Search mode for live demo if time-constrained
  - Async implementation (asyncio.gather) for concurrent candidate processing

### MVP Simplifications (Decide Now)
- [ ] Module 1 (Upload): Build full CSV processing or pre-populate data manually?
  - **Recommendation:** Pre-populate manually (focus on Module 4)
- [ ] Module 2 (New Role): Build UI flow or create records manually?
  - **Recommendation:** Create records manually in Airtable
- [ ] Module 3 (New Search): Build UI flow or create records manually?
  - **Recommendation:** Create records manually in Airtable
- [ ] Airtable Interface: Custom interfaces or standard grid views?
  - **Recommendation:** Standard grid views + basic filtering
- [x] ~~File upload deduplication~~ → **RESOLVED**
  - **Decision:** Skip for demo (assume clean data)
- [x] ~~Citation handling~~ → **RESOLVED**
  - **Decision:** Store URLs + key quotes from API response (no full content scraping)

---

## High Priority - Foundation

### Mock Data Generation
- [ ] Design and generate mock data
  - [ ] Use existing guildmember_scrape.csv (64 executives - already available)
  - [ ] Create job descriptions for 4 demo portcos
    - [ ] Pigment - CFO Role (B2B SaaS, enterprise, international)
    - [ ] Mockingbird - CFO Role (Consumer DTC, physical product)
    - [ ] Synthesia - CTO Role (AI/ML SaaS, global scale)
    - [ ] Estuary - CTO Role (Data infrastructure, developer tools)
  - [ ] Generate mock research data for 3 pre-run scenarios (Pigment, Mockingbird, Synthesia)
  - [ ] Mock Apollo enrichment data (stub function)

### Data Schemas
- [ ] Design and generate data schemas
  - [ ] Input schemas (CSV structure)
  - [ ] Storage schemas (Airtable tables/fields)
  - [ ] Output schemas (assessment results, reports)

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
- [ ] Set up Python project structure
- [ ] Install dependencies (flask, pyairtable, openai, python-dotenv)
- [ ] Set up environment variables and API key management (.env file)
- [ ] Create requirements.txt

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

- [ ] Implement second evaluation method (LLM generating own rubric) - if time permits
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

### Phase 0: Immediate Pre-Build Tasks (DO FIRST) ⚡
**Time: ~3 hours remaining | Blocks all other work**
1. [x] ~~Document confidence calculation logic~~ ✅ APPROVED
2. [x] ~~Document counterfactuals definition~~ ✅ APPROVED
3. [ ] Review OpenAI Deep Research API documentation (1 hour)
   - File: `reference/docs_and_examples/agno/agno_openai_itegration.md`
   - Understand: response format, citation structure, rate limits, execution time
   - Confirm: Structured output support, web_search_preview tool usage
4. [ ] Create detailed Airtable schema document (2 hours)
   - New file: `demo_planning/airtable_schema.md`
   - Complete field definitions for: People, Screen, Workflows, Role Eval tables
   - Note: Role spec validation can happen during build phase based on actual API results

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
2. Assessment module (evaluation logic + two evaluation types)
   - Implement AssessmentResult Pydantic schema
   - Create assessment agent with web search capability
   - Evidence-aware scoring with confidence levels
3. Module 4 (Screen workflow) - end-to-end
   - Async endpoint implementation with asyncio.gather()
   - Concurrent candidate processing
   - Real-time status updates
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
- Async implementation critical for acceptable demo timing (4-8 min vs 30-60 min sequential)
- This provides demo flexibility: comprehensive results (Deep Research) or faster live execution (Web Search)

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
