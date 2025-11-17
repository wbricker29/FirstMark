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

## Workflow Orchestration

The screening workflow executes a 4-step linear pipeline that coordinates research, quality checking, and assessment agents.

### Execution Flow

```
1. Deep Research → 2. Quality Check → 3. Incremental Search (conditional) → 4. Assessment
```

**Step 1: Deep Research**
- Agent: `o4-mini-deep-research`
- Executes comprehensive candidate research using built-in web search
- Returns markdown report + citations

**Step 2: Quality Gate**
- Heuristic check: `≥3 unique citations` AND `non-empty summary`
- Pass → proceed to Assessment
- Fail → trigger Incremental Search

**Step 3: Incremental Search (Conditional)**
- Agent: `gpt-5-mini` + web_search_preview
- Triggered only when quality gate fails
- Single-pass: max 2 web searches to fill gaps
- Results merged with original research

**Step 4: Assessment**
- Agent: `gpt-5-mini` + ReasoningTools
- Evaluates candidate against role spec
- Outputs structured assessment with dimension scores

### Session State Persistence

**Storage:** SqliteDb at `tmp/agno_sessions.db`

Session state tracks:
- `screen_id`: Airtable record ID
- `candidate_id`: Candidate record ID
- `candidate_name`: For logging
- `last_step`: Most recent completed step
- `quality_gate_triggered`: Whether incremental search ran

**Why SqliteDb?** Persistent audit trail for demo review. InMemoryDb deferred to Phase 2+ fast mode.

### Event Streaming & Logging

**Configuration:** `stream_events=True` on Workflow creation

**Log Format:** INFO level with emoji indicators
- 🔍 Step start (research, quality check, assessment)
- ✅ Step success with metadata (citation count, scores)
- 🔄 Incremental search triggered
- ❌ Errors with context

**Example Output:**
```
2025-11-17 | INFO | 🔍 Starting deep research for Alex Rivera (CFO at Armis)
2025-11-17 | INFO | ✅ Deep research completed for Alex Rivera with 4 citations
2025-11-17 | INFO | 🔍 Checking research quality for Alex Rivera
2025-11-17 | INFO | ✅ Research quality threshold met for Alex Rivera
2025-11-17 | INFO | 🔍 Starting assessment for Alex Rivera
2025-11-17 | INFO | ✅ Assessment complete for Alex Rivera (overall_score=95.0)
```

### Error Handling

**Retry Configuration:** All agents use exponential backoff
- `retries=2` (Deep Research, Assessment)
- `retries=1` (Incremental Search - lightweight)
- `exponential_backoff=True`
- `delay_between_retries=1s`

**Failure Behavior:**
- Agent retries automatically on transient failures
- Session state preserved on errors (no corruption)
- Clear RuntimeError raised after retry exhaustion
- Logs capture failure context with ❌ indicator

### Usage Example

```python
from demo.agents import screen_single_candidate

# Candidate data from Airtable People table
candidate = {
    "id": "recABC123",
    "name": "Alex Rivera",
    "current_title": "CFO",
    "current_company": "Armis",
    "linkedin_url": "https://linkedin.com/in/alex-rivera"
}

# Role spec markdown from Airtable Role_Specs table
role_spec = """
# CFO Role Specification
## Must-Haves
- 10+ years finance leadership
- B2B SaaS experience
- Series B+ fundraising
...
"""

# Execute full workflow
assessment = screen_single_candidate(
    candidate_data=candidate,
    role_spec_markdown=role_spec,
    screen_id="recSCREEN001"
)

# Access results
print(f"Overall Score: {assessment.overall_score}")
print(f"Confidence: {assessment.overall_confidence}")
print(f"Summary: {assessment.summary}")

for score in assessment.dimension_scores:
    print(f"{score.dimension}: {score.score}/5 ({score.confidence})")
```

**Output Schema:** Returns `AssessmentResult` Pydantic model with:
- `overall_score`: 0-100 scale (or None if insufficient evidence)
- `overall_confidence`: High/Medium/Low
- `dimension_scores`: List of scored evaluation dimensions
- `summary`: 2-3 sentence topline assessment
- `must_haves_check`: Requirements verification
- `green_flags` / `red_flags_detected`: Signal extraction
- `counterfactuals`: "Why candidate might NOT be ideal"

### Design Decisions

**Linear (not parallel):** Single candidate, synchronous processing. Simplifies v1 implementation and demo presentation. Parallel execution deferred to Phase 2+.

**Quality Gate (not multi-iteration):** Single incremental search pass (max 2 web searches) balances quality improvement with execution speed. Prevents infinite research loops.

**SqliteDb (not InMemoryDb):** Persistent session history enables post-demo review of workflow execution. Critical for demonstrating thinking process to FirstMark team.

**No Custom Event Tables:** Uses Agno-managed session tables only. Custom WorkflowEvent model and event persistence deferred to Phase 2+ production features.

## Flask Webhook Server Setup

The Flask webhook server integrates with Airtable automations to trigger candidate screening workflows.

### Local Development with ngrok

