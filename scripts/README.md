# Project Scripts

This directory contains active, production-ready scripts for the Talent Signal Agent project.

## Directory Structure

```
scripts/
├── generate_markdown_reports.py    # PRIMARY: SQLite-based report generation
├── validate_airtable_client.py     # Airtable schema validation
├── validation/                      # AIdev workflow validators
│   └── validate-prerequisites.py
├── scrape_companies.js              # Portfolio data scraping (reference)
├── process_portfolio.js             # Portfolio data processing (reference)
├── create_summary.js                # Portfolio summary generation (reference)
├── archived/                        # Obsolete scripts (preserved for history)
│   ├── manual_tests/               # Integration test scripts
│   ├── legacy_reports/             # Superseded report generators
│   ├── utilities/                  # One-off utility scripts
│   └── linkedin/                   # LinkedIn integration experiments
└── README.md, README_REPORTS.md    # Documentation
```

## Why Scripts Are Here (Not in `.claude/skills/`)

Following Claude Code skill best practices:

- **Skills should be reusable** - The web-browser skill provides general browser automation tools
- **Project work stays in project directories** - These scripts are specific to FirstMark research
- **Separation of concerns** - Keeps skill directories clean and portable

## Active Scripts

### Validation Scripts (`validation/`)

#### `validate-prerequisites.py`

Pre-flight validator for `/work` command execution. Validates all Phase 1 (UNDERSTAND) prerequisites before loading context.

**What it validates:**
- Unit directory exists (`spec/units/###-SLUG/`)
- Required files exist (plan.md, design.md, spec.md, constitution.md)
- Task ID exists in plan.md
- Task status is "ready" or "doing"
- All dependencies are complete (status: "done")

**Usage:**

```bash
python scripts/validation/validate-prerequisites.py SLUG TK-##
```

**Examples:**

```bash
# Validate task TK-01 in phase-1 unit
python scripts/validation/validate-prerequisites.py phase-1 TK-01

# Validate using full unit ID
python scripts/validation/validate-prerequisites.py 001-phase-1 TK-01

# Validate task in agent-implementation unit
python scripts/validation/validate-prerequisites.py agent-implementation TK-03
```

**Exit codes:**
- `0` - All validations passed (JSON output to stdout)
- `1` - Validation failed (error message to stderr)

**Output (on success):**

```json
{
  "validation": "passed",
  "unit_path": "/path/to/spec/units/001-phase-1",
  "unit_id": "001-phase-1",
  "task": {
    "id": "TK-01",
    "title": "Create Project Directory Structure",
    "description": "...",
    "status": "ready",
    "dependencies": "None",
    "files": ["demo/agentos_app.py", "demo/agents.py"],
    ...
  },
  "dependencies": [],
  "files_validated": {
    "plan.md": true,
    "design.md": true,
    "spec.md": true,
    "constitution.md": true
  }
}
```

**Error examples:**

```bash
# Invalid unit slug
❌ Validation failed: No unit directory found matching slug: nonexistent-unit
Available units: 002-agent-implementation, 001-phase-1

# Invalid task ID
❌ Validation failed: Task TK-99 not found in plan.md
Available tasks: TK-01, TK-02, TK-03, TK-04, TK-05

# Task already complete
❌ Validation failed: Task TK-01 is already complete (status: done)
If you want to re-run it, manually change status to 'ready' in plan.md

# Incomplete dependencies
❌ Validation failed: Task TK-02 has incomplete dependencies:
  TK-01 (status: ready)

Complete these dependencies first before running this task.
```

**Integration with `/work` command:**

The `/work` command automatically runs this validator in Phase 1 (UNDERSTAND) before loading context. This saves ~450 tokens and 7-10 minutes per execution by catching invalid tasks early.

---

### Portfolio Scraping Scripts

#### `scrape_companies.js`

Automated web scraping script that:

