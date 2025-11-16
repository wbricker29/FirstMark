# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This is a working directory for Will Bricker's evaluation for the AI Lead role at FirstMark Capital. The repository contains research, preparation materials, and case study work for the interview process.

## Current Project Status

**Phase:** Implementation planning for Talent Signal Agent prototype
**Framework Selected:** Agno (Python-based agentic AI framework)
**Progress:**
- ✅ Requirements defined
- ✅ Solution strategy documented
- ✅ Technical specification complete
- ✅ Implementation refinement proposal created
- ✅ Presentation plan drafted
- ✅ Mock data design complete
- 🚧 Prototype implementation in progress

## Directory Structure

```
.
├── case/                         # Case study deliverables and planning
│   ├── case_requirements.md      # Case study requirements
│   ├── solution_strategy.md      # High-level approach and strategy
│   ├── technical_spec.md         # Technical architecture and design
│   ├── implementation_refinement_proposal.md  # Implementation details
│   ├── presentation_plan.md      # Presentation structure
│   ├── tracking.md               # Progress tracking
│   └── archive/                  # Previous iterations
├── demo_planning/                # Prototype planning and design
│   ├── data_design.md            # Mock data structure design
│   ├── role_spec_design.md       # Role specification design
│   └── AGNO_REFERENCE_GUIDE.md   # Agno framework reference
├── demo_files/                   # Prototype implementation files
├── spec/                         # Technical specifications
│   └── units/                    # Component specifications
├── research/                     # Research and preparation materials
│   ├── Firm_DeepResearch.md
│   ├── member_research/          # Individual partner research
│   └── interview_research/       # Interview preparation
├── reference/                    # Reference materials and examples
│   ├── role_overview.md          # AI Builder role description
│   └── docs_and_examples/        # Framework docs and code examples
│       ├── agno/                 # Agno framework documentation (~2,000 files)
│       └── alternative_architectures/  # Other agent frameworks for reference
├── scripts/                      # Node.js automation scripts
│   ├── scrape_companies.js       # Portfolio scraping
│   ├── process_portfolio.js      # Data processing
│   └── create_summary.js         # Summary generation
└── .claude/                      # Claude Code configuration
    ├── skills/                   # Custom skills (crawl4ai, ai-agent-architect, etc.)
    ├── commands/                 # Slash commands (/work, /plan, /spec, etc.)
    ├── hooks/                    # Git hooks and automation
    └── templates/                # Document templates (PRD, SPEC, PLAN, etc.)
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

**Framework:** Agno - Python-based agentic AI framework
- Selected for rapid development, built-in agent patterns, and strong examples
- See `AGNO_QUICK_START.md` for quick reference
- See `reference/docs_and_examples/agno/` for comprehensive documentation
- See `demo_planning/AGNO_REFERENCE_GUIDE.md` for case-specific guidance

**Python Environment:**
- Python 3.11+ managed with `uv` (see `.python-version`)
- Minimal dependencies approach (see `pyproject.toml`)
- Virtual environment in `.venv/`

**Supporting Tools:**
- Node.js scripts for portfolio data scraping and processing
- Git hooks for type checking and state tracking (`.claude/hooks/`)
- Slash commands for workflow automation (`.claude/commands/`)

## Key Documentation

### Primary Case Documents (in `case/`)
- **case_requirements.md** - Start here for case overview
- **solution_strategy.md** - High-level approach and design decisions
- **technical_spec.md** - Detailed technical architecture
- **implementation_refinement_proposal.md** - Implementation roadmap
- **presentation_plan.md** - Structure for final deliverable
- **tracking.md** - Current progress and task tracking

### Planning Documents (in `demo_planning/`)
- **data_design.md** - Mock data structures for executives, roles, companies
- **role_spec_design.md** - Role specification design
- **AGNO_REFERENCE_GUIDE.md** - Framework patterns relevant to this case

### Supporting Documents
- **AGENTS.md** - Repository-level guidelines and conventions
- **REQUIREMENTS.md** - Core development requirements and principles
- **AGNO_QUICK_START.md** - Quick reference for Agno framework
- **README.md** - Repository overview

## Context

**Role:** AI Builder at FirstMark Capital
- Greenfield opportunity to build AI capabilities across investing, platform, and back office
- Focus areas: deal memos, valuation analysis, event management, content repurposing, portfolio analytics
- 5 days in-office in Flatiron, NYC
- Targeting hire by end of year

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

### Current Focus: Prototype Implementation

The case planning is complete. Current work involves:
- Implementing the Talent Signal Agent prototype in Python using Agno
- Creating mock data based on designs in `demo_planning/data_design.md`
- Building agent components per `case/technical_spec.md`
- Testing and validating the prototype
- Documenting implementation and preparing presentation

### Key Reference Materials

**For Agno Framework:**
- Quick start: `AGNO_QUICK_START.md`
- Case-specific guide: `demo_planning/AGNO_REFERENCE_GUIDE.md`
- Full documentation: `reference/docs_and_examples/agno/00_INDEX.md`
- Recruiter patterns: `reference/docs_and_examples/agno/agno_recruiter.md`
- Working example: `reference/docs_and_examples/agno/candidate_analyser/`

**For Case Strategy:**
- Requirements: `case/case_requirements.md`
- Approach: `case/solution_strategy.md`
- Architecture: `case/technical_spec.md`
- Implementation plan: `case/implementation_refinement_proposal.md`

### Python Development

**Environment Setup:**
```bash
# Python version managed by uv
python --version  # Should be 3.11+

# Install dependencies (when added to pyproject.toml)
uv pip install -e .

# Activate virtual environment
source .venv/bin/activate
```

**Code Location:**
- Prototype code goes in `demo_files/` or root-level Python files
- Mock data generation scripts in `demo_files/` or `scripts/`
- Keep implementation minimal and focused on demonstrating the concept

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

### Repository Context Tool

You can use the repomix file to help understand the repo structure:
```bash
# Generate updated repository context (if repomix is installed)
repomix

# View repository context
cat repomix-output.xml
```

## Next Steps

1. **Implement prototype** - Build the Talent Signal Agent using Agno framework
2. **Create mock data** - Generate synthetic data per `demo_planning/data_design.md`
3. **Test functionality** - Validate matching, ranking, and reasoning outputs
4. **Document implementation** - Create README or prepare Loom walkthrough
5. **Prepare presentation** - Follow structure in `case/presentation_plan.md`
6. **Final review** - Ensure all deliverables meet evaluation criteria

**Remember:** The goal is demonstrating quality of thinking through a minimal, working prototype—not building production-ready infrastructure.
