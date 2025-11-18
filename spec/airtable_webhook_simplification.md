# Airtable Webhook Simplification Design

**Status:** Design Document
**Created:** 2025-11-18
**Purpose:** Eliminate brittle Airtable interactions by pushing complexity into Airtable formulas and using delimiter-based data transfer

---

## Problem Statement

### Current Issues

1. **Complex traversal code** - Python makes 4+ API calls to assemble screening context:
   - `GET /screens/{id}` → `GET /searches/{id}` → `GET /role_specs/{id}` → `GET /people/{id}` (×N)
2. **Brittle field mappings** - Multiple fallback checks for field names (`"Full Name"` vs `"Name"`, `"structured_spec_markdown"` vs `"Spec Content"`)
3. **Error-prone data assembly** - Manual RecordDict conversion, nested structure building
4. **High latency** - Sequential API calls add 500ms+ overhead
5. **Difficult to test** - Requires mocking entire Airtable traversal chain

### Proposed Solution

**Push complexity into Airtable, keep Python minimal:**

```
┌──────────────────────────────────────────────┐
│ AIRTABLE (Smart Database)                   │
│ - Rollup formulas create consolidated fields │
│ - Webhook sends ONE complete record          │
│ - Delimiter-based parallel arrays            │
└─────────────────┬────────────────────────────┘
                  │ POST /screen
                  │ {screen_id, role_name, spec_markdown,
                  │  candidate_ids, candidate_names, ...}
                  ▼
┌──────────────────────────────────────────────┐
│ PYTHON (Thin Validation Layer)              │
│ - Pydantic validates payload                 │
│ - Parse delimiters → structured data         │
│ - No Airtable traversal                      │
│ - Direct use in agents                       │
└─────────────────┬────────────────────────────┘
                  │
                  ▼
┌──────────────────────────────────────────────┐
│ RESULTS (Simple JSON Blob)                  │
│ - Write to single "Results JSON" field       │
│ - Optional: denormalize key metrics          │
└──────────────────────────────────────────────┘
```

---

## Target Code Design

### 1. Webhook Payload Model

**File:** `demo/models.py`

