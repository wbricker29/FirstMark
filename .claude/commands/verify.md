---
name: verify
description: Run Verification Gates
---

# /verify SLUG - Run Verification Gates

<objective>
Run all verification gates for a unit to ensure quality standards are met before considering it complete.

Validate unit quality through automated gates:

- Code analysis to validate implementation
- Tests (correctness)
- Coverage target (test thoroughness)
- Acceptance criteria (functionality)
</objective>

## Prerequisites

- plan.md must exist for the specified unit
- At least some tasks should be complete
- Verification section must be defined in plan.md (commands, gates, coverage_target)

## Execution Pattern

### Step 0: Review Workflow

**Before proceeding, invoke the aidev-workflow skill to review:**

- Verification gate definitions and must_pass logic
- Coverage measurement and acceptance criteria validation
- Quality gate evaluation patterns and reporting standards

### Phase 1: Validate

Before proceeding, verify:

- Unit directory exists at `spec/units/###-SLUG/`
- plan.md exists for unit
- plan.md contains verification section with commands and gates
- At least one task has status "done"

### Phase 2: Gather

Load verification plan from plan.md:

- Read verification.commands (linting, type_checking, tests, coverage)
- Read verification.gates (gate definitions with must_pass flags)
- Read verification.coverage_target (from constitution)
- Read verification.acceptance_refs (design.md criteria IDs)
- Load design.md acceptance criteria for validation

### Phase 3: Generate

Execute verification commands and evaluate gates:

**Run Linting:**

- Execute linting command from plan.md (e.g., `pnpm lint`, `ruff check`)
- Capture exit code and output
- Determine pass/fail status

**Run Type Checking:**

- Execute type checking command from plan.md (e.g., `pnpm type-check`, `pyright`)
- Capture exit code and output
- Determine pass/fail status

**Run Tests:**

- Execute test command from plan.md (e.g., `pnpm test`, `pytest`)
- Capture exit code, output, and coverage metrics
- Determine pass/fail status

**Check Coverage:**

- Parse coverage percentage from test output
- Compare against coverage_target from constitution
- Determine pass/fail (pass if >= target)

**Evaluate Gates:**

- For each gate, determine if passed based on command results
- Check must_pass flag (critical if true, warning if false)
- Calculate overall pass/fail (all must_pass gates must pass)

**Check Acceptance Criteria:**

- Review each criterion from design.md
- Determine if satisfied based on implementation
- Flag any unmet criteria

Generate comprehensive report with gate results, coverage metrics, and acceptance status.

### Phase 4: Validate

Ensure verification completeness:

- ✅ All verification commands executed
- ✅ All gates evaluated with correct must_pass logic
- ✅ Coverage measured and compared to target
- ✅ Acceptance criteria reviewed
- ✅ Overall pass/fail status determined
- ✅ Clear feedback provided for failures
- ✅ Actionable next steps identified

### Phase 5: Confirm

Display verification report:

- **Command Results**: Each verification command (linting, type checking, tests) with pass/fail and output
- **Gate Evaluation**: Each gate result with must_pass status
- **Coverage**: Achieved percentage vs. target (✅ if met, ❌ if not)
- **Acceptance Criteria**: Status of each criterion from design.md
- **Overall Status**: ✅ PASS if all must_pass gates pass, ❌ FAIL otherwise
- **Blockers**: List of failures requiring attention
- **Next Steps**: If PASS, consider unit ready; if FAIL, fix issues and re-run

## Error Handling

**plan.md missing verification section:**

- Solution: Re-run /plan to regenerate with verification section

**Verification command fails:**

- Solution: Check command syntax, ensure tools installed

**Invalid SLUG:**

- Solution: List available units, prompt for valid SLUG

**No completed tasks:**

- Solution: Complete at least one task with /work before verifying

## Reference

For detailed gate evaluation logic, acceptance criteria validation, and examples:

```
aidev-workflow skill → execution-framework.md, commands-reference.md
```
