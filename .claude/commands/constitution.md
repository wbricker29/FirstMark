---
name: constitution
description: Create Python Project Governance
---

# /constitution - Create Python Project Governance

## Purpose
Establish non-negotiable Python development principles, quality bars, and constraints.

## Usage
```
/constitution
```

## Prerequisites
- None (this is typically the first command to run)

## Process

### Step 1: Gather Information
Ask the user about:
- Python version requirements (minimum 3.10+)
- Code quality standards (PEP 8, type hints, docstrings)
- Testing requirements (coverage target, pytest)
- Type checking preferences (mypy vs pyright)
- Performance constraints
- Security requirements

### Step 2: Define Principles
Establish:
- **KISS:** Simple, readable Python code
- **YAGNI:** Build only what's needed
- **Type Safety:** Comprehensive type hints
- **Testing:** pytest with high coverage

### Step 3: Set Quality Bars
Define measurable standards:
- Coverage target (default: 85%)
- Type checking strictness
- Code formatting (ruff)
- Linting rules (ruff)

### Step 4: Document Constraints
Capture:
- Python version (e.g., 3.10+)
- Package manager (UV)
- Project structure (src/ layout)
- Dependency management

### Step 5: Create Constitution
Generate `spec/constitution.md` using CONSTITUTION-TEMPLATE.md with:
- All gathered information
- Python-specific sections
- UV workflow commands
- pytest and type checking requirements

### Step 6: Validate
Check that:
- File created at correct path
- All sections populated
- Quality bars are measurable
- Constraints are specific

### Step 7: Confirm
Display summary and next steps

## Output
- **File:** `spec/constitution.md`
- **Status:** Active governance document

## Next Steps
Run `/prd` to capture product requirements