```python
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class ScreenWebhookPayload(BaseModel):
    """Complete screening payload from Airtable with delimiter-based candidate data.

    All candidate fields are pipe-delimited parallel arrays that will be zipped together.
    Airtable creates these via Rollup formulas: ARRAYJOIN({Candidates → Field}, " | ")

    Example webhook payload:
    {
        "screen_id": "recABC123",
        "role_name": "CFO - Pigment",
        "portco_name": "Pigment",
        "spec_markdown": "# CFO Role Spec\\n...",
        "custom_instructions": "Focus on Series B experience",
        "candidate_ids": "recP1 | recP2 | recP3",
        "candidate_names": "Jane Doe | John Smith | Bob Jones",
        "candidate_titles": "CFO at Acme | CTO at Beta | VP Finance",
        "candidate_companies": "Acme Inc | Beta Corp | Gamma LLC",
        "candidate_linkedin": "https://... | https://... | https://...",
        "candidate_locations": "San Francisco | New York | Austin",
        "candidate_bios": "Jane has 15 years... | John led... | Bob scaled..."
    }
    """

    # Screen Identity
    screen_id: str = Field(
        ...,
        description="Airtable record ID for the Screen (recXXXX)"
    )

    # Role Context (direct lookups from Search → Role → Role Spec chain)
    role_name: str = Field(
        ...,
        description="Role name, e.g., 'CFO - Pigment'"
    )
    portco_name: str = Field(
        ...,
        description="Portfolio company name"
    )
    spec_markdown: str = Field(
        ...,
        description="Complete role specification in markdown format"
    )
    custom_instructions: Optional[str] = Field(
        None,
        description="Screen-specific evaluation guidance"
    )

    # Candidate Data (pipe-delimited parallel arrays)
    # Required fields
    candidate_ids: str = Field(
        ...,
        description="Pipe-delimited Airtable record IDs: 'recA | recB | recC'"
    )
    candidate_names: str = Field(
        ...,
        description="Pipe-delimited full names: 'Jane Doe | John Smith'"
    )
    candidate_titles: str = Field(
        ...,
        description="Pipe-delimited current titles: 'CFO at Acme | CTO at Beta'"
    )
    candidate_companies: str = Field(
        ...,
        description="Pipe-delimited current companies: 'Acme Inc | Beta Corp'"
    )
    candidate_linkedin: str = Field(
        ...,
        description="Pipe-delimited LinkedIn URLs"
    )

    # Optional candidate fields (may be empty strings)
    candidate_locations: str = Field(
        default="",
        description="Pipe-delimited locations"
    )
    candidate_bios: str = Field(
        default="",
        description="Pipe-delimited professional bio summaries"
    )

    # Optional: Portco Context (for richer agent prompts)
    portco_stage: Optional[str] = Field(
        None,
        description="Company stage: Seed, Series A, Series B, etc."
    )
    portco_sector: Optional[str] = Field(
        None,
        description="Sector: B2B SaaS, Consumer, AI/ML, etc."
    )
    portco_description: Optional[str] = Field(
        None,
        description="Company overview"
    )

    @field_validator('candidate_ids', 'candidate_names', 'candidate_titles',
                     'candidate_companies', 'candidate_linkedin')
    @classmethod
    def validate_not_empty(cls, v: str, info) -> str:
        """Ensure required candidate fields are not empty."""
        field_name = info.field_name
        if not v or not v.strip():
            raise ValueError(f"{field_name} cannot be empty")
        return v.strip()

    def get_candidates(self) -> list[dict[str, str]]:
        """Parse delimiter-based fields into structured candidate records.

        Returns:
            List of candidate dicts with keys: id, name, title, company, linkedin,
            location, bio. All fields guaranteed to exist (may be empty string).

        Raises:
            ValueError: If required arrays have mismatched lengths.

        Example:
            >>> payload.get_candidates()
            [
                {
                    "id": "recP1",
                    "name": "Jane Doe",
                    "title": "CFO at Acme",
                    "company": "Acme Inc",
                    "linkedin": "https://linkedin.com/in/janedoe",
                    "location": "San Francisco",
                    "bio": "Jane has 15 years..."
                },
                ...
            ]
        """
        delimiter = " | "

        # Split all fields
        ids = self.candidate_ids.split(delimiter)
        names = self.candidate_names.split(delimiter)
        titles = self.candidate_titles.split(delimiter)
        companies = self.candidate_companies.split(delimiter)
        linkedin = self.candidate_linkedin.split(delimiter)

        # Optional fields (may be empty)
        locations = self.candidate_locations.split(delimiter) if self.candidate_locations else []
        bios = self.candidate_bios.split(delimiter) if self.candidate_bios else []

        # Validate all required arrays have same length
        required_lengths = [len(ids), len(names), len(titles), len(companies), len(linkedin)]
        if len(set(required_lengths)) != 1:
            raise ValueError(
                f"Candidate field arrays have mismatched lengths: "
                f"ids={len(ids)}, names={len(names)}, titles={len(titles)}, "
                f"companies={len(companies)}, linkedin={len(linkedin)}"
            )

        # Pad optional arrays to match
        num_candidates = len(ids)
        locations = locations + [""] * (num_candidates - len(locations))
        bios = bios + [""] * (num_candidates - len(bios))

        # Zip into structured records
        return [
            {
                "id": id_.strip(),
                "name": name.strip(),
                "title": title.strip(),
                "company": company.strip(),
                "linkedin": linkedin_url.strip(),
                "location": location.strip(),
                "bio": bio.strip(),
            }
            for id_, name, title, company, linkedin_url, location, bio
            in zip(ids, names, titles, companies, linkedin, locations, bios)
        ]
```

### 2. Simplified Webhook Handler

**File:** `demo/app.py`

Replace complex `screen_webhook()` function with:

