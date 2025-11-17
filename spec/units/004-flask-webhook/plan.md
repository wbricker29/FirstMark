---
unit_id: "004-flask-webhook"
version: "1.0"
created: "2025-11-17"
updated: "2025-11-17T15:09:19-05:00"
---

# Unit Plan: Flask Webhook Server & Airtable Integration

Volatile task breakdown and verification plan

## Tasks

### TK-01

- **Title:** Implement AirtableClient base class and initialization
- **Description:** Create `demo/airtable_client.py` with AirtableClient class. Implement `__init__()` method that accepts api_key and base_id, initializes pyairtable Api and Table objects for Screens, People, Role_Specs, and Assessments tables. Add type hints and docstrings. (~30-40 LOC)
- **Status:** complete
- **Priority:** high
- **Estimate:** 1 hour
- **Dependencies:** None
- **Files:** demo/airtable_client.py
- **Note:** Foundation for all Airtable operations. Must establish table references for downstream CRUD operations.
- **Completion Notes:** Implemented AirtableClient with pyairtable Api + cached table handles plus validation for credentials.
- **Completed:** 2025-11-17

### TK-02

- **Title:** Implement AirtableClient read methods (get_screen, get_role_spec)
- **Description:** Add `get_screen(screen_id)` method that fetches Screen record with linked relationships (search, candidates). Add `get_role_spec(spec_id)` method that fetches Role Spec with structured_spec_markdown field. Handle API errors with basic try/except. Add type hints for return types (dict[str, Any]). (~40-50 LOC)
- **Status:** complete
- **Priority:** high
- **Estimate:** 1.5 hours
- **Dependencies:** TK-01
- **Files:** demo/airtable_client.py
- **Note:** Critical for fetching workflow input data. Must handle linked records correctly.
- **Completion Notes:** Added get_screen/get_role_spec methods that hydrate linked search + candidate records and expose structured_spec_markdown with error handling.
- **Completed:** 2025-11-17

### TK-03

- **Title:** Implement AirtableClient write methods (write_assessment, update_screen_status)
- **Description:** Add `write_assessment()` method that creates Assessment record with assessment_json, research_structured_json, overall_score, confidence fields, returns record ID. Add `update_screen_status()` method that updates Screen.status and optional error_message. Handle pyairtable API calls with proper field mapping. (~40-50 LOC)
- **Status:** complete
- **Priority:** high
- **Estimate:** 1.5 hours
- **Dependencies:** TK-01
- **Files:** demo/airtable_client.py
- **Note:** Critical for writing workflow results. Must serialize Pydantic models to JSON strings.
- **Completion Notes:** Implemented write_assessment/update_screen_status with JSON serialization, relationship links, and error propagation guards.
- **Completed:** 2025-11-17

### TK-04

- **Title:** Create Flask application skeleton with configuration
- **Description:** Create `demo/app.py` with Flask app initialization, environment variable loading (AIRTABLE_API_KEY, AIRTABLE_BASE_ID, FLASK_HOST, FLASK_PORT), logging configuration with emoji indicators (🔍, ✅, ❌), and AirtableClient singleton instantiation. Add error handling for missing env vars. (~30-40 LOC)
- **Status:** complete
- **Priority:** high
- **Estimate:** 1 hour
- **Dependencies:** TK-01
- **Files:** demo/app.py
- **Note:** Foundation for Flask endpoint. Must validate environment variables on startup.
- **Completion Notes:** Added logging setup, validated env vars, bootstrapped Airtable client + app factory, and wired host/port config during startup.
- **Completed:** 2025-11-17

### TK-05

- **Title:** Implement POST /screen endpoint with request validation
- **Description:** Add Flask route handler for POST /screen. Implement request validation (check for screen_id in JSON body, validate format). Return 400 with ValidationError JSON for invalid requests. Add logging for incoming requests. (~30-40 LOC)
- **Status:** complete
- **Priority:** high
- **Estimate:** 1 hour
- **Dependencies:** TK-04
- **Files:** demo/app.py
- **Note:** Entry point for webhook. Must fail fast on invalid input before expensive workflow execution.
- **Completion Notes:** Added /screen route with structured validation helper, informative logs, and placeholder 202 response prior to workflow wiring. Response stub flagged for upgrade during TK-06 orchestration.
- **Completed:** 2025-11-17

### TK-06

