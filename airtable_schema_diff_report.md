# Airtable Schema Differences Report
**Date:** 2025-11-17 (Updated)
**Base:** FMC Talent Demo (appeY64iIwU5CEna7)
**Comparison:** Actual Airtable vs spec/dev_reference/airtable_ai_spec.md
**Schema Retrieved:** 2025-11-17 via MCP Airtable tools

---

## TABLE STRUCTURE OVERVIEW

| Spec Table Name | Actual Table Name | Status | Table ID |
|----------------|-------------------|--------|----------|
| People | People | ✅ Matches | tblHqYymo3Av9hLeC |
| Portco | Portcos | ✅ Matches | tblie7yBgF0gZywy4 |
| Portco_Roles | Platform-Open_Roles | ⚠️ Renamed | tblRSTbBg3meBCW1x |
| Role_Specs | Platform-Role_Specs | ⚠️ Renamed | tblbrV5s0023vzdE0 |
| Searches | Platform-Searches | ⚠️ Renamed | tbl6gHz2gM4pE75ne |
| Screens | Platform-Screens | ⚠️ Renamed | tbl2hrmaTWLEeaywL |
| Assessments | Platform-Assessments | ⚠️ Renamed | tblIhMnOG7Hp9xYna |
| N/A | Companies | ➕ New | tblM0zd2qAu9dgDUQ |
| N/A | Operations-Automation Log | ➕ New | tblEueGSDHYR6zNYA |
| N/A | Operations-FMC_Roster | ➕ New | tbll9VW0m5pbbUEUx |
| N/A | ⚙️ Base Schema | ➕ New | tbluD1y5x2TACM5yB |

---

## 1. PEOPLE TABLE

### Field Comparison

| Spec Field | Actual Field | Status | Notes |
|------------|--------------|--------|-------|
| Name (Single Line Text) | Name (singleLineText) | ✅ Match | |
| Current Title (Single Line Text) | Current Title (singleLineText) | ✅ Match | |
| **Current Company (Single Line Text)** | **MISSING** | ❌ Missing | Replaced with Companies relationship |
| LinkedIn URL (URL) | LinkedIn URL (singleLineText) | ⚠️ Type Change | url → singleLineText |
| LinkedIn Headline (Long Text) | LinkedIn Headline (multilineText) | ✅ Match | |
| **Normalized Function (Single Select)** | **Normalized Title (singleSelect)** | ⚠️ Renamed | Field renamed |
| Source (Single Select) | Source (singleSelect) | ⚠️ Options Reduced | See options below |
| Location (Single Line Text) | Location (singleLineText) | ✅ Match | |
| Bio (Long Text) | Bio (multilineText) | ✅ Match | |
| Created (Created Time) | Created (createdTime) | ✅ Match | |
| Creator (Created By) | Creator (createdBy) | ✅ Match | |
| Edited (Last modified time) | Edited (lastModifiedTime) | ✅ Match | |
| Editor (Last modified by) | Editor (lastModifiedBy) | ✅ Match | |
| N/A | **Companies (multipleRecordLinks)** | ➕ New | Links to Companies table |
| N/A | **Photo (multipleAttachments)** | ➕ New | |
| N/A | **Roles (Portco Roles) (multipleLookupValues)** | ➕ New | Lookup field |
| N/A | **Assessments (multipleRecordLinks)** | ➕ New | Relationship field |
| N/A | **Screens (multipleRecordLinks)** | ➕ New | Relationship field |
| N/A | **ATID (formula)** | ➕ New | RECORD_ID() |

### Single-Select Option Differences

**Normalized Function → Normalized Title:**
| Spec Options | Actual Options | Status |
|--------------|----------------|--------|
| CEO | MISSING | ❌ |
| CFO | CFO (Chief Financial Officer) | ✅ (expanded label) |
| CTO | CTO (Chief Technology Officer) | ✅ (expanded label) |
| CPO | MISSING | ❌ |
| CRO | MISSING | ❌ |
| COO | MISSING | ❌ |
| CMO | MISSING | ❌ |
| Other | MISSING | ❌ |

**Source:**
| Spec Options | Actual Options | Status |
|--------------|----------------|--------|
| FMLinkedIN | FMLinkedIN | ✅ |
| FMGuildPage | FMGuildPage | ✅ |
| FMCFO | MISSING | ❌ |
| FMCTOSummit | MISSING | ❌ |
| FMFounder | MISSING | ❌ |
| FMProduct | MISSING | ❌ |

