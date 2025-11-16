# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This is a working directory for Will Bricker's evaluation for the AI Lead role at FirstMark Capital. The repository contains research, preparation materials, and case study work for the interview process.

## Current Project Status

**Phase:** Planning Complete → Ready for Implementation
**Framework Selected:** Agno (Python-based agentic AI framework)
**Presentation:** Tuesday, Nov 19, 2025 at 5 PM

**Progress:**
- ✅ Requirements defined (case_requirements.md)
- ✅ Solution strategy documented (solution_strategy.md)
- ✅ Technical specification complete (technical_spec.md)
- ✅ Product Requirements Document (spec/prd.md)
- ✅ Technical Specification (spec/spec.md)
- ✅ Project Constitution (spec/constitution.md)
- ✅ Implementation refinement proposal created
- ✅ Presentation plan drafted
- ✅ Mock data design complete (data_design.md)
- ✅ Complete Airtable schema designed (airtable_schema.md - 9 tables)
- ✅ Screening workflow specification (screening_workflow_spec.md)
- ✅ Deep Research findings documented (deep_research_findings.md)
- ❌ Python implementation NOT STARTED (0%)
- ❌ Airtable base setup NOT STARTED (0%)
- ❌ Demo pre-runs NOT STARTED (0%)

**Estimated Remaining:** 34-38 hours total

## Directory Structure

```
.
├── case/                         # Case study deliverables and planning
│   ├── case_requirements.md      # Original case study requirements
│   ├── solution_strategy.md      # High-level approach and strategy
│   ├── technical_spec.md         # Initial technical architecture
│   ├── implementation_refinement_proposal.md  # Implementation roadmap
│   ├── presentation_plan.md      # Presentation structure (Nov 19)
│   ├── tracking.md               # Detailed task tracking (CHECK HERE FIRST)
│   └── archive/                  # Previous iterations
├── spec/                         # ⭐ Current authoritative specifications
│   ├── prd.md                    # Product Requirements Document (CURRENT)
│   ├── spec.md                   # Technical Specification (CURRENT)
│   ├── constitution.md           # Project governance & principles
│   └── units/                    # Component specifications
├── demo_planning/                # ⭐ Implementation design documents
│   ├── airtable_schema.md        # Complete 9-table Airtable schema
│   ├── data_design.md            # Mock data structures & Pydantic models
│   ├── role_spec_design.md       # CFO/CTO role spec templates
│   ├── screening_workflow_spec.md # Module 4 workflow specification
│   ├── deep_research_findings.md # OpenAI Deep Research API research
│   ├── airtable_ai_spec.md       # Airtable AI automation spec
│   ├── alignment_issues_and_fixes.md # Alignment documentation
│   └── AGNO_REFERENCE.md         # Agno framework reference
├── reference/                    # Reference materials
│   ├── guildmember_scrape.csv    # ⭐ 64 executives for demo (PRE-LOADED)
│   ├── role_overview.md          # AI Builder role description
│   └── docs_and_examples/        # Framework docs and code examples
│       └── agno/                 # Agno framework documentation
├── scripts/                      # Node.js automation scripts
│   ├── scrape_companies.js       # Portfolio scraping
│   ├── process_portfolio.js      # Data processing
│   └── create_summary.js         # Summary generation
├── non_code/                     # Research and notes (ignored by git)
├── main.py                       # ⚠️ Stub only - implementation pending
├── pyproject.toml                # ⚠️ No dependencies yet
├── .env                          # API keys (gitignored)
└── .claude/                      # Claude Code configuration
    ├── skills/                   # Custom skills
    ├── commands/                 # Slash commands (/work, /plan, /spec, etc.)
    └── templates/                # Document templates
```

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

## Key Documentation

### ⭐ START HERE - Current Authoritative Documents
- **case/tracking.md** - Detailed task tracking and current status (CHECK HERE FIRST!)
- **spec/prd.md** - Product Requirements Document (authoritative requirements)
- **spec/spec.md** - Technical Specification (authoritative technical design)
- **spec/constitution.md** - Project governance and development principles

### Implementation Design (in `demo_planning/`)
- **airtable_schema.md** - Complete 9-table Airtable schema with all field definitions
- **data_design.md** - Pydantic models and data structures
- **role_spec_design.md** - CFO/CTO role spec templates (fully designed)
- **screening_workflow_spec.md** - Module 4 workflow specification
- **deep_research_findings.md** - OpenAI Deep Research API findings
- **airtable_ai_spec.md** - Airtable AI automation specification
- **AGNO_REFERENCE.md** - Agno framework patterns for this case

### Case Planning Documents (in `case/`)
- **case_requirements.md** - Original case study requirements
- **solution_strategy.md** - High-level approach and strategy
- **technical_spec.md** - Initial technical architecture
- **implementation_refinement_proposal.md** - Implementation roadmap
- **presentation_plan.md** - Presentation structure (Nov 19, 5 PM)

### Supporting Documents
- **AGENTS.md** - Repository-level guidelines and conventions
- **REQUIREMENTS.md** - Core development requirements and principles
- **README.md** - Repository overview

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
new_feature?    → MVP → test → expand
```

### Prioritization Framework
```
Simple Features, Working > Perfect
Clear > Clever
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

## Working on This Repository

