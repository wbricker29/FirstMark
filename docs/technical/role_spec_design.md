# Role Spec Feature Design Document

**Version:** 1.1
**Date:** 2025-11-16
**Author:** Will Bricker
**Project:** FirstMark Talent Signal Agent

---

## 1. Overview

### Purpose

A **Role Spec** is a structured evaluation framework that defines what "good fit" means for a specific executive role. It enables consistent candidate assessment by both human reviewers and AI agents.

### Goals

- Provide standardized evaluation criteria for CFO/CTO roles
- Enable AI to produce explainable, dimension-level assessments
- Balance reusability (templates) with customization (role-specific needs)
- Integrate seamlessly with Airtable-based workflow
- Keep evaluations grounded in realistically observable, web-available signals

### Non-Goals (for demo)

- Version control system
- Collaborative editing features
- Analytics on spec effectiveness
- Dynamic AI-generated specs

### V1 Implementation Note

**Score Calculation:** v1.0-minimal uses **simple average × 20 algorithm**, ignoring dimension weights. Weights are preserved in role specs for Phase 2+ weighted calculation enhancement.

**Function:** `calculate_overall_score()` - Simple average of scored dimensions (None/Unknown excluded)

**Phase 2+:** Weighted scoring algorithm will use dimension weights defined in role specs.

---

## 2. Requirements

### Functional Requirements

- **FR1:** Create role specs from pre-built templates (CFO, CTO)
- **FR2:** Customize specs by editing dimensions, weights, and criteria
- **FR3:** Store specs in format consumable by both humans and LLMs
- **FR4:** Link specs to active searches for candidate evaluation
- **FR5:** Support 4-6 weighted evaluation dimensions per spec
- **FR6:** Include must-haves, nice-to-haves, and red flags
- **FR7:** For each dimension, define how observable it is from public/web data and allow the system to return “unknown/insufficient evidence” rather than forcing a score

### Technical Requirements

- **TR1:** Store in Airtable (no additional database)
- **TR2:** Use markdown format for LLM parsing
- **TR3:** Enable duplication for customization
- **TR4:** Support GPT-5 structured evaluation prompts

### User Experience Requirements

- **UX1:** Templates get user to 80% complete spec in <2 min
- **UX2:** Customization is intuitive (edit text, no complex UI)
- **UX3:** Spec is readable in Airtable without external tools

---

## 3. Design

### 3.1 Data Model

#### Role Spec Schema

| Field | Type | Description |
|-------|------|-------------|
| `spec_id` | Auto-number | Primary key |
| `spec_name` | Text | e.g., "Series B SaaS CFO" |
| `base_role_type` | Single Select | CTO, CFO, CPO, CRO |
| `company_stage` | Single Select | Seed, A, B, C, Growth |
| `sector` | Single Select | SaaS, Consumer, Fintech, etc. |
| `is_template` | Checkbox | Reusable template vs one-off |
| `structured_spec_markdown` | Long Text | Full spec in markdown format |
| `search_instructions` | Long Text | Additional AI guidance |
| `created_date` | Created Time | Auto-populated |
| `last_modified` | Last Modified | Auto-populated |

### 3.2 Spec Template Structure

```markdown
# Role Spec: [Role Type] @ [Company Context]

## Role Context
[2-3 sentences: role description, company stage, key challenges]

## Evaluation Framework

### 1. [Dimension Name] (Weight: X%)
**Definition:** [What this measures]
**Evidence Level:** [High / Medium / Low]  <!-- How reliably this dimension can be assessed from public/web data -->
**Evidence Hints:** [1–2 examples of signals to look for (e.g., funding rounds led, team size, public talks)]
**Scale:**
- 5 (Exceptional): [Criteria using observable signals]
- 4 (Strong): [Criteria using observable signals]
- 3 (Adequate): [Criteria using observable signals]
- 2 (Weak): [Criteria using observable signals]
- 1 (Poor): [Criteria using observable signals]
- _Leave blank (null/None) if insufficient public evidence to score_
- _DO NOT use 0, NaN, or empty string - use null/None for unknown_

[Repeat for 4-6 dimensions, weights sum to 100%]

## Must-Haves
- [ ] Requirement 1
- [ ] Requirement 2

## Nice-to-Haves
- Prior experience with [X]
- Track record of [Y]

## Red Flags
- [Disqualifying factor 1]
- [Disqualifying factor 2]
```

