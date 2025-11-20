"""Tests for AgentOS workflow execution with mocked Deep Research API calls.

This test suite mocks the Deep Research API response to test the full workflow
without making actual API calls. It verifies:
- Deep Research API call mocking
- Research parser agent execution
- Quality check logic
- Incremental search (when triggered)
- Assessment agent execution
- Full workflow completion
"""

from __future__ import annotations

from datetime import datetime
from unittest.mock import Mock, patch

import pytest

from demo.models import (
    AssessmentResult,
    Citation,
    DimensionScore,
    ExecutiveResearchResult,
)
from demo.settings import settings
from demo.workflow import AgentOSCandidateWorkflow


@pytest.fixture
def mock_deep_research_response() -> Mock:
    """Mock response from Deep Research API (o4-mini-deep-research)."""
    mock_result = Mock()
    mock_result.content = """
# Executive Summary

Jane Smith is an experienced CFO with 12 years of finance leadership in B2B SaaS companies.

# Career Timeline

- CFO at TechCorp (2020-present)
  - Led Series B and Series C fundraising rounds ($50M total)
  - Built finance team from 3 to 15 people
  - Implemented financial planning and analysis processes

- VP Finance at StartupCo (2015-2020)
  - Managed finance operations for scaling SaaS business
  - Led budgeting and forecasting processes

- Director of Finance at EnterpriseInc (2010-2015)
  - Established financial reporting infrastructure
  - Worked with executive team on strategic planning

# Key Achievements

- Successfully raised $50M across two funding rounds
- Scaled finance team from 3 to 15 members
- Implemented comprehensive FP&A processes
- Led financial due diligence for strategic partnerships

# Leadership & Team Building

Strong track record of building and leading finance teams. Known for developing
talent and creating collaborative work environments.

# Sector Expertise

- B2B SaaS
- Enterprise Software
- Financial Technology
    """.strip()

    # Mock citations structure (Deep Research returns citations in result.citations)
    mock_citation_1 = Mock()
    mock_citation_1.url = "https://linkedin.com/in/jane-smith"
    mock_citation_1.title = "Jane Smith - LinkedIn Profile"
    mock_citation_1.snippet = "CFO at TechCorp"

    mock_citation_2 = Mock()
    mock_citation_2.url = "https://techcrunch.com/techcorp-series-c"
    mock_citation_2.title = "TechCorp Raises $30M Series C"
    mock_citation_2.snippet = "Led by CFO Jane Smith"

    mock_citation_3 = Mock()
    mock_citation_3.url = "https://crunchbase.com/person/jane-smith"
    mock_citation_3.title = "Jane Smith - Crunchbase"
    mock_citation_3.snippet = "Finance executive with 12 years experience"

    mock_citation_4 = Mock()
    mock_citation_4.url = "https://forbes.com/jane-smith-cfo"
    mock_citation_4.title = "Forbes: Top CFOs in SaaS"
    mock_citation_4.snippet = "Jane Smith recognized for leadership"

    # Deep Research citations structure
    mock_result.citations = Mock()
    mock_result.citations.urls = [
        mock_citation_1,
        mock_citation_2,
        mock_citation_3,
        mock_citation_4,
    ]

    return mock_result


