# CLAUDE.md

---
## ⚠️ V1 CRITICAL SCOPE - READ FIRST

**Architecture:** Linear workflow ONLY (Deep Research → Quality Check → Optional Single Incremental Search → Assessment)
**Tables:** 6 tables (People, Portco, Portco_Roles, Role_Specs, Searches, Assessments)
**Storage:** Research data in **Assessments** table (research_structured_json, research_markdown_raw, assessment_json, assessment_markdown_report)
**Database:** SqliteDb at `tmp/agno_sessions.db` (NO InMemoryDb, NO custom WorkflowEvent tables)
**Pipeline:** Direct structured outputs via `output_schema` (NO parser agent)

**Phase 2+ (DO NOT IMPLEMENT):** Fast mode | Loops/conditions | Parser agents | Workflows table | Research_Results table | Multi-iteration search

**Authority:** `spec/v1_minimal_spec*.md` > `spec/prd.md` > `spec/dev_reference/implementation_guide.md`

**Before ANY architectural work:**
1. Read spec/v1_minimal_spec.md + addendum
2. Build explicit design model
3. Scope filter (what to DELETE) before detail check
4. If unsure → ASK, cite conflict + sources

---

## Project Overview

**Mission:** Talent Signal Agent - AI-powered executive matching for FirstMark Capital portfolio companies
**Presentation:** Nov 19, 2025 5pm
**Framework:** Agno (Python agent framework)

**Status:** ✅ READY FOR IMPLEMENTATION
- All specs aligned with v1 minimal scope
- Master implementation guide: `spec/dev_reference/implementation_guide.md`
- Estimated: 34-38 hours implementation

## Deliverables

1. **Presentation:** 1-2 page write-up or slide deck (problem framing, agent design, architecture, production considerations)
2. **Prototype:** Python implementation using Agno framework (data ingestion → research → assessment → ranked recommendations with reasoning)
3. **Documentation:** README or Loom video explaining implementation

## Evaluation Criteria
- Product Thinking (25%): VC/talent workflow understanding
- Technical Design (25%): Modern LLM/agent frameworks, modular design, retrieval/context/prompting
- Data Integration (20%): Structured + unstructured data handling
- Insight Generation (20%): Explainable, ranked outputs with reasoning
- Communication (10%): Clear explanation of approach and next steps

## Technology Stack

**Core:**
- Python 3.11+ (uv package manager) + virtual environment in `.venv/`
- Agno framework (agent orchestration) - see `spec/dev_reference/AGNO_REFERENCE.md`
- OpenAI: o4-mini-deep-research (research), gpt-5/gpt-5-mini (assessment)
- Airtable (6 tables) + Flask webhook + ngrok
- Pydantic (structured outputs via `output_schema`)

**Dependencies:**
- flask, pyairtable, openai, python-dotenv, pydantic

**Demo Data:**
- 64 executives from `reference/guildmember_scrape.csv`
- 4 scenarios: Pigment CFO, Mockingbird CFO, Synthesia CTO, Estuary CTO
- 3 pre-runs + 1 live demo

## Documentation Hierarchy

**Authority (in order):**
1. `spec/v1_minimal_spec.md` + `spec/v1_minimal_spec_agno_addendum.md` (HIGHEST)
2. `spec/prd.md` - Product requirements
3. `spec/spec.md` - Technical specification
4. `spec/dev_reference/implementation_guide.md` ⭐ MASTER IMPLEMENTATION DOC
5. `spec/dev_reference/airtable_ai_spec.md` - Airtable schema (6 tables)
6. `spec/dev_reference/role_spec_design.md` - CFO/CTO templates
7. `spec/dev_reference/AGNO_REFERENCE.md` - Framework patterns

**V1 Exclusions (Phase 2+ Only):**
- Parser agent pipeline | Workflows/Research_Results tables | Fast mode | Multi-iteration loops | Async processing

## Key Design Decisions

**Scope:**
- Module 4 (Screen workflow) ONLY - Modules 1-3 pre-populated manually
- Linear workflow: Deep Research → Quality Check → Optional Incremental Search → Assessment
- Synchronous/sequential processing (async deferred to Phase 2+)

**Data & Integration:**
- Airtable (6 tables) via Flask webhook + ngrok
- Deep Research API (o4-mini-deep-research) + Web Search builtin
- No third-party search APIs (LinkedIn/web via Deep Research only)
- Direct structured outputs via Pydantic (no parser agent)

**Assessment:**
- Spec-guided assessment with evidence-aware scoring
- LLM self-assessment confidence + evidence count threshold
- Counterfactuals: "Why candidate might NOT be ideal" + key assumptions

**V1 Simplifications:**
- No candidate profiles (bespoke research per role)
- No deduplication (assume clean data)
- No Apollo enrichment (stub/mock only)
- Standard Airtable views (no custom UI)

## Development Principles

**Constraints:** 48 hours | Demonstrate quality of thinking | Minimal, quick-to-stand-up components

**Decision Matrix:**
```
always          → explain → code → verify
ambiguous?      → clarify
existing_code?  → change_minimum
new_feature?    → MVP → validate → expand
```

**Prioritization:**
Simple > Perfect | Clear > Clever | Working > Optimal | Request > BestPractice | Smaller > Larger

**Process:** Understand → Plan → Code → Test → Validate

**Key Rules:**
- **SIMPLICITY:** Minimal changes | No feature creep | Smallest working increment | Target <100 LOC per change
- **QUALITY:** Types, docstrings, comments | No placeholders | Complete code
- **COMMUNICATION:** Clarify ambiguity | Never assume, always verify

**Strategic Focus:**
1. Domain calibration before solution design (VC/talent workflow understanding first)
2. Incremental value delivery (complete value units, not infrastructure speculation)
3. Maximize expected value (quick wins that demonstrate thinking quality)
4. Context engineering for AI (domain-specific knowledge injection)

## Implementation Roadmap (34-38 hours)

1. **Airtable Setup** - Configure 6 tables with schema
2. **Python Core** - Research + Assessment agents (direct structured outputs)
3. **Workflow** - Flask webhook + Agno linear workflow integration
4. **Pre-runs** - Execute Pigment CFO, Mockingbird CFO, Synthesia CTO
5. **Demo Prep** - Live scenario: Estuary CTO

**Goal:** Minimal, working prototype (Module 4 only) demonstrating quality of thinking
