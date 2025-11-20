---
name: constitution
description: Create Project Governance
---

# /constitution - Create Project Governance

Establish non-negotiable principles, quality bars, and constraints that guide all development work.

## Purpose

Establish non-negotiable principles, quality bars, and constraints that guide all technical and product decisions.

## Prerequisites

None. This is typically the first command run in a new project.

## Execution Pattern

### Step 0: Review Workflow

**Before proceeding, invoke the aidev-workflow skill to review:**

- Constitutional governance principles and structure
- Quality bar definitions and enforcement patterns
- Template requirements and validation criteria

### Phase 1: Validate

1. Check if `spec/constitution.md` already exists
2. If exists, ask user: "Constitution already exists. Overwrite (o), merge (m), or cancel (c)?"
3. Load template from `.claude/skills/aidev-workflow/assets/templates/CONSTITUTION-TEMPLATE.md`
4. Verify template exists and is valid markdown

### Phase 2: Gather

Ask user these questions (provide smart defaults based on codebase detection):

1. **Prompt:** "3-5 core principles? (e.g., 'Simple > Perfect', 'Security by default')"
   → Validate: At least 3 principles with clear rules
   → Note: MUST include "Sufficiency over assumptions: Ask questions early vs fill gaps with guesses"

2. **Prompt:** "Quality bars? Coverage target (default 85%), typing (strict/loose), linting (enabled/disabled)"
   → Validate: Coverage 0-100%, valid choices | Default: Detect from configs

3. **Prompt:** "Performance targets? (e.g., 'API p95 < 200ms', 'Page load < 3s')"
   → Validate: Each has metric, threshold, measurement method | Default: Suggest from stack

4. **Prompt:** "Non-negotiable constraints? Runtime (versions), security, dependencies"
   → Validate: Each has clear requirement + enforcement | Default: Detect from package.json

5. **Prompt:** "Decision owners? Architecture, API contracts, infrastructure, testing"
   → Validate: Each area has clear owner/team | Default: Single dev → "Developer"

### Phase 3: Generate

1. Populate template with gathered information
2. Format principles (Rule + Rationale + Examples), quality bars (measurement methods)
3. Organize constraints by category, map decision rights to owners
4. Write to `spec/constitution.md`

### Phase 4: Validate

Run these checks before confirming:

- ✅ File exists at `spec/constitution.md`
- ✅ Contains mandatory "Sufficiency over assumptions" principle
- ✅ All principles have Rule, Rationale, and Examples
- ✅ Quality bars specify measurement methods
- ✅ Performance targets include how to verify
- ✅ All constraints are enforceable (not aspirational)
- ✅ Decision rights cover all key areas
- ✅ Valid markdown structure with proper headings

### Phase 5: Confirm

Display summary to user:

```
✅ Constitution created: spec/constitution.md

Principles: [count]
Quality Bars: Coverage [X]%, Typing [strict/loose], Linting [enabled/disabled]
Performance Targets: [count]
Constraints: [Runtime/Security/Dependencies summary]
Decision Rights: [count] areas defined

Next: Run /prd to define product requirements
```

## Integration

- **Runs first**: Before `/prd` and `/spec` to establish governance baseline
- **Informs /spec**: Architecture principles guide interface design and module structure
- **Enforces /work**: Quality bars become verification gates in `/work` and `/verify`
- **Blocks /update**: Constitution changes cascade to all dependent documents (plan.md verification sections update automatically)

## Error Handling

**Missing template:**

- Error: "Template not found at .claude/skills/aidev-workflow/assets/templates/CONSTITUTION-TEMPLATE.md"
- Resolution: Check file exists, suggest creating from reference

**Invalid user input:**

- Error: "Principle must include rule, rationale, and examples"
- Resolution: Re-prompt with example format

**Merge conflict:**

- Error: "Cannot auto-merge constitutions with different principle sets"
- Resolution: Ask user to manually reconcile, then re-run

## Reference

For framework patterns, detailed context, and examples:
aidev-workflow skill → execution-framework.md, commands-reference.md
