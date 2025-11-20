---
name: airtable-schema-validator
description: Validate Airtable People table schema and data quality before demo day. Pre-flight schema checks (fields, single-select options), post-import data quality validation (duplicates, format validation, completeness scoring). Provides actionable fix suggestions. Production-ready for FirstMark presentation.
---

# Airtable Schema Validator

## Overview

Validate Airtable schema and data quality before demo day. **Two validation modes: pre-flight schema checks and post-import data quality verification.**

**Key features:**
- 🔍 **Schema validation:** Check tables, fields, single-select options, relationships
- ✅ **Data quality checks:** Duplicates, format validation, completeness scoring
- 🛠️ **Fix suggestions:** Actionable recommendations for schema issues
- 📊 **Detailed reporting:** CSV comparison, field-level validation, warnings vs errors
- 🚨 **Early issue detection:** Catch problems before demo day

**Use this skill when:**
- Setting up Airtable before demo day (pre-flight validation)
- After importing data to verify quality (post-import validation)
- Troubleshooting schema configuration issues
- Need to verify single-select options are configured correctly
- Want to ensure data meets quality standards

---

## Quick Start

### Pre-Flight: Schema Validation (Before Loading Data)

**Purpose:** Validate Airtable schema matches expected structure before importing data.

```bash
cd .claude/skills/airtable-schema-validator
python scripts/validate_schema.py
```

**What it checks:**
- ✅ People table exists
- ✅ Required fields present (Name)
- ✅ Optional fields present (Current Title, Current Company, LinkedIn URL, Location, Bio, etc.)
- ✅ Single-select options configured:
  - Normalized Title: CFO, CTO, CPO, CEO, CMO, COO, CRO, CDO, Exec roles
  - Source: FMGuildPage, FMLinkedIN

**With fix suggestions:**
```bash
python scripts/validate_schema.py --fix-suggestions
```

**Output example:**
```
🔍 Airtable Schema Validator
============================================================
Validating base: appeY64iIwU5CEna7
Expected tables: 1
Found tables: 11

Checking table: People

============================================================
✅ Schema validation passed!
```

---

### Post-Import: Data Quality Validation (After Loading Data)

**Purpose:** Validate data quality in People table after import to catch issues early.

```bash
cd .claude/skills/airtable-schema-validator
python scripts/validate_data.py
```

**What it checks:**

**Critical issues (will fail validation):**
- ❌ Duplicate names
- ❌ Missing required fields (Name, Added Date)
- ❌ Invalid email formats
- ❌ Invalid LinkedIn URL formats
- ❌ Invalid Normalized Title values
- ❌ Invalid Source values

**Warnings (non-critical):**
- ⚠️ Missing important fields (Title, Company, LinkedIn URL)
- ⚠️ Orphaned records (no linked roles)

**With CSV comparison:**
```bash
python scripts/validate_data.py --csv /path/to/original/csv/
```

**Save detailed report:**
```bash
python scripts/validate_data.py --csv /path/to/csv/ --report quality_report.txt --verbose
```

**Output example:**
```
🔍 Airtable Data Quality Validator
============================================================

📊 Data Quality Report - People Table
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Records: 66
✅ Complete: 58 (88%)
⚠️  Incomplete: 8 (12%)

⚠️  WARNINGS (Non-Critical):
────────────────────────────────────────────────────────────
• Missing LinkedIn URL (3 records)
• Missing Normalized Title (5 records)

📋 CSV Comparison:
────────────────────────────────────────────────────────────
Expected (from CSV): 64 records
Found in Airtable: 66 records
✅ All CSV records found in Airtable

============================================================
✅ Data quality validation passed!
   8 records have optional fields missing
```

---

## Validation Workflows

### Complete Demo Day Pre-Check (7-8 minutes)

Run before demo to ensure everything is configured:

```bash
cd .claude/skills/airtable-schema-validator

# Step 1: Validate schema (1 minute)
python scripts/validate_schema.py --fix-suggestions

# Step 2: Validate data quality (1 minute)
python scripts/validate_data.py --csv /path/to/csv/ --verbose

# Step 3: Save quality report for reference
python scripts/validate_data.py --csv /path/to/csv/ --report quality_report.txt
```

### Quick Schema Check (1 minute)

Just check if schema is configured correctly:

```bash
python scripts/validate_schema.py
```

Look for:
- ✅ Green checkmarks = all good
- ⚠️ Yellow warnings = non-critical (optional fields missing)
- ❌ Red errors = critical issues (must fix before demo)

### Quick Data Quality Check (30 seconds)

After loading data, verify it's valid:

```bash
python scripts/validate_data.py
```

Look for:
- Total record count matches expected
- No critical errors
- Warnings are acceptable (incomplete optional fields)

---

## Schema Validation Details

### What Tables Are Checked

**Required tables (v1 minimal spec):**
1. **People** - Executive candidates
2. **Portco** - Portfolio companies
3. **Portco_Roles** - Open roles at companies
4. **Role_Specs** - Evaluation templates (CFO/CTO)
5. **Searches** - Search records (linking roles to candidates)
6. **Assessments** - AI-generated assessments

### What Fields Are Validated

**People table:**
- Required: Name, Added Date
- Optional: Title, Company, Normalized Title, Source, LinkedIn URL, Bio
- Single-select: Normalized Title (CFO/CTO/etc.), Source (FMGuildPage/etc.)

