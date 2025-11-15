# Repository Guidelines (FirstMark Interview Case)

This repo is optimized around preparing for a FirstMark interview, with the current primary focus on completing `case/case_brief.md` and associated case materials.

## What To Prioritize
- Treat `case/case_brief.md` as the north star for work; any new code, notes, or experiments should ultimately support the Talent Signal Agent case.
- Capture case-specific reasoning, architectures, and drafts in `case/` (e.g., `case/WB-case_notes.md`, new case-specific files), not in `reference/`.
- Use `brainstorming/` for early sketches or rough plans that may later be distilled into the case deliverables.

## Project Structure & Module Organization
- `case/` contains the official prompt (`FirstMark_case...`), case brief (`case_brief.md`), and solution notes; edit drafts here when iterating on the case response.
- `scripts/` holds all Node-based automation (`scrape_companies.js`, `process_portfolio.js`, `create_summary.js`) plus their README; keep any new automation or data-processing tools in this folder so data paths (defaulting to `../research`) remain consistent.
- `research/` is the canonical home for generated datasets used by scripts (e.g., `portfolio_raw.json`, `portfolio_detailed.json`, `portfolio_table.md`, `portfolio_export.csv`, `portfolio_summary.md`) and deeper notes (`member_research/`, `interview_research/`); treat files here as source-of-truth outputs for the data pipeline or deeper firm/talent research.
- `reference/` aggregates cleaned portfolio summaries and exports for sharing (e.g., `reference/portfolio/portfolio_*.{json,md,csv}`) plus curated reading and decks; do not treat this as the primary workspace for case drafts.
- `brainstorming/` and root-level briefs (`Interview_info.md`, `role_overview.md`, `Firm_DeepResearch.md`) track qualitative prep and context you may reference from the case.

## Build, Test, and Development Commands
- `cd scripts && node scrape_companies.js` scrapes FirstMark portfolio pages; start Chrome on `:9222` beforehand via `.claude/skills/web-browser/tools/start.js`.
- `cd scripts && node process_portfolio.js` transforms `research/portfolio_raw.json` into the Markdown table.
- `cd scripts && node create_summary.js` produces CSV and narrative summaries from the processed data.
- Run scripts with Node 18+ in an ES module–friendly setup; prefer project-local dependencies to avoid polluting the global toolchain.
- Treat scripts as supporting tools for the case (e.g., to quickly assemble portfolio or exec datasets) rather than the main product; wire only what is necessary for the current case deliverables.

## Coding Style & Naming Conventions
- JavaScript files use ES modules, 2-space indentation, camelCase variables, and small helper functions (`scrapeCompanyPage`) for clarity.
- Console logging should explain progress (`Found N unique companies`) and surface recoverable errors without exiting the process.
- Name derived data files with explicit scopes (`portfolio_detailed.json`, `member_research/AlexDR_ANT.md`) so downstream notes stay discoverable via `rg`.
- For new case-specific code (e.g., Python prototypes, notebooks), favor clear, interview-friendly naming that reflects the Talent Signal Agent (e.g., `talent_signal_agent.ipynb`, `exec_matching_pipeline.py`).

## Testing & Validation Guidelines
- No dedicated test suite exists; treat each script run as an integration test by verifying deltas with `git status` and inspecting generated artifacts in `research/` (and any mirrored copies under `reference/portfolio/`).
- Before using generated data in the case, perform quick spot checks (e.g., open `research/portfolio_detailed.json` to confirm expected founders field) and sanity-check that examples match the narrative in `case/case_brief.md`.
- When altering scrapers, rerun `node scrape_companies.js` against a short subset by editing the input list locally and confirm the data flow diagram from `scripts/README.md` still holds.

## Communication & Versioning for the Case
- Keep the main narrative concise and interview-ready in `case/case_brief.md`; move longer explorations into adjacent notes (e.g., `case/WB-case_notes.md` or new `case/*_appendix.md` files).
- If multiple variants of the solution exist, use explicit filenames (`case/agent_v1_baseline.md`, `case/agent_v2_reranker.md`) and cross-link from `case_brief.md` so it is clear which is the “final” interview version.
- Avoid large, breaking restructures right before interviews; prefer small, incremental updates that preserve a stable, presentable case narrative.

## Commit & Pull Request Guidelines
- History currently uses plain, capitalized subjects; prefer concise, imperative messages (`scripts: add retry logic`, `case: refine matching rubric`) and scope prefixes when touching multiple areas.
- Each PR (or logical commit group) should include: context summary, affected directories, sample output snippets or file sizes, and note any manual steps (Chrome port, credentials).
- Link to relevant briefs (`case/case_brief.md`, `research/Firm_DeepResearch.md`) so reviewers can trace decisions; add screenshots only when UI scraping or data-exploration notebook changes are involved.

## Data & Security Tips
- Many `research/` and `reference/portfolio/` files contain scraped or interview-derived information; avoid sharing raw exports outside this repository and scrub PII before publishing or presenting.
- Store API keys or browser credentials in your local environment, never inside tracked files; redact sensitive URLs from commit descriptions when referencing partner portals.
- When creating mock datasets for the case (e.g., `Mock_Guilds.csv`, `Exec_Network.csv`, bios, JDs), prefer synthetic or anonymized examples that still resemble realistic VC/talent workflows.