### Current Focus: READY FOR IMPLEMENTATION

**Status:** All planning is complete. Implementation has NOT started yet.

**Critical Path (34-38 hours remaining):**
1. **Airtable Base Setup** (7 hours) - Create base, tables, import executives
2. **Python Dependencies** (1 hour) - Install flask, pyairtable, openai, pydantic
3. **Core Implementation** (20-24 hours) - Research agent, assessment agent, Flask webhook
4. **Webhook Setup** (1 hour) - ngrok + Airtable automation
5. **Pre-Run Executions** (4-6 hours) - Run 3 pre-run scenarios
6. **Demo Prep & Polish** (3-4 hours) - Test, practice, write-up

**See `case/tracking.md` for detailed task breakdown and next steps.**

### Key Implementation References

**Authoritative Specifications:**
- Product requirements: `spec/prd.md` (current)
- Technical design: `spec/spec.md` (current)
- Project governance: `spec/constitution.md`

**Implementation Design:**
- Airtable schema: `demo_planning/airtable_schema.md` (9 tables, all fields defined)
- Data models: `demo_planning/data_design.md` (Pydantic schemas)
- Workflow spec: `demo_planning/screening_workflow_spec.md` (Module 4)
- Role templates: `demo_planning/role_spec_design.md` (CFO/CTO)

**Agno Framework:**
- Case-specific guide: `demo_planning/AGNO_REFERENCE.md`
- Full documentation: `reference/docs_and_examples/agno/`
- Recruiter example: `reference/docs_and_examples/agno/agno_recruiter.md`

### Python Development

**Environment Setup:**
```bash
# Python 3.11+ managed by uv
python --version  # Should be 3.11+

# Install dependencies (REQUIRED - not yet done)
# First add to pyproject.toml: flask, pyairtable, openai, python-dotenv, pydantic
uv pip install -e .

# Activate virtual environment
source .venv/bin/activate

# Set up environment variables
# Create .env file with: OPENAI_API_KEY, AIRTABLE_API_KEY, AIRTABLE_BASE_ID
```

**Implementation Location:**
- Main application: `main.py` (currently stub only)
- Pydantic models: Create `models.py`
- Agent implementations: Create `agents.py` or separate files
- Flask routes: Add to `main.py` or create `routes.py`
- Keep implementation minimal and focused on Module 4 (Screen workflow)

**Data Location:**
- Executive data: `reference/guildmember_scrape.csv` (64 executives - ALREADY EXISTS)
- Airtable: Primary data store (9 tables - NOT YET CREATED)
- Generated results: Stored in Airtable tables

### Node.js Scripts

Located in `scripts/`:
- `scrape_companies.js` - Scrape FirstMark portfolio data
- `process_portfolio.js` - Process scraped data into structured format
- `create_summary.js` - Generate summaries and exports

These are supporting tools for research; not part of main deliverable.

### Using Claude Code Features

**Slash Commands** (in `.claude/commands/`):
- `/work` - Execute tasks following UPEVD pattern
- `/plan` - Generate implementation plans
- `/spec` - Create technical specifications
- `/verify` - Run verification gates
- `/check` - Validate project alignment

**Skills** (in `.claude/skills/`):
- `ai-agent-architect` - Framework-agnostic agent design patterns
- `crawl4ai` - Web scraping and data extraction
- `brainstorming` - Ideation and design refinement

**Templates** (in `.claude/templates/`):
- PRD, SPEC, PLAN, DESIGN, CONSTITUTION templates for structured documentation

## Next Steps - Immediate Actions

### Critical Path to Demo (34-38 hours remaining)

**1. Airtable Base Setup (7 hours) - DO FIRST**
- Create new base: "FirstMark Talent Signal Agent Demo"
- Create all 9 tables from `demo_planning/airtable_schema.md`
- Import 64 executives from `reference/guildmember_scrape.csv`
- Create 4 portco records, 4 role records, 6 role specs
- Create 4 search records and 4 screen records

**2. Python Environment Setup (1 hour)**
- Add dependencies to `pyproject.toml`: flask, pyairtable, openai, python-dotenv, pydantic
- Run `uv pip install -e .`
- Create `.env` with API keys (OpenAI, Airtable)
- Test basic API connectivity

**3. Core Python Implementation (20-24 hours)**
- Create Pydantic models (ExecutiveResearchResult, AssessmentResult, etc.)
- Implement research agent (Deep Research API + parser)
- Implement assessment agent (spec-guided evaluation)
- Implement Flask webhook server with `/screen` endpoint
- Implement Airtable integration
- End-to-end testing

**4. Webhook & Automation (1 hour)**
- Start Flask + ngrok
- Create Airtable automation trigger
- Test automation flow

**5. Pre-Run Executions (4-6 hours)**
- Run Pigment CFO screening
- Run Mockingbird CFO screening
- Run Synthesia CTO screening
- Verify all results in Airtable

**6. Demo Prep & Polish (3-4 hours)**
- Test Estuary live demo flow
- Create Airtable demo views
- Practice presentation
- Write 1-2 page deliverable

**See `case/tracking.md` for complete detailed breakdown.**

**Remember:** The goal is demonstrating quality of thinking through a minimal, working prototype focused on Module 4 (Screen workflow) only.
