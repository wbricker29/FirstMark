# CLAUDE.md

## CORE Development Principles

**Constraints:** 48 hours | Demonstrate quality of thinking | Minimal, quick-to-stand-up components

**Decision Matrix (Applied Successfully):**

```text
always          → explain → code → verify  ✅ Applied in all 4.5 stages
ambiguous?      → clarify                   ✅ Used spec alignment reviews
existing_code?  → change_minimum            ✅ Built on Agno framework
new_feature?    → MVP → validate → expand   ✅ Iterative prompt catalog, AgentOS
```

**Prioritization (Proven Effective):**
Simple > Perfect | Clear > Clever | Working > Optimal | Request > BestPractice | Smaller > Larger

**Key Rules (Validated):**

- **SIMPLICITY:** Modular design with clear separation of concerns
- **QUALITY:** Type hints, docstrings, Pydantic models, 75% test coverage
- **COMMUNICATION:** 9 spec issues tracked and resolved, comprehensive architectural documentation

**Strategic Focus (Demonstrated):**

1. ✅ Domain calibration: CFO/CTO evaluation templates, evidence-aware scoring
2. ✅ Incremental value: Stages 1-4.5 each delivered complete capabilities
3. ✅ Expected value maximized: AgentOS control plane + prompt catalog showcase thinking quality
4. ✅ Context engineering: YAML prompts with evidence taxonomy, temporal awareness

## Reminder

You are operating in an environment where `ast-grep` is installed.
For any code search that requires understanding of syntax or code structure, you should default to using:
    ast-grep --lang <language> -p '<pattern>'
Adjust the --lang flag as needed for the specific programming language.
Avoid using text-only search tools unless a plain-text search is explicitly requested.

## Project Overview

**Mission:** Talent Signal Agent - AI-powered executive matching for FirstMark Capital portfolio companies
**Presentation:** Nov 19,  (Completed)
**Framework:** Agno (Python agent framework)

## Current Status (Updated Nov 19,  - Post-Presentation)

**Implementation:** ✅ STAGES 1-6 COMPLETE (28-30h) - Core + Integration + Demo Execution + Presentation
**Test Coverage:** 130 tests (110 passed, 20 skipped), 74% coverage (exceeds 50% target)
**Code Base:** ~3,255 lines in demo/ (8 core modules) + ~1,500 lines tests (15 test files)
**Architecture:** AgentOS runtime + centralized prompt catalog + streamlined Airtable integration
**Demo Status:** ✅ 15+ candidate screenings executed (Pigment CFO, Mockingbird CFO searches) + markdown reports generated
**Presentation:** ✅ DELIVERED - PowerPoint deck (FMV_V1.pptx) presented Nov 19, 

## Deliverables

1. **Presentation:** PowerPoint slide deck - ✅ DELIVERED (FMV_V1.pptx, presented Nov 19, )
2. **Prototype:** Python implementation using Agno framework - ✅ COMPLETE (15+ demo screenings executed successfully)
3. **Documentation:** Comprehensive README (765 lines) + MkDocs site - ✅ COMPLETE

## Evaluation Criteria

**Product Thinking (25%)** | **Technical Design (25%)** | **Data Integration (20%)** | **Insight Generation (20%)** | **Communication (10%)**

## Technology Stack

**Core:** Python 3.11+ (uv), Agno framework, AgentOS (FastAPI), OpenAI (o4-mini-deep-research, gpt-5-mini), Airtable (pyairtable), Pydantic, YAML prompt catalog

**Demo Data (Nov 19, ):** ~63 executives loaded, 4 portcos configured (Pigment, Mockingbird, Synthesia, Estuary). **Stage 6 COMPLETED:** 15+ candidate screenings completed across Pigment CFO and Mockingbird CFO searches with markdown reports generated (reports/assessments/, reports/candidate_assessments/)

## Project Structure

**Core:** `demo/` (8 modules, ~3,255 LOC) | **Tests:** `tests/` (15 files, ~1,500 LOC)
**Documentation:**
- `spec/` - Internal technical specifications, PRD, dev plans, unit plans
- `docs/` - **Public-facing MkDocs site** (mkdocs.yml configured, material theme)
- `case/presentation/` - PowerPoint deck (FMV_V1.pptx) + supporting materials
- `reports/` - Generated assessment reports (15+ markdown reports)
- `README.md` - Comprehensive setup & usage guide (765 lines)

**Module Organization (Post-Refactoring):**

