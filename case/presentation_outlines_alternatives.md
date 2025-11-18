# Presentation Outline Alternatives

> Three distinct narrative approaches for the FirstMark case study presentation
>
> Each outline is designed for a 1-hour format (15 min intro, 30 min presentation, 15 min Q&A)

---

## Outline 1: "The Transformation Partner"

**Narrative Strategy:** Position as strategic partner who brings systematic methodology to VC transformation. Lead with framework, demonstrate through application.

**Core Message:** "I don't just build solutions—I build transformation capabilities that compound over time."

**Audience Impact:** Best for demonstrating depth of strategic thinking and ability to drive organizational change.

---

### Structure

#### **Part 1: Introduction (15 min)**

**1.1 About Will (5 min)**
- Background and relevant experience
- **Hook:** "I've learned that the best transformations don't start with technology—they start with understanding why current approaches exist"

**1.2 The Transformation Playbook (10 min)**
*Position the framework that guides all work*

**The Five Questions Framework:**
1. **What do you want?** (Business outcome definition)
2. **Should we do it?** (Expected ROI + opportunity cost)
3. **How do we do it?** (Execution approach)
4. **How do we know it's working?** (Validation criteria)
5. **How do we build on it?** (Compounding value)

**The Critical Success Factors:**
- Understanding the current state (and the "why" behind it)
- Identifying your sponsors and stakeholders
- Building credibility through quick wins
- Designing for organizational adoption, not just technical elegance
- Acknowledging what you don't know

**Transition:** "Let me show you how this framework applies to a real use case..."

---

#### **Part 2: Applying the Framework (30 min)**

**2.1 Question 1: What Do You Want? (5 min)**

