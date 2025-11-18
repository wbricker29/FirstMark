"""Integration tests for the legacy Flask webhook (/screen) endpoint.

Validates end-to-end Flask behavior including request validation, workflow
orchestration, partial failures, and critical error handling.

Run manually with ``pytest -m legacy tests/test_app.py`` because CI skips
legacy tests by default while AgentOS serves as the canonical runtime.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from flask import Flask
from flask.testing import FlaskClient

from demo.app import create_app
from demo.models import AssessmentResult, DimensionScore


pytestmark = pytest.mark.legacy


@pytest.fixture
def mock_airtable_client() -> MagicMock:
    """Create a mock AirtableClient for testing."""
    client = MagicMock()
    client.get_screen = MagicMock()
    client.get_role_spec = MagicMock()
    client.write_assessment = MagicMock()
    client.update_screen_status = MagicMock()
    return client


@pytest.fixture
def app() -> Flask:
    """Create Flask app for testing."""
    # Import the app module to get the app with registered routes
    from demo import app as app_module

    test_app = app_module.app
    test_app.config["TESTING"] = True
    return test_app


@pytest.fixture
def client(app: Flask, mock_airtable_client: MagicMock):  # type: ignore[misc]
    """Create Flask test client with mocked Airtable client."""
    # Patch _get_airtable_client to return our mock throughout all tests
    with patch("demo.app._get_airtable_client", return_value=mock_airtable_client):
        yield app.test_client()


@pytest.fixture
def sample_candidate() -> dict[str, Any]:
    """Sample candidate record from Airtable."""
    return {
        "id": "recCandidate123",
        "fields": {
            "Full Name": "Jane Executive",
            "Email": "jane@example.com",
            "Title": "VP of Engineering",
        },
    }


@pytest.fixture
def sample_screen_data(sample_candidate: dict[str, Any]) -> dict[str, Any]:
    """Sample screen record with linked candidates and search."""
    return {
        "id": "recScreen123",
        "fields": {
            "status": "Ready to Screen",
            "Search": ["recSearch123"],
            "Candidates": ["recCandidate123"],
        },
        "search": {
            "id": "recSearch123",
            "fields": {"Role Spec": ["recRoleSpec123"]},
        },
        "role_spec_id": "recRoleSpec123",
        "candidates": [sample_candidate],
    }


@pytest.fixture
def sample_role_spec() -> dict[str, Any]:
    """Sample role spec record."""
    return {
        "id": "recRoleSpec123",
        "fields": {
            "Role Title": "CTO",
            "structured_spec_markdown": "# CTO Role Spec\n\nTechnical leadership...",
        },
        "structured_spec_markdown": "# CTO Role Spec\n\nTechnical leadership...",
    }


@pytest.fixture
def sample_assessment() -> AssessmentResult:
    """Sample assessment result."""
    return AssessmentResult(
        overall_score=78.5,
        overall_confidence="High",
        dimension_scores=[
            DimensionScore(
                dimension="Technical Leadership",
                score=4,
                evidence_level="High",
                confidence="High",
                reasoning="Strong background in scaling engineering teams.",
                evidence_quotes=["Led 50+ person engineering org"],
                citation_urls=["https://linkedin.com/in/jane"],
            )
        ],
        must_haves_check=[],
        red_flags_detected=[],
        green_flags=["Strong technical background"],
        summary="Excellent technical leader with proven scaling experience.",
        counterfactuals=["May lack experience in early-stage companies"],
        assessment_timestamp=datetime(2025, 11, 17, 12, 0, 0),
        assessment_model="gpt-5-mini",
        role_spec_used="# CTO Role Spec",
    )


# ============================================================================
# AC-FW-01: Flask Server Startup
# ============================================================================


def test_flask_app_creation_with_valid_client(mock_airtable_client: MagicMock) -> None:
    """Test Flask app initializes successfully with valid client."""
    app = create_app(client=mock_airtable_client)
    assert app is not None
    assert "AIRTABLE_CLIENT" in app.config
    assert app.config["AIRTABLE_CLIENT"] == mock_airtable_client


def test_flask_app_has_screen_endpoint(client: FlaskClient) -> None:
    """Test /screen endpoint is accessible."""
    # Test that endpoint exists (even with empty body, should get 400, not 404)
    response = client.post("/screen")
    assert response.status_code == 400  # Validation error, not 404


# ============================================================================
# AC-FW-02: Request Validation
# ============================================================================


def test_screen_endpoint_missing_json_body(client: FlaskClient) -> None:
    """Test /screen returns 400 when JSON body is missing."""
    response = client.post("/screen", data="not json")
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "validation_error"
    assert "JSON" in data["message"]


def test_screen_endpoint_empty_json_body(client: FlaskClient) -> None:
    """Test /screen returns 400 when JSON body is empty object."""
    response = client.post("/screen", json={})
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "validation_error"
    assert "screen_id" in data["message"]


def test_screen_endpoint_missing_screen_id(client: FlaskClient) -> None:
    """Test /screen returns 400 when screen_id is missing."""
    response = client.post("/screen", json={"other_field": "value"})
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "validation_error"
    assert "screen_id" in data["message"]


def test_screen_endpoint_empty_screen_id(client: FlaskClient) -> None:
    """Test /screen returns 400 when screen_id is empty string."""
    response = client.post("/screen", json={"screen_id": ""})
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "validation_error"


def test_screen_endpoint_whitespace_screen_id(client: FlaskClient) -> None:
    """Test /screen returns 400 when screen_id is only whitespace."""
    response = client.post("/screen", json={"screen_id": "   "})
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "validation_error"


def test_screen_endpoint_invalid_screen_id_format(client: FlaskClient) -> None:
    """Test /screen returns 400 when screen_id doesn't start with 'rec'."""
    response = client.post("/screen", json={"screen_id": "invalid123"})
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "validation_error"
    assert "rec" in data["message"]