```python
from pydantic import ValidationError
from demo.models import ScreenWebhookPayload


@app.post("/screen")
def screen_webhook():
    """Process screening webhook with pre-assembled Airtable data.

    Expects complete screening context in webhook payload (no traversal needed).
    Validates, processes, and writes results back to Airtable.
    """

    # 1. Validate payload structure (Pydantic does all validation)
    try:
        payload = ScreenWebhookPayload.model_validate(request.json)
    except ValidationError as e:
        logger.error("%s Invalid webhook payload", LOG_ERROR)
        return jsonify({
            "error": "validation_error",
            "message": "Webhook payload is invalid or missing required fields",
            "details": [
                {
                    "field": ".".join(str(loc) for loc in err["loc"]),
                    "message": err["msg"],
                    "type": err["type"]
                }
                for err in e.errors()
            ]
        }), 400

    logger.info(
        "%s Received screen webhook for %s (%s candidates)",
        LOG_SEARCH,
        payload.screen_id,
        len(payload.candidate_ids.split(" | "))
    )

    # 2. Parse candidates from delimiter-based fields
    try:
        candidates = payload.get_candidates()
    except ValueError as e:
        logger.error("%s Failed to parse candidates: %s", LOG_ERROR, e)
        return jsonify({
            "error": "validation_error",
            "message": f"Candidate data parsing failed: {e}"
        }), 400

    # 3. Process screen (no Airtable traversal needed!)
    airtable = _get_airtable_client()

    try:
        results = process_screen_direct(
            screen_id=payload.screen_id,
            role_spec_markdown=payload.spec_markdown,
            candidates=candidates,
            custom_instructions=payload.custom_instructions,
            airtable=airtable,
            logger=logger,
        )

        # 4. Write consolidated results back
        airtable.update_screen_results(
            screen_id=payload.screen_id,
            results=results,
            status="Complete"
        )

        logger.info(
            "%s Screen %s completed successfully",
            LOG_SUCCESS,
            payload.screen_id
        )
        return jsonify(results), 200

    except Exception as e:
        logger.exception("%s Screen processing failed", LOG_ERROR)
        airtable.update_screen_status(
            payload.screen_id,
            status="Failed",
            error_message=str(e)
        )
        return jsonify({
            "error": "processing_error",
            "screen_id": payload.screen_id,
            "message": str(e)
        }), 500
```

### 3. Simplified Airtable Client

**File:** `demo/airtable_client.py`

Reduce from 253 lines to ~100 lines. Remove all traversal methods:

```python
"""Minimal Airtable API wrapper - no traversal, just CRUD operations."""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any, Final, Optional

from pyairtable import Api, Table

from demo.models import AssessmentResult, ExecutiveResearchResult

__all__: list[str] = ["AirtableClient"]


class AirtableClient:
    """Minimal typed wrapper around pyairtable for write operations only.

    All read operations (traversals, lookups) are handled by Airtable formulas.
    Python only writes results back to Airtable.
    """

    SCREENS_TABLE: Final[str] = "Platform-Screens"
    ASSESSMENTS_TABLE: Final[str] = "Platform-Assessments"

    def __init__(self, api_key: str, base_id: str) -> None:
        """Instantiate the Airtable client and table handles.

        Args:
            api_key: Airtable personal access token with base permissions.
            base_id: Base identifier (appXXXX) optionally containing a
                trailing /table suffix from Airtable's UI URLs.

        Raises:
            ValueError: If either credential is blank.
        """
        api_key = api_key.strip()
        base_id = base_id.strip()
        if not api_key:
            raise ValueError("Airtable API key is required")
        if not base_id:
            raise ValueError("Airtable base ID is required")

        # Strip table ID suffix if present
        clean_base_id = base_id.split("/")[0]

        self.api_key: str = api_key
        self.base_id: str = clean_base_id
        self.api: Api = Api(api_key)

        # Only instantiate tables we write to
        self.screens: Table = self.api.table(self.base_id, self.SCREENS_TABLE)
        self.assessments: Table = self.api.table(self.base_id, self.ASSESSMENTS_TABLE)

    def update_screen_status(
        self,
        screen_id: str,
        status: str,
        error_message: Optional[str] = None,
    ) -> None:
        """Update the status and optional error for a Screen record.

        Args:
            screen_id: Airtable record ID (recXXXX).
            status: Status value (Processing, Complete, Failed).
            error_message: Optional error details.
        """
        screen_id = screen_id.strip()
        status = status.strip()
        if not screen_id:
            raise ValueError("screen_id is required")
        if not status:
            raise ValueError("status is required")

        payload: dict[str, Any] = {"Status": status}
        if error_message:
            payload["Error Message"] = error_message

        try:
            self.screens.update(screen_id, payload)
        except Exception as exc:
            raise RuntimeError(
                f"Failed to update screen {screen_id} status to {status}"
            ) from exc

    def update_screen_results(
        self,
        screen_id: str,
        results: dict[str, Any],
        status: str = "Complete"
    ) -> None:
        """Write screening results back to Airtable.

        Stores complete results as JSON blob plus denormalized key metrics
        for Airtable filtering/sorting.

        Args:
            screen_id: Airtable record ID (recXXXX).
            results: Complete screening results dict.
            status: Final status (default: Complete).
        """
        screen_id = screen_id.strip()
        if not screen_id:
            raise ValueError("screen_id is required")

        # Calculate average score if available
        avg_score = None
        assessment_results = results.get("results", [])
        if assessment_results:
            scores = [
                r["overall_score"]
                for r in assessment_results
                if r.get("overall_score") is not None
            ]
            if scores:
                avg_score = round(sum(scores) / len(scores), 1)

        payload: dict[str, Any] = {
            "Status": status,
            "Results JSON": json.dumps(results, indent=2),
            "Candidates Processed": results.get("candidates_processed", 0),
            "Candidates Failed": results.get("candidates_failed", 0),
            "Completion Time": datetime.now().isoformat(),
        }

        if avg_score is not None:
            payload["Avg Score"] = avg_score

        try:
            self.screens.update(screen_id, payload)
        except Exception as exc:
            raise RuntimeError(
                f"Failed to write results for screen {screen_id}"
            ) from exc

    def write_assessment(
        self,
        screen_id: str,
        candidate_id: str,
        assessment: AssessmentResult,
        research: Optional[ExecutiveResearchResult] = None,
    ) -> str:
        """Persist assessment outputs to the Assessments table.

        Args:
            screen_id: Parent screen record ID.
            candidate_id: Candidate record ID.
            assessment: Structured assessment payload.
            research: Optional structured research payload.

        Returns:
            Newly-created assessment record ID.
        """
        if not screen_id or not candidate_id:
            raise ValueError("screen_id and candidate_id are required")

        fields: dict[str, Any] = {
            "Screen": [screen_id],
            "Candidate": [candidate_id],
            "Status": "Complete",
            "Assessment JSON": assessment.model_dump_json(indent=2),
            "Overall Score": assessment.overall_score,
            "Overall Confidence": assessment.overall_confidence,
            "Topline Summary": assessment.summary,
            "Assessment Model": assessment.assessment_model,
            "Assessment Timestamp": assessment.assessment_timestamp.date().isoformat(),
        }

        if research is not None:
            fields["Research Structured JSON"] = research.model_dump_json(indent=2)
            fields["Research Model"] = research.research_model

        try:
            record = self.assessments.create(fields)
        except Exception as exc:
            raise RuntimeError(
                f"Failed to write assessment for candidate {candidate_id}"
            ) from exc

        record_id = record.get("id")
        if not record_id:
            raise RuntimeError(
                f"Assessment created but Airtable did not return record ID for candidate {candidate_id}"
            )
        return record_id
```

