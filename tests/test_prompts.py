"""Tests for the centralized prompt loader."""

import pytest

from demo.prompts import get_prompt


def test_assessment_prompt_loaded() -> None:
    """Assessment template returns expected instructions."""

    context = get_prompt("assessment")

    assert context.name == "assessment"
    assert isinstance(context.instructions, str)
    assert "1-5 scale" in context.instructions
    assert context.markdown is True


def test_missing_prompt_raises_key_error() -> None:
    """Unknown prompt names surface a clear KeyError."""

    with pytest.raises(KeyError):
        get_prompt("nonexistent_prompt")
