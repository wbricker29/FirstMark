# Technical Implementation Specification

> Detailed technical design, architecture, data models, and implementation guide for the Talent Signal Agent demo

---

## Resolved Decisions (as of 2025-11-16)

### Technology Stack Confirmed
- **Framework:** AGNO (agent framework)
- **LLM Model:** GPT-5 (available via OpenAI Deep Research API)
  - Reference: `reference/docs_and_examples/openai_reference/deep_research_api/OAI_deepresearchapi.md`
- **Infrastructure:** Flask + ngrok webhook architecture (required for demo)

### Demo Scope Confirmed
**All 4 modules are in scope:**
1. Module 1 (Data Upload) - ✅ In demo
2. Module 2 (New Open Role) - ✅ In demo
3. Module 3 (New Search) - ✅ In demo
4. Module 4 (New Screen) - ✅ In demo (primary workflow)

### Demo Execution Strategy
- **Portco Scenarios:**
  - 3 portcos: Pre-run results ready for demonstration
  - 1 portco: Live execution during demo
  - Total: 4 portco/role combinations (see Demo-Specific Components section)
- **Candidates:** Sourced from `reference/guildmember_scrape.csv`
- **Demo Flow:** Showcase both pre-run results AND live execution

### Role Spec Design
- **Structure & Schema:** Fully defined in `demo_planning/role_spec_design.md`
- **Format:** Markdown-based specs stored in Airtable Long Text field
- **Dimensions:** 6 weighted dimensions per spec (CFO and CTO templates)
- **Storage:** Individual records with template vs customized versions

### Research Execution Strategy
- **Primary Method:** OpenAI Deep Research API
- **Supplemental:** Tavily API for incremental search
- **Rationale:** "Good enough" - balances quality with implementation speed
- **No LinkedIn scraping:** Deep Research API handles web research

### Assessment Approach
- **Two Evaluations Confirmed:**
  1. LLM guided via spec and rubric (structured evaluation)
  2. LLM generating own rubric (exploratory evaluation)
- **Both will be implemented** and presented for comparison

### Candidate Profiles
- **Decision:** OUT OF SCOPE for demo
- **Rationale:** Not mission critical; can extend later if needed
- **Approach:** Run bespoke research per role spec rather than maintaining pre-generated profiles

### Design Principles
- **Recall over Precision:** "Rather not miss a great match vs see some duds"
- **Filter, Don't Decide:** Goal is to focus review, not replace human judgment
- **Augmentation, Not Replacement:** Target is enhancing talent team capabilities
- **Success Metric:** "Evaluators should say 'I'd actually use this ranking'"

---

## Technology Stack

**DB:** Airtable
**UI:** Airtable
**Actions:** Python script
**LLM:**
- Framework: AGNO
- Model: GPT-5

**APIs:**
- OpenAI Deep Research API
- OpenAI API
- Tavily API

**Other:**
- pyairtable

---

## Webhook Architecture (Flask + ngrok)

### Design Decision

Flask-based webhook receiver with ngrok tunnel for local demo

### Why This Approach

- Single Python codebase (no additional orchestration tools needed)
- All logic in one place (webhook receive + AI workflow + Airtable writes)
- Simple setup (~15 min)
- Full automation for demo (button click OR status change → results)
- Local hosting OK for demo (no cloud deployment needed)
- Real-time visibility (terminal logs during execution)

### How It Works

```
Airtable Trigger (Button click OR Status field change)
  → Airtable Automation (webhook trigger)
  → ngrok public URL (tunnel to localhost)
  → Flask server on localhost:5000
  → Python matching workflow (research + assessment)
  → Write results back to Airtable
  → Update status field
```

### Trigger Options

- **Button**: Explicit action button in record (e.g., "Start Screening")
- **Status Field**: Automation triggers when field changes (e.g., Status → "Ready to Screen")
- **Recommended**: Status field triggers for more natural workflow and state management

### Components

1. `webhook_server.py` - Flask app with multiple endpoints (`/upload`, `/screen`, etc.)
2. ngrok - Exposes localhost to public internet
3. Airtable Automations - Trigger webhooks on button clicks or field changes
4. Python workflow - Core matching logic

### Setup

```bash
# Install dependencies
pip install flask pyairtable python-dotenv

# Start Flask server
python webhook_server.py

# Start ngrok (separate terminal)
ngrok http 5000

# Configure Airtable automation with ngrok URL
```

### Demo Flow (Status Field Trigger - Recommended)

