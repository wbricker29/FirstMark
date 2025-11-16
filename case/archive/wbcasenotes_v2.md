# WB Case Working Doc v2

> Document for planning and developing case study response and demo for FirstMark (FMC)
> **Note:** For technical design specifications see tech_specs_v2.md

Version: 0.2
Last Updated: 2025-11-16

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
| **Structured data** | "Mock_Guilds.csv" of FirstMark Guild members | Executive profiles with role, company, location, etc. |
| **Structured data** | "Exec_Network.csv" of partner connections | Additional candidate pool from broader network |
| **Unstructured data** | Executive bios or press snippets | ~10–20 bios (mock or real) in text format |
| **Unstructured data** | Job descriptions | Text of 3–5 open portfolio roles for CFO and CTO |

*See tech_specs_v2.md for detailed data schemas*

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

**WHO:** Beth Viner, Shilpa Nayyar, Matt Turck, Adam Nelson (optional)
**WHEN:** 5 PM 11/19/2025
**FORMAT:** 1 Hour presentation - 15 minute intro about me; 30 minute presentation of case and demo; 15 minute Q&A

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

- Match candidates to roles (CTO and CFO focus)
- Provide diagnostic capability to investigate matches
- Demonstrate reasoning trails and explainability

**Core Workflow:**

- Ingest → Match → Explain

**Success Criteria:**

- Evaluators say "I'd actually use this ranking"
- Quality of thinking demonstrated > feature completeness
- Functional demo that shows the approach works

---

## 3-DAY SPRINT PLAN

**Timeline:** Nov 16 (Day 1) → Nov 17 (Day 2) → Nov 18 (Day 3) → Nov 19 (5 PM Presentation)

### Day 1 - Saturday Nov 16: Foundation & Derisking (10 hours)

**Morning (4 hours): Data & Infrastructure**
- [ ] 9-10am: Generate mock data (see tech_specs_v2.md for schemas)
  - Mock_Guilds.csv (15-20 guild members)
  - Exec_Network.csv (additional 10 candidates)
  - 4 job descriptions (2 CFO, 2 CTO roles at specific portcos)
- [ ] 10-11am: Set up Airtable base
  - Create tables: People, Companies, Portcos, Searches, Screens, Workflows
  - Configure fields and relationships
- [ ] 11am-1pm: Build data ingestion script
  - CSV parser and normalizer
  - Airtable upload via pyairtable
  - Test with mock data

**Afternoon (4 hours): Core Research Capability**
- [ ] 2-3pm: Set up Flask webhook server + ngrok
  - Test webhook trigger from Airtable
- [ ] 3-5pm: Build candidate research module
  - OpenAI Deep Research API integration
  - Prompt template for candidate research
  - Test with 2-3 real candidates
- [ ] 5-6pm: Research storage and logging
  - Store research results in Workflow table
  - Create markdown export

**Evening (2 hours): Role Spec Framework**
- [ ] 6-8pm: Design and generate role spec framework
  - Define spec structure (dimensions, weights, scales)
  - Create 2 base specs (CFO, CTO)
  - Generate custom specs for 4 demo roles

**End of Day 1 Checkpoint:**
- ✓ Mock data loaded into Airtable
- ✓ Webhook infrastructure working
- ✓ Research API functional with examples
- ✓ Role specs defined for demo roles

---

### Day 2 - Sunday Nov 17: Core Demo Build (12 hours)

**Morning (4 hours): Assessment Engine**
- [ ] 9-11am: Build candidate assessment module
  - Assessment prompt engineering
  - Structured output for scores + reasoning
  - Integration with role specs
- [ ] 11am-1pm: Test assessment workflow end-to-end
  - Run 5 candidate assessments
  - Review quality of reasoning and scores
  - Iterate on prompts

**Afternoon (4 hours): Full Screening Workflow**
- [ ] 2-4pm: Complete `/screen` endpoint
  - Link Screen → Search → Role → Spec
  - Process multiple candidates
  - Store results in Workflow table
- [ ] 4-6pm: Run full screening for demo
  - Screen 10-15 candidates across 2 roles
  - Generate pre-baked examples with full audit trails
  - Export markdown reports

