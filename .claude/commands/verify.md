---
name: verify
description: Run Python Verification Gates
---

# /verify - Run Python Verification Gates

## Purpose
Run all verification gates defined in unit plan to ensure implementation meets quality standards.

## Usage
```
/verify <slug>
```

**Example:**
```
/verify csv-parser
/verify user-authentication
```

## Prerequisites
- `spec/units/###-SLUG/plan.md` must exist
- All tasks in plan should be "done"

## Process

### Step 1: Load Plan
- Read `plan.md` for unit ###-SLUG
- Extract verification commands
- Extract verification gates
- Extract coverage target

### Step 2: Check Task Completion
- Count tasks with status="done"
- If incomplete tasks exist, warn user:
  ```
  ⚠️ Warning: 2 tasks still incomplete
  - TK-05: Write unit tests (ready)
  - TK-07: Performance optimization (blocked)

  Continue verification anyway? [y/N]
  ```

### Step 3: Run Verification Commands
Execute each command from plan.md in order:

#### Command 1: Run Tests
```bash
uv run pytest tests/ -v
```
- Capture output
- Check exit code
- Gate: Must pass (exit code 0) ✅

#### Command 2: Check Coverage
```bash
uv run pytest --cov=src --cov-report=term-missing --cov-report=html
```
- Parse coverage percentage
- Compare to target from plan.md
- Gate: Coverage ≥ target ✅

#### Command 3: Type Check
```bash
uv run pyright src/
# OR
uv run mypy src/
```
- Capture error count
- Gate: Zero type errors ✅

#### Command 4: Linting
```bash
uv run ruff check src/
```
- Capture error/warning count
- Gate: Zero errors ✅

#### Command 5: Format Check
```bash
uv run ruff format --check src/
```
- Check if reformatting needed
- Gate: No changes needed ✅

### Step 4: Additional Python Checks
Run optional but recommended checks:

#### Security Audit
```bash
uv pip audit
```
- Check for known vulnerabilities
- Report findings (not a gate, but informational)

#### Import Order
```bash
uv run ruff check --select I src/
```
- Verify import organization (handled by ruff)

### Step 5: Evaluate Gates
For each gate in plan.md:
- **tests:** Did all tests pass?
- **type_check:** Zero type errors?
- **coverage:** Met or exceeded target?
- **linting:** Zero linting errors?
- **formatting:** No formatting changes?

### Step 6: Validate Acceptance Criteria
For each acceptance criterion in design.md:
- Which test(s) verify this criterion?
- Are those tests passing?
- Mark criteria as verified ✅ or failed ❌

### Step 7: Update Plan
In `plan.md`:
- Update **Coverage** in Status section with actual value
- Update **Blockers** if any gates failed
- Add verification timestamp

### Step 8: Generate Report
Create comprehensive verification report:

```
Verification Report: Unit 001-csv-parser
Generated: 2025-01-15 10:30:00

Task Completion:
✅ 7/7 tasks completed (100%)

Verification Commands:
✅ pytest tests/ -v (8 passed)
✅ pytest --cov (Coverage: 92%)
✅ pyright src/ (0 errors)
✅ ruff check src/ (0 errors)
✅ ruff format --check src/ (compliant)

Gates:
✅ tests: PASSED (8/8 tests passing)
✅ type_check: PASSED (0 errors)
✅ coverage: PASSED (92% ≥ 85% target)
✅ linting: PASSED (0 errors)
✅ formatting: PASSED (no changes needed)

Acceptance Criteria:
✅ AC-001-01: Parse Valid CSV (verified by test_parse_valid_csv)
✅ AC-001-02: Handle Empty File (verified by test_parse_empty_csv)
✅ AC-001-03: Validate Against Schema (verified by test_validate_schema)
✅ AC-001-04: Stream Large Files (verified by test_large_file_memory)
✅ AC-001-05: Error Messages (verified by test_error_messages)

Additional Checks:
ℹ️  Security Audit: 0 known vulnerabilities
ℹ️  Import Order: Compliant

Result: ✅ ALL GATES PASSED

Coverage Report:
HTML coverage report generated: htmlcov/index.html
View with: open htmlcov/index.html

Unit 001-csv-parser is ready for integration.
```

### Step 9: Update CLAUDE.md
Add verification results to working memory:
- Verification timestamp
- All gates passed/failed
- Actual coverage achieved
- Any issues found

### Step 10: Suggest Next Steps
If all gates passed:
```
✅ Unit verification complete!

Next steps:
- Review implementation for final polish
- Run /check to validate alignment with spec.md
- Integrate with other units
- Consider /reflect to capture learnings
```

If any gates failed:
```
❌ Verification failed

Failed gates:
- coverage: 78% < 85% target

Required actions:
1. Run /work csv-parser to add more tests
2. Focus on uncovered lines (see htmlcov/index.html)
3. Re-run /verify csv-parser when ready
```

## Output
- **Console:** Comprehensive verification report
- **HTML:** Coverage report (htmlcov/index.html)
- **Updated:** plan.md with actual coverage
- **Updated:** CLAUDE.md with verification results

## Validation
- ✅ All verification commands executed
- ✅ All gates evaluated
- ✅ Acceptance criteria checked
- ✅ Coverage report generated
- ✅ plan.md updated
- ✅ CLAUDE.md updated

## Next Steps
- If passed: Run `/check` to validate alignment
- If failed: Run `/work SLUG` to fix issues, then re-verify