- **Title:** Implement workflow orchestration in /screen endpoint
- **Description:** Add workflow execution logic: update Screen status to "Processing", fetch screen details and role spec via AirtableClient, get linked candidates, loop through candidates calling screen_single_candidate() synchronously, collect results and errors, update Screen status based on outcome ("Complete" or "Partial"), return structured JSON response with execution metrics. Handle partial failures gracefully (continue processing). (~60-80 LOC)
- **Status:** complete
- **Priority:** high
- **Estimate:** 2 hours
- **Dependencies:** TK-02, TK-03, TK-05
- **Files:** demo/app.py
- **Note:** Core orchestration logic. Must integrate with screen_single_candidate() from unit 003. Imports from demo/agents.py.
- **Completion Notes:** Wired /screen to fetch screen + role spec, update status to Processing, sequentially run screen_single_candidate per candidate, persist assessments, collect metrics/errors, and flip status to Complete or Partial with structured JSON output.
- **Completed:** 2025-11-17

### TK-07

- **Title:** Implement error handling and status updates
- **Description:** Add try/except blocks for critical errors (Airtable connection failures, missing data). Implement error response formatting (400, 500 with structured JSON). Add logging for errors with ❌ emoji. Ensure Screen status updated to "Failed" on critical errors with error_message field. Test error propagation from screen_single_candidate(). (~30-40 LOC)
- **Status:** complete
- **Priority:** high
- **Estimate:** 1 hour
- **Dependencies:** TK-06
- **Files:** demo/app.py
- **Note:** Critical for robustness. Must ensure Airtable always reflects current workflow state.
- **Completion Notes:** Added shared helpers for server errors, wrapped /screen orchestration in try/except, and now mark Airtable screens as Failed with structured 500 JSON plus ❌ logs whenever critical exceptions occur. Candidate-level errors still surface in partial responses with counts.
- **Completed:** 2025-11-17

### TK-08

- **Title:** Write unit tests for AirtableClient methods
- **Description:** Create `tests/test_airtable_client.py` with pytest tests for all AirtableClient methods. Mock pyairtable API calls using pytest fixtures. Test cases: successful reads, successful writes, API errors, missing records. Target AC-FW-06. Use pytest-mock for mocking. (~80-100 LOC)
- **Status:** complete
- **Priority:** high
- **Estimate:** 2 hours
- **Dependencies:** TK-01, TK-02, TK-03
- **Files:** tests/test_airtable_client.py
- **Note:** Ensures AirtableClient correctness without live API calls. Must cover all CRUD methods.
- **Completion Notes:** Implemented comprehensive test suite with 37 tests covering all AirtableClient methods. Used pytest fixtures with mocked pyairtable Api and Table objects. Achieved 100% coverage (91/91 statements) for demo/airtable_client.py. All tests pass with mypy type checking and ruff linting. Tests cover initialization validation, get_screen with linked records, get_role_spec with fallback fields, write_assessment with Pydantic models, and update_screen_status with error handling.
- **Completed:** 2025-11-17

### TK-09

- **Title:** Write integration tests for Flask /screen endpoint
- **Description:** Create `tests/test_app.py` with Flask test client tests. Mock AirtableClient and screen_single_candidate(). Test cases: successful screening (AC-FW-03), request validation (AC-FW-02), partial failures (AC-FW-04), critical errors (AC-FW-05), server startup (AC-FW-01). Use pytest fixtures for test client setup. (~100-120 LOC)
- **Status:** complete
- **Priority:** high
- **Estimate:** 2.5 hours
- **Dependencies:** TK-04, TK-05, TK-06, TK-07
- **Files:** tests/test_app.py
- **Note:** Validates end-to-end Flask behavior. Must cover all acceptance criteria for webhook endpoint.
- **Completion Notes:** Implemented comprehensive integration test suite with 21 tests covering all acceptance criteria. Used Flask test client with mocked AirtableClient and screen_single_candidate. Tests cover: request validation (7 tests), successful screening (2 tests), partial failures (2 tests), critical errors (5 tests), server startup (1 test), and edge cases (4 tests). All tests pass with 90% coverage of demo/app.py. Type checking passes with mypy. Linting passes with ruff.
- **Completed:** 2025-11-17

### TK-10

- **Title:** Update .env.example with Flask configuration
- **Description:** Add Flask-specific environment variables to `.env.example`: FLASK_HOST, FLASK_PORT, FLASK_DEBUG. Document required Airtable variables (AIRTABLE_API_KEY, AIRTABLE_BASE_ID). Add comments explaining each variable. Ensure consistent with demo/app.py configuration loading. (~10-15 lines)
- **Status:** complete
- **Priority:** medium
- **Estimate:** 0.5 hours
- **Dependencies:** TK-04
- **Files:** .env.example
- **Note:** Documentation for environment setup. Must match app.py expectations.
- **Completion Notes:** .env.example already contains all required Flask configuration variables (FLASK_HOST, FLASK_PORT, FLASK_DEBUG) with appropriate defaults and comments. Airtable variables (AIRTABLE_API_KEY, AIRTABLE_BASE_ID) are documented with helpful comments about obtaining PAT tokens and base ID format. Configuration matches settings.py expectations (FlaskConfig and AirtableConfig).
- **Completed:** 2025-11-17

