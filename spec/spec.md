---
version: "1.0-minimal"
created: "2025-01-16"
updated: "2025-11-19"
project: "Talent Signal Agent"
context: "FirstMark Capital AI Lead Case Study"
implementation_status: "Stages 1-6 Complete (28-30h), Post-Presentation Cleanup Complete"
---

# Technical Specification: Talent Signal Agent (v1.0-Minimal)

Engineering contract for Python implementation of AI-powered executive matching system

## Current Implementation Status (2025-11-19)

**Stage 1 (Airtable Foundation): ✅ COMPLETE**
- 8 tables configured (6 core + 1 helper + 1 audit bonus)
- Base ID: appeY64iIwU5CEna7
- ~63 executives loaded (TK-20 verified 2025-11-19, sufficient for demo)
- 4 portfolio companies loaded (Pigment, Mockingbird, Synthesia, Estuary)
- Role spec design template complete (601 lines)
- Schema 95% aligned with spec (minor cosmetic deviations documented below)
- Data loading tools production-ready (airtable-csv-loader, airtable-schema-validator)

**Stage 2 (Agent Implementation): ✅ COMPLETE**
- ✅ demo/models.py - All Pydantic models implemented
- ✅ demo/prompts/catalog.yaml + library.py - Centralized YAML prompt catalog with loader
- ✅ demo/agents.py - Research, Assessment, Incremental Search agents consume catalog templates
- ✅ tests/test_prompts.py - Loader regression protection
- ✅ tests/test_scoring.py - 7 test cases with fixtures (all passing)
- ✅ tests/test_quality_check.py - 9 test cases with fixtures (all passing)
- ✅ tests/test_research_agent.py - 21 test cases (all passing)
- ✅ 58 total tests passing (Stage 2 baseline), 76% coverage (exceeds 50% constitution target)
- ✅ Type hints and docstrings on all public functions

**Stage 3 (Workflow Orchestration): ✅ COMPLETE**
- ✅ Linear workflow with 4-step pipeline (Deep Research → Quality Check → Incremental Search → Assessment)
- ✅ SqliteDb session state management at tmp/agno_sessions.db
- ✅ AgentOS Dashboard - Real-time workflow monitoring and session inspection validated
- ✅ AgentOSCandidateWorkflow class in demo/workflow.py (canonical workflow)
- ✅ Event streaming with emoji indicators (🔍, ✅, ❌, 🔄) + UI visualization
- ✅ Quality gate triggering conditional incremental search
- ✅ tests/test_agentos_workflow_mocked.py - Workflow step coverage with AgentOS session state
- ✅ tests/test_agentos_session_registration.py - Session persistence + API integration coverage
- ✅ 76% coverage (exceeds 50% constitution target)
- ✅ Workflow architecture + AgentOS usage documented in README.md

**Stage 4 (Webhook Integration): ✅ COMPLETE**
- ✅ AirtableClient simplified to write-only operations (status + assessments + automation log) (`demo/airtable_client.py`)
- ✅ Structured `ScreenWebhookPayload` + `process_screen_direct()` path (no Airtable reads during screening) (`demo/models.py`, `demo/agentos_app.py`, `demo/screening_service.py`)
- ✅ AgentOS FastAPI runtime with POST `/screen` endpoint (`demo/agentos_app.py`)
- ✅ tests/test_airtable_client.py - 37 tests, 100% coverage (all passing)
- ✅ tests/test_agentos_app.py - FastAPI endpoint tests (all passing)
- ✅ Comprehensive README documentation with ngrok setup

**Stage 4.5 (Prompt Templating & AgentOS Runtime): ✅ COMPLETE**
- ✅ **Centralized Prompt Catalog** (`demo/prompts/catalog.yaml`)
  - Canonical YAML prompt definitions for all 4 agents (deep_research, research_parser, incremental_search, assessment)
  - Structured prompt contexts: `description`, `instructions`, `expected_output`, `additional_context`
  - Version-controlled prompts (no hardcoded Python strings)
  - Deep Research template encodes evidence taxonomy ([FACT]/[OBSERVATION]/[HYPOTHESIS]), structured sections, and explicit "Gaps in Public Evidence"
  - Parser template respects the taxonomy and maps Deep Research markdown into `ExecutiveResearchResult` (FACT → structured fields, OBS/HYP → narrative + gaps)
  - Incremental search template targets specific gaps and low-confidence areas with at most two web searches
  - Assessment template codifies 1–5 scale semantics, investor/board-lens headline summaries, board-ready red/green flags, and counterfactuals as concrete follow-up questions
