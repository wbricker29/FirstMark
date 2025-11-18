---
version: "1.0-minimal"
created: "2025-01-16"
updated: "2025-01-17"
project: "Talent Signal Agent"
context: "FirstMark Capital AI Lead Case Study"
agentos_status: "Prototype complete (demo/agentos_app.py). See docs/agent_os_integration_spec.md for migration roadmap."
---

# Product Requirements Document: Talent Signal Agent

AI-powered executive matching system for FirstMark Capital's talent team

## Problem Statement

### Current Situation

FirstMark Capital's talent team manages relationships with hundreds of executives across their network (guild members, portfolio executives, partner connections) and regularly assists portfolio companies with critical leadership hires (CFO, CTO, CPO roles). The current process is:

- **Manual and Time-Intensive:** Talent team relies on memory, spreadsheets, and personal networks to identify candidates
- **Limited Scalability:** Partner/talent team bandwidth constrains the number of searches they can support
- **Inconsistent Coverage:** Some portfolio companies get deep talent support, others get minimal assistance
- **Implicit Matching Logic:** Matching criteria lives in team members' heads, not captured systematically
- **No Reasoning Trail:** Hard to explain why specific candidates were/weren't recommended

**Key Pain Points:**

1. Takes significant partner/talent time to generate initial candidate shortlists for open roles
2. Risk of missing strong matches when network data isn't top-of-mind
3. Hard to explain match quality objectively to portfolio CEOs
4. Difficult to track what searches have been run and for whom

### Desired State

An AI-powered system that:

1. **Accelerates Shortlist Generation:** From hours/days → minutes to generate ranked candidate lists
2. **Increases Coverage:** Surface strong matches the team might not immediately recall
3. **Provides Clear Reasoning:** Explain why each candidate is/isn't a fit with evidence
4. **Captures Matching Logic:** Codify evaluation criteria in reusable role specifications and centralized prompt templates
5. **Enables Self-Service:** Portfolio companies can see match rationale, talent team focuses on high-value relationship work
6. **Provides Execution Transparency:** Real-time visibility into agent workflows via Agno's built-in UI dashboard

**Success Looks Like:**

- Talent team says "I'd actually use these rankings to prioritize my outreach"
- Portfolio CEOs understand why candidates were recommended (transparent reasoning)
- Faster turnaround on search requests without sacrificing match quality
- Ability to run exploratory searches without heavy manual effort

### Gap Analysis

**What's Missing:**

1. **Structured Executive Data:** Network data exists in scattered sources (LinkedIn exports, email threads, CRM notes)
2. **Role Evaluation Framework:** No standardized way to define "what good looks like" for CFO vs CTO roles
3. **Research Automation:** Manual research on each candidate (LinkedIn, news, company background)
4. **Evidence-Based Ranking:** No systematic scoring that ties back to observable evidence
5. **Audit Trail:** No record of searches run, candidates evaluated, reasoning provided
6. **Prompt Management:** Agent prompts are hardcoded, making iteration and A/B testing difficult
7. **Workflow Visibility:** No real-time visibility into agent execution, debugging requires log parsing

**Why This Gap Exists:**

- Talent work has been relationship-first, not data-first
- Small team size prioritizes execution over tooling
- No AI expertise in-house to build sophisticated matching systems
- Insufficient time to build production infrastructure from scratch

**Why Now:**

- Agno framework provides native UI dashboard and prompt template system for rapid prototyping
- Modern LLM frameworks make agent orchestration feasible
- OpenAI Deep Research API enables automated executive research
- Airtable provides no-code data layer for talent team adoption
- 48-hour case study window forces MVP scope discipline

---

## Goals

### Primary Objectives

1. **Demonstrate AI-Augmented Matching:** Prototype system that ranks candidates for open roles with clear reasoning
2. **Validate Approach Quality:** Show FirstMark team this direction is worth pursuing further
3. **Prove Technical Capability:** Demonstrate modern agent frameworks, structured outputs, evidence-based evaluation, centralized prompt management, and workflow transparency
4. **Establish Product Thinking:** Show understanding of VC talent workflows and stakeholder needs
5. **Enable Rapid Iteration:** Use Agno's native prompt templates and UI dashboard for fast experimentation and debugging

### Success Metrics

**Product Evaluation (From Case Rubric):**

- **Product Thinking (25%):** Understanding of VC/talent workflows, stakeholder needs, UX considerations
- **Technical Design (25%):** Modern frameworks, modular architecture, retrieval/context/prompting patterns
- **Data Integration (20%):** Structured + unstructured data handling, vector stores, metadata joins
- **Insight Generation (20%):** Useful, explainable, ranked outputs with reasoning trails
- **Communication (10%):** Clear explanation of approach, tradeoffs, next steps