### 4. Updated Screening Service

**File:** `demo/screening_service.py`

Add new function that accepts parsed candidate data directly:

```python
def process_screen_direct(
    screen_id: str,
    role_spec_markdown: str,
    candidates: list[dict[str, str]],
    custom_instructions: Optional[str],
    airtable: AirtableClient,
    *,
    logger: logging.Logger,
    symbols: LogSymbols | None = None,
) -> dict[str, Any]:
    """Execute screening workflow with pre-parsed candidate data.

    Args:
        screen_id: Airtable record ID for the Screen.
        role_spec_markdown: Complete role specification markdown.
        candidates: List of candidate dicts from webhook payload.
        custom_instructions: Optional screen-specific guidance.
        airtable: Airtable client for writing results.
        logger: Logger for workflow progress.
        symbols: Optional logging glyphs.

    Returns:
        Summary payload with results for all candidates.
    """
    glyphs = symbols or LogSymbols()
    start_ts = perf_counter()

    results: list[dict[str, Any]] = []
    errors: list[dict[str, str]] = []

    for candidate in candidates:
        candidate_id = candidate["id"]
        candidate_name = candidate["name"]

        try:
            assessment = screen_single_candidate(
                candidate_data=candidate,
                role_spec_markdown=role_spec_markdown,
                screen_id=screen_id,
            )

            assessment_record_id = airtable.write_assessment(
                screen_id=screen_id,
                candidate_id=candidate_id,
                assessment=assessment,
            )

            results.append({
                "candidate_id": candidate_id,
                "assessment_id": assessment_record_id,
                "overall_score": assessment.overall_score,
                "confidence": assessment.overall_confidence,
                "summary": assessment.summary,
                "assessed_at": assessment.assessment_timestamp.isoformat(),
            })

            logger.info(
                "%s Candidate %s screened successfully (score=%s)",
                glyphs.success,
                candidate_name,
                assessment.overall_score,
            )

        except Exception as exc:
            logger.error(
                "%s Candidate %s failed during screening: %s",
                glyphs.error,
                candidate_name,
                exc,
            )
            errors.append({
                "candidate_id": candidate_id,
                "error": str(exc),
            })

    duration = perf_counter() - start_ts

    return {
        "status": "success" if not errors else "partial",
        "screen_id": screen_id,
        "candidates_total": len(candidates),
        "candidates_processed": len(results),
        "candidates_failed": len(errors),
        "execution_time_seconds": round(duration, 2),
        "results": results,
        "errors": errors if errors else None,
    }
```

