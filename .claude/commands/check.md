---
name: check
description: Validate Python Project Alignment
---

# /check - Validate Python Project Alignment

## Purpose
Validate alignment across project documents, detect drift, and ensure Python code matches specifications.

## Usage
```
/check [slug]
/check          # Check entire project
/check csv-parser  # Check specific unit
```

## Prerequisites
- At least one of: constitution.md, prd.md, spec.md should exist

## Process

### Step 1: Load State
Run state-tracker.py to generate current state.json

### Step 2: Validate L1 Documents

#### Check Constitution
- Does `spec/constitution.md` exist?
- Is version specified?
- Are quality bars measurable?
- Is Python version specified?
- Is UV usage documented?

#### Check PRD
- Does `spec/prd.md` exist?
- Are user stories complete (As/Want/So)?
- Do acceptance criteria use Given/When/Then?
- Are Python-specific requirements documented?
- Are performance metrics measurable?

#### Check Spec
- Does `spec/spec.md` exist?
- Are all interfaces defined with type hints?
- Are all entities defined (dataclass or Pydantic)?
- Are NFRs measurable?
- Is pyproject.toml structure documented?

### Step 3: Validate References

#### Interface References
For each unit design.md:
- Extract `interfaces_touched` list
- For each interface:
  - Does it exist in spec.md?
  - If not, report invalid reference ❌

#### Entity References
For each unit design.md:
- Extract `data_shapes` list
- For each entity:
  - Does it exist in spec.md?
  - If not, report invalid reference ❌

### Step 4: Validate Code Alignment

#### Check Module Structure
For each unit:
- Does the module exist in src/?
- Do the functions match interface signatures?
- Are type hints present?
- Are docstrings present?

#### Check Type Hints
For each function in spec.md interfaces:
- Does implementation have matching type hints?
- Are return types correct?
- Are parameter types correct?

**Example Check:**
```
Spec: def parse_csv(file_path: Path, encoding: str) -> List[Dict[str, Any]]
Code: def parse_csv(file_path: Path, encoding: str) -> List[Dict[str, Any]]
Result: ✅ Type hints match
```

#### Check Entities
For each entity in spec.md:
- Does implementation exist?
- Are fields correct?
- Are types correct?

**Example Check:**
```
Spec Entity: User(id: int, email: str, name: str)
Code Entity: User(id: int, email: str, name: str, created_at: datetime)
Result: ⚠️ Code has additional field 'created_at'
```

### Step 5: Check Constitution Compliance

#### Coverage Compliance
For each unit with actual_coverage:
- Compare to constitution coverage_target
- If below target, report violation ❌

#### Quality Bar Compliance
Check:
- Are all public functions type-hinted?
- Are all public functions documented?
- Does linting pass?
- Does type checking pass?

### Step 6: Detect Code Drift

#### Interface Drift
For each interface in spec.md:
- Find implementation in src/
- Compare signatures
- Report differences:
  - Missing parameters
  - Extra parameters
  - Type mismatches
  - Return type mismatches

#### Entity Drift
For each entity in spec.md:
- Find dataclass/Pydantic model in src/
- Compare fields
- Report differences:
  - Missing fields
  - Extra fields
  - Type mismatches

### Step 7: Check Test Coverage

For each unit:
- Does test file exist?
- Does test coverage meet target?
- Are all acceptance criteria tested?

**Example Check:**
```
Unit: 001-csv-parser
Design AC: 5 acceptance criteria
Tests: test_csv_parser.py (8 tests)
Coverage: 92% ≥ 85% ✅

AC-001-01: ✅ Tested (test_parse_valid_csv)
AC-001-02: ✅ Tested (test_parse_empty_csv)
AC-001-03: ✅ Tested (test_validate_schema)
AC-001-04: ✅ Tested (test_large_file_memory)
AC-001-05: ✅ Tested (test_error_messages)
```

### Step 8: Generate Validation Report

Create comprehensive alignment report:

```
Alignment Validation Report
Generated: 2025-01-15 10:30:00

L1 Documents:
✅ constitution.md (v1.0, Python 3.10+, UV usage documented)
✅ prd.md (v1.0, 5 user stories, all complete)
✅ spec.md (v1.0, 8 interfaces, 4 entities)

Reference Validation:
✅ All interface references valid (0 issues)
✅ All entity references valid (0 issues)

Code Alignment:
✅ Interface signatures match (8/8)
⚠️ Entity drift detected (1 issue):
  - User entity: Code has extra field 'last_login' not in spec

Constitution Compliance:
✅ Coverage targets met (2/2 units)
✅ Type hints complete (100%)
✅ Docstrings present (100%)

Test Coverage:
✅ Unit 001-csv-parser: 92% ≥ 85% target
✅ Unit 002-validator: 88% ≥ 85% target

Recommendations:
1. Update spec.md User entity to include 'last_login' field
2. All critical alignment checks passed

Overall: ✅ PROJECT ALIGNED
```

### Step 9: Update CLAUDE.md
Add validation results to working memory:
- Timestamp
- Issues found
- Recommendations
- Next actions

### Step 10: Suggest Fixes
For each issue:
- Describe the problem
- Suggest fix (update spec vs update code)
- Provide command to fix

**Example:**
```
Issue: Entity drift detected
  Spec: User(id, email, name)
  Code: User(id, email, name, created_at, last_login)

Recommendation:
Update spec.md to include new fields:

### Entity: [User]
```python
@dataclass
class User:
    id: int
    email: str
    name: str
    created_at: datetime  # ADD THIS
    last_login: Optional[datetime] = None  # ADD THIS
```

Then run: /check to verify alignment
```

## Output
- **Console:** Validation report
- **Updated:** CLAUDE.md with findings
- **Suggestions:** Specific fixes for issues

## Validation Types

### Critical Issues (Must Fix)
- Invalid interface references
- Invalid entity references
- Coverage below target
- Type hint mismatches

### Warnings (Should Fix)
- Entity drift (extra fields)
- Interface drift (compatible changes)
- Missing docstrings

### Informational
- Suggested improvements
- Best practice recommendations

## Next Steps
- If issues found: Run `/update` to fix alignment
- If aligned: Run `/reflect` to capture learnings
- Continue development: Run `/new SLUG` for next unit