**Demo Success Metrics:**

- ✅ Process 10-15 candidates across 4 portfolio company scenarios
- ✅ Generate ranked lists with dimension-level scores (0-100 scale)
- ✅ Provide evidence-based reasoning for each assessment
- ✅ Complete assessment pipeline in <10 minutes per candidate
- ✅ Export results to Airtable + markdown reports

**Team Adoption Indicators (Qualitative):**

- "I'd use this ranking to prioritize my outreach calls"
- "The reasoning helps me explain matches to portfolio CEOs"
- "This surfaces candidates I wouldn't have thought of immediately"
- "I trust the evaluation because it shows its work"

---

## Scope

### In Scope (Demo v1.0-minimal)

**Module 1: Data Upload**

- ✅ CSV ingestion via Airtable webhook (Phase 1 design)
- ✅ People table population (64 executives from guild scrape)
- ✅ Basic deduplication logic (name + company matching)
- ✅ **Phase 0:** Using `talent-signal-candidate-loader` Claude skill as temporary setup automation

**Module 2: New Open Role**

- ✅ Airtable-only workflow (no Python backend)
- ✅ Create role records linking to portfolio companies
- ✅ Attach role specifications (CFO/CTO templates)

**Module 3: New Search**

- ✅ Airtable-only workflow (no Python backend)
- ✅ Link searches to open roles
- ✅ Attach custom search guidance/notes

**Module 4: Candidate Screening (PRIMARY DEMO)**

- ✅ Webhook-triggered screening workflow
- ✅ **Deep Research – primary and only required mode for v1.0-minimal** (OpenAI Deep Research API)
- ✅ **Incremental Search – optional single-pass supplement when quality is low** (up to two web/search calls)
- ✅ Spec-guided assessment with evidence-aware scoring (uses Agno ReasoningTools for structured reasoning trails)
- ✅ **Centralized Prompt Templates** using Agno's native template system for research and assessment agents
- ✅ **Agno UI Dashboard** for real-time workflow monitoring, debugging, and session inspection
- ✅ Dimension-level scores (1-5 scale with None for Unknown)
- ✅ Overall score calculation (0-100 scale)
- ✅ Reasoning, counterfactuals, confidence tracking
- ✅ Citation tracking
- ✅ Raw research markdown retention (Deep Research API response)
- ✅ Markdown assessment report generation (human-readable exports)

**Data & Infrastructure:**

- ✅ Mock data from guildmember_scrape.csv (64 real executives)
- ✅ 4 portfolio scenarios (Pigment CFO, Mockingbird CFO, Synthesia CTO, Estuary CTO)
- ✅ Airtable database with 7 tables (6 core workflow + Role_Specs helper for template storage; Phase 2+: Workflows, Research_Results)
- ✅ Flask webhook server with ngrok tunnel
- ✅ Synchronous execution for demo simplicity (single-process)

**Airtable Schema (7 Tables):**

**Core Workflow Tables (6):**
- **People**: Executive network data (guild members, portfolio execs, partner connections)
- **Portco**: Portfolio company records (Pigment, Mockingbird, Synthesia, Estuary)
- **Portco_Roles**: Open leadership positions (CFO/CTO roles at portfolio companies)
- **Searches**: Talent search requests (links roles to candidate screening batches)
- **Screens**: Candidate screening batches (webhook-triggered workflow executions)
- **Assessments**: Individual candidate evaluations (research + assessment results)

**Helper Tables (1):**
- **Role_Specs**: Template storage table (not workflow data) - Reusable evaluation templates (CFO_Standard_v1, CTO_Standard_v1) for role specifications

**Phase 2+ Tables (Deferred):**
- Workflows: Audit trail for multi-step workflows
- Research_Results: Separate storage for deep research outputs

**Demo Scenarios:**

| Scenario | Portfolio Company | Role Type | Role Spec Template | Candidates | Pre-run Status |
|----------|------------------|-----------|-------------------|-----------|----------------|
| 1 | Pigment | CFO | CFO_Standard_v1 | 3-5 from guild | ⏸️ Pre-run before demo |
| 2 | Mockingbird | CFO | CFO_Standard_v1 | 3-5 from guild | ⏸️ Pre-run before demo |
| 3 | Synthesia | CTO | CTO_Standard_v1 | 3-5 from guild | ⏸️ Pre-run before demo |
| 4 | Estuary | CTO | CTO_Standard_v1 | 2-3 from guild | ⏸️ Live demo execution |