### Impact Summary
- **Breaking Changes:** 2 (Current Company removed, Normalized Function renamed)
- **Option Reductions:** 2 fields (6 missing function options, 4 missing source options)
- **New Features:** 5 fields added
- **Type Changes:** 1 (LinkedIn URL)

---

## 2. PORTCOS TABLE

### Field Comparison

| Spec Field | Actual Field | Status | Notes |
|------------|--------------|--------|-------|
| Company Name (Single Line Text) | Company Name (singleLineText) | ✅ Match | |
| Stage (Single Select) | Stage (singleSelect) | ⚠️ Options Reduced | See options below |
| Sector (Single Select) | Sector (singleSelect) | ⚠️ Options Reduced | See options below |
| Description (Long Text) | Description (multilineText) | ✅ Match | |
| Website (URL) | Website (singleLineText) | ⚠️ Type Change | url → singleLineText |
| **Employee Count (Number)** | **MISSING** | ❌ Missing | |
| **HQ Location (Single Line Text)** | **Primary Location (singleLineText)** | ⚠️ Renamed | Semantic match |
| Created (Created Time) | Created (createdTime) | ✅ Match | |
| Creator (Created By) | Creator (createdBy) | ✅ Match | |
| Edited (Last modified time) | Edited (lastModifiedTime) | ✅ Match | |
| Editor (Last modified by) | Editor (lastModifiedBy) | ✅ Match | |
| N/A | **Investor POC (multipleRecordLinks)** | ➕ New | Links to Operations-FMC_Roster |
| N/A | **Portco Roles (multipleRecordLinks)** | ➕ New | Relationship field |
| N/A | **Companies (multipleRecordLinks)** | ➕ New | Links to Companies table |
| N/A | **ATID (formula)** | ➕ New | RECORD_ID() |

### Single-Select Option Differences

**Stage:**
| Spec Options | Actual Options | Status |
|--------------|----------------|--------|
| Seed | MISSING | ❌ |
| Series A | MISSING | ❌ |
| Series B | Series B | ✅ |
| Series C | Series C | ✅ |
| Growth | MISSING | ❌ |
| Public | MISSING | ❌ |

**Sector:**
| Spec Options | Actual Options | Status |
|--------------|----------------|--------|
| B2B SaaS | B2B SaaS | ✅ |
| Consumer | MISSING | ❌ |
| AI/ML | MISSING | ❌ |
| Infrastructure | Infrastructure | ✅ |
| FinTech | MISSING | ❌ |
| HealthTech | MISSING | ❌ |
| Other | MISSING | ❌ |

### Impact Summary
- **Breaking Changes:** 2 (Employee Count removed, HQ Location renamed)
- **Option Reductions:** 2 fields (4 missing stage options, 5 missing sector options)
- **New Features:** 4 fields added
- **Type Changes:** 1 (Website)

---

## 3. PLATFORM-OPEN_ROLES (Portco_Roles)

### Field Comparison

| Spec Field | Actual Field | Status | Notes |
|------------|--------------|--------|-------|
| Role Name (Single Line Text) | Role Name (formula) | ⚠️ Type Change | Manual → Computed (Portco & Role Type) |
| Portco (Link to Portco) | Portco (multipleRecordLinks) | ✅ Match | prefersSingleRecordLink: true |
| Role Type (Single Select) | Role Type (singleSelect) | ⚠️ Options Expanded | See options below |
| Status (Single Select) | Status (singleSelect) | ⚠️ Options Reduced | See options below |
| Description (Long Text) | Description (multilineText) | ✅ Match | |
| Priority (Single Select) | Priority (singleSelect) | ⚠️ Options Reduced | See options below |
| Created (Created Time) | Created (createdTime) | ✅ Match | |
| Creator (Created By) | Creator (createdBy) | ✅ Match | |
| Edited (Last modified time) | Edited (lastModifiedTime) | ✅ Match | |
| Editor (Last modified by) | Editor (lastModifiedBy) | ✅ Match | |
| N/A | **Searches (multipleRecordLinks)** | ➕ New | Relationship field |
| N/A | **Assessments (multipleRecordLinks)** | ➕ New | Relationship field |
| N/A | **ATID (formula)** | ➕ New | RECORD_ID() |

### Single-Select Option Differences

