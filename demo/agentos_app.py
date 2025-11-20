"""AgentOS-backed FastAPI runtime for the Talent Signal screening workflow."""

from __future__ import annotations

import logging
from typing import Any, Final

from agno.os import AgentOS
from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from demo.airtable_client import AirtableClient
from demo.agents import (
    create_assessment_agent,
    create_incremental_search_agent,
    create_research_agent,
    create_research_parser_agent,
)
from demo.models import ScreenWebhookPayload
from demo.screening_service import (
    LogSymbols,
    ScreenValidationError,
    process_screen_direct,
)
from demo.settings import settings
from demo.workflow import AgentOSCandidateWorkflow

LOG_FORMAT: Final[str] = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"


def _configure_logging() -> logging.Logger:
    """Configure structured logging for the AgentOS FastAPI runtime."""

    level_name = settings.app.log_level.upper()
    level = getattr(logging, level_name, logging.INFO)
    logging.basicConfig(level=level, format=LOG_FORMAT)
    logger = logging.getLogger("talent-signal.agentos")
    logger.setLevel(level)
    return logger


logger = _configure_logging()
# Use centralized LogSymbols from screening_service
SCREEN_LOG_SYMBOLS = LogSymbols()

# Configure bearer auth (optional - only enforced if AGENTOS_SECURITY_KEY is set)
security = HTTPBearer(auto_error=False)


