# Airtable Database Spec: Talent Signal Agent

## Purpose
Track executive candidates and evaluate their fit for portfolio company roles (CFO/CTO positions).

## Tables & Fields

### 1. People
Stores executive profiles from FirstMark's talent network.

**Fields:**
- Name (Single Line Text) - Executive's full name
- Current Title (Single Line Text) - Job title
- Current Company (Single Line Text) - Company name
- LinkedIn URL (URL) - LinkedIn profile link
- LinkedIn Headline (Long Text) - Additional context from LinkedIn
- Normalized Function (Single Select: CEO, CFO, CTO, CPO, CRO, COO, CMO, Other)
- Source (Single Select: FMLinkedIN, FMGuildPage, FMCFO, FMCTOSummit, FMFounder, FMProduct)
- Location (Single Line Text) - Geographic location
- Bio (Long Text) - Professional background summary
- Added Date (Date) - When record was created

---

### 2. Portco (Portfolio Companies)
Companies in FirstMark's portfolio with active hiring needs.

**Fields:**
- Company Name (Single Line Text) - Portfolio company name
- Stage (Single Select: Seed, Series A, Series B, Series C, Growth, Public)
- Sector (Single Select: B2B SaaS, Consumer, AI/ML, Infrastructure, FinTech, HealthTech, Other)
- Description (Long Text) - Company overview
- Website (URL) - Company website
- Employee Count (Number) - Approximate team size
- HQ Location (Single Line Text) - Primary office location

---

### 3. Portco_Roles
Open executive roles at portfolio companies.

**Fields:**
- Role Name (Single Line Text) - e.g., "CFO - Pigment"
- Portco (Link to Portco) - Link to company
- Role Type (Single Select: CFO, CTO, CPO, CRO, COO)
- Status (Single Select: Open, On Hold, Filled, Cancelled)
- Description (Long Text) - Role overview
- Priority (Single Select: Critical, High, Medium, Low)
- Created Date (Date)

---

### 4. Role_Specs
Structured evaluation criteria for roles.

**Fields:**
- Spec Name (Single Line Text) - e.g., "CFO - Series B SaaS"
- Role Type (Single Select: CFO, CTO)
- Is Template (Checkbox) - True for reusable base specs
- Spec Content (Long Text) - Markdown-formatted evaluation criteria
- Created Date (Date)
- Modified Date (Date)

---

### 5. Searches
Active executive searches FirstMark is supporting.

**Fields:**
- Search Name (Single Line Text) - Descriptive name
- Role (Link to Portco_Roles) - Associated role
- Role Spec (Link to Role_Specs) - Evaluation criteria being used
- Status (Single Select: Planning, Active, Paused, Completed)
- Start Date (Date)
- Target Close Date (Date)
- Notes (Long Text) - Search context and updates

---

### 6. Screens
Batch evaluations of candidates for a search.

**Fields:**
- Screen ID (Auto Number)
- Search (Link to Searches) - Associated search
- Candidates (Link to People - Multiple) - Executives being evaluated
- Status (Single Select: Draft, Processing, Complete, Failed)
- Custom Instructions (Long Text) - Special evaluation criteria
- Created Date (Date)
- Completed Date (Date)

---

### 7. Research_Results
Structured research findings for each candidate.

**Fields:**
- Research ID (Auto Number)
- Workflow (Link to Workflows) - Execution record
- Candidate (Link to People) - Executive researched
- Research Summary (Long Text) - 2-3 paragraph overview
- Research JSON (Long Text) - Full structured data (career timeline, achievements, expertise areas)
- Citations (Long Text) - Source URLs and snippets as JSON
- Research Confidence (Single Select: High, Medium, Low)
- Research Gaps (Long Text) - What information was missing
- Research Timestamp (Date & Time)
- Research Model (Single Line Text) - AI model used

---

### 8. Assessments
Candidate evaluations against role specifications.

**Fields:**
- Assessment ID (Auto Number)
- Workflow (Link to Workflows) - Execution record
- Candidate (Link to People) - Executive evaluated
- Role (Link to Portco_Roles) - Role being filled
- Role Spec (Link to Role_Specs) - Criteria used
- Overall Score (Number, 0-100) - Composite fit score
- Overall Confidence (Single Select: High, Medium, Low)
- Dimension Scores JSON (Long Text) - Detailed scores per evaluation dimension (1-5 scale)
- Must Haves Check JSON (Long Text) - Required qualifications verification
- Red Flags (Long Text) - Concerns identified
- Green Flags (Long Text) - Strong positives
- Summary (Long Text) - 2-3 sentence assessment
- Counterfactuals (Long Text) - Key assumptions that could change recommendation
- Assessment Timestamp (Date & Time)
- Assessment Model (Single Line Text) - AI model used

---

### 9. Workflows
Audit trail for all AI operations.

**Fields:**
- Workflow ID (Auto Number)
- Screen (Link to Screens) - Associated batch evaluation
- Operation Type (Single Select: Research, Assessment, Report Generation)
- Status (Single Select: Queued, Running, Complete, Failed)
- Execution Log (Long Text) - Technical logs
- Error Message (Long Text) - Failure details if applicable
- Started At (Date & Time)
- Completed At (Date & Time)
- Duration Seconds (Number)

---

## Key Relationships

- **People** → **Research_Results** (1:Many) - One exec can have multiple research runs
- **People** → **Assessments** (1:Many) - One exec evaluated for multiple roles
- **Portco** → **Portco_Roles** (1:Many) - Companies have multiple open roles
- **Portco_Roles** → **Searches** (1:1) - Each role has one active search
- **Searches** → **Screens** (1:Many) - Multiple evaluation batches per search
- **Screens** → **Workflows** (1:Many) - Each screen spawns multiple operations
- **Role_Specs** → **Searches** (1:Many) - Specs are reused across searches

---

## Notes

- Long Text fields storing JSON contain structured data for complex objects (dimension scores, citations, career timelines)
- Workflows table provides complete audit trail for all AI operations
- Role_Specs support both templates (reusable) and customized versions (role-specific)
- Research and Assessment tables separate data collection from evaluation
