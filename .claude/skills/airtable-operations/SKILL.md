---
name: airtable-operations
description: Complete Airtable operations toolkit for FirstMark Talent Signal Agent. SCHEMA EXPLORATION - Discover bases, list tables, examine field types/constraints (single-select options, linked records), validate data requirements, and understand table relationships using MCP tools. DATA LOADING-Automate Module 1 (Candidate Sourcing) by loading executive candidates from ANY CSV file into Airtable People table with intelligent schema detection, automatic column mapping, executive bio .txt file loading, data cleaning, duplicate detection, and progress reporting. Production-ready for case presentation.
---

# Airtable Operations

## Overview

This skill provides complete Airtable operations for the FirstMark Talent Signal Agent project:
- **Schema Exploration:** Validate table schemas, field constraints, and relationships using MCP tools
- **Data Loading:** Automate Module 1 (Candidate Sourcing) by loading executive candidates from **any CSV format** into the Airtable People table

Designed for flexibility during the case presentation when data formats may vary.

**Key Features:**
- 🔄 **Flexible CSV Input:** Handles any CSV format with intelligent schema detection
- 📄 **Bio File Loading:** Automatically loads executive bios from .txt files (matches by name)
- 🧠 **Smart Column Mapping:** Maps common field name variations to Airtable schema
- ✅ **Duplicate Detection:** Skips existing candidates automatically
- 🔍 **Dry-Run Mode:** Preview changes before committing to Airtable
- 📊 **Progress Reporting:** Detailed status updates during import

**Use this skill when:**
- You need to load candidates from ANY CSV file into Airtable
- You're given surprise data during the case presentation
- You have executive bio .txt files to import alongside CSV data
- You want to automate Module 1 instead of manual data entry

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

### Step 1: Detect CSV Schema

Automatically identifies which columns map to Airtable fields:

```
📋 Step 1: Detecting CSV schema...
   Schema mapping:
     name ← full_name
     title ← title_raw
     company ← company
     linkedin_headline ← misc_liheadline
     source ← source
```

**Supported column name variations:**
- **Name:** full_name, name, executive_name, candidate_name, exec_name
- **Title:** title_raw, current_title, title, role_title, position, role
- **Company:** company, current_company, organization, employer
- **LinkedIn Headline:** misc_liheadline, linkedin_headline, headline
- **Function:** function, role_type, exec_function, normalized_function
- **Source:** source, data_source, origin

See [implementation_guide.md](references/implementation_guide.md#column-mapping) for full mapping details.

### Step 2: Read & Parse CSV

```
📖 Step 2: Reading CSV...
   Read 64 candidates
```

Handles UTF-8 encoding with BOM, filters out rows without names.

### Step 3: Load Executive Bios

```
📄 Step 3: Loading bio files...
   Found 3 .txt files
   ✅ Matched: Jonathan Carr.txt → Jonathan Carr
   ✅ Fuzzy matched: alex_rivera.txt → Alex Rivera
   ⏭️ No match: random_notes.txt
   Loaded 2 bios
```

**Bio file naming:**
- `Jonathan Carr.txt` → exact match
- `bio_alex_rivera.txt` → fuzzy match (prefix stripped)
- `Nia Patel CFO.txt` → fuzzy match (suffix ignored)

Place .txt files in same directory as CSV. Uses 80% similarity threshold for fuzzy matching.

### Step 4: Normalize Data

```
🔄 Step 4: Normalizing data...
   ✅ Normalized all candidates
```

**Normalization rules:**
- **Infer Function:** CFO, CTO, CPO, CRO, COO, CMO, CEO from title keywords
- **Fix Typos:** "FMGUildPage" → "FMGuildPage"
- **Set Added Date:** Today's date (ISO format)

See [implementation_guide.md](references/implementation_guide.md#data-normalization) for function inference logic.

### Step 5: Check Duplicates

```
🔍 Step 5: Checking for duplicates...
   🆕 62 new candidates
   ⏭️ 2 duplicates
```

Matches on exact name (case-insensitive) against existing Airtable records. Duplicates safely skipped.

### Step 6: Create Records

```
💾 Step 6: Creating records...
  ✅ 1/62: Jonathan Carr
  ✅ 2/62: Alex Rivera
  ⚠️ Skipping Normalized Function 'CPO' for Nia Patel (not in schema)
  ✅ 3/62: Nia Patel
  ...
  ✅ 62/62: Sarah Chen
```

**Field mapping:**
- **Required:** Name, Added Date
- **Optional:** Current Title, Current Company, LinkedIn Headline, LinkedIn URL, Location, Bio
- **Conditional:** Normalized Function (only CFO/CTO in demo schema), Source (only FMGuildPage/FMLinkedIN)

### Step 7: Summary Report

```
============================================================
📊 SUMMARY
============================================================
✅ Created: 62 records
⏭️ Skipped (duplicates): 2
❌ Errors: 0
============================================================

✅ Import complete! Check Airtable People table.
```

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

**Main script:**
- [scripts/load_candidates.py](scripts/load_candidates.py) - Executable Python script (451 lines)
  - CLI argument parsing
  - Flexible CSV reading
  - Intelligent schema detection
  - Bio file loading with fuzzy matching
  - Airtable integration via MCP
  - Error handling and progress reporting

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

**Data Loading:**
- [references/implementation_guide.md](references/implementation_guide.md) - Technical deep-dive
- [references/troubleshooting.md](references/troubleshooting.md) - Common issues & solutions
- [scripts/load_candidates.py](scripts/load_candidates.py) - Main implementation
- [scripts/quick_load.sh](scripts/quick_load.sh) - Shell wrapper

**Project Context:**
- `spec/v1_minimal_spec.md` - Project scope (Module 4 only in v1)
- `spec/dev_reference/airtable_ai_spec.md` - People table schema
