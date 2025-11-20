# Talent Signal Agent

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Test Coverage](https://img.shields.io/badge/coverage-76%25-brightgreen.svg)](tests/)
[![Tests](https://img.shields.io/badge/tests-109%20passed-brightgreen.svg)](tests/)

> AI-powered executive matching for FirstMark Capital portfolio companies.
> Automates candidate screening with evidence-based assessment and transparent reasoning.

---

## The Problem

Executive hiring at VC-backed companies is time-intensive and high-stakes. Talent teams manually research dozens of candidates—reviewing LinkedIn profiles, news articles, funding announcements—to match executives with portfolio company needs. This process:

- **Takes 2-4 hours per candidate** for thorough research
- **Scales poorly** (10 candidates = 20-40 hours of manual work)
- **Introduces inconsistency** (different researchers apply criteria differently)
- **Delays time-to-hire** for critical roles (CFO, CTO, VP positions)

## The Solution

The Talent Signal Agent augments talent teams with AI-powered research and evidence-based assessment. It transforms manual candidate evaluation into a systematic, scalable workflow designed to enhance recruiter effectiveness:

- **Augments Human Judgment:** AI handles comprehensive research and initial assessment; talent teams make final decisions
- **Maintains Consistency:** Same evaluation criteria applied systematically to every candidate
- **Surfaces Non-Obvious Matches:** Prioritizes recall over precision—rather not miss a great match than filter out potential fits
- **Provides Transparency:** Every claim backed by citations, every score explained with confidence levels

### How It Works

1. **Talent team triggers a "Screen"** in Airtable (familiar workflow—meets users where they are)
2. **AI agents research each candidate** using public sources (LinkedIn, news, company sites)
3. **Evidence-aware assessment** evaluates candidates against role requirements with explicit confidence levels
4. **Talent team reviews results** in Airtable—scores, reasoning, citations, and counterfactuals—then decides who to contact

All powered by a 4-step AI workflow with quality gates, guardrails, and full observability. The system provides decision support; humans make the final call.

---

## Key Innovations

### 1. Augmentation Over Automation

Following the principle that **AI should enhance decisions, not replace decision-makers:**

- **Human-in-the-Loop:** Talent teams review AI-generated insights and make final hiring decisions
- **Recruiter Enablement:** System makes recruiters more effective by handling time-intensive research
- **Iterative Learning:** Start with AI augmentation, evolve toward higher automation as trust builds
- **Decision Support:** Provides structured information for talent teams to make better-informed choices

### 2. Evidence-Aware Assessment

Explicitly tracks **what is known vs. unknown** to prevent hallucinations and surface uncertainty:

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

---

## Quick Start

### For Evaluators (FirstMark Team)

- 📊 **[View Presentation](docs/case/FMV_V1.1.pptx)** - PowerPoint deck + demo walkthrough (Final version delivered Nov 19, 2025)
- 🏗️ **[Design Synthesis](docs/technical/DESIGN_SYNTHESIS.md)** - 1,880-line architectural analysis
- 📈 **[Evaluation Rubric Alignment](#evaluation-rubric-alignment)** - Map deliverables to criteria

### For Users (Talent Teams)

- 📘 **[Complete User Guide](docs/user_guide_comprehensive.md)** - Learn how to use the system via Airtable
- 🎬 **[Demo Runbook](docs/DEMO_RUNBOOK.md)** - Step-by-step demo execution guide

### For Developers

- 🚀 **[Getting Started](docs/getting_started.md)** - 5-minute local setup
- 🔧 **[Technical Reference](docs/technical/technical_reference.md)** - Complete technical documentation
- 🏛️ **[Architecture](docs/how_it_works/architecture.md)** - High-level system overview

---

## Architecture at a Glance

**4-Step Evidence-Based Workflow:**

```
1. Deep Research       → o4-mini-deep-research performs comprehensive OSINT profiling
2. Quality Gate        → Validates ≥3 citations + complete summary (prevents hallucination)
3. Incremental Search  → (conditional) gpt-5 fills gaps if quality insufficient
4. Assessment          → gpt-5-mini with ReasoningTools evaluates against role spec
                         Outputs structured scores + confidence + counterfactuals
```

**Technology Stack:** Python 3.11+ | Agno Framework | AgentOS (FastAPI) | OpenAI (o4-mini, gpt-5) | Airtable (pyairtable) | Pydantic

**Data Flow:**
- Airtable automation triggers webhook → AgentOS runtime → Workflow orchestration → AI agents → Results written back to Airtable

**Development Approach:**
- **Calibrate First, Build Second:** Understand user needs before implementation
- **Ship Vertical Slices:** Deliver complete value units iteratively, not horizontal infrastructure layers
- **Learning Velocity Over Initial Accuracy:** Ship quickly, gather feedback, iterate based on real usage
- **Let Usage Inform Target State:** Build what's validated, not what's speculated
- Full principles documented in [docs/case/wb_development_principles.md](docs/case/wb_development_principles.md)

**Entity Hierarchy:**

```
Portfolio Company
    │
    ├─── Open Role (CFO, CTO, VP Engineering, etc.)
    │       │
    │       └─── Screen (screening process)
    │               │
    │               ├─── Candidate 1 (Person) ──┬─── Research Result
    │               │                            └─── Assessment
    │               │
    │               ├─── Candidate 2 (Person) ──┬─── Research Result
    │               │                            └─── Assessment
    │               │
    │               └─── Candidate N (Person) ──┬─── Research Result
    │                                            └─── Assessment
    │
    Person (Executive)
        └─── Can participate in multiple Screens across different roles/companies

Key Relationships:
• Portfolio Company : Open Role      = 1 : Many
• Open Role : Screen                 = 1 : Many
• Screen : Person                    = Many : Many (junction)
• Screen + Person : Research Result  = 1 : 1
• Screen + Person : Assessment       = 1 : 1
```

See **[Architecture Overview](docs/how_it_works/architecture.md)** for complete technical details.

---

## Key Design Decisions

**Augmentation-First Design:** System designed to make talent teams more effective, not replace them. Follows principle of "begin with AI augmentation, evolve toward automation" as trust builds through demonstrated value.

**Evidence-Aware Scoring:** Unknown dimensions score as `None` (not 0 or NaN), preventing false negatives. LLM provides self-assessed confidence levels (High/Medium/Low) per dimension. Prioritizes recall over precision—better to surface potential matches than miss great candidates.

**Quality-Gated Research:** Minimum 3 unique citations required. Conditional incremental search triggered if quality gate fails (single-pass, max 2 additional web searches). Prevents hallucination by requiring sufficient evidence before assessment.

**Airtable-First Integration:** Zero traversal API calls during execution. All context pre-assembled in structured webhook payload using Airtable formulas. Python client is write-only (~235 lines, 41% reduction). Meets users where they are—integrates with existing workflows.

**Prompt Catalog Architecture:** Centralized YAML system (`demo/prompts/catalog.yaml`) enables code-free prompt iteration. Evidence taxonomy ([FACT]/[OBSERVATION]/[HYPOTHESIS]) embedded in research prompts. Supports learning velocity through rapid experimentation.

**Session State Persistence:** SqliteDb storage (`tmp/agno_sessions.db`) for audit trail. AgentOS control plane provides real-time monitoring and session inspection. Observable at every step for trust-building and debugging.

**Incremental Value Delivery:** Tier 3 (80h proof-of-concept) → Tier 2 (1-month sprint) → Tier 1 (12-18 month full platform). Ship vertical slices that deliver complete value units, not horizontal infrastructure layers.

**Full Analysis:** [Design Synthesis](docs/technical/DESIGN_SYNTHESIS.md) (1,880 lines) | [Agent Definitions](docs/technical/AGENT_DEFINITIONS.md)

---

## Project Stats

- **Code:** ~3,255 lines across 8 focused modules (`demo/`)
- **Tests:** 129 tests (109 passed, 20 skipped), 76% coverage (exceeds 50% target)
- **Documentation:** 9,000+ lines across 16 documentation files
- **Demo Executions:** 15+ candidate screenings completed (Pigment CFO, Mockingbird CFO searches)
- **Reports Generated:** 15+ markdown assessment reports auto-generated

---

## Evaluation Rubric Alignment

This implementation maps to FirstMark's evaluation criteria:

| Criterion | Weight | Evidence | Documentation |
|-----------|--------|----------|---------------|
| **Product Thinking** | 25% | Problem framing, VC talent workflow understanding, value proposition | [Design Synthesis](docs/technical/DESIGN_SYNTHESIS.md), [User Guide](docs/user_guide_comprehensive.md) |
| **Technical Design** | 25% | AgentOS architecture, prompt catalog, modular design, 76% test coverage | [Architecture](docs/how_it_works/architecture.md), [Technical Reference](docs/technical/technical_reference.md) |
| **Data Integration** | 20% | Write-only Airtable pattern, structured payloads, zero traversal calls | [Airtable Schema](docs/how_it_works/airtable_ai_spec.md), [Integration Spec](docs/technical/agent_os_integration_spec.md) |
| **Insight Generation** | 20% | Evidence-aware assessment, counterfactuals, confidence levels, citation backing | [Agent Definitions](docs/technical/AGENT_DEFINITIONS.md), [Assessment Logic](docs/technical/technical_reference.md) |
| **Communication** | 10% | Clear documentation, no jargon, visible thinking process | This README, [Complete Documentation](docs/) |

---

## Local Development

### Prerequisites

- Python 3.11+ (verified with `.python-version`)
- UV package manager ([installation guide](https://github.com/astral-sh/uv))

### Setup (5 Minutes)

```bash
# 1. Install dependencies
uv pip install -e .

# 2. Configure environment variables
cp .env.example .env
# Edit .env with your API keys:
#   - OPENAI_API_KEY
#   - AIRTABLE_API_KEY
#   - AIRTABLE_BASE_ID

# 3. Verify installation
pytest tests/ -v
```

**Detailed Setup:** [Getting Started Guide](docs/getting_started.md)

### Project Structure

```
demo/                      # Core implementation (~3,255 lines)
├── agentos_app.py        # AgentOS FastAPI runtime (~255 lines)
├── workflow.py            # AgentOSCandidateWorkflow orchestration (~410 lines)
├── agents.py             # Agent factories & execution runners (~550 lines)
├── airtable_client.py    # Airtable API wrapper (~235 lines)
├── models.py             # Pydantic data models (~60 lines)
├── screening_helpers.py  # Business logic utilities (~70 lines)
├── settings.py           # Configuration/env loading
└── prompts/              # Centralized YAML prompt catalog
    ├── catalog.yaml      # Agent prompt definitions (4 agents)
    └── library.py        # Prompt loader (get_prompt function)

docs/                      # MkDocs public-facing documentation
spec/                      # Internal specifications & planning
tests/                     # Test suite (129 tests, 76% coverage)
case/presentation/         # Demo materials & PowerPoint slides
reports/                   # Auto-generated markdown assessment reports
```

---

## Running the Demo

### Option 1: Airtable Automation (Recommended)

1. **Start AgentOS server:**
   ```bash
   source .venv/bin/activate
   uv run python demo/agentos_app.py
   ```

2. **Start ngrok tunnel** (separate terminal):
   ```bash
   ngrok http 5001
   ```

3. **Configure Airtable automation** (see [Demo Runbook](docs/DEMO_RUNBOOK.md))

4. **Trigger screening:** Update Screen status → "Ready to Screen" in Airtable

### Option 2: Direct API Call

```bash
curl -X POST http://localhost:5001/screen \
  -H "Content-Type: application/json" \
  -d @sample_payload.json
```

**Complete Demo Guide:** [DEMO_RUNBOOK.md](docs/DEMO_RUNBOOK.md)

---

## Testing

```bash
# Run full test suite
pytest tests/

# Run with coverage report
pytest tests/ --cov=demo --cov-report=term-missing

# Run specific test modules
pytest tests/test_agentos_app.py -v
pytest tests/test_workflow.py -v
```

**Test Coverage:** 76% (exceeds 50% target)
**Test Files:** 15 files, ~1,500 lines
**Status:** 109 passed, 20 skipped

---

## Documentation

### Essential Reading

- **[Complete User Guide](docs/user_guide_comprehensive.md)** - For talent team users (Airtable workflow)
- **[Technical Reference](docs/technical/technical_reference.md)** - For developers (API, modules, testing)
- **[Design Synthesis](docs/technical/DESIGN_SYNTHESIS.md)** - For understanding architectural thinking (1,880 lines)

### Full Documentation Site

Run `uv run mkdocs serve` to browse the complete MkDocs documentation locally at `http://127.0.0.1:8000`.

**Navigation:** [Documentation Index](docs/index.md)

### Documentation Hierarchy

**Public-Facing (docs/):**
- `index.md` - Landing page with problem/solution framing
- `getting_started.md` - Local development setup
- `user_guide_comprehensive.md` - Complete user guide for talent teams
- `DEMO_RUNBOOK.md` - Demo execution guide
- `how_it_works/` - Architecture, Airtable integration, API reference
- `technical/` - Design synthesis, agent definitions, technical deep dives

**Internal Specifications (spec/):**
- `spec.md` - Primary technical specification (2,040+ lines, v1.0-minimal contract)
- `prd.md` - Product requirements and acceptance criteria
- `dev_reference/` - Implementation guides, Agno patterns, Airtable schema

---

## Case Study Context

This project was created as a case study for **FirstMark Capital's AI Lead role**, demonstrating:

1. **Product Thinking (25%):** Understanding of VC talent workflows and value creation
2. **Technical Design (25%):** Modern AI agent architecture with production-quality engineering
3. **Data Integration (20%):** Elegant handling of structured (Airtable) + unstructured (web) data
4. **Insight Generation (20%):** Evidence-based assessment with explainable reasoning trails
5. **Communication (10%):** Clear documentation showing thinking process

**Case Requirements Alignment:**
- ✅ **Structured + Unstructured Data Integration:** Airtable (structured) + web research (unstructured) via OpenAI Deep Research API
- ✅ **Candidate Identification & Ranking:** Evidence-aware scoring with ranked recommendations (0-100 scale)
- ✅ **Reasoning Trail:** Every assessment includes dimension-level scores, evidence quotes, citations, counterfactuals, and confidence levels

**Original Brief:** [docs/case/case_requirements.md](docs/case/case_requirements.md)  
**Presentation:** ✅ Delivered November 19, 2025 at 5:00 PM  
**Deliverables:**
- ✅ **Slide Deck:** [FMV_V1.1.pptx](docs/case/FMV_V1.1.pptx) - Problem framing, architecture, design decisions, production roadmap
- ✅ **Lightweight Prototype:** Python implementation with AgentOS runtime, 15+ candidate screenings executed
- ✅ **Comprehensive Documentation:** README + 9,000+ lines across 16 documentation files

---

## Contact & Contributing

**Author:** Will Bricker
**Purpose:** FirstMark Capital AI Lead case study
**Presentation Date:** November 19, 2025

For contribution guidelines, see [CONTRIBUTING.md](docs/contributing.md).

---

## License

[MIT License](LICENSE) - This is a case study project created for FirstMark Capital evaluation.
