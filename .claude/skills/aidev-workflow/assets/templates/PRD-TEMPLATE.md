---
version: "1.0"
last_updated: "YYYY-MM-DD"
status: "draft"
---

# Product Requirements Document Template

## Problem

**Statement:** [2-3 sentences describing the problem this project solves]

**Audience:** [Who experiences this problem]

**Impact:** [Why solving this matters]

## Outcomes

### Primary
- [Measurable primary outcome]
- [Another primary outcome]

### Secondary
- [Secondary outcome]

## Success Metrics

- **[Metric name]:** [Target value] (measured via [How to measure])
- **[Another metric]:** [Target value] (measured via [How to measure])

## Scope

### In Scope
- [Feature or capability that IS included]
- [Another in-scope item]

### Out of Scope
- [Feature or capability that is NOT included]
- [Another out-of-scope item]

## Acceptance Criteria

### AC-PRD-01
- **Given:** [Initial state or context]
- **When:** [Action or trigger]
- **Then:** [Expected outcome]

### AC-PRD-02
- **Given:** [Context]
- **When:** [Action]
- **Then:** [Outcome]

## Roadmap

### Milestone: MVP
- **Target date:** YYYY-MM-DD
- **Deliverables:**
  - [Deliverable 1]
  - [Deliverable 2]

### Milestone: V1.0
- **Target date:** YYYY-MM-DD
- **Deliverables:**
  - [Deliverable 1]

## Assumptions

- [Assumption about users, technology, or constraints]
- [Another assumption]

## Risks

### [Risk Description]
- **Likelihood:** high | medium | low
- **Impact:** high | medium | low
- **Mitigation:** [How to address this risk]

<!--
============================================================
Optional Expanded PRD Sections
These sections are allowed for orientation only. Keep them
link-first and derive any numbers from automation (state.json,
`/status`, `/check`). Do NOT duplicate task lists from plan.md.
Uncomment and fill as needed.
============================================================
-->

<!--
## Current Project State (Optional)

Phase: [e.g., Phase 4 — Production Readiness]

Status: See `.claude/logs/state.json` for auto-generated progress. Use `/status` and `/check` for live metrics.

Notes:
- [One or two bullets about current focus]
- [Link to any relevant reports]
-->

<!--
## Critical Path (Optional)

- [Blocking Item 1] — link to `specs/units/###-slug/plan.md` and evidence report
- [Blocking Item 2] — link to `specs/units/###-slug/plan.md` and evidence report
-->

<!--
## Feature Inventory (Optional)

As of YYYY-MM-DD (derived from `.claude/logs/state.json`)

| ID  | Feature Name | Status/Progress | Blocks Deployment? | Documentation |
|-----|--------------|------------------|--------------------|---------------|
| 012 | Example      | 47% (state.json) | ✅ Yes             | specs/units/012-example/ |
-->

<!--
## Document Hierarchy (Optional)

L0 (Governance):
- `specs/constitution.md`

L1 (Project-Level):
- `specs/PRD.md` (this doc)
- `specs/spec.md`

L2 (Feature-Level):
- `specs/units/###-slug/design.md`
- `specs/units/###-slug/plan.md`

Workflow:
1. /constitution → /prd → /spec
2. /new SLUG → /plan SLUG
3. /work SLUG TK-## → /verify SLUG → /check → /reflect
-->
