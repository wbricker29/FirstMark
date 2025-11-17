# Airtable AI Builder Spec — Talent Signal Agent Demo (Excel-backed)

Context: We're building a Talent Signal Agent demo for FirstMark. Airtable is the system of record for executive data, open roles, structured role specs, search projects, screening batches, and the AI-generated research + assessment outputs from Module 4. Flask/ngrok handles webhooks, but all state and audit data must live in Airtable so recruiters can review results inside the base. Airtable AI should generate the schema using the accompanying Excel sample.

Instructions: Upload `case/airtable_base_seed.xlsx` in Airtable AI Builder. Each sheet header represents a table; keep the order and convert fields per notes below. Long-text JSON fields store Pydantic payloads (`ExecutiveResearchResult`, `AssessmentResult`) coming from the Python workflow, so they must stay plain text.

## Table-by-table instructions

1. **People** (sheet `People`): treat `Normalized Function` + `Source` as single-selects using the sample values. Keep `LinkedIn Headline`/`Bio` as long text; `Added Date` is a date.  
2. **Portco**: convert `Stage` and `Sector` to single-selects; `Employee Count` numeric; `Description` long text.  
3. **Portco Roles**: `Portco` links to the Portco table; `Role Type`, `Status`, `Priority` are single-selects; `Created Date` is a date.  
4. **Role Specs**: `Role Type` single-select; `Is Template` checkbox; `Spec Content` long text markdown.  
5. **Searches**: `Role` links to Portco Roles; `Role Spec` links to Role Specs; `Status` single-select; `Notes` long text.  
6. **Screens**: `Screen ID` auto number; `Search` links to Searches; `Candidates` links to People (allow multiple); `Status` single-select; `Custom Instructions` long text; capture created/completed dates.  
7. **Assessments**: `Screen`, `Candidate`, `Role`, `Role Spec` link to their respective tables; `Status` single-select; `Overall Score` numeric (0–100, nullable); `Overall Confidence` single-select; keep all `... JSON` + `Research Markdown Raw` + `Assessment Markdown Report` as plain long text since they store structured payloads; `Runtime Seconds` numeric; `Assessment Timestamp` date/time; `Research Model`/`Assessment Model` plain text.

## Relationship notes

- Portco → Portco Roles (1:M) → Searches (1:1).  
- Screens belong to a Search and list multiple People; each Screen spawns Assessments (one per candidate).  
- Assessments inherit the linked Role Spec but remain editable.  
- Status fields (“Draft/Processing/Complete/Failed”) power automations (e.g., trigger webhook when Screen status changes to “Ready to Screen” and write back “Processing/Complete”).  
- Long-text JSON fields must remain plain text to store `ExecutiveResearchResult` and `AssessmentResult` blobs.
