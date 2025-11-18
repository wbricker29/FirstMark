# Phase 2 Alignment Preparation

**Document Purpose:** Record spec/spec.md review findings and prepare remediation plan for Phase 2
**Review Date:** 2025-01-17
**Reviewer:** Claude Code Analysis
**Status:** Draft - Awaiting Implementation

---

## Executive Summary

The spec/spec.md and spec/prd.md files are comprehensive and well-structured but contain **8 categories of issues** requiring remediation before Phase 2:

- **Critical**: 3 issues (dates, success criteria, status values)
- **Important**: 2 issues (messaging consistency, hour estimates)
- **Optimization**: 3 opportunities (document length, minor cleanup, PRD clarity enhancements)

**High ROI Quick Wins (10 minutes):**
- Issue #8a: Table helper identification (PRD)
- Issue #8b: Scenario-to-role-spec mapping (PRD)

**Recommended Action:** Address critical issues immediately, implement high ROI quick wins, defer larger optimizations to Phase 2 planning.

---

## Issue Categories

### 🔴 CRITICAL: Must Fix Before Phase 2

#### Issue #1: Date Inconsistencies

**Severity:** Critical
**Impact:** Documentation credibility, timestamp accuracy
**status:** Complete ✅


---

#### Issue #2: Premature Success Criteria

**Severity:** Critical
**Impact:** Misrepresents project completion status
**status:** Complete ✅
---

#### Issue #3: Status Value Inconsistencies

**Severity:** Critical
**Impact:** Runtime errors, Airtable schema misalignment
**Status:** ✅ COMPLETE (Verified 2025-01-17)

**Original Problem:**
Three different status schemas were in use:
1. **Code implementation**: "Partial"
2. **Current Airtable**: "Error"
3. **Spec definition**: "Failed"

**Remediation Applied:**

✅ **Standardized on Spec-Defined Values (Option A)**
```python
# Standardized status values for v1.0-minimal
SCREEN_STATUS = ["Draft", "Processing", "Complete", "Failed"]
ASSESSMENT_STATUS = ["Pending", "Processing", "Complete", "Failed"]
```

**Verification Results:**
- ✅ Line 881 (spec.md): Code example uses "Failed" (not "Partial")
- ✅ Lines 1388-1389 (spec.md): Correctly documents canonical schema with demo subset notes
- ✅ airtable_ai_spec.md: Matches spec.md status definitions
- ✅ Implementation: Uses subset of canonical values ("Processing", "Complete") - acceptable for v1 demo
- ✅ No "Error" or "Partial" status values exist in current codebase

**Action Items:**
- [x] Decide on canonical status value set (Option A chosen)
- [x] Update line 864 code example to use chosen values (now line 881, already updated)
- [x] Update line 1322 Airtable schema notes (not applicable - different content at that line)
- [x] Update line 1371 single-select options (now lines 1388-1389, correctly documented)
- [x] Add status migration guide if Option A chosen (not needed - no migration required)
- [x] Verify demo/app.py uses consistent status values (verified - uses subset of canonical values)

---

### 🟡 IMPORTANT: Should Fix Before Phase 2

#### Issue #4: Contradictory Audit Trail Messaging

**Severity:** Important
**Impact:** Unclear observability strategy, messaging confusion

**Locations:**
- Line 102: "**Minimal Audit Trail:** Airtable fields + terminal logs (no separate event DB for v1)"
- Line 1010: "**Primary:** Agno UI Dashboard - Real-time workflow monitoring, session inspection, reasoning traces"

**Problem:**
"Minimal" contradicts comprehensive Agno UI capabilities. Both statements are technically true but messaging is confusing.

**Proposed Remediation:**

**Option A: Emphasize Agno-Managed vs Custom**
```markdown
# Line 102 (Key Design Principles section)
- **Agno-Managed Observability:** Agno UI dashboard for workflow monitoring; no custom event DB for v1
- **Quality-Gated Research:** Optional single incremental search agent step when initial research has quality issues
- **Minimal Custom Infrastructure:** Airtable fields + terminal logs (Agno handles session state)
- **Deep Research Primary:** v1 uses o4-mini-deep-research as default; fast mode is Phase 2+
```


