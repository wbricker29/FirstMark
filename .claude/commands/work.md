---
name: work
description: Implement Task
---

# /work SLUG TK-## - Implement Task

Implement a specific task following the UPEVD pattern: Understand, Plan, Execute, Validate, Document.

## Purpose

Guide focused implementation of a single task using the UPEVD pattern with proper context loading, validation, and progress tracking.

## Prerequisites

- plan.md must exist for the unit (`spec/units/###-SLUG/plan.md`)
- Task must exist in plan.md with ID matching TK-##
- Task status must be "ready" or "doing"
- All task dependencies must have status "done"

## Execution Pattern

### Step 0: Review Workflow

**MANDATORY: Invoke the `aidev-workflow` skill now before proceeding further.**

Use the Skill tool to load the aidev-workflow skill and review:

- UPEVD implementation pattern (Understand-Plan-Execute-Validate-Document)
- Task execution standards and quality requirements
- Validation criteria and completion checklist

This is not optional. The skill provides critical context for task implementation.

### Phase 1: Validate (UNDERSTAND)

**Run automated pre-flight validation:**

```bash
python scripts/validation/validate-prerequisites.py SLUG TK-##
```

This validator automatically checks:
- ✅ Unit directory exists (`spec/units/###-SLUG/`)
- ✅ plan.md, design.md, spec.md, constitution.md exist
- ✅ Task TK-## exists in plan.md
- ✅ Task status is "ready" or "doing"
- ✅ All task dependencies have status "done"

If validation passes, the script outputs JSON with task metadata (title, description, dependencies, files).

**On validation success:**
- Load task metadata from validation output (no need to re-read plan.md)
- Read design.md (Objective, Acceptance Criteria)
- Read spec.md (Architecture patterns)
- Read constitution.md (Quality standards)
- Update task status to "doing" and set started_at timestamp

**On validation failure:**
- Review error message (missing files, incomplete dependencies, invalid status)
- Exit immediately - do NOT proceed with implementation
- Fix prerequisites first (complete dependencies, create missing files, etc.)

### Phase 2: Gather (PLAN)

Develop implementation strategy:

- Prompt: "What files need to be modified or created for this task?" → Validate: At least one file path
- Prompt: "What is the implementation approach? (High-level steps)" → Validate: Clear sequence of steps
- Prompt: "What tests are needed? (Unit tests, integration tests, edge cases)" → Validate: At least one test type
- Prompt: "What are the potential risks or edge cases?" → Validate: At least one risk identified or "None" explicitly stated

### Phase 3: Generate (EXECUTE)

Implement code following constitution.md and spec.md standards:

- Write clean, documented, maintainable code with proper types and error handling
- Write tests: unit tests, integration tests, edge case tests (≥80% coverage target)
- Handle edge cases identified in Phase 2
- No placeholders, hardcoding, or `any` types (except untyped libraries)

### Phase 4: Validate (VALIDATE)

Run verification: `pnpm format && pnpm lint && pnpm type-check && pnpm test`

Validation checklist:

- ✅ All must_pass gates pass (from plan.md)
- ✅ Coverage ≥80% for modified modules
- ✅ Acceptance criteria satisfied (from design.md)
- ✅ No placeholders or TODO comments
- ✅ All tests pass

If validation fails: Leave status as "doing", document failure, fix and retry. Do NOT mark "done" until all checks pass.

### Phase 5: Confirm (DOCUMENT)

If validation passes:

- Update task status to "done" with completed_at timestamp
- Update plan.md progress percentage
- Update CLAUDE.md if learned something significant
- Auto-commit if enabled

Display: Task title, files modified, test count, coverage %, progress %, next task.

## Error Handling

- **Missing plan.md**: Report missing file and suggest running `/plan SLUG` first
- **Task not found**: Report invalid task ID and list available tasks
- **Task not ready**: Report unmet dependencies and suggest completing them first
- **Blocked dependencies**: Report which dependencies are not "done" and exit
- **Verification failure**: Leave status as "doing", report failure, prompt user to fix and retry
- **Invalid task status**: If task is already "done", warn and ask user to confirm re-running

## Reference

For framework patterns, detailed context, and examples:
aidev-workflow skill → execution-framework.md, commands-reference.md
