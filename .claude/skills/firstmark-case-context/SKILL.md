---
name: firstmark-case-context
description: Context and requirements for the FirstMark Capital Talent Signal Agent case study. Includes case specifications, evaluation rubric (25% product thinking, 25% technical design, 20% data integration, 20% insight generation, 10% communication), deliverable checklists, FirstMark firm context, and mock data structures. This skill should only be invoked explicitly when working on the FirstMark case study deliverables or when mentioned in conversation.
---

# FirstMark Case Context

## Overview

This skill provides all context, requirements, and resources specific to the FirstMark Capital "Talent Signal Agent" case study. Use this skill when working on any aspect of the case study deliverables.

**Case Due:** November 19, 2025, 5:00 PM
**Reviewers:** Beth Viner, Shilpa Nayyar, Matt Turck, Adam Nelson (optional)

**Core Challenge:** Build an AI-powered agent that helps FirstMark's talent team proactively surface executive matches (CTO, CFO) for open roles across their portfolio companies by integrating structured and unstructured data.

## Case Study Requirements

### The Problem

FirstMark's network includes:
- Portfolio company executives
- Members of FirstMark Guilds (role-based peer groups: CTO, CPO, CRO, etc.)
- Broader professional networks (LinkedIn, founders, event attendees)

**Goal:** Automatically identify which executives in this extended network could be strong candidates for open roles in portfolio companies and surface those insights with clear reasoning.

### What to Build

Design and demonstrate a "Talent Signal Agent" that can:

1. **Integrate Data Sources**
   - Structured: Company data, role specifications, hiring needs
   - Unstructured: Executive bios, articles, LinkedIn profiles, job descriptions

2. **Identify & Rank Candidates**
   - Match executives to open CTO and CFO roles
   - Rank candidates by fit quality
   - Provide scores/grades

3. **Explain Reasoning**
   - Clear reasoning trails for each match
   - Explainable scoring logic
   - Transparent decision-making

**Important:** Use mock/synthetic data. The goal is to demonstrate reasoning, architecture, and usability—not data volume or perfection.

## Required Deliverables

### Deliverable 1: Write-Up or Slide Deck (1-2 pages)

**Required Sections:**

- [ ] **Problem Framing & Agent Design**
  - How you understand the VC talent workflow
  - Why your approach fits the use case
  - Key assumptions made

- [ ] **Data Sources & Architecture**
  - How structured + unstructured data are integrated
  - Technical architecture diagram or description
  - Data flow overview

- [ ] **Key Design Decisions & Tradeoffs**
  - Why you chose specific patterns/approaches
  - What you prioritized and why
  - What you simplified or excluded

- [ ] **Production Extension Plan**
  - How you'd scale this beyond the prototype
  - What would change in production
  - Next steps and improvements

**Format:** Markdown document OR slide deck (PDF/PowerPoint)

### Deliverable 2: Lightweight Python Prototype

**Required Functionality:**

- [ ] **Data Ingestion**
  - Load structured data (CSVs)
  - Load unstructured data (text files, JSONs)
  - Parse and normalize inputs

- [ ] **Matching Logic**
  - Compare candidates against role requirements
  - Apply scoring/ranking algorithm
  - Generate match recommendations

- [ ] **Explainable Output**
  - Ranked list of candidate matches per role
  - Score/rating for each match
  - Reasoning explaining why the match is strong/weak
  - Example: "Jane Doe → strong fit for CFO @ AcmeCo because of prior Series B fundraising experience at consumer startup"

**Technical Requirements:**
- Python-based
- Can use LangChain, LlamaIndex, or vanilla Python + OpenAI/Anthropic
- Should run with `python main.py` or similar simple command
- Include requirements.txt

### Deliverable 3: README or Loom Video (Optional but Recommended)

**Should Explain:**

- [ ] What's implemented vs what's conceptual
- [ ] How to run the code
- [ ] What the output looks like
- [ ] Key design decisions

## Evaluation Rubric