- ✅ **Prompt Library** (`demo/prompts/library.py` + `__init__.py`)
  - `get_prompt(name, **placeholders)` loader returning `PromptContext` dataclass
  - `PromptContext.as_agent_kwargs()` for direct Agno Agent integration
  - Placeholder support via Python `str.format` syntax
- ✅ **Agent Integration** (`demo/agents.py`)
  - All agent factories now use `get_prompt()` for prompt loading
  - Temporal awareness with `add_datetime_to_context=True` on research/assessment agents
  - Context engineering aligned with Agno best practices
- ✅ **Prompt Tests** (`tests/test_prompts.py`)
  - Catalog validation and regression protection
  - Missing key error handling verification
- ✅ **AgentOS Runtime** (`demo/agentos_app.py`)
  - FastAPI entrypoint now canonical `/screen` implementation
  - Control plane UI validated + `/docs` contract codified in spec
  - Shared workflow orchestration via `demo/screening_service.py`
  - README/runbooks updated to use AgentOS + ngrok
  - FastAPI-specific regression tests (`tests/test_agentos_app.py`)
  - `/screen` now delegates each candidate to the multi-step AgentOS workflow so runs/logs appear in the control plane
  - **Canonical Workflow**: `AgentOSCandidateWorkflow.run_candidate_workflow()` in `demo/workflow.py` is the primary execution path with step executors and proper AgentOS session tracking
- ✅ **Outstanding Cutover Tasks**
  - ✅ Ensure all Airtable automations/scripts use the AgentOS URL + optional bearer auth (helper scripts + runbooks now reference AgentOS; confirm Airtable automations next)
- 📋 Reference: `docs/agent_os_integration_spec.md` (migration plan + deployment checklist)
- 📋 Reference: `docs/prompt_system_summary.md`

**Stage 4.7 (Airtable Payload Simplification): ✅ COMPLETE** (1.5 hours)

**Scope:** Refactor webhook payload handling to eliminate sequential API traversal and JSON string parsing.

**Completed (Phases 2-4 per spec/adhoc/airtable_refactor_proposal_v-r.md):**
- ✅ **Structured Payload Model** - Created `ScreenWebhookPayload` with nested objects (`ScreenSlugData`, `RoleSpecSlug`, `SearchSlug`, `CandidateSlug`)
  - Direct Pydantic validation (no JSON string parsing)
  - `get_candidates()` helper returns standardized array format
  - Removed ~100 lines of JSON parsing logic from models.py (62% reduction)
- ✅ **Write-Only Airtable Client** - Simplified `airtable_client.py` to write-only operations
  - Removed traversal methods: `get_screen()`, `get_role_spec()`, `get_search()`, `get_role()`
  - Reduced from ~400 to ~235 lines (41% reduction)
  - Zero Airtable API reads during workflow execution
- ✅ **Webhook Handler Refactor** - Updated `POST /screen` endpoint and workflow orchestration
  - Accepts `ScreenWebhookPayload` (pre-assembled structured data)
  - Created `process_screen_direct()` function in `screening_service.py`
  - Eliminated 4+ sequential API calls per screen

**Technical Benefits:**
- **Zero Airtable API traversal** during workflow execution (100% elimination of read operations)
- **100% JSON parsing elimination** - Direct Pydantic validation of nested objects
- **~500ms latency reduction** per screen (no sequential API call overhead)
- **Improved reliability** - Payload structure validated immediately at endpoint
- **Easier testing** - Mock single payload instead of multi-step Airtable chain
- **Airtable-First pattern** - Complexity pushed to declarative formulas, Python kept minimal

**Files Modified:**
- `demo/models.py` - Payload model refactoring (62% parsing logic reduction)
- `demo/airtable_client.py` - Removed read-only table traversal (~165 lines removed)
- `demo/agentos_app.py` - Updated endpoint to use structured payload
- `demo/screening_service.py` - New `process_screen_direct()` function
- `tests/test_models_validation.py` - Updated model tests
- `tests/test_agentos_app.py` - Updated webhook tests

**Pending (Phases 5-6 per spec/adhoc/airtable_refactor_proposal_v-r.md):**
- [ ] **Phase 5:** Integration testing with real Airtable webhook (~20-30 min)
- [ ] **Phase 6:** Remove backward compatibility (optional cleanup, ~10-15 min)

