# WB Case Working Doc

> Document for planning and developing case study response and demo for FirstMark (FMC)
Version: 0.1

## Background

### Case

#### The Context

FirstMark's network includes:

- Portfolio company executives
- Members of FirstMark Guilds (role-based peer groups: CTO, CPO, CRO, etc.)
- Broader professional networks (LinkedIn, founders, event attendees)

We want to identify which executives in this extended network could be strong candidates for open roles in our portfolio companies — and surface those insights automatically.

---

#### The Challenge

You are designing an AI-powered agent that helps a VC talent team proactively surface **executive matches** for open roles across the portfolio.

Build and demonstrate (conceptually and technically) how this "Talent Signal Agent" could:

1. Integrate data from **structured** (e.g., company + role data, hiring needs) and **unstructured** (e.g., bios, articles, LinkedIn text) sources.
2. Identify and rank potential candidates for given open CTO and CFO roles.
3. Provide a clear **reasoning trail** or explanation for its matches.

Create and use **mock data** (CSV, sample bios, job descriptions, etc.), **public data**, or **synthetic examples** to create your structured and unstructured inputs. The goal is to demonstrate reasoning, architecture, and usability — not data volume. Aka should be enough individual CFO/CTO entries to show the how. This exercise mirrors the real data and decision challenges we face. We don't need a perfect working prototype nor perfect data — we want to see how you think, structure, and communicate a solution.

---

#### The Data Inputs

| Type | Example | Description |
|------|---------|-------------|
| **Structured data** | "Mock_Guilds.csv" of mock data of two FirstMark Guilds | Columns: company, role title, location, seniority, function. |
| **Structured data** | "Exec_Network.csv", could be an example of a Partner's connections to fill out additional potential candidates | Columns: name, current title, company, role type (CTO, CRO, etc.), location, LinkedIn URL. |
| **Unstructured data** | Executive bios or press snippets | ~10–20 bios (mock or real) in text format. |
| **Unstructured data** | Job descriptions | Text of 3–5 open portfolio roles for CFO and CTO. |

---

#### Deliverable

##### 1. A short write-up or slide deck (1–2 pages)

- Overview of problem framing and agent design
- Description of data sources and architecture
- Key design decisions and tradeoffs
- How they'd extend this in production

##### 2. A lightweight prototype (Python / LangChain / LlamaIndex / etc or other relevant tools/workspaces that facilitate agent creation.)

Demonstrate how the agent:

- Ingests mock structured + unstructured data
- Identifies potential matches
- Outputs ranked recommendations with reasoning (e.g., "Jane Doe → strong fit for CFO @ AcmeCo because of prior Series B fundraising experience at consumer startup")

##### 3. A brief README or Loom video (optional)

- Explain what's implemented and what's conceptual.

#### Case Assessment

WHO: Beth Viner, Shilpa Nayyar, Matt Turck, Adam Nelson (optional)
WHEN: 5 PM 11/19
Details: 1 Hour presentation - 15 minute intro about me; 30 minute presentation of case and demn; 15 minute Q&A

##### Rubric

| Category                    | Weight | What "Excellent" Looks Like                                  |
| --------------------------- | ------ | ------------------------------------------------------------ |
| **Product Thinking**        | 25%    | Clear understanding of VC and talent workflows. Scopes an agent that actually fits how the firm works. Communicates assumptions and value. |
| **Technical Design**        | 25%    | Uses modern LLM/agent frameworks logically; modular design; thoughtful about retrieval, context, and prompting. |
| **Data Integration**        | 20%    | Handles structured + unstructured data elegantly (e.g., vector store, metadata joins). Sensible about what's automatable. |
| **Insight Generation**      | 20%    | Produces useful, explainable, ranked outputs — not just text dumps. Demonstrates reasoning or scoring logic. |
| **Communication & Clarity** | 10%    | Clean, clear explanation of what was done, why, and next steps. No jargon for the sake of it. |

### WB Case Notes

