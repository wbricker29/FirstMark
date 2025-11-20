# Talent Signal Agent - Demo Runbook

**Complete guide for setting up and running the Talent Signal Agent demo**

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Prerequisites](#prerequisites)
3. [Initial Setup](#initial-setup)
4. [Demo Infrastructure Setup](#demo-infrastructure-setup)
5. [Pre-Demo Preparation](#pre-demo-preparation)
6. [Live Demo Execution](#live-demo-execution)
7. [Troubleshooting](#troubleshooting)
8. [Quick Reference](#quick-reference)

---

## Quick Start

### Are you new to this demo?

**→ Follow the Full Setup path** (Sections 2-4, ~30 minutes)

### Have you run this demo before?

**→ Follow the Quick Start path** (5 minutes)

### Quick Start Path (Experienced Users)

If you've already completed the full setup once, you can skip to Section 4 and just start the demo infrastructure:

1. ✅ **Verify prerequisites** (Section 2) - Accounts and API keys ready
2. ✅ **Start AgentOS server** (Section 4.1) - Terminal 1
3. ✅ **Start ngrok tunnel** (Section 4.2) - Terminal 2
4. ✅ **Connect control plane** (Section 4.3) - Optional but recommended
5. ✅ **Verify Airtable automation** (Section 4.4) - Check it's still configured
6. ✅ **Test connection** (Section 4.5) - Run a quick test

**Time estimate:** 5 minutes

---

### Common Mistakes to Avoid

⚠️ **Don't skip these!**

- ❌ Starting ngrok before AgentOS server (connection will fail)
- ❌ Using HTTP instead of HTTPS for ngrok URL in Airtable
- ❌ Forgetting to enable the Airtable automation (toggle must be ON)
- ❌ Using an expired ngrok session (free tier expires after 2 hours)
- ❌ Missing `/screen` path in the webhook URL

---

## Prerequisites

Before you begin, make sure you have everything listed below. This section tells you what you need and how to get it.

### Estimated Time: 15-20 minutes (first time)

---

### 1. Accounts You Need

#### Airtable Account
- **What it is:** Cloud database where candidate data and results are stored
- **How to get it:** Sign up at [airtable.com](https://airtable.com) (free tier works)
- **What you'll need:** 
  - Access to a base (database) with the Talent Signal tables
  - A Personal Access Token (API key) - see "API Keys" section below

#### OpenAI Account
- **What it is:** Provides the AI models that do the research and assessment
- **How to get it:** Sign up at [platform.openai.com](https://platform.openai.com)
- **What you'll need:**
  - An API key with billing enabled (the demo uses paid API calls)
  - Access to `o4-mini-deep-research` and `gpt-5-mini` models

#### ngrok Account
- **What it is:** Creates a secure tunnel so Airtable can reach your local server
- **How to get it:** Sign up at [ngrok.com](https://ngrok.com) (free tier works)
- **What you'll need:**
  - An auth token from the dashboard (needed to run ngrok)

#### AgentOS Control Plane (Optional)
- **What it is:** Web UI for monitoring the demo in real-time
- **How to get it:** Sign up at [os.agno.com](https://os.agno.com) (free account)
- **Why it's useful:** Shows workflow progress visually during demos

---

### 2. Software You Need

#### Python 3.11 or Higher
- **What it is:** Programming language the demo runs on
- **How to check:** Open a terminal and run:
  ```bash
  python --version
  ```
- **Expected output:** `Python 3.11.x` or higher
- **If you don't have it:** Download from [python.org](https://www.python.org/downloads/)

#### UV Package Manager
- **What it is:** Tool for managing Python dependencies (like npm for Node.js)
- **How to check:** Run:
  ```bash
  uv --version
  ```
- **If you don't have it:** Install with:
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
- **Why we use it:** Faster and more reliable than pip for dependency management

#### ngrok (Command Line Tool)
- **What it is:** Command-line tool that creates the secure tunnel
- **How to check:** Run:
  ```bash
  ngrok version
  ```
- **If you don't have it:**
  - **macOS:** `brew install ngrok/ngrok/ngrok`
  - **Other platforms:** Download from [ngrok.com/download](https://ngrok.com/download)

---

### 3. API Keys Setup

You'll need to collect these API keys and save them - you'll add them to a `.env` file in the next section.

#### Airtable Personal Access Token

1. Go to [airtable.com/account](https://airtable.com/account)
2. Scroll to "Personal access tokens"
3. Click "Create new token"
4. Give it a name (e.g., "Talent Signal Demo")
5. Set scopes: `data.records:read`, `data.records:write`, `schema.bases:read`
6. Select the base(s) you want to access
7. Click "Create token"
8. **Copy the token immediately** - it starts with `pat...` and you won't see it again

**Save this as:** `AIRTABLE_API_KEY` (you'll use it in Section 3)

#### Airtable Base ID

1. Open your Airtable base in a web browser
2. Look at the URL: `https://airtable.com/appXXXXXXXXXXXXXX/...`
3. The Base ID is the part after `/app` - it starts with `app...`

**Save this as:** `AIRTABLE_BASE_ID` (you'll use it in Section 3)

#### OpenAI API Key

1. Go to [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Click "Create new secret key"
3. Give it a name (e.g., "Talent Signal Demo")
4. Click "Create secret key"
5. **Copy the key immediately** - it starts with `sk-...` and you won't see it again

**Save this as:** `OPENAI_API_KEY` (you'll use it in Section 3)

**Important:** Make sure billing is enabled on your OpenAI account, as the demo makes paid API calls.

#### ngrok Auth Token

1. Go to [dashboard.ngrok.com/get-started/your-authtoken](https://dashboard.ngrok.com/get-started/your-authtoken)
2. Copy your auth token
3. Configure it (one-time setup):
   ```bash
   ngrok config add-authtoken YOUR_AUTH_TOKEN
   ```

**Why this is needed:** ngrok requires authentication to create tunnels.

---

### 4. Verification Checklist

Before moving to Initial Setup, verify you have:

- [ ] Python 3.11+ installed (`python --version` works)
- [ ] UV installed (`uv --version` works)
- [ ] ngrok installed (`ngrok version` works)
- [ ] ngrok auth token configured (`ngrok config check` shows no errors)
- [ ] Airtable Personal Access Token copied (starts with `pat...`)
- [ ] Airtable Base ID copied (starts with `app...`)
- [ ] OpenAI API Key copied (starts with `sk-...`)
- [ ] OpenAI account has billing enabled

**If anything is missing, go back and complete it before continuing.**

---

## Initial Setup

This section covers the one-time setup you need to do before running any demo. Once complete, you can skip this section for future demos.

### Estimated Time: 10-15 minutes

---

### Step 1: Install Dependencies

The demo needs several Python packages. The Makefile automates the entire setup process.

1. **Navigate to the project directory:**
   ```bash
   cd /path/to/FirstMark
   ```
   (Replace with your actual path)

2. **Run the setup command:**
   ```bash
   make setup
   ```

   **What this does:**
   - Verifies Python 3.11+ is installed
   - Installs UV package manager (if needed)
   - Installs all required packages (agno, fastapi, pyairtable, openai, etc.)
   - Creates `.env` file from `.env.example` (if it doesn't exist)
   - Verifies the installation

   **Expected output:** You'll see progress indicators with ✅ checkmarks and a completion message.

   **Alternative (manual installation):**
   ```bash
   uv pip install -e .
   ```

3. **Verify installation:**
   ```bash
   make verify-deps
   ```

   **Expected output:** `✅ Required packages installed` and `✅ Models loaded successfully`

   **If this doesn't work:** Make sure you're in the project directory and Python 3.11+ is installed.

---

### Step 2: Configure Environment Variables

The demo needs your API keys to connect to Airtable and OpenAI. You'll store them in a `.env` file.

1. **Create or edit the `.env` file:**
   ```bash
   # In the project root directory
   nano .env
   # Or use any text editor (VS Code, vim, etc.)
   ```

   **Note:** If you ran `make setup` in Step 1, the `.env` file was created automatically from `.env.example`.

2. **Add your API keys:**
   ```bash
   # Required: Airtable credentials
   AIRTABLE_API_KEY=patYOUR_PAT_HERE
   AIRTABLE_BASE_ID=appYOUR_BASE_ID_HERE

   # Required: OpenAI API key
   OPENAI_API_KEY=sk-YOUR_KEY_HERE

   # Optional: Server configuration (defaults work fine)
   FASTAPI_HOST=0.0.0.0
   FASTAPI_PORT=5001
   FASTAPI_DEBUG=true

   # Optional: AgentOS security (only if you want bearer token auth)
   # AGENTOS_SECURITY_KEY=super-secret-token
   ```

   **Replace the placeholder values** with your actual keys from the Prerequisites section.

3. **Save the file** (`.env` should be in the project root directory)

4. **Validate your configuration:**
   ```bash
   make validate-env
   ```

   **Expected output:** `✅ Environment configuration valid`

   **If validation fails:** The command will tell you which keys are missing or incorrectly formatted.

   **Security note:** The `.env` file is already in `.gitignore`, so it won't be committed to version control.

---

### Step 3: Verify Setup

Run these quick tests to make sure everything is configured correctly.

1. **Run smoke tests (recommended):**
   ```bash
   make smoke-test
   ```

   **What this does:**
   - Validates environment variables
   - Verifies dependencies are installed
   - Tests model imports
   - Runs basic functionality tests

   **Expected output:** `✅ Smoke tests passed!`

2. **Or verify components individually:**

   **Test Python imports:**
   ```bash
   make verify-deps
   ```

   **Expected output:** `✅ Required packages installed` and `✅ Models loaded successfully`

   **Test environment variables:**
   ```bash
   make validate-env
   ```

   **Expected output:** `✅ Environment configuration valid`

   **Validate Airtable schema:**
   ```bash
   make validate-airtable
   ```

   **Expected output:** `✅ Airtable schema validation complete`

3. **Run full test suite (optional but recommended):**
   ```bash
   make test-fast
   ```

   **Expected output:** Tests should pass (typically 110 passed, 20 skipped)

---

### Step 4: Verify Port Availability

The demo server runs on port 5001. Make sure nothing else is using it.

1. **Check if port 5001 is in use:**
   ```bash
   lsof -ti:5001
   ```

   **Expected output:** Nothing (empty) - port is free

   **If something is using it:** Kill the process:
   ```bash
   lsof -ti:5001 | xargs kill -9
   ```

---

### Setup Complete! ✅

You've completed the one-time setup. For future demos, you can skip directly to Section 4 (Demo Infrastructure Setup).

**Next:** Move to Section 4 to start the demo infrastructure.

---

## Demo Infrastructure Setup

This section covers starting the demo infrastructure. You'll need to do this each time you run a demo. You'll need **3 terminal windows** open.

### Estimated Time: 5-10 minutes

---

### Step 1: Start AgentOS Server (Terminal 1)

The AgentOS server is the webhook endpoint that receives requests from Airtable and runs the screening workflow.

1. **Open Terminal 1**

2. **Navigate to the project directory:**
   ```bash
   cd /path/to/FirstMark
   ```

3. **Start the AgentOS server:**
   ```bash
   make server
   ```

   **Alternative (same command):**
   ```bash
   make dev
   ```

   **What this does:**
   - Verifies dependencies are installed
   - Validates environment configuration
   - Activates the virtual environment automatically
   - Starts the FastAPI server on port 5001

   **Expected output:**
   ```
   🚀 Starting AgentOS server on port 5001...
   OpenAPI docs will be available at: http://localhost:5001/docs
   Press Ctrl+C to stop

   🔍 Connecting AgentOS runtime to Airtable base appXXXXXXXXXXXXXX
   INFO:     Started server process [12345]
   INFO:     Application startup complete.
   INFO:     Uvicorn running on http://0.0.0.0:5001
   ```

   **What this means:** The server is running and ready to receive requests.

4. **Verify the server is working:**
   - Open a browser and go to: `http://localhost:5001/docs`
   - You should see the OpenAPI documentation page
   - Look for the `/screen` endpoint in the list

   **Keep Terminal 1 open** - the server needs to keep running.

   **If the server won't start:**
   - Check Section 7 (Troubleshooting) for common errors
   - Most common: Missing environment variables or port 5001 already in use

   **Manual startup (if needed):**
   ```bash
   source .venv/bin/activate
   uv run python demo/agentos_app.py
   ```

---

### Step 2: Start ngrok Tunnel (Terminal 2)

ngrok creates a secure tunnel so Airtable can reach your local server from the internet.

1. **Open Terminal 2** (keep Terminal 1 running)

2. **Start ngrok:**
   ```bash
   make tunnel
   ```

   **What this does:**
   - Verifies ngrok is installed
   - Starts tunnel on port 5001
   - Displays the public HTTPS URL

   **Expected output:**
   ```
   🚀 Starting ngrok tunnel on port 5001...
   Copy the HTTPS URL and update your Airtable webhook
   Press Ctrl+C to stop

   Session Status                online
   Account                       Your Name (Plan: Free)
   Forwarding                    https://abc123.ngrok.io -> http://localhost:5001

   Connections                   ttl     opn     rt1     rt5     p50     p90
                                 0       0       0.00    0.00    0.00    0.00
   ```

3. **Copy the HTTPS URL:**
   - Look for the line that says `Forwarding`
   - Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`)
   - **You'll need this URL in the next step**

   **Important:**
   - Use the **HTTPS** URL (not HTTP)
   - Free ngrok sessions expire after 2 hours - you'll need to restart and update Airtable if this happens

   **Keep Terminal 2 open** - ngrok needs to keep running.

   **If ngrok won't start:**
   - The make command will check if ngrok is installed and provide install instructions
   - Make sure you configured the auth token (Prerequisites section)
   - Check Section 7 (Troubleshooting) for ngrok-specific errors

---

### Alternative: Start Both Server and Tunnel Together

If you prefer, you can start both the server and prepare for the tunnel in one step:

```bash
make dev-all
```

**What this does:**
- Starts AgentOS server in the background
- Provides instructions for starting the tunnel
- Logs server output to `/tmp/agentos.log`

**To view server logs:**
```bash
tail -f /tmp/agentos.log
```

**To stop the background server:**
```bash
make stop-dev
```

**Note:** You'll still need to run `make tunnel` in a separate terminal for the ngrok connection.

---

### Step 3: Connect AgentOS Control Plane (Optional but Recommended)

The control plane gives you a visual dashboard to monitor the demo in real-time. This is especially useful during presentations.

1. **Open a web browser** and go to [os.agno.com](https://os.agno.com)

2. **Sign in** (or create a free account if you don't have one)

3. **Add your AgentOS instance:**
   - Click the team/organization dropdown in the top navigation
   - Click the **"+"** button next to "Add new OS"
   - The "Connect your AgentOS" dialog will open

4. **Configure the connection:**
   - **Environment:** Select **"Local"** (for development)
   - **Endpoint URL:** 
     - For local access: `http://localhost:5001`
     - For remote access: Use your ngrok HTTPS URL from Step 2
   - **OS Name:** Give it a descriptive name (e.g., "Talent Signal Demo")
   - **Tags (Optional):** Add tags like `demo`, `talent-signal`

5. **Security (Optional):**
   - If you set `AGENTOS_SECURITY_KEY` in your `.env` file, enter it here
   - Otherwise, leave it blank

6. **Test the connection:**
   - Click **"CONNECT"**
   - The platform will verify the connection
   - Once connected, you'll see your OS in the dashboard

**What you can do with the control plane:**
- View workflow runs in real-time
- See session state as it flows through each step
- Monitor agent activity and outputs
- View structured logs without tailing Terminal 1
- Debug issues by inspecting failed runs

**For live demos:** Connect the control plane before starting, and show it alongside Airtable to demonstrate real-time workflow progress.

---

### Step 4: Configure Airtable Automation

Airtable needs to know where to send webhook requests when a Screen's status changes to "Ready to Screen".

1. **Open your Airtable base** in a web browser

2. **Create or edit the automation:**
   - Click **"Automations"** in the top toolbar
   - Click **"Create automation"** (or edit existing one)
   - Name it: "Trigger Candidate Screening"

3. **Configure the trigger:**
   - **Trigger Type:** "When record matches conditions"
   - **Table:** Screens (or Platform-Screens, depending on your schema)
   - **Conditions:**
     - When: `status`
     - Changes to: `Ready to Screen`

4. **Add the webhook action (script-based):**
   - Click **"+ Add action"**
   - Select **"Run a script"** (not "Send a request")
   - Paste the contents of `scripts/airtable_webhook_automation.js` (located in project root)
   - Update the following script variables before saving:
     - `const WEBHOOK_URL = "https://YOUR_NGROK_URL.ngrok.io/screen"` → replace with your HTTPS ngrok URL (keep the `/screen` suffix)
     - If you set `AGENTOS_SECURITY_KEY`, the script automatically adds the required `Authorization` header (no manual change needed)
     - Confirm the table names (`Platform-Screens`, `Platform-Role_Specs`, etc.) match your base, or rename them in the script
   - The script loads the Screen’s linked Search, Role Spec, and Candidate records, assembles the nested `screen_slug` payload (matching the `ScreenWebhookPayload` schema), and POSTs it to AgentOS. You do **not** need intermediary rollup fields or a "Send request" action—the webhook already contains the entire spec snapshot + candidate data so Python never reads from Airtable during screening.
   - Optional: if you store the full structured payload in a text field (e.g., `Admin-screen_slug`), you can switch to the lightweight script in the same file that reads that field instead of hydrating linked tables.

5. **Enable the automation:**
   - Toggle the switch in the top right to **ON** (green)
   - The automation is now active

**Important:** 
- The script must reference your active HTTPS ngrok URL (`https://...ngrok.io/screen`)
- Keep the automation enabled (toggle ON) so the script runs when status flips to "Ready to Screen"
- If you change any Airtable field names, update them in the script as well

---

### Step 5: Test the Connection

Before running a real demo, test that everything is connected correctly.

1. **Verify all components are running:**
   - [ ] Terminal 1: AgentOS server running (you see logs)
   - [ ] Terminal 2: ngrok tunnel active (shows "online" status)
   - [ ] Browser: Control plane connected (optional)
   - [ ] Airtable: Automation enabled (toggle ON)

2. **Test with curl (optional but recommended):**
   ```bash
   curl -X POST http://localhost:5001/screen \
     -H "Content-Type: application/json" \
     -d '{
           "screen_slug": {
             "screen_id": "recTEST",
             "role_spec_slug": {
               "role_spec": {
                 "role_spec_id": "recSPEC",
                 "role_spec_name": "Demo CFO Spec",
                 "role_spec_content": "### Demo Spec..."
               }
             },
             "search_slug": {
               "role": {
                 "ATID": "recROLE",
                 "portco": "Pigment",
                 "role_type": "CFO",
                 "role_title": "",
                 "role_description": "Demo role description"
               }
             },
             "candidate_slugs": [
               {
                 "candidate": {
                   "ATID": "recCAND",
                   "candidate_name": "Demo Exec",
                   "candidate_current_title": "CFO",
                   "candidate_current_company": "Acme",
                   "candidate_location": "",
                   "candidate_linkedin": "",
                   "candidate_bio": ""
                 }
               }
             ]
           }
         }'
   ```

   **Expected output:** You should see workflow execution logs in Terminal 1 plus a `202 Accepted` JSON response such as:
   ```json
   {
     "status": "accepted",
     "message": "Screen workflow started",
     "screen_id": "recTEST",
     "candidates_queued": 1
   }
   ```

   **If this doesn't work:** Check Section 7 (Troubleshooting) for common issues.

3. **Test via Airtable (full end-to-end):**
   - Go to your Screens table in Airtable
   - Find or create a test Screen record with:
     - At least one linked candidate
     - Linked search with role spec
     - Status set to something other than "Ready to Screen"
   - Change the `status` field to "Ready to Screen"
   - **Watch Terminal 1** - you should see:
     ```
     🔍 Received AgentOS screen webhook for recXXXX
     🔍 Starting deep research for [Candidate Name]
     ✅ Deep research completed for [Candidate Name] with N citations
     ✅ Assessment complete for [Candidate Name] (overall_score=XX)
     ✅ Screen recXXXX completed (N successes, 0 failures)
     ```
   - **Check Airtable:**
     - Screen `status` should update to "Complete"
     - New Assessment record(s) should appear in the Assessments table
     - Assessment should contain `overall_score`, `overall_confidence`, `topline_summary`

**If the test works:** ✅ You're ready for the demo!

**If the test fails:** Check Section 7 (Troubleshooting) for help.

---

## Pre-Demo Preparation

Before running a live demo, you should prepare your data and run a few test scenarios to ensure everything works smoothly.

### Estimated Time: 30-60 minutes (depending on data loading)

---

### Step 1: Load Demo Data

The demo needs candidate data, role specifications, and screening scenarios.

#### Load Executives (Candidates)

1. **Open your Airtable base** → People table

2. **Import candidates:**
   - Option A: Use the `talent-signal-candidate-loader` Claude skill (recommended)
     - Import from `data/mock_candidates.csv`
     - Should load 64 executives
   - Option B: Manual import
     - Export CSV from `data/mock_candidates.csv`
     - Import into People table via Airtable UI

3. **Verify candidates loaded:**
   - Check People table has records
   - Each should have: name, current_title, current_company, linkedin_url

#### Create Role Specifications

1. **Open Role_Specs table** in Airtable

2. **Create CFO template:**
   - Name: "CFO - Series B SaaS"
   - `structured_spec_markdown` field should contain markdown with:
     - Must-have requirements
     - Evaluation dimensions
     - Role context

3. **Create CTO template:**
   - Name: "CTO - Growth Stage"
   - Similar structure to CFO template

#### Create Portfolio Companies and Roles

1. **Portco table:** Create 4 companies:
   - Pigment
   - Mockingbird
   - Synthesia
   - Estuary

2. **Portco_Roles table:** Create 4 roles:
   - Pigment CFO
   - Mockingbird CFO
   - Synthesia CTO
   - Estuary CTO
   - Link each to the appropriate Portco record

#### Create Searches

1. **Searches table:** Create 4 searches:
   - One for each role (Pigment CFO, Mockingbird CFO, Synthesia CTO, Estuary CTO)
   - Link each Search to the appropriate Role_Spec

---

### Step 2: Create Pre-Run Screens

Run 3 test scenarios before the live demo to validate everything works.

1. **Create Screen 1: Pigment CFO**
   - Link 5-10 candidates from People table
   - Link to Pigment CFO Search
   - Set status to "Pending" (not "Ready to Screen" yet)

2. **Create Screen 2: Mockingbird CFO**
   - Link 5-10 candidates
   - Link to Mockingbird CFO Search
   - Set status to "Pending"

3. **Create Screen 3: Synthesia CTO**
   - Link 5-10 candidates
   - Link to Synthesia CTO Search
   - Set status to "Pending"

---

### Step 3: Run Pre-Run Scenarios

Execute the 3 test screens to validate the workflow.

1. **Start demo infrastructure** (Section 4) if not already running:
   - AgentOS server (Terminal 1)
   - ngrok tunnel (Terminal 2)
   - Control plane connected (optional)

2. **Run Screen 1: Pigment CFO**
   - Go to Screens table in Airtable
   - Find the Pigment CFO screen
   - Change status to "Ready to Screen"
   - **Watch Terminal 1** for execution logs
   - **Monitor control plane** (if connected) for workflow progress
   - **Wait for completion** (typically 5-10 minutes per candidate)

3. **Verify results:**
   - Screen status should be "Complete"
   - Assessment records created in Assessments table
   - Each assessment has:
     - `overall_score` (0-100)
     - `overall_confidence` (High/Medium/Low)
     - `topline_summary` (2-3 sentences)
     - `assessment_json` (full structured output)

4. **Repeat for Screens 2 and 3:**
   - Mockingbird CFO
   - Synthesia CTO

**Expected timing:** 5-10 minutes per candidate, so 25-50 minutes for 5 candidates per screen.

**If any screen fails:** Check Section 7 (Troubleshooting) and fix issues before proceeding.

---

### Step 3.5: Run Pre-Demo Validation (Recommended)

Before the live demo, run the automated pre-demo checklist:

```bash
make pre-demo
```

**What this does:**
- Validates environment configuration
- Verifies dependencies
- Validates Airtable schema alignment
- Runs smoke tests
- Provides manual checklist for infrastructure

**Expected output:**
```
🚀 Pre-Demo Checklist:
  ✅ Environment validated
  ✅ Dependencies verified
  ✅ Airtable schema aligned
  ✅ Smoke tests passed

Manual checklist:
  [ ] Start server: make server (separate terminal)
  [ ] Start tunnel: make tunnel (separate terminal)
  [ ] Verify webhook: curl http://localhost:5001/healthz
  [ ] Test Airtable automation
  [ ] Capture screenshots of workflow stages

✅ Ready for demo!
```

---

### Step 4: Prepare Live Demo Scenario

Set up the scenario you'll run during the live presentation.

1. **Create Screen 4: Estuary CTO**
   - Link 5-10 candidates
   - Link to Estuary CTO Search
   - **Set status to "Pending"** (NOT "Ready to Screen")
   - This is your live demo screen

2. **Document setup:**
   - Write down the Screen record ID (starts with `rec...`)
   - Note how many candidates are linked
   - Document your ngrok URL (in case you need to restart)

3. **Prepare backup plan:**
   - Have the curl command ready (see Quick Reference)
   - Know how to manually trigger if Airtable automation fails
   - Have a second test screen ready as backup

---

### Pre-Demo Checklist

Before the live demo, verify:

- [ ] All 3 pre-run screens completed successfully
- [ ] Assessment quality looks reasonable (scores make sense, summaries are coherent)
- [ ] Execution time is acceptable (<10 minutes per candidate)
- [ ] Live demo screen (Estuary CTO) is ready with status "Pending"
- [ ] Demo infrastructure is running (AgentOS + ngrok)
- [ ] Control plane is connected (optional but recommended)
- [ ] Airtable automation is enabled
- [ ] ngrok URL is documented (in case of restart)
- [ ] Backup plan is ready (curl command, second screen)

**If everything checks out:** ✅ You're ready for the live demo!

---

## Live Demo Execution

This section covers running the demo during your presentation. Follow these steps to execute smoothly.

### Estimated Time: 10-15 minutes (for 5-10 candidates)

---

### Before You Start

1. **Verify infrastructure is running:**
   - AgentOS server (Terminal 1) - shows logs
   - ngrok tunnel (Terminal 2) - shows "online"
   - Control plane connected (optional) - dashboard visible

2. **Have these ready:**
   - Airtable base open in browser
   - Control plane dashboard open (optional)
   - Terminal 1 visible (to show logs)
   - Live demo screen (Estuary CTO) ready with status "Pending"

---

### Step-by-Step Execution

#### Step 1: Introduce the Demo (1-2 minutes)

**What to say:**
- "I'll demonstrate the Talent Signal Agent by screening candidates for a CTO role at Estuary"
- "The system will research each candidate, assess them against the role spec, and produce ranked recommendations"

**What to show:**
- Airtable Screens table
- The Estuary CTO screen with linked candidates
- Role spec content (what we're evaluating against)

---

#### Step 2: Trigger the Screening (30 seconds)

**What to do:**
1. In Airtable, find the Estuary CTO screen
2. Change the `status` field from "Pending" to "Ready to Screen"
3. Click Save

**What happens:**
- Airtable automation triggers
- Webhook sent to AgentOS server
- Workflow begins execution

**What to show:**
- Terminal 1 logs (you should see: `🔍 Received AgentOS screen webhook for recXXXX`)
- Control plane dashboard (if connected) - shows workflow starting

**What to say:**
- "The automation has triggered, and the workflow is starting"
- "You can see the logs in real-time, and the control plane shows the workflow progress"

---

#### Step 3: Monitor Execution (5-10 minutes)

**What happens:**
The workflow runs through 4 steps for each candidate:
1. **Deep Research** - Comprehensive candidate research with web search
2. **Quality Check** - Validates research quality (≥3 citations, non-empty summary)
3. **Incremental Search** (conditional) - Fills gaps if quality check fails
4. **Assessment** - Evaluates candidate against role spec, produces scores

**What to show:**
- **Terminal 1 logs:**
  ```
  🔍 Starting deep research for [Candidate Name]
  ✅ Deep research completed for [Candidate Name] with 4 citations
  🔍 Checking research quality for [Candidate Name]
  ✅ Research quality threshold met for [Candidate Name]
  🔍 Starting assessment for [Candidate Name]
  ✅ Assessment complete for [Candidate Name] (overall_score=85.0)
  ```

- **Control plane dashboard:**
  - Workflow steps progressing
  - Session state showing research results
  - Agent outputs and reasoning

**What to say:**
- "The system is researching each candidate using web search"
- "You can see it's finding citations and building a comprehensive profile"
- "Now it's assessing each candidate against the role requirements"
- "The control plane shows the workflow state as it progresses"

**Timing:** This takes 5-10 minutes per candidate. For a demo, you might want to:
- Show the first candidate fully
- Then skip ahead to show results for all candidates
- Or run with fewer candidates (3-5) for faster demo

---

#### Step 4: Show Results (2-3 minutes)

**What happens:**
- Screen status updates to "Complete"
- Assessment records created in Assessments table
- Each assessment contains scores, confidence, summary, reasoning

**What to show:**
1. **Airtable Assessments table:**
   - Sort by `overall_score` (descending)
   - Show top candidates
   - Click into an assessment to show:
     - `overall_score` (0-100)
     - `overall_confidence` (High/Medium/Low)
     - `topline_summary` (2-3 sentence assessment)
     - `dimension_scores` (breakdown by evaluation dimension)
     - `green_flags` and `red_flags_detected`
     - `counterfactuals` (why candidate might NOT be ideal)

2. **Control plane:**
   - Show completed workflow runs
   - Show session state with research results
   - Show agent reasoning trails

**What to say:**
- "Here are the ranked results - the system has scored each candidate"
- "The top candidate scored 85/100 with High confidence"
- "Let me show you the reasoning - here's why this candidate is a strong fit"
- "Notice the counterfactuals - the system also identifies potential concerns"
- "The research citations are available if you want to verify the information"

---

#### Step 5: Demonstrate Drill-Down (1-2 minutes)

**What to show:**
- Click into a top candidate's assessment
- Show the detailed `assessment_json` field
- Explain the dimension scores
- Show research citations

**What to say:**
- "You can drill into any candidate to see the detailed reasoning"
- "The system provides evidence-backed assessments, not just scores"
- "Each dimension is scored with confidence levels"
- "The research citations let you verify the information"

---

### Handling Questions During Demo

**Common questions and answers:**

**Q: "How long does this take?"**
- A: "About 5-10 minutes per candidate. For a batch of 10 candidates, that's roughly 50-100 minutes total, but it runs automatically."

**Q: "What if the research quality is low?"**
- A: "The system has a quality gate - if research doesn't meet thresholds (≥3 citations, non-empty summary), it triggers an incremental search to fill gaps."

**Q: "Can we customize the evaluation criteria?"**
- A: "Yes - the role spec is stored in Airtable and can be edited. You can also use custom specs per screen for A/B testing different criteria."

**Q: "What happens if a candidate has limited public information?"**
- A: "The system handles unknowns explicitly - dimensions without evidence are marked as 'Unknown' (not scored as 0), and confidence levels reflect this."

**Q: "Can this scale to more candidates?"**
- A: "Yes - the workflow processes candidates sequentially. For production, we'd add parallel processing and caching to improve throughput."

---

### If Something Goes Wrong

**Problem: Workflow doesn't start**
- **Check:** Terminal 1 logs for errors
- **Fix:** Verify AgentOS server is running, ngrok is active, Airtable automation is enabled
- **Backup:** Use curl command (see Quick Reference) to trigger manually

**Problem: Workflow fails mid-execution**
- **Check:** Terminal 1 logs for error messages (look for ❌)
- **Fix:** Check Section 7 (Troubleshooting) for specific error
- **Backup:** Restart the screen with status "Pending" → "Ready to Screen"

**Problem: Results don't appear in Airtable**
- **Check:** Assessments table for new records
- **Fix:** Verify Airtable API key has write permissions
- **Backup:** Check Terminal 1 logs for Airtable write errors

**Problem: ngrok session expired**
- **Fix:** Restart ngrok, get new URL, update Airtable automation URL
- **Prevention:** For longer demos, consider ngrok paid plan or production hosting

---

### Demo Completion

**What to do:**
1. Acknowledge completion: "The screening is complete - we have ranked results"
2. Show summary: "Top 3 candidates scored 85, 82, and 78"
3. Offer next steps: "We can drill into any candidate or adjust the evaluation criteria"

**What to say:**
- "The system has completed the screening and produced ranked recommendations"
- "Each candidate has been researched, assessed, and scored with reasoning"
- "The results are now in Airtable for the talent team to review"

---

## Troubleshooting

This section covers common issues and how to fix them. If you encounter an error, check here first.

---

### AgentOS Server Issues

#### Error: "Missing required environment variables"

**Symptoms:**
```
❌ Missing required environment variables: AIRTABLE_API_KEY
```

**Fix:**
1. Check your `.env` file exists in the project root
2. Verify it contains all required keys:
   ```bash
   cat .env
   ```
3. Make sure variable names match exactly (no typos)
4. Restart the AgentOS server after fixing

**Prevention:** Always verify `.env` file before starting the server.

---

#### Error: "Address already in use"

**Symptoms:**
```
ERROR: Address already in use
```

**Fix:**
1. Find what's using port 5001:
   ```bash
   lsof -ti:5001
   ```
2. Kill the process:
   ```bash
   lsof -ti:5001 | xargs kill -9
   ```
3. Restart AgentOS server

**Prevention:** Always check port availability before starting (see Initial Setup, Step 4).

---

#### Error: Server starts but `/screen` endpoint not found

**Symptoms:**
- Server starts successfully
- But `http://localhost:5001/docs` doesn't show `/screen` endpoint

**Fix:**
1. Check `demo/agentos_app.py` exists and is correct
2. Verify dependencies are installed:
   ```bash
   uv pip list | grep fastapi
   ```
3. Check Terminal 1 logs for import errors
4. Restart server

---

### ngrok Issues

#### Error: "ERR_NGROK_108" or "authentication failed"

**Symptoms:**
```
ERR_NGROK_108: Your account '' is limited to 1 simultaneous ngrok session
```

**Fix:**
1. Verify ngrok auth token is configured:
   ```bash
   ngrok config check
   ```
2. If not configured, add your token:
   ```bash
   ngrok config add-authtoken YOUR_AUTH_TOKEN
   ```
3. Restart ngrok

**Prevention:** Complete ngrok setup in Prerequisites section.

---

#### Error: "Session expired"

**Symptoms:**
- ngrok was working but now shows "Session expired"
- Airtable automation fails with connection errors

**Fix:**
1. Free ngrok sessions expire after 2 hours
2. Restart ngrok:
   ```bash
   ngrok http 5001
   ```
3. Copy the new HTTPS URL
4. Update Airtable automation URL with the new ngrok URL
5. Test the connection

**Prevention:** For longer demos, use ngrok paid plan or production hosting.

---

#### Error: ngrok shows "offline" status

**Symptoms:**
```
Session Status                offline
```

**Fix:**
1. Check AgentOS server is running first (Terminal 1)
2. Restart ngrok
3. Verify internet connection
4. Check ngrok auth token is valid

---

### Airtable Automation Issues

#### Error: Automation doesn't trigger

**Symptoms:**
- Changed Screen status to "Ready to Screen"
- But no webhook sent (no logs in Terminal 1)

**Fix:**
1. Check automation is enabled (toggle ON in Airtable)
2. Verify trigger conditions:
   - Table: Screens (or Platform-Screens)
   - Condition: `status` changes to "Ready to Screen"
3. Check automation runs log:
   - Open automation → "Runs" tab
   - Look for errors or failed requests
4. Test with a different Screen record

---

#### Error: "Webhook failed" in Airtable

**Symptoms:**
- Automation triggers but shows "Webhook failed" in runs log

**Fix:**
1. Verify ngrok URL is correct:
   - Must use HTTPS (not HTTP)
   - Must include `/screen` path: `https://abc123.ngrok.io/screen`
2. Check ngrok is running (Terminal 2 shows "online")
3. Test with curl (see Quick Reference)
4. If curl works but Airtable doesn't, check:
   - The automation action is running the script in `scripts/airtable_webhook_automation.js`
   - `WEBHOOK_URL` inside the script matches your ngrok URL
   - The script still posts the nested `screen_slug` payload (inspect the payload logged to Automation Runs → Details)
   - Headers: `Content-Type: application/json` (plus `Authorization: Bearer ...` if using `AGENTOS_SECURITY_KEY`)

---

### Workflow Execution Issues

#### Error: "Screen missing linked role spec"

**Symptoms:**
```
❌ Screen missing linked role spec
```

**Fix:**
1. In Airtable, open the Screen record
2. Verify it's linked to a Search record
3. Verify the Search is linked to a Role_Spec record
4. Verify the Role_Spec has `structured_spec_markdown` content
5. Re-trigger the screen

---

#### Error: "No candidates linked to screen"

**Symptoms:**
```
❌ No candidates linked to screen
```

**Fix:**
1. In Airtable, open the Screen record
2. Add at least one candidate to the "Candidates" field (linked to People table)
3. Re-trigger the screen

---

#### Error: "Role spec missing structured markdown content"

**Symptoms:**
```
❌ Role spec missing structured markdown content
```

**Fix:**
1. In Airtable, open the Role_Spec record
2. Populate the `structured_spec_markdown` field with markdown content
3. Re-trigger the screen

---

#### Error: Workflow fails mid-execution

**Symptoms:**
- Workflow starts but fails with ❌ error partway through
- Terminal 1 shows error logs

**Fix:**
1. Check Terminal 1 logs for specific error message
2. Common causes:
   - OpenAI API key invalid or billing disabled
   - Airtable API key lacks write permissions
   - Network connectivity issues
3. Verify API keys are correct in `.env` file
4. Check OpenAI account has billing enabled
5. Check Airtable API key has `data.records:write` scope
6. Retry the screen (change status back to "Pending", then "Ready to Screen")

---

### Results Not Appearing in Airtable

#### Problem: Screen completes but no Assessment records

**Symptoms:**
- Terminal 1 shows "✅ Screen completed"
- But Assessments table has no new records

**Fix:**
1. Check Terminal 1 logs for Airtable write errors
2. Verify Airtable API key has write permissions:
   - Go to [airtable.com/account](https://airtable.com/account)
   - Check token has `data.records:write` scope
3. Verify Assessments table exists and is accessible
4. Check Airtable base ID is correct in `.env`
5. Try creating an Assessment record manually to test write access

---

#### Problem: Assessment records created but fields are empty

**Symptoms:**
- Assessment records appear but `overall_score`, `topline_summary` are empty

**Fix:**
1. Check `assessment_json` field - it should contain the full assessment
2. Verify Airtable table schema matches expected fields:
   - `overall_score` (number)
   - `overall_confidence` (single select: High/Medium/Low)
   - `topline_summary` (long text)
   - `assessment_json` (long text)
3. Check Terminal 1 logs for field mapping errors
4. Verify the workflow completed successfully (no errors in logs)

---

### Performance Issues

#### Problem: Workflow takes too long (>10 minutes per candidate)

**Symptoms:**
- Each candidate takes 15+ minutes to process

**Possible causes:**
1. OpenAI API rate limiting
2. Network connectivity issues
3. Deep Research API slow responses

**Fix:**
1. Check Terminal 1 logs for rate limit errors
2. Verify internet connection is stable
3. Consider reducing number of candidates for demo
4. For production, implement caching and parallel processing

---

### General Debugging Tips

1. **Check logs first:** Terminal 1 shows detailed execution logs with emoji indicators
2. **Verify each component:** Use the verification steps in each section
3. **Test incrementally:** Test AgentOS → Test ngrok → Test Airtable → Test full workflow
4. **Use curl for testing:** Test the `/screen` endpoint directly before using Airtable
5. **Check control plane:** If connected, use it to inspect workflow state and errors

---

## Quick Reference

This section provides quick access to common commands, URLs, and information you'll need during the demo.

---

### Command Cheat Sheet

#### Setup & Installation
```bash
make setup          # Complete initial setup (one-time)
make install        # Install/update dependencies only
make verify-deps    # Verify packages are installed
make validate-env   # Validate .env configuration
```

#### Start Demo Infrastructure
```bash
make server         # Start AgentOS server (foreground)
make dev            # Alias for 'make server'
make tunnel         # Start ngrok tunnel (separate terminal)
make dev-all        # Start server in background + instructions
make stop-dev       # Stop background server
```

#### Manual Server Startup (if needed)
```bash
source .venv/bin/activate
uv run python demo/agentos_app.py
```

#### Manual ngrok Startup (if needed)
```bash
ngrok http 5001
```

#### Test Webhook Endpoint (curl)
```bash
curl -X POST http://localhost:5001/screen \
  -H "Content-Type: application/json" \
  -d '{
        "screen_slug": {
          "screen_id": "recTEST",
          "role_spec_slug": {
            "role_spec": {
              "role_spec_id": "recSPEC",
              "role_spec_name": "Demo CFO Spec",
              "role_spec_content": "### Demo Spec..."
            }
          },
          "search_slug": {
            "role": {
              "ATID": "recROLE",
              "portco": "Pigment",
              "role_type": "CFO",
              "role_title": "",
              "role_description": "Demo role description"
            }
          },
          "candidate_slugs": [
            {
              "candidate": {
                "ATID": "recCAND",
                "candidate_name": "Demo Exec",
                "candidate_current_title": "CFO",
                "candidate_current_company": "Acme",
                "candidate_location": "",
                "candidate_linkedin": "",
                "candidate_bio": ""
              }
            }
          ]
        }
      }'
```

#### Check Port 5001 Usage
```bash
lsof -ti:5001
```

#### Kill Process on Port 5001
```bash
lsof -ti:5001 | xargs kill -9
```

#### Validation & Testing
```bash
make validate           # Run all validations (env + deps + airtable)
make validate-airtable  # Validate Airtable schema alignment
make smoke-test         # Quick functionality tests
make pre-demo           # Complete pre-demo validation checklist

make test               # Run full test suite with coverage
make test-fast          # Quick tests without coverage
make test-specific TEST=test_models  # Run specific test
```

#### Documentation
```bash
make docs-serve         # Preview MkDocs docs locally (port 8000)
make docs-build         # Build static docs site
make docs-clean         # Clean docs build artifacts
```

#### Utilities
```bash
make clean              # Remove cache files
make clean-all          # Deep clean (cache + docs + sessions)
make list-routes        # List all FastAPI routes
make help               # Show all available commands
```

#### Manual Commands (if needed)
```bash
# Verify environment variables
.venv/bin/python -c "from demo.settings import settings; print(f'Base: {settings.airtable.base_id}')"

# Run tests manually
uv run pytest tests/
```

---

### Key URLs

- **AgentOS API Docs:** `http://localhost:5001/docs`
- **AgentOS Health Check:** `http://localhost:5001/healthz`
- **AgentOS Config:** `http://localhost:5001/config`
- **Control Plane:** `https://os.agno.com`
- **ngrok Dashboard:** `https://dashboard.ngrok.com`

---

### File Locations

- **Project Root:** `/path/to/FirstMark`
- **Environment File:** `.env` (in project root)
- **AgentOS App:** `demo/agentos_app.py`
- **Session Database:** `tmp/agno_sessions.db`
- **Tests:** `tests/`

---

### Airtable Table Structure

**Core Tables:**
- **People** - Candidate profiles
- **Portco** - Portfolio companies
- **Portco_Roles** - Open roles at portfolio companies
- **Role_Specs** - Role specifications (evaluation criteria)
- **Searches** - Search requests (links Role_Spec to Portco_Role)
- **Screens** - Screening batches (links Candidates to Search)
- **Assessments** - Assessment results (output of screening workflow)

**Key Fields:**
- **Screens.status** - "Pending" → "Ready to Screen" → "Complete"
- **Role_Specs.structured_spec_markdown** - Evaluation criteria
- **Assessments.overall_score** - 0-100 score
- **Assessments.overall_confidence** - High/Medium/Low
- **Assessments.topline_summary** - 2-3 sentence assessment
- **Assessments.assessment_json** - Full structured output

---

### Workflow Steps Reference

1. **Deep Research** - Comprehensive candidate research with web search
2. **Quality Check** - Validates research quality (≥3 citations, non-empty summary)
3. **Incremental Search** (conditional) - Fills gaps if quality check fails
4. **Assessment** - Evaluates candidate against role spec, produces scores

**Log Indicators:**
- 🔍 Step starting
- ✅ Step completed successfully
- ❌ Error occurred
- 🔄 Incremental search triggered

---

### Expected Timing

- **Per candidate:** 5-10 minutes
- **5 candidates:** 25-50 minutes
- **10 candidates:** 50-100 minutes

**Note:** Timing varies based on candidate research complexity and API response times.

---

### Support Resources

- **Full Documentation:** `README.md`
- **Technical Spec:** `spec/spec.md`
- **Product Requirements:** `spec/prd.md`
- **Troubleshooting:** Section 7 of this runbook

---

**End of Demo Runbook**