1. Create Screen record, link candidates and search
2. Change Status field to "Ready to Screen"
3. Automation fires → Terminal shows live progress with emoji indicators
4. Status auto-updates: Draft → Processing → Complete
5. Refresh Airtable to see populated Assessment results
6. Show ranked candidates view with reasoning and drill-down

### Alternative Demo Flow (Button Trigger)

1. Create Screen record, link candidates
2. Click "Start Screening" button
3. Terminal shows progress
4. Results populate in Airtable

---

## Flask Endpoints

**All Airtable modules use the same Flask + ngrok webhook pattern:**

- `/upload` - Data ingestion (CSV → clean → load)
- `/screen` - Run candidate screening workflow
- `/new-role` - Process new role creation
- `/research` - Trigger deep research on candidate

**Benefits:**
- Consistent architecture across all modules
- Single Python codebase with multiple endpoints
- All modules benefit from same logging/monitoring
- Easy to extend with new modules
- Demo shows scalable pattern

---

## Data Models

### Input Data Schemas

#### Structured: Mock_Guilds.csv

(One row per guild member seat)

- `guild_member_id` (string) – unique row id
- `guild_name` (string) – e.g., CTO Guild, CFO Guild
- `exec_id` (string) – stable id used across all tables
- `exec_name` (string)
- `company_name` (string)
- `company_domain` (string, optional) – acmeco.com
- `role_title` (string) – raw title (SVP Engineering, CFO)
- `function` (enum) – CTO, CFO, CPO, etc.
- `seniority_level` (enum) – C-Level, VP, Head, Director
- `location` (string) – city/region; can normalize to country
- `company_stage` (enum, optional) – Seed, A, B, C, Growth
- `sector` (enum, optional) – SaaS, Consumer, Fintech, etc.
- `is_portfolio_company` (bool) – whether it's FirstMark portfolio

#### Structured: Exec_Network.csv

(One row per known executive in the wider network)

- `exec_id` (string) – primary key; matches Mock_Guilds.csv
- `exec_name` (string)
- `current_title` (string)
- `current_company_name` (string)
- `current_company_domain` (string, optional)
- `role_type` (enum) – normalized function: CTO, CFO, CRO, etc.
- `primary_function` (enum, optional) – broader grouping: Engineering, Finance, Revenue
- `location` (string)
- `company_stage` (enum, optional) – current company stage
- `sector` (enum, optional)
- `recent_exit_experience` (bool, optional) – IPO/M&A in last X years
- `prior_companies` (string, optional) – semi-colon separated list
- `linkedin_url` (string)
- `relationship_type` (enum, optional) – Guild, Portfolio Exec, Partner 1st-degree, Event
- `source_partner` (string, optional) – which partner/guild list

#### Unstructured: Executive bios and Job descriptions

Bios and job descriptions will come via txt files.

### Output Artifacts

**Search - Config & Trail:**
- Logging of Search
  - All agent steps, messages, reasoning
  - OpenAI Deep research full response and parsing
  - Response citation source links
- Storage of All logs and intermediate parts

**Assessment Results:**
- Assessment results Overview
- Individual assessment results
  - Result Scorecard
  - Result Justification
  - Individual component drill down of some type
- Everything needs to have a markdown copy, since some people will not care about UI

---

## Airtable Database Design

### Tables

**People Table:**
- Needs bio field + other normal descriptors

**Company Table:**
- Standard company information

**Portco Table:**
- Portfolio company specific information

**Platform - Hiring - Portco Roles:**
- Where all open roles live

**Platform - Hiring - Search:**
- Roles where we are actively assisting with the search
- Contains Search Custom Info
- Allows for tracking of work and status
- Contains spec info that can then be used for Eval

**Platform - Hiring - Screen:**
- Batch of screens done

**Operations - Audit & Logging:**
- Audit trail for all operations

**Operations - Workflows:**
- Standardized set of fields that contain execution trail and reporting info that can be linked to other items like Screen

**Role Spec Table:**
- Standard role specifications

**Research Table:**
- Holds all granular research sprint info (could fold into role eval temporarily)

**Role Eval Table:**
- Holds all Assessments
- Linked to Operation, Role, People

### Design Notes

**Confirmed Decisions:**
- Demo: Only upload people (no company/role uploads via Module 1)
- Title Table: NOT in demo - using standard dropdowns instead
- Role Spec Structure: See `demo_planning/role_spec_design.md` for full details
  - Markdown-based storage in Long Text field
  - Template + customization workflow
  - 6 dimensions with weights, definitions, scales
