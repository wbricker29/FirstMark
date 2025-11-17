# CLAUDE.md

---
## ⚠️ V1 CRITICAL SCOPE - READ FIRST

**Architecture:** Linear workflow ONLY (Deep Research → Quality Check → Optional Single Incremental Search → Assessment)
**Tables:** 6 tables (People, Portco, Portco_Roles, Role_Specs, Searches, Screens, Assessments)
**Storage:** Research data in **Assessments** table (research_structured_json, research_markdown_raw, assessment_json, assessment_markdown_report)
**Database:** SqliteDb at `tmp/agno_sessions.db` (NO InMemoryDb, NO custom WorkflowEvent tables)
**Pipeline:** Direct structured outputs via `output_schemaa` (NO parser agent)

**Phase 2+ (DO NOT IMPLEMENT):** Fast mode | Loops/conditions | Parser agents | Workflows table | Research_Results table | Multi-iteration search

**Authority:** `spec/v1_minimal_spec*.md` > `spec/prd.md` > `demo_planning/*.md`
**Stale Docs:** airtable_schema.md (shows 9 tables), screening_workflow_spec.md (has loops/fast mode)

**Before ANY architectural work:**
1. Read spec/v1_minimal_spec.md + addendum
2. Build explicit design model
3. Scope filter (what to DELETE) before detail check
4. If unsure → ASK, cite conflict + sources

---

## Repository Purpose

FirstMark Capital AI Lead case study: Talent Signal Agent demo (presentation Nov 19, 2025 5pm)

## Current Project Status

**Phase:** Documentation alignment required before implementation
**Framework:** Agno (Python agent framework)
**Presentation:** Nov 19, 2025 5pm

**Blocking Issues:**
- ⚠️ Docs contain outdated 9-table design (v1 uses 6 tables)
- ⚠️ Workflow specs show loops/fast mode (v1 is linear only)
- ⚠️ Parser agent still documented (v1 uses direct structured outputs)
- See `demo_planning/v1_alignment_conflicts.md` for full list

**Status:**
- ✅ v1 scope defined (spec/v1_minimal_spec.md + addendum)
- ⚠️ Implementation docs need updates per v1 scope
- ❌ Python implementation not started (blocked by doc alignment)
- ❌ Airtable base setup not started

**Estimated:** 4-6 hrs doc fixes + 34-38 hrs implementation

## Key Directories

- `spec/` - Requirements and specifications (v1_minimal_spec.md is authoritative)
- `demo_planning/` - Implementation design (some docs outdated, see trust signals below)
- `reference/` - Data and documentation (guildmember_scrape.csv has 64 executives)
- `case/` - Planning history and tracking

## Case Study Overview

**Project:** Talent Signal Agent - an AI-powered system that helps FirstMark's talent team match executives from their network to open roles across portfolio companies.

**Key Requirements:**
- Integrate structured data (CSVs with company/role data) and unstructured data (bios, job descriptions, LinkedIn profiles)
- Identify and rank potential CTO/CFO candidates for open roles
- Provide clear reasoning trails for matches
- Use mock/synthetic data for demonstration

**Deliverables:**
1. Write-up or slide deck (1-2 pages) covering problem framing, agent design, architecture, and production considerations
2. Lightweight Python prototype using modern agent frameworks that ingests data, identifies matches, outputs ranked recommendations with reasoning
3. README or Loom video explaining implementation

**Evaluation Criteria:**
- Product Thinking (25%): Understanding of VC/talent workflows
- Technical Design (25%): Modern LLM/agent frameworks, modular design, retrieval/context/prompting
- Data Integration (20%): Structured + unstructured data handling (vector stores, metadata joins)
- Insight Generation (20%): Useful, explainable, ranked outputs with reasoning
- Communication & Clarity (10%): Clear explanation of approach and next steps

## Technology Stack

**AI Framework:** Agno (Python-based agentic AI framework)
- Selected for rapid development, built-in agent patterns, and strong examples
- See `demo_planning/AGNO_REFERENCE.md` for case-specific guidance
- See `reference/docs_and_examples/agno/` for comprehensive documentation

**LLM Models:**
- GPT-5, GPT-5-mini (assessment/evaluation)
- o4-mini-deep-research (research phase via OpenAI Deep Research API)
- Web Search builtin tool (web_search_preview) for supplemental research

