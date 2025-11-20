# AgentOS Integration Specification

## Document Purpose

This document provides a comprehensive specification for the AgentOS integration in the Talent Signal project, including migration history, current implementation status, deployment checklist, and security configuration.

## Context

### Implementation Status

**Stage 4: Core Workflow Integration - ✅ COMPLETE**
- AgentOS FastAPI runtime with POST `/screen` endpoint (`demo/agentos_app.py`)
- Workflow class extracted to `demo/workflow.py` with AgentOSCandidateWorkflow
- Session persistence via Agno SqliteDb (`tmp/agno_sessions.db`)
- Control plane integration for workflow inspection
- Comprehensive test coverage (tests/test_agentos_app.py)

**Stage 4.5: Prompt Templating & Runtime - ✅ COMPLETE**
- Centralized YAML prompt catalog (`demo/prompts/catalog.yaml`)
- Evidence taxonomy integration ([FACT]/[OBSERVATION]/[HYPOTHESIS])
- Temporal awareness and structured prompt contexts
- Version-controlled prompts (no hardcoded strings)

**Stage 4.7: Airtable Payload Simplification - ✅ COMPLETE**
- Zero-traversal Airtable pattern (4+ API calls → 0 during execution)
- Structured nested object payloads via ScreenWebhookPayload
- Write-only Airtable client (41% code reduction)
- Eliminated JSON parsing operations (3 → 0)

**Stage 5: Integration Testing & Validation - ✅ COMPLETE**
- Test suite validation (TK-01: ✅ 130 tests, 75% coverage)
- Infrastructure setup (TK-02: ✅ Server + ngrok running)
- Webhook automation (TK-03: ✅ Airtable automation configured)
- Manual end-to-end testing (TK-04-06: ✅ Test data ready, workflows executing)
- Security hardening (TK-19: 🔄 Bearer auth implementation + documentation alignment tracked here; gating item for Stage 5 sign-off)

### Migration History

The Talent Signal project evolved through multiple architectural iterations:

1. **Initial Flask Runtime** (Stages 1-3): Monolithic Flask app with embedded workflow logic
2. **AgentOS Migration** (Stage 4): Extracted workflow to AgentOS runtime with FastAPI
3. **Prompt Centralization** (Stage 4.5): Moved all prompts to YAML catalog
4. **Airtable Simplification** (Stage 4.7): Eliminated API traversal via structured payloads
5. **Security Hardening** (Stage 5/TK-19): Bearer token authentication for webhook endpoint

## Architecture Overview

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                    Airtable Automation                       │
│  (Trigger: Status = "Ready to Screen")                      │
│   - Reads Admin-screen_slug field (pre-assembled JSON)      │
│   - Sends structured payload to AgentOS webhook              │
└────────────────────┬────────────────────────────────────────┘
                     │ POST /screen
                     │ Authorization: Bearer <token>
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              AgentOS FastAPI Runtime                         │
│                (demo/agentos_app.py)                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Bearer Auth Middleware (Optional)                     │  │
│  │  - Validates AGENTOS_SECURITY_KEY if configured       │  │
│  │  - Returns 401 Unauthorized if token invalid/missing  │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ POST /screen Endpoint                                 │  │
│  │  - Validates ScreenWebhookPayload (Pydantic)          │  │
│  │  - Returns 202 Accepted immediately                   │  │
│  │  - Queues workflow in background (FastAPI Tasks)      │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────────┘
                     │ Background execution
                     ▼
┌─────────────────────────────────────────────────────────────┐
│          AgentOSCandidateWorkflow                            │
│              (demo/workflow.py)                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Step 1: Deep Research (o4-mini-deep-research)         │  │
│  │ Step 2: Quality Check (citation + content validation) │  │
│  │ Step 3: Incremental Search (conditional, if needed)   │  │
│  │ Step 4: Assessment (gpt-5-mini + ReasoningTools)      │  │
│  └──────────────────────────────────────────────────────┘  │
│  - Session state persisted to tmp/agno_sessions.db          │
│  - All steps tracked via AgentOS control plane              │
└────────────────────┬────────────────────────────────────────┘
                     │ Write results
                     ▼