**Recommendation:** Option A - Emphasizes that Agno provides rich tooling without custom infrastructure.

**Action Items:**
- [ ] Rewrite line 102 bullet using Option A wording
- [ ] Add clarification to line 1010 audit trail section
- [ ] Ensure consistent messaging in README.md
- [ ] Update observability section (lines 965-1022) for consistency

---

#### Issue #5: Hour Estimate Mismatch

**Severity:** Important
**Impact:** Project planning accuracy, stakeholder expectations

**Locations:**
- CLAUDE.md: "Estimated: 34-38 hours implementation"
- Line 1644: "Total: 22 hours per developer (adjusted for AgentOS prototype)"

**Problem:**
Two different estimates:
- Single developer: 34-38 hours
- Two developers (parallel): 22 hours each = 44 hours total

**Analysis:**
```
Single Developer Path (Sequential):
Stage 1: 2h
Stage 2: 6h
Stage 3: 4h
Stage 4: 4h
Stage 4.5: 2h
Stage 5: 2h
Stage 6: 3h
Total: 23h (core) + buffer = 34-38h ✓

Two Developer Path (Parallel):
Per developer: 22h
Total effort: 44h
Wall time: ~22h (with good parallelization)
```

**Proposed Remediation:**

Update both documents to clarify:

```markdown
# CLAUDE.md - Line with hour estimate
**Estimated Implementation Time:**
- Single Developer (Sequential): 34-38 hours over 4-5 days
- Two Developers (Parallel): 22 hours per developer, ~44 hours total effort, 2.5 days wall time

# spec/spec.md - Line 1644
**Timeline Analysis:**
- **Single Developer**: 34-38 hours sequential (Stages 1-6 with buffer)
- **Two Developers**: 22 hours per developer (44 hours total effort, ~22 hours wall time with parallelization)
- **Completed**: 17 hours per developer (Stages 1-4.5)
- **Remaining**: 5 hours per developer (Stages 5-6)
```

**Action Items:**
- [ ] Update CLAUDE.md with clarified estimates
- [ ] Update spec/spec.md line 1644 with both paths
- [ ] Add note explaining total effort vs wall time difference
- [ ] Reconcile with actual time tracking data

---

### 🟢 OPTIMIZATION: Consider for Phase 2

#### Issue #6: Document Length & Modularity

**Severity:** Optimization
**Impact:** Maintainability, discoverability, cognitive load

**Analysis:**
- **Current**: 1,718 lines in single file
- **Sections for potential extraction**:
  - Lines 1054-1268 (215 lines): Agno Framework Implementation Guidance
  - Lines 1380-1678 (298 lines): Implementation Roadmap
  - Lines 823-879 (56 lines): Full code examples

**Proposed Remediation:**

**Phase 2 Document Restructuring:**

```
spec/
├── spec.md (REDUCED to ~1,200 lines)
│   ├── Architecture & interfaces
│   ├── Data models (reference only)
│   ├── API specification (simplified)
│   └── Configuration
│
├── dev_reference/
│   ├── AGNO_PATTERNS.md (NEW - 250 lines)
│   │   ├── Structured outputs pattern
│   │   ├── Workflow orchestration
│   │   ├── Session state management
│   │   ├── ReasoningTools usage
│   │   └── Prompt template loading
│   │
│   └── (existing files remain)
│
└── planning/
    └── roadmap.md (NEW - 350 lines)
        ├── Single developer track
        ├── Two developer parallel track
        ├── Stage breakdowns
        └── Timeline analysis
```

**Benefits:**
- Easier navigation (sections < 1,000 lines)
- Clear separation of concerns (specification vs patterns vs planning)
- Better discoverability (dedicated pattern reference)
- Reduced cognitive load (focused documents)

