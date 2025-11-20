# Spec Selection Architecture - Final Design

## Overview

This document describes the flexible Spec selection system that allows testing different evaluation criteria without creating permanent Role_Spec records.

---

## Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────┐
│ USER ACTIONS (Airtable UI)                                  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 1. Create Screen Record                                     │
│    - Link to Search                                         │
│    - Link to Candidates                                     │
│    - Set Role Spec Selection dropdown                       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Choose Spec Source (Role Spec Selection field)           │
│                                                              │
│    Option A: "Search Spec" (default)                        │
│    └─> Uses Role_Specs linked via Search                    │
│                                                              │
│    Option B: "Custom Spec"                                  │
│    └─> Paste markdown into Custom Role spec content         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Master Role Spec Content (Formula Field)                 │
│                                                              │
│    Formula:                                                  │
│    IF(                                                       │
│      {Role Spec Selection} = "Custom Spec",                 │
│      {Custom Role spec content},                            │
│      {Role Spec Content (from Search)}                      │
│    )                                                         │
│                                                              │
│    Output: Resolved Spec markdown (current state)           │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Set Status → "Processing" (Triggers Automation)          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ AIRTABLE AUTOMATION (Runs Automatically)                    │
│                                                              │
│ Trigger: Status changes to "Processing"                     │
│ Action:  Copy {Master Role Spec Content}                    │
│          → {Admin-Automation Spec Content Snapshot}         │
│                                                              │
│ Result: Immutable snapshot created                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ PYTHON CODE (FastAPI/AgentOS Runtime)                         │
│                                                              │
│ 1. POST /screen receives ScreenWebhookPayload              │
│    ├─> Payload contains screen_slug with nested data        │
│    ├─> role_spec_slug.role_spec.role_spec_content (snapshot)│
│    └─> candidate_slugs[] array with all candidate data    │
│                                                              │
│ 2. Validate payload (Pydantic ScreenWebhookPayload model)  │
│    ├─> Extract spec_markdown from payload                   │
│    └─> Extract candidates via payload.get_candidates()      │
│                                                              │
│ 3. AgentOSCandidateWorkflow.run_candidate_workflow(...)     │
│    ├─> Passes snapshot Spec + candidate data to workflow    │
│    └─> Executes 4-step AgentOS pipeline (research → assess) │
│                                                              │
│ 4. write_assessment(role_spec_markdown)                     │
│    └─> Stores Spec in Assessment JSON for audit             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ AUDIT TRAIL (Permanent Records)                             │
│                                                              │
│ Screen Record:                                               │
│   - Admin-Automation Spec Content Snapshot (frozen)         │
│                                                              │
│ Assessment Records:                                          │
│   - Assessment JSON (contains role_spec_used field)         │
│                                                              │
│ Result: Full traceability of evaluation criteria            │
└─────────────────────────────────────────────────────────────┘
```

---

The FastAPI/AgentOS runtime receives structured `ScreenWebhookPayload` objects from Airtable automations. The payload contains all required data (spec snapshot, candidate data, role info) in nested objects - no Airtable API reads are performed during execution. The `/screen` endpoint validates the payload using Pydantic, extracts the spec markdown and candidates, then calls `AgentOSCandidateWorkflow.run_candidate_workflow()` for each candidate. This write-only pattern ensures the snapshot Spec is what the workflow evaluates, with zero traversal API calls.

## Field Definitions

### Screens Table

| Field Name | Type | Purpose | Populated By |
|------------|------|---------|--------------|
| **Role Spec Selection** | Single Select | Dropdown to choose Spec source | User |
| **Custom Role spec content** | Long Text | Ad-hoc Spec markdown input | User (optional) |
| **Master Role Spec Content** | Formula | Resolves to active Spec | Airtable (auto) |
| **Admin-Automation Spec Content Snapshot** | Long Text | Frozen Spec copy | Automation (auto) |
| **Role Spec Content (from Search)** | Lookup | Pulls Spec from linked Search | Airtable (auto) |

### Assessments Table

| Field Name | Type | Purpose | Populated By |
|------------|------|---------|--------------|
| **Assessment JSON** | Long Text | Full AssessmentResult (includes role_spec_used) | Python code |
| **Role Spec Markdown Used** | Long Text | Standalone Spec audit field (optional) | Python code |

---

## Workflow States

### State 1: Draft (User Setup)

```
Screen Record:
├─ Status: "Draft"
├─ Role Spec Selection: "Search Spec" (or "Custom Spec")
├─ Custom Role spec content: "" (empty, or user-filled if Custom)
├─ Master Role Spec Content: [Formula resolves to Spec markdown]
└─ Admin-Automation Spec Content Snapshot: "" (empty)
```

**User Actions:**
- Configure Spec source via dropdown
- Optionally paste custom Spec markdown
- Master Role Spec Content updates automatically as formula

---

### State 2: Processing (Automation Triggers)

```
Screen Record:
├─ Status: "Processing" ← User changes this
├─ Role Spec Selection: "Search Spec"
├─ Custom Role spec content: ""
├─ Master Role Spec Content: "# CFO Role Spec\n\n..."
└─ Admin-Automation Spec Content Snapshot: "# CFO Role Spec\n\n..." ← Automation copies
```

**Automation Actions:**
1. Detects Status change to "Processing"
2. Copies Master Role Spec Content → Admin-Automation Spec Content Snapshot
3. Snapshot is now frozen (won't change even if source Spec edited)

---

### State 3: Complete (Assessments Created)

```
Screen Record:
├─ Status: "Complete"
├─ Admin-Automation Spec Content Snapshot: "# CFO Role Spec\n\n..." (frozen)
└─ Linked Assessments: [recAssmt1, recAssmt2, ...]

