# Document Alignment Issues & Required Fixes

**Date:** 2025-01-16
**Documents Reviewed:** data_design.md, airtable_schema.md, role_spec_design.md, deep_research_findings.md

---

## 1. Critical Misalignments

### Issue 1.1: data_design.md Not Updated with Deep Research Findings

**Problem:**
- Lines 266-427 show `ExecutiveResearchResult` as direct output from `o4-mini-deep-research`
- deep_research_findings.md proved structured outputs NOT supported by Deep Research models
- Two-step approach required: Deep Research → Parser Agent

**Fix Required in data_design.md:**

Lines 266-315 - Change header comment:
```python
# FROM:
# Research Output Models (from o4-mini-deep-research)

# TO:
# Research Output Models (from research pipeline)
```

Update `ExecutiveResearchResult` docstring:
```python
# FROM:
"""Structured output from Deep Research API (o4-mini-deep-research)."""

# TO:
"""Structured research output produced by parser agent over Deep Research
markdown + citations (see deep_research_findings.md)."""
```

Replace usage example with two-step pattern:
```python
# Step 1: Deep Research (unstructured markdown + citations)
deep_research_agent = Agent(
    model=OpenAIResponses(id="o4-mini-deep-research", max_tool_calls=1),
    instructions="Comprehensive executive research with inline citations..."
    # NO response_model
)

# Step 2: Parser → structured ExecutiveResearchResult
parser_agent = Agent(
    model=OpenAIResponses(id="gpt-5-mini"),
    output_schema=ExecutiveResearchResult,
    instructions="Parse research markdown + citations into structured form."
)
```

**Reference:** See deep_research_findings.md "Implementation Recommendations"

### Issue 1.2: ExecutiveResearchResult Schema Incomplete

**Problem:**
Missing fields that exist in airtable_schema.md Research_Results table:
- `research_confidence: Literal["High", "Medium", "Low"]`
- `gaps: List[str]` for missing information

**Fix Required in data_design.md:**

Line 289 - Add to ExecutiveResearchResult:
```python
class ExecutiveResearchResult(BaseModel):
    # ... existing fields ...

    # Add these (align with airtable_schema.md Research_Results table):
    research_confidence: Literal["High", "Medium", "Low"] = "Medium"
    gaps: List[str] = Field(
        default_factory=list,
        description="Information not found or unclear from public sources"
    )

    # Metadata
    research_timestamp: datetime = Field(default_factory=datetime.now)
    research_model: str = "o4-mini-deep-research"
```

**Fix Required in airtable_schema.md:**

Line 349 - Add missing fields to Research_Results table:
```
| `research_confidence` | Single Select | High/Medium/Low | ✓ | Overall confidence |
| `research_gaps` | Long Text | **JSON array** | ○ | Missing information |
```

### Issue 1.3: Scoring Scale Inconsistency (0-5 vs 1-5)

**Problem:**
- DimensionScore Pydantic model correctly uses `score: Optional[int] = Field(None, ge=1, le=5)`
- But role_spec_design.md examples say "Score 0-5 where 0 = Unknown"
- This creates confusion about encoding unknown scores

**Fix Required in role_spec_design.md:**

Lines 86-94 - Replace scale definition in spec template:
```markdown
# FROM:
**Scale:**
- 5 (Exceptional): [Criteria]
- 4 (Strong): [Criteria]
- 3 (Adequate): [Criteria]
- 2 (Weak): [Criteria]
- 1 (Poor): [Criteria]
- 0 (Unknown): Insufficient public evidence

# TO:
**Scale:**
- 5 (Exceptional): [Criteria using observable signals]
- 4 (Strong): [Criteria using observable signals]
- 3 (Adequate): [Criteria using observable signals]
- 2 (Weak): [Criteria using observable signals]
- 1 (Poor): [Criteria using observable signals]
- _Leave blank (null/None) if insufficient public evidence to score_
- _DO NOT use 0, NaN, or empty string - use null/None for unknown_
```