**Action Items (Phase 2):**
- [ ] Extract Agno patterns to `spec/dev_reference/AGNO_PATTERNS.md`
- [ ] Extract roadmap to `spec/planning/roadmap.md`
- [ ] Replace code examples with pseudocode + file references
- [ ] Update cross-references in spec.md
- [ ] Validate all links after restructuring

---

#### Issue #7: Minor Inconsistencies & Cleanup

**Severity:** Optimization
**Impact:** Polish, professional presentation

**Findings:**

1. **Duplicate JSON Fields (Lines 1349-1357)**
   - Problem: Assessments table has both singleLineText "(text)" and multilineText versions
   - Remediation: Remove singleLineText duplicates, use only multilineText
   - Timeline: Phase 2 Airtable cleanup

2. **JSON Field Count Discrepancy (Line 254)**
   - States: "4 JSON fields in Assessments table"
   - Actual: 7+ fields (research_structured_json, assessment_json, dimension_scores_json, etc.)
   - Remediation: Update to "7 primary JSON fields" or list explicitly
   - Timeline: Quick fix in Phase 2

3. **Test File Naming (Line 673)**
   - Spec mentions: `test_workflow_smoke.py` (optional)
   - Actual: `test_workflow.py` (9 tests, complete)
   - Remediation: Update reference to match actual implementation
   - Timeline: Quick fix in Phase 2

4. **Demo-Scoped Options Documentation (Lines 1362-1375)**
   - Current: Buried in Airtable schema notes
   - Improvement: Move to separate "Demo Scope Limitations" section
   - Timeline: Phase 2 documentation reorganization

**Action Items (Phase 2):**
- [ ] Clean up duplicate Airtable JSON fields
- [ ] Update JSON field count reference (line 254)
- [ ] Fix test file naming (line 673)
- [ ] Create "Demo Scope Limitations" section consolidating reduced option sets

---

#### Issue #8: PRD Clarity Enhancements (HIGH ROI)

**Severity:** Optimization
**Impact:** Demo clarity, stakeholder understanding
**Source:** PRD review (spec/prd.md)

**Findings:**

1. **Table Helper Identification Ambiguity (PRD Line 159)**
   - Problem: States "7 tables (v1: 6 core + 1 helper)" but doesn't identify which is the helper
   - Tables: People, Portco, Portco_Roles, Searches, Screens, Assessments, Role_Specs
   - Likely helper: Role_Specs (template storage, not workflow data)
   - Impact: Confusion about data architecture
   - Effort: 1 minute fix

2. **Missing Scenario-to-Role-Spec Mapping (PRD)**
   - Problem: PRD mentions 4 scenarios and CFO/CTO templates but doesn't map them
   - Scenarios: Pigment CFO, Mockingbird CFO, Synthesia CTO, Estuary CTO
   - Impact: Unclear which template applies to which demo scenario
   - Effort: 5 minutes to add table

3. **PRD Length & Redundancy (849 Lines)**
   - Technical stack mentioned 3+ times (lines 163-173, 446-464)
   - Python-Specific Considerations overlaps with Technical Constraints
   - Could consolidate to reduce by 15-20% (~120-170 lines)
   - Impact: Medium - improves scanability, but comprehensive detail demonstrates product thinking
   - Note: Already covered by Issue #6 document restructuring approach

**Proposed Remediation:**

**Fix #8a: Table Helper Clarification**
```markdown
# PRD Line 159 (Scope Section)
- Current: "7 tables (v1: 6 core + 1 helper - People, Portco, Portco_Roles, Searches, Screens, Assessments, Role_Specs"
+ Improved: "7 tables (6 core workflow + Role_Specs helper for template storage)"

# Add explicit breakdown:
**Core Workflow Tables (6):**
- People: Executive network data
- Portco: Portfolio companies
- Portco_Roles: Open leadership positions
- Searches: Talent search requests
- Screens: Candidate screening batches
- Assessments: Individual candidate evaluations

**Helper Tables (1):**
- Role_Specs: Reusable evaluation templates (CFO, CTO)
```