**Key Requirements:**

- Needs to match the candidate
- Roles - CFO and CTO
- Ability to Diagnose/investigate 'match'

**Core Items**

- Ingest, Match, Explain

---

## TRACKING

High Priority

- [ ] design generate mock data
  - [ ] Mock_Guilds.csv
  - [ ] Exec_Network.csv
  - [ ] | Executive bios
  - [ ] Job descriptions
- [ ] design and generate data schemas
  - [ ] Inputs
  - [ ] Storage
  - [ ] outputs
- [ ]  Standup db
- [ ] design and generate key framework elements
  - [ ] role spec
  - [ ] candidate profile
  - [ ] assessment/match score
- [ ] design and generate prompts
- [ ] Identify platform
  - [ ] Agno or lang chain/graph
  - [ ] firecrawl
  - [ ]

Mid Priority

- [ ] Apollo API schema and logistics

Optional

- [ ] Review the existing company finder skill
- [ ] Note - Tamar Yehoshua is fslack on one page

## Notes & Planning

### Reference items

<https://github.com/lastmile-ai/mcp-agent/tree/main/src/mcp_agent/workflows/deep_orchestrator>
<https://github.com/FrancyJGLisboa/agent-skill-creator>

**DeepREsearch APIS**

- EXA
- FIRECRAWL
- OEPNAI
- Perplexity
- <https://parallel.ai/>
- <https://deeplookup.com/welcome/>
- <https://brightdata.com/products/web-scraper>

- <https://huggingface.co/Alibaba-NLP/Tongyi-DeepResearch-30B-A3B>
  - <https://github.com/Alibaba-NLP/DeepResearch>
- Provider SHowcase - <https://medium.com/@leucopsis/open-source-deep-research-ai-assistants-157462a59c14>

**Deep Research Agent Examples**

<https://github.com/Arindam200/awesome-ai-apps/tree/main/advance_ai_agents/deep_researcher_agent>

<https://github.com/Arindam200/awesome-ai-apps/tree/main/advance_ai_agents/candidate_analyser>

Tools
https://github.com/Alibaba-NLP/DeepResearch

<https://huggingface.co/spaces?q=Web&sort=likes>

<https://anotherwrapper.com/open-deep-research>

<https://github.com/camel-ai/camel>

### Response Notes & Planning

#### Response Guiding Principles

- Emphasize the quality of thinking
- Make basic assumptions, and err on the side of KISS where possible
- Demo must be functional

#### **Components of response**

##### Intro

- How I think about attacking transformation in venture
  - How we would ideally get to this use case
    - Expected ROI
  - part of process
    - What do you want
    - Do we do it <-- Epected roi
    - How do we do it
    - How do we know we are on track
  - Generally loooking for
    - portfolio value - business + tech
  - What i do know is that there are countless things i dont know
    - there will be nuances that matter
    - there will be failure and bumps
  - i dont really know
    - current what is, project frequency, relative trade
    - how are oyu using affinity?

- The biggest determining factors  will be
  - Understanding the what is - what are current systems like, where does data live, what does it look like - and the why!
  - Paying all my sponsors - investors, coo, platform
  - While trying to make headway on foundation
  - Organizational dynamics
    - who do i need to convert
    - who do i need to accomodate
  - understanding fmc
    - how do you invest
    - what are your frustrations, hills you will die on, ideas
  
##### The Case

- The business context
  - Differentiation helps, have guild, use it
  - Case of thing that is done many times in peoples minds in different ways --> Get value from rationalizing and augmenting
  - People evaluation is a fundamental pillar of vc, especialyl early stage

- The Requirements and Components
  - Recall over precision
    - Rather not miss a great match vs see some dudes

  - The goal is not to make the decision, it's to filter and focus review
    - Needs to sufficiently filter who is reviewed
    - needs to inform review of an individual (pop key info, enable quick action)
    - needs to enable investigation

  - The target is augmentation, not replacement
  - The goal is to
    - Validate the quality of research methods
    - Validate the quality of the evaluation and traces
    - Cut operational cost
    - Optimize execution time

  - Our future cases for extension are
    - Other people enrichment and research use cases - founders, lps, hires
    - Applications could be current and or retroactive