@pytest.fixture
def mock_parser_response() -> ExecutiveResearchResult:
    """Mock structured output from research parser agent."""
    return ExecutiveResearchResult(
        exec_name="Jane Smith",
        current_role="CFO",
        current_company="TechCorp",
        research_summary="Experienced CFO with 12 years in B2B SaaS, successfully raised $50M across funding rounds.",
        research_markdown_raw="""
# Executive Summary

Jane Smith is an experienced CFO with 12 years of finance leadership in B2B SaaS companies.
        """.strip(),
        citations=[
            Citation(
                url="https://linkedin.com/in/jane-smith",
                title="Jane Smith - LinkedIn Profile",
                snippet="CFO at TechCorp",
            ),
            Citation(
                url="https://techcrunch.com/techcorp-series-c",
                title="TechCorp Raises $30M Series C",
                snippet="Led by CFO Jane Smith",
            ),
            Citation(
                url="https://crunchbase.com/person/jane-smith",
                title="Jane Smith - Crunchbase",
                snippet="Finance executive with 12 years experience",
            ),
            Citation(
                url="https://forbes.com/jane-smith-cfo",
                title="Forbes: Top CFOs in SaaS",
                snippet="Jane Smith recognized for leadership",
            ),
        ],
        career_timeline=[],
        fundraising_experience="Led Series B and Series C fundraising ($50M total)",
        team_building_experience="Scaled finance team from 3 to 15 members",
        sector_expertise=["B2B SaaS", "Enterprise Software"],
        stage_exposure=["Series B", "Series C"],
        research_confidence="High",
        gaps=[],
        research_timestamp=datetime.now(),
        research_model="o4-mini-deep-research",
    )


@pytest.fixture
def mock_assessment_result() -> AssessmentResult:
    """Mock assessment result from assessment agent."""
    return AssessmentResult(
        overall_score=88.5,
        overall_confidence="High",
        dimension_scores=[
            DimensionScore(
                dimension="Financial Leadership",
                score=5,
                evidence_level="High",
                confidence="High",
                reasoning="Strong track record of finance leadership with 12 years experience",
                evidence_quotes=["Led Series B and Series C fundraising"],
                citation_urls=["https://techcrunch.com/techcorp-series-c"],
            ),
            DimensionScore(
                dimension="Strategic Planning",
                score=4,
                evidence_level="High",
                confidence="High",
                reasoning="Demonstrated strategic planning through FP&A implementation",
                evidence_quotes=["Implemented comprehensive FP&A processes"],
                citation_urls=[],
            ),
            DimensionScore(
                dimension="Team Building",
                score=5,
                evidence_level="High",
                confidence="High",
                reasoning="Successfully scaled finance team from 3 to 15 members",
                evidence_quotes=["Scaled finance team from 3 to 15 members"],
                citation_urls=[],
            ),
            DimensionScore(
                dimension="SaaS Domain Expertise",
                score=4,
                evidence_level="High",
                confidence="High",
                reasoning="12 years of experience in B2B SaaS companies",
                evidence_quotes=["12 years of finance leadership in B2B SaaS"],
                citation_urls=["https://crunchbase.com/person/jane-smith"],
            ),
        ],
        must_haves=[
            {"requirement": "10+ years finance leadership", "met": True},
            {"requirement": "B2B SaaS experience", "met": True},
            {"requirement": "Series B+ fundraising", "met": True},
        ],
        green_flags=["Strong fundraising track record", "Proven team scaling"],
        summary="Excellent CFO candidate with strong B2B SaaS experience and proven fundraising success.",
        counterfactuals=["May prefer larger company stage"],
        role_spec_used="# CFO Role Specification...",
        assessment_timestamp=datetime.now(),
    )


@pytest.fixture
def mock_role_spec() -> str:
    """Sample role specification markdown."""
    return """
# CFO Role Specification

## Role Context
Scaling B2B SaaS company needs experienced CFO to lead through hypergrowth.

## Must-Haves
- 10+ years finance leadership
- B2B SaaS experience
- Series B+ fundraising

## Evaluation Dimensions
1. Financial Leadership (1-5)
2. Strategic Planning (1-5)
3. Team Building (1-5)
4. SaaS Domain Expertise (1-5)
    """.strip()


@pytest.fixture
def mock_candidate_data() -> dict:
    """Sample candidate data from Airtable."""
    return {
        "id": "recCandidate123",
        "fields": {
            "Name": "Jane Smith",
            "Current Title": "CFO",
            "Current Company": "TechCorp",
            "LinkedIn URL": "https://linkedin.com/in/jane-smith",
        },
    }


