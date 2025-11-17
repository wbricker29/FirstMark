---
unit_id: "004-flask-webhook"
title: "Flask Webhook Server & Airtable Integration"
version: "1.0"
created: "2025-11-17"
updated: "2025-11-17"
status: "draft"
---

# Unit Design: Flask Webhook Server & Airtable Integration

Stable intent and acceptance criteria for Stage 4 implementation

## Objective

**Summary:** Create a Flask webhook server that receives Airtable automation triggers and orchestrates candidate screening workflows, writing results back to Airtable.

**Success Metrics:**

- Flask server successfully receives webhook POST requests from Airtable automation
- AirtableClient performs all CRUD operations (read screens, read role specs, write assessments, update statuses)
- End-to-end workflow completes: Airtable trigger → Flask → screen_single_candidate() → Airtable results
- Graceful handling of partial failures (continue processing remaining candidates)
- Structured JSON responses with execution metrics (time, candidates processed, errors)

## Behavior

**Description:** The Flask webhook server acts as the integration layer between Airtable's automation system and the Python screening workflow. When a Screen record's status changes to "Ready to Screen" in Airtable, an automation triggers a POST request to the `/screen` endpoint. The server validates the request, fetches necessary data from Airtable, executes the screening workflow for each candidate synchronously, writes assessment results back to Airtable, and returns a summary response.

### Inputs

#### POST /screen Request Body

- **Type:** `application/json`
- **Description:** Webhook payload from Airtable automation containing the Screen record ID to process
- **Examples:**
  - `{"screen_id": "recABC123"}`
  - `{"screen_id": "rec5x9KPqR2mNvZYz"}`

#### Environment Variables

- **Type:** Configuration via `.env` file
- **Description:** API keys, base IDs, Flask configuration, and runtime settings
- **Examples:**
  - `AIRTABLE_API_KEY=pat...`
  - `AIRTABLE_BASE_ID=appeY64iIwU5CEna7`
  - `FLASK_HOST=0.0.0.0`
  - `FLASK_PORT=5000`
  - `OPENAI_API_KEY=sk-...`

### Outputs

#### Success Response (200)

- **Type:** `application/json`
- **Description:** Indicates all candidates processed successfully
- **Examples:**
  ```json
  {
    "status": "success",
    "screen_id": "recABC123",
    "candidates_processed": 3,
    "execution_time_seconds": 342.5,
    "results": [
      {
        "candidate_id": "recXYZ1",
        "overall_score": 78.0,
        "confidence": "High"
      }
    ]
  }
  ```

#### Partial Success Response (200)

- **Type:** `application/json`
- **Description:** Some candidates succeeded, others failed
- **Examples:**
  ```json
  {
    "status": "partial",
    "screen_id": "recABC123",
    "candidates_processed": 2,
    "candidates_failed": 1,
    "results": [...],
    "errors": [
      {
        "candidate_id": "recXYZ3",
        "error": "Research agent failed after 2 retries"
      }
    ]
  }
  ```

#### Validation Error Response (400)

- **Type:** `application/json`
- **Description:** Invalid request payload
- **Examples:**
  ```json
  {
    "error": "ValidationError",
    "message": "Invalid request payload",
    "details": {
      "field": "screen_id",
      "constraint": "must be valid Airtable record ID"
    }
  }
  ```

#### Server Error Response (500)

- **Type:** `application/json`
- **Description:** Critical failure during workflow execution
- **Examples:**
  ```json
  {
    "error": "InternalError",
    "message": "Workflow execution failed",
    "details": {
      "screen_id": "recABC123",
      "error": "Airtable API connection timeout"
    }
  }
  ```

#### Airtable Writes

- **Type:** Database records
- **Description:** Assessment results written to Assessments table, Screen status updates
- **Examples:**
  - Assessment record with research_structured_json, assessment_json, overall_score, confidence
  - Screen status updated to "Processing" → "Complete" or "Partial" or "Failed"

### Edge Cases

- **Scenario:** Screen has no linked candidates
  - **Expected behavior:** Return 400 with error "No candidates found for screen"

- **Scenario:** Role spec not found for screen's search
  - **Expected behavior:** Return 500 with error "Role spec not found", update Screen status to "Failed"

- **Scenario:** One candidate fails research, others succeed
  - **Expected behavior:** Continue processing remaining candidates, return 200 with "partial" status, include failed candidate in errors array

- **Scenario:** Airtable API rate limit exceeded
  - **Expected behavior:** Agent retry logic exhausted, return 500 with error details, update Screen status to "Failed"

- **Scenario:** Duplicate webhook trigger (user clicks twice)
  - **Expected behavior:** Process normally (idempotency not required for v1, but status check could prevent reprocessing)

## Interfaces Touched

- **Flask Route**: POST `/screen` endpoint (spec.md:651-795)
- **AirtableClient**: `get_screen()`, `get_role_spec()`, `write_assessment()`, `update_screen_status()` (spec.md:368-450)
- **Workflow Orchestration**: `screen_single_candidate()` from unit 003-workflow-orchestration
- **Logging**: Python `logging` module with emoji indicators (spec.md:884-904)

## Data Shapes

- **AssessmentResult** (Pydantic model from demo/models.py)
- **ExecutiveResearchResult** (Pydantic model from demo/models.py)
- **Screen** (Airtable record from Screens table)
- **Role Spec** (Airtable record from Role_Specs table)
- **Candidate** (Airtable record from People table)
- **Assessment** (Airtable record from Assessments table)

## Constraints

### Functional

- Synchronous execution only (no async/concurrent processing in v1)
- Sequential candidate processing (loop through candidates one at a time)
- Graceful degradation (continue if one candidate fails)
- Basic Python exceptions for error handling (no custom error hierarchy)
- Python standard library logging (no structlog)