- The key complexity points and decisions
  - boundaries
    - What parts of this are central and universal
      - EG. Person intake and normalization

    - What parts of this are standard practices beyond this use case
      - Is enrichment on all People?
      - What is the cadence of

    - what do we keep+Maintain vs Keep+ Redo vs toss
      - Do we try to define refresh process?

  - Where do we need LLM
  - What is the balance of enabling vs confining the llm
  - How we guardrail LLM
  - How do we optimize human engagement?
  - Where do we build vs buy?
    - and where start from scratch vs leverage existing methods
  - Know messy corners
    - titles will be non-normalized
    - there will be a need for disambiguation
    - This happens to often to be centralized

##### Approach Context

Top-level approach breakdown to show thinking and contextualize the demo

- Distinction and articulation of

  - Ideal solution - What this would look like in an ideal state, both in terms of this feature and the surrounding ecosystem
    - Some centralization exists or is incorporated into it
    - Would be modular to lift and shift new methods and capabiliteis and use elsewhere
    - Model Agnostic
  - MVP Solution - If asked to develop my first cut of this for use and evaluation, what would It would look like
    - Actual ROI discussion and roadmapping
    - Some standard framework (but def just some )
    - Ideally leveraging central tools
    - Post real market research (timeboxed) of at least providers
    - Option for consensus
    - With Anthropic

  - Demo Solution - The demo I think, is illustrative in 2 days

##### My Demo method

- What I know about fmc
  - I Know you use airtable
  - I Know when i ask about data, you dont say a lot
  - i know that i need to demonstrate value quick
    - Add functionality, get buy in, inform the roadmap
  - I know that i need to start by meeting you where you are
    - adding to you stack needs critical mass and value
    - Ryan is adding value but no one is using it
    - can build the beautiful thing, but without cred, its not going to get used
  - We have to prototype quick to get to value

- My process and decisions
  - Bets
    - I can meet you in airtable
    - OpenaI deepresearch is a sufficient base when paired with subagents
  - Trades
    - Cheap - GPT for basic llm usage, Fake apollo
- How the process led to demo
- demo

##### Demo

**The Setup:**

- Portco Roles: Have list of portco roles (company, role, optional note)
- Open Role: CFO for Series B SaaS company preparing for growth stage
- Candidate Pool: 8 executives (mix of Guild members, network connections)
- The Challenge: 3 look similar on paper; AI must surface differentiating signals

**The Story Arc:**

1. Role spec gets generated/refined
2. Candidates get researched (show 2-3 in depth)
3. Ranking emerges with reasoning trails
4. User can "drill down" into why #1 beat #2

**Success Metric:** Evaluators should say "I'd actually use this ranking"
LOGISTICAL NOTE

- demo will be run live on my computer
- we will need to have a pre-run example for the research section with full audit trails that i can walk them through

#### Talking Points (Items to cover in response)

Ultimate design depends on Time, Value, and security concerns

- Security is a firm-level decision and its needs to be clear

Distinguish demo from other scenarios

- Ideal would already have x, and would approach by doing y
- MVP Would have x, woudl spend more time to do

We are creating frameworks to help gudie LLM and standardize and compound what we do

The ideal model for FirstMArk AI path is a guild

- There are forward-deployed development use cases
- centralized foundation and standards building

In ideal and MVP, Would start by identifying what solutions are in the market.

- Are there solutions that can perform this e2e
  - cost, performance
- are there solutions that can perform parts
  - EG enrichment - Apollo, People dat labs
  - Candidate AI Eval
  - Networking Matching
- what are the development options
  - General python Frameworks & LLM frameworks (Idealy firm standard)
  - Research approaches
    - research as api
    - open source approaches
    - custom

