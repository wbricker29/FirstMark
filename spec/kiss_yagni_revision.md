# KISS/YAGNI Revision: Talent Signal Agent v1

**Status:** Proposed Simplification
**Date:** 2025-01-16
**Context:** Align PRD and SPEC with REQUIREMENTS.md for 48-hour demo constraint

---

## Executive Summary

**Current State:** PRD and SPEC describe a production-quality system with 15+ files, ~1200 LOC, complex quality gates, and 34-hour implementation timeline.

**KISS-Aligned State:** Minimal demo with 6 files, ~650 LOC, simple sequential workflow, and 20-hour implementation timeline.

**Key Reductions:**
- **Files:** 15+ → 6 (60% reduction)
- **Code:** ~1200 LOC → ~650 LOC (45% reduction)
- **Timeline:** 34 hours → 20 hours (41% reduction)
- **Risk:** High → Medium (simpler scope, more buffer)

**Alignment:** Matches REQUIREMENTS.md principles: "minimal, quick to stand up," "Clear > Clever," "Simple Features, Working > Perfect"

---

## Simplified v1 Scope

### What STAYS (Core Demo) ✅

**Workflow:**
- Research candidate using o4-mini-deep-research
- Assess candidate against role spec
- Calculate dimension scores (1-5 scale, None for Unknown)
- Calculate overall score (0-100 scale)
- Write results to Airtable
- Trigger via webhook

**Technical Stack:**
- Flask webhook server
- Agno workflow (simple sequence)
- Pydantic structured outputs
- Airtable database (6 tables)
- OpenAI API (o4-mini-deep-research, gpt-5-mini)

**Data:**
- 64 executives from guildmember_scrape.csv
- 4 portfolio scenarios
- 1 pre-run scenario, 2-3 live scenarios

---

### What's SIMPLIFIED (KISS) ⚠️

**1. Project Structure**

FROM (15+ files):
```
demo_files/
├── agents/ (3 files)
├── models/ (3 files)
├── workflows/ (2 files)
├── integrations/ (2 files)
├── utils/ (3 files)
└── tests/ (full suite)
```

TO (6 files):
```
demo_files/
├── models.py          # All Pydantic models
├── agents.py          # Research + assessment agents
├── workflow.py        # Simple sequential workflow
├── airtable.py        # Airtable client
├── server.py          # Flask endpoint
└── test_workflow.py   # 1 integration test
```

**2. Scoring Algorithm**

FROM (complex weighted algorithm):
- Filter scored dimensions
- Check minimum threshold
- Renormalize weights
- Compute weighted average
- Boost high-evidence dimensions
- Scale to 0-100

TO (simple average):
```python
def calculate_overall_score(dimension_scores):
    scored = [d.score for d in dimension_scores if d.score is not None]
    return (sum(scored) / len(scored)) * 20 if scored else None
```

**3. Testing**

FROM:
- Unit tests for agents, models, workflows, utils
- Integration tests
- 50%+ coverage target

TO:
- 1 end-to-end integration test
- 1 Pydantic model validation test

**4. Configuration**

FROM (21 env vars):
```bash
MIN_EXPERIENCES=3
MIN_EXPERTISE=2
MIN_CITATIONS=3
MAX_GAPS=2
MAX_SUPPLEMENTAL_ITERATIONS=3
WORKFLOW_DB_PATH=...
# etc.
```

TO (5 env vars):
```bash
OPENAI_API_KEY=...
AIRTABLE_API_KEY=...
AIRTABLE_BASE_ID=...
USE_DEEP_RESEARCH=true
DEBUG=true
```

**5. Airtable Schema**

FROM (9 tables):
- People, Companies, Portcos, Roles, Searches, Screens, Workflows, Research, Assessments

TO (6 tables):
- People, Portcos, Roles, Specs, Searches, Assessments

---

### What's REMOVED (YAGNI) ❌

**1. Quality Gate + Supplemental Search Loop**
- **Saves:** ~250 LOC, 4+ hours development
- **Rationale:** Over-engineering for demo. Mark unknown dimensions as None instead.
- **Files removed:** `workflows/workflow_functions.py`, `models/workflow.py`, `agents/web_search_agent.py`