**Notes:**
- Scenarios 1-3 demonstrate results quality and assessment reasoning
- Scenario 4 demonstrates real-time workflow execution and Agno UI monitoring
- All candidates sourced from guildmember_scrape.csv (64 total executives)
- Each scenario uses standard role spec template (CFO_Standard_v1 or CTO_Standard_v1)
- Role specs stored in Role_Specs table, attached to Portco_Roles records

**Technical Stack:**

- ✅ Agno agent framework with native UI dashboard and prompt template system
- ✅ **AgentOS prototype** (demo/agentos_app.py) - FastAPI runtime with enhanced observability (parallel to Flask)
- ✅ OpenAI models: o4-mini-deep-research (research), gpt-5-mini (assessment)
- ✅ Pydantic structured outputs (ExecutiveResearchResult, AssessmentResult)
- ✅ Airtable for database + data management
- ✅ Flask (production webhook) + FastAPI (AgentOS prototype) dual entrypoints
- ✅ Python 3.11+ with uv package manager
- ✅ Agno UI for workflow visualization and debugging
- ✅ Agno prompt templates for centralized prompt management

### Out of Scope (Phase 2+)

**Not in Demo:**

- ❌ Company/role uploads via Module 1 (only people uploads)
- ❌ Production authentication/authorization
- ❌ Real Apollo API enrichment (using mock data instead)
- ❌ Model-generated rubric evaluation (alternative assessment)
- ❌ Candidate profile standardization
- ❌ Async/concurrent processing (demo uses synchronous execution)
- ❌ Production deployment (Docker, cloud hosting)
- ❌ Rate limiting, retry logic beyond basic exponential backoff
- ❌ Vector stores for semantic search (using deterministic filters)
- ❌ **Fast Mode** – future optimization (Phase 2+), not required for demo
- ❌ **Multi-iteration supplemental search loops** – Phase 2+ enhancement
- ❌ **SQLite workflow events database** – Phase 2+ audit trail enhancement
- ❌ **Concurrent workers and parallel processing** – Phase 2+ performance optimization

**Explicitly Deferred:**

- Alternative evaluation path (model-generated dimensions)
- Comprehensive error handling and edge cases
- Performance optimization and load testing
- Advanced deduplication (fuzzy matching)
- Multi-tenant support
- External API integrations beyond OpenAI
- SQLite-backed workflow audit trail (Phase 2+)
- Rich observability stack (metrics, events DB) – Phase 2+

### Future Considerations

**Phase 2 Enhancements:**

1. **AgentOS Migration:** Transition from Flask to AgentOS (FastAPI) runtime for enhanced observability, control plane features, and production deployment (see `docs/agent_os_integration_spec.md`)
2. **Fast Mode:** Web search fallback for quicker candidate screening
3. **Multi-iteration supplemental search:** Adaptive quality thresholds with iterative research
4. **Research Caching:** Avoid re-researching same candidates
5. **Parallel Processing:** Concurrent candidate screening with multiple workers (leverages AgentOS multi-agent orchestration)
6. **SQLite → Postgres Migration:** Production-grade database with AgentOS templates
7. **Enhanced Observability:** Metrics, eval hooks, RBAC via AgentOS control plane

**Phase 3+ Vision:**

- Two-way sync with portfolio company ATS systems
- Proactive candidate recommendations ("You should meet X for Y role")
- Network growth suggestions ("Add executives from sector Z")
- Historical search analytics and learning from outcomes

---

## User Stories

### Story 1: Portfolio CEO Requests Talent Help

**As a** Portfolio Company CEO
**I want** FirstMark's talent team to quickly identify strong CFO/CTO candidates from their network
**So that** I can move fast on a critical leadership hire without starting from scratch

**Acceptance Criteria:**

- Given CEO submits open role details to FirstMark talent team
- When talent team creates a new search and runs screening
- Then CEO receives ranked shortlist within 1-2 days with clear reasoning for each candidate
- And CEO can understand why candidates were recommended based on transparent criteria

### Story 2: Talent Team Runs Candidate Screening

**As a** FirstMark Talent Team Member
**I want** to screen 10-15 candidates against a role specification in minutes
**So that** I can focus my time on relationship building vs manual research

**Acceptance Criteria:**

- Given open role with attached role specification (CFO/CTO template)
- When I link 10-15 candidate records and click "Start Screening"
- Then system automatically researches each candidate and generates assessments
- And results include ranked list with scores, reasoning, and confidence levels
- And I can export results as markdown or share Airtable view with portfolio CEO

