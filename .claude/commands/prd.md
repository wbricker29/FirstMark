---
name: prd
description: Create Product Requirements
---

# /prd - Create Product Requirements

Define the problem, audience, outcomes, scope, and success metrics for the project.

## Purpose

Define the problem, audience, outcomes, scope, and success metrics. Serves as the "what and why" contract between stakeholders and engineering.

## Prerequisites

- `spec/constitution.md` should exist (establishes governance)
- Project goals understood by stakeholder/user

## Execution Pattern

### Step 0: Review Workflow

**Before proceeding, invoke the aidev-workflow skill to review:**

- PRD structure and measurable outcome definitions
- Acceptance criteria patterns (Given-When-Then format)
- Scope definition and boundary-setting best practices

### Phase 1: Validate

1. Check if `spec/PRD.md` already exists
2. If exists, ask user: "PRD already exists. Overwrite (o), update (u), or cancel (c)?"
3. Load template from `.claude/skills/aidev-workflow/assets/templates/PRD-TEMPLATE.md`
4. Verify template exists and is valid markdown
5. Check that constitution exists (warn if missing, but continue)

### Phase 2: Gather

Ask user these questions (guide toward specificity and measurability):

1. **Prompt:** "What problem does this project solve? (2-3 sentences)"
   → Validate: Clear problem statement, includes audience

2. **Prompt:** "What are the primary outcomes? (1-3 measurable outcomes, not features)"
   → Validate: Measurable, specific results (e.g., "50% faster completion" not "build feature X")

3. **Prompt:** "Secondary/nice-to-have outcomes?"
   → Validate: Clearly labeled as secondary | Default: Can be empty

4. **Prompt:** "How will we measure success? (2-4 metrics with targets and measurement method)"
   → Validate: Each has name, target, measurement method; aligns with outcomes

5. **Prompt:** "What is IN scope? (features, capabilities, use cases)"
   → Validate: Specific, actionable, aligns with primary outcomes

6. **Prompt:** "What is OUT of scope? (set boundaries)"
   → Validate: Clear boundaries | Default: Suggest scope creep items

7. **Prompt:** "Define 3-5 acceptance criteria in Given-When-Then format."
   → Validate: All three components present, testable, specific

8. **Prompt:** "Key milestones and deliverables? (MVP, V1.0, etc.)"
   → Validate: Each has target date and deliverables | Default: MVP + V1.0 structure

9. **Prompt:** "Assumptions and risks?"
   → Validate: Risks have likelihood, impact, mitigation | Default: Can be minimal

### Phase 3: Generate

1. Populate template with gathered information
2. Format problem (audience + impact), outcomes (primary/secondary), metrics (measurement methods)
3. Create scope lists, acceptance criteria (Given-When-Then), roadmap (milestones)
4. Add assumptions and risks with mitigation
5. Write to `spec/PRD.md`

### Phase 4: Validate

Run these checks before confirming:

- ✅ File exists at `spec/PRD.md`
- ✅ Problem statement is clear and includes audience
- ✅ At least one primary outcome defined
- ✅ All metrics have targets and measurement methods
- ✅ In-scope and out-of-scope are both defined
- ✅ At least 3 acceptance criteria in Given-When-Then format
- ✅ At least one milestone with deliverables
- ✅ Risks include likelihood, impact, mitigation
- ✅ Valid markdown structure with proper headings

### Phase 5: Confirm

Display summary to user:

```
✅ PRD created: spec/PRD.md

Problem: [one-line summary]
Primary Outcomes: [count]
Success Metrics: [count]
In Scope: [count] items
Out of Scope: [count] items
Acceptance Criteria: [count]
Milestones: [count]

Next: Run /spec to create engineering specification
```

## Error Handling

**Missing template:**

- Error: "Template not found at .claude/skills/aidev-workflow/assets/templates/PRD-TEMPLATE.md"
- Resolution: Check file exists, suggest creating from reference

**Unmeasurable outcomes:**

- Error: "Outcome '[text]' is not measurable—reframe as a result with metrics"
- Resolution: Guide user to convert feature-focused language to outcome-focused

**Missing measurement method:**

- Error: "Metric '[name]' must specify how to measure (e.g., 'via logging', 'via analytics')"
- Resolution: Re-prompt for measurement method

**Invalid Given-When-Then:**

- Error: "Acceptance criterion missing [component]"
- Resolution: Show format example, re-prompt

## Reference

For framework patterns, detailed context, and examples:
aidev-workflow skill → execution-framework.md, commands-reference.md
