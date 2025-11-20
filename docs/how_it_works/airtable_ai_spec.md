# Airtable Database Spec: Talent Signal Agent

## Purpose

Track executive candidates and evaluate their fit for portfolio company roles (CFO/CTO positions).

## Tables & Fields

### 1. People

**Table ID:** `tblHqYymo3Av9hLeC`

Stores executive profiles from FirstMark's talent network.

**Fields:**

- Name (Single Line Text) - Executive's full name
- Current Title (Single Line Text) - Job title
- Current Company (multipleRecordLinks → Companies) - Link to company record in Companies table
- LinkedIn URL (Single Line Text) - LinkedIn profile link (stored as text, not URL type)
- LinkedIn Headline (Long Text) - Additional context from LinkedIn
- Normalized Title (Single Select: CFO, CTO) - Normalized executive function (limited options in actual schema)
- Source (Single Select: FMLinkedIN, FMGuildPage) - Source of candidate data (limited options in actual schema)
- Location (Single Line Text) - Geographic location
- Bio (Long Text) - Professional background summary
- Photo (multipleAttachments) - Executive photo (optional)
- Created (Created Time)
- Creator (Created By)
- Edited (Last modified time)
- Editor (Last modified by)

**Note:** Current Company is a linked record field, not a text field. When loading candidates, companies must be created/linked separately. See `Companies` table below.

---

### 2. Companies

**Table ID:** `tblM0zd2qAu9dgDUQ`

General company records (separate from portfolio companies). Used for linking People records to their current companies.

**Fields:**

- Company Name (Single Line Text) - Company name
- Alternative Names (Long Text) - Other names/variations
- Website (URL) - Company website
- Company Type (multipleSelects) - Portfolio Company, Partner, Vendor, Prospect, Other
- Primary Location (Single Line Text) - Main office location
- Related Portcos (multipleRecordLinks → Portcos) - Links to portfolio companies if applicable
- Related People (multipleRecordLinks → People) - People currently at this company
- Created (Created Time)
- Creator (Created By)
- Edited (Last modified time)
- Editor (Last modified by)

---

### 3. Portcos (Portfolio Companies)

**Table ID:** `tblie7yBgF0gZywy4`

Companies in FirstMark's portfolio with active hiring needs.

**Fields:**

- Company Name (Single Line Text) - Portfolio company name
- Stage (Single Select: Series B, Series C) - Funding stage (limited options in actual schema)
- Sector (Single Select: B2B SaaS, Infrastructure) - Industry sector (limited options in actual schema)
- Description (Long Text) - Company overview
- Website (Single Line Text) - Company website (stored as text)
- Primary Location (Single Line Text) - Primary office location
- Investor POC (multipleRecordLinks → Operations-FMC_Roster) - FirstMark team member point of contact
- Portco Roles (multipleRecordLinks → Platform-Portco_Roles) - Open roles at this company
- Companies (multipleRecordLinks → Companies) - Related company records
- Created (Created Time)
- Creator (Created By)
- Edited (Last modified time)
- Editor (Last modified by)

**Note:** Employee Count and HQ Location fields are not present in actual schema. Use Primary Location instead.
---

### 4. Platform-Portco_Roles

**Table ID:** `tblRSTbBg3meBCW1x`

Open executive roles at portfolio companies.

**Fields:**

- Role Name (Formula) - Auto-generated: "{Portco} - {Role Type}"
- Portco (multipleRecordLinks → Portcos) - Link to portfolio company
- Role Type (Single Select) - CFO, CTO, CEO, CPO, CRO, COO, CMO, CDO, CPO (People), Exec_Other, Exec_Finance, Exec_Product, Exec_People, Exec_Tech, Exec_Sales-Revenue, Exec_Operations, Exec_Marketing, Exec_Design
- Status (Single Select: Open, Paused, Filled, Killed)
- Priority (Single Select: Critical, High) - Priority level (limited options in actual schema)
- Description (Long Text) - Role overview
- Searches (multipleRecordLinks → Platform-Searches) - Associated searches
- Search Status (multipleLookupValues) - Status from linked searches
- Assessments (multipleRecordLinks → Platform-Assessments) - Candidate assessments
- Created (Created Time)
- Creator (Created By)
- Edited (Last modified time)
- Editor (Last modified by)

