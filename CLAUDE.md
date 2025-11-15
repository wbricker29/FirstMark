# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This is a working directory for Will Bricker's evaluation for the AI Lead role at FirstMark Capital. The repository contains research, preparation materials, and case study work for the interview process.

## Directory Structure

```
.
├── case/                    # Case study deliverables
│   ├── FirstMark_case.md   # Case study requirements and specifications
│   └── FirstMark AI Product Case Study.pdf  # Original case study brief
├── research/               # Research and preparation materials
│   ├── Firm_DeepResearch.md
│   ├── interviewprep_111325.md
│   └── member_research/    # Individual partner/team member research
└── role_overview.md        # AI Builder role description and requirements
```

## Case Study Overview

The main focus is building a "Talent Signal Agent" - an AI-powered system that helps FirstMark's talent team match executives from their network (portfolio companies, guilds, LinkedIn) to open roles across their portfolio companies.

**Key Requirements:**
- Integrate structured data (CSVs with company/role data) and unstructured data (bios, job descriptions, LinkedIn profiles)
- Identify and rank potential CTO/CFO candidates for open roles
- Provide clear reasoning trails for matches
- Use mock/synthetic data for demonstration

**Deliverables:**
1. Write-up or slide deck (1-2 pages) covering problem framing, agent design, architecture, and production considerations
2. Lightweight Python prototype (using LangChain/LlamaIndex/similar) that ingests data, identifies matches, outputs ranked recommendations with reasoning
3. README or Loom video explaining implementation

**Evaluation Criteria:**
- Product Thinking (25%): Understanding of VC/talent workflows
- Technical Design (25%): Modern LLM/agent frameworks, modular design, retrieval/context/prompting
- Data Integration (20%): Structured + unstructured data handling (vector stores, metadata joins)
- Insight Generation (20%): Useful, explainable, ranked outputs with reasoning
- Communication & Clarity (10%): Clear explanation of approach and next steps

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

### Strategic Context (from development_principles.md)

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

Since this is a research and case study repository (not a code project with build/test commands), work typically involves:
- Adding or updating markdown documentation in `case/` and `research/`
- Creating case study deliverables (code, documentation, presentations)
- Organizing research materials about FirstMark, the role, and interview preparation

When building the case study prototype:
- Set up a Python environment with LangChain/LlamaIndex or similar agent frameworks
- Create mock data (CSVs for structured data, text files for unstructured data)
- Build data ingestion, vector storage, and retrieval components
- Implement ranking/matching logic with reasoning trails
- Document architecture and design decisions

**Remember:** The goal is demonstrating quality of thinking through a minimal, working prototype—not building production-ready infrastructure.
