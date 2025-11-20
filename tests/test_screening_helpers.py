"""Unit tests for screening helper markdown formatters."""

from datetime import datetime

from demo.models import (
    AssessmentResult,
    DimensionScore,
    ExecutiveResearchResult,
    MustHaveCheck,
)
from demo.screening_helpers import (
    render_assessment_markdown_inline,
    render_screen_report,
)


def _sample_assessment() -> AssessmentResult:
    return AssessmentResult(
        overall_score=87.5,
        overall_confidence="High",
        dimension_scores=[
            DimensionScore(
                dimension="Fundraising",
                score=4,
                evidence_level="High",
                confidence="High",
                reasoning="Raised $500M across two IPOs",
            ),
            DimensionScore(
                dimension="Systems",
                score=3,
                evidence_level="Medium",
                confidence="Medium",
                reasoning="Scaled ERP across regions",
            ),
        ],
        must_haves_check=[
            MustHaveCheck(
                requirement="IPO experience", met=True, evidence="Led 2021 IPO"
            ),
            MustHaveCheck(requirement="PE reporting", met=False, evidence=None),
        ],
        red_flags_detected=["Limited public company tenure"],
        green_flags=["Excellent board communication"],
        counterfactuals=["Consider as interim CFO for Portco X"],
        summary="Evidence-backed operator with deep fundraising breadth.",
        assessment_timestamp=datetime(2025, 1, 19, 12, 0, 0),
        assessment_model="gpt-5-mini",
        role_spec_used="# CFO Spec\n- Requirement",
    )


def _sample_research() -> ExecutiveResearchResult:
    return ExecutiveResearchResult(
        exec_name="Jane Doe",
        current_role="CFO",
        current_company="TechCo",
        career_timeline=[],
        research_summary="Former IPO leader with repeatable playbook across finance ops.",
        research_markdown_raw="# Research\n- Lots of data",
        research_timestamp=datetime(2025, 1, 19, 11, 0, 0),
        research_model="o4-mini-deep-research",
        key_achievements=["Led $500M IPO", "Scaled finance org to 200+"],
    )


def test_render_assessment_markdown_inline_includes_key_sections():
    candidate = {
        "id": "recCandidate123",
        "name": "Jane Doe",
        "title": "CFO",
        "company": "TechCo",
        "linkedin": "https://linkedin.com/in/janedoe",
    }
    assessment = _sample_assessment()
    research = _sample_research()

    inline_markdown = render_assessment_markdown_inline(candidate, assessment, research)

    assert "### Jane Doe" in inline_markdown
    assert "Overall Score" in inline_markdown
    assert "Fundraising" in inline_markdown
    assert "Must-Haves" in inline_markdown
    assert "Research Signal" in inline_markdown


def test_render_screen_report_combines_assessment_and_research():
    candidate = {
        "id": "recCandidate123",
        "name": "Jane Doe",
        "title": "CFO",
        "company": "TechCo",
        "linkedin": "https://linkedin.com/in/janedoe",
    }
    assessment = _sample_assessment()
    research = _sample_research()

    report = render_screen_report(
        screen_id="recScreen111",
        candidate=candidate,
        assessment=assessment,
        research=research,
        role_spec_markdown="# CFO Spec\n- Requirement 1\n- Requirement 2",
        custom_instructions="Prioritize IPO depth",
    )

    assert "# Screen Report: Jane Doe" in report
    assert "## Candidate Snapshot" in report
    assert "### Dimension Details" in report
    assert "### Key Achievements" in report
    assert "## Role Spec Snapshot" in report


def test_render_screen_report_without_research_handles_gaps():
    candidate = {
        "id": "recCandidate999",
        "name": "John Smith",
        "title": "VP Finance",
        "company": "GrowthCo",
    }
    assessment = _sample_assessment()

    report = render_screen_report(
        screen_id="recScreen222",
        candidate=candidate,
        assessment=assessment,
        research=None,
        role_spec_markdown=None,
        custom_instructions=None,
    )

    assert "John Smith" in report
    assert "No research results were available" in report
    assert "## Role Spec Snapshot" not in report
