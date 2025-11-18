"""Legacy Flask webhook server retained for backwards compatibility.

AgentOS (`demo/agentos_app.py`) is the canonical `/screen` runtime. This
module remains for historical demos/tests and will be removed after the
AgentOS cutover is fully validated.
"""

from __future__ import annotations

import logging
from typing import Final

from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException

from demo.agents import screen_single_candidate as _screen_single_candidate
from demo.airtable_client import AirtableClient
from demo.screening_service import (
    LogSymbols,
    ScreenValidationError,
    process_screen,
)
from demo.settings import settings

__all__ = ["app", "create_app", "airtable_client", "screen_single_candidate"]

LOG_SEARCH: Final[str] = "🔍"
LOG_SUCCESS: Final[str] = "✅"
LOG_ERROR: Final[str] = "❌"
LOG_WARNING: Final[str] = "⚠️"
LOG_FORMAT: Final[str] = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"


def _configure_logging() -> logging.Logger:
    """Configure application-wide logging."""

    level_name = settings.app.log_level.upper()
    level = getattr(logging, level_name, logging.INFO)
    logging.basicConfig(level=level, format=LOG_FORMAT)
    logger = logging.getLogger("talent-signal.flask")
    logger.setLevel(level)
    return logger


logger = _configure_logging()
logger.warning(
    "%s Legacy Flask server loaded; use uv run python demo/agentos_app.py for canonical AgentOS runtime",
    LOG_WARNING,
)
SCREEN_LOG_SYMBOLS = LogSymbols(
    search=LOG_SEARCH,
    success=LOG_SUCCESS,
    error=LOG_ERROR,
)
screen_single_candidate = _screen_single_candidate


def _init_airtable_client() -> AirtableClient:
    """Instantiate the Airtable client with validation."""

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

    logger.info("%s Connecting to Airtable base %s", LOG_SEARCH, base_id)
    return AirtableClient(api_key, base_id)


def create_app(client: AirtableClient | None = None) -> Flask:
    """Application factory for the Talent Signal Agent Flask server."""

    app = Flask(__name__)
    app.config["JSON_SORT_KEYS"] = False

    try:
        airtable = client or _init_airtable_client()
    except Exception:
        logger.exception("%s Unable to initialize Airtable client", LOG_ERROR)
        raise

    app.config["AIRTABLE_CLIENT"] = airtable
    logger.info(
        "%s Flask app initialized (host=%s port=%s)",
        LOG_SUCCESS,
        settings.flask.host,
        settings.flask.port,
    )
    return app


airtable_client = _init_airtable_client()
app = create_app(airtable_client)


def _get_airtable_client() -> AirtableClient:
    """Return the configured Airtable client instance."""

    client = app.config.get("AIRTABLE_CLIENT")
    if not isinstance(client, AirtableClient):  # pragma: no cover - sanity guard
        raise RuntimeError("Airtable client is not configured on the Flask app")
    return client


def _validation_error(message: str, field_errors: dict[str, str] | None = None):
    """Return a standardized validation error response."""

    payload: dict[str, object] = {
        "error": "validation_error",
        "message": message,
    }
    if field_errors:
        payload["fields"] = field_errors
    return jsonify(payload), 400


def _server_error(
    message: str,
    *,
    screen_id: str | None = None,
    details: str | None = None,
):
    """Return a standardized server error response."""

    payload: dict[str, object] = {
        "error": "server_error",
        "message": message,
    }
    if screen_id:
        payload["screen_id"] = screen_id
    if details:
        payload["details"] = details
    return jsonify(payload), 500


def _mark_screen_failed(
    airtable: AirtableClient, screen_id: str, error_message: str
) -> None:
    """Best-effort update of Screen status to Failed during critical errors."""

    try:
        # Note: "Failed" is not a valid status in Platform-Screens schema
        # Valid values: "Processing", "Complete"
        # Using "Complete" to mark final state; errors logged separately
        airtable.update_screen_status(
            screen_id,
            status="Complete",
            error_message=error_message,
        )
    except Exception:  # pragma: no cover - defensive logging path
        logger.exception(
            "%s Unable to update failure status for screen %s",
            LOG_ERROR,
            screen_id,
        )


def _handle_screen_exception(
    *, airtable: AirtableClient, screen_id: str, exc: Exception
):
    """Log and format a critical error response for /screen failures."""

    error_message = str(exc) or exc.__class__.__name__
    logger.exception(
        "%s Critical failure while processing screen %s",
        LOG_ERROR,
        screen_id,
    )
    _mark_screen_failed(airtable, screen_id, error_message)
    return _server_error(
        "Unexpected server error while processing screen.",
        screen_id=screen_id,
        details=error_message,
    )


@app.post("/screen")
def screen_webhook():
    """Validate webhook requests before kicking off the screening workflow."""

    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        logger.warning("%s /screen called without JSON body", LOG_ERROR)
        return _validation_error(
            "Request body must be a JSON object.",
            {"body": "Expected JSON payload with screen_id."},
        )

    screen_id = payload.get("screen_id")
    if not isinstance(screen_id, str) or not screen_id.strip():
        logger.warning("%s Missing or empty screen_id in request body", LOG_ERROR)
        return _validation_error(
            "screen_id is required and must be a non-empty string.",
            {"screen_id": "Provide Airtable record ID (recXXXX)."},
        )

    screen_id = screen_id.strip()
    if not screen_id.startswith("rec"):
        logger.warning("%s Invalid screen_id format provided: %s", LOG_ERROR, screen_id)
        return _validation_error(
            "screen_id must be a valid Airtable record identifier (recXXXX).",
            {"screen_id": "Value must start with 'rec'."},
        )

    logger.info("%s Received screen webhook for %s", LOG_SEARCH, screen_id)

    airtable = _get_airtable_client()

    try:
        result = process_screen(
            screen_id,
            airtable,
            logger=logger,
            symbols=SCREEN_LOG_SYMBOLS,
        )
        return jsonify(result), 200
    except ScreenValidationError as exc:
        return _validation_error(exc.message, exc.field_errors)
    except HTTPException:
        raise
    except Exception as exc:  # pragma: no cover - ensures robust API errors
        return _handle_screen_exception(
            airtable=airtable,
            screen_id=screen_id,
            exc=exc,
        )


if __name__ == "__main__":
    logger.info(
        "%s Starting Flask development server on %s:%s",
        LOG_SEARCH,
        settings.flask.host,
        settings.flask.port,
    )
    app.run(
        host=settings.flask.host,
        port=settings.flask.port,
        debug=settings.flask.debug,
    )
