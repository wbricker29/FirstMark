# Repository Guidelines (Talent Signal Agent)

This repo now reflects the AgentOS-backed Talent Signal Agent build powering Stage 4.5+ of the FirstMark demo. Stage 1-4 (Airtable, agents, workflow, webhook) are complete; Stage 5 (integration testing) and Stage 6 (demo prep) remain. Keep every change aligned to the living product + technical specs under `spec/`.

## Quick Tips

- **Use UV only** for Python environments (`uv pip install -e .`, `uv run pytest`, etc.). No `pip`, no `venv` helpers.
- Keep `spec/prd.md` (product view) and `spec/spec.md` (technical contract) open while you work; everything else is supporting context.
- `demo/` (AgentOS runtime, workflow, agents, prompts) and `tests/` are the center of gravity. Keep diffs small and demo-ready.
- AgentOS FastAPI runtime (`demo/agentos_app.py`) is canonical—do not reintroduce the deprecated Flask app or legacy runners.
- Prompt edits belong in `demo/prompts/catalog.yaml` + `demo/prompts/library.py`. Never hardcode template strings inside Python modules.
- Do not commit `tmp/agno_sessions.db`, `.env`, or Airtable exports. Scripts in `scripts/` and research data in `data/` are helpers, not the product.

## Canonical References

- `spec/prd.md` – **only product truth** (stakeholders, scenarios, acceptance criteria).
- `spec/spec.md` – **only technical truth** (architecture, workflows, API surfaces, current stage status).
- Supporting context lives in `spec/dev_reference/*` (implementation guides, Airtable schema, prompt system deep dives), `docs/` (e.g., `docs/agent_os_integration_spec.md`), and the long-form `README.md`. None of these documents override the canonical pair above.
- Historical artifacts (`case/`, `reference/`, archived briefs) are color only—never let them drift the implementation away from the spec.

## Priority Stack (January 2025)

1. **Stage 5 – Integration testing + AgentOS observability.** Run the full suite (`uv run pytest` plus targeted `tests/test_agentos_app.py`, `tests/test_agentos_api_integration.py`, `tests/test_agentos_session_registration.py`, `tests/test_prompts.py`, `tests/test_workflow.py`) and validate the AgentOS control plane logs + `/screen` FastAPI contract per `spec/spec.md#Screening API`.
2. **Stage 6 – Demo data completeness + pre-runs.** Load the remaining 62 executives and two pending scenarios via the `talent-signal-candidate-loader`, reconcile against `spec/spec.md#Demo Data`, and execute the Pigment/Pigment + Mockingbird/Synthesia dry runs.
3. **Stage 4.5 Cutover Polish.** Ensure every Airtable automation + helper script points at the AgentOS ngrok URL with the structured `ScreenWebhookPayload`, finish bearer-auth wiring (`AGENTOS_SECURITY_KEY`), and scrub lingering Flask references (see `docs/agent_os_integration_spec.md` checklist).
4. Maintain Stage 1-4 assets (Airtable schema, agents, workflow orchestrator, 58+ tests) without churn unless required by the canonical specs.

## Project Structure & Ownership

- `demo/` – Core Python package. `agentos_app.py` (FastAPI runtime), `workflow.py` (`AgentOSCandidateWorkflow` + Sqlite session persistence), `screening_service.py` (shared `/screen` runner), `agents.py`, `airtable_client.py`, `models.py`, `settings.py`, and `prompts/` (YAML catalog + loader). Keep modules lean and interview-friendly.
- `tests/` – Pytest suite covering agents, prompts, workflow orchestration, AgentOS runtime, Airtable client, models, and settings. Key suites: `tests/test_agentos_app.py`, `tests/test_agentos_api_integration.py`, `tests/test_agentos_session_registration.py`, `tests/test_workflow.py`, `tests/test_research_agent.py`, `tests/test_quality_check.py`, `tests/test_prompts.py`, `tests/test_scoring.py`, `tests/test_airtable_client.py`, `tests/test_models_validation.py`, `tests/test_settings.py`.
- `spec/` – Documentation home. Only `spec/prd.md` + `spec/spec.md` are canonical; `spec/dev_reference/*`, `spec/units/*`, and `spec/dev_plan_and_checklist.md` track implementation guidance.
- `docs/` – Runbooks + migration notes (e.g., `docs/agent_os_integration_spec.md`). Useful background, not new requirements.
- `scripts/` – Node + Python utilities for scraping, Deep Research experiments, webhook tests (`scripts/test_webhook_basic.py` sanity-checks `/screen`), and Airtable validation. Default inputs live in `../research`.
- `data/` – Synthetic CSVs for experimentation. Keep mock-only and document provenance.
- `reference/` & `non_code/` – Presentation-ready briefs and qualitative research. No implementation plans here.
- `case/`, `archive/`, `docs/legacy` – Historical artifacts; edit only when explicitly calling out variance from canonical specs.
- `tmp/` – Runtime artifacts (e.g., `tmp/agno_sessions.db`). Gitignored; tests must clean up.

