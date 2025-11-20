---
name: demo-load
description: Load demo CSV data into Airtable with validation
---

# /demo-load - Load Demo CSV Data

Execute the complete Airtable data loading workflow for demo preparation:

## Step 1: Validate Schema (Pre-flight)

Invoke the `airtable-schema-validator` skill to verify:
- All required tables exist (People, Companies, Searches, etc.)
- Field definitions match expected schema
- Single-select options are configured
- Relationships are properly defined
- Data quality baselines are established

## Step 2: Load CSV Data

Invoke the `airtable-csv-loader` skill to:
- Load executive candidate CSV into People table
- Apply intelligent column mapping (handles 20+ variations)
- Check for duplicates before insertion
- Load associated bio files if available
- Provide dry-run preview option for safety

## Expected Behavior

**Success Path:**
1. Schema validation passes → proceed to load
2. CSV loaded with duplicate detection
3. Summary report: records added, skipped, errors

**Failure Path:**
1. Schema validation fails → report issues and exit
2. Do NOT attempt load if schema is misaligned

## Usage

```
/demo-load
```

No parameters needed - the skills will prompt for required inputs (CSV path, base ID, etc.)
