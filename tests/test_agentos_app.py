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
    """/screen returns 202 Accepted and queues processing in background."""

    expected = {
        "status": "accepted",
        "message": "Screen workflow started",
        "screen_id": "recScreen123",
        "candidates_queued": 1,
    }

    payload = {
        "screen_slug": {
            "screen_id": "recScreen123",
            "screen_edited": "2025-11-18T20:01:46.000Z",
            "role_spec_slug": {
                "role_spec": {
                    "role_spec_id": "recRS123",
                    "role_spec_name": "CFO - Series B",
                    "role_spec_content": "# Role Spec\n...",
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
                        "ATID": "recCandidate123",
                        "candidate_name": "Jane Doe",
                        "candidate_current_title": "CFO",
                        "candidate_normalized_title": "",
                        "candidate_current_company": "Acme Inc",
                        "candidate_location": "",
                        "candidate_linkedin": "",
                        "candidate_bio": "",
                    }
                }
            ],
        }
    }

    # Disable auth for this test (default behavior when AGENTOS_SECURITY_KEY not set)
    with patch("demo.agentos_app.settings.agentos.security_key", None):
        # Mock process_screen_direct to avoid background task execution
        with patch("demo.agentos_app.process_screen_direct"):
            response = client.post("/screen", json=payload)

    assert response.status_code == 202
    assert response.json() == expected