def test_screen_endpoint_wrong_type_screen_id(client: FlaskClient) -> None:
    """Test /screen returns 400 when screen_id is not a string."""
    response = client.post("/screen", json={"screen_id": 12345})
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "validation_error"


# ============================================================================
# AC-FW-03: Successful Screening End-to-End
# ============================================================================


def test_successful_screening_single_candidate(
    client: FlaskClient,
    mock_airtable_client: MagicMock,
    sample_screen_data: dict[str, Any],
    sample_role_spec: dict[str, Any],
    sample_assessment: AssessmentResult,
) -> None:
    """Test successful screening workflow with one candidate."""
    # Configure mocks
    mock_airtable_client.get_screen.return_value = sample_screen_data
    mock_airtable_client.get_role_spec.return_value = sample_role_spec
    mock_airtable_client.write_assessment.return_value = "recAssessment123"

    with patch("demo.screening_service.screen_single_candidate") as mock_screen:
        mock_screen.return_value = sample_assessment

        response = client.post("/screen", json={"screen_id": "recScreen123"})

        # Verify response
        assert response.status_code == 200
        data = response.get_json()
        assert data["status"] == "success"
        assert data["screen_id"] == "recScreen123"
        assert data["candidates_processed"] == 1
        assert data["candidates_failed"] == 0
        assert data["candidates_total"] == 1
        assert "execution_time_seconds" in data
        assert len(data["results"]) == 1

        result = data["results"][0]
        assert result["candidate_id"] == "recCandidate123"
        assert result["assessment_id"] == "recAssessment123"
        assert result["overall_score"] == 78.5
        assert result["confidence"] == "High"

        # Verify Airtable interactions
        mock_airtable_client.update_screen_status.assert_any_call(
            "recScreen123", status="Processing"
        )
        mock_airtable_client.update_screen_status.assert_any_call(
            "recScreen123", status="Complete"
        )
        mock_airtable_client.get_screen.assert_called_once_with("recScreen123")
        mock_airtable_client.get_role_spec.assert_called_once_with("recRoleSpec123")
        mock_airtable_client.write_assessment.assert_called_once()


