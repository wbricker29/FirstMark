# Repository Guidelines

## Project Structure & Module Organization
- `case/` contains the official prompt (`FirstMark_case...`) and solution notes; edit drafts here, not in `reference/`.
- `scripts/` holds all Node-based automation (`scrape_companies.js`, `process_portfolio.js`, `create_summary.js`) plus their README; keep new tools in this folder so data paths (`../research`) remain consistent.
- `research/` stores generated datasets (`portfolio_raw.json`, `portfolio_table.md`, member/interview notes); treat files here as source-of-truth outputs.
- `reference/` aggregates cleaned portfolio summaries and exports for sharing, while `brainstorming/` and root-level briefs (`Interview_info.md`, `role_overview.md`) track qualitative prep.
## Build, Test, and Development Commands
- `cd scripts && node scrape_companies.js` scrapes FirstMark portfolio pages; start Chrome on `:9222` beforehand via `.claude/skills/web-browser/tools/start.js`.
- `cd scripts && node process_portfolio.js` transforms `research/portfolio_raw.json` into the Markdown table.
- `cd scripts && node create_summary.js` produces CSV and narrative summaries from the processed data.
- Run scripts with Node 18+; prefer project-local dependencies to avoid polluting the global toolchain.

## Coding Style & Naming Conventions
- JavaScript files use ES modules, 2-space indentation, camelCase variables, and small helper functions (`scrapeCompanyPage`) for clarity.
- Console logging should explain progress (`Found N unique companies`) and surface recoverable errors without exiting the process.
- Name derived data files with explicit scopes (`portfolio_detailed.json`, `member_research/AlexDR_ANT.md`) so downstream notes stay discoverable via `rg`.

## Testing Guidelines
- No dedicated test suite exists; treat each script run as an integration test by verifying deltas with `git status` and inspecting generated artifacts.
- Capture spot checks (e.g., open `research/portfolio_detailed.json` to confirm expected founders field) before sharing results.
- When altering scrapers, rerun `node scrape_companies.js` against a short subset by editing the input list locally and confirm the data flow diagram from `scripts/README.md` still holds.

## Commit & Pull Request Guidelines
- History currently uses plain, capitalized subjects; prefer concise, imperative messages (`scripts: add retry logic`) and scope prefixes when touching multiple areas.
- Each PR should include: context summary, affected directories, sample output snippets or file sizes, and note any manual steps (Chrome port, credentials).
- Link to relevant briefs (`case/case_brief.md`, `research/Firm_DeepResearch.md`) so reviewers can trace decisions; add screenshots only when UI scraping changes are involved.

## Data & Security Tips
- Many `research/` files contain scraped or interview-derived information; avoid sharing raw exports outside this repository and scrub PII before publishing.
- Store API keys or browser credentials in your local environment, never inside tracked files; redact sensitive URLs from commit descriptions when referencing partner portals.