### 3.3 Standard Dimensions

#### CFO Roles (6 dimensions)

Below are standard CFO dimensions with their intended weight in the *human* spec and an **Evidence Level** indicating how reliably they can be scored from public/web data.

1. **Fundraising & Investor Relations (25%, Evidence: High)**  
   - Capital raising track record, board experience, investor-facing role.  
   - Web signals: funding announcements, IPO/M&A news, press quotes about “led financing,” board memberships.
2. **Operational Finance & Systems (20%, Evidence: Medium)**  
   - FP&A, unit economics, finance systems and processes.  
   - Web signals: mentions of “built FP&A function,” “implemented ERP/BI systems,” transformation case studies. Likely sparse; often “Unknown.”
3. **Strategic Business Partnership (15%, Evidence: Low)**  
   - Cross-functional influence, CEO partnership, strategic decision-making.  
   - Web signals: occasional quotes about being a “trusted partner,” but mostly internal. Use primarily for qualitative commentary; automated scoring may often be Unknown (null/None).
4. **Financial Leadership Scope (15%, Evidence: Medium)**  
   - Team size, org-building, process maturity.  
   - Web signals: “built finance team from X→Y,” “first finance hire,” “global team,” leadership awards.
5. **Sector / Domain Expertise (15%, Evidence: High)**  
   - Industry relevance, GTM familiarity.  
   - Web signals: company/sector, recurring themes across roles (e.g., B2B SaaS, consumer, fintech).
6. **Growth Stage Exposure (10%, Evidence: High)**  
   - Scaling experience (B→D, pre-IPO, etc.), change management.  
   - Web signals: stage labels in press (Series A/B/C, growth equity), “took company from X to Y ARR,” IPO/M&A timing.

#### CTO Roles (6 dimensions)

Similarly, CTO dimensions are defined with Evidence Levels:

1. **Technical Leadership & Architecture (25%, Evidence: Medium)**  
   - Technical depth, architecture decisions, technical vision.  
   - Web signals: talks, blog posts, open-source work, architecture write-ups; may be thin for some candidates.
2. **Team Building & Engineering Culture (20%, Evidence: Low)**  
   - Hiring, retention, culture-building.  
   - Web signals: references to “scaled team from X→Y,” hiring campaigns; most rich signals are internal → expect many Unknowns and rely on human judgment.
3. **Execution & Delivery (15%, Evidence: Low)**  
   - Shipping velocity, quality of delivery, tech debt tradeoffs.  
   - Web signals: release notes, case studies, but usually not enough for precise scoring → primarily qualitative commentary.
4. **Product Partnership (10%, Evidence: Low)**  
   - Partnership with PM, customer empathy, product thinking.  
   - Web signals: interviews, talks referencing customer work; mostly a human-interview dimension.
5. **Scalability & Growth Experience (15%, Evidence: High)**  
   - Handling scale (users, data, global footprint), infra scaling.  
   - Web signals: “grew platform from X to Y,” global traffic claims, scale-focused case studies.
6. **Domain / Tech Stack Fit (15%, Evidence: High)**  
   - Alignment with tech stack and domain (ML, infra, SaaS, etc.).  
   - Web signals: company’s product, stated stack, open-source repos, personal profiles.

> Note: We keep the full, richer spec for humans, but the automated scoring pipeline may reweight dimensions to emphasize **High** and **Medium** evidence dimensions and treat **Low** evidence dimensions as “qualitative, often Unknown.”

### 3.5 Grounding in Web-Available Evidence

- Each dimension should explicitly call out:
  - **Evidence Level** (High/Medium/Low) as above.
  - **Evidence Hints** that reference concrete web signals.
