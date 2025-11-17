---
unit_id: "[###-slug]"
title: "[Descriptive title]"
version: "1.0"
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
status: "draft"
---

# Unit Design Template

Stable intent and acceptance criteria for a unit of work

## Objective

**Summary:** [1-2 sentences: what this unit accomplishes]

**Success Metrics:**
- [Measurable outcome 1]
- [Measurable outcome 2]

## Behavior

**Description:** [Detailed description of expected behavior]

### Inputs

#### [input_name]
- **Type:** [type]
- **Description:** [What this input represents]
- **Examples:**
  - [Example value 1]
  - [Example value 2]

### Outputs

#### [output_name]
- **Type:** [type]
- **Description:** [What this output represents]
- **Examples:**
  - [Example value 1]

### Edge Cases

- **Scenario:** [Description of edge case]
  - **Expected behavior:** [How system should respond]

- **Scenario:** [Another edge case]
  - **Expected behavior:** [Expected behavior]

## Interfaces Touched

- [interface_name from spec.md]
- [another_interface from spec.md]

## Data Shapes

- [EntityName from spec.md]
- [AnotherEntity from spec.md]

## Constraints

### Functional
- [Functional constraint or requirement]
- [Another constraint]

### Non-Functional
- [Performance constraint]
- [Security constraint]

## Acceptance Criteria

### AC-[UNIT]-01
- **Given:** [Initial state]
- **When:** [Action]
- **Then:** [Expected outcome]
- **Testable:** ✅

### AC-[UNIT]-02
- **Given:** [Context]
- **When:** [Action]
- **Then:** [Outcome]
- **Testable:** ✅

## Dependencies

**Blocks:** None

**Blocked by:** None

## Notes

[Optional additional context, decisions, or clarifications]
