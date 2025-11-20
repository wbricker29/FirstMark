"""Prompt catalog + loader used by all Talent Signal agents.

The catalog is defined in ``catalog.yaml`` so prompts can be edited without
touching code. Each entry aligns with the context-engineering guidance in
``reference/docs_and_examples/agno/agno_contextmanagement.md``.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class PromptContext:
    """Materialized prompt values for an agent system message."""

    name: str
    description: str | None = None
    instructions: str | list[str] | None = None
    expected_output: str | None = None
    additional_context: str | None = None
    markdown: bool | None = None

    def as_agent_kwargs(self) -> dict[str, Any]:
        """Return dict of keyword args consumable by ``Agent``."""

        return {
            key: value
            for key, value in {
                "description": self.description,
                "instructions": self.instructions,
                "expected_output": self.expected_output,
                "additional_context": self.additional_context,
                "markdown": self.markdown,
            }.items()
            if value is not None
        }


_CATALOG_PATH = Path(__file__).with_name("catalog.yaml")
_CATALOG_DATA = yaml.safe_load(_CATALOG_PATH.read_text(encoding="utf-8"))


def _format_value(value: Any, fmt: dict[str, Any]) -> Any:
    """Format template values with ``str.format``."""

    if value is None:
        return None

    if isinstance(value, str):
        return value.format(**fmt) if fmt else value

    if isinstance(value, list):
        return [entry.format(**fmt) if fmt else entry for entry in value]

    return value


def get_prompt(name: str, **format_kwargs: Any) -> PromptContext:
    """Return prompt context for ``name`` with optional placeholder values."""

    try:
        entry = _CATALOG_DATA[name]
    except KeyError as exc:  # pragma: no cover - developer error path
        raise KeyError(f"Prompt '{name}' not found in catalog {_CATALOG_PATH}") from exc

    return PromptContext(
        name=name,
        description=_format_value(entry.get("description"), format_kwargs),
        instructions=_format_value(entry.get("instructions"), format_kwargs),
        expected_output=_format_value(entry.get("expected_output"), format_kwargs),
        additional_context=_format_value(
            entry.get("additional_context"), format_kwargs
        ),
        markdown=entry.get("markdown"),
    )