**Fix #8b: Add Scenario-to-Spec Mapping Table**
```markdown
# PRD - Add to "Scope" section after line 158

**Demo Scenarios:**

| Scenario | Portfolio Company | Role Type | Role Spec Template | Pre-run Status |
|----------|------------------|-----------|-------------------|----------------|
| 1 | Pigment | CFO | CFO_Standard_v1 | Pre-run before demo |
| 2 | Mockingbird | CFO | CFO_Standard_v1 | Pre-run before demo |
| 3 | Synthesia | CTO | CTO_Standard_v1 | Pre-run before demo |
| 4 | Estuary | CTO | CTO_Standard_v1 | Live demo execution |

**Notes:**
- Scenarios 1-3 demonstrate results quality
- Scenario 4 demonstrates real-time workflow execution
- Each scenario processes 3-5 candidates from guildmember_scrape.csv
```

**Fix #8c: Optional PRD Consolidation (Defer to Issue #6 Approach)**
```markdown
# Consider for Phase 2 (Low priority - detail level is appropriate for case study)

Potential consolidations:
- Merge "Python-Specific Considerations" → "Technical Constraints"
- Move detailed timeline (lines 563-666) → spec/planning/roadmap.md
- Deduplicate technical stack references

Note: PRD comprehensiveness demonstrates product thinking depth for case study.
Defer consolidation to Phase 2 document restructuring (Issue #6).
```

**ROI Analysis:**

| Fix | Effort | Impact | ROI Score | Priority |
|-----|--------|--------|-----------|----------|
| #8a Table Helper ID | 1 min | Medium (clarity) | ⭐⭐⭐ High | P1 Quick Win |
| #8b Scenario Mapping | 5 min | High (demo prep) | ⭐⭐⭐ High | P1 Quick Win |
| #8c PRD Consolidation | 2 hours | Low (already detailed) | ⭐ Low | P3 Defer |

**Action Items (Immediate - 10 Minutes):**
- [ ] Update PRD line 159 with explicit table helper identification
- [ ] Add scenario-to-role-spec mapping table to PRD Scope section
- [ ] Add table breakdown (6 core + 1 helper) with purpose descriptions
- [ ] Verify mapping matches actual Airtable configuration

**Action Items (Phase 2 - Optional):**
- [ ] Consider PRD consolidation as part of Issue #6 document restructuring
- [ ] Evaluate whether detail level should be reduced or maintained for case study context

---

## Remediation Priority Matrix

| Issue | Severity | Effort | Priority | Timeline |
|-------|----------|--------|----------|----------|
| #1 Date Inconsistencies | 🔴 Critical | Low | P0 | Pre-Stage 5 |
| #2 Success Criteria | 🔴 Critical | Low | P0 | Pre-Stage 5 |
| #3 Status Values | 🔴 Critical | Medium | P0 | Pre-Stage 5 |
| #4 Audit Trail Messaging | 🟡 Important | Low | P1 | Pre-Stage 5 |
| #5 Hour Estimates | 🟡 Important | Low | P1 | Phase 2 Planning |
| #6 Document Length | 🟢 Optimization | High | P2 | Phase 2 Refactor |
| #7 Minor Inconsistencies | 🟢 Optimization | Low | P3 | Phase 2 Polish |
| **#8a-b PRD Quick Wins** | **🟢 Optimization** | **Very Low (10 min)** | **P1 ⭐** | **Pre-Stage 5 (High ROI)** |
| #8c PRD Consolidation | 🟢 Optimization | Medium | P3 | Phase 2 Refactor |

---

## Recommended Remediation Sequence

### Immediate (Pre-Stage 5) - 1 Hour 10 Minutes

**Goal:** Fix critical issues blocking accurate status representation + High ROI quick wins