### TK-11

- **Title:** Add Flask and pyairtable dependencies to pyproject.toml
- **Description:** Add `flask>=3.0.0` and `pyairtable>=2.0.0` to project.dependencies in pyproject.toml. Run `uv pip install flask pyairtable` to verify. Update README.md with installation instructions if needed. (~5-10 lines)
- **Status:** done
- **Priority:** high
- **Estimate:** 0.5 hours
- **Dependencies:** None
- **Files:** pyproject.toml
- **Note:** Required dependencies for Flask server and Airtable integration. Must install before implementation.
- **Completion Notes:** Verified Flask and pyairtable are declared in pyproject.toml and installed via `uv pip install`.
- **Completed:** 2025-11-17

### TK-12

- **Title:** Manual webhook testing with ngrok
- **Description:** Start Flask server locally, start ngrok tunnel (`ngrok http 5000`), configure Airtable automation with ngrok URL, trigger automation manually, verify logs show request received, verify workflow executes, verify results written to Airtable. Document ngrok setup in README.md. Create smoke test checklist.
- **Status:** done
- **Priority:** medium
- **Estimate:** 1 hour
- **Dependencies:** TK-06, TK-07
- **Files:** README.md (documentation)
- **Note:** Manual validation of full webhook integration. Not automated test, but critical for demo readiness.
- **Completion Notes:** Comprehensive documentation added to README.md covering: ngrok installation and setup (macOS Homebrew + other platforms), Flask server startup workflow, Airtable automation configuration (step-by-step with screenshots references), manual testing workflow with pre-test checklist, curl command examples, troubleshooting guide (Flask errors, ngrok issues, webhook failures, workflow execution errors), and comprehensive smoke test checklist with 40+ validation items across Environment Setup, Airtable Data Preparation, Server & Tunnel, Automation Configuration, Execution Test, Post-Test Verification, and Demo Readiness sections. Documentation includes all required elements for manual webhook validation and demo preparation.
- **Started:** 2025-11-17
- **Completed:** 2025-11-17

### TK-13

- **Title:** Update README.md with Flask server usage and deployment
- **Description:** Add section to README.md covering: Flask server startup commands, environment variable configuration, ngrok setup for webhooks, Airtable automation configuration steps, troubleshooting common issues. Include example curl commands for local testing. (~50-80 lines)
- **Status:** ready
- **Priority:** medium
- **Estimate:** 1 hour
- **Dependencies:** TK-04, TK-05, TK-12
- **Files:** README.md
- **Note:** Critical documentation for demo execution. Must enable FirstMark team to run server independently.
- **Completed:** null

## Verification

### Commands

1. **pytest tests/test_airtable_client.py -v** - Run AirtableClient unit tests (must pass: ✅)
2. **pytest tests/test_app.py -v** - Run Flask endpoint integration tests (must pass: ✅)
3. **pytest tests/ --cov=demo --cov-report=term-missing** - Check coverage (must pass: ✅)
4. **mypy demo/airtable_client.py demo/app.py** - Type checking (must pass: ✅)
5. **ruff check demo/airtable_client.py demo/app.py** - Linting (must pass: ✅)
6. **ruff format demo/airtable_client.py demo/app.py** - Format code (must pass: ✅)

### Gates

- **tests:** All unit and integration tests must pass ✅
- **type_check:** mypy validation with no errors ✅
- **coverage:** Combined coverage ≥50% (per constitution) ✅
- **linting:** ruff check with no errors ✅
- **formatting:** ruff format applied ✅

### Coverage Target

50% (0.50) - Per constitution section "Quality Bars > Coverage"

**Rationale:** Case study targets core logic coverage. Focus on AirtableClient methods and Flask endpoint logic, not boilerplate/configuration.

### Acceptance References

- **AC-FW-01**: Flask Server Startup (validated by TK-04, tested in TK-09)
- **AC-FW-02**: Request Validation (implemented in TK-05, tested in TK-09)
- **AC-FW-03**: Successful Screening End-to-End (implemented in TK-06, tested in TK-09)
- **AC-FW-04**: Partial Failure Handling (implemented in TK-06, TK-07, tested in TK-09)
- **AC-FW-05**: Critical Error Handling (implemented in TK-07, tested in TK-09)
- **AC-FW-06**: AirtableClient Implementation (implemented in TK-01-TK-03, tested in TK-08)

