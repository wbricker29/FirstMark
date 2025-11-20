"""Validation tests for Pydantic models."""

from demo.models import (
    AssessmentResult,
    CareerEntry,
    Citation,
    DimensionScore,
    ExecutiveResearchResult,
    MustHaveCheck,
    ScreenWebhookPayload,
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


def test_screen_webhook_payload_valid():
    """Test ScreenWebhookPayload model with valid payload."""
    payload = ScreenWebhookPayload(
        screen_slug={
            "screen_id": "recABC123",
            "screen_edited": "2025-11-18T20:01:46.000Z",
            "role_spec_slug": {
                "role_spec": {
                    "role_spec_id": "recfy1dp87DrnM8Y0",
                    "role_spec_name": "CFO (Chief Financial Officer)-Series B + Saas",
                    "role_spec_content": "### Dimensions\n\n1. Fundraising Excellence (25)",
                }
            },
            "search_slug": {
                "role": {
                    "ATID": "recGkLnHEGEvjDdvM",
                    "portco": "Pigment",
                    "role_title": "",
                    "role_type": "CFO (Chief Financial Officer)",
                    "role_description": "Own fundraising readiness",
                }
            },
            "candidate_slugs": [
                {
                    "candidate": {
                        "ATID": "recxjQfFfY4y6R25R",
                        "candidate_name": "Deb Schwartz",
                        "candidate_current_title": "CFO",
                        "candidate_normalized_title": "CFO (Chief Financial Officer)",
                        "candidate_current_company": "Cameo",
                        "candidate_location": "",
                        "candidate_linkedin": "",
                        "candidate_bio": "",
                    }
                }
            ],
        }
    )
    assert payload.screen_id == "recABC123"
    assert payload.portco_name == "Pigment"
    assert "Fundraising Excellence" in payload.spec_markdown
    print("✅ ScreenWebhookPayload model (valid) validated")


def test_screen_webhook_payload_get_candidates():
    """Test get_candidates() method with multiple candidates."""
    payload = ScreenWebhookPayload(
        screen_slug={
            "screen_id": "recABC123",
            "role_spec_slug": {
                "role_spec": {
                    "role_spec_id": "recRS123",
                    "role_spec_name": "CFO - Series B",
                    "role_spec_content": "# Spec",
                }
            },
            "search_slug": {
                "role": {
                    "ATID": "recR123",
                    "portco": "Pigment",
                    "role_type": "CFO",
                    "role_title": "",
                    "role_description": "",
                }
            },
            "candidate_slugs": [
                {
                    "candidate": {
                        "ATID": "recP1",
                        "candidate_name": "Jane Doe",
                        "candidate_current_title": "CFO",
                        "candidate_normalized_title": "CFO (Chief Financial Officer)",
                        "candidate_current_company": "Acme Inc",
                        "candidate_location": "San Francisco",
                        "candidate_linkedin": "https://linkedin.com/jane",
                        "candidate_bio": "Jane bio",
                    }
                },
                {
                    "candidate": {
                        "ATID": "recP2",
                        "candidate_name": "John Smith",
                        "candidate_current_title": "CTO",
                        "candidate_normalized_title": "CTO (Chief Technology Officer)",
                        "candidate_current_company": "Beta Corp",
                        "candidate_location": "New York",
                        "candidate_linkedin": "https://linkedin.com/john",
                        "candidate_bio": "John bio",
                    }
                },
            ],
        }
    )
    candidates = payload.get_candidates()
    assert len(candidates) == 2
    assert candidates[0]["id"] == "recP1"
    assert candidates[0]["name"] == "Jane Doe"
    assert candidates[0]["title"] == "CFO"
    assert candidates[0]["company"] == "Acme Inc"
    assert candidates[0]["linkedin"] == "https://linkedin.com/jane"
    assert candidates[0]["location"] == "San Francisco"
    assert candidates[0]["bio"] == "Jane bio"
    assert candidates[1]["id"] == "recP2"
    assert candidates[1]["name"] == "John Smith"
    print("✅ ScreenWebhookPayload.get_candidates() validated")


def test_screen_webhook_payload_optional_fields_empty():
    """Test payload with empty optional fields."""
    payload = ScreenWebhookPayload(
        screen_slug={
            "screen_id": "recABC123",
            "role_spec_slug": {
                "role_spec": {
                    "role_spec_id": "recRS123",
                    "role_spec_name": "CFO - Series B",
                    "role_spec_content": "# Spec",
                }
            },
            "search_slug": {
                "role": {
                    "ATID": "recR123",
                    "portco": "Pigment",
                    "role_type": "CFO",
                    "role_title": "",
                    "role_description": "",
                }
            },
            "candidate_slugs": [
                {
                    "candidate": {
                        "ATID": "recP1",
                        "candidate_name": "Jane Doe",
                        "candidate_current_title": "CFO",
                        "candidate_normalized_title": "",
                        "candidate_current_company": "Acme Inc",
                        "candidate_location": "",  # Empty optional field
                        "candidate_linkedin": "",
                        "candidate_bio": "",
                    }
                }
            ],
        }
    )
    candidates = payload.get_candidates()
    assert len(candidates) == 1
    assert candidates[0]["location"] == ""
    assert candidates[0]["bio"] == ""
    print("✅ ScreenWebhookPayload (empty optional fields) validated")


def test_screen_webhook_payload_missing_required_fields():
    """Test validation error for missing required fields."""
    import pytest

    with pytest.raises(Exception):  # Pydantic validation error
        ScreenWebhookPayload(
            screen_slug={
                "screen_id": "recABC123",
                # Missing required fields
            }
        )
    print("✅ ScreenWebhookPayload (missing required fields validation) validated")


if __name__ == "__main__":
    test_citation_model()
    test_career_entry_model()
    test_executive_research_result_model()
    test_dimension_score_model()
    test_must_have_check_model()
    test_assessment_result_model()
    test_screen_webhook_payload_valid()
    test_screen_webhook_payload_get_candidates()
    test_screen_webhook_payload_optional_fields_empty()
    test_screen_webhook_payload_missing_required_fields()
    print("\n✅ All Pydantic models validated successfully!")