## Implementation Focus

- **AgentOS runtime & workflow:** `demo/agentos_app.py` hosts the FastAPI `/screen` endpoint and AgentOS control plane hooks. `AgentOSCandidateWorkflow` (`demo/workflow.py`) runs Deep Research → quality gate → optional incremental search → assessment, persisting every session in `tmp/agno_sessions.db` via `SqliteDb`. Shared helpers live in `demo/screening_service.py` (logging, validation, Airtable writes).
- **Prompt catalog:** All prompt text lives in `demo/prompts/catalog.yaml` and is loaded through `demo/prompts/library.py:get_prompt()`. Agents never embed literal prompt strings; use placeholders + `PromptContext.as_agent_kwargs()` for dynamic values. Update the YAML + `tests/test_prompts.py` together.
- **Airtable integration:** Eight-table base (`People`, `Companies`, `Portcos`, `Platform-Portco_Roles`, `Platform-Role_Specs`, `Platform-Searches`, `Platform-Screens`, `Platform-Assessments`) plus helper tables (`Operations-Automation_Log`, `Operations-FMC_Roster`). All Airtable I/O flows through `demo/airtable_client.py`; `/screen` receives a structured `ScreenWebhookPayload` (screen slug + role spec snapshot + candidate slugs) so Python never performs read traversals during screening.
- **Agents:** `o4-mini-deep-research` for research (no `output_schema`), `gpt-5-mini` parser + assessment, optional incremental search via `gpt-5` with two tool calls max. Agent factories in `demo/agents.py` pull prompts from the catalog and set `add_datetime_to_context=True` where required.
- **Models:** `demo/models.py` houses `ExecutiveResearchResult`, `AssessmentResult`, `DimensionScore`, `ScreenWebhookPayload`, etc. Every structured output must validate against these Pydantic schemas.
- **Settings:** `.env` parsing lives in `demo/settings.py`. Required vars: `OPENAI_API_KEY`, `AIRTABLE_API_KEY`, `AIRTABLE_BASE_ID`, AgentOS host/port settings, optional `NGROK_FORWARDING_URL`, and optional `AGENTOS_SECURITY_KEY` for bearer auth.

## Build & Test Commands

- Install deps: `uv pip install -e .`
- Lint + format: `uv run ruff format . && uv run ruff check .`
- Type check: `uv run mypy demo tests`
- Test suite: `uv run pytest` (Stage 5 requires green runs for `tests/test_agentos_app.py`, `tests/test_agentos_api_integration.py`, `tests/test_prompts.py`, `tests/test_workflow.py`, and data/model suites).
- Manual server: `uv run python demo/agentos_app.py` (pair with `ngrok http 5001`).
- Webhook sanity: `uv run python scripts/test_webhook_basic.py` ensures the FastAPI endpoint responds + validates payloads; use the sample payload in `spec/spec.md#Screening API` for full `curl` tests.
- Scripts: `cd scripts && node create_summary.js`, `node scripts/scrape_companies.js`, or `uv run python scripts/test_deep_research.py`.

## Coding Style & Naming

