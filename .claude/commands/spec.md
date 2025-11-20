---
name: spec
description: Create Engineering Contract
---

# /spec - Create Engineering Contract

Define architecture, interfaces, data models, and non-functional requirements. This is the technical contract between product (PRD) and implementation.

## Purpose

Translate product requirements into technical design. Define architecture, interfaces, data models, and non-functional requirements as the contract between PRD and implementation.

## Prerequisites

- `spec/constitution.md` must exist
- `spec/PRD.md` must exist

## Execution Pattern

### Step 0: Review Workflow

**Before proceeding, invoke the aidev-workflow skill to review:**

- Engineering specification structure and interface contract patterns
- Architecture pattern selection and documentation standards
- NFR definition and measurement methodology

### Phase 1: Validate

1. Check that `spec/constitution.md` exists
2. Check that `spec/PRD.md` exists
3. If missing, error: "Prerequisites not met. Run /constitution and /prd first."
4. Check if `spec/spec.md` already exists
5. If exists, ask user: "Spec already exists. Overwrite (o), update (u), or cancel (c)?"
6. Load template from `.claude/skills/aidev-workflow/assets/templates/SPEC-TEMPLATE.md`
7. Verify template exists and is valid markdown
8. Detect project stack (package.json, tsconfig.json, etc.) for smart defaults

### Phase 2: Gather

Ask user these questions (provide smart defaults based on detected stack):

1. **Prompt:** "Architecture pattern? (e.g., ports-and-adapters, layered, microservices, RAG pipeline)"
   → Validate: Pattern recognized and appropriate | Default: Next.js → layered + server actions
   → Follow-up: "Why this pattern?" (captures rationale)

2. **Prompt:** "Core modules/components? (3-7 major modules, each with responsibility)"
   → Validate: Each has responsibility, location, dependencies | Default: Suggest from PRD + stack

3. **Prompt:** "Data flow: key steps from input to output?"
   → Validate: Clear start/end, references modules | Default: Suggest from architecture pattern

4. **Prompt:** "Critical interfaces? (2-5 key interfaces with inputs, outputs, errors)"
   → Validate: Each has module, description, typed inputs/outputs, errors, pre/postconditions
   → Default: Suggest from PRD acceptance criteria

5. **Prompt:** "Data models/entities? (2-5 core entities with fields and relationships)"
   → Validate: Each has description, typed fields, constraints, relationships
   → Default: Suggest from PRD scope + architecture

6. **Prompt:** "Non-functional requirements? (performance, reliability, observability, security)"
   → Validate: Each has requirement + measurement method; aligns with constitution
   → Default: Pull from constitution, suggest stack defaults

### Phase 3: Generate

1. Populate template with gathered information
2. Format architecture (pattern + rationale), modules (dependencies + locations)
3. Write data flow (numbered steps), interfaces (full contracts)
4. Create data model (entities + fields + constraints), NFRs (measurement methods)
5. Write to `spec/spec.md`

### Phase 4: Validate

Run these checks before confirming:

- ✅ File exists at `spec/spec.md`
- ✅ Architecture pattern is stated with rationale
- ✅ At least 3 modules defined with responsibilities
- ✅ Data flow references defined modules
- ✅ At least 2 interfaces with complete contracts
- ✅ All interface inputs/outputs specify types
- ✅ At least 2 entities with fields and constraints
- ✅ NFRs include performance, reliability, observability, security
- ✅ All NFRs specify measurement method
- ✅ Spec aligns with PRD acceptance criteria
- ✅ Spec adheres to constitution constraints
- ✅ Valid markdown structure with proper headings

### Phase 5: Confirm

Display summary to user:

```
✅ Engineering Spec created: spec/spec.md

Architecture: [pattern]
Modules: [count]
Interfaces: [count]
Entities: [count]
NFRs: [count] requirements

Next: Run /new [feature-id] to start feature development
```

## Error Handling

**Missing prerequisites:**

- Error: "spec/constitution.md not found. Run /constitution first."
- Error: "spec/PRD.md not found. Run /prd first."
- Resolution: Run prerequisite commands in order

**Missing template:**

- Error: "Template not found at .claude/skills/aidev-workflow/assets/templates/SPEC-TEMPLATE.md"
- Resolution: Check file exists, suggest creating from reference

**Stack detection failure:**

- Warning: "Could not detect project stack. Provide manual defaults."
- Resolution: Continue with generic prompts, no smart defaults

**Misalignment with PRD:**

- Warning: "Interface [name] doesn't map to any PRD acceptance criteria"
- Resolution: Ask user to confirm or revise interface

**Misalignment with constitution:**

- Error: "NFR [name] conflicts with constitution quality bar [bar]"
- Resolution: Revise NFR or ask user to update constitution

## Reference

For framework patterns, detailed context, and examples:
aidev-workflow skill → execution-framework.md, commands-reference.md
