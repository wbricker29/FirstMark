---
name: update
description: Update Python Project Documents
---

# /update - Update Python Project Documents

## Purpose
Apply coordinated updates across project artifacts (constitution, prd, spec, designs, plans) to maintain alignment.

## Usage
```
/update <document> <path>
/update spec interfaces#parse_document
/update spec entities#User
/update prd user-stories
/update constitution quality-bars
```

## Prerequisites
- Target document must exist
- Should run `/check` first to identify what needs updating

## Process

### Step 1: Parse Update Target
Extract:
- Document name (constitution, prd, spec, design, plan)
- Section path (e.g., interfaces#parse_document)
- Unit slug (if updating unit-specific docs)

### Step 2: Load Current Content
- Read target document
- Parse Markdown structure
- Locate target section

### Step 3: Gather Update Information
Ask user:
- What needs to change?
- Why is this change needed?
- What's the new value/content?

### Step 4: Validate Python Syntax
If updating Python code sections:

#### For Interfaces
Verify:
- Function signature has complete type hints
- Docstring follows Google/NumPy style
- Parameters documented with types
- Return type documented
- Exceptions documented

**Example:**
```python
from pathlib import Path
from typing import List, Dict, Any, Optional

def parse_document(
    file_path: Path,
    encoding: str = "utf-8",
    validate: bool = False,
    schema: Optional[Dict[str, Any]] = None  # NEW PARAMETER
) -> List[Dict[str, Any]]:
    """Parse document from file.

    Args:
        file_path: Path to document file
        encoding: Character encoding (default: utf-8)
        validate: Whether to validate against schema
        schema: Validation schema (required if validate=True)  # NEW

    Returns:
        List of parsed records

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If validation fails or schema invalid  # UPDATED
    """
    pass
```

#### For Entities
Verify:
- Uses dataclass or Pydantic BaseModel
- All fields have type hints
- Field descriptions documented
- Constraints specified

**Example:**
```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class User:
    """User entity."""
    id: int
    email: str
    name: str
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None  # NEW FIELD
```

### Step 5: Apply Update
- Modify target document
- Update version number
- Update timestamp
- Add change note (if applicable)

### Step 6: Propagate Changes

#### If Updating spec.md Interface
Propagate to:
1. **Affected unit designs:** Update interfaces_touched
2. **Code implementation:** Flag for update
3. **Tests:** Flag for review

#### If Updating spec.md Entity
Propagate to:
1. **Affected unit designs:** Update data_shapes
2. **Data models:** Flag for update
3. **Database migrations:** Flag for creation

#### If Updating Constitution Quality Bars
Propagate to:
1. **All unit plans:** Update coverage target
2. **CI configuration:** Update thresholds
3. **CLAUDE.md:** Document change

### Step 7: Identify Impacted Units
Scan all units to find:
- Which designs reference updated interface/entity?
- Which plans need verification commands updated?
- Which implementations need code changes?

### Step 8: Create Update Checklist
Generate checklist of required changes:

```
Update Checklist for spec.md Interface: parse_document

Spec Changes:
✅ Updated parse_document signature (added schema parameter)
✅ Updated docstring
✅ Incremented version: 1.0 → 1.1

Propagation Required:
⬜ Unit 001-csv-parser design.md (references parse_document)
  - Review if new parameter affects design

⬜ src/package_name/parsers/csv_parser.py
  - Add schema parameter to implementation
  - Update type hints
  - Update docstring

⬜ tests/test_parsers/test_csv_parser.py
  - Add tests for schema parameter
  - Test validation logic

⬜ Unit 001-csv-parser plan.md
  - Add task for schema validation if not present
  - Update verification to test new parameter

Next Steps:
1. Review design: /check csv-parser
2. Update code: /work csv-parser TK-NEW
3. Run tests: /verify csv-parser
```

### Step 9: Execute Updates
For each item in checklist:
- Update document
- Increment version if needed
- Update timestamp
- Mark as complete ✅

### Step 10: Validate Alignment
Run `/check` to verify:
- All references still valid
- No new drift introduced
- Python syntax correct
- Type hints complete

### Step 11: Update CLAUDE.md
Document:
- What was updated and why
- Which units were affected
- What actions were taken
- Any learnings

### Step 12: Generate Update Report

```
Update Report: spec.md Interface parse_document
Generated: 2025-01-15 10:30:00

Changes Made:
✅ Added 'schema' parameter (Optional[Dict[str, Any]])
✅ Updated docstring with new parameter
✅ Updated Raises section (added schema validation error)
✅ Incremented version: 1.0 → 1.1

Propagated To:
✅ Unit 001-csv-parser design.md (reviewed, no changes needed)
✅ src/package_name/parsers/csv_parser.py (updated)
✅ tests/test_parsers/test_csv_parser.py (added 3 tests)
✅ Unit 001-csv-parser plan.md (added TK-08 for schema validation)

Verification:
✅ All references valid
✅ Type hints complete
✅ Tests passing (11/11)
✅ Coverage: 94% ≥ 85%

Result: ✅ UPDATE COMPLETE AND VERIFIED
```

## Common Update Scenarios

### Scenario 1: Add Field to Entity
```
/update spec entities#User

What to add: last_login field
Type: Optional[datetime]
Default: None
Reason: Track user activity for analytics
```

**Propagates to:**
- Data models in src/
- Database migrations
- Unit designs using User entity
- Tests for User entity

### Scenario 2: Add Parameter to Interface
```
/update spec interfaces#parse_csv

What to add: max_rows parameter
Type: Optional[int]
Default: None
Reason: Allow limiting parsed rows for testing
```

**Propagates to:**
- Function implementations
- Function tests
- Unit designs calling this interface

### Scenario 3: Update Coverage Target
```
/update constitution quality-bars

What to change: coverage_target
New value: 0.90 (90%)
Old value: 0.85 (85%)
Reason: Raising quality standards
```

**Propagates to:**
- All unit plans (coverage target)
- CI configuration
- Verification gates

## Output
- **Updated:** Target document with changes
- **Checklist:** Required propagation actions
- **Report:** Summary of changes and impacts
- **CLAUDE.md:** Documentation of update

## Validation
- ✅ Python syntax valid
- ✅ Type hints complete
- ✅ Docstrings updated
- ✅ Versions incremented
- ✅ Timestamps updated
- ✅ Propagation complete
- ✅ Alignment verified

## Next Steps
- Run `/check` to verify alignment
- Update affected code with `/work`
- Run `/verify` on affected units