- Specs include custom instructions field for additional guidance
- Generalized search rules may include tenure-based scoring adjustments

**See "Outstanding Decisions Needed" section at end of document for remaining questions**

---

## System Components

### Person Components

#### Person Ingestion & Normalization
- **Ideal:** (Centralized Platform)
- **Project:** Python script to ingest, normalize and store

#### Person Enrichment
- **Implementation:** Fake - Stub function that looks up mock Apollo data

#### Person Researcher
**Execution:**
- Current Design: Static Prompt Template + OpenAI Deep research API
- Later: Maybe custom or firecrawl
- Research Run live status updates

**Research Storage:**
- Research Run log Table
- Research Result Storage
  - Need citations to be distinct
  - TBD: Do we scrape citations ourselves and store their content

### Portco Components

**Standardized storage of portco information:**
- Basic Portco Info Define subset
- Review Startup Taxonomy
- Includes stage

**Demo:**
- Cut-through portco table pre-enriched
- Maybe add startup taxonomy
- Maybe do research
- Need to select subset

### Role Spec Components

**Full specification defined in:** `demo_planning/role_spec_design.md`

**Summary:**
- Markdown-based role evaluation frameworks
- Template library (CFO, CTO base templates)
- 6 weighted dimensions per spec:
  - **CFO:** Fundraising (25%), Operational Finance (25%), Strategic Partnership (20%), Leadership (15%), Domain Expertise (10%), Growth Readiness (5%)
  - **CTO:** Technical Leadership (30%), Team Building (25%), Execution (20%), Product Partnership (10%), Scalability (10%), Domain Fit (5%)
- Must-haves, nice-to-haves, red flags
- Customization via duplication and editing
- Python parser module for LLM consumption
- Structured output schema for assessments

### Candidate Components

**OUT OF SCOPE FOR DEMO**

- Standard Candidate profile components
  - Standardized Candidate Profile Definition: Components, definitions, requirements, standards for a spec
    - Goal is to have standard way we describe a candidate generally, and then how we translate and populate for a given spec

### Candidate Matching

**Candidate Assessment Definition:**
- Standardized definitions, framework, process for evaluating a candidate
- The definition encompasses two processes: 1. A general process for human execution, and 2. LLM Agent execution process

**Process entails:**
- Population of candidate info
- Evaluation vs benchmark
- Score + Confidence + Justification

**Output includes:**
- Topline assessment
- Individual component assessment score, confidence (H/M/L), and reasoning
- Counterfactuals
- Ability to investigate somehow
- Research insight or states

---

## Airtable Modules

### Module 1: Data Uploading

**Pattern:** Airtable Button → Webhook → Flask `/upload` endpoint

**Flow (via Airtable Interface UI):**
- Upload file via Airtable attachment field
- Select File type dropdown (person, company)
  - No role uploads for demo
- Click "Process Upload" button
  - Can either be webflow trigger button if UI allows, or can be an action that changes a field value to trigger webhook
- **Webhook triggers Flask `/upload` endpoint**
  - Python: Download file from Airtable
  - Python: Clean, normalize, dedupe
  - Python: Load into proper table
  - Python: Update status field with results

**Demo:**
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

### Module 2: New Open Role

**Defs and Notes:**
- Open roles exist for many portcos. Not all of them we will be actively assisting with
- Portcos can provide us open roles that we provide in careers portal externally
- Note: Can have portcos submit + Aging mechanism

**Flow (via Airtable Interface UI):**
- Select Portco
- Select Role type
- Optional notes for candidate parameters
- Optional add spec
  - Select Existing
    - Ability to add bespoke requirements
  - Create Own
  - Maybe create new version of existing

**Demo:**
- Create new Role live

### Module 3: New Search

**Defs and Notes:**
- Search is a role we are actively assisting with. Will have role spec
- Have as distinct item so we can attach other items to it (like notes)

**Flow (via Airtable Interface UI):**
- Link Role
- Link spec?
- Add notes
- Add timeline date

**Demo:**
- Create new search live

### Module 4: New Screen

**Pattern:** Airtable Button → Webhook → Flask `/screen` endpoint

**Definition:**
- Perform screening on a set of people for a search
- Main demo workflow for talent matching

**Requirements:**
- Process one or more candidates at a time
- Bulk selection via linked records
- Multiple screens per search allowed
- Can redo evals with new guidance

**Flow (via Airtable Interface UI):**
- Create new Screen record in Airtable
- Link to Search (which links to Role + Spec)
- Add custom guidance/specifications (optional)
- Link one or more candidates from People table
  - Use Airtable multi-select