```bash
# Step 1: Fix dates (5 minutes)
- Line 4: 2025-11-17 → 2025-01-17
- Line 1715: 2025-11-17 → 2025-01-17

# Step 2: Fix success criteria (15 minutes)
- Reorganize into Completed vs Pending sections
- Move Demo Ready to pending

# Step 3: Standardize status values (30 minutes)
- Choose canonical status schema (recommend spec-defined)
- Update code examples
- Update Airtable schema notes
- Create migration guide if needed

# Step 4: Fix audit trail messaging (10 minutes)
- Rewrite line 102 using "Agno-Managed Observability"
- Update observability section for consistency

# Step 5: PRD Quick Wins ⭐ HIGH ROI (10 minutes)
- Update PRD line 159 with table helper identification
- Add scenario-to-role-spec mapping table to PRD Scope section
- Add table breakdown (6 core + 1 helper) with purpose descriptions
- Verify mapping matches actual Airtable configuration
```

### Phase 2 Planning - 30 Minutes

**Goal:** Align documentation with actual implementation

```bash
# Step 5: Reconcile hour estimates
- Update CLAUDE.md with clarified paths
- Update spec.md with both single/parallel timelines
- Add actual time tracking data

# Step 6: Minor consistency fixes
- Update JSON field count
- Fix test file naming
- Document demo scope limitations
```

### Phase 2 Refactor - 4 Hours

**Goal:** Optimize document structure for long-term maintainability

```bash
# Step 7: Extract Agno patterns (2 hours)
- Create AGNO_PATTERNS.md
- Move framework guidance from spec.md
- Update cross-references

# Step 8: Extract roadmap (1 hour)
- Create planning/roadmap.md
- Move implementation timeline from spec.md
- Update project structure references

# Step 9: Simplify code examples (30 minutes)
- Replace full implementations with pseudocode
- Add references to actual implementation files

# Step 10: Validation (30 minutes)
- Verify all cross-references
- Check document lengths
- Test navigation flow
```

---

## Alignment Validation Checklist

After remediation, verify alignment with:

### ✅ Cross-Document Consistency
- [ ] spec.md aligns with v1_minimal_spec.md (scope, exclusions)
- [ ] spec.md aligns with prd.md (requirements, acceptance criteria)
- [ ] spec.md aligns with implementation_guide.md (data models, interfaces)
- [ ] spec.md aligns with airtable_ai_spec.md (schema, field types)
- [ ] spec.md aligns with AGNO_REFERENCE.md (framework patterns)
- [ ] prd.md table definitions match airtable_ai_spec.md (7 tables, helper identified)
- [ ] prd.md scenarios map to correct role specs (CFO/CTO templates)

### ✅ Internal Consistency
- [ ] All status values use same schema throughout
- [ ] All dates are accurate (no future dates)
- [ ] Success criteria reflect actual implementation status
- [ ] Hour estimates reconciled across documents
- [ ] Observability messaging consistent (Agno-managed vs custom)

### ✅ Implementation Alignment
- [ ] Code examples match actual demo/ implementations
- [ ] Test file references match actual test/ files
- [ ] Airtable schema matches actual base configuration
- [ ] Agent patterns match actual agents.py implementation
- [ ] Workflow steps match actual screening_service.py

---

## Phase 2 Enhancement Opportunities

Beyond fixing issues, consider these enhancements:

### 1. Add Explicit Traceability Matrix
```markdown
## Requirements Traceability

| PRD Requirement | Spec Section | Implementation File | Test File | Status |
|----------------|--------------|---------------------|-----------|--------|
| AC-PRD-01 | Lines 258-327 | demo/agents.py:45 | test_research_agent.py:12 | ✅ |
| AC-PRD-02 | Lines 344-376 | demo/agents.py:89 | test_scoring.py:24 | ✅ |
| ... | ... | ... | ... | ... |
```

### 2. Add Version Control Section
```markdown
## Specification Versioning

- v0.1-draft: Initial case study scope (2025-01-14)
- v1.0-minimal: Scoped to Module 4 only (2025-01-16)
- v1.1-implementation: Added Agno UI, prompts catalog (2025-01-17)
- v1.2-agentos: Added AgentOS prototype (2025-01-17)
```

