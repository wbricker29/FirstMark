"""Pydantic models for structured research and assessment outputs.

This module defines all data models used throughout the screening workflow,
including research results, dimension scores, and assessment outputs.
"""

from datetime import datetime
from typing import Any, Literal, Optional, TypedDict

from pydantic import BaseModel, Field


class Citation(BaseModel):
    """Source citation from research."""

    url: str
    title: str
    snippet: str
    relevance_note: Optional[str] = None


class CareerEntry(BaseModel):
    """Timeline entry for career history."""

    company: str
    role: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    key_achievements: list[str] = Field(default_factory=list)


class ExecutiveResearchResult(BaseModel):
    """Structured research output."""

    exec_name: str
    current_role: str
    current_company: str

    # Career & Experience
    career_timeline: list[CareerEntry] = Field(default_factory=list)
    total_years_experience: Optional[int] = None

    # Key Areas (aligned with role spec dimensions)
    fundraising_experience: Optional[str] = None  # CFO-specific
    operational_finance_experience: Optional[str] = None  # CFO-specific
    technical_leadership_experience: Optional[str] = None  # CTO-specific
    team_building_experience: Optional[str] = None
    sector_expertise: list[str] = Field(default_factory=list)
    stage_exposure: list[str] = Field(default_factory=list)

    # Summary & Evidence
    research_summary: str
    research_markdown_raw: str = ""
    key_achievements: list[str] = Field(default_factory=list)
    notable_companies: list[str] = Field(default_factory=list)
    citations: list[Citation] = Field(default_factory=list)

    # Confidence & Gaps
    research_confidence: Literal["High", "Medium", "Low"] = "Medium"
    gaps: list[str] = Field(default_factory=list)

    # Metadata
    research_timestamp: datetime = Field(default_factory=datetime.now)
    research_model: str = "o4-mini-deep-research"


class DimensionScore(BaseModel):
    """Evidence-aware dimension score for a single evaluation criterion."""

    dimension: str

    # Scoring (1-5 scale with None for Unknown)
    score: Optional[int] = Field(None, ge=1, le=5)
    # None (Python) / null (JSON) = Unknown / Insufficient evidence
    # DO NOT use NaN or 0 - always use None for missing scores

    # Evidence Quality
    evidence_level: Literal["High", "Medium", "Low"]  # From role spec
    confidence: Literal["High", "Medium", "Low"]  # LLM self-assessment

    # Reasoning & Evidence
    reasoning: str  # 1-3 sentences explaining the score
    evidence_quotes: list[str] = Field(default_factory=list)
    citation_urls: list[str] = Field(default_factory=list)


class MustHaveCheck(BaseModel):
    """Evaluation of must-have requirements."""

    requirement: str
    met: bool
    evidence: Optional[str] = None


class AssessmentResult(BaseModel):
    """Structured assessment output from gpt-5-mini."""

    # Overall Assessment
    overall_score: Optional[float] = Field(None, ge=0, le=100)
    # Computed in Python from dimension scores
    overall_confidence: Literal["High", "Medium", "Low"]

    # Dimension-Level Scores
    dimension_scores: list[DimensionScore]

    # Requirements Checking
    must_haves_check: list[MustHaveCheck] = Field(default_factory=list)
    red_flags_detected: list[str] = Field(default_factory=list)
    green_flags: list[str] = Field(default_factory=list)

    # Qualitative Assessment
    summary: str  # 2-3 sentence topline
    counterfactuals: list[str] = Field(default_factory=list)

    # Metadata
    assessment_timestamp: datetime = Field(default_factory=datetime.now)
    assessment_model: str = "gpt-5-mini"
    role_spec_used: Optional[str] = None


class RoleSpecData(BaseModel):
    """Role spec data from role_spec_slug.role_spec."""

    role_spec_id: str
    role_spec_name: str
    role_spec_content: str


class RoleSpecSlug(BaseModel):
    """Wrapper for role_spec_slug."""

    role_spec: RoleSpecData


class RoleData(BaseModel):
    """Role data from search_slug.role."""

    ATID: str
    portco: str
    role_title: str = ""
    role_type: str
    role_description: str = ""


class SearchSlug(BaseModel):
    """Wrapper for search_slug."""

    role: RoleData