### Story 3: Understanding Match Reasoning

**As a** Talent Team Member
**I want** clear, evidence-based reasoning for each candidate assessment
**So that** I can explain recommendations to portfolio CEOs and make judgment calls

**Acceptance Criteria:**

- Given completed candidate screening
- When I review assessment results
- Then I see dimension-level scores (1-5) with evidence quotes and citations
- And I see overall score (0-100) calculated from dimension scores
- And I see "reasons for" and "reasons against" summaries
- And I see counterfactuals (critical assumptions that must be true)
- And unknown dimensions are marked as "Insufficient Evidence" rather than forced scores

### Story 4: Customizing Role Specifications

**As a** Talent Team Member
**I want** to create custom role specifications for unique searches
**So that** evaluations match portfolio company's specific needs vs generic criteria

**Acceptance Criteria:**

- Given base CFO or CTO template
- When I duplicate and customize dimension weights/definitions
- Then new spec is saved and can be attached to searches
- And assessments use custom spec for dimension-level scoring
- And audit trail captures which spec version was used

### Story 5: Reviewing Assessment Quality

**As a** Talent Team Member
**I want** to see confidence levels and research quality metrics
**So that** I know which assessments are reliable vs need manual review

**Acceptance Criteria:**

- Given completed screening workflow
- When I review assessment results
- Then I see overall confidence (High/Medium/Low)
- And I see dimension-level confidence for each score
- And I see a simple research sufficiency indicator (e.g., citation count + pass/fail)
- And insufficient research is flagged so I know when manual review is needed (including when the single incremental search step ran)

### Story 6: Monitoring Agent Workflows

**As a** Developer or Talent Team Power User
**I want** real-time visibility into agent execution via Agno UI dashboard
**So that** I can debug issues, understand agent reasoning, and optimize workflow performance

**Acceptance Criteria:**

- Given screening workflow is running
- When I open Agno UI dashboard
- Then I see real-time workflow execution status and progress
- And I can inspect session state, agent inputs/outputs, and reasoning trails
- And I can review historical workflow runs for debugging and optimization
- And I can view prompt templates used for each agent step

### Story 7: Iterating on Prompts

**As a** Developer or Talent Team Member
**I want** centralized, version-controlled prompt templates
**So that** I can rapidly iterate on agent prompts without code changes

**Acceptance Criteria:**

- Given Agno native prompt template system
- When I need to adjust research or assessment prompts
- Then I can edit templates in centralized location (not hardcoded in Python)
- And changes are version-controlled for audit trail
- And I can A/B test different prompt variations
- And I can revert to previous versions if new prompts underperform

---

## Python-Specific Considerations

### Performance Requirements

**Throughput:**

- For v1.0-minimal:
  - Process candidates sequentially per Screen
  - One Flask worker is sufficient
  - Demo expectation: up to ~10 candidates per Screen in <10 minutes total (dominated by Deep Research API latency)
- Not a high-throughput system (talent use case, not consumer product)

**Latency:**

- **Deep Research (Primary Mode):** 3-6 minutes per candidate (acceptable for v1.0-minimal demo)
- **Incremental Search (Optional):** +30-60 seconds when quality check triggers (up to two web/search calls)
- **Fast Mode:** Phase 2+ optimization (1-2 minutes per candidate using web search fallback)
- **Batch Processing:** 10 candidates in 30-60 minutes (synchronous demo implementation)
- **Target:** <10 seconds for quality check and assessment logic (excluding LLM API calls)

**Memory:**

- <512MB per Flask worker (small dataset, no heavy computation)
- Airtable handles primary data storage
- **Agno SqliteDb (REQUIRED for v1):** Persists workflow session state locally at `tmp/agno_sessions.db` (gitignored) for reviewable run history
  - Agno-managed tables only; no custom schema
  - InMemoryDb() is Phase 2+ fallback option (NOT used in v1)
- **Custom SQLite audit/event stores:** Phase 2+ enhancement only (not in v1.0-minimal)

**Concurrency:**

- Synchronous execution for v1.0-minimal (simpler implementation)
- Single-process, single Flask worker
- Concurrent workers and async/await are Phase 2+ optimizations

### Integration Points

**APIs:**

- OpenAI API (Deep Research, GPT-5-mini, Web Search)
- Airtable API (data read/write via pyairtable)
- Flask webhook server (receive triggers from Airtable automations)

**Agno Framework Features:**

- Native UI dashboard for workflow monitoring and session inspection
- Prompt template system for centralized prompt management
- SqliteDb for session persistence and audit trail
- ReasoningTools for structured reasoning traces

