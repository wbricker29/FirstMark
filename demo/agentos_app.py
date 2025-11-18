"""AgentOS-backed FastAPI runtime for the Talent Signal screening workflow."""

from __future__ import annotations

import logging
from typing import Any, Final

from agno.os import AgentOS
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator

from demo.airtable_client import AirtableClient
from demo.agents import (
    create_assessment_agent,
    create_incremental_search_agent,
    create_research_agent,
    create_research_parser_agent,
    create_screening_workflow,
)
from demo.screening_service import LogSymbols, ScreenValidationError, process_screen
from demo.settings import settings

LOG_SEARCH: Final[str] = "🔍"
LOG_SUCCESS: Final[str] = "✅"
LOG_ERROR: Final[str] = "❌"
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
SCREEN_LOG_SYMBOLS = LogSymbols(
    search=LOG_SEARCH,
    success=LOG_SUCCESS,
    error=LOG_ERROR,
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
        message = (
            f"{LOG_ERROR} Missing required environment variables: {', '.join(missing)}"
        )
        logger.critical(message)
        raise RuntimeError(message)

    logger.info(
        "%s Connecting AgentOS runtime to Airtable base %s", LOG_SEARCH, base_id
    )
    return AirtableClient(api_key, base_id)


airtable_client = _init_airtable_client()


class ScreenRequest(BaseModel):
    """Pydantic model for the /screen webhook payload."""

    screen_id: str = Field(..., description="Airtable record ID (recXXXX)")

    @field_validator("screen_id")
    @classmethod
    def _validate_screen_id(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("screen_id is required.")
        if not cleaned.startswith("rec"):
            raise ValueError(
                "screen_id must be a valid Airtable record identifier (recXXXX)."
            )
        return cleaned


def _mark_screen_failed(screen_id: str, error_message: str) -> None:
    """Mark the screen as complete with an error message."""

    try:
        airtable_client.update_screen_status(
            screen_id,
            status="Complete",
            error_message=error_message,
        )
    except Exception:  # pragma: no cover - best effort logging
        logger.exception(
            "%s Unable to update failure status for screen %s",
            LOG_ERROR,
            screen_id,
        )


def _server_error_response(screen_id: str, exc: Exception) -> JSONResponse:
    """Format a consistent JSON error response for server errors."""

    error_message = str(exc) or exc.__class__.__name__
    logger.exception(
        "%s Critical failure while processing screen %s",
        LOG_ERROR,
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


@fastapi_app.post("/screen")
def screen_endpoint(payload: ScreenRequest) -> dict[str, Any]:
    """FastAPI implementation of the Airtable webhook entrypoint."""

    logger.info(
        "%s Received AgentOS screen webhook for %s", LOG_SEARCH, payload.screen_id
    )

    try:
        return process_screen(
            payload.screen_id,
            airtable_client,
            logger=logger,
            symbols=SCREEN_LOG_SYMBOLS,
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
    workflows=[create_screening_workflow()],
    base_app=fastapi_app,
)

app = agent_os.get_app()


if __name__ == "__main__":  # pragma: no cover - manual dev server
    agent_os.serve(
        app="demo.agentos_app:app",
        host=settings.flask.host,
        port=settings.flask.port,
        reload=False,
    )