- Click "Start Screening" button
  - Can either be webflow trigger button if UI allows, or can be an action that changes a field value to trigger webhook
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

**Demo:**
- Demo UI and kick off flow
- Use pre-run example for discussion and can check in periodically to see the live run is progressing

---

## Technical Implementation Notes

- Must have confidence alongside any evaluation score
- Rubrics are dimensions, weights, definition, and scale
- Need quotation level detail somewhere
- Counterfactuals
- All ins and outs will use structured outputs
- Will use GPT-5 (A NEW MODEL)
- Demo db schemas will be MVP, not beautiful thing
- Will do two evaluations
  - LLM guided via spec and rubric
  - LLM generating own rubric
- Data schema
  - People will always have LinkedIn associated with them

### Airtable Requirements

- DB & UI features quickly
- Meet them in their stack
- Requirements
  - Ability to kickoff workflow from Airtable
  - Ability to use Python for Data ops and Agent work

---

## Demo-Specific Components

### Candidates
- **Source:** `reference/guildmember_scrape.csv` (64 executives from FirstMark guilds)
- **Roles:** Mix of CFOs, CTOs, CPOs, CROs across various companies
- **Demo Scope:** Execute evaluations for 10-15 candidates
- **Enrichment:** Basic profiles + LinkedIn URLs (mock research data for demo)

### Portco + Role Scenarios

**4 total scenarios:**

1. **Pigment - CFO Role** (B2B SaaS, enterprise, international)
   - Status: Pre-run ✅

2. **Mockingbird - CFO Role** (Consumer DTC, physical product)
   - Status: Pre-run ✅

3. **Synthesia - CTO Role** (AI/ML SaaS, global scale)
   - Status: Pre-run ✅

4. **Estuary - CTO Role** (Data infrastructure, developer tools)
   - Status: **LIVE EXECUTION** during demo 🔴

**Demo Strategy:**
- Show pre-run results for 3 scenarios (full data, insights, rankings ready)
- Kick off live screening for 1 scenario to demonstrate real-time workflow
- Toggle between completed results and in-progress execution
- Highlight different assessment patterns across CFO vs CTO roles

---

## Outstanding Decisions Needed

### Critical Implementation Details

#### 1. Assessment Scoring Mechanics
- **Confidence Calculation:** How is confidence (High/Medium/Low) determined?
  - Based on amount of evidence found?
  - Based on directness of evidence match?
  - LLM self-assessment of certainty?
  - Combination approach?
  - **Recommendation:** Use LLM self-assessment + evidence quantity (simple heuristic)

- **Counterfactuals Definition:** What does "counterfactuals" mean in this context?
  - "What if" scenarios? (e.g., "If candidate had X experience, score would be Y")
  - Alternative interpretations of ambiguous evidence?
  - Reasons candidate might NOT be a good fit despite high score?
  - **Recommendation needed** for operational definition

- **Two Evaluation Comparison:** How do we present both evaluation results?
  - Side-by-side comparison in UI?
  - Separate sections in markdown report?
  - Highlight where they agree vs disagree?
  - Use spec-based as primary, AI-generated as validation?

#### 2. Airtable Schema Details
Need complete field definitions for these tables:

**People Table:**
- Standard fields: name, current_title, current_company, location, linkedin_url
- Bio field: Long Text? Rich Text?
- Which fields from guildmember_scrape.csv map to People table?

**Platform - Hiring - Screen:**
- Fields: screen_id, search_link, candidates_links, status, created_date
- Status enum values: Draft, Ready to Screen, Processing, Complete, Failed?
- Custom instructions field?

**Operations - Workflows:**
- Fields needed for audit trail?
- Research results storage structure?
- Assessment results storage structure?
- Execution logs format?

**Role Eval Table:**
- How are dimension scores stored? Individual fields vs JSON?
- Evidence quotes storage?
- Citation links storage?

**Research Table:**
- Full research text field?
- Citation structure: URLs only or full content snapshots?
- OpenAI Deep Research API response format?

#### 3. Data Ingestion & Processing

**File Upload Deduplication:**
- Do we implement dedupe logic for demo? (checking exec_id or name+company?)
- **Recommendation:** Skip for demo - assume clean uploads only
- Simplifies implementation; can note as future enhancement

**OpenAI Deep Research API Integration:**
- Expected response format and structure?
- How are citations returned in the API response?
- Rate limits and cost implications?
- **Need to review:** `reference/docs_and_examples/openai_reference/deep_research_api/OAI_deepresearchapi.md`

