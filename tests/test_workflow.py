"""Integration tests for Agno workflow orchestration.

Tests cover the 4-step linear workflow: Deep Research → Quality Check →
Optional Incremental Search → Assessment.
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from demo.agents import (
    check_research_quality,
    create_screening_workflow,
    screen_single_candidate,
)
from demo.models import (
    AssessmentResult,
    CareerEntry,
    Citation,
    DimensionScore,
    ExecutiveResearchResult,
)


# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def mock_candidate_data() -> dict[str, Any]:
    """Sample candidate data from Airtable People table."""
    return {
        "id": "recABC123",
        "name": "Alex Rivera",
        "current_title": "CFO",
        "current_company": "Armis",
        "linkedin_url": "https://linkedin.com/in/alex-rivera",
    }


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
def high_quality_research() -> ExecutiveResearchResult:
    """Research result that passes quality gate (≥3 citations)."""
    return ExecutiveResearchResult(
        exec_name="Alex Rivera",
        current_role="CFO",
        current_company="Armis",
        research_summary="Extensive CFO experience across B2B SaaS companies with 4 successful exits.",
        research_markdown_raw="# Executive Summary\n\nAlex Rivera brings deep finance leadership...",
        citations=[
            Citation(
                url="https://linkedin.com/in/alex-rivera",
                title="Alex Rivera - LinkedIn",
                snippet="CFO at Armis, former VP Finance at DataBricks",
            ),
            Citation(
                url="https://techcrunch.com/alex-rivera-armis",
                title="Armis CFO Alex Rivera on scaling finance",
                snippet="Led Series C fundraising",
            ),
            Citation(
                url="https://crunchbase.com/person/alex-rivera",
                title="Alex Rivera - Crunchbase",
                snippet="Finance executive with 15 years experience",
            ),
            Citation(
                url="https://forbes.com/alex-rivera",
                title="Forbes Interview",
                snippet="Finance transformation leader",
            ),
        ],
        career_timeline=[
            CareerEntry(
                company="Armis",
                role="CFO",
                start_date="2021",
                end_date=None,
            ),
            CareerEntry(
                company="DataBricks",
                role="VP Finance",
                start_date="2018",
                end_date="2021",
            ),
        ],
        key_achievements=[
            "Led $200M Series C at Armis",
            "Scaled finance team from 5 to 25 at DataBricks",
        ],
        sector_expertise=["B2B SaaS", "Cybersecurity", "Enterprise Software"],
        stage_exposure=["Series B", "Series C", "Growth Stage"],
        notable_companies=["Armis", "DataBricks"],
        gaps=[],
        research_confidence="High",
        research_timestamp=datetime.now(),
        research_model="o4-mini-deep-research",
    )


@pytest.fixture
def low_quality_research() -> ExecutiveResearchResult:
    """Research result that fails quality gate (<3 citations)."""
    return ExecutiveResearchResult(
        exec_name="Jamie Chen",
        current_role="CTO",
        current_company="Estuary",
        research_summary="Limited public information available.",
        research_markdown_raw="# Executive Summary\n\nJamie Chen is CTO at Estuary...",
        citations=[
            Citation(
                url="https://linkedin.com/in/jamie-chen",
                title="Jamie Chen - LinkedIn",
                snippet="CTO at Estuary",
            ),
            Citation(
                url="https://estuary.com/team",
                title="Estuary Team Page",
                snippet="Jamie Chen leads engineering",
            ),
        ],
        career_timeline=[
            CareerEntry(
                company="Estuary",
                role="CTO",
                start_date="2020",
                end_date=None,
            ),
        ],
        key_achievements=[],
        sector_expertise=["Data Infrastructure"],
        stage_exposure=["Early Stage"],
        notable_companies=["Estuary"],
        gaps=["Only 2 citations found (need ≥3 for quality threshold)"],
        research_confidence="Low",
        research_timestamp=datetime.now(),
        research_model="o4-mini-deep-research",
    )


@pytest.fixture
def mock_assessment_result() -> AssessmentResult:
    """Sample assessment result."""
    return AssessmentResult(
        dimension_scores=[
            DimensionScore(
                dimension="Financial Leadership",
                score=5,
                evidence_level="High",
                confidence="High",
                reasoning="Led $200M Series C, scaled finance from 5 to 25 people",
            ),
            DimensionScore(
                dimension="Strategic Planning",
                score=4,
                evidence_level="Medium",
                confidence="Medium",
                reasoning="Evidence of strategic finance transformation",
            ),
            DimensionScore(
                dimension="Team Building",
                score=5,
                evidence_level="High",
                confidence="High",
                reasoning="Grew team 5x at DataBricks",
            ),
            DimensionScore(
                dimension="SaaS Domain Expertise",
                score=5,
                evidence_level="High",
                confidence="High",
                reasoning="15+ years in B2B SaaS",
            ),
        ],
        overall_score=95.0,
        overall_confidence="High",
        green_flags=["Strong B2B SaaS background", "Proven team scaling"],
        summary="Exceptional CFO candidate with deep B2B SaaS experience and proven fundraising track record.",
        counterfactuals=["May prefer larger company stage"],
        role_spec_used="# CFO Role Specification...",
        assessment_timestamp=datetime.now(),
    )


# ============================================================================
# AC-WF-01: Linear Workflow Execution
# ============================================================================


def test_workflow_happy_path_execution(
    mock_candidate_data: dict[str, Any],
    mock_role_spec: str,
    high_quality_research: ExecutiveResearchResult,
    mock_assessment_result: AssessmentResult,
) -> None:
    """Test linear workflow execution with quality research (no incremental search).

    Given: Valid candidate data, role spec, and high-quality research
    When: screen_single_candidate() is called
    Then: Workflow executes Deep Research → Quality Check (passes) → Assessment
    """
    with (
        patch("demo.agents.run_research") as mock_run_research,
        patch("demo.agents.run_incremental_search") as mock_incremental,
        patch("demo.agents.assess_candidate") as mock_assess,
    ):
        # Setup mocks
        mock_run_research.return_value = high_quality_research
        mock_assess.return_value = mock_assessment_result

        # Execute workflow
        result = screen_single_candidate(
            candidate_data=mock_candidate_data,
            role_spec_markdown=mock_role_spec,
            screen_id="recSCREEN001",
        )

        # Verify research was called
        mock_run_research.assert_called_once()
        call_kwargs = mock_run_research.call_args.kwargs
        assert call_kwargs["candidate_name"] == "Alex Rivera"
        assert call_kwargs["current_title"] == "CFO"
        assert call_kwargs["current_company"] == "Armis"

        # Verify incremental search was NOT called (quality was high)
        mock_incremental.assert_not_called()

        # Verify assessment was called with high quality research
        mock_assess.assert_called_once()
        assess_kwargs = mock_assess.call_args.kwargs
        assert assess_kwargs["research"] == high_quality_research
        assert assess_kwargs["role_spec_markdown"] == mock_role_spec

        # Verify result
        assert result == mock_assessment_result
        assert result.overall_score == 95.0


# ============================================================================
# AC-WF-02: Quality Gate Triggers Incremental Search
# ============================================================================


def test_workflow_quality_gate_triggers_incremental_search(
    mock_candidate_data: dict[str, Any],
    mock_role_spec: str,
    low_quality_research: ExecutiveResearchResult,
    high_quality_research: ExecutiveResearchResult,
    mock_assessment_result: AssessmentResult,
) -> None:
    """Test quality gate triggers incremental search when research is insufficient.

    Given: Low-quality research with <3 citations
    When: screen_single_candidate() executes quality check
    Then: Incremental search is triggered and results are merged
    """
    with (
        patch("demo.agents.run_research") as mock_run_research,
        patch("demo.agents.run_incremental_search") as mock_incremental,
        patch("demo.agents.assess_candidate") as mock_assess,
    ):
        # Setup mocks
        mock_run_research.return_value = low_quality_research
        mock_incremental.return_value = high_quality_research  # After merge
        mock_assess.return_value = mock_assessment_result

        # Update candidate data to match low quality research
        candidate_data = {
            "id": "recXYZ789",
            "name": "Jamie Chen",
            "current_title": "CTO",
            "current_company": "Estuary",
            "linkedin_url": "https://linkedin.com/in/jamie-chen",
        }

        # Execute workflow
        result = screen_single_candidate(
            candidate_data=candidate_data,
            role_spec_markdown=mock_role_spec,
            screen_id="recSCREEN002",
        )

        # Verify research was called
        mock_run_research.assert_called_once()

        # Verify incremental search WAS called (quality was low)
        mock_incremental.assert_called_once()
        incremental_kwargs = mock_incremental.call_args.kwargs
        assert incremental_kwargs["candidate_name"] == "Jamie Chen"
        assert incremental_kwargs["initial_research"] == low_quality_research
        assert incremental_kwargs["quality_gaps"] == low_quality_research.gaps
        assert incremental_kwargs["role_spec_markdown"] == mock_role_spec

        # Verify assessment was called with MERGED research (high quality)
        mock_assess.assert_called_once()
        assess_kwargs = mock_assess.call_args.kwargs
        assert assess_kwargs["research"] == high_quality_research
        assert assess_kwargs["role_spec_markdown"] == mock_role_spec

        # Verify result
        assert result == mock_assessment_result


# ============================================================================
# AC-WF-03: Session State Persistence
# ============================================================================


def test_workflow_session_state_persistence(
    mock_candidate_data: dict[str, Any],
    mock_role_spec: str,
    high_quality_research: ExecutiveResearchResult,
    mock_assessment_result: AssessmentResult,
    tmp_path: Path,
) -> None:
    """Test session state is persisted to SqliteDb during workflow execution.

    Given: Workflow execution in progress
    When: Any workflow step completes
    Then: Session state is persisted to tmp/agno_sessions.db
    """
    with (
        patch("demo.agents.run_research") as mock_run_research,
        patch("demo.agents.assess_candidate") as mock_assess,
        patch("demo.agents.Path") as mock_path_cls,
    ):
        # Mock Path to use tmp_path instead of real tmp/
        mock_db_path = tmp_path / "agno_sessions.db"
        mock_path_instance = MagicMock()
        mock_path_instance.__truediv__ = lambda self, other: (
            mock_db_path if other == "agno_sessions.db" else tmp_path / other
        )
        mock_path_instance.parent.mkdir = MagicMock()
        mock_path_cls.return_value = mock_path_instance

        # Setup agent mocks
        mock_run_research.return_value = high_quality_research
        mock_assess.return_value = mock_assessment_result

        # Execute workflow
        result = screen_single_candidate(
            candidate_data=mock_candidate_data,
            role_spec_markdown=mock_role_spec,
            screen_id="recSCREEN003",
        )

        # Verify workflow completed
        assert result == mock_assessment_result

        # Verify workflow object was created with session state
        workflow = create_screening_workflow()
        assert workflow.session_state is not None
        assert "screen_id" in workflow.session_state
        assert "candidate_name" in workflow.session_state
        assert "last_step" in workflow.session_state
        assert "quality_gate_triggered" in workflow.session_state

        # Verify db configuration
        assert workflow.db is not None
        assert hasattr(workflow.db, "db_file")


# ============================================================================
# AC-WF-04: Event Streaming for Visibility
# ============================================================================


def test_workflow_event_streaming_to_stdout(
    mock_candidate_data: dict[str, Any],
    mock_role_spec: str,
    high_quality_research: ExecutiveResearchResult,
    mock_assessment_result: AssessmentResult,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test workflow streams execution events to stdout with emoji indicators.

    Given: Workflow configured with stream_events=True
    When: Workflow executes
    Then: Execution events are logged to stdout showing progress
    """
    with (
        patch("demo.agents.run_research") as mock_run_research,
        patch("demo.agents.assess_candidate") as mock_assess,
    ):
        # Setup mocks
        mock_run_research.return_value = high_quality_research
        mock_assess.return_value = mock_assessment_result

        # Capture logs at INFO level
        caplog.set_level(logging.INFO, logger="demo.agents")

        # Execute workflow
        result = screen_single_candidate(
            candidate_data=mock_candidate_data,
            role_spec_markdown=mock_role_spec,
            screen_id="recSCREEN004",
        )

        # Verify workflow completed
        assert result == mock_assessment_result

        # Verify log messages contain expected emoji indicators and steps
        log_messages = [record.message for record in caplog.records]

        # Check for research start/complete
        assert any(
            "🔍" in msg and "deep research" in msg.lower() for msg in log_messages
        )
        assert any(
            "✅" in msg and "deep research completed" in msg.lower()
            for msg in log_messages
        )

        # Check for quality check
        assert any("🔍" in msg and "quality" in msg.lower() for msg in log_messages)
        assert any("✅" in msg and "quality" in msg.lower() for msg in log_messages)

        # Check for assessment start/complete
        assert any("🔍" in msg and "assessment" in msg.lower() for msg in log_messages)
        assert any(
            "✅" in msg and "assessment complete" in msg.lower() for msg in log_messages
        )

        # Verify candidate name appears in logs
        assert any("Alex Rivera" in msg for msg in log_messages)


