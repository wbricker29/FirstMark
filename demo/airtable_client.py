"""Airtable API wrapper for the Talent Signal Agent demo.

This module exposes :class:`AirtableClient`, a minimal helper for write operations only.
All read operations (traversals, lookups) are handled by Airtable formulas and sent
via webhook payload. Python only writes results back to Airtable.
"""

from __future__ import annotations

import json
import logging
from typing import Any, Final, Optional

from pyairtable import Api, Table

from demo.models import AssessmentResult, ExecutiveResearchResult

__all__: list[str] = ["AirtableClient"]

logger = logging.getLogger("demo.airtable_client")
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
    logger.addHandler(handler)
logger.setLevel(logging.INFO)


class AirtableClient:
    """Minimal typed wrapper around pyairtable for write operations only.

    All read operations (traversals, lookups) are handled by Airtable formulas.
    Python only writes results back to Airtable.
    """

    SCREENS_TABLE: Final[str] = "Platform-Screens"
    ASSESSMENTS_TABLE: Final[str] = "Platform-Assessments"
    AUTOMATION_LOG_TABLE: Final[str] = "Operations-Automation_Log"

    def __init__(self, api_key: str, base_id: str) -> None:
        """Instantiate the Airtable client and table handles.

        Args:
            api_key: Airtable personal access token with base permissions.
            base_id: Base identifier (``appXXXX``) optionally containing a
                trailing ``/table`` suffix from Airtable's UI URLs.

        Raises:
            ValueError: If either credential is blank.
        """

        api_key = api_key.strip()
        base_id = base_id.strip()
        if not api_key:
            raise ValueError("Airtable API key is required")
        if not base_id:
            raise ValueError("Airtable base ID is required")

        # Airtable often appends the table ID to the base ID in URLs such as
        # ``appXXXXXXXX/tblYYYYYYYY``; only the base prefix is needed here.
        clean_base_id = base_id.split("/")[0]

        self.api_key: str = api_key
        self.base_id: str = clean_base_id
        self.api: Api = Api(api_key)

        # Only instantiate tables we write to (no read-only tables)
        self.screens: Table = self.api.table(self.base_id, self.SCREENS_TABLE)
        self.assessments: Table = self.api.table(self.base_id, self.ASSESSMENTS_TABLE)
        self.automation_log: Table = self.api.table(
            self.base_id, self.AUTOMATION_LOG_TABLE
        )

    def write_assessment(
        self,
        screen_id: str,
        candidate_id: str,
        assessment: AssessmentResult,
        research: Optional[ExecutiveResearchResult] = None,
        role_spec_markdown: Optional[str] = None,
        assessment_markdown: Optional[str] = None,
    ) -> str:
        """Persist assessment outputs to Platform-Assessments table.

        Writes consolidated JSON blobs plus extracted top-level fields for easy querying.

        **Fields Written:**
        - Screen (link), Candidate (link), Status ("Complete")
        - Assessment JSON: Full AssessmentResult object (includes dimension_scores,
          must_haves_check, red_flags_detected, green_flags, counterfactuals)
        - Overall Score (if not None), Overall Confidence, Topline Summary
        - Assessment Model, Assessment Timestamp
        - Assessment Markdown Report: Inline summary for recruiters (optional)
        - Research JSON: Full ExecutiveResearchResult object (if provided)
        - Research Model (if provided)
        - Research Markdown Report: Raw Deep Research markdown (conditionally, if exists)

        **Note:** Granular JSON fields (Dimension Scores JSON, Red Flags JSON, etc.)
        exist in Airtable schema but are NOT populated - all data stored in consolidated
        Assessment JSON and Research JSON blobs.

        Args:
            screen_id: Parent screen record ID.
            candidate_id: Candidate record ID.
            assessment: Structured assessment payload.
            research: Optional structured research payload.
            role_spec_markdown: Optional Spec markdown used (for audit trail).
            assessment_markdown: Optional inline markdown summary for recruiters.

        Returns:
            Newly-created assessment record ID.
        """

        if not screen_id or not candidate_id:
            raise ValueError("screen_id and candidate_id are required")

        fields: dict[str, Any] = {
            "Screen": [screen_id],
            "Candidate": [candidate_id],
            "Status": "Complete",
            "Assessment JSON": assessment.model_dump_json(),
            "Overall Confidence": assessment.overall_confidence,
            "Topline Summary": assessment.summary,
            "Assessment Model": assessment.assessment_model,
            "Assessment Timestamp": assessment.assessment_timestamp.isoformat(),
        }

        # Only set Overall Score if not None (prevents Airtable API error)
        if assessment.overall_score is not None:
            fields["Overall Score"] = assessment.overall_score

        # Note: Role Spec markdown audit trail is stored in Assessment JSON (assessment.role_spec_used)
        # The role_spec_markdown parameter is used to populate assessment.role_spec_used before JSON serialization
        # No separate Airtable field exists for this data - it's embedded in the Assessment JSON field

        if research is not None:
            fields["Research JSON"] = research.model_dump_json()
            fields["Research Model"] = research.research_model
            # Preserve Deep Research markdown so recruiters can review the raw output
            if research.research_markdown_raw:
                fields["Research Markdown Report"] = research.research_markdown_raw

        if assessment_markdown:
            fields["Assessment Markdown Report"] = assessment_markdown

        try:
            record = self.assessments.create(fields)
        except Exception as exc:  # pragma: no cover - passthrough from API
            raise RuntimeError(
                f"Failed to write assessment for candidate {candidate_id}"
            ) from exc

        record_id = record.get("id")
        if not record_id:
            raise RuntimeError(
                f"Assessment created but Airtable did not return record ID for candidate {candidate_id}"
            )

        return record_id

    def log_automation_event(
        self,
        action: str,
        event_type: str,
        related_table: str,
        related_record_ids: list[str],
        event_summary: str,
        error_message: Optional[str] = None,
        webhook_payload: Optional[dict[str, Any]] = None,
        screen_id: Optional[str] = None,
        assessment_ids: Optional[list[str]] = None,
    ) -> str:
        """Write an automation event to Operations-Automation_Log.

        Args:
            action: Action type (e.g., "Candidate Assessment", "Ingest People File")
            event_type: Event type (e.g., "State Change", "Webhook Event", "System Update")
            related_table: Table name where event occurred
            related_record_ids: List of record IDs affected
            event_summary: Description of the event
            error_message: Optional error details if event failed
            webhook_payload: Optional webhook payload JSON
            screen_id: Optional screen record ID to link
            assessment_ids: Optional list of assessment record IDs to link

        Returns:
            Created log record ID (recXXXX)

        Raises:
            RuntimeError: If log creation fails
        """
        from datetime import datetime, timezone

        payload: dict[str, Any] = {
            "Action": action,
            "Event Type": event_type,
            "Related Table": related_table,
            "Related Record ID(s)": ", ".join(related_record_ids),
            "Event Summary": event_summary,
            "Timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if error_message:
            payload["Error Message"] = error_message

        if webhook_payload:
            payload["Webhook Payload JSON"] = json.dumps(webhook_payload, indent=2)

        if screen_id:
            payload["Platform-Screens"] = [screen_id]

        if assessment_ids:
            payload["Platform-Assessments"] = assessment_ids

        try:
            record = self.automation_log.create(payload)
            logger.info(f"✅ Logged automation event: {record['id']} ({action})")
            return record["id"]
        except Exception as exc:  # pragma: no cover - API failure path
            logger.error(f"❌ Failed to log automation event: {exc}")
            raise RuntimeError(f"Failed to log automation event: {action}") from exc

    def update_screen_status(
        self,
        screen_id: str,
        status: str,
        error_message: Optional[str] = None,
    ) -> None:
        """Update Platform-Screens status field and optionally log errors.

        Args:
            screen_id: Airtable record identifier for the screen.
            status: New status value (e.g., "Processing", "Complete", "Failed").
            error_message: Optional error message. If provided, creates an
                Operations-Automation_Log entry linked to this screen, which
                makes the error visible via the lookup field in the Screens table.
        """

        screen_id = screen_id.strip()
        status = status.strip()
        if not screen_id:
            raise ValueError("screen_id is required")
        if not status:
            raise ValueError("status is required")

        payload: dict[str, Any] = {"Status": status}

        try:
            self.screens.update(screen_id, payload)

            # Log error to Operations-Automation_Log if provided
            if error_message is not None:
                self.log_automation_event(
                    action="Candidate Assessment",
                    event_type="System Update",
                    related_table="Platform-Screens",
                    related_record_ids=[screen_id],
                    event_summary=f"Screen {screen_id} failed: {error_message}",
                    error_message=error_message,
                    screen_id=screen_id,
                )
        except Exception as exc:  # pragma: no cover - API failure path
            raise RuntimeError(
                f"Failed to update screen {screen_id} status to {status}"
            ) from exc
