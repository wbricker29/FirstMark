# Implementation Tracking

> Task checklist and progress tracking for FirstMark Talent Signal Agent case study
> **Presentation:** 5 PM 11/18 (48 hours remaining)

## High Priority - Critical Decisions First

### Outstanding Decisions (Must Resolve Before Build)

#### Assessment Scoring Mechanics
- [ ] Define confidence calculation method
  - [ ] Based on amount of evidence found?
  - [ ] Based on directness of evidence match?
  - [ ] LLM self-assessment of certainty?
  - [ ] Combination approach?
- [ ] Define what "counterfactuals" means in this context
  - [ ] "What if" scenarios?
  - [ ] Alternative interpretations of ambiguous evidence?
  - [ ] Reasons candidate might NOT be a good fit despite high score?
- [ ] Decide on two evaluation approach
  - [ ] Do BOTH evaluations (rubric-based + LLM self-generated)?
  - [ ] Or just rubric-based evaluation?
  - [ ] If both, how to present/compare results?

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

#### Research Execution Strategy
- [ ] Decide research approach (critical for timeline)
  - [ ] Real OpenAI Deep Research API (potential latency issues)
  - [ ] Mock/stub research data (faster, controlled demo)
  - [ ] Hybrid: Real API for 1 live scenario, mock for 3 pre-runs
- [ ] Decide on LinkedIn scraping
  - [ ] Use Deep Research API only?
  - [ ] Add separate LinkedIn scraping?
  - [ ] Skip for demo?

#### Technical Execution Parameters
- [ ] Determine expected execution times
  - [ ] Research phase: ~X minutes per candidate
  - [ ] Assessment phase: ~X minutes per candidate
  - [ ] Full screen of 10 candidates: ~X minutes total
- [ ] Plan demo execution strategy based on timing
  - [ ] Can we run live screening during demo?
  - [ ] Pre-run all scenarios?
  - [ ] Mix of pre-run + live?

### MVP Simplifications (Decide Now)
- [ ] Module 1 (Upload): Build full CSV processing or pre-populate data manually?
- [ ] Module 2 (New Role): Build UI flow or create records manually?
- [ ] Module 3 (New Search): Build UI flow or create records manually?
- [ ] Airtable Interface: Custom interfaces or standard grid views?
- [ ] File upload deduplication: Implement or skip for demo?
- [ ] Citation handling: Store URLs only or scrape full content?

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
- [ ] Tavily API setup (for incremental search if needed)
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

### Phase 1: Critical Decisions & Schema (Complete First)
1. Resolve all Outstanding Decisions (assessment scoring, schemas, research strategy)
2. Document complete Airtable schema
3. Create structured output schemas for LLM responses
4. Expected: 4-6 hours

### Phase 2: Foundation (Core Infrastructure)
1. Python project setup + dependencies
2. Airtable base creation + table setup
3. Flask webhook server skeleton
4. Expected: 3-4 hours

### Phase 3: Core Workflow (Minimum Viable Demo)
1. Research module (OpenAI Deep Research API integration)
2. Assessment module (evaluation logic)
3. Module 4 (Screen workflow) - end-to-end
4. Expected: 8-10 hours

### Phase 4: Demo Data & Pre-Runs
1. Create 4 role specs for demo portcos
2. Generate/run research for 3 pre-run scenarios
3. Create markdown reports
4. Expected: 6-8 hours

### Phase 5: Supporting Modules (If Time Permits)
1. Module 1 (Upload) - optional
2. Module 2 (New Role) - optional
3. Module 3 (New Search) - optional
4. Expected: 4-6 hours

### Phase 6: Testing & Polish
1. End-to-end testing
2. Demo rehearsal
3. Backup plans
4. Write-up completion
5. Expected: 4-6 hours

**Total Estimated: 29-40 hours** (fits within 48-hour window with buffer)

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
