---
name: reflect
description: Capture Learnings
---

# /reflect - Capture Learnings

Capture important learnings, decisions, and insights from development work to improve future iterations.

## Purpose

Capture learnings, decisions, and insights to preserve project knowledge and improve future iterations.

## Prerequisites

- None (can be run at any time)

## Execution Pattern

### Step 0: Review Workflow

**Before proceeding, invoke the aidev-workflow skill to review:**

- Reflection capture methodology and categorization
- CLAUDE.md maintenance patterns and entry limits
- Learning-to-action pathways and document propagation

### Phase 1: Validate

Before proceeding:

- Confirm CLAUDE.md exists (should be in project root)
- Verify CLAUDE.md has "Reflection Patterns" section
- Check current reflection count (keep 5-10 most recent)

### Phase 2: Gather

Prompt user for reflection details with these exact questions:

**Prompt 1: "What would you like to reflect on?"**
→ Validate: User provides a topic or context

**Prompt 2: "What did you learn or observe?"**
→ Validate: Observation is specific and concrete (not vague)

**Prompt 3: "Why does this matter? What is the impact?"**
→ Validate: Impact is clear and measurable

**Prompt 4: "How should this be applied in the future?"**
→ Validate: Application is actionable

**Prompt 5: "Which category does this fall under: Technical, Process, Quality, Collaboration, Performance, or Other?"**
→ Validate: User selects one category

### Phase 3: Generate

Create reflection entry:

**Format:**

```markdown
- YYYY-MM-DD: [Context]: [Learning]. [Why it matters]. [Application].
```

**Check for Actionable Items:**

- If reflection suggests constitution changes, ask: "Should we update constitution.md?"
- If reflection suggests spec changes, ask: "Should we update spec.md?"
- If reflection suggests PRD changes, ask: "Should we update PRD.md?"

**Manage Reflection List Size:**

- If >10 reflections exist, remove oldest entries to maintain 5-10
- Keep most relevant and recent learnings

### Phase 4: Validate

Ensure reflection quality:

- ✅ Reflection added to CLAUDE.md "Reflection Patterns" section
- ✅ Proper date format (YYYY-MM-DD)
- ✅ Category tag applied (Technical/Process/Quality/Collaboration/Performance/Other)
- ✅ Content is clear and specific (not vague)
- ✅ Impact is articulated (why it matters)
- ✅ Application is actionable (what to do)
- ✅ List maintained at 5-10 entries

### Phase 5: Confirm

Display summary to user:

- **Reflection Added**: Show formatted reflection entry
- **Category**: Confirm category assignment
- **Documents Updated** (if applicable): List any constitution/spec/PRD updates made
- **Action Items** (if applicable): List any follow-up actions identified
- **Current Reflection Count**: Show how many reflections are now in CLAUDE.md

## Error Handling

**CLAUDE.md missing:**

- Solution: Create CLAUDE.md with "Reflection Patterns" section

**Reflection Patterns section missing:**

- Solution: Add "## Reflection Patterns" section to CLAUDE.md

**Vague reflection:**

- Solution: Re-prompt for specifics and concrete observations

**Category unclear:**

- Solution: Use "Other" category

## Reference

For reflection pattern examples, categorization guidance, and best practices:

```
aidev-workflow skill → execution-framework.md, commands-reference.md
```