- Connects to Chrome via the web-browser skill
- Visits each FirstMark portfolio company page
- Extracts: website, details, founders, about, social links, tags, status
- Saves progress incrementally to `research/portfolio_detailed.json`

**Usage:**

```bash
# 1. Start Chrome with web-browser skill
cd .claude/skills/web-browser && ./tools/start.js &

# 2. Run scraper
cd scripts && node scrape_companies.js
```

**Output:** `research/portfolio_detailed.json` (207 KB, 133 companies)

### `process_portfolio.js`

Processes raw portfolio data to create a clean markdown table:

- Extracts clean company names from raw text
- Removes duplicates by slug
- Parses stock tickers and acquisition info
- Sorts alphabetically

**Usage:**

```bash
cd scripts && node process_portfolio.js
```

**Input:** `research/portfolio_raw.json`
**Output:** `research/portfolio_table.md`

### `create_summary.js`

Generates summary documents and CSV export:

- Creates CSV with all company details
- Generates markdown summary with statistics
- Breaks down portfolio by FirstMark partner
- Includes sample company profiles

**Usage:**

```bash
cd scripts && node create_summary.js
```

**Outputs:**

- `research/portfolio_export.csv` (44 KB)
- `research/portfolio_summary.md` (9.7 KB)

## Data Flow

```
FirstMark Website
    ↓
scrape_companies.js  →  research/portfolio_raw.json
    ↓                   research/portfolio_detailed.json
process_portfolio.js →  research/portfolio_table.md
    ↓
create_summary.js    →  research/portfolio_export.csv
                        research/portfolio_summary.md
```

## Requirements

- Node.js v18+
- Chrome running on `:9222` (via web-browser skill)
- Dependencies: `puppeteer-core` (installed in `.claude/skills/web-browser/tools/node_modules`)

## Data Location

All output data is stored in `research/` directory:

- `portfolio_raw.json` - Raw scraped data from portfolio list page
- `portfolio_detailed.json` - Complete data from individual company pages
- `portfolio_table.md` - Markdown table with all companies
- `portfolio_export.csv` - CSV export for spreadsheet analysis
- `portfolio_summary.md` - Executive summary with statistics

## Archived Scripts

Scripts moved to `archived/` on Nov 19, 2025 (presentation day cleanup):

### `archived/manual_tests/` (5 scripts, ~1,115 lines)
Manual integration test scripts used during development:
- `test_bearer_auth.py` - AgentOS authentication testing
- `test_deep_research.py` - Deep Research API exploration
- `test_research_write.py` - Airtable write verification
- `test_screen_integration.py` - Full webhook integration test
- `test_webhook_basic.py` - Basic webhook connectivity test

### `archived/legacy_reports/` (3 scripts, ~781 lines)
Superseded report generation implementations:
- `generate_assessment_markdown_reports.py` - CSV-based reports (superseded by SQLite version)
- `generate_markdown_reports.js` - Node.js/Airtable version (marked legacy in README_REPORTS.md)
- `airtable_generate_reports.js` - Airtable scripting extension version (API limited)

### `archived/utilities/` (6 scripts, ~505 lines)
One-off utility scripts:
- `demo_agent_usage.py` - Agent framework exploration
- `send_sample_query.py` - Sample query testing
- `fix_company_links.py` - Data cleanup utility
- `verify_markdown_fields.py` - Field validation utility
- `airtable_script_defensive.js` - Airtable automation (undocumented)
- `airtable_webhook_automation.js` - Webhook setup (undocumented)

### `archived/linkedin/` (8 files)
LinkedIn integration experiments (not used in final implementation):
- Various LinkedIn search and profile extraction tools
- See `archived/linkedin/LINKEDIN_README.md` for details

**Total archived:** ~2,400 lines across 22 files

## Future Enhancements

Potential improvements:

- [ ] Add error retry logic
- [ ] Implement rate limiting
- [ ] Extract founder LinkedIn profiles
- [ ] Scrape funding round data
- [ ] Track portfolio changes over time
- [ ] Add company category classification