- The LLM is instructed to:
  - Use only evidence it can actually infer (or quote) from the provided research and context.
  - Return `null` (JSON) / `None` (Python) when there is insufficient public evidence, rather than guessing.
  - **DO NOT use:** NaN, 0, or empty values - use `null`/`None` exclusively for unknown scores.
- The scoring engine:
  - Aggregates dimension scores but ignores or down-weights `None`/`null` dimensions in the numeric total.
  - Still surfaces those dimensions in the explanation so humans know where additional internal data or references are needed.
  - Only dimensions with non-None scores contribute to the overall weighted average.

### 3.4 User Flows

#### Flow A: Create from Template

```
1. Navigate to Role Specs table
2. Click "New from Template" button
3. Select template (Series B CFO, Series B CTO, etc.)
4. System creates record with pre-filled markdown
5. User edits markdown (adjust weights, criteria, must-haves)
6. Save
```

#### Flow B: Link to Search

```
1. Create Search record (links to Role + Portco)
2. Select Role Spec from dropdown (existing specs)
3. Optionally add custom instructions
4. Click "Start Screening" to evaluate candidates
```

#### Flow C: Duplicate & Customize

```
1. Find similar existing spec
2. Click "Duplicate" button
3. System creates copy with "- Copy" suffix
4. Edit as needed
5. Save as new spec
```

---

## 4. Implementation

### 4.1 Airtable Setup

#### Tables & Views

**Role Specs Table**

- Grid View (default): All specs
- Template Library View: Filter `is_template = true`
- By Role Type View: Group by `base_role_type`

**Automation: Duplicate Spec**

```
Trigger: Button field clicked
Actions:
1. Create new record
2. Copy fields: spec_name (+ " - Copy"), base_role_type,
   company_stage, sector, structured_spec_markdown
3. Set is_template = false
```

**Interface (optional for demo)**

- Spec detail view with markdown preview
- Template gallery for quick selection

### 4.2 Template Creation

**Pre-build 4 templates:**

1. `Series A/B SaaS CFO` (is_template=true)
2. `Series B/C SaaS CTO` (is_template=true)
3. `Growth Stage CFO - Consumer` (is_template=true)
4. `Early Stage CTO - Infrastructure` (is_template=true)

**Customize 4 specs for demo roles:**

