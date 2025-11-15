# WB Case Working Doc

## Organization



High Priority

- [ ] 
- [ ] design and generate data components
- [ ] design and generate key framework elements
- [ ] generate fake data

Mid Priority

- [ ] Apollo API schema and logistics

Optional

- [ ] Review the existing company finder skill

# Background

## Case Brief Breakdown

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

| Category | Weight | What "Excellent" Looks Like |
|----------|--------|----------------------------|
| **Product Thinking** | 25% | Clear understanding of VC and talent workflows. Scopes an agent that actually fits how the firm works. Communicates assumptions and value. |
| **Technical Design** | 25% | Uses modern LLM/agent frameworks logically; modular design; thoughtful about retrieval, context, and prompting. |
| **Data Integration** | 20% | Handles structured + unstructured data elegantly (e.g., vector store, metadata joins). Sensible about what's automatable. |
| **Insight Generation** | 20% | Produces useful, explainable, ranked outputs — not just text dumps. Demonstrates reasoning or scoring logic. |
| **Communication & Clarity** | 10% | Clean, clear explanation of what was done, why, and next steps. No jargon for the sake of it. |

---



# Notes & Planning

## Reference items

https://github.com/lastmile-ai/mcp-agent/tree/main/src/mcp_agent/workflows/deep_orchestrator
https://github.com/FrancyJGLisboa/agent-skill-creator
## Response Notes

**Components of response**

- Distinction and articulation of 
  - Ideal solution - What this would look like in an ideal state, both in terms of this feature and surrounding ecosystem
  - MVP Solution - If asked to develop my first cut of this for use and evaluation, what would It would look like
  - Demo Solution - The demo I think is illustrative in 2 days



**In general**

- Emphasize the quality of thinking
- Make basic assumptions, and err on the side of KISS where possible



Points to hit

- Depends on Time, Value,  security concerns
- 



### Case Parts

Tech

- People data ingestion 
- People Info Enricher
- People researcher
- Role spec generator
- Candidate Evaluator
- Report generation

### 

## Thoughts and ideas

### Notes

DeepREsearch APIS

- EXA
- FIRECRAWL
- OEPNAI
- Perplexity
- https://parallel.ai/
- https://deeplookup.com/welcome/
- https://brightdata.com/products/web-scraper

- https://huggingface.co/Alibaba-NLP/Tongyi-DeepResearch-30B-A3B
  - https://github.com/Alibaba-NLP/DeepResearch
-  Provider SHowcase - https://medium.com/@leucopsis/open-source-deep-research-ai-assistants-157462a59c14

Deep Research Agent Examples

https://github.com/Arindam200/awesome-ai-apps/tree/main/advance_ai_agents/deep_researcher_agent

https://github.com/Arindam200/awesome-ai-apps/tree/main/advance_ai_agents/candidate_analyser



Tools

https://anotherwrapper.com/open-deep-research

### Idea - Target Infrastructure



While we will include ingestion of data in our case study response, the response should also note that, in an ideal world, we would have a central firm storage platform where this would happen independently:

- IN an ideal scenario, data ingestion and storage is a distinct evergreen component of the broader system
  - There is a central table storing core information for all use cases
    - Including people, roles (title + company), companies, relationships
    - Also Canonical title mapping table and mechanism
    - 
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
    - 

> **QUESTIONS**

> - would we decompose down to role name table?
> - how handle location? is both person and role based, and subsject to change
> - Can we use affinity as Central source of people truth? what does affinity design look like



### real mvp

use whatever apis you have - harmonic, apollo, etc

A2a



# Planning

## Key Decisions 

### Open

- Use more than just Deepresearch api?
- Use LLM or code or both for ingestion?
- How to decompose key LLM responsibilties
  - research
  - enrichment
  - assessment
  - reporting
- UI or not?
- IF agent, what framework?
- What is right level of granularity to express ideal state of db?
- What is differernt about the db 
- What are the easiest portfolio companies to use as examples?
  - 



## Tech Design Planning

### Artifacts

#### Inputs

| Type | Example | Description |
|------|---------|-------------|
| **Structured data** | "Mock_Guilds.csv" of mock data of two FirstMark Guilds | Columns: company, role title, location, seniority, function. |
| **Structured data** | "Exec_Network.csv", could be an example of a Partner's connections to fill out additional potential candidates | Columns: name, current title, company, role type (CTO, CRO, etc.), location, LinkedIn URL. |
| **Unstructured data** | Executive bios or press snippets | ~10–20 bios (mock or real) in text format. |
| **Unstructured data** | Job descriptions | Text of 3–5 open portfolio roles for CFO and CTO. |



#### Output

(Maybe via Vis)

- Assessment results Overview
- Individual assessment results
  - Result Scorecard
  - Result Justification
  - Indovodial component drill down of some type

### Gates

- Data Ingestion and Normalization
- Enrichment
- Frameworks
  - Role
  - Candidate
  - Assessment
- Presentation

### Components

**General**

- Standardized Entity Storage
- Standardized operations definition and orchestration

 **Person Components**

- Person Ingestion & Normalization (Centralized Platform)
- Person Enrichment
- Person Researcher
  - Web and API researcher
  - Research Synthesis Storage
  - Research Run Log
  - Research Source Storage ( at a min )

**Portco Components**

- Standardized storage of portco information, including characteristics
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
- 
