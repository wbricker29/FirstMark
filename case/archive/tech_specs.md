# Tech Specs
> document for planning demo build

## Tech Planning & Notes

### Key Decisions

#### Open

- What is research method
  - Options
    - Out of the box API
      - Open AI Deepresearch API
      - Other deep research API
      - Hugging Face Model
    - Open Source Approach/Framwork
      - Open Deep research
      - Caml
      - owl
    - Custom Agentic
  - **Decision**
    - OpenAI Deep research API + ability to do incremental search via Tavily
    - REason: Good enough

- Where and how do we provide granularity
  - Do we need granularity in seeing all sources (aka scraping all source content)
  - Are we ok with synthesized report and sources or need to see how put tgoether (aka full internal agent)
  - Do we want AI to generate its own non-deterministic grade and pair it with a deterministic hybrid?
    - AKA have 2 asessments - via provided rubric; via own rubric and high lvel orientation, then mathc

- Ingestion method
  - Use LLM or code or both for ingestion?
  - **Decision:**
    - Basic CSV Ingest Via Python.
    - Reason: Wouldnt be part of this in reality, and pretty basic

- How to decompose key LLM responsibilities (and whcih are llm)
  - Options
    - research
    - enrichment
    - assessment
    - reporting
  - **DECISION**
    - Enrichment is going to be fake ( because will be Apollo anyway)
      - Not doing real apollo because havent used it
      - Other options could ahve used
    - Research
      - API Tool
      - Subagent for search and extract
    - distinct Agent for assessment and reportomg

- UI or not?
  - Options
    - if use deep agents , they have ui
    - streamlit
    - Jupyter notebook?
  - DECISION: AIRTABLE

- IF agent, what framework?
  - Options
    - Agno
    - lang chain
    - openai sdk
  - DECISION: Agno

- Demo DB platform
  - Local sqlite or supabase
  - Airtable
  - DECISION: AIRTABLE

- Enrichment
  - Optoins
    - Bright data
    - firecrawl
    - Apollo
  - Decision
    - For now, nothing - Enrichment tool will be stub
      - Will mock api response data from Apollo
    - backup:Can use crawl4ai if needed

- Mock Data
  - Mock People
    - Real people for canadiates?
    - If real, are they portco members? people in the room?
    - **DECISION**: REAL PEOPLE, Part from scrape, others we can search
  - Mock Companies
    - Real companies?
      - I think yes, some portcos
      - **DECISION**: Yes, subset of portcos
  - Mock Roles
    - 4 roles, 2 cto + 2 cfo
      - real portcos
      - series a - d
      - easy portcos to characterize and find cto and cfo for
      - Decision: done

  - Data Edge cases
    - Non-normalized names, field names
    - bios just one text file

- Do we skip creating profile and jsut have bespoke research anchored on spec for now?
  - I think yes and can say "probably takes some more refinement on what a profile is, if we keep standardized profiles or auto-gen when create new person (of x y z type)
  - Decision: Yes, skip

### Open Questions

#### Case + Demo spcific

What is the right level of granularity to express the ideal state of the DB?

- Ideally rationalized schema

- but not going to come in and try to rationalize full world and transform all the data once

#### Other

- How do they currently serve materials to the portcos

### Artifacts

#### Inputs

| Type                  | Example                                                      | Description                                                  |
| --------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| **Structured data**   | "Mock_Guilds.csv" of mock data of two FirstMark Guilds       | Columns: company, role title, location, seniority, function. |
| **Structured data**   | "Exec_Network.csv", could be an example of a Partner's connections to fill out additional potential candidates | Columns: name, current title, company, role type (CTO, CRO, etc.), location, LinkedIn URL. |
| **Unstructured data** | Executive bios or press snippets                             | ~10–20 bios (mock or real) in text format.                   |
| **Unstructured data** | Job descriptions                                             | Text of 3–5 open portfolio roles for CFO and CTO.            |

bios and job descriptions will come via txt files.

#### Output

Search - Config & Trail

- Logging of Search
  - All agent steps, messages, reasoning
  - OpenAI Depp research full response and parsing
  - response citation source links
  -
- Storage of All logs and intermediate parts

- Assessment results Overview
- Individual assessment results
  - Result Scorecard
  - Result Justification
  - Indovodial component drill down of some type
- everything needs to have a markdown copy, since some people will not care about ui

#### Key Artifacts to generate

- Data Ingestion and Normalization Mechanism
- Enrichment
- Frameworks
  - Role
  - Candidate
  - Assessment
- Presentation

