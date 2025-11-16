---
name: plan
description: Generate Python Unit Plan
---

# /plan - Generate Python Unit Plan

## Purpose
Generate task breakdown and verification plan from design document.

## Usage
```
/plan <slug>
```

**Example:**
```
/plan csv-parser
/plan user-authentication
```

## Prerequisites
- `spec/units/###-SLUG/design.md` must exist (run `/new SLUG` first)

## Process

### Step 1: Locate Unit
- Find unit directory matching SLUG
- Load `design.md`
- Extract objective, behavior, acceptance criteria

### Step 2: Break Down Into Tasks
Generate granular tasks for Python implementation:

**Common Task Pattern:**
1. Set up module structure and type stubs
2. Implement core logic
3. Add input validation
4. Handle edge cases
5. Write unit tests with pytest
6. Add type hints and docstrings
7. Performance optimization (if needed)

### Step 3: Define Task Details
For each task:
- **Title:** Clear, action-oriented
- **Description:** What needs to be done
- **Status:** ready/doing/done/blocked
- **Priority:** high/medium/low
- **Estimate:** Time estimate (1h, 3h, 1d)
- **Dependencies:** Which tasks must finish first
- **Completed:** Date when done (YYYY-MM-DD)

### Step 4: Verification Commands
Define Python-specific verification:

**Required commands:**
```bash
# Tests
uv run pytest tests/ -v

# Coverage
uv run pytest --cov=src --cov-report=term

# Type checking
uv run pyright src/
# OR
uv run mypy src/

# Linting
uv run ruff check src/

# Formatting
uv run ruff format --check src/
```

### Step 5: Verification Gates
Define pass criteria:
- **tests:** All pytest tests must pass ✅
- **type_check:** Zero type errors ✅
- **coverage:** Must be ≥ constitution target ✅
- **linting:** Zero linting errors ✅
- **formatting:** No format changes needed ✅

### Step 6: Coverage Target
Extract from constitution.md (default: 85%)

### Step 7: Acceptance References
Link to acceptance criteria from design.md:
- AC-[UNIT]-01
- AC-[UNIT]-02
- etc.

### Step 8: Python-Specific Notes
Add:
- Package structure (src/, tests/)
- Test fixtures examples
- Type hints examples
- Performance profiling commands

### Step 9: Generate Plan
Create `spec/units/###-SLUG/plan.md` with:
- Task breakdown
- Verification commands
- Gates and coverage target
- Status tracking (progress, blockers)
- Python-specific notes

### Step 10: Validate Plan
Check that:
- All tasks have estimates
- Dependencies are valid (no cycles)
- Verification commands use UV
- All acceptance criteria covered
- Python structure documented

### Step 11: Update Design Status
Change `design.md` status from "draft" to "planned"

### Step 12: Confirm
Display summary:
- Task count
- Total estimated time
- Verification gates
- Next step: Run `/work SLUG TK-##` to start first task

## Output
- **File:** `spec/units/###-SLUG/plan.md`
- **Status:** Ready for implementation

## Example Interaction
```
User: /plan csv-parser

Claude: Loading design for unit 001-csv-parser...

Generated 7 tasks:
1. TK-01: Set up module structure (1h)
2. TK-02: Implement core parsing logic (3h)
3. TK-03: Add input validation (2h)
4. TK-04: Implement schema validation (3h)
5. TK-05: Write unit tests (4h)
6. TK-06: Add type hints and docstrings (2h)
7. TK-07: Performance optimization (3h)

Total estimate: 18 hours

Verification gates:
✅ Tests (uv run pytest tests/ -v)
✅ Coverage ≥ 85% (uv run pytest --cov=src)
✅ Type check (uv run pyright src/)
✅ Linting (uv run ruff check src/)
✅ Formatting (uv run ruff format --check src/)

Plan created: spec/units/001-csv-parser/plan.md
Design status updated: draft → planned

Next step: Run `/work csv-parser TK-01` to start first task
```

## Validation
- ✅ plan.md created in unit directory
- ✅ All tasks have estimates and priorities
- ✅ Dependencies form valid DAG (no cycles)
- ✅ Verification commands use UV
- ✅ Coverage target matches constitution
- ✅ All acceptance criteria referenced

## Next Steps
Run `/work SLUG TK-##` to implement first task with UPEVD pattern