For webhook testing during development, you'll need to expose your local Flask server to the internet using ngrok.

#### Install ngrok

**macOS (Homebrew):**
```bash
brew install ngrok/ngrok/ngrok
```

**Other Platforms:**
Download from [ngrok.com/download](https://ngrok.com/download)

**Verify Installation:**
```bash
ngrok version
```

#### Setup ngrok Authentication

1. Sign up for a free account at [ngrok.com](https://ngrok.com)
2. Get your auth token from the dashboard
3. Configure ngrok:
   ```bash
   ngrok config add-authtoken YOUR_AUTH_TOKEN
   ```

### Running the Flask Server

#### 1. Configure Environment Variables

Ensure your `.env` file contains:
```bash
AIRTABLE_API_KEY=patYOUR_PAT_HERE
AIRTABLE_BASE_ID=appYOUR_BASE_ID
OPENAI_API_KEY=sk-YOUR_KEY_HERE
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
FLASK_DEBUG=true
```

#### 2. Start the Flask Server

Activate your virtual environment and run the server:
```bash
source .venv/bin/activate
python demo/app.py
```

You should see:
```
🔍 Starting Flask development server on 0.0.0.0:5000
 * Running on http://0.0.0.0:5000
```

#### 3. Start ngrok Tunnel

In a **separate terminal window**, start ngrok:
```bash
ngrok http 5000
```

You'll see output like:
```
Session Status                online
Forwarding                    https://abc123.ngrok.io -> http://localhost:5000
```

**Copy the HTTPS URL** (e.g., `https://abc123.ngrok.io`) - you'll need this for Airtable automation configuration.

### Configuring Airtable Automation

#### 1. Open Your Airtable Base

Navigate to your Talent Signal base (the one with `AIRTABLE_BASE_ID` from your `.env`)

#### 2. Create Automation

1. Click **Automations** in the top toolbar
2. Click **Create automation**
3. Name it: "Trigger Candidate Screening"

#### 3. Configure Trigger

1. **Trigger Type:** When record matches conditions
2. **Table:** Screens
3. **Conditions:**
   - When: `status`
   - Changes to: `Ready to Screen`

#### 4. Add Webhook Action

1. Click **+ Add action**
2. Select **Send a request to a URL**
3. Configure webhook:
   - **Method:** POST
   - **URL:** `https://YOUR_NGROK_URL.ngrok.io/screen` (replace with your ngrok URL)
   - **Headers:** Add header
     - Key: `Content-Type`
     - Value: `application/json`
   - **Body:** JSON
     ```json
     {
       "screen_id": "{RECORD_ID}"
     }
     ```
     (Use the Insert field button to select RECORD_ID)

#### 5. Test the Automation

1. Turn on the automation (toggle in top right)
2. Go to your Screens table
3. Find or create a test Screen record with:
   - Linked candidates (at least one)
   - Linked search with role spec
4. Change the `status` field to "Ready to Screen"

### Manual Testing Workflow

#### Pre-Test Checklist

Before triggering the webhook, verify:

1. ✅ Flask server is running (check terminal for startup logs)
2. ✅ ngrok tunnel is active (check ngrok terminal for "online" status)
3. ✅ Airtable automation is enabled
4. ✅ Test Screen record has:
   - Valid `screen_id` (starts with "rec")
   - At least one linked candidate
   - Linked search with valid role spec
   - Role spec has `structured_spec_markdown` content
5. ✅ Environment variables are set (`.env` loaded)
6. ✅ All dependencies installed (`uv pip list` shows flask, pyairtable, agno)

#### Execute Test

1. **Start Flask server:**
   ```bash
   source .venv/bin/activate
   python demo/app.py
   ```

2. **Start ngrok (separate terminal):**
   ```bash
   ngrok http 5000
   ```

3. **Configure Airtable automation** with ngrok URL (see above)

4. **Trigger automation:**
   - Open Screens table in Airtable
   - Update test record `status` → "Ready to Screen"

5. **Monitor Flask logs:**
   Watch for these log indicators:
   ```
   🔍 Received screen webhook for recXXXX
   🔍 Starting deep research for [Candidate Name]
   ✅ Deep research completed for [Candidate Name] with N citations
   ✅ Assessment complete for [Candidate Name] (overall_score=XX)
   ✅ Screen recXXXX completed (N successes, 0 failures)
   ```

6. **Verify Airtable results:**
   - Screen `status` updated to "Complete"
   - New Assessment records created in Assessments table
   - Assessment records contain:
     - `overall_score` (0-100)
     - `overall_confidence` (High/Medium/Low)
     - `topline_summary` (2-3 sentences)
     - `assessment_json` (full structured output)

#### Test curl Command (Alternative)

If you want to test the endpoint directly without Airtable:
```bash
curl -X POST http://localhost:5000/screen \
  -H "Content-Type: application/json" \
  -d '{"screen_id": "recYOUR_TEST_SCREEN_ID"}'
```

Expected response:
```json
{
  "status": "success",
  "screen_id": "recXXXX",
  "candidates_total": 1,
  "candidates_processed": 1,
  "candidates_failed": 0,
  "execution_time_seconds": 45.23,
  "results": [
    {
      "candidate_id": "recYYYY",
      "assessment_id": "recZZZZ",
      "overall_score": 85.0,
      "confidence": "High",
      "summary": "Strong CFO candidate with relevant B2B SaaS experience..."
    }
  ]
}
```

### Troubleshooting

#### Flask Server Won't Start

**Error:** `Missing required environment variables: AIRTABLE_API_KEY`
- **Fix:** Verify `.env` file exists and contains all required keys
- **Check:** Run `cat .env` to confirm variables are set

**Error:** `Address already in use`
- **Fix:** Kill existing process on port 5000:
  ```bash
  lsof -ti:5000 | xargs kill -9
  ```

#### ngrok Connection Issues

**Error:** `ERR_NGROK_108`
- **Fix:** Verify ngrok auth token is configured:
  ```bash
  ngrok config check
  ```

**Error:** `Session expired`
- **Fix:** Free ngrok sessions expire after 2 hours. Restart ngrok and update Airtable automation URL.

#### Webhook Not Triggering

1. **Check Airtable automation logs:**
   - Open automation
   - Click "Runs" tab
   - Look for errors or failed requests

2. **Verify ngrok URL is correct:**
   - Ensure you're using HTTPS (not HTTP)
   - Include `/screen` path: `https://abc123.ngrok.io/screen`

3. **Test with curl first:**
   - Use the curl command above to verify Flask endpoint works
   - If curl works but Airtable doesn't, issue is with automation config

#### Workflow Execution Errors

**Error:** `Screen missing linked role spec`
- **Fix:** Ensure Screen → Search → Role Spec linkage is complete

**Error:** `No candidates linked to screen`
- **Fix:** Add at least one candidate to the Screen's "Candidates" field

**Error:** `Role spec missing structured markdown content`
- **Fix:** Populate the `structured_spec_markdown` field in the Role Spec record

### Smoke Test Checklist (Pre-Demo)

Use this checklist to validate the full webhook integration before your demo:

#### Environment Setup
- [ ] Virtual environment activated (`.venv`)
- [ ] All dependencies installed (`uv pip list` confirms flask, pyairtable, agno, openai)
- [ ] `.env` file contains all required keys (AIRTABLE_API_KEY, AIRTABLE_BASE_ID, OPENAI_API_KEY)
- [ ] Port 5000 is available (not in use)

#### Airtable Data Preparation
- [ ] Test Screen record exists with status != "Ready to Screen"
- [ ] Screen has ≥1 linked candidate with profile data
- [ ] Screen linked to Search record
- [ ] Search linked to Role_Spec record
- [ ] Role_Spec has populated `structured_spec_markdown` field

#### Server & Tunnel
- [ ] Flask server starts without errors (`python demo/app.py`)
- [ ] Startup logs show: "✅ Flask app initialized"
- [ ] ngrok tunnel active (`ngrok http 5000`)
- [ ] ngrok shows "Session Status: online"
- [ ] Copied ngrok HTTPS URL (e.g., `https://abc123.ngrok.io`)

#### Airtable Automation Configuration
- [ ] Automation created in Airtable
- [ ] Trigger: "When record matches conditions" → Screens → status = "Ready to Screen"
- [ ] Action: "Send request" → POST → `https://YOUR_NGROK_URL/screen`
- [ ] Request body includes `{"screen_id": "{RECORD_ID}"}`
- [ ] Automation is enabled (toggle ON)

#### Execution Test
- [ ] Changed Screen status → "Ready to Screen" in Airtable
- [ ] Flask logs show: "🔍 Received screen webhook for recXXXX"
- [ ] Workflow executes without ❌ errors
- [ ] Flask logs show: "✅ Screen recXXXX completed"
- [ ] Screen status updated to "Complete" in Airtable
- [ ] New Assessment record(s) created in Assessments table
- [ ] Assessment contains:
  - [ ] `overall_score` (numeric, 0-100)
  - [ ] `overall_confidence` (High/Medium/Low)
  - [ ] `topline_summary` (non-empty text)
  - [ ] `assessment_json` (valid JSON)

#### Post-Test Verification
- [ ] Execution time <10 minutes per candidate
- [ ] No memory errors or crashes
- [ ] Logs are readable and helpful (emoji indicators visible)
- [ ] Can trigger multiple Screens sequentially without server restart

#### Demo Readiness
- [ ] 3+ pre-run Screens completed successfully (Pigment CFO, Mockingbird CFO, Synthesia CTO)
- [ ] 1 live demo Screen prepared (Estuary CTO) with status = "Pending" (not triggered yet)
- [ ] ngrok tunnel URL documented for live demo
- [ ] Backup plan if ngrok fails (curl command ready)

**Note:** For production deployment, replace ngrok with a proper hosting solution (Cloud Run, Heroku, etc.) with static URLs.

## Case Study Resources

- **Directory:** `case/`
- **Brief:** `case/FirstMark_case.md`
- **Specifications:** `spec/`
- **Reference Materials:** `reference/`