**Other tables:**
- Validates required fields exist
- Checks single-select options are configured
- Verifies linked record relationships

**For complete field reference:** See [references/field_types.md](references/field_types.md)

### Common Schema Issues

**Issue 1: Missing single-select options**
```
⚠️ Normalized Title: Missing options [CPO, CRO, COO]
```
**Fix:** Add options via Airtable UI → People table → Normalized Title column → Edit field → Edit options

**Issue 2: Table not found**
```
❌ Portco_Roles table not found
```
**Fix:** Create table via Airtable UI or use schema template

**Issue 3: Required field missing**
```
❌ People table: Missing required field 'Name'
```
**Fix:** Add field via Airtable UI (should not happen with proper setup)

---

## Data Quality Validation Details

### Critical Validation Checks

**1. Duplicate Detection**
- Checks for duplicate names in People table
- Exact match only (case-sensitive)
- Lists all duplicates found

**2. Required Fields**
- Name must be present (non-empty)
- Added Date must be set
- Fails validation if missing

**3. Format Validation**
- Email: Must match standard email format (xxx@xxx.xxx)
- LinkedIn URL: Must start with linkedin.com or www.linkedin.com
- Fails validation if invalid format

**4. Single-Select Values**
- Normalized Title: Must be in valid set (CFO, CTO, etc.)
- Source: Must be in valid set (FMGuildPage, etc.)
- Fails validation if invalid value

### Warning Checks (Non-Critical)

**1. Missing Optional Fields**
- Title, Company, LinkedIn URL recommended but not required
- Reports count of records missing these fields

**2. Orphaned Records**
- People records with no linked Portco_Roles
- Searches with no linked candidates

### CSV Comparison

When you provide `--csv /path/to/csv/`, the validator:
1. Counts records in original CSV file
2. Compares to Airtable record count
3. Reports discrepancies (missing or extra records)
4. Useful for verifying complete import

---

## Demo Day Checklist

Use this before demo to ensure everything is ready:

### Schema Checklist
- [ ] All 6 tables exist
- [ ] Normalized Title has all options (CFO, CTO, CPO, etc.)
- [ ] Source has all options (FMGuildPage, etc.)
- [ ] No schema validation errors
- [ ] Run `validate_schema.py --fix-suggestions` and address all issues

### Data Quality Checklist
- [ ] No duplicate names
- [ ] All records have Name + Added Date
- [ ] LinkedIn URLs in valid format
- [ ] No critical data quality issues
- [ ] CSV comparison shows all records loaded
- [ ] Run `validate_data.py --csv /path/to/csv/` and verify output

### Manual Spot Check
- [ ] Filter People table by Added Date = today
- [ ] Review 5-10 random records
- [ ] Verify data looks correct
- [ ] Check one record end-to-end (can you create a Screen for it?)

---

## Troubleshooting

### Schema validation fails

**Check 1: API key set correctly**
```bash
cat .env | grep AIRTABLE_API_KEY
```

**Check 2: Base ID correct**
- Open `scripts/validate_schema.py`
- Verify BASE_ID = "appeY64iIwU5CEna7" (or your base)

**Check 3: Tables exist in Airtable**
- Open Airtable base in browser
- Verify all 6 tables are present

### Data validation fails with format errors

**LinkedIn URL format:**
- Valid: `linkedin.com/in/john-doe`, `www.linkedin.com/in/john-doe`
- Invalid: `http://linkedin.com/in/john-doe` (protocol not required)

**Email format:**
- Valid: `john@example.com`
- Invalid: `john@example` (missing TLD)

### CSV comparison shows missing records

**Common causes:**
1. Duplicates were skipped during import (check loader output)
2. CSV has invalid rows that were filtered
3. Import was interrupted

**Solution:**
- Re-run loader with `--verbose` to see which records were skipped
- Check loader summary for skip reasons

---

## Configuration

### Prerequisites

**Required dependencies:**
- `pyairtable>=2.0.0` (Airtable API client)
- `python-dotenv>=1.0.0` (Environment variable management)

These are already included in the project's `pyproject.toml`.

### Environment Variables

**.env file in project root:**
```bash
AIRTABLE_API_KEY=your_api_key_here
```

### Hardcoded Values

**Base ID (in both scripts):**
```python
BASE_ID = "appeY64iIwU5CEna7"
```

**To use with different base:**
Edit BASE_ID in both `validate_schema.py` and `validate_data.py`.

---

## Success Criteria

**Schema validation:**
✅ All 6 tables exist
✅ Required fields present
✅ Single-select options configured
✅ No critical errors

**Data quality validation:**
✅ No duplicate names
✅ All records have required fields
✅ Valid email/LinkedIn formats
✅ CSV comparison matches expected count

---

## See Also

**Technical Documentation:**
- [references/schema_reference.md](references/schema_reference.md) - Complete schema exploration guide
- [references/field_types.md](references/field_types.md) - Field type catalog with validation rules
- [references/testing_guide.md](references/testing_guide.md) - Complete testing workflows
- [scripts/validate_schema.py](scripts/validate_schema.py) - Schema validation implementation
- [scripts/validate_data.py](scripts/validate_data.py) - Data quality validation implementation
- [scripts/airtable_utils.py](scripts/airtable_utils.py) - Shared API utilities

**Related Skills:**
- `airtable-csv-loader` - Load executive candidate CSVs into Airtable
