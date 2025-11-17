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

    SCREENS_TABLE: Final[str] = "Screens"
    PEOPLE_TABLE: Final[str] = "People"
    ROLE_SPECS_TABLE: Final[str] = "Role_Specs"
    ASSESSMENTS_TABLE: Final[str] = "Assessments"
    SEARCHES_TABLE: Final[str] = "Searches"

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
                search_record = self.searches.get(linked_search_id)
            except Exception as exc:  # pragma: no cover - API call failure
                raise RuntimeError(
                    f"Failed to fetch search {linked_search_id} for screen {screen_id}"
                ) from exc

            search_fields = search_record.get("fields", {})
            role_spec_links = search_fields.get("Role Spec") or []
            if role_spec_links:
                role_spec_id = role_spec_links[0]

        # Hydrate linked candidate records for downstream processing.
        candidate_records: list[dict[str, Any]] = []
        for candidate_id in fields.get("Candidates", []) or []:
            try:
                candidate_records.append(self.people.get(candidate_id))
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
            "screen": [screen_id],
            "candidate": [candidate_id],
            "status": "Complete",
            "assessment_json": assessment.model_dump_json(),
            "overall_score": assessment.overall_score,
            "overall_confidence": assessment.overall_confidence,
            "topline_summary": assessment.summary,
            "assessment_model": assessment.assessment_model,
            "assessment_timestamp": assessment.assessment_timestamp.isoformat(),
        }

        if assessment.role_spec_used:
            fields["role_spec_markdown"] = assessment.role_spec_used

        if research is not None:
            fields["research_structured_json"] = research.model_dump_json()
            fields["research_model"] = research.research_model

        try:
            record = self.assessments.create(fields)
        except Exception as exc:  # pragma: no cover - passthrough from API
            raise RuntimeError(
                f"Failed to write assessment for candidate {candidate_id}"
            ) from exc

        return record.get("id")

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

        payload: dict[str, Any] = {"status": status}
        if error_message is not None:
            payload["error_message"] = error_message

        try:
            self.screens.update(screen_id, payload)
        except Exception as exc:  # pragma: no cover - API failure path
            raise RuntimeError(
                f"Failed to update screen {screen_id} status to {status}"
            ) from exc