def test_successful_screening_multiple_candidates(
    client: FlaskClient,
    mock_airtable_client: MagicMock,
    sample_screen_data: dict[str, Any],
    sample_role_spec: dict[str, Any],
    sample_assessment: AssessmentResult,
) -> None:
    """Test successful screening with multiple candidates."""
    # Add second candidate
    candidate2 = {
        "id": "recCandidate456",
        "fields": {"Full Name": "John Smith", "Title": "Engineering Manager"},
    }
    screen_data = sample_screen_data.copy()
    screen_data["candidates"] = [screen_data["candidates"][0], candidate2]
    screen_data["fields"]["Candidates"] = ["recCandidate123", "recCandidate456"]

    mock_airtable_client.get_screen.return_value = screen_data
    mock_airtable_client.get_role_spec.return_value = sample_role_spec
    mock_airtable_client.write_assessment.side_effect = [
        "recAssessment123",
        "recAssessment456",
    ]

    with patch("demo.screening_service.screen_single_candidate") as mock_screen:
        mock_screen.return_value = sample_assessment

        response = client.post("/screen", json={"screen_id": "recScreen123"})

        assert response.status_code == 200
        data = response.get_json()
        assert data["status"] == "success"
        assert data["candidates_processed"] == 2
        assert data["candidates_failed"] == 0
        assert len(data["results"]) == 2

        # Verify screen_single_candidate called twice
        assert mock_screen.call_count == 2


# ============================================================================
# AC-FW-04: Partial Failure Handling
# ============================================================================


def test_partial_failure_one_candidate_fails(
    client: FlaskClient,
    mock_airtable_client: MagicMock,
    sample_screen_data: dict[str, Any],
    sample_role_spec: dict[str, Any],
    sample_assessment: AssessmentResult,
) -> None:
    """Test partial success when one candidate fails."""
    # Add second candidate
    candidate2 = {
        "id": "recCandidate456",
        "fields": {"Full Name": "John Smith"},
    }
    screen_data = sample_screen_data.copy()
    screen_data["candidates"] = [screen_data["candidates"][0], candidate2]

    mock_airtable_client.get_screen.return_value = screen_data
    mock_airtable_client.get_role_spec.return_value = sample_role_spec
    mock_airtable_client.write_assessment.return_value = "recAssessment123"

    with patch("demo.screening_service.screen_single_candidate") as mock_screen:
        # First candidate succeeds, second fails
        mock_screen.side_effect = [
            sample_assessment,
            RuntimeError("Research agent failed"),
        ]

        response = client.post("/screen", json={"screen_id": "recScreen123"})

        assert response.status_code == 200
        data = response.get_json()
        assert data["status"] == "partial"
        assert data["candidates_processed"] == 1
        assert data["candidates_failed"] == 1
        assert len(data["results"]) == 1
        assert len(data["errors"]) == 1

        error = data["errors"][0]
        assert error["candidate_id"] == "recCandidate456"
        assert "Research agent failed" in error["error"]

        # Verify status updated to Complete (Platform-Screens schema only has Processing/Complete)
        mock_airtable_client.update_screen_status.assert_any_call(
            "recScreen123", status="Complete"
        )


def test_partial_failure_candidate_missing_id(
    client: FlaskClient,
    mock_airtable_client: MagicMock,
    sample_screen_data: dict[str, Any],
    sample_role_spec: dict[str, Any],
    sample_assessment: AssessmentResult,
) -> None:
    """Test handling of candidate record missing Airtable ID."""
    # Add malformed candidate (no ID)
    bad_candidate = {"fields": {"Full Name": "No ID Candidate"}}
    screen_data = sample_screen_data.copy()
    screen_data["candidates"] = [screen_data["candidates"][0], bad_candidate]

    mock_airtable_client.get_screen.return_value = screen_data
    mock_airtable_client.get_role_spec.return_value = sample_role_spec
    mock_airtable_client.write_assessment.return_value = "recAssessment123"

    with patch("demo.screening_service.screen_single_candidate") as mock_screen:
        mock_screen.return_value = sample_assessment

        response = client.post("/screen", json={"screen_id": "recScreen123"})

        assert response.status_code == 200
        data = response.get_json()
        assert data["status"] == "partial"
        assert data["candidates_processed"] == 1
        assert data["candidates_failed"] == 1

        error = data["errors"][0]
        assert error["candidate_id"] == "unknown"
        assert "missing Airtable ID" in error["error"]


