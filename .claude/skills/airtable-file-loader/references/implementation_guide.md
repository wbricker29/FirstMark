# Implementation Guide: Airtable Candidate Loader

## Table of Contents

1. [Schema Detection](#schema-detection)
2. [Column Mapping](#column-mapping)
3. [Data Normalization](#data-normalization)
4. [Bio File Loading](#bio-file-loading)
5. [Duplicate Detection](#duplicate-detection)
6. [Record Creation](#record-creation)

---

## Schema Detection

The loader automatically detects CSV schema and maps columns to Airtable fields using intelligent matching.

### Field Mappings

| Airtable Field | Possible CSV Column Names |
|----------------|---------------------------|
| Name | full_name, name, executive_name, candidate_name, exec_name |
| Current Title | title_raw, current_title, title, role_title, position, role |
| Current Company | company, current_company, organization, employer |
| LinkedIn Headline | misc_liheadline, linkedin_headline, headline, description |
| LinkedIn URL | linkedin_url, linkedin, profile_url, url |
| Location | location, city, region, geo |
| Normalized Function | function, role_type, seniority, exec_function, normalized_function |
| Source | source, data_source, origin |
| Bio | bio, biography, background, summary |

### Detection Algorithm

1. Read CSV headers with UTF-8-sig encoding (handles BOM)
2. Normalize column names to lowercase
3. Match against field mapping dictionary (first match wins)
4. Build schema map: `{airtable_field: csv_column_name}`
5. Validate required fields present (name, title, company)

### Example

**Input CSV:** `guildmember_scrape.csv`
```csv
full_name,title_raw,company,misc_liheadline,source
John Smith,CFO,Acme Corp,Finance leader,FMGuildPage
```

**Detected Schema:**
```python
{
    'name': 'full_name',
    'title': 'title_raw',
    'company': 'company',
    'linkedin_headline': 'misc_liheadline',
    'source': 'source'
}
```

---

## Column Mapping

### Flexible CSV Support

The loader handles various CSV formats commonly encountered:

**Format 1: Guild Member Scrape**
```csv
full_name,title_raw,company,misc_liheadline,source
```

**Format 2: Mock Guilds**
```csv
name,role title,company,location,function
```

**Format 3: Exec Network**
```csv
exec_name,current_title,organization,linkedin_url,role_type
```

### Mapping Strategy

1. **Case-insensitive matching** - `Full_Name` matches `full_name`
2. **First match wins** - Prioritizes more specific names (e.g., `title_raw` over `title`)
3. **Optional fields gracefully handled** - Missing columns result in empty values
4. **Row-level tracking** - Each candidate includes `_row_num` for debugging

---

## Data Normalization

### Function Inference

Automatically infers `Normalized Function` from job titles:

| Title Contains | Inferred Function |
|----------------|-------------------|
| CFO, Chief Financial Officer | CFO |
| CTO, Chief Technology Officer, Chief Technical Officer | CTO |
| CPO, Chief Product Officer | CPO |
| CRO, Chief Revenue Officer | CRO |
| COO, Chief Operating Officer | COO |
| CMO, Chief Marketing Officer | CMO |
| CEO, Chief Executive Officer | CEO |
| Founder, Co-founder, Cofounder | CEO |
| (anything else) | Other |

**Implementation:**
```python
def infer_function(title: str) -> str:
    title_upper = title.upper()

    if 'CFO' in title_upper or 'CHIEF FINANCIAL OFFICER' in title_upper:
        return 'CFO'
    elif 'CTO' in title_upper or ...:
        return 'CTO'
    # ... (see load_candidates.py for full logic)
    else:
        return 'Other'
```

### Source Normalization

Fixes known typos in source field:

| Input | Normalized Output |
|-------|-------------------|
| FMGUildPage | FMGuildPage |
| (all others) | (unchanged) |

### Date Handling

- **Added Date**: Automatically set to today's date (ISO format: YYYY-MM-DD)
- **All timestamps**: Consistent timezone handling (UTC recommended)

---

## Bio File Loading

### File Discovery

Loader searches for `.txt` files in the same directory as the CSV:

```
reference/
├── guildmember_scrape.csv
├── Jonathan Carr.txt          ← Exact match
├── bio_alex_rivera.txt         ← Fuzzy match (prefix removed)
└── Nia Patel CFO.txt           ← Fuzzy match (suffix ignored)
```

### Matching Algorithm

**Step 1: Name Normalization**
```python
def normalize_name(name: str) -> str:
    # Remove prefixes: bio_, exec_, executive_
    name = re.sub(r'^(bio_|exec_|executive_)', '', name, flags=re.IGNORECASE)

    # Convert to lowercase, replace special chars with spaces
    name = re.sub(r'[^a-z0-9\s]', ' ', name.lower())

    # Collapse multiple spaces
    return ' '.join(name.split())
```

**Step 2: Exact Match**
- Normalize filename stem (without .txt)
- Compare with normalized candidate names
- If match → load bio content

**Step 3: Fuzzy Match (fallback)**
- Use `difflib.get_close_matches()` with 80% similarity threshold
- Handles typos, slight variations in spacing/punctuation
- First close match wins

### Bio Attachment

Bios loaded into memory are attached to candidate records before import:

```python
for candidate in candidates:
    if candidate['name'] in bios:
        candidate['bio'] = bios[candidate['name']]
```

---

## Duplicate Detection

### Strategy

Match on exact `Name` field (case-insensitive) against existing Airtable records.

### Implementation

```python
def check_duplicates(candidates: List[Dict], verbose: bool = False) -> Tuple[List[Dict], List[str]]:
    # Query existing People table
    existing_people = mcp__airtable__list_records(
        baseId=BASE_ID,
        tableId=PEOPLE_TABLE_ID,
        maxRecords=200
    )

    # Extract lowercase names
    existing_names = {
        record['fields'].get('Name', '').lower()
        for record in existing_people
        if 'Name' in record['fields']
    }

    # Filter candidates
    new_candidates = []
    duplicates = []

    for candidate in candidates:
        if candidate['name'].lower() in existing_names:
            duplicates.append(candidate['name'])
        else:
            new_candidates.append(candidate)

    return new_candidates, duplicates
```

### Graceful Degradation

If Airtable MCP is unavailable:
- Logs warning to user
- Proceeds without duplicate detection
- All candidates treated as new

---

## Record Creation

### Field Mapping to Airtable

| CSV Field (normalized) | Airtable Field | Required? |
|------------------------|----------------|-----------|
| name | Name | ✅ Yes |
| added_date | Added Date | ✅ Yes |
| title | Current Title | No |
| company | Current Company | No |
| linkedin_headline | LinkedIn Headline | No |
| linkedin_url | LinkedIn URL | No |
| location | Location | No |
| bio | Bio | No |
| function | Normalized Function | No* |
| source | Source | No* |

*\*Single-select fields only set if value exists in Airtable schema*

### Schema Validation

**Current demo schema (limited scope):**
- **Normalized Function**: CFO, CTO only
- **Source**: FMGuildPage, FMLinkedIN only

**Script behavior:**
```python
VALID_FUNCTIONS = {'CFO', 'CTO'}
VALID_SOURCES = {'FMGuildPage', 'FMLinkedIN'}

# Only set if value in valid set
if candidate.get('function') in VALID_FUNCTIONS:
    fields["Normalized Function"] = candidate['function']
elif verbose:
    print(f"⚠️  Skipping Normalized Function '{candidate['function']}' (not in schema)")
```

### Batch Processing

- Candidates processed one-by-one (not batched)
- Progress reported per candidate: `✅ 1/64: John Smith`
- Errors logged but don't stop processing
- Final summary includes counts: created, skipped, errors

### Error Handling

**Graceful error handling per candidate:**
```python
try:
    result = mcp__airtable__create_record(baseId, tableId, fields)
    created_count += 1
except Exception as e:
    error_count += 1
    errors.append(f"{candidate['name']}: {str(e)}")
```

**Common errors:**
- Invalid field values (e.g., URL format)
- Single-select option not in schema
- Airtable API rate limits (429)
- Network connectivity issues

---

## Advanced Usage

### Dry Run Mode

Preview changes before committing:

```bash
python load_candidates.py reference/guildmember_scrape.csv --dry-run
```

**Output:**
- Schema detection results
- Candidate count and duplicate detection
- List of records that WOULD be created
- No actual Airtable API calls made

### Verbose Mode

Detailed progress logging:

```bash
python load_candidates.py reference/guildmember_scrape.csv --verbose
```

**Additional output:**
- Full schema mapping (airtable field ← csv column)
- Bio file matching details (exact vs fuzzy)
- Single-select field skipping warnings
- Error details per failed candidate

### Combined Modes

Test thoroughly before live import:

```bash
# Preview with full detail
python load_candidates.py data/new_execs.csv --dry-run --verbose

# Execute with progress tracking
python load_candidates.py data/new_execs.csv --verbose
```

---

## Performance Considerations

### Scalability Limits

| Metric | Limit | Notes |
|--------|-------|-------|
| CSV rows | ~1000 | Tested up to 1000 candidates |
| Bio files | ~500 | Fuzzy matching slows with >500 files |
| Airtable records | 200 (configurable) | `maxRecords` parameter in duplicate check |
| API rate limit | ~5 req/sec | Airtable standard tier limit |

### Optimization Tips

1. **Pre-clean CSV** - Remove unnecessary columns before import
2. **Batch bio files** - Split large bio directories into subdirectories
3. **Increase maxRecords** - Adjust if People table > 200 records
4. **Run during off-hours** - Avoid Airtable API congestion

---

## Integration with Demo Workflow

### Pre-Demo Setup

```bash
# Test with dry-run
./scripts/quick_load.sh reference/guildmember_scrape.csv --dry-run

# Load candidates
./scripts/quick_load.sh reference/guildmember_scrape.csv

# Verify in Airtable
# Expected: ~64 total records (2 existing + 62 new)
```

### Live Demo Scenario

**If given surprise CSV during presentation:**

```bash
# 1. Quick preview
python load_candidates.py /path/to/surprise_data.csv --dry-run --verbose

# 2. Check schema compatibility
# Look for: "⚠️ Missing required fields" warnings

# 3. Load if compatible
python load_candidates.py /path/to/surprise_data.csv --verbose
```

### Emergency Rollback

If bad data imported during demo:

1. **Identify bad records** - Check Added Date (today's date)
2. **Delete via Airtable UI** - Filter by Added Date, bulk delete
3. **Re-run with corrected CSV** - Fix CSV and reload

---

## See Also

- [troubleshooting.md](troubleshooting.md) - Common errors and solutions
- [scripts/load_candidates.py](../scripts/load_candidates.py) - Main implementation
- [../SKILL.md](../SKILL.md) - Skill overview and quick start
