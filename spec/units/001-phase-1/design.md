---
unit_id: "001-phase-1"
title: "Phase 1: Project Setup and Foundation"
version: "1.1"
created: "2025-01-16"
updated: "2025-11-17"
status: "completed"
---

# Phase 1: Project Setup and Foundation

Stable intent and acceptance criteria for establishing the minimal v1.0 project foundation

## Objective

**Summary:** Set up Python environment and install all required dependencies to prepare for agent implementation. Establish the minimal 5-file project structure and validate Pydantic models against spec schemas.

**Success Metrics:**

- Python 3.11+ environment active with all dependencies installed via uv
- All Pydantic models defined and validated against `spec/dev_reference/implementation_guide.md`
- Project ready for Phase 2 (Agent Implementation)

## Behavior

**Description:** Phase 1 establishes the foundational project setup without implementing any agent logic or workflows. It creates the minimal file structure, configures the development environment, installs all required packages, and defines Pydantic models that will be used throughout the implementation.

### Inputs

#### spec/dev_reference/implementation_guide.md

- **Type:** Markdown documentation
- **Description:** Canonical source for Pydantic model definitions
- **Examples:**
  - ExecutiveResearchResult schema (lines 113-162)
  - AssessmentResult schema (lines 358-382)
  - DimensionScore schema (lines 334-350)

#### .env.example

- **Type:** Environment variable template
- **Description:** Template for required configuration variables
- **Examples:**
  - `OPENAI_API_KEY=sk-...`
  - `AIRTABLE_API_KEY=pat...`
  - `AIRTABLE_BASE_ID=app...`

### Outputs

#### demo/ directory

- **Type:** Python package directory
- **Description:** Contains 5 core implementation files
- **Examples:**
  - `demo/app.py` (Flask webhook entrypoints)
  - `demo/agents.py` (agent creation + runners)
  - `demo/models.py` (Pydantic models)
  - `demo/airtable_client.py` (Airtable wrapper)
  - `demo/settings.py` (typed config/env loading with Pydantic BaseSettings)

#### models.py

- **Type:** Python module
- **Description:** Pydantic models validated against implementation guide
- **Examples:**
  - `ExecutiveResearchResult` class
  - `AssessmentResult` class
  - `DimensionScore` class
  - Supporting models: `Citation`, `CareerEntry`, `MustHaveCheck`

#### .env

- **Type:** Environment configuration file
- **Description:** Populated environment variables (gitignored)
- **Examples:**
  - All API keys configured
  - Flask host/port settings
  - Quality check thresholds

### Edge Cases

- **Scenario:** Python version < 3.11 detected
  - **Expected behavior:** Fail with clear error message directing user to upgrade

- **Scenario:** UV not installed
  - **Expected behavior:** Provide installation instructions for UV package manager

- **Scenario:** Required API keys missing from .env
  - **Expected behavior:** List missing keys and reference .env.example template

## Interfaces Touched

- Python environment configuration (.python-version file)
- Package dependency manifest (pyproject.toml)
- Environment variable schema (.env, .env.example)
- Pydantic model definitions (models.py)

## Data Shapes

- ExecutiveResearchResult (from spec/spec.md:415-419)
- AssessmentResult (from spec/spec.md:421-425)
- DimensionScore (from spec/spec.md:427-431)
- Citation (supporting model)
- CareerEntry (supporting model)
- MustHaveCheck (supporting model)

## Constraints

### Functional

- Must use Python 3.11+ as specified in `.python-version`
- Must use UV package manager (not pip) for dependency management
- Exactly 5 files in `demo/` directory for v1.0-minimal scope
- Pydantic models must match `spec/dev_reference/implementation_guide.md` schemas exactly
- No implementation code in Phase 1 (setup only, no agent/workflow logic)

### Non-Functional

- Setup should complete in < 15 minutes on standard development machine
- All dependencies must install without compilation (pure Python or wheels)
- .env file must never be committed (in .gitignore)
- Directory structure must match spec/spec.md:96-125

## Acceptance Criteria

### AC-PH1-01: Environment Ready

- **Given:** Clean development environment
- **When:** `python --version` is run
- **Then:** Output shows Python 3.11 or later
- **And:** `.python-version` file exists with content `3.11`
- **And:** `uv pip list` shows all required packages: agno-ai, pydantic, flask, pyairtable, python-dotenv
- **Testable:** ✅

### AC-PH1-02: Configuration Complete

- **Given:** Project root directory
- **When:** Environment files are checked
- **Then:** `.env` exists with all required variables (OPENAI_API_KEY, AIRTABLE_API_KEY, AIRTABLE_BASE_ID, FLASK_HOST, FLASK_PORT, USE_DEEP_RESEARCH, MIN_CITATIONS)
- **And:** `.env.example` exists as template with placeholder values
- **And:** `.gitignore` includes `.env` entry
- **Testable:** ✅

### AC-PH1-03: Pydantic Models Validated

- **Given:** `demo/models.py` file created
- **When:** Models are imported in Python REPL
- **Then:** All models can be instantiated without errors
- **And:** Field types match `spec/dev_reference/implementation_guide.md` exactly
- **And:** Models include: ExecutiveResearchResult, AssessmentResult, DimensionScore, Citation, CareerEntry, MustHaveCheck
- **Testable:** ✅

### AC-PH1-04: Project Structure Complete

- **Given:** Project root directory
- **When:** Directory structure is validated
- **Then:** All 5 files exist in `demo/` directory (app.py, agents.py, models.py, airtable_client.py, settings.py)
- **And:** `tmp/` directory exists for Agno session database
- **And:** `tests/` directory exists with placeholder files (test_scoring.py, test_quality_check.py, test_workflow_smoke.py)
- **And:** Structure matches spec/spec.md:96-125
- **Testable:** ✅

### AC-PH1-05: Settings Module Complete

- **Given:** `demo/settings.py` file created
- **When:** Settings module is imported and used
- **Then:** Module loads successfully with typed Pydantic BaseSettings classes
- **And:** All 5 config sections are defined (AppConfig, OpenAIConfig, AirtableConfig, FlaskConfig, QualityCheckConfig)
- **And:** Settings can be imported via `from demo.settings import settings`
- **And:** `tests/test_settings.py` exists with comprehensive test coverage
- **Testable:** ✅

## Dependencies

**Blocks:**

- 002-phase-2-agents (cannot implement agents without models and environment)

**Blocked by:** None (initial setup phase)

## Notes

- This is the foundation phase - no agent implementation or business logic
- All files in `demo/` can be stub/skeleton implementations in Phase 1
- Focus on structural correctness and dependency readiness
- Pydantic model validation is critical - these are referenced throughout spec
- Estimated time: 2 hours (from spec/spec.md:1068)
- Reference checklist: spec/spec.md:1069-1075
