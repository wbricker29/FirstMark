# Troubleshooting Guide: Airtable Candidate Loader

## Table of Contents

- [Common Issues & Solutions](#common-issues--solutions)
  - [1. CSV File Not Found](#1-csv-file-not-found)
  - [2. Missing Required CSV Columns](#2-missing-required-csv-columns)
  - [3. Airtable MCP Not Available](#3-airtable-mcp-not-available)
  - [4. Single-Select Option Not in Schema](#4-single-select-option-not-in-schema)
  - [5. Duplicate Candidates Skipped](#5-duplicate-candidates-skipped)
  - [6. Bio Files Not Matching](#6-bio-files-not-matching)
  - [7. Import Partially Succeeds](#7-import-partially-succeeds)
  - [8. Rate Limit Exceeded](#8-rate-limit-exceeded)
  - [9. Schema Detection Incorrect](#9-schema-detection-incorrect)
  - [10. Dry Run Shows Wrong Data](#10-dry-run-shows-wrong-data)
  - [11. Schema Exploration Issues](#11-schema-exploration-issues)
- [Emergency Procedures](#emergency-procedures)
  - [Demo Day Issue: Can't Load Candidates](#demo-day-issue-cant-load-candidates)
- [Getting Help](#getting-help)
  - [Debug Checklist](#debug-checklist)
  - [Verbose Output](#verbose-output)
  - [Logs to Share](#logs-to-share)
- [See Also](#see-also)

## Common Issues & Solutions

### 1. CSV File Not Found

**Error:**
```
❌ ERROR: CSV file not found: 
```

**Causes:**
- Incorrect file path
- File moved/renamed
- Running from wrong directory

**Solutions:**
```bash
# Use absolute path
python load_candidates.py /full/path/to/file.csv

# Or navigate to correct directory first
cd /path/to/project
python .claude/skills/airtable-file-loader/scripts/load_candidates.py 
```

---

### 2. Missing Required CSV Columns

**Error:**
```
⚠️ Missing required fields: name, title
CSV may not be compatible
```

**Causes:**
- CSV doesn't have recognizable name/title/company columns
- Column names don't match any field mapping variations

**Solutions:**

**Option A: Rename CSV columns**
Edit CSV to use recognized column names:
```csv
# Before:
exec_full_name,job_title,employer
# After:
full_name,title,company
```

**Option B: Add to field mappings**
Edit `scripts/load_candidates.py`:
```python
FIELD_MAPPINGS = {
    'name': ['full_name', 'name', 'exec_full_name'],  # Add custom variant
    'title': ['title_raw', 'current_title', 'job_title'],  # Add custom variant
    # ...
}
```

---

### 3. Airtable MCP Not Available

**Error:**
```
❌ ERROR: Airtable MCP not available
   Install Airtable MCP server to create records
```

**Causes:**
- Airtable MCP server not installed
- MCP server not running
- Claude Code not configured for MCP

**Solutions:**

**Step 1: Check MCP installation**
```bash
# Look for airtable in MCP config
cat ~/.config/claude/mcp_settings.json | grep airtable
```

**Step 2: Verify Airtable MCP configured**
```json
{
  "mcpServers": {
    "airtable": {
      "command": "npx",
      "args": ["-y", "@airtable-mcp/server"],
      "env": {
        "AIRTABLE_API_KEY": "your_key_here"
      }
    }
  }
}
```

**Step 3: Restart Claude Code**
After configuration changes, restart Claude Code to load MCP servers.

---

### 4. Single-Select Option Not in Schema

**Warning (non-fatal):**
```
⚠️ Skipping Normalized Title 'CPO' for Alex Rivera (not in schema)
```

**Causes:**
- Demo Airtable schema only has CFO, CTO options
- CSV contains other functions (CPO, CRO, COO, CMO, CEO)

**Solutions:**

**Option A: Accept limited data (recommended for demo)**
- Non-CFO/CTO candidates will have blank Normalized Title
- Records still created successfully
- Can manually update in Airtable UI after import

**Option B: Expand Airtable schema (pre-demo setup)**
1. Open Airtable People table
2. Click Normalized Title column header
3. Select "Edit field"
4. Add missing options: CPO, CRO, COO, CMO, CEO, Other
5. Re-run loader script

**Option C: Update valid options in script**
Edit `scripts/load_candidates.py`:
```python
# Expand valid options to match your Airtable schema
VALID_FUNCTIONS = {'CFO', 'CTO', 'CPO', 'CRO', 'COO', 'CMO', 'CEO', 'Other'}
VALID_SOURCES = {'FMGuildPage', 'FMLinkedIN', 'FMCFO', 'FMCTOSummit'}
```

---

### 5. Duplicate Candidates Skipped

**Output:**
```
⏭️ 10 duplicates will be skipped
```

**Causes:**
- Candidates already exist in Airtable (matching Name field)
- CSV contains duplicate rows
- Re-running loader without clearing previous import

**Solutions:**

**If expected (re-running script):**
- No action needed - duplicates safely skipped

**If unexpected (should be new candidates):**
```bash
# Check Airtable for existing records
# 1. Open People table in Airtable
# 2. Filter by Added Date = today
# 3. Review records - delete if needed

# Re-run loader
python load_candidates.py 
```

**To force re-import:**
1. Delete existing records in Airtable
2. Re-run loader script

---

### 6. Bio Files Not Matching

**Output:**
```
📄 Loaded 0 bios for 64 candidates
```

**Causes:**
- Bio .txt files not in same directory as CSV
- Filename doesn't match candidate name closely enough
- Bio files have wrong extension (not .txt)

**Solutions:**

**Step 1: Check file location**
```bash
# Bio files must be in SAME directory as CSV
ls reference/*.txt
# Expected: Jonathan Carr.txt, Alex Rivera.txt, etc.
```

**Step 2: Check filename matching**
```bash
# Good matches:
Jonathan Carr.txt → candidate "Jonathan Carr" ✅
alex_rivera.txt → candidate "Alex Rivera" ✅
bio_nia_patel.txt → candidate "Nia Patel" ✅

# Poor matches (won't work):
j_carr.txt → candidate "Jonathan Carr" ❌ (too different)
exec.txt → candidate "Jonathan Carr" ❌ (no name)
```

**Step 3: Run with verbose to debug**
```bash
python load_candidates.py  --dry-run --verbose

# Output shows matching attempts:
#   ✅ Matched: Jonathan Carr.txt → Jonathan Carr
#   ✅ Fuzzy matched: alex_rivera.txt → Alex Rivera
#   ⏭️ No match: random_bio.txt
```

---

### 7. Import Partially Succeeds

**Output:**
```
✅ Created: 50 records
❌ Errors: 14
```

**Causes:**
- Some candidates have invalid data
- Airtable field validation failures
- Network issues during import

**Solutions:**

**Step 1: Review error messages**
```bash
# Run with verbose to see specific errors
python load_candidates.py  --verbose

# Example error:
# ❌ Error: John Smith: Invalid URL format for LinkedIn URL
```

**Step 2: Fix data issues**
- Clean CSV of problematic records
- Validate URLs, dates, required fields
- Re-run for failed candidates only

**Step 3: Check partial import**
```bash
# Query Airtable
# Filter People by Added Date = today
# Verify 50 records created (not 64)

# Extract failed candidates from error log
# Create new CSV with just those 14
# Fix data issues
# Re-run loader
```

---

### 8. Rate Limit Exceeded

**Error:**
```
❌ Error: Jane Doe: 429 Too Many Requests
```

**Causes:**
- Airtable API rate limit hit (5 requests/second)
- Running multiple import scripts simultaneously

**Solutions:**

**Option A: Add retry logic (code modification)**
```python
import time
from requests.exceptions import HTTPError

def create_with_retry(base_id, table_id, fields, max_retries=3):
    for attempt in range(max_retries):
        try:
            return mcp__airtable__create_record(base_id, table_id, fields)
        except HTTPError as e:
            if e.response.status_code == 429 and attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"   Rate limited, waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise
```

**Option B: Reduce load**
- Import smaller batches (<50 candidates at a time)
- Add delays between API calls
- Run during off-peak hours

---

### 9. Schema Detection Incorrect

**Output:**
```
📋 Schema mapping:
   name ← full_name
   title ← misc_liheadline  ← WRONG
   company ← title_raw      ← WRONG
```

**Causes:**
- CSV has non-standard column order
- Column names partially match multiple field mappings
- First match not the best match

**Solutions:**

**Option A: Rename CSV columns**
Use standard column names (full_name, title_raw, company)

**Option B: Adjust field mapping priority**
Edit `FIELD_MAPPINGS` in `scripts/load_candidates.py`:
```python
FIELD_MAPPINGS = {
    # Put more specific names first
    'title': ['title_raw', 'current_title', 'title'],  # 'title_raw' checked first
    'company': ['company', 'current_company', 'organization'],
}
```

**Option C: Manual mapping**
Create a custom loader script with explicit mapping:
```python
schema_map = {
    'name': 'exec_name',
    'title': 'job_title',
    'company': 'employer'
}
```

---

### 10. Dry Run Shows Wrong Data

**Output:**
```
🔍 DRY RUN MODE
   Would create 64 records:
     - John Smith (Chief Executive Officer)  ← Should be CFO?
```

**Causes:**
- CSV data incorrect (not a script issue)
- Schema detection mapped wrong columns

**Solutions:**

**Step 1: Verify CSV data**
```bash
head -5 
# Check: Is "Chief Executive Officer" actually in the title column?
```

**Step 2: Check schema mapping**
```bash
python load_candidates.py  --dry-run --verbose

# Look for:
# 📋 Detected schema mapping:
#    title ← correct_column_name?
```

**Step 3: Fix before live import**
- Clean CSV data if needed
- Adjust column mappings if needed
- Re-run dry-run to verify

---

### 11. Schema Exploration Issues

**Use case:** Troubleshooting schema validation before data loading

#### Issue 11.1: "Invalid value for single-select field"

**Error:**
```
❌ INVALID_VALUE_FOR_COLUMN: Field "Status" cannot accept value "active"
```

**Cause:** Value doesn't match schema options exactly (case-sensitive)

**Solution:**
```bash
# Step 1: Get schema to see valid options
mcp__airtable__describe_table({
  baseId: "appeY64iIwU5CEna7",
  tableId: "People"
})

# Step 2: Extract valid options from field definition
# Look for field "Status" in response, check options.choices

# Step 3: Update your data to match exact option
# Schema: ["Active", "Inactive"]
# Your value: "active" ❌
# Correct: "Active" ✅
```

**Prevention:**
Always call `describe_table` before creating records to validate against current schema.

#### Issue 11.2: "Field not found"

**Error:**
```
❌ UNKNOWN_FIELD_NAME: Unknown field name: "Normalized Title"
```

**Cause:** Using field name that doesn't exist or has typo

**Solution:**
```bash
# Step 1: List all fields in table
mcp__airtable__describe_table({
  baseId: "appeY64iIwU5CEna7",
  tableId: "People"
})

# Step 2: Find correct field name (check spelling and case)
# Common mistakes:
# - Extra spaces: "Normalized  Function" vs "Normalized Title"
# - Wrong case: "Normalized Title" vs "Normalized Title"
# - Using field ID instead of name: "fldXXX" vs "Normalized Title"

# Step 3: Use exact field name from schema
```

**Best practice:** Use field names (not IDs) and match exactly as shown in schema.

#### Issue 11.3: "Linked record ID not found"

**Error:**
```
❌ INVALID_RECORD_ID: Record recXXXXXXXXXXXXXX not found in target table
```

**Cause:** Using invalid or non-existent record ID in linked record field

**Solution:**
```bash
# Step 1: Verify record exists
mcp__airtable__list_records({
  baseId: "appeY64iIwU5CEna7",
  tableId: "Portco",
  filterByFormula: "RECORD_ID() = 'recXXXXXXXXXXXXXX'"
})

# Step 2: If not found, search by name to get correct ID
mcp__airtable__list_records({
  baseId: "appeY64iIwU5CEna7",
  tableId: "Portco",
  filterByFormula: "{Company Name} = 'Pigment'"
})

# Step 3: Use correct record ID from response
```

**Common mistakes:**
- Using company name instead of record ID: `["Pigment"]` ❌
- Correct: `["recXXXXXXXXXXXXXX"]` ✅

#### Issue 11.4: "Date format invalid"

**Error:**
```
❌ INVALID_VALUE_FOR_COLUMN: "11/17/2025" is not a valid date
```

**Cause:** Date not in ISO 8601 format

**Solution:**
```python
from datetime import datetime

# For date fields (YYYY-MM-DD)
date_value = datetime.strptime("11/17/2025", "%m/%d/%Y").strftime("%Y-%m-%d")
# Result: "2025-11-17"

# For datetime fields (ISO 8601 with UTC)
datetime_value = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z")
# Result: "2025-11-17T15:30:45.000Z"
```

**Format requirements:**
- **Date:** `YYYY-MM-DD` (e.g., `"2025-11-17"`)
- **DateTime:** `YYYY-MM-DDTHH:mm:ss.sssZ` (e.g., `"2025-11-17T15:30:45.000Z"`)

#### Issue 11.5: "Cannot find base or table"

**Error:**
```
❌ NOT_FOUND: Could not find base appXXXXXXXXXXXXXX
```

**Cause:** Invalid base ID or insufficient permissions

**Solution:**
```bash
# Step 1: List all accessible bases
mcp__airtable__list_bases()

# Step 2: Verify base ID from response
# Correct format: "appXXXXXXXXXXXXXX" (14 characters after "app")

# Step 3: Check permissions
# - Verify Airtable API key has access to base
# - Check base sharing settings
```

**For table errors:**
```bash
# List tables in base
mcp__airtable__list_tables({baseId: "appeY64iIwU5CEna7"})

# Use exact table name or ID from response
```

#### Issue 11.6: MCP Schema Tools Not Available

**Error:**
```
❌ Tool 'mcp__airtable__describe_table' not found
```

**Cause:** Airtable MCP server not configured or running

**Solution:**
See [Issue 3: Airtable MCP Not Available](#3-airtable-mcp-not-available) for complete MCP setup instructions.

**Quick check:**
```bash
# Verify MCP configuration
cat ~/.config/claude/mcp_settings.json | grep airtable

# Restart Claude Code after any config changes
```

**Additional Resources:**
- [Schema Exploration Reference](schema_reference.md) - Complete MCP operations guide
- [Field Types Reference](field_types.md) - Field type validation rules

---

## Emergency Procedures

### Demo Day Issue: Can't Load Candidates

**Scenario:** 5 minutes before demo, loader fails.

**Fallback Plan:**

1. **Skip automation, use Airtable UI**
   - Manually create 2-3 candidate records
   - Demonstrate Module 4 (Screen workflow) with existing data
   - Mention "Module 1 automation available but focusing on core agent"

2. **Use pre-loaded demo data**
   - Keep 4-5 candidates always in Airtable
   - Demo Screen workflow with those candidates
   - Skip showing Module 1 loader

3. **Quick diagnostic (30 seconds)**
   ```bash
   # Test basic functionality
   python load_candidates.py  --dry-run

   # If works → run live
   # If fails → fallback plan
   ```

---

## Getting Help

### Debug Checklist

Before asking for help, verify:

- [ ] CSV file exists and path is correct
- [ ] CSV has recognizable column names (name, title, company variants)
- [ ] Airtable MCP configured and running
- [ ] Running from correct directory
- [ ] Python 3.11+ installed (`python --version`)
- [ ] Required packages installed (`csv`, `re`, `pathlib`, `difflib`, `datetime`, `argparse`)

### Verbose Output

Always include verbose output when reporting issues:

```bash
python load_candidates.py path/to/file.csv --dry-run --verbose > debug.log 2>&1
```

### Logs to Share

- Full command used
- Verbose output (`--verbose` flag)
- CSV file structure (first 5 rows)
- Airtable schema (screenshot of People table fields)
- Python version (`python --version`)

---

## See Also

**Schema Exploration:**
- [schema_reference.md](schema_reference.md) - Complete schema exploration guide
- [field_types.md](field_types.md) - Field type catalog with validation rules

**Data Loading:**
- [implementation_guide.md](implementation_guide.md) - Detailed technical documentation
- [../SKILL.md](../SKILL.md) - Skill overview and quick start
- [../scripts/load_candidates.py](../scripts/load_candidates.py) - Main implementation
