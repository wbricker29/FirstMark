"""Unit tests for AirtableClient with mocked pyairtable API calls.

This test module validates all CRUD methods in demo/airtable_client.py
using pytest fixtures to mock pyairtable Api and Table objects.
"""

from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest

from demo.airtable_client import AirtableClient
from demo.models import AssessmentResult, DimensionScore, ExecutiveResearchResult


@pytest.fixture
def mock_api():
    """Mock pyairtable Api object with table() method."""
    api = MagicMock()
    return api


@pytest.fixture
def mock_tables(mock_api):
    """Mock pyairtable Table objects for each table in the schema."""
    tables = {
        "Platform-Screens": MagicMock(),
        "People": MagicMock(),
        "Platform-Role_Specs": MagicMock(),
        "Platform-Assessments": MagicMock(),
        "Platform-Searches": MagicMock(),
    }

    def table_factory(base_id: str, table_name: str):
        return tables[table_name]

    mock_api.table.side_effect = table_factory
    return tables


@pytest.fixture
def client(mock_api, mock_tables):
    """Create AirtableClient with mocked Api and connected mock tables."""
    with patch("demo.airtable_client.Api", return_value=mock_api):
        client_instance = AirtableClient(
            api_key="pat_test_key", base_id="appTestBase123"
        )
        # Wire up the mock tables to the client instance
        client_instance.screens = mock_tables["Platform-Screens"]
        client_instance.people = mock_tables["People"]
        client_instance.role_specs = mock_tables["Platform-Role_Specs"]
        client_instance.assessments = mock_tables["Platform-Assessments"]
        client_instance.searches = mock_tables["Platform-Searches"]
        return client_instance


# ============================================================================
# Tests for __init__ method
# ============================================================================


def test_init_with_valid_credentials(mock_api):
    """Test AirtableClient initialization with valid credentials."""
    with patch("demo.airtable_client.Api", return_value=mock_api):
        client = AirtableClient(api_key="pat_valid_key", base_id="appValidBase")

    assert client.api_key == "pat_valid_key"
    assert client.base_id == "appValidBase"
    assert client.api == mock_api
    assert mock_api.table.call_count == 5  # 5 tables initialized


def test_init_with_base_id_containing_table_suffix(mock_api):
    """Test that base_id with /tblXXX suffix is cleaned correctly."""
    with patch("demo.airtable_client.Api", return_value=mock_api):
        client = AirtableClient(api_key="pat_key", base_id="appBaseID/tblTableSuffix")

    assert client.base_id == "appBaseID"
    assert "/" not in client.base_id


def test_init_with_whitespace_credentials(mock_api):
    """Test that credentials are stripped of whitespace."""
    with patch("demo.airtable_client.Api", return_value=mock_api):
        client = AirtableClient(
            api_key="  pat_key_with_spaces  ", base_id="  appBase123  "
        )

    assert client.api_key == "pat_key_with_spaces"
    assert client.base_id == "appBase123"


def test_init_with_empty_api_key():
    """Test that empty API key raises ValueError."""
    with pytest.raises(ValueError, match="Airtable API key is required"):
        AirtableClient(api_key="", base_id="appValidBase")


def test_init_with_empty_base_id():
    """Test that empty base_id raises ValueError."""
    with pytest.raises(ValueError, match="Airtable base ID is required"):
        AirtableClient(api_key="pat_valid_key", base_id="")


def test_init_with_whitespace_only_api_key():
    """Test that whitespace-only API key raises ValueError."""
    with pytest.raises(ValueError, match="Airtable API key is required"):
        AirtableClient(api_key="   ", base_id="appValidBase")


def test_init_with_whitespace_only_base_id():
    """Test that whitespace-only base_id raises ValueError."""
    with pytest.raises(ValueError, match="Airtable base ID is required"):
        AirtableClient(api_key="pat_valid_key", base_id="   ")


# ============================================================================
# Tests for get_screen method
# ============================================================================


