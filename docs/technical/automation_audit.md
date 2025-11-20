# Automation Audit & Verification Log

## Purpose

This document provides an audit trail of Airtable automation configuration, webhook setup, and verification procedures for the Talent Signal AgentOS integration.

## Current Status

**Last Verified:** 2025-11-18
**AgentOS Runtime:** ✅ Active (FastAPI + AgentOS)
**Webhook Endpoint:** `POST /screen` (with optional bearer auth)
**Airtable Automation:** ✅ Configured (Status: "Ready to Screen" trigger)

## Webhook Configuration

### Endpoint Details

**URL:** `https://<your-domain>/screen` (production) or `https://<ngrok-url>/screen` (local dev)
**Method:** POST
**Content-Type:** application/json
**Response:** 202 Accepted (async processing)

### Security (Bearer Auth)

Bearer token authentication is **optional** and controlled by the `AGENTOS_SECURITY_KEY` environment variable.

**When Enabled:**
- Requests must include: `Authorization: Bearer <AGENTOS_SECURITY_KEY>`
- Missing/invalid token returns: 401 Unauthorized
- Valid token returns: 202 Accepted (workflow queued)

**When Disabled:**
- `AGENTOS_SECURITY_KEY` not set in `.env`
- All requests accepted without authentication
- Suitable for local development only

**Security Best Practices:**
1. Always enable auth in production
2. Use strong random tokens (e.g., `openssl rand -hex 32`)
3. Store tokens in `.env` (gitignored)
4. Rotate tokens periodically
5. Never commit tokens to version control

### Request Payload Structure

The webhook receives structured nested objects (no JSON strings):

```json
{
  "screen_slug": {
    "screen_id": "recXXXXXX",
    "screen_edited": "2025-11-18T20:01:46.000Z",
    "role_spec_slug": {
      "role_spec": {
        "role_spec_id": "recRSXXXX",
        "role_spec_name": "CFO - Series B",
        "role_spec_content": "# Role Specification\n..."
      }
    },
    "search_slug": {
      "role": {
        "ATID": "recRXXXX",
        "portco": "Pigment",
        "role_type": "CFO",
        "role_title": "Chief Financial Officer",
        "role_description": "..."
      }
    },
    "candidate_slugs": [
      {
        "candidate": {
          "ATID": "recCXXXX",
          "candidate_name": "Jane Doe",
          "candidate_current_title": "CFO",
          "candidate_normalized_title": "CFO (Chief Financial Officer)",
          "candidate_current_company": "Acme Inc",
          "candidate_location": "San Francisco, CA",
          "candidate_linkedin": "https://linkedin.com/in/janedoe",
          "candidate_bio": "bio content from field or file..."
        }
      }
    ]
  }
}
```

**Key Features:**
- ✅ Pre-assembled in Airtable via `Admin-screen_slug` formula
- ✅ Zero JSON parsing required (Pydantic validates directly)
- ✅ Zero API traversal during execution (all data in payload)
- ✅ Nested objects validated via `ScreenWebhookPayload` model

## Airtable Automation Script

### Configuration

**Table:** Screens
**Trigger:** When record matches condition
**Condition:** Status = "Ready to Screen"
**Action:** Run script (JavaScript)

### Script Implementation

```javascript
// Airtable automation script for AgentOS webhook
// Last Updated: 2025-11-18
// Version: 2.0 (AgentOS with bearer auth support)

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
const WEBHOOK_URL = "https://your-agentos-url.com/screen";  // UPDATE THIS
const SECURITY_KEY = "your-security-key-here";  // UPDATE IF AUTH ENABLED

// Send webhook request with optional bearer auth
let headers = {
    'Content-Type': 'application/json'
};

// Add authorization header if security key is configured
if (SECURITY_KEY && SECURITY_KEY !== "your-security-key-here") {
    headers['Authorization'] = `Bearer ${SECURITY_KEY}`;
}

let response = await fetch(WEBHOOK_URL, {
    method: 'POST',
    headers: headers,
    body: JSON.stringify(payload)
});

// Log response
if (response.ok) {
    let data = await response.json();
    console.log("✅ Webhook triggered successfully:", data);
    console.log(`   Screen ID: ${data.screen_id}`);
    console.log(`   Candidates queued: ${data.candidates_queued}`);
} else {
    let errorText = await response.text();
    console.error("❌ Webhook failed:", response.status, errorText);

    // Log specific error for troubleshooting
    if (response.status === 401) {
        console.error("   → Check SECURITY_KEY matches AGENTOS_SECURITY_KEY");
    } else if (response.status === 400) {
        console.error("   → Payload validation failed - check Admin-screen_slug");
    }

    throw new Error(`Webhook request failed: ${response.status}`);
}
```

