"""Flask webhook server for Airtable automation triggers.

Bootstraps the Flask app, configures logging, and exposes HTTP entrypoints
for Airtable automation callbacks.
"""

from __future__ import annotations

import logging
from time import perf_counter
from typing import Any, Final

from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException

from demo.agents import screen_single_candidate
from demo.airtable_client import AirtableClient
from demo.settings import settings

__all__ = ["app", "create_app", "airtable_client"]

LOG_SEARCH: Final[str] = "🔍"
LOG_SUCCESS: Final[str] = "✅"
LOG_ERROR: Final[str] = "❌"
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
        airtable.update_screen_status(
            screen_id,
            status="Failed",
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
    start_ts = perf_counter()

    try:
        airtable.update_screen_status(screen_id, status="Processing")

        screen_record = airtable.get_screen(screen_id)
        role_spec_id = screen_record.get("role_spec_id")
        if not role_spec_id:
            logger.error("%s Screen %s missing linked role spec", LOG_ERROR, screen_id)
            airtable.update_screen_status(
                screen_id,
                status="Failed",
                error_message="Screen missing linked role spec.",
            )
            return _validation_error(
                "Screen is missing a linked role spec.",
                {"role_spec_id": "Link a Role Spec to the Search before screening."},
            )

        role_spec = airtable.get_role_spec(role_spec_id)
        role_spec_markdown = role_spec.get("structured_spec_markdown")
        if not role_spec_markdown:
            logger.error(
                "%s Role spec %s missing markdown content", LOG_ERROR, role_spec_id
            )
            airtable.update_screen_status(
                screen_id,
                status="Failed",
                error_message="Role spec missing structured markdown content.",
            )
            return _validation_error(
                "Role spec is missing structured markdown content.",
                {
                    "structured_spec_markdown": "Populate the structured_spec_markdown field."
                },
            )

        candidate_records: list[dict[str, Any]] = screen_record.get("candidates") or []
        if not candidate_records:
            logger.warning(
                "%s Screen %s has no linked candidates", LOG_ERROR, screen_id
            )
            airtable.update_screen_status(
                screen_id,
                status="Failed",
                error_message="No candidates linked to screen.",
            )
            return _validation_error(
                "Screen has no linked candidates to process.",
                {"candidates": "Attach at least one candidate to the screen."},
            )

        results: list[dict[str, Any]] = []
        errors: list[dict[str, str]] = []

        for candidate in candidate_records:
            candidate_id = (
                candidate.get("id")
                or candidate.get("record_id")
                or candidate.get("fields", {}).get("id")
            )
            if candidate_id is None:
                logger.error(
                    "%s Candidate record missing Airtable ID; skipping record.",
                    LOG_ERROR,
                )
                errors.append(
                    {
                        "candidate_id": "unknown",
                        "error": "Candidate record missing Airtable ID.",
                    }
                )
                continue

            candidate_id_str = str(candidate_id)
            candidate_name = (
                candidate.get("fields", {}).get("Full Name")
                or candidate.get("fields", {}).get("Name")
                or candidate_id_str
            )

            try:
                assessment = screen_single_candidate(
                    candidate_data=candidate,
                    role_spec_markdown=str(role_spec_markdown),
                    screen_id=screen_id,
                )
                assessment_record_id = airtable.write_assessment(
                    screen_id=screen_id,
                    candidate_id=candidate_id_str,
                    assessment=assessment,
                )
                results.append(
                    {
                        "candidate_id": candidate_id_str,
                        "assessment_id": assessment_record_id,
                        "overall_score": assessment.overall_score,
                        "confidence": assessment.overall_confidence,
                        "summary": assessment.summary,
                        "assessed_at": assessment.assessment_timestamp.isoformat(),
                    }
                )
                logger.info(
                    "%s Candidate %s screened successfully (score=%s)",
                    LOG_SUCCESS,
                    candidate_name,
                    assessment.overall_score,
                )
            except Exception as exc:  # pragma: no cover - depends on downstream errors
                logger.error(
                    "%s Candidate %s failed during screening: %s",
                    LOG_ERROR,
                    candidate_name,
                    exc,
                )
                errors.append(
                    {
                        "candidate_id": candidate_id_str,
                        "error": str(exc),
                    }
                )

        final_status = "Complete" if not errors else "Partial"
        airtable.update_screen_status(screen_id, status=final_status)

        duration = perf_counter() - start_ts
        response_payload: dict[str, Any] = {
            "status": "success" if not errors else "partial",
            "screen_id": screen_id,
            "candidates_total": len(candidate_records),
            "candidates_processed": len(results),
            "candidates_failed": len(errors),
            "execution_time_seconds": round(duration, 2),
            "results": results,
        }
        if errors:
            response_payload["errors"] = errors

        logger.info(
            "%s Screen %s completed (%s successes, %s failures)",
            LOG_SUCCESS if not errors else LOG_ERROR,
            screen_id,
            len(results),
            len(errors),
        )
        return jsonify(response_payload), 200
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
