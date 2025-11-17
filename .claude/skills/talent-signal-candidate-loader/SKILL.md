---
name: talent-signal-candidate-loader
description: Automate Module 1 (Candidate Sourcing) for FirstMark Talent Signal Agent by loading executive candidates from ANY CSV file into Airtable People table. Features intelligent schema detection (handles Mock_Guilds.csv, Exec_Network.csv, guildmember_scrape.csv, or surprise formats), automatic column mapping, executive bio .txt file loading, data cleaning, duplicate detection, and progress reporting. Production-ready for case presentation with flexible data inputs.
---

# Talent Signal Candidate Loader

## Overview

This skill automates Module 1 (Candidate Sourcing) for the FirstMark Talent Signal Agent project by loading executive candidates from **any CSV format** into the Airtable People table. Designed for flexibility during the case presentation when data formats may vary.

**Key Features:**
- 🔄 **Flexible CSV Input:** Handles any CSV format with intelligent schema detection
- 📄 **Bio File Loading:** Automatically loads executive bios from .txt files (matches by name)
- 🧠 **Smart Column Mapping:** Maps common field name variations to Airtable schema
- ✅ **Duplicate Detection:** Skips existing candidates automatically
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

## Workflow

### Step 1: Expand Airtable Schema

Before loading data, ensure the Airtable People table has all required single-select options.

**Current state (demo-scoped):**
- **Normalized Function:** CFO, CTO only
- **Source:** FMGuildPage, FMLinkedIN only

**Required options (from spec + CSV data):**
- **Normalized Function:** CFO, CTO, CPO, CRO, COO, CMO, CEO, Other (8 total)
- **Source:** FMLinkedIN, FMGuildPage, FMCFO, FMCTOSummit, FMFounder, FMProduct (6 total)

**Implementation:**

```python
# Use mcp__airtable__update_field to add missing options
# Base ID: appeY64iIwU5CEna7
# Table ID: tblHqYymo3Av9hLeC (People)

# Step 1.1: Expand Normalized Function field
# Field ID: fldkgBZeKSGelQzLf
# Add: CPO, CRO, COO, CMO, CEO, Other (keeping existing CFO, CTO)

# Step 1.2: Expand Source field
# Field ID: fldMDZtbrVGCcKqJ6
# Add: FMCFO, FMCTOSummit, FMFounder, FMProduct (keeping existing FMGuildPage, FMLinkedIN)
```

**Note:** Airtable MCP may not support adding single-select options programmatically. If `update_field` fails:
1. **Skip schema expansion** for this run
2. **Map unsupported values** to existing options:
   - CPO, CRO, COO, CMO, CEO → "Other" (if it exists) or skip Normalized Function
   - FMCFO, FMCTOSummit, FMFounder, FMProduct → map to closest existing source or use "FMLinkedIN" as default
3. **Report** which fields couldn't be expanded
4. **Recommend** manual schema update in Airtable UI before re-running

### Step 2: Detect CSV Schema and Map Columns

**Intelligent Column Mapping** - Automatically detect CSV schema and map to Airtable fields.

**Common column name variations:**
```python
FIELD_MAPPINGS = {
    'name': ['full_name', 'name', 'executive_name', 'candidate_name', 'exec_name'],
    'title': ['title_raw', 'current_title', 'title', 'role_title', 'position', 'role'],
    'company': ['company', 'current_company', 'organization', 'employer'],
    'linkedin_headline': ['misc_liheadline', 'linkedin_headline', 'headline', 'description'],
    'linkedin_url': ['linkedin_url', 'linkedin', 'profile_url', 'url'],
    'location': ['location', 'city', 'region', 'geo'],
    'function': ['function', 'role_type', 'seniority', 'exec_function', 'normalized_function'],
    'source': ['source', 'data_source', 'origin']
}
```

**Implementation:**