- **Python:** PEP 8 names, explicit type hints, Google-style docstrings, minimal abstraction layers. Keep reasoning comments focused on constraints, not narration.
- **Prompts:** Store longer prompts as triple-quoted YAML strings in `demo/prompts/catalog.yaml`; annotate Deep Research limitations inline. All prompt placeholders must be documented in the catalog and validated via `tests/test_prompts.py`.
- **JavaScript:** ES modules, 2-space indentation, camelCase, descriptive logging (`console.info("Found %d companies", count)`).
- **Data files:** Use scoped names (`research/member_research/...`, `reference/portfolio/<scenario>.md`). Document provenance for regenerated CSV/JSON artifacts.

## Testing & Validation

- Maintain ≥50% coverage (current suites exceed that). Use `pytest --cov=demo --cov=tests` for large changes.
- Workflow + AgentOS: `tests/test_workflow.py`, `tests/test_agentos_workflow_mocked.py`, `tests/test_agentos_session_registration.py`, and `tests/test_agentos_api_integration.py` guard the orchestrator + session persistence.
- Runtime: `tests/test_agentos_app.py` verifies the FastAPI `/screen` contract, validation, and error handling.
- Prompts + agents: `tests/test_prompts.py`, `tests/test_research_agent.py`, `tests/test_scoring.py`, `tests/test_quality_check.py` lock the prompt catalog, research parser, scoring heuristics, and quality gate.
- Airtable client + models + settings: keep `tests/test_airtable_client.py`, `tests/test_models_validation.py`, and `tests/test_settings.py` in sync with schema or env changes.
- Scripts: manual inspection of generated artifacts (CSV/Markdown). Summarize output diffs in commits/PR descriptions.

## Communication & Versioning

- Commit prefix examples: `demo: add agentos session guard`, `spec: document stage 5 workflow`, `scripts: update webhook smoke test`.
- Update `spec/prd.md` or `spec/spec.md` **before** shipping code that changes requirements; the repo should never outrun the canonical docs.
- Reference the spec section you touched (e.g., `spec/spec.md#Workflow Orchestration`, `spec/spec.md#Screening API`) in commit bodies or PR notes.
- Presentation-ready summaries belong in `reference/` or `non_code/`; implementation details go into `spec/dev_reference/` or inline comments.

## Data & Security

- Keep Airtable/OpenAI secrets in `.env` (not tracked). Use `.env.example` for onboarding hints only.
- Configure `AGENTOS_SECURITY_KEY` when exposing `/screen` beyond localhost; include `Authorization: Bearer <key>` in Airtable automations + scripts.
- Treat `reference/` and `non_code/research/` outputs as sensitive; redact before sharing externally.
- Mock datasets in `data/` remain synthetic. If you regenerate, document methodology at the top of the file.
- Remove ngrok URLs, Airtable record IDs, and candidate PII from commit descriptions and docs unless explicitly required.

## Demo Runbook Reminders

- Airtable automation triggers when `Platform-Screens.Status` flips to `Processing` and posts the structured `ScreenWebhookPayload` (screen slug + role spec snapshot + candidate slugs) to `POST /screen`. The payload already contains the immutable spec markdown—Python performs zero Airtable reads during screening.
- Local smoke test: run `uv run python demo/agentos_app.py`, expose via `ngrok http 5001`, connect the AgentOS control plane, and monitor emoji logs (`🔍/✅/🔄/❌`) plus AgentOS session detail to prove observability.
- Update automation descriptions + helper scripts to reference the AgentOS URL + bearer auth whenever `AGENTOS_SECURITY_KEY` is set; log every webhook invocation to `Operations-Automation_Log` for traceability.
- Demo data: load the remaining executives/scenarios via the `talent-signal-candidate-loader` Claude skill, track outstanding records in `spec/dev_plan_and_checklist.md` (canonical tracking), and reconcile status against `spec/spec.md` before sharing.
- Capture log snippets + AgentOS UI screenshots for `README.md` once /screen flows are validated; ensure `tmp/agno_sessions.db` stays healthy (delete between runs if corruption occurs).

Following these guidelines keeps the repo aligned with the canonical specs, demonstrates Stage 5 readiness, and ensures the engineering narrative matches what the FirstMark panel will review.