---

### 5. Platform-Role_Specs

**Table ID:** `tblbrV5s0023vzdE0`

Structured evaluation criteria for roles.

**Fields:**

- Spec Name (Formula) - Auto-generated: "{Role Type} - {Variant}"
- Role Type (Single Select) - CFO, CTO, CEO, CPO, CRO, COO, CMO, CDO, CPO (People)
- Variant (Single Select: Series B + Saas, Growth + Infra) - Spec variant/template type
- Is Template (Checkbox) - True for reusable base specs
- Spec Content (Long Text) - Markdown-formatted evaluation criteria
- Created Date (Date) - Creation date
- Modified Date (Date) - Last modification date
- Searches (multipleRecordLinks → Platform-Searches) - Searches using this spec
- Assessments (multipleRecordLinks → Platform-Assessments) - Assessments using this spec
- Created (Created Time)
- Creator (Created By)
- Edited (Last modified time)
- Editor (Last modified by)

---

### 6. Platform-Searches

**Table ID:** `tbl6gHz2gM4pE75ne`

Active executive searches FirstMark is supporting.

**Fields:**

- Search Name (Formula) - Auto-generated: "{Role} Search"
- Role (multipleRecordLinks → Platform-Portco_Roles) - Associated role
- Role Spec (multipleRecordLinks → Platform-Role_Specs) - Evaluation criteria being used
- Role Spec Content (multipleLookupValues) - Lookup of Spec Content from linked Role Spec
- Status (Single Select: Planning, Active, Completed (FMC Assisted), Completed)
- Start Date (Date) - Search start date
- Target Close Date (Date) - Target completion date
- Notes (Long Text) - Search context and updates
- Portcos (multipleLookupValues) - Portfolio companies from linked roles
- Screens (multipleRecordLinks → Platform-Screens) - Screening batches for this search
- ATID Rollup (from Screens) (Rollup) - Aggregated screen IDs
- Created (Created Time)
- Creator (Created By)
- Edited (Last modified time)
- Editor (Last modified by)

---

### 7. Platform-Screens

**Table ID:** `tbl2hrmaTWLEeaywL`

Batch evaluations of candidates for a search.

**Fields:**

- Screen (Formula) - Auto-generated: "{Search} - {Record_#}"
- Screen_Name (Formula) - Auto-generated: "{Search} - {Search_Sequence}"
- Record_# (Auto Number) - Sequential screen number
- Search (multipleRecordLinks → Platform-Searches) - Associated search
- Candidates (multipleRecordLinks → People) - Executives being evaluated
- Candidate Company (Rollup) - Company names from linked candidates
- Candidate Company (text) (Formula) - Text representation of candidate companies
- Status (Single Select: Draft, Pending, Processing, Complete, Failed)
- Current Search Role Spec (multipleLookupValues) - Role Spec from linked search
- Role Spec Content (from Search) (multipleLookupValues) - Spec content from linked search
- Role Spec Selection (Single Select: "Search Spec", "Custom Spec") - How to determine evaluation criteria (default: "Search Spec")
- AI Screen Kickoff (Single Select: "Kickoff AI Assessment", "Block AI Assessment") - Automation control
- Custom Role Spec Content (Rich Text) - Ad-hoc evaluation criteria (only used when mode = "Custom Spec")
- Master Role Spec Content (Formula) - Resolved Spec markdown used for assessment (formula: `IF({Role Spec Selection} != "Custom Spec", {Role Spec Content (from Search)}, {Custom Role Spec Content})`)
- Admin-Automation Spec Content Snapshot (Rich Text) - Immutable snapshot of Master Role spec content captured when screening starts (populated by automation when Status → "Processing")
- Custom Instructions (Rich Text) - Special evaluation criteria
- Start Time (Date & Time) - When screening started
- End Time (Date & Time) - When screening completed
- Assessments (multipleRecordLinks → Platform-Assessments) - Individual candidate assessments
- admin-automation notes (Single Line Text) - Automation tracking notes
- admin-Search_ATIDs (Rollup) - Search record IDs
- Search_Sequence (Formula) - Calculated sequence number within search
- Operations-Automation Log (multipleRecordLinks → Operations-Automation_Log) - Automation event logs
- Error Message (from Operations-Automation Log) (multipleLookupValues) - Error messages from automation logs
- Created (Created Time)
- Creator (Created By)
- Edited (Last modified time)
- Editor (Last modified by)