Lines 186-193 - Update `build_assessment_prompt()` example:
```markdown
# FROM:
Score (0-5, where 0 = Unknown / Not enough public evidence):

# TO:
Score (1–5; if you cannot score due to insufficient public evidence,
leave the score as null/None and explain why):
```

**Fix Required in data_design.md:**

Lines 320-340 - Add explicit encoding rule to DimensionScore notes:
```python
# Evidence-Aware Scoring:
- `score: Optional[int]` allows `None` (Python) / `null` (JSON) for "Unknown/Insufficient Evidence"
- Range 1-5 when evidence exists, `None` when it doesn't
- **DO NOT use:** NaN, 0, or empty string - always use `None` for missing scores
- Prevents forced guessing when public data is thin
- Example: `{"score": null, "reasoning": "No public data on fundraising experience"}`

# Correct:
{"dimension": "Strategic Partnership", "score": null, "reasoning": "No public data."}

# Incorrect:
{"dimension": "Strategic Partnership", "score": 0, ...}  # NEVER use 0 for Unknown
```

### Issue 1.4: "All LLM Interactions Use Pydantic" Oversimplification

**Problem:**
data_design.md line 262 states "All LLM interactions use structured outputs via Pydantic models" but Deep Research can't use Pydantic.

**Fix Required in data_design.md:**

Line 262 - Soften the claim:
```
# FROM:
All LLM interactions use structured outputs via Pydantic models to ensure
type safety and consistent parsing.

# TO:
All **structured** LLM interactions (assessment, parsing, fast web-search mode)
use Pydantic models. Deep Research itself returns markdown + citations that are
parsed into these models.
```

### Issue 1.5: "Pending Decisions" Already Resolved

**Problem:**
data_design.md lines 502-522 list questions as pending, but airtable_schema.md answers them.

**Fix Required in data_design.md:**

Lines 502-522 - Delete "Outstanding Questions for Schema Definition" section. Replace with:
```markdown
## Schema Status

All schema decisions finalized. See:
- Field mappings: airtable_schema.md Lines 60-92 (People table)
- Research storage: airtable_schema.md Lines 333-356 (Research_Results table)
- Assessment storage: airtable_schema.md Lines 359-383 (Assessments table)
- Deduplication: See Section 4 of this document (alignment_issues_and_fixes.md)
```

---

## 2. Missing Algorithm Specifications

### Missing 2.1: Overall Score Calculation

**Problem:**
All documents mention "evidence-aware weighting" but none define the actual algorithm.

**Specification (add to technical spec or PRD):**

**Algorithm Definition:**
```
Evidence-Aware Overall Score Calculation

Input:
- dimension_scores: List[DimensionScore] (with score 1-5 or None)
- spec_dimensions: List[dict] (with name, weight)

Logic:
1. Filter to scored dimensions (score is not None)
2. If <2 scored dimensions, return None
3. Extract weights for scored dimensions only
4. Normalize weights to sum to 100%
5. Calculate weighted average on 1-5 scale
6. Convert to 0-100 scale: (avg - 1) * 25
7. Round to 1 decimal place

Edge Cases:
- All scores null → return None
- 1 scored dimension → return None (need ≥2 for reliability)
- Strategic Partnership null, 5 others scored → calculate from 5 only

Example:
  Spec: Fundraising(25%), Operations(20%), Strategic(15%), Leadership(15%), Sector(15%), Stage(10%)
  Scored: Fundraising=4, Operations=4, Leadership=3, Sector=5, Stage=5
  Missing: Strategic (score=None)

  Scored weights: 25+20+15+15+10 = 85
  Normalized: 25/85=0.294, 20/85=0.235, 15/85=0.176, 15/85=0.176, 10/85=0.118
  Weighted avg: 4*0.294 + 4*0.235 + 3*0.176 + 5*0.176 + 5*0.118 = 4.12
  Scaled to 100: (4.12 - 1) * 25 = 78.0
```

