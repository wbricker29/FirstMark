# Presentation Content Inventory

> Comprehensive inventory of all potential content pieces, talking points, and narrative elements for FirstMark Talent Signal Agent presentation
>
> **Usage:** Pick and arrange elements based on chosen presentation outline and audience

---

## Table of Contents

1. [Strategic Frameworks](#strategic-frameworks)
2. [Business Context & Requirements](#business-context--requirements)
3. [Technical Decision Frameworks](#technical-decision-frameworks)
4. [Solution Architecture](#solution-architecture)
5. [Demo Content](#demo-content)
6. [Roadmap & Vision](#roadmap--vision)
7. [Talking Points Library](#talking-points-library)
8. [Q&A Preparation](#qa-preparation)
9. [Narrative Hooks & Transitions](#narrative-hooks--transitions)

---

## Strategic Frameworks

### Three-Tier Solution Framework

**Tier 1: The Ideal Solution (12-18 months)**

*What this would look like in an ideal state:*
- **Centralized data platform** → Universal people/company/role storage, Affinity integration, immutable event log
- **Modular architecture** → Lift-and-shift capabilities to new use cases
- **Model agnostic** → Swap LLM providers, research methods without rewiring
- **Standard operations** → Reusable enrichment (Apollo, Harmonic), normalization, deduplication
- **Foundational artifacts** → Role specs, assessment methods as reusable components

*Key characteristics:*
- Enterprise-grade talent intelligence platform
- Standardized ETL pipelines for ingestion
- Parallel operations storage system with event logging
- Storage and maintenance process for open roles

*This is the strategic destination—but you can't build it without learning what you're building on.*

---

**Tier 2: The MVP Solution (1-month sprint)**

*What I'd build if asked to develop first cut for production use:*
- Actual ROI discussion and roadmapping
- Market research on providers (Apollo, People Data Labs, AI candidate eval tools, networking matching)
- Standard framework leveraging central tools (firm-standard Python frameworks, LLM framework like ADK)
- Research via:
  - External providers (research as API)
  - Open source approaches
  - Custom in-house agents
- Store content from all cited sources
- Better investigation capability (drill-down into raw data)
- Consensus mechanisms for quality control
- Use whatever APIs you have (Harmonic, Apollo, etc.)

*This is what you build after Tier 3 proves the value hypothesis.*

---

**Tier 3: The 2-Day Demo (What I'm Showing Today)**

*What's illustrative and functional in 48 hours:*
- **Meet you in Airtable** → Start where you are, not where I want you to be
- **OpenAI Deep Research** → Good enough for demo; demonstrates integration capability
- **Module 1 + Module 4** → Production-quality ingestion + screening workflow
- **Synchronous processing** → Simpler implementation, faster to value
- **Mock enrichment** → Don't need Apollo API for demo validation
- **Standard Airtable views** → No custom UI

*This is what earns credibility to have the Tier 2 conversation.*

---

**Why This Order Matters:**
- Can't skip to Tier 1 without learning from Tier 3
- Each tier builds credibility and understanding for the next
- Tier 3 validates the approach; Tier 2 validates the ROI; Tier 1 delivers strategic leverage
- The best strategies emerge from delivered value, not planning exercises

---

### Horizon Framework (Quick Win Progression)

**Horizon 1: Quick Wins (Today → 3 months)**
- Value-generating MVP
- Learning-generating prototypes
- Credibility-building demonstrations
- **Goal:** Prove value + build relationships

**Horizon 2: Strategic Foundation (3-12 months)**
- Centralized data models
- Reusable components
- Process standardization
- **Goal:** Create leverage + reduce friction

**Horizon 3: Transformational Capability (12+ months)**
- Platform thinking
- Ecosystem integration
- Organizational capabilities
- **Goal:** Compounding advantage

**The Critical Path:**
- Each horizon builds on the last
- Can't skip to Horizon 3 without earning Horizon 1
- Learning from H1 shapes H2 strategy
- Credibility from H1+H2 enables H3 investment

---

### Five Questions Framework

**1. What do you want?** (Business outcome definition)
- Business context and pain points
- Success metrics
- Stakeholder needs

**2. Should we do it?** (Expected ROI + opportunity cost)
- The case for
- Known constraints
- The bet we're making

**3. How do we do it?** (Execution approach)
- Three-tier solution design
- Technical decisions
- Key complexity decisions

**4. How do we know it's working?** (Validation criteria)
- Demo setup
- Success criteria
- Evaluation metrics

**5. How do we build on it?** (Compounding value)
- Immediate next steps
- Phase 2 extensions
- What I still need to learn

---

## Business Context & Requirements

### Current State Understanding

**What I Know About FMC:**
- Airtable is your operational hub
- Data conversations happen carefully
- Tools exist that aren't being adopted (Ryan's work)
- Need to prove value before changing workflows
- Can't build the beautiful thing without credibility—it won't get used
- Portfolio companies need executive talent
- Guild network is valuable but underutilized
- I need to prototype quickly to get to value

**What I Don't Know (And Need To Learn):**
- Current workflow details and frequency
- Data landscape and structure
- How Affinity is being used today
- Organizational readiness and stakeholder dynamics
- Where data lives and what it looks like
- What current systems look like
- Workflow frequency and relative value
- Who are conversion targets

---

### The Opportunity

**Business Context:**
- **Differentiation:** Guild network is a differentiator—use it
- **Rationalization:** People evaluation done many times, many ways → rationalize + augment = value
- **Fundamentals:** People evaluation is fundamental to VC, especially early stage
- **Scalability:** Repeated process across portfolio (scalable value)
- **Extension potential:** Other people enrichment use cases (founders, LPs, portfolio hires)
- **Retroactive application:** Historical analysis potential

**Pain Points:**
- Manual screening is time-consuming (hours → should be minutes)
- Research quality varies by researcher
- Hard to audit decision trails
- Network connections get lost in noise
- Similar candidates are hard to differentiate on paper
- Limited scalability (partner/talent team bandwidth constrains searches)
- Inconsistent coverage (some portcos get deep support, others minimal)
- Implicit matching logic (lives in team members' heads, not captured systematically)

---

### Core Requirements

**Primary Requirements:**
- **Recall over precision** → Rather not miss a great match vs see some duds
- **Filter, not decide** → Goal is to filter candidates for review, not make the final decision
  - Sufficiently filter who is reviewed
  - Inform review of an individual (surface key info, enable quick action)
  - Enable deeper investigation
- **Augment, not replace** → Target is augmentation of the talent team, not replacement
- **Show your work** → Validate quality of research methods AND evaluation traces
- **Explain match quality** → Clear reasoning for why candidates were/weren't recommended
- **Capture matching logic** → Codify evaluation criteria in reusable role specifications

**Success Metrics (Business Value):**
- Validate quality of research methods
- Validate quality of evaluation and traces
- Cut operational cost
- Optimize execution time
- Faster turnaround on search requests without sacrificing match quality

**Success Metrics (Adoption Indicators):**
- Talent team says: "I'd actually use these rankings to prioritize my outreach"
- Portfolio CEOs understand why candidates were recommended (transparent reasoning)
- System surfaces candidates the team might not immediately recall
- Evaluators trust the reasoning trails

**Success Metrics (Demo Validation):**
- Process 10-15 candidates across 4 portfolio company scenarios
- Generate ranked lists with dimension-level scores (1-5 scale)
- Provide evidence-based reasoning for each assessment
- Complete assessment pipeline in <10 minutes per candidate
- Export results to Airtable + markdown reports

---

## Technical Decision Frameworks

### Decision 1: Where Do We Need LLMs vs Rules?

**LLMs for:**
- Research synthesis (Deep Research API - unstructured web content)
- Assessment (spec-guided evaluation - nuanced judgment)
- Optional: Enrichment (though Apollo API is better for structured data)
- Reporting (markdown generation)

**Rules/Code for:**
- Data ingestion (CSV parsing)
- Deduplication (name + company matching)
- Validation (URL formats, required fields)
- Score calculation (deterministic aggregation)

**Why:**
- Use the right tool for the job—LLMs for unstructured reasoning, code for structured operations
- LLMs are expensive and non-deterministic—reserve for where they add unique value
- Code is faster, cheaper, more reliable for deterministic logic

---

### Decision 2: How Do We Guardrail LLMs?

**Structural Guardrails:**
- **Structured outputs** → Pydantic schemas force valid JSON (no hallucinated fields)
- **Evidence requirements** → Citation thresholds, evidence-aware scoring
- **Quality gates** → Research sufficiency checks before assessment
- **Constrain vs enable balance** → Role specs guide but don't over-constrain LLM reasoning

**Transparency Guardrails:**
- **Confidence scoring** → LLM self-assessment of research quality
- **Counterfactuals** → "Why candidate might NOT be ideal" prevents overconfidence
- **Evidence quotes** → Every score backed by specific evidence
- **Citation tracking** → All claims traceable to sources

**Process Guardrails:**
- **Spec-guided assessment** → Role requirements drive evaluation dimensions
- **1-5 scale with None** → "Insufficient Evidence" option (no forced guessing)
- **Human-in-the-loop** → Filter for review, not autonomous decision-making

---

### Decision 3: How Do We Optimize Human Engagement?

**Filter, Don't Decide:**
- Recall over precision (don't miss great matches)
- Generate ranked shortlists, not final decisions
- Human reviews top candidates, system filters the rest

**Surface Key Info:**
- Role spec drives what to research and assess
- Dimension-level scores show strengths/weaknesses at a glance
- Topline summary for quick scanning

**Enable Investigation:**
- Drill-down into evidence, citations, reasoning trails
- Raw research markdown available
- All assessment data exportable

**Show Your Work:**
- Every score has evidence quotes and reasoning
- Counterfactuals surface key assumptions
- Confidence scores flag where to double-check

**Focus Time on High-Value Work:**
- Automate manual research (LinkedIn scrolling, news searches)
- Standardize evaluation framework (consistent criteria)
- Enable talent team to focus on relationships, not data gathering

---

### Decision 4: Build vs Buy?

**Build:**
- Workflow orchestration (custom to FMC workflow)
- Assessment logic (spec-guided evaluation is unique)
- Deduplication (simple name + company matching)
- Module integration (connects CSV → screening → results)

**Buy:**
- LLM APIs (OpenAI - Deep Research, GPT-4)
- Database + UI (Airtable - meet them where they are)
- Agent framework (Agno - orchestration + native UI monitoring)
- Integration layer (Flask + ngrok - quick webhook setup)

**Mock (For Demo):**
- Apollo enrichment (not needed to validate approach)
- Not doing real Apollo because: haven't used it, adds cost/complexity, not value-critical for demo

**Defer (Phase 2+):**
- Async processing (optimization, not validation)
- Candidate profiles (requires refinement on what a profile is)
- Incremental search (enhancement, not core workflow)
- Custom UI (Airtable views sufficient for demo)

**Why:**
- Build where you create differentiated value
- Buy commodity capabilities
- Mock what doesn't affect validation
- Defer optimizations until value is proven

---

### Decision 5: Research Method

**Options Considered:**
- Out-of-the-box API (OpenAI Deep Research, other deep research API, Hugging Face model)
- Open source approach/framework (Open Deep Research, Caml, Owl)
- Custom agentic build

**Decision:** OpenAI Deep Research API + ability to do incremental search via GPT + web search

**Reason:**
- Good enough for demo purposes
- Demonstrates integration capability
- 2-6 minutes per candidate (acceptable for demo)
- Comprehensive, well-cited research
- Can layer incremental search if quality check fails

---

### Decision 6: UI Platform

**Options Considered:**
- Deep agents with native UI
- Streamlit (custom dashboard)
- Jupyter notebook (data science workflow)

**Decision:** Airtable

**Reason:**
- Meet FirstMark where they are
- Demonstrate ability to integrate with existing stack
- DB + UI features quickly
- Talent team already familiar
- No adoption friction

---

### Decision 7: Candidate Profiles (Deferred)

**Question:** Do we skip creating profile and just have bespoke research anchored on spec for now?

**Decision:** Yes, skip

**Reason:**
- Probably takes some more refinement on what a profile is
- If we keep standardized profiles or auto-gen when create new person (of x y z type)
- Not mission critical for demo validation
- Can do it as an extension if we want (Tier 2)

---

## Solution Architecture

### Module 1: Data Upload (Production-Quality Ingestion)

**Scope:**
- CSV ingestion via Airtable webhook
- People table population (64 executives from guild scrape)
- Smart deduplication (name + company matching)
- Data quality validation
- Upload audit trail

**What Makes It Production-Quality:**
- **Validation:** Malformed LinkedIn URLs, missing companies, required fields
- **Deduplication:** Prevent duplicate records (name + company matching)
- **Audit trail:** Track who uploaded, when, how many records, errors encountered
- **Error handling:** Which records failed and why (logged in Airtable)
- **Batch processing:** Handle full CSV uploads, not one-by-one

**Known Messy Corners:**
- **Non-normalized titles:** CFO vs Chief Financial Officer vs VP Finance → Design for variability
- **Disambiguation needs:** Same name, different people → Company + LinkedIn URL matching
- **This happens too often to centralize:** Make it easy to handle at point of use

**Deferred to Phase 2+:**
- Real-time enrichment (Apollo, LinkedIn APIs)
- Company/role uploads (only People in v1)
- Complex fuzzy matching (simple deterministic for demo)

---

### Module 4: Screening Workflow (AI-Powered Assessment)

**Linear Workflow:**
1. **Deep Research** → Comprehensive executive research (o4-mini-deep-research)
2. **Quality Check** → Evaluate research sufficiency (citation count, content depth)
3. **Optional Incremental Search** → Single-pass supplement if quality is low (≤2 web tool calls)
4. **Assessment** → Spec-guided evaluation with evidence-backed scores (gpt-5-mini)

**Key Components:**

*Deep Research Agent:*
- OpenAI o4-mini-deep-research model
- 2-6 minutes per candidate
- Returns markdown with inline citations
- Built-in web search capability
- ~$0.36 per candidate cost

*Quality Check Logic:*
- Citation threshold (≥3 sources)
- Content depth (≥500 chars meaningful text)
- Source diversity (≥2 unique domains)
- Flags insufficient research for supplemental search

*Incremental Search Agent (Optional):*
- Triggered when quality check fails
- GPT-5 + web search tool
- Single pass, max 2 web tool calls
- Targets specific gaps identified by quality check
- Adds 30-90 seconds when triggered

*Assessment Agent:*
- GPT-5-mini with ReasoningTools
- Spec-guided evaluation (role requirements drive dimensions)
- Evidence-aware scoring (1-5 scale with None for "Insufficient Evidence")
- Structured output (Pydantic AssessmentResult model)
- Counterfactual reasoning ("Why candidate might NOT be ideal")
- Confidence self-assessment

**What Makes This Different:**
- **End-to-end audit trail:** CSV upload → research → assessment → final score
- **Evidence-aware scoring:** 1-5 scale with None for "Insufficient Evidence" (no forced guessing)
- **Spec-guided assessment:** Role requirements drive evaluation dimensions
- **Counterfactual reasoning:** Surfaces key assumptions and potential downsides
- **Quality gates:** Don't assess until research is sufficient
- **Explainability:** Every score has evidence quotes, citations, reasoning

---

### Technical Stack

**Core Framework:**
- **Agent orchestration:** Agno (native UI monitoring, prompt templates, workflow management)
- **LLMs:** OpenAI (o4-mini-deep-research for research, gpt-5-mini for assessment)
- **Database/UI:** Airtable (6 tables: People, Portco, Portco_Roles, Searches, Screens, Assessments)
- **Integration:** Flask + ngrok (webhook for Airtable automation)
- **Structure:** Pydantic (type-safe structured outputs, data validation)
- **Session persistence:** Agno SqliteDb (stored at tmp/agno_sessions.db)

**Execution Model:**
- **Processing:** Synchronous, single-process (async deferred to Phase 2+)
- **Workflow:** Linear sequential steps (no complex branching)
- **Error handling:** Exponential backoff, retry logic, Airtable status tracking

**Data Storage:**
- All research + assessment data in Airtable Assessments table
- Raw research markdown + structured JSON stored
- Assessment JSON + markdown reports stored
- No separate Workflows or Research_Results tables (v1 simplification)

---

### Strategic Boundaries Questions (What I Still Need To Learn)

**What's Central and Universal?**
- Person intake and normalization → Should this be centralized across all use cases?
- All people enrichment → Standard operation or use-case specific?
- Role spec framework → Reusable across searches or custom per search?

**What Do We Keep vs Redo vs Toss?**
- Should we define a refresh process for stale data?
- When do we re-research vs use cached profiles?
- What's the lifecycle of a role spec? (versioning, updates)

**These are Tier 2 questions—can't answer them without Tier 3 learnings.**

---

## Demo Content

### Demo Setup

**Scenarios:**
- 4 real portfolio scenarios (CFO/CTO roles)
- 64 real executives (Guild members + network from scrape)
- Challenge: 3 similar-on-paper candidates (AI must surface differentiation)

**Portfolio Companies:**
- Pigment (CFO role)
- Mockingbird (CFO role)
- Synthesia (CTO role)
- Estuary (CTO role - live demo)

**Pre-Run Strategy:**
- Scenarios 1-3: Pre-run before demo to show results quality
- Scenario 4: Live execution to show real-time workflow

---

### Demo Flow (10 min)

**Module 1: Data Ingestion (1 min)**
- Show CSV upload with deduplication
- Highlight validation: malformed LinkedIn URLs, missing companies
- Show upload audit trail (64 records, 3 duplicates detected, 2 validation errors)

**Module 4: Screening Workflow (9 min)**

*Role Spec (1 min):*
- Show how CFO requirements are structured (fundraising, ops finance, stage expertise)
- Demonstrate dimension definitions with evidence levels

*Research (2 min):*
- Walk through Deep Research output for 2 candidates
- Show citations, career timeline extraction
- Highlight structured markdown format

*Quality Check (30 sec):*
- Show evidence sufficiency logic (did we get enough to assess?)
- Demonstrate when incremental search would trigger

*Assessment (2 min):*
- Show spec-guided evaluation with evidence-backed dimension scores
- Walk through reasoning for one dimension
- Show confidence levels

*Ranking (2 min):*
- Demonstrate why #1 beat #2 with reasoning (not just scores)
- Show counterfactuals ("Why candidate might NOT be ideal")
- Highlight key assumptions

*Drill-Down (1.5 min):*
- Show evidence trails (click through to citations)
- Demonstrate exportable markdown reports
- Show Airtable views for talent team review

**Success Metric:**
"I'd actually use this ranking to prioritize my review time—and I trust the reasoning"

---

### Demo Talking Points

**Opening:**
- "What you're seeing is Tier 3—a 48-hour demo built to validate the approach"
- "Module 1 shows production thinking; Module 4 shows AI capability"

**During Module 1:**
- "This isn't just CSV parsing—it's production-quality data handling"
- "Deduplication prevents garbage in, garbage out"
- "Audit trail shows every upload: what succeeded, what failed, why"

**During Research:**
- "Deep Research is comprehensive—but we validate it before using it"
- "3-6 minutes per candidate, but it's doing hours of manual work"
- "Citations matter—every claim is traceable to a source"

**During Quality Check:**
- "We don't assess if we don't have enough evidence—that's the guard rail"
- "Quality gate can trigger incremental search if needed"

**During Assessment:**
- "Role spec drives what we evaluate—not a generic rubric"
- "1-5 scale with None for 'Insufficient Evidence'—no forced guessing"
- "Every score has evidence quotes—this is why we scored this way"

**During Ranking:**
- "It's not just scores—it's reasoning about fit"
- "Counterfactuals surface the assumptions: 'This is great IF...'"
- "The goal is to inform your review, not replace it"

**Closing:**
- "This is what earns credibility to have the Tier 2 conversation"
- "What would you want to see different?"

---

## Roadmap & Vision

### Horizon 1: Quick Wins (Today → 3 months)

**What We're Shipping:**
- Module 1: Production-quality People CSV ingestion
- Module 4: AI-powered screening workflow
- Lives in Airtable (meet you where you are)
- 48-hour build time
- Real demo with real data

**Value Proposition:**
- Faster candidate screening (hours → minutes)
- More consistent research quality
- Auditable reasoning trails from data ingestion → final ranking
- Surfaces non-obvious differentiators
- Extensible to other use cases (founders, LPs, portfolio hires)

**Learning Agenda:**
- **Value Validation:** Does this actually save time vs manual screening?
- **Trust Check:** Do evaluators trust the rankings enough to act on them?
- **Quality Benchmark:** What's the accuracy vs manual research/assessment?
- **Failure Analysis:** Where does it break down? (edge cases, missing data)
- **Data Strategy:** What does usage teach us about data quality needs?
- **Integration Planning:** How does this inform Affinity/CRM strategy?
- **Use Case Validation:** Which extensions deliver most value? (founders, LPs, portfolio hires)

---

### Horizon 2: Strategic Foundation (3-12 months)

**Phase 2A: Production-Ready Modules**
- **Module 1 Enhancement:** Real-time enrichment (Apollo, LinkedIn APIs)
- **Module 4 Enhancement:** Async processing, candidate profiles (reusable research)
- **Workflow Optimization:** Incremental search for gap-filling, adaptive quality thresholds
- **Integration:** Affinity CRM sync, custom UI for stakeholder views

**Phase 2B: Module Expansion**
- **Module 2:** Portfolio company + role uploads (not just People)
- **Module 3:** AI-powered role spec generation (from job descriptions)
- **Enrichment Layer:** Automated data quality checks, missing field detection
- **Downstream:** Placement tracking, retrospective analysis

**Phase 2C: Capability Expansion**
- **Use Case 1:** Founder research workflows (diligence support)
- **Use Case 2:** LP research workflows (fundraising support)
- **Use Case 3:** Portfolio company hire support (self-service talent matching)
- **Learning Loop:** Track placement outcomes, refine assessment criteria

---

### Horizon 3: Transformational Capability (12+ months)

**Centralized People Intelligence:**
- Normalized people database across all use cases
- Reusable enrichment components
- Cross-use-case insights (founder today, hire tomorrow)
- Network effect from usage (more searches → better data)

**Portfolio Value Platform:**
- Standardized people processes across portfolio
- Shared research capabilities (avoid redundant work)
- Portfolio company self-service (reduce talent team bottleneck)
- Ecosystem integration (Affinity, CRM, ATS systems)

**Strategic Extensions:**
- Two-way sync with portfolio company ATS systems
- Proactive candidate recommendations ("You should meet X for Y role")
- Network growth suggestions ("Add executives from sector Z")
- Historical search analytics and learning from outcomes

---

### "EvolutionIQ for VC" Vision

**What EvolutionIQ Did for Insurance:**
- Applied AI to unstructured claims data
- Made faster, more consistent decisions
- Explainable recommendations with evidence trails
- Production-ready architecture scaled across use cases

**What We're Doing for VC Talent:**
- Applied AI to unstructured candidate data (LinkedIn, news, research)
- Faster, more consistent talent screening
- Explainable rankings with evidence and counterfactuals
- Modular architecture that extends beyond talent (founder eval, LP research)

**The Difference (Being Realistic):**
- EvolutionIQ is a mature SaaS product with years of refinement
- This is a 48-hour prototype demonstrating the **approach**
- We're showing **how** to apply structured AI workflows to VC operations
- Not claiming feature parity—claiming **directional validity**

**The Parallel:**
- AI-powered structured workflows for domain-specific decision-making
- Explainable outputs with evidence trails (not black-box AI)
- High-stakes decisions where transparency matters
- Production-ready thinking from day one

---

## Talking Points Library

### On the Three-Tier Framework

- "Tier 1 is the strategic destination—but you can't build it without learning what you're building on"
- "Tier 3 validates the approach; Tier 2 validates the ROI; Tier 1 delivers strategic leverage"
- "Each tier builds credibility and understanding for the next"
- "Before I show you what I built, let me show you how I thought about what to build"
- "Can't skip to Tier 1 without learning from Tier 3"
- "The framework ensures we're building the right thing, not just building things right"

### On Key Decisions

- "Every technical decision is really a business decision about where to create value"
- "Where do we need LLMs vs rules? Use the right tool for the job"
- "Build vs buy isn't about cost—it's about where you create differentiated value"
- "Known messy corners: Titles will be non-normalized, there will be disambiguation—design for it"
- "I optimized for learning velocity over completeness"

### On Requirements and Constraints

- "Recall over precision—I'd rather not miss a great match vs see some duds"
- "Filter, not decide—the goal is to filter candidates for review, not make the final decision"
- "Augment, not replace—the target is augmentation of the talent team, not replacement"
- "Show your work—validate quality of research methods AND evaluation traces"
- "Constraints are features—they force clarity and prioritization"
- "The best demos are built in 48 hours because you can't overthink them"

### On Credibility and Adoption

- "Meet them where they are" is about earning the right to lead them somewhere new
- "Ryan's tools aren't used because they skipped the credibility-building step"
- "Can't build the beautiful thing without credibility—it won't get used"
- "Quick wins buy credibility for harder work"
- "Technology is easy. Adoption is hard. We design for adoption."
- "You can build the beautiful thing, but without cred, it's not going to get used"

### On Strategic Thinking

- "The best strategies emerge from delivered value, not planning exercises"
- "I'm optimizing for compounding learning, not comprehensive coverage"
- "Strategic boundaries questions can't be answered until you ship something and learn"
- "Horizon 3 looks completely different after you've shipped Horizon 1"
- "Every 'no' today is a strategic choice that enables a 'yes' tomorrow"

### On What I Don't Know

- "The biggest determining factors are things I don't know yet—and that's expected"
- "What's your data landscape? How are you using Affinity? What are the organizational dynamics?"
- "These unknowns inform Tier 2—they don't block Tier 3"
- "I'm optimizing for learning velocity, not certainty"
- "There are countless things I don't know about FMC—and that's expected"

### On Partnership

- "I'm not selling you this demo—I'm showing you how I approach building with you"
- "The value isn't in the prototype, it's in the thinking that produced it"
- "Module 1 demonstrates production thinking; Module 4 demonstrates AI capability—together they show end-to-end competence"
- "I'm not selling you a solution—I'm showing you how I think about building solutions with you"

### On the EvolutionIQ Comparison

- "EvolutionIQ proved structured AI workflows work for high-stakes decisions in insurance—we're applying that model to VC talent operations"
- "This isn't claiming feature parity with a mature product—it's demonstrating directional validity of the approach"
- "The parallel: AI-powered structured workflows with explainable outputs for domain-specific decision-making"

### On Deferred Decisions

- "Candidate profiles? Probably takes refinement on what a profile is—deferred to Tier 2"
- "Async processing, incremental search—these are optimizations, not validations"
- "Every 'no' today enables a clearer 'yes' tomorrow"

### On Quick Wins

- "Quick wins aren't shortcuts—they're strategic learning investments"
- "The goal isn't to build perfectly, it's to learn precisely"
- "Every quick win should answer a strategic question"
- "The fastest path to transformation is through a series of compounding quick wins"

### On Foundation Building

- "You can't build the foundation until you know what you're building on it"
- "The quick win teaches us what the foundation should look like"
- "Each horizon builds on the credibility and learning of the last"

### On Execution

- "Meet them where they are" isn't just about tools—it's about credibility
- "I've built enough things that nobody used to know that execution is only half the battle—adoption is the other half"
- "Great transformation requires understanding both the ideal destination and the practical path to get there"

### On Organizational Change

- "The biggest determining factors are understanding the 'what is' (current systems, data, processes) and the 'why'"
- "Paying your sponsors (investors, COO, platform team)"
- "Making headway on foundation while delivering value"
- "Navigating organizational dynamics (who to convert, who to accommodate)"

### On Methodology

- "I don't just build solutions—I build transformation capabilities that compound over time"
- "I've learned that the best transformations don't start with technology—they start with understanding why current approaches exist"

---

## Q&A Preparation

### Anticipated Questions - Technical

**Q: How accurate is the research?**
A: Deep Research cites sources—you can verify. Quality gate ensures minimum citation threshold (3+ sources). Incremental search fills gaps when needed. For demo, pre-ran scenarios show quality level.

**Q: What happens when it gets things wrong?**
A: Three layers of protection:
1. Evidence-aware scoring (None for "Insufficient Evidence"—no forced guessing)
2. Counterfactuals surface key assumptions
3. Confidence scores flag where to double-check
Goal is to filter for human review, not autonomous decision-making.

**Q: How do you prevent hallucinations?**
A:
1. Structured outputs (Pydantic schemas—can't hallucinate field names)
2. Citation requirements (every claim traceable to source)
3. Evidence quotes (must extract from research, not generate)
4. Quality gates (don't assess if research is insufficient)
5. Confidence scoring (LLM self-assesses reliability)

**Q: What's the path to production?**
A: Tier 2 → Tier 1 progression:
- Tier 2: Async processing, candidate profiles, Affinity integration, real enrichment APIs
- Tier 1: Centralized data platform, modular architecture, model-agnostic design
Each phase informed by learnings from previous tier.

**Q: How does this scale?**
A:
- Current: Synchronous, ~10 candidates in 30-60 min
- Tier 2: Async processing, 100+ candidates in parallel
- Cost scales linearly (~$0.37/candidate for research + assessment)
- Architecture designed for horizontal scaling (add workers)

**Q: What about data privacy/security?**
A:
- Security is a firm-level decision—needs to be clear upfront
- Currently: Public data only (LinkedIn, news, company websites)
- Production: Would need to discuss data handling policies, API security, access controls
- Can use self-hosted LLMs if needed (though adds complexity)

**Q: How does this integrate with existing tools?**
A:
- Airtable: Already integrated (webhook-triggered workflows)
- Affinity: Phase 2—would sync candidates, roles, activity tracking
- Would need to understand: Current data schema, API access, update frequency
- Design principle: Meet you where you are, minimal workflow disruption

**Q: What's the cost structure?**
A:
- Current demo: ~$0.37/candidate (dominated by Deep Research API)
- At scale: Depends on research mode (fast vs deep), assessment complexity
- Trade-offs: Speed vs thoroughness, cost vs quality
- Tier 2 discussion: ROI analysis based on actual usage patterns

---

### Anticipated Questions - Product

**Q: How do we measure success?**
A: Two layers:
1. **Product metrics:** Time saved, candidates processed, rankings used
2. **Outcome metrics:** Placement quality, talent team satisfaction, portfolio CEO feedback

Learning agenda (Tier 3):
- Does this save time vs manual?
- Do evaluators trust rankings?
- Where does it break down?
- What does usage teach us about data needs?

**Q: What if the quick win doesn't work?**
A: That's valuable learning:
- Tells us what NOT to build in Tier 2
- Reveals constraints we didn't understand
- Informs different approach or different use case
- Cheap to learn now vs expensive to learn after Tier 2 investment

**Q: How do you prevent scope creep?**
A: Three-tier framework is the discipline:
- Tier 3: Validate approach only (not production features)
- Tier 2: Build after learning from Tier 3
- Tier 1: Strategic investment after Tier 2 proves ROI
Clear boundaries on what's in vs deferred.

**Q: How do we handle edge cases?**
A: Design philosophy:
- Build for the 80% case first
- Flag edge cases for human review (confidence scores, evidence levels)
- Learn from edge cases to improve Tier 2
- Don't over-engineer Tier 3 for every edge case

**Q: What about bias in AI assessments?**
A: Transparency mechanisms:
- Evidence-backed scores (can audit reasoning)
- Counterfactuals (surface assumptions)
- Human-in-the-loop (filter, not decide)
- Role specs are explicit (bias in spec is visible, not hidden in model)

---

### Anticipated Questions - Strategic

**Q: How do you decide what's a quick win vs foundation?**
A: Quick wins:
- Demonstrate value quickly
- Answer a strategic question
- Build credibility
- Generate learning

Foundation:
- Require credibility to secure investment
- Depend on learnings from quick wins
- Create leverage for multiple use cases
- Compounding value over time

**Q: How does this inform broader platform strategy?**
A: Three ways:
1. **Data centralization:** People data model extends to founders, LPs, hires
2. **Reusable components:** Enrichment, assessment, research frameworks
3. **Use case templates:** Talent → Founder → LP → Portfolio hire (similar patterns)

**Q: What's the governance model for AI tools?**
A: Needs firm-level discussion:
- Who approves new use cases?
- What's the data handling policy?
- How do we ensure quality?
- What's the approval process for role specs?
- How do we handle feedback and iteration?

---

## Narrative Hooks & Transitions

### Opening Hooks

**Transformation Partner:**
- "I've learned that the best transformations don't start with technology—they start with understanding why current approaches exist"

**Executable Vision:**
- "I've built enough things that nobody used to know that execution is only half the battle—adoption is the other half"

**Quick Win Architect:**
- "I've learned that the best way to predict the future is to ship something small today that teaches you what to build tomorrow"

---

### Key Transitions

**From Introduction to Framework:**
- "Let me show you how this framework applies to a real use case..."
- "Before I show you what I built, let me show you how I thought about what to build"

**From Business Context to Technical Approach:**
- "So how do we actually do this? Let me walk you through the key decisions..."
- "This is what we're building—now let me show you how we're building it"

**From Strategy to Demo:**
- "Enough talking about it—let me show you how it works"
- "This is Tier 3 in action—a 48-hour demo that validates the approach"

**From Demo to Roadmap:**
- "If this quick win works, what's next?"
- "This is where we are today—here's where we could go"

**From Roadmap to Partnership:**
- "But I can't answer these questions without you. Here's what I need to learn..."
- "This demo informs the roadmap—it doesn't define it"

---

### Closing Transitions

**To Q&A:**
- "That's what I've built in 48 hours. Now I want to hear from you—what questions do you have?"
- "I've shown you my thinking—now help me refine it with your questions"

**Final Message:**
- "I'm not selling you this demo—I'm showing you how I approach building with you"
- "The value isn't in the prototype, it's in the thinking that produced it, and the partnership we could build together"

---

## Usage Notes

**Picking Content for Your Presentation:**

1. **Choose Your Narrative** (Outline 1, 2, or 3)
2. **Select Framework Elements** (Three-Tier vs Horizon vs Five Questions)
3. **Pick Business Context** (Level of detail based on audience knowledge)
4. **Include Key Decisions** (Shows judgment and trade-off thinking)
5. **Prepare Demo Script** (Module 1 + Module 4 flow)
6. **Select Roadmap Detail** (Based on how much future vision to show)
7. **Prepare Talking Points** (3-5 key themes to reinforce)
8. **Anticipate Questions** (Based on audience type)

**Audience-Specific Adjustments:**

- **For COO/Strategic Hire:** Heavy on Three-Tier Framework, Strategic Thinking
- **For Investor/Delivery Focus:** Heavy on Key Decisions, Execution Points
- **For Platform/Product Hire:** Heavy on Horizon Framework, Quick Wins Philosophy

---

**Document Version:** 1.0
**Created:** 2025-01-17
**Purpose:** Comprehensive inventory for presentation assembly
