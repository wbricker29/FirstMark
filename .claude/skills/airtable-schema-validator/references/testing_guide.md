# Testing & Validation Guide

Complete guide to testing and validation tools for Airtable operations.

## Table of Contents

- [Overview](#overview)
- [Schema Validation](#schema-validation)
- [Data Quality Validation](#data-quality-validation)
- [Pre-Import Workflow](#pre-import-workflow)
- [Post-Import Workflow](#post-import-workflow)
- [Testing Checklist](#testing-checklist)
- [Troubleshooting](#troubleshooting)

---

## Overview

The airtable-operations skill includes two validation tools to ensure data integrity:

1. **validate_schema.py** - Pre-flight schema validation (checks structure before import)
2. **validate_data.py** - Post-import data quality validation (checks data after import)

**When to use:**
- **Before demo:** Validate schema matches expected structure
- **After import:** Verify data quality and completeness
- **During development:** Catch configuration issues early
- **Before presentation:** Ensure everything is ready

---

## Schema Validation

### Purpose

Validate that your Airtable base schema matches the expected structure for the FirstMark Talent Signal Agent.

### What It Checks

**Tables (6 expected):**
- People, Portco, Portco_Roles, Role_Specs, Searches, Assessments

**For each table:**
- ✅ Required fields exist
- ✅ Single-select options configured (CFO/CTO, Sources, etc.)
- ✅ Linked record fields point to correct tables
- ✅ Field types match expectations

### Usage

**Basic validation:**
```bash
cd .claude/skills/airtable-operations
python scripts/validate_schema.py
```

**With fix suggestions:**
```bash
python scripts/validate_schema.py --fix-suggestions
```

**Verbose mode:**
```bash
python scripts/validate_schema.py --verbose
```

### Expected Output

**Success:**
```
🔍 Airtable Schema Validator
============================================================
Validating base: appeY64iIwU5CEna7
Expected tables: 6

✅ People table: All fields present
✅ Portco table: All fields present
✅ Portco_Roles table: All fields present
✅ Role_Specs table: All fields present
✅ Searches table: All fields present
✅ Assessments table: All fields present

============================================================
✅ Schema validation passed!
```

**With warnings:**
```
🔍 Airtable Schema Validator
============================================================

⚠️  WARNINGS:
  • People → Normalized Title: Missing options [CPO, CRO, COO]
  • People → Source: Missing options [FMCFO, FMCTOSummit]

============================================================
✅ Schema validation passed!
   2 warnings (non-critical)
```

**With fix suggestions:**
```
📋 RECOMMENDED FIXES:
============================================================

People → Normalized Title:
  1. Open Airtable and navigate to People table
  2. Click on 'Normalized Title' column header
  3. Click 'Edit field' → 'Edit options'
  4. Add missing options: CFO, CTO, CPO, CRO, COO, CMO, CEO, Other

People → Source:
  1. Open Airtable and navigate to People table
  2. Click on 'Source' column header
  3. Click 'Edit field' → 'Edit options'
  4. Add missing options: FMGuildPage, FMLinkedIN, FMCFO, FMCTOSummit, FMFounder, FMProduct
```

### Fix Workflow

1. Run validator with `--fix-suggestions`
2. Follow step-by-step instructions in output
3. Make changes in Airtable UI
4. Re-run validator to confirm fixes
5. Proceed with data loading

---

## Data Quality Validation

### Purpose

Validate data quality in the People table after import to catch issues early.

### What It Checks

**Critical Issues (will fail validation):**
- ❌ Duplicate names
- ❌ Missing required fields (Name, Added Date)
- ❌ Invalid email formats
- ❌ Invalid LinkedIn URL formats
- ❌ Invalid Normalized Title values
- ❌ Invalid Source values

**Warnings (non-critical):**
- ⚠️  Missing important fields (Title, Company, LinkedIn URL)
- ⚠️  Orphaned records (no linked roles)

**CSV Comparison:**
- Expected vs actual record count
- Missing candidates (in CSV but not Airtable)

### Usage

**Basic validation:**
```bash
cd .claude/skills/airtable-operations
python scripts/validate_data.py
```

**With CSV comparison:**
```bash
python scripts/validate_data.py --csv ../../../
```

**Save report to file:**
```bash
python scripts/validate_data.py --report quality_report.txt
```

**Verbose mode:**
```bash
python scripts/validate_data.py --csv ../../../ --verbose
```

### Expected Output

**Success:**
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

**With issues:**
```
🔍 Airtable Data Quality Validator
============================================================

📊 Data Quality Report - People Table
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Records: 66
✅ Complete: 55 (83%)
⚠️  Incomplete: 11 (17%)

🚨 CRITICAL ISSUES:
────────────────────────────────────────────────────────────

❌ Duplicate Names (2):
  • John Smith (appears 2 times)
  • Sarah Johnson (appears 2 times)

❌ Invalid LinkedIn URLs (3):
  • Jane Doe: linkedin.com/janedoe
  • Bob Wilson: http://linkedin/bob
  • Alice Brown: www.linkedin.com

❌ Invalid Function Values (1):
  • Mike Davis: VP Engineering

📋 CSV Comparison:
────────────────────────────────────────────────────────────
Expected (from CSV): 64 records
Found in Airtable: 62 records
❌ Missing from Airtable: 2 records
  • James Anderson
  • Emily Taylor

============================================================
❌ Data quality issues detected!
   Review critical issues above and fix in Airtable
```

### Fix Workflow

1. Run validator with `--csv` and `--verbose`
2. Review critical issues section
3. Fix issues in Airtable:
   - **Duplicates:** Merge or delete duplicate records
   - **Invalid emails:** Correct format (user@domain.com)
   - **Invalid LinkedIn:** Use full URL (https://linkedin.com/in/username)
   - **Invalid functions:** Use valid options (CFO, CTO, etc.)
4. Re-run validator to confirm fixes
5. Save clean report with `--report` flag

---

## Pre-Import Workflow

**Recommended steps before loading candidates:**

### Step 1: Validate Schema (1 minute)

```bash
cd .claude/skills/airtable-operations
python scripts/validate_schema.py --fix-suggestions
```

**Action:** Fix any schema issues in Airtable UI

### Step 2: Preview Import (30 seconds)

```bash
python scripts/load_candidates.py ../../../ --dry-run --verbose
```

**Check:**
- ✅ CSV schema detected correctly
- ✅ Column mapping looks reasonable
- ✅ Expected candidate count
- ⚠️  No compatibility warnings

### Step 3: Load Data (5 minutes)

```bash
python scripts/load_candidates.py ../../../ --verbose
```

**Monitor:** Progress output, watch for errors

### Step 4: Validate Data (1 minute)

```bash
python scripts/validate_data.py --csv ../../../ --verbose
```

**Action:** Fix any data quality issues

**Total time: ~7-8 minutes**

---

## Post-Import Workflow

**After loading candidates, run full validation:**

### Quick Check (30 seconds)

```bash
cd .claude/skills/airtable-operations
python scripts/validate_data.py
```

### Full Report (1 minute)

```bash
python scripts/validate_data.py \
  --csv ../../../ \
  --report quality_report.txt \
  --verbose
```

### Spot Check in Airtable (2 minutes)

1. Open People table
2. Filter by Added Date = today
3. Review 5-10 random records
4. Check:
   - ✅ Names look correct
   - ✅ LinkedIn URLs formatted properly
   - ✅ Functions mapped correctly (CFO/CTO)
   - ✅ No obvious data corruption

---

## Testing Checklist

Use this checklist before demo day:

### Schema Validation

- [ ] All 6 tables exist (People, Portco, Portco_Roles, Role_Specs, Searches, Assessments)
- [ ] People table has all required fields
- [ ] Normalized Title has all options (CFO, CTO, CPO, CRO, COO, CMO, CEO, Other)
- [ ] Source has all options (FMGuildPage, FMLinkedIN, FMCFO, FMCTOSummit, FMFounder, FMProduct)
- [ ] Linked record fields configured correctly
- [ ] No schema validation errors

### Data Quality

- [ ] Total record count matches expected (existing + imported)
- [ ] No duplicate names
- [ ] All records have Name + Added Date
- [ ] LinkedIn URLs in valid format
- [ ] Email addresses (if any) in valid format
- [ ] Normalized Title values are valid
- [ ] Source values are valid
- [ ] CSV comparison shows all records loaded
- [ ] No critical data quality issues

### Manual Spot Check

- [ ] Filter People table by Added Date = today
- [ ] Review 5-10 random records
- [ ] Check names, titles, companies look correct
- [ ] Verify LinkedIn URLs clickable
- [ ] Confirm functions mapped correctly
- [ ] No obvious data corruption

### Demo Readiness

- [ ] Schema validation passes
- [ ] Data quality validation passes
- [ ] Manual spot check passes
- [ ] Quality report saved for reference
- [ ] Ready to proceed with Module 4 demo

---

## Troubleshooting

### Schema Validator Not Running

**Issue:** Script won't execute

**Solutions:**
```bash
# Check Python version (requires 3.11+)
python --version

# Try with python3
python3 scripts/validate_schema.py

# Check file permissions
chmod +x scripts/validate_schema.py
./scripts/validate_schema.py
```

### MCP Tools Not Available

**Issue:** "MCP tools not found" error

**Solution:**
1. Check MCP configuration: `cat ~/.config/claude/mcp_settings.json | grep airtable`
2. Verify Airtable API key is set in environment
3. Restart Claude Code
4. Re-run validator

### Data Validator Shows No Records

**Issue:** "Total Records: 0"

**Solution:**
1. Verify BASE_ID and PEOPLE_TABLE_ID in script
2. Check Airtable API key has read access
3. Confirm People table has records
4. Run with `--verbose` to see debug output

### CSV Comparison Not Working

**Issue:** "Could not read CSV file"

**Solutions:**
```bash
# Use absolute path
python scripts/validate_data.py --csv /full/path/to/file.csv

# Check file exists
ls -la ../../../

# Verify CSV encoding (should be UTF-8)
file ../../../
```

### Too Many Warnings

**Issue:** Lots of "missing optional field" warnings

**This is normal:**
- Optional fields (Title, Company, LinkedIn URL) may be blank
- Warnings are informational, not errors
- Only critical issues (duplicates, invalid formats) fail validation

**To reduce noise:**
- Run without `--verbose` flag
- Focus on critical issues section
- Use `--report` to save details for later review

### False Positive Duplicates

**Issue:** Names flagged as duplicates but are different people

**Solutions:**
1. Check if names are truly identical (case-sensitive)
2. Add middle initials or suffixes to disambiguate
3. Use "Name (Company)" format if necessary
4. Update records in Airtable to be unique

### Invalid LinkedIn URLs

**Issue:** Valid-looking URLs flagged as invalid

**Common mistakes:**
- Missing `https://` prefix
- Using `linkedin.com` instead of `linkedin.com/in/username`
- Extra spaces or characters
- Shortened URLs (bit.ly, etc.)

**Fix:** Use full format: `https://www.linkedin.com/in/username`

---

## Next Steps

After successful validation:

1. **Save quality report:** Keep for demo day reference
2. **Update spec.md:** Document actual record counts
3. **Test Module 4:** Create test Search record
4. **Proceed with implementation:** Begin demo/agents.py development

**Questions?** See [troubleshooting.md](troubleshooting.md) for additional help.