**Evening (4 hours): UI & Visualization**
- [ ] 6-8pm: Build Airtable interface views
  - Candidate ranking view (sorted by score)
  - Drill-down view (assessment details)
  - Research trail view (citations and reasoning)
- [ ] 8-10pm: Polish and test demo flow
  - Practice triggering screening live
  - Verify all data displays correctly
  - Test fallback scenarios

**End of Day 2 Checkpoint:**
- ✓ Full screening workflow functional
- ✓ Pre-baked examples with complete audit trails
- ✓ Airtable UI ready for demo
- ✓ Can run live screening during presentation

---

### Day 3 - Monday Nov 18: Polish & Presentation (10 hours)

**Morning (4 hours): Presentation Materials**
- [ ] 9-11am: Create presentation deck/document
  - Problem framing (Product Thinking - 25%)
  - Architecture overview (Technical Design - 25%)
  - Data integration approach (Data Integration - 20%)
  - Demo results walkthrough (Insight Generation - 20%)
  - Extension roadmap (Communication - 10%)
- [ ] 11am-1pm: Write demo script
  - Minute-by-minute presentation flow
  - Key talking points for each section
  - Transitions between slides and live demo

**Afternoon (3 hours): Demo Rehearsal & Refinement**
- [ ] 2-3pm: Full demo dry run
  - Time each section
  - Identify rough spots
- [ ] 3-4pm: Refine based on dry run
  - Improve unclear explanations
  - Simplify complex parts
  - Prepare for Q&A scenarios
- [ ] 4-5pm: Second full rehearsal
  - Practice with timer
  - Ensure smooth flow

**Evening (3 hours): Final Preparation**
- [ ] 5-6pm: Prepare fallback materials
  - Screenshots of live demo in case of technical issues
  - Backup pre-recorded segments
  - Printed presentation deck
- [ ] 6-7pm: Final technical checks
  - Test all APIs
  - Verify ngrok tunnel
  - Check Airtable access
- [ ] 7-8pm: Review talking points and Q&A prep
  - Anticipated questions
  - Key messages to reinforce
  - Relax and get ready

**End of Day 3 Checkpoint:**
- ✓ Presentation complete and rehearsed
- ✓ Demo script ready
- ✓ Fallback plan in place
- ✓ Ready for 5 PM presentation

---

## RISK MITIGATION PLAN

### Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| **OpenAI API failure during demo** | Medium | High | Pre-run all examples; have screenshots; can explain from cached results |
| **ngrok tunnel drops** | Low | High | Have backup ngrok account; test 1 hour before; can show pre-baked results if needed |
| **Airtable rate limits** | Low | Medium | Throttle API calls; use pre-loaded data for demo; keep request count low |
| **Research quality poor** | Medium | High | Test with 20+ candidates beforehand; iterate prompts; cherry-pick best examples for demo |
| **Assessment scores don't differentiate** | Medium | High | Manual review of scoring logic; ensure role specs have sufficient detail; test edge cases |

### Demo Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| **Live demo takes too long** | High | Medium | Have pre-run example as primary; live demo as "bonus" if time permits |
| **Results don't look compelling** | Medium | High | Curate candidate pool to include clear differentiators; ensure 3+ candidates look similar on paper but differ in reality |
| **Can't explain reasoning trail** | Low | High | Pre-analyze all assessment outputs; prepare talking points for each dimension; practice drill-down |
| **Questions on scalability** | High | Low | Have Tier 1 / Tier 2 talking points ready; acknowledge demo limitations clearly; focus on thinking quality |

### Presentation Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| **Run over 30 minutes** | High | Medium | Strict time budget per section; practice with timer; identify skippable content |
| **Too technical for audience** | Medium | Medium | Balance technical depth with business context; lead with "why" before "how"; use clear analogies |
| **Miss key rubric categories** | Low | High | Map each presentation section to rubric explicitly; ensure all 5 categories covered |

---

## Response Strategy & Planning

### Response Guiding Principles

1. **Emphasize quality of thinking** - Show how I approach problems, not just what I built
2. **KISS where possible** - Simple solutions that work > complex solutions that might work
3. **Demo must be functional** - Not vapor ware; must actually run
4. **Meet them where they are** - Airtable integration shows understanding of their context
5. **Demonstrate extensibility** - Show how this scales to production