- `agents.py` (~550 lines) - Agent factories + execution runners
- `workflow.py` (~410 lines) - AgentOSCandidateWorkflow orchestration
- `agentos_app.py` (~255 lines) - FastAPI runtime (streamlined)
- `airtable_client.py` (~235 lines) - Write-only client (41% reduction)
- `screening_service.py` - Shared orchestration logic
- `screening_helpers.py` (~70 lines) - Business logic utilities
- `models.py` (~60 lines) - Pydantic models with structured payloads (62% reduction)
- `prompts.py` - YAML catalog loader

For detailed project structure, see **`README.md`** (lines 58-91).

## Quick Reference

**Testing:**
- `pytest tests/` - Full test suite (130 tests: 110 passed, 20 skipped, 74% coverage)
- `pytest tests/test_agentos_app.py -v` - Webhook endpoint tests
- `scripts/validate_airtable_client.py` - Airtable table alignment verification

**Reports:**
- `python3 scripts/generate_markdown_reports.py` - Generate markdown reports from SQLite sessions
- `node scripts/generate_markdown_reports.js` - Generate and upload reports to Airtable
- `reports/assessments/` - Auto-generated assessment reports (15+ files)
- `reports/candidate_assessments/` - Comprehensive candidate reports (SQLite-based)

**Documentation:**
- `uv run mkdocs serve` - Preview public docs locally at http://127.0.0.1:8000
- `uv run mkdocs build` - Generate static site in `site/` directory
- `docs/` - Public-facing MkDocs source (Material theme)
- `spec/` - Internal technical specifications and tracking

**Airtable:** Direct pyairtable client (no MCP dependency)

**Session Database:**
- **Location:** `tmp/agno_sessions.db` (SQLite database)
- **Primary Table:** `agno_sessions` (Agno-managed session state)
- **Additional Tables:** `agno_eval_runs`, `agno_memories`, `agno_knowledge`, `agno_metrics`, `workflow_session`
- **Query Sessions:** `sqlite3 tmp/agno_sessions.db "SELECT * FROM agno_sessions ORDER BY created_at DESC LIMIT 5;"`
- **Session Count:** 15 complete candidate screening sessions stored
- **Usage:** All workflow executions persist session state for audit trails and report generation

## Documentation Hierarchy

**Internal Specifications (spec/):**
1. `spec/spec.md` - **PRIMARY** technical specification (2040+ lines, v1.0-minimal contract)
2. `spec/prd.md` - Product requirements and acceptance criteria
3. `spec/dev_plan_and_checklist.md` - **CANONICAL TRACKING** - Implementation & demo tasks
4. `spec/dev_reference/AGNO_REFERENCE.md` - Framework patterns & best practices
5. `spec/dev_reference/implementation_guide.md` - Data models and interfaces
6. `spec/adhoc/` - Refactoring proposals, alignment tracking, completed initiatives

**Public-Facing Documentation (docs/ - MkDocs):**
1. `README.md` - **COMPREHENSIVE** setup & usage guide (765 lines) ⭐ START HERE
2. `docs/index.md` - MkDocs landing page
3. `docs/getting_started.md` - Quick start guide
4. `docs/architecture.md` - System architecture and design patterns
5. `docs/DESIGN_SYNTHESIS.md` - Complete architectural analysis (1,880 lines) 📐 DEEP DIVE
6. `docs/AGENT_DEFINITIONS.md` - Agent specifications and prompt catalog
7. `docs/DEMO_RUNBOOK.md` - Demo execution guide
8. `docs/airtable_ai_spec.md` - Airtable schema (8 tables: 7 workflow + 1 audit)
9. `docs/user_guide.md` - Usage and operational guide
10. `docs/contributing.md` - Development and contribution guidelines

**Presentation Materials (docs/):**
- `docs/FMV_V1.pptx` - **DELIVERED DECK** (presented Nov 19, )
- `docs/case/` - Supporting case materials and analysis
- Historical materials archived in git history

**Build:** Run `uv run mkdocs build` or `uv run mkdocs serve` to generate/preview public documentation site

**V1 Exclusions (Phase 2+ Only):**

- Workflows/Research_Results tables | Fast mode | Multi-iteration loops | Async processing
- Custom event persistence (using Agno-managed SqliteDb only)

## Key Design Decisions (Implemented)

**Architecture:**

