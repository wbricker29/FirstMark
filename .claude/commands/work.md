---
name: work
description: Execute Python Task (UPEVD Pattern)
---

# /work - Execute Python Task (UPEVD Pattern)

## Purpose
Implement a specific task following the UPEVD workflow:
**U**nderstand → **P**lan → **E**xecute → **V**alidate → **D**ocument

## Usage
```
/work <slug> [task-id]
```

**Examples:**
```
/work csv-parser TK-01
/work user-authentication TK-03
/work csv-parser  # Work on next ready task
```

## Prerequisites
- `spec/units/###-SLUG/plan.md` must exist (run `/plan SLUG` first)
- If task-id omitted, will select next "ready" task

## Process: UPEVD Workflow

### U - Understand (Load Context)

#### Step U1: Load Unit Context
- Read `design.md` for objective and acceptance criteria
- Read `plan.md` for task breakdown
- Identify the specific task to work on

#### Step U2: Check Dependencies
- Verify all dependency tasks are "done"
- If dependencies not met, suggest completing them first
- Update task status to "doing"

#### Step U3: Load Python Environment
- Check for `pyproject.toml` and dependencies
- Verify UV is available
- Note relevant type hints and interfaces from spec.md

#### Step U4: Regenerate State
- Run state-tracker.py to update state.json
- Review current project state

### P - Plan (Develop Strategy)

#### Step P1: Review Task Requirements
- Understand what code needs to be written
- Identify modules/functions to create or modify
- Note testing requirements

#### Step P2: Identify Risks
- What could go wrong?
- What edge cases need handling?
- What performance concerns exist?

#### Step P3: Outline Approach
Present approach to user:
```
Task: TK-02 - Implement core parsing logic

Approach:
1. Create src/package_name/parsers/csv_parser.py
2. Implement parse_csv() function with type hints
3. Use csv.DictReader for parsing
4. Handle encoding parameter
5. Add error handling for FileNotFoundError
6. Write docstring with Args, Returns, Raises

Files to create/modify:
- src/package_name/parsers/csv_parser.py (create)
- src/package_name/parsers/__init__.py (update exports)

Tests to write:
- tests/test_parsers/test_csv_parser.py

Estimated time: 3h
```

### E - Execute (Implement)

#### Step E1: Create/Modify Python Code
Write implementation with:
- **Complete type hints** for all functions
- **Google or NumPy style docstrings**
- **PEP 8 compliant** naming and structure
- **Error handling** with specific exceptions
- **Input validation** for parameters

**Example:**
```python
from pathlib import Path
from typing import List, Dict, Any
import csv

def parse_csv(
    file_path: Path,
    encoding: str = "utf-8",
    validate: bool = False
) -> List[Dict[str, Any]]:
    """Parse CSV file into list of dictionaries.

    Args:
        file_path: Path to CSV file
        encoding: Character encoding (default: utf-8)
        validate: Whether to validate rows against schema

    Returns:
        List of parsed records as dictionaries

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If encoding is invalid or file is malformed
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    records = []
    try:
        with open(file_path, encoding=encoding) as f:
            reader = csv.DictReader(f)
            for row in reader:
                if validate:
                    # Validation logic
                    pass
                records.append(row)
    except UnicodeDecodeError as e:
        raise ValueError(f"Invalid encoding '{encoding}': {e}")

    return records
```

#### Step E2: Write Tests
Create pytest tests with:
- **Fixtures** for test data (use tmp_path)
- **Parametrize** for multiple test cases
- **Coverage** of happy paths and edge cases
- **Clear test names** describing what is tested

