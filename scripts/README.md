# FirstMark Portfolio Scraping Scripts

This directory contains project-specific scripts for scraping and processing FirstMark Capital's portfolio data.

## Why Scripts Are Here (Not in `.claude/skills/`)

Following Claude Code skill best practices:
- **Skills should be reusable** - The web-browser skill provides general browser automation tools
- **Project work stays in project directories** - These scripts are specific to FirstMark research
- **Separation of concerns** - Keeps skill directories clean and portable

## Scripts

### `scrape_companies.js`
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