Assessment Records:
├─ Assessment JSON: {
│    "role_spec_used": "# CFO Role Spec\n\n...",
│    "overall_score": 85.0,
│    ...
│  }
└─ Role Spec Markdown Used: "# CFO Role Spec\n\n..." (optional)
```

**Python Actions:**
- Reads Admin-Automation Spec Content Snapshot
- Runs assessment with frozen Spec
- Stores Spec in Assessment JSON for audit

---

## Immutability Guarantee

### Problem: Spec Drift

**Without snapshot:**
```
Time 0: User creates Screen with "CFO - Series B" Spec
Time 1: Screening starts (reads Spec A)
Time 2: User edits "CFO - Series B" Spec to add new dimension
Time 3: Screening continues (reads Spec B - DIFFERENT!)
```

Result: Some candidates evaluated with Spec A, others with Spec B ❌

---

**With snapshot:**
```
Time 0: User creates Screen with "CFO - Series B" Spec
Time 1: Status → "Processing", automation creates snapshot (Spec A frozen)
Time 2: User edits "CFO - Series B" Spec to add new dimension
Time 3: Screening continues (reads Spec A from snapshot - SAME!)
```

Result: All candidates evaluated with Spec A ✅

---

## Two-Level Audit Trail

### Screen Level (Batch Audit)

**Field:** `Admin-Automation Spec Content Snapshot`

**Question Answered:** "What Spec was used for this screening batch?"

**Query Example:**
```
Show all Screens that used "CFO - Pre-IPO" criteria
→ Filter: Admin-Automation Spec Content Snapshot contains "Pre-IPO"
```

---

### Assessment Level (Individual Audit)

**Field:** `Assessment JSON` (contains `role_spec_used`)

**Question Answered:** "What Spec was used for this specific candidate assessment?"

**Query Example:**
```python
assessment = json.loads(assessment_record["Assessment JSON"])
spec_used = assessment["role_spec_used"]
```

---

## Use Cases

### Use Case 1: Standard Evaluation (Search Spec)

**Setup:**
1. Create Screen
2. Role Spec Selection = "Search Spec"
3. Link to Search (which links to Role_Spec)
4. Set Status → "Processing"

**Result:**
- Master Role Spec Content pulls from linked Role_Spec
- Automation snapshots this Spec
- All assessments use stable, reusable Spec

**Best for:** Production evaluations with standard criteria

---

### Use Case 2: Experimental Criteria (Custom Spec)

**Setup:**
1. Create Screen
2. Role Spec Selection = "Custom Spec"
3. Paste experimental markdown into Custom Role spec content
4. Set Status → "Processing"

**Result:**
- Master Role Spec Content uses custom text
- Automation snapshots this Spec
- All assessments use ad-hoc criteria
- No permanent Role_Spec record created

**Best for:** Testing new evaluation dimensions, demo day flexibility

---

### Use Case 3: A/B Testing Evaluation Criteria

**Setup:**
1. Create Screen A:
   - Role Spec Selection = "Custom Spec"
   - Custom Role spec content = "Growth-stage CFO criteria"
   - Link candidates: [Candidate 1, 2, 3]

2. Create Screen B:
   - Role Spec Selection = "Custom Spec"
   - Custom Role spec content = "Pre-IPO CFO criteria"
   - Link candidates: [Candidate 1, 2, 3] (same candidates)

3. Run both Screens → Compare results

**Result:**
- Same candidates evaluated with different criteria
- Can compare scores side-by-side
- Full audit trail for both experiments

**Best for:** Optimizing evaluation criteria, research

---

## Code Implementation

### Payload Validation (agentos_app.py)

The `/screen` endpoint receives a `ScreenWebhookPayload` that already contains the spec snapshot:

```python
from fastapi import BackgroundTasks, Depends

from demo.models import ScreenWebhookPayload
from demo.screening_service import process_screen_direct