**Databases:**

- Airtable (primary database for all tables)
- Agno `SqliteDb` (stored at `tmp/agno_sessions.db`) for agent session persistence only; no custom workflow-event tables in v1.0-minimal
- No PostgreSQL/MongoDB needed for demo

**Message Queues:**

- Not needed for demo (synchronous execution)
- Phase 2+: Consider Celery/RQ for async background jobs

**External Services:**

- ngrok (local tunnel for webhook testing)
- No cloud deployment for demo (local Flask server)

### Data Requirements

**Input Formats:**

- CSV (guildmember_scrape.csv → People table)
- Markdown (role specifications)
- JSON (Airtable API responses, structured outputs)
- Agno prompt templates (research and assessment agent prompts)

**Output Formats:**

- Markdown (raw Deep Research API responses, assessment reports)
- JSON (AssessmentResult → Airtable)
- Airtable records (primary output destination)
  - Assessments.research_markdown_raw (long text field - v1 stores research in Assessments)
  - Assessments.research_structured_json (long text field - serialized ExecutiveResearchResult)
  - Assessments.assessment_json (long text field - serialized AssessmentResult)
  - Assessments.assessment_markdown_report (long text field - human-readable summary)

**Data Volume:**

- 64 executive records (mock data from guild scrape)
- 4 portfolio company scenarios
- 10-15 assessments per scenario
- ~40-60 total assessment records for demo

**Data Retention:**

- All data persists in Airtable indefinitely
- Raw research markdown + structured JSON stored in Assessments table (v1: no separate Research_Results table)
- Assessment JSON + markdown reports stored in Assessments table
- Terminal logs provide execution audit trail for v1.0-minimal
- No automated cleanup/archival for demo

---

## Technical Constraints

**Note:** For high-level technical stack overview, see "Technical Stack" section in Scope (line 196). This section provides detailed constraints and requirements.

### Python Version

- **Minimum:** Python 3.11+
- **Reason:**
  - Modern type hints (PEP 604, 646)
  - Pattern matching for cleaner code
  - Better error messages for debugging
  - Agno framework compatibility

### Dependencies

**Core (see Technical Stack section for high-level overview):**

- `agno-ai` - Agent framework with workflow orchestration (Agno UI dashboard, prompt templates)
- `pydantic` - Data validation and structured outputs (ExecutiveResearchResult, AssessmentResult)
- `flask` - Webhook server for Airtable integration (production entrypoint)
- `pyairtable` - Airtable API client (database operations)
- `python-dotenv` - Environment variable management

**Dev/Test:**

- `pytest` - Testing framework
- `pytest-cov` - Coverage reporting (basic tests, no strict threshold)
- `ruff` - Formatting and linting
- `mypy` - Type checking (standard mode)

**Optional:**

- `structlog` - Structured logging (Phase 2+, not required for v1.0-minimal)
- `requests` - HTTP client (pyairtable dependency)

### Deployment

**Environment:**

- Local development (Mac/Linux with Python 3.11+)
- Flask server on localhost:5000
- Agno UI dashboard (accessible via browser for workflow monitoring)
- ngrok tunnel for Airtable webhook connectivity
- No Docker/cloud deployment for demo

**Configuration:**

- Environment variables via `.env` file
- API keys: OpenAI, Airtable
- Feature flags: USE_DEEP_RESEARCH (default: true)
- Quality gate thresholds (MIN_EXPERIENCES, MIN_CITATIONS, etc.)

**Monitoring:**

- **Agno UI Dashboard** (primary) - Real-time workflow monitoring, session inspection, reasoning traces
- Terminal logs (stdout) for execution visibility
- Airtable status fields for workflow state (Status, error message)
- Agno SqliteDb session persistence for audit trail
- No custom SQLite event storage for v1.0-minimal (Phase 2+ enhancement)
- No production monitoring/alerting for demo

---

## Risks & Assumptions

### Risks

1. **Risk:** OpenAI Deep Research API rate limits or downtime during demo
   **Likelihood:** Low-Medium
   **Impact:** High (breaks primary demo flow)
   **Mitigation:**
   - Pre-run 3 of 4 scenarios before demo
   - Test thoroughly day before presentation
   - Have incremental search as fallback if needed

2. **Risk:** Quality gate triggers excessive supplemental searches (time overrun)
   **Likelihood:** Medium
   **Impact:** Medium (demo feels slow)
   **Mitigation:**
   - Tune quality gate thresholds based on test runs
   - Limit to single incremental search pass (up to two web/search calls)
   - Skip incremental search in live demo if time-constrained