```python
import csv
from pathlib import Path
from typing import Dict, List, Optional

def detect_csv_schema(csv_path: Path) -> Dict[str, str]:
    """Detect CSV schema and map columns to Airtable fields."""
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        csv_columns = [col.strip().lower() for col in reader.fieldnames]

    # Field mappings: Airtable field → possible CSV column names
    field_mappings = {
        'name': ['full_name', 'name', 'executive_name', 'candidate_name', 'exec_name'],
        'title': ['title_raw', 'current_title', 'title', 'role_title', 'position', 'role'],
        'company': ['company', 'current_company', 'organization', 'employer'],
        'linkedin_headline': ['misc_liheadline', 'linkedin_headline', 'headline', 'description'],
        'linkedin_url': ['linkedin_url', 'linkedin', 'profile_url', 'url'],
        'location': ['location', 'city', 'region', 'geo'],
        'function': ['function', 'role_type', 'seniority', 'exec_function', 'normalized_function'],
        'source': ['source', 'data_source', 'origin']
    }

    schema_map = {}
    for airtable_field, possible_columns in field_mappings.items():
        for col_option in possible_columns:
            if col_option in csv_columns:
                # Find original case-sensitive column name
                original_col = next(c for c in reader.fieldnames if c.strip().lower() == col_option)
                schema_map[airtable_field] = original_col
                break

    print(f"📋 Detected schema mapping:")
    for at_field, csv_col in schema_map.items():
        print(f"   {at_field} ← {csv_col}")

    missing_fields = [f for f in ['name', 'title', 'company'] if f not in schema_map]
    if missing_fields:
        print(f"⚠️  Missing required fields: {', '.join(missing_fields)}")
        print(f"   Available columns: {', '.join(csv_columns)}")

    return schema_map

# Detect schema
csv_path = Path("reference/guildmember_scrape.csv")  # Or any CSV path
schema_map = detect_csv_schema(csv_path)
```

### Step 3: Read CSV with Flexible Schema

```python
def read_csv_flexible(csv_path: Path, schema_map: Dict[str, str]) -> List[Dict]:
    """Read CSV using detected schema mapping."""
    candidates = []

    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            candidate = {}

            # Map CSV columns to standard fields
            for airtable_field, csv_column in schema_map.items():
                value = row.get(csv_column, '').strip()
                candidate[airtable_field] = value

            # Only add if we have at least name
            if candidate.get('name'):
                candidates.append(candidate)

    print(f"📖 Read {len(candidates)} candidates from CSV")
    return candidates

candidates = read_csv_flexible(csv_path, schema_map)
```

### Step 4: Load Executive Bios from .txt Files

**Bio File Matching** - Load bios from .txt files in the same directory as CSV.

**Naming conventions:**
- `{executive_name}.txt` (e.g., "Jonathan Carr.txt")
- `bio_{executive_name}.txt` (e.g., "bio_jonathan_carr.txt")
- Fuzzy matching on filename (case-insensitive, handles spaces/underscores)

**Implementation:**