**Role Type:**
| Spec Options | Actual Options | Status |
|--------------|----------------|--------|
| CFO | CFO (Chief Financial Officer) | ✅ (expanded label) |
| CTO | CTO (Chief Technical Officer) | ✅ (expanded label) |
| CPO | CPO (Chief Product Officer) | ✅ (expanded label) |
| CRO | CRO (Chief Revenue Officer) | ✅ (expanded label) |
| COO | COO (Chief Operating Officer) | ✅ (expanded label) |
| N/A | CEO (Chief Executive Officer) | ➕ New |
| N/A | CMO (Chief Marketing Officer) | ➕ New |
| N/A | CDO (Chief Design Officer) | ➕ New |
| N/A | CPO (Chief People Officer) | ➕ New |
| N/A | Exec_Other | ➕ New |
| N/A | Exec_Finance | ➕ New |
| N/A | Exec_Product | ➕ New |
| N/A | Exec_People | ➕ New |
| N/A | Exec_Tech | ➕ New |
| N/A | Exec_Sales-Revenue | ➕ New |
| N/A | Exec_Operations | ➕ New |
| N/A | Exec_Marketing | ➕ New |
| N/A | Exec_Design | ➕ New |

**Status:**
| Spec Options | Actual Options | Status |
|--------------|----------------|--------|
| Open | Open | ✅ |
| On Hold | MISSING | ❌ |
| Filled | MISSING | ❌ |
| Cancelled | MISSING | ❌ |

**Priority:**
| Spec Options | Actual Options | Status |
|--------------|----------------|--------|
| Critical | Critical | ✅ |
| High | High | ✅ |
| Medium | MISSING | ❌ |
| Low | MISSING | ❌ |

### Impact Summary
- **Breaking Changes:** 1 (Role Name now computed)
- **Option Expansions:** 1 field (13+ new role type options)
- **Option Reductions:** 2 fields (3 missing status options, 2 missing priority options)
- **New Features:** 3 fields added

---

## 4. PLATFORM-ROLE_SPECS (Role_Specs)

### Field Comparison

| Spec Field | Actual Field | Status | Notes |
|------------|--------------|--------|-------|
| Spec Name (Single Line Text) | Spec Name (formula) | ⚠️ Type Change | Manual → Computed (Role Type & Variant) |
| Role Type (Single Select) | Role Type (singleSelect) | ✅ Match | CFO, CTO |
| Is Template (Checkbox) | Is Template (checkbox) | ✅ Match | |
| Spec Content (Long Text) | Spec Content (multilineText) | ✅ Match | |
| Created (Created Time) | Created (createdTime) | ✅ Match | |
| Creator (Created By) | Creator (createdBy) | ✅ Match | |
| Edited (Last modified time) | Edited (lastModifiedTime) | ✅ Match | |
| Editor (Last modified by) | Editor (lastModifiedBy) | ✅ Match | |
| N/A | **Variant (singleSelect)** | ➕ New | "Series B + Saas", "Growth + Infra" |
| N/A | **Created Date (date)** | ➕ New | Manual date field |
| N/A | **Modified Date (date)** | ➕ New | Manual date field |
| N/A | **Searches (multipleRecordLinks)** | ➕ New | Relationship field |
| N/A | **Assessments (multipleRecordLinks)** | ➕ New | Relationship field |
| N/A | **ATID (formula)** | ➕ New | RECORD_ID() |

### Single-Select Option Differences

**Role Type:**
| Spec Options | Actual Options | Status |
|--------------|----------------|--------|
| CFO | CFO (Chief Financial Officer) | ✅ (expanded label) |
| CTO | CTO (Chief Technology Officer) | ✅ (expanded label) |

**Variant (New Field):**
| Options | Notes |
|---------|-------|
| Series B + Saas | New categorization |
| Growth + Infra | New categorization |

### Impact Summary
- **Breaking Changes:** 1 (Spec Name now computed)
- **New Features:** 6 fields added
- **Option Changes:** None (Role Type matches)

---

## 5. PLATFORM-SEARCHES (Searches)

### Field Comparison