| Criterion | Weight | What "Excellent" Looks Like | How to Demonstrate |
|-----------|--------|----------------------------|-------------------|
| **Product Thinking** | 25% | Clear understanding of VC and talent workflows. Scopes an agent that actually fits how the firm works. Communicates assumptions and value. | - Show understanding of FirstMark's guilds, portfolio, network<br>- Explain why this approach solves real pain points<br>- Identify edge cases and limitations<br>- Discuss user experience for talent team |
| **Technical Design** | 25% | Uses modern LLM/agent frameworks logically; modular design; thoughtful about retrieval, context, and prompting. | - Apply ai-agent-architect principles (KISS, YAGNI)<br>- Justify complexity level chosen<br>- Show modular, clean architecture<br>- Smart prompt engineering<br>- Appropriate use of RAG if needed |
| **Data Integration** | 20% | Handles structured + unstructured data elegantly (e.g., vector store, metadata joins). Sensible about what's automatable. | - Clean CSV parsing and normalization<br>- Text processing for bios/job descriptions<br>- Metadata enrichment<br>- If using vector search, explain why<br>- Show data flow clearly |
| **Insight Generation** | 20% | Produces useful, explainable, ranked outputs — not just text dumps. Demonstrates reasoning or scoring logic. | - Clear ranking/scoring system<br>- Structured output format<br>- Detailed reasoning for matches<br>- Actionable insights<br>- Not just "this person might be good" |
| **Communication & Clarity** | 10% | Clean, clear explanation of what was done, why, and next steps. No jargon for the sake of it. | - Well-organized write-up<br>- Clear architecture diagrams<br>- Code is readable and documented<br>- Explain tradeoffs honestly<br>- README that actually helps |

**Total:** 100%

### Rubric Strategy

**How to maximize each criterion:**

**Product Thinking (25%):**
- Reference FirstMark's guilds and portfolio explicitly
- Explain how talent team would actually use this
- Discuss iteration and feedback loops
- Show you understand VC talent challenges (passive candidates, executive-level matching, relationship-first culture)

**Technical Design (25%):**
- Follow ai-agent-architect skill principles (start simple)
- Don't over-engineer (they want to see thinking, not complexity)
- Use the right tool for the job (prompt chain might beat multi-agent)
- Show modular design that's easy to extend

**Data Integration (20%):**
- Demonstrate both structured and unstructured data handling
- Show thoughtful data modeling (how you represent candidates, roles)
- If using embeddings, explain why keyword search wasn't enough
- Clean code for data processing

**Insight Generation (20%):**
- Create structured output format (JSON, DataFrame, or similar)
- Provide numerical scores AND qualitative reasoning
- Rank candidates clearly (1st choice, 2nd choice, etc.)
- Make it actionable (talent team should know who to call first)

**Communication (10%):**
- Clear, concise writeup (1-2 pages means 1-2 pages)
- No unnecessary jargon
- Diagrams if they help (but not required)
- Be honest about limitations

## Mock Data Requirements

### Structured Data Files

**1. `mock_guilds.csv` - FirstMark Guild Members**

Example structure:
```csv
name,current_company,current_title,location,seniority,function,linkedin_url,guild
Sarah Chen,Stripe,VP Engineering,San Francisco,VP,Engineering,https://linkedin.com/in/sarahchen,CTO Guild
Marcus Johnson,Plaid,CFO,New York,C-Suite,Finance,https://linkedin.com/in/marcusj,CFO Guild
```

**Columns:**
- name: Full name
- current_company: Where they work now
- current_title: Their current role
- location: City/region
- seniority: (IC, Manager, Director, VP, C-Suite)
- function: (Engineering, Finance, Product, Revenue, Operations)
- linkedin_url: Mock LinkedIn URL
- guild: Which FirstMark guild they're in

**Size:** 15-20 executives across CTO and CFO guilds

---

**2. `exec_network.csv` - Extended Network (Partner Connections)**

Example structure:
```csv
name,current_title,current_company,role_type,location,linkedin_url,connection_source
Elena Rodriguez,CTO,TechCorp,CTO,Austin,https://linkedin.com/in/elena,Partner Network
David Kim,VP Finance,ScaleUp Inc,CFO,Boston,https://linkedin.com/in/davidkim,Event Attendee
```

**Columns:**
- name: Full name
- current_title: Current role
- current_company: Current employer
- role_type: (CTO, CFO, CRO, CPO, etc.)
- location: City/region
- linkedin_url: Mock URL
- connection_source: (Partner Network, Guild, Event Attendee, LinkedIn)

**Size:** 10-15 additional executives

---

**3. `open_roles.csv` - Portfolio Company Open Positions**

Example structure:
```csv
role_id,company,role_title,role_type,location,stage,industry,required_experience,nice_to_have
CFO_001,AcmeCo,Chief Financial Officer,CFO,New York,Series B,FinTech,10+ years finance; Series B+ exp,Consumer fintech background
CTO_002,DataFlow,Chief Technology Officer,CTO,San Francisco,Series C,Data Infrastructure,15+ years eng; scaled 50+ eng teams,Open source contributions
```

**Columns:**
- role_id: Unique identifier
- company: Portfolio company name (use real FirstMark portfolio or mock names)
- role_title: Official title
- role_type: (CFO, CTO)
- location: Where the role is based
- stage: (Seed, Series A, Series B, Series C, etc.)
- industry: (FinTech, SaaS, Data, Consumer, etc.)
- required_experience: Key requirements
- nice_to_have: Bonus qualifications

**Size:** 3-5 open roles (2-3 CTO, 2-3 CFO)

### Unstructured Data Files

