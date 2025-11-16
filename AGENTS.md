# Repository Guidelines (FirstMark Talent Signal Agent Demo)

This repo is optimized around a live Talent Signal Agent demo for the FirstMark interview, centered on the Airtable + Flask + AGNO workflow defined in `case/technical_spec_V2.md` and narrated in the case brief.

## What To Prioritize
- Treat the case brief as the north star narrative (currently `reference/case_brief.md`) and `case/technical_spec_V2.md` as the source of truth for the implementation plan.
- Any new code, notes, or experiments should support the Talent Signal Agent demo (screening workflow, role specs, research/assessment) rather than generic infra.
- Capture case-specific reasoning, architectures, and drafts in `case/` (e.g., `case/WB-case_notes.md`, `case/*_appendix.md`), not in `reference/`.
- Use `brainstorming/` for early sketches or rough plans that may later be distilled into the case deliverables.

## Project Structure & Module Organization
- `case/`
  - Contains the official prompt, technical spec (`technical_spec_V2.md`), and solution notes.
  - Treat `technical_spec_V2.md` as the canonical description of the demo architecture (Airtable tables, Flask endpoints, AGNO agents, data schemas).
- `spec/`
  - Older or auxiliary specs; refer to `case/technical_spec_V2.md` first for current decisions.
- `scripts/`
  - Holds all Node-based automation (`scrape_companies.js`, `process_portfolio.js`, `create_summary.js`) plus their README.
  - Keep any new automation or data-processing tools here so data paths (defaulting to `../research`) remain consistent.
  - Treat scripts as supporting tools (e.g., portfolio/exec datasets), not the main product.
- `research/`
  - Canonical home for generated datasets used by scripts and deeper firm/talent research.
  - Includes portfolio exports, candidate/network mocks (e.g., `Mock_Guilds.csv`, `Exec_Network.csv`), and deeper notes (`member_research/`, `interview_research/`).
- `reference/`
  - Aggregates cleaned portfolio summaries and exports for sharing plus curated reading and decks.
  - Do not treat this as the primary workspace for new case drafts or implementation docs.
- `brainstorming/` and root-level briefs (`Interview_info.md`, `role_overview.md`, `Firm_DeepResearch.md`)
  - Track qualitative prep and context you may reference from the case.

## Demo Implementation Focus
- Core demo path follows `case/technical_spec_V2.md`:
  - Airtable as DB + UI (People, Screen, Workflows, Role Eval, Role Spec).
  - Flask + ngrok webhook server with minimal endpoints (e.g., `/upload`, `/screen`).
  - AGNO-based agents for research (`o4-mini-deep-research`) and assessment (`gpt-5-mini`) using Pydantic schemas.
- For the current demo:
  - Use **spec-guided evaluation only**; model-generated rubrics are explicitly future work.
  - Keep Flask endpoints **synchronous and simple**; async/concurrency is optional Phase 2.
  - Modules 2 and 3 (New Role, New Search) are primarily **Airtable-only flows**; they should not require new Python endpoints unless explicitly needed.

## Build, Test, and Development Commands
- Node-based data prep (supporting, not primary):
  - `cd scripts && node scrape_companies.js` scrapes FirstMark portfolio pages; start Chrome on `:9222` beforehand via `.claude/skills/web-browser/tools/start.js`.
  - `cd scripts && node process_portfolio.js` transforms `research/portfolio_raw.json` into the Markdown table.
  - `cd scripts && node create_summary.js` produces CSV and narrative summaries from the processed data.
  - Run scripts with Node 18+ in an ES module–friendly setup; prefer project-local dependencies.
- Python demo stack (primary):
  - Follow `case/technical_spec_V2.md` for environment assumptions (Python version, AGNO/OpenAI dependencies, Flask/ngrok usage).
  - Keep the Python surface area tight: one small Flask app, AGNO agents, and Airtable integration.

## Coding Style & Naming Conventions
- JavaScript:
  - ES modules, 2-space indentation, camelCase variables, and small helper functions (`scrapeCompanyPage`) for clarity.
  - Console logging should explain progress (`Found N unique companies`) and surface recoverable errors without exiting the process.
- Python (demo code):
  - Prefer clear, interview-friendly naming that reflects the Talent Signal Agent (e.g., `run_screening`, `create_research_agent`, `AssessmentResult`).
  - Keep modules small and aligned with the spec: one Flask entrypoint, small AGNO/LLM helpers, and thin Airtable client functions.
  - Favor explicit, typed Pydantic models for structured inputs/outputs, as in `case/technical_spec_V2.md`.
- Data / files:
  - Name derived data files with explicit scopes (`portfolio_detailed.json`, `member_research/AlexDR_ANT.md`, `Mock_Guilds.csv`) so downstream notes stay discoverable via `rg`.

## Testing & Validation Guidelines
- No dedicated test suite exists.
- Treat each script or demo run as an integration test:
  - For Node scripts: verify deltas with `git status` and inspect generated artifacts in `research/` (and any mirrored copies under `reference/portfolio/`).
  - For the Flask/AGNO demo: run through the Module 4 “Screen” flow with a small candidate set and verify Airtable status changes + outputs match the expectations in `case/technical_spec_V2.md`.
- Before using generated data in the case narrative, perform spot checks and sanity-check that examples match the case brief (`reference/case_brief.md`).

## Communication & Versioning for the Case
- Keep the main narrative concise and interview-ready in the case brief (currently `reference/case_brief.md`); move longer explorations into adjacent notes (e.g., `case/WB-case_notes.md` or `case/*_appendix.md`).
- If multiple variants of the solution exist (e.g., different agent architectures), use explicit filenames (`case/agent_v1_spec_guided.md`, `case/agent_v2_async_reranker.md`) and cross-link from the case brief so it is clear which is the “final” interview version.
- Avoid large, breaking restructures right before interviews; prefer small, incremental updates that preserve a stable, presentable case narrative.

## Commit & Pull Request Guidelines
- Use concise, imperative messages with scope prefixes (`case: refine technical_spec`, `demo: add screen endpoint`, `scripts: update portfolio transform`).
- Each PR (or logical commit group) should include:
  - Short context summary.
  - Affected directories.
  - Sample output snippets or file sizes (for research/data changes).
  - Any manual steps (Chrome port, ngrok URL, Airtable config assumptions).
- Link to relevant briefs (`reference/case_brief.md`, `case/technical_spec_V2.md`, `research/Firm_DeepResearch.md`) so reviewers can trace decisions.

## Data & Security Tips
- Many `research/` and `reference/portfolio/` files contain scraped or interview-derived information; avoid sharing raw exports outside this repository and scrub PII before publishing or presenting.
- Store API keys or browser credentials in your local environment, never inside tracked files; redact sensitive URLs from commit descriptions when referencing partner portals.
- When creating mock datasets for the demo (e.g., `Mock_Guilds.csv`, `Exec_Network.csv`, bios, JDs), prefer synthetic or anonymized examples that still resemble realistic VC/talent workflows.
