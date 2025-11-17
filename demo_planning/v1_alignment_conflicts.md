# v1 Minimal Alignment Tracker (as of 2025-01-19)

This note reflects the current alignment between the demo-planning docs and the **v1 minimal** scope (single `/screen` workflow, Airtable-only storage via Assessments, optional single incremental search pass, Agno `SqliteDb`, ReasoningTools-enabled assessment agent).

## Status Snapshot

**Actual Alignment: ~65% (3 of 6 areas fully resolved)**

- ✅ **Resolved (Verified):** Airtable schema docs (airtable_schema.md, airtable_ai_spec.md), ReasoningTools additions (all 3 files)
- ❌ **Not Resolved (Major Issues):** Workflow spec (async/loops/fast mode remain), data design (broken code examples)
- 🔄 **In Progress:** Updating `spec/spec.md` and `spec/prd.md` to point to the simplified Airtable + workflow architecture and to mention ReasoningTools explicitly.
- ⚠️ **To Confirm:** `spec/v1_minimal_spec.md` still claims 95% alignment; actual alignment is ~65-70%.

## Resolved Items (Verified ✅)

| Area | Files Updated | Verification Status | Notes |
|------|---------------|---------------------|-------|
| Airtable schema/storage | `airtable_schema.md`, `airtable_ai_spec.md` | ✅ **100% VERIFIED** | Reduced to 6 core + 1 helper table (7 total). Assessments stores all 4 fields (`research_structured_json`, `research_markdown_raw`, `assessment_json`, `assessment_markdown_report`). Workflows/Research_Results marked Phase 2+ (lines 36, 44, 50). Pre-population checklist updated. |
| ReasoningTools requirement | `airtable_ai_spec.md`, `data_design.md`, `screening_workflow_spec.md` | ✅ **100% VERIFIED** | Assessment agent configured with `ReasoningTools(add_instructions=True)` in all 3 files. Code example in data_design.md:421-427 matches v1_minimal_spec.md requirements. Tied to PRD AC-PRD-04. |

## Remaining Work

### 🔴 Critical Blockers (Must Fix Before Implementation)

| Priority | Task | File | Lines | Estimated | Status |
|----------|------|------|-------|-----------|--------|
| 🔴 | **Fix async/concurrent code examples** | `screening_workflow_spec.md` | 555, 579, 619, 642, 795 | 30 min | ❌ NOT FIXED |
| 🔴 | **Remove loop constructs** | `screening_workflow_spec.md` | 421, 433-436, 885, 899, 991 | 20 min | ❌ NOT FIXED |
| 🔴 | **Remove fast mode reference** | `screening_workflow_spec.md` | 275 | 5 min | ❌ NOT FIXED |
| 🔴 | **Fix broken code examples** | `data_design.md` | 400-407 | 30 min | ❌ NOT FIXED |
| 🔴 | **Add ReasoningTools to spec** | `spec/spec.md` | ~940 | 15 min | ⏳ PENDING |
| 🔴 | **Fix Airtable schema refs** | `spec/spec.md` | 994-1027 | 20 min | ⏳ PENDING |
| 🔴 | **Fix Airtable schema refs** | `spec/prd.md` | 137, 323-335 | 15 min | ⏳ PENDING |

**Total Critical Path: ~2 hours 15 minutes**

### 🟡 Quality/Documentation (Can Defer)

| Priority | Task | File | Estimated | Status |
|----------|------|------|-----------|--------|
| 🟡 | Correct alignment claim | `spec/v1_minimal_spec.md` | 15 min | ⏳ PENDING |

---

## Detailed Issue Descriptions

### screening_workflow_spec.md Issues

**Issue 1: Async/Concurrent Examples (Lines 555, 579, 619, 642, 795)**
- Contains `async def`, `async for`, `asyncio.gather()` throughout
- Line 642: Direct concurrent task execution with `await asyncio.gather(*tasks)`
- Line 622 acknowledges "async pattern is Phase 2" but code remains
- **Fix**: Remove all async examples OR move to appendix clearly marked "Phase 2+ Only"

**Issue 2: Loop Constructs (Lines 421, 433-436, 885, 899, 991)**
- Line 421: Comment "# From loop" indicates loop context
- Lines 433-436: Active `for` loop over supplements (multi-iteration)
- Lines 885, 899: Test assertions expect loop logic
- Line 991: Changelog references loop end-conditions
- **Fix**: Remove loop iteration code, show single optional incremental search pass

**Issue 3: Fast Mode Reference (Line 275)**
- "Fast mode: 30-60 seconds" timing estimate still documented
- **Fix**: Remove this line entirely (Fast Mode is Phase 2+)

### data_design.md Issues

**Issue: Architecturally Incorrect Code (Lines 400-407)**
- Shows `output_schema=ExecutiveResearchResult` on deep_research_agent
- This will FAIL: deep_research_findings.md:131 states Deep Research models "do NOT support structured outputs"
- Creates parser-less pipeline that contradicts API limitations
- **Fix**: Remove `output_schema` from deep_research_agent config OR document two-step parse approach from deep_research_findings.md

---

## Implementation Readiness Checklist

After completing Critical Blockers:

- [ ] screening_workflow_spec.md shows linear synchronous workflow only
- [ ] data_design.md code examples are runnable (no output_schema on deep_research_agent)
- [ ] spec/spec.md includes ReasoningTools requirement
- [ ] spec/spec.md references 6-7 table Airtable schema
- [ ] spec/prd.md references 6-7 table Airtable schema
- [ ] All docs consistent on: Deep Research → quality check → optional single incremental search → assessment

Once all items are complete, v1 documentation will be fully aligned (~95%+ actual alignment).
