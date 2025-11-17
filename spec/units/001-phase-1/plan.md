---
unit_id: "001-phase-1"
version: "1.0"
created: "2025-01-16"
updated: "2025-01-16T22:30:00"
---

# Phase 1: Project Setup and Foundation - Implementation Plan

Volatile task breakdown and verification plan for establishing minimal v1.0 foundation

## Tasks

### TK-01: Create Project Directory Structure

- **Title:** Create minimal 5-file project structure
- **Description:** Create the foundational directory structure with demo/, tmp/, and tests/ directories. Create skeleton files for all 5 core modules (app.py, agents.py, models.py, airtable_client.py, settings.py) with module docstrings only. Create placeholder test files in tests/.
- **Files:**
  - `demo/app.py`
  - `demo/agents.py`
  - `demo/models.py`
  - `demo/airtable_client.py`
  - `demo/settings.py`
  - `demo/__init__.py`
  - `tmp/.gitkeep`
  - `tests/test_scoring.py`
  - `tests/test_quality_check.py`
  - `tests/test_workflow_smoke.py`
  - `tests/__init__.py`
- **Status:** ready
- **Priority:** high
- **Estimate:** 15 minutes
- **Dependencies:** None
- **Acceptance Criteria:** AC-PH1-04 (partial - directory structure)
- **Note:** Skeleton files only - no implementation code yet
- **Completed:** null

### TK-02: Configure Python Environment

- **Title:** Set up Python 3.11+ with .python-version
- **Description:** Create .python-version file with content "3.11". Verify Python 3.11+ is active. Document Python version requirements in project root.
- **Files:**
  - `.python-version`
- **Status:** done
- **Priority:** high
- **Estimate:** 5 minutes
- **Dependencies:** None
- **Acceptance Criteria:** AC-PH1-01 (partial - Python version)
- **Note:** User must have Python 3.11+ installed; provide clear error if not
- **Completed:** 2025-01-16 (pre-existing)

### TK-03: Create pyproject.toml with Dependencies

- **Title:** Define all project dependencies
- **Description:** Create pyproject.toml with project metadata and all required dependencies (agno-ai>=0.1.0, pydantic>=2.5.0, flask>=3.0.0, pyairtable>=2.0.0, python-dotenv>=1.0.0). Include dev dependencies (pytest>=7.4.0, ruff>=0.1.0, mypy>=1.7.0). Follow spec/spec.md:559-586 for exact versions.
- **Files:**
  - `pyproject.toml`
- **Status:** ready
- **Priority:** high
- **Estimate:** 15 minutes
- **Dependencies:** TK-02
- **Acceptance Criteria:** AC-PH1-01 (partial - dependency manifest)
- **Note:** Use exact version constraints from spec
- **Completed:** null

### TK-04: Install Dependencies with UV

- **Title:** Install all packages via uv
- **Description:** Run `uv pip install -e .` to install project in editable mode with all dependencies. Verify installation with `uv pip list` showing all required packages. Document any installation issues or requirements.
- **Files:** None (installation only)
- **Status:** ready
- **Priority:** high
- **Estimate:** 10 minutes
- **Dependencies:** TK-03
- **Acceptance Criteria:** AC-PH1-01 (complete - all packages installed)
- **Note:** Requires uv to be installed; provide installation instructions if missing
- **Completed:** null

### TK-05: Create Environment Configuration Files

- **Title:** Set up .env and .env.example templates
- **Description:** Create .env.example with all required environment variables as placeholders (OPENAI_API_KEY, AIRTABLE_API_KEY, AIRTABLE_BASE_ID, FLASK_HOST, FLASK_PORT, USE_DEEP_RESEARCH, MIN_CITATIONS, APP_NAME, APP_ENV, DEBUG, LOG_LEVEL). Copy to .env for user to populate. Update .gitignore to exclude .env. Follow spec/spec.md:737-761.
- **Files:**
  - `.env.example`
  - `.env`
  - `.gitignore`
- **Status:** doing
- **Priority:** high
- **Estimate:** 15 minutes
- **Dependencies:** TK-01
- **Acceptance Criteria:** AC-PH1-02 (complete)
- **Note:** Partial completion - .env and .gitignore exist, but .env.example missing
- **Completed:** null

### TK-06: Implement Pydantic Models

- **Title:** Define all Pydantic models from implementation guide
- **Description:** Implement all 6 Pydantic models in demo/models.py following spec/dev_reference/implementation_guide.md exactly: Citation, CareerEntry, ExecutiveResearchResult, MustHaveCheck, DimensionScore, AssessmentResult. Include all fields, types, constraints, and docstrings. Use Optional[int] for evidence-aware scores (not 0 or NaN). Add module-level docstring and imports.
- **Files:**
  - `demo/models.py`
- **Status:** ready
- **Priority:** high
- **Estimate:** 45 minutes
- **Dependencies:** TK-04
- **Acceptance Criteria:** AC-PH1-03 (complete)
- **Note:** Critical task - models are referenced throughout entire implementation
- **Completed:** null

### TK-07: Validate Pydantic Models