@fastapi_app.post("/screen", response_model=None, status_code=202)
def screen_endpoint(
    payload: ScreenWebhookPayload,
    background_tasks: BackgroundTasks,
    _auth: None = Depends(verify_bearer_token),
) -> dict[str, Any] | JSONResponse:
    """Process screening request with structured payload."""

    candidates = payload.get_candidates()

    background_tasks.add_task(
        process_screen_direct,
        screen_id=payload.screen_id,
        role_spec_markdown=payload.spec_markdown,
        candidates=candidates,
        custom_instructions=payload.custom_instructions,
        airtable=airtable_client,
        logger=logger,
        symbols=SCREEN_LOG_SYMBOLS,
        candidate_runner=candidate_workflow_runner.run_candidate_workflow,
    )

    return {
        "status": "accepted",
        "message": "Screen workflow started",
        "screen_id": payload.screen_id,
        "candidates_queued": len(candidates),
    }
```

**Note:** The Airtable automation sends the complete `screen_slug` object with nested `role_spec_slug`, `search_slug`, and `candidate_slugs[]`. The Python code validates this structure using Pydantic and extracts the needed data directly - no API traversal required.

---

### Writing Assessment (airtable_client.py)

```python
def write_assessment(
    self,
    screen_id: str,
    candidate_id: str,
    assessment: AssessmentResult,
    role_spec_markdown: Optional[str] = None,
) -> str:
    """Create Assessment record with Spec audit trail."""

    fields = {
        "Screen": [screen_id],
        "Candidate": [candidate_id],
        "Assessment JSON": assessment.model_dump_json(),  # Includes role_spec_used
        # ... other fields
    }

    # Optional: Store Spec in standalone field for Airtable filtering
    if role_spec_markdown is not None:
        fields["Role Spec Markdown Used"] = role_spec_markdown

    return self.assessments.create(fields).get("id")
```

---

## Required Airtable Automation

**Automation Name:** "Snapshot Spec on Processing"

**Trigger:**
- Type: When record matches conditions
- Table: Platform-Screens
- Condition: `{Status}` changes to "Processing"

**Action:**
- Type: Update record
- Record: Trigger record
- Field: `Admin-Automation Spec Content Snapshot`
- Value: `{Master Role Spec Content}`

**Additional Settings:**
- Run immediately: Yes
- Only run if snapshot field is empty: Optional (recommended to prevent overwrites)

---

## Testing Checklist

**Pre-Flight:**
- [ ] Automation exists and is active
- [ ] Master Role Spec Content formula is correct
- [ ] Role Spec Selection dropdown has both options

**Functional Test:**
1. [ ] Create Screen with Search Spec mode
2. [ ] Verify Master Role Spec Content shows linked Spec
3. [ ] Set Status → "Processing"
4. [ ] Verify Admin-Automation Spec Content Snapshot populated
5. [ ] Edit linked Role_Spec (change some text)
6. [ ] Verify snapshot unchanged (immutable)

**Custom Spec Test:**
1. [ ] Create Screen with Custom Spec mode
2. [ ] Paste custom markdown
3. [ ] Verify Master Role Spec Content shows custom text
4. [ ] Set Status → "Processing"
5. [ ] Verify snapshot captured custom text

**Code Integration Test:**
1. [ ] Run screening workflow via webhook
2. [ ] Verify payload contains spec snapshot in role_spec_slug.role_spec.role_spec_content
3. [ ] Verify Assessment created with Spec in JSON
4. [ ] Check Assessment JSON contains role_spec_used field
5. [ ] Verify no Airtable API reads occur during execution (write-only pattern)

---

## Troubleshooting

### Issue: Snapshot Not Populated

**Symptoms:** Admin-Automation Spec Content Snapshot is empty after setting Status to "Processing"

**Diagnosis:**
1. Check automation is active in Airtable
2. Check automation trigger condition (Status = "Processing")
3. Check automation action field name matches exactly

**Fix:**
- Manually run automation or create new automation
- Verify field name spelling: `Admin-Automation Spec Content Snapshot`

---

### Issue: Code Reads Empty Spec

**Symptoms:** Screening fails with "No role spec markdown" error

**Diagnosis:**
1. Check if snapshot field exists and is populated
2. Check if Master Role Spec Content formula is working
3. Check if Role Spec Selection is set correctly

**Fix:**
- If snapshot empty: Ensure automation has run
- If formula empty: Check Role Spec Selection value and linked data
- Code will fall back to Master Role Spec Content if snapshot empty

---

### Issue: Assessments Show Different Specs

**Symptoms:** Some Assessments have different Spec than others in same Screen

**Diagnosis:**
- Snapshot was not created before screening started
- Source Spec was edited mid-screening

**Fix:**
- Always trigger automation by setting Status → "Processing" BEFORE starting screening
- Verify snapshot populated before running Python workflow
- Check automation logs for failures

---

## Summary

**Architecture:** Two-level Spec selection with immutable snapshots
**Primary Source:** Admin-Automation Spec Content Snapshot (frozen by automation)
**Fallback Source:** Master Role Spec Content (formula, current state)
**Audit Trail:** Screen-level snapshot + Assessment-level JSON storage
**Flexibility:** Supports both standard (linked) and custom (inline) Specs
**Immutability:** Automation creates point-in-time snapshot when screening starts
**Testing:** Enables A/B testing of evaluation criteria without permanent records

This design balances flexibility for experimentation with immutability for audit compliance.