**1. `executive_bios.json` - Biographical Text**

Example structure:
```json
[
  {
    "name": "Sarah Chen",
    "bio": "Sarah Chen is VP of Engineering at Stripe, where she leads a team of 200+ engineers building payment infrastructure. Prior to Stripe, Sarah was Director of Engineering at Square, scaling the platform from Series B through IPO. She holds a BS in Computer Science from Stanford and has been recognized in Forbes 30 Under 30. Sarah is passionate about building diverse engineering teams and has spoken at QCon and Strange Loop on engineering leadership.",
    "source": "LinkedIn About + Press"
  },
  {
    "name": "Marcus Johnson",
    "bio": "Marcus Johnson serves as CFO at Plaid, overseeing all financial operations and strategic planning. He joined Plaid pre-Series B and helped raise $425M in growth funding. Previously, Marcus was VP of Finance at Robinhood during hypergrowth, managing a team through Series C and D rounds. He started his career in investment banking at Goldman Sachs. Marcus holds an MBA from Wharton and a BA in Economics from Yale.",
    "source": "Company bio + LinkedIn"
  }
]
```

**Fields:**
- name: Match to CSV data
- bio: 2-4 sentences with career highlights, achievements, background
- source: Where this info came from (for realism)

**Size:** 10-20 bios covering both guild members and extended network

---

**2. `job_descriptions/` - Role Descriptions**

Example file: `job_descriptions/CFO_AcmeCo.txt`

```
Chief Financial Officer - AcmeCo

AcmeCo is a fast-growing FinTech startup revolutionizing consumer payments. We've raised $45M Series B and are scaling rapidly (150% YoY growth).

We're seeking an experienced CFO to:
- Lead all financial planning and analysis
- Manage Series C fundraising ($75M+ target)
- Build finance team from 3 to 15+ people
- Establish financial controls and reporting for growth stage
- Partner with CEO and board on strategic planning

Requirements:
- 10+ years progressive finance experience
- Experience as CFO or VP Finance at Series B+ startup
- Track record of successful fundraising (Series B, C, or later)
- Built finance teams from scratch
- FinTech or consumer tech background preferred
- Comfort with high-growth, fast-paced environment

Compensation: $250-350K base + equity
Location: New York (hybrid, 3 days in office)
Reports to: CEO
```

**Size:** 3-5 job descriptions (one per open role in `open_roles.csv`)

**Format:** Plain text files, realistic startup job postings

## FirstMark Context

### About FirstMark

**Focus:** Early-stage B2B and infrastructure companies
**Stage:** Seed through Series B
**Check Size:** $1M - $15M
**Geography:** Primarily US, with global portfolio

**Key Differentiators:**
- Platform team (talent, marketing, ops support)
- FirstMark Guilds (peer networks for executives)
- Long-term partnership approach
- Deep domain expertise in data, infrastructure, dev tools

### Portfolio Highlights (Sample - Use for Mock Data)

**Data & Infrastructure:**
- Airflow (Apache)
- Astronomer
- DataDog (IPO)
- Looker (acquired by Google)

**FinTech:**
- Betterment
- Ramp
- Narmi

**Developer Tools:**
- Gitlab
- Klaviyo (IPO)
- Contentful

**Consumer:**
- Pinterest (IPO)
- Shopify
- Ro

### FirstMark Guilds

**What they are:** Role-based peer groups where executives from portfolio companies meet regularly to share knowledge, challenges, and best practices.

**Active Guilds:**
- CTO Guild
- CPO Guild (Chief Product Officer)
- CFO Guild
- CRO Guild (Chief Revenue Officer)
- CMO Guild

**Relevance to Case:**
- Guild members are high-quality, pre-vetted executives
- They know FirstMark's portfolio and values
- They're warm intros (not cold outreach)
- Guild participation signals engagement with FirstMark ecosystem

### Talent Team Workflow (Context for Product Thinking)

**Current Process (Manual):**
1. Portfolio company posts open executive role
2. Talent team reviews role requirements
3. Team manually reviews guild membership lists
4. Check partner networks and LinkedIn
5. Send individual messages to gauge interest
6. Make warm introductions

**Pain Points:**
- Time-consuming manual review
- Can't easily search across bios/backgrounds
- May miss good fits in extended network
- Hard to explain "why this match" systematically
- No ranking/prioritization system