**Spec Selection Logic:**
- **Search Spec (default):** Uses Role_Specs record linked via Search (stable, reusable)
- **Custom Spec:** Uses inline markdown from Custom Role spec content field (ephemeral, ad-hoc testing)
- **Master Role Spec Content** formula automatically selects the correct source based on mode

**Spec Snapshot Workflow:**
1. User sets up Screen with Spec (via Role Spec Selection dropdown)
2. User sets Status → "Processing" (triggers automation)
3. Airtable automation copies Master Role Spec Content → Admin-Automation Spec Content Snapshot
4. Python code reads Admin-Automation Spec Content Snapshot (immutable)
5. Even if Master Role Spec Content changes later, snapshot remains frozen

**Why Snapshot is Critical:**
- Prevents Spec drift if Custom Role spec content is edited mid-screening
- Prevents Spec drift if linked Role_Specs record is updated mid-screening
- Ensures Assessment audit trail matches exactly what was evaluated
- Creates point-in-time capture for compliance/review

---

### Webhook Automation & Structured Payload

- **Trigger:** `Platform-Screens.Status` → `Processing`
- **Action:** Airtable automation posts to AgentOS `/screen`
- **Headers:** `Content-Type: application/json` (+ `Authorization: Bearer <AGENTOS_SECURITY_KEY>` when configured)
- **Payload:** Matches `demo.models.ScreenWebhookPayload`:
  - `screen_slug`: Screen metadata (record ID, timestamps, custom instructions)
  - `role_spec_slug.role_spec.role_spec_content`: Markdown copied from `Admin-Automation Spec Content Snapshot`
  - `search_slug.role`: Portco, role type/title, description (no further reads needed)
  - `candidate_slugs[]`: Array of candidate dicts (ATID, name, title, company, LinkedIn, location, bio)
- **Processing:** FastAPI endpoint validates the payload and calls `demo.screening_service.process_screen_direct()` with the supplied data
- **Error Handling:** Validation issues raise `ScreenValidationError`, returning 400 responses Airtable can display inline

### Zero-Traversal Airtable Pattern

- Python never performs Airtable reads during screening; all payload data is pre-assembled via Airtable formulas
- `demo/airtable_client.AirtableClient` only writes:
  - Screen status updates (`Pending` → `Processing` → `Complete`/`Failed`)
  - Automation log rows (`Operations-Automation_Log`)
  - Assessment records (Platform-Assessments)
- Spec markdown is stored inside `Assessment JSON` as `role_spec_used`, preserving the snapshot used for scoring
- Automation log rows keep webhook payload JSON for traceability and align with Stage 5 observability requirements

---

### 8. Platform-Assessments

**Table ID:** `tblIhMnOG7Hp9xYna`

Individual Candidate evaluation against role specifications **and** storage for research outputs (per v1 minimal spec).

**Fields:**

