"""Tests for research agent implementation.

Tests the Deep Research agent creation, execution, and result parsing.
"""

from unittest.mock import Mock, patch

import pytest

from demo.agents import (
    create_research_agent,
    run_research,
    _extract_summary,
    _estimate_confidence,
    _identify_gaps,
)
from demo.models import Citation, ExecutiveResearchResult


class TestCreateResearchAgent:
    """Tests for create_research_agent function."""

    def test_create_agent_with_deep_research(self):
        """Test creating Deep Research agent returns properly configured Agent."""
        agent = create_research_agent(use_deep_research=True)

        assert agent is not None
        assert agent.name == "Deep Research Agent"
        assert agent.model.id == "o4-mini-deep-research"
        assert agent.model.max_tool_calls == 1
        assert agent.exponential_backoff is True
        assert agent.retries == 2
        assert agent.delay_between_retries == 1

    def test_create_agent_fast_mode_not_implemented(self):
        """Test fast mode raises NotImplementedError (Phase 2+)."""
        with pytest.raises(NotImplementedError, match="Fast mode.*Phase 2"):
            create_research_agent(use_deep_research=False)


class TestRunResearch:
    """Tests for run_research function with mocked agent."""

    @patch("demo.agents.create_research_parser_agent")
    @patch("demo.agents.create_research_agent")
    def test_run_research_success_with_citations(
        self,
        mock_create_agent,
        mock_create_parser,
    ) -> None:
        """Test successful research with citations returns ExecutiveResearchResult."""
        # Mock Deep Research result
        mock_agent = Mock()
        mock_result = Mock()
        mock_result.content = """
# Executive Summary

John Doe is a seasoned CFO with 15 years of experience in SaaS companies.

# Career Timeline

- CFO at Acme Corp (2020-present)
- VP Finance at Beta Inc (2015-2020)
- Director of Finance at Gamma LLC (2010-2015)

# Leadership & Team Building

Led finance teams of 20+ across multiple companies.
        """.strip()

        # Mock citations
        mock_citation_1 = Mock()
        mock_citation_1.url = "https://linkedin.com/in/johndoe"
        mock_citation_1.title = "John Doe - LinkedIn"

        mock_citation_2 = Mock()
        mock_citation_2.url = "https://acmecorp.com/team"
        mock_citation_2.title = "Acme Corp Team"

        mock_citation_3 = Mock()
        mock_citation_3.url = "https://techcrunch.com/johndoe"
        mock_citation_3.title = "John Doe raises $50M"

        mock_result.citations = Mock()
        mock_result.citations.urls = [mock_citation_1, mock_citation_2, mock_citation_3]

        mock_agent.run.return_value = mock_result
        mock_create_agent.return_value = mock_agent

        # Mock parser output
        parser_agent = Mock()
        parser_agent.run.return_value = ExecutiveResearchResult(
            exec_name="John Doe",
            current_role="CFO",
            current_company="Acme Corp",
            research_summary="Parsed summary",
            citations=[
                Citation(
                    url="https://linkedin.com/in/johndoe",
                    title="John Doe - LinkedIn",
                    snippet="",
                ),
                Citation(
                    url="https://acmecorp.com/team",
                    title="Acme Corp Team",
                    snippet="",
                ),
                Citation(
                    url="https://techcrunch.com/johndoe",
                    title="John Doe raises $50M",
                    snippet="",
                ),
            ],
        )
        mock_create_parser.return_value = parser_agent

        # Execute
        result = run_research(
            candidate_name="John Doe",
            current_title="CFO",
            current_company="Acme Corp",
            linkedin_url="https://linkedin.com/in/johndoe",
        )

        # Verify
        assert isinstance(result, ExecutiveResearchResult)
        assert result.exec_name == "John Doe"
        assert result.current_role == "CFO"
        assert result.current_company == "Acme Corp"
        assert len(result.citations) == 3
        assert result.citations[0].url == "https://linkedin.com/in/johndoe"
        assert result.research_confidence == "Low"  # 3 citations + content < 2000
        assert result.research_model == "o4-mini-deep-research"
        assert result.research_summary == "Parsed summary"
        assert result.research_markdown_raw.startswith("# Executive Summary")

    @patch("demo.agents.create_research_parser_agent")
    @patch("demo.agents.create_research_agent")
    def test_run_research_without_linkedin(
        self,
        mock_create_agent,
        mock_create_parser,
    ) -> None:
        """Test research works without LinkedIn URL."""
        mock_agent = Mock()
        mock_result = Mock()
        mock_result.content = "Research content"
        mock_result.citations = Mock()
        mock_result.citations.urls = []

        mock_agent.run.return_value = mock_result
        mock_create_agent.return_value = mock_agent

        parser_agent = Mock()
        parser_agent.run.return_value = ExecutiveResearchResult(
            exec_name="Jane Smith",
            current_role="CTO",
            current_company="Beta Inc",
            research_summary="Structured",
        )
        mock_create_parser.return_value = parser_agent

        result = run_research(
            candidate_name="Jane Smith",
            current_title="CTO",
            current_company="Beta Inc",
            linkedin_url=None,
        )

        assert result.exec_name == "Jane Smith"
        assert result.current_role == "CTO"

        # Verify prompt was built correctly (check call args)
        call_args = mock_agent.run.call_args[0][0]
        assert "Jane Smith" in call_args
        assert "LinkedIn: Not provided" in call_args

    @patch("demo.agents.create_research_parser_agent")
    @patch("demo.agents.create_research_agent")
    def test_run_research_handles_missing_citations(
        self,
        mock_create_agent,
        mock_create_parser,
    ) -> None:
        """Test research handles missing citations gracefully."""
        mock_agent = Mock()
        mock_result = Mock()
        mock_result.content = "Minimal research content"
        mock_result.citations = None  # No citations attribute

        mock_agent.run.return_value = mock_result
        mock_create_agent.return_value = mock_agent

        parser_agent = Mock()
        parser_agent.run.return_value = ExecutiveResearchResult(
            exec_name="Bob Test",
            current_role="VP Eng",
            current_company="Test Co",
            research_summary="Summary",
            citations=[],
        )
        mock_create_parser.return_value = parser_agent

        result = run_research(
            candidate_name="Bob Test",
            current_title="VP Eng",
            current_company="Test Co",
        )

        assert len(result.citations) == 0
        assert result.research_confidence == "Low"
        assert len(result.gaps) > 0

    @patch("demo.agents.create_research_parser_agent")
    @patch("demo.agents.create_research_agent")
    def test_run_research_raises_on_agent_failure(
        self,
        mock_create_agent,
        mock_create_parser,
    ) -> None:
        """Test research raises RuntimeError when agent fails after retries."""
        mock_agent = Mock()
        mock_agent.run.side_effect = Exception("API timeout")

        mock_create_agent.return_value = mock_agent
        mock_create_parser.return_value = Mock()

        with pytest.raises(RuntimeError, match="Research agent failed.*after retries"):
            run_research(
                candidate_name="Error Test",
                current_title="CEO",
                current_company="Fail Corp",
            )

    @patch("demo.agents.create_research_parser_agent")
    @patch("demo.agents.create_research_agent")
    def test_run_research_parser_failure(
        self,
        mock_create_agent,
        mock_create_parser,
    ) -> None:
        """Parser failure should raise RuntimeError with context."""
        mock_agent = Mock()
        mock_result = Mock()
        mock_result.content = "Research"
        mock_result.citations = []
        mock_agent.run.return_value = mock_result
        mock_create_agent.return_value = mock_agent

        parser_agent = Mock()
        parser_agent.run.side_effect = Exception("parser error")
        mock_create_parser.return_value = parser_agent

        with pytest.raises(RuntimeError, match="Research parser failed"):
            run_research(
                candidate_name="Parser Fail",
                current_title="CFO",
                current_company="Acme",
            )

    @patch("demo.agents.create_research_parser_agent")
    @patch("demo.agents.create_research_agent")
    def test_run_research_handles_list_citations(
        self,
        mock_create_agent,
        mock_create_parser,
    ) -> None:
        """Deep Research citations provided as list should be parsed."""
        mock_agent = Mock()
        mock_result = Mock()
        mock_result.content = "Research"
        mock_result.citations = [
            {"url": "https://example.com/one", "title": "One"},
            {"url": "https://example.com/two", "title": "Two"},
        ]
        mock_agent.run.return_value = mock_result
        mock_create_agent.return_value = mock_agent

        parser_agent = Mock()
        parser_agent.run.return_value = ExecutiveResearchResult(
            exec_name="List Case",
            current_role="CTO",
            current_company="Sample",
            research_summary="Summary",
            citations=[],
        )
        mock_create_parser.return_value = parser_agent

        result = run_research(
            candidate_name="List Case",
            current_title="CTO",
            current_company="Sample",
        )

        assert len(result.citations) == 2
        assert result.citations[0].url == "https://example.com/one"