def test_get_screen_with_valid_screen_id(client, mock_tables):
    """Test successful screen fetch with linked search and candidates."""
    # Mock screen record
    mock_tables["Platform-Screens"].get.return_value = {
        "id": "recScreen123",
        "fields": {
            "status": "Ready to Screen",
            "Search": ["recSearch456"],
            "Candidates": ["recCandidate1", "recCandidate2"],
        },
    }

    # Mock search record with role spec link
    mock_tables["Platform-Searches"].get.return_value = {
        "id": "recSearch456",
        "fields": {"Role Spec": ["recRoleSpec789"], "search_name": "CFO Search"},
    }

    # Mock candidate records
    mock_tables["People"].get.side_effect = [
        {"id": "recCandidate1", "fields": {"name": "Jane Doe"}},
        {"id": "recCandidate2", "fields": {"name": "John Smith"}},
    ]

    result = client.get_screen("recScreen123")

    assert result["id"] == "recScreen123"
    assert result["fields"]["status"] == "Ready to Screen"
    assert result["role_spec_id"] == "recRoleSpec789"
    assert len(result["candidates"]) == 2
    assert result["candidates"][0]["fields"]["name"] == "Jane Doe"
    assert result["search"]["id"] == "recSearch456"


def test_get_screen_with_no_linked_search(client, mock_tables):
    """Test get_screen when screen has no linked search."""
    mock_tables["Platform-Screens"].get.return_value = {
        "id": "recScreen123",
        "fields": {"status": "Ready to Screen", "Candidates": []},
    }

    result = client.get_screen("recScreen123")

    assert result["id"] == "recScreen123"
    assert result["search"] is None
    assert result["role_spec_id"] is None
    assert result["candidates"] == []


def test_get_screen_with_empty_candidates(client, mock_tables):
    """Test get_screen when screen has no linked candidates."""
    mock_tables["Platform-Screens"].get.return_value = {
        "id": "recScreen123",
        "fields": {"status": "Ready to Screen"},
    }

    result = client.get_screen("recScreen123")

    assert result["candidates"] == []


def test_get_screen_with_empty_screen_id(client):
    """Test that empty screen_id raises ValueError."""
    with pytest.raises(ValueError, match="screen_id is required"):
        client.get_screen("")


def test_get_screen_with_whitespace_only_screen_id(client):
    """Test that whitespace-only screen_id raises ValueError."""
    with pytest.raises(ValueError, match="screen_id is required"):
        client.get_screen("   ")


def test_get_screen_with_api_error(client, mock_tables):
    """Test get_screen when Airtable API call fails."""
    mock_tables["Platform-Screens"].get.side_effect = RuntimeError(
        "API connection timeout"
    )

    with pytest.raises(RuntimeError, match="Failed to fetch screen"):
        client.get_screen("recScreen123")


def test_get_screen_with_search_fetch_error(client, mock_tables):
    """Test get_screen when linked search fetch fails."""
    mock_tables["Platform-Screens"].get.return_value = {
        "id": "recScreen123",
        "fields": {"Search": ["recSearch456"]},
    }
    mock_tables["Platform-Searches"].get.side_effect = RuntimeError("Search not found")

    with pytest.raises(RuntimeError, match="Failed to fetch search"):
        client.get_screen("recScreen123")


def test_get_screen_with_candidate_fetch_error(client, mock_tables):
    """Test get_screen when candidate fetch fails."""
    mock_tables["Platform-Screens"].get.return_value = {
        "id": "recScreen123",
        "fields": {"Candidates": ["recCandidate1"]},
    }
    mock_tables["People"].get.side_effect = RuntimeError("Candidate not found")

    with pytest.raises(RuntimeError, match="Failed to fetch candidate"):
        client.get_screen("recScreen123")


# ============================================================================
# Tests for get_role_spec method
# ============================================================================


