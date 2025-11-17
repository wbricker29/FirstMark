# Talent Signal Agent

AI-powered executive matching for FirstMark Capital portfolio companies.

## Overview

Working directory for all information and projects related to Will Bricker's evaluation for the role of AI Lead at FirstMark Capital.

**Case Study:** Prototype AI agent for matching executives with portfolio company roles.

## Phase 1: Project Setup (✅ COMPLETE)

The foundational setup has been completed. All dependencies are installed and Pydantic models are validated.

### Prerequisites

- Python 3.11+ (verified with `.python-version`)
- UV package manager (for dependency management)

### Setup Instructions

1. **Verify Python Version**
   ```bash
   python --version  # Should show Python 3.11+
   ```

2. **Install UV** (if not already installed)
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Install Dependencies**
   ```bash
   uv pip install -e .
   ```

4. **Configure Environment Variables**
   - Copy `.env.example` to `.env`
   - Populate required API keys:
     - `OPENAI_API_KEY`: OpenAI API key
     - `AIRTABLE_API_KEY`: Airtable personal access token
     - `AIRTABLE_BASE_ID`: Airtable base ID

5. **Verify Installation**
   ```bash
   # Check all packages installed
   uv pip list | grep -E "(agno|pydantic|flask|pyairtable|dotenv)"

   # Verify models can be imported
   .venv/bin/python -c "from demo.models import ExecutiveResearchResult, AssessmentResult; print('✅ Models loaded')"

   # Run model validation tests
   .venv/bin/python tests/test_models_validation.py
   ```

### Project Structure

```
demo/                      # 5-file v1.0 implementation
├── __init__.py           # Package initialization
├── app.py                # Flask webhook server
├── agents.py             # Agno agent definitions
├── models.py             # Pydantic data models (✅ implemented)
├── airtable_client.py    # Airtable API wrapper
└── settings.py           # Configuration/env loading

tmp/                       # Agno session database location
tests/                     # Test suite
├── test_models_validation.py  # ✅ Model validation tests
├── test_scoring.py       # Dimension scoring tests (Phase 2)
├── test_quality_check.py # Research quality tests (Phase 2)
└── test_workflow_smoke.py # End-to-end tests (Phase 2)

spec/                      # Technical specifications
├── constitution.md       # Project governance
├── prd.md                # Product requirements
├── spec.md               # Technical spec
└── units/001-phase-1/    # Phase 1 design & plan
```

### What's Complete

- ✅ Python 3.11+ environment configured
- ✅ All dependencies installed via UV
- ✅ Environment configuration files (.env, .env.example, .gitignore)
- ✅ Project directory structure (demo/, tmp/, tests/)
- ✅ All 6 Pydantic models implemented and validated
  - Citation
  - CareerEntry
  - ExecutiveResearchResult
  - DimensionScore
  - MustHaveCheck
  - AssessmentResult

### Next Steps (Phase 2)

Phase 2 will implement:
- Deep Research Agent (o4-mini-deep-research)
- Incremental Search Agent (gpt-5-mini with web search)
- Assessment Agent (gpt-5-mini with ReasoningTools)
- Agno Workflow orchestration
- Flask webhook server
- Airtable integration

See `spec/units/002-phase-2/` for Phase 2 implementation plan.

## Case Study Resources

- **Directory:** `case/`
- **Brief:** `case/FirstMark_case.md`
- **Specifications:** `spec/`
- **Reference Materials:** `reference/`