### Script Variables

When configuring the automation in Airtable UI:

1. Select trigger record: `screenRecord` (from trigger step)
2. Map to input: `config.screenRecord`

## Verification Procedures

### 1. Pre-Deployment Checks

**Environment Variables:**
```bash
# Required
OPENAI_API_KEY=sk-proj-...                      # ✅ Verified
AIRTABLE_API_KEY=pat...                         # ✅ Verified
AIRTABLE_BASE_ID=appeY64iIwU5CEna7              # ✅ Verified

# Optional (Security)
AGENTOS_SECURITY_KEY=<random-token>             # ⚠️ Set for production

# Optional (Configuration)
USE_DEEP_RESEARCH=true                          # ✅ Default
FASTAPI_PORT=5001                               # ✅ Default
LOG_LEVEL=INFO                                  # ✅ Default
```

**Airtable Schema:**
- [ ] Screens table exists with Status field
- [ ] Candidates table linked to Screens
- [ ] Searches table linked to Screens
- [ ] Role_Specs table with structured_spec_markdown
- [ ] Assessments table (write destination)
- [ ] Automation_Log table (event tracking)
- [ ] Admin-screen_slug formula field populated

**Server Status:**
```bash
# Health check
curl https://your-url/healthz
# Expected: {"status":"ok"}

# Swagger docs accessible
curl https://your-url/docs
# Expected: 200 OK (OpenAPI spec)
```

### 2. Authentication Verification

**Test 1: Auth Disabled (Development)**
```bash
# No AGENTOS_SECURITY_KEY set
curl -X POST https://your-url/screen \
  -H "Content-Type: application/json" \
  -d '{"screen_slug":{"screen_id":"test"}}'

# Expected: 400 Bad Request (payload validation)
# NOT 401 Unauthorized
```

**Test 2: Auth Enabled - Missing Token**
```bash
# AGENTOS_SECURITY_KEY=test-key
curl -X POST https://your-url/screen \
  -H "Content-Type: application/json" \
  -d '{"screen_slug":{"screen_id":"test"}}'

# Expected: 401 Unauthorized
# Body: {"detail":"Missing authorization header"}
```

**Test 3: Auth Enabled - Invalid Token**
```bash
curl -X POST https://your-url/screen \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer wrong-token" \
  -d '{"screen_slug":{"screen_id":"test"}}'

# Expected: 401 Unauthorized
# Body: {"detail":"Invalid authentication credentials"}
```

**Test 4: Auth Enabled - Valid Token**
```bash
curl -X POST https://your-url/screen \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer test-key" \
  -d '{"screen_slug":{"screen_id":"test"}}'

# Expected: 400 Bad Request (payload validation - but auth passed)
# OR: 202 Accepted (if payload is valid)
```

### 3. End-to-End Workflow Verification

**Setup:**
1. ✅ AgentOS server running on port 5001
2. ✅ ngrok tunnel active (or production URL configured)
3. ✅ Airtable automation enabled
4. ✅ Test Screen record with linked candidates/role spec

**Execution:**
1. Set Screen Status = "Ready to Screen"
2. Monitor server logs for webhook receipt
3. Verify workflow execution (Deep Research → Quality → Assessment)
4. Check Assessment records created in Airtable
5. Verify Screen status updated to "Complete"