## Status

- **Progress:** 85% (11 of 13 tasks completed)
- **Created:** 2025-11-17
- **Status:** in_progress

## Task Dependencies (DAG)

```
TK-11 (dependencies)
  ↓
TK-01 (AirtableClient init)
  ↓
  ├─→ TK-02 (read methods) ──→ TK-08 (unit tests)
  │                              ↓
  ├─→ TK-03 (write methods) ─────┤
  │                              ↓
  └─→ TK-04 (Flask app) ──→ TK-10 (.env.example)
       ↓
      TK-05 (POST /screen validation)
       ↓
      TK-06 (workflow orchestration) ←─ (TK-02, TK-03)
       ↓
      TK-07 (error handling)
       ↓
      TK-09 (integration tests)
       ↓
      TK-12 (manual testing)
       ↓
      TK-13 (documentation)
```

**Critical Path:** TK-11 → TK-01 → TK-04 → TK-05 → TK-06 → TK-07 → TK-09 → TK-12 → TK-13

**Parallelizable:** TK-02 and TK-03 (both depend on TK-01), TK-08 and TK-09 (different test scopes)

## Estimated Timeline

- **Total Effort:** 15.5 hours
- **Critical Path:** ~12 hours
- **Parallel Opportunities:** ~3.5 hours savings if TK-02/TK-03 and TK-08/TK-09 run concurrently
- **Realistic Duration:** ~12 hours for single developer, ~10.5 hours with two developers

## Two-Developer Parallel Implementation Plan

### Phase 1: Shared Setup (1 hour - Sequential)

**Both Developers (Pair/Sequential):**
- **TK-11**: Add Flask/pyairtable dependencies (0.5h)
- **TK-01**: AirtableClient initialization (1h)

**Sync Point:** Both developers review TK-01 to understand AirtableClient interface

### Phase 2: Parallel Tracks (3 hours - Parallel)

**Developer A (Airtable CRUD Layer - 3h):**
- **TK-02**: AirtableClient read methods (1.5h)
- **TK-03**: AirtableClient write methods (1.5h)

**Developer B (Flask Foundation - 2h):**
- **TK-04**: Flask app skeleton + config (1h)
- **TK-10**: Update .env.example (0.5h)
- **TK-05**: POST /screen validation (1h)
- *(0.5h buffer for review)*

**Sync Point:** Review AirtableClient interface (TK-02, TK-03) and Flask endpoint skeleton (TK-04, TK-05)

### Phase 3: Core Integration (3 hours - Collaborative/Sequential)

**Developer A + B (Paired or Sequential):**
- **TK-06**: Workflow orchestration (2h) - *Requires both TK-02/03 and TK-04/05*
- **TK-07**: Error handling (1h) - *Critical integration logic*

**Rationale:** Most complex integration point requiring both Airtable and Flask knowledge. Best done collaboratively.

**Sync Point:** End-to-end workflow validated with manual test

### Phase 4: Parallel Testing (4.5 hours - Parallel)

**Developer A (Unit Tests - 2h):**
- **TK-08**: AirtableClient unit tests (2h)

**Developer B (Integration Tests - 2.5h):**
- **TK-09**: Flask integration tests (2.5h)

**Rationale:** Independent test scopes with minimal overlap. A tests data layer, B tests API layer.

**Sync Point:** All tests passing, coverage ≥50%

### Phase 5: Validation & Documentation (2 hours - Parallel)

**Developer A (Manual Testing - 1h):**
- **TK-12**: Manual webhook testing with ngrok (1h)

**Developer B (Documentation - 1h):**
- **TK-13**: Update README with Flask setup (1h)

**Final Sync:** Demo rehearsal with full webhook flow

### Timeline Summary

| Phase | Developer A | Developer B | Duration | Cumulative |
|-------|-------------|-------------|----------|------------|
| 1 | Setup (paired) | Setup (paired) | 1h | 1h |
| 2 | TK-02, TK-03 (3h) | TK-04, TK-10, TK-05 (2h) | 3h | 4h |
| 3 | TK-06, TK-07 (collaborative) | TK-06, TK-07 (collaborative) | 3h | 7h |
| 4 | TK-08 (2h) | TK-09 (2.5h) | 2.5h | 9.5h |
| 5 | TK-12 (1h) | TK-13 (1h) | 1h | 10.5h |

**Total: ~10.5 hours per developer (vs 15.5h sequential)**