**✅ Actively Written by Python (`write_assessment()`):**
- Screen (multipleRecordLinks → Platform-Screens) - Batch run identifier
- Candidate (multipleRecordLinks → People) - Executive evaluated
- Status (Single Select: Pending, In Progress, Complete, Error) - Set to "Complete" on success
- Overall Score (Number) - Composite fit score (0-100, nullable) - Only written if not None
- Overall Confidence (Single Select: High, Medium, Low) - Extracted from `assessment.overall_confidence`
- Topline Summary (Long Text) - 2-3 sentence assessment from `assessment.summary`
- **Assessment JSON (Long Text)** - **PRIMARY DATA STORE**: Full `AssessmentResult` object including dimension_scores, must_haves_check, red_flags_detected, green_flags, counterfactuals, summary, role_spec_used. Produced with Agno `ReasoningTools` enabled.
- Assessment Model (Single Line Text) - Model used for assessment (e.g., "gpt-5-mini")
- Assessment Timestamp (Date & Time) - When assessment completed
- **Research JSON (Long Text)** - **PRIMARY DATA STORE**: Full `ExecutiveResearchResult` object including career_timeline, citations, sector_expertise, stage_exposure, research_summary, gaps (only written if research provided)
- Research Model (Single Line Text) - Model used for research (e.g., "o4-mini-deep-research") (only written if research provided)
- **Research Markdown Report (Long Text)** - Raw Deep Research markdown output with inline citations (conditionally written if `research.research_markdown_raw` exists)
- **Assessment Markdown Report (Long Text)** - Inline markdown summary generated by `render_assessment_markdown_inline()` (conditionally written if `assessment_markdown` parameter provided). Contains candidate snapshot, overall score, summary, dimension snapshot, must-haves, and research signal.
- **Screen Report (Attachment)** - Markdown attachments generated by `render_screen_report()` (assessment) plus a dedicated research report. Both files are uploaded via `AirtableClient.write_assessment(report_files=[...])`. **⚠️ SCHEMA FIELD MISSING**: Code attempts to upload to "Screen Report" field, but this field does not exist in Airtable schema (field "Reports" exists instead). Attachment upload will fail until "Screen Report" attachment field is created in schema.

**📋 Schema Fields (Exist but NOT Written by Python):**
- Assessment ID (Formula) - Auto-generated: "{Role} - {Candidate} - {Screen}"
- Role (Single Line Text) - Role being filled (field exists but not populated by current code)
- Role Spec (multipleRecordLinks → Platform-Role_Specs) - Criteria used (field exists but not populated by current code)
- Dimension Scores JSON (Long Text) - **UNUSED** - Data exists within `Assessment JSON` field
- Must Haves Check JSON (Long Text) - **UNUSED** - Data exists within `Assessment JSON` field
- Red Flags JSON (Long Text) - **UNUSED** - Data exists within `Assessment JSON` field
- Green Flags JSON (Long Text) - **UNUSED** - Data exists within `Assessment JSON` field
- Counterfactuals JSON (Long Text) - **UNUSED** - Data exists within `Assessment JSON` field
- Research Structured JSON (Long Text) - **SCHEMA FIELD NAME MISMATCH** - Actual field written is "Research JSON" (see actively written section above)
- Assessment Markdown Report (Long Text) - **ACTIVELY WRITTEN** - Inline markdown summary generated by `render_assessment_markdown_inline()` and written via `AirtableClient.write_assessment(assessment_markdown=...)`. Contains candidate snapshot, overall score, summary, dimension snapshot, must-haves, and research signal.
- Runtime Seconds (Number) - **UNUSED** - Execution duration not currently tracked
- Error Message (Long Text) - **UNUSED** - Errors logged via Operations-Automation_Log instead
- Operations-Automation Log (multipleRecordLinks → Operations-Automation_Log) - Automation event logs
- Error Message (from Operations-Automation Log) (multipleLookupValues) - Error messages from automation logs (lookup field)
- Created (Created Time)
- Creator (Created By)
- Edited (Last modified time)
- Editor (Last modified by)
- ATID (Formula) - Auto-generated record ID

**Data Architecture Notes:**
- **All assessment data** (dimension scores, must-haves, red flags, green flags, counterfactuals) is stored as a **single JSON blob** in `Assessment JSON` field
- **All research data** (career timeline, citations, sector expertise, etc.) is stored as a **single JSON blob** in `Research JSON` field
- **Raw research markdown** from Deep Research API is stored in `Research Markdown Report` field (conditionally - only if data exists)
- Granular JSON fields (Dimension Scores JSON, Red Flags JSON, etc.) exist in schema for potential future use but are **not currently populated**
- To extract specific data (e.g., individual dimension scores), use Airtable formula fields with `REGEX_EXTRACT()` on the consolidated JSON fields
- Role spec markdown audit trail is stored within `Assessment JSON` as `assessment.role_spec_used`, not in a separate field