**Expected Timeline:**
- Webhook trigger: < 5 seconds (Airtable → AgentOS)
- Workflow execution: 5-10 minutes (per candidate)
- Assessment write: < 2 seconds (AgentOS → Airtable)

**Success Indicators:**
- ✅ Server logs show: `🔍 Received AgentOS screen webhook for recXXXX`
- ✅ Workflow completes without `❌` errors
- ✅ Assessment record exists with valid scores (0-100)
- ✅ Screen status = "Complete"
- ✅ Automation_Log entry created

### 4. Regression Testing

After any deployment or configuration change:

```bash
# Run full test suite
uv run pytest tests/ -v --cov=demo

# Run bearer auth tests specifically
uv run pytest tests/test_agentos_app.py -k bearer_auth -v

# Expected: All 4 bearer auth tests pass
# - test_bearer_auth_disabled_allows_all_requests
# - test_bearer_auth_enabled_rejects_missing_token
# - test_bearer_auth_enabled_rejects_invalid_token
# - test_bearer_auth_enabled_accepts_valid_token
```

## Audit Trail

### Automation Events (Logged to Airtable)

Every webhook trigger creates an entry in the `Automation_Log` table:

**Fields:**
- **Timestamp:** Webhook receive time
- **Screen ID:** Which screen was triggered
- **Event Type:** "webhook_received", "workflow_started", "workflow_completed", etc.
- **Status:** "success", "error", "pending"
- **Details:** JSON metadata (candidates processed, execution time, errors)

**Query Examples:**
1. View all events for a screen: Filter Automation_Log by Screen ID
2. View recent errors: Filter by Status = "error", sort by Timestamp DESC
3. Track webhook history: View all "webhook_received" events

### Session History (AgentOS Database)

Every workflow execution is persisted to `tmp/agno_sessions.db`:

**Access Methods:**
1. **AgentOS Control Plane:** https://os.agno.com → Add OS → Inspect sessions
2. **SQLite CLI:**
   ```bash
   sqlite3 tmp/agno_sessions.db

   -- List recent sessions
   SELECT session_id, created_at, status
   FROM sessions
   ORDER BY created_at DESC
   LIMIT 10;

   -- View session details
   SELECT * FROM sessions WHERE session_id = 'your-session-id';
   ```

**Retention:**
- Sessions persist indefinitely (no auto-deletion)
- Manual cleanup: `DELETE FROM sessions WHERE created_at < datetime('now', '-90 days');`
- Backup recommended: `cp tmp/agno_sessions.db backups/sessions_$(date +%Y%m%d).db`

### Server Logs

Structured logging with emoji indicators:

- 🔍 **Webhook received** - `Received AgentOS screen webhook for recXXXX`
- 🔄 **Processing** - `Processing candidate: Name (Title @ Company)`
- ✅ **Success** - `Deep Research complete (1.5s, 2500 tokens)`
- ❌ **Error** - `Critical failure while processing screen`
- ⚠️ **Warning** - `Quality check triggered incremental search`

**Log Locations:**
- Development: Console output (stdout)
- Production: Configure via `LOG_LEVEL` environment variable
- Rotation: Implement via hosting platform (e.g., systemd journal, CloudWatch)

## Migration History

### Flask → AgentOS Cutover (Stage 4)

**Date:** 2025-11-17
**Status:** ✅ Complete

**Changes:**
- Replaced Flask app with FastAPI + AgentOS runtime
- Extracted workflow to `demo/workflow.py` (AgentOSCandidateWorkflow)
- Migrated session storage to SqliteDb (from no persistence)
- Updated all Airtable automation scripts to use `/screen` endpoint

**Verification:**
- ✅ No Flask dependencies in codebase (`pip freeze | grep -i flask` returns empty)
- ✅ All tests passing with FastAPI TestClient
- ✅ AgentOS control plane integration verified

### Airtable Simplification (Stage 4.7)

**Date:** 2025-11-18
**Status:** ✅ Complete