---

## Target Airtable Schema

### Platform-Screens Table Additions

Add these **formula/rollup fields** to consolidate linked data:

#### Required Fields

| Field Name | Field Type | Formula/Configuration |
|------------|-----------|----------------------|
| **Candidate IDs** | Rollup | Rollup from `{Candidates}` → `ARRAYJOIN(values, " \| ")` |
| **Candidate Names** | Rollup | Rollup from `{Candidates}` → Field: `Name` → `ARRAYJOIN(values, " \| ")` |
| **Candidate Titles** | Rollup | Rollup from `{Candidates}` → Field: `Current Title` → `ARRAYJOIN(values, " \| ")` |
| **Candidate Companies** | Rollup | Rollup from `{Candidates}` → Field: `Current Company` → `ARRAYJOIN(values, " \| ")` |
| **Candidate LinkedIn** | Rollup | Rollup from `{Candidates}` → Field: `LinkedIn URL` → `ARRAYJOIN(values, " \| ")` |
| **Role Name** | Lookup | Lookup from `{Search}` → `{Role}` → `Role Name` |
| **Portco Name** | Lookup | Lookup from `{Search}` → `{Role}` → `{Portco}` → `Company Name` |
| **Spec Markdown** | Lookup | Lookup from `{Search}` → `{Role Spec}` → `Spec Content` |

#### Optional Fields

| Field Name | Field Type | Formula/Configuration |
|------------|-----------|----------------------|
| **Candidate Locations** | Rollup | Rollup from `{Candidates}` → Field: `Location` → `ARRAYJOIN(values, " \| ")` |
| **Candidate Bios** | Rollup | Rollup from `{Candidates}` → Field: `Bio` → `ARRAYJOIN(values, " \| ")` |
| **Portco Stage** | Lookup | Lookup from `{Search}` → `{Role}` → `{Portco}` → `Stage` |
| **Portco Sector** | Lookup | Lookup from `{Search}` → `{Role}` → `{Portco}` → `Sector` |
| **Portco Description** | Lookup | Lookup from `{Search}` → `{Role}` → `{Portco}` → `Description` |

#### Results Storage Fields

| Field Name | Field Type | Purpose |
|------------|-----------|---------|
| **Results JSON** | Long Text | Complete screening results as JSON blob |
| **Candidates Processed** | Number | Count of successfully screened candidates (for filtering) |
| **Candidates Failed** | Number | Count of failed candidates (for filtering) |
| **Avg Score** | Number | Average assessment score across candidates (for sorting) |
| **Completion Time** | Date & Time | When screening completed |
| **Error Message** | Long Text | Error details if screening fails |

### Step-by-Step Airtable Configuration

#### 1. Add Candidate Rollup Fields

For each candidate data field:

1. Click **+** to add new field in `Platform-Screens`
2. Choose **Rollup** field type
3. Configure:
   - **Field name**: `Candidate IDs`, `Candidate Names`, etc. (match table above)
   - **Link to table**: Select `{Candidates}` (existing linked record field)
   - **Field from People**: Select corresponding field (`Name`, `Current Title`, etc.)
   - **Aggregation function**: `ARRAYJOIN(values, " | ")`
4. Click **Create field**

Repeat for:
- Candidate IDs (linked record IDs)
- Candidate Names
- Candidate Titles
- Candidate Companies
- Candidate LinkedIn
- Candidate Locations (optional)
- Candidate Bios (optional)

#### 2. Add Role Context Lookup Fields

For each role/portco field:

1. Click **+** to add new field in `Platform-Screens`
2. Choose **Lookup** field type
3. Configure:
   - **Field name**: `Role Name`, `Portco Name`, etc.
   - **Link to table**: Select `{Search}` (existing linked record field)
   - **Field from Searches**:
     - For `Role Name`: Select `{Role}` → then `Role Name`
     - For `Portco Name`: Select `{Role}` → `{Portco}` → `Company Name`
     - For `Spec Markdown`: Select `{Role Spec}` → `Spec Content`
4. Click **Create field**

Repeat for:
- Role Name
- Portco Name
- Spec Markdown
- Portco Stage (optional)
- Portco Sector (optional)
- Portco Description (optional)

#### 3. Add Results Storage Fields

