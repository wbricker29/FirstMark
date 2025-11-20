"""Tests for evidence-aware dimension scoring logic."""

import pytest

from demo.models import DimensionScore
from demo.screening_helpers import calculate_overall_score


@pytest.fixture
def dimension_score_all_scored() -> list[DimensionScore]:
    """Fixture with all dimensions scored (no None values)."""
    return [
        DimensionScore(
            dimension="Leadership",
            score=4,
            evidence_level="High",
            confidence="High",
            reasoning="Strong track record of team building and organizational design.",
        ),
        DimensionScore(
            dimension="Strategic Vision",
            score=5,
            evidence_level="High",
            confidence="Medium",
            reasoning="Demonstrated strategic thinking across multiple scaling contexts.",
        ),
        DimensionScore(
            dimension="Execution",
            score=3,
            evidence_level="Medium",
            confidence="Medium",
            reasoning="Solid execution track record with measurable outcomes.",
        ),
    ]


@pytest.fixture
def dimension_score_partial_scored() -> list[DimensionScore]:
    """Fixture with some dimensions scored and some None (Unknown)."""
    return [
        DimensionScore(
            dimension="Leadership",
            score=4,
            evidence_level="High",
            confidence="High",
            reasoning="Strong evidence of team leadership.",
        ),
        DimensionScore(
            dimension="Strategic Vision",
            score=None,  # Unknown - insufficient evidence
            evidence_level="Low",
            confidence="Low",
            reasoning="Insufficient public evidence to assess strategic vision.",
        ),
        DimensionScore(
            dimension="Execution",
            score=5,
            evidence_level="High",
            confidence="High",
            reasoning="Exceptional execution track record.",
        ),
        DimensionScore(
            dimension="Domain Expertise",
            score=None,  # Unknown - insufficient evidence
            evidence_level="Low",
            confidence="Low",
            reasoning="No public evidence of domain expertise in target sector.",
        ),
    ]


@pytest.fixture
def dimension_score_none_scored() -> list[DimensionScore]:
    """Fixture with no dimensions scored (all None)."""
    return [
        DimensionScore(
            dimension="Leadership",
            score=None,
            evidence_level="Low",
            confidence="Low",
            reasoning="No public evidence available.",
        ),
        DimensionScore(
            dimension="Strategic Vision",
            score=None,
            evidence_level="Low",
            confidence="Low",
            reasoning="No public evidence available.",
        ),
    ]


def test_calculate_overall_score_all_scored(
    dimension_score_all_scored: list[DimensionScore],
) -> None:
    """Test overall score calculation when all dimensions are scored.

    Expected: (4 + 5 + 3) / 3 * 20 = 80.0
    """
    result = calculate_overall_score(dimension_score_all_scored)

    assert result is not None
    assert result == 80.0


def test_calculate_overall_score_partial_scored(
    dimension_score_partial_scored: list[DimensionScore],
) -> None:
    """Test overall score calculation with partial scoring (some None values).

    Expected: (4 + 5) / 2 * 20 = 90.0 (None values are filtered out)
    """
    result = calculate_overall_score(dimension_score_partial_scored)

    assert result is not None
    assert result == 90.0


def test_calculate_overall_score_none_scored(
    dimension_score_none_scored: list[DimensionScore],
) -> None:
    """Test overall score calculation when no dimensions are scored.

    Expected: None (no scorable dimensions)
    """
    result = calculate_overall_score(dimension_score_none_scored)

    assert result is None


def test_calculate_overall_score_empty_list() -> None:
    """Test overall score calculation with empty dimension list.

    Expected: None (no dimensions provided)
    """
    result = calculate_overall_score([])

    assert result is None


def test_calculate_overall_score_single_dimension() -> None:
    """Test overall score calculation with single scored dimension.

    Expected: score * 20 (e.g., 3 * 20 = 60.0)
    """
    dimensions = [
        DimensionScore(
            dimension="Leadership",
            score=3,
            evidence_level="Medium",
            confidence="Medium",
            reasoning="Moderate evidence of leadership capability.",
        )
    ]

    result = calculate_overall_score(dimensions)

    assert result is not None
    assert result == 60.0


def test_calculate_overall_score_edge_values() -> None:
    """Test overall score calculation with edge score values (1 and 5).

    Expected: (1 + 5) / 2 * 20 = 60.0
    """
    dimensions = [
        DimensionScore(
            dimension="Low Score",
            score=1,
            evidence_level="High",
            confidence="High",
            reasoning="Clear evidence of weakness in this dimension.",
        ),
        DimensionScore(
            dimension="High Score",
            score=5,
            evidence_level="High",
            confidence="High",
            reasoning="Exceptional performance in this dimension.",
        ),
    ]

    result = calculate_overall_score(dimensions)

    assert result is not None
    assert result == 60.0


def test_calculate_overall_score_type_safety() -> None:
    """Test that calculate_overall_score returns Optional[float] as expected."""
    all_scored = [
        DimensionScore(
            dimension="Test",
            score=4,
            evidence_level="High",
            confidence="High",
            reasoning="Test reasoning",
        )
    ]
    all_none = [
        DimensionScore(
            dimension="Test",
            score=None,
            evidence_level="Low",
            confidence="Low",
            reasoning="Test reasoning",
        )
    ]

    # Type annotations should be correct
    result_scored = calculate_overall_score(all_scored)
    result_none = calculate_overall_score(all_none)

    assert isinstance(result_scored, float)
    assert result_none is None