3. **Risk:** Evidence-aware scoring produces too many Unknown dimensions
   **Likelihood:** Medium
   **Impact:** Low-Medium (reduces ranking confidence)
   **Mitigation:**
   - Design role specs with High evidence dimensions weighted heavily
   - Incremental search specifically targets scorable dimensions
   - Explain Unknown scores as feature, not bug (transparency)

4. **Risk:** Airtable webhook reliability issues during live demo
   **Likelihood:** Low
   **Impact:** High (breaks live execution)
   **Mitigation:**
   - Pre-run 3 scenarios with results ready
   - Test webhook connectivity multiple times before demo
   - Have backup plan to trigger via curl/Postman

5. **Risk:** 48-hour timeline insufficient for complete implementation
   **Likelihood:** Medium
   **Impact:** High (incomplete demo)
   **Mitigation:**
   - Strict scope discipline (v1.0-minimal only)
   - Pre-populate Airtable data manually
   - Focus dev time on Module 4 (core screening)
   - Skip Modules 1-3 automation if needed

6. **Risk:** Learning curve for Agno UI and prompt template system delays implementation
   **Likelihood:** Low-Medium
   **Impact:** Medium (slower development, less demo polish)
   **Mitigation:**
   - Leverage Agno documentation and examples
   - Start with simple prompt templates, iterate during testing
   - Use basic UI features first, advanced features in Phase 2+
   - Terminal logs as backup monitoring if UI setup delayed

### Assumptions

1. **Mock data quality:** guildmember_scrape.csv provides sufficient diversity for demo
2. **Network connectivity:** Stable internet for OpenAI API calls and Airtable sync
3. **Execution time:** LLM API latency matches documented estimates (2-5 min deep research)
4. **Role spec design:** CFO/CTO templates cover 80% of use cases
5. **Airtable limits:** Free/Plus tier sufficient for demo data volume
6. **Python environment:** uv package manager works reliably on Mac/Linux
7. **Audience technical literacy:** Can follow agent workflow concepts and structured outputs
8. **Evaluation criteria:** Case rubric accurately reflects FirstMark's priorities
9. **Agno UI reliability:** Agno's native UI dashboard works reliably for local development workflows
10. **Prompt template flexibility:** Agno's template system supports rapid iteration without code redeployment

---

## Timeline

### Phase 1: Planning & Setup (Hours 1-8) ✅ COMPLETE

- ✅ Define requirements and solution strategy
- ✅ Design data models and Airtable schema
- ✅ Create role specification framework
- ✅ Plan screening workflow architecture
- ✅ Write technical specification
- ✅ Set up Python environment and dependencies
- ✅ Configure Agno UI dashboard and prompt template system

### Phase 2: Core Implementation (Hours 9-24)

**Data Layer (2 hours):**

- Create Airtable database with 7 tables (6 core + 1 helper)
- Populate portco data (Pigment, Mockingbird, Synthesia, Estuary)
- Load people records from guildmember_scrape.csv
- Create role spec templates (CFO, CTO)

**Agent Implementation (6 hours):**

- Implement ExecutiveResearchResult and AssessmentResult Pydantic models
- Create Agno prompt templates for research and assessment agents
- Build deep research agent (o4-mini-deep-research + structured outputs + templates)
- Build assessment agent (gpt-5-mini with structured outputs + templates)
- Implement quality check and optional incremental search logic
- Build research merging function
- Test agents via Agno UI dashboard for debugging

**Workflow Implementation (4 hours):**

- Assemble Agno workflow (linear: deep research → quality check → optional incremental search → assessment)
- Implement custom step functions (quality check, merge, coordination)
- Add event streaming for logging (stdout + Agno UI monitoring)
- Test workflow end-to-end with mock data
- Validate Agno UI dashboard displays workflow execution correctly

**Flask Integration (4 hours):**

- Build /screen endpoint (single webhook)
- Implement Airtable read/write functions
- Add status field updates and error handling
- Set up ngrok tunnel and test webhook triggers

**AgentOS Prototype (2 hours):**

- Build AgentOS/FastAPI entrypoint (demo/agentos_app.py)
- Extract shared workflow orchestration (demo/screening_service.py)
- Validate dual runtime architecture (Flask + AgentOS)
- Document migration roadmap (docs/agent_os_integration_spec.md)

### Phase 3: Testing & Pre-Run Scenarios (Hours 27-34)

**Testing (4 hours):**

