---
unit_id: "[###-slug]"
version: "1.0"
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
---

# Unit Plan Template

Volatile task breakdown and verification plan

## Tasks

### TK-01

- **Title:** [Task title]
- **Description:** [Detailed description of what needs to be done]
- **Status:** ready
- **Priority:** high
- **Dependencies:** None
- **Note:** None
- **Completed:** null

### TK-02

- **Title:** [Another task]
- **Description:** [Description]
- **Status:** ready
- **Priority:** medium
- **Dependencies:** TK-01
- **Note:** Per investigation...
- **Completed:** null

### TK-03

- **Title:** [Final task]
- **Description:** [Description]
- **Status:** ready
- **Priority:** medium
- **Dependencies:** TK-01, TK-02
- **Note:** None
- **Completed:** null

## Verification

### Commands

1. **[e.g., pytest tests/]** - Run unit tests (must pass: ✅)
2. **[e.g., pyright .]** - Type checking (must pass: ✅)
3. **[e.g., ruff check .]** - Linting (must pass: ✅)

### Gates

- **tests:** must pass ✅
- **type_check:** must pass ✅
- **coverage:** must pass ✅

### Coverage Target

85% (0.85)

### Acceptance References

- AC-[UNIT]-01
- AC-[UNIT]-02