**Reference Implementation:**
See alignment_issues_and_fixes.md (original version) lines 100-173 for full Python code.
Will be implemented in `assessment.py` module.

### Missing 2.2: Role Spec Parser Algorithm

**Problem:**
role_spec_design.md defines `parse_role_spec()` signature but no implementation.

**Specification (add to technical spec):**

**Parser Algorithm:**
```
Role Spec Markdown Parser

Input: Markdown text with structured sections
Output: Dict with role_context, dimensions[], must_haves[], nice_to_haves[], red_flags[]

Parsing Logic:
1. Extract "## Role Context" section (until next ##)
2. Find all dimension headers: "### N. DimensionName (Weight: X%)"
3. For each dimension:
   - Extract weight from header
   - Extract "**Definition:**" text
   - Extract "**Evidence Level:**" (High/Medium/Low)
   - Extract scale entries "- N (Label): criteria"
4. Extract "## Must-Haves" checkboxes
5. Extract "## Nice-to-Haves" bullets
6. Extract "## Red Flags" bullets

Implementation: Regex-based extraction (see alignment_issues_and_fixes.md original lines 185-281)
Module: spec_parser.py
```

**Reference:** Full regex implementation available in alignment_issues_and_fixes.md (original).

### Missing 2.3: Citation → Evidence Quote Extraction

**Problem:**
Citations from Deep Research are `{url, title}`, but DimensionScore.evidence_quotes needs text snippets.

**Specification (add to technical spec):**

**Quote Extraction Process:**
```
Evidence Quote Extraction

Input:
- research_text: Full markdown research output
- dimension: Dimension name
- citations: List[Citation]

Process:
1. Use gpt-5-mini with structured output
2. Prompt: "Extract 1-3 key quotes supporting {dimension}"
3. Requirements: Direct excerpts, 1-2 sentences, concrete evidence
4. Return: List[str] (or empty if no relevant quotes)

Implementation: LLM-based extraction using Agno Agent
Model: gpt-5-mini with QuoteExtraction Pydantic schema
Module: assessment.py
```

**Reference:** Full implementation in alignment_issues_and_fixes.md (original) lines 295-350.

---

## 3. Cross-Document Reference Fixes

### Fix 3.1: Establish data_design.md as Canonical Schema Source

**Add to top of data_design.md:**
```markdown
## Document Status

This document defines the **canonical Pydantic schemas** for the Talent Signal Agent.

Other documents reference these schemas:
- airtable_schema.md: Shows how these schemas map to Airtable JSON fields
- role_spec_design.md: Uses these schemas in assessment flow
- deep_research_findings.md: Explains two-step research → structured output process

For schema changes, update this document first, then sync references.
```

### Fix 3.2: Add Source Attribution to airtable_schema.md

**Add to "JSON Field Schemas" section (line 393):**
```markdown
## JSON Field Schemas

> **Note:** These JSON examples show the serialized form of Pydantic models defined
> in `data_design.md` (Structured Output Schemas section). The parser agent produces
> these via `gpt-5-mini` over Deep Research markdown + citations.

### ExecutiveResearchResult (Research_Results.research_json)

**Source Model:** `data_design.md` lines 289-315
**Production:** Parser agent (`gpt-5-mini`) over Deep Research output
```

### Fix 3.3: Unify ExecutiveResearchResult Definition

**Problem:**
deep_research_findings.md defines ExecutiveResearchResult locally with slight differences from data_design.md.

**Fix Required in deep_research_findings.md:**

Lines 193-220 - Replace local class definition with reference:
```python
# FROM:
class ExecutiveResearchResult(BaseModel):
    exec_name: str
    current_role: str
    ...

# TO:
"""
We use the ExecutiveResearchResult Pydantic model defined in
demo_planning/data_design.md (Structured Output Schemas section).

Key fields:
- career_timeline: List[CareerEntry] (not List[str])
- research_confidence: Literal["High", "Medium", "Low"]
- gaps: List[str]
- citations: List[Citation] with url, title, snippet, relevance_note

See data_design.md lines 289-315 for complete schema.
"""
```