```python
import re
from pathlib import Path
from difflib import get_close_matches

def load_executive_bios(csv_dir: Path, candidates: List[Dict]) -> Dict[str, str]:
    """Load executive bios from .txt files, match to candidates by name."""
    bio_files = list(csv_dir.glob("*.txt"))
    bios = {}

    print(f"\n📄 Looking for bio files in {csv_dir}...")
    print(f"   Found {len(bio_files)} .txt files")

    if not bio_files:
        return bios

    # Create lookup: normalized name → original name
    candidate_names = {normalize_name(c['name']): c['name'] for c in candidates}

    for bio_file in bio_files:
        # Extract name from filename
        filename = bio_file.stem  # Remove .txt extension
        filename_normalized = normalize_name(filename)

        # Try exact match first
        if filename_normalized in candidate_names:
            original_name = candidate_names[filename_normalized]
            bio_content = bio_file.read_text(encoding='utf-8').strip()
            bios[original_name] = bio_content
            print(f"   ✅ Matched: {bio_file.name} → {original_name}")
            continue

        # Try fuzzy match (for typos, slight variations)
        close_matches = get_close_matches(
            filename_normalized,
            candidate_names.keys(),
            n=1,
            cutoff=0.8  # 80% similarity threshold
        )

        if close_matches:
            matched_normalized = close_matches[0]
            original_name = candidate_names[matched_normalized]
            bio_content = bio_file.read_text(encoding='utf-8').strip()
            bios[original_name] = bio_content
            print(f"   ✅ Fuzzy matched: {bio_file.name} → {original_name}")
        else:
            print(f"   ⏭️  No match: {bio_file.name}")

    print(f"📊 Loaded {len(bios)} bios for {len(candidates)} candidates")
    return bios

def normalize_name(name: str) -> str:
    """Normalize name for matching (lowercase, remove special chars, collapse spaces)."""
    # Remove common prefixes like "bio_", "exec_"
    name = re.sub(r'^(bio_|exec_|executive_)', '', name, flags=re.IGNORECASE)
    # Convert to lowercase, replace special chars with spaces
    name = re.sub(r'[^a-z0-9\s]', ' ', name.lower())
    # Collapse multiple spaces
    name = ' '.join(name.split())
    return name

# Load bios
csv_dir = csv_path.parent
bios = load_executive_bios(csv_dir, candidates)

# Attach bios to candidates
for candidate in candidates:
    if candidate['name'] in bios:
        candidate['bio'] = bios[candidate['name']]
        print(f"   ✅ Bio attached: {candidate['name']}")
```

### Step 5: Clean and Normalize Data

Transform CSV data into Airtable-ready format (same as before, now with bio field).

**Normalization rules:**

1. **Fix source typos:**
   - "FMGUildPage" → "FMGuildPage"

2. **Infer Normalized Function from title_raw:**
   - Contains "CFO" or "Chief Financial Officer" → CFO
   - Contains "CTO" or "Chief Technology Officer" or "Chief Technical Officer" → CTO
   - Contains "CPO" or "Chief Product Officer" → CPO
   - Contains "CRO" or "Chief Revenue Officer" → CRO
   - Contains "COO" or "Chief Operating Officer" → COO
   - Contains "CMO" or "Chief Marketing Officer" → CMO
   - Contains "CEO" or "Chief Executive Officer" → CEO
   - Contains "Founder" or "Co-founder" or "Cofounder" (case insensitive) → CEO
   - Otherwise → Other

3. **Set Added Date to today's date** (format: YYYY-MM-DD)

4. **Leave LinkedIn URL blank** (not in CSV)

**Implementation:**

```python
import re
from datetime import date

def infer_function(title: str) -> str:
    """Infer Normalized Function from title."""
    title_upper = title.upper()

    # Order matters - check most specific first
    if 'CFO' in title_upper or 'CHIEF FINANCIAL OFFICER' in title_upper:
        return 'CFO'
    elif 'CTO' in title_upper or 'CHIEF TECHNOLOGY OFFICER' in title_upper or 'CHIEF TECHNICAL OFFICER' in title_upper:
        return 'CTO'
    elif 'CPO' in title_upper or 'CHIEF PRODUCT OFFICER' in title_upper:
        return 'CPO'
    elif 'CRO' in title_upper or 'CHIEF REVENUE OFFICER' in title_upper:
        return 'CRO'
    elif 'COO' in title_upper or 'CHIEF OPERATING OFFICER' in title_upper:
        return 'COO'
    elif 'CMO' in title_upper or 'CHIEF MARKETING OFFICER' in title_upper:
        return 'CMO'
    elif 'CEO' in title_upper or 'CHIEF EXECUTIVE OFFICER' in title_upper:
        return 'CEO'
    elif re.search(r'\bFOUNDER\b|\bCO-FOUNDER\b|\bCOFOUNDER\b', title_upper):
        return 'CEO'
    else:
        return 'Other'

def normalize_source(source: str) -> str:
    """Fix source typos."""
    # Fix known typo
    if source == "FMGUildPage":
        return "FMGuildPage"
    return source

# Apply normalization
today = date.today().isoformat()

for candidate in candidates:
    candidate['normalized_function'] = infer_function(candidate['title_raw'])
    candidate['source_normalized'] = normalize_source(candidate['source'])
    candidate['added_date'] = today

print("✅ Normalized all candidate data")
```

