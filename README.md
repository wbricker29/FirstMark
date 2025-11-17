# Talent Signal Agent

AI-powered executive matching for FirstMark Capital portfolio companies.

## Overview

Working directory for all information and projects related to Will Bricker's evaluation for the role of AI Lead at FirstMark Capital.

**Case Study:** Prototype AI agent for matching executives with portfolio company roles.

## Phase 1: Project Setup (✅ COMPLETE)

The foundational setup has been completed. All dependencies are installed and Pydantic models are validated.

### Prerequisites

- Python 3.11+ (verified with `.python-version`)
- UV package manager (for dependency management)

### Setup Instructions

1. **Verify Python Version**
   ```bash
   python --version  # Should show Python 3.11+
   ```

2. **Install UV** (if not already installed)
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Install Dependencies**
   ```bash
   uv pip install -e .
   ```

4. **Configure Environment Variables**
   - Copy `.env.example` to `.env`
   - Populate required API keys:
     - `OPENAI_API_KEY`: OpenAI API key
     - `AIRTABLE_API_KEY`: Airtable personal access token
     - `AIRTABLE_BASE_ID`: Airtable base ID

5. **Verify Installation**
   ```bash
   # Check all packages installed
   uv pip list | grep -E "(agno|pydantic|flask|pyairtable|dotenv)"

   # Verify models can be imported
   .venv/bin/python -c "from demo.models import ExecutiveResearchResult, AssessmentResult; print('✅ Models loaded')"

   # Run model validation tests
   .venv/bin/python tests/test_models_validation.py
   ```

### Project Structure

```
demo/                      # 5-file v1.0 implementation
├── __init__.py           # Package initialization
├── app.py                # Flask webhook server
├── agents.py             # Agno agent definitions
├── models.py             # Pydantic data models (✅ implemented)
├── airtable_client.py    # Airtable API wrapper
└── settings.py           # Configuration/env loading

tmp/                       # Agno session database location
tests/                     # Test suite
├── test_models_validation.py  # ✅ Model validation tests
├── test_scoring.py       # Dimension scoring tests (Phase 2)
├── test_quality_check.py # Research quality tests (Phase 2)
└── test_workflow_smoke.py # End-to-end tests (Phase 2)

spec/                      # Technical specifications
├── constitution.md       # Project governance
├── prd.md                # Product requirements
├── spec.md               # Technical spec
└── units/001-phase-1/    # Phase 1 design & plan
```

### What's Complete

- ✅ Python 3.11+ environment configured
- ✅ All dependencies installed via UV
- ✅ Environment configuration files (.env, .env.example, .gitignore)
- ✅ Project directory structure (demo/, tmp/, tests/)
- ✅ All 6 Pydantic models implemented and validated
  - Citation
  - CareerEntry
  - ExecutiveResearchResult
  - DimensionScore
  - MustHaveCheck
  - AssessmentResult

## Workflow Orchestration

The screening workflow executes a 4-step linear pipeline that coordinates research, quality checking, and assessment agents.

### Execution Flow

```
1. Deep Research → 2. Quality Check → 3. Incremental Search (conditional) → 4. Assessment
```

**Step 1: Deep Research**
- Agent: `o4-mini-deep-research`
- Executes comprehensive candidate research using built-in web search
- Returns markdown report + citations

**Step 2: Quality Gate**
- Heuristic check: `≥3 unique citations` AND `non-empty summary`
- Pass → proceed to Assessment
- Fail → trigger Incremental Search

**Step 3: Incremental Search (Conditional)**
- Agent: `gpt-5-mini` + web_search_preview
- Triggered only when quality gate fails
- Single-pass: max 2 web searches to fill gaps
- Results merged with original research

**Step 4: Assessment**
- Agent: `gpt-5-mini` + ReasoningTools
- Evaluates candidate against role spec
- Outputs structured assessment with dimension scores

### Session State Persistence

**Storage:** SqliteDb at `tmp/agno_sessions.db`