1. **Results JSON** - Long Text field (create new)
2. **Candidates Processed** - Number field (create new)
3. **Candidates Failed** - Number field (create new)
4. **Avg Score** - Number field (create new, format as decimal with 1 decimal place)
5. **Completion Time** - Date & Time field (create new)
6. **Error Message** - Long Text field (may already exist)

#### 4. Verify Webhook Payload

Create a test automation in Airtable:

1. **Trigger**: When record matches conditions → Table: `Platform-Screens`, Condition: `Status = "Processing"`
2. **Action**: Send webhook to `{your-ngrok-url}/screen`
3. **Webhook body**: Select "Send custom JSON"
4. **JSON payload**:

```json
{
  "screen_id": "{{RECORD_ID}}",
  "role_name": "{{Role Name}}",
  "portco_name": "{{Portco Name}}",
  "spec_markdown": "{{Spec Markdown}}",
  "custom_instructions": "{{Custom Instructions}}",
  "candidate_ids": "{{Candidate IDs}}",
  "candidate_names": "{{Candidate Names}}",
  "candidate_titles": "{{Candidate Titles}}",
  "candidate_companies": "{{Candidate Companies}}",
  "candidate_linkedin": "{{Candidate LinkedIn}}",
  "candidate_locations": "{{Candidate Locations}}",
  "candidate_bios": "{{Candidate Bios}}",
  "portco_stage": "{{Portco Stage}}",
  "portco_sector": "{{Portco Sector}}",
  "portco_description": "{{Portco Description}}"
}
```

---

## Implementation Plan

### Phase 1: Add Airtable Fields (You - 30 mins)

**Status:** Not Started
**Owner:** Will (Airtable configuration)
**Estimated Time:** 30 minutes

#### Steps

1. **[5 min] Add Candidate Rollup Fields**
   - [ ] `Candidate IDs` - Rollup from Candidates → ARRAYJOIN(values, " | ")
   - [ ] `Candidate Names` - Rollup from Candidates → Name → ARRAYJOIN(values, " | ")
   - [ ] `Candidate Titles` - Rollup from Candidates → Current Title → ARRAYJOIN(values, " | ")
   - [ ] `Candidate Companies` - Rollup from Candidates → Current Company → ARRAYJOIN(values, " | ")
   - [ ] `Candidate LinkedIn` - Rollup from Candidates → LinkedIn URL → ARRAYJOIN(values, " | ")
   - [ ] `Candidate Locations` - Rollup from Candidates → Location → ARRAYJOIN(values, " | ")
   - [ ] `Candidate Bios` - Rollup from Candidates → Bio → ARRAYJOIN(values, " | ")

2. **[5 min] Add Role Context Lookup Fields**
   - [ ] `Role Name` - Lookup from Search → Role → Role Name
   - [ ] `Portco Name` - Lookup from Search → Role → Portco → Company Name
   - [ ] `Spec Markdown` - Lookup from Search → Role Spec → Spec Content
   - [ ] `Portco Stage` - Lookup from Search → Role → Portco → Stage
   - [ ] `Portco Sector` - Lookup from Search → Role → Portco → Sector
   - [ ] `Portco Description` - Lookup from Search → Role → Portco → Description

3. **[5 min] Add Results Storage Fields**
   - [ ] `Results JSON` - Long Text field
   - [ ] `Candidates Processed` - Number field
   - [ ] `Candidates Failed` - Number field
   - [ ] `Avg Score` - Number field (1 decimal place)
   - [ ] `Completion Time` - Date & Time field

4. **[10 min] Test Field Population**
   - [ ] Create or select test Screen record with linked Search + Candidates
   - [ ] Verify all rollup fields populate correctly
   - [ ] Check delimiter format (should be " | " with spaces)
   - [ ] Verify Spec Markdown contains full content

5. **[5 min] Update Webhook Automation**
   - [ ] Update Airtable automation to send new fields
   - [ ] Use JSON payload template from schema section above
   - [ ] Test webhook sends correctly to ngrok/local endpoint

**Acceptance Criteria:**
- All fields populate with correct data
- Delimiters are consistent (" | ")
- Webhook automation sends complete payload

---

### Phase 2: Create Simplified Models (Claude - 15 mins)

**Status:** Not Started
**Owner:** Claude
**Estimated Time:** 15 minutes

#### Steps

1. **[5 min] Add ScreenWebhookPayload to models.py**
   - [ ] Add import for pydantic validators
   - [ ] Create `ScreenWebhookPayload` class with all fields
   - [ ] Add `get_candidates()` method with delimiter parsing
   - [ ] Add field validators for required fields