**Infrastructure:**
- Flask webhook server + ngrok for Airtable automation triggers
- Airtable as primary data store (9 tables with complete schema)
- pyairtable for Airtable API integration
- Pydantic for data validation and structured outputs

**Python Environment:**
- Python 3.11+ managed with `uv` (see `.python-version`)
- Virtual environment in `.venv/`
- Dependencies: flask, pyairtable, openai, python-dotenv, pydantic (NOT YET INSTALLED)

**Demo Data:**
- 64 executives from `reference/guildmember_scrape.csv`
- 4 demo portcos: Pigment (CFO), Mockingbird (CFO), Synthesia (CTO), Estuary (CTO)
- 3 pre-run scenarios + 1 live demo scenario

**Supporting Tools:**
- Node.js scripts for portfolio research (not part of deliverable)
- Slash commands for workflow automation (`.claude/commands/`)
- Custom skills for agent design (`.claude/skills/`)

## Documentation Trust Signals

### ⭐ AUTHORITATIVE (Tier 1)
- **spec/v1_minimal_spec.md** - V1 scope contract (HIGHEST AUTHORITY)
- **spec/v1_minimal_spec_agno_addendum.md** - Agno clarifications for v1
- **spec/prd.md** - Product requirements (aligned with v1 scope)
- **spec/spec.md** - Technical specification (aligned with v1 scope)
- **spec/constitution.md** - Development principles

### ✅ IMPLEMENTATION GUIDES (Tier 2)
- **demo_planning/implementation_guide.md** ⭐ MASTER IMPLEMENTATION DOC
  - Consolidates: Pydantic models, agent configs, workflow, Deep Research limitations
  - 100% aligned with spec/v1_minimal_spec.md
  - Single source of truth for implementation details
- **demo_planning/airtable_ai_spec.md** - Airtable schema (7 tables: 6 core + 1 helper)
- **demo_planning/role_spec_design.md** - CFO/CTO templates
- **demo_planning/AGNO_REFERENCE.md** - Framework patterns

### 📦 ARCHIVED (Consolidated into implementation_guide.md)
- ~~data_design.md~~ → Merged into implementation_guide.md
- ~~screening_workflow_spec.md~~ → Merged into implementation_guide.md
- ~~deep_research_findings.md~~ → Merged into implementation_guide.md
- ~~v1_alignment_conflicts.md~~ → Issues resolved, archived

### ❌ V1 EXCLUSIONS (Phase 2+ Only)
- Parser agent pipeline → Deep Research returns markdown
- Workflows or Research_Results tables → Use Assessments table only
- Fast mode → v1 Deep Research only
- Multi-iteration loops → Single optional incremental search
- Async/concurrent processing → Sequential only

## Context

**Role:** AI Builder at FirstMark Capital
- Greenfield opportunity to build AI capabilities across investing, platform, and back office
- Focus areas: deal memos, valuation analysis, event management, content repurposing, portfolio analytics
- 5 days in-office in Flatiron, NYC
- Targeting hire by end of year

## Key Technical Decisions (RESOLVED)

All major technical decisions have been finalized. Implementation can proceed without further design work.

**Architecture:**
- ✅ Module scope: Module 4 (Screen workflow) ONLY - Modules 1-3 pre-populated manually
- ✅ Data store: Airtable (9 tables with complete schema defined)
- ✅ Integration: Flask webhook + ngrok for Airtable automation triggers
- ✅ Execution: Synchronous/sequential processing (async deferred to post-demo)

**AI/LLM Stack:**
- ✅ Research: OpenAI Deep Research API (o4-mini-deep-research) + Web Search builtin
- ✅ Assessment: GPT-5 or GPT-5-mini with structured outputs
- ✅ No third-party search APIs: LinkedIn/web research via Deep Research API only
- ✅ Citation handling: URLs + key quotes from API (no separate scraping)

**Assessment Approach:**
- ✅ Single evaluation method: Spec-guided assessment with evidence-aware scoring
- ✅ Confidence levels: LLM self-assessment + evidence count threshold
- ✅ Counterfactuals: "Why candidate might NOT be ideal" + key assumptions
- ✅ AI-generated rubric: Explicitly deferred to Phase 2+ (not in demo)

**Demo Strategy:**
- ✅ Execution modes: Deep Research (comprehensive) + Web Search (fast fallback)
- ✅ Pre-runs: 3 scenarios (Pigment CFO, Mockingbird CFO, Synthesia CTO)
- ✅ Live demo: 1 scenario (Estuary CTO) with smaller candidate set or Web Search mode
- ✅ Data source: 64 executives from `reference/guildmember_scrape.csv`

