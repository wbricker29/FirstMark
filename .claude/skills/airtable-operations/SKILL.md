---
name: airtable-operations
description: Complete Airtable operations toolkit for FirstMark Talent Signal Agent. SCHEMA EXPLORATION - Discover bases, list tables, examine field types/constraints using MCP tools. DATA LOADING - Automate Module 1 by loading executive candidates from ANY CSV file with intelligent schema detection, column mapping, bio file loading, duplicate detection, and progress reporting. TESTING & VALIDATION - Pre-flight schema validation, post-import data quality checks, duplicate detection, format validation (emails, LinkedIn URLs), completeness scoring, and CSV comparison. Production-ready for case presentation.
---

# Airtable Operations

## Table of Contents

- [Overview](#overview)
- [Quick Start (3 Commands)](#quick-start-3-commands)
- [Schema Exploration (Pre-Flight Check)](#schema-exploration-pre-flight-check)
- [Testing & Validation](#testing--validation)
- [Usage Examples](#usage-examples)
- [What It Does (Step-by-Step)](#what-it-does-step-by-step)
  - [Step 1: Detect CSV Schema](#step-1-detect-csv-schema)
  - [Step 2: Read & Parse CSV](#step-2-read--parse-csv)
  - [Step 3: Load Executive Bios](#step-3-load-executive-bios)
  - [Step 4: Normalize Data](#step-4-normalize-data)
  - [Step 5: Check Duplicates](#step-5-check-duplicates)
  - [Step 6: Create Records](#step-6-create-records)
  - [Step 7: Summary Report](#step-7-summary-report)
- [Demo Day Usage](#demo-day-usage)
- [Schema Limitations (Demo Scope)](#schema-limitations-demo-scope)
- [Expected Results](#expected-results)
- [Troubleshooting](#troubleshooting)
- [Technical Documentation](#technical-documentation)
- [Configuration](#configuration)
- [Integration with v1 Minimal Spec](#integration-with-v1-minimal-spec)
- [Success Criteria](#success-criteria)
- [Next Steps After Import](#next-steps-after-import)
- [See Also](#see-also)

## Overview

This skill provides complete Airtable operations for the FirstMark Talent Signal Agent project:
- **Schema Exploration:** Validate table schemas, field constraints, and relationships using MCP tools
- **Data Loading:** Automate Module 1 (Candidate Sourcing) by loading executive candidates from **any CSV format** into the Airtable People table
- **Testing & Validation:** Pre-flight schema checks and post-import data quality validation

Designed for flexibility during the case presentation when data formats may vary.

**Key Features:**
- 🔄 **Flexible CSV Input:** Handles any CSV format with intelligent schema detection
- 📄 **Bio File Loading:** Automatically loads executive bios from .txt files (matches by name)
- 🧠 **Smart Column Mapping:** Maps common field name variations to Airtable schema
- ✅ **Duplicate Detection:** Skips existing candidates automatically
- 🔍 **Dry-Run Mode:** Preview changes before committing to Airtable
- 📊 **Progress Reporting:** Detailed status updates during import
- 🧪 **Schema Validation:** Pre-flight checks for table structure and field configuration
- ✨ **Data Quality Checks:** Post-import validation for duplicates, formats, and completeness

**Use this skill when:**
- You need to load candidates from ANY CSV file into Airtable
- You're given surprise data during the case presentation
- You have executive bio .txt files to import alongside CSV data
- You want to automate Module 1 instead of manual data entry
- You need to validate Airtable schema before demo day
- You want to verify data quality after import

**Supported CSV Formats:**
- `guildmember_scrape.csv` (64 executives from Guild pages)
- `Mock_Guilds.csv` (Guild member data)
- `Exec_Network.csv` (Partner connections)
- Any CSV with executive/candidate data

**Time savings:** Reduces 2-4 hours of manual data entry to ~5-10 minutes of automated processing.

---

## Quick Start (3 Commands)

### 1. Preview Before Import (Recommended)

```bash
cd .claude/skills/airtable-file-loader
python scripts/load_candidates.py ../../../reference/guildmember_scrape.csv --dry-run
```

**Output:** Shows what WOULD be created without making any changes.

### 2. Load Candidates

```bash
python scripts/load_candidates.py ../../../reference/guildmember_scrape.csv
```

**Output:** Creates records in Airtable People table, reports progress.

### 3. Verify Results

Open Airtable → People table → Filter by Added Date = today

**Expected:** ~64 total records (2 existing + 62 new)

---

## Schema Exploration (Pre-Flight Check)

Before loading data, you may want to validate your Airtable schema to understand field constraints, especially for single-select fields and table relationships.

### Quick Schema Validation Workflow

**1. List available bases:**
```
mcp__airtable__list_bases()
```

**2. Explore tables in your base:**
```
mcp__airtable__list_tables({
  baseId: "appeY64iIwU5CEna7"
})
```

**3. Get detailed field schema:**
```
mcp__airtable__describe_table({
  baseId: "appeY64iIwU5CEna7",
  tableId: "People"
})
```

### Why Schema Exploration Matters

**For data loading:**
- Validate single-select options (Normalized Function, Source) before import
- Understand required vs. optional fields
- Check linked record relationships (People ↔ Portco_Roles)
- Prevent "invalid value" errors during record creation

**Example use case:**
Before running the loader, verify that your Airtable People table has the expected Normalized Function options (CFO, CTO). If you need to add more options (CPO, CRO, etc.), you can update the schema first.

### Common Validation Patterns

**Check single-select field options:**
```python
# Get People table schema
schema = describe_table(baseId="appeY64iIwU5CEna7", tableId="People")

# Extract valid options for Normalized Function
function_field = next(f for f in schema["fields"] if f["name"] == "Normalized Function")
valid_functions = [choice["name"] for choice in function_field["options"]["choices"]]

# Validate before import
print(f"Valid functions: {valid_functions}")  # ['CFO', 'CTO']
```

**Understand table relationships:**
```python
# Find linked record fields
for field in schema["fields"]:
    if field["type"] == "multipleRecordLinks":
        print(f"{field['name']} links to table: {field['options']['linkedTableId']}")
```

### Detailed Schema Documentation

For comprehensive schema exploration including field types, validation patterns, and troubleshooting:
- See [references/schema_reference.md](references/schema_reference.md) - Complete schema exploration guide
- See [references/field_types.md](references/field_types.md) - Field type catalog with validation rules

---

## Testing & Validation

Before loading data or after import, use validation tools to ensure data integrity and catch issues early.

### Schema Validation (Pre-Flight Check)

**Purpose:** Validate Airtable schema matches expected structure before importing data.

**What it checks:**
- ✅ All 6 tables exist (People, Portco, Portco_Roles, Role_Specs, Searches, Assessments)
- ✅ Required fields present
- ✅ Single-select options configured (CFO/CTO, Sources)
- ✅ Linked record fields point to correct tables

**Quick validation:**
```bash
cd .claude/skills/airtable-operations
python scripts/validate_schema.py
```

**With fix suggestions:**
```bash
python scripts/validate_schema.py --fix-suggestions
```

**Output example:**
```
🔍 Airtable Schema Validator
============================================================
✅ People table: All fields present
⚠️  Normalized Function: Missing options [CPO, CRO, COO]
⚠️  Source: Missing options [FMCFO, FMCTOSummit]

📋 RECOMMENDED FIXES:
People → Normalized Function:
  1. Open Airtable and navigate to People table
  2. Click on 'Normalized Function' column header
  3. Click 'Edit field' → 'Edit options'
  4. Add missing options: CFO, CTO, CPO, CRO, COO, CMO, CEO, Other
============================================================
✅ Schema validation passed!
   2 warnings (non-critical)
```

---

### Data Quality Validation (Post-Import Check)

**Purpose:** Validate data quality in People table after import to catch issues early.

**What it checks:**

**Critical issues (will fail validation):**
- ❌ Duplicate names
- ❌ Missing required fields (Name, Added Date)
- ❌ Invalid email formats
- ❌ Invalid LinkedIn URL formats
- ❌ Invalid Normalized Function values
- ❌ Invalid Source values

**Warnings (non-critical):**
- ⚠️  Missing important fields (Title, Company, LinkedIn URL)
- ⚠️  Orphaned records (no linked roles)

**Quick validation:**
```bash
cd .claude/skills/airtable-operations
python scripts/validate_data.py
```

**With CSV comparison:**
```bash
python scripts/validate_data.py --csv ../../../reference/guildmember_scrape.csv
```

**Save detailed report:**
```bash
python scripts/validate_data.py --csv ../../../reference/guildmember_scrape.csv --report quality_report.txt --verbose
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
• Missing Normalized Function (5 records)

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

### Recommended Testing Workflow

**Before demo day (complete workflow):**

```bash
# Step 1: Validate schema (1 minute)
python scripts/validate_schema.py --fix-suggestions

# Step 2: Preview import (30 seconds)
python scripts/load_candidates.py ../../../reference/guildmember_scrape.csv --dry-run

# Step 3: Load data (5 minutes)
python scripts/load_candidates.py ../../../reference/guildmember_scrape.csv --verbose

# Step 4: Validate data quality (1 minute)
python scripts/validate_data.py --csv ../../../reference/guildmember_scrape.csv --verbose

# Step 5: Save quality report for reference
python scripts/validate_data.py --csv ../../../reference/guildmember_scrape.csv --report quality_report.txt
```

**Total time: ~7-8 minutes**

---

### Testing Checklist

Use this checklist before demo:

**Schema:**
- [ ] All 6 tables exist
- [ ] Normalized Function has all options
- [ ] Source has all options
- [ ] No schema validation errors

**Data Quality:**
- [ ] No duplicate names
- [ ] All records have Name + Added Date
- [ ] LinkedIn URLs in valid format
- [ ] No critical data quality issues
- [ ] CSV comparison shows all records loaded

**Manual Spot Check:**
- [ ] Filter People table by Added Date = today
- [ ] Review 5-10 random records
- [ ] Verify data looks correct

---

### Detailed Testing Guide

For comprehensive testing workflows, troubleshooting, and validation patterns:
- See [references/testing_guide.md](references/testing_guide.md) - Complete testing & validation guide

---

## Usage Examples

### Basic Import

```bash
# From skill directory
cd .claude/skills/airtable-file-loader
python scripts/load_candidates.py path/to/candidates.csv
```

### Dry Run (Safe Preview)

```bash
# Preview changes without creating records
python scripts/load_candidates.py path/to/candidates.csv --dry-run
```

### Verbose Mode (Detailed Logging)

```bash
# Show detailed progress and debugging info
python scripts/load_candidates.py path/to/candidates.csv --verbose
```

### Combined Modes

```bash
# Preview with full detail (recommended before live import)
python scripts/load_candidates.py path/to/candidates.csv --dry-run --verbose

# Execute with progress tracking
python scripts/load_candidates.py path/to/candidates.csv --verbose
```

### Shell Wrapper (Convenience)

```bash
# From project root
./claude/skills/airtable-file-loader/scripts/quick_load.sh reference/guildmember_scrape.csv
```

---

## What It Does (Step-by-Step)

The loader executes a 7-step workflow to import candidates:

1. **Detect CSV Schema** - Automatically maps CSV columns to Airtable fields (supports 20+ column name variations)
2. **Read & Parse CSV** - Loads data with UTF-8 encoding, filters invalid rows
3. **Load Executive Bios** - Matches .txt files to candidates using fuzzy matching (80% similarity)
4. **Normalize Data** - Infers functions (CFO/CTO/etc.) from titles, fixes typos, sets dates
5. **Check Duplicates** - Compares against existing Airtable records (exact name match)
6. **Create Records** - Inserts into People table with progress tracking
7. **Summary Report** - Shows created/skipped/error counts

**Detailed walkthrough with examples:** See [implementation_guide.md](references/implementation_guide.md) for complete step-by-step execution details, column mapping rules, normalization logic, and field configurations.

---

## Demo Day Usage

### Scenario: Given Surprise CSV During Presentation

**Step 1: Quick validation (30 seconds)**
```bash
python scripts/load_candidates.py /path/to/surprise_data.csv --dry-run --verbose
```

**Check for:**
- ✅ Schema detected successfully
- ✅ Required fields mapped (name, title, company)
- ✅ Reasonable candidate count
- ⚠️ Any compatibility warnings

**Step 2: Load if compatible**
```bash
python scripts/load_candidates.py /path/to/surprise_data.csv --verbose
```

**Step 3: Verify in Airtable**
- Open People table
- Filter by Added Date = today
- Spot-check 3-5 records for accuracy

**Fallback Plan:** If loader fails, manually create 2-3 sample records and proceed with Module 4 demo.

---

## Schema Limitations (Demo Scope)

**Current Airtable schema (limited for demo):**
- **Normalized Function:** CFO, CTO only (missing: CPO, CRO, COO, CMO, CEO, Other)
- **Source:** FMGuildPage, FMLinkedIN only (missing: FMCFO, FMCTOSummit, FMFounder, FMProduct)

**Script behavior with limited schema:**
- Only sets Normalized Function if value is CFO or CTO
- Only sets Source if value is FMGuildPage or FMLinkedIN
- Other candidates will have these fields blank (not an error)
- Records still created successfully (these are optional fields)

**To expand schema (optional pre-demo setup):**
1. Open Airtable People table
2. Click Normalized Function column → Edit field
3. Add options: CPO, CRO, COO, CMO, CEO, Other
4. Click Source column → Edit field
5. Add options: FMCFO, FMCTOSummit, FMFounder, FMProduct
6. Re-run loader

---

## Expected Results

**From guildmember_scrape.csv (64 candidates):**
- ~25-30 CFOs (function populated)
- ~20-25 CTOs (function populated)
- ~10-15 Other functions (function blank)

**After import:**
```
People table: 66 records (4 pre-existing + 62 new)
├── 30 CFOs (Normalized Function = CFO)
├── 25 CTOs (Normalized Function = CTO)
└── 11 Other (Normalized Function = blank)
```

**Verification checklist:**
- [ ] Total count matches expected (existing + created)
- [ ] No duplicate names
- [ ] All records have Name + Added Date
- [ ] CFO/CTO candidates have Normalized Function populated
- [ ] Spot-check 5 random records for data accuracy

---

## Troubleshooting

### Common Issues

**CSV file not found:**
```bash
# Use absolute path or navigate to correct directory
python scripts/load_candidates.py /full/path/to/file.csv
```

**Airtable MCP not available:**
```bash
# Check MCP configuration
cat ~/.config/claude/mcp_settings.json | grep airtable

# Verify Airtable API key set
# Restart Claude Code after config changes
```

**Schema detection incorrect:**
```bash
# Run with verbose to see mapping
python scripts/load_candidates.py file.csv --dry-run --verbose

# Check: Does CSV have recognizable column names?
# Solution: Rename columns or adjust FIELD_MAPPINGS in script
```

**Bio files not matching:**
```bash
# Verify .txt files in same directory as CSV
ls path/to/csv/directory/*.txt

# Run with verbose to see matching attempts
python scripts/load_candidates.py file.csv --dry-run --verbose
```

**Rate limit errors (429):**
- Import smaller batches (<50 candidates)
- Run during off-peak hours
- See [troubleshooting.md](references/troubleshooting.md#8-rate-limit-exceeded) for retry logic

### Full Troubleshooting Guide

See [references/troubleshooting.md](references/troubleshooting.md) for:
- 10 common issues with detailed solutions
- Emergency procedures for demo day
- Debug checklist
- Verbose logging examples

---

## Technical Documentation

### For Developers

**Implementation details:**
- [references/implementation_guide.md](references/implementation_guide.md) - Complete technical documentation
  - Schema detection algorithm
  - Column mapping strategy
  - Data normalization rules
  - Bio file matching logic
  - Duplicate detection implementation
  - Record creation process
  - Performance considerations

**Data loading script:**
- [scripts/load_candidates.py](scripts/load_candidates.py) - Executable Python script (451 lines)
  - CLI argument parsing
  - Flexible CSV reading
  - Intelligent schema detection
  - Bio file loading with fuzzy matching
  - Airtable integration via MCP
  - Error handling and progress reporting

**Validation scripts:**
- [scripts/validate_schema.py](scripts/validate_schema.py) - Schema validation tool
  - Checks all 6 tables exist
  - Validates required fields
  - Checks single-select options
  - Verifies linked record relationships
  - Provides actionable fix suggestions

- [scripts/validate_data.py](scripts/validate_data.py) - Data quality validation tool
  - Duplicate detection
  - Required field checking
  - Email/LinkedIn URL format validation
  - Single-select value validation
  - CSV comparison
  - Completeness scoring

**Shell wrapper:**
- [scripts/quick_load.sh](scripts/quick_load.sh) - Convenience wrapper for bash users

---

## Configuration

### Airtable Settings

**Hardcoded in scripts/load_candidates.py:**
```python
BASE_ID = "appeY64iIwU5CEna7"
PEOPLE_TABLE_ID = "tblHqYymo3Av9hLeC"
```

**To use with different base/table:**
Edit `scripts/load_candidates.py` and update IDs.

### Valid Single-Select Options

**Hardcoded for demo schema:**
```python
VALID_FUNCTIONS = {'CFO', 'CTO'}
VALID_SOURCES = {'FMGuildPage', 'FMLinkedIN'}
```

**To expand:**
1. Update Airtable schema (add options via UI)
2. Edit `scripts/load_candidates.py` and expand sets
3. Re-run loader

---

## Integration with v1 Minimal Spec

**Module 1 Status:** Pre-populated manually (per v1_minimal_spec.md)

**This skill is for:**
- ✅ Demo setup (loading 64 candidates before presentation)
- ✅ Demo backup (re-load if Airtable data corrupted)
- ✅ Testing Module 4 (populate People table for Screen workflow tests)

**This skill is NOT:**
- ❌ Part of v1 production workflow (Module 4 only in v1 scope)
- ❌ Required for v1 implementation (candidates pre-populated)

**Demo timeline:**
1. **Pre-demo (Nov 18):** Run loader to populate People table
2. **Demo day (Nov 19):** Use pre-loaded candidates for Module 4 Screen workflow
3. **If needed:** Re-run loader as backup if data issues arise

---

## Success Criteria

✅ **Script completes without fatal errors**
✅ **All non-duplicate records created in Airtable**
✅ **Data correctly mapped to People table fields**
✅ **Duplicates detected and skipped**
✅ **Progress and errors clearly reported**
✅ **Final count matches expected (existing + created)**
✅ **Dry-run mode works for safe previewing**

---

## Next Steps After Import

1. **Verify in Airtable:** Check People table has expected record count
2. **Spot-check data:** Review 5-10 random records for accuracy
3. **Test Module 4:** Create a Screen record and run assessment workflow
4. **Document:** Update spec.md with actual People table count
5. **Proceed:** Begin Module 4 Python implementation (demo/agents.py)

---

## See Also

**Schema Exploration:**
- [references/schema_reference.md](references/schema_reference.md) - Complete schema exploration guide
- [references/field_types.md](references/field_types.md) - Field type catalog with validation rules

**Testing & Validation:**
- [references/testing_guide.md](references/testing_guide.md) - Complete testing & validation guide
- [scripts/validate_schema.py](scripts/validate_schema.py) - Schema validation script
- [scripts/validate_data.py](scripts/validate_data.py) - Data quality validation script

**Data Loading:**
- [references/implementation_guide.md](references/implementation_guide.md) - Technical deep-dive
- [references/troubleshooting.md](references/troubleshooting.md) - Common issues & solutions
- [scripts/load_candidates.py](scripts/load_candidates.py) - Main implementation
- [scripts/quick_load.sh](scripts/quick_load.sh) - Shell wrapper

**Project Context:**
- `spec/v1_minimal_spec.md` - Project scope (Module 4 only in v1)
- `spec/dev_reference/airtable_ai_spec.md` - People table schema