**2. Multiple Research Modes**
- **Saves:** ~50 LOC, 1 hour development
- **Rationale:** Pick one mode (deep research) and stick with it
- **Config removed:** `USE_DEEP_RESEARCH` toggle logic

**3. SQLite Workflow Events**
- **Saves:** ~80 LOC, 2 hours development
- **Rationale:** Airtable status fields + terminal logs sufficient for demo
- **Files removed:** `tmp/screening_workflows.db`, event storage logic

**4. Markdown Exports**
- **Saves:** ~40 LOC, 1 hour development
- **Rationale:** Show Airtable directly in demo
- **Files removed:** Markdown report generation

**5. Spec Parser Utility**
- **Saves:** ~60 LOC, 1 hour development
- **Rationale:** Pass markdown to LLM directly (LLM can parse)
- **Files removed:** `utils/spec_parser.py`

**6. Custom Exception Hierarchy**
- **Saves:** ~30 LOC, 30 minutes development
- **Rationale:** Use basic exceptions, catch at Flask level
- **Classes removed:** `AirtableError`, `ResearchError`, `AssessmentError`, etc.

**7. Structured Logging**
- **Saves:** ~40 LOC, 30 minutes development
- **Rationale:** Basic logging with emoji indicators sufficient
- **Dependencies removed:** `structlog`

**8. Complex Utils Directory**
- **Saves:** ~100 LOC total
- **Rationale:** Inline simple logic, no separate utilities needed
- **Files removed:** `utils/scoring.py`, `utils/spec_parser.py`, `utils/logger.py`

---

## PRD Modifications (spec/prd.md)

### Change 1: Module 4 Scope (Lines 122-132)

**REMOVE:**
```markdown
- ✅ Quality gate with conditional supplemental search
- ✅ Dimension-level scores (1-5 scale with None for Unknown)
- ✅ Overall score calculation (0-100 scale)
- ✅ Reasoning, counterfactuals, confidence tracking
- ✅ Citation tracking and audit trail
- ✅ Markdown report generation
```

**REPLACE WITH:**
```markdown
- ✅ Deep research using OpenAI o4-mini-deep-research
- ✅ Spec-guided assessment with evidence-aware scoring
- ✅ Dimension scores (1-5 scale, None for Unknown)
- ✅ Overall score (simple average × 20)
- ✅ Reasoning and confidence tracking
- ✅ Results written to Airtable
```

---

### Change 2: Out of Scope (Lines 149-167)

**ADD TO "Explicitly Deferred":**
```markdown
- Quality gate logic with supplemental search iterations
- SQLite workflow event storage
- Complex weighted scoring algorithm
- Multiple research modes (deep vs fast toggle)
- Markdown report exports
- Spec parser utility
- Structured logging (structlog)
- Custom exception hierarchy
- 50%+ test coverage
```

---

### Change 3: Timeline (Lines 438-515)

**REPLACE Phase 2-5 with:**

```markdown
### Phase 2: Core Implementation (12 hours)

**Models (2 hours):**
- ExecutiveResearchResult and AssessmentResult Pydantic models
- Simple validation logic

**Agents (4 hours):**
- Research agent (o4-mini-deep-research)
- Assessment agent (gpt-5-mini with spec)

**Workflow (3 hours):**
- Simple sequential Agno workflow
- No custom functions, no loops

**Integrations (2 hours):**
- Airtable client (basic CRUD)
- Flask /screen endpoint

**Server (1 hour):**
- Request validation, error handling

### Phase 3: Testing (2 hours)
- 1 end-to-end integration test
- Manual testing with 1 candidate

### Phase 4: Demo Prep (4 hours)
- Pre-run 1 scenario (Pigment CFO)
- Prepare 2 scenarios for live demo (Mockingbird CFO, Estuary CTO)
- Test webhook trigger

### Phase 5: Documentation (2 hours)
- README with architecture
- Brief slide deck or written deliverable

**Total: 20 hours active work (28-hour buffer for debugging)**
```

---

### Change 4: Acceptance Criteria (Lines 522-565)

**UPDATE AC-PRD-03:**
```markdown
**AC-PRD-03: Candidate Screening**
- ✅ Webhook triggers Flask /screen endpoint
- ✅ Deep research executes and returns ExecutiveResearchResult
- ✅ Assessment produces dimension scores, overall score, reasoning
- ✅ Results written to Airtable
- ✅ Failed workflows marked with error messages
```

