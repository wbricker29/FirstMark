"""Business logic helpers for candidate screening workflow.

This module contains standalone utility functions used by the screening workflow
that are not tightly coupled to agent execution or workflow orchestration.
"""

from textwrap import shorten
from typing import Any, Mapping, Optional, cast

from demo.models import (
    AssessmentResult,
    CandidateDict,
    DimensionScore,
    ExecutiveResearchResult,
    MustHaveCheck,
)
from demo.settings import settings


def reconstruct_research(
    data: dict | ExecutiveResearchResult,
) -> ExecutiveResearchResult:
    """Reconstruct ExecutiveResearchResult from dict or return as-is.

    Args:
        data: Either a dict representation or an ExecutiveResearchResult instance.

    Returns:
        ExecutiveResearchResult: Validated research object.

    Example:
        >>> research_dict = {"exec_name": "Jane", "current_role": "CTO", ...}
        >>> result = reconstruct_research(research_dict)
        >>> isinstance(result, ExecutiveResearchResult)
        True
    """
    if isinstance(data, dict):
        return ExecutiveResearchResult.model_validate(data)
    return data


def check_research_quality(research: ExecutiveResearchResult) -> bool:
    """Determine if research meets the minimum sufficiency threshold.

    Args:
        research: Research payload to evaluate.

    Returns:
        bool: ``True`` if there are ≥min_citations unique citations and a non-empty summary.
        Citations are counted by URL if present, otherwise by title (fallback).

    Example:
        >>> research = ExecutiveResearchResult(
        ...     exec_name="Jamie",
        ...     current_role="COO",
        ...     current_company="Acme",
        ...     research_summary="Summary",
        ...     citations=[
        ...         Citation(url="https://1", title="One", snippet=""),
        ...         Citation(url="https://2", title="Two", snippet=""),
        ...         Citation(url="https://3", title="Three", snippet=""),
        ...     ],
        ... )
        >>> check_research_quality(research)
        True
    """

    summary_present = bool(research.research_summary.strip())

    # Count unique citations by URL only (stricter quality gate)
    # Citations without URLs are ignored as they likely indicate low-quality sources
    unique_citations = set()
    for citation in research.citations:
        if citation.url:
            unique_citations.add(citation.url)

    return summary_present and len(unique_citations) >= settings.quality.min_citations


def calculate_overall_score(
    dimension_scores: list[DimensionScore],
) -> Optional[float]:
    """Calculate a candidate's overall score based on scored dimensions.

    Args:
        dimension_scores: Dimension-level outputs from ``AssessmentResult``.

    Returns:
        Optional[float]: Score on a 0-100 scale or ``None`` if no dimensions
        were scorable.

    Example:
        >>> scores = [
        ...     DimensionScore(
        ...         dimension="Leadership",
        ...         score=4,
        ...         evidence_level="High",
        ...         confidence="Medium",
        ...         reasoning="",
        ...     ),
        ...     DimensionScore(
        ...         dimension="Strategy",
        ...         score=None,
        ...         evidence_level="Medium",
        ...         confidence="Low",
        ...         reasoning="",
        ...     ),
        ... ]
        >>> calculate_overall_score(scores)
        80.0
    """

    scored = [score.score for score in dimension_scores if score.score is not None]

    if not scored:
        return None

    return round((sum(scored) / len(scored)) * 20, 1)


def validate_candidates(candidates: list[CandidateDict]) -> None:
    """Validate that candidates list is non-empty.

    Args:
        candidates: List of candidate dicts to validate.

    Raises:
        ValueError: If candidates list is empty.
    """
    if not candidates:
        raise ValueError("At least one candidate is required")