**References:**
- 📋 Complete design + status: `spec/adhoc/airtable_refactor_proposal_v-r.md`
- 📋 Payload model: `demo/models.py` (ScreenWebhookPayload class)
- 📋 Simplified client: `demo/airtable_client.py` (write-only operations)

**Stage 5 (Integration Testing & Observability): ✅ COMPLETE** (25.6h)

**Completed Tasks (2025-01-18 through 2025-01-19):**
- ✅ TK-00: Critical bug fixes (FastAPI return type, session persistence, None handling, quality check citations)
- ✅ TK-01: Test suite validation (109 passed, 20 skipped, 76% coverage)
- ✅ TK-02: Infrastructure setup (AgentOS on port 5001, ngrok tunnel configured)
- ✅ TK-03: Airtable automation (async endpoint with BackgroundTasks, eliminated timeouts)
- ✅ TK-04: Test data preparation (Screen recBWjkAZDCFrW25q with 3 candidates)
- ✅ TK-05: Full webhook dry run on live Airtable payload ✅ Completed 2025-11-18
- ✅ TK-06: Airtable write verification (assessment JSON blobs, score ranges, citation counts) ✅ Completed 2025-11-18
- ✅ TK-07: AgentOS control plane review ✅ Completed 2025-01-19
- ✅ TK-08: Airtable payload integration (verified zero-traversal pattern)
- ✅ TK-11: Mypy type safety (fixed 33 strict errors, `mypy demo --strict` passing)
- ✅ TK-12: Failure status bug (fixed `_mark_screen_failed()` to write "Failed")
- ✅ TK-13: Custom instructions flow (threaded through workflow chain)
- ✅ TK-14: USE_DEEP_RESEARCH wiring (environment variable control)
- ✅ TK-16/17: Code quality improvements (model reconstruction, inline helpers) ✅ Completed 2025-01-19
- ✅ TK-20/21: Module 1 skills (validation + two focused skills) ✅ Completed 2025-01-19

**Pending Tasks (Optional):**
- [ ] TK-09, TK-10: Negative-path drills and log quality pass (optional)

**Stage 5.7 (Documentation Review): ⏸️ PENDING** (1.5-3 hours)
- Update mkdocs navigation, rewrite architecture.md, expand user-facing docs
- See `spec/dev_plan_and_checklist.md` lines 173-271 for detailed task breakdown

**Stage 5.8 (Markdown Reports): ⏸️ PENDING** (3 hours, optional)
- Add markdown formatters, wire into workflow, update Airtable client
- See `spec/dev_plan_and_checklist.md` lines 274-371 for detailed task breakdown

**Stage 6 (Demo Prep - Minimal Viable Path): ✅ COMPLETE** (Nov 19, 2025)

**Scope Adjustment (2025-01-19):** Retargeted to minimal viable demo due to presentation deadline constraints.

**Completed:**
- ✅ Manual scenario setup - Created scenarios via Airtable UI
- ✅ Execute quality pre-runs - 15+ candidate screenings executed (Pigment CFO, Mockingbird CFO searches)
- ✅ Finalize presentation deck - PowerPoint deck delivered (FMV_V1.1.pptx)
- ✅ Quick rehearsal - Practice flow completed
- ✅ Environment validation - AgentOS, ngrok, webhook automation verified

**Post-Presentation Status:**
- ✅ Codebase cleanup complete (Nov 19, 2025)
- ✅ All tests passing (109 passed, 20 skipped, 76% coverage)
- ✅ Security review complete
- ✅ Documentation reviewed and professional
- ⏸️ Stage 5.7: Documentation review (optional, 1.5-3h)
- ⏸️ Stage 5.8: Markdown reports (optional, 3h)

**Detailed Tracking:** See `spec/dev_plan_and_checklist.md` for task-level progress

See "Implementation Roadmap" section for detailed breakdown. AgentOS integration complete (see `docs/agent_os_integration_spec.md`).

## Architecture

### System Overview

The Talent Signal Agent is a demo-quality Python application that uses AI agents to research and evaluate executive candidates against role specifications. The system integrates with Airtable for data storage and UI, uses OpenAI's Deep Research API for candidate research, and employs structured LLM outputs for evidence-aware assessments.

**Key Design Principles:**

- **Evidence-Aware Scoring:** Explicit handling of "Unknown" when public data is insufficient (using `None`/`null`, not 0 or NaN)
- **Quality-Gated Research:** Optional single incremental search agent step when initial research has quality issues
- **Agno-Managed Observability:** AgentOS dashboard for workflow monitoring; no custom event DB for v1
- **Deep Research Primary:** v1 uses o4-mini-deep-research as default; fast mode is Phase 2+
- **Airtable-First Data Packaging:** Airtable automation posts a structured `ScreenWebhookPayload` (role spec + search + candidate objects) so Python never performs read traversals during screening.

### Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      AIRTABLE DATABASE                       │
│  People (64) | Portco (4) | Portco_Roles (4) | Role_Specs (6)│
│  Searches (4) | Screens (4) | Assessments (research+scores)│
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ Automation Trigger (Status Change)
                     ▼
            ┌─────────────────┐
            │  NGROK TUNNEL    │ (Demo Only)
            └────────┬─────────┘
                     │
                     ▼
         ┌──────────────────────┐
            │   AGENTOS WEBHOOK    │  (:5001)
         │   SERVER             │
         └────────┬─────────────┘
                  │
                  ▼
    ┌─────────────────────────────┐
    │  AGNO WORKFLOW ORCHESTRATOR  │
    │                              │
    │  Step 1: Deep Research Agent │
    │    └─ o4-mini-deep-research  │
    │                              │
    │  Step 2: Quality Check       │
    │    └─ Simple sufficiency     │
    │                              │
    │  Step 3: Conditional Branch  │
    │    ├─ Incremental Search     │
    │    │   (optional, single)    │
    │    └─ Merge Research         │
    │                              │
    │  Step 4: Assessment Agent    │
    │    └─ gpt-5-mini + spec      │
    └────────┬────────────────────┘
             │
             │ Write Results
             ▼
    ┌────────────────────┐
    │  AIRTABLE API      │
    │  (pyairtable)      │
    │                    │
    │  - Research        │
    │  - Assessments     │
    │  - Status fields   │
    └────────────────────┘

    ┌────────────────────┐
    │  OPENAI APIS       │
    │                    │
    │  - Deep Research   │
    │  - GPT-5-mini      │
    │  - Web Search      │
    └────────────────────┘
```

### Technology Stack

- **Language:** Python 3.11+
- **Framework:** FastAPI + AgentOS (canonical webhook server), Agno (agent orchestration + UI dashboard)
- **LLM Provider:** OpenAI (o4-mini-deep-research, gpt-5-mini)
- **Database:** Airtable (primary storage), Agno SqliteDb for session state (tmp/agno_sessions.db, no custom event tables)
- **Validation:** Pydantic (structured outputs)
- **Package Manager:** UV
- **Tunnel:** ngrok (local demo)
- **UI/Monitoring:** Agno built-in UI dashboard (browser-accessible), AgentOS control plane (prototype)
- **Prompt Management:** YAML prompt catalog (`demo/prompts/catalog.yaml`) + loader (`demo/prompts/library.py`)

### Project Structure

**v1.0-Minimal Layout (core modules + prompt catalog):**

```
demo/
├── agentos_app.py       # AgentOS/FastAPI entrypoint (canonical runtime, 255 lines)
├── workflow.py          # AgentOSCandidateWorkflow class (374 lines)
├── screening_helpers.py # Business logic helpers (176 lines)
├── screening_service.py # Shared workflow orchestration logic (332 lines)
├── agents.py            # Research + assessment agent creation + runners (865 lines)
├── models.py            # Pydantic models (research + assessment, 298 lines)
├── airtable_client.py   # Thin Airtable wrapper (238 lines)
├── settings.py          # Config/env loading (optional)
└── prompts/
    ├── catalog.yaml     # Canonical prompt definitions (YAML)
    └── library.py       # Loader that materializes PromptContext objects

tmp/
└── agno_sessions.db    # Agno workflow session state (gitignored, SqliteDb only)

tests/
├── test_scoring.py         # calculate_overall_score tests
├── test_quality_check.py   # quality check heuristics
├── test_prompts.py         # prompt catalog loader tests
├── test_agentos_workflow_mocked.py  # AgentOS workflow orchestration tests
└── test_agentos_session_registration.py  # session persistence + API hooks

spec/                   # Documentation
├── constitution.md     # Project governance
├── prd.md              # Product requirements
├── spec.md             # This file (canonical technical contract)
└── dev_reference/      # Implementation guides (non-canonical)

docs/                   # Integration specifications
└── agent_os_integration_spec.md  # AgentOS migration roadmap

