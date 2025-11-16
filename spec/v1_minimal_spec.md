---
version: "1.0-minimal"
created: "2025-01-17"
project: "Talent Signal Agent"
context: "FirstMark Capital AI Lead Case Study"
---

# Talent Signal Agent – v1.0 Minimal Scope Proposal

This document defines a **v1.0-minimal** implementation scope for the Talent Signal Agent and enumerates the **specific changes required** in:

- `spec/prd.md` (PRD)
- `spec/spec.md` (technical spec)

The goal is to:

- Preserve the core story in `case/technical_spec_V2.md`
- Strictly apply **KISS** and **YAGNI** for a 48-hour demo
- Reduce implementation surface area while still scoring well on the case rubric

---

## 1. v1.0-Minimal – What It Includes

### 1.1 Functional Scope (Minimal Demo)

v1.0-minimal supports **one primary workflow** (Module 4 – Screen) implemented end-to-end:

- Data lives in Airtable:
  - People (executives)
  - Portcos / Roles / Role Specs
  - Screens / Assessments (results)
- A single Flask app exposes **one main endpoint**:
  - `POST /screen` – given a Screen record ID:
    - Read Screen + linked Role + Spec + People from Airtable
    - For each candidate:
      - Run **deep research** (OpenAI Deep Research API)
      - Optionally trigger an **incremental search agent step** if a simple quality check flags missing evidence
        - That agent step may perform up to **two** web/search calls internally
      - Merge research signals and parse into `ExecutiveResearchResult`
      - Run spec-guided assessment → `AssessmentResult`
    - Write back:
      - Research JSON (optional field)
      - Assessment JSON
      - Key summary fields (overall score, confidence, top-line summary)
    - Update status fields in Airtable (e.g., `Status: In Progress → Complete` or `Failed`)
- UI is **Airtable-only**:
  - Creating roles/searches/specs is done via Airtable views/forms
  - No additional web UI, CLI, or dashboards

### 1.2 Technical Scope (Minimal)

**Core components:**

- **Flask app** (`app.py` or equivalent):
  - `POST /screen` endpoint
  - 1–2 small helpers for request parsing and response formatting
- **Agents module** (single file or small package):
  - `create_research_agent(use_deep_research: bool = True) -> Agent`
    - v1: default and only required path is `use_deep_research=True`
  - `run_research(...) -> ExecutiveResearchResult`
    - May optionally call an incremental search agent that performs up to **two** web/search calls internally when requested
  - `assess_candidate(research, role_spec_markdown, custom_instructions="") -> AssessmentResult`
- **Models module**:
  - Pydantic models for `ExecutiveResearchResult`, `AssessmentResult`, and supporting types
  - Keep fields necessary for the demo; avoid over-modeling
- **Airtable client module**:
  - Thin wrapper around pyairtable for reading:
    - Screen record + linked candidates + linked role + spec markdown
  - Writing:
    - Assessment results back to Airtable
    - Minimal status fields and key summary metrics

**Non-goals for v1.0-minimal:**

- No dedicated SQLite database for workflow events
- No separate CLI interface or Python package entrypoint
- No message queues, background workers, or async orchestration
- No production deployment (local Flask + ngrok only)
- No full-blown observability stack (stdout logging only)

### 1.3 Quality & Testing (Minimal)

- **Quality goals:**
  - Code is readable, typed, and split into small, clear modules
  - Errors during a screen:
    - Logged to terminal
    - Reflected in Airtable via `Status` + an error message field
- **Testing:**
  - A few focused tests (e.g., `calculate_overall_score`, quality check heuristics, maybe one end-to-end happy path with mocks)
  - No strict coverage percentage requirement

---

## 2. Required Changes to `spec/prd.md`

Below are concrete changes to align the PRD with v1.0-minimal. References are by section headings in `spec/prd.md`.

### 2.1 Scope & Modes

**Current:** PRD describes both **Deep Research** and **Fast Mode** as first-class modes, plus a more complex quality-gate/supplemental-search loop.

**Change (v1-minimal):**

- In sections describing the research strategy and performance (including the "Python-Specific Considerations → Performance Requirements" and "Latency" bullets):
  - Reframe **Fast Mode** as a **Phase 2+** feature, not required for the demo.
  - Reframe the full multi-iteration **supplemental search loop** as **Phase 2+**, but keep a **single incremental search agent step** (which may perform up to two web/search calls) as an optional v1 feature.
  - For v1, commit to:
    - Primary mode: **Deep Research** (`o4-mini-deep-research`) for all candidates
    - Optional, very simple quality check (e.g., "has at least N citations") that may trigger **one incremental search agent step** per candidate.

**Suggested wording adjustment:**

- Replace "Deep Research Mode" / "Fast Mode" as parallel options with:
  - "Deep Research – primary and only required mode for v1.0-minimal"
  - "Incremental Search – optional single-pass supplement when quality is low"
  - "Fast Mode – future optimization (Phase 2+), not required for demo"