2. **[5 min] Write Unit Tests**
   - [ ] Test valid payload parsing
   - [ ] Test candidate parsing with matching arrays
   - [ ] Test validation errors for empty required fields
   - [ ] Test validation errors for mismatched array lengths
   - [ ] Test optional field handling (locations, bios)

3. **[5 min] Run Tests**
   - [ ] Execute: `uv run pytest tests/test_models.py -v`
   - [ ] Verify all tests pass
   - [ ] Fix any validation issues

**Acceptance Criteria:**
- Pydantic model validates all required fields
- `get_candidates()` correctly parses delimiter-based data
- All tests pass

**Files Modified:**
- `demo/models.py` (~100 lines added)
- `tests/test_models.py` (new file, ~150 lines)

---

### Phase 3: Simplify Airtable Client (Claude - 15 mins)

**Status:** Not Started
**Owner:** Claude
**Estimated Time:** 15 minutes

#### Steps

1. **[10 min] Refactor airtable_client.py**
   - [ ] Remove `get_screen()` method (no longer needed)
   - [ ] Remove `get_role_spec()` method (no longer needed)
   - [ ] Remove table handles for read-only tables (searches, role_specs, people, etc.)
   - [ ] Keep only `screens` and `assessments` table handles
   - [ ] Add `update_screen_results()` method
   - [ ] Update `update_screen_status()` to handle error messages
   - [ ] Keep `write_assessment()` unchanged

2. **[5 min] Update Tests**
   - [ ] Remove tests for deleted traversal methods
   - [ ] Add tests for `update_screen_results()`
   - [ ] Verify `write_assessment()` still works

**Acceptance Criteria:**
- Client reduced from ~253 lines to ~100 lines
- No traversal methods remain
- All tests pass

**Files Modified:**
- `demo/airtable_client.py` (~150 lines removed)
- `tests/test_airtable_client.py` (~50 lines modified)

---

### Phase 4: Update Webhook Handler (Claude - 20 mins)

**Status:** Not Started
**Owner:** Claude
**Estimated Time:** 20 minutes

#### Steps

1. **[5 min] Add process_screen_direct() to screening_service.py**
   - [ ] Create new function accepting parsed candidates
   - [ ] Copy logic from existing `process_screen()`
   - [ ] Remove Airtable traversal calls
   - [ ] Accept `role_spec_markdown` and `candidates` directly

2. **[10 min] Update app.py webhook handler**
   - [ ] Import `ScreenWebhookPayload` from models
   - [ ] Replace request parsing with Pydantic validation
   - [ ] Call `payload.get_candidates()` to parse delimiter data
   - [ ] Call `process_screen_direct()` instead of `process_screen()`
   - [ ] Update error handling for validation errors
   - [ ] Add logging for payload validation

3. **[5 min] Update agentos_app.py (if needed)**
   - [ ] Apply same changes to AgentOS runtime
   - [ ] Ensure consistency between Flask and AgentOS handlers

**Acceptance Criteria:**
- Webhook validates payload with Pydantic
- No Airtable traversal occurs in handler
- Error messages are clear for validation failures
- Both Flask and AgentOS runtimes updated

**Files Modified:**
- `demo/screening_service.py` (~50 lines added)
- `demo/app.py` (~30 lines modified)
- `demo/agentos_app.py` (~30 lines modified)

---

### Phase 5: Integration Testing (Both - 20 mins)

**Status:** Not Started
**Owner:** Will + Claude
**Estimated Time:** 20 minutes

#### Steps

1. **[5 min] Start Local Server**
   - [ ] Execute: `uv run python demo/app.py`
   - [ ] Verify server starts without errors
   - [ ] Confirm Airtable connection succeeds

2. **[5 min] Start ngrok**
   - [ ] Execute: `ngrok http 5001`
   - [ ] Copy ngrok URL
   - [ ] Update Airtable webhook automation with new URL

3. **[5 min] Test with Real Screen**
   - [ ] Create test Screen in Airtable with 1-2 candidates
   - [ ] Set Status to "Processing" to trigger webhook
   - [ ] Monitor Flask logs for webhook receipt
   - [ ] Verify Screen status updates to "Complete"
   - [ ] Check Results JSON field populated

4. **[5 min] Verify Results**
   - [ ] Open Results JSON field
   - [ ] Verify structure matches expected format
   - [ ] Check Assessment records created
   - [ ] Verify all candidate data correctly parsed
   - [ ] Check no errors in logs