### Fix 3.4: Clarify Research_Results vs Workflows Table Separation

**Problem:**
deep_research_findings.md line 362-383 describes research fields on Workflows table, but finalized design uses separate Research_Results table.

**Fix Required in deep_research_findings.md:**

Lines 362-383 - Replace Workflows-centric schema with:
```markdown
### Research Storage Schema

**Workflows Table:**
- workflow_id (primary key)
- screen (link to Screens)
- candidate (link to People)
- status, execution_log, error_message
- Timestamps: research_started, research_completed, assessment_started, assessment_completed

**Research_Results Table:**
- research_id (primary key)
- workflow (link to Workflows) - 1:1 relationship
- candidate (link to People)
- research_summary (Long Text) - extracted from ExecutiveResearchResult
- research_json (Long Text) - full ExecutiveResearchResult JSON
- citations (Long Text, JSON array)
- research_confidence (Single Select: High/Medium/Low)
- research_gaps (Long Text, JSON array)
- research_timestamp, research_model

**Mapping:** Execution metadata → Workflows; Structured research → Research_Results
**Reference:** See airtable_schema.md lines 293-356 for complete field definitions
```

---

## 4. Deduplication Strategy

**Problem:**
guildmember_scrape.csv may contain duplicates (same person from multiple sources: FMLinkedIN, FMGuildPage, FMCFO).

**Solution (add to setup documentation):**

```markdown
### CSV Preprocessing: Deduplication

Before Airtable import, run deduplication on guildmember_scrape.csv:

**Strategy:**
1. Normalize names (lowercase, strip whitespace)
2. Exact match detection
3. Keep record with most data (prefer non-null linkedin_headline)

**Script:** data_prep.py (create if needed)
**Reference Implementation:** alignment_issues_and_fixes.md (original) lines 514-551

**Usage:**
```bash
python data_prep.py --dedupe reference/guildmember_scrape.csv
# Output: reference/guildmember_scrape_deduped.csv
```

**Add to:** airtable_schema.md Phase 2 setup instructions (before CSV import)
```

---

## 5. Error Handling Specifications

**Problem:**
No specifications for handling timeouts, API limits, or missing data.

**Solution (add to technical spec):**

```markdown
### Error Handling Patterns

**Pattern 1: Deep Research Timeout**
- Timeout: 600 seconds (10 minutes)
- Retry: 2 attempts with exponential backoff
- Fallback: Switch to fast web search mode (gpt-5 + web_search_preview)

**Pattern 2: Insufficient Public Data**
- Detection: research_confidence = "Low"
- Response: Set all dimension scores to None
- Summary: "Candidate has minimal public information. Assessment requires internal data."

**Pattern 3: Airtable Rate Limits**
- Detection: HTTP 429 or "rate limit" in error
- Retry: Exponential backoff (2^attempt seconds)
- Max attempts: 3

**Implementation:** webhook_server.py error handling
**Reference:** alignment_issues_and_fixes.md (original) lines 363-424
```

---

## 6. Implementation Status & Remaining Items

### ✅ Completed (Verified)

