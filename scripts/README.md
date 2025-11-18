# Project Scripts

This directory contains project-specific scripts for data scraping and workflow automation.

## Why Scripts Are Here (Not in `.claude/skills/`)

Following Claude Code skill best practices:

- **Skills should be reusable** - The web-browser skill provides general browser automation tools
- **Project work stays in project directories** - These scripts are specific to FirstMark research
- **Separation of concerns** - Keeps skill directories clean and portable

## Scripts

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

## Future Enhancements

Potential improvements:

- [ ] Add error retry logic
- [ ] Implement rate limiting
- [ ] Extract founder LinkedIn profiles
- [ ] Scrape funding round data
- [ ] Track portfolio changes over time
- [ ] Add company category classification