def extract_candidate_context(candidate: CandidateDict) -> dict[str, str]:
    """Extract candidate context from standardized webhook payload.

    Args:
        candidate: Candidate dict with keys: id, name, title, company, linkedin, location, bio.
            These come from ScreenWebhookPayload.get_candidates() parsing.

    Returns:
        Dict with keys: candidate_id, candidate_name, current_title, current_company, linkedin_url.
        All values are strings (empty strings for missing optional fields).

    Note:
        Supports both new webhook format (direct keys) and legacy format (nested fields)
        for backward compatibility.
    """
    candidate_mapping = cast(Mapping[str, Any], candidate)

    # Support both new webhook format (direct keys) and legacy format (nested fields)
    # Legacy format: candidate["fields"]["Name"] or candidate["fields"]["Full Name"]
    # New format: candidate["name"] (from webhook payload parsing)
    if "name" in candidate_mapping:
        # New webhook payload format
        candidate_id_raw = candidate_mapping.get("id", "unknown")
        candidate_name_raw = candidate_mapping.get("name", "Unnamed Candidate")
        current_title = str(candidate_mapping.get("title") or "")
        current_company = str(candidate_mapping.get("company") or "")
        linkedin_url = str(candidate_mapping.get("linkedin") or "")
    else:
        # Legacy format (backward compatibility)
        fields_raw = candidate_mapping.get("fields", {})
        if isinstance(fields_raw, Mapping):
            fields: Mapping[str, Any] = fields_raw
        else:
            fields = {}
        candidate_id_raw = (
            candidate_mapping.get("id")
            or candidate_mapping.get("record_id")
            or candidate_mapping.get("airtable_id")
            or fields.get("id")
        )
        candidate_name_raw = (
            fields.get("Name")
            or fields.get("Full Name")
            or candidate_mapping.get("Full Name")
            or candidate_mapping.get("name")
            or "Unnamed Candidate"
        )
        current_title = (
            fields.get("Current Title")
            or fields.get("Title")
            or candidate_mapping.get("current_title")
            or candidate_mapping.get("title")
            or ""
        )
        current_company_field = (
            fields.get("Current Company")
            or fields.get("Company")
            or candidate_mapping.get("current_company")
            or candidate_mapping.get("company")
        )
        if isinstance(current_company_field, list):
            current_company = ""
        else:
            current_company = (
                str(current_company_field) if current_company_field else ""
            )
        linkedin_url = (
            fields.get("LinkedIn URL")
            or fields.get("LinkedIn")
            or candidate_mapping.get("linkedin_url")
            or ""
        )

    candidate_id = str(candidate_id_raw) if candidate_id_raw else "unknown"
    candidate_name = (
        str(candidate_name_raw) if candidate_name_raw else "Unnamed Candidate"
    )
    current_title = str(current_title or "Unknown")
    current_company = str(current_company or "Unknown")
    linkedin_url = str(linkedin_url or "")

    return {
        "candidate_id": candidate_id,
        "candidate_name": candidate_name,
        "current_title": current_title,
        "current_company": current_company,
        "linkedin_url": linkedin_url,
    }


def _format_dimension_snapshot(scores: list[DimensionScore]) -> list[str]:
    """Render a compact markdown list summarizing dimension scores."""

    if not scores:
        return ["- No dimension scores were provided."]

    formatted: list[str] = []
    for score in scores:
        rating = f"{score.score}/5" if score.score is not None else "Unknown"
        formatted.append(
            f"- **{score.dimension}:** {rating} — {score.confidence} confidence, {score.evidence_level} evidence"
        )

    return formatted[:5]


def _format_must_have_summary(checks: list[MustHaveCheck]) -> str:
    """Return a single-line description of must-have coverage."""

    if not checks:
        return "No must-have requirements were evaluated."

    met = sum(1 for check in checks if check.met)
    return f"Met {met}/{len(checks)} must-have requirements."


def render_assessment_markdown_inline(
    candidate: CandidateDict,
    assessment: AssessmentResult,
    research: Optional[ExecutiveResearchResult] = None,
) -> str:
    """Render a concise markdown summary for Airtable's inline field."""

    context = extract_candidate_context(candidate)
    candidate_name = context["candidate_name"] or "Unnamed Candidate"
    title = context["current_title"] or "Unknown title"
    company = context["current_company"] or "Unknown company"

    score_display = (
        f"{assessment.overall_score:.1f}"
        if assessment.overall_score is not None
        else "Unknown"
    )
    summary = assessment.summary.strip() or "No summary provided."

    lines = [
        f"### {candidate_name}",
        f"**Current Role:** {title} @ {company}",
        f"**Overall Score:** {score_display}/100 ({assessment.overall_confidence} confidence)",
        "",
        "**Summary**",
        summary,
        "",
        "**Dimension Snapshot**",
    ]
    lines.extend(_format_dimension_snapshot(assessment.dimension_scores))
    lines.append("")
    lines.append("**Must-Haves**")
    lines.append(f"- {_format_must_have_summary(assessment.must_haves_check)}")

    if research and research.research_summary.strip():
        lines.append("")
        lines.append("**Research Signal**")
        lines.append(
            f"- {shorten(research.research_summary.strip(), width=240, placeholder='…')}"
        )

    rendered = "\n".join(lines).strip()
    return f"{rendered}\n"