| Spec Field | Actual Field | Status | Notes |
|------------|--------------|--------|-------|
| Search Name (Single Line Text) | Search Name (formula) | ⚠️ Type Change | Manual → Computed (Role & " Search") |
| Role (Link to Portco_Roles) | Role (multipleRecordLinks) | ✅ Match | prefersSingleRecordLink: true |
| Role Spec (Link to Role_Specs) | Role Spec (multipleRecordLinks) | ✅ Match | prefersSingleRecordLink: true |
| Status (Single Select) | Status (singleSelect) | ⚠️ Options Reduced | See options below |
| Start Date (Date) | Start Date (date) | ✅ Match | |
| Target Close Date (Date) | Target Close Date (date) | ✅ Match | |
| Notes (Long Text) | Notes (multilineText) | ✅ Match | |
| Created (Created Time) | Created (createdTime) | ✅ Match | |
| Creator (Created By) | Creator (createdBy) | ✅ Match | |
| Edited (Last modified time) | Edited (lastModifiedTime) | ✅ Match | |
| Editor (Last modified by) | Editor (lastModifiedBy) | ✅ Match | |
| N/A | **ATID Rollup (from Screens) (rollup)** | ➕ New | |
| N/A | **Portcos (multipleLookupValues)** | ➕ New | Lookup field |
| N/A | **Screens (multipleRecordLinks)** | ➕ New | Relationship field |
| N/A | **ATID (formula)** | ➕ New | RECORD_ID() |

### Single-Select Option Differences

**Status:**
| Spec Options | Actual Options | Status |
|--------------|----------------|--------|
| Planning | Planning | ✅ |
| Active | Active | ✅ |
| Paused | MISSING | ❌ |
| Completed | MISSING | ❌ |

### Impact Summary
- **Breaking Changes:** 1 (Search Name now computed)
- **Option Reductions:** 1 field (2 missing status options)
- **New Features:** 4 fields added

---

## 6. PLATFORM-SCREENS (Screens)

### Field Comparison

| Spec Field | Actual Field | Status | Notes |
|------------|--------------|--------|-------|
| Screen ID (Auto Number) | Record_# (autoNumber) | ✅ Match | Semantic match |
| Search (Link to Searches) | Search (multipleRecordLinks) | ✅ Match | prefersSingleRecordLink: true |
| Candidates (Link to People - Multiple) | Candidates (multipleRecordLinks) | ✅ Match | |
| Status (Single Select) | Status (singleSelect) | ⚠️ Options Reduced | See options below |
| Custom Instructions (Long Text) | Custom Instructions (multilineText) | ✅ Match | |
| Start Time (Date time) | Start Time (dateTime) | ✅ Match | |
| **completion time (Date time)** | **End Time (dateTime)** | ⚠️ Renamed | Semantic match |
| **Created Date (Date)** | **MISSING** | ❌ Missing | Only Created (timestamp) exists |
| Created (Created Time) | Created (createdTime) | ✅ Match | |
| Creator (Created By) | Creator (createdBy) | ✅ Match | |
| Edited (Last modified time) | Edited (lastModifiedTime) | ✅ Match | |
| Editor (Last modified by) | Editor (lastModifiedBy) | ✅ Match | |
| N/A | **Screen (formula)** | ➕ New | Computed identifier |
| N/A | **Role Spec (multipleLookupValues)** | ➕ New | Lookup field |
| N/A | **Assessments (multipleRecordLinks)** | ➕ New | Relationship field |
| N/A | **admin-Search_ATIDs (rollup)** | ➕ New | |
| N/A | **Screen_Name (formula)** | ➕ New | |
| N/A | **Search_Sequence (formula)** | ➕ New | |
| N/A | **Operations-Automation Log (multipleRecordLinks)** | ➕ New | |
| N/A | **Error Message (from Operations-Automation Log) (multipleLookupValues)** | ➕ New | |
| N/A | **ATID (formula)** | ➕ New | RECORD_ID() |

### Single-Select Option Differences

**Status:**
| Spec Options | Actual Options | Status |
|--------------|----------------|--------|
| Draft | MISSING | ❌ |
| Processing | Processing | ✅ |
| Complete | Complete | ✅ |
| Failed | MISSING | ❌ |

### Impact Summary
- **Breaking Changes:** 2 (Created Date removed, completion time renamed)
- **Option Reductions:** 1 field (2 missing status options)
- **New Features:** 9 fields added (including automation integration)

---

## 7. PLATFORM-ASSESSMENTS (Assessments)

### Field Comparison