### Components of Response

#### Intro (15 minutes - separate from case presentation)

**Key Messages:**
- How I think about AI transformation in venture capital
- My framework for evaluating and prioritizing AI opportunities
- What I know and what I don't know about FirstMark
- Why I'm excited about this role

**Structure:**
- Background: AI/ML engineering + product experience
- Approach: Portfolio thinking for AI initiatives
  - Quick wins (immediate value)
  - Foundational bets (platform capabilities)
  - Learning experiments (validate assumptions)
- Process framework:
  - What do you want? (Define objectives)
  - Should we do it? (Expected ROI)
  - How do we do it? (Execution plan)
  - How do we know we're on track? (Metrics & iteration)
- Humility: "There are countless things I don't know about FirstMark's context"
  - Current systems, data landscape, organizational dynamics
  - How they invest, what frustrates them, their hills to die on

#### The Case Presentation (30 minutes)

**Minute 0-5: Problem Framing (Product Thinking)**
- The business context: Talent matching is core VC value-add
- FirstMark's unique assets: Guilds provide differentiation
- Current state: Manual, inconsistent, time-intensive
- Opportunity: Rationalize and augment existing process
- Success = augmentation, not replacement

**Minute 5-12: Solution Approach (Technical Design + Data Integration)**
- Three-tier thinking:
  - **Demo Solution:** What I built in 3 days (show pragmatism)
  - **MVP Solution:** What I'd build in 1 month for actual use (show product thinking)
  - **Target Solution:** 12-18 month vision (show strategic thinking)
- Architecture overview:
  - Meet you where you are: Airtable integration
  - Modern AI: OpenAI Deep Research + GPT-5 for assessment
  - Modular design: Components can be swapped/improved
- Data integration:
  - Structured: Guild CSVs, network data
  - Unstructured: Bios, job descriptions, web research
  - Storage: Airtable for demo; future = centralized platform

**Minute 12-23: Demo (Insight Generation)**
- **Setup** (2 min): Show the scenario
  - 4 open roles across portfolio (2 CFO, 2 CTO)
  - 20 candidates from guilds + network
  - Challenge: Surface best matches with reasoning
- **Walkthrough pre-run example** (6 min):
  - Show role spec for specific CFO role
  - Show research trail for 2-3 candidates
  - Show assessment with scores, confidence, reasoning
  - Show ranked list with drill-down capability
  - Highlight: "Why did #1 beat #2?" → Show counterfactuals
- **Live demo** (3 min - if time permits):
  - Trigger new screening in Airtable
  - Show terminal progress
  - Show results populating
- **Key Insights** (2 min):
  - Quality of reasoning trails
  - Confidence levels help prioritize review
  - Counterfactuals aid decision-making

**Minute 23-30: Extension & Next Steps (Communication + All Categories)**
- What works now vs. what's conceptual
- Known limitations and rough edges
- Path to production (Tier 2 → Tier 1)
  - Market research on vendors
  - Centralized data platform
  - Standardized enrichment
  - Model flexibility
- Broader applications:
  - Founder evaluation
  - LP profiling
  - Portfolio analytics
- How we'd measure success
- Open questions that need FirstMark input

#### Talking Points to Cover

**Distinguish Demo from Other Scenarios:**
- "In an ideal world with 18 months and full team, I'd build X"
- "For MVP in 1 month to validate value, I'd do Y"
- "For this 3-day demo to show thinking, I built Z"

**Acknowledge What I Don't Know:**
- Your current data hygiene and systems
- How you currently use Affinity
- Guild management process and cadence
- Security requirements and constraints

**Decision Framework:**
- Ultimate design depends on Time, Value, Security
- Security is firm-level decision (needs clarity upfront)
- Build vs. Buy analysis for each component
- Standard frameworks compound value across use cases

**The FirstMark AI Guild Model:**
- Centralized foundation (data platform, standards, frameworks)
- Forward-deployed development (use-case specific agents)
- Knowledge sharing and iteration across use cases

**Key Complexity Points:**
- Boundaries: What's universal vs. use-case specific?
- LLM scope: Where do we need AI vs. deterministic logic?
- Human engagement: How do we optimize the human-in-loop?
- Messy corners: Non-normalized titles, disambiguation, edge cases