def render_screen_report(
    screen_id: str,
    candidate: CandidateDict,
    assessment: AssessmentResult,
    research: Optional[ExecutiveResearchResult] = None,
    role_spec_markdown: Optional[str] = None,
    custom_instructions: Optional[str] = None,
) -> str:
    """Create a comprehensive markdown report combining assessment + research."""

    context = extract_candidate_context(candidate)
    candidate_name = context["candidate_name"] or "Unnamed Candidate"
    candidate_id = context["candidate_id"] or "unknown"
    title = context["current_title"] or "Unknown title"
    company = context["current_company"] or "Unknown company"
    linkedin = context["linkedin_url"] or "Not provided"

    score_display = (
        f"{assessment.overall_score:.1f}"
        if assessment.overall_score is not None
        else "Unknown"
    )

    lines: list[str] = [
        f"# Screen Report: {candidate_name}",
        "",
        "## Candidate Snapshot",
        f"- **Screen ID:** {screen_id}",
        f"- **Candidate ID:** {candidate_id}",
        f"- **Current Role:** {title} @ {company}",
        f"- **LinkedIn:** {linkedin}",
    ]

    if custom_instructions:
        lines.append(f"- **Custom Instructions:** {custom_instructions.strip()}")

    lines.extend(
        [
            "",
            "## Assessment Summary",
            f"- **Overall Score:** {score_display}/100",
            f"- **Confidence:** {assessment.overall_confidence}",
            "",
            "### Topline Narrative",
            assessment.summary.strip() or "No summary provided.",
            "",
            "### Dimension Details",
        ]
    )

    dimension_lines = [
        f"- **{score.dimension}** — {('Unknown' if score.score is None else f'{score.score}/5')} | {score.confidence} confidence"
        + (
            f"\n  - Evidence: {score.reasoning.strip()}"
            if score.reasoning.strip()
            else ""
        )
        for score in assessment.dimension_scores
    ]
    lines.extend(dimension_lines or ["- No dimension scores provided."])

    lines.extend(
        [
            "",
            "### Must-Haves",
            _format_must_have_summary(assessment.must_haves_check),
        ]
    )

    if assessment.red_flags_detected:
        lines.append("")
        lines.append("### Red Flags")
        for flag in assessment.red_flags_detected:
            lines.append(f"- {flag}")
    if assessment.green_flags:
        lines.append("")
        lines.append("### Green Flags")
        for flag in assessment.green_flags:
            lines.append(f"- {flag}")
    if assessment.counterfactuals:
        lines.append("")
        lines.append("### Counterfactuals")
        for idea in assessment.counterfactuals:
            lines.append(f"- {idea}")

    if research:
        lines.extend(
            [
                "",
                "## Research Summary",
                research.research_summary.strip() or "Research summary unavailable.",
            ]
        )

        if research.key_achievements:
            lines.append("")
            lines.append("### Key Achievements")
            for achievement in research.key_achievements:
                lines.append(f"- {achievement}")

        if research.career_timeline:
            lines.append("")
            lines.append("### Career Timeline (most recent first)")
            for entry in list(reversed(research.career_timeline))[:5]:
                start = entry.start_date or "?"
                end = entry.end_date or "Present"
                lines.append(f"- {entry.role} @ {entry.company} ({start} – {end})")

        if research.citations:
            lines.append("")
            lines.append("### Citations")
            for citation in research.citations[:10]:
                suffix = f" — {citation.url}" if citation.url else ""
                lines.append(f"- {citation.title}{suffix}")
    else:
        lines.extend(
            [
                "",
                "## Research Summary",
                "No research results were available for this candidate.",
            ]
        )

    if role_spec_markdown:
        snippet_lines = role_spec_markdown.strip().splitlines()[:20]
        if snippet_lines:
            lines.append("")
            lines.append("## Role Spec Snapshot")
            lines.append("```markdown")
            lines.extend(snippet_lines)
            lines.append("```")

    return "\n".join(lines).strip() + "\n"