---

## Additional Tables

### 9. Operations-Automation_Log

**Table ID:** `tblEueGSDHYR6zNYA`

Table for recording external automated events and webhook activity.

**Fields:**

- Log (Formula) - Auto-generated log identifier
- Action (Single Select) - Candidate Assessment, Ingest People File, Ingest Company File
- Event Type (Single Select) - State Change, Webhook Event, Manual Edit, System Update, Other, Automation Trigger
- Related Table (Single Line Text) - Table name where event occurred
- Related Record ID(s) (Single Line Text) - Record IDs affected
- User Note (Long Text) - Manual notes
- Event Summary (Long Text) - Event description
- Webhook Payload JSON (Long Text) - Full webhook payload (if applicable)
- Error Message (Long Text) - Error details (if applicable)
- File (multipleAttachments) - Related files
- Timestamp (Date & Time) - When event occurred
- Platform-Assessments (multipleRecordLinks) - Related assessments
- Platform-Screens (multipleRecordLinks) - Related screens
- Created (Created Time)
- Creator (Created By)
- Edited (Last modified time)
- Editor (Last modified by)

### 10. Operations-FMC_Roster

**Table ID:** `tbll9VW0m5pbbUEUx`

FirstMark Capital team roster (internal use).

**Fields:**

- Name (Single Line Text) - Team member name
- Current Title (Single Line Text) - Job title
- Email (Email) - Contact email
- LinkedIn URL (Single Line Text) - LinkedIn profile
- Team (Single Select) - Investment, Operations, Finance, Platform, Legal
- Bio (Long Text) - Team member bio
- Photo (multipleAttachments) - Team member photo
- Portcos (multipleRecordLinks → Portcos) - Portfolio companies they work with
- Created (Created Time)
- Creator (Created By)
- Edited (Last modified time)
- Editor (Last modified by)

---

## Key Relationships

- **People** → **Companies** (Many:Many via Current Company link) - People linked to their current companies
- **People** → **Platform-Assessments** (1:Many) - One exec evaluated for multiple roles/screens
- **Companies** → **Portcos** (Many:Many) - Companies can be linked to portfolio companies
- **Portcos** → **Platform-Portco_Roles** (1:Many) - Companies have multiple open roles
- **Platform-Portco_Roles** → **Platform-Searches** (1:Many) - Each role can have multiple searches
- **Platform-Searches** → **Platform-Screens** (1:Many) - Multiple evaluation batches per search
- **Platform-Screens** → **Platform-Assessments** (1:Many) - Each screen spawns assessments for its candidates
- **Platform-Role_Specs** → **Platform-Searches/Platform-Assessments** (1:Many) - Specs reused across searches and linked on each assessment

---

## Notes

- **Table Naming:** All Platform tables use "Platform-" prefix (e.g., `Platform-Screens`, not `Screens`)
- **Field Types:** Many fields are formulas, lookups, or rollups rather than direct user input. Check field types before writing.
- **Current Company Field:** People.Current Company is a linked record field (multipleRecordLinks → Companies), not a text field. When loading candidates, companies must be created/linked separately.
- **LinkedIn URL:** Stored as Single Line Text (not URL type) but functions identically.
- **Long Text fields storing JSON:** Contain structured data for complex objects (dimension scores, citations, career timelines)
- **All research + assessment data:** Lives on Platform-Assessments (no Workflows/Research_Results tables in v1). Use Airtable status fields + Agno `SqliteDb` session history for audit trails.
- **Role Specs:** Support both templates (reusable) and customized versions (role-specific)
- **Assessment agent:** Must run with Agno `ReasoningTools` enabled to capture explicit reasoning traces inside `assessment_json`.
- **Role Spec Audit Trail:** Role spec markdown used for each assessment is stored in `Assessment JSON` field as `assessment.role_spec_used`, not in a separate field.
