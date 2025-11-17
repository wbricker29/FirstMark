# Tech Specs v2

> Technical design specifications for FirstMark Talent Signal Agent demo
> **Note:** For case strategy and presentation planning see wbcasenotes_v2.md

Version: 0.2
Last Updated: 2025-11-16

---

## Table of Contents

1. [Stack & Framework Decisions](#stack--framework-decisions)
2. [Architecture Overview](#architecture-overview)
3. [Data Models](#data-models)
4. [Core Components](#core-components)
5. [Airtable Design](#airtable-design)
6. [Role Spec Framework](#role-spec-framework)
7. [Assessment Framework](#assessment-framework)
8. [Implementation Details](#implementation-details)
9. [API References](#api-references)

---

## Stack & Framework Decisions

### Core Stack

**Database & UI:**

- **Airtable** - Primary data storage and user interface
  - Rationale: Meet FirstMark in their existing stack, rapid development
  - Trade-off: Less flexibility vs. faster adoption

**Backend:**

- **Python 3.11+** - Primary language for all logic
- **Flask** - Lightweight webhook server
- **ngrok** - Tunnel for local demo (production would use cloud hosting)

**LLM & AI:**

- **Framework:** Agno (<https://docs.agno.com>)
  - Rationale: Modern agent framework, good observability, structured outputs
  - Alternative considered: LangGraph (more complex), OpenAI SDK (less structure)
- **Primary Model:** GPT-5 (gpt-5-1)
  - For: Candidate assessment, synthesis, structured reasoning
  - Rationale: Latest model, best reasoning capabilities
- **Research API:** OpenAI Deep Research API
  - For: Candidate background research and citation gathering
  - Rationale: Production-ready, high-quality results
- **Search API:** Tavily (backup/supplemental)
  - For: Incremental search if needed
  - Rationale: Fast, reliable web search

**APIs & Integrations:**

- **pyairtable** - Airtable Python SDK
- **openai** - OpenAI Python SDK
- **tavily-python** - Tavily search SDK (optional)

**Development Tools:**

- **python-dotenv** - Environment variable management
- **pydantic** - Data validation and structured outputs
- **requests** - HTTP client for webhooks

### Key Technical Decisions

| Decision | Options Considered | Final Choice | Rationale |
|----------|-------------------|--------------|-----------|
| **Research Method** | OpenAI API, Custom Agent, HuggingFace Model | OpenAI Deep Research API | Production-ready, high quality, fast |
| **Agent Framework** | Agno, LangChain, OpenAI SDK | Agno | Balance of simplicity and structure |
| **Database** | SQLite, Postgres, Supabase, Airtable | Airtable | Meet them in their stack |
| **Enrichment** | Apollo, Bright Data, Firecrawl | Stub (mock Apollo) | Not core to demo, would use Apollo in production |
| **UI** | Streamlit, Custom React, Jupyter, Airtable | Airtable Interface | Zero additional build time |
| **Deployment** | Cloud (Render/Railway), Local (ngrok) | Local + ngrok | Sufficient for demo, easy debugging |

### Dependencies

```bash
# requirements.txt
flask==3.0.0
pyairtable==2.3.0
openai==1.12.0
tavily-python==0.3.0  # optional
python-dotenv==1.0.0
pydantic==2.5.0
requests==2.31.0
agno==0.1.0  # check latest version
```

---

## Architecture Overview

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        AIRTABLE UI                          │
│  (Data Entry, Triggering, Results Viewing)                  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   AIRTABLE AUTOMATIONS                       │
│  (Webhook Triggers on Button/Status Change)                  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼ (HTTPS Webhook)
┌─────────────────────────────────────────────────────────────┐
│                      NGROK TUNNEL                            │
│  (Public URL → localhost:5000)                               │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                     FLASK WEBHOOK SERVER                     │
│                    (webhook_server.py)                       │
│                                                              │
│  Routes:                                                     │
│  • POST /upload   - Data ingestion                          │
│  • POST /screen   - Run candidate screening (MAIN)          │
│  • POST /research - Individual candidate research           │
│  • POST /health   - Health check                            │
└─────────────────────────────────────────────────────────────┘
                            │
            ┌───────────────┼───────────────┐
            ▼               ▼               ▼
┌─────────────────┐ ┌─────────────┐ ┌─────────────┐
│  DATA INGESTION │ │  RESEARCH   │ │ ASSESSMENT  │
│     MODULE      │ │   MODULE    │ │   MODULE    │
└─────────────────┘ └─────────────┘ └─────────────┘
            │               │               │
            │               ▼               ▼
            │     ┌──────────────┐ ┌──────────────┐
            │     │ OpenAI Deep  │ │  GPT-5 with  │
            │     │ Research API │ │  Agno Agent  │
            │     └──────────────┘ └──────────────┘
            │               │               │
            └───────────────┴───────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    AIRTABLE STORAGE                          │
│  (Write Results, Update Status, Store Logs)                  │
└─────────────────────────────────────────────────────────────┘
```

### Webhook Flow (Primary Demo Path)

```
1. User creates Screen record in Airtable
2. User links Search (→ Role → Role Spec)
3. User links Candidates (multi-select from People table)
4. User clicks "Start Screening" button
   │
   ├─→ Airtable Automation triggers
   │
   ├─→ Webhook fires to ngrok URL
   │   POST https://abc123.ngrok.io/screen
   │   Body: { screen_id: "recXXX", trigger_time: "..." }
   │
   ├─→ Flask receives request at /screen endpoint
   │
   ├─→ Fetch Screen record + linked data from Airtable
   │   - Get Search record
   │   - Get Role record
   │   - Get Role Spec
   │   - Get linked Candidates (list)
   │
   ├─→ FOR EACH Candidate:
   │   │
   │   ├─→ Create Workflow record (audit trail)
   │   │   - Status: "Running"
   │   │   - Start time
   │   │
   │   ├─→ Run Deep Research
   │   │   - Call OpenAI Deep Research API
   │   │   - Prompt: "Research {name} for {role} role..."
   │   │   - Store: Citations, summary, raw response
   │   │
   │   ├─→ Update Workflow: Research complete
   │   │
   │   ├─→ Run Assessment
   │   │   - Load Role Spec dimensions
   │   │   - Call GPT-5 via Agno
   │   │   - Structured output: Scores, confidence, reasoning
   │   │
   │   ├─→ Update Workflow: Assessment complete
   │   │   - Store: Overall score, dimension scores, reasoning
   │   │   - Status: "Complete"
   │   │
   │   └─→ Update Candidate record: Link to Workflow
   │
   ├─→ Update Screen record
   │   - Status: "Complete"
   │   - Completion time
   │   - Summary stats
   │
   └─→ Return success response to Airtable
```

---

## Data Models

### Input Data Schemas

#### Structured: Mock_Guilds.csv

Purpose: FirstMark Guild member data (CTO Guild, CFO Guild, etc.)

```csv
guild_member_id,guild_name,exec_id,exec_name,company_name,company_domain,role_title,function,seniority_level,location,company_stage,sector,is_portfolio_company
gm_001,CFO Guild,exec_001,Sarah Chen,Airtable,airtable.com,Chief Financial Officer,CFO,C-Level,San Francisco,Growth,B2B SaaS,false
gm_002,CTO Guild,exec_002,Michael Torres,Stripe,stripe.com,CTO,CTO,C-Level,San Francisco,Public,Fintech,false
```

**Fields:**

- `guild_member_id` (string) - Unique row ID
- `guild_name` (string) - e.g., "CTO Guild", "CFO Guild"
- `exec_id` (string) - Stable ID used across all tables
- `exec_name` (string) - Full name
- `company_name` (string) - Current company
- `company_domain` (string, optional) - e.g., "airtable.com"
- `role_title` (string) - Raw title (e.g., "SVP Engineering", "CFO")
- `function` (enum) - Normalized: CTO, CFO, CPO, CRO, CMO, COO
- `seniority_level` (enum) - C-Level, VP, Head, Director, Senior
- `location` (string) - City/region (can normalize to country)
- `company_stage` (enum, optional) - Seed, A, B, C, D, Growth, Public
- `sector` (enum, optional) - B2B SaaS, Consumer, Fintech, Healthcare, etc.
- `is_portfolio_company` (bool) - Whether FirstMark portfolio company

#### Structured: Exec_Network.csv

Purpose: Broader network of executives from partner connections

```csv
exec_id,exec_name,current_title,current_company_name,current_company_domain,role_type,primary_function,location,company_stage,sector,recent_exit_experience,prior_companies,linkedin_url,relationship_type,source_partner
exec_015,Jennifer Wu,CFO,Notion,notion.com,CFO,Finance,San Francisco,Growth,B2B SaaS,false,Dropbox; Google,https://linkedin.com/in/jenniferwu,Partner 1st-degree,Matt Turck
```

**Fields:**

- `exec_id` (string) - Primary key (matches Mock_Guilds.csv)
- `exec_name` (string)
- `current_title` (string) - Raw title
- `current_company_name` (string)
- `current_company_domain` (string, optional)
- `role_type` (enum) - Normalized function: CTO, CFO, CRO, etc.
- `primary_function` (enum, optional) - Broader: Engineering, Finance, Revenue, Product
- `location` (string)
- `company_stage` (enum, optional)
- `sector` (enum, optional)
- `recent_exit_experience` (bool, optional) - IPO/M&A in last 3 years
- `prior_companies` (string, optional) - Semicolon-separated list
- `linkedin_url` (string) - Profile URL
- `relationship_type` (enum, optional) - Guild, Portfolio Exec, Partner 1st-degree, Event, Other
- `source_partner` (string, optional) - Which partner/guild introduced them

#### Unstructured: Executive Bios

Purpose: Additional context for candidates (optional enrichment)

**Format:** Text files, one per executive (optional)

```
Name: Sarah Chen
Title: Chief Financial Officer at Airtable
Bio: Sarah Chen is the CFO of Airtable, where she oversees all financial
operations for the collaborative work platform. Prior to Airtable, Sarah
was VP of Finance at Dropbox, where she led the company through its IPO
in 2018. She has deep expertise in B2B SaaS unit economics and scaling
finance organizations through hypergrowth phases.
```

#### Unstructured: Job Descriptions

Purpose: Open role descriptions for portfolio companies

**Format:** Text files, one per role

```
Company: Pigment
Role: Chief Financial Officer
Stage: Series B
Description:
Pigment is seeking a CFO to lead our finance organization as we scale
from $30M to $100M ARR. The ideal candidate has:
- Experience scaling B2B SaaS finance operations through hypergrowth
- Track record managing Series B+ fundraising rounds
- International finance operations experience (we have teams in US, EU, APAC)
- Expertise in complex B2B revenue models and unit economics
- Startup DNA with enterprise-scale operational rigor
```

### Airtable Data Schema

#### Table: People

**Purpose:** All executives in the system (guild members, network, candidates)

**Fields:**

- `person_id` (Auto-number, Primary Key)
- `exec_id` (Single line text) - External stable ID
- `name` (Single line text) - Full name
- `current_title` (Single line text)
- `current_company` (Link to Companies table)
- `linkedin_url` (URL)
- `location` (Single line text)
- `function` (Single select) - CTO, CFO, CPO, CRO, CMO, COO, Other
- `seniority_level` (Single select) - C-Level, VP, Head, Director, Senior
- `relationship_type` (Single select) - Guild Member, Partner Network, Portfolio, Event, Other
- `source_partner` (Single line text) - Who introduced them
- `bio` (Long text) - Unstructured bio text (optional)
- `prior_companies` (Long text) - Semicolon-separated
- `recent_exit` (Checkbox) - IPO/M&A experience
- `created_at` (Created time)
- `updated_at` (Last modified time)
- `workflows` (Link to Workflows table) - All assessments/research runs

#### Table: Companies

**Purpose:** All companies (portfolio and external)

**Fields:**

- `company_id` (Auto-number, Primary Key)
- `name` (Single line text)
- `domain` (Single line text) - e.g., "airtable.com"
- `stage` (Single select) - Seed, A, B, C, D, Growth, Public
- `sector` (Single select) - B2B SaaS, Consumer, Fintech, Healthcare, etc.
- `is_portfolio` (Checkbox)
- `description` (Long text)
- `website` (URL)
- `people` (Link to People table) - Employees/execs at this company

#### Table: Portcos (Portfolio Companies)

**Purpose:** Subset of Companies that are FirstMark portfolio

**Fields:**

- `portco_id` (Auto-number, Primary Key)
- `company` (Link to Companies table)
- `stage` (Single select) - Series A, B, C, D, Growth
- `sector` (Single select)
- `founding_year` (Number)
- `employee_count` (Number)
- `geography` (Multiple select) - US, EMEA, APAC, LATAM
- `key_metrics` (Long text) - ARR, growth rate, etc.
- `roles` (Link to Portco Roles table)

#### Table: Portco Roles

**Purpose:** All open roles at portfolio companies

**Fields:**

- `role_id` (Auto-number, Primary Key)
- `portco` (Link to Portcos table)
- `role_type` (Single select) - CFO, CTO, CPO, CRO, CMO, COO
- `title` (Single line text) - Exact title for JD
- `description` (Long text) - Full job description
- `status` (Single select) - Open, In Progress, Filled, Closed
- `priority` (Single select) - High, Medium, Low
- `posted_date` (Date)
- `searches` (Link to Searches table) - Active searches for this role

#### Table: Role Specs

**Purpose:** Standardized evaluation frameworks for roles

**Fields:**

- `spec_id` (Auto-number, Primary Key)
- `name` (Single line text) - e.g., "Series B CFO - B2B SaaS"
- `role_type` (Single select) - CFO, CTO, CPO, etc.
- `is_template` (Checkbox) - Base template vs. customized
- `dimensions` (Long text, JSON) - Structured spec (see Role Spec Framework section)
- `description` (Long text) - Human-readable overview
- `created_at` (Created time)
- `searches` (Link to Searches table) - Searches using this spec

**Dimensions JSON Structure:**

```json
{
  "dimensions": [
    {
      "name": "Financial Expertise",
      "weight": 0.30,
      "description": "Deep expertise in finance operations, accounting, FP&A, and financial strategy",
      "scale": {
        "1": "Limited finance experience, junior roles",
        "2": "Mid-level finance experience, some leadership",
        "3": "Senior finance leader, managed teams",
        "4": "CFO or equivalent at similar stage/scale",
        "5": "CFO at larger/more complex organization with exceptional track record"
      }
    },
    {
      "name": "Scaling Experience",
      "weight": 0.25,
      "description": "Experience scaling companies through hypergrowth phases",
      "scale": { ... }
    }
  ]
}
```

#### Table: Searches

**Purpose:** Active executive searches FirstMark is assisting with

**Fields:**

- `search_id` (Auto-number, Primary Key)
- `role` (Link to Portco Roles table)
- `role_spec` (Link to Role Specs table)
- `status` (Single select) - Planning, Active, On Hold, Completed
- `priority` (Single select) - High, Medium, Low
- `custom_guidance` (Long text) - Additional requirements beyond spec
- `start_date` (Date)
- `target_close_date` (Date)
- `screens` (Link to Screens table) - Screening batches for this search
- `notes` (Long text)

#### Table: Screens

**Purpose:** Batch screening runs for a search

**Fields:**

- `screen_id` (Auto-number, Primary Key)
- `search` (Link to Searches table)
- `candidates` (Link to People table, multiple) - Who to evaluate
- `status` (Single select) - Draft, Ready, Processing, Complete, Failed
- `custom_guidance` (Long text) - Additional context for this batch
- `started_at` (Date)
- `completed_at` (Date)
- `workflows` (Link to Workflows table) - Individual candidate workflows
- `summary` (Long text) - Overall results summary

#### Table: Workflows

**Purpose:** Individual candidate research + assessment runs (audit trail)

**Fields:**

- `workflow_id` (Auto-number, Primary Key)
- `screen` (Link to Screens table)
- `candidate` (Link to People table)
- `search` (Link to Searches table)
- `status` (Single select) - Pending, Researching, Assessing, Complete, Failed
- `started_at` (Date)
- `completed_at` (Date)
- `research_summary` (Long text) - Summary from deep research
- `research_citations` (Long text, JSON) - List of sources
- `research_raw` (Long text) - Full OpenAI API response
- `assessment_overall_score` (Number) - 1.0 to 5.0
- `assessment_confidence` (Single select) - High, Medium, Low
- `assessment_dimensions` (Long text, JSON) - Dimension-level scores
- `assessment_reasoning` (Long text) - Overall justification
- `assessment_counterfactuals` (Long text) - "What would make this a 5.0?"
- `assessment_raw` (Long text) - Full LLM response
- `error_log` (Long text) - If failed, why
- `export_markdown` (Attachment) - Markdown export of full report

---

## Core Components

### 1. Data Ingestion Module

**File:** `src/ingestion.py`

**Purpose:** Parse CSVs, normalize data, deduplicate, load to Airtable

**Functions:**

```python
def parse_csv(file_path: str, file_type: str) -> List[Dict]:
    """
    Parse CSV file and normalize to standard schema.

    Args:
        file_path: Path to CSV file
        file_type: "guild" or "network"

    Returns:
        List of normalized records
    """

def normalize_person(raw_record: Dict) -> Dict:
    """
    Normalize person record to standard schema.
    Handles field name variations, empty values, etc.
    """

def deduplicate_people(records: List[Dict]) -> List[Dict]:
    """
    Simple deduplication by exec_id and name.
    More sophisticated logic would use fuzzy matching.
    """

def load_to_airtable(records: List[Dict], table_name: str):
    """
    Batch upload to Airtable with error handling.
    """
```

**Demo Scope:**

- ✅ Basic CSV parsing
- ✅ Field normalization
- ✅ Simple deduplication by ID
- ⚠️ No fuzzy matching or entity resolution
- ⚠️ Limited error handling

### 2. Research Module

**File:** `src/research.py`

**Purpose:** Deep research on candidates using OpenAI Deep Research API

**Functions:**

```python
def research_candidate(
    person: Dict,
    role_context: Dict,
    search_guidance: str = ""
) -> Dict:
    """
    Run deep research on a candidate for a specific role.

    Args:
        person: Person record from Airtable
        role_context: Role and company info
        search_guidance: Additional search parameters

    Returns:
        {
            "summary": "...",
            "citations": [...],
            "raw_response": {...},
            "confidence": "high|medium|low"
        }
    """
```

**Research Prompt Template:**

```python
RESEARCH_PROMPT = """
You are researching {candidate_name} as a potential candidate for the {role_title}
role at {company_name}.

Company Context:
{company_description}

Role Requirements:
{role_spec_summary}

Research Focus:
1. Current role and responsibilities at {current_company}
2. Career trajectory and relevant experience
3. Key accomplishments and track record
4. Domain expertise relevant to {role_type}
5. Stage experience (especially {target_stage})
6. Geographic experience (especially {target_geography})
7. Any public signals about career interests or availability

Provide:
- Comprehensive summary (300-500 words)
- Key signals (bulleted list of 5-8 most relevant facts)
- Potential concerns or gaps
- 10+ citations from diverse sources (LinkedIn, company blogs, press, interviews)

Be thorough but concise. Focus on facts over speculation.
"""
```

**OpenAI Deep Research API Call:**

```python
import openai

response = openai.beta.deep_research.create(
    model="gpt-5-1",
    messages=[{
        "role": "user",
        "content": research_prompt
    }],
    max_tokens=4000,
    temperature=0.3
)

# Response includes:
# - response.choices[0].message.content (summary)
# - response.citations (list of sources)
```

**Demo Scope:**

- ✅ OpenAI Deep Research API integration
- ✅ Structured research prompts
- ✅ Citation extraction and storage
- ⚠️ No custom web scraping
- ⚠️ No incremental search (would use Tavily if needed)

### 3. Assessment Module

**File:** `src/assessment.py`

**Purpose:** Evaluate candidates against role specs using structured LLM assessment

**Functions:**

```python
from pydantic import BaseModel
from typing import List

class DimensionScore(BaseModel):
    dimension_name: str
    score: float  # 1.0 to 5.0
    confidence: str  # "High", "Medium", "Low"
    reasoning: str  # Justification with evidence
    evidence_quotes: List[str]  # Direct quotes from research

class Assessment(BaseModel):
    overall_score: float
    overall_confidence: str
    dimension_scores: List[DimensionScore]
    overall_reasoning: str
    counterfactuals: str  # "What would make this a 5.0?"
    red_flags: str  # Concerns or missing info
    recommendation: str  # "Strong fit", "Moderate fit", "Weak fit"

def assess_candidate(
    person: Dict,
    research: Dict,
    role_spec: Dict
) -> Assessment:
    """
    Assess candidate against role spec using GPT-5 with structured output.

    Args:
        person: Person record
        research: Research results
        role_spec: Role specification with dimensions

    Returns:
        Assessment object with scores and reasoning
    """
```

**Assessment Prompt Template:**

```python
ASSESSMENT_PROMPT = """
You are evaluating {candidate_name} for the {role_title} role at {company_name}.

ROLE SPECIFICATION:
{role_spec_json}

CANDIDATE RESEARCH:
{research_summary}

CITATIONS:
{research_citations}

Evaluate the candidate on each dimension in the role specification:

For each dimension:
1. Assign a score from 1.0 to 5.0 based on the scale provided
2. Indicate your confidence (High/Medium/Low) based on evidence quality
3. Provide detailed reasoning citing specific evidence
4. Include direct quotes from research to support your assessment

Then provide:
- Overall score (weighted average of dimensions)
- Overall confidence level
- Overall reasoning (synthesis of dimensional assessments)
- Counterfactuals: What evidence would make this candidate a 5.0?
- Red flags: Any concerns or missing critical information
- Recommendation: Strong fit / Moderate fit / Weak fit

Be rigorous. High scores require strong evidence. Acknowledge gaps in information.
Use the confidence field to indicate when you're inferring vs. when you have direct evidence.
"""
```

**Agno Agent Implementation:**

```python
import agno

# Define assessment agent with structured output
assessment_agent = agno.Agent(
    model="gpt-5-1",
    response_model=Assessment,
    system_prompt="You are an expert executive recruiter...",
    temperature=0.2,
    max_tokens=3000
)

# Run assessment
assessment = assessment_agent.run(
    prompt=assessment_prompt,
    research=research_data,
    role_spec=role_spec_data
)
```

**Demo Scope:**

- ✅ GPT-5 with Agno framework
- ✅ Structured outputs (Pydantic models)
- ✅ Dimension-level scoring
- ✅ Confidence levels
- ✅ Evidence-based reasoning
- ✅ Counterfactual analysis
- ⚠️ No multi-model consensus (would be good for production)
- ⚠️ No human-in-the-loop calibration

### 4. Webhook Server

**File:** `webhook_server.py`

**Purpose:** Flask server to receive Airtable webhooks and orchestrate workflows

**Routes:**

```python
from flask import Flask, request, jsonify
from pyairtable import Api
import os

app = Flask(__name__)
airtable = Api(os.getenv("AIRTABLE_API_KEY"))

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy"})

@app.route('/upload', methods=['POST'])
def process_upload():
    """
    Handle CSV upload and ingestion.

    Webhook payload:
    {
        "upload_id": "recXXX",
        "file_url": "https://...",
        "file_type": "guild" | "network"
    }
    """
    # Download file from Airtable
    # Parse and normalize
    # Load to appropriate table
    # Update upload record with results

@app.route('/screen', methods=['POST'])
def run_screening():
    """
    Main screening workflow. Process multiple candidates for a search.

    Webhook payload:
    {
        "screen_id": "recXXX"
    }
    """
    # Get screen record + linked data
    # For each candidate:
    #   - Create workflow record
    #   - Run research
    #   - Run assessment
    #   - Store results
    # Update screen status

@app.route('/research', methods=['POST'])
def run_research():
    """
    Run research on individual candidate (standalone).

    Webhook payload:
    {
        "person_id": "recXXX",
        "search_id": "recYYY"  # optional
    }
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

**Detailed `/screen` Implementation:**

```python
@app.route('/screen', methods=['POST'])
def run_screening():
    data = request.json
    screen_id = data['screen_id']

    print(f"🚀 Starting screening: {screen_id}")

    # 1. Fetch screen record
    screens_table = airtable.table('base_id', 'Screens')
    screen = screens_table.get(screen_id)

    # Update status
    screens_table.update(screen_id, {"status": "Processing"})

    # 2. Get linked data
    search_id = screen['fields']['search'][0]
    candidate_ids = screen['fields']['candidates']

    searches_table = airtable.table('base_id', 'Searches')
    search = searches_table.get(search_id)

    role_id = search['fields']['role'][0]
    spec_id = search['fields']['role_spec'][0]

    # 3. Load role spec
    specs_table = airtable.table('base_id', 'Role Specs')
    spec = specs_table.get(spec_id)
    spec_data = json.loads(spec['fields']['dimensions'])

    # 4. Process each candidate
    workflows_table = airtable.table('base_id', 'Workflows')
    people_table = airtable.table('base_id', 'People')

    results = []

    for i, candidate_id in enumerate(candidate_ids):
        print(f"\n📝 Processing candidate {i+1}/{len(candidate_ids)}: {candidate_id}")

        # Create workflow record
        workflow = workflows_table.create({
            "screen": [screen_id],
            "candidate": [candidate_id],
            "search": [search_id],
            "status": "Researching"
        })
        workflow_id = workflow['id']

        try:
            # Get candidate
            person = people_table.get(candidate_id)

            # Run research
            print(f"  🔍 Researching {person['fields']['name']}...")
            research_result = research_candidate(
                person=person['fields'],
                role_context={...},
                search_guidance=search['fields'].get('custom_guidance', '')
            )

            # Update workflow
            workflows_table.update(workflow_id, {
                "status": "Assessing",
                "research_summary": research_result['summary'],
                "research_citations": json.dumps(research_result['citations']),
                "research_raw": json.dumps(research_result['raw_response'])
            })

            print(f"  ✅ Research complete ({len(research_result['citations'])} citations)")

            # Run assessment
            print(f"  🎯 Running assessment...")
            assessment = assess_candidate(
                person=person['fields'],
                research=research_result,
                role_spec=spec_data
            )

            # Update workflow
            workflows_table.update(workflow_id, {
                "status": "Complete",
                "assessment_overall_score": assessment.overall_score,
                "assessment_confidence": assessment.overall_confidence,
                "assessment_dimensions": assessment.model_dump_json(),
                "assessment_reasoning": assessment.overall_reasoning,
                "assessment_counterfactuals": assessment.counterfactuals,
                "completed_at": datetime.now().isoformat()
            })

            print(f"  ✅ Assessment complete (Score: {assessment.overall_score:.1f}/5.0)")

            results.append({
                "candidate_id": candidate_id,
                "workflow_id": workflow_id,
                "score": assessment.overall_score,
                "status": "success"
            })

        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
            workflows_table.update(workflow_id, {
                "status": "Failed",
                "error_log": str(e)
            })
            results.append({
                "candidate_id": candidate_id,
                "status": "failed",
                "error": str(e)
            })

    # 5. Update screen record
    screens_table.update(screen_id, {
        "status": "Complete",
        "completed_at": datetime.now().isoformat(),
        "summary": json.dumps(results)
    })

    print(f"\n✅ Screening complete: {len(results)} candidates processed")

    return jsonify({
        "status": "success",
        "screen_id": screen_id,
        "candidates_processed": len(results),
        "results": results
    })
```

---

## Airtable Design

### Automation Triggers

**Trigger 1: Start Screening (Button)**

```
When: Button field "Start Screening" clicked in Screens table
Action: Send webhook to ngrok URL
URL: https://[ngrok-id].ngrok.io/screen
Method: POST
Body:
{
  "screen_id": "{Screen ID}",
  "trigger_time": "{Created Time}"
}
```

**Trigger 2: Start Screening (Status Change)**

```
When: Status field in Screens table changes to "Ready"
Action: Send webhook to ngrok URL
URL: https://[ngrok-id].ngrok.io/screen
Method: POST
Body:
{
  "screen_id": "{Screen ID}",
  "trigger_time": "{Last Modified Time}"
}
```

### Airtable Interface Views

**View 1: Candidate Ranking (for Search)**

**Table:** Workflows
**Filter:** `Search = [specific search]` AND `Status = Complete`
**Sort:** `assessment_overall_score` DESC
**Fields Shown:**

- Candidate (linked)
- Overall Score
- Confidence
- Top 2 Dimension Scores
- Recommendation
- Link to full Workflow

**View 2: Assessment Detail**

**Table:** Workflows
**Layout:** Expanded record view
**Sections:**

- Candidate Info
- Research Summary + Citations
- Assessment Scores (all dimensions)
- Reasoning
- Counterfactuals
- Download Markdown Report

**View 3: Active Searches Dashboard**

**Table:** Searches
**Filter:** `Status = Active`
**Fields:**

- Role (linked)
- Priority
- Status

- # Candidates Screened

- Top 3 Candidates (linked, sorted by score)
- Last Updated

---

## Role Spec Framework

### Structure

A Role Spec defines **what "good" looks like** for a specific role type at a specific company stage/context.

**Components:**

1. **Dimensions** - Key evaluation criteria (typically 4-6)
2. **Weights** - Relative importance of each dimension (sum to 1.0)
3. **Scales** - Definition of scores 1-5 for each dimension
4. **Context** - Company stage, sector, specific requirements

### Base Template: CFO

```json
{
  "name": "CFO - Series B B2B SaaS",
  "role_type": "CFO",
  "is_template": true,
  "dimensions": [
    {
      "name": "Financial Expertise",
      "weight": 0.30,
      "description": "Deep expertise in finance operations, accounting, FP&A, and financial strategy for SaaS businesses",
      "scale": {
        "1": "Limited finance experience. Junior or functional specialist roles. No SaaS background.",
        "2": "Mid-level finance experience (Manager/Sr Manager). Some exposure to SaaS metrics but not primary focus.",
        "3": "Senior finance leader (Director/VP Finance). Managed finance teams. Good understanding of SaaS unit economics.",
        "4": "CFO or Head of Finance at similar stage B2B SaaS company. Deep SaaS finance expertise. Proven track record.",
        "5": "CFO at larger/more complex B2B SaaS org ($100M+ ARR). Exceptional track record. Thought leader in SaaS finance."
      }
    },
    {
      "name": "Scaling Experience",
      "weight": 0.25,
      "description": "Experience scaling companies through rapid growth phases, especially Series B to C/D",
      "scale": {
        "1": "No hypergrowth experience. Only steady-state or slow-growth companies.",
        "2": "Some exposure to growth companies but not primary driver. Joined post-hypergrowth.",
        "3": "Led finance through moderate growth phase (50-100% YoY). Series A or B stage focus.",
        "4": "Led finance through hypergrowth (100%+ YoY for 2+ years). Series B to D experience. Scaled team and systems.",
        "5": "Multiple hypergrowth experiences. Series B to IPO/exit. Exceptional track record across different stages."
      }
    },
    {
      "name": "Fundraising & Investor Relations",
      "weight": 0.20,
      "description": "Experience leading or supporting fundraising efforts and managing investor relationships",
      "scale": {
        "1": "No fundraising involvement. Public company or bootstrapped background only.",
        "2": "Supported fundraising in operational capacity. Limited direct investor interaction.",
        "3": "Co-led fundraising process (with CEO). Managed investor updates and board materials. Series A/B rounds.",
        "4": "Led Series B+ fundraising rounds. Strong investor relationships. Regular board reporting.",
        "5": "Led multiple later-stage rounds (C/D+) and/or IPO process. Top-tier investor relationships. Board-level credibility."
      }
    },
    {
      "name": "International Operations",
      "weight": 0.15,
      "description": "Experience managing finance across multiple geographies with different regulatory requirements",
      "scale": {
        "1": "Domestic-only experience. No international exposure.",
        "2": "Some international awareness but no direct management responsibility.",
        "3": "Managed finance for 1-2 international markets. Basic multi-currency and compliance experience.",
        "4": "Led finance across 3+ major markets (e.g., US + EMEA + APAC). Deep expertise in international accounting and tax.",
        "5": "Global finance operations across major markets. Complex multi-entity structures. Regulatory expertise."
      }
    },
    {
      "name": "Cultural & Network Fit",
      "weight": 0.10,
      "description": "Fit with startup culture and FirstMark network. Values alignment.",
      "scale": {
        "1": "Pure big company background. No startup or VC-backed experience. Unknown to network.",
        "2": "Some startup exposure but primarily corporate. Limited network connections.",
        "3": "Strong startup DNA. Prior VC-backed companies. Some FirstMark network overlap.",
        "4": "Deep startup experience. Well-connected in FirstMark network (Guild member, prior portco, etc.). Strong references.",
        "5": "Exceptional cultural fit. Key FirstMark relationships. Proven startup builder with our values. Multiple strong internal advocates."
      }
    }
  ],
  "custom_notes": "For companies with complex revenue models or international operations, weight Financial Expertise and International Operations higher. For earlier stage (Series A), reduce Fundraising weight and increase Scaling weight."
}
```

### Base Template: CTO

```json
{
  "name": "CTO - Series B Technical Product",
  "role_type": "CTO",
  "is_template": true,
  "dimensions": [
    {
      "name": "Technical Leadership",
      "weight": 0.30,
      "description": "Deep technical expertise and ability to lead engineering teams through scaling challenges",
      "scale": {
        "1": "Limited technical depth. Junior IC or recent transition to management. No architecture experience.",
        "2": "Strong IC background but limited leadership. Managed small teams. Some architecture work.",
        "3": "Experienced engineering leader (Director/VP Eng). Led teams of 20-50. Solid technical decisions at scale.",
        "4": "Head of Engineering or CTO at similar-stage company. Scaled eng org 50-150+. Strong technical vision and execution.",
        "5": "CTO at larger/more complex technical organization. Built world-class eng cultures. Thought leader in technical leadership."
      }
    },
    {
      "name": "Product & Architecture Vision",
      "weight": 0.25,
      "description": "Ability to set technical strategy and architecture that enables product innovation",
      "scale": {
        "1": "Execution-focused only. No product or architecture strategy experience.",
        "2": "Some product input but primarily executes others' vision. Basic architecture decisions.",
        "3": "Collaborative product thinking. Shaped architecture for current scale. Good technical decisions.",
        "4": "Strong product partnership. Designed architecture for 10x scale. Made bold technical bets that paid off.",
        "5": "Product-minded engineering leader. Visionary technical architecture. Track record of innovative product+tech decisions."
      }
    },
    {
      "name": "Scaling Experience",
      "weight": 0.20,
      "description": "Experience scaling engineering teams, systems, and processes through rapid growth",
      "scale": {
        "1": "No scaling experience. Steady-state teams only.",
        "2": "Grew team modestly (2x over 2 years). Some scaling challenges addressed.",
        "3": "Scaled team 3-5x through growth phase. Implemented good processes. Some system rewrites.",
        "4": "Scaled team 5-10x through hypergrowth. Re-architected major systems. Built scalable processes.",
        "5": "Multiple scaling experiences across companies/stages. 10x+ team growth. Rebuilt systems at massive scale."
      }
    },
    {
      "name": "Recruiting & Team Building",
      "weight": 0.15,
      "description": "Ability to attract, hire, and retain top engineering talent",
      "scale": {
        "1": "Limited hiring experience. No strong track record building teams.",
        "2": "Hired and managed small teams. Some good hires but inconsistent.",
        "3": "Built solid engineering teams. Good hiring bar. Low regrettable attrition.",
        "4": "Exceptional recruiter. Attracted top talent repeatedly. Built high-performing teams. Strong employee brand.",
        "5": "Magnetic hiring presence. Track record of building world-class eng teams. Alumni network. Destination employer."
      }
    },
    {
      "name": "Cultural & Network Fit",
      "weight": 0.10,
      "description": "Fit with startup culture, product focus, and FirstMark network",
      "scale": {
        "1": "Pure big tech background. No startup experience. Unknown to network.",
        "2": "Some startup exposure but primarily corporate. Limited network connections.",
        "3": "Strong startup DNA. Product-minded. Some FirstMark network overlap.",
        "4": "Deep startup experience. Product-obsessed. Well-connected in FirstMark network (Guild member, prior portco).",
        "5": "Exceptional cultural fit. Key FirstMark relationships. Proven product+eng leader. Multiple strong advocates."
      }
    }
  ],
  "custom_notes": "For AI/ML or data-intensive products, add or upweight a 'Domain Expertise' dimension. For developer tools, emphasize 'Product Vision' and 'Technical Credibility' with target audience."
}
```

### Customization Process

**Option 1: Start from Template**

1. Select base template (CFO or CTO)
2. Adjust weights based on role specifics
3. Modify scale definitions for company context
4. Add custom dimension if needed (max 6 total)
5. Add custom notes

**Option 2: Generate with AI** (Future enhancement)

1. Input: Job description + company context
2. LLM generates draft spec based on templates
3. Human reviews and edits
4. Saves as custom spec

**Option 3: Manual Creation**

1. Define 4-6 dimensions
2. Set weights (sum to 1.0)
3. Write scale definitions for each dimension
4. Add context notes

### Usage in Assessment

When assessing a candidate:

1. Load role spec dimensions and weights
2. For each dimension:
   - LLM scores 1-5 based on scale definition
   - LLM provides confidence (H/M/L) based on evidence
   - LLM writes reasoning with citations
3. Calculate overall score: `Σ(dimension_score × weight)`
4. LLM provides overall reasoning and counterfactuals

---

## Assessment Framework

### Assessment Process Flow

```
1. Input:
   - Candidate research (summary + citations)
   - Role spec (dimensions, weights, scales)
   - Search guidance (optional custom requirements)

2. Dimensional Assessment:
   For each dimension:
     a. Review scale definitions (1-5)
     b. Analyze research evidence
     c. Assign score with reasoning
     d. Indicate confidence level
     e. Extract supporting quotes

3. Overall Assessment:
   a. Calculate weighted average score
   b. Synthesize overall reasoning
   c. Generate counterfactuals
   d. Identify red flags or gaps
   e. Provide recommendation

4. Output:
   - Structured Assessment object (Pydantic model)
   - Stored in Airtable Workflows table
   - Exported as markdown for portability
```

### Confidence Levels

**High Confidence:**

- Direct evidence from multiple sources
- Clear, specific information
- Consistent across sources
- Recent and relevant

**Medium Confidence:**

- Some direct evidence, some inference
- Limited sources or older information
- Reasonable extrapolation from related experience

**Low Confidence:**

- Minimal direct evidence
- Significant inference required
- Conflicting information
- Critical gaps in research

### Counterfactual Analysis

**Purpose:** Help humans understand what's missing for a perfect score

**Template:**

```
For this candidate to achieve a 5.0 on [Dimension X], we would need to see:
1. [Specific evidence type 1]
2. [Specific evidence type 2]
3. [Specific evidence type 3]

Current gap: [What's missing or weak]
```

**Example:**

```
For this candidate to achieve a 5.0 on International Operations, we would need to see:
1. Direct experience managing finance across 5+ countries including complex markets (China, Brazil, etc.)
2. Evidence of handling multi-currency treasury operations at scale
3. Track record navigating complex international regulatory requirements (GDPR, data localization, etc.)

Current gap: Limited to US + basic EMEA. No evidence of APAC or complex regulatory experience.
```

### Red Flags & Gaps

**Red Flags:**

- Inconsistencies in timeline or role descriptions
- Short tenures at multiple companies (without clear explanation)
- Gaps in employment
- Misalignment with key requirements
- Evidence of poor judgment or ethics

**Gaps:**

- Missing critical information
- Areas where research couldn't find evidence
- Dimensions where confidence is low
- Unverified claims

### Markdown Export Format

```markdown
# Candidate Assessment Report

**Candidate:** [Name]
**Role:** [Title] at [Company]
**Search:** [Search name]
**Date:** [YYYY-MM-DD]

---

## Overall Assessment

**Score:** [X.X] / 5.0
**Confidence:** [High|Medium|Low]
**Recommendation:** [Strong fit|Moderate fit|Weak fit]

### Summary
[2-3 paragraph synthesis of overall fit]

---

## Research Summary

[Summary from deep research]

### Key Signals
- [Signal 1]
- [Signal 2]
- [Signal 3]

### Citations
1. [Citation 1 with URL]
2. [Citation 2 with URL]
...

---

## Dimensional Assessment

### [Dimension 1 Name] (Weight: XX%)

**Score:** [X.X] / 5.0
**Confidence:** [High|Medium|Low]

**Reasoning:**
[Detailed reasoning with evidence]

**Supporting Evidence:**
> "[Quote from research]"
> "[Quote from research]"

---

[Repeat for each dimension]

---

## Counterfactual Analysis

**What would make this a 5.0 overall?**

[Dimension by dimension breakdown of gaps]

---

## Red Flags & Concerns

[Any concerns or missing critical information]

---

## Next Steps

**Recommended Actions:**
- [ ] [Action 1]
- [ ] [Action 2]
- [ ] [Action 3]

**Questions to Ask in Interview:**
1. [Question about gap or unclear area]
2. [Question to validate assumption]
3. [Question to explore fit]

---

*Generated by FirstMark Talent Signal Agent*
*Workflow ID: [workflow_id]*
```

---

## Implementation Details

### Environment Setup

**Required Environment Variables (.env file):**

```bash
# Airtable
AIRTABLE_API_KEY=pat... # Personal access token
AIRTABLE_BASE_ID=app... # Base ID for this project

# OpenAI
OPENAI_API_KEY=sk-... # OpenAI API key

# Tavily (optional)
TAVILY_API_KEY=tvly-... # Tavily search API key

# Flask
FLASK_SECRET_KEY=... # Random secret for session management
FLASK_ENV=development

# ngrok (for demo)
NGROK_AUTH_TOKEN=... # ngrok auth token
```

### Project Structure

```
talent-signal-agent/
├── .env                      # Environment variables
├── .gitignore
├── README.md
├── requirements.txt
│
├── data/                     # Mock data
│   ├── mock_guilds.csv
│   ├── exec_network.csv
│   ├── job_descriptions/
│   │   ├── pigment_cfo.txt
│   │   ├── mockingbird_cfo.txt
│   │   ├── synthesia_cto.txt
│   │   └── estuary_cto.txt
│   └── bios/                 # Optional
│
├── src/
│   ├── __init__.py
│   ├── ingestion.py          # CSV parsing and data loading
│   ├── research.py           # Deep research module
│   ├── assessment.py         # Candidate assessment module
│   ├── models.py             # Pydantic models
│   └── utils.py              # Shared utilities
│
├── webhook_server.py         # Flask server
├── setup_airtable.py         # Script to create/configure tables
└── exports/                  # Generated markdown reports
```

### Setup Script

**File:** `setup_airtable.py`

```python
"""
Script to create Airtable base structure.
Run once to set up all tables and fields.
"""

from pyairtable import Api
import os
from dotenv import load_dotenv

load_dotenv()

def create_tables():
    api = Api(os.getenv("AIRTABLE_API_KEY"))
    base_id = os.getenv("AIRTABLE_BASE_ID")

    # Create People table
    # Create Companies table
    # Create Portcos table
    # ... etc

    print("✅ Airtable base structure created")

if __name__ == "__main__":
    create_tables()
```

### Running the Demo

**Terminal 1: Start Flask Server**

```bash
python webhook_server.py
```

**Terminal 2: Start ngrok**

```bash
ngrok http 5000
```

**Terminal 3: Load Mock Data (one-time)**

```bash
python -m src.ingestion
```

**In Airtable:**

1. Configure automation with ngrok URL
2. Create Screen record
3. Link Search and Candidates
4. Click "Start Screening" or change Status to "Ready"

**Monitor Progress:**

- Watch Terminal 1 for real-time logs
- Refresh Airtable to see results populate

---

## API References

### OpenAI Deep Research API

**Documentation:** <https://platform.openai.com/docs/api-reference/deep-research>

**Example Call:**

```python
import openai

response = openai.beta.deep_research.create(
    model="gpt-5-1",
    messages=[{
        "role": "user",
        "content": "Research Sarah Chen, CFO at Airtable, as a candidate for a Series B SaaS CFO role..."
    }],
    max_tokens=4000,
    temperature=0.3,
    metadata={
        "purpose": "candidate_research",
        "candidate_id": "exec_001"
    }
)

# Response structure
{
    "id": "dr_...",
    "object": "deep_research",
    "created": 1234567890,
    "model": "gpt-5-1",
    "choices": [{
        "index": 0,
        "message": {
            "role": "assistant",
            "content": "# Research Summary\n\n..."
        },
        "finish_reason": "stop"
    }],
    "citations": [
        {
            "url": "https://linkedin.com/in/sarahchen",
            "title": "Sarah Chen - LinkedIn",
            "snippet": "CFO at Airtable...",
            "accessed_at": "2025-11-16T..."
        },
        ...
    ],
    "usage": {
        "prompt_tokens": 245,
        "completion_tokens": 1823,
        "total_tokens": 2068
    }
}
```

### GPT-5 with Structured Outputs

**Example with Pydantic:**

```python
from openai import OpenAI
from pydantic import BaseModel

client = OpenAI()

class Assessment(BaseModel):
    overall_score: float
    overall_confidence: str
    # ... other fields

completion = client.beta.chat.completions.parse(
    model="gpt-5-1",
    messages=[
        {"role": "system", "content": "You are an expert executive recruiter..."},
        {"role": "user", "content": assessment_prompt}
    ],
    response_format=Assessment,
    temperature=0.2,
    max_tokens=3000
)

assessment = completion.choices[0].message.parsed
```

### Tavily Search API

**Documentation:** <https://docs.tavily.com>

**Example Call:**

```python
from tavily import TavilyClient

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

response = tavily.search(
    query="Sarah Chen CFO Airtable background experience",
    search_depth="advanced",
    max_results=10,
    include_domains=["linkedin.com", "techcrunch.com", "forbes.com"]
)

# Response structure
{
    "query": "...",
    "results": [
        {
            "title": "...",
            "url": "...",
            "content": "...",
            "score": 0.95
        },
        ...
    ]
}
```

### Airtable API (via pyairtable)

**Documentation:** <https://pyairtable.readthedocs.io>

**Example Operations:**

```python
from pyairtable import Api

api = Api(os.getenv("AIRTABLE_API_KEY"))
table = api.table("base_id", "People")

# Create record
record = table.create({
    "name": "Sarah Chen",
    "current_title": "CFO",
    "linkedin_url": "https://..."
})

# Get record
record = table.get("rec123...")

# Update record
table.update("rec123...", {
    "assessment_score": 4.2
})

# List records with filter
records = table.all(
    formula="{function} = 'CFO'",
    sort=["name"]
)

# Batch create
records = table.batch_create([
    {"name": "Person 1", ...},
    {"name": "Person 2", ...},
    ...
])
```

---

## Technical Notes & Constraints

### Demo Scope & Limitations

**What Works:**

- ✅ End-to-end workflow from data ingestion to ranked output
- ✅ Real OpenAI Deep Research API integration
- ✅ Structured assessment with GPT-5
- ✅ Airtable UI for viewing results
- ✅ Webhook-triggered workflows
- ✅ Full audit trail and logging
- ✅ Markdown exports

**What's Simplified:**

- ⚠️ Enrichment is stubbed (mock Apollo data)
- ⚠️ Limited error handling and retry logic
- ⚠️ No deduplication or entity resolution
- ⚠️ Manual role spec creation (no AI assist)
- ⚠️ Small candidate pool (20 people)
- ⚠️ No rate limiting or queue management
- ⚠️ Local hosting (ngrok, not production)

**What's Conceptual:**

- 📋 Centralized data platform
- 📋 Affinity integration
- 📋 Historical candidate profiles
- 📋 Multi-model consensus
- 📋 Human-in-the-loop calibration
- 📋 Production infrastructure and monitoring

### Future Enhancements (Tier 2 MVP)

**Data Quality:**

- Real enrichment via Apollo or Harmonic
- Fuzzy matching for deduplication
- Entity resolution across sources
- Data validation and cleansing

**Assessment Quality:**

- Multi-model consensus (GPT-5 + Claude + others)
- Human calibration loop
- Historical assessment quality tracking
- A/B testing of assessment prompts

**Infrastructure:**

- Production hosting (Render, Railway, or AWS)
- Queue system for async processing (Celery + Redis)
- Rate limiting and retry logic
- Comprehensive error handling
- Monitoring and alerting (Sentry, DataDog)

**User Experience:**

- Better Airtable interface design
- Email notifications for completed screenings
- Export to Google Sheets or Notion
- Bulk operations and batch processing

**Extensibility:**

- Plugin architecture for new research sources
- Customizable assessment frameworks
- Multi-use case support (founders, LPs, etc.)
- API for programmatic access

---

## Demo Data Specifications

### Mock Companies (Portcos)

**Pigment:**

- Stage: Series B
- Sector: B2B SaaS
- Description: Business planning platform for enterprise finance teams
- Geography: US, EMEA
- Open Role: CFO

**Mockingbird:**

- Stage: Series A
- Sector: Consumer DTC
- Description: Direct-to-consumer premium kitchenware brand
- Geography: US
- Open Role: CFO

**Synthesia:**

- Stage: Series C
- Sector: AI/ML SaaS
- Description: AI video generation platform
- Geography: Global (US, EMEA, APAC)
- Open Role: CTO

**Estuary:**

- Stage: Series A
- Sector: Data Infrastructure
- Description: Real-time data integration and CDC platform
- Geography: US
- Open Role: CTO

### Mock Candidates

**Target: 15-20 candidates total**

**CFO Candidates (10):**

- 3 strong fits (scores 4.0-4.5)
- 4 moderate fits (scores 3.0-3.9)
- 3 weak fits (scores 2.0-2.9)

**CTO Candidates (10):**

- 3 strong fits (scores 4.0-4.5)
- 4 moderate fits (scores 3.0-3.9)
- 3 weak fits (scores 2.0-2.9)

**Diversity:**

- Mix of guild members and network connections
- Range of company stages (Series A to Public)
- Various sectors (B2B SaaS, Consumer, Fintech, etc.)
- Geographic diversity (US-focused, some international)

**Edge Cases:**

- 2-3 candidates who look very similar on paper but differ in key dimensions
- 1-2 candidates with incomplete LinkedIn profiles (test research limitations)
- 1 candidate with potential red flags (short tenures, unclear gaps)

### Job Descriptions

**See data/job_descriptions/ for full text**

Each JD should include:

- Company context and stage
- Role overview and key responsibilities
- Required experience and qualifications
- Nice-to-have qualifications
- What makes this role unique

---

*End of Technical Specifications v2*
