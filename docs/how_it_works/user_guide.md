# User Guide

This guide explains how to use the Talent Signal Agent's features.

## API Endpoints

The Talent Signal Agent exposes two endpoints: a webhook endpoint for screening workflows and a health check endpoint for monitoring.

### POST /screen

The primary way to interact with the Talent Signal Agent is through its webhook endpoint.

### Authentication

The endpoint is protected by a bearer token (optional). If `AGENTOS_SECURITY_KEY` is set in your `.env` file, you must include an `Authorization` header with your request:

`Authorization: Bearer YOUR_AGENTOS_SECURITY_KEY`

Replace `YOUR_AGENTOS_SECURITY_KEY` with the value you set in your `.env` file.

### Request Payload

The endpoint expects a JSON payload matching the `ScreenWebhookPayload` structure. Airtable sends structured nested objects (not JSON strings), so no parsing is needed.

```json
{
  "screen_slug": {
    "screen_id": "recABC123",
    "screen_edited": "2025-11-18T20:01:46.000Z",
    "role_spec_slug": {
      "role_spec": {
        "role_spec_id": "recRS123",
        "role_spec_name": "CFO - Series B",
        "role_spec_content": "# Role Spec\n\n## Evaluation Framework\n..."
      }
    },
    "search_slug": {
      "role": {
        "ATID": "recR123",
        "portco": "Pigment",
        "role_type": "CFO",
        "role_title": "",
        "role_description": "The CFO will be responsible for..."
      }
    },
    "candidate_slugs": [
      {
        "candidate": {
          "ATID": "recP1",
          "candidate_name": "Jane Doe",
          "candidate_current_title": "CFO",
          "candidate_current_company": "Acme Inc",
          "candidate_linkedin": "https://www.linkedin.com/in/janedoe/",
          "candidate_location": "San Francisco, CA",
          "candidate_bio": "Experienced CFO with..."
        }
      }
    ]
  }
}
```

**Key Fields:**

-   `screen_slug` (object): Complete screen record data
    -   `screen_id` (string): Airtable record ID for the screen
    -   `role_spec_slug.role_spec.role_spec_content` (string): Role specification markdown (immutable snapshot)
    -   `search_slug.role` (object): Role information (portco, role_type, role_description)
    -   `candidate_slugs[]` (array): Array of candidate objects, each containing:
        -   `candidate.ATID` (string): Candidate Airtable record ID
        -   `candidate.candidate_name` (string): Candidate full name
        -   `candidate.candidate_current_title` (string): Current job title
        -   `candidate.candidate_current_company` (string): Current company name
        -   `candidate.candidate_linkedin` (string): LinkedIn profile URL
        -   `candidate.candidate_location` (string): Geographic location
        -   `candidate.candidate_bio` (string): Candidate biography text

**Note:** The payload structure uses nested objects as sent by Airtable automations. The Python code validates this structure using the `ScreenWebhookPayload` Pydantic model (see `demo/models.py`).

### Response

The webhook triggers the screening workflow asynchronously. The endpoint returns immediately with a JSON response indicating the workflow has started:

**Success Response (202 Accepted):**
```json
{
  "status": "accepted",
  "message": "Screen workflow started",
  "screen_id": "recABC123",
  "candidates_queued": 3
}
```

**Error Responses:**

**400 Bad Request - Invalid Payload:**
```json
{
  "detail": "Validation error: field 'candidate.candidate_name' is required"
}
```
*Common causes:*
- Missing required fields (screen_id, candidate.ATID, candidate.candidate_name, role_spec_content)
- Malformed nested structure (e.g., flat JSON instead of nested objects)
- Invalid data types (e.g., string instead of array for candidate_slugs)

**401 Unauthorized - Missing/Invalid Bearer Token:**
```json
{
  "detail": "Invalid or missing authorization token"
}
```
*Cause:* `AGENTOS_SECURITY_KEY` is configured but request lacks valid `Authorization: Bearer <token>` header

**500 Internal Server Error - Workflow Initialization Failed:**
```json
{
  "detail": "Failed to initialize screening workflow"
}
```
*Common causes:*
- OpenAI API key invalid or expired
- Airtable API connection failure
- Internal database error (session persistence)

### Testing the Endpoint

**Example curl command:**

```bash
# Without authentication (if AGENTOS_SECURITY_KEY not set)
curl -X POST http://localhost:5001/screen \
  -H "Content-Type: application/json" \
  -d '{
    "screen_slug": {
      "screen_id": "recTEST123",
      "screen_edited": "2025-11-19T12:00:00.000Z",
      "role_spec_slug": {
        "role_spec": {
          "role_spec_id": "recRS001",
          "role_spec_name": "CFO - Test",
          "role_spec_content": "# CFO Role\n\n## Must-Haves\n- 10+ years finance leadership\n\n## Evaluation Dimensions\n- Fundraising Experience (1-5)\n- Team Building (1-5)"
        }
      },
      "search_slug": {
        "role": {
          "ATID": "recR001",
          "portco": "Test Company",
          "role_type": "CFO",
          "role_title": "Chief Financial Officer",
          "role_description": "Lead all finance operations"
        }
      },
      "candidate_slugs": [
        {
          "candidate": {
            "ATID": "recP001",
            "candidate_name": "Jane Doe",
            "candidate_current_title": "VP Finance",
            "candidate_current_company": "Acme Corp",
            "candidate_linkedin": "https://linkedin.com/in/janedoe",
            "candidate_location": "San Francisco, CA",
            "candidate_bio": "Finance leader with 12 years experience"
          }
        }
      ]
    }
  }'
```