# ============================================================================
# AC-FW-05: Critical Error Handling
# ============================================================================


def test_critical_error_airtable_connection_failure(
    client: FlaskClient,
    mock_airtable_client: MagicMock,
) -> None:
    """Test critical error handling when Airtable API fails."""
    mock_airtable_client.update_screen_status.side_effect = [
        None,  # First call succeeds (Processing status)
        RuntimeError("Airtable API timeout"),  # Second call fails
    ]
    mock_airtable_client.get_screen.side_effect = RuntimeError("Airtable API timeout")

    response = client.post("/screen", json={"screen_id": "recScreen123"})

    assert response.status_code == 500
    data = response.get_json()
    assert data["error"] == "server_error"
    assert data["screen_id"] == "recScreen123"
    assert "details" in data


def test_critical_error_missing_role_spec_link(
    client: FlaskClient,
    mock_airtable_client: MagicMock,
    sample_screen_data: dict[str, Any],
) -> None:
    """Test validation error when screen missing role spec link."""
    screen_data = sample_screen_data.copy()
    screen_data["role_spec_id"] = None

    mock_airtable_client.get_screen.return_value = screen_data

    response = client.post("/screen", json={"screen_id": "recScreen123"})

    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "validation_error"
    assert "role spec" in data["message"].lower()

    # Verify screen status updated to Complete (error_message passed but not actually written)
    # Check that update_screen_status was called with status="Complete"
    calls = mock_airtable_client.update_screen_status.call_args_list
    complete_calls = [c for c in calls if c.kwargs.get("status") == "Complete"]
    assert len(complete_calls) > 0, (
        "Expected update_screen_status to be called with status='Complete'"
    )


def test_critical_error_missing_role_spec_markdown(
    client: FlaskClient,
    mock_airtable_client: MagicMock,
    sample_screen_data: dict[str, Any],
) -> None:
    """Test validation error when role spec missing markdown content."""
    mock_airtable_client.get_screen.return_value = sample_screen_data
    mock_airtable_client.get_role_spec.return_value = {
        "id": "recRoleSpec123",
        "fields": {"Role Title": "CTO"},
        "structured_spec_markdown": None,
    }

    response = client.post("/screen", json={"screen_id": "recScreen123"})

    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "validation_error"
    assert "markdown" in data["message"].lower()

    # Verify screen status updated to Complete (error_message passed but not actually written)
    # Check that update_screen_status was called with status="Complete"
    calls = mock_airtable_client.update_screen_status.call_args_list
    complete_calls = [c for c in calls if c.kwargs.get("status") == "Complete"]
    assert len(complete_calls) > 0, (
        "Expected update_screen_status to be called with status='Complete'"
    )


def test_critical_error_no_candidates_linked(
    client: FlaskClient,
    mock_airtable_client: MagicMock,
    sample_screen_data: dict[str, Any],
    sample_role_spec: dict[str, Any],
) -> None:
    """Test validation error when screen has no candidates."""
    screen_data = sample_screen_data.copy()
    screen_data["candidates"] = []

    mock_airtable_client.get_screen.return_value = screen_data
    mock_airtable_client.get_role_spec.return_value = sample_role_spec

    response = client.post("/screen", json={"screen_id": "recScreen123"})

    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "validation_error"
    assert "no linked candidates" in data["message"].lower()

    # Verify screen status updated to Complete (error_message passed but not actually written)
    # Check that update_screen_status was called with status="Complete"
    calls = mock_airtable_client.update_screen_status.call_args_list
    complete_calls = [c for c in calls if c.kwargs.get("status") == "Complete"]
    assert len(complete_calls) > 0, (
        "Expected update_screen_status to be called with status='Complete'"
    )