- **Title:** Test model instantiation and validation
- **Description:** Create simple validation script or REPL session to instantiate all 6 Pydantic models with sample data. Verify field types, constraints, and optional fields work correctly. Document any validation issues. Ensure models match spec exactly.
- **Files:**
  - `tests/test_models_validation.py` (optional validation script)
- **Status:** ready
- **Priority:** high
- **Estimate:** 20 minutes
- **Dependencies:** TK-06
- **Acceptance Criteria:** AC-PH1-03 (validation)
- **Note:** Can be manual REPL testing or automated test - focus on correctness
- **Completed:** null

### TK-08: Create README with Setup Instructions

- **Title:** Document Phase 1 setup and next steps
- **Description:** Create or update README.md with Phase 1 setup instructions (Python version, UV installation, dependency installation, environment configuration). Include verification commands to check setup is complete. Document next steps for Phase 2. Keep concise and actionable.
- **Files:**
  - `README.md`
- **Status:** ready
- **Priority:** medium
- **Estimate:** 20 minutes
- **Dependencies:** TK-04, TK-05, TK-07
- **Acceptance Criteria:** Documentation complete for Phase 1
- **Note:** User-facing documentation - clarity is critical
- **Completed:** null

### TK-09: Verify Phase 1 Completion

- **Title:** Run all verification checks
- **Description:** Execute all verification commands (python --version, uv pip list, model imports, directory structure check). Confirm all acceptance criteria (AC-PH1-01 through AC-PH1-04) are met. Document any issues or deviations. Update status to complete if all checks pass.
- **Files:** None (verification only)
- **Status:** ready
- **Priority:** high
- **Estimate:** 15 minutes
- **Dependencies:** TK-01, TK-02, TK-04, TK-05, TK-06, TK-07, TK-08
- **Acceptance Criteria:** All AC-PH1-* criteria validated
- **Note:** Final gate before Phase 2 - all criteria must pass
- **Completed:** null

## Verification

### Commands

1. **python --version** - Verify Python 3.11+ (must pass: ✅)
2. **uv pip list** - Verify all dependencies installed (must pass: ✅)
3. **python -c "from demo.models import ExecutiveResearchResult, AssessmentResult, DimensionScore, Citation, CareerEntry, MustHaveCheck; print('Models imported successfully')"** - Verify models load (must pass: ✅)
4. **ls -la demo/ tmp/ tests/** - Verify directory structure (must pass: ✅)
5. **test -f .env && test -f .env.example && grep -q ".env" .gitignore** - Verify environment config (must pass: ✅)

### Gates

- **structure:** Directory structure matches spec (must pass: ✅)
- **environment:** Python 3.11+ with all dependencies (must pass: ✅)
- **models:** All Pydantic models defined and importable (must pass: ✅)
- **config:** Environment files configured (must pass: ✅)
- **documentation:** README documents setup (must pass: ✅)

### Coverage Target

50% (0.50) - Per constitution.md:62, case study target is 50% coverage for core logic. Phase 1 has no logic to test, so coverage not applicable for this unit.

### Acceptance References

- AC-PH1-01: Environment Ready (TK-02, TK-03, TK-04)
- AC-PH1-02: Configuration Complete (TK-05)
- AC-PH1-03: Pydantic Models Validated (TK-06, TK-07)
- AC-PH1-04: Project Structure Complete (TK-01)

## Status

- **Progress:** 11%
- **Tasks Completed:** 1/9 (TK-02 done, TK-05 in progress)
- **Created:** 2025-01-16
- **Updated:** 2025-01-16
- **Status:** in_progress
- **Estimated Total Time:** 2.5 hours (150 minutes)
- **Time Remaining:** ~2.3 hours (140 minutes)

**Current State Notes:**
- ✅ Python 3.11.10 active with .python-version file
- ✅ Some packages already installed (agno 2.2.13, pydantic 2.12.4, openai 2.8.0, python-dotenv 1.2.1)
- ⚠️ pyproject.toml exists but dependencies array is empty - needs population
- ⚠️ .env and .gitignore exist, but .env.example missing
- ❌ demo/, tmp/, tests/ directories not created yet
- ❌ No skeleton files created yet

## Notes

### Implementation Order Rationale

1. **Structure First (TK-01, TK-02):** Establish directory layout and Python version before dependencies
2. **Dependencies (TK-03, TK-04):** Install packages needed for model implementation
3. **Configuration (TK-05):** Set up environment before implementing code that uses it
4. **Models (TK-06, TK-07):** Core data structures - critical for all subsequent phases
5. **Documentation & Verification (TK-08, TK-09):** Final validation and handoff to Phase 2

### Critical Path

TK-02 → TK-03 → TK-04 → TK-06 → TK-07 → TK-09

All other tasks can be parallelized or interleaved with critical path.

### Known Risks

1. **UV not installed:** Provide clear installation instructions
2. **Python version mismatch:** Document upgrade path for Python 3.11+
3. **API keys missing:** .env.example provides template, but user must populate
4. **Model schema drift:** Lock to spec/dev_reference/implementation_guide.md as single source of truth

### Phase 2 Readiness

Phase 1 completes when:

- All 9 tasks marked complete
- All verification commands pass
- All acceptance criteria (AC-PH1-01 through AC-PH1-04) validated
- README documents setup process
- Phase 2 can begin agent implementation immediately
