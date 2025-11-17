"""Pydantic models for structured research and assessment outputs.

This module defines all data models used throughout the screening workflow,
including research results, dimension scores, and assessment outputs.
"""

from datetime import datetime
from typing import Literal, Optional

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
