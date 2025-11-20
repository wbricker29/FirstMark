"""Integration tests for workflow helper functions.

Tests cover helper functions used by the workflow orchestration.
Note: Legacy workflow tests (screen_single_candidate, create_screening_workflow) have been
removed as those functions no longer exist. Workflow orchestration is now tested via
AgentOSCandidateWorkflow in test_agentos_workflow_mocked.py and related files.

Quality check tests have been moved to test_quality_check.py to consolidate all
quality check testing in one place.
"""

from demo.models import ExecutiveResearchResult
from demo.screening_helpers import reconstruct_research


class TestReconstructResearch:
    """Tests for reconstruct_research() helper function."""

    def test_reconstruct_from_dict(self):
        """Test reconstruction from dict representation."""
        research_dict = {
            "exec_name": "Jane Doe",
            "current_role": "CTO",
            "current_company": "Acme Corp",
            "research_summary": "Experienced CTO",
            "citations": [],
            "key_achievements": [],
            "notable_companies": [],
            "sector_expertise": [],
            "stage_exposure": [],
            "career_timeline": [],
            "gaps": [],
        }

        result = reconstruct_research(research_dict)

        assert isinstance(result, ExecutiveResearchResult)
        assert result.exec_name == "Jane Doe"
        assert result.current_role == "CTO"
        assert result.current_company == "Acme Corp"

    def test_reconstruct_from_model_instance(self):
        """Test that ExecutiveResearchResult instances are returned as-is."""
        original = ExecutiveResearchResult(
            exec_name="John Smith",
            current_role="CFO",
            current_company="TechCo",
            research_summary="Finance leader",
        )

        result = reconstruct_research(original)

        assert result is original
        assert isinstance(result, ExecutiveResearchResult)
        assert result.exec_name == "John Smith"

    def test_reconstruct_with_minimal_dict(self):
        """Test reconstruction with minimal required fields."""
        minimal_dict = {
            "exec_name": "Alex Johnson",
            "current_role": "VP Engineering",
            "current_company": "StartupInc",
            "research_summary": "Technical leader",
        }

        result = reconstruct_research(minimal_dict)

        assert isinstance(result, ExecutiveResearchResult)
        assert result.exec_name == "Alex Johnson"
        assert result.citations == []
        assert result.key_achievements == []