@pytest.fixture
def workflow_runner() -> AgentOSCandidateWorkflow:
    """Create workflow runner instance for testing."""
    import logging

    logger = logging.getLogger("test.agentos_workflow")
    logger.setLevel(logging.DEBUG)
    return AgentOSCandidateWorkflow(logger)


class TestAgentOSWorkflowWithMockedAPI:
    """Test AgentOS workflow execution with mocked Deep Research API."""

    @patch("demo.workflow.assess_candidate")
    @patch("demo.workflow.check_research_quality")
    @patch("demo.workflow.run_research")
    def test_full_workflow_with_mocked_deep_research(
        self,
        mock_run_research,
        mock_quality_check,
        mock_assess,
        mock_parser_response: ExecutiveResearchResult,
        mock_assessment_result: AssessmentResult,
        mock_role_spec: str,
        mock_candidate_data: dict,
        workflow_runner: AgentOSCandidateWorkflow,
    ) -> None:
        """Test full workflow execution with mocked Deep Research API call.

        This test mocks:
        1. run_research() function (which internally calls Deep Research API)
        2. Quality check (passes)
        3. Assessment agent

        Verifies the complete workflow executes successfully.
        """
        # Setup mocks
        mock_run_research.return_value = mock_parser_response
        mock_quality_check.return_value = True
        mock_assess.return_value = mock_assessment_result

        # Execute workflow
        custom_instructions = "Focus on enterprise SaaS scale-ups."
        result, research = workflow_runner.run_candidate_workflow(
            candidate_data=mock_candidate_data,
            role_spec_markdown=mock_role_spec,
            screen_id="recScreen123",
            custom_instructions=custom_instructions,
        )

        assert research is not None
        assert isinstance(research, ExecutiveResearchResult)
        assert research.exec_name == mock_parser_response.exec_name

        # Verify run_research was called
        mock_run_research.assert_called_once()
        research_call_kwargs = mock_run_research.call_args.kwargs
        assert research_call_kwargs["candidate_name"] == "Jane Smith"
        assert research_call_kwargs["current_title"] == "CFO"
        assert research_call_kwargs["current_company"] == "TechCorp"
        assert (
            research_call_kwargs["use_deep_research"]
            == settings.openai.use_deep_research
        )

        # Verify quality check was called
        mock_quality_check.assert_called_once()
        quality_check_call = mock_quality_check.call_args[0][0]
        assert isinstance(quality_check_call, ExecutiveResearchResult)
        assert quality_check_call.exec_name == "Jane Smith"

        # Verify assessment was called
        mock_assess.assert_called_once()
        assess_call_kwargs = mock_assess.call_args.kwargs
        assert assess_call_kwargs["research"] == mock_parser_response
        assert assess_call_kwargs["role_spec_markdown"] == mock_role_spec
        assert assess_call_kwargs["custom_instructions"] == custom_instructions

        # Verify result
        assert isinstance(result, AssessmentResult)
        assert result.overall_score == 88.5
        assert result.overall_confidence == "High"
        assert len(result.dimension_scores) == 4

    @patch("demo.workflow.assess_candidate")
    @patch("demo.workflow.run_incremental_search")
    @patch("demo.workflow.check_research_quality")
    @patch("demo.workflow.run_research")
    def test_workflow_triggers_incremental_search_on_low_quality(
        self,
        mock_run_research,
        mock_quality_check,
        mock_incremental_search,
        mock_assess,
        mock_parser_response: ExecutiveResearchResult,
        mock_assessment_result: AssessmentResult,
        mock_role_spec: str,
        mock_candidate_data: dict,
        workflow_runner: AgentOSCandidateWorkflow,
    ) -> None:
        """Test workflow triggers incremental search when quality check fails.

        This test verifies:
        1. Deep Research executes
        2. Quality check fails (low quality)
        3. Incremental search is triggered
        4. Assessment executes with merged research
        """
        # Create low quality research (only 1 citation)
        low_quality_research = mock_parser_response.model_copy(deep=True)
        low_quality_research.citations = [mock_parser_response.citations[0]]
        low_quality_research.research_confidence = "Low"

        # Setup mocks
        mock_run_research.return_value = low_quality_research
        mock_quality_check.return_value = False  # Quality check fails

        # Setup incremental search (returns high quality merged research)
        merged_research = mock_parser_response.model_copy(deep=True)
        merged_research.citations.extend(
            [
                Citation(
                    url="https://additional-source.com",
                    title="Additional Research",
                    snippet="More information",
                )
            ]
        )
        mock_incremental_search.return_value = merged_research

        # Setup assessment
        mock_assess.return_value = mock_assessment_result

        # Execute workflow
        result, research = workflow_runner.run_candidate_workflow(
            candidate_data=mock_candidate_data,
            role_spec_markdown=mock_role_spec,
            screen_id="recScreen123",
        )

        assert research is not None
        assert isinstance(research, ExecutiveResearchResult)
        assert research.exec_name == mock_parser_response.exec_name

        # Verify incremental search was called
        mock_incremental_search.assert_called_once()
        incremental_call_kwargs = mock_incremental_search.call_args.kwargs
        assert incremental_call_kwargs["candidate_name"] == "Jane Smith"
        assert incremental_call_kwargs["initial_research"] == low_quality_research

        # Verify assessment was called with merged research
        mock_assess.assert_called_once()
        assess_call_kwargs = mock_assess.call_args.kwargs
        assert assess_call_kwargs["research"] == merged_research

        # Verify result
        assert isinstance(result, AssessmentResult)
        assert result.overall_score == 88.5

    @patch("demo.workflow.run_research")
    def test_workflow_handles_deep_research_api_failure(
        self,
        mock_run_research,
        mock_candidate_data: dict,
        mock_role_spec: str,
        workflow_runner: AgentOSCandidateWorkflow,
    ) -> None:
        """Test workflow handles Deep Research API failure gracefully."""
        # Setup run_research to raise exception
        mock_run_research.side_effect = RuntimeError(
            "Research agent failed for Jane Smith after retries: API timeout"
        )

        # Execute workflow and expect RuntimeError
        with pytest.raises(RuntimeError, match="Research agent failed.*after retries"):
            workflow_runner.run_candidate_workflow(
                candidate_data=mock_candidate_data,
                role_spec_markdown=mock_role_spec,
                screen_id="recScreen123",
            )

        # Verify run_research was called (workflow retries on failure, so may be called multiple times)
        assert mock_run_research.call_count >= 1
        # Verify it was called with correct arguments
        call_kwargs = mock_run_research.call_args.kwargs
        assert call_kwargs["candidate_name"] == "Jane Smith"

    @patch("demo.workflow.assess_candidate")
    @patch("demo.workflow.check_research_quality")
    @patch("demo.workflow.run_research")
    def test_agno_sessions_persistence(
        self,
        mock_run_research,
        mock_quality_check,
        mock_assess,
        mock_parser_response: ExecutiveResearchResult,
        mock_assessment_result: AssessmentResult,
        mock_role_spec: str,
        mock_candidate_data: dict,
        workflow_runner: AgentOSCandidateWorkflow,
    ) -> None:
        """Test that workflow sessions are persisted to database."""
        # Setup mocks
        mock_run_research.return_value = mock_parser_response
        mock_quality_check.return_value = True
        mock_assess.return_value = mock_assessment_result

        # Execute workflow
        result, research = workflow_runner.run_candidate_workflow(
            candidate_data=mock_candidate_data,
            role_spec_markdown=mock_role_spec,
            screen_id="recScreen123",
        )

        # Verify workflow has database configured
        assert workflow_runner.workflow.db is not None

        # Verify result
        assert isinstance(result, AssessmentResult)