### 3. Add Glossary Section
```markdown
## Glossary

- **Deep Research**: OpenAI's o4-mini-deep-research model for comprehensive candidate research
- **Evidence-Aware Scoring**: Using None/null for Unknown dimensions (not 0 or NaN)
- **Quality Gate**: Threshold-based trigger for optional incremental search
- **Session State**: Agno-managed workflow context persisted in SqliteDb
```

---

## Document Control

**Created:** 2025-01-17
**Purpose:** Track spec.md alignment issues and remediation plan
**Owner:** Development Team
**Review Cycle:** Before each major phase
**Next Review:** Post-Stage 5 (Integration Testing Complete)

**Related Documents:**
- spec/spec.md (subject of this review)
- spec/v1_minimal_spec.md (scope authority)
- spec/prd.md (requirements authority)
- spec/constitution.md (governance authority)

**Status:** Draft - Awaiting team review and prioritization

---

## Appendix: Detailed Line-by-Line Fixes

### Fix #1: Date Corrections

```diff
# Line 4
- updated: "2025-11-17T20:30:00-05:00"
+ updated: "2025-01-17T20:30:00-05:00"

# Line 1715
- Updated: 2025-11-17 (Added Agno UI dashboard, centralized prompt templates, and AgentOS prototype to v1.0-minimal scope)
+ Updated: 2025-01-17 (Added Agno UI dashboard, centralized prompt templates, and AgentOS prototype to v1.0-minimal scope)
```

### Fix #2: Success Criteria Reorganization

```diff
# Lines 1682-1694
## Success Criteria

This specification succeeds if:

+### ✅ Completed (Stages 1-4.5)
1. ✅ **Working Prototype:** Demonstrates end-to-end candidate screening
2. ✅ **Evidence-Aware Scoring:** Handles Unknown dimensions with None/null (not 0 or NaN)
3. ✅ **Quality-Gated Research:** Optional incremental search triggered when quality is low
4. ✅ **Minimal Implementation:** 5-file structure + prompt templates, simple algorithms, basic logging
5. ✅ **Type Safety:** Type hints on public functions (mypy as goal, not gate)
6. ✅ **Basic Tests:** Core logic tested (scoring, quality check) - 118 tests passing, 82% coverage
-7. ✅ **Demo Ready:** 3 pre-run scenarios complete, 1 ready for live execution
-8. ✅ **Clear Documentation:** This spec + README explain implementation
-9. ✅ **Agno UI Dashboard:** Real-time workflow monitoring, session inspection operational
-10. ✅ **Prompt Templates:** Centralized, version-controlled prompts for research and assessment agents
+7. ✅ **Clear Documentation:** This spec + README explain implementation
+8. ✅ **Agno UI Dashboard:** Real-time workflow monitoring, session inspection operational
+9. ✅ **Prompt Templates:** Centralized, version-controlled prompts for research and assessment agents
+
+### ⏸️ Pending (Stages 5-6)
+10. ⏸️ **Demo Ready:** 3 pre-run scenarios complete, 1 ready for live execution (requires Stage 6)

**Remember:** The goal is demonstrating quality of thinking through minimal, working code—not building production infrastructure. Agno UI and prompt templates showcase modern agent development best practices.
```

### Fix #3: Status Value Standardization

```diff
# Line 864 (API Specification - Code Example)
        # Update screen status
-       final_status = "Complete" if not errors else "Partial"
+       final_status = "Complete" if not errors else "Failed"
        airtable.update_screen_status(screen_id, status=final_status)

        return {
            "status": "success" if not errors else "partial",
            "screen_id": screen_id,
            "candidates_processed": len(results),
            "candidates_failed": len(errors),
            "results": results,
            "errors": errors
        }

# Line 1322 (Airtable Schema Reference)
- **Processing:** Python sets status to "Processing" → "Complete" or "Error"
-   - **Note:** Current implementation uses "Error" status (not "Failed" as originally specified)
+ **Processing:** Python sets status to "Processing" → "Complete" or "Failed"

# Line 1372-1373 (Airtable Schema - Current Implementation Notes)
- **Screens.Status:** Complete, Processing only (spec defines: Draft, Processing, Complete, Failed)
- **Assessments.Status:** Complete, In Progress, Error, Pending (spec defines: Pending, Processing, Complete, Failed)
-   - Note: "Error" used instead of "Failed"
+ **Screens.Status:** Draft, Processing, Complete, Failed (demo uses: Processing, Complete, Failed)
+ **Assessments.Status:** Pending, Processing, Complete, Failed (demo uses: Pending, Complete, Failed)
```