**Example:**
```python
import pytest
from pathlib import Path
from package_name.parsers.csv_parser import parse_csv

@pytest.fixture
def valid_csv(tmp_path: Path) -> Path:
    """Create valid test CSV file."""
    csv_file = tmp_path / "test.csv"
    csv_file.write_text(
        "name,age,email\n"
        "Alice,30,alice@example.com\n"
        "Bob,25,bob@example.com\n"
    )
    return csv_file

def test_parse_valid_csv(valid_csv):
    """Test parsing valid CSV file."""
    result = parse_csv(valid_csv)

    assert len(result) == 2
    assert result[0]["name"] == "Alice"
    assert result[0]["age"] == "30"
    assert result[1]["name"] == "Bob"

def test_parse_nonexistent_file():
    """Test error when file doesn't exist."""
    with pytest.raises(FileNotFoundError):
        parse_csv(Path("nonexistent.csv"))

@pytest.mark.parametrize("encoding", ["utf-8", "latin-1", "cp1252"])
def test_parse_different_encodings(tmp_path, encoding):
    """Test parsing with different encodings."""
    csv_file = tmp_path / f"test_{encoding}.csv"
    csv_file.write_text("name\nAlice\n", encoding=encoding)

    result = parse_csv(csv_file, encoding=encoding)
    assert len(result) == 1
```

#### Step E3: Follow Best Practices
- Use **generators** for memory efficiency (large files)
- Use **async/await** for I/O-bound operations (if applicable)
- Use **dataclasses** or **Pydantic** for data structures
- Follow **constitution** principles

### V - Validate (Run Verification)

#### Step V1: Run Tests
```bash
uv run pytest tests/ -v
```
**Gate:** All tests must pass ✅

#### Step V2: Check Coverage
```bash
uv run pytest --cov=src --cov-report=term-missing
```
**Gate:** Coverage must be ≥ target (e.g., 85%) ✅

#### Step V3: Type Check
```bash
uv run pyright src/
# OR
uv run mypy src/
```
**Gate:** Zero type errors ✅

#### Step V4: Lint
```bash
uv run ruff check src/
```
**Gate:** Zero linting errors ✅

#### Step V5: Format Check
```bash
uv run ruff format --check src/
```
**Gate:** No formatting changes needed ✅

#### Step V6: Verify Acceptance Criteria
Check that task satisfies relevant acceptance criteria from design.md

### D - Document (Update State)

#### Step D1: Update Task Status
In `plan.md`:
- Change task status: "doing" → "done"
- Set completed date: YYYY-MM-DD
- Update progress percentage

#### Step D2: Update Coverage
If tests were run, update **Coverage** field in Status section with actual coverage

#### Step D3: Recalculate Progress
```
Progress = (completed_tasks / total_tasks) * 100
```

#### Step D4: Update CLAUDE.md
Add to working memory:
- What was implemented
- Key decisions made
- Any learnings or gotchas
- What's next

#### Step D5: Regenerate State
Run state-tracker.py to update state.json

#### Step D6: Confirm Completion
Display summary:
```
✅ Task TK-02 completed

Implementation:
- Created src/package_name/parsers/csv_parser.py
- Implemented parse_csv() with full type hints
- Added comprehensive error handling

Tests:
- Wrote 8 tests in test_csv_parser.py
- All tests passing ✅
- Coverage: 92% ✅

Verification:
✅ Tests passed (8/8)
✅ Coverage: 92% (target: 85%)
✅ Type check: 0 errors
✅ Linting: 0 errors
✅ Formatting: compliant

Updated:
- plan.md: TK-02 status → done
- Progress: 28% → 42%
- CLAUDE.md: Added implementation notes

Next task: TK-03 - Add input validation
```

## Output
- **Code:** Implementation files created/modified
- **Tests:** Test files created/modified
- **Plan:** Task status updated to "done"
- **Coverage:** Actual coverage recorded
- **Memory:** CLAUDE.md updated with learnings

## Validation Checklist
- ✅ All verification gates passed
- ✅ Type hints complete for all functions
- ✅ Docstrings present (Google/NumPy style)
- ✅ Tests written and passing
- ✅ Coverage meets or exceeds target
- ✅ plan.md updated with completion date
- ✅ CLAUDE.md updated with notes
- ✅ state.json regenerated

## Next Steps
- If more tasks remain: `/work SLUG TK-##` for next task
- If all tasks done: `/verify SLUG` to run full verification