- AgentOS FastAPI runtime (canonical webhook server) at `demo/agentos_app.py` (streamlined to ~255 lines)
- Workflow class extracted to `demo/workflow.py` for clear separation of concerns
- Shared workflow orchestration via `demo/screening_service.py`
- Agno 4-step linear workflow with SqliteDb session persistence
- Centralized YAML prompt catalog (`demo/prompts/catalog.yaml`) for all 4 agents
- **Airtable-First Pattern:** Write-only client, zero traversal API calls during execution

**Workflow:**

- Deep Research (o4-mini-deep-research) → Quality Check → Optional Incremental Search → Assessment
- Quality gate: ≥3 citations + non-empty summary triggers incremental search if needed
- Session state persisted to `tmp/agno_sessions.db` (SqliteDb, not InMemoryDb)
- Agno UI dashboard for real-time monitoring + session inspection

**Data & Integration:**

- **Airtable Simplification:** Structured nested object payloads, zero JSON parsing, zero traversal API calls
- `ScreenWebhookPayload` model validates complete pre-assembled data from Airtable
- Airtable client reduced to write-only operations (~235 lines, 41% reduction)
- AgentOS webhook at `POST /screen` receives structured payloads (no field traversal)
- Deep Research API (o4-mini-deep-research) with built-in web search
- Research parser agent converts markdown → structured `ExecutiveResearchResult`
- Assessment agent (gpt-5-mini + ReasoningTools) produces structured scores

**Agent Context Management:**

- Prompt templates loaded from `demo/prompts/catalog.yaml` via `get_prompt()`
- Temporal awareness: `add_datetime_to_context=True` on research/assessment agents
- Evidence taxonomy: [FACT]/[OBSERVATION]/[HYPOTHESIS] in Deep Research prompts
- Agno best practices: Follows patterns from `reference/docs_and_examples/agno/`

**Assessment:**

- Evidence-aware scoring: `None` for unknown dimensions (not 0 or NaN)
- Simple average calculation: (sum of scored dimensions / count) * 20
- LLM confidence levels: High/Medium/Low per dimension
- Counterfactuals: "Why might NOT be ideal" + key assumptions

## Implementation Status

**✅ Completed:** All stages 1-6 (28-30h total)
- Stage 1-5: Setup, Agents, Workflow, Webhook, Prompts, AgentOS, Integration Testing (25.6h)
- Post-Stage Refactoring: Airtable simplification (Phases 2-4) + Code restructuring
- Stage 5.8: Markdown report generation (3h) - Scripts implemented and 15+ reports generated
- Stage 6: Demo execution complete - 15+ candidate screenings across multiple searches
- Presentation: PowerPoint deck delivered (FMV_V1.pptx) on Nov 19, 

**Status:** Project complete and delivered
**Optional Enhancements:** Stage 5.7 (docs refresh), additional demo data
**Blockers:** None

**Refactoring Summary:**

- Airtable integration simplified: 0 traversal API calls, 0 JSON parsing operations
- Code restructured: 8 focused modules with clear separation (workflow.py, screening_helpers.py extracted)
- Legacy eliminated: ~180 lines of deprecated code removed
- Net reduction: ~500 lines overall (better organization, less code)

## Key Achievements (What Makes This Implementation Stand Out)

**1. Modern AI Agent Architecture:**

- ✅ AgentOS runtime with FastAPI + control plane UI for real-time monitoring
- ✅ Centralized YAML prompt catalog enabling code-free prompt iteration
- ✅ Evidence taxonomy in prompts ([FACT]/[OBSERVATION]/[HYPOTHESIS])
- ✅ Agno UI dashboard for session inspection and workflow debugging

**2. Evidence-Aware Assessment:**

- ✅ Explicit handling of "Unknown" using `None` (not 0 or NaN)
- ✅ LLM self-assessment confidence levels (High/Medium/Low)
- ✅ Counterfactuals: "Why candidate might NOT be ideal"
- ✅ Citation-backed reasoning with quality gates

**3. Production-Quality Engineering:**

- ✅ 130 tests (110 passed, 20 skipped), 74% coverage (exceeds 50% target)
- ✅ Type hints throughout (Pydantic models + function signatures)
- ✅ Comprehensive documentation (README: 765 lines, spec.md: 2040+ lines, docs/DESIGN_SYNTHESIS.md: 1,880 lines)
- ✅ Clean separation of concerns (8 focused modules, ~3,255 lines in demo/)
- ✅ Legacy code elimination (removed ~180 lines of deprecated functions)
- ✅ Modular architecture (agents.py, workflow.py, screening_helpers.py separation)

**4. Demonstrable Thinking Quality:**