**Decision to Skip Candidate Profiles:**
- Could maintain standardized profiles for certain people
- Trade-off: Data freshness vs. storage/maintenance cost
- Not mission critical for demo
- Can extend if needed based on usage patterns

---

## Demo Design

### The Setup

**Scenario:** FirstMark talent team has 4 open executive roles across portfolio

**Roles:**
1. Pigment (Series B B2B SaaS, enterprise, international) - CFO
2. Mockingbird (Series A Consumer DTC, physical product) - CFO
3. Synthesia (Series C AI/ML SaaS, global scale) - CTO
4. Estuary (Series A Data infrastructure, developer tools) - CTO

**Candidate Pool:**
- 15-20 executives from Guild members + partner networks
- Mix of obviously qualified, edge cases, and clear mismatches
- 3 candidates that look similar on paper but differ in key ways

**The Challenge:**
AI must surface differentiating signals that aren't obvious from titles alone

### The Story Arc

1. **Context Setting** - Show the business problem and current pain
2. **Role Spec** - Demonstrate framework for defining what "good" looks like
3. **Research** - Show depth of candidate investigation (2-3 examples)
4. **Assessment** - Demonstrate scoring logic and reasoning trails
5. **Ranking** - Show ranked output with clear differentiation
6. **Drill-Down** - "Why did #1 beat #2?" → Counterfactual analysis
7. **Investigation** - Show ability to explore assessment reasoning

### Demo Script (Detailed)

**[Minute 12-14: Setup & Context]**
- Screen share Airtable base
- "Here's what we're working with today..."
- Show People table: "20 executives from FirstMark guilds and partner networks"
- Show Portcos table: "4 portfolio companies with open executive roles"
- Show Searches table: "Let's focus on this CFO search for Pigment..."
- **Key talking point:** "Pigment is Series B, B2B SaaS, scaling internationally - they need a CFO who can handle hypergrowth and complex finance ops"

**[Minute 14-16: Role Spec Framework]**
- Open Search detail view, show linked Role Spec
- "This is the role specification framework we've defined..."
- Walk through dimensions:
  - Financial Expertise (weight: 30%) - scale, complexity, domain fit
  - Scaling Experience (weight: 25%) - hypergrowth, stage match
  - International Operations (weight: 20%) - multi-geo, compliance
  - Fundraising (weight: 15%) - later-stage rounds, investor relations
  - Cultural Fit (weight: 10%) - startup DNA, FirstMark network
- Show scale definitions (1-5 for each dimension)
- **Key talking point:** "These specs are customizable - start with template, refine based on hiring manager input"

**[Minute 16-19: Research Trail]**
- Show Workflows table (pre-run examples)
- Open Workflow for Candidate A: "Sarah Chen, CFO at Airtable"
- Show research report:
  - Summary of background
  - 8-10 citations from LinkedIn, press, company blogs
  - Key signals extracted: "Led Airtable through Series D, scaled finance team 5→25, international expansion to EMEA"
- Scroll through Research Markdown export
- **Key talking point:** "The AI is doing deep research we'd normally spend 30 minutes per candidate doing manually"
- Quick peek at 1-2 other candidate research summaries

**[Minute 19-22: Assessment & Reasoning]**
- Open Assessment view for Sarah Chen
- Show structured output:
  ```
  Overall Score: 4.2/5.0
  Confidence: High

  Dimension Scores:
  - Financial Expertise: 4.5/5 (High confidence)
    Reasoning: "Managed complex B2B SaaS unit economics at scale..."
  - Scaling Experience: 4.0/5 (High confidence)
    Reasoning: "Scaled through Series D, 3x revenue growth..."
  - International Operations: 4.5/5 (Medium confidence)
    Reasoning: "Led EMEA expansion, but limited APAC experience..."
  - Fundraising: 4.0/5 (High confidence)
  - Cultural Fit: 3.5/5 (Medium confidence)
  ```
- **Key talking point:** "Notice the confidence levels - helps prioritize where we need human verification"
- Show counterfactuals: "What would make this a 5.0? → Evidence of APAC scaling experience"

