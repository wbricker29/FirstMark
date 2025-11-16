# FirstMark Talent Signal Agent - Quick Reference

## Key Documentation Files (Absolute Paths)

### Planning & Architecture
- **Master Planning**: `/home/user/FirstMark/case/wbcasenotes_v1.md` (674 lines - MOST DETAILED)
  - All workflow design decisions
  - Architecture options evaluated
  - Components breakdown
  - Production considerations
  
- **Case Requirements**: `/home/user/FirstMark/case/case_brief.md` (76 lines)
  - Official deliverables
  - Evaluation rubric (25% Product, 25% Tech Design, 20% Data, 20% Insight, 10% Communication)
  - Data input/output specifications

- **Data Schema**: `/home/user/FirstMark/case/data_schema.md` (40 lines)
  - Mock_Guilds.csv schema (17 fields)
  - Exec_Network.csv schema (16 fields)

### Project Guidelines
- **Development Requirements**: `/home/user/FirstMark/REQUIREMENTS.md`
- **Project Guidelines**: `/home/user/FirstMark/AGENTS.md`
- **Claude Code Instructions**: `/home/user/FirstMark/CLAUDE.md`

## Existing Scripts (Node.js Data Prep)

### Purpose: Scrape & Process FirstMark Portfolio
- **Scraper**: `/home/user/FirstMark/scripts/scrape_companies.js` - Puppeteer-based web scraping
- **Processor**: `/home/user/FirstMark/scripts/process_portfolio.js` - Data transformation
- **Exporter**: `/home/user/FirstMark/scripts/create_summary.js` - CSV/MD generation
- **Guide**: `/home/user/FirstMark/scripts/README.md` - Full documentation

## Research Materials
- **Firm Analysis**: `/home/user/FirstMark/research/Firm_DeepResearch.md` (99KB)
- **Partner Research**: `/home/user/FirstMark/research/member_research/` directory
- **Interview Prep**: `/home/user/FirstMark/research/interviewprompt.md`

## Critical Design Decisions Summary

### Selected Approach
1. **Research**: OpenAI Deep Research API (not custom agent)
2. **Enrichment**: Mock Apollo responses (not real API integration)
3. **Assessment**: Dual evaluation (rubric-guided + self-generated)
4. **Database**: SQLite for demo, Supabase future-ready
5. **Candidate Profiles**: SKIPPED for demo (can extend)
6. **Ingestion**: Simple Python CSV parsing (not LLM)
7. **UI**: Markdown + JSON outputs (optional Streamlit later)
8. **Framework**: Lean toward custom Python (KISS principle)

### Deferred Decisions
- Vector store selection (defer to MVP)
- Investigation interface implementation (CLI/UI/Notebook)
- Real Apollo API integration (MVP phase)
- Confidence scoring mechanics (H/M/L + percentage)
- Counterfactual generation method

## Workflow Architecture at a Glance

```
INPUT DATA
├── Structured: Mock_Guilds.csv, Exec_Network.csv
├── Unstructured: Executive bios (text), Job descriptions (text)
└── FirstMark Portfolio: Via scrape_companies.js

FOUR MAIN WORKFLOWS
1. Data Ingestion        → Load CSVs, normalize, store in SQLite
2. Role Spec Generation  → LLM creates standardized role specs
3. Research + Assessment → OpenAI API research + LLM evaluation
4. Ranking & Reporting   → Aggregate scores, output results

OUTPUTS
├── Ranked candidates (JSON + Markdown)
├── Assessment scorecards (per candidate)
├── Research trails (with citations)
└── Comparative analysis (why #1 beats #2)
```

## Status at a Glance

| Phase | Status |
|-------|--------|
| Planning & Design | ✅ Complete |
| Documentation | ✅ Complete |
| Mock Data Generation | ❌ Not started |
| Python Implementation | ❌ Not started |
| API Integration | ❌ Not started |
| Testing | ❌ Not started |
| Presentation Materials | ⏳ In progress |

## Timeline Constraint
- **Presentation Date**: 5 PM on 11/19 (3 days from Nov 16)
- **Available Time**: ~48 hours
- **Evaluation Panel**: Beth Viner, Shilpa Nayyar, Matt Turck, Adam Nelson

## What Doesn't Exist Yet

### Python Code (All Missing)
- No main orchestration script
- No data ingestion pipeline
- No role spec generator
- No research wrapper
- No assessment engine
- No ranking logic
- No database setup scripts

### Data (All Missing)
- No Mock_Guilds.csv
- No Exec_Network.csv
- No executive bio text files
- No job description files
- No SQLite database

### Infrastructure (All Missing)
- No API connections (OpenAI, Apollo)
- No vector store setup
- No database schemas created
- No environment setup (Python venv, dependencies)

## Next Immediate Actions (Critical Path)

**Next 2 hours (TODAY)**:
1. Generate mock data CSVs (8-12 guild members each guild, 15-20 network execs)
2. Generate bio text files (10-15 executive profiles)
3. Generate job description files (3-5 open roles: CFO/CTO)
4. Set up Python project structure

**Next 4-6 hours (TODAY)**:
1. Data ingestion pipeline (CSV → SQLite)
2. Role spec generator (LLM-based)
3. Candidate researcher (OpenAI Deep Research wrapper)

**Next 6-8 hours (TOMORROW)**:
1. Assessment engine (structured LLM evaluation)
2. Ranking logic (score aggregation)
3. End-to-end pipeline integration

**Final 4-6 hours (BEFORE PRESENTATION)**:
1. Run full demo pipeline
2. Create presentation write-up (1-2 pages)
3. Prepare talking points
4. Test all components

---

## Repository File Locations (Key Files)

```
/home/user/FirstMark/
├── case/
│   ├── case_brief.md                    ← Official requirements
│   ├── data_schema.md                   ← Database schema definitions
│   ├── wbcasenotes_v1.md                ← DETAILED ARCHITECTURE (PRIMARY)
│   └── archive/                         ← Previous versions
├── scripts/
│   ├── scrape_companies.js              ← Web scraper
│   ├── process_portfolio.js             ← Data transformer
│   ├── create_summary.js                ← CSV exporter
│   └── README.md                        ← Script documentation
├── research/
│   ├── Firm_DeepResearch.md             ← Firm analysis
│   ├── member_research/                 ← Partner deep dives
│   └── interview_research/              ← Role context
├── REQUIREMENTS.md                      ← Dev guidelines
├── AGENTS.md                            ← Architecture guidelines
├── CLAUDE.md                            ← Claude Code instructions
└── README.md                            ← Project overview
```

---

**Use this as reference while implementing the Python agent system.**