┌─────────────────────────────────────────────────────────────┐
│          Airtable Write-Only Client                          │
│          (demo/airtable_client.py)                           │
│  - Creates assessment records (Assessments table)            │
│  - Updates screen status (Processing → Complete/Failed)      │
│  - Logs automation events (Automation_Log table)             │
│  - Zero traversal API calls (all data from webhook payload)  │
└─────────────────────────────────────────────────────────────┘
```

### Key Design Patterns

1. **Zero-Traversal Airtable Integration**
   - All candidate/role data pre-assembled in Airtable formula (Admin-screen_slug)
   - Webhook payload contains complete nested objects (no JSON parsing)
   - Python client only writes results (no read operations during execution)
   - Performance: ~500ms+ latency reduction per screen

2. **Async Request Handling**
   - Webhook returns 202 Accepted immediately (prevents Airtable timeouts)
   - Workflow processes in background via FastAPI BackgroundTasks
   - Status updates written to Airtable when complete
   - Long-running workflows (5-10 min) don't block HTTP responses

3. **Bearer Token Security (Optional)**
   - `AGENTOS_SECURITY_KEY` environment variable enables auth
   - Middleware validates `Authorization: Bearer <token>` header
   - Rejects unauthorized requests with 401 (prevents public access)
   - Configurable per deployment (dev/staging/prod)

4. **Session Persistence & Observability**
   - All workflow executions tracked in SqliteDb (tmp/agno_sessions.db)
   - AgentOS control plane provides real-time monitoring
   - Session inspection shows step-by-step execution history
   - Token usage and performance metrics available per workflow

5. **Shared Screening Service (`demo/screening_service.py`)**
   - `process_screen_direct()` is the canonical entrypoint invoked from FastAPI
   - Helper functions `_update_screen_status_and_log_webhook()`, `_process_candidate_batch()`, and `_log_completion_event()` centralize status updates, batch processing, and Airtable automation logging
   - Validation errors raise `ScreenValidationError` so FastAPI can surface 400 responses with structured field metadata
   - Keeps orchestration logic isolated from HTTP transport concerns while avoiding any Airtable read traversal

## Security Configuration

### Bearer Token Authentication

**Purpose:** Protect the `/screen` webhook endpoint from unauthorized access.

**Environment Variable:**
```bash
# Optional - if not set, authentication is disabled
AGENTOS_SECURITY_KEY=your-secret-token-here
```

**Implementation Details:**

The bearer auth middleware is implemented in `demo/agentos_app.py` as a FastAPI dependency:

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer(auto_error=False)

async def verify_bearer_token(
    credentials: HTTPAuthorizationCredentials | None = Depends(security)
) -> None:
    """Validate bearer token if AGENTOS_SECURITY_KEY is configured.

    Raises:
        HTTPException: 401 Unauthorized if token is missing or invalid
    """
    if not settings.agentos.security_key:
        # Security not configured - allow all requests
        return

    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if credentials.credentials != settings.agentos.security_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
```

**Usage in Endpoints:**

```python
@fastapi_app.post("/screen", response_model=None, status_code=202)
def screen_endpoint(
    payload: ScreenWebhookPayload,
    background_tasks: BackgroundTasks,
    _auth: None = Depends(verify_bearer_token),  # Enforce auth if configured
) -> dict[str, Any] | JSONResponse:
    # ... endpoint logic
```

**Airtable Automation Configuration:**

When `AGENTOS_SECURITY_KEY` is set, configure the Airtable automation script to include the bearer token:

```javascript
// Airtable automation script
let response = await fetch(webhook_url, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer YOUR_SECURITY_KEY_HERE'  // Add this line
    },
    body: JSON.stringify(payload)
});
```

**Security Best Practices:**

1. **Never commit tokens to version control** - Use `.env` file (gitignored)
2. **Use strong random tokens** - Generate with `openssl rand -hex 32`
3. **Rotate tokens periodically** - Update both server and Airtable automation
4. **Use HTTPS only** - ngrok provides this automatically, ensure production does too
5. **Different tokens per environment** - Separate dev/staging/prod keys

### Error Responses

**401 Unauthorized - Missing Token:**
```json
{
    "detail": "Missing authorization header"
}
```