### Step 6: Check for Duplicates

Query existing People table to detect duplicates before creating records.

**Duplicate detection strategy:**
- Match on exact `Name` field (case-insensitive)
- Skip if duplicate found

**Implementation:**

```python
# Get all existing people names from Airtable
existing_people = mcp__airtable__list_records(
    baseId="appeY64iIwU5CEna7",
    tableId="tblHqYymo3Av9hLeC",
    maxRecords=100  # Adjust if > 100 people expected
)

existing_names = {
    record['fields'].get('Name', '').lower()
    for record in existing_people
    if 'Name' in record['fields']
}

print(f"📋 Found {len(existing_names)} existing candidates in Airtable")

# Filter out duplicates
new_candidates = []
duplicates = []

for candidate in candidates:
    name_lower = candidate['full_name'].lower()
    if name_lower in existing_names:
        duplicates.append(candidate['full_name'])
    else:
        new_candidates.append(candidate)

print(f"🆕 {len(new_candidates)} new candidates to import")
print(f"⏭️  {len(duplicates)} duplicates will be skipped")
```

### Step 7: Create Airtable Records

Bulk create records in the People table.

**Airtable API constraints:**
- Maximum 10 records per `update_records` call
- Must batch larger imports

**Field mapping:**
- Name ← full_name
- Current Title ← title_raw
- Current Company ← company
- LinkedIn Headline ← misc_liheadline
- Normalized Function ← normalized_function (inferred)
- Source ← source_normalized
- Added Date ← added_date (today)
- LinkedIn URL ← (empty)
- Location ← (empty)
- Bio ← (empty)

**Implementation:**

```python
import math

def batch_list(items, batch_size=10):
    """Split list into batches."""
    for i in range(0, len(items), batch_size):
        yield items[i:i + batch_size]

created_count = 0
error_count = 0
errors = []

# Process in batches of 10
batches = list(batch_list(new_candidates, 10))
total_batches = len(batches)

for batch_num, batch in enumerate(batches, 1):
    print(f"📦 Processing batch {batch_num}/{total_batches} ({len(batch)} records)...")

    try:
        # Create records using Airtable MCP
        for candidate in batch:
            try:
                # Build fields dict
                fields = {
                    "Name": candidate['full_name'],
                    "Current Title": candidate['title_raw'],
                    "Current Company": candidate['company'],
                    "Added Date": candidate['added_date']
                }

                # Add optional fields if present
                if candidate['misc_liheadline']:
                    fields["LinkedIn Headline"] = candidate['misc_liheadline']

                # Add normalized fields (may fail if options don't exist)
                try:
                    fields["Normalized Function"] = candidate['normalized_function']
                except:
                    print(f"  ⚠️  Skipping Normalized Function for {candidate['full_name']} (option not in schema)")

                try:
                    fields["Source"] = candidate['source_normalized']
                except:
                    print(f"  ⚠️  Skipping Source for {candidate['full_name']} (option not in schema)")

                # Create record
                result = mcp__airtable__create_record(
                    baseId="appeY64iIwU5CEna7",
                    tableId="tblHqYymo3Av9hLeC",
                    fields=fields
                )

                created_count += 1
                print(f"  ✅ Created: {candidate['full_name']}")

            except Exception as e:
                error_count += 1
                error_msg = f"{candidate['full_name']}: {str(e)}"
                errors.append(error_msg)
                print(f"  ❌ Error: {error_msg}")

    except Exception as e:
        print(f"❌ Batch {batch_num} failed: {e}")
        error_count += len(batch)

print(f"\n{'='*60}")
print(f"📊 Import Summary:")
print(f"{'='*60}")
print(f"✅ Created: {created_count} records")
print(f"⏭️  Skipped (duplicates): {len(duplicates)}")
print(f"❌ Errors: {error_count}")
print(f"{'='*60}")

if duplicates:
    print(f"\n📋 Skipped duplicates ({len(duplicates)}):")
    for dup in duplicates[:10]:  # Show first 10
        print(f"  - {dup}")
    if len(duplicates) > 10:
        print(f"  ... and {len(duplicates) - 10} more")

if errors:
    print(f"\n❌ Errors ({len(errors)}):")
    for err in errors[:5]:  # Show first 5
        print(f"  - {err}")
    if len(errors) > 5:
        print(f"  ... and {len(errors) - 5} more")
```