**Citation Storage:**
- Store URLs only (from Deep Research API response)?
- Or also store citation snippets/quotes provided by API?
- **Recommendation:** URLs + key quotes provided in API response (no additional scraping)

#### 4. Technical Robustness

**Error Handling:**
- Rate limiting strategy for OpenAI API calls?
- Retry logic for failed research/assessment calls?
- Fallback behavior if API fails during demo?

**Execution Time:**
- Expected runtime for single candidate evaluation?
  - Research phase: ~X minutes
  - Assessment phase: ~X minutes
- Expected runtime for full screen of 10 candidates?
- Implications for demo (can we run live or pre-run only)?

**Structured Outputs:**
- All API calls use structured outputs (confirmed)
- Schema validation: strict or permissive?
- Handling of schema mismatches?

#### 5. Demo Logistics

**Airtable Setup Scope:**
- Which Interface views are needed for demo?
- Are automations essential or can we trigger webhooks manually?
- Pre-populated test data requirements?

**Webhook Testing:**
- Can we test webhook locally before demo?
- Ngrok stability concerns for live demo?
- Backup plan if webhook fails?

**Output Artifacts:**
- Markdown export of all assessment results (confirmed requirement)
- Where are markdown files stored? (Airtable attachment? Local folder?)
- Format template for markdown reports?

#### 6. MVP Simplifications (Given 48-Hour Constraint)

**Resolved Simplifications:**
- Person enrichment: **Stub function** (no real Apollo API) ✅
- Research: **Real OpenAI Deep Research API** (not mock data) ✅
- Candidate profiles: **Skip entirely** ✅
- Deduplication: **Skip** (assume clean data) ✅

**Still Need to Decide:**
- Module 1 (Upload): Build full CSV processing webhook or pre-populate data manually?
- Module 2 (New Role): Build UI flow or create records manually in Airtable?
- Module 3 (New Search): Build UI flow or create records manually in Airtable?
- Airtable Interface: Custom interfaces or standard grid views?
- **Recommendation:** Pre-populate data for Modules 1-3; focus dev time on Module 4 (screening)

### Prioritization Recommendation

**Must Have Before Build (4 critical items):**
1. ✅ ~~Research execution strategy~~ → **RESOLVED:** OpenAI Deep Research API + Tavily
2. **Confidence calculation methodology** → Define H/M/L logic
3. **Counterfactuals operational definition** → What does this mean in practice?
4. **Airtable schema details** → Complete field definitions for core tables
5. **Expected execution times** → Critical for demo planning (live vs pre-run)

**Can Decide During Build:**
1. ✅ ~~Deduplication approach~~ → **RESOLVED:** Skip for demo
2. Citation storage details (review Deep Research API docs for format)
3. Error handling specifics (retry logic, fallbacks)
4. Two evaluation comparison presentation (can iterate based on results)
5. Markdown export format (can use simple template)

**Recommended Simplifications for Demo:**
1. **Modules 1-3:** Pre-populate data manually (no webhook automation needed)
2. **Module 4:** Build full webhook + automation (this is the core demo)
3. **Airtable UI:** Standard grid views + basic filtering (no custom interfaces)
4. **3 portcos pre-run, 1 live** → Manage execution time risk

---

## Next Steps

### Immediate Decisions Needed (Before Build)
1. **Define confidence calculation logic** (30 min)
   - Propose simple heuristic: LLM self-assessment + evidence count threshold
   - Document in assessment schema

2. **Define counterfactuals** (30 min)
   - Operational definition for demo
   - Recommendation: "Key reasons candidate might NOT be ideal fit despite high score"

3. **Review OpenAI Deep Research API docs** (1 hour)
   - Understand response format, citation structure, rate limits
   - File: `reference/docs_and_examples/openai_reference/deep_research_api/OAI_deepresearchapi.md`
   - Determine expected execution time per candidate

4. **Create detailed Airtable schema** (2 hours)
   - Complete field definitions for: People, Screen, Workflows, Role Eval tables
   - Create new document: `demo_planning/airtable_schema.md`

### Implementation Sequence
1. **Phase 1:** Airtable setup + manual data population (4 hours)
2. **Phase 2:** Core assessment logic + prompts (6 hours)
3. **Phase 3:** Flask webhook + Module 4 integration (4 hours)
4. **Phase 4:** Pre-run 3 scenarios + generate results (4 hours)
5. **Phase 5:** Testing + demo rehearsal (2 hours)

**Total Estimated: 20 hours** (leaves buffer within 48-hour window)
