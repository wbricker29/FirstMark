# v1 Minimal Alignment Conflicts

This note captures the gaps between the current demo-planning/spec artifacts and the approved **v1 minimal** scope defined in `spec/v1_minimal_spec.md` and clarified in `spec/v1_minimal_spec_agno_addendum.md` (single `/screen` workflow, Airtable-only storage across People/Portco/Role/Spec/Screens/Assessments, optional single incremental search step, Agno `SqliteDb` for session state).

## Summary

- Several demo-planning docs (and the legacy `spec/spec.md` + `spec/prd.md`) still describe the older 9-table Airtable design with dedicated `Workflows` + `Research_Results` tables and a parser-based research pipeline.
- Workflow specs continue to document fast mode, multi-iteration supplemental search loops, and Condition/Loop constructs that v1 explicitly defers.
- Logging/audit guidance conflicts with the addendum decision to rely on Airtable fields + stdout + Agno `SqliteDb` (no custom WorkflowEvent tables).
- These inconsistencies will confuse implementers unless we either update or clearly mark the docs as Phase 2.

## Detailed Conflicts

### 1. Airtable Schema Scope

- `demo_planning/airtable_schema.md:293-356` and `airtable_ai_spec.md:293-365` still define **Workflows** and **Research_Results** tables (execution logs + structured research) plus JSON schemas that assume a parser step. The current spec only allows People / Portco / Portco_Roles / Role_Specs / Screens / Assessments.
- `spec/spec.md:954-969` and `spec/prd.md:122-184` repeat the “9 tables” language (including Workflows + Research_Results) even though `spec/v1_minimal_spec.md:24-75` and the Agno addendum require storing raw + structured research/assessment outputs on the **Assessments** records.

**Action:** Remove or clearly mark Workflows/Research_Results as Phase 2, and update all schema docs/checklists to describe the new Assessment fields (`research_structured_json`, `research_markdown_raw`, `assessment_json`, `assessment_markdown_report`).

### 2. Workflow Architecture & Execution Modes

- `demo_planning/screening_workflow_spec.md` still documents fast mode, a quality gate with a **Loop** (up to 3 supplemental search iterations), and Condition nodes (see lines 50-430 and code around lines 558-837). `spec/v1_minimal_spec.md:24-55` + §3.3-3.4 limit v1 to a **linear** workflow: Deep Research → lightweight quality heuristic → optional single incremental search (max two web calls) → Assessment → Airtable writeback.

**Action:** Rewrite the workflow spec to remove fast mode, loops, and Condition/Loop code so it mirrors the simplified path and emphasizes the single optional incremental search step.

### 3. Research Pipeline Expectations

- `demo_planning/data_design.md:212-238,508-517` and `deep_research_findings.md:300-361` still describe a two-step “Deep Research markdown → parser agent → Research_Results table” process plus Workflows linking. `spec/v1_minimal_spec.md:337-386` states that both research and assessment agents should emit structured outputs directly (no parser layer), while the Agno addendum routes raw markdown + structured JSON into the Assessments table.

**Action:** Update data design + deep research docs to describe the direct structured-output path, optional incremental search, and the new Assessment storage fields instead of referencing a parser + Research_Results table.

### 4. Logging / Audit Trail Guidance

- `airtable_schema.md:293-320`, `data_design.md:178-238`, and `alignment_issues_and_fixes.md:362-391` instruct readers to capture execution logs in the Workflows table (execution_log JSON, event streaming) and to treat Research_Results vs Workflows as the canonical split. The Agno addendum (§2.1–§3.3) set the v1 policy: **no custom WorkflowEvent tables**, rely on Airtable status/fields plus stdout + `tmp/agno_sessions.db` (Agno `SqliteDb`) for inspection.

**Action:** Replace the Workflows-table guidance with the Agno `SqliteDb` approach and explicitly note that custom workflow audit tables are Phase 2.

### 5. Legacy References in spec/spec.md and spec/prd.md

- Both documents still point to the older artifacts (`demo_planning/airtable_schema.md`, `screening_workflow_spec.md`) without the v1 caveats, reinforcing the outdated scope (e.g., `spec/spec.md:954-969` and `spec/prd.md:122-184`).

**Action:** Update those sections to summarize the v1-minimal constraints (5-table Airtable footprint, linear workflow, Assessment storage for raw/structured data) and link to the refreshed docs once the above fixes land.

## Next Steps

1. Update Airtable schema docs + spec/prd to reflect the v1 table set and Assessment storage fields.
2. Rewrite screening workflow doc to show the linear path (no loops/fast mode) and reference Agno `SqliteDb` logging.
3. Refresh data design + deep_research docs to remove parser/Research_Results assumptions and highlight the new storage plan.
4. Mark Workflows/Research_Results guidance as Phase 2 in any remaining documents until the edits are complete.
