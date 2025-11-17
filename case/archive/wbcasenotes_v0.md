# WB Case Working Doc

V0

## Background

### Case Brief Breakdown

### WB Case Notes

**Key Requirements:**

- Needs to match the candidate
- Roles - CFO and CTO
- Ability to Diagnose/investigate 'match'

**Core Item**

- Ingest, Match, Explain

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

##### Rubric

| Category                    | Weight | What "Excellent" Looks Like                                  |
| --------------------------- | ------ | ------------------------------------------------------------ |
| **Product Thinking**        | 25%    | Clear understanding of VC and talent workflows. Scopes an agent that actually fits how the firm works. Communicates assumptions and value. |
| **Technical Design**        | 25%    | Uses modern LLM/agent frameworks logically; modular design; thoughtful about retrieval, context, and prompting. |
| **Data Integration**        | 20%    | Handles structured + unstructured data elegantly (e.g., vector store, metadata joins). Sensible about what's automatable. |
| **Insight Generation**      | 20%    | Produces useful, explainable, ranked outputs — not just text dumps. Demonstrates reasoning or scoring logic. |
| **Communication & Clarity** | 10%    | Clean, clear explanation of what was done, why, and next steps. No jargon for the sake of it. |

---

## TRACKING

High Priority

- [ ] design and generate data schemas
  - [ ] Inputs
  - [ ] Storage
  - [ ] outputs
- [ ] design and generate key framework elements
  - [ ] role spec
  - [ ] candidate profile
  - [ ] assessment/match score
- [ ] design and generate prompts
- [ ] Identify platform
  - [ ] Agno or lang chain/graph
  - [ ] firecrawl
  - [ ]
- [ ] design generate mock data
  - [ ] Mock_Guilds.csv
  - [ ] Exec_Network.csv
  - [ ] | Executive bios
  - [ ] Job descriptions

Mid Priority

- [ ] Apollo API schema and logistics

Optional

- [ ] Review the existing company finder skill

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

<https://huggingface.co/spaces?q=Web&sort=likes>

<https://anotherwrapper.com/open-deep-research>

<https://github.com/camel-ai/camel>

### Response Notes & Planning

#### Response Guiding Principles

- Emphasize the quality of thinking
- Make basic assumptions, and err on the side of KISS where possible

#### **Components of response**

Intro

- How I think about attacking transformation in venture

The Case

- The Requirements and Components
- The key complexity points and decisions

Top-level approach breakdown to show thinking and contextualize the

- Distinction and articulation of
  - Ideal solution - What this would look like in an ideal state, both in terms of this feature and the surrounding ecosystem
  - MVP Solution - If asked to develop my first cut of this for use and evaluation, what would It would look like
  - Demo Solution - The demo I think, is illustrative in 2 days

Use case

- My process and decisions
- How the process led to demo
- demo

#### Talking Points (Items to cover in response)

Ultimate design depends on Time, Value, and security concerns

- Security is a firm-level decision and its needs to be clear

Distinguish demo from other scenarios

- Ideal would already have x, and would approach by doing y
- MVP Would have x, woudl spend more time to do Y

The ideal model for FirstMArk AI path is a guild

- There are forward-deployed development use cases
- centralized foundation and standards building
-

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

#### Future Ideas to potentially cover

- Mock interview

- generalized enrichment

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
- the solution (demo
  - How it works
  - What it does and doesn't address

##

### Assorted Notes

#### ON target infrastructure

**DATA PLATFORM (NO BUILD, JUST DESCRIBE)**

While we will include ingestion of data in our case study response, the response should also note that, in an ideal world, we would have a central firm storage platform where this would happen independently:

- TLDR: Rationalized Schema, Central Storage, Standard Operation and orchestration

- IN an ideal scenario, data ingestion and storage is a distinct evergreen component of the broader system

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

Ideal/Target design open questions

- would we decompose down to role name table?
- how handle location? is both person and role based, and subsject to change
- Can we use affinity as Central source of people truth? what does affinity design look like

### ON real mvp

use whatever apis you have - harmonic, apollo, etc

A2A as framework most liekl y

## Tech Planning

### Key Decisions

#### Open

- What is research method
  - Open AI Deepresearch API
  - Other deep research API
  - Custom Agentic
- Use LLM or code or both for ingestion?
  - Basic CSV Ingest
- How to decompose key LLM responsibilities
  - research
  - enrichment
  - assessment
  - reporting
- UI or not?
- IF agent, what framework?
  - Agno or lang chain
- What is the right level of granularity to express the ideal state of the DB?
- DB platform
  - Local sqlite or supabase
- What does the mock data look like?
  - totally fake
  - some reality
- Datascraper
  - Bright or firecrawl

#### Made

- mock data
  - real people + maybe fake
  - data will shwo normalization issues (non-standard convventions, names, etc )

- Enrichment tool will be stub
  - Will mock api response data from Apollo

### Artifacts

#### Inputs

| Type                  | Example                                                      | Description                                                  |
| --------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| **Structured data**   | "Mock_Guilds.csv" of mock data of two FirstMark Guilds       | Columns: company, role title, location, seniority, function. |
| **Structured data**   | "Exec_Network.csv", could be an example of a Partner's connections to fill out additional potential candidates | Columns: name, current title, company, role type (CTO, CRO, etc.), location, LinkedIn URL. |
| **Unstructured data** | Executive bios or press snippets                             | ~10–20 bios (mock or real) in text format.                   |
| **Unstructured data** | Job descriptions                                             | Text of 3–5 open portfolio roles for CFO and CTO.            |

#### Output

(Maybe via Vis)

- Assessment results Overview
- Individual assessment results
  - Result Scorecard
  - Result Justification
  - Indovodial component drill down of some type

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

**Role Spec Components**

- Standard Role Spec Components
  - Standardized Role Spec Framework Definition: Components, definitions, requirements, standards for a spec
    - Values, Abilities, Skills, Experience
    - Some idea of grade scale
  - Base Role Specs: a standard spec for a given role
    - Either for a title
    - and or title and company archetype
- Company-specific role spec enricher (can customize standardized )
  - plain text Input job description translator and enricher

  - manual editing capabilities
    -

**Candidate Components**

- Standard Candidate Profile Framework Definition  - Standardized way to describe a candidate for a role
  - Standardized Candidate Profile Definition: Components, definitions, requirements, standards for a spec

**Matching**

- Candidate Assessment Definition - standardized definitions, framework , process for evaluating a candidate
  - The definition encompasses two processes: 1. A general process for human execution, and 2. LLM Agent execution process
  - Output includes
    - topline assessment
    - individual component assessment score and reasoning

> **QUESTIONS**
>
> - Do we want to perform research using synthesized and granular methods?
> - Do we want to store full source citation content?
> - Do we want AI to generate its own non-deterministic grade and pair it with a deterministic hybrid?
> - Does the candidate profile include an assessment or not?

> **OPTIONS**
>
> - Could do an assessment of previous people in the role
>   - Profiling them
>   - input of fit

### Tech Outline

Data Ingestion - Python

- Read CSV
- Normalize titles
- Extract and normalize entities and values

Data Storage (Either Supabase or Sqllite)

- Existing Company Table

### Tech Notes

must have confidence alongside any evaluation

# Other

Note - Tamar Yehoshua is fslack on one page