**[Minute 22-24: Ranked Results & Differentiation]**
- Switch to Ranked Candidates view
- Show top 5 ranked for Pigment CFO role:
  1. Sarah Chen (4.2/5)
  2. Michael Torres (4.1/5)
  3. Jennifer Wu (3.8/5)
  4. Alex Kumar (3.5/5)
  5. David Park (3.2/5)
- **Key talking point:** "Sarah and Michael look identical on paper - both CFOs at similar stage companies"
- Click into comparison view
- Show differentiator: "Sarah has international experience, Michael has stronger fundraising track record but domestic-only"
- **Key talking point:** "This is where AI adds value - surfaces the nuance"

**[Minute 24-26: Live Demo (if time)]**
- "Let me show you this running live..."
- Create new Screen record
- Link to different Search (CTO role)
- Select 3-4 candidates
- Click "Start Screening" button
- Show terminal output:
  ```
  🔍 Starting screening for CTO @ Synthesia...
  📝 Researching candidate 1/4: Alex Johnson...
  ✅ Research complete (28 citations found)
  🎯 Running assessment...
  ✅ Assessment complete (Score: 3.8/5)
  ```
- "While this runs, let's look at the architecture..."
- Show quick architecture diagram
- Check back: "Results are populating in Airtable now..."

**[Minute 26-28: What Works / What Doesn't]**
- "Let's be clear about what's real and what's conceptual..."
- **What works:**
  - ✅ Data ingestion from CSVs
  - ✅ Deep research via OpenAI API
  - ✅ Structured assessment with reasoning
  - ✅ Ranked output with drill-down
  - ✅ Audit trail and citations
- **What's simplified for demo:**
  - ⚠️ Enrichment is stubbed (would use Apollo in production)
  - ⚠️ Limited error handling
  - ⚠️ No deduplication logic
  - ⚠️ Manual role spec creation (could be AI-assisted)
- **What's conceptual:**
  - 📋 Centralized data platform
  - 📋 Real-time Affinity integration
  - 📋 Historical candidate profiling

**[Minute 28-30: Extension & Questions]**
- Show Tier 2 (MVP) and Tier 1 (Target) slides
- "Here's how this evolves..."
- Tier 2 (1 month): Real enrichment APIs, better UI, production infrastructure
- Tier 1 (12-18 mo): Centralized platform, standardized operations, multi-use case
- "This same approach extends to founder evaluation, LP profiling, portfolio talent mapping..."
- "Questions I need FirstMark input on:"
  - Current Affinity usage and data quality
  - Security requirements and constraints
  - Priority across talent use cases
  - Guild management process
- "I'm ready for your questions..."

---

## Presentation Materials

### Slide Outline (Notion or Google Slides - 8-10 slides)

**Slide 1: Title**
- Talent Signal Agent: AI-Powered Executive Matching for FirstMark
- Will Bricker | Nov 19, 2025

**Slide 2: The Problem**
- Challenge: Match 100+ guild/network executives to portfolio roles
- Current: Manual, time-intensive, inconsistent
- Opportunity: Rationalize and augment with AI
- Success = Better matches, faster, with clear reasoning

**Slide 3: Solution Approach - Three Tiers**
- Demo (3 days): Prove thinking quality and technical approach
- MVP (1 month): Production-ready for hypothesis validation
- Target (12-18 mo): Enterprise talent intelligence platform

**Slide 4: Architecture Overview**
- Data Layer: Airtable (meet you where you are)
- Research Layer: OpenAI Deep Research API
- Assessment Layer: GPT-5 + structured prompting
- Output Layer: Ranked candidates with reasoning trails

**Slide 5: Key Design Decisions**
| Decision | Rationale | Trade-off |
|----------|-----------|-----------|
| Airtable vs. custom DB | Integration with existing stack | Flexibility vs. familiarity |
| OpenAI API vs. custom agent | Speed to value, quality | Cost vs. control |
| Role specs vs. freeform | Standardization, explainability | Flexibility vs. consistency |

**Slide 6: Data Integration**
- Structured: CSVs (guilds, networks) → normalized → Airtable
- Unstructured: Bios, job descriptions → embeddings → research prompts
- Enrichment: LinkedIn, Apollo (stubbed for demo)
- Storage: Airtable + markdown exports

**Slide 7: Demo Results Summary**
- 20 candidates evaluated across 4 roles
- Research: Avg 12 citations per candidate, 2-3 min per deep research
- Assessment: Dimension-level scores, confidence, reasoning, counterfactuals
- Output: Ranked lists with clear differentiation

**Slide 8: Extension Roadmap**
- Near-term (Tier 2 MVP):
  - Real enrichment APIs (Apollo, Harmonic)
  - Affinity integration
  - Production infrastructure
  - Broader candidate pool testing
- Long-term (Tier 1 Target):
  - Centralized data platform
  - Multi-use case (founders, LPs, portfolio analytics)
  - Standardized operations and logging
  - Model flexibility and consensus approaches

**Slide 9: Broader Applications**
- Founder evaluation for new investments
- LP profiling and relationship management
- Portfolio company talent mapping
- Retroactive analysis of successful hires

**Slide 10: Open Questions & Next Steps**
- FirstMark input needed:
  - Current Affinity usage and data schemas
  - Security requirements
  - Priority ranking across talent use cases
  - Guild management process and cadence
- Next steps:
  - Validate approach with real search
  - Build Tier 2 MVP for production testing
  - Expand to additional use cases

---

## Future State Vision

### TIER 1: Target Production System (12-18 month vision)

**Scope:** Enterprise-grade talent intelligence platform

**Core Philosophy:** Rationalized Schema, Central Storage, Standard Operations

#### Data Platform (Foundation)

**Centralized Storage:**
- Central tables for: People, Companies, Roles, Relationships
- Canonical title mapping table and reconciliation mechanism
- Immutable event log (append-only, time-series)
- Operations log for all system events

**ETL Pipelines:**
- Extract from multiple sources (Affinity, CSVs, APIs, manual entry)
- Normalize schemas and field mappings
- Reconcile entities (detect duplicates, merge records)
- Append new records with version tracking

**Standardized Operations:**
- Enrichment: Apollo, Harmonic, LinkedIn for people/companies
- Research: Standardized LLM web search + deep research
- Assessment: Role spec framework + LLM evaluation
- Storage: Raw inputs, processed outputs, intermediate artifacts

**Human-in-the-Loop:**
- Disambiguation workflows for unclear entity matches
- Role spec customization and approval
- Assessment review and override capability

#### Integration Layer

**Affinity Integration:**
- Bi-directional sync: People, companies, relationships
- Event streaming for real-time updates
- Investigate if Affinity can be source of truth vs. parallel system

**API Access:**
- GraphQL API for portfolio companies to query talent data
- Webhooks for real-time notifications
- REST endpoints for standard CRUD operations

#### Use Case Modules

**Talent Matching (this demo):**
- Executive search for portfolio roles
- Automated screening and ranking
- Research trails and assessment reasoning

**Founder Evaluation:**
- Background research and pattern matching
- Track record analysis
- Network mapping

**LP Profiling:**
- Relationship intelligence
- Investment pattern analysis
- Engagement recommendations

**Portfolio Analytics:**
- Talent density mapping across portfolio
- Hiring velocity and quality metrics
- Network effects and relationship graphs

#### Open Questions for Tier 1

- Should we decompose to role name normalization table?
- How to handle location (person-level and role-level, changes over time)?
- Can Affinity serve as central source of truth, or parallel system?
- What's acceptable data latency for different use cases?
- How do we handle data retention and privacy requirements?

---

### TIER 2: MVP for Hypothesis Validation (1-month sprint)

**Scope:** Prove value before infrastructure investment

**Goal:** Production-ready system for real talent matching use cases

#### Technical Stack

**Data & Storage:**
- Airtable or lightweight Postgres database
- Basic deduplication and entity resolution
- Manual data hygiene processes

**APIs & Integrations:**
- Apollo for enrichment (or Harmonic if available)
- OpenAI Deep Research API
- Tavily for incremental search if needed
- Affinity read-only integration (if feasible)

**LLM Framework:**
- Agno or LangGraph for agent orchestration
- GPT-5 for assessment and synthesis
- Structured outputs for all LLM calls

**Infrastructure:**
- Flask + production WSGI server (Gunicorn)
- Cloud hosting (Render, Railway, or similar)
- Proper webhook authentication and rate limiting

#### Features

**Enhanced from Demo:**
- Real enrichment via Apollo API
- Better error handling and retry logic
- Deduplication and entity resolution
- Role spec templates with AI-assisted customization
- Improved UI (Streamlit or Airtable Interface)
- Email notifications for completed screenings
- Export to Google Sheets or Notion

**New Capabilities:**
- Historical candidate profiling (optional)
- Batch processing for large candidate pools
- A/B testing different assessment prompts
- Feedback loop for assessment quality

#### Validation Criteria

**Quantitative:**
- Research quality: 80%+ of citations relevant and accurate
- Assessment accuracy: Human review agrees with AI ranking 70%+ of time
- Time savings: 10x reduction in initial screening time
- Coverage: Can handle 100+ candidates per search

**Qualitative:**
- Talent team actually uses it for real searches
- Hiring managers trust the reasoning and recommendations
- Clear value demonstrated vs. manual process

#### Investment Required

**Time:** 4 weeks (1 engineer full-time)
**Cost:** ~$5K (APIs, hosting, tools)
**Risk:** Low (can validate or kill quickly based on usage)

---

### TIER 3: Demo Solution (What I Built)

**Scope:** 3-day demo to show thinking quality and technical approach

**What's Real:**
- ✅ Data ingestion from CSVs to Airtable
- ✅ Flask webhook server with ngrok tunnel
- ✅ OpenAI Deep Research API integration
- ✅ GPT-5 structured assessment with role specs
- ✅ Ranked output with reasoning trails
- ✅ Audit logging and markdown exports
- ✅ Airtable interface for viewing results

**What's Simplified:**
- ⚠️ Enrichment stubbed (mock Apollo data)
- ⚠️ Limited error handling
- ⚠️ No deduplication logic
- ⚠️ Manual role spec creation
- ⚠️ Small candidate pool (20 people)

**What's Conceptual:**
- 📋 Centralized data platform
- 📋 Affinity integration
- 📋 Historical candidate profiles
- 📋 Multi-use case extensibility
- 📋 Production infrastructure

**Purpose:**
- Demonstrate quality of thinking
- Prove technical approach is sound
- Show understanding of VC talent workflows
- Validate hypothesis that AI can add value

---

## Open Questions & Inputs Needed

### About FirstMark's Current State

- What does your Affinity setup look like? (schema, usage patterns, data quality)
- How do you currently manage guilds? (frequency, data capture, CRM)
- What's your current data hygiene like? (duplicates, outdated info, completeness)
- How do you currently serve materials to portfolio companies?
- Who are the key stakeholders who would need to buy in?

### About Requirements & Constraints

- What are your security requirements? (data handling, API access, audit logs)
- What's the priority across talent use cases? (exec search, founder eval, LP profiling)
- What's your tolerance for AI errors and confidence thresholds?
- Do you have existing API access to enrichment services? (Apollo, Harmonic, etc.)

### About Future Direction

- What's the timeline for AI initiatives? (experimentation vs. production)
- What's the expected ROI and how would you measure it?
- What's your appetite for build vs. buy decisions?
- What would make you say "this is production-ready"?

---

## Notes & Context

### What I Know About FirstMark

**Facts:**
- Use Airtable for various operations
- Have active guild system (competitive advantage)
- Data quality is a known challenge ("their data is crap")
- Ryan is building things but adoption is unclear

**Assumptions:**
- Need to demonstrate quick value to build credibility
- Meeting them in their stack (Airtable) reduces friction
- Prototype-first approach aligns with startup mentality
- Quality of thinking matters more than polish

**What I Don't Know:**
- Current systems and where data lives
- Project frequency and relative priorities
- How they use Affinity day-to-day
- Organizational dynamics and decision-makers

### Success Factors

**For the Role:**
- Understanding the "what is" - current systems, data, workflows
- Paying all stakeholders - investors, COO, platform team
- Making progress on foundation while delivering quick wins
- Navigating organizational dynamics
- Learning FirstMark's investment approach and culture

**For This Presentation:**
- Show I can think strategically about product and technology
- Demonstrate I understand VC and talent workflows
- Prove I can build functional prototypes quickly
- Communicate clearly without jargon
- Be honest about what I know and don't know

---

*End of Case Working Doc v2*