| Spec Field | Actual Field | Status | Notes |
|------------|--------------|--------|-------|
| Assessment ID (Auto Number) | Assessment ID (formula) | ⚠️ Type Change | Auto → Computed (Role-Candidate-Screen) |
| Screen (Link to Screens) | Screen (multipleRecordLinks) | ✅ Match | prefersSingleRecordLink: true |
| Candidate (Link to People) | Candidate (multipleRecordLinks) | ✅ Match | prefersSingleRecordLink: true |
| Role (Link to Portco_Roles) | Role (multipleRecordLinks) | ✅ Match | prefersSingleRecordLink: true |
| Role Spec (Link to Role_Specs) | Role Spec (multipleRecordLinks) | ✅ Match | prefersSingleRecordLink: true |
| Status (Single Select) | Status (singleSelect) | ⚠️ Options Modified | See options below |
| Overall Score (Number, 0-100) | Overall Score (number) | ✅ Match | |
| Overall Confidence (Single Select) | Overall Confidence (singleSelect) | ✅ Match | High, Medium, Low |
| Topline Summary (Long Text) | Topline Summary (multilineText) | ✅ Match | |
| Dimension Scores JSON (Long Text) | Dimension Scores JSON (multilineText) | ✅ Match | |
| Must Haves Check JSON (Long Text) | Must Haves Check JSON (multilineText) | ✅ Match | |
| Red Flags JSON (Long Text) | Red Flags JSON (multilineText) | ✅ Match | |
| Green Flags JSON (Long Text) | Green Flags JSON (multilineText) | ✅ Match | |
| Counterfactuals JSON (Long Text) | Counterfactuals JSON (multilineText) | ✅ Match | |
| Research Structured JSON (Long Text) | Research Structured JSON (multilineText) | ✅ Match | |
| Research Markdown Raw (Long Text) | Research Markdown Raw (multilineText) | ✅ Match | |
| Assessment JSON (Long Text) | Assessment JSON (multilineText) | ✅ Match | |
| Assessment Markdown Report (Long Text) | Assessment Markdown Report (multilineText) | ✅ Match | |
| Runtime Seconds (Number) | Runtime Seconds (number) | ✅ Match | |
| Error Message (Long Text) | Error Message (multilineText) | ✅ Match | |
| Assessment Timestamp (Date & Time) | Assessment Timestamp (date) | ⚠️ Type Change | dateTime → date (lost time) |
| Research Model (Single Line Text) | Research Model (singleLineText) | ✅ Match | |
| Assessment Model (Single Line Text) | Assessment Model (singleLineText) | ✅ Match | |
| **Created Date (Date)** | **MISSING** | ❌ Missing | Only Created (timestamp) exists |
| Created (Created Time) | Created (createdTime) | ✅ Match | |
| Creator (Created By) | Creator (createdBy) | ✅ Match | |
| Edited (Last modified time) | Edited (lastModifiedTime) | ✅ Match | |
| Editor (Last modified by) | Editor (lastModifiedBy) | ✅ Match | |
| N/A | **Operations-Automation Log (multipleRecordLinks)** | ➕ New | |
| N/A | **Error Message (from Operations-Automation Log) (multipleLookupValues)** | ➕ New | |
| N/A | **ATID (formula)** | ➕ New | RECORD_ID() |

### Single-Select Option Differences

**Status:**
| Spec Options | Actual Options | Status | Notes |
|--------------|----------------|--------|-------|
| Pending | Pending | ✅ | |
| **Processing** | **In Progress** | ⚠️ Renamed | Label change |
| Complete | Complete | ✅ | |
| **Failed** | **Error** | ⚠️ Renamed | Label change |

**Overall Confidence:**
| Spec Options | Actual Options | Status |
|--------------|----------------|--------|
| High | High | ✅ |
| Medium | Medium | ✅ |
| Low | Low | ✅ |

### Impact Summary
- **Breaking Changes:** 3 (Assessment ID now computed, Created Date removed, Assessment Timestamp lost time precision)
- **Option Renames:** 2 (Processing → In Progress, Failed → Error)
- **New Features:** 3 fields added (automation integration)
- **Type Changes:** 1 (Assessment Timestamp)
- **All JSON fields:** ✅ Present and correct

---

## 8. ADDITIONAL TABLES (Not in Spec)

### Companies Table
**Purpose:** General company directory (separate from Portcos)
**Key Fields:**
- Company Name
- Alternative Names
- Website (url type - NOTE: different from Portcos.Website which is singleLineText)
- Company Type (Portfolio Company, Partner, Vendor, Prospect, Other)
- Primary Location
- Related Portcos (link)
- Related People (link)
- ATID (formula)