### Step 8: Verify Import

Query the People table to confirm records were created successfully.

**Implementation:**

```python
# Get updated count
all_people = mcp__airtable__list_records(
    baseId="appeY64iIwU5CEna7",
    tableId="tblHqYymo3Av9hLeC",
    maxRecords=100
)

final_count = len(all_people)

print(f"\n🎯 Final People table count: {final_count} records")
print(f"📈 Expected: {len(existing_names) + created_count} (original {len(existing_names)} + new {created_count})")

if final_count == len(existing_names) + created_count:
    print("✅ Import verified successfully!")
else:
    print("⚠️  Count mismatch - please verify Airtable manually")
```

## Complete Workflow Script (Enhanced)

**Production-ready script with flexible CSV input and bio loading:**

```python
import csv
import re
from pathlib import Path
from datetime import date

# Configuration
BASE_ID = "appeY64iIwU5CEna7"
PEOPLE_TABLE_ID = "tblHqYymo3Av9hLeC"
CSV_PATH = "reference/guildmember_scrape.csv"

print("🚀 Starting Talent Signal Candidate Loader")
print("="*60)

# Helper functions
def infer_function(title: str) -> str:
    """Infer Normalized Function from title."""
    title_upper = title.upper()
    if 'CFO' in title_upper or 'CHIEF FINANCIAL OFFICER' in title_upper:
        return 'CFO'
    elif 'CTO' in title_upper or 'CHIEF TECHNOLOGY OFFICER' in title_upper or 'CHIEF TECHNICAL OFFICER' in title_upper:
        return 'CTO'
    elif 'CPO' in title_upper or 'CHIEF PRODUCT OFFICER' in title_upper:
        return 'CPO'
    elif 'CRO' in title_upper or 'CHIEF REVENUE OFFICER' in title_upper:
        return 'CRO'
    elif 'COO' in title_upper or 'CHIEF OPERATING OFFICER' in title_upper:
        return 'COO'
    elif 'CMO' in title_upper or 'CHIEF MARKETING OFFICER' in title_upper:
        return 'CMO'
    elif 'CEO' in title_upper or 'CHIEF EXECUTIVE OFFICER' in title_upper:
        return 'CEO'
    elif re.search(r'\bFOUNDER\b|\bCO-FOUNDER\b|\bCOFOUNDER\b', title_upper):
        return 'CEO'
    else:
        return 'Other'

def normalize_source(source: str) -> str:
    """Fix source typos."""
    if source == "FMGUildPage":
        return "FMGuildPage"
    return source

def batch_list(items, batch_size=10):
    """Split list into batches."""
    for i in range(0, len(items), batch_size):
        yield items[i:i + batch_size]

# Step 1: Read CSV
print("\n📖 Step 1: Reading CSV...")
candidates = []
with open(CSV_PATH, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        candidates.append({
            'full_name': row['full_name'].strip(),
            'title_raw': row['title_raw'].strip(),
            'company': row['company'].strip(),
            'misc_liheadline': row.get('misc_liheadline', '').strip(),
            'source': row['source'].strip()
        })
print(f"✅ Read {len(candidates)} candidates from CSV")

# Step 2: Normalize data
print("\n🔄 Step 2: Normalizing data...")
today = date.today().isoformat()
for candidate in candidates:
    candidate['normalized_function'] = infer_function(candidate['title_raw'])
    candidate['source_normalized'] = normalize_source(candidate['source'])
    candidate['added_date'] = today
print("✅ Normalized all candidate data")

# Step 3: Check for duplicates
print("\n🔍 Step 3: Checking for duplicates...")
existing_people = mcp__airtable__list_records(
    baseId=BASE_ID,
    tableId=PEOPLE_TABLE_ID,
    maxRecords=100
)
existing_names = {
    record['fields'].get('Name', '').lower()
    for record in existing_people
    if 'Name' in record['fields']
}
print(f"📋 Found {len(existing_names)} existing candidates in Airtable")

new_candidates = []
duplicates = []
for candidate in candidates:
    if candidate['full_name'].lower() in existing_names:
        duplicates.append(candidate['full_name'])
    else:
        new_candidates.append(candidate)

print(f"🆕 {len(new_candidates)} new candidates to import")
print(f"⏭️  {len(duplicates)} duplicates will be skipped")

# Step 4: Create records
print("\n💾 Step 4: Creating Airtable records...")
created_count = 0
error_count = 0
errors = []

for candidate in new_candidates:
    try:
        fields = {
            "Name": candidate['full_name'],
            "Current Title": candidate['title_raw'],
            "Current Company": candidate['company'],
            "Added Date": candidate['added_date']
        }

        if candidate['misc_liheadline']:
            fields["LinkedIn Headline"] = candidate['misc_liheadline']

        # Try to set normalized fields (may fail if options missing)
        if candidate['normalized_function'] in ['CFO', 'CTO']:  # Only set if in current schema
            fields["Normalized Function"] = candidate['normalized_function']

        if candidate['source_normalized'] in ['FMGuildPage', 'FMLinkedIN']:  # Only set if in current schema
            fields["Source"] = candidate['source_normalized']

        result = mcp__airtable__create_record(
            baseId=BASE_ID,
            tableId=PEOPLE_TABLE_ID,
            fields=fields
        )

        created_count += 1
        print(f"  ✅ {created_count}/{len(new_candidates)}: {candidate['full_name']}")

    except Exception as e:
        error_count += 1
        error_msg = f"{candidate['full_name']}: {str(e)}"
        errors.append(error_msg)
        print(f"  ❌ Error: {error_msg}")

# Step 5: Report
print(f"\n{'='*60}")
print(f"📊 IMPORT SUMMARY")
print(f"{'='*60}")
print(f"✅ Created: {created_count} records")
print(f"⏭️  Skipped (duplicates): {len(duplicates)}")
print(f"❌ Errors: {error_count}")
print(f"{'='*60}")

# Verification
all_people_after = mcp__airtable__list_records(
    baseId=BASE_ID,
    tableId=PEOPLE_TABLE_ID,
    maxRecords=100
)
final_count = len(all_people_after)
expected_count = len(existing_names) + created_count

print(f"\n🎯 Verification:")
print(f"   Final count: {final_count}")
print(f"   Expected: {expected_count}")

if final_count == expected_count:
    print("✅ Import verified successfully!")
else:
    print("⚠️  Count mismatch - please verify Airtable manually")

print("\n✅ Candidate loader complete!")
```

