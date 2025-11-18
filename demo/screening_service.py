"""Shared screening workflow runner used by Flask and AgentOS runtimes."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from time import perf_counter
from typing import Any

from demo.agents import screen_single_candidate
from demo.airtable_client import AirtableClient

__all__ = [
    "LogSymbols",
    "ScreenValidationError",
    "process_screen",
]


@dataclass(frozen=True)
class LogSymbols:
    """Emoji-style logging glyphs to keep console output consistent."""

    search: str = "🔍"
    success: str = "✅"
    error: str = "❌"


class ScreenValidationError(Exception):
    """Raised when the Airtable payload is invalid for screening."""

    def __init__(
        self,
        message: str,
        field_errors: dict[str, str] | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.field_errors = field_errors or {}


def process_screen(
    screen_id: str,
    airtable: AirtableClient,
    *,
    logger: logging.Logger,
    symbols: LogSymbols | None = None,
) -> dict[str, Any]:
    """Execute the end-to-end screening workflow for a Screen record.

    Args:
        screen_id: Airtable record ID for the Screen (``recXXXX``).
        airtable: Airtable client configured for the Talent Signal base.
        logger: Logger used for workflow progress output.
        symbols: Optional logging glyphs. Defaults match Flask runtime emoji.

    Returns:
        dict[str, Any]: Summary payload mirroring the Flask `/screen` response.

    Raises:
        ScreenValidationError: When the Screen is missing required linked data.
        RuntimeError: For unexpected downstream failures.
    """

    glyphs = symbols or LogSymbols()

    def _raise_validation_error(
        message: str,
        field_errors: dict[str, str] | None = None,
    ) -> None:
        airtable.update_screen_status(
            screen_id,
            status="Complete",
            error_message=message,
        )
        logger.error("%s %s", glyphs.error, message)
        raise ScreenValidationError(message, field_errors)

    start_ts = perf_counter()
    airtable.update_screen_status(screen_id, status="Processing")

    screen_record = airtable.get_screen(screen_id)
    role_spec_id = screen_record.get("role_spec_id")
    if not role_spec_id:
        _raise_validation_error(
            "Screen is missing a linked role spec.",
            {"role_spec_id": "Link a Role Spec to the Search before screening."},
        )

    role_spec = airtable.get_role_spec(role_spec_id)
    role_spec_markdown = role_spec.get("structured_spec_markdown")
    if not role_spec_markdown:
        _raise_validation_error(
            "Role spec is missing structured markdown content.",
            {
                "structured_spec_markdown": (
                    "Populate the structured_spec_markdown field."
                )
            },
        )

    candidate_records: list[dict[str, Any]] = screen_record.get("candidates") or []
    if not candidate_records:
        _raise_validation_error(
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
                glyphs.error,
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
                glyphs.success,
                candidate_name,
                assessment.overall_score,
            )
        except Exception as exc:  # pragma: no cover - depends on downstream errors
            logger.error(
                "%s Candidate %s failed during screening: %s",
                glyphs.error,
                candidate_name,
                exc,
            )
            errors.append(
                {
                    "candidate_id": candidate_id_str,
                    "error": str(exc),
                }
            )

    airtable.update_screen_status(screen_id, status="Complete")

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
        glyphs.success if not errors else glyphs.error,
        screen_id,
        len(results),
        len(errors),
    )
    return response_payload