def test_get_role_spec_with_valid_spec_id(client, mock_tables):
    """Test successful role spec fetch with structured_spec_markdown."""
    mock_tables["Platform-Role_Specs"].get.return_value = {
        "id": "recRoleSpec789",
        "fields": {
            "role_title": "CFO",
            "structured_spec_markdown": "# CFO Role Spec\n\n## Must-Haves...",
        },
    }

    result = client.get_role_spec("recRoleSpec789")

    assert result["id"] == "recRoleSpec789"
    assert result["fields"]["role_title"] == "CFO"
    assert result["structured_spec_markdown"].startswith("# CFO Role Spec")


def test_get_role_spec_with_spec_content_fallback(client, mock_tables):
    """Test role spec fetch with Spec Content field fallback."""
    mock_tables["Platform-Role_Specs"].get.return_value = {
        "id": "recRoleSpec789",
        "fields": {"Spec Content": "# Role Spec Content\n\nDetails..."},
    }

    result = client.get_role_spec("recRoleSpec789")

    assert result["structured_spec_markdown"].startswith("# Role Spec Content")


def test_get_role_spec_with_spec_markdown_fallback(client, mock_tables):
    """Test role spec fetch with spec_markdown field fallback."""
    mock_tables["Platform-Role_Specs"].get.return_value = {
        "id": "recRoleSpec789",
        "fields": {"spec_markdown": "# Spec Markdown\n\nDetails..."},
    }

    result = client.get_role_spec("recRoleSpec789")

    assert result["structured_spec_markdown"].startswith("# Spec Markdown")


def test_get_role_spec_with_missing_markdown_field(client, mock_tables):
    """Test that missing markdown content raises RuntimeError."""
    mock_tables["Platform-Role_Specs"].get.return_value = {
        "id": "recRoleSpec789",
        "fields": {"role_title": "CFO"},
    }

    with pytest.raises(RuntimeError, match="missing structured_spec_markdown content"):
        client.get_role_spec("recRoleSpec789")


def test_get_role_spec_with_empty_spec_id(client):
    """Test that empty spec_id raises ValueError."""
    with pytest.raises(ValueError, match="spec_id is required"):
        client.get_role_spec("")


def test_get_role_spec_with_whitespace_only_spec_id(client):
    """Test that whitespace-only spec_id raises ValueError."""
    with pytest.raises(ValueError, match="spec_id is required"):
        client.get_role_spec("   ")


def test_get_role_spec_with_api_error(client, mock_tables):
    """Test get_role_spec when Airtable API call fails."""
    mock_tables["Platform-Role_Specs"].get.side_effect = RuntimeError(
        "API connection timeout"
    )

    with pytest.raises(RuntimeError, match="Failed to fetch role spec"):
        client.get_role_spec("recRoleSpec789")


# ============================================================================
# Tests for write_assessment method
# ============================================================================


def test_write_assessment_with_research_and_assessment(client, mock_tables):
    """Test successful assessment write with both research and assessment data."""
    # Create sample assessment
    assessment = AssessmentResult(
        overall_score=85.0,
        overall_confidence="High",
        dimension_scores=[
            DimensionScore(
                dimension="Fundraising Experience",
                score=4,
                evidence_level="High",
                confidence="High",
                reasoning="Strong IPO experience",
                evidence_quotes=["Led $200M IPO"],
                citation_urls=["https://example.com"],
            )
        ],
        summary="Excellent match for CFO role",
        assessment_timestamp=datetime(2025, 11, 17, 10, 0, 0),
        assessment_model="gpt-5-mini",
        role_spec_used="# CFO Role Spec",
    )

    # Create sample research
    research = ExecutiveResearchResult(
        exec_name="Jane Doe",
        current_role="VP Finance",
        current_company="TechCo",
        research_summary="Strong finance background",
        research_timestamp=datetime(2025, 11, 17, 9, 0, 0),
        research_model="o4-mini-deep-research",
    )

    # Mock Airtable response
    mock_tables["Platform-Assessments"].create.return_value = {
        "id": "recAssessment123",
        "fields": {},
    }

    result = client.write_assessment(
        screen_id="recScreen123",
        candidate_id="recCandidate456",
        assessment=assessment,
        research=research,
    )

    assert result == "recAssessment123"

    # Verify create was called with correct fields
    call_args = mock_tables["Platform-Assessments"].create.call_args
    fields = call_args[0][0]

    assert fields["Screen"] == ["recScreen123"]
    assert fields["Candidate"] == ["recCandidate456"]
    assert fields["Status"] == "Complete"
    assert fields["Overall Score"] == 85.0
    assert fields["Overall Confidence"] == "High"
    assert fields["Topline Summary"] == "Excellent match for CFO role"
    assert fields["Assessment Model"] == "gpt-5-mini"
    # Note: role_spec_used is stored in Assessment JSON, not as a direct field
    assert "Research Structured JSON" in fields
    assert fields["Research Model"] == "o4-mini-deep-research"