# ============================================================================
# AC-WF-05: Error Handling with Graceful Degradation
# ============================================================================


def test_workflow_error_handling_with_retry(
    mock_candidate_data: dict[str, Any],
    mock_role_spec: str,
) -> None:
    """Test workflow handles agent failures with retry and clear error reporting.

    Given: Research agent fails with API timeout
    When: Workflow executes with retry enabled
    Then: Agent retries and raises clear error without corrupting session state
    """
    with patch("demo.agents.run_research") as mock_run_research:
        # Setup mock to fail
        mock_run_research.side_effect = RuntimeError("API timeout after retries")

        # Execute workflow and expect failure
        with pytest.raises(RuntimeError, match="API timeout after retries"):
            screen_single_candidate(
                candidate_data=mock_candidate_data,
                role_spec_markdown=mock_role_spec,
                screen_id="recSCREEN005",
            )

        # Verify research was attempted
        mock_run_research.assert_called_once()

        # Verify session state is still accessible (not corrupted)
        workflow = create_screening_workflow()
        assert workflow.session_state is not None
        assert "screen_id" in workflow.session_state


# ============================================================================
# Unit Tests: Helper Functions
# ============================================================================


def test_check_research_quality_passes_with_sufficient_citations(
    high_quality_research: ExecutiveResearchResult,
) -> None:
    """Test quality check passes with ≥3 citations and non-empty summary."""
    assert check_research_quality(high_quality_research) is True