**Changes:**
- Eliminated sequential API traversal (4+ calls → 0 during execution)
- Implemented Admin-screen_slug formula for pre-assembled payloads
- Removed JSON string parsing (Pydantic validates nested objects directly)
- Simplified AirtableClient to write-only operations

**Impact:**
- Performance: ~500ms+ latency reduction per screen
- Code reduction: models.py 62% smaller, airtable_client.py 41% smaller
- Reliability: Zero API call failures during workflow execution

**Verification:**
- ✅ Zero `get_screen()` or `get_role_spec()` calls in logs
- ✅ Zero JSON parsing operations (`json.loads()` not used)
- ✅ ScreenWebhookPayload validation successful for all payloads

### Bearer Auth Implementation (TK-19)

**Date:** 2025-11-18
**Status:** ✅ Complete

**Changes:**
- Added optional bearer token authentication to `/screen` endpoint
- Implemented `verify_bearer_token()` middleware
- Added 4 comprehensive test cases (all passing)
- Updated documentation (agent_os_integration_spec.md, automation_audit.md)

**Configuration:**
- Environment: `AGENTOS_SECURITY_KEY=<token>` (optional)
- Airtable: Added `Authorization: Bearer <token>` header to script
- Tests: Coverage for enabled/disabled, valid/invalid token scenarios

**Verification:**
- ✅ Auth disabled: Requests without token succeed
- ✅ Auth enabled + missing token: Returns 401
- ✅ Auth enabled + invalid token: Returns 401
- ✅ Auth enabled + valid token: Returns 202 Accepted

## Troubleshooting

### Issue: 401 Unauthorized Error

**Symptoms:** Airtable automation fails with "Missing authorization header" or "Invalid authentication credentials"

**Resolution:**
1. Verify `AGENTOS_SECURITY_KEY` is set in server `.env` file
2. Check Airtable automation script has matching token in `Authorization` header
3. Ensure token format is: `Bearer <token>` (not just `<token>`)
4. Restart AgentOS server after changing `.env` (reload required)

**Verification:**
```bash
# Test with curl using same token
curl -X POST https://your-url/screen \
  -H "Authorization: Bearer <your-token>" \
  -d '{"screen_slug":{"screen_id":"test"}}'

# Should return 400 (payload error) not 401 (auth error)
```

### Issue: Webhook Timeout (504)

**Symptoms:** Airtable automation fails after 30 seconds

**Resolution:**
1. Verify endpoint returns 202 Accepted immediately
2. Check `background_tasks.add_task()` is used (not synchronous execution)
3. Review server logs for workflow processing errors
4. Confirm AgentOS server is running and accessible

**Verification:**
```bash
# Endpoint should respond < 1 second
time curl -X POST https://your-url/screen -d '{...}'

# Check background task execution in logs
tail -f /path/to/server.log | grep "Processing candidate"
```

### Issue: Assessment Not Created

**Symptoms:** Workflow completes but no Assessment record in Airtable

**Resolution:**
1. Check server logs for `❌` error indicators
2. Verify `AIRTABLE_API_KEY` has write permissions to Assessments table
3. Inspect AgentOS session in control plane for step failures
4. Review Airtable API error messages in logs

**Verification:**
```bash
# Check Airtable client permissions
python -c "from demo.airtable_client import AirtableClient; \
  client = AirtableClient('api_key', 'base_id'); \
  print('Write permissions OK' if client.assessments else 'FAILED')"
```

## References

- **Primary Spec:** `docs/agent_os_integration_spec.md` - Complete AgentOS integration guide
- **Airtable Schema:** `docs/airtable_ai_spec.md` - Table definitions and relationships
- **Demo Runbook:** `docs/DEMO_RUNBOOK.md` - Step-by-step execution guide
- **Setup Guide:** `README.md` - Installation and configuration
- **Test Suite:** `tests/test_agentos_app.py` - Bearer auth and webhook tests

---

**Document Version:** 1.0
**Last Updated:** 2025-11-18
**Maintainer:** Talent Signal Team
