# Repository Guidelines (Talent Signal Agent)

This repo now reflects the Python-first Talent Signal Agent build powering Stage 4+ of the FirstMark demo. All implementation, process, and prioritization decisions must align with the living product + technical specs under `spec/`.

## Quick Tips

- **Use UV only** for Python environments (`uv pip install -e .`, `uv run pytest`, etc.).
- Keep `spec/prd.md` (product view) and `spec/spec.md` (technical contract) open—everything else is supporting context.
- Assume the `demo/` package and `tests/` folder are the center of gravity; keep diffs small and execution-ready.
- Do not commit `tmp/agno_sessions.db`, `.env`, or any generated Airtable exports.
- Treat automation scripts (`scripts/`) and research data as helpers, not the product.

## Canonical References

- `spec/prd.md` – **only product truth** (stakeholders, scenarios, acceptance criteria).
- `spec/spec.md` – **only technical truth** (architecture, workflows, API surfaces, current stage status).
- Supporting context lives in `spec/dev_reference/*`, `docs/`, and `non_code/`, but those documents must never override the canonical pair above.
- `case/`, `reference/`, and legacy briefs are historical; use them for additional color only when they do not contradict `spec/prd.md` or `spec/spec.md`.

## Priority Stack (January 2025)

1. **Stage 4 – Flask webhook + Airtable client polish.** Synchronous `/screen` endpoint, ngrok-ready logging, and thin `pyairtable` wrapper per `spec/spec.md`.
2. **Stage 5 – End-to-end workflow validation.** Screen multiple candidates via Airtable automation, capture logs, and keep Sqlite session state healthy.
3. **Stage 6 – Demo data completeness.** Load remaining executives and scenarios via `talent-signal-candidate-loader`; reconcile status with the spec roadmap.
4. Maintain Stage 1-3 assets (Airtable schema, agents, workflow orchestrator, 58+ tests) without churn unless required by the canonical specs.

## Project Structure & Ownership

- `demo/` – Core Python package (AgentOS FastAPI runtime, legacy Flask app, agents, models, Airtable client, settings). Keep modules lean and interview-friendly.
- `tests/` – Pytest suite covering models, agents, workflow orchestration, Airtable client, and settings. Target ≥50% coverage (constitution requirement).
- `spec/` – Documentation home. Only `spec/prd.md` and `spec/spec.md` are canonical; use `spec/dev_reference/*` (implementation guide, AGNO reference, Airtable schema) for supporting details.
- `scripts/` – Node + Python utilities for scraping, Deep Research experiments, and integration smoke tests. Default inputs live in `../research`.
- `data/` – Synthetic CSVs for quick experimentation (keep mock-only).
- `reference/` & `non_code/` – Presentation-ready briefs, qualitative research, and contextual notes. Do not place implementation plans here.
- `case/`, `archive/`, `docs/` – Legacy planning artifacts; edit only if you explicitly call out the variance from canonical specs.
- `tmp/` – Runtime artifacts (e.g., `tmp/agno_sessions.db`). Gitignored; ensure tests clean up temporary files.

## Implementation Focus

- **Airtable Integration:** Seven-table base (People, Portco, Portco_Roles, Searches, Screens, Assessments, Role_Specs) plus helper/audit tables. All Airtable calls flow through `demo/airtable_client.py` using `pyairtable`.
- **Workflow:** Linear pipeline (Deep Research → Quality Gate → optional Incremental Search → Assessment) defined in `demo/agents.py`. Session state persisted via `SqliteDb` at `tmp/agno_sessions.db`. Keep the orchestration synchronous for v1.
- **Agents:** `o4-mini-deep-research` for research (no `output_schema`), `gpt-5-mini` for assessment, optional incremental search via `gpt-5` with strict `max_tool_calls`. Encode constraints explicitly in prompts.
- **Models:** `demo/models.py` houses the Pydantic schemas (`ExecutiveResearchResult`, `AssessmentResult`, `DimensionScore`, etc.). All structured outputs must validate against these classes.
- **Settings:** `.env` parsing handled by `demo/settings.py`. Required vars: `OPENAI_API_KEY`, `AIRTABLE_API_KEY`, `AIRTABLE_BASE_ID`, AgentOS host/port (shared with legacy Flask), optional `NGROK_FORWARDING_URL`.