- Basic tests for core scoring logic (calculate_overall_score)
- Unit tests for quality check logic
- Happy-path workflow smoke test with mocks (if time permits)
- Validate structured output schemas

**Pre-Run Scenarios (4 hours):**

- Execute Pigment CFO screening (3-5 candidates)
- Execute Mockingbird CFO screening (3-5 candidates)
- Execute Synthesia CTO screening (3-5 candidates)
- Generate markdown reports for all pre-run results

### Phase 4: Documentation & Demo Prep (Hours 35-42)

**Documentation (4 hours):**

- Write implementation README with architecture diagram
- Document design decisions and tradeoffs (including AgentOS migration path)
- Create demo script with talking points
- Prepare markdown exports of sample assessments

**Demo Rehearsal (4 hours):**

- Practice full demo flow (Modules 1-4)
- Test live execution of Estuary CTO screening
- Rehearse Agno UI dashboard walkthrough (workflow monitoring, session inspection)
- Demonstrate AgentOS control plane features (optional)
- Demonstrate prompt template iteration capabilities
- Prepare backup plans for common failures
- Refine presentation narrative

### Phase 5: Presentation & Buffer (Hours 43-50)

**Presentation Creation (4 hours):**

- Create slide deck or written deliverable
- Highlight product thinking and technical decisions
- Prepare production roadmap discussion
- Polish visualizations and examples

**Final Review & Buffer (4 hours):**

- Final testing and bug fixes
- Review against case rubric
- Practice presentation delivery
- Reserve time for unexpected issues

---

## Acceptance Criteria (Project-Level)

### Functional

**AC-PRD-01: Data Upload**

- ✅ CSV upload via Airtable webhook
- ✅ People records created with proper field mapping
- ✅ Deduplication prevents duplicate records

**AC-PRD-02: Role & Search Creation**

- ✅ Can create role records via Airtable UI
- ✅ Can link role specs to roles
- ✅ Can create search records linking to roles

**AC-PRD-03: Candidate Screening**

- ✅ Webhook triggers Flask /screen endpoint
- ✅ Deep research executes and returns ExecutiveResearchResult
- ✅ Quality gate correctly evaluates research sufficiency
- ✅ Optional incremental search triggers when quality check flags missing evidence (up to two web/search calls)
- ✅ Assessment produces dimension scores, overall score, reasoning
- ✅ Results written to Airtable with status updates and key summary fields
- ✅ Raw Deep Research markdown and assessment markdown reports stored in Airtable long text fields

**AC-PRD-04: Assessment Quality**

- ✅ Dimension scores use 1-5 scale with None for Unknown
- ✅ Overall score calculated in Python (0-100 scale, simple average of scored dimensions)
- ✅ Evidence quotes and citations captured
- ✅ Counterfactuals and confidence levels provided
- ✅ Reasoning is clear and evidence-based
- ✅ Assessment agent uses Agno ReasoningTools to generate explicit reasoning trails

**AC-PRD-04b: Agno UI & Prompt Management**

- ✅ Agno UI dashboard accessible and displays workflow execution in real-time
- ✅ Can inspect session state, agent inputs/outputs, and reasoning via UI
- ✅ Prompt templates stored in Agno's native template system (not hardcoded)
- ✅ Research and assessment agents use templated prompts
- ✅ Can iterate on prompts without code changes (template edits only)

### Non-Functional

**AC-PRD-05: Performance**

- ✅ Deep research completes in 2-6 minutes per candidate
- ✅ Quality check executes in <1 second
- ✅ Incremental search (when triggered) adds 30-60 seconds
- ✅ Full workflow (research + assessment) completes in <10 minutes per candidate
- ✅ Synchronous, single-process execution is sufficient for v1.0-minimal

**AC-PRD-06: Code Quality**

- ✅ All public functions have type hints
- ✅ Core matching and scoring logic is covered by smoke tests
- ✅ Type hints are present on public functions
- ✅ Code is reasonably linted/typed (ruff, mypy goals, not hard gates)
- ✅ No strict coverage threshold required for 48-hour demo

**AC-PRD-07: Reliability**

- ✅ Agent retry logic handles transient API errors (basic exponential backoff)
- ✅ Failed workflows marked in Airtable with error messages
- ✅ Minimal audit trail via:
  - Status and summary fields in Airtable
  - Terminal logs during execution
- ✅ Ngrok tunnel remains stable during demo

### Documentation

**AC-PRD-08: Implementation Docs**

- ✅ README explains architecture and design decisions
- ✅ All Pydantic models have docstrings
- ✅ Custom workflow functions have inline comments
- ✅ Demo script with talking points