**Usage:** Referenced by People.Companies and Portcos.Companies

**Note:** This table uses proper `url` field type for Website, while Portcos table uses `singleLineText` for the same field.

---

### Operations-Automation Log
**Purpose:** Webhook events & automation history tracking
**Key Fields:**
- Entity Record
- Event Type (State Change, Webhook Event, Manual Edit, System Update, Other)
- Entity Type (People, Portcos, Portco Roles, Role Specs, Searches, Screens, Assessments)
- Related Table
- Event Summary
- Related Record ID(s)
- Webhook Payload JSON
- File
- Error Message
- Timestamp

**Usage:** Referenced by Platform-Screens and Platform-Assessments for error tracking

---

### Operations-FMC_Roster
**Purpose:** FirstMark Capital team roster
**Key Fields:**
- Name
- Current Title
- Email
- LinkedIn URL
- Team (Investment, Operations, Finance, Platform, Legal)
- Bio
- Photo

**Usage:** Referenced by Portcos.Investor POC

---

### ⚙️ Base Schema
**Purpose:** Metadata table for tracking the base schema structure itself
**Key Fields:**
- Field Name
- Field ID
- Field Type (40+ Airtable field types)
- Field Description
- Table Name (links to all tables in base)
- Table ID
- Is Primary Field?
- Field Options
- Field Contents
- Computed Using (Table/Field)
- Used to Compute
- Blank Records Count/Percentage

**Usage:** Internal schema documentation and analysis table (not part of application workflow)

---

## CROSS-CUTTING PATTERNS

### Consistent Changes Across All 7 Core Tables

| Pattern | Tables Affected | Impact |
|---------|----------------|--------|
| ATID field added (formula: RECORD_ID()) | All 7 tables | ➕ New feature |
| "Platform-" prefix on table names | 5 tables (not People, Portcos) | ⚠️ Naming convention |
| Computed identifiers (formula vs manual) | 4 tables (Roles, Specs, Searches, Assessments) | ⚠️ Breaking |
| URL fields → singleLineText | People, Portcos | ⚠️ Type change |
| Reduced single-select options | 6 tables | ⚠️ Limited scope |
| Operations-Automation Log integration | Screens, Assessments | ➕ New feature |

---

## IMPACT SUMMARY BY SEVERITY

### 🔴 CRITICAL (Breaking Changes - Requires Code Updates)

1. **People.Normalized Function → Normalized Title** (renamed field)
2. **People.Current Company removed** (replaced with Companies relationship)
3. **Portcos.Employee Count removed**
4. **Portcos.HQ Location → Primary Location** (renamed field)
5. **Platform-Open_Roles.Role Name** (manual → computed)
6. **Platform-Role_Specs.Spec Name** (manual → computed)
7. **Platform-Searches.Search Name** (manual → computed)
8. **Platform-Screens.completion time → End Time** (renamed field)
9. **Platform-Screens.Created Date removed**
10. **Platform-Assessments.Assessment ID** (auto number → computed)
11. **Platform-Assessments.Created Date removed**
12. **Platform-Assessments.Assessment Timestamp** (dateTime → date, lost time precision)

**Total:** 12 breaking changes

---

### ⚠️ MODERATE (Option Reductions - May Limit Functionality)

| Table | Field | Spec Options | Actual Options | Missing Count |
|-------|-------|--------------|----------------|---------------|
| People | Normalized Title | 8 | 2 | 6 missing |
| People | Source | 6 | 2 | 4 missing |
| Portcos | Stage | 6 | 2 | 4 missing |
| Portcos | Sector | 7 | 2 | 5 missing |
| Platform-Open_Roles | Status | 4 | 1 | 3 missing |
| Platform-Open_Roles | Priority | 4 | 2 | 2 missing |
| Platform-Searches | Status | 4 | 2 | 2 missing |
| Platform-Screens | Status | 4 | 2 | 2 missing |
| Platform-Assessments | Status | 4 | 4 | 0 (renamed only) |

**Total:** 28 missing single-select options across 8 fields

---

### ✅ LOW IMPACT (Cosmetic or Additive)