def test_critical_error_status_update_on_exception(
    client: FlaskClient,
    mock_airtable_client: MagicMock,
    sample_screen_data: dict[str, Any],
    sample_role_spec: dict[str, Any],
) -> None:
    """Test candidate-level exceptions handled as partial failures."""
    mock_airtable_client.get_screen.return_value = sample_screen_data
    mock_airtable_client.get_role_spec.return_value = sample_role_spec

    with patch("demo.screening_service.screen_single_candidate") as mock_screen:
        # Candidate-level exception is caught and treated as partial failure
        mock_screen.side_effect = Exception("Unexpected error during screening")

        response = client.post("/screen", json={"screen_id": "recScreen123"})

        # Candidate-level errors result in 200 with partial status
        assert response.status_code == 200
        data = response.get_json()
        assert data["status"] == "partial"
        assert data["candidates_failed"] == 1
        assert len(data["errors"]) == 1
        assert "Unexpected error" in data["errors"][0]["error"]

        # Verify screen marked as Complete (Platform-Screens only has Processing/Complete statuses)
        mock_airtable_client.update_screen_status.assert_any_call(
            "recScreen123", status="Complete"
        )


# ============================================================================
# Edge Cases
# ============================================================================


def test_screen_id_trimmed_before_processing(
    client: FlaskClient,
    mock_airtable_client: MagicMock,
    sample_screen_data: dict[str, Any],
    sample_role_spec: dict[str, Any],
    sample_assessment: AssessmentResult,
) -> None:
    """Test screen_id with whitespace is trimmed before processing."""
    mock_airtable_client.get_screen.return_value = sample_screen_data
    mock_airtable_client.get_role_spec.return_value = sample_role_spec
    mock_airtable_client.write_assessment.return_value = "recAssessment123"

    with patch("demo.screening_service.screen_single_candidate") as mock_screen:
        mock_screen.return_value = sample_assessment

        response = client.post("/screen", json={"screen_id": "  recScreen123  "})

        assert response.status_code == 200
        data = response.get_json()
        assert data["screen_id"] == "recScreen123"


def test_response_includes_execution_time(
    client: FlaskClient,
    mock_airtable_client: MagicMock,
    sample_screen_data: dict[str, Any],
    sample_role_spec: dict[str, Any],
    sample_assessment: AssessmentResult,
) -> None:
    """Test response includes execution time metric."""
    mock_airtable_client.get_screen.return_value = sample_screen_data
    mock_airtable_client.get_role_spec.return_value = sample_role_spec
    mock_airtable_client.write_assessment.return_value = "recAssessment123"

    with patch("demo.screening_service.screen_single_candidate") as mock_screen:
        mock_screen.return_value = sample_assessment

        response = client.post("/screen", json={"screen_id": "recScreen123"})

        assert response.status_code == 200
        data = response.get_json()
        assert "execution_time_seconds" in data
        assert isinstance(data["execution_time_seconds"], (int, float))
        assert data["execution_time_seconds"] >= 0


def test_no_errors_key_in_successful_response(
    client: FlaskClient,
    mock_airtable_client: MagicMock,
    sample_screen_data: dict[str, Any],
    sample_role_spec: dict[str, Any],
    sample_assessment: AssessmentResult,
) -> None:
    """Test errors key only present when there are errors."""
    mock_airtable_client.get_screen.return_value = sample_screen_data
    mock_airtable_client.get_role_spec.return_value = sample_role_spec
    mock_airtable_client.write_assessment.return_value = "recAssessment123"

    with patch("demo.screening_service.screen_single_candidate") as mock_screen:
        mock_screen.return_value = sample_assessment

        response = client.post("/screen", json={"screen_id": "recScreen123"})

        assert response.status_code == 200
        data = response.get_json()
        # errors key should only be present when there are errors
        if data["candidates_failed"] == 0:
            assert "errors" not in data or data.get("errors") == []