### Non-Functional

- **Performance**: <10 minutes per candidate workflow execution (spec.md:542)
- **Memory**: <512MB per Flask worker (spec.md:543)
- **Concurrency**: Single Flask worker sufficient for demo (spec.md:550-552)
- **Database Writes**: <5 seconds per Airtable operation (spec.md:544)
- **Environment**: Local development with ngrok tunnel (spec.md:605-610)
- **Security**: API keys via environment variables only, never in code (spec.md:562-570)

## Acceptance Criteria

### AC-FW-01: Flask Server Startup

- **Given**: Flask app configured with environment variables from .env
- **When**: Server starts via `flask run` or `python demo/app.py`
- **Then**: Server listens on localhost:5000, POST `/screen` endpoint accessible
- **Testable**: ✅ (curl test or pytest with Flask test client)

### AC-FW-02: Request Validation

- **Given**: POST request to `/screen` with missing `screen_id` or invalid format
- **When**: Request processed by Flask route handler
- **Then**: Returns 400 status with ValidationError JSON, no workflow execution
- **Testable**: ✅ (pytest with invalid payloads: empty body, missing field, wrong type)

### AC-FW-03: Successful Screening End-to-End

- **Given**: Valid screen_id with linked candidates and role spec in Airtable
- **When**: POST `/screen` executes successfully for all candidates
- **Then**:
  - Screen status updated to "Processing" at start
  - All candidates processed via screen_single_candidate()
  - Assessments written to Airtable with all required fields
  - Screen status updated to "Complete"
  - Returns 200 with success status, candidates_processed count, execution_time, results array
- **Testable**: ✅ (integration test with Airtable or mocked AirtableClient)

### AC-FW-04: Partial Failure Handling

- **Given**: Valid screen_id where one candidate's research agent fails
- **When**: Workflow encounters exception for one candidate (e.g., API timeout)
- **Then**:
  - Logs error with ❌ emoji indicator
  - Continues processing remaining candidates
  - Returns 200 with "partial" status
  - Results array contains successful assessments
  - Errors array contains failed candidate IDs with error messages
  - Screen status updated to "Partial"
- **Testable**: ✅ (mock screen_single_candidate to raise exception for one candidate)

### AC-FW-05: Critical Error Handling

- **Given**: Airtable API failure or unhandled exception during workflow setup
- **When**: Critical error occurs (e.g., Airtable connection timeout, invalid credentials)
- **Then**:
  - Logs error with ❌ emoji indicator
  - Updates Screen status to "Failed" with error_message field populated
  - Returns 500 status with InternalError JSON containing details
- **Testable**: ✅ (mock AirtableClient methods to raise exceptions)

### AC-FW-06: AirtableClient Implementation

- **Given**: AirtableClient instantiated with AIRTABLE_API_KEY and AIRTABLE_BASE_ID
- **When**: Methods called: get_screen(screen_id), get_role_spec(spec_id), write_assessment(...), update_screen_status(...)
- **Then**:
  - get_screen() returns Screen record dict with linked candidates and search
  - get_role_spec() returns Role Spec record dict with structured_spec_markdown
  - write_assessment() creates Assessment record and returns record ID
  - update_screen_status() updates Screen.status field and optional error_message
  - All methods use pyairtable library for API calls
- **Testable**: ✅ (unit tests with mocked pyairtable API responses)

## Dependencies

**Blocks:**
- Stage 5 (Testing & Validation)
- Stage 6 (Demo Preparation & Pre-runs)

**Blocked by:**
- Unit 003-workflow-orchestration (requires screen_single_candidate() function)
- Unit 002-agent-implementation (requires AssessmentResult, ExecutiveResearchResult models)

## Notes

### Implementation Files

This unit creates two new files:
1. **demo/app.py** - Flask application with `/screen` route handler (~80-100 LOC)
2. **demo/airtable_client.py** - AirtableClient class with CRUD methods (~120-150 LOC)

### Airtable Automation Configuration

The webhook automation must be configured in Airtable:
- **Trigger Table**: Screens
- **Trigger Condition**: When "status" field changes to "Ready to Screen"
- **Action**: Send POST request to ngrok URL (e.g., `https://abc123.ngrok.io/screen`)
- **Payload**: `{"screen_id": "{RECORD_ID}"}`

### Ngrok Setup

For local development webhook testing:
```bash
ngrok http 5000
# Copy https URL to Airtable automation webhook configuration
```

### Error Logging Pattern

Use emoji indicators for terminal visibility:
- 🔍 Starting operation (info)
- ✅ Successful completion (info)
- ❌ Error or failure (error)
- 🔄 Processing/in-progress (info)

### Environment Variables

Required in `.env` file:
- AIRTABLE_API_KEY (personal access token)
- AIRTABLE_BASE_ID (appeY64iIwU5CEna7 for demo)
- OPENAI_API_KEY (for agents)
- FLASK_HOST (default: 0.0.0.0)
- FLASK_PORT (default: 5000)
- FLASK_DEBUG (default: true)

### Testing Strategy

1. **Unit Tests**: AirtableClient methods with mocked pyairtable
2. **Integration Tests**: Flask endpoint with mocked AirtableClient
3. **Manual Tests**: Full webhook flow with ngrok + Airtable automation
4. **Smoke Test**: Execute one Screen with real Airtable data

### Reference Spec Sections

- Flask endpoint specification: spec.md:651-795
- AirtableClient interface: spec.md:368-450
- Error handling strategy: spec.md:836-878
- Configuration: spec.md:799-833
- Logging patterns: spec.md:884-904
- Airtable schema: spec/dev_reference/airtable_ai_spec.md
