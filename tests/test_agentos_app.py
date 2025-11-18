"""Tests for the AgentOS FastAPI runtime (/screen + /healthz)."""

from __future__ import annotations

from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from demo import agentos_app
from demo.screening_service import ScreenValidationError


@pytest.fixture
def client() -> TestClient:
    """FastAPI TestClient for the AgentOS app."""

    with TestClient(agentos_app.app) as test_client:
        yield test_client


def test_agentos_screen_success(client: TestClient) -> None:
    """/screen returns 200 and delegates to process_screen."""

    expected = {
        "status": "success",
        "screen_id": "recScreen123",
        "candidates_total": 1,
        "candidates_processed": 1,
        "candidates_failed": 0,
        "execution_time_seconds": 12.34,
        "results": [
            {
                "candidate_id": "recCandidate123",
                "assessment_id": "recAssessment123",
                "overall_score": 78.5,
                "confidence": "High",
                "summary": "Summary",
            }
        ],
    }

    with patch(
        "demo.agentos_app.process_screen", return_value=expected
    ) as mock_process:
        response = client.post("/screen", json={"screen_id": "recScreen123"})

    assert response.status_code == 200
    assert response.json() == expected
    mock_process.assert_called_once_with(
        "recScreen123",
        agentos_app.airtable_client,
        logger=agentos_app.logger,
        symbols=agentos_app.SCREEN_LOG_SYMBOLS,
    )


def test_agentos_screen_validation_error_from_workflow(client: TestClient) -> None:
    """Workflow validation errors return HTTP 400 with details."""

    with patch(
        "demo.agentos_app.process_screen",
        side_effect=ScreenValidationError(
            "Screen missing linked role spec.",
            {"role_spec_id": "Link a role spec"},
        ),
    ):
        response = client.post("/screen", json={"screen_id": "recScreen123"})

    assert response.status_code == 400
    body = response.json()
    assert body["error"] == "validation_error"
    assert body["fields"]["role_spec_id"] == "Link a role spec"


def test_agentos_screen_pydantic_validation_error(client: TestClient) -> None:
    """Pydantic validation errors should return 400 via the custom handler."""

    response = client.post("/screen", json={"screen_id": "invalid"})

    assert response.status_code == 400
    data = response.json()
    assert data["error"] == "validation_error"
    assert "screen_id" in data.get("fields", {})


def test_agentos_screen_server_error(client: TestClient) -> None:
    """Server-side exceptions return HTTP 500 payload with screen_id."""

    with patch(
        "demo.agentos_app.process_screen",
        side_effect=RuntimeError("boom"),
    ):
        response = client.post("/screen", json={"screen_id": "recScreen123"})

    assert response.status_code == 500
    payload = response.json()
    assert payload["error"] == "server_error"
    assert payload["screen_id"] == "recScreen123"


def test_agentos_health_endpoint(client: TestClient) -> None:
    """Health check returns OK for monitoring."""

    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