### Fix #4: Audit Trail Messaging

```diff
# Line 102 (Key Design Principles)
**Key Design Principles:**

- **Evidence-Aware Scoring:** Explicit handling of "Unknown" when public data is insufficient (using `None`/`null`, not 0 or NaN)
- **Quality-Gated Research:** Optional single incremental search agent step when initial research has quality issues
- **Minimal Audit Trail:** Airtable fields + terminal logs (no separate event DB for v1)
+ **Agno-Managed Observability:** Agno UI dashboard for workflow monitoring; no custom event DB for v1
- **Deep Research Primary:** v1 uses o4-mini-deep-research as default; fast mode is Phase 2+
```

### Fix #8a: PRD Table Helper Clarification

```diff
# PRD Line 159 (Scope Section - Module 4: Candidate Screening)
- ✅ Airtable database with 7 tables (v1: 6 core + 1 helper - People, Portco, Portco_Roles, Searches, Screens, Assessments, Role_Specs; Phase 2+: Workflows, Research_Results)
+ ✅ Airtable database with 7 tables (6 core workflow + Role_Specs helper for template storage; Phase 2+: Workflows, Research_Results)

# Add new subsection after line 162 (before "Technical Stack:")

**Airtable Schema (7 Tables):**

**Core Workflow Tables (6):**
- **People**: Executive network data (guild members, portfolio execs, partner connections)
- **Portco**: Portfolio company records (Pigment, Mockingbird, Synthesia, Estuary)
- **Portco_Roles**: Open leadership positions (CFO/CTO roles at portfolio companies)
- **Searches**: Talent search requests (links roles to candidate screening batches)
- **Screens**: Candidate screening batches (webhook-triggered workflow executions)
- **Assessments**: Individual candidate evaluations (research + assessment results)

**Helper Tables (1):**
- **Role_Specs**: Reusable evaluation templates (CFO_Standard_v1, CTO_Standard_v1)

**Phase 2+ Tables (Deferred):**
- Workflows: Audit trail for multi-step workflows
- Research_Results: Separate storage for deep research outputs
```

### Fix #8b: PRD Scenario-to-Spec Mapping

```diff
# PRD - Add to "Scope" section after the new Airtable Schema subsection (after line 162+)

**Demo Scenarios:**

| Scenario | Portfolio Company | Role Type | Role Spec Template | Candidates | Pre-run Status |
|----------|------------------|-----------|-------------------|-----------|----------------|
| 1 | Pigment | CFO | CFO_Standard_v1 | 3-5 from guild | ⏸️ Pre-run before demo |
| 2 | Mockingbird | CFO | CFO_Standard_v1 | 3-5 from guild | ⏸️ Pre-run before demo |
| 3 | Synthesia | CTO | CTO_Standard_v1 | 3-5 from guild | ⏸️ Pre-run before demo |
| 4 | Estuary | CTO | CTO_Standard_v1 | 2-3 from guild | ⏸️ Live demo execution |

**Notes:**
- Scenarios 1-3 demonstrate results quality and assessment reasoning
- Scenario 4 demonstrates real-time workflow execution and Agno UI monitoring
- All candidates sourced from guildmember_scrape.csv (64 total executives)
- Each scenario uses standard role spec template (CFO_Standard_v1 or CTO_Standard_v1)
- Role specs stored in Role_Specs table, attached to Portco_Roles records
```

---

**End of Document**
