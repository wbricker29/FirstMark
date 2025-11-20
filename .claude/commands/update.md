---
name: update
description: Change & Propagate Updates
---

# /update DOCUMENT PATH - Change & Propagate Updates

Make changes to L1 or L2 documents and automatically propagate updates to dependent documents.

## Purpose

Update documents and propagate changes to dependent documents to maintain system consistency.

## Prerequisites

- Target document must exist (constitution.md, PRD.md, spec.md, design.md, or plan.md)
- PATH must be valid path within document structure

## Execution Pattern

### Step 0: Review Workflow

**Before proceeding, invoke the aidev-workflow skill to review:**

- Document dependency chains and propagation rules
- Impact analysis methodology and severity assessment
- Change propagation patterns across architectural levels

### Phase 1: Validate

Before proceeding, verify:

- Parse DOCUMENT argument (which document to update)
- Parse PATH argument (which section/field to update)
- Verify target document exists
- Verify PATH is valid within document structure
- Load current document content

### Phase 2: Gather

Collect change information with these exact prompts:

**Show Current Value:**

- Navigate to PATH in document
- Display current value to user

**Prompt 1: "What should the new value be?"**
→ Validate: New value is different from current value, appropriate type/format

**Prompt 2: "What is the rationale for this change?"**
→ Validate: Rationale is clear and justifies the change

**Prompt 3: "Should this change propagate automatically to dependent documents, or would you like to review dependencies first?"**
→ Validate: User selects "automatic" or "review"

### Phase 3: Generate

Make primary change and analyze impact:

**Update Target Document:**

- Replace old value with new value at PATH
- Update `updated_at` timestamp in frontmatter
- Increment version if appropriate (major changes)
- Save document

**Identify Dependencies:**
Based on DOCUMENT type, determine what depends on this change:

- **constitution.md** → All units' plan.md (coverage_target, quality standards), spec.md (principles)
- **PRD.md** → spec.md (technical decisions), all units' design.md (outcomes alignment)
- **spec.md** → All units' design.md (interface/entity references), all units' plan.md (verification), code implementations
- **design.md** → Same unit's plan.md (tasks), dependent units (if this unit is a dependency)
- **plan.md** → Dependent units (less impact, volatile document)

**Analyze Impact:**
For each dependent document:

- Check if it references the changed value (exact match or semantic reference)
- Determine what needs updating (specific sections, values)
- Assess severity (critical, high, medium, low)
- Assess priority (immediate, soon, deferred)

**Generate Impact Report:**

- List primary change made
- List affected documents with change details
- Categorize by severity and priority
- Provide recommendations

### Phase 4: Validate

Ensure update completeness:

- ✅ Target document updated with new value
- ✅ Version incremented (if appropriate)
- ✅ Timestamp updated
- ✅ All dependencies identified
- ✅ Impact correctly assessed for each dependency
- ✅ Severity and priority assigned
- ✅ Propagation plan is sound
- ✅ User prompted before automatic changes

### Phase 5: Confirm

Display impact analysis and propagate changes:

**Impact Report:**

- **Primary Change**: Document, PATH, old value → new value, rationale
- **Affected Documents**: List each dependent document with required changes, severity, priority
- **Propagation Plan**: Which changes will be made automatically (if approved)
- **Deferred Updates**: Which changes flagged as blockers for later

**Execute Propagation (if approved):**

- Update approved dependencies
- Maintain consistency across documents
- Update timestamps for modified documents
- Add deferred updates to blockers in state.json

**Summary:**

- Changes made (count)
- Documents updated (list)
- Blockers added (list)
- Next steps (what user should review or do)

## Integration

- **Runs when changes needed**: Triggered by design changes, requirement evolution, or drift detected by `/check`
- **Propagates from /constitution**: Quality bar changes cascade to all plan.md verification sections
- **Propagates from /prd**: Requirement changes cascade to spec.md and design.md alignment
- **Propagates from /spec**: Interface changes cascade to all design.md and plan.md that reference them
- **Informs /check**: After propagation, `/check` should validate that all updates maintained consistency

## Error Handling

**Invalid DOCUMENT:**

- Solution: List valid documents, prompt for correct one

**Invalid PATH:**

- Solution: Display document structure, prompt for valid PATH

**New value same as old:**

- Solution: Confirm user wants to proceed or cancel

**Dependency update fails:**

- Solution: Add to blockers, warn user, continue with other dependencies

**Circular dependencies:**

- Solution: Warn user, require manual resolution

## Reference

For dependency chain details, propagation patterns, and examples:

```
aidev-workflow skill → execution-framework.md, commands-reference.md
```
