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

## Working on This Repository

Since this is a research and case study repository (not a code project with build/test commands), work typically involves:
- Adding or updating markdown documentation in `case/` and `research/`
- Creating case study deliverables (code, documentation, presentations)
- Organizing research materials about FirstMark, the role, and interview preparation

When building the case study prototype, you'll likely need to:
- Set up a Python environment with LangChain/LlamaIndex or similar agent frameworks
- Create mock data (CSVs for structured data, text files for unstructured data)
- Build data ingestion, vector storage, and retrieval components
- Implement ranking/matching logic with reasoning trails
- Document architecture and design decisions