**What Success Looks Like:**
- Faster identification of potential matches
- More coverage (don't miss people in extended network)
- Clear reasoning to explain to both candidate and company
- Ranked shortlist to prioritize outreach
- Warm intro context preserved (not cold spam)

## Implementation Guidance

### Mapping Rubric to Technical Decisions

**To score well on Product Thinking (25%):**
- Explicitly mention guilds, portfolio companies, warm intros
- Design for talent team use (not generic recruiting)
- Acknowledge that this is relationship-first, not spam
- Show understanding of executive-level matching nuances

**To score well on Technical Design (25%):**
- Apply KISS principle: Use simplest approach that works
- If using prompt chains: Explain why steps are separated
- If using RAG: Explain what you're retrieving and why
- If using agents: Justify the agentic pattern
- Show you chose complexity level intentionally

**To score well on Data Integration (20%):**
- Clean data loading and normalization code
- Smart use of both CSV metadata AND bio text
- If using embeddings: Show both structured filters AND semantic search
- Demonstrate thoughtful data modeling

**To score well on Insight Generation (20%):**
- Create structured match output (not just LLM text dump)
- Provide scores/rankings
- Give detailed, specific reasoning
- Make output actionable (talent team knows what to do)

**To score well on Communication (10%):**
- 1-2 pages means 1-2 pages (not 10)
- Clear, simple language
- Explain tradeoffs honestly
- Good README

### Common Pitfalls to Avoid

**❌ Over-Engineering:**
- Don't build a full multi-agent orchestration if prompt chains work
- Don't use vector DB if you have < 50 candidates
- Don't build complex RAG if simple filtering + LLM works

**❌ Under-Explaining:**
- Don't just show code without explaining *why*
- Don't skip the reasoning for matches
- Don't forget to address the rubric criteria explicitly

**❌ Generic Solution:**
- Don't build "generic recruiting tool"
- Don't ignore FirstMark-specific context (guilds, warm intros)
- Don't forget this is VC talent, not corporate recruiting

**❌ Perfect Data Obsession:**
- Don't spend all time on realistic mock data
- Don't build actual web scrapers for real LinkedIn profiles
- Focus on demonstrating the logic, not data perfection

**❌ Jargon Overload:**
- Don't use buzzwords without explaining them
- Don't assume they know all LLM/agent terminology
- Explain clearly what you built and why

### Recommended Approach (Based on ai-agent-architect Principles)

**Phase 1: Start Simple (Get 80% of value)**

Use basic prompt chain:
1. Load structured data (CSVs)
2. Load unstructured data (bios, job descriptions)
3. For each open role:
   - Filter candidates by basic criteria (role type, location)
   - Create prompt with role requirements + candidate bios
   - Ask LLM to score and explain matches
4. Rank by score, output top candidates

**Phase 2: Add Complexity Only If Needed**

If basic approach works but has issues:
- Issue: Too many candidates → Add vector search to pre-filter
- Issue: Scoring inconsistent → Add structured output + few-shot examples
- Issue: Need multi-step reasoning → Add ReAct agent pattern

**Phase 3: Polish**

- Clean output format (JSON, CSV, or nice text)
- Add error handling
- Write clear README
- Document design decisions

**Remember:** They want to see your thinking process, not perfect code.

## Resources

### references/

**`case_brief.md`** - Full case study requirements extracted from the PDF brief.

**`firstmark_context.md`** - Detailed information about FirstMark (portfolio, guilds, platform team).

**`role_context.md`** - AI Builder role description and what they're looking for in candidates.

**`data_specifications.md`** - Detailed specifications for mock data generation.

### assets/

**`mock_data_examples/`** - Example CSV and JSON file structures with sample data.

**`writeup_template.md`** - Template structure for the 1-2 page deliverable.

**`architecture_diagram_template.md`** - Optional architecture diagram guidance.

### scripts/

**`generate_mock_data.py`** - Generates realistic synthetic data for all required files.

**`validate_deliverables.py`** - Checklist script to ensure all requirements are met before submission.

---

## Quick Reference Checklist

**Before Starting:**
- [ ] Read full case brief (references/case_brief.md)
- [ ] Understand FirstMark context (references/firstmark_context.md)
- [ ] Review evaluation rubric (this document)
- [ ] Decide on technical approach using ai-agent-architect principles

**During Development:**
- [ ] Generate mock data (scripts/generate_mock_data.py)
- [ ] Build minimal prototype first
- [ ] Test with 2-3 examples
- [ ] Validate output format is useful
- [ ] Add complexity only if needed

**Before Submission:**
- [ ] Run deliverables validation (scripts/validate_deliverables.py)
- [ ] Check all rubric criteria are addressed
- [ ] Ensure 1-2 page writeup is actually 1-2 pages
- [ ] Test that code runs with simple command
- [ ] Write clear README
- [ ] Review submission by Nov 19, 5:00 PM

**Submission Checklist:**
- [ ] Write-up or slide deck (1-2 pages)
- [ ] Python prototype with requirements.txt
- [ ] README or Loom video explanation
- [ ] Mock data files
- [ ] Code is runnable

---

**Remember:** This is a case study to demonstrate thinking, not build production software. Show your process, explain your decisions, and make it clear why your approach fits FirstMark's actual use case.
