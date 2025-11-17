---
name: new
description: Create New Unit
---

# /new SLUG - Create New Unit

Initialize a new unit of work (feature) with a design document that captures stable intent and acceptance criteria.

## Purpose

This command establishes a new unit of work by creating a design document that serves as the single source of truth for feature intent. It ensures all stakeholders agree on scope, behavior, and acceptance criteria before implementation begins, reducing rework and scope creep.

## Prerequisites

- `spec/spec.md` must exist
- `.claude/skills/aidev-workflow/assets/templates/DESIGN-TEMPLATE.md` must exist

## Execution Pattern

### Step 0: Review Workflow

**Before proceeding, invoke the aidev-workflow skill to review:**

- Unit creation patterns and design document structure
- Acceptance criteria definition standards
- Design document validation requirements

### Phase 1: Validate

Before proceeding, verify:

- ✅ `spec/spec.md` exists and is readable
- ✅ `.claude/skills/aidev-workflow/assets/templates/DESIGN-TEMPLATE.md` exists and is readable
- ✅ SLUG argument is provided and valid (lowercase, hyphenated, no spaces)
- ✅ `spec/units/` directory exists or can be created

### Phase 2: Gather

Ask the user these specific questions in order:

- Prompt: "What is the primary objective of this unit? (1-2 sentences describing the core goal)" → Validate: Non-empty, clear, concise
- Prompt: "What are the expected behaviors? (List key user-facing behaviors or system outcomes)" → Validate: At least one behavior, specific and observable
- Prompt: "What interfaces, data structures, or schemas are involved? (APIs, database tables, types, etc.)" → Validate: At least one interface or "None" explicitly stated
- Prompt: "What are the key constraints? (Performance requirements, dependencies, limitations)" → Validate: At least one constraint or "None" explicitly stated
- Prompt: "What are the acceptance criteria? (Specific, testable conditions for completion)" → Validate: At least 2 criteria, each testable and specific

### Phase 3: Generate

1. Determine next unit number by scanning `spec/units/` (e.g., 001, 002, 003)
2. Create directory: `spec/units/###-SLUG/`
3. Load template from `.claude/skills/aidev-workflow/assets/templates/DESIGN-TEMPLATE.md`
4. Populate template sections with gathered information:
   - Metadata: unit number, slug, status "draft", created date
   - Objective: primary objective (from Phase 2)
   - Behavior: expected behaviors (from Phase 2)
   - Interfaces: interfaces/data (from Phase 2)
   - Constraints: key constraints (from Phase 2)
   - Acceptance Criteria: testable criteria (from Phase 2)
5. Write `spec/units/###-SLUG/design.md`
6. Validate all references to `spec/spec.md` are valid section IDs

### Phase 4: Validate

Run these checks before confirming:

- ✅ design.md created at correct path
- ✅ All template sections populated (no placeholders)
- ✅ Status set to "draft"
- ✅ At least 2 acceptance criteria defined
- ✅ All spec.md references valid
- ✅ File is valid markdown and readable

### Phase 5: Confirm

Display to user:

```
Created unit: ###-SLUG
Location: spec/units/###-SLUG/design.md
Status: draft
Next step: Review design.md and run /plan when ready
```

## Error Handling

- **Missing prerequisites**: Report missing file and exit (e.g., "spec/spec.md not found")
- **Invalid SLUG**: Reject and prompt for valid format (lowercase, hyphenated, no spaces)
- **Duplicate unit number**: Auto-increment to next available number
- **Template missing**: Report missing template and exit
- **Invalid spec.md reference**: Report invalid reference and ask user to correct

## Reference

For framework patterns, detailed context, and examples:
aidev-workflow skill → execution-framework.md, commands-reference.md