### 2.2 Concurrency & Performance Targets

**Current:** PRD specifies support for 3–5 concurrent screenings, multiple workers, and fairly detailed throughput numbers.

**Change (v1-minimal):**

- In "Python-Specific Considerations → Performance Requirements" and any "Throughput" sections:
  - Set expectation to **single-process, synchronous execution**.
  - Remove or clearly tag concurrent workers and higher throughput as **Phase 2+**.

**Suggested constraints:**

- "For v1.0-minimal:
  - Process candidates sequentially per Screen
  - One Flask worker is sufficient
  - Demo expectation: up to ~10 candidates per Screen in <10 minutes total (dominated by Deep Research API latency)."

### 2.3 SQLite Workflow Events

**Current:** PRD requires SQLite for workflow event storage and includes it in performance/memory constraints.

**Change (v1-minimal):**

- In "Python-Specific Considerations → Memory" and "Data Requirements":
  - Remove SQLite as a **required** component.
  - If needed, relegate SQLite audit logging to a **Phase 2** enhancement.
- In "Non-Functional → Reliability" and "Acceptance Criteria":
  - Replace "Workflow events captured for complete audit trail" with:
    - "Minimal audit trail via:
      - Status and summary fields in Airtable
      - Terminal logs during execution"

### 2.4 Code Quality & Testing Targets

**Current:** PRD sets:

- 50%+ test coverage
- Passing `ruff` + `mypy`

**Change (v1-minimal):**

- In "Non-Functional → AC-PRD-06: Code Quality":
  - Relax 50%+ coverage to "basic tests for core scoring/quality-check logic and at least one workflow happy path with mocks, if time permits."
  - Keep type hints and linting as **goals**, but not hard acceptance gates for the demo.

**Suggested wording:**

- "Core matching and scoring logic is covered by smoke tests; type hints are present on public functions; code is reasonably linted/typed, but strict coverage and typing thresholds are out of scope for the 48-hour demo."

### 2.5 Reliability & Observability

**Current:** PRD assumes:

- SQLite-backed workflow audit trail
- Rich event capture

**Change (v1-minimal):**

- In "Non-Functional → AC-PRD-07: Reliability" and "Demo Validation Checklist":
  - Remove any requirement for SQLite-based audit trails.
  - Keep:
    - Ngrok reliability
    - Error surfacing in Airtable (`Status` + error message)
    - Console logs
  - Treat richer observability (events DB, metrics) as **Phase 2**.

---

## 3. Required Changes to `spec/spec.md`

These changes align the technical spec with the reduced surface area while still matching the narrative in `case/technical_spec_V2.md`.

### 3.1 Project Structure Simplification

**Current:** `spec/spec.md` defines a fairly large package structure:

- `demo_files/agents/`, `demo_files/models/`, `demo_files/workflows/`, `demo_files/db/`, `demo_files/api/`, `demo_files/cli/`, extensive `tests/`, etc.

**Change (v1-minimal):**

- Replace the detailed multi-package tree with a **minimal layout**, for example:

```text
demo/
├── app.py              # Flask app + webhook entrypoints
├── agents.py           # research + assessment agent creation + runners
├── models.py           # Pydantic models (research + assessment)
├── airtable_client.py  # Thin Airtable wrapper
└── settings.py         # Config/env loading (optional)
```

- Mention that further decomposition into subpackages (`agents/`, `models/`, `workflows/`) is a **future refactor**, not required for v1.

### 3.2 Removal of SQLite-Based WorkflowEvent DB (for v1)

**Current:** Technical spec includes:

- A dedicated `WorkflowEvent` Pydantic model
- A SQLite database (`tmp/screening_workflows.db`)
- Logic to store and retrieve workflow events

**Change (v1-minimal):**

- Mark the entire `WorkflowEvent` entity and SQLite storage as **Phase 2+**.
- For v1:
  - Keep the conceptual notion of "events" in Agno and logs.
  - Persist only what is necessary in Airtable:
    - Final assessment JSON
    - Status + error message fields
    - Optional small execution metadata (e.g., total runtime) if trivial to add.

**Spec edits:**

- In the "Entity: WorkflowEvent" section:
  - Prefix with "Phase 2+" and clarify it is **not required for v1.0-minimal**.
- In "Observability → Audit Trail":
  - Replace SQLite storage description with:
    - "For v1.0-minimal, rely on Airtable fields + logs; SQLite audit DB is an optional future enhancement."

### 3.3 Single Research Mode + Optional Incremental Search

**Current:** Technical spec treats Deep Research and Fast Mode as parallel options, with additional logic for supplemental search.

**Change (v1-minimal):**