class CandidateData(BaseModel):
    """Candidate data from candidate_slugs[].candidate."""

    ATID: str
    candidate_name: str
    candidate_current_title: str = ""
    candidate_normalized_title: str = ""
    candidate_current_company: str = ""
    candidate_location: str = ""
    candidate_linkedin: str = ""
    candidate_bio: str = ""


class CandidateDict(TypedDict, total=False):
    """TypedDict for candidate data passed to workflow functions.

    This represents the standardized candidate dict structure used throughout
    the screening workflow. Keys match the output of ScreenWebhookPayload.get_candidates().
    """

    id: str  # Required: Airtable record ID
    name: str  # Required: Candidate full name
    title: str  # Optional: Current job title
    company: str  # Optional: Current company name
    linkedin: str  # Optional: LinkedIn profile URL
    location: str  # Optional: Geographic location
    bio: str  # Optional: Candidate biography text
    record_id: str  # Legacy Airtable record ID field
    airtable_id: str  # Alternate legacy identifier
    current_title: str  # Legacy direct field for title
    current_company: str  # Legacy direct field for company
    linkedin_url: str  # Legacy direct field for LinkedIn
    fields: dict[str, Any]  # Legacy embedded Airtable fields dictionary


class CandidateSlug(BaseModel):
    """Wrapper for candidate in candidate_slugs array."""

    candidate: CandidateData


class ScreenSlugData(BaseModel):
    """Screen record data from screen_slug."""

    screen_id: str
    screen_edited: Optional[str] = None
    role_spec_slug: RoleSpecSlug
    search_slug: SearchSlug
    candidate_slugs: list[CandidateSlug]


class ScreenWebhookPayload(BaseModel):
    """Complete screening payload from Airtable with structured nested objects.

    Airtable sends this as structured objects (not JSON strings), so no parsing needed.

    Example webhook payload:
    {
        "screen_slug": {
            "screen_id": "recABC123",
            "screen_edited": "2025-11-18T20:01:46.000Z",
            "role_spec_slug": {
                "role_spec": {
                    "role_spec_id": "recRS123",
                    "role_spec_name": "CFO - Series B",
                    "role_spec_content": "# Role Spec\n..."
                }
            },
            "search_slug": {
                "role": {
                    "ATID": "recR123",
                    "portco": "Pigment",
                    "role_type": "CFO",
                    "role_title": "",
                    "role_description": "..."
                }
            },
            "candidate_slugs": [
                {
                    "candidate": {
                        "ATID": "recP1",
                        "candidate_name": "Jane Doe",
                        "candidate_current_title": "CFO",
                        ...
                    }
                }
            ]
        }
    }
    """

    screen_slug: ScreenSlugData = Field(..., description="Screen record data")

    @property
    def screen_id(self) -> str:
        """Get screen Airtable record ID."""
        return self.screen_slug.screen_id

    @property
    def spec_markdown(self) -> str:
        """Get role specification markdown content."""
        return self.screen_slug.role_spec_slug.role_spec.role_spec_content

    @property
    def role_name(self) -> str:
        """Get role name from search info."""
        role = self.screen_slug.search_slug.role
        return role.role_title or role.role_type

    @property
    def portco_name(self) -> str:
        """Get portfolio company name."""
        return self.screen_slug.search_slug.role.portco

    @property
    def custom_instructions(self) -> Optional[str]:
        """Get custom instructions if available."""
        # Not in current payload structure, but can be added
        return None

    def get_candidates(self) -> list[CandidateDict]:
        """Get candidate data as structured list.

        Returns:
            List of candidate dicts with keys: id, name, title, company, linkedin,
            location, bio. All fields guaranteed to exist (may be empty string).

        Example:
            >>> payload.get_candidates()
            [
                {
                    "id": "recP1",
                    "name": "Jane Doe",
                    "title": "CFO",
                    "company": "Acme Inc",
                    "linkedin": "",
                    "location": "",
                    "bio": ""
                },
                ...
            ]
        """
        return [
            {
                "id": slug.candidate.ATID,
                "name": slug.candidate.candidate_name,
                "title": slug.candidate.candidate_current_title or "",
                "company": slug.candidate.candidate_current_company or "",
                "linkedin": slug.candidate.candidate_linkedin or "",
                "location": slug.candidate.candidate_location or "",
                "bio": slug.candidate.candidate_bio or "",
            }
            for slug in self.screen_slug.candidate_slugs
        ]