.python-version         # Python 3.11
pyproject.toml          # Dependencies
.env.example            # Environment variables template
README.md               # Implementation guide
```

**Phase 2+ Enhancements:**

**Core Functionality:**
- Fast Mode (web search fallback optimization for quicker screening)
- Multi-iteration supplemental search loops (adaptive quality thresholds)
- Research result caching (reduce API costs)
- Parser agent optimization (using Agno native structured outputs)
- Further decomposition into subpackages (`agents/`, `models/`, `workflows/`)
- Async/concurrent candidate processing (5-10x throughput)

**Observability & Operations:**
- SQLite event DB, event replay, custom Agno dashboards
- Structured logging (structlog)
- Advanced AgentOS features (custom dashboards)

**Advanced Features:**
- Rate limiting, retry logic beyond basic exponential backoff
- Alternative evaluation path (model-generated dimensions)
- Advanced deduplication (fuzzy matching)
- External API integrations beyond OpenAI (e.g., Apollo API enrichment)
- Weighted scoring algorithm (sophisticated matching beyond simple average)


### v1.0-Minimal Scope Contract

**What v1 INCLUDES:**
- ✅ Single AgentOS endpoint (`POST /screen`)
- ✅ Deep Research API (o4-mini-deep-research) as primary research mode
- ✅ Optional single incremental search step (max 2 web/search calls) when quality is low
- ✅ Spec-guided assessment with evidence-aware scoring (None for Unknown)
- ✅ Agno workflow with SqliteDb at tmp/agno_sessions.db (session state only)
- ✅ **AgentOS Dashboard** for real-time workflow monitoring and session inspection
- ✅ **Centralized Prompt Templates** (`demo/prompts/catalog.yaml` + loader)
- ✅ ReasoningTools enabled for all assessment agents
- ✅ Airtable-only storage (research + assessment data in Assessments table)
- ✅ Terminal logs + Airtable status fields + AgentOS (comprehensive observability)
- ✅ Synchronous, sequential processing (one candidate at a time)

**What v1 EXCLUDES (Phase 2+):**
- ❌ Fast Mode (web search fallback optimization)
- ❌ Multi-iteration supplemental search loops
- ❌ Weighted scoring algorithm (v1 uses simple average)
- ❌ Research result caching
- ❌ Custom SQLite WorkflowEvent tables or audit database
- ❌ Separate Research_Results or Workflows tables in Airtable
- ❌ Concurrent workers or async processing
- ❌ Parser agent optimization (using Agno native structured outputs)
- ❌ Production deployment (Docker, cloud hosting, monitoring)
- ❌ Postgres migration (v1 uses SqliteDb only)
- ❌ CLI interface (webhook is primary)
- ❌ Agno Teams, memory persistence, or multi-agent coordination
- ❌ Custom error hierarchy and recovery strategies
- ❌ Event replay and custom dashboards
- ❌ Structured logging (structlog)
- ❌ CI/CD pipeline
- ❌ Vector stores for semantic search
- ❌ Alternative evaluation paths (model-generated dimensions)
- ❌ Advanced deduplication (fuzzy matching)
- ❌ Multi-tenant support
- ❌ External API integrations beyond OpenAI
- ❌ Production authentication/authorization
- ❌ Candidate profile standardization

**Critical Design Decisions:**
- Simple average scoring (no weighted algorithm in v1)
- Parser agent converts Deep Research markdown to structured outputs (Phase 2+ may use native structured outputs)
- All user-facing data in Airtable (7 primary JSON fields in Assessments table: research_structured_json, assessment_json, dimension_scores_json, must_haves_check_json, red_flags_json, green_flags_json, counterfactuals_json - see Airtable Schema Reference section for details)
- SqliteDb required for v1 (InMemoryDb is Phase 2+ fallback only)

### Demo Scope Limitations

**Reduced Single-Select Options:**

To simplify the demo, several single-select fields have reduced option sets compared to the full specification:

- **People.Normalized Title:** CFO, CTO only (full spec defines 8 options: CEO, CPO, CRO, COO, CMO, CFO, CTO, Other)
- **People.Source:** FMGuildPage, FMLinkedIN only (full spec defines 6 sources)
- **Portcos.Stage:** Series B, Series C only (full spec defines 6 stages: Seed, Series A, Series B, Series C, Growth, Public)
- **Portcos.Sector:** B2B SaaS, Infrastructure only (full spec defines 7 sectors)
- **Portco Roles.Role Type:** CFO, CTO only (full spec defines 5 types)
- **Portco Roles.Status:** Open only (full spec defines: Open, On Hold, Filled, Cancelled)
- **Portco Roles.Priority:** Critical, High only (full spec defines: Critical, High, Medium, Low)
- **Searches.Status:** Active, Planning only (full spec defines: Planning, Active, Paused, Completed)
- **Screens.Status:** Demo uses Processing, Complete, Failed (full spec defines: Draft, Processing, Complete, Failed)
- **Assessments.Status:** Demo uses Pending, Complete, Failed (full spec defines: Pending, Processing, Complete, Failed)

**Phase 2+ Enhancement:** Expand single-select options to full specification when supporting broader use cases beyond CFO/CTO demo scenarios.

---

## Core Interfaces

High-level contracts for key system components. **Full signatures:** `spec/dev_reference/implementation_guide.md`

### Research Agent

- `create_research_agent(use_deep_research=True) -> Agent` - Configure o4-mini-deep-research agent
- `run_research(name, title, company, linkedin) -> ExecutiveResearchResult` - Execute research workflow
- **⚠️ Critical:** Deep Research returns markdown (NOT structured output via `output_schema`)
- Citations extracted from `result.citations` (built-in API feature)

### Assessment Agent

- `assess_candidate(research, role_spec, custom_instructions) -> AssessmentResult` - Evaluate candidate against spec
- Uses gpt-5-mini with ReasoningTools and structured outputs
- Returns evidence-aware dimension scores (1-5 scale, None for Unknown)

### Quality Check

- `check_research_quality(research) -> bool` - Evaluate research sufficiency
- Criteria: ≥3 citations + non-empty summary
- Triggers optional incremental search when False

### Score Calculation

- `calculate_overall_score(dimension_scores) -> Optional[float]` - Simple average algorithm
- Filter to scored dimensions → compute average (1-5) → scale to 0-100 (×20)
- Returns None when no dimensions scored

### Airtable Client (Write-Only)

- `write_assessment(screen_id, candidate_id, assessment, research)` - Persist assessment + research to Platform-Assessments
  - **Consolidated JSON storage:** Full `AssessmentResult` → "Assessment JSON", full `ExecutiveResearchResult` → "Research JSON"
  - **Extracted fields:** Overall Score (if not None), Overall Confidence, Topline Summary, Assessment Model, Assessment Timestamp, Research Model
  - **Conditional field:** Research Markdown Report (if `research.research_markdown_raw` exists)
  - **Schema note:** Granular JSON fields (Dimension Scores JSON, Red Flags JSON, Green Flags JSON, Counterfactuals JSON) exist in Airtable but are NOT populated by Python code
- `update_screen_status(screen_id, status, error_message)` - Update Platform-Screens status and optional error message lookup
- `log_automation_event(action, event_type, related_table, record_ids, summary, ...)` - Append to Operations-Automation_Log
- **No read traversals.** Airtable pre-assembles workflow context; Python only writes results/status.

### Webhook Payload

- `ScreenWebhookPayload` (Pydantic) models the structured webhook body with `screen_slug.role_spec_slug.role_spec`, `screen_slug.search_slug.role`, and `screen_slug.candidate_slugs[]`.
- Helper props/methods: `screen_id`, `spec_markdown`, `role_name`, `portco_name`, optional `custom_instructions`, and `get_candidates()` returning normalized dicts consumed by `process_screen_direct()`.
- Airtable automation POSTs this payload directly to `/screen`, enabling the workflow to start without additional Airtable API calls.

---

## Data Models

Pydantic models for structured agent inputs/outputs. **Full definitions:** `spec/dev_reference/implementation_guide.md`

**Key Models:**
- `ExecutiveResearchResult` - Career timeline, expertise, citations (Deep Research returns markdown, must parse)
- `AssessmentResult` - Evidence-aware dimension scores, must-haves, red/green flags, counterfactuals
- `DimensionScore` - 1-5 scale scoring with `Optional[int]` (None for Unknown/Insufficient Evidence)
- Supporting: `Citation`, `CareerEntry`, `MustHaveCheck`

**Critical Pattern:** Use `None` (not 0 or NaN) for insufficient evidence; overall score calculated in Python, not by LLM

**Phase 2+ Only:** Custom `WorkflowEvent` model (v1 uses Agno-managed SqliteDb tables only)

---

## Non-Functional Requirements

**Performance:** <10 min per candidate (Deep Research: 2-6 min, Assessment: 30-60 sec) | <512MB memory | <5 sec Airtable writes

**Scalability (v1):** Synchronous, single worker, ~10 candidates per Screen | **Phase 2+:** Async with multiple workers

**Security:** API keys in `.env` only, Pydantic validation, no secrets in Airtable

**Reliability:** Agno retry (exponential_backoff=True, retries=2), graceful degradation, Airtable status tracking

**Testing:** Core logic tests (scoring, quality, workflow), type hints, ruff format/check | **Phase 2+:** 50%+ coverage, CI/CD

**Deployment:** Local dev (Mac/Linux), AgentOS on localhost:5001, ngrok tunnel, uv package manager

---

## Dependencies

### Core Dependencies

```toml
[project]
name = "talent-signal-agent"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "agno>=2.2.0",              # Agent framework
    "pydantic>=2.5.0",          # Data validation
    "fastapi[standard]>=0.115.0", # FastAPI runtime + AgentOS
    "pyairtable>=2.0.0",        # Airtable API client
    "python-dotenv>=1.0.0",     # Environment variables
    "PyYAML>=6.0",              # Prompt catalog loader
    "uvicorn>=0.30.0",          # FastAPI dev server
]
```

### Development Dependencies

```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",            # Testing framework
    "ruff>=0.1.0",              # Formatting + linting
    "mypy>=1.7.0",              # Type checking (optional)
]
```

**Note:** `structlog` removed from dependencies for v1.0-minimal. Standard Python `logging` is sufficient.

---

## API Specification

**GET /healthz** - Health check endpoint for smoke tests

- **Purpose:** Simple health check endpoint for infrastructure validation
- **Response 200:** `{"status": "ok"}`
- **Implementation:** `demo/agentos_app.py:164-166`

**POST /screen** - Execute candidate screening workflow

- **Trigger:** Airtable automation (Screens.status → "Ready to Screen")
- **Request:** `ScreenWebhookPayload` JSON body with `screen_slug` (includes `screen_id`, `role_spec_slug.role_spec`, `search_slug.role`, and `candidate_slugs[]`). Airtable supplies the complete context—Python performs zero read traversals.
- **Response 200:** `{"status": "success|partial", "candidates_processed": N, "results": [...]}`
- **Response 400/500:** `{"error": "...", "message": "...", "details": {...}}`
- **Implementation:** `demo/agentos_app.py` → `AgentOSCandidateWorkflow.run_candidate_workflow()`

---

## Configuration

**Required Environment Variables:** OPENAI_API_KEY, AIRTABLE_API_KEY, AIRTABLE_BASE_ID, FASTAPI_PORT (default: 5001)

**Optional:** APP_ENV, DEBUG, LOG_LEVEL, USE_DEEP_RESEARCH (true), MIN_CITATIONS (3)

**Files:** `pyproject.toml` (dependencies), `.python-version` (3.11), `.env` (local, gitignored), `.env.example` (template)

**Full Setup:** See README.md

---

## Error Handling

**Agent-Level:** Agno built-in retry (exponential_backoff=True, retries=2, retry_delay=1)

**Workflow-Level:** Basic Python exceptions, update Airtable status to "Failed" with error message

**Graceful Degradation:** Continue processing other candidates if one fails, return partial results

**Phase 2+:** Custom error hierarchy, structured responses, recovery strategies

---

## Observability

**Logging:** Python stdlib (emoji indicators: 🔍 ✅ ❌), `stream_events=True` for stdout + AgentOS

**Metrics:** Terminal output (execution time, quality checks, scores, token usage)

**Audit Trail:** AgentOS Dashboard (primary), Airtable fields (status, errors, assessment/research JSON), terminal logs

**Phase 2+:** SQLite event DB, event replay, custom Agno dashboards, structured logging (structlog)

---

## Agno Framework Requirements

Required features for v1.0-minimal. **Full patterns:** `spec/dev_reference/AGNO_REFERENCE.md`

**Must Use:**
- Structured outputs via `output_schema` (gpt-5-mini only; Deep Research returns markdown)
- Linear Workflow with `stream_events=True`
- SqliteDb at `tmp/agno_sessions.db` for session state (NOT InMemoryDb)
- ReasoningTools on assessment agent (`add_instructions=True`)
- Built-in retry/backoff (`exponential_backoff=True`, `retries=2`)
- OpenAI web_search tools for incremental search
- AgentOS Dashboard (http://localhost:7777)
- Centralized prompt templates (`demo/prompts/catalog.yaml`)

**Do NOT Use:**
- Agno memory / Postgres DB
- Teams or multi-agent coordination
- Large unrelated toolkits (Notion, Slack, etc.)
- Nested workflows or complex state machines
- Custom event persistence (use Agno-managed tables only)

---

## Airtable Schema

8 tables for v1: People, Portcos, Portco Roles, Searches, Screens (webhook trigger), Assessments (stores all results), Role Specs, Audit Logs. **Full schema:** `docs/airtable_ai_spec.md`

**Webhook:** Screens.status → "Ready to Screen" triggers POST `/screen` endpoint

**Storage Pattern:** Complex data in JSON fields (research_structured_json, assessment_json, etc.); extracted fields for viewing (overall_score, confidence, summary)

**Base ID:** appeY64iIwU5CEna7 | **Phase 2+ Excluded:** Workflows, Research_Results tables

---

## Implementation Status

**Current:** Stages 1-6 complete (28-30h) | **Status:** ✅ Presentation Delivered, Codebase Ready for Submission

**Stage Breakdown:**
- ✅ Stages 1-4.7: Complete (19h)
- ✅ Stage 5: Integration Testing & Observability - Complete (25.6h)
- ✅ Stage 6: Demo Prep & Presentation - Complete (Nov 19, 2025)
- 📋 Optional Post-Submission: Stage 5.7 (1.5-3h), Stage 5.8 (3h)

**Total Progress:** ~28-30h invested | **Status:** Complete and ready for submission

**Presentation:** ✅ Delivered Nov 19, 2025 (FMV_V1.1.pptx)

**What's Complete:**
- ✅ Core implementation (all stages 1-6)
- ✅ Test suite (109 passed, 20 skipped, 76% coverage)
- ✅ Comprehensive documentation (4,054+ lines across key docs)
- ✅ Infrastructure (AgentOS, ngrok, webhook automation verified)
- ✅ Data loading tools (production-ready, ~63 executives in Airtable)
- ✅ Demo execution (15+ candidate screenings completed)
- ✅ Presentation deck delivered
- ✅ Codebase cleanup and security review complete

**Detailed Tracking:** See `spec/dev_plan_and_checklist.md` for task-level progress and acceptance criteria

## Success Criteria

This specification succeeds when:

1. **Working Prototype:** Demonstrates end-to-end candidate screening
2. **Evidence-Aware Scoring:** Handles Unknown dimensions with None/null (not 0 or NaN)
3. **Quality-Gated Research:** Optional incremental search triggered when quality is low
4. **Minimal Implementation:** Focused structure with prompt templates, simple algorithms, clear logging
5. **Type Safety:** Type hints on public functions
6. **Tested Core Logic:** Scoring, quality check, workflow orchestration covered
7. **Clear Documentation:** Specification, README, and implementation guide complete
8. **AgentOS Dashboard:** Real-time workflow monitoring and session inspection
9. **Prompt Templates:** Centralized, version-controlled prompts for all agents
10. **Demo Ready:** Pre-run scenarios complete, live demo prepared
11. **Airtable Simplification:** Zero-traversal data flow with structured payloads (100% JSON parsing elimination, 0 API reads during execution)

**Goal:** Demonstrate quality of thinking through minimal, working code—not building production infrastructure.

---


## Document Control

**Related Documents:**

- `spec/constitution.md` - Project governance and principles
- `spec/prd.md` - Product requirements document
- `spec/dev_reference/implementation_guide.md` - Data models and schemas
- `docs/role_spec_design.md` - Role specification framework

**Approval:**

- Created: 2025-01-16
- Updated: 2025-01-17 (v1.0-minimal refactor)
- Updated: 2025-01-17 (Added AgentOS dashboard, centralized prompt templates, and AgentOS prototype to v1.0-minimal scope)
- Updated: 2025-01-19 (Stage 5 progress alignment, added Stages 5.7-5.8 tracking, synchronized with dev_plan_and_checklist.md)
- Updated: 2025-01-19 Evening (Corrected data status, retargeted Stage 6 to minimal demo path - 3-4h to demo ready)
- Updated: 2025-01-19 (Aligned with design.md: fixed port numbers, resolved Stage 5 status contradiction, updated test metrics to 105 passed/20 skipped/75% coverage, added /healthz endpoint documentation)
- Updated: 2025-11-19 (Post-presentation cleanup: updated test metrics to 109 passed/20 skipped/76% coverage, Stage 6 complete, codebase ready for submission)
- Status: Stages 1-6 Complete, Codebase Cleaned and Ready for Submission
- **Presentation:** ✅ Delivered Nov 19, 2025
- Next Review: Post-submission retrospective