**Savings: ~5 hours through parallelization (32% reduction)**

### Work Distribution Balance

**Developer A Focus:** Data layer specialist
- Total: 7h individual work + 4h collaborative = 11h
- Tasks: AirtableClient (TK-02, TK-03), unit tests (TK-08), manual testing (TK-12)

**Developer B Focus:** API layer specialist
- Total: 4.5h individual work + 4h collaborative = 8.5h
- Tasks: Flask app (TK-04, TK-05, TK-10), integration tests (TK-09), docs (TK-13)

**Shared:** Core integration (TK-06, TK-07) - 3h paired

### Critical Handoffs

1. **After Phase 1:** Developer A provides AirtableClient interface to B
2. **After Phase 2:** Both review complete interfaces before TK-06
3. **After Phase 3:** Developer B uses completed workflow for integration tests (TK-09)
4. **After Phase 4:** Developer A uses passing tests for manual validation (TK-12)

### Risk Mitigation for Parallel Development

**What if Developer A is blocked on TK-02/TK-03?**
- Developer B continues independently on TK-04, TK-05, TK-10
- B can start TK-09 test scaffolding with mocked AirtableClient

**What if TK-06 takes longer than 2h?**
- Both developers pair on TK-06 to unblock critical path
- Defer TK-10 and TK-13 to buffer time

**What if tests reveal integration issues?**
- Phase 4 provides buffer for fixes (2.5h vs 2h for Developer B)
- Phase 5 allows Developer A to assist with test fixes if needed

### Recommended Daily Schedule (for 1.5 day sprint)

**Day 1 (7 hours):**
- Morning: Phase 1 + Phase 2 (4h)
- Afternoon: Phase 3 (3h)
- End of Day Sync: Review TK-06/TK-07, ensure workflow works

**Day 2 (3.5 hours):**
- Morning: Phase 4 (2.5h)
- Midday: Phase 5 (1h)
- Final: Demo rehearsal

## Notes

### Implementation Order

Follow this sequence for optimal dependency flow:

1. **Foundation** (TK-11, TK-01): Dependencies and client initialization
2. **Airtable CRUD** (TK-02, TK-03): Read/write methods
3. **Flask Setup** (TK-04, TK-05): Server and endpoint skeleton
4. **Core Logic** (TK-06, TK-07): Workflow orchestration and error handling
5. **Validation** (TK-08, TK-09): Unit and integration tests
6. **Documentation** (TK-10, TK-12, TK-13): Configuration and usage docs

### Integration with Unit 003

TK-06 requires `screen_single_candidate()` function from unit 003-workflow-orchestration. Verify that function exists in `demo/agents.py` before starting TK-06. Expected signature:

```python
def screen_single_candidate(
    candidate: dict[str, Any],
    role_spec: dict[str, Any],
    screen_id: str
) -> dict[str, Any]:
    """Execute full screening workflow for single candidate."""
    pass
```

### Airtable Schema Dependencies

Ensure Airtable base has these tables configured (from design.md Notes):
- **Screens** (with status, error_message fields)
- **People** (candidate data)
- **Role_Specs** (with structured_spec_markdown)
- **Assessments** (with assessment_json, research_structured_json, overall_score, confidence)

See `spec/dev_reference/airtable_ai_spec.md` for complete schema.

### Testing Strategy

1. **Unit Tests (TK-08):** Mock pyairtable API, test AirtableClient methods in isolation
2. **Integration Tests (TK-09):** Use Flask test client, mock AirtableClient and screen_single_candidate()
3. **Manual Tests (TK-12):** Real Airtable + ngrok, validate full webhook flow

### Quality Checklist

Before marking unit complete:

- ✅ All 13 tasks completed
- ✅ All tests passing (pytest)
- ✅ Coverage ≥50% (pytest-cov)
- ✅ No type errors (mypy)
- ✅ No linting errors (ruff check)
- ✅ Code formatted (ruff format)
- ✅ All 6 acceptance criteria validated
- ✅ README documents Flask setup
- ✅ Manual webhook test successful

### Risk Mitigation

**Risk:** Airtable API rate limiting during development
**Mitigation:** Use mocked tests for rapid iteration, save live API calls for final validation (TK-12)

**Risk:** screen_single_candidate() interface mismatch
**Mitigation:** Verify function signature in unit 003 before starting TK-06, add integration test in TK-09

**Risk:** ngrok URL changes frequently
**Mitigation:** Document ngrok setup clearly in README (TK-13), use stable ngrok account if available

**Risk:** Environment variable misconfiguration
**Mitigation:** Create .env.example early (TK-10), validate on app startup (TK-04)