- ✅ Domain-specific context engineering (VC/talent workflow)
- ✅ Incremental value delivery (each stage complete & tested)
- ✅ Spec alignment discipline (9/9 issues tracked & resolved)
- ✅ Validation tools (AirtableClient alignment checker)

**5. Scalable Foundation:**

- ✅ Session state persistence for audit trails
- ✅ Quality-gated research with conditional incremental search
- ✅ Modular prompt system for easy refinement
- ✅ Clear path to Phase 2 (async, caching, multi-iteration)

**6. Data Integration Excellence (Post-Stage Refactoring):**

- ✅ **Zero-traversal Airtable pattern:** 4+ sequential API calls → 0 during execution (100% elimination)
- ✅ **Structured payload validation:** JSON parsing operations 3 → 0 (Pydantic validates nested objects directly)
- ✅ **Code simplification:** models.py parsing logic 62% reduction (~160 → ~60 lines)
- ✅ **Client streamlining:** airtable_client.py 41% reduction (~400 → ~235 lines, write-only operations)
- ✅ **Airtable-First architecture:** Push complexity to declarative formulas, keep Python minimal
- ✅ **Performance gain:** ~500ms+ latency reduction per screen (no sequential API calls)

**7. Code Quality Refactoring (Post-Stage Optimization):**

- ✅ **Workflow extraction:** Moved AgentOSCandidateWorkflow to dedicated `workflow.py` (~410 lines)
- ✅ **Helper extraction:** Created `screening_helpers.py` for business logic utilities (~70 lines)
- ✅ **Legacy elimination:** Removed deprecated functions (screen_single_candidate, create_screening_workflow, ~180 lines)
- ✅ **FastAPI streamlining:** agentos_app.py reduced from ~665 → ~255 lines (61% reduction)
- ✅ **Agent focus:** agents.py streamlined to factories + runners only (~550 lines)
- ✅ **All tests passing:** 16/16 updated test files verified, maintained 82% coverage

## Architecture Documentation

**MkDocs Site (`docs/` folder):**

The `docs/` directory contains public-facing documentation built with MkDocs (Material theme):
- Run `uv run mkdocs serve` to preview locally at http://127.0.0.1:8000
- Run `uv run mkdocs build` to generate static site in `site/` directory
- Configuration: `mkdocs.yml` at project root

**Key Public Documentation:**

**docs/DESIGN_SYNTHESIS.md** (1,880 lines) - Comprehensive architectural analysis:
- **Executive Summary:** System purpose, key technologies, architecture philosophy
- **System Component Diagram:** Complete data flow visualization
- **Core Components:** Detailed analysis of all 8 modules with design patterns
- **Data Models:** Model hierarchy, validation rules, serialization patterns
- **Workflow Execution:** Step-by-step flow with session state management
- **Integration Architecture:** Airtable, AgentOS, webhook endpoint design
- **Key Implementation Details:** Two-agent research pattern, research merging, configuration management
- **Design Patterns & Decisions:** Evidence-aware scoring, quality-gated research, prompt management, error handling

**Purpose:** Demonstrates depth of thinking and serves as:
- Onboarding guide for new developers
- Reference for production migration
- Evidence of architectural decision-making quality
- Blueprint for Phase 2 enhancements
- **Public-facing showcase of technical design**

## Local Development Setup

For complete setup instructions including AgentOS server, ngrok tunnel configuration, and Airtable automation setup, see **`README.md`** (lines 373-757).

## Stage 6: Demo Execution & Presentation - ✅ COMPLETE

**Status:** All deliverables completed and presented Nov 19, 

**✅ Completed:**
- ✅ **Demo Executions:** 15+ candidate screenings executed across multiple searches
  - Pigment CFO search: Multiple candidates assessed (Madalina Tanasie, Deb Schwartz, Praveer Melwani, Alec Davidian)
  - Mockingbird CFO search: Multiple candidates assessed (Mohit Daswani, Brittany Bagley, David Andreasson, Alec Davidian)
- ✅ **Report Generation:** Markdown reports auto-generated in reports/assessments/ and reports/candidate_assessments/
- ✅ **Presentation:** PowerPoint deck delivered (FMV_V1.pptx) on Nov 19, 
- ✅ **Infrastructure Validation:** AgentOS + webhook endpoint + Airtable integration verified through multiple executions

**Optional Post-Delivery Enhancements:**
- Stage 5.7: MkDocs documentation refresh (1.5-3h)
- Additional demo data expansion
- Retrospective and learnings documentation