1. **data_design.md** - Two-step research pipeline implemented (lines 268-427)
2. **data_design.md** - Added `research_confidence` and `gaps` fields (lines 323-324)
3. **data_design.md** - Cleaned up "Outstanding Questions" section (lines 522-531)
4. **data_design.md** - Added evidence-aware scoring encoding rules (lines 339-341, 434-436)
5. **data_design.md** - Softened Pydantic statement (line 270)
6. **role_spec_design.md** - Fixed 0-5 to 1-5 scale (lines 86-94, 303)
7. **role_spec_design.md** - Added null/None encoding guidance (lines 39, 166-167, 431-436)
8. **airtable_schema.md** - Added research fields (lines 348-349)
9. **airtable_schema.md** - Cross-references to data_design.md (lines 461, 552)
10. **deep_research_findings.md** - Two-step limitation stated (lines 143-144)
11. **deep_research_findings.md** - Table separation clarified (lines 329-359)
12. **airtable_schema.md** - Parser agent note added at top of "JSON Field Schemas" section (lines ~392-399)
13. **deep_research_findings.md** - Inline reference to canonical `ExecutiveResearchResult` schema added in parser agent code (lines ~190-200)
14. **deep_research_findings.md** - Airtable cross-reference added in Research Storage Schema section (lines ~329-359)
15. **technical_spec_V2.md** - Overall score calculation algorithm specified (evidence-aware weighting)
16. **technical_spec_V2.md** - Role spec markdown parser behavior specified (high-level algorithm)
17. **technical_spec_V2.md** - Evidence quote extraction process specified (optional helper)
18. **technical_spec_V2.md** - Error-handling patterns documented (retries, failure marking, non-crashing behavior)
19. **technical_spec_V2.md** - Deduplication strategy for CSV import documented (name + company soft key)

### Remaining Implementation Artifacts

20. **spec_parser.py** - Role spec markdown parser module
21. **assessment.py** - Include `calculate_overall_score()` and optional `extract_evidence_quotes()`
22. **data_prep.py** - Deduplication script for CSV preprocessing (using the documented strategy)
23. **error_handlers.py** - Centralized retry and fallback patterns for API and Airtable errors

---

## 7. Document Map & Cross-References

**Canonical Sources:**
- **Pydantic Schemas:** data_design.md (Structured Output Schemas section)
- **Airtable Implementation:** airtable_schema.md
- **Role Spec System:** role_spec_design.md
- **Research Pipeline:** deep_research_findings.md

**Reference Pattern:**
- When docs reference schemas → point to data_design.md
- When docs reference table fields → point to airtable_schema.md
- When docs reference research behavior → point to deep_research_findings.md

**Technical Spec Cross-Reference (implemented in technical_spec_V2.md):**
```markdown
## Planning Document Map

- **Data Models:** demo_planning/data_design.md
- **Airtable Schema:** demo_planning/airtable_schema.md
- **Role Specs:** demo_planning/role_spec_design.md
- **Research Pipeline:** demo_planning/deep_research_findings.md
- **Alignment Review:** demo_planning/alignment_issues_and_fixes.md
```

---

## 8. Summary of Changes

**✅ Completed Documentation Fixes (19 items):**
1. data_design.md: Two-step research approach
2. data_design.md: Added research_confidence and gaps fields
3. data_design.md: Cleaned up pending questions
4. data_design.md: Clarified evidence-aware scoring encoding
5. data_design.md: Softened Pydantic statement
6. role_spec_design.md: Fixed 0-5 to 1-5 scale
7. role_spec_design.md: Added null/None encoding guidance
8. airtable_schema.md: Added research_confidence and research_gaps fields
9. airtable_schema.md: Cross-references to data_design.md
10. deep_research_findings.md: Two-step limitation stated
11. deep_research_findings.md: Table separation clarified
12. airtable_schema.md: Parser agent note added in JSON Field Schemas section
13. deep_research_findings.md: Inline reference to canonical `ExecutiveResearchResult` schema in parser agent
14. deep_research_findings.md: Airtable cross-reference added in Research Storage Schema
15. technical_spec_V2.md: Overall score calculation algorithm documented
16. technical_spec_V2.md: Role spec parser behavior documented
17. technical_spec_V2.md: Evidence quote extraction described (optional helper)
18. technical_spec_V2.md: Error handling patterns specified
19. technical_spec_V2.md: Deduplication strategy documented

**Implementation Artifacts (4 items):**
20. spec_parser.py module
21. assessment.py (scoring + quote extraction)
22. data_prep.py (deduplication)
23. error_handlers.py (retry/fallback)

---

**Status:** Core documentation alignment complete; remaining work is implementation of helper modules (items 20-23).
**Next Step:** Implement the Python helpers (`spec_parser.py`, `assessment.py`, `data_prep.py`, `error_handlers.py`) according to the documented specs.

**End of Document**
