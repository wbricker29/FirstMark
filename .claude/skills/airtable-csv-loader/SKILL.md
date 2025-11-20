---
name: airtable-csv-loader
description: Load executive candidate CSVs into Airtable People table with intelligent schema detection, flexible column mapping (20+ variations), duplicate checking, and bio file loading. Handles any CSV format with fuzzy matching. Dry-run preview mode for safe testing. Production-ready for FirstMark demo day.
---

# Airtable CSV Loader

## Overview

Load executive candidate CSVs into Airtable People table. **One job: CSV in → Airtable records out.**

**Key features:**
- 🔄 **Flexible CSV input:** Handles any CSV format with intelligent schema detection
- 📄 **Bio file loading:** Auto-loads executive bios from .txt files (fuzzy name matching)
- 🧠 **Smart column mapping:** 20+ field name variations (e.g., "full_name", "exec_name" → Name)
- ✅ **Duplicate detection:** Skips existing candidates automatically
- 🔍 **Dry-run mode:** Preview changes before committing
- 📊 **Progress reporting:** Clear status updates during import

**Use this skill when:**
- You need to load candidates from CSV files into Airtable
- You're given surprise data during demo day
- You have executive bio .txt files to import alongside CSV
- You want to automate data entry (reduces 2-4 hours to 5-10 minutes)

---

## Quick Start (3 Commands)

### 1. Preview Before Import (Recommended)

```bash
cd .claude/skills/airtable-csv-loader
python scripts/load_candidates.py /path/to/candidates.csv --dry-run
```

**Output:** Shows what WOULD be created without making changes.

### 2. Load Candidates

```bash
python scripts/load_candidates.py /path/to/candidates.csv
```

**Output:** Creates records in Airtable People table with progress reporting.

### 3. Verify Results

Open Airtable → People table → Filter by Added Date = today

**Expected:** New records visible (e.g., 2 existing + 62 new = 64 total)

---

## How It Works (7 Steps)

The loader executes an automated workflow:

**Step 1: Detect CSV Schema**
- Automatically maps CSV columns to Airtable fields
- Supports 20+ column name variations (e.g., "full_name", "candidate_name", "exec_name" all map to Name field)
- Recognizes common field patterns across different data sources

**Step 2: Read & Parse CSV**
- Loads data with UTF-8 encoding
- Filters invalid rows (empty names, malformed data)
- Handles special characters and formatting

**Step 3: Load Executive Bios**
- Searches for .txt files in same directory as CSV
- Matches files to candidates using fuzzy name matching (80% similarity threshold)
- Handles typos, prefixes, suffixes automatically

**Step 4: Normalize Data**
- Infers executive functions (CFO/CTO/etc.) from job titles
- Cleans company names (removes stock tickers, extracts from descriptions)
- Sets source and dates automatically

**Step 5: Check Duplicates**
- Compares against existing Airtable records (exact name match)
- Skips duplicates automatically
- Reports skipped candidates

**Step 6: Create Records**
- Inserts new records into People table
- Batch processing with error handling
- Continues on individual failures

**Step 7: Summary Report**
- Shows created/skipped/error counts
- Lists any issues encountered
- Provides next steps

**For detailed technical walkthrough:** See [references/implementation_guide.md](references/implementation_guide.md)

---

## Usage Examples

### Basic Import

```bash
# From skill directory
cd .claude/skills/airtable-csv-loader
python scripts/load_candidates.py /path/to/candidates.csv
```

### Dry Run (Safe Preview)

```bash
# Preview changes without creating records
python scripts/load_candidates.py /path/to/candidates.csv --dry-run
```

### Verbose Mode (Detailed Logging)

```bash
# Show detailed progress and debugging info
python scripts/load_candidates.py /path/to/candidates.csv --verbose
```

### Combined Modes

```bash
# Preview with full detail (recommended before live import)
python scripts/load_candidates.py /path/to/candidates.csv --dry-run --verbose

# Execute with progress tracking
python scripts/load_candidates.py /path/to/candidates.csv --verbose
```

---

## Demo Day: Surprise CSV Scenario

**Scenario:** Given unexpected CSV file during presentation

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

**Fallback:** If loader fails, manually create 2-3 sample records and proceed with demo.

---

## Supported CSV Formats

