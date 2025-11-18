"""Airtable API wrapper for the Talent Signal Agent demo.

This module exposes :class:`AirtableClient`, a thin helper that bootstraps
pyairtable primitives for the Airtable tables used in the screening workflow.
"""

from __future__ import annotations

from typing import Any, Final, Optional

from pyairtable import Api, Table

from demo.models import AssessmentResult, ExecutiveResearchResult

__all__: list[str] = ["AirtableClient"]


class AirtableClient:
    """Typed wrapper around pyairtable for the demo's Airtable schema."""

    SCREENS_TABLE: Final[str] = "Platform-Screens"
    PEOPLE_TABLE: Final[str] = "People"
    ROLE_SPECS_TABLE: Final[str] = "Platform-Role_Specs"
    ASSESSMENTS_TABLE: Final[str] = "Platform-Assessments"
    SEARCHES_TABLE: Final[str] = "Platform-Searches"
    PORTCOS_TABLE: Final[str] = "Portcos"
    PORTCO_ROLES_TABLE: Final[str] = "Platform-Portco_Roles"

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

        # Precompute table handles for the main workflow tables so downstream
        # CRUD methods can reuse them without recreating Table instances.
        self.screens: Table = self.api.table(self.base_id, self.SCREENS_TABLE)
        self.people: Table = self.api.table(self.base_id, self.PEOPLE_TABLE)
        self.role_specs: Table = self.api.table(self.base_id, self.ROLE_SPECS_TABLE)
        self.assessments: Table = self.api.table(self.base_id, self.ASSESSMENTS_TABLE)
        self.searches: Table = self.api.table(self.base_id, self.SEARCHES_TABLE)
        self.portcos: Table = self.api.table(self.base_id, self.PORTCOS_TABLE)
        self.portco_roles: Table = self.api.table(self.base_id, self.PORTCO_ROLES_TABLE)

    def get_screen(self, screen_id: str) -> dict[str, Any]:
        """Return a Screen record plus linked search + candidate details.

        Args:
            screen_id: Airtable record identifier (``recXXXX``).

        Returns:
            Dictionary containing the screen fields, linked search, linked
            candidates, and resolved role spec identifier.
        """

        screen_id = screen_id.strip()
        if not screen_id:
            raise ValueError("screen_id is required")

        try:
            screen_record = self.screens.get(screen_id)
        except Exception as exc:  # pragma: no cover - API client handles errors
            raise RuntimeError(f"Failed to fetch screen {screen_id}") from exc

        fields: dict[str, Any] = screen_record.get("fields", {})

        # Resolve linked search + derive role spec ID from the search record.
        search_record: Optional[dict[str, Any]] = None
        role_spec_id: Optional[str] = None
        search_links = fields.get("Search") or []
        if search_links:
            linked_search_id = search_links[0]
            try:
                raw_search_record = self.searches.get(linked_search_id)
                search_record = dict(raw_search_record)  # Convert RecordDict to dict
            except Exception as exc:  # pragma: no cover - API call failure
                raise RuntimeError(
                    f"Failed to fetch search {linked_search_id} for screen {screen_id}"
                ) from exc

            if search_record is not None:
                search_fields = search_record.get("fields", {})
                role_spec_links = search_fields.get("Role Spec") or []
                if role_spec_links:
                    role_spec_id = role_spec_links[0]

        # Hydrate linked candidate records for downstream processing.
        candidate_records: list[dict[str, Any]] = []
        for candidate_id in fields.get("Candidates", []) or []:
            try:
                raw_candidate = self.people.get(candidate_id)
                candidate_records.append(
                    dict(raw_candidate)
                )  # Convert RecordDict to dict
            except Exception as exc:  # pragma: no cover - API failure path
                raise RuntimeError(
                    f"Failed to fetch candidate {candidate_id} linked to screen {screen_id}"
                ) from exc

        return {
            "id": screen_record.get("id"),
            "fields": fields,
            "search": search_record,
            "role_spec_id": role_spec_id,
            "candidates": candidate_records,
        }

    def get_role_spec(self, spec_id: str) -> dict[str, Any]:
        """Fetch a Role Spec record with markdown content.

        Args:
            spec_id: Airtable Role_Spec record ID.

        Returns:
            Dictionary containing the role spec fields along with a
            ``structured_spec_markdown`` convenience key.
        """

        spec_id = spec_id.strip()
        if not spec_id:
            raise ValueError("spec_id is required")

        try:
            role_spec = self.role_specs.get(spec_id)
        except Exception as exc:  # pragma: no cover - API propagation
            raise RuntimeError(f"Failed to fetch role spec {spec_id}") from exc

        fields: dict[str, Any] = role_spec.get("fields", {})
        markdown = (
            fields.get("structured_spec_markdown")
            or fields.get("Spec Content")
            or fields.get("spec_markdown")
        )

        if markdown is None:
            raise RuntimeError(
                "Role spec record is missing structured_spec_markdown content"
            )

        return {
            "id": role_spec.get("id"),
            "fields": fields,
            "structured_spec_markdown": markdown,
        }

    def write_assessment(
        self,
        screen_id: str,
        candidate_id: str,
        assessment: AssessmentResult,
        research: Optional[ExecutiveResearchResult] = None,
    ) -> str:
        """Persist assessment outputs to the Assessments table.

        Args:
            screen_id: Parent screen record ID.
            candidate_id: Candidate record ID.
            assessment: Structured assessment payload.
            research: Optional structured research payload.

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
            "Overall Score": assessment.overall_score,
            "Overall Confidence": assessment.overall_confidence,
            "Topline Summary": assessment.summary,
            "Assessment Model": assessment.assessment_model,
            "Assessment Timestamp": assessment.assessment_timestamp.date().isoformat(),
        }

        # Note: Role Spec is a linked record field in Airtable, not a markdown storage field
        # The role_spec_used data is stored in the assessment JSON itself
        # Omitting direct field assignment as it would require a record link, not markdown text

        if research is not None:
            fields["Research Structured JSON"] = research.model_dump_json()
            fields["Research Model"] = research.research_model

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

    def update_screen_status(
        self,
        screen_id: str,
        status: str,
        error_message: Optional[str] = None,
    ) -> None:
        """Update the status (and optional error) for a Screen record."""

        screen_id = screen_id.strip()
        status = status.strip()
        if not screen_id:
            raise ValueError("screen_id is required")
        if not status:
            raise ValueError("status is required")

        payload: dict[str, Any] = {"Status": status}
        # Note: error_message field doesn't exist as writable field in Platform-Screens
        # The "Error Message (from Operations-Automation_Log)" is a lookup field (read-only)
        # Errors should be logged to Operations-Automation_Log table instead
        # Keeping parameter for backward compatibility but not writing to Airtable
        if error_message is not None:
            # TODO: Write to Operations-Automation_Log table instead
            pass

        try:
            self.screens.update(screen_id, payload)
        except Exception as exc:  # pragma: no cover - API failure path
            raise RuntimeError(
                f"Failed to update screen {screen_id} status to {status}"
            ) from exc
