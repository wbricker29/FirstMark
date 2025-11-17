"""Validation tests for Pydantic models."""

from demo.models import (
    AssessmentResult,
    CareerEntry,
    Citation,
    DimensionScore,
    ExecutiveResearchResult,
    MustHaveCheck,
)


def test_citation_model():
    """Test Citation model instantiation."""
    citation = Citation(
        url="https://example.com",
        title="Example Article",
        snippet="This is a test snippet",
        relevance_note="Relevant for testing",
    )
    assert citation.url == "https://example.com"
    assert citation.title == "Example Article"
    print("✅ Citation model validated")


def test_career_entry_model():
    """Test CareerEntry model instantiation."""
    entry = CareerEntry(
        company="Example Corp",
        role="CFO",
        start_date="2020-01",
        end_date="2023-12",
        key_achievements=["Led Series B", "Built finance team"],
    )
    assert entry.company == "Example Corp"
    assert len(entry.key_achievements) == 2
    print("✅ CareerEntry model validated")


def test_executive_research_result_model():
    """Test ExecutiveResearchResult model instantiation."""
    research = ExecutiveResearchResult(
        exec_name="Jane Doe",
        current_role="CFO",
        current_company="TechCo",
        research_summary="Experienced CFO with 15 years in SaaS",
        career_timeline=[
            CareerEntry(company="TechCo", role="CFO", start_date="2020-01")
        ],
        total_years_experience=15,
        fundraising_experience="Led 3 rounds totaling $50M",
        sector_expertise=["SaaS", "FinTech"],
        stage_exposure=["Series A", "Series B", "Growth"],
        citations=[
            Citation(
                url="https://linkedin.com/jane",
                title="Jane Doe Profile",
                snippet="CFO at TechCo",
            )
        ],
        research_confidence="High",
    )
    assert research.exec_name == "Jane Doe"
    assert len(research.sector_expertise) == 2
    assert research.research_model == "o4-mini-deep-research"
    print("✅ ExecutiveResearchResult model validated")


def test_dimension_score_model():
    """Test DimensionScore model with evidence-aware scoring."""
    # Test with valid score
    score = DimensionScore(
        dimension="Fundraising",
        score=4,
        evidence_level="High",
        confidence="High",
        reasoning="Strong track record of fundraising",
        evidence_quotes=["Led Series B", "Raised $50M"],
        citation_urls=["https://example.com"],
    )
    assert score.score == 4
    assert score.dimension == "Fundraising"
    print("✅ DimensionScore model (with score) validated")

    # Test with None score (insufficient evidence)
    unknown_score = DimensionScore(
        dimension="Team Building",
        score=None,  # Evidence-aware: Unknown
        evidence_level="Low",
        confidence="Low",
        reasoning="Insufficient public evidence",
    )
    assert unknown_score.score is None
    print("✅ DimensionScore model (None score) validated")


def test_must_have_check_model():
    """Test MustHaveCheck model instantiation."""
    check = MustHaveCheck(
        requirement="10+ years experience",
        met=True,
        evidence="15 years total experience",
    )
    assert check.met is True
    print("✅ MustHaveCheck model validated")


def test_assessment_result_model():
    """Test AssessmentResult model instantiation."""
    assessment = AssessmentResult(
        overall_score=75.5,
        overall_confidence="High",
        dimension_scores=[
            DimensionScore(
                dimension="Fundraising",
                score=4,
                evidence_level="High",
                confidence="High",
                reasoning="Strong fundraising track record",
            )
        ],
        must_haves_check=[
            MustHaveCheck(requirement="10+ years", met=True, evidence="15 years")
        ],
        red_flags_detected=[],
        green_flags=["Strong CFO background", "Multiple successful fundraises"],
        summary="Excellent candidate with strong fundraising and operational experience",
        counterfactuals=["May lack experience in hyper-growth stage"],
        assessment_model="gpt-5-mini",
        role_spec_used="CFO-Pigment",
    )
    assert assessment.overall_score == 75.5
    assert len(assessment.dimension_scores) == 1
    assert len(assessment.green_flags) == 2
    print("✅ AssessmentResult model validated")


if __name__ == "__main__":
    test_citation_model()
    test_career_entry_model()
    test_executive_research_result_model()
    test_dimension_score_model()
    test_must_have_check_model()
    test_assessment_result_model()
    print("\n✅ All Pydantic models validated successfully!")