### Components

 **Person Components**

- Person Ingestion & Normalization
  - Ideal: (Centralized Platform)
  - Project: Python script to ingest, normalize and store
- Person Enrichment
  - Fake - Stub function that looks up mock apollo data
- Person Researcher
  - Execution
    - Current Design: Static Prompt Tempalte +  OpenAI Deep research API
    - Later: Maybe custom or firecrawl
    - Research Run live status updates
  - Research Storage
    - Research Run log Table
    - Research Result Storage
      - NEed citations to be distinct
      - TBD: Do we scrape citations ourselves and store their content

**Portco Components**

- Standardized storage of portco information, including characteristics
  - Basic Portco Info Define subset
  - Review Startup Taxonomy
  - Includes stage
- demo
  - Cuthrough portco table pre-enriched
  - Maybe add startup taxonomy
  - maybe do research
  - need to select sunbset

**Role Spec Components**

- Standard Role Spec Components
  - Standardized Role Spec Framework Definition: Components, definitions, requirements, standards for a spec
    - Values, Abilities, Skills, Experience
    - Some idea of grade scale
  - Base Role Specs: a standard spec for a given role
    - Potential Designs
      - Spec for title
      - Spec for title and company type
- Spec Customization and Clean generation
  - Ability to generate new spec from scratch  via standard ai conversational workflow
  - ability to edit exisitng spec via instructions and LLM refactoring of spec
  - Ability to manually customize (Add dimension, change dimension, change scale)

**Candidate Components**
OUT OF SCOPE FOR DEMO

- Standard Candidate profile components
  - Standardized Candidate Profile Definition: Components, definitions, requirements, standards for a spec
    - Goal is to have standard way we describe a candidate generally, and then how we translate and populate for a given spec

**Candaidate Matching**

- Candidate Assessment Definition - standardized definitions, framework , process for evaluating a candidate
  - The definition encompasses two processes: 1. A general process for human execution, and 2. LLM Agent execution process
  - Process entails
  - Population of candidate info
  - evaluation vs benchmark
  - Score + Confidence + Justification
  - Output includes
    - topline assessment
    - individual component assessment score, confidence (H/M/L), and reasoning
    - counter factuals
    - Ability to investigate somehow
    - Research insight or sttes
- requirements
  - provide

### Airtable Design

#### Architecture Pattern

**All Airtable modules use the same Flask + ngrok webhook pattern:**

```
Airtable UI Action (button/automation)
  → Webhook trigger
  → Flask endpoint (/upload, /screen, /new-role, etc.)
  → Python processing logic
  → Write results back to Airtable
  → Update status/completion
```

**Benefits:**
- Consistent architecture across all modules
- Single Python codebase with multiple endpoints
- All modules benefit from same logging/monitoring
- Easy to extend with new modules
- Demo shows scalable pattern

**Flask Endpoints:**
- `/upload` - Data ingestion (CSV → clean → load)
- `/screen` - Run candidate screening workflow
- `/new-role` - Process new role creation
- `/research` - Trigger deep research on candidate

#### Notes

- Q - For file upload, Do we do dedupe for demo?
- Q - Do we have title Table in demo
  - I think not for now, just standard dropdowns

- Demo - Only upload people

- Q - What is a role spec?
  - Is it role or role+company type specific?
  - Is it dynamically generated based on job description?
  - What are its dimensions
    - Skill specific
    - Generalized ( Skill, Experience, )
- Q - Do we allow for custom Specs?
  - Note: Dependent on what role spec definition is
  - How do we have (in UI) Select existing spec, duplicate, and chabnge
  - Could Have Spec Hub that either
    - Is selected and copied into Open role spec fields (allow customization)
      - Downside, Mixing of concerns, a bit messy
    - Is selected and and has customize option that duplicates and links it
      - Unclear how would use airtable automations and ui to do that

- Q - How do we store a spec
  - Do we have spec as individual record with standardized fields with sets of attribute, defininition, Scale, Weight (EG Attribute 1, def 1 , scale 1, weigh 1, attribute 2, def 2...)
  - Do we have it as a Text field that is rich text and is copied over w/ ability to edit
    - and ability to draft
- Specs always have wildcard spot for custom description

- Will need generalized search rules
  - Reduce score depending on tenure of current role

- Q - Is research also linkedin scrape?

#### Tables

People Table

