---
name: new
description: Create New Python Unit
---

# /new - Create New Python Unit

## Purpose
Create a new development unit (feature) with design document for Python implementation.

## Usage
```
/new <slug>
```

**Example:**
```
/new csv-parser
/new user-authentication
/new data-validation
```

## Prerequisites
- `spec/spec.md` should exist (run `/spec` first)

## Process

### Step 1: Determine Unit Number
- Scan `spec/units/` directory
- Find highest existing unit number (###)
- Increment by 1 for new unit

### Step 2: Create Directory
Create `spec/units/###-SLUG/` directory

### Step 3: Gather Design Information
Ask user about:
- **Objective:** What does this unit accomplish?
- **Success Metrics:** How do we measure completion?
- **Behavior:** What is the expected behavior?
- **Inputs/Outputs:** Function signatures with types
- **Edge Cases:** What edge cases need handling?

### Step 4: Python Interface Design
For each function:
- Function name (snake_case)
- Type hints for all parameters
- Return type hint
- Docstring (Google or NumPy style)
- Examples

**Example:**
```python
from pathlib import Path
from typing import List, Dict, Any

def parse_csv(
    file_path: Path,
    encoding: str = "utf-8",
    validate: bool = False
) -> List[Dict[str, Any]]:
    """Parse CSV file into list of dictionaries.

    Args:
        file_path: Path to CSV file
        encoding: Character encoding (default: utf-8)
        validate: Whether to validate rows

    Returns:
        List of parsed records as dictionaries

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If encoding is invalid
    """
    pass
```

### Step 5: Interface & Data References
Ask:
- Which interfaces from spec.md does this touch?
- Which entities from spec.md does this use?
- **Validate:** All references exist in spec.md

### Step 6: Constraints
Document:
- Functional constraints
- Non-functional constraints (performance, memory)
- Python-specific constraints (use generators, async/await, etc.)

### Step 7: Acceptance Criteria
Define testable criteria in Given-When-Then format:

**Example:**
- **AC-001-01:** Parse Valid CSV
  - Given: A valid CSV file with headers
  - When: parse_csv() is called
  - Then: Return list of dicts with correct values

Assign IDs: AC-[UNIT]-01, AC-[UNIT]-02, etc.

### Step 8: Dependencies
Document:
- What blocks this unit?
- What does this unit block?

### Step 9: Implementation Notes
Add:
- Suggested approach with code examples
- Testing strategy (pytest fixtures, parametrize)
- Test examples
- Coverage target for this unit

### Step 10: Validate References
For each interface/entity referenced:
- Verify it exists in `spec/spec.md`
- If not found, warn user:
  - Update spec.md first, or
  - Revise design to use existing references

### Step 11: Generate Design
Create `spec/units/###-SLUG/design.md` with:
- All gathered information
- Status: "draft"
- Timestamps
- Python-specific sections

### Step 12: Validate Design
Check that:
- Directory created with correct numbering
- design.md exists and is valid Markdown
- All spec.md references are valid
- Acceptance criteria are testable
- Type hints are complete
- All required fields present

### Step 13: Confirm
Display summary:
- Unit created: ###-SLUG
- Interfaces touched: [list]
- Entities used: [list]
- Acceptance criteria count
- Next step: Run `/plan SLUG` to generate task breakdown

## Output
- **Directory:** `spec/units/###-SLUG/`
- **File:** `spec/units/###-SLUG/design.md`
- **Status:** draft

## Example Interaction
```
User: /new csv-parser

Claude: Creating new unit for CSV parser. This will be unit 001.

What is the objective? (1-2 sentences)
User: Parse CSV files into structured dictionaries for data processing

What success metrics define completion?
User: Parse 10k rows/second, handle files up to 1GB, 99% accuracy

[Gathering interface design...]

Which interfaces from spec.md does this implement?
User: parse_document

Which entities does this create?
User: Record

Checking references against spec.md...
✅ Interface 'parse_document' exists in spec.md
✅ Entity 'Record' exists in spec.md

Unit created: spec/units/001-csv-parser/
- Status: draft
- Interfaces: parse_document
- Entities: Record
- Acceptance criteria: 5 (AC-001-01 through AC-001-05)
- Type hints: Complete

Next step: Run `/plan csv-parser` to generate task breakdown
```

## Validation
- ✅ Directory created: `spec/units/###-SLUG/`
- ✅ design.md exists with valid Markdown
- ✅ All spec.md references are valid
- ✅ All functions have type hints
- ✅ Acceptance criteria in Given-When-Then format
- ✅ Test examples provided
- ✅ Status is "draft"

## Next Steps
Run `/plan SLUG` to break down the design into implementation tasks