**401 Unauthorized - Invalid Token:**
```json
{
    "detail": "Invalid authentication credentials"
}
```

## Deployment Checklist

### Prerequisites

- [ ] Python 3.11+ installed
- [ ] `uv` package manager installed (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- [ ] Airtable base configured with required tables (Screens, Candidates, Assessments, etc.)
- [ ] OpenAI API key with access to o4-mini-deep-research and gpt-5-mini
- [ ] ngrok installed (for local development with Airtable webhooks)

### Environment Configuration

Create `.env` file in project root:

```bash
# Required Configuration
OPENAI_API_KEY=sk-proj-...                      # OpenAI API key
AIRTABLE_API_KEY=pat...                         # Airtable personal access token
AIRTABLE_BASE_ID=appeY64iIwU5CEna7              # Airtable base ID

# Optional Configuration
AGENTOS_SECURITY_KEY=                           # Bearer token (leave blank = disabled)
USE_DEEP_RESEARCH=true                          # Enable o4-mini-deep-research (recommended)
FASTAPI_HOST=0.0.0.0                            # Server host (default: 0.0.0.0)
FASTAPI_PORT=5001                               # Server port (default: 5001)
LOG_LEVEL=INFO                                  # Logging verbosity (DEBUG/INFO/WARNING/ERROR)
MIN_CITATIONS=3                                 # Quality check threshold (default: 3)
```

### Installation Steps

1. **Clone repository and install dependencies:**
   ```bash
   git clone <repository-url>
   cd talent-signal-agent
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install -e .
   ```

2. **Verify installation:**
   ```bash
   uv run python -c "from demo.agentos_app import app; print('✅ Installation successful')"
   ```

3. **Run test suite:**
   ```bash
   uv run pytest tests/ -v --cov=demo --cov-report=term-missing
   ```

### Server Deployment

#### Local Development (with ngrok)

1. **Start AgentOS server:**
   ```bash
   uv run python demo/agentos_app.py
   ```

   Expected output:
   ```
   INFO:     Started server process [12345]
   INFO:     Waiting for application startup.
   INFO:     Application startup complete.
   INFO:     Uvicorn running on http://0.0.0.0:5001
   ✅ AgentOS initialized with workflow AgentOSCandidateWorkflow (id: ...)
   ```

2. **Start ngrok tunnel (separate terminal):**
   ```bash
   ngrok http 5001
   ```

   Copy the public forwarding URL (e.g., `https://abc123.ngrok-free.app`)

3. **Verify endpoints:**
   ```bash
   # Health check
   curl https://abc123.ngrok-free.app/healthz
   # Expected: {"status":"ok"}

   # Swagger docs
   open https://abc123.ngrok-free.app/docs
   ```

4. **Configure Airtable automation:**
   - Update webhook URL to ngrok URL
   - Add `Authorization: Bearer <token>` header if `AGENTOS_SECURITY_KEY` is set
   - Test trigger by setting a Screen record to "Ready to Screen"

#### Production Deployment

For production, replace ngrok with a persistent hosting solution:

- **Cloud Providers:** AWS EC2, Google Cloud Run, Azure App Service
- **Platform-as-a-Service:** Railway, Render, Fly.io
- **Containerization:** Docker + Docker Compose (see `Dockerfile` if available)

**Production-specific considerations:**

1. **Enable bearer auth:** Set `AGENTOS_SECURITY_KEY` to a strong random token
2. **Use HTTPS:** Ensure SSL/TLS certificates are configured
3. **Configure logging:** Set `LOG_LEVEL=WARNING` or `ERROR` to reduce noise
4. **Set up monitoring:** Track uptime, response times, error rates
5. **Database persistence:** Mount `tmp/agno_sessions.db` to persistent volume
6. **Auto-restart:** Configure process manager (systemd, supervisor, or platform equivalent)

### Airtable Configuration

#### Required Tables

The following tables must exist in your Airtable base:

1. **Screens** - Screen records with status tracking
2. **Candidates** - Executive candidate profiles
3. **Searches** - Search requests (links Screens to Role_Specs)
4. **Role_Specs** - Role specification templates
5. **Assessments** - Assessment results (written by AgentOS)
6. **Automation_Log** - Webhook event audit trail

Schema details available in `docs/airtable_ai_spec.md`.

#### Admin-screen_slug Formula

The `Admin-screen_slug` field in the Screens table must contain a formula that assembles the complete payload:

```javascript
// Example formula (simplified - see Airtable base for full implementation)
CONCATENATE(
  '{"screen_slug":{"screen_id":"', RECORD_ID(), '",',
  '"role_spec_slug":', {Role Spec Formula}, ',',
  '"search_slug":', {Search Formula}, ',',
  '"candidate_slugs":', {Candidates Formula}, '}}'
)
```

This formula pre-assembles all nested data so the webhook payload contains:
- Screen ID and metadata
- Complete role spec content
- Search context
- All candidate details (name, title, company, LinkedIn, etc.)

#### Automation Script

Create an Airtable automation with:

**Trigger:** When record in Screens matches condition
- Field: Status
- Condition: equals
- Value: "Ready to Screen"

**Action:** Run script

```javascript
// Airtable automation script for AgentOS webhook
let config = input.config();
let screenRecord = config.screenRecord;

// Read pre-assembled payload from Admin-screen_slug formula field
let payloadStr = screenRecord.getCellValue("Admin-screen_slug");
if (!payloadStr) {
    console.error("❌ Admin-screen_slug field is empty");
    throw new Error("Cannot trigger webhook - missing Admin-screen_slug");
}

// Parse and validate payload structure
let payload;
try {
    payload = JSON.parse(payloadStr);
} catch (e) {
    console.error("❌ Failed to parse Admin-screen_slug JSON:", e);
    throw new Error("Invalid JSON in Admin-screen_slug field");
}

// Webhook configuration
const WEBHOOK_URL = "https://your-agentos-url.com/screen";  // Update this
const SECURITY_KEY = "your-security-key-here";  // Update if auth enabled

// Send webhook request
let response = await fetch(WEBHOOK_URL, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        // Uncomment if bearer auth is enabled:
        // 'Authorization': `Bearer ${SECURITY_KEY}`
    },
    body: JSON.stringify(payload)
});

// Log response
if (response.ok) {
    let data = await response.json();
    console.log("✅ Webhook triggered successfully:", data);
} else {
    let errorText = await response.text();
    console.error("❌ Webhook failed:", response.status, errorText);
    throw new Error(`Webhook request failed: ${response.status}`);
}
```

### Verification Steps

After deployment, verify the integration:

1. **Health Check:**
   ```bash
   curl https://your-agentos-url.com/healthz
   # Expected: {"status":"ok"}
   ```

2. **Bearer Auth Test (if enabled):**
   ```bash
   # Without token - should fail
   curl -X POST https://your-agentos-url.com/screen \
     -H "Content-Type: application/json" \
     -d '{"screen_slug":{}}'
   # Expected: 401 Unauthorized

   # With valid token - should accept
   curl -X POST https://your-agentos-url.com/screen \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer your-token-here" \
     -d '{"screen_slug":{"screen_id":"test"}}'
   # Expected: 202 Accepted (or 400 if payload invalid)
   ```

3. **End-to-End Workflow:**
   - Create a test Screen record in Airtable
   - Link to Role_Spec and Candidates
   - Verify Admin-screen_slug field is populated
   - Set Status = "Ready to Screen"
   - Monitor server logs for workflow execution
   - Verify Assessment record created in Airtable
   - Check Screen status updated to "Complete"

4. **AgentOS Control Plane:**
   - Visit https://os.agno.com
   - Add new OS with your server URL
   - Inspect workflow sessions
   - Verify step-by-step execution history visible

## Monitoring & Observability

### Server Logs

AgentOS logs structured events with emoji indicators:

- 🔍 **Search** - Webhook received, workflow starting
- ✅ **Success** - Step completed successfully
- ❌ **Error** - Fatal error occurred
- ⚠️ **Warning** - Non-fatal issue (e.g., low quality research)

Example log output:
```
2025-11-18 20:15:00 | INFO | 🔍 Received AgentOS screen webhook for recScreen123
2025-11-18 20:15:01 | INFO | 🔄 Processing candidate: Jane Doe (CFO @ Acme Inc)
2025-11-18 20:16:30 | INFO | ✅ Deep Research complete (1.5s, 2500 tokens)
2025-11-18 20:16:31 | INFO | ✅ Quality Check passed (3 citations, 250 words)
2025-11-18 20:18:00 | INFO | ✅ Assessment complete (overall_score: 85, confidence: High)
2025-11-18 20:18:01 | INFO | ✅ Screen recScreen123 completed (3 candidates, 2m 45s)
```

### AgentOS Control Plane

Access workflow inspection UI at https://os.agno.com:

1. **Add your OS:**
   - Click "Add OS"
   - Enter server URL: `https://your-agentos-url.com`
   - Name: "Talent Signal Production"

2. **Inspect sessions:**
   - View all workflow executions
   - Click session to see step-by-step history
   - Review input/output for each step
   - Check token usage and performance metrics

3. **Debug failures:**
   - Filter by failed sessions
   - Review error messages and stack traces
   - Inspect intermediate state at failure point
   - Replay failed steps with modified inputs

### Session Database

All workflow sessions are persisted to `tmp/agno_sessions.db` (SQLite).

**Query session history:**
```bash
sqlite3 tmp/agno_sessions.db

-- List all sessions
SELECT session_id, created_at, updated_at, status
FROM sessions
ORDER BY created_at DESC
LIMIT 10;

-- View session details
SELECT * FROM sessions WHERE session_id = 'your-session-id';
```

**Backup sessions:**
```bash
# Copy database to backup location
cp tmp/agno_sessions.db backups/sessions_$(date +%Y%m%d).db
```

## Troubleshooting

### Common Issues

**Issue: "Missing authorization header" error**

**Cause:** `AGENTOS_SECURITY_KEY` is set but Airtable automation doesn't include bearer token.

**Solution:**
1. Add `Authorization: Bearer <token>` header to Airtable automation script
2. OR remove `AGENTOS_SECURITY_KEY` from `.env` to disable auth

---

**Issue: Airtable automation times out (504 Gateway Timeout)**

**Cause:** Workflow takes >30 seconds (Airtable webhook timeout limit).

**Solution:**
- Verify endpoint returns 202 Accepted immediately (not waiting for workflow completion)
- Check `background_tasks.add_task()` is used in `/screen` endpoint
- Workflow should process asynchronously, not in request handler

---

**Issue: Assessment records not created in Airtable**

**Cause:** Workflow fails silently or Airtable write permissions issue.

**Solution:**
1. Check server logs for `❌` error indicators
2. Verify `AIRTABLE_API_KEY` has write permissions to Assessments table
3. Inspect session in AgentOS control plane for step failures
4. Review Airtable API error messages in logs

---

**Issue: "Session not persisted to database" error**

**Cause:** SqliteDb write failure or incorrect session_type parameter.

**Solution:**
1. Verify `tmp/agno_sessions.db` file exists and is writable
2. Check disk space availability
3. Review `workflow.py` for correct `SessionType.WORKFLOW` parameter in `get_session()` calls

---

**Issue: Deep Research returns empty results**

**Cause:** OpenAI API key invalid or o4-mini-deep-research model not accessible.

**Solution:**
1. Verify `OPENAI_API_KEY` is correct and active
2. Check OpenAI account has access to o4-mini-deep-research model
3. Review API rate limits and quota
4. Inspect logs for OpenAI API error messages

## Audit & Compliance

### Automation Event Logging

All webhook triggers are logged to the `Automation_Log` table in Airtable. The
full audit workflow, field mapping, and reviewer checklist now live in
`docs/automation_audit.md` (replacing the temporary notes that once lived under
`tmp/`), so operators have a durable reference outside the runtime artifacts:

- **Timestamp** - When webhook was triggered
- **Screen ID** - Which screen was processed
- **Event Type** - "webhook_received", "workflow_started", "workflow_completed", etc.
- **Status** - "success", "error", "pending"
- **Details** - JSON with metadata (candidates processed, execution time, errors)

**Query automation history:**

Access Airtable base → Automation_Log table → Filter by Screen or Date Range

### Session Audit Trail

Every workflow execution is tracked with:

- **Session ID** - Unique identifier for this execution
- **Input Data** - Complete candidate + role spec context
- **Step History** - All intermediate outputs (research, quality check, assessment)
- **Token Usage** - Tokens consumed per step and total
- **Execution Time** - Duration per step and total
- **Final Output** - Assessment scores and reasoning

**Access audit trail:**

1. AgentOS Control Plane: https://os.agno.com → Select session
2. SQLite DB: `sqlite3 tmp/agno_sessions.db` → Query sessions table
3. Server Logs: `grep "session_id=<id>" /path/to/server.log`

### Data Retention

**Default retention policies:**

- **Server Logs** - Rotate daily, keep 30 days (configurable via logging settings)
- **Session Database** - No automatic deletion (manual cleanup required)
- **Airtable Records** - Permanent (managed by Airtable retention policies)

**Manual cleanup:**

```bash
# Delete sessions older than 90 days
sqlite3 tmp/agno_sessions.db <<EOF
DELETE FROM sessions
WHERE created_at < datetime('now', '-90 days');
EOF
```

## Migration from Flask (Historical Reference)

**Note:** This section documents the completed migration from Flask to AgentOS. All references are for historical context only - the Flask runtime has been fully retired.

### What Changed

| Component | Flask Implementation | AgentOS Implementation |
|-----------|---------------------|----------------------|
| **Runtime** | Flask app with manual routes | FastAPI + AgentOS with workflow DSL |
| **Workflow** | Imperative Python functions | Declarative workflow with step executors |
| **Session** | No persistence | SqliteDb with full audit trail |
| **Prompts** | Hardcoded Python strings | YAML catalog (version-controlled) |
| **Airtable** | Sequential API traversal (4+ calls) | Zero-traversal (structured payloads) |
| **Monitoring** | Print statements | AgentOS control plane + structured logs |
| **Security** | None | Optional bearer token auth |

### Deprecated Components

The following files/patterns are no longer used:

- ❌ `demo/flask_app.py` - Replaced by `demo/agentos_app.py`
- ❌ Hardcoded prompt strings in `demo/agents.py` - Replaced by `demo/prompts/catalog.yaml`
- ❌ `screen_single_candidate()` function - Replaced by `AgentOSCandidateWorkflow.run_candidate_workflow()`
- ❌ `create_screening_workflow()` function - Replaced by workflow class initialization
- ❌ Airtable traversal methods (`get_screen()`, `get_role_spec()`) - Replaced by payload validation

### Cutover Verification

All Airtable automations, helper scripts, and documentation now reference the AgentOS runtime:

- ✅ Airtable webhook automation points to `/screen` endpoint
- ✅ README.md documents AgentOS setup and ngrok configuration
- ✅ DEMO_RUNBOOK.md references AgentOS server startup
- ✅ All tests updated to use FastAPI TestClient
- ✅ No Flask dependencies remaining in requirements

**Verification command:**

```bash
# Confirm no Flask references in codebase
grep -r "flask" demo/ tests/ --include="*.py"
# Expected: No results

# Confirm AgentOS is primary runtime
grep -r "AgentOS\|agentos_app" spec/ docs/ --include="*.md"
# Expected: Multiple references confirming AgentOS integration
```

## References

- **Primary Specification:** `spec/spec.md` - Complete technical specification
- **Product Requirements:** `spec/prd.md` - User stories and acceptance criteria
- **Implementation Guide:** `spec/dev_reference/implementation_guide.md` - Data models and interfaces
- **Agno Framework Patterns:** `spec/dev_reference/AGNO_REFERENCE.md` - Best practices and examples
- **Airtable Schema:** `docs/airtable_ai_spec.md` - Table definitions and relationships
- **Demo Runbook:** `docs/DEMO_RUNBOOK.md` - Step-by-step demo execution guide
- **Comprehensive Setup:** `README.md` - Installation, configuration, and usage instructions

---

**Document Version:** 1.0
**Last Updated:** 2025-11-18
**Status:** ✅ AgentOS integration complete (Stages 4, 4.5, 4.7) | ⏸️ Stage 5 pending until TK-19/TK-21/TK-22 ship (per `spec/spec.md`)