## Build & Test Commands

- Install deps: `uv pip install -e .`
- Lint + format: `uv run ruff format . && uv run ruff check .`
- Type check: `uv run mypy demo tests`
- Test suite: `uv run pytest` (or targeted `uv run pytest tests/test_workflow.py`)
- Manual server: `uv run python demo/agentos_app.py` (pair with `ngrok http 5000`)
- Scripts: `cd scripts && node create_summary.js`, `node scripts/scrape_companies.js`, or `uv run python scripts/test_deep_research.py`

## Coding Style & Naming

- **Python:** PEP 8 names, explicit type hints, Google-style docstrings, minimal abstraction layers. Keep comments for reasoning or constraints, not restating code. Workflows and agents should be easily narrated live.
- **Prompts:** Store longer prompts as triple-quoted strings inside the relevant agent factory; annotate Deep Research limitations inline.
- **JavaScript:** ES modules, 2-space indentation, camelCase, descriptive logging (`console.info("Found %d companies", count)`).
- **Data files:** Use scoped names (`research/member_research/...`, `reference/portfolio/<scenario>.md`). Document provenance for any new CSV/JSON artifact.

## Testing & Validation

- Maintain ≥50% coverage. Use `pytest --cov=demo --cov=tests` when validating larger changes.
- Workflow: `tests/test_workflow.py` + `tests/test_workflow_smoke.py` cover orchestration; extend fixtures rather than building new harnesses.
- Research Quality: `tests/test_quality_check.py` governs gap heuristics; keep fixtures aligned with new thresholds.
- Agents: `tests/test_research_agent.py`, `tests/test_scoring.py`, and `tests/test_agentos_app.py` verify prompt, schema, and `/screen` contracts. Run `pytest -m legacy tests/test_app.py` only when reproducing the deprecated Flask server.
- Airtable client + settings: keep `tests/test_airtable_client.py` and `tests/test_settings.py` in sync with env or schema changes.
- Scripts: manual inspection of generated artifacts (CSV/Markdown). Summarize output diffs in commits/PRs.

## Communication & Versioning

- Commit prefix examples: `demo: add incremental search helper`, `spec: document stage 4 webhook`, `scripts: update guild scrape`.
- Update `spec/prd.md` or `spec/spec.md` *before* shipping code that changes requirements; the repo should never outrun the canonical docs.
- Mention which spec section you satisfied or updated in PR/commit bodies to keep reviewers aligned.
- Presentation-ready summaries or narratives belong in `reference/` or `non_code/`; implementation notes or reasoning go into `spec/dev_reference/` or inline comments.

## Data & Security

- Keep Airtable/OpenAI secrets in `.env` (not tracked). Use `.env.example` for onboarding hints only.
- Treat `reference/` and `non_code/research/` outputs as sensitive; redact before sharing externally.
- Mock datasets in `data/` remain synthetic. If you regenerate, document methodology at the top of the file.
- Remove ngrok URLs, Airtable record IDs, and candidate PII from commit descriptions and docs unless explicitly required.

## Demo Runbook Reminders

- Airtable automation: trigger on `Screens.status == "Ready to Screen"`; POST `{ "screen_id": "{RECORD_ID}" }` to `/screen`. Update `spec/spec.md` if the payload or trigger changes.
- End-to-end smoke: run AgentOS, start ngrok, trigger Airtable automation, monitor emoji logs (`🔍/✅/🔄/❌`), and verify Airtable tables update. Capture log snippets for `README.md`.
- Data loading: use the `talent-signal-candidate-loader` Claude skill for bulk imports; track outstanding records in `SCHEMA_ALIGNMENT_PLAN.md` or `case/tracking.md` but reconcile final status against `spec/spec.md`.

Following these guidelines keeps the repo demo-ready and ensures the engineering narrative always matches the canonical specs the FirstMark panel will review.