Decision to skip candidate profile

- There is a world where we have a standardardized set of informaiotn that we collect, synthesize and maintain for certain people
  - trade is always keep all data just in case, and not reinvesnting the full wheel vs data storage problems
  - I dont think its mission critical
  - I think we can do it as an extension if we want

### Case Parts

Tech

- People data ingestion
  - Take in CSVs
  - normalize the headers and add to db
- People Info Enricher
  - Quick LLM-based search to enrich titles
- People researcher
  - OpenAI deep research API done via prompt template

- Role spec generator
- Candidate Evaluator
- Report generation

Response

- thinking and perspective
- Defining the problem
- The solution generation process
- the solution (demo)
  - How it works
  - What it does and doesn't address

### Future State notes

#### TIER 1: Target Production System (12-18 month vision)

**DATA PLATFORM (NO BUILD, JUST DESCRIBE)**
**Scope:** Enterprise-grade talent intelligence platform
Ideally, have centralized and universal foundation

- TLDR: Rationalized Schema, Central Storage, Standard Operation and orchestration

- Centralized data platform (Affinity integration, immutable event log)
- Real-time enrichment (Apollo, Harmonic) for people and companies as necessary
- Standardized LLM Web search
- Foundational Artifact pieces (Role spec, Assessment method)

IN an ideal scenario, data ingestion and storage is a distinct evergreen component of the broader system

- There is a central table storing core information for all use cases
  - Including people, roles (title + company), companies, relationships
  - Also Canonical title mapping table and mechanism
- There are standardized ETL pipelines for ingestion
  - Extract, Normalize, Reconcile Entity (Person, Company, etc) with existing data and appends new records
- Ideally, the system is immutable
  - ability only to add new records and identify and relate active items
- The system will have a parallel operations storage system
  - standardized logging of all events
- There are standardized operations that can be run on records that are also ever green
  - including enriching people/companies via  Apollo
  - that return  the raw enrichment request response, the cleaned response content, and the enrichement data
  - enrich the record
  - store enrichment results, betfore and after
- When new people need to be added, they are imported, cleaned, mapped
  - Where mapping is unclear, HITL loop

Platform would also include

- Storage and maintenence process for open roles (maybe jsut active searches)

Ideal/Target design open questions:

- would we decompose down to role name table?
- how handle location? is both person and role based, and subsject to change
- Can we use affinity as Central source of people truth? what does affinity design look like

#### TIER 2: MVP for Hypothesis Validation (1-month sprint)

**Scope:** Prove value before infrastructure investment

- use whatever apis you have - harmonic, apollo, etc
- Stanadrd Python frameowrks
- Standard LLM Framework (ADK maybe?)
- Research via
  - External Provider(s)
  - In-house agent (either via framework or full custom build)
- Would store content from all cited items
- Would want better investigation capability

#### Future Ideas to potentially cover

- Mock interview
- generalized enrichment
- Historical Role analysis ( profileing, fit estimate)

#### Future questions

- What does affinity api look like? What is data schema like?
- what is current hygiene
- who are biggest slackers
- What does apollo api look like?
- WOuld addfinity be ideal source of truth?
- Where and how is guild managed now?

## Tech Design

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
    - OpenAI Deep research API + ability to do incremental search
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

- Demo DB platform
  - Local sqlite or supabase
  - Airtable
  - DECISION: AIRTABLE

- Data schema
  - People will always have linked in associated with them

- What does the mock data look like?
  - totally fake
  - some reality

- Airtable
  - DB & UI features quickly
  - Meet them in their stack
  - Requirements
    - Ability to kickoff workflow from airtable
    - Ability to use Python for Data ops and Agent work

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
  - Data Edge cases
    - Non-normalized names, field names
    - bios just one text file

- Do we skip creating profile and jsut have bespoke research anchored on spec for now?
  - I think yes and can say "probably takes some more refinement on what a profile is, if we keep standardized profiles or auto-gen when create new person (of x y z type)

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