- Pigment - CFO (from template #1, customized)
- Mockingbird - CFO (from template #3, customized)
- Synthesia - CTO (from template #2, customized)
- Estuary - CTO (from template #4, customized)

### 4.3 Python Integration

#### Spec Parser Module & Prompt Payload

```python
# spec_parser.py

def parse_role_spec(markdown_text: str) -> dict:
    """
    Parse markdown spec into structured dict for AI consumption.

    Returns:
        {
            'role_context': str,
            'dimensions': [
                {
                    'name': str,
                    'weight': float,           # Human-design weight
                    'evidence_level': str,     # "High" | "Medium" | "Low"
                    'definition': str,
                    'scale': {5: str, 4: str, 3: str, 2: str, 1: str}
                }
            ],
            'must_haves': list[str],
            'nice_to_haves': list[str],
            'red_flags': list[str]
        }
    """
    # Use regex to extract sections
    # Parse dimension headers for weights
    # Extract scale definitions
    # Return structured dict that downstream agents can consume
    ...

def build_assessment_payload(spec: dict, research_data: str) -> str:
    """Package role spec + research into the user content sent to Agno agents."""

    payload = [
        "ROLE SPECIFICATION:",
        spec["role_context"],
        "",
        "DIMENSIONS:",
    ]

    for dim in spec["dimensions"]:
        payload.extend(
            [
                f"- {dim['name']} (Weight: {dim['weight']}%)",
                f"  Definition: {dim['definition']}",
                f"  Evidence Level: {dim['evidence_level']}",
                "",
                "  Scale:",
                format_scale(dim["scale"]),
                "",
            ]
        )

    payload.extend(
        [
            "",
            "CANDIDATE RESEARCH:",
            research_data.strip(),
        ]
    )

    return "\n".join(payload)
```

#### Assessment Module + Centralized Prompt Templates

```python
# assessment.py
from demo.agents import create_assessment_agent

def assess_candidate(
    candidate_research: str,
    role_spec_markdown: str,
    custom_instructions: str = ""
) -> dict:
    """Run the Agno-driven assessment against the canonical prompt catalog."""

    spec = parse_role_spec(role_spec_markdown)
    payload = build_assessment_payload(spec, candidate_research)

    if custom_instructions:
        payload += f"\n\nCUSTOM INSTRUCTIONS:\n{custom_instructions}"

    assessment_agent = create_assessment_agent()

    # Agno handles ReasoningTools + structured output (AssessmentResult)
    result = assessment_agent.run(payload)
    assessment = result.content

    return assessment
```

> **Note:** The scoring instructions (1–5 scale, evidence-aware handling, ReasoningTools hints) live in `demo/prompts/catalog.yaml` under the `assessment` entry. Update that YAML when rubric language changes; agent factories automatically pick up the new template.

### 4.4 Webhook Integration

```python
# demo/agentos_app.py (FastAPI/AgentOS endpoint)

from fastapi import BackgroundTasks, Depends, FastAPI

from demo.models import ScreenWebhookPayload
from demo.screening_service import process_screen_direct

@fastapi_app.post("/screen", response_model=None, status_code=202)
def screen_endpoint(
    payload: ScreenWebhookPayload,
    background_tasks: BackgroundTasks,
    _auth: None = Depends(verify_bearer_token),
) -> dict[str, Any] | JSONResponse:
    """Triggered when 'Ready to Screen' automation fires in Airtable."""

    candidates = payload.get_candidates()

    background_tasks.add_task(
        process_screen_direct,
        screen_id=payload.screen_id,
        role_spec_markdown=payload.spec_markdown,
        candidates=candidates,
        custom_instructions=payload.custom_instructions,
        airtable=airtable_client,
        logger=logger,
        symbols=SCREEN_LOG_SYMBOLS,
        candidate_runner=candidate_workflow_runner.run_candidate_workflow,
    )

    return {
        "status": "accepted",
        "message": "Screen workflow started",
        "screen_id": payload.screen_id,
        "candidates_queued": len(candidates),
    }
```

**Key differences from earlier iterations:**
- Spec markdown, role info, and candidate data arrive pre-assembled via `ScreenWebhookPayload` so **no Airtable reads** occur during screening.
- `process_screen_direct()` handles status flips, automation logging, validation, and candidate batching in one place.
- FastAPI returns 202 immediately; the AgentOS control plane (and Airtable logs) track completion asynchronously.

### 4.5 Structured Output Schema

**NOTE:** All structured output schemas have been migrated to Pydantic models in `spec/dev_reference/implementation_guide.md` (lines 256-427).

**Key Models for Role Spec Integration:**

```python
# From spec/dev_reference/implementation_guide.md

from pydantic import BaseModel, Field
from typing import Optional, Literal

class DimensionScore(BaseModel):
    """Evidence-aware dimension score."""
    dimension: str
    score: Optional[int] = Field(None, ge=1, le=5)
    # None (Python) / null (JSON) = Unknown / Insufficient evidence
    # DO NOT use NaN, 0, or empty values
    evidence_level: Literal["High", "Medium", "Low"]  # From spec
    confidence: Literal["High", "Medium", "Low"]
    reasoning: str
    evidence_quotes: list[str]
    citation_urls: list[str]

class AssessmentResult(BaseModel):
    """Structured assessment from gpt-5-mini."""
    overall_score: Optional[float] = Field(None, ge=0, le=100)
    overall_confidence: Literal["High", "Medium", "Low"]
    dimension_scores: list[DimensionScore]
    must_haves_check: list[MustHaveCheck]
    red_flags_detected: list[str]
    green_flags: list[str]
    summary: str
    counterfactuals: list[str]
```

**Usage with Agno:**

```python
from agno import Agent, OpenAIResponses

assessment_agent = Agent(
    model=OpenAIResponses(id="gpt-5-mini"),
    tools=[{"type": "web_search_preview"}],
    instructions="Evaluate candidate against role spec...",
    response_model=AssessmentResult,  # Pydantic model
)
```

**See full schema definitions in:** `spec/dev_reference/implementation_guide.md`

---

## 5. Testing & Validation

### 5.1 Test Cases

**TC1: Template Usage**

- Action: Create spec from "Series B SaaS CFO" template
- Expected: Record created with pre-filled markdown, all 6 dimensions present

**TC2: Customization**

- Action: Edit template spec, change weight from 25% to 30%
- Expected: Markdown updates, parser extracts correct weight

**TC3: AI Parsing**

- Action: Run `parse_role_spec()` on template markdown
- Expected: Returns dict with 6 dimensions, weights sum to 100%

**TC4: Assessment Integration**

- Action: Run screening with custom spec
- Expected: Assessment includes all spec dimensions, weighted score calculated

**TC5: Must-Haves Validation**

- Action: Assess candidate missing must-have
- Expected: `must_haves_check` shows false for that requirement

### 5.2 Demo Validation

**Success Criteria:**

- [ ] 4 specs created (1 per demo role)
- [ ] All specs parse correctly via Python
- [ ] Assessment returns dimension-level scores
- [ ] Weighted overall score calculated accurately
- [ ] Reasoning references spec definitions
- [ ] Demo shows template → customize → evaluate flow

---

## 6. Future Considerations

### Production Enhancements

**Structured Fields (vs Markdown)**

- Migrate to individual fields per dimension for analytics
- Enable programmatic spec generation
- Support A/B testing of dimension weights

**Spec Analytics**

- Track which dimensions correlate with successful hires
- Optimize weights based on outcomes
- Benchmark scores across searches

**Collaborative Features**

- Hiring manager + talent team co-authoring
- Comment threads on dimensions
- Approval workflows

**Dynamic Generation**

- AI drafts spec from job description
- Human reviews and refines
- Learning from past specs

### Open Questions

1. Should specs be versioned when edited? (Track changes over time)
2. How granular should scale definitions be? (3-point vs 5-point)
3. Should different evaluators weight dimensions differently?
4. How to handle cross-functional roles (CFO+COO hybrid)?

---

## 7. Implementation Checklist

**Phase 1: Setup (2 hours)**

- [ ] Create Role Specs table in Airtable with schema
- [ ] Add Single Select fields (role type, stage, sector)
- [ ] Create Template Library view
- [ ] Add "Duplicate" button automation

**Phase 2: Templates (3 hours)**

- [ ] Write 2 base templates (CFO, CTO) with full dimensions
- [ ] Create 4 customized specs for demo companies
- [ ] Test markdown formatting in Airtable

**Phase 3: Python Integration (4 hours)**

- [ ] Implement `parse_role_spec()` function
- [ ] Implement `build_assessment_prompt()` function
- [ ] Test parsing on all 4 demo specs
- [ ] Validate structured output schema

**Phase 4: Assessment Integration (3 hours)**

- [ ] Update `assess_candidate()` to consume specs
- [ ] Calculate weighted scores correctly
- [ ] Add must-haves/red flags checking
- [ ] Test end-to-end screening workflow

**Phase 5: Validation (1 hour)**

- [ ] Run all test cases
- [ ] Verify demo flow works
- [ ] Check markdown rendering in Airtable
- [ ] Review assessment outputs for quality

**Total Estimated Time: 13 hours**

---

## Appendix A: Example Template

See `templates/series_b_saas_cfo_spec.md` for full template example.

## Appendix B: API Reference

```python
# Key functions for implementation

spec_parser.parse_role_spec(markdown: str) -> dict
spec_parser.build_assessment_prompt(spec: dict, research: str) -> str
assessment.assess_candidate(research: str, spec_markdown: str, instructions: str) -> dict
assessment.calculate_overall_score(dimension_scores: list, dimensions: list) -> float
```

---

**Document Status:** Draft → Ready for Implementation
**Next Steps:** Begin Phase 1 (Airtable setup) and Phase 2 (template creation)