**Simplifications (Demo v1.0):**
- ✅ Candidate Profiles: OUT OF SCOPE - bespoke research per role instead
- ✅ Deduplication: Skip (assume clean data)
- ✅ Apollo enrichment: Stub/mock only (not real integration)
- ✅ Custom Airtable UI: Standard views only (no custom interfaces)

## Development Principles

### Constraints
- **Time allowance:** 48 hours to execute the case
- **Priority:** Demonstrate quality of thinking first and foremost
- **Technical approach:** All components must be minimal and quick to stand up

### Decision Matrix
```
always          → explain → code → verify
ambiguous?      → clarify
existing_code?  → change_minimum
new_feature?    → MVP → validate → expand
```

### Prioritization Framework
```
Simple > Perfect
Clear > Clever
Working > Optimal
Request > BestPractice
Smaller > Larger
```

### Core Development Process

**Understand → Plan → Code → Test → Validate**

1. **Understand:** requirements, context, dependencies
2. **Plan:** consider multiple approaches, select optimal approach, define implementation plan and atomic steps
3. **Execute:** Implement code according to plan, follow best practices
4. **Validate:** verify functionality, validate acceptance criteria
5. **Document:** Update task status, provide required completion information

**Key Rules:**

- **SIMPLICITY (KISS & YAGNI)**
  - New Code → Targeted + Elegant + Simple
  - Code Change → Minimal changes to code and files possible
  - No feature creep & unrelated refactoring
  - Deliver the smallest working increment
  - Minimal files and complete code

- **QUALITY (Complete & documented)**
  - Types, docstrings, comments for complex logic
  - No placeholders
  - Code Change → Target <100 LOC per change

- **COMMUNICATION**
  - Request clarification or ask questions if ambiguous
  - Never assume; always verify

### Strategic Context

When building the case study prototype, apply these key principles:

1. **Domain Calibration Before Solution Design**
   - Deep understanding of VC/talent workflows must precede technical architecture
   - Value definition is stakeholder-specific: what FirstMark's talent team needs vs. what's technically impressive

2. **Incremental Value Delivery**
   - Deliver complete value units iteratively rather than building infrastructure first
   - Each development increment should provide independently useful functionality
   - Build foundational capabilities through practical applications, not speculation

3. **Maximize Expected Value**
   - Balance business impact (solving real talent matching problems), technical leverage (reusable components), and learning (validating assumptions)
   - Think in portfolios: quick wins + foundational bets + learning experiments
   - Given 48-hour constraint, bias toward quick wins that demonstrate thinking quality

4. **Context Engineering for AI Effectiveness**
   - AI performance depends on information quality and relevance
   - Identify what information matters when, inject domain-specific knowledge, provide relevant examples
   - Generic AI fails in specialized domains; contextualized AI excels

## Quick Reference

**Tech Stack:**
- Python 3.11+ (uv package manager)
- Agno framework (agent orchestration)
- OpenAI: o4-mini-deep-research (research), gpt-5-mini (assessment)
- Airtable (6 tables) + Flask webhook + ngrok
- Pydantic (structured outputs)

**Data:**
- 64 executives in `reference/guildmember_scrape.csv`
- 4 demo scenarios (Pigment CFO, Mockingbird CFO, Synthesia CTO, Estuary CTO)

**Slash Commands:**
- `/work`, `/plan`, `/spec`, `/verify`, `/check`

**Skills:**
- `ai-agent-architect`, `crawl4ai`, `brainstorming`

**Templates:**
- PRD, SPEC, PLAN, DESIGN, CONSTITUTION templates for structured documentation

## Next Steps

**READY FOR IMPLEMENTATION** ✅
- All documentation alignment issues resolved (2025-01-19)
- Master implementation guide created: `demo_planning/implementation_guide.md`
- All specs aligned with v1 minimal scope

**Implementation Path** (34-38 hours)
1. Airtable setup (6 tables, not 9)
2. Python: Research + Assessment agents (direct structured outputs, no parser)
3. Flask webhook + Agno linear workflow
4. Pre-runs (Pigment, Mockingbird, Synthesia)
5. Demo prep (Estuary live)

**Goal:** Demonstrate quality of thinking through minimal, working prototype (Module 4 only)