**With authentication:**

```bash
# Set security key
export AGENTOS_SECURITY_KEY="your-secret-key-here"

# Make authenticated request
curl -X POST http://localhost:5001/screen \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AGENTOS_SECURITY_KEY" \
  -d @test_payload.json
```

**Expected output (success):**
```
{"status":"accepted","message":"Screen workflow started","screen_id":"recTEST123","candidates_queued":1}
```

### Workflow Execution

**Asynchronous Processing:**
- The screening workflow runs in the background; the HTTP call returns immediately (202 Accepted)
- This prevents Airtable automation timeouts (Airtable has 30-second webhook limits)
- Each candidate processes independently - if one fails, others continue

**Workflow Steps (per candidate):**
1. **Deep Research** (2-3 min) - `o4-mini-deep-research` gathers comprehensive OSINT profile
2. **Quality Check** (instant) - Validates ≥3 citations + non-empty summary
3. **Incremental Search** (1-2 min, conditional) - Runs only if quality gate fails
4. **Assessment** (1-2 min) - `gpt-5-mini` evaluates against role spec

**Data Flow:**
- All role spec + candidate context arrives via the webhook payload
- Python **never reads from Airtable** during processing (write-only pattern)
- Results written to `Platform-Assessments` table
- Screen status updated to "Complete" when all candidates finish

**Monitoring Workflow Progress:**

1. **AgentOS Control Plane** (recommended for real-time monitoring):
   - URL: `https://os.agno.com`
   - Shows live workflow execution with step-by-step progress
   - Displays token usage, execution time per step
   - Session format: `screen_{screen_id}_{candidate_id}`

2. **Airtable Automation Log** (for error tracking):
   - Table: `Operations-Automation_Log`
   - Filter by `screen_id` to see all events for your Screen
   - Check for error messages if workflow fails

3. **Assessment Table** (for results):
   - Table: `Platform-Assessments`
   - Filter by linked Screen to see completed assessments
   - New records appear as candidates complete (incremental updates)

### Rate Limits and Performance

**OpenAI API Limits:**
- Tier-dependent (check your OpenAI account dashboard)
- Typical limits: 10,000 requests/day, 3,000,000 tokens/day (Tier 2)
- Deep research uses ~3,000-5,000 tokens per candidate
- Assessment uses ~2,000-3,000 tokens per candidate
- **Estimate:** 10-candidate screen ≈ 50,000-80,000 tokens

**Processing Capacity:**
- Single workflow: 3-5 minutes per candidate
- Parallel processing: Limited by OpenAI rate limits (RPM)
- Recommended batch size: 5-15 candidates per screen for optimal performance

**Retry Behavior:**
- OpenAI rate limit errors (429): Automatic exponential backoff (Agno framework handles this)
- Transient failures: Up to 3 retries per step
- Permanent failures: Logged to Operations-Automation_Log, Screen marked "Failed"

### Error Handling Best Practices

**Validation Errors (400):**
- Test payload structure with curl before setting up Airtable automation
- Use the example payload above as a template
- Verify nested object structure (not JSON strings)

**Authentication Errors (401):**
- If using bearer auth, ensure `Authorization` header is included in automation script
- Verify `AGENTOS_SECURITY_KEY` matches between server .env and automation

**Workflow Failures (500 or incomplete assessments):**
- Check OpenAI API key validity: `curl https://api.openai.com/v1/models -H "Authorization: Bearer $OPENAI_API_KEY"`
- Check Airtable API access: verify base ID and API key in server .env
- Review Operations-Automation_Log for specific error messages

**Recovery from Failures:**
- Failed screens can be retried by changing status to "Draft" then back to "Ready to Screen"
- Existing assessments won't be duplicated (keyed by candidate + screen)
- Partial completions: If 5/10 candidates completed before failure, re-triggering will process remaining 5

### GET /healthz

Simple health check endpoint for monitoring and smoke tests. Useful for verifying the server is running and accessible.

**Endpoint:** `GET /healthz`

**Authentication:** None required

**Response (200 OK):**
```json
{
  "status": "ok"
}
```

**Use Cases:**
- Health checks for load balancers or monitoring systems
- Smoke tests during deployment
- Verifying server accessibility before triggering screens

**Example curl command:**
```bash
curl http://localhost:5001/healthz
```

**Expected output:**
```json
{"status":"ok"}
```
