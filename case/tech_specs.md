# Tech Specs

## Overview

### Stack

DB: Airtable
UI: Airtable
Actions: Python script
LLM:

- Framework: AGNO
- Model: GPT-5
APIs
- Openai Deep research api
- Openai api
- tavily api
Other
- pyairtable

### Modules

Data Ingestion

- What: receive, clean, map, load
- How: Python

### Webhook Architecture (Flask + ngrok)

**Design Decision:** Flask-based webhook receiver with ngrok tunnel for local demo

**Why This Approach:**

- Single Python codebase (no additional orchestration tools needed)
- All logic in one place (webhook receive + AI workflow + Airtable writes)
- Simple setup (~15 min)
- Full automation for demo (button click OR status change → results)
- Local hosting OK for demo (no cloud deployment needed)
- Real-time visibility (terminal logs during execution)

**How It Works:**

```
Airtable Trigger (Button click OR Status field change)
  → Airtable Automation (webhook trigger)
  → ngrok public URL (tunnel to localhost)
  → Flask server on localhost:5000
  → Python matching workflow (research + assessment)
  → Write results back to Airtable
  → Update status field
```

**Trigger Options:**

- **Button**: Explicit action button in record (e.g., "Start Screening")
- **Status Field**: Automation triggers when field changes (e.g., Status → "Ready to Screen")
- **Recommended**: Status field triggers for more natural workflow and state management

**Components:**

1. `webhook_server.py` - Flask app with multiple endpoints (`/upload`, `/screen`, etc.)
2. ngrok - Exposes localhost to public internet
3. Airtable Automations - Trigger webhooks on button clicks or field changes
4. Python workflow - Core matching logic

**Setup:**

```bash
# Install dependencies
pip install flask pyairtable python-dotenv

# Start Flask server
python webhook_server.py

# Start ngrok (separate terminal)
ngrok http 5000

# Configure Airtable automation with ngrok URL
```

**Demo Flow (Status Field Trigger - Recommended):**

1. Create Screen record, link candidates and search
2. Change Status field to "Ready to Screen"
3. Automation fires → Terminal shows live progress with emoji indicators
4. Status auto-updates: Draft → Processing → Complete
5. Refresh Airtable to see populated Assessment results
6. Show ranked candidates view with reasoning and drill-down

**Alternative Demo Flow (Button Trigger):**

1. Create Screen record, link candidates
2. Click "Start Screening" button
3. Terminal shows progress
4. Results populate in Airtable

## Data Models

### Inputs

#### Structured: Mock_Guilds.csv

  (One row per guild member seat)

- guild_member_id (string) – unique row id.
- guild_name (string) – e.g., CTO Guild, CFO Guild.
- exec_id (string) – stable id used across all tables.
- exec_name (string).
- company_name (string).
- company_domain (string, optional) – acmeco.com.
- role_title (string) – raw title (SVP Engineering, CFO).
- function (enum) – CTO, CFO, CPO, etc.
- seniority_level (enum) – C-Level, VP, Head, Director.
- location (string) – city/region; can normalize to country.
- company_stage (enum, optional) – Seed, A, B, C, Growth.
- sector (enum, optional) – SaaS, Consumer, Fintech, etc.
- is_portfolio_company (bool) – whether it’s FirstMark portfolio.

#### Structured: Exec_Network.csv

  (One row per known executive in the wider network)

- exec_id (string) – primary key; matches Mock_Guilds.csv.
- exec_name (string).
- current_title (string).
- current_company_name (string).
- current_company_domain (string, optional).
- role_type (enum) – normalized function: CTO, CFO, CRO, etc.
- primary_function (enum, optional) – broader grouping: Engineering, Finance, Revenue.
- location (string).
- company_stage (enum, optional) – current company stage.
- sector (enum, optional).
- recent_exit_experience (bool, optional) – IPO/M&A in last X years.
- prior_companies (string, optional) – semi-colon separated list.
- linkedin_url (string).
- relationship_type (enum, optional) – Guild, Portfolio Exec, Partner 1st-degree, Event.
- source_partner (string, optional) – which partner/guild list.

# Demo components

## Candidates

- from scraped guild
  - can add more later
- Execuite Eval for 15

## Portco + Role

- Pigment (B2B SaaS, enterprise, international) - CFO Role
- Mockingbird (Consumer DTC, physical product) - CFO Role
- Synthesia (AI/ML SaaS, global scale) - CTO Role
- Estuary (Data infrastructure, developer tools) - CTO Role