The loader handles various CSV formats through intelligent schema detection:

**Examples:**
- `guildmember_scrape.csv` (64 executives from Guild pages)
- `Mock_Guilds.csv` (Guild member data)
- `Exec_Network.csv` (Partner connections)
- Any CSV with executive/candidate data

**Column mapping supports:**
- **Name:** full_name, name, executive_name, candidate_name, exec_name
- **Title:** title_raw, current_title, title, role_title, position, role
- **Company:** company, current_company, organization, employer
- **LinkedIn:** linkedin_url, linkedin, profile_url, url
- **Location:** location, city, region, geo
- **Bio:** bio, background, summary, about

**For complete mapping reference:** See [references/implementation_guide.md](references/implementation_guide.md)

---

## Expected Results

**From typical CSV (64 candidates):**
- ~25-30 CFOs (Normalized Title populated)
- ~20-25 CTOs (Normalized Title populated)
- ~10-15 Other functions (Normalized Title blank)

**After import:**
```
People table: 66 records (4 pre-existing + 62 new)
├── 30 CFOs (Normalized Title = CFO)
├── 25 CTOs (Normalized Title = CTO)
└── 11 Other (Normalized Title = blank)
```

**Verification checklist:**
- [ ] Total count matches expected (existing + created)
- [ ] No duplicate names
- [ ] All records have Name + Added Date
- [ ] CFO/CTO candidates have Normalized Title populated
- [ ] Spot-check 5 random records for data accuracy

---

## Troubleshooting

### CSV file not found

```bash
# Use absolute path or navigate to correct directory
python scripts/load_candidates.py /full/path/to/file.csv
```

### Airtable API key not set

```bash
# Check if .env file exists and contains AIRTABLE_API_KEY
cat .env | grep AIRTABLE_API_KEY

# If missing, add it to .env file in project root:
echo "AIRTABLE_API_KEY=your_api_key_here" >> .env
```

### Schema detection incorrect

```bash
# Run with verbose to see mapping
python scripts/load_candidates.py file.csv --dry-run --verbose

# Check: Does CSV have recognizable column names?
# Solution: Rename columns to match supported variations
```

### Bio files not matching

```bash
# Verify .txt files in same directory as CSV
ls /path/to/csv/directory/*.txt

# Run with verbose to see matching attempts
python scripts/load_candidates.py file.csv --dry-run --verbose
```

### Rate limit errors (429)

- Import smaller batches (<50 candidates)
- Run during off-peak hours
- Add delays between batches

**For complete troubleshooting guide:** See [references/troubleshooting.md](references/troubleshooting.md)

---

## Configuration

### Prerequisites

**Required dependencies:**
- `pyairtable>=2.0.0` (Airtable API client)
- `python-dotenv>=1.0.0` (Environment variable management)

These are already included in the project's `pyproject.toml`.

### Airtable Settings

**Environment variables (.env file in project root):**
```bash
AIRTABLE_API_KEY=your_api_key_here
```

**Hardcoded in scripts:**
```python
BASE_ID = "appeY64iIwU5CEna7"
PEOPLE_TABLE_ID = "tblHqYymo3Av9hLeC"
```

**To use with different base/table:**
Edit the BASE_ID and PEOPLE_TABLE_ID constants in `scripts/load_candidates.py`.

### Valid Single-Select Options

**Hardcoded for current Airtable schema:**
```python
VALID_FUNCTIONS = {'CFO', 'CTO'}
VALID_SOURCES = {'FMGuildPage', 'FMLinkedIN'}
```

**To expand:**
1. Update Airtable schema (add options via UI)
2. Edit `scripts/load_candidates.py` and expand sets
3. Re-run loader

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
3. **Use for demo:** Records are now available for screening workflows
4. **Document:** Note actual People table count for reference

---

## See Also

**Technical Documentation:**
- [references/implementation_guide.md](references/implementation_guide.md) - Complete technical deep-dive
- [references/troubleshooting.md](references/troubleshooting.md) - Common issues & solutions
- [scripts/load_candidates.py](scripts/load_candidates.py) - Main implementation
- [scripts/airtable_utils.py](scripts/airtable_utils.py) - Shared API utilities

**Related Skills:**
- `airtable-schema-validator` - Validate Airtable schema before loading data