**Business Context:**
- People evaluation is fundamental to early-stage VC
- Guild network is a differentiator—but underutilized
- Manual screening processes create bottlenecks
- Recall > Precision (don't miss great matches)
- Goal is augmentation, not replacement

**Success Metrics:**
- Validate quality of research methods
- Validate quality of evaluation and traces
- Cut operational cost
- Optimize execution time

**2.2 Question 2: Should We Do It? (4 min)**

**The Case For:**
- Repeated process across portfolio (scalable value)
- High-judgment task that benefits from structured augmentation
- Data exists but isn't structured for AI leverage
- Extension potential (founders, LPs, hires)

**Known Constraints:**
- Don't know current workflow frequency
- Don't know how Affinity is being used
- Don't know data quality/structure
- Don't know organizational readiness

**The Bet:**
- Can demonstrate value quickly in Airtable
- Can show approach that extends beyond this use case
- Can build credibility through working prototype

**2.3 Question 3: How Do We Do It? (12 min)**

**Three-Tier Approach:**

**Tier 1: The Ideal State (2 min)**
- Centralized people data normalized across use cases
- Modular research/enrichment components
- Model-agnostic architecture
- Lift-and-shift capabilities for new use cases

**Tier 2: The MVP (3 min)**
- ROI-validated roadmap
- Lightweight framework leveraging central tools
- Market research on providers (timeboxed)
- Consensus mechanisms for quality
- Anthropic as primary LLM

**Tier 3: The 2-Day Demo (7 min)**

**What I Know About FMC:**
- You use Airtable
- Data discussions are cautious
- Need to demonstrate value quickly
- Must start where you are (adoption > perfection)
- Ryan's tools aren't being used (lesson learned)

**My Bets:**
- Can meet you in Airtable
- OpenAI Deep Research + subagents sufficient for demo
- GPT for basic LLM (cheap exploration)

**Technical Decisions:**
- Module 4 only (screening workflow)
- Linear, synchronous processing (async deferred)
- Deep Research API for candidate research
- Structured outputs via Pydantic
- Direct Airtable integration

**Key Complexity Decisions:**
- Where do we need LLMs vs rules?
- How do we balance enabling vs constraining the LLM?
- How do we optimize human engagement points?
- What do we build vs buy?

**2.4 Question 4: How Do We Know It's Working? (4 min)**

**Demo Setup:**
- 4 portfolio role scenarios (CFO/CTO positions)
- 64 real executives (Guild members + network)
- 3 similar-on-paper candidates (AI must surface differentiation)

**Success Criteria:**
- Evaluators say "I'd actually use this ranking"
- Reasoning trails are auditable and make sense
- System surfaces non-obvious differentiators
- Human can drill down into any decision

**[LIVE DEMO - 4 min]**
- Show role spec → research → assessment flow
- Walk through 2 candidates in depth
- Show ranking with reasoning trails
- Demonstrate drill-down capability

**2.5 Question 5: How Do We Build On It? (5 min)**

**Immediate Next Steps:**
- Validate approach with real portfolio needs
- Understand data landscape and integration points
- Identify quick wins in current workflow
- Map organizational stakeholders

**Phase 2 Extensions:**
- Add async processing and workflows
- Build candidate profiles (reusable research)
- Add incremental search for gap-filling
- Integrate with Affinity

**Compounding Value:**
- Centralized people data model
- Reusable enrichment components
- Extension to founder/LP research
- Foundation for other portfolio services

**What I Still Need to Learn:**
- How you're using Affinity today
- What your current systems look like
- Where data lives and what it looks like
- Workflow frequency and relative value
- Organizational dynamics and conversion targets

---

#### **Part 3: Q&A (15 min)**

**Anticipated Questions:**
- How does this integrate with existing tools?
- What's the cost structure?
- How do we handle edge cases?
- What's the production roadmap?
- How do we measure success?

---

### **Key Talking Points**

**On Methodology:**
- "The framework ensures we're building the right thing, not just building things right"
- "Every 'no' today is a strategic choice that enables a 'yes' tomorrow"

**On Organizational Change:**
- "Technology is easy. Adoption is hard. We design for adoption."
- "Quick wins buy credibility to do the harder work"

**On Uncertainty:**
- "The biggest determining factors are things I don't know yet—and that's expected"
- "I'm optimizing for learning velocity, not certainty"

**On Partnership:**
- "I'm not selling you a solution—I'm showing you how I think about building solutions with you"

---

## Outline 2: "The Executable Vision"

**Narrative Strategy:** Start with business pain, walk through constrained decision-making, show pragmatic execution. Emphasize judgment under uncertainty.

**Core Message:** "Great transformation requires understanding both the ideal destination and the practical path to get there."

**Audience Impact:** Best for demonstrating practical judgment, delivery focus, and ability to ship under constraints.

---

### Structure

#### **Part 1: Introduction (15 min)**

**1.1 About Will (7 min)**
- Background and relevant experience
- **Hook:** "I've built enough things that nobody used to know that execution is only half the battle—adoption is the other half"

**1.2 How I Think About VC Transformation (8 min)**

**The Reality:**
- Portfolio value = business value + technical value
- You're looking for both in your platform investments
- There are countless things I don't know about FMC
- There will be nuances that matter
- There will be failure and bumps

**The Determining Factors:**
- Understanding the "what is" (current systems, data, processes) and the "why"
- Paying your sponsors (investors, COO, platform team)
- Making headway on foundation while delivering value
- Navigating organizational dynamics (who to convert, who to accommodate)
- Understanding how FMC invests and what frustrates you

**Transition:** "Let me show you how this thinking applies to a specific use case..."

---

#### **Part 2: The Case Study (30 min)**

**2.1 The Business Problem (7 min)**

**The Context:**
- Guild network is a differentiator—use it
- People evaluation done many times, many ways (rationalize + augment = value)
- People evaluation is fundamental to VC, especially early stage

**The Pain Points:**
- Manual screening is time-consuming
- Quality varies by researcher
- Hard to audit decision trails
- Network connections get lost in noise
- Similar candidates hard to differentiate

**The Requirements:**
- Recall over precision (don't miss great matches)
- Filter candidates for review (not make the decision)
- Inform individual review (surface key info, enable quick action)
- Enable deeper investigation
- Augment, don't replace

**The Opportunity:**
- Validate research quality
- Validate evaluation quality with traces
- Cut operational cost
- Optimize execution time
- Extend to other use cases (founders, LPs, hires)

**2.2 The Constraints (5 min)**

**What I Know:**
- You use Airtable
- You're cautious about data
- I need to demonstrate value quickly
- I need to start where you are
- Ryan built things people aren't using (lesson)
- 48 hours to build a demo

**What I Don't Know:**
- Current workflow details
- Data landscape
- Affinity usage patterns
- Organizational readiness

**What I'm Betting On:**
- Can meet you in Airtable
- OpenAI Deep Research is sufficient base
- Can prototype quickly enough to get to value
- Value demonstration will inform roadmap

**2.3 The Decisions (8 min)**

**Decision 1: Scope Boundaries**
- What's central and universal? (Person intake and normalization)
- What's standard practice beyond this use case? (All people enrichment)
- What do we keep/maintain vs redo vs toss?

**Decision 2: Technical Architecture**
- Where do we need LLMs? (Research synthesis, assessment)
- Where do we need structure? (Data model, workflow)
- How do we guardrail LLMs? (Structured outputs, evidence requirements)
- How do we optimize human engagement? (Focus on review, not research)

**Decision 3: Build vs Buy**
- Build: Workflow orchestration, assessment logic
- Buy: LLM APIs (OpenAI), database (Airtable)
- Mock: Apollo enrichment (not needed for demo)
- Defer: Async processing, candidate profiles, incremental search

**Decision 4: Known Messy Corners**
- Titles will be non-normalized (handle variability)
- Disambiguation will be needed (design for it)
- This happens too often to centralize (make it easy)

**2.4 The Solution (10 min)**

**What We're Building:**
- Module 4 only: Screening workflow
- Linear flow: Role spec → Deep Research → Quality check → Assessment
- 6 Airtable tables, Flask webhook, Agno agents
- Synchronous processing (fast feedback)

**The Components:**

*Input Layer:*
- CSV ingestion with header normalization
- Role spec generation/refinement

*Research Layer:*
- OpenAI Deep Research for candidate research
- Research parser (markdown → structured data)
- Quality check with evidence threshold

*Assessment Layer:*
- Spec-guided evaluation
- Evidence-aware scoring
- Counterfactual reasoning ("why might NOT be ideal")
- Confidence scores

*Output Layer:*
- Ranked candidates with reasoning trails
- Drill-down capability
- Exportable reports

**[LIVE DEMO - 8 min]**

**Setup:**
- CFO role for Series B SaaS (growth prep)
- 8 executives (mix of Guild + network)
- 3 similar on paper (AI must differentiate)

**Story Arc:**
1. Show role spec in Airtable
2. Walk through research for 2-3 candidates
3. Show assessment with reasoning
4. Demonstrate "why #1 beat #2"
5. Show drill-down into evidence

**Success Metric:**
"I'd actually use this ranking"

---

#### **Part 3: Q&A (15 min)**

**Anticipated Questions:**
- How accurate is the research?
- What happens when it gets things wrong?
- How do you prevent hallucinations?
- What's the path to production?
- How does this scale?

---

### **Key Talking Points**

**On Constraints:**
- "Constraints are features—they force clarity and prioritization"
- "The best demos are built in 48 hours because you can't overthink them"

**On Decisions:**
- "Every technical decision is really a business decision about where to create value"
- "I optimized for learning velocity over completeness"

**On Execution:**
- "Meet them where they are" isn't just about tools—it's about credibility
- "You can build the beautiful thing, but without cred, it won't get used"

**On Next Steps:**
- "This demo informs the roadmap—it doesn't define it"
- "Real conversations about real needs will change everything"

---

## Outline 3: "The Quick Win Architect"

**Narrative Strategy:** Start with current state understanding, emphasize speed to value, show how quick wins build strategic foundation. Agile transformation approach.

**Core Message:** "The fastest path to transformation is through a series of compounding quick wins—each one building credibility and capability."

**Audience Impact:** Best for building trust through near-term delivery while demonstrating long-term strategic vision.

---

### Structure

#### **Part 1: Introduction (15 min)**

**1.1 About Will (5 min)**
- Background and relevant experience
- **Hook:** "I've learned that the best way to predict the future is to ship something small today that teaches you what to build tomorrow"

**1.2 The Quick Win Philosophy (10 min)**

**Why Quick Wins Matter:**
- Build credibility before asking for major investment
- Generate learning to inform strategy
- Create momentum for organizational change
- De-risk bigger bets through iterative validation

**The Quick Win Framework:**

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

**Transition:** "Let me show you what a Horizon 1 quick win looks like..."

---

#### **Part 2: The Case Study Journey (30 min)**

**2.1 Where You Are Today (6 min)**

**What I Understand About FMC:**
- Airtable is your operational hub
- Data conversations happen carefully
- Tools exist that aren't being adopted (Ryan's work)
- Need to prove value before changing workflows
- Portfolio companies need executive talent
- Guild network is valuable but underutilized

**What I Know About The Opportunity:**
- People evaluation happens repeatedly
- Manual screening is time-intensive
- Research quality varies
- Hard to audit decision trails
- Similar candidates are hard to differentiate

**The Quick Win Hypothesis:**
- Can demonstrate AI-augmented screening in Airtable
- Can show value in 2 days of development
- Can create template for other use cases
- Can inform broader platform strategy

**2.2 The Horizon 1 Quick Win (12 min)**

**What We're Building:**
- **Module 1:** Production-quality People CSV ingestion (smart deduplication, validation, audit trail)
- **Module 4:** AI-powered screening workflow for executive roles
- Lives in Airtable (meet you where you are)
- 48-hour build time
- Real demo with real data

**The Value Proposition:**
- Faster candidate screening (hours → minutes)
- More consistent research quality
- Auditable reasoning trails from data ingestion → final ranking
- Surfaces non-obvious differentiators
- Extensible to other use cases (founders, LPs, portfolio hires)

**The "EvolutionIQ for VC" Framing:**

*What EvolutionIQ Did for Insurance:*
- Applied AI to unstructured claims data
- Made faster, more consistent decisions
- Explainable recommendations with evidence trails
- Production-ready architecture scaled across use cases

*What We're Doing for VC Talent:*
- Applied AI to unstructured candidate data (LinkedIn, news, research)
- Faster, more consistent talent screening
- Explainable rankings with evidence and counterfactuals
- Modular architecture that extends beyond talent (founder eval, LP research)

*The Difference (Being Realistic):*
- EvolutionIQ is a mature SaaS product with years of refinement
- This is a 48-hour prototype demonstrating the **approach**
- We're showing **how** to apply structured AI workflows to VC operations
- Not claiming feature parity—claiming **directional validity**

**The Technical Approach:**

*Simplified Scope:*
- Two modules, not full platform (Module 1 + Module 4)
- Linear workflow, not complex orchestration
- Synchronous processing, not async
- No enrichment APIs (deferred to Phase 2+)
- Standard Airtable views, not custom UI

*Smart Bets:*
- OpenAI Deep Research for candidate research (2-6 min per candidate, comprehensive)
- GPT-4 for assessment and synthesis
- Pydantic for structured outputs (type safety, validation)
- Flask + ngrok for quick integration
- Agno framework for agent orchestration + native UI monitoring

*What's Different:*
- **Data Quality:** Smart CSV ingestion with deduplication and validation
- **Spec-Guided Assessment:** Role requirements drive evaluation dimensions
- **Evidence-Aware Scoring:** 1-5 scale with None for "Insufficient Evidence" (no forced guessing)
- **Counterfactual Reasoning:** "Why candidate might NOT be ideal" + key assumptions
- **Confidence Scoring:** LLM self-assessment of research quality
- **Audit Trail:** From CSV upload → research → assessment → final score

**[LIVE DEMO - 10 min]**

**The Setup:**
- 4 real portfolio scenarios (CFO/CTO roles)
- 64 real executives (Guild + network)
- Challenge: 3 similar-on-paper candidates

**The Flow:**
1. **Module 1: Data Ingestion** (1 min)
   - Show CSV upload with deduplication
   - Highlight validation: malformed LinkedIn URLs, missing companies
   - Show upload audit trail (64 records, 3 duplicates detected, 2 validation errors)

2. **Module 4: Screening Workflow** (9 min)
   - **Role Spec** - Show how CFO requirements are structured (fundraising, ops finance, stage expertise)
   - **Research** - Walk through Deep Research output for 2 candidates (citations, career timeline)
   - **Quality Check** - Show evidence sufficiency logic (did we get enough to assess?)
   - **Assessment** - Show spec-guided evaluation with evidence-backed dimension scores
   - **Ranking** - Demonstrate why #1 beat #2 with reasoning (not just scores)
   - **Drill-Down** - Show evidence trails and counterfactuals ("Why candidate might NOT be ideal")

**The Success Metric:**
"I'd actually use this ranking to prioritize my review time—and I trust the reasoning"

**2.3 The Path Forward: Horizons 2 & 3 (7 min)**

**If This Quick Win Works, What's Next?**

**Horizon 2: Foundation Building (3-6 months)**

*Phase 2A: Production-Ready Modules*
- **Module 1 Enhancement:** Real-time enrichment (Apollo, LinkedIn APIs)
- **Module 4 Enhancement:** Async processing, candidate profiles (reusable research)
- **Workflow Optimization:** Incremental search for gap-filling, quality thresholds
- **Integration:** Affinity CRM sync, custom UI for stakeholder views

*Phase 2B: Module Expansion*
- **Module 2:** Portfolio company + role uploads (not just People)
- **Module 3:** AI-powered role spec generation (from job descriptions)
- **Enrichment Layer:** Automated data quality checks, missing field detection
- **Downstream:** Placement tracking, retrospective analysis

*Phase 2C: Capability Expansion*
- **Use Case 1:** Founder research workflows (diligence support)
- **Use Case 2:** LP research workflows (fundraising support)
- **Use Case 3:** Portfolio company hire support (self-service talent matching)
- **Learning Loop:** Track placement outcomes, refine assessment criteria

**Horizon 3: Strategic Platform (6-12 months)**

*Centralized People Intelligence:*
- Normalized people database
- Reusable enrichment components
- Cross-use-case insights
- Network effect from usage

*Portfolio Value Platform:*
- Standardized people processes
- Shared research capabilities
- Portfolio company self-service
- Ecosystem integration (Affinity, CRM, etc.)

**The Learning Agenda:**
- **Value Validation:** Does this actually save time vs manual screening?
- **Trust Check:** Do evaluators trust the rankings enough to act on them?
- **Quality Benchmark:** What's the accuracy vs manual research/assessment?
- **Failure Analysis:** Where does it break down? (edge cases, missing data)
- **Data Strategy:** What does usage teach us about data quality needs?
- **Integration Planning:** How does this inform Affinity/CRM strategy?
- **Use Case Validation:** Which extensions deliver most value? (founders, LPs, portfolio hires)

**2.4 What I Need From You (5 min)**

**To Validate This Quick Win:**
- Run it against 2-3 real current searches
- Get feedback from team members who would use it
- Understand where it helps vs where it misses

**To Inform Horizon 2:**
- Understand current data landscape
- Map integration points (Affinity, other tools)
- Identify organizational stakeholders
- Prioritize use case extensions

**To Shape Horizon 3:**
- Understand FMC's platform vision
- Identify portfolio pain points beyond talent
- Map investor/COO/platform priorities
- Define success metrics for transformation

**What I'm Committing To:**
- Learning fast and adapting
- Building credibility through delivery
- Being honest about constraints
- Designing for adoption, not perfection
- Compounding value over time

---

#### **Part 3: Q&A (15 min)**

**Anticipated Questions:**
- How do you decide what's a quick win vs foundation?
- What if the quick win doesn't work?
- How do you prevent scope creep?
- What's the cost to scale this?
- How do you handle edge cases?

---

### **Key Talking Points**

**On Quick Wins:**
- "Quick wins aren't shortcuts—they're strategic learning investments"
- "The goal isn't to build perfectly, it's to learn precisely"
- "Every quick win should answer a strategic question"
- "Module 1 demonstrates production thinking; Module 4 demonstrates AI capability—together they show end-to-end competence"

**On Foundation Building:**
- "You can't build the foundation until you know what you're building on it"
- "The quick win teaches us what the foundation should look like"
- "Each horizon builds on the credibility and learning of the last"

**On Credibility:**
- "Meet them where they are" is about earning the right to lead them somewhere new
- "Ryan's tools aren't used because they skipped the credibility-building step"
- "You can't transformation-manage your way past a trust deficit"

**On Strategy:**
- "The best strategies emerge from delivered value, not planning exercises"
- "I'm optimizing for compounding learning, not comprehensive coverage"
- "Horizon 3 looks completely different after you've shipped Horizon 1"

**On Partnership:**
- "I'm not selling you this demo—I'm showing you how I approach building with you"
- "The value isn't in the prototype, it's in the thinking that produced it"

**On the EvolutionIQ Comparison:**
- "EvolutionIQ proved structured AI workflows work for high-stakes decisions in insurance—we're applying that model to VC talent operations"
- "This isn't claiming feature parity with a mature product—it's demonstrating directional validity of the approach"
- "The parallel: AI-powered structured workflows with explainable outputs for domain-specific decision-making"

---

## Comparison Matrix

| Dimension | Outline 1: Partner | Outline 2: Executor | Outline 3: Quick Win |
|-----------|-------------------|---------------------|---------------------|
| **Opening Energy** | Strategic Framework | Business Problem | Current State |
| **Core Narrative** | Methodology → Application | Pain → Solution | Today → Tomorrow |
| **Demo Position** | Framework Validation | Solution Proof | H1 Quick Win |
| **What You Sell** | Strategic Partnership | Execution Capability | Incremental Value |
| **Risk** | Too Abstract | Too Tactical | Too Cautious |
| **Strength** | Shows Depth | Shows Judgment | Shows Pragmatism |
| **Best For** | COO/Strategic Hire | Investor/Delivery Focus | Platform/Product Hire |
| **Emotional Arc** | Trust → Confidence | Pain → Relief | Uncertainty → Momentum |
| **Demo Length** | 4 min (illustration) | 8 min (centerpiece) | 10 min (proof point) |
| **Next Steps Emphasis** | Learning Agenda | Production Path | Horizon Planning |
| **Differentiation** | Systematic Thinker | Pragmatic Builder | Strategic Incrementalist |

---

## Recommendations

**If FMC values strategic thinking and partnership:**
→ Use **Outline 1** (The Transformation Partner)

**If FMC values execution and delivery:**
→ Use **Outline 2** (The Executable Vision)

**If FMC values de-risked progress and learning:**
→ Use **Outline 3** (The Quick Win Architect)

**Hybrid Approach:**
Consider taking the **framework from Outline 1** (5 Questions), the **constraints section from Outline 2** (decision clarity), and the **horizon planning from Outline 3** (compounding value).

---

## Key Themes Across All Outlines

**Preserved Core Strengths:**
- Understanding before solving
- Meeting them where they are (Airtable)
- Honest about unknowns
- Focus on adoption, not perfection
- Augmentation, not replacement
- Quick wins build credibility

**Enhanced Elements:**
- Clearer narrative arc in each version
- More explicit value proposition
- Better emotional engagement
- Stronger differentiation of approach
- More actionable next steps
- Better setup for demo as climax

**Consistent Talking Points:**
- "Technology is easy. Adoption is hard."
- "Meet them where they are"
- "Quick wins buy credibility for harder work"
- "Optimizing for learning velocity"
- "Every 'no' today enables a 'yes' tomorrow"