**Acceptance Criteria:**
- Webhook triggers successfully
- Payload validates without errors
- Screening completes end-to-end
- Results written back to Airtable
- No traversal errors in logs

**Test Checklist:**
- [ ] Webhook receives correct payload structure
- [ ] Delimiter parsing produces correct candidate count
- [ ] All candidate fields accessible in agents
- [ ] Assessment records created successfully
- [ ] Screen status updates correctly
- [ ] Results JSON contains all expected data

---

### Phase 6: Cleanup & Documentation (Claude - 10 mins)

**Status:** Not Started
**Owner:** Claude
**Estimated Time:** 10 minutes

#### Steps

1. **[5 min] Remove Dead Code**
   - [ ] Mark old `process_screen()` as deprecated
   - [ ] Add comments explaining new pattern
   - [ ] Remove unused imports

2. **[5 min] Update README**
   - [ ] Document new webhook payload structure
   - [ ] Add example payload JSON
   - [ ] Update Airtable setup instructions
   - [ ] Add troubleshooting guide for delimiter parsing

**Acceptance Criteria:**
- No dead code remains
- Documentation reflects new pattern
- Setup instructions are clear

**Files Modified:**
- `demo/screening_service.py` (deprecation notices)
- `README.md` (updated setup instructions)
- `spec/airtable_webhook_simplification.md` (this document)

---

## Benefits Summary

### Code Simplification

| Metric | Before | After | Reduction |
|--------|--------|-------|-----------|
| **airtable_client.py** | 253 lines | ~100 lines | **60%** |
| **API calls per screen** | 4+ sequential | 0 (webhook only) | **100%** |
| **Field mapping logic** | 15+ fallback checks | 0 (Pydantic validation) | **100%** |
| **Test mocking complexity** | High (mock chain) | Low (mock payload) | **80%** |

### Operational Benefits

- **Faster**: No sequential API calls → ~500ms+ saved per screen
- **More reliable**: Pydantic validation catches payload issues immediately
- **Easier to test**: Mock single webhook payload instead of Airtable chain
- **Simpler to extend**: Add field in Airtable → add line to Pydantic model
- **Less brittle**: Field name changes isolated to Airtable formulas

### Maintenance Benefits

- **Self-documenting**: Pydantic model = API contract
- **Type-safe**: MyPy can validate entire webhook flow
- **Clear errors**: Pydantic errors point to exact field + issue
- **No traversal bugs**: Can't have stale data or broken links

---

## Rollback Plan

If issues arise during implementation:

### Immediate Rollback (< 5 mins)

1. Keep old `process_screen()` function intact during Phase 4
2. Add feature flag in settings:
   ```python
   USE_SIMPLIFIED_WEBHOOK = os.getenv("USE_SIMPLIFIED_WEBHOOK", "false").lower() == "true"
   ```
3. Branch in webhook handler:
   ```python
   if settings.USE_SIMPLIFIED_WEBHOOK:
       # New path
   else:
       # Old path (existing code)
   ```

### Gradual Migration

1. Deploy both paths simultaneously
2. Test simplified path with subset of screens
3. Monitor error rates
4. Gradually increase traffic to new path
5. Remove old path once validated

---

## Success Metrics

### Quantitative

- [ ] Webhook processing time < 100ms (down from ~500ms+)
- [ ] Zero field mapping errors in logs
- [ ] 100% test coverage for new models
- [ ] Zero Airtable traversal API calls

### Qualitative

- [ ] Webhook handler code reads clearly top-to-bottom
- [ ] New developer can understand flow in < 5 minutes
- [ ] Pydantic validation errors are actionable
- [ ] Airtable field changes don't require Python changes

---

## Open Questions

1. **Delimiter choice**: Is " | " (space-pipe-space) acceptable, or prefer different delimiter?
2. **Portco context**: Should we include stage/sector/description, or is role spec sufficient?
3. **Error handling**: Should validation errors write to Airtable Error Message field?
4. **Backward compatibility**: Keep old `process_screen()` for a grace period?

---

## References

- **Current Implementation**:
  - `demo/airtable_client.py:66-127` - Complex traversal code
  - `demo/screening_service.py:42-201` - Existing workflow
  - `demo/app.py:187-236` - Current webhook handler

- **Airtable Schema**:
  - `spec/dev_reference/airtable_ai_spec.md` - Current schema
  - Platform-Screens table structure

- **Models**:
  - `demo/models.py` - Existing Pydantic models
