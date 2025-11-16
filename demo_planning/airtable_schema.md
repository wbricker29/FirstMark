# Airtable Schema Design - Talent Signal Agent Demo

> Complete field definitions, relationships, and setup instructions for the demo Airtable base

**Last Updated:** 2025-01-16
**Status:** Ready for Implementation
**Design Principles:** KISS, YAGNI, MVP-focused

---

## Table of Contents

1. [Overview](#overview)
2. [Table Schemas](#table-schemas)
3. [JSON Field Schemas](#json-field-schemas)
4. [Relationships Diagram](#relationships-diagram)
5. [Setup Instructions](#setup-instructions)
6. [Pre-Population Checklist](#pre-population-checklist)

---

## Overview

### Design Summary

**Total Tables:** 9
**Total Pre-populated Records:** ~110
**Primary Workflow Table:** Screens (Module 4)
**Key Design Pattern:** JSON storage for complex nested data

### Key Simplifications

1. **JSON Storage:** Store complex Pydantic outputs as JSON in Long Text fields (vs creating many linked tables)
2. **Pre-population:** Manually create Modules 1-3 data (skip CSV upload webhook for v1.0)
3. **Status Triggers:** Use status field changes to trigger automations (vs buttons)
4. **Minimal Tables:** 9 tables only (excluded: Company, Title_Taxonomy, Candidate_Profiles)

### Version Scope

**v1.0 (Demo - 48 hour constraint):**
- Module 2: New Open Role (Airtable-only, pre-populated)
- Module 3: New Search (Airtable-only, pre-populated)
- Module 4: New Screen (Python webhook workflow) ⭐ PRIMARY FOCUS

**v1.1 (Post-Demo Enhancements):**
- Module 1: CSV Upload (webhook endpoint for bulk data ingestion)
- Startup Taxonomy Classification (4-letter DNA codes for portcos)
- Enhanced portco enrichment with sector/stage/business model tags

---

## Table Schemas

### 1. People

**Purpose:** Store all executives/candidates from guildmember_scrape.csv

**Record Count:** 64 (pre-populated)

| Field Name | Field Type | Configuration | Required | Notes |
|------------|-----------|---------------|----------|-------|
| `person_id` | Auto-number | - | ✓ | Primary key |
| `full_name` | Single Line Text | - | ✓ | From CSV: full_name |
| `current_title` | Single Line Text | - | ✓ | From CSV: title_raw |
| `current_company` | Single Line Text | - | ✓ | From CSV: company |
| `linkedin_headline` | Long Text | - | ○ | From CSV: misc_liheadline |
| `linkedin_url` | URL | - | ○ | **Not in CSV - add placeholder pattern** |
| `source` | Single Select | Options below | ✓ | From CSV: source |

**Source Options:**
- FMLinkedIN
- FMGuildPage
- FMCFO
- FMCTOSummit
- FMFounder
- FMProduct

**LinkedIn URL Pattern (for records without real URLs):**
```
https://linkedin.com/in/[first-last-name-slug]
```

**Sample Record:**
```
person_id: 1
full_name: Jonathan Carr
current_title: CFO
current_company: Armis
linkedin_headline: Chief Financial Officer at Armis Security
linkedin_url: https://linkedin.com/in/jonathan-carr
source: FMCFO
```

---

### 2. Portco

**Purpose:** Store portfolio companies for demo scenarios

**Record Count:** 4 (pre-populated)

| Field Name | Field Type | Configuration | Required | Notes |
|------------|-----------|---------------|----------|-------|
| `portco_id` | Auto-number | - | ✓ | Primary key |
| `company_name` | Single Line Text | - | ✓ | Company name |
| `stage` | Single Select | Options below | ✓ | Funding stage |
| `sector` | Single Select | Options below | ✓ | Industry sector |
| `description` | Long Text | - | ○ | Company context |

**Stage Options:**
- Seed
- Series A
- Series B
- Series C
- Growth
- Public

**Sector Options:**
- B2B SaaS
- Consumer
- Fintech
- AI/ML
- Data Infrastructure
- Healthcare
- Enterprise Software
- Developer Tools

**Sample Records:**
```
1. Pigment - Series B, B2B SaaS, "Enterprise planning platform"
2. Mockingbird - Series A, Consumer, "DTC physical products"
3. Synthesia - Series C, AI/ML, "AI video generation platform"
4. Estuary - Series A, Data Infrastructure, "Real-time data pipelines"
```

---

### 3. Portco_Roles

**Purpose:** Store open roles at portfolio companies

**Record Count:** 4 (pre-populated)

| Field Name | Field Type | Configuration | Required | Notes |
|------------|-----------|---------------|----------|-------|
| `role_id` | Auto-number | - | ✓ | Primary key |
| `portco` | Link to Portco | Single link | ✓ | Portfolio company |
| `role_type` | Single Select | Options below | ✓ | Executive function |
| `role_title` | Single Line Text | - | ✓ | Official role title |
| `status` | Single Select | Options below | ✓ | Role status |
| `description` | Long Text | - | ○ | Role context |

**Role Type Options:**
- CFO
- CTO
- CPO
- CRO
- COO
- CMO

**Status Options:**
- Open
- Filled
- On Hold
- Cancelled

**Sample Records:**
```
1. Portco: Pigment, Role: CFO, Title: "Chief Financial Officer", Status: Open
2. Portco: Mockingbird, Role: CFO, Title: "Chief Financial Officer", Status: Open
3. Portco: Synthesia, Role: CTO, Title: "Chief Technology Officer", Status: Open
4. Portco: Estuary, Role: CTO, Title: "Chief Technology Officer", Status: Open
```

---

### 4. Role_Specs

**Purpose:** Store role evaluation specifications (templates + customized)

**Record Count:** 6 (pre-populated: 2 templates + 4 customized)

| Field Name | Field Type | Configuration | Required | Notes |
|------------|-----------|---------------|----------|-------|
| `spec_id` | Auto-number | - | ✓ | Primary key |
| `spec_name` | Single Line Text | - | ✓ | Descriptive name |
| `base_role_type` | Single Select | CFO, CTO, CPO, etc. | ✓ | Base role function |
| `company_stage` | Single Select | Same as Portco.stage | ○ | Target company stage |
| `sector` | Single Select | Same as Portco.sector | ○ | Target sector |
| `is_template` | Checkbox | - | ✓ | True for base templates |
| `structured_spec_markdown` | Long Text | Markdown format | ✓ | Full spec content |
| `search_instructions` | Long Text | - | ○ | Additional AI guidance |
| `created_date` | Created Time | Auto-populated | - | Auto |
| `last_modified` | Last Modified Time | Auto-populated | - | Auto |

**Spec Structure (in `structured_spec_markdown`):**

See `role_spec_design.md` for complete format. Key sections:
- Role Overview
- Must-Haves (hard requirements)
- Evaluation Dimensions (4-6 weighted dimensions)
  - Dimension name
  - Weight (percentage)
  - Evidence Level (High/Medium/Low)
  - Scale definition (1-5 with `None/null` for Unknown / Insufficient Evidence)
- Nice-to-Haves
- Red Flags

**Sample Records:**
```
1. spec_name: "CFO Template", base_role_type: CFO, is_template: true
2. spec_name: "CTO Template", base_role_type: CTO, is_template: true
3. spec_name: "Pigment CFO - Series B SaaS", base_role_type: CFO, is_template: false
4. spec_name: "Mockingbird CFO - Consumer DTC", base_role_type: CFO, is_template: false
5. spec_name: "Synthesia CTO - AI/ML Scale", base_role_type: CTO, is_template: false
6. spec_name: "Estuary CTO - Data Infrastructure", base_role_type: CTO, is_template: false
```

---

### 5. Searches

**Purpose:** Link roles to specs and track active talent searches

**Record Count:** 4 (pre-populated)

| Field Name | Field Type | Configuration | Required | Notes |
|------------|-----------|---------------|----------|-------|
| `search_id` | Auto-number | - | ✓ | Primary key |
| `search_name` | Single Line Text | - | ✓ | Descriptive name |
| `role` | Link to Portco_Roles | Single link | ✓ | Open role |
| `role_spec` | Link to Role_Specs | Single link | ✓ | Evaluation spec |
| `custom_instructions` | Long Text | - | ○ | Additional AI guidance |
| `status` | Single Select | Options below | ✓ | Search status |
| `created_date` | Created Time | Auto-populated | - | Auto |

**Status Options:**
- Draft
- Active
- On Hold
- Closed

**Sample Records:**
```
1. search_name: "Pigment CFO Search", role: [Pigment CFO], spec: [Pigment CFO Spec], status: Active
2. search_name: "Mockingbird CFO Search", role: [Mockingbird CFO], spec: [Mockingbird CFO Spec], status: Active
3. search_name: "Synthesia CTO Search", role: [Synthesia CTO], spec: [Synthesia CTO Spec], status: Active
4. search_name: "Estuary CTO Search", role: [Estuary CTO], spec: [Estuary CTO Spec], status: Active
```

---

### 6. Screens ⭐ **PRIMARY MODULE 4 TABLE**

**Purpose:** Trigger and track candidate screening runs (webhook trigger table)

**Record Count:** 4 (3 complete pre-run + 1 draft for live demo)

| Field Name | Field Type | Configuration | Required | Notes |
|------------|-----------|---------------|----------|-------|
| `screen_id` | Auto-number | - | ✓ | Primary key |
| `screen_name` | Single Line Text | - | ✓ | Descriptive name |
| `search` | Link to Searches | Single link | ✓ | Active search |
| `candidates` | Link to People | Multiple links | ✓ | Candidates to screen |
| `status` | Single Select | **Options below** | ✓ | **Webhook trigger field** |
| `results_summary` | Long Text | - | ○ | High-level summary |
| `created_date` | Created Time | Auto-populated | - | Auto |

**Status Options (CRITICAL - drives automation):**
- `Draft` - Initial state when created
- `Ready to Screen` - **WEBHOOK TRIGGER** (status change → automation fires)
- `Processing` - Python sets during execution
- `Complete` - Python sets when done
- `Failed` - Python sets on error

**Automation Trigger:**
```
When: Screen.status changes to "Ready to Screen"
Action: Send webhook to Flask /screen endpoint
Payload: {screen_id: <record_id>}
```

**Sample Records:**
```
1. Pigment CFO - Batch 1, Search: [Pigment CFO], Candidates: [3 people], Status: Complete
2. Mockingbird CFO - Batch 1, Search: [Mockingbird CFO], Candidates: [4 people], Status: Complete
3. Synthesia CTO - Batch 1, Search: [Synthesia CTO], Candidates: [5 people], Status: Complete
4. Estuary CTO - Live Demo, Search: [Estuary CTO], Candidates: [2-3 people], Status: Draft
```

---

### 7. Workflows

**Purpose:** Store execution logs and audit trail for each candidate-screen pair

**Record Count:** ~12-15 (one per candidate per screen for pre-run scenarios)

| Field Name | Field Type | Configuration | Required | Notes |
|------------|-----------|---------------|----------|-------|
| `workflow_id` | Auto-number | - | ✓ | Primary key |
| `screen` | Link to Screens | Single link | ✓ | Parent screen |
| `candidate` | Link to People | Single link | ✓ | Candidate being evaluated |
| `status` | Single Select | Options below | ✓ | Execution status |
| `research_started` | Date & Time | Include time | ○ | Research phase start |
| `research_completed` | Date & Time | Include time | ○ | Research phase end |
| `assessment_started` | Date & Time | Include time | ○ | Assessment phase start |
| `assessment_completed` | Date & Time | Include time | ○ | Assessment phase end |
| `execution_log` | Long Text | JSON format | ○ | Event stream log |
| `error_message` | Long Text | - | ○ | Error details if failed |

**Status Options:**
- Queued
- Research
- Assessment
- Complete
- Failed

**Execution Log Format (JSON):**
```json
[
  {"timestamp": "2025-01-16T10:30:00Z", "event": "workflow_started", "message": "Starting screening for John Doe"},
  {"timestamp": "2025-01-16T10:30:05Z", "event": "research_started", "message": "Running Deep Research API"},
  {"timestamp": "2025-01-16T10:33:45Z", "event": "tool_call", "tool": "web_search", "query": "John Doe CFO Acme Corp"},
  {"timestamp": "2025-01-16T10:35:00Z", "event": "research_completed", "message": "Research complete with 12 citations"},
  {"timestamp": "2025-01-16T10:35:05Z", "event": "assessment_started", "message": "Running assessment against spec"},
  {"timestamp": "2025-01-16T10:36:30Z", "event": "assessment_completed", "message": "Assessment complete - score: 78/100"},
  {"timestamp": "2025-01-16T10:36:35Z", "event": "workflow_completed", "message": "Screening complete"}
]
```

---

### 8. Research_Results

**Purpose:** Store structured research output from the research pipeline (Deep Research + parser or fast web-search)

**Record Count:** ~12-15 (one per candidate for pre-run scenarios)

| Field Name | Field Type | Configuration | Required | Notes |
|------------|-----------|---------------|----------|-------|
| `research_id` | Auto-number | - | ✓ | Primary key |
| `workflow` | Link to Workflows | Single link | ✓ | Parent workflow |
| `candidate` | Link to People | Single link | ✓ | Research subject |
| `research_summary` | Long Text | - | ✓ | Text summary |
| `research_json` | Long Text | **JSON format** | ✓ | Full ExecutiveResearchResult |
| `citations` | Long Text | **JSON array** | ○ | Citation objects |
| `research_confidence` | Single Select | High/Medium/Low | ✓ | Overall confidence |
| `research_gaps` | Long Text | **JSON array** | ○ | Missing information |
| `research_timestamp` | Date & Time | Include time | ✓ | When research ran |
| `research_model` | Single Line Text | - | ✓ | Upstream research model (e.g., "o4-mini-deep-research" or "gpt-5+web_search") |

**Key Design:** Store full Pydantic `ExecutiveResearchResult` (produced by the parser agent, not Deep Research directly) as JSON in `research_json` field

**See JSON Field Schemas section below for detailed structure**

---

### 9. Assessments ⭐ **KEY OUTPUT TABLE**

**Purpose:** Store assessment results with dimension-level scores and reasoning

**Record Count:** ~12-15 (one per candidate for pre-run scenarios)

| Field Name | Field Type | Configuration | Required | Notes |
|------------|-----------|---------------|----------|-------|
| `assessment_id` | Auto-number | - | ✓ | Primary key |
| `workflow` | Link to Workflows | Single link | ✓ | Parent workflow |
| `candidate` | Link to People | Single link | ✓ | Candidate evaluated |
| `role` | Link to Portco_Roles | Single link | ✓ | Role being evaluated for |
| `role_spec` | Link to Role_Specs | Single link | ✓ | Spec used |
| `overall_score` | Number | 0-100, allow negatives: NO, precision: 1 | ○ | **Nullable** - null if no scoreable dimensions |
| `overall_confidence` | Single Select | High/Medium/Low | ✓ | Combined confidence |
| `dimension_scores_json` | Long Text | **JSON array** | ✓ | DimensionScore objects |
| `must_haves_check_json` | Long Text | **JSON array** | ○ | MustHaveCheck objects |
| `red_flags` | Long Text | **JSON array** | ○ | Red flag strings |
| `green_flags` | Long Text | **JSON array** | ○ | Green flag strings |
| `summary` | Long Text | - | ✓ | 2-3 sentence assessment |
| `counterfactuals` | Long Text | **JSON array** | ○ | "What would change the recommendation" |
| `raw_assessment_json` | Long Text | **JSON format** | ○ | Full AssessmentResult (debugging) |
| `assessment_timestamp` | Date & Time | Include time | ✓ | When assessment ran |
| `assessment_model` | Single Line Text | - | ✓ | Model used (e.g., "gpt-5-mini") |

**Key Design:**
- Store dimension scores as JSON array (not individual records)
- `overall_score` is nullable (null when no dimensions could be scored)
- Evidence-aware: dimension scores can be null for "insufficient evidence"

**See JSON Field Schemas section below for detailed structure**

---

## JSON Field Schemas

> **Note:** These JSON examples show the serialized form of Pydantic models defined
> in `demo_planning/data_design.md` (Structured Output Schemas section). The parser
> agent (`gpt-5-mini` or `gpt-5`) produces these by processing Deep Research markdown
> + citations (or fast web search results).

### ExecutiveResearchResult (Research_Results.research_json)

**Python Pydantic Model → JSON Storage**

```json
{
  "exec_name": "Jonathan Carr",
  "current_role": "CFO",
  "current_company": "Armis",
  "career_timeline": [
    {
      "company": "Armis",
      "role": "Chief Financial Officer",
      "start_date": "2020-01",
      "end_date": null,
      "key_achievements": [
        "Led Series D fundraising ($200M)",
        "Scaled finance team from 5 to 30"
      ]
    },
    {
      "company": "Previous Corp",
      "role": "VP Finance",
      "start_date": "2015-06",
      "end_date": "2019-12",
      "key_achievements": ["IPO preparation", "Built FP&A function"]
    }
  ],
  "total_years_experience": 15,
  "fundraising_experience": "Led 3 major funding rounds totaling $350M, including Series C ($100M) and Series D ($200M). Managed investor relations across 20+ institutional investors.",
  "operational_finance_experience": "Built and scaled finance operations at two high-growth SaaS companies. Implemented NetSuite and Adaptive Planning systems.",
  "technical_leadership_experience": null,
  "team_building_experience": "Grew finance team from 5 to 30, hired VP FP&A and VP Controller. Known for developing talent.",
  "sector_expertise": ["B2B SaaS", "Cybersecurity", "Enterprise Software"],
  "stage_exposure": ["Series A", "Series B", "Series C", "Series D", "Pre-IPO"],
  "research_summary": "Experienced CFO with strong fundraising track record and operational finance expertise in high-growth B2B SaaS. Deep experience in Series B through pre-IPO stages.",
  "key_achievements": [
    "Led $200M Series D round at Armis",
    "Scaled finance operations at two unicorns",
    "Built financial systems for IPO readiness"
  ],
  "notable_companies": ["Armis", "Previous Corp"],
  "citations": [
    {
      "url": "https://techcrunch.com/armis-series-d",
      "title": "Armis raises $200M Series D",
      "snippet": "CFO Jonathan Carr led the fundraising process...",
      "relevance_note": "Primary source for fundraising experience"
    },
    {
      "url": "https://linkedin.com/in/jonathan-carr",
      "title": "Jonathan Carr - LinkedIn Profile",
      "snippet": "Chief Financial Officer at Armis. Previously VP Finance...",
      "relevance_note": "Career timeline and achievements"
    }
  ],
  "research_timestamp": "2025-01-16T10:35:00Z",
  "research_model": "o4-mini-deep-research"
}
```

**Field Mapping:**
- Store entire JSON object in `Research_Results.research_json` (Long Text)
- Extract `citations` array to separate field for easier display
- Extract `research_summary` to dedicated field for quick viewing

> Canonical Pydantic definition for `ExecutiveResearchResult` lives in `demo_planning/data_design.md` under "Structured Output Schemas".

---

### DimensionScore (Assessments.dimension_scores_json)

**Evidence-Aware Scoring with null Support**

```json
[
  {
    "dimension": "Fundraising & Investor Relations",
    "score": 4,
    "evidence_level": "High",
    "confidence": "High",
    "reasoning": "Led 3 major funding rounds totaling $350M across Series C and D. Strong track record with institutional investors. Public evidence of successful fundraising at Armis ($200M Series D).",
    "evidence_quotes": [
      "Led Series D fundraising ($200M) at Armis",
      "Managed investor relations across 20+ institutional investors"
    ],
    "citation_urls": [
      "https://techcrunch.com/armis-series-d",
      "https://linkedin.com/in/jonathan-carr"
    ]
  },
  {
    "dimension": "Operational Finance & Systems",
    "score": 4,
    "evidence_level": "Medium",
    "confidence": "Medium",
    "reasoning": "Implemented NetSuite and Adaptive Planning systems. Built FP&A function at previous company. Scaled finance team from 5 to 30, indicating operational depth.",
    "evidence_quotes": [
      "Implemented NetSuite and Adaptive Planning systems",
      "Scaled finance team from 5 to 30"
    ],
    "citation_urls": ["https://linkedin.com/in/jonathan-carr"]
  },
  {
    "dimension": "Strategic Business Partnership",
    "score": null,
    "evidence_level": "Low",
    "confidence": "Low",
    "reasoning": "No public evidence of strategic partnership capabilities beyond standard CFO investor relations. This dimension is difficult to assess from public data.",
    "evidence_quotes": [],
    "citation_urls": []
  },
  {
    "dimension": "Culture & Leadership",
    "score": 3,
    "evidence_level": "Low",
    "confidence": "Medium",
    "reasoning": "Known for developing talent and grew team significantly. However, limited public evidence on specific leadership style or cultural contributions. Score based on team-building track record.",
    "evidence_quotes": [
      "Known for developing talent",
      "Hired VP FP&A and VP Controller"
    ],
    "citation_urls": ["https://linkedin.com/in/jonathan-carr"]
  },
  {
    "dimension": "Stage & Sector Fit",
    "score": 5,
    "evidence_level": "High",
    "confidence": "High",
    "reasoning": "Perfect fit for Series B SaaS role. Deep experience in B2B SaaS across Series A through pre-IPO stages. Current role at Armis (cybersecurity SaaS) directly relevant.",
    "evidence_quotes": [
      "Series A through Pre-IPO experience",
      "B2B SaaS and Enterprise Software expertise"
    ],
    "citation_urls": ["https://linkedin.com/in/jonathan-carr"]
  },
  {
    "dimension": "Team Building & Talent Development",
    "score": 4,
    "evidence_level": "Medium",
    "confidence": "High",
    "reasoning": "Strong evidence of building and scaling teams. Grew finance org from 5 to 30. Made key hires (VP FP&A, VP Controller). Known for talent development.",
    "evidence_quotes": [
      "Grew finance team from 5 to 30",
      "Hired VP FP&A and VP Controller",
      "Known for developing talent"
    ],
    "citation_urls": ["https://linkedin.com/in/jonathan-carr"]
  }
]
```

**Critical Evidence-Aware Pattern:**
- `score: null` (not 0, not NaN, not empty) = "Insufficient Evidence"
- Allows dimensions to be explicitly unscored when public data is thin
- Overall score calculation ignores/down-weights null dimensions

> Canonical Pydantic definitions for `DimensionScore`, `AssessmentResult`, and related models live in `demo_planning/data_design.md` under "Structured Output Schemas".

---

### MustHaveCheck (Assessments.must_haves_check_json)

```json
[
  {
    "requirement": "5+ years CFO or VP Finance experience",
    "met": true,
    "evidence": "15 years total experience, CFO at Armis since 2020, VP Finance 2015-2019"
  },
  {
    "requirement": "Series B+ fundraising experience",
    "met": true,
    "evidence": "Led Series C ($100M) and Series D ($200M) rounds at Armis"
  },
  {
    "requirement": "B2B SaaS sector experience",
    "met": true,
    "evidence": "Current CFO at B2B SaaS company (Armis), previous experience in enterprise software"
  }
]
```

---

### Citations (Research_Results.citations)

```json
[
  {
    "url": "https://techcrunch.com/2023/04/armis-series-d-200m",
    "title": "Armis Security Raises $200M Series D",
    "snippet": "Cybersecurity platform Armis announced today a $200M Series D round led by General Catalyst. CFO Jonathan Carr led the fundraising process and managed relationships with investors.",
    "relevance_note": "Primary source for fundraising experience and investor relations capabilities"
  },
  {
    "url": "https://www.linkedin.com/in/jonathan-carr-cfo",
    "title": "Jonathan Carr - Chief Financial Officer at Armis",
    "snippet": "Chief Financial Officer at Armis Security. Previously VP Finance at Previous Corp where I led IPO preparation and built the FP&A function. Expertise in high-growth B2B SaaS.",
    "relevance_note": "Career timeline, role responsibilities, and self-described expertise areas"
  },
  {
    "url": "https://www.builtinsf.com/company/armis/jobs",
    "title": "Armis Career Page - Finance Team",
    "snippet": "Our finance team, led by CFO Jonathan Carr, has grown from 5 to 30 people in 3 years. We're hiring across FP&A, Accounting, and Strategic Finance.",
    "relevance_note": "Evidence of team-building and organizational scaling"
  }
]
```

---

### Full AssessmentResult (Assessments.raw_assessment_json)

**Complete Pydantic model output for debugging**

```json
{
  "overall_score": 78.0,
  "overall_confidence": "High",
  "dimension_scores": [...],
  "must_haves_check": [...],
  "red_flags_detected": [],
  "green_flags": [
    "Strong fundraising track record at scale ($350M+)",
    "Sector expertise perfectly aligned (B2B SaaS)",
    "Team building demonstrated (5 to 30 person org)"
  ],
  "summary": "Strong candidate with excellent fundraising experience and operational finance depth. Perfect sector fit for B2B SaaS. Some uncertainty on strategic partnership capabilities due to limited public evidence.",
  "counterfactuals": [
    "If candidate had more public evidence of board-level strategic partnerships, score would increase to 85+",
    "Lack of international finance experience could be limiting factor for global expansion stage",
    "Assessment assumes fundraising track record translates to Series B context (vs later-stage only)"
  ],
  "assessment_timestamp": "2025-01-16T10:36:30Z",
  "assessment_model": "gpt-5-mini",
  "role_spec_used": "Pigment CFO - Series B SaaS"
}
```

---

## Relationships Diagram

```
Portco (4)
  ├─→ Portco_Roles (4) [1:many]

Role_Specs (6)

Searches (4)
  ├─→ Portco_Roles (linked) [many:1]
  └─→ Role_Specs (linked) [many:1]

People (64)

Screens (4) ⭐ WEBHOOK TRIGGER
  ├─→ Searches (linked) [many:1]
  └─→ People (linked) [many:many]

Workflows (12-15) - created by Python
  ├─→ Screens (linked) [many:1]
  └─→ People (linked) [many:1]

Research_Results (12-15) - created by Python
  ├─→ Workflows (linked) [1:1]
  └─→ People (linked) [many:1]

Assessments (12-15) - created by Python ⭐ OUTPUT
  ├─→ Workflows (linked) [1:1]
  ├─→ People (linked) [many:1]
  ├─→ Portco_Roles (linked) [many:1]
  └─→ Role_Specs (linked) [many:1]
```

**Key Relationships:**
- **Screen → Candidates (People):** Many-to-many (one screen evaluates multiple candidates)
- **Workflow → Candidate:** Many-to-one (multiple workflows per candidate across different screens)
- **Assessment → Role & Spec:** Many-to-one (candidate can be evaluated for multiple roles)

---

## Setup Instructions

### Phase 1: Create Base Structure (2 hours)

**Step 1: Create New Airtable Base**
1. Create new base: "FirstMark Talent Signal Agent Demo"
2. Delete default tables

**Step 2: Create All 9 Tables**
1. Create tables in this order (to handle dependencies):
   - People
   - Portco
   - Portco_Roles
   - Role_Specs
   - Searches
   - Screens
   - Workflows
   - Research_Results
   - Assessments

**Step 3: Add Fields to Each Table**
- Follow field definitions in Table Schemas section above
- Pay special attention to:
  - **Link fields:** Must create both tables first
  - **Single Select options:** Add all options listed
  - **Number field precision:** Set to 1 decimal place for overall_score
  - **Date fields:** Enable time for all timestamp fields

### Phase 2: Load People Data (1 hour)

**Step 1: Prepare CSV**
1. Open `reference/guildmember_scrape.csv`
2. Add `linkedin_url` column with placeholder URLs:
   ```
   https://linkedin.com/in/[first-name]-[last-name]
   ```
3. Map columns:
   - `full_name` → full_name
   - `title_raw` → current_title
   - `company` → current_company
   - `misc_liheadline` → linkedin_headline
   - `source` → source

**Step 2: Import to Airtable**
1. Go to People table
2. Click "..." → Import data → CSV file
3. Map columns to fields
4. Verify 64 records imported

**Step 3: Validate Data**
- Check for duplicates (by full_name)
- Ensure all required fields populated
- Fix any LinkedIn URL formatting issues

### Phase 3: Create Demo Scenarios (3 hours)

**Step 1: Create Portco Records (15 min)**
```
1. Pigment
   - Stage: Series B
   - Sector: B2B SaaS
   - Description: "Enterprise planning and FP&A platform for CFOs"

2. Mockingbird
   - Stage: Series A
   - Sector: Consumer
   - Description: "Direct-to-consumer physical products brand"

3. Synthesia
   - Stage: Series C
   - Sector: AI/ML
   - Description: "AI video generation platform for enterprises"

4. Estuary
   - Stage: Series A
   - Sector: Data Infrastructure
   - Description: "Real-time data pipeline and CDC platform"
```

**Step 2: Create Portco_Roles (15 min)**
```
1. Pigment CFO
   - Portco: [Link to Pigment]
   - Role Type: CFO
   - Role Title: "Chief Financial Officer"
   - Status: Open

2. Mockingbird CFO
   - Portco: [Link to Mockingbird]
   - Role Type: CFO
   - Role Title: "Chief Financial Officer"
   - Status: Open

3. Synthesia CTO
   - Portco: [Link to Synthesia]
   - Role Type: CTO
   - Role Title: "Chief Technology Officer"
   - Status: Open

4. Estuary CTO
   - Portco: [Link to Estuary]
   - Role Type: CTO
   - Role Title: "Chief Technology Officer"
   - Status: Open
```

**Step 3: Create Role Specs (2 hours)**

See `role_spec_design.md` for complete markdown templates.

1. **CFO Template** (is_template: true)
   - Copy markdown template from role_spec_design.md
   - Paste into `structured_spec_markdown` field

2. **CTO Template** (is_template: true)
   - Copy markdown template from role_spec_design.md
   - Paste into `structured_spec_markdown` field

3. **Pigment CFO Spec** (customize from CFO template)
   - Emphasize: International finance, SaaS metrics, enterprise sales support
   - Adjust dimension weights for Series B SaaS context

4. **Mockingbird CFO Spec** (customize from CFO template)
   - Emphasize: DTC finance, inventory management, unit economics
   - Add consumer-specific dimensions

5. **Synthesia CTO Spec** (customize from CTO template)
   - Emphasize: AI/ML infrastructure, model serving, scale challenges
   - Add AI-specific technical dimensions

6. **Estuary CTO Spec** (customize from CTO template)
   - Emphasize: Data infrastructure, open source, developer tools
   - Add data engineering specific dimensions

**Step 4: Create Searches (15 min)**
```
1. Pigment CFO Search
   - Search Name: "Pigment CFO Search"
   - Role: [Link to Pigment CFO]
   - Role Spec: [Link to Pigment CFO Spec]
   - Status: Active

2. Mockingbird CFO Search
   - Search Name: "Mockingbird CFO Search"
   - Role: [Link to Mockingbird CFO]
   - Role Spec: [Link to Mockingbird CFO Spec]
   - Status: Active

3. Synthesia CTO Search
   - Search Name: "Synthesia CTO Search"
   - Role: [Link to Synthesia CTO]
   - Role Spec: [Link to Synthesia CTO Spec]
   - Status: Active

4. Estuary CTO Search
   - Search Name: "Estuary CTO Search"
   - Role: [Link to Estuary CTO]
   - Role Spec: [Link to Estuary CTO Spec]
   - Status: Active
```

**Step 5: Create Screen Records (15 min)**

**Pre-run Scenarios (will have data):**
```
1. Pigment CFO - Batch 1
   - Search: [Link to Pigment CFO Search]
   - Candidates: [Select 3-4 CFOs from People table]
   - Status: Draft (will change to Complete after running Python)

2. Mockingbird CFO - Batch 1
   - Search: [Link to Mockingbird CFO Search]
   - Candidates: [Select 3-4 different CFOs]
   - Status: Draft

3. Synthesia CTO - Batch 1
   - Search: [Link to Synthesia CTO Search]
   - Candidates: [Select 4-5 CTOs from People table]
   - Status: Draft
```

**Live Demo Scenario:**
```
4. Estuary CTO - Live Demo
   - Search: [Link to Estuary CTO Search]
   - Candidates: [Select 2-3 CTOs] (keep this small for demo timing)
   - Status: Draft
```

### Phase 4: Configure Webhook Automation (1 hour)

**Step 1: Set Up ngrok (local tunnel)**
```bash
# Start Flask server first (on port 5000)
python webhook_server.py

# In separate terminal, start ngrok
ngrok http 5000

# Copy the HTTPS URL (e.g., https://abc123.ngrok.io)
```

**Step 2: Create Airtable Automation**
1. In Airtable base, click "Automations" (top right)
2. Click "Create automation"
3. Name: "Trigger Screening Workflow"

**Step 3: Configure Trigger**
1. Trigger Type: "When record matches conditions"
2. Table: Screens
3. Conditions:
   - When: `status` → is → "Ready to Screen"
4. Test trigger (should show screens in Draft status)

**Step 4: Configure Action**
1. Action Type: "Send webhook"
2. URL: `https://[your-ngrok-url]/screen`
3. Method: POST
4. Headers:
   - Content-Type: application/json
5. Body (JSON):
   ```json
   {
     "screen_id": "{{AIRTABLE_RECORD_ID}}"
   }
   ```
6. Test action (should return 200 OK when Flask server is running)

**Step 5: Enable Automation**
- Turn automation ON
- Test by changing a Screen status to "Ready to Screen"
- Check Flask terminal for webhook received log

### Phase 5: Run Pre-Run Scenarios (4 hours)

**Prerequisites:**
- Python environment set up (see technical_spec.md)
- OpenAI API key configured
- Flask server running
- ngrok tunnel active
- Airtable automation enabled

**Execution:**
1. Change Pigment CFO screen status → "Ready to Screen"
2. Wait for completion (~3-6 minutes per candidate with Deep Research)
3. Verify results populated in Workflows, Research_Results, Assessments tables
4. Repeat for Mockingbird CFO screen
5. Repeat for Synthesia CTO screen

**Expected Runtime:**
- Deep Research mode: 3-6 min per candidate
- 3-4 candidates per screen × 3 screens = ~30-60 minutes total
- Plus Python processing time, Airtable writes

**Fallback (if time-constrained):**
- Use Web Search mode instead (set `USE_DEEP_RESEARCH=false`)
- Runtime: 1-2 min per candidate = ~10-20 minutes total

---

## Pre-Population Checklist

### Core Data (Must Complete Before Demo)

- [ ] **People Table:** 64 executives loaded from guildmember_scrape.csv
  - [ ] LinkedIn URLs added (placeholder pattern OK)
  - [ ] All required fields populated
  - [ ] No duplicate records

- [ ] **Portco Table:** 4 companies created
  - [ ] Pigment (Series B, B2B SaaS)
  - [ ] Mockingbird (Series A, Consumer)
  - [ ] Synthesia (Series C, AI/ML)
  - [ ] Estuary (Series A, Data Infrastructure)

- [ ] **Portco_Roles Table:** 4 roles created
  - [ ] Pigment CFO (Open)
  - [ ] Mockingbird CFO (Open)
  - [ ] Synthesia CTO (Open)
  - [ ] Estuary CTO (Open)

- [ ] **Role_Specs Table:** 6 specs created
  - [ ] CFO Template (is_template: true)
  - [ ] CTO Template (is_template: true)
  - [ ] Pigment CFO Spec (customized)
  - [ ] Mockingbird CFO Spec (customized)
  - [ ] Synthesia CTO Spec (customized)
  - [ ] Estuary CTO Spec (customized)

- [ ] **Searches Table:** 4 searches created
  - [ ] Pigment CFO Search (Active)
  - [ ] Mockingbird CFO Search (Active)
  - [ ] Synthesia CTO Search (Active)
  - [ ] Estuary CTO Search (Active)

- [ ] **Screens Table:** 4 screens created
  - [ ] Pigment CFO - Batch 1 (3-4 candidates, Status: Draft)
  - [ ] Mockingbird CFO - Batch 1 (3-4 candidates, Status: Draft)
  - [ ] Synthesia CTO - Batch 1 (4-5 candidates, Status: Draft)
  - [ ] Estuary CTO - Live Demo (2-3 candidates, Status: Draft)

### Automation & Infrastructure

- [ ] **ngrok:** Tunnel running, HTTPS URL copied
- [ ] **Flask Server:** Running on localhost:5000, accepting webhooks
- [ ] **Airtable Automation:** Created, tested, enabled
- [ ] **OpenAI API:** Key configured, credits available
- [ ] **Environment Variables:** All required vars set (API keys, Airtable credentials)

### Pre-Run Execution (Generate Demo Data)

- [ ] **Pigment CFO Screening:** Completed, results in database
  - [ ] Workflows records created (1 per candidate)
  - [ ] Research_Results populated
  - [ ] Assessments populated
  - [ ] Screen status: Complete

- [ ] **Mockingbird CFO Screening:** Completed, results in database
  - [ ] Workflows records created
  - [ ] Research_Results populated
  - [ ] Assessments populated
  - [ ] Screen status: Complete

- [ ] **Synthesia CTO Screening:** Completed, results in database
  - [ ] Workflows records created
  - [ ] Research_Results populated
  - [ ] Assessments populated
  - [ ] Screen status: Complete

- [ ] **Estuary CTO Screen:** Ready for live demo
  - [ ] Candidates selected and linked
  - [ ] Status: Draft (do NOT run yet)
  - [ ] Will execute live during demo

### Validation

- [ ] **Data Quality:** All JSON fields properly formatted
- [ ] **Relationships:** All links between tables working correctly
- [ ] **Scoring:** Evidence-aware scores (with null values) displaying correctly
- [ ] **Ranking:** Candidates ranked by overall_score in Assessments table
- [ ] **Citations:** URLs and quotes properly stored and accessible
- [ ] **Audit Trail:** Workflow logs readable and complete

---

## Quick Reference: Field Types Summary

| Airtable Field Type | Use Cases | Example Fields |
|--------------------|-----------|----------------|
| Auto-number | Primary keys | person_id, screen_id, workflow_id |
| Single Line Text | Short text | full_name, current_title, company_name |
| Long Text | Multi-line text, JSON | research_summary, dimension_scores_json |
| URL | Web links | linkedin_url, citation URLs |
| Single Select | Dropdown | status, confidence, role_type |
| Checkbox | Boolean | is_template |
| Number | Numeric values | overall_score (0-100) |
| Link to Record | Relationships | portco, role, candidate |
| Date & Time | Timestamps | created_date, research_timestamp |
| Created Time | Auto timestamp | created_date (auto) |
| Last Modified | Auto timestamp | last_modified (auto) |

---

## Notes & Gotchas

### Evidence-Aware Scoring
- **CRITICAL:** Use `null` in JSON (not 0, not NaN, not empty string) for unknown scores
- Python: `score: Optional[int] = None`
- JSON: `"score": null`
- Display: Use Airtable formula to show "Insufficient Evidence" when null

### JSON Storage Best Practices
1. **Format JSON:** Use proper formatting in Long Text fields (indent with 2 spaces)
2. **Validate:** Test JSON parsing before storing in production
3. **Size Limits:** Airtable Long Text max is 100,000 characters (should be plenty)
4. **Display:** Consider creating formula fields to extract key JSON values for quick viewing

### Webhook Timing
- **ngrok Stability:** Free tier times out after 2 hours - may need to restart and update automation URL
- **Airtable Delays:** 1-2 second delay between status change and webhook trigger
- **Python Processing:** Update Screen status to "Processing" immediately to prevent re-triggering

### Demo Day Readiness
1. **Pre-start ngrok:** Start tunnel before demo to get stable URL
2. **Test automation:** Trigger one test screen 30 min before demo
3. **Have backup:** Keep pre-run results ready if live demo fails
4. **Monitor logs:** Have Flask terminal visible to show real-time progress

---

## v1.1 Enhancements (Post-Demo)

### Module 1: CSV Upload Webhook

**Purpose:** Automate bulk data ingestion for executives, companies, and roles

**Implementation:**
- Flask `/upload` endpoint
- File type detection (people, company, portco)
- Data cleaning and normalization
- Deduplication logic
- Bulk Airtable writes
- Status reporting

**Estimated Time:** 4-6 hours

### Startup Taxonomy Classification

**Purpose:** Enrich portfolio companies with standardized 4-letter DNA codes

**Taxonomy Structure (from `startup_tax.md`):**
- **Business Model** (1 letter): B2B, B2C, D2C, B2B2C, B2G, C2C
- **Product Type** (1 letter): Software, Marketplace, Hardware, E-commerce/Physical, Services, Content/Media
- **Industry Cluster** (1 letter): Financial Services, Healthcare, Commerce, Media, Enterprise Productivity, Developer/Infrastructure, Consumer Services, Industrial, Sustainability, Horizontal
- **Monetization** (1 letter): Subscription, Transaction %, Fixed Fee, One-time, Usage-based, Advertising

**Example Classifications:**
- Shopify: **BSPS** (B2B-Software-Enterprise Productivity-Subscription)
- Pinterest: **CMMA** (Consumer-Marketplace-Media-Advertising)
- Synthesia: **BSPS** (B2B-Software-Enterprise Productivity-Subscription)

**Schema Changes Needed:**

Add to **Portco** table:
- `business_model` (Single Select): B2B, B2C, D2C, B2B2C, B2G, C2C
- `product_type` (Single Select): Software, Marketplace, Hardware, E-commerce, Services, Content
- `industry_cluster` (Single Select): Financial Services, Healthcare, Commerce, etc.
- `monetization` (Single Select): Subscription, Transaction, Fixed Fee, One-time, Usage, Advertising
- `dna_code` (Formula): Concatenates first letters → "BSPS"
- `dna_secondary` (Long Text, optional): Secondary tags when applicable (≥25% revenue influence)

**Enrichment Approach:**

**Option 1: Manual Classification** (4-6 hours for 190 portcos)
- Review company descriptions from CSV
- Classify each dimension
- Enter into Airtable

**Option 2: LLM-Assisted Batch Classification** (1-2 hours)
- Extract company descriptions from `fmc_portco_export.csv`
- Use GPT-4 with structured output to classify all 190 companies
- Taxonomy provided as system context
- Human review for ambiguous cases
- Bulk import to Airtable

**Option 3: Hybrid with Web Research** (2-3 hours)
- Use company descriptions as primary source
- Fetch websites with `crawl4ai` skill for unclear cases
- LLM classification with web context
- High accuracy, moderate time

**Feasibility Assessment:**

Using available skills and tools:

✅ **Easy** - LLM-assisted batch classification (Option 2)
- CSV already has rich company descriptions
- Most companies have clear business models (e.g., Shopify = obvious B2B software subscription)
- Structured output ensures consistent format
- Can process all 190 companies in single API call or batches

✅ **Medium** - Hybrid with selective web research (Option 3)
- Use `crawl4ai` skill for ~20-30 ambiguous cases
- Most companies are well-documented
- FirstMark portfolio = high-profile companies with good online presence

**Recommended Approach:**

```python
# Pseudocode for v1.1 enrichment script

import pandas as pd
from openai import OpenAI
from pydantic import BaseModel

class StartupTaxonomy(BaseModel):
    company: str
    business_model: str  # B2B, B2C, etc.
    product_type: str  # Software, Marketplace, etc.
    industry_cluster: str  # Financial Services, Healthcare, etc.
    monetization: str  # Subscription, Transaction %, etc.
    dna_code: str  # Computed 4-letter code
    confidence: str  # High, Medium, Low
    reasoning: str  # Brief explanation

# Load portfolio CSV
portcos = pd.read_csv('fmc_portco_export.csv')

# Batch classify using GPT-4
for batch in batches(portcos, size=10):
    classifications = classify_startups(
        companies=batch,
        taxonomy=STARTUP_TAXONOMY,
        model="gpt-4"
    )

    # Write to Airtable
    write_to_airtable(classifications)

# Human review for low-confidence cases
review_ambiguous_cases()
```

**Estimated Time:**
- Script development: 2 hours
- Batch classification: 30 minutes
- Human review: 1 hour
- **Total: ~3.5 hours for 190 companies**

**Value:**
- Enables better matching (e.g., "Find B2B SaaS CFOs for B2B SaaS portcos")
- Searchable by business model, product type, monetization
- Consistent categorization across portfolio
- Foundation for analytics and insights

**Sample Output:**
```
Shopify: BSPS
  - B2B (sells to merchants)
  - Software (SaaS platform)
  - Enterprise Productivity (commerce tools)
  - Subscription (monthly pricing)

Airbnb: XMST
  - B2B2C (platform connecting hosts to guests)
  - Marketplace (two-sided network)
  - Consumer Services (travel/lodging)
  - Transaction % (take rate on bookings)

Synthesia: BSPS
  - B2B (sells to enterprises)
  - Software (SaaS video platform)
  - Enterprise Productivity (AI video creation)
  - Subscription (monthly/annual plans)
```

---

## Next Steps After Schema Setup

1. **Implement Python webhook server** (`webhook_server.py`)
2. **Create Pydantic models** matching JSON schemas
3. **Implement research agent** (Deep Research + Web Search modes)
4. **Implement assessment agent** (spec-guided evaluation)
5. **Write Airtable integration** (read screens, write results)
6. **Test end-to-end flow** with one candidate
7. **Run pre-run scenarios** (3 screens)
8. **Create demo views/interfaces** in Airtable (optional)
9. **Prepare presentation materials**

**Estimated Total Setup Time:** ~14 hours (Airtable) + ~20 hours (Python) = **34 hours total**

---

**Document Version:** 1.0
**Last Updated:** 2025-01-16
**Status:** Ready for Implementation
