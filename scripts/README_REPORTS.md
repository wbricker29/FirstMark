# Report Generation Scripts

This directory contains scripts for generating Markdown reports from candidate assessment data.

## Available Scripts

### 1. Python: SQLite Database Reports (Primary) ✅

**File:** `generate_markdown_reports.py`

Generates comprehensive Markdown reports from the workflow research content stored in the SQLite database.

**Features:**
- Extracts complete workflow data from `tmp/agno_sessions.db`
- Generates detailed reports with research, assessments, and citations
- Includes visual score indicators
- Handles missing data gracefully
- No external dependencies (standard library only)

**Usage:**
```bash
python3 scripts/generate_markdown_reports.py
# or with uv:
uv run python scripts/generate_markdown_reports.py
```

**Output:** `reports/candidate_assessments/*.md`

**Report Contents:**
- Executive summary with score visualization
- Candidate profile and research summary
- Career timeline with achievements
- Detailed dimension scores with evidence
- Must-haves assessment (✅/❌)
- Red flags and green flags
- Counterfactual analysis
- Full research citations

---

### 2. Node.js: Airtable Direct Upload (Legacy)

**File:** `generate_markdown_reports.js`

Node.js script that generates reports from Airtable data and uploads them back to Airtable.

**Setup:**
```bash
npm install airtable dotenv
```

**Usage:**
```bash
node scripts/generate_markdown_reports.js
```

**Note:** This script reads from Airtable's Screen_Results table and writes attachments back to Airtable. Use the Python script (above) for SQLite-based reports.

---

### 3. Airtable Script (Manual)

**Files:**
- `airtable_generate_reports_display.js` - Display-only version
- `airtable_generate_reports.js` - Original (limited by API)

Use in Airtable Scripting Extension:
- Generates markdown reports
- Displays them in script output
- Manual copy/paste to save

**Limitation:** Airtable's scripting extension cannot directly create file attachments.

---

## Recommendation

**For SQLite workflow data:** Use `generate_markdown_reports.py` (Python)

**For Airtable data upload:** Use `generate_markdown_reports.js` (Node.js)

---

## Comparison

| Feature | Python (SQLite) | Node.js (Airtable) |
|---------|----------------|-------------------|
| Data Source | SQLite DB | Airtable API |
| Dependencies | None (stdlib) | npm packages |
| Research Data | Full workflow details | Assessment JSON only |
| Citations | Complete with URLs | Limited |
| Career Timeline | Yes | No |
| Output Location | Local files | Airtable attachments |

---

## Sample Output

Both scripts generate Markdown files with candidate assessments. Example:

```
📊 Found 3 workflow sessions

📝 Processing session: screen_recBWjkAZDCFrW25q_recLAcXvaAp5jEy7G
   ✅ Generated report: Praveer_Melwani_20251118_203925.md
   📍 Location: reports/candidate_assessments/Praveer_Melwani_20251118_203925.md
   📊 Score: 76.0/100 (Confidence: Medium)

======================================================================
✨ Report generation complete!
📁 Generated 3 reports in: /path/to/reports/candidate_assessments
```