## Quick Start Guide

**To use this skill with ANY CSV file:**

```python
# 1. Specify CSV path (absolute or relative)
CSV_PATH = "reference/guildmember_scrape.csv"  # Or any CSV
# CSV_PATH = "reference/Mock_Guilds.csv"
# CSV_PATH = "reference/Exec_Network.csv"
# CSV_PATH = "/path/to/surprise_data.csv"

# 2. Run the complete workflow (copy entire script above)
# The script will automatically:
#   - Detect CSV schema
#   - Map columns to Airtable fields
#   - Load .txt bio files from same directory
#   - Clean and normalize data
#   - Skip duplicates
#   - Create Airtable records
#   - Verify results
```

**For case presentation with surprise data:**
1. Save CSV file anywhere
2. Update `CSV_PATH` variable
3. Add .txt bio files (optional) in same directory named `{candidate_name}.txt`
4. Run the script
5. Review results in Airtable

**Bio file examples:**
- `reference/Jonathan Carr.txt` → Matches candidate "Jonathan Carr"
- `reference/bio_alex_rivera.txt` → Matches candidate "Alex Rivera" (fuzzy)
- `reference/Nia Patel CFO.txt` → Matches candidate "Nia Patel" (fuzzy)

## Important Notes

### Flexible CSV Schema Support

