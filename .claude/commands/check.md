---
name: check
description: Validate Alignment & Drift
---

<objective>
Validate document alignment, detect implementation drift, and check constitution compliance at different architectural levels. The architecture levels (determined by user_input) are:
- **L1**: Project-level documents (constitution, PRD, spec) vs code
- **L2**: Unit-level documents (design, plan) vs code
- **CROSS**: Cross-level alignment (L2 references valid in L1 documents)
</objective>

<user_input> $ARGUMENTS </user_input>

## Prerequisites

- **L1 Mode**: constitution.md, PRD.md, spec.md should exist
- **L2 Mode**: Unit directory at `spec/units/###-SLUG/` with design.md and/or plan.md
- **CROSS Mode**: Both L1 and L2 documents should exist
- State tracker hook should be functional (`.claude/hooks/state-tracker.py`)

### Step 0: Review Workflow

**MANDATORY: Invoke the `aidev-workflow` skill now before proceeding further.**

Use the Skill tool to load the aidev-workflow skill and review:

- Validation patterns and drift detection methodology
- Alignment check requirements across architectural levels
- Report generation standards and severity categorization

This is not optional. The skill provides critical context for validation checks.

### Phase 1: Validate

Before proceeding, determine MODE based on user_input:

**L1 Mode:**

- State tracker exists at `.claude/hooks/state-tracker.py`
- L1 documents exist: `spec/constitution.md`, `spec/PRD.md`, `spec/spec.md`

**L2 Mode:**

- SLUG argument provided
- Unit directory exists at `spec/units/###-SLUG/`
- design.md and/or plan.md exist for unit

**CROSS Mode:**

- State tracker exists
- L1 documents exist (constitution, PRD, spec)
- At least one unit exists with design.md or plan.md
- If SLUG provided: validate unit exists

### Phase 2: Gather

Run state tracker to collect current system state:

- Execute: `python .claude/hooks/state-tracker.py`
- Load generated state.json
- Determine scope based on MODE
- review aidev-workflow skill for relevant information

### Phase 3: Generate

Perform mode-specific alignment and drift checks:

#### L1 Mode: Project-Level Validation

**Document Status & Alignment:**

- Check constitution.md exists, valid YAML frontmatter, contains required sections
- Check PRD.md exists, valid structure, measurable metrics defined
- Check spec.md exists, complete interface contracts, valid data models
- Ensure spec.md, prd.md and constitution.md are aligned

**Implementation Drift Detection:**

- Compare spec.md interface contracts with actual code signatures
  - Identify modules in code not documented in spec.md
  - Identify modules in spec.md not implemented in code
  - Check for signature mismatches (parameters, return types, type annotations)
- Compare prd.md with implemented project features to ensure they align

#### L2 Mode: Unit-Level Validation

**Unit Document Status & Alignment:**

- Check design.md exists and has a valid structure
- Check plan.md exists and has a valid task breakdown
- Verify plan.md and design.md are aligned

**Unit Implementation Drift:**

- Compare design.md interface contracts with unit code
- Check plan.md tasks vs actual implementation status
- Identify completed tasks not marked done
- Identify planned features not implemented
- Identify implemented features not planned

#### CROSS Mode: Cross-Level Alignment

Use subagents to perform L1 and L2 mode. When they are done:
**Reference Validation:**

- Verify all design.md interface references exist in spec.md
- Verify all design.md entity/model references exist in spec.md
- Check all plan.md references to PRD metrics are valid
- Verify all design.md features align with prd.md
- Validate design goals and feature implementation align with PRD objectives

**Scope Validation:**

- Ensure unit scope doesn't exceed spec boundaries
- Check for feature duplication and deviation
- Validate unit dependencies reference valid spec interfaces

**Consistency Checks:**

- Verify terminology consistency between L1 and L2 documents
- Check version compatibility between referenced specs
- Ensure no unnecessary redundency
- Validate timestamp coherence (design.md not older than referenced spec changes)

Generate comprehensive report with findings categorized by severity (✅ pass, ⚠️ warning, ❌ critical).

### Phase 4: Validate

Ensure report completeness based on MODE:

**L1 Mode:**

- ✅ All L1 documents checked (constitution, PRD, spec)
- ✅ Drift detection performed
- ✅ Issues prioritized by severity

**L2 Mode:**

- ✅ Unit directory and documents validated
- ✅ Unit-specific drift detection completed
- ✅ Task status verified

**CROSS Mode:**

- ✅ L1 & L2 Complete
- ✅ Reference validation completed
- ✅ Scope validation performed
- ✅ Consistency checks completed
- ✅ All invalid references identified

### Phase 5: Confirm

Generate a report with

- Concise summary of findings
- Clear walkthrough of issues identified
- Recommended remediation or next steps

## Integration

- **Runs after implementation**: Validates alignment after code changes, before considering work complete
- **Consumes /constitution**: Uses quality bars and principles to validate compliance
- **Validates /spec**: Detects drift between spec.md contracts and actual code implementations
- **Informs /update**: Identifies inconsistencies that require document updates or code fixes
- **Tracks /work progress**: Reads plan.md task status via state-tracker.py to generate progress metrics

## Reference

For detailed validation criteria, drift detection patterns, and examples:

```
aidev-workflow skill → execution-framework.md, commands-reference.md
```
