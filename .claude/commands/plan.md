---
name: plan
description: Generate Unit Plan
---

# /plan SLUG - Generate Unit Plan

Generate implementation plan from an approved design, creating a task breakdown with verification plan and progress tracking.

## Purpose

This command translates a design document into an actionable implementation plan. It breaks down the work into discrete, sequenced tasks with clear verification criteria, enabling incremental progress tracking and ensuring nothing is overlooked during implementation.

## Prerequisites

- design.md must exist for the specified unit (`spec/units/###-SLUG/design.md`)
- design.md status should be "approved" or "draft"
- `spec/spec.md` must exist
- `spec/constitution.md` must exist

## Execution Pattern

### Step 0: Review Workflow

**MANDATORY: Invoke the `aidev-workflow` skill now before proceeding further.**

Use the Skill tool to load the aidev-workflow skill and review:

- Plan generation methodology and task breakdown patterns
- Verification gate configuration and quality standards
- Task dependency modeling and DAG validation

This is not optional. The skill provides critical context for plan generation.

### Phase 1: Validate

Before proceeding, verify:

- ✅ Unit directory exists (`spec/units/###-SLUG/`)
- ✅ design.md exists and is readable
- ✅ design.md has all required sections (Objective, Behavior, Acceptance Criteria)
- ✅ `spec/spec.md` exists and is readable
- ✅ `spec/constitution.md` exists and is readable

### Phase 2: Gather

Load context automatically (no user prompts):

- Read design.md, spec.md (patterns), constitution.md (quality standards, gates)
- Identify implementation patterns and quality gates

### Phase 3: Generate

1. Task breakdown (TK-01, TK-02...):
   - Order: Data models → Core logic → Integration → Tests
   - Each task: 1-3 files, <4 hours, status "ready"
   - Include: ID, title, description, priority, estimate, dependencies
   - Ensure valid DAG (no cycles)

2. Verification section:
   - Extract must_pass gates from constitution.md
   - Coverage target ≥80%, verification commands

3. Status section: progress 0%, created_at timestamp, status "planning"

4. Write `spec/units/###-SLUG/plan.md` (Metadata, Tasks, Verification, Status)

### Phase 4: Validate

Run these checks before confirming:

- ✅ plan.md created at correct path
- ✅ All tasks have unique IDs (TK-01, TK-02, etc.)
- ✅ All tasks have status "ready"
- ✅ All dependencies reference valid task IDs
- ✅ No circular dependencies
- ✅ At least one verification gate defined
- ✅ Coverage target specified (≥80%)
- ✅ File is valid markdown and readable

### Phase 5: Confirm

Display: Plan location, task count (TK-01 through TK-##), verification gates count, next step (/work ###-SLUG TK-01).

### Phase 6: Capture Follow-ups

- Add a final task to the generated plan for any required downstream clean-up (e.g., updating documentation/scripts to cover new structural metadata such as `chunk_index` ordering) so no design-aligned modifications are dropped once implementation begins.

## Integration

- **Runs after /new**: Requires approved design.md to exist
- **Informs /work**: Tasks become input for UPEVD implementation pattern
- **Validated by /verify**: Verification section defines quality gates for the unit
- **Tracked by /check**: State-tracker.py reads plan.md to generate progress metrics in state.json

## Error Handling

- **Missing design.md**: Report missing file and suggest running `/new SLUG` first
- **Invalid design status**: Warn if status is not "approved" or "draft", ask user to confirm proceeding
- **Incomplete design.md**: Report missing required sections and exit
- **Circular dependencies**: Report cycle and ask user to manually resolve
- **Invalid task ID format**: Auto-correct to TK-## format
- **Missing constitution.md**: Warn and use default gates (linting, type checking, tests)

## Reference

For framework patterns, detailed context, and examples:
aidev-workflow skill → execution-framework.md, commands-reference.md