def test_write_assessment_without_research(client, mock_tables):
    """Test assessment write without research data."""
    assessment = AssessmentResult(
        overall_score=75.0,
        overall_confidence="Medium",
        dimension_scores=[],
        summary="Good candidate",
        assessment_timestamp=datetime(2025, 11, 17, 10, 0, 0),
        assessment_model="gpt-5-mini",
    )

    mock_tables["Platform-Assessments"].create.return_value = {
        "id": "recAssessment789",
        "fields": {},
    }

    result = client.write_assessment(
        screen_id="recScreen123",
        candidate_id="recCandidate456",
        assessment=assessment,
        research=None,
    )

    assert result == "recAssessment789"

    # Verify research fields are not included
    call_args = mock_tables["Platform-Assessments"].create.call_args
    fields = call_args[0][0]

    assert "research_structured_json" not in fields
    assert "research_model" not in fields


def test_write_assessment_without_role_spec(client, mock_tables):
    """Test assessment write without role_spec_used field."""
    assessment = AssessmentResult(
        overall_score=70.0,
        overall_confidence="Low",
        dimension_scores=[],
        summary="Moderate candidate",
        assessment_timestamp=datetime(2025, 11, 17, 10, 0, 0),
        assessment_model="gpt-5-mini",
        role_spec_used=None,
    )

    mock_tables["Platform-Assessments"].create.return_value = {
        "id": "recAssessment999",
        "fields": {},
    }

    client.write_assessment(
        screen_id="recScreen123",
        candidate_id="recCandidate456",
        assessment=assessment,
    )

    # Verify role_spec_markdown is not included
    call_args = mock_tables["Platform-Assessments"].create.call_args
    fields = call_args[0][0]

    assert "role_spec_markdown" not in fields


def test_write_assessment_with_empty_screen_id(client):
    """Test that empty screen_id raises ValueError."""
    assessment = AssessmentResult(
        overall_score=80.0,
        overall_confidence="High",
        dimension_scores=[],
        summary="Test",
    )

    with pytest.raises(ValueError, match="screen_id and candidate_id are required"):
        client.write_assessment(
            screen_id="", candidate_id="recCandidate123", assessment=assessment
        )


def test_write_assessment_with_empty_candidate_id(client):
    """Test that empty candidate_id raises ValueError."""
    assessment = AssessmentResult(
        overall_score=80.0,
        overall_confidence="High",
        dimension_scores=[],
        summary="Test",
    )

    with pytest.raises(ValueError, match="screen_id and candidate_id are required"):
        client.write_assessment(
            screen_id="recScreen123", candidate_id="", assessment=assessment
        )