**AC-PRD-09: Deliverables**

- ✅ Working prototype demonstrating Module 4 workflow
- ✅ Markdown reports for pre-run scenarios
- ✅ Slide deck or written deliverable (1-2 pages)
- ✅ Loom video or live demo walkthrough

**AC-PRD-10: Case Rubric Alignment**

- ✅ Demonstrates understanding of VC talent workflows (Product Thinking)
- ✅ Uses modern agent framework with modular design (Technical Design)
- ✅ Integrates structured + unstructured data (Data Integration)
- ✅ Produces explainable, ranked outputs with reasoning (Insight Generation)
- ✅ Clear communication of approach and tradeoffs (Communication)

---

## Validation & Next Steps

### Demo Validation Checklist

**Pre-Demo:**

- [ ] All 3 pre-run scenarios completed with results in Airtable
- [ ] Flask server + ngrok tunnel tested and stable
- [ ] Agno UI dashboard accessible and displaying session history
- [ ] Prompt templates validated and ready for demo
- [ ] Estuary CTO scenario ready for live execution (candidates loaded, spec attached)
- [ ] Demo script rehearsed with timing estimates

**During Demo:**

- [ ] Show Airtable UI (People, Roles, Searches, Screens tables)
- [ ] Explain role spec framework (CFO/CTO templates)
- [ ] Demo Agno UI dashboard (workflow visualization, session inspection)
- [ ] Show prompt templates and explain centralized management approach
- [ ] Walk through pre-run results (dimension scores, reasoning, rankings)
- [ ] Trigger live screening for Estuary CTO (2-3 candidates)
- [ ] Monitor execution in real-time via Agno UI dashboard
- [ ] Show terminal logs and Airtable status updates
- [ ] Export markdown report and discuss

**Post-Demo:**

- [ ] Gather feedback on match quality and reasoning clarity
- [ ] Document lessons learned and implementation surprises
- [ ] Identify highest-value Phase 2 enhancements

### Next Steps (Phase 2+)

**Immediate Priorities:**

1. **AgentOS Migration:** Replace Flask runtime with AgentOS (FastAPI) for production deployment
   - Enable control plane UI for stakeholder demos
   - Configure bearer token authentication
   - Deploy via Docker Compose or AWS ECS templates
   - Migrate Sqlite → Postgres for production durability
2. Fast Mode fallback (web search for quicker screening)
3. Multi-iteration supplemental search with adaptive quality thresholds
4. Async processing for faster batch screening (leverages AgentOS orchestration)
5. Research caching to avoid redundant API calls
6. Enhanced error handling and observability (via AgentOS metrics/eval endpoints)

**Medium-Term Enhancements:**

1. Vector stores for semantic candidate search
2. Model-generated rubric evaluation (alternative assessment)
3. Integration with portfolio company ATS systems
4. Historical search analytics and outcome tracking
5. Advanced Agno UI customization (custom dashboards, alerts)
6. A/B testing framework for prompt template optimization
7. Prompt versioning and rollback capabilities

**Long-Term Vision:**

1. Proactive candidate recommendations
2. Network growth suggestions (identify gaps)
3. Multi-tenant support (other VC firms)
4. Outcome learning (which matches led to hires)

---

## Success Definition

This PRD succeeds if:

1. ✅ **Prototype demonstrates clear thinking:** Design decisions show understanding of talent workflows and stakeholder needs
2. ✅ **Code quality signals professionalism:** Type-safe, tested, well-documented Python code with modular architecture
3. ✅ **Demo execution is smooth:** Live screening completes without errors, results are impressive
4. ✅ **Reasoning is compelling:** Assessment outputs feel useful and trustworthy
5. ✅ **Presentation is clear:** Can explain approach, tradeoffs, and next steps in 30 minutes
6. ✅ **Evaluation criteria met:** Scores well across all 5 case rubric dimensions
7. ✅ **Technical sophistication:** Agno UI and prompt templates demonstrate modern agent development practices
8. ✅ **Rapid iteration capability:** Prompt template system enables fast experimentation and refinement

**Remember:** The goal is demonstrating quality of thinking through minimal, working code—not building production infrastructure. Agno's native UI and templates showcase modern best practices without heavy custom engineering.

**Approval:**

- Created: 2025-01-16
- Updated: 2025-01-17 (v1.0-minimal scope alignment)
- Updated: 2025-11-17 (Added Agno UI dashboard and centralized prompt templates to v1.0-minimal scope)
- Status: Approved for v1.0-minimal implementation
- Next Review: Post-demo retrospective
