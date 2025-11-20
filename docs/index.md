# Talent Signal Agent

## The Problem

Executive hiring at VC-backed companies is time-intensive and high-stakes. Talent teams manually research dozens of candidates—reviewing LinkedIn profiles, news articles, funding announcements—to match executives with portfolio company needs. This process:

- Takes 2-4 hours per candidate for thorough research
- Scales poorly (10 candidates = 20-40 hours of manual work)
- Introduces inconsistency (different researchers apply criteria differently)
- Delays time-to-hire for critical roles (CFO, CTO, VP positions)

## The Solution

The Talent Signal Agent augments talent teams with AI-powered research and evidence-based assessment. It transforms manual candidate evaluation into a systematic, scalable workflow designed to enhance recruiter effectiveness:

**Augments Human Judgment:** AI handles comprehensive research and initial assessment; talent teams make final decisions
**Maintains Consistency:** Same evaluation criteria applied systematically to every candidate
**Surfaces Non-Obvious Matches:** Prioritizes recall over precision—rather not miss a great match than filter out potential fits
**Provides Transparency:** Every claim backed by citations, every score explained with confidence levels

### How It Works

1. **Talent team triggers a "Screen"** in Airtable (familiar workflow—meets users where they are)
2. **AI agents research each candidate** using public sources (LinkedIn, news, company sites)
3. **Evidence-aware assessment** evaluates candidates against role requirements with explicit confidence levels
4. **Talent team reviews results** in Airtable—scores, reasoning, citations, and counterfactuals—then decides who to contact

All powered by a 4-step AI workflow with quality gates, guardrails, and full observability. The system provides decision support; humans make the final call.

## Key Innovations

### 1. Augmentation Over Automation

Following the principle that **AI should enhance decisions, not replace decision-makers:**

- **Human-in-the-Loop:** Talent teams review AI-generated insights and make final hiring decisions
- **Recruiter Enablement:** System makes recruiters more effective by handling time-intensive research
- **Iterative Learning:** Start with AI augmentation, evolve toward higher automation as trust builds
- **Decision Support:** Provides structured information for talent teams to make better-informed choices

### 2. Evidence-Aware Assessment

Unlike traditional screening systems that produce black-box scores, the Talent Signal Agent explicitly tracks **what it knows vs. doesn't know**:

- **Unknown ≠ Poor:** Missing evidence scores as `None` (not 0), preventing false negatives
- **Confidence Levels:** AI self-assesses confidence (High/Medium/Low) per evaluation dimension
- **Counterfactuals:** Every assessment includes "Why this candidate might NOT be ideal"
- **Citation-Backed:** Minimum 3 citations required; all claims verifiable

### 3. Quality-Gated Research

Prevents garbage-in-garbage-out with built-in quality checks:

- **Quality Gate:** Research must meet threshold (≥3 citations + non-empty summary)
- **Conditional Incremental Search:** Automatically fills gaps if initial research insufficient
- **Prevents Hallucination:** No assessment generated without sufficient evidence

### 4. Write-Only Data Integration

Eliminates expensive API traversals with structured payload architecture:

- **Zero reads during execution:** All context arrives via pre-assembled webhook payload
- **Airtable formulas do the work:** Declarative data assembly (push complexity to Airtable)
- **~500ms latency reduction:** From 4+ sequential API calls to 0

This documentation provides a comprehensive guide to understanding, using, and evaluating the Talent Signal Agent.

## Quick Start

**New to the project?** Start here based on your role:

### For Non-Technical Users (Talent Team, Recruiters)
1. **[Complete User Guide](user_guide_comprehensive.md)** - Learn how to use the system via Airtable
2. **[Demo Runbook](DEMO_RUNBOOK.md)** - Step-by-step demo guide

### For Technical Users (Developers, DevOps)
1. **[Getting Started](getting_started.md)** - Set up your local development environment
2. **[Technical Reference](technical/technical_reference.md)** - Complete technical documentation
3. **[Architecture](how_it_works/architecture.md)** - High-level system overview

## Documentation Index

### User Documentation

- **[Complete User Guide](user_guide_comprehensive.md)** - Comprehensive guide for using the Talent Signal Agent via Airtable
- **[Quick Reference (API)](how_it_works/user_guide.md)** - Brief API webhook reference

### Technical Documentation

- **[Technical Reference](technical/technical_reference.md)** - Complete technical documentation for developers
- **[Architecture Overview](how_it_works/architecture.md)** - System architecture, components, and data flow
- **[Design Synthesis](technical/DESIGN_SYNTHESIS.md)** - Comprehensive architectural analysis (1,880 lines)
- **[Agent Definitions](technical/AGENT_DEFINITIONS.md)** - Detailed specifications for all agents

### Setup & Operations

- **[Getting Started](getting_started.md)** - Local development setup
- **[Demo Runbook](DEMO_RUNBOOK.md)** - Complete demo setup and execution guide
- **[Airtable Schema](how_it_works/airtable_ai_spec.md)** - Database schema and field definitions

### Feature Documentation

- **[Prompt System Summary](technical/prompt_system_summary.md)** - Centralized YAML prompt catalog
- **[Role Spec Design](technical/role_spec_design.md)** - Role specification framework
- **[Spec Selection Architecture](technical/SPEC_SELECTION_ARCHITECTURE.md)** - Flexible spec selection system

### Internal Specifications

For authoritative technical and product requirements (internal development docs):

- **Technical Specification** (`spec/spec.md`) - Primary technical specification (canonical, 2040+ lines)
- **Product Requirements** (`spec/prd.md`) - Product requirements and acceptance criteria
- **Development Plan** (`spec/dev_plan_and_checklist.md`) - Implementation tracking and demo preparation

These specifications are maintained in the `spec/` directory for internal development use.

## Technical Highlights

**Production-Ready Implementation:**
- 129 automated tests (109 passed, 20 skipped, 76% coverage) validate core workflows
- Type-safe data models (Pydantic) prevent runtime errors
- Real-time monitoring via AgentOS control plane
- Comprehensive documentation (9,000+ lines across 16 files)

**Modern AI Agent Architecture:**
- Centralized YAML prompt catalog (code-free iteration)
- Evidence taxonomy in prompts ([FACT]/[OBSERVATION]/[HYPOTHESIS])
- Session state persistence for audit trails
- Quality-gated research with conditional incremental search

**4-Step Workflow:**

1. **Deep Research** - `o4-mini-deep-research` performs comprehensive OSINT profiling
2. **Quality Gate** - Validates ≥3 citations + complete summary
3. **Incremental Search** (conditional) - `gpt-5` fills gaps if quality insufficient
4. **Assessment** - `gpt-5-mini` with ReasoningTools evaluates against role spec

See **[Architecture Overview](how_it_works/architecture.md)** for complete technical details.

## Need Help?

- **Setup Issues?** See [Getting Started](getting_started.md) or [Demo Runbook](DEMO_RUNBOOK.md)
- **Architecture Questions?** See [Architecture](how_it_works/architecture.md) or [Design Synthesis](technical/DESIGN_SYNTHESIS.md)
- **API Usage?** See [API Reference](how_it_works/user_guide.md)
- **Agent Details?** See [Agent Definitions](technical/AGENT_DEFINITIONS.md)