class TestExtractSummary:
    """Tests for _extract_summary helper function."""

    def test_extract_summary_short_content(self):
        """Test summary extraction for content shorter than max_length."""
        markdown = "This is a short summary."
        summary = _extract_summary(markdown, max_length=2000)
        assert summary == "This is a short summary."

    def test_extract_summary_long_content_with_sentence_boundary(self):
        """Test summary truncates at sentence boundary."""
        markdown = (
            "First sentence. Second sentence. " + "X" * 1900 + ". Final sentence."
        )
        summary = _extract_summary(markdown, max_length=2000)

        # Should end at a period within the last 30%
        assert summary.endswith(".")
        assert len(summary) <= 2000
        assert not summary.endswith("...")

    def test_extract_summary_long_content_no_sentence_boundary(self):
        """Test summary adds ellipsis when no sentence boundary found."""
        markdown = "No periods in this long content " * 100
        summary = _extract_summary(markdown, max_length=500)

        assert summary.endswith("...")
        assert len(summary) <= 504  # 500 + "..."

    def test_extract_summary_empty_content(self):
        """Test empty markdown returns empty string."""
        assert _extract_summary("") == ""
        assert _extract_summary("   ") == ""


class TestEstimateConfidence:
    """Tests for _estimate_confidence helper function."""

    def test_high_confidence(self):
        """Test high confidence for ≥5 citations and substantial content."""
        citations = [
            Citation(url=f"https://example.com/{i}", title=f"Source {i}", snippet="")
            for i in range(5)
        ]
        markdown = "X" * 2500
        confidence = _estimate_confidence(citations, markdown)
        assert confidence == "High"

    def test_low_confidence_few_citations(self):
        """Test low confidence for <3 citations."""
        citations = [
            Citation(url="https://example.com/1", title="Source 1", snippet=""),
        ]
        markdown = "X" * 2500
        confidence = _estimate_confidence(citations, markdown)
        assert confidence == "Low"

    def test_low_confidence_minimal_content(self):
        """Test low confidence for minimal content."""
        citations = [
            Citation(url=f"https://example.com/{i}", title=f"Source {i}", snippet="")
            for i in range(5)
        ]
        markdown = "Short"
        confidence = _estimate_confidence(citations, markdown)
        assert confidence == "Low"

    def test_medium_confidence(self):
        """Test medium confidence for intermediate cases."""
        citations = [
            Citation(url=f"https://example.com/{i}", title=f"Source {i}", snippet="")
            for i in range(3)
        ]
        markdown = "X" * 1000
        confidence = _estimate_confidence(citations, markdown)
        assert confidence == "Medium"