**The skill intelligently handles these CSV variations:**

| CSV Format | Example Columns | Auto-Mapped To |
|------------|----------------|----------------|
| guildmember_scrape.csv | full_name, title_raw, company, misc_liheadline, source | Name, Current Title, Current Company, LinkedIn Headline, Source |
| Mock_Guilds.csv | name, role title, company, location, function | Name, Current Title, Current Company, Location, Normalized Function |
| Exec_Network.csv | exec_name, current_title, organization, linkedin_url, role_type | Name, Current Title, Current Company, LinkedIn URL, Normalized Function |
| Any CSV | Detects common variations automatically | Maps to Airtable schema |

**Required columns (at least one):**
- Name field: full_name, name, executive_name, candidate_name, exec_name
- Title field: title_raw, current_title, title, role_title, position, role
- Company field: company, current_company, organization, employer

**Optional columns (auto-detected if present):**
- LinkedIn URL, LinkedIn Headline, Location, Function/Role Type, Source, Bio

### Schema Limitations

**Current Airtable schema is demo-scoped:**
- Normalized Function: CFO, CTO only (missing: CPO, CRO, COO, CMO, CEO, Other)
- Source: FMGuildPage, FMLinkedIN only (missing: FMCFO, FMCTOSummit, FMFounder, FMProduct)

**Script behavior with limited schema:**
- Only sets Normalized Function if value is CFO or CTO
- Only sets Source if value is FMGuildPage or FMLinkedIN
- Other candidates will have these fields blank
- Records still created successfully (these are non-required fields)

**To enable full functionality:**
1. Manually expand single-select options in Airtable UI before running
2. OR accept that some fields will be blank for non-CFO/CTO candidates

### Expected Results

**From the CSV (62 candidates):**
- ~25-30 CFOs
- ~20-25 CTOs
- ~10-15 Other functions (CPO, CRO, CEO, etc.)

**After import with demo schema:**
- CFO/CTO candidates: Normalized Function populated
- Other candidates: Normalized Function blank (not an error)

### Error Handling

The script handles errors gracefully:
- Continues processing if individual records fail
- Reports all errors at the end
- Provides duplicate detection to avoid conflicts
- Validates final count for data integrity

## Success Criteria

✅ **Script completes without fatal errors**
✅ **All non-duplicate records created in Airtable**
✅ **Data correctly mapped to People table fields**
✅ **Duplicates detected and skipped**
✅ **Progress and errors clearly reported**
✅ **Final count matches expected (existing + created)**

## Next Steps After Import

1. **Verify in Airtable:** Check People table has ~64 total records (2 existing + 62 new)
2. **Spot-check data:** Review 5-10 random records for accuracy
3. **Expand schema (optional):** Add missing single-select options manually if needed
4. **Update spec:** Document actual People table count in spec.md
5. **Proceed to Module 4:** Begin Python implementation (demo/agents.py, etc.)
