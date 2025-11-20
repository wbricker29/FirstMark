"""Shared screening workflow runner for the AgentOS runtime."""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from time import perf_counter
from typing import Any, Callable, Optional

from demo.airtable_client import AirtableClient
from demo.models import AssessmentResult, CandidateDict, ExecutiveResearchResult
from demo.screening_helpers import (
    render_assessment_markdown_inline,
    validate_candidates,
)

__all__ = [
    "LogSymbols",
    "ScreenValidationError",
    "process_screen_direct",
]

CandidateRunner = Callable[
    [CandidateDict, str, str, Optional[str]],
    tuple[AssessmentResult, Optional[ExecutiveResearchResult]],
]


@dataclass(frozen=True)
class LogSymbols:
    """Emoji-style logging glyphs to keep console output consistent."""

    search: str = "🔍"
    success: str = "✅"
    error: str = "❌"


class ScreenValidationError(Exception):
    """Raised when the Airtable payload is invalid for screening.

    Use this exception for validation errors that should return 400 status codes.
    """

    def __init__(
        self,
        message: str,
        field_errors: dict[str, str] | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.field_errors = field_errors or {}


def _update_screen_status_and_log_webhook(
    screen_id: str,
    airtable: AirtableClient,
    logger: logging.Logger,
    symbols: LogSymbols,
) -> None:
    """Update screen status to Processing and log webhook trigger event.

    Args:
        screen_id: Airtable record ID for the Screen.
        airtable: Airtable client for status updates and logging.
        logger: Logger for workflow progress.
        symbols: Logging glyphs for consistent output.
    """
    airtable.update_screen_status(screen_id, status="Processing")

    try:
        airtable.log_automation_event(
            action="Candidate Assessment",
            event_type="Webhook Event",
            related_table="Platform-Screens",
            related_record_ids=[screen_id],
            event_summary=f"Webhook triggered for screen {screen_id}",
            screen_id=screen_id,
        )
    except Exception as exc:
        # Don't fail the workflow if logging fails, just warn
        logger.warning(f"⚠️  Failed to log webhook event: {exc}")


def _process_candidate_batch(
    candidates: list[CandidateDict],
    role_spec_markdown: str,
    screen_id: str,
    airtable: AirtableClient,
    candidate_runner: CandidateRunner,
    logger: logging.Logger,
    symbols: LogSymbols,
    custom_instructions: Optional[str] = None,
) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    """Process a batch of candidates through the screening workflow.

    Args:
        candidates: List of candidate dicts with keys: id, name, title, company, etc.
        role_spec_markdown: Complete role specification markdown.
        screen_id: Airtable record ID for the Screen.
        airtable: Airtable client for writing assessments.
        candidate_runner: Function to run candidate workflow.
        logger: Logger for workflow progress.
        symbols: Logging glyphs for consistent output.
        custom_instructions: Optional recruiter-provided overrides.

    Returns:
        Tuple of (results list, errors list). Results contain assessment metadata,
        errors contain candidate_id and error message.
    """
    results: list[dict[str, Any]] = []
    errors: list[dict[str, str]] = []

    for candidate in candidates:
        candidate_id = candidate.get("id")
        candidate_name = candidate.get("name", candidate_id or "Unknown")

        if not candidate_id:
            logger.error(
                "%s Candidate record missing ID; skipping record.",
                symbols.error,
            )
            errors.append(
                {
                    "candidate_id": "unknown",
                    "error": "Candidate record missing ID.",
                }
            )
            continue

        candidate_id_str = str(candidate_id)

        logger.debug(
            "📦 PROCESSING CANDIDATE (ID: %s, Name: %s):\n%s",
            candidate_id_str,
            candidate_name,
            json.dumps(candidate, indent=2, default=str),
        )

        try:
            assessment, research = candidate_runner(
                candidate,
                role_spec_markdown,
                screen_id,
                custom_instructions,
            )
            inline_markdown = render_assessment_markdown_inline(
                candidate, assessment, research
            )
            assessment_record_id = airtable.write_assessment(
                screen_id=screen_id,
                candidate_id=candidate_id_str,
                assessment=assessment,
                research=research,
                role_spec_markdown=role_spec_markdown,
                assessment_markdown=inline_markdown,
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
                symbols.success,
                candidate_name,
                assessment.overall_score,
            )
        except Exception as exc:
            # Catch all exceptions to continue processing remaining candidates
            logger.error(
                "%s Candidate %s failed during screening: %s",
                symbols.error,
                candidate_name,
                exc,
            )
            errors.append(
                {
                    "candidate_id": candidate_id_str,
                    "error": str(exc),
                }
            )
        finally:
            for report_path in report_paths:
                if report_path.exists():
                    try:
                        report_path.unlink()
                    except OSError:
                        logger.debug(
                            "Unable to delete temporary report file %s",
                            report_path,
                        )

    return results, errors


def _log_completion_event(
    screen_id: str,
    results: list[dict[str, Any]],
    errors: list[dict[str, str]],
    duration: float,
    airtable: AirtableClient,
    logger: logging.Logger,
) -> None:
    """Log completion event to Airtable automation log.

    Args:
        screen_id: Airtable record ID for the Screen.
        results: List of successful assessment results.
        errors: List of error dicts.
        duration: Execution time in seconds.
        airtable: Airtable client for logging.
        logger: Logger for warnings if logging fails.
    """
    try:
        assessment_ids = [r["assessment_id"] for r in results if "assessment_id" in r]
        airtable.log_automation_event(
            action="Candidate Assessment",
            event_type="State Change",
            related_table="Platform-Screens",
            related_record_ids=[screen_id],
            event_summary=(
                f"Screen {screen_id} completed: {len(results)} successful, "
                f"{len(errors)} failed, {duration:.1f}s elapsed"
            ),
            screen_id=screen_id,
            assessment_ids=assessment_ids if assessment_ids else None,
        )
    except Exception as exc:
        # Don't fail the workflow if logging fails, just warn
        logger.warning(f"⚠️  Failed to log completion event: {exc}")


def _format_response_payload(
    screen_id: str,
    candidates_total: int,
    results: list[dict[str, Any]],
    errors: list[dict[str, str]],
    duration: float,
) -> dict[str, Any]:
    """Format response payload for webhook endpoint.

    Args:
        screen_id: Airtable record ID for the Screen.
        candidates_total: Total number of candidates processed.
        results: List of successful assessment results.
        errors: List of error dicts.
        duration: Execution time in seconds.

    Returns:
        Formatted response dict with status, counts, results, and optional errors.
    """
    payload: dict[str, Any] = {
        "status": "success" if not errors else "partial",
        "screen_id": screen_id,
        "candidates_total": candidates_total,
        "candidates_processed": len(results),
        "candidates_failed": len(errors),
        "execution_time_seconds": round(duration, 2),
        "results": results,
    }
    if errors:
        payload["errors"] = errors
    return payload


def process_screen_direct(
    screen_id: str,
    role_spec_markdown: str,
    candidates: list[CandidateDict],
    custom_instructions: Optional[str],
    airtable: AirtableClient,
    *,
    logger: logging.Logger,
    symbols: LogSymbols | None = None,
    candidate_runner: CandidateRunner,
) -> dict[str, Any]:
    """Execute screening workflow with pre-parsed candidate data.

    This is the simplified version that accepts pre-assembled data from webhook payload.
    No Airtable traversal is performed - all data comes from the webhook.

    Args:
        screen_id: Airtable record ID for the Screen.
        role_spec_markdown: Complete role specification markdown.
        candidates: List of candidate dicts from webhook payload (parsed from delimiters).
        custom_instructions: Optional screen-specific guidance.
        airtable: Airtable client for writing results.
        logger: Logger for workflow progress.
        symbols: Optional logging glyphs.
        candidate_runner: Function to run candidate workflow.

    Returns:
        Summary payload with results for all candidates.
    """
    glyphs = symbols or LogSymbols()
    start_ts = perf_counter()

    # Update status and log webhook trigger
    _update_screen_status_and_log_webhook(screen_id, airtable, logger, glyphs)

    # Validate candidates
    try:
        validate_candidates(candidates)
    except ValueError as exc:
        airtable.update_screen_status(
            screen_id,
            status="Failed",
            error_message=str(exc),
        )
        raise ScreenValidationError(
            str(exc),
            {"candidates": str(exc)},
        ) from exc

    # Process all candidates
    results, errors = _process_candidate_batch(
        candidates=candidates,
        role_spec_markdown=role_spec_markdown,
        screen_id=screen_id,
        airtable=airtable,
        candidate_runner=candidate_runner,
        logger=logger,
        symbols=glyphs,
        custom_instructions=custom_instructions,
    )

    # Update final status
    airtable.update_screen_status(screen_id, status="Complete")

    duration = perf_counter() - start_ts

    # Log completion event
    _log_completion_event(screen_id, results, errors, duration, airtable, logger)

    # Format and return response
    response_payload = _format_response_payload(
        screen_id, len(candidates), results, errors, duration
    )

    logger.info(
        "%s Screen %s completed (%s successes, %s failures)",
        glyphs.success if not errors else glyphs.error,
        screen_id,
        len(results),
        len(errors),
    )
    return response_payload
