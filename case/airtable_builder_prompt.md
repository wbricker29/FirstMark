# Airtable AI Builder Spec — Talent Signal Agent Demo

Goal: single Airtable base that stores executives, portfolio roles/specs, active searches, screen runs, and AI-generated research + assessments for Module 4.

## Tables (in order)

1. **People** – executive directory  
   `Name` (text); `Current Title` (text); `Current Company` (text); `LinkedIn URL` (URL); `LinkedIn Headline` (long text); `Normalized Function` (single select: CEO, CFO, CTO, CPO, CRO, COO, CMO, Other); `Source` (single select: FMLinkedIN, FMGuildPage, FMCFO, FMCTOSummit, FMFounder, FMProduct); `Location` (text); `Bio` (long text); `Added Date` (date).

2. **Portco** – portfolio companies  
   `Company Name` (text); `Stage` (single select: Seed, Series A, Series B, Series C, Growth, Public); `Sector` (single select: B2B SaaS, Consumer, AI/ML, Infrastructure, FinTech, HealthTech, Other); `Description` (long text); `Website` (URL); `Employee Count` (number); `HQ Location` (text).

3. **Portco Roles** – open exec roles  
   `Role Name` (text); `Portco` (link to Portco, single); `Role Type` (single select: CFO, CTO, CPO, CRO, COO); `Status` (single select: Open, On Hold, Filled, Cancelled); `Description` (long text); `Priority` (single select: Critical, High, Medium, Low); `Created Date` (date).

4. **Role Specs** – evaluation rubrics  
   `Spec Name` (text); `Role Type` (single select: CFO, CTO); `Is Template` (checkbox); `Spec Content` (long text markdown with weighted dimensions + must-haves); `Created Date` (date); `Modified Date` (date).

5. **Searches** – active search projects  
   `Search Name` (text); `Role` (link to Portco Roles, single); `Role Spec` (link to Role Specs); `Status` (single select: Planning, Active, Paused, Completed); `Start Date` (date); `Target Close Date` (date); `Notes` (long text).

6. **Screens** – batch screening runs  
   `Screen ID` (auto number); `Search` (link to Searches); `Candidates` (link to People, allow multiple); `Status` (single select: Draft, Processing, Complete, Failed); `Custom Instructions` (long text); `Created Date` (date); `Completed Date` (date).

7. **Assessments** – per-candidate research + eval results  
   `Assessment ID` (auto number); `Screen` (link to Screens); `Candidate` (link to People); `Role` (link to Portco Roles); `Role Spec` (link to Role Specs); `Status` (single select: Pending, Processing, Complete, Failed); `Overall Score` (number 0–100, blanks allowed); `Overall Confidence` (single select: High, Medium, Low); `Topline Summary` (long text); `Dimension Scores JSON` (long text, stores list of 1–5 scores + evidence); `Must Haves Check JSON` (long text); `Red Flags JSON` (long text); `Green Flags JSON` (long text); `Counterfactuals JSON` (long text); `Research Structured JSON` (long text, full ExecutiveResearchResult); `Research Markdown Raw` (long text); `Assessment JSON` (long text, full AssessmentResult); `Assessment Markdown Report` (long text); `Runtime Seconds` (number); `Error Message` (long text); `Assessment Timestamp` (date/time); `Research Model` (text); `Assessment Model` (text).

## Relationship notes

- Portco → Portco Roles (1:M) → Searches (1:1).  
- Screens link to a Search and include many People; each Screen produces multiple Assessments (one per linked candidate).  
- Assessments inherit the Role Spec from the Search but remain editable.  
- Status fields drive automations (e.g., Screen status “Ready to Screen” triggers webhook; update to “Processing/Complete” when results return).  
- Long-text JSON fields must stay plain text to store structured payloads from the Pydantic models.