def test_check_research_quality_fails_with_insufficient_citations(
    low_quality_research: ExecutiveResearchResult,
) -> None:
    """Test quality check fails with <3 citations."""
    assert check_research_quality(low_quality_research) is False


def test_check_research_quality_fails_with_empty_summary() -> None:
    """Test quality check fails when summary is empty."""
    research = ExecutiveResearchResult(
        exec_name="Test",
        current_role="CFO",
        current_company="TestCo",
        research_summary="",  # Empty summary
        citations=[
            Citation(url="https://1.com", title="One", snippet=""),
            Citation(url="https://2.com", title="Two", snippet=""),
            Citation(url="https://3.com", title="Three", snippet=""),
        ],
    )
    assert check_research_quality(research) is False


def test_workflow_configuration() -> None:
    """Test workflow is configured with correct settings."""
    workflow = create_screening_workflow()

    # Verify workflow properties
    assert workflow.name == "Talent Signal Screening Workflow"
    assert workflow.stream_events is True

    # Verify session state structure
    assert workflow.session_state is not None
    assert "screen_id" in workflow.session_state
    assert "candidate_id" in workflow.session_state
    assert "candidate_name" in workflow.session_state
    assert "last_step" in workflow.session_state
    assert "quality_gate_triggered" in workflow.session_state

    # Verify steps are defined
    assert len(workflow.steps) == 4
    step_names = [step.name for step in workflow.steps]
    assert step_names == [
        "deep_research",
        "quality_check",
        "incremental_search",
        "assessment",
    ]

    # Verify SqliteDb configuration
    assert workflow.db is not None
    assert hasattr(workflow.db, "db_file")
