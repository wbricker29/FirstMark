"""Tests for research quality checking (citation count, sufficiency)."""

from datetime import datetime

import pytest

from demo.models import Citation, ExecutiveResearchResult
from demo.screening_helpers import check_research_quality


@pytest.fixture
def research_sufficient() -> ExecutiveResearchResult:
    """Fixture with sufficient research (≥3 citations + non-empty summary)."""
    return ExecutiveResearchResult(
        exec_name="Jane Doe",
        current_role="CFO",
        current_company="Acme Corp",
        research_summary="Experienced CFO with 15+ years in SaaS finance. Led Series B through IPO at multiple companies.",
        citations=[
            Citation(
                url="https://linkedin.com/in/janedoe",
                title="Jane Doe LinkedIn Profile",
                snippet="CFO at Acme Corp, previously VP Finance at TechCo",
            ),
            Citation(
                url="https://techcrunch.com/jane-doe-ipo",
                title="Acme Corp IPO Success",
                snippet="Under CFO Jane Doe's leadership, Acme raised $100M Series B",
            ),
            Citation(
                url="https://forbes.com/jane-doe-interview",
                title="Forbes Interview with Jane Doe",
                snippet="Discussing scaling finance operations from seed to IPO",
            ),
        ],
        research_timestamp=datetime.now(),
    )


@pytest.fixture
def research_insufficient_citations() -> ExecutiveResearchResult:
    """Fixture with insufficient citations (<3)."""
    return ExecutiveResearchResult(
        exec_name="John Smith",
        current_role="CTO",
        current_company="StartupCo",
        research_summary="Technical leader with background in distributed systems.",
        citations=[
            Citation(
                url="https://linkedin.com/in/johnsmith",
                title="John Smith LinkedIn",
                snippet="CTO at StartupCo",
            ),
            Citation(
                url="https://github.com/johnsmith",
                title="John Smith GitHub",
                snippet="Open source contributor",
            ),
        ],
        research_timestamp=datetime.now(),
    )


@pytest.fixture
def research_empty_summary() -> ExecutiveResearchResult:
    """Fixture with empty research summary."""
    return ExecutiveResearchResult(
        exec_name="Alice Johnson",
        current_role="VP Engineering",
        current_company="BigCo",
        research_summary="",  # Empty summary
        citations=[
            Citation(url="https://example.com/1", title="Source 1", snippet=""),
            Citation(url="https://example.com/2", title="Source 2", snippet=""),
            Citation(url="https://example.com/3", title="Source 3", snippet=""),
        ],
        research_timestamp=datetime.now(),
    )


@pytest.fixture
def research_whitespace_summary() -> ExecutiveResearchResult:
    """Fixture with whitespace-only summary."""
    return ExecutiveResearchResult(
        exec_name="Bob Williams",
        current_role="Head of Product",
        current_company="ProductCo",
        research_summary="   \n\t  ",  # Whitespace only
        citations=[
            Citation(url="https://example.com/1", title="Source 1", snippet=""),
            Citation(url="https://example.com/2", title="Source 2", snippet=""),
            Citation(url="https://example.com/3", title="Source 3", snippet=""),
        ],
        research_timestamp=datetime.now(),
    )


@pytest.fixture
def research_duplicate_urls() -> ExecutiveResearchResult:
    """Fixture with duplicate citation URLs (should count as unique URLs)."""
    return ExecutiveResearchResult(
        exec_name="Charlie Brown",
        current_role="COO",
        current_company="OpsCo",
        research_summary="Operational excellence leader with proven track record.",
        citations=[
            Citation(
                url="https://example.com/charlie",
                title="Charlie Profile",
                snippet="First mention",
            ),
            Citation(
                url="https://example.com/charlie",
                title="Charlie Profile Duplicate",
                snippet="Duplicate URL",
            ),
            Citation(url="https://example.com/article", title="Article", snippet=""),
            Citation(
                url="https://example.com/interview", title="Interview", snippet=""
            ),
        ],
        research_timestamp=datetime.now(),
    )


def test_check_research_quality_sufficient(
    research_sufficient: ExecutiveResearchResult,
) -> None:
    """Test quality check passes with ≥3 citations and non-empty summary."""
    result = check_research_quality(research_sufficient)

    assert result is True


def test_check_research_quality_insufficient_citations(
    research_insufficient_citations: ExecutiveResearchResult,
) -> None:
    """Test quality check fails with <3 citations."""
    result = check_research_quality(research_insufficient_citations)

    assert result is False


def test_check_research_quality_empty_summary(
    research_empty_summary: ExecutiveResearchResult,
) -> None:
    """Test quality check fails with empty summary."""
    result = check_research_quality(research_empty_summary)

    assert result is False


def test_check_research_quality_whitespace_summary(
    research_whitespace_summary: ExecutiveResearchResult,
) -> None:
    """Test quality check fails with whitespace-only summary."""
    result = check_research_quality(research_whitespace_summary)

    assert result is False


def test_check_research_quality_duplicate_urls(
    research_duplicate_urls: ExecutiveResearchResult,
) -> None:
    """Test quality check counts unique URLs only (deduplication).

    Expected: 3 unique URLs (charlie, article, interview) → passes
    """
    result = check_research_quality(research_duplicate_urls)

    assert result is True


def test_check_research_quality_no_citations() -> None:
    """Test quality check fails with no citations."""
    research = ExecutiveResearchResult(
        exec_name="Test Person",
        current_role="Test Role",
        current_company="Test Co",
        research_summary="Valid summary but no citations",
        citations=[],
        research_timestamp=datetime.now(),
    )

    result = check_research_quality(research)

    assert result is False


def test_check_research_quality_exactly_three_citations() -> None:
    """Test quality check passes with exactly 3 citations (boundary case)."""
    research = ExecutiveResearchResult(
        exec_name="Test Person",
        current_role="Test Role",
        current_company="Test Co",
        research_summary="Valid summary with exactly three citations",
        citations=[
            Citation(url="https://example.com/1", title="Source 1", snippet=""),
            Citation(url="https://example.com/2", title="Source 2", snippet=""),
            Citation(url="https://example.com/3", title="Source 3", snippet=""),
        ],
        research_timestamp=datetime.now(),
    )

    result = check_research_quality(research)

    assert result is True


def test_check_research_quality_empty_url_citations() -> None:
    """Test quality check handles citations with empty URLs correctly."""
    research = ExecutiveResearchResult(
        exec_name="Test Person",
        current_role="Test Role",
        current_company="Test Co",
        research_summary="Valid summary",
        citations=[
            Citation(url="", title="Empty URL 1", snippet=""),  # Should be ignored
            Citation(url="", title="Empty URL 2", snippet=""),  # Should be ignored
            Citation(url="https://example.com/1", title="Valid", snippet=""),
            Citation(url="https://example.com/2", title="Valid", snippet=""),
        ],
        research_timestamp=datetime.now(),
    )

    result = check_research_quality(research)

    # Only 2 valid URLs → should fail
    assert result is False


def test_check_research_quality_both_failures() -> None:
    """Test quality check fails when both citations and summary are insufficient."""
    research = ExecutiveResearchResult(
        exec_name="Test Person",
        current_role="Test Role",
        current_company="Test Co",
        research_summary="",  # Empty
        citations=[
            Citation(url="https://example.com/1", title="Source 1", snippet=""),
        ],  # Only 1 citation
        research_timestamp=datetime.now(),
    )

    result = check_research_quality(research)

    assert result is False