async def verify_bearer_token(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> None:
    """Validate bearer token if AGENTOS_SECURITY_KEY is configured.

    This middleware enforces authentication when the AGENTOS_SECURITY_KEY environment
    variable is set. If the key is not configured, all requests are allowed through
    (authentication disabled).

    Args:
        credentials: Bearer token credentials from Authorization header

    Raises:
        HTTPException: 401 Unauthorized if token is missing or invalid
    """
    if not settings.agentos.security_key:
        # Security not configured - allow all requests
        return

    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if credentials.credentials != settings.agentos.security_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def _init_airtable_client() -> AirtableClient:
    """Instantiate the Airtable client for the AgentOS runtime."""

    api_key = (settings.airtable.api_key or "").strip()
    base_id = (settings.airtable.base_id or "").strip()
    missing: list[str] = []
    if not api_key:
        missing.append("AIRTABLE_API_KEY")
    if not base_id:
        missing.append("AIRTABLE_BASE_ID")

    if missing:
        symbols = LogSymbols()
        message = f"{symbols.error} Missing required environment variables: {', '.join(missing)}"
        logger.critical(message)
        raise RuntimeError(message)

    symbols = LogSymbols()
    logger.info(
        "%s Connecting AgentOS runtime to Airtable base %s", symbols.search, base_id
    )
    return AirtableClient(api_key, base_id)


airtable_client = _init_airtable_client()


# Create workflow runner instance (will be updated with agent_os reference after AgentOS initialization)
candidate_workflow_runner = AgentOSCandidateWorkflow(logger)


def _mark_screen_failed(screen_id: str, error_message: str) -> None:
    """Mark the screen as failed with an error message."""

    try:
        airtable_client.update_screen_status(
            screen_id,
            status="Failed",
            error_message=error_message,
        )
    except Exception:  # pragma: no cover - best effort logging
        symbols = LogSymbols()
        logger.exception(
            "%s Unable to update failure status for screen %s",
            symbols.error,
            screen_id,
        )


def _server_error_response(screen_id: str, exc: Exception) -> JSONResponse:
    """Format a consistent JSON error response for server errors."""

    error_message = str(exc) or exc.__class__.__name__
    symbols = LogSymbols()
    logger.exception(
        "%s Critical failure while processing screen %s",
        symbols.error,
        screen_id,
    )
    _mark_screen_failed(screen_id, error_message)
    return JSONResponse(
        status_code=500,
        content={
            "error": "server_error",
            "message": "Unexpected server error while processing screen.",
            "screen_id": screen_id,
            "details": error_message,
        },
    )


fastapi_app = FastAPI(
    title="Talent Signal AgentOS Runtime",
    description="FastAPI + AgentOS runtime for FirstMark Talent Signal screening",
    version="1.0.0",
)


@fastapi_app.get("/healthz")
def health_check() -> dict[str, str]:
    """Simple health endpoint for smoke tests."""

    return {"status": "ok"}


@fastapi_app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Normalize FastAPI validation errors to match legacy Flask schema."""

    field_errors: dict[str, str] = {}
    for error in exc.errors():
        loc = error.get("loc", [])
        field_name = next(
            (item for item in reversed(loc) if isinstance(item, str)),
            "body",
        )
        field_errors[str(field_name)] = error.get("msg", "Invalid value")

    payload = {
        "error": "validation_error",
        "message": "Invalid request payload.",
        "fields": field_errors or None,
    }
    return JSONResponse(status_code=400, content=payload)


@fastapi_app.post("/screen", response_model=None, status_code=202)
def screen_endpoint(
    payload: ScreenWebhookPayload,
    background_tasks: BackgroundTasks,
    _auth: None = Depends(verify_bearer_token),
) -> dict[str, Any] | JSONResponse:
    """FastAPI implementation of the Airtable webhook entrypoint.

    Processes screening webhook with pre-assembled Airtable data.
    Returns 202 Accepted immediately and processes workflow in background.
    No Airtable traversal is performed - all data comes from the webhook payload.

    Args:
        payload: ScreenWebhookPayload with pre-assembled Airtable data
        background_tasks: FastAPI background task queue
        _auth: Bearer token validation (enforced if AGENTOS_SECURITY_KEY is set)

    Returns:
        202 Accepted with screen_id and candidates_queued count

    Raises:
        HTTPException: 401 Unauthorized if bearer token is invalid or missing (when auth enabled)
    """

    symbols = LogSymbols()
    logger.info(
        "%s Received AgentOS screen webhook for %s",
        symbols.search,
        payload.screen_id,
    )

    try:
        # Extract candidates from structured payload
        candidates = payload.get_candidates()

        # Schedule workflow to run in background
        background_tasks.add_task(
            process_screen_direct,
            screen_id=payload.screen_id,
            role_spec_markdown=payload.spec_markdown,
            candidates=candidates,
            custom_instructions=payload.custom_instructions,
            airtable=airtable_client,
            logger=logger,
            symbols=SCREEN_LOG_SYMBOLS,
            candidate_runner=candidate_workflow_runner.run_candidate_workflow,
        )

        # Return 202 Accepted immediately
        return {
            "status": "accepted",
            "message": "Screen workflow started",
            "screen_id": payload.screen_id,
            "candidates_queued": len(candidates),
        }
    except ValueError as exc:
        # Validation errors from get_candidates() or Pydantic
        symbols = LogSymbols()
        logger.error("%s Invalid webhook payload: %s", symbols.error, exc)
        return JSONResponse(
            status_code=400,
            content={
                "error": "validation_error",
                "message": str(exc),
                "fields": None,
            },
        )
    except ScreenValidationError as exc:
        return JSONResponse(
            status_code=400,
            content={
                "error": "validation_error",
                "message": exc.message,
                "fields": exc.field_errors or None,
            },
        )
    except Exception as exc:  # pragma: no cover - runtime error path
        return _server_error_response(payload.screen_id, exc)


# Register AgentOS runtime with existing workflow + agents.
agent_os = AgentOS(
    id="talent-signal-os",
    description="FirstMark Talent Signal AgentOS runtime",
    agents=[
        create_research_agent(),
        create_research_parser_agent(),
        create_incremental_search_agent(),
        create_assessment_agent(),
    ],
    workflows=[candidate_workflow_runner.workflow],
    base_app=fastapi_app,
)

# Update workflow runner with AgentOS reference for proper session tracking
# This ensures workflows executed through run_candidate_workflow are tracked by AgentOS
# and visible in the AgentOS control plane UI
candidate_workflow_runner.agent_os = agent_os

symbols = LogSymbols()
logger.info(
    "%s AgentOS initialized with workflow %s (id: %s)",
    symbols.success,
    candidate_workflow_runner.workflow.name,
    candidate_workflow_runner.workflow.id,
)

# Log security key status (security is handled via middleware/environment, not constructor)
if settings.agentos.security_key:
    symbols = LogSymbols()
    logger.info(
        "%s AgentOS security key configured (use middleware for bearer token auth)",
        symbols.search,
    )

app = agent_os.get_app()


if __name__ == "__main__":  # pragma: no cover - manual dev server
    agent_os.serve(
        app="demo.agentos_app:app",
        host=settings.server.host,
        port=settings.server.port,
        reload=False,
    )