1. Table name prefixes ("Platform-")
2. ATID fields added (7 tables)
3. Expanded Role Type options (Platform-Open_Roles)
4. New tables (Companies, Operations-Automation Log, Operations-FMC_Roster)
5. New relationship fields (lookup, rollup)
6. Automation integration fields
7. Photo fields
8. Variant field (Platform-Role_Specs)

**Total:** 30+ new fields added

---

## CODE COMPATIBILITY CHECKLIST

### Required Code Updates

```python
# Table name changes
"Portco_Roles" → "Platform-Open_Roles"
"Role_Specs" → "Platform-Role_Specs"
"Searches" → "Platform-Searches"
"Screens" → "Platform-Screens"
"Assessments" → "Platform-Assessments"

# Field name changes
"Normalized Function" → "Normalized Title"
"HQ Location" → "Primary Location"
"completion time" → "End Time"

# Field type changes
People.LinkedIn URL: url → singleLineText
Portcos.Website: url → singleLineText
Assessments.Assessment Timestamp: dateTime → date (time lost)

# Removed fields (find alternatives)
People.Current Company → Use Companies relationship
Portcos.Employee Count → No replacement
Screens.Created Date → Use Created (timestamp)
Assessments.Created Date → Use Created (timestamp)

# Computed fields (read-only, don't try to set)
Platform-Open_Roles.Role Name
Platform-Role_Specs.Spec Name
Platform-Searches.Search Name
Platform-Assessments.Assessment ID

# Valid single-select options (data loading)
People.Normalized Title: {'CFO (Chief Financial Officer)', 'CTO (Chief Technology Officer)'}
People.Source: {'FMGuildPage', 'FMLinkedIN'}
Portcos.Stage: {'Series B', 'Series C'}
Portcos.Sector: {'B2B SaaS', 'Infrastructure'}
Platform-Open_Roles.Status: {'Open'}
Platform-Open_Roles.Priority: {'Critical', 'High'}
Platform-Searches.Status: {'Active', 'Planning'}
Platform-Screens.Status: {'Complete', 'Processing'}
Platform-Assessments.Status: {'Complete', 'In Progress', 'Error', 'Pending'}
```

---

## RECOMMENDATIONS

### Immediate Actions (Before Nov 19 Demo)

1. ✅ **Accept reduced options** - aligns with v1 minimal scope
2. 🔧 **Update all code** to use:
   - New table names (Platform-* prefix)
   - New field names (Normalized Title, Primary Location, End Time)
   - Read-only computed fields (don't try to set them)
   - Valid option sets (reduced lists)
3. 🧪 **Test data loading** with actual schema
4. 📝 **Update spec document** to match reality (or vice versa)

### Consider Adding Back (If Needed for Demo)

1. **Platform-Searches.Status:** Add "Completed" option for workflow closure
2. **Platform-Screens.Status:** Add "Draft" and "Failed" for error handling
3. **Platform-Assessments.Assessment Timestamp:** Change date → dateTime for precision

### Post-Demo / Phase 2

1. Expand all single-select options to full spec
2. Add Employee Count back to Portcos
3. Consider reverting computed identifiers to manual entry
4. Standardize on url field type instead of singleLineText

---

## VALIDATION QUERIES

Use these to verify the actual schema matches this report:

```python
# List all tables with IDs
mcp__airtable__list_tables(baseId="appeY64iIwU5CEna7", detailLevel="full")

# Check specific table schema
mcp__airtable__describe_table(baseId="appeY64iIwU5CEna7", tableId="tblHqYymo3Av9hLeC")  # People
mcp__airtable__describe_table(baseId="appeY64iIwU5CEna7", tableId="tblie7yBgF0gZywy4")  # Portcos
mcp__airtable__describe_table(baseId="appeY64iIwU5CEna7", tableId="tblRSTbBg3meBCW1x")  # Platform-Open_Roles
mcp__airtable__describe_table(baseId="appeY64iIwU5CEna7", tableId="tblbrV5s0023vzdE0")  # Platform-Role_Specs
mcp__airtable__describe_table(baseId="appeY64iIwU5CEna7", tableId="tbl6gHz2gM4pE75ne")  # Platform-Searches
mcp__airtable__describe_table(baseId="appeY64iIwU5CEna7", tableId="tbl2hrmaTWLEeaywL")  # Platform-Screens
mcp__airtable__describe_table(baseId="appeY64iIwU5CEna7", tableId="tblIhMnOG7Hp9xYna")  # Platform-Assessments
```

---

**End of Report**
