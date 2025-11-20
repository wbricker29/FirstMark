# Contributing Guide

Welcome! This repository powers the Stage 4.5+ Talent Signal Agent demo. Follow these guardrails so every change stays aligned with the canonical specs.

## 1. Know the Canonical Sources

- **Product truth:** `spec/prd.md`
- **Technical truth:** `spec/spec.md`
- **Task-specific plans:** `spec/units/*/plan.md`
- Supporting docs (`docs/`, `spec/dev_reference/*`, `case/`) add color but never override the PRD/spec pair. Update the spec before shipping behavior that changes requirements.

## 2. Environment Setup

```bash
uv venv
source .venv/bin/activate
uv pip install -e .
cp .env.example .env  # add OpenAI/Airtable credentials + optional AGENTOS_SECURITY_KEY
```

**Runtime commands**

- Start AgentOS server: `uv run python demo/agentos_app.py`
- Launch tests: `uv run pytest`
- Lint/format: `uv run ruff format . && uv run ruff check .`
- Type check: `uv run mypy demo tests`

## 3. Coding Standards

- Python 3.11+, Pydantic v2, FastAPI runtime (no legacy Flask code).
- Keep prompt strings in `demo/prompts/catalog.yaml`; load via `demo/prompts/library.get_prompt`.
- Use the write-only Airtable pattern (`demo/airtable_client.py`); never add read traversals inside workflows.
- All structured outputs must validate against models in `demo/models.py` (`ScreenWebhookPayload`, `ExecutiveResearchResult`, `AssessmentResult`, etc.).
- Add succinct, high-value comments only if logic is non-obvious.

## 4. Testing Expectations

- Maintain ≥75% total coverage (current suite: 130 tests, 75% coverage).
- Always run targeted suites when you touch a feature (`tests/test_agentos_app.py`, `tests/test_workflow.py`, `tests/test_prompts.py`, etc.).
- Integration flows (`uv run pytest tests/test_agentos_api_integration.py`) must pass before demo prep.
- Never skip failing tests without recording the debt in the relevant `spec/units/*/plan.md`.

**Run full test suite with coverage:**

```bash
uv run pytest

Expected output should show tests passing and 75%+ coverage (current: 130 tests, 75% coverage)

## 5. Documentation Requirements

- Update affected docs in `docs/` (runbook, user guide, architecture, etc.) when behavior, commands, or reference data changes.
- Reference the relevant spec section for every substantive change (e.g., `spec/spec.md#Screening API`).
- Do not introduce new prompt text or webhook schemas inside ad-hoc Markdown—link back to the YAML catalog or models instead.

## 6. Submitting Work

1. Ensure `git status` is clean or that your diff only contains intentional files.
2. Confirm no `tmp/` artifacts (`tmp/agno_sessions.db`) or secrets are included.
3. Write descriptive commit messages (e.g., `docs: align runbook with AgentOS bearer auth`).
4. Note follow-up items or blocked work directly in the relevant plan (`spec/units/005-testing_sprint/plan.md#TK-XX`).

By following these guidelines you keep the demo stable, the specs authoritative, and the documentation trustworthy for the Stage 5/6 review panels.