**REMOVE:**
- Quality gate evaluation criteria
- Supplemental search trigger criteria

---

## SPEC Modifications (spec/spec.md)

### Change 1: Project Structure (Lines 103-153)

**REPLACE WITH:**
```markdown
demo_files/
├── __init__.py
├── models.py                    # Pydantic models (200 LOC)
│   ├── ExecutiveResearchResult
│   ├── AssessmentResult
│   └── DimensionScore
├── agents.py                    # Agent implementations (150 LOC)
│   ├── research_candidate()
│   └── assess_candidate()
├── workflow.py                  # Agno workflow (100 LOC)
│   └── screen_candidate_workflow()
├── airtable.py                  # Airtable client (100 LOC)
│   ├── get_screen()
│   ├── get_role_spec()
│   └── write_assessment()
├── server.py                    # Flask endpoint (50 LOC)
│   └── /screen route
└── test_workflow.py             # Integration test (50 LOC)

.env                             # 5 environment variables
pyproject.toml                   # 5 dependencies
README.md                        # Implementation guide

**Total: ~650 LOC across 6 files**
```

---

### Change 2: Remove Quality Check Interface (Lines 269-308)

**DELETE ENTIRE SECTION:**
- `QualityMetrics` TypedDict
- `QualityCheckResult` TypedDict
- `check_research_quality()` function

**RATIONALE:** Quality gate removed from scope

---

### Change 3: Simplify Score Calculation (Lines 313-350)

**REPLACE WITH:**
```python
def calculate_overall_score(dimension_scores: list[DimensionScore]) -> Optional[float]:
    """Calculate simple average score from dimensions.

    Args:
        dimension_scores: List of DimensionScore objects

    Returns:
        Overall score (0-100) or None if no dimensions scored

    Example:
        >>> scores = [
        ...     DimensionScore(dimension="Fundraising", score=4, ...),
        ...     DimensionScore(dimension="Operations", score=3, ...),
        ...     DimensionScore(dimension="Strategy", score=None, ...),
        ... ]
        >>> calculate_overall_score(scores)
        70.0  # (4 + 3) / 2 * 20
    """
    scored = [d.score for d in dimension_scores if d.score is not None]
    if not scored:
        return None
    return (sum(scored) / len(scored)) * 20
```

---

### Change 4: Configuration (Lines 891-924)

**REPLACE WITH:**
```bash
# OpenAI
OPENAI_API_KEY=sk-...

# Airtable
AIRTABLE_API_KEY=pat...
AIRTABLE_BASE_ID=app...

# Flask
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
DEBUG=true
```

---

### Change 5: Remove Error Hierarchy (Lines 939-965)

**DELETE ENTIRE SECTION**

**REPLACE WITH:**
```python
# Use basic exceptions:
# - ValueError for validation errors
# - RuntimeError for workflow failures
# - Exception for general errors
# Catch all at Flask endpoint level
```

---

### Change 6: Implementation Checklist (Lines 1122-1194)

**REPLACE WITH:**

```markdown
### Implementation Checklist (20 hours)

**Phase 1: Models (2 hours)**
- [ ] ExecutiveResearchResult Pydantic model
- [ ] AssessmentResult Pydantic model
- [ ] Validate model schemas

**Phase 2: Agents (4 hours)**
- [ ] research_candidate() using o4-mini-deep-research
- [ ] assess_candidate() using gpt-5-mini
- [ ] Test agents individually

**Phase 3: Workflow (3 hours)**
- [ ] Simple sequential Agno workflow
- [ ] Input/output handling
- [ ] Error handling

**Phase 4: Integrations (3 hours)**
- [ ] Airtable client (get_screen, get_role_spec, write_assessment)
- [ ] Flask /screen endpoint
- [ ] Webhook trigger testing

**Phase 5: Testing (2 hours)**
- [ ] End-to-end integration test
- [ ] Manual testing with 1 candidate

**Phase 6: Demo Prep (4 hours)**
- [ ] Pre-run 1 scenario
- [ ] Prepare 2 scenarios for live demo
- [ ] Test webhook automation

**Phase 7: Documentation (2 hours)**
- [ ] README with architecture
- [ ] Deliverable write-up

**Total: 20 hours**
```

---

## Implementation Diff Summary