@pytest.mark.skip(reason="Endpoint now uses background tasks - errors handled async")
def test_agentos_screen_validation_error_from_workflow(client: TestClient) -> None:
    """Workflow validation errors return HTTP 400 with details."""

    payload = {
        "screen_slug": {
            "screen_id": "recScreen123",
            "role_spec_slug": {
                "role_spec": {
                    "role_spec_id": "recRS123",
                    "role_spec_name": "CFO",
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
            "candidate_slugs": [],
        }
    }

    with patch(
        "demo.agentos_app.process_screen_direct",
        side_effect=ScreenValidationError(
            "Screen missing linked role spec.",
            {"role_spec_id": "Link a role spec"},
        ),
    ):
        response = client.post("/screen", json=payload)

    assert response.status_code == 400
    body = response.json()
    assert body["error"] == "validation_error"
    assert body["fields"]["role_spec_id"] == "Link a role spec"


def test_agentos_screen_pydantic_validation_error(client: TestClient) -> None:
    """Pydantic validation errors should return 400 via the custom handler."""

    # Disable auth for this test
    with patch("demo.agentos_app.settings.agentos.security_key", None):
        response = client.post(
            "/screen", json={"screen_slug": {"screen_id": "invalid"}}
        )

    assert response.status_code == 400
    data = response.json()
    assert data["error"] == "validation_error"
    # Check that validation errors are present (nested fields will be reported)
    assert len(data.get("fields", {})) > 0


@pytest.mark.skip(reason="Endpoint now uses background tasks - errors handled async")
def test_agentos_screen_server_error(client: TestClient) -> None:
    """Server-side exceptions return HTTP 500 payload with screen_id."""

    payload = {
        "screen_slug": {
            "screen_id": "recScreen123",
            "role_spec_slug": {
                "role_spec": {
                    "role_spec_id": "recRS123",
                    "role_spec_name": "CFO",
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
            "candidate_slugs": [],
        }
    }

    with patch(
        "demo.agentos_app.process_screen_direct",
        side_effect=RuntimeError("boom"),
    ):
        response = client.post("/screen", json=payload)

    assert response.status_code == 500
    response_payload = response.json()
    assert response_payload["error"] == "server_error"
    assert response_payload["screen_id"] == "recScreen123"


def test_agentos_health_endpoint(client: TestClient) -> None:
    """Health check returns OK for monitoring."""

    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# Bearer Auth Tests


def test_bearer_auth_disabled_allows_all_requests(client: TestClient) -> None:
    """When AGENTOS_SECURITY_KEY is not set, requests without auth should succeed."""

    # Valid payload
    payload = {
        "screen_slug": {
            "screen_id": "recScreen123",
            "screen_edited": "2025-11-18T20:01:46.000Z",
            "role_spec_slug": {
                "role_spec": {
                    "role_spec_id": "recRS123",
                    "role_spec_name": "CFO",
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
                        "ATID": "recC123",
                        "candidate_name": "Jane Doe",
                        "candidate_current_title": "CFO",
                        "candidate_normalized_title": "",
                        "candidate_current_company": "Acme",
                        "candidate_location": "",
                        "candidate_linkedin": "",
                        "candidate_bio": "",
                    }
                }
            ],
        }
    }

    # Patch settings to disable security
    with patch("demo.agentos_app.settings.agentos.security_key", None):
        # Mock process_screen_direct to avoid background execution
        with patch("demo.agentos_app.process_screen_direct"):
            # Request without Authorization header should succeed
            response = client.post("/screen", json=payload)

    assert response.status_code == 202
    assert response.json()["status"] == "accepted"


def test_bearer_auth_enabled_rejects_missing_token(client: TestClient) -> None:
    """When AGENTOS_SECURITY_KEY is set, requests without auth should return 401."""

    payload = {
        "screen_slug": {
            "screen_id": "recScreen123",
            "screen_edited": "2025-11-18T20:01:46.000Z",
            "role_spec_slug": {
                "role_spec": {
                    "role_spec_id": "recRS123",
                    "role_spec_name": "CFO",
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
                        "ATID": "recC123",
                        "candidate_name": "Jane Doe",
                        "candidate_current_title": "CFO",
                        "candidate_normalized_title": "",
                        "candidate_current_company": "Acme",
                        "candidate_location": "",
                        "candidate_linkedin": "",
                        "candidate_bio": "",
                    }
                }
            ],
        }
    }

    # Patch settings to enable security
    with patch("demo.agentos_app.settings.agentos.security_key", "test-secret-key"):
        # Request without Authorization header should fail
        response = client.post("/screen", json=payload)

    assert response.status_code == 401
    assert response.json()["detail"] == "Missing authorization header"


def test_bearer_auth_enabled_rejects_invalid_token(client: TestClient) -> None:
    """When AGENTOS_SECURITY_KEY is set, requests with invalid token should return 401."""

    payload = {
        "screen_slug": {
            "screen_id": "recScreen123",
            "screen_edited": "2025-11-18T20:01:46.000Z",
            "role_spec_slug": {
                "role_spec": {
                    "role_spec_id": "recRS123",
                    "role_spec_name": "CFO",
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
                        "ATID": "recC123",
                        "candidate_name": "Jane Doe",
                        "candidate_current_title": "CFO",
                        "candidate_normalized_title": "",
                        "candidate_current_company": "Acme",
                        "candidate_location": "",
                        "candidate_linkedin": "",
                        "candidate_bio": "",
                    }
                }
            ],
        }
    }

    # Patch settings to enable security
    with patch("demo.agentos_app.settings.agentos.security_key", "test-secret-key"):
        # Request with wrong token should fail
        response = client.post(
            "/screen",
            json=payload,
            headers={"Authorization": "Bearer wrong-token"},
        )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid authentication credentials"


def test_bearer_auth_enabled_accepts_valid_token(client: TestClient) -> None:
    """When AGENTOS_SECURITY_KEY is set, requests with valid token should succeed."""

    payload = {
        "screen_slug": {
            "screen_id": "recScreen123",
            "screen_edited": "2025-11-18T20:01:46.000Z",
            "role_spec_slug": {
                "role_spec": {
                    "role_spec_id": "recRS123",
                    "role_spec_name": "CFO",
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
                        "ATID": "recC123",
                        "candidate_name": "Jane Doe",
                        "candidate_current_title": "CFO",
                        "candidate_normalized_title": "",
                        "candidate_current_company": "Acme",
                        "candidate_location": "",
                        "candidate_linkedin": "",
                        "candidate_bio": "",
                    }
                }
            ],
        }
    }

    # Patch settings to enable security
    with patch("demo.agentos_app.settings.agentos.security_key", "test-secret-key"):
        # Mock process_screen_direct to avoid background execution
        with patch("demo.agentos_app.process_screen_direct"):
            # Request with correct token should succeed
            response = client.post(
                "/screen",
                json=payload,
                headers={"Authorization": "Bearer test-secret-key"},
            )

    assert response.status_code == 202
    assert response.json()["status"] == "accepted"