Session state tracks:
- `screen_id`: Airtable record ID
- `candidate_id`: Candidate record ID
- `candidate_name`: For logging
- `last_step`: Most recent completed step
- `quality_gate_triggered`: Whether incremental search ran

**Why SqliteDb?** Persistent audit trail for demo review. InMemoryDb deferred to Phase 2+ fast mode.

### Event Streaming & Logging

**Configuration:** `stream_events=True` on Workflow creation

**Log Format:** INFO level with emoji indicators
- 🔍 Step start (research, quality check, assessment)
- ✅ Step success with metadata (citation count, scores)
- 🔄 Incremental search triggered
- ❌ Errors with context

**Example Output:**
```
2025-11-17 | INFO | 🔍 Starting deep research for Alex Rivera (CFO at Armis)
2025-11-17 | INFO | ✅ Deep research completed for Alex Rivera with 4 citations
2025-11-17 | INFO | 🔍 Checking research quality for Alex Rivera
2025-11-17 | INFO | ✅ Research quality threshold met for Alex Rivera
2025-11-17 | INFO | 🔍 Starting assessment for Alex Rivera
2025-11-17 | INFO | ✅ Assessment complete for Alex Rivera (overall_score=95.0)
```

### Error Handling

**Retry Configuration:** All agents use exponential backoff
- `retries=2` (Deep Research, Assessment)
- `retries=1` (Incremental Search - lightweight)
- `exponential_backoff=True`
- `delay_between_retries=1s`

**Failure Behavior:**
- Agent retries automatically on transient failures
- Session state preserved on errors (no corruption)
- Clear RuntimeError raised after retry exhaustion
- Logs capture failure context with ❌ indicator

### Usage Example

```python
from demo.agents import screen_single_candidate

# Candidate data from Airtable People table
candidate = {
    "id": "recABC123",
    "name": "Alex Rivera",
    "current_title": "CFO",
    "current_company": "Armis",
    "linkedin_url": "https://linkedin.com/in/alex-rivera"
}

# Role spec markdown from Airtable Role_Specs table
role_spec = """
# CFO Role Specification
## Must-Haves
- 10+ years finance leadership
- B2B SaaS experience
- Series B+ fundraising
...
"""

# Execute full workflow
assessment = screen_single_candidate(
    candidate_data=candidate,
    role_spec_markdown=role_spec,
    screen_id="recSCREEN001"
)

# Access results
print(f"Overall Score: {assessment.overall_score}")
print(f"Confidence: {assessment.overall_confidence}")
print(f"Summary: {assessment.summary}")

for score in assessment.dimension_scores:
    print(f"{score.dimension}: {score.score}/5 ({score.confidence})")
```

**Output Schema:** Returns `AssessmentResult` Pydantic model with:
- `overall_score`: 0-100 scale (or None if insufficient evidence)
- `overall_confidence`: High/Medium/Low
- `dimension_scores`: List of scored evaluation dimensions
- `summary`: 2-3 sentence topline assessment
- `must_haves_check`: Requirements verification
- `green_flags` / `red_flags_detected`: Signal extraction
- `counterfactuals`: "Why candidate might NOT be ideal"

### Design Decisions

**Linear (not parallel):** Single candidate, synchronous processing. Simplifies v1 implementation and demo presentation. Parallel execution deferred to Phase 2+.

**Quality Gate (not multi-iteration):** Single incremental search pass (max 2 web searches) balances quality improvement with execution speed. Prevents infinite research loops.

**SqliteDb (not InMemoryDb):** Persistent session history enables post-demo review of workflow execution. Critical for demonstrating thinking process to FirstMark team.

**No Custom Event Tables:** Uses Agno-managed session tables only. Custom WorkflowEvent model and event persistence deferred to Phase 2+ production features.

## Case Study Resources

- **Directory:** `case/`
- **Brief:** `case/FirstMark_case.md`
- **Specifications:** `spec/`
- **Reference Materials:** `reference/`