| Aspect | Current (Production) | Revised (Demo KISS) | Change |
|--------|---------------------|---------------------|--------|
| **Files** | 15+ files (agents/, models/, workflows/, integrations/, utils/) | 6 files (flat structure) | -60% |
| **LOC** | ~1200 lines | ~650 lines | -45% |
| **Dependencies** | 8+ packages (agno, pydantic, flask, pyairtable, dotenv, structlog, pytest, pytest-cov, ruff, mypy) | 5 packages (agno, pydantic, flask, pyairtable, dotenv) | -37% |
| **Env Vars** | 21 variables | 5 variables | -76% |
| **Database** | Airtable (9 tables) + SQLite | Airtable (6 tables) | -33% tables |
| **Workflow** | Sequential + conditional + loop (quality gate) | Sequential only | -70% complexity |
| **Scoring** | Evidence-aware weighted algorithm | Simple average × 20 | -90% LOC |
| **Testing** | 50%+ coverage with unit + integration tests | 1-2 integration tests | -75% test time |
| **Timeline** | 34 hours (high risk) | 20 hours (medium risk) | -41% |
| **Buffer** | 14 hours | 28 hours | +100% |

---

## Workflow Comparison

### Current (Complex)
```
1. Deep Research (o4-mini-deep-research)
2. Quality Check (custom function)
   ├─ Sufficient? → Assessment
   └─ Insufficient? → Loop:
       ├─ Supplemental Search (gpt-5 + web_search)
       ├─ Merge Research
       ├─ Quality Check (repeat)
       └─ Max 3 iterations
3. Assessment (gpt-5-mini)
4. Write Results (Airtable + SQLite + Markdown)
```

### Revised (Simple)
```
1. Research (o4-mini-deep-research)
2. Assessment (gpt-5-mini)
   - Unknown dimensions → None
3. Calculate Score (simple average × 20)
4. Write Results (Airtable)
```

**Complexity Reduction:** 4 steps → 4 steps, but no loops/conditionals/merges

---

## Risk Assessment

### Current Plan Risks
- ❌ Quality gate implementation: 6-8 hours (budgeted 4)
- ❌ Testing infrastructure: 6-8 hours (budgeted 4)
- ❌ Agno learning curve with loops: 4+ hours debugging
- ❌ Pre-running 3 scenarios: If bugs found, all must re-run

### Revised Plan Risks
- ✅ Simple workflow: Lower Agno learning curve
- ✅ Minimal testing: 2 hours realistic
- ✅ 28-hour buffer: Adequate for debugging
- ⚠️ Pre-run 1 scenario: Still risk if workflow has bugs (mitigated by simpler code)

---

## Rationale: Why Each Removal Aligns with Case Goals

**Case Goal:** "Demonstrate quality of thinking through minimal, working code"

| Removed Feature | Why Not Needed |
|-----------------|----------------|
| **Quality Gate** | Shows production optimization, not domain thinking. Marking dimensions as "Unknown" demonstrates transparency—arguably better product thinking. |
| **Supplemental Search** | Adds workflow complexity without demonstrating new concepts. Single research pass proves the pattern. |
| **SQLite Events** | Audit trail is production feature. Airtable status fields + terminal logs sufficient for demo. |
| **Weighted Scoring** | Complex algorithm doesn't demonstrate better matching logic. Simple average proves the concept. |
| **Spec Parser** | LLMs can parse markdown natively. Utility is premature abstraction. |
| **Custom Exceptions** | Production error handling. Basic exceptions + Flask error catching sufficient. |
| **Structured Logging** | Observability infrastructure. Terminal logs with emojis adequate for demo. |
| **50%+ Test Coverage** | Engineering hygiene, not domain thinking. 1-2 integration tests prove it works. |

---

## Recommendation

**Adopt the simplified v1 scope immediately.** Update PRD and SPEC per modifications above before starting implementation.

**Why:**
- Matches REQUIREMENTS.md: "minimal, quick to stand up"
- Reduces risk of timeline overrun
- Focuses on demonstrating domain thinking, not engineering prowess
- 28-hour buffer allows for unexpected issues
- Simpler code = easier to explain in presentation

**Next Steps:**
1. Update spec/prd.md (30 minutes)
2. Update spec/spec.md (30 minutes)
3. Begin implementation with simplified scope (20 hours)