- In "Research Agent Interface" and any "Execution Modes" section:
  - Keep the function signature that allows `use_deep_research: bool = True` but note:
    - v1 implementation **only requires** `use_deep_research=True`.
    - `use_deep_research=False` and any special fast-mode behavior are **Phase 2+**.
  - Allow an **optional single incremental search agent step** (e.g., web-search-backed) when a simple quality check indicates missing evidence; that agent may use up to two web/search calls internally.
- In "Workflow Specification Reference":
  - Simplify the description to:
    - Step 1: Deep Research Agent
    - Step 2: (Optional) Lightweight quality check
    - Step 3: (Optional) Single incremental search agent step + merge
    - Step 4: Assessment Agent
  - Mark multi-iteration supplemental search loops as **future**.

### 3.4 Workflow & Quality Check Simplification

**Current:** Quality check interface and workflow description assume:

- Detailed metrics
- Conditional branching with supplemental search
- Potential loops with max iterations

**Change (v1-minimal):**

- In "Quality Check Interface":
  - Keep a simple `check_research_quality(...)` but:
    - Make it a pure function over `ExecutiveResearchResult`, not tied to complex workflow types if not needed.
    - Limit sufficiency criteria to a minimal set (e.g., "≥3 citations and non-empty summary").
    - Remove `StepInput`/`StepOutput` complexity from the v1 implementation description.
- In "Workflow Specification Reference":
  - Explicitly state that v1 workflow is **linear**:
    - `Deep Research → Quality Check → (optional single incremental search) → Assessment → Airtable write`.

### 3.5 Observability & Error Handling

**Current:** Spec includes:

- Optional `structlog`
- Detailed event streaming and metrics
- Structured error-handling examples with custom exceptions

**Change (v1-minimal):**

- In "Observability" and "Error Handling Strategy":
  - Emphasize **basic logging** using Python’s `logging` module as sufficient for v1.
  - Mark:
    - Structured logging (`structlog`)
    - Event streaming to SQLite
    - Rich metrics
    as **optional enhancements**, not required for demo success.

### 3.6 Tests Layout

**Current:** Spec proposes:

- Multiple test directories (`test_agents`, `test_models`, `test_workflows`, `test_utils`, fixtures, etc.).

**Change (v1-minimal):**

- Replace with a simpler recommendation:

```text
tests/
├── test_scoring.py      # calculate_overall_score, etc.
├── test_quality_check.py
└── test_workflow_smoke.py  # happy-path /screen flow with mocks (optional)
```

- Remove any implication that a large, granular test suite is mandatory for the demo.

### 3.7 Recommended Native AGNO Features for v1

To keep the implementation simple while leveraging AGNO effectively, v1.0-minimal should:

- **Use structured outputs natively:**
  - Configure research and assessment agents with AGNO’s structured output / `output_model` support so they return `ExecutiveResearchResult` and `AssessmentResult` directly.
  - Avoid a separate “parser agent” layer and heavy custom JSON-parsing prompts.

- **Use a single AGNO Workflow for orchestration:**
  - Implement `Deep Research → Quality Check → (optional incremental search agent step) → Assessment` as an AGNO `Workflow` instead of a custom state machine.
  - Keep the workflow linear and small; no teams, no nested workflows for v1.

- **Rely on built-in retry/backoff:**
  - Configure agents with `exponential_backoff=True` and a small `retries` count for OpenAI calls.
  - Remove any bespoke retry wrappers in Python around research/assessment agents.

- **Use streaming events only for logging (not storage):**
  - Enable `stream_events=True` and log events to stdout for demo-time visibility.
  - Do not persist events in a separate database; Airtable + logs are the v1 audit trail.

- **Use built-in OpenAI tools for search:**
  - Implement the incremental search agent using AGNO’s OpenAI/web-search tools instead of hand-written HTTP calls.

And v1.0-minimal should explicitly **not** use:

- AGNO memory / Postgres DB (`enable_user_memories` / `enable_agentic_memory`) for candidate data.
- AGNO Teams or other multi-agent coordination abstractions.
- Large toolkits unrelated to Airtable/OpenAI (e.g., Notion tools).

---

## 4. Summary: v1.0-Minimal Contract

**Core contract for v1.0-minimal:**

- One main API path: Airtable → ngrok → Flask `/screen` → AGNO workflow (deep research + assessment) → Airtable.
- Minimal Python surface area:
  - Flask app
  - Agents
  - Pydantic models
  - Thin Airtable wrapper
- Deep research as the primary mode; optional **single incremental search agent step** (which may perform up to two web/search calls) when quality is low; no fast-mode orchestration or multi-iteration supplemental search loops.
- No SQLite or extra databases; Airtable + logs provide sufficient auditability.
- Basic testing and logging; correctness and clarity are prioritized over coverage metrics or production-grade observability.

These changes keep the implementation aligned with `case/technical_spec_V2.md` while making the delivered code achievable, maintainable, and clearly scoped for a 48-hour interview demo.