- needs bio field + other normal descriptors
Company Table
Portco Table
Platform - Hiring - Portco Roles (Where all open roles live)
Platform - Hiring - Search (Roles where we are actively assisting with the search)
- Contains Search Custom Info
- Allows for tracking of work and stastus
- Contains spec info that can then be used for Eval
Platform - Hiring - Screen (Batch of screens done)
Operations - Audit & Logging
Operations - Workflows (Stabdardized set of fields that contain execution trail and reporting info that can be linked to other items like Screen)

Role Spec Table
Research Table - Holds all granular research sprint info (could fold into role eval temporarily)
Role Eval Table - Holds all Assessments

- Linked to Operation, Role, People
- linked to

#### Modules

##### Data Uploading

**Pattern:** Airtable Button → Webhook → Flask `/upload` endpoint

**Flow (via Airtable Interface UI):**
- Upload file via Airtable attachment field
- Select File type dropdown (person, company)
  - No role uploads for demo
- Click "Process Upload" button
  - can either be webflow trigger button if ui allows, or can be an action that changes a field value to trigger webhook
- **Webhook triggers Flask `/upload` endpoint**
  - Python: Download file from Airtable
  - Python: Clean, normalize, dedupe
  - Python: Load into proper table
  - Python: Update status field with results

**Demo**
- Add new people CSV
  - Could add bios in text field too

**Implementation:**
```python
@app.route('/upload', methods=['POST'])
def process_upload():
    # Get file from Airtable
    # Clean and normalize
    # Load to appropriate table
    # Return status
```

##### New Open role

**Defs and Notes**

- Open roles exist for many portcos. not all of them we will be actively assisting with
- Portcos can provide us open roles that we provide in careers portal extnernally
- note: - can have portcos submit + Aging mechanism

**Flow (via Airtable Interface UI)**

- Select Portco
- Select Role type
- Optional notes for candidate parameters
- Optional add spec
  - Select Existing
    - Ability to add bespoke requirmentsL
  - Create Own
  - Maybe create new version of existing
**Demo**
- Create new Role live
##### New Search

**Defs and Notes**
- Search is an role we are actively assisting with. Will have role spec
- have as distinct item so we can attach other items to it ( like notes)

**Flow (via Airtable Interface UI)**
- Link Role
- link spec ?
- Add notes
- Add timeline date

**Demo**
- Create new search live

##### New Screen

**Pattern:** Airtable Button → Webhook → Flask `/screen` endpoint

**Definition:**
- Perform screening on a set of people for a search
- Main demo workflow for talent matching

**Requirements:**
- Process one or more candidates at a time
- Bulk selection via linked records
- Multiple screens per search allowed
- Can redo evals with new guidance

**Flow (via Airtable Interface UI)**
- Create new Screen record in Airtable
- Link to Search (which links to Role + Spec)
- Add custom guidance/specifications (optional)
- Link one or more candidates from People table
  - Use Airtable multi-select
- Click "Start Screening" button
  - can either be webflow trigger button if ui allows, or can be an action that changes a field value to trigger webhook
- **Webhook triggers Flask `/screen` endpoint**
  - For each linked candidate:
    - Create Workflow record (audit trail)
    - Run Deep Research via OpenAI API
    - Store research results in Workflow record
    - Run Assessment against role spec
    - Store assessment in Workflow record
      - Overall score + confidence
      - Dimension-level scores
      - Reasoning + counterfactuals
    - Update candidate status
    - Mark Workflow as complete
  - Update Screen status to "Complete"
  - Terminal shows real-time progress

**Implementation:**
```python
@app.route('/screen', methods=['POST'])
def run_screening():
    screen_id = request.json['screen_id']

    # Get screen details + linked candidates
    # For each candidate:
    #   - Create workflow record
    #   - run_deep_research()
    #   - run_assessment()
    #   - write results to Airtable
    # Update screen status

    return {'status': 'success', 'candidates_processed': n}
```
**Demo**
- demo ui and kick off flow
- use pre-run example for discussion and can check in periodically to see the live run is porgressing



### Tech Notes

- must have confidence alongside any evaluation score
- Rubrics are dimensions, weights, definition, and scale
- Need quotation level detail somehwere
- Counterfactuals
- All ins and outs will use structured outputs
- Will use gpt 5 ( A NEW MODEL)
- Demo db schemas will be MVP, not beautiful thing
- will do two evaluations
  - llm guided via spec and rubric
  - llm generating own rubric
- Data schema
  - People will always have linked in associated with them

Airtable
- DB & UI features quickly
- Meet them in their stack
- Requirements
  - Ability to kickoff workflow from airtable
  - Ability to use Python for Data ops and Agent work

---

## Demo Design Spec

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