def test_write_assessment_with_api_error(client, mock_tables):
    """Test write_assessment when Airtable API call fails."""
    assessment = AssessmentResult(
        overall_score=80.0,
        overall_confidence="High",
        dimension_scores=[],
        summary="Test",
    )

    mock_tables["Platform-Assessments"].create.side_effect = RuntimeError(
        "API connection timeout"
    )

    with pytest.raises(RuntimeError, match="Failed to write assessment"):
        client.write_assessment(
            screen_id="recScreen123",
            candidate_id="recCandidate456",
            assessment=assessment,
        )


def test_write_assessment_with_missing_record_id(client, mock_tables):
    """Test write_assessment when Airtable doesn't return record ID."""
    assessment = AssessmentResult(
        overall_score=80.0,
        overall_confidence="High",
        dimension_scores=[],
        summary="Test",
    )

    mock_tables["Platform-Assessments"].create.return_value = {
        "fields": {}
    }  # No "id" field

    with pytest.raises(RuntimeError, match="did not return record ID"):
        client.write_assessment(
            screen_id="recScreen123",
            candidate_id="recCandidate456",
            assessment=assessment,
        )


# ============================================================================
# Tests for update_screen_status method
# ============================================================================


def test_update_screen_status_with_status_only(client, mock_tables):
    """Test successful status update without error_message."""
    mock_tables["Platform-Screens"].update.return_value = {
        "id": "recScreen123",
        "fields": {"Status": "Processing"},
    }

    client.update_screen_status(screen_id="recScreen123", status="Processing")

    mock_tables["Platform-Screens"].update.assert_called_once_with(
        "recScreen123", {"Status": "Processing"}
    )


def test_update_screen_status_with_error_message(client, mock_tables):
    """Test status update with error_message parameter (backward compatibility)."""
    mock_tables["Platform-Screens"].update.return_value = {
        "id": "recScreen123",
        "fields": {"Status": "Failed"},
    }

    # error_message parameter is accepted for backward compatibility but not written
    # (Error Message is a read-only lookup field from Operations-Automation_Log)
    client.update_screen_status(
        screen_id="recScreen123", status="Failed", error_message="API timeout"
    )

    # Only Status field is written, error_message is not included in payload
    mock_tables["Platform-Screens"].update.assert_called_once_with(
        "recScreen123", {"Status": "Failed"}
    )


def test_update_screen_status_with_whitespace_trimming(client, mock_tables):
    """Test that screen_id and status are trimmed of whitespace."""
    mock_tables["Platform-Screens"].update.return_value = {
        "id": "recScreen123",
        "fields": {"Status": "Complete"},
    }

    client.update_screen_status(screen_id="  recScreen123  ", status="  Complete  ")

    mock_tables["Platform-Screens"].update.assert_called_once_with(
        "recScreen123", {"Status": "Complete"}
    )


def test_update_screen_status_with_empty_screen_id(client):
    """Test that empty screen_id raises ValueError."""
    with pytest.raises(ValueError, match="screen_id is required"):
        client.update_screen_status(screen_id="", status="Processing")


def test_update_screen_status_with_empty_status(client):
    """Test that empty status raises ValueError."""
    with pytest.raises(ValueError, match="status is required"):
        client.update_screen_status(screen_id="recScreen123", status="")


def test_update_screen_status_with_whitespace_only_screen_id(client):
    """Test that whitespace-only screen_id raises ValueError."""
    with pytest.raises(ValueError, match="screen_id is required"):
        client.update_screen_status(screen_id="   ", status="Processing")


def test_update_screen_status_with_whitespace_only_status(client):
    """Test that whitespace-only status raises ValueError."""
    with pytest.raises(ValueError, match="status is required"):
        client.update_screen_status(screen_id="recScreen123", status="   ")


def test_update_screen_status_with_api_error(client, mock_tables):
    """Test update_screen_status when Airtable API call fails."""
    mock_tables["Platform-Screens"].update.side_effect = RuntimeError(
        "API connection timeout"
    )

    with pytest.raises(RuntimeError, match="Failed to update screen"):
        client.update_screen_status(screen_id="recScreen123", status="Processing")