class TestIdentifyGaps:
    """Tests for _identify_gaps helper function."""

    def test_no_gaps_sufficient_data(self):
        """Test no gaps identified when data is sufficient."""
        citations = [
            Citation(url=f"https://example.com/{i}", title=f"Source {i}", snippet="")
            for i in range(3)
        ]
        markdown = (
            """
Career history shows strong leadership experience.
Multiple roles demonstrate expertise in technical domains.
        """.strip()
            * 10
        )  # Make it long enough

        gaps = _identify_gaps(markdown, citations)
        assert len(gaps) == 0

    def test_gap_insufficient_citations(self):
        """Test gap identified for insufficient citations."""
        citations = [
            Citation(url="https://example.com/1", title="Source 1", snippet=""),
        ]
        markdown = "X" * 1000

        gaps = _identify_gaps(markdown, citations)
        assert any("Only 1 citations found" in g for g in gaps)

    def test_gap_minimal_content(self):
        """Test gap identified for minimal content."""
        citations = [
            Citation(url=f"https://example.com/{i}", title=f"Source {i}", snippet="")
            for i in range(3)
        ]
        markdown = "Short"

        gaps = _identify_gaps(markdown, citations)
        assert any("minimal" in g for g in gaps)

    def test_gap_missing_sections(self):
        """Test gap identified for missing required sections."""
        citations = [
            Citation(url=f"https://example.com/{i}", title=f"Source {i}", snippet="")
            for i in range(3)
        ]
        markdown = "This content lacks key sections." * 50

        gaps = _identify_gaps(markdown, citations)
        # Should identify missing sections (career, leadership, experience)
        assert any("missing sections" in g for g in gaps)

    def test_multiple_gaps(self):
        """Test multiple gaps can be identified."""
        citations = []  # No citations
        markdown = "Short"  # Minimal content, no key sections

        gaps = _identify_gaps(markdown, citations)
        assert len(gaps) >= 2  # Should have multiple gap types
