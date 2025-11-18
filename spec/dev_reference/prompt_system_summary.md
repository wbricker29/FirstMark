# Prompt Catalog Summary

Snapshot of the centralized prompt template system introduced January 2025.

## Why

- **Consistency:** All Agno agents (Deep Research, parser, incremental search, assessment) now share a single source of truth for system prompts instead of scattered triple-quoted strings.
- **Context Engineering Alignment:** Mirrors the best practices outlined in `reference/docs_and_examples/agno/agno_contextmanagement.md`—separate `description`, `instructions`, `expected_output`, and optional `additional_context`.
- **Editable by Non-Coders:** YAML catalog lets anyone tweak prompts without editing Python files; changes are version-tracked like code.

## Files

- `demo/prompts/catalog.yaml` – Canonical prompt definitions. Each entry includes:
  - `description`: Agent persona / role.
  - `instructions`: Multi-line guidance block (supports bullet lists).
  - Optional `expected_output`, `additional_context`, `markdown`.
- `demo/prompts/library.py` – Loader that:
  - Reads the YAML once at import.
  - Provides `get_prompt(name, **placeholders)` returning a `PromptContext` dataclass.
  - Offers `PromptContext.as_agent_kwargs()` to plug directly into `Agent(...)`.
- `demo/prompts/__init__.py` – Re-exports `get_prompt` for cleaner imports.
- `tests/test_prompts.py` – Ensures catalog entries load correctly and missing keys raise clear errors.

## Integration Points

- `demo/agents.py` now calls `get_prompt("<agent_name>")` in each factory (`create_research_agent`, `create_research_parser_agent`, `create_incremental_search_agent`, `create_assessment_agent`). Resulting context maps 1:1 to Agno parameters.
- Additional prompt types can be added by extending `catalog.yaml`; no code changes required unless a new agent needs special placeholder formatting.

## Usage Notes

1. Edit `catalog.yaml` to adjust phrasing or add new entries.
2. Placeholders (e.g., `{role_title}`) are supported via Python `str.format` syntax; missing placeholders raise `KeyError` to catch mistakes early.
3. Keep instructions concise but explicit—Agno’s system message builder preserves list formatting from YAML.
4. When adding new prompts, also add a quick sanity test to `tests/test_prompts.py`.

## Future Ideas (Phase 2+)

- Add optional variants (e.g., `assessment.fast`) keyed off an environment variable.
- Store example few-shot responses per template and inject via `additional_context`.
- Build a small CLI (`scripts/validate_prompts.py`) to preview rendered prompts for sample scenarios before running agents.
