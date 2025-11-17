"""Agno agent definitions and workflow orchestration.

This module defines the three core agents (Deep Research, Incremental Search, Assessment)
and the linear screening workflow that coordinates them.
"""

from datetime import datetime
from typing import TYPE_CHECKING, Any, Optional, TypeVar

from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.tools.reasoning import ReasoningTools
from pydantic import BaseModel

from demo.models import (
    AssessmentResult,
    Citation,
    DimensionScore,
    ExecutiveResearchResult,
)

if TYPE_CHECKING:
    from typing import Literal


ModelT = TypeVar("ModelT", bound=BaseModel)


def create_research_agent(use_deep_research: bool = True) -> Agent:
    """Create research agent with flexible execution mode.

    Args:
        use_deep_research: When ``True``, configure the agent with
            ``o4-mini-deep-research``. Fast mode (``False``) is deferred to
            Phase 2.

    Returns:
        Agent: Configured Deep Research agent instance.

    Raises:
        NotImplementedError: If ``use_deep_research`` is ``False`` during the
            minimal v1 implementation.

    Example:
        >>> agent = create_research_agent()
        >>> agent.model.id
        'o4-mini-deep-research'

    Notes:
        - v1 implementation only requires ``use_deep_research=True``
        - Fast mode (gpt-5 + web_search) is future enhancement
        - Deep Research returns markdown (NOT structured output)
        - DO NOT use ``output_schema`` with Deep Research models
    """
    if not use_deep_research:
        raise NotImplementedError(
            "Fast mode (gpt-5 + web_search) is Phase 2+. "
            "v1.0-minimal only supports Deep Research mode."
        )

    return Agent(
        name="Deep Research Agent",
        model=OpenAIResponses(id="o4-mini-deep-research", max_tool_calls=1),
        # CRITICAL: NO output_schema - Deep Research API doesn't support structured outputs
        instructions="""
Research this executive comprehensively using all available sources.

Focus on:
- Career trajectory: roles, companies, tenure, progression
- Leadership experience: team sizes, scope of responsibility
- Domain expertise: technical/functional areas, industry sectors
- Company stage experience: startup, growth, scale, public
- Notable achievements: exits, fundraising, product launches
- Public evidence: LinkedIn, company sites, news articles

Structure your response with clear sections:
- Executive Summary
- Career Timeline
- Leadership & Team Building
- Domain Expertise
- Stage & Sector Experience
- Key Achievements
- Gaps in Public Evidence

Include inline citations with URLs and relevant quotes.

Be explicit about:
- What you found with supporting citations
- What you couldn't find (gaps)
- Confidence level based on evidence quality/quantity
        """.strip(),
        exponential_backoff=True,
        retries=2,
        delay_between_retries=1,
    )


def create_incremental_search_agent(max_tool_calls: int = 2) -> Agent:
    """Create incremental search agent for single-pass supplemental research.

    Args:
        max_tool_calls: Maximum number of web search tool calls permitted. The
            default of ``2`` matches the v1 constraint.

    Returns:
        Agent: Configured incremental search Agno agent.

    Example:
        >>> agent = create_incremental_search_agent()
        >>> agent.max_tool_calls
        2
    """

    return Agent(
        name="Incremental Search Agent",
        model=OpenAIResponses(id="gpt-5"),
        tools=[{"type": "web_search_preview"}],
        max_tool_calls=max_tool_calls,
        output_schema=ExecutiveResearchResult,
        instructions="""
You are a single-pass supplemental researcher. Only run when Deep Research
results lack sufficient citations or key evidence.

Perform at most TWO targeted web searches to address the supplied gaps, then
stop. Focus on:
- Missing LinkedIn/biography details
- Leadership scope (team size, budgets, org design)
- Fundraising or product evidence relevant to the supplied role spec

Return only NEW information with supporting citations. If gaps remain after
the search, document them explicitly.
        """.strip(),
        exponential_backoff=True,
        retries=1,
        delay_between_retries=1,
    )


def create_assessment_agent() -> Agent:
    """Create assessment agent configured with ReasoningTools.

    Returns:
        Agent: Configured Agno agent that emits ``AssessmentResult`` outputs.

    Example:
        >>> agent = create_assessment_agent()
        >>> agent.tools[0].__class__.__name__
        'ReasoningTools'
    """

    return Agent(
        name="Assessment Agent",
        model=OpenAIResponses(id="gpt-5-mini"),
        tools=[ReasoningTools(add_instructions=True)],
        output_schema=AssessmentResult,
        instructions="""
Evaluate the candidate using the provided research and role specification.

Your process:
1. For each dimension in the role spec:
   - Score on a 1-5 scale. Use null/None when evidence is insufficient.
   - Provide confidence (High/Medium/Low) and reasoning tied to citations.
2. Summarize must-have checks, red flags, green flags, and counterfactuals.
3. Keep reasoning explicit and reference public evidence. Never fabricate.
        """.strip(),
        exponential_backoff=True,
        retries=2,
        delay_between_retries=1,
    )


def run_research(
    candidate_name: str,
    current_title: str,
    current_company: str,
    linkedin_url: Optional[str] = None,
    use_deep_research: bool = True,
) -> ExecutiveResearchResult:
    """Execute research on candidate and return structured results.

    Args:
        candidate_name: Executive full name.
        current_title: Current job title.
        current_company: Current company name.
        linkedin_url: LinkedIn profile URL (optional).
        use_deep_research: Toggle between deep and fast modes (v1: ``True``
            only).

    Returns:
        ExecutiveResearchResult: Parsed research output.

    Raises:
        RuntimeError: If the research agent fails after the configured retries.

    Example:
        >>> result = run_research(
        ...     candidate_name="Jane Doe",
        ...     current_title="CTO",
        ...     current_company="Acme Corp",
        ... )
        >>> result.exec_name
        'Jane Doe'

    Notes:
        - Uses Agno's built-in retry with ``exponential_backoff=True``
        - Deep Research returns markdown via ``result.content``
        - Citations extracted from ``result.citations``
        - No separate parser agent needed
    """
    # Create agent
    agent = create_research_agent(use_deep_research=use_deep_research)

    # Build prompt
    linkedin_section = (
        f"\nLinkedIn: {linkedin_url}" if linkedin_url else "\nLinkedIn: Not provided"
    )

    prompt = f"""
Candidate: {candidate_name}
Current Title: {current_title} at {current_company}{linkedin_section}

Research this executive comprehensively.
    """.strip()

    # Execute research
    try:
        result = agent.run(prompt)
    except Exception as e:
        raise RuntimeError(
            f"Research agent failed for {candidate_name} after retries: {e}"
        ) from e

    # Extract markdown and citations with type checking
    research_markdown: str = str(result.content) if hasattr(result, "content") else ""
    citations_raw = (
        result.citations.urls
        if hasattr(result, "citations") and result.citations
        else []
    )

    # Build Citation objects with safe type handling
    citations = [
        Citation(
            url=str(c.url) if hasattr(c, "url") else "",
            title=str(c.title) if hasattr(c, "title") and c.title else str(c.url),
            snippet="",  # Deep Research doesn't provide snippets directly
            relevance_note=None,
        )
        for c in (citations_raw if citations_raw else [])
    ]

    # Parse markdown for summary (first 2000 chars or up to first major section)
    research_summary = _extract_summary(research_markdown)

    # Estimate confidence based on citation count and content length
    confidence = _estimate_confidence(citations, research_markdown)

    # Create structured result
    # NOTE: v1 does minimal markdown parsing - just stores markdown and extracts summary
    # Phase 2+ can add structured extraction for career_timeline, expertise_areas, etc.
    return ExecutiveResearchResult(
        exec_name=candidate_name,
        current_role=current_title,
        current_company=current_company,
        # Career fields (v1: empty - parsed from markdown in Phase 2+)
        career_timeline=[],
        total_years_experience=None,
        # Domain fields (v1: empty - parsed from markdown in Phase 2+)
        fundraising_experience=None,
        operational_finance_experience=None,
        technical_leadership_experience=None,
        team_building_experience=None,
        sector_expertise=[],
        stage_exposure=[],
        # Summary & Evidence
        research_summary=research_summary,
        key_achievements=[],  # v1: empty - parsed in Phase 2+
        notable_companies=[],  # v1: empty - parsed in Phase 2+
        citations=citations,
        # Confidence & Gaps
        research_confidence=confidence,
        gaps=_identify_gaps(research_markdown, citations),
        # Metadata
        research_timestamp=datetime.now(),
        research_model="o4-mini-deep-research",
    )


def run_incremental_search(
    candidate_name: str,
    initial_research: ExecutiveResearchResult,
    quality_gaps: Optional[list[str]] = None,
    role_spec_markdown: Optional[str] = None,
) -> ExecutiveResearchResult:
    """Perform single-pass supplemental research when quality checks fail.

    Args:
        candidate_name: Candidate name for logging/context.
        initial_research: Baseline research output from Deep Research.
        quality_gaps: Specific gaps detected by ``check_research_quality``.
        role_spec_markdown: Role spec snippet to guide targeted searches.

    Returns:
        ExecutiveResearchResult: Merged research artifact.

    Raises:
        RuntimeError: If the incremental search agent fails after retries.

    Example:
        >>> base = ExecutiveResearchResult(
        ...     exec_name="Casey",
        ...     current_role="CFO",
        ...     current_company="Northwind",
        ...     research_summary="Baseline",
        ... )
        >>> merged = run_incremental_search("Casey", base, ["Need citations"])
        >>> merged.exec_name
        'Casey'
    """

    agent = create_incremental_search_agent()
    prompt = _build_incremental_prompt(
        candidate_name=candidate_name,
        initial_research=initial_research,
        quality_gaps=quality_gaps,
        role_spec_markdown=role_spec_markdown,
    )

    try:
        result = agent.run(prompt)
    except Exception as exc:  # pragma: no cover - depends on API behavior
        raise RuntimeError(
            f"Incremental search failed for {candidate_name}: {exc}"
        ) from exc

    supplemental = _coerce_model(result, ExecutiveResearchResult)

    if not supplemental:
        return initial_research

    return _merge_research_results(
        original=initial_research,
        supplemental=supplemental,
    )


def assess_candidate(
    research: ExecutiveResearchResult,
    role_spec_markdown: str,
    custom_instructions: Optional[str] = None,
) -> AssessmentResult:
    """Evaluate a candidate against the role spec with evidence-aware scoring.

    Args:
        research: Structured research produced by ``run_research`` (plus any
            incremental addenda).
        role_spec_markdown: Role specification markdown used as the evaluation
            rubric.
        custom_instructions: Optional recruiter-provided overrides.

    Returns:
        AssessmentResult: Structured assessment with dimension scores and
        overall score populated.

    Raises:
        RuntimeError: If the assessment agent fails after retries.

    Example:
        >>> research = ExecutiveResearchResult(
        ...     exec_name="Alex",
        ...     current_role="CTO",
        ...     current_company="ExampleCo",
        ...     research_summary="Summary",
        ... )
        >>> assess_candidate(research, "# Role Spec\n- Dimension: ...")
        AssessmentResult(...)
    """

    agent = create_assessment_agent()
    prompt = _build_assessment_prompt(
        research=research,
        role_spec_markdown=role_spec_markdown,
        custom_instructions=custom_instructions,
    )

    try:
        result = agent.run(prompt)
    except Exception as exc:  # pragma: no cover - depends on API behavior
        raise RuntimeError(
            f"Assessment agent failed for {research.exec_name}: {exc}"
        ) from exc

    assessment = _coerce_model(result, AssessmentResult)
    assessment.overall_score = calculate_overall_score(assessment.dimension_scores)
    assessment.role_spec_used = role_spec_markdown

    return assessment


def check_research_quality(research: ExecutiveResearchResult) -> bool:
    """Determine if research meets the minimum sufficiency threshold.

    Args:
        research: Research payload to evaluate.

    Returns:
        bool: ``True`` if there are ≥3 unique citations and a non-empty summary.

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
    unique_citations = {citation.url for citation in research.citations if citation.url}

    return summary_present and len(unique_citations) >= 3


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

    return (sum(scored) / len(scored)) * 20


def _extract_summary(markdown: str, max_length: int = 2000) -> str:
    """Extract research summary from markdown (first section or truncated).

    Args:
        markdown: Full research markdown
        max_length: Maximum summary length

    Returns:
        Truncated summary text
    """
    if not markdown:
        return ""

    # Take first max_length characters
    if len(markdown) <= max_length:
        return markdown.strip()

    # Truncate at max_length and try to end at a sentence boundary
    truncated = markdown[:max_length]
    last_period = truncated.rfind(".")
    if last_period > max_length * 0.7:  # If we found a period in last 30%
        return truncated[: last_period + 1].strip()

    return truncated.strip() + "..."


def _estimate_confidence(
    citations: list[Citation], markdown: str
) -> "Literal['High', 'Medium', 'Low']":
    """Estimate research confidence based on citations and content.

    Args:
        citations: List of Citation objects
        markdown: Research markdown text

    Returns:
        Confidence level: "High", "Medium", or "Low"
    """
    citation_count = len(citations)
    content_length = len(markdown)

    # High confidence: ≥5 citations and substantial content
    if citation_count >= 5 and content_length >= 2000:
        return "High"

    # Low confidence: <3 citations or minimal content
    if citation_count < 3 or content_length < 500:
        return "Low"

    # Medium confidence: everything else
    return "Medium"


def _identify_gaps(markdown: str, citations: list[Citation]) -> list[str]:
    """Identify gaps in research evidence.

    Args:
        markdown: Research markdown text
        citations: List of Citation objects

    Returns:
        List of identified gaps (empty if sufficient)
    """
    gaps = []

    # Check for insufficient citations
    if len(citations) < 3:
        gaps.append(
            f"Only {len(citations)} citations found (need ≥3 for quality threshold)"
        )

    # Check for minimal content
    if len(markdown) < 500:
        gaps.append("Research content is minimal (< 500 chars)")

    # Check for missing sections (simple keyword search)
    required_sections = ["career", "leadership", "experience"]
    markdown_lower = markdown.lower()
    missing_sections = [s for s in required_sections if s not in markdown_lower]

    if missing_sections:
        gaps.append(f"Potentially missing sections: {', '.join(missing_sections)}")

    return gaps


def _build_incremental_prompt(
    candidate_name: str,
    initial_research: ExecutiveResearchResult,
    quality_gaps: Optional[list[str]],
    role_spec_markdown: Optional[str],
) -> str:
    """Create supplemental search instructions for the incremental agent."""

    summary = initial_research.research_summary or "No research summary recorded yet."
    gaps_section = (
        "\n".join(f"- {gap}" for gap in quality_gaps)
        if quality_gaps
        else "- Missing public evidence (general)"
    )
    citations_section = (
        "\n".join(f"- {c.title}: {c.url}" for c in initial_research.citations)
        if initial_research.citations
        else "- No citations were captured"
    )
    role_section = (
        f"\nROLE SPECIFICATION CONTEXT:\n{role_spec_markdown.strip()}"
        if role_spec_markdown
        else ""
    )

    return (
        f"CANDIDATE: {candidate_name}\n"
        f"CURRENT ROLE: {initial_research.current_role} at {initial_research.current_company}\n\n"
        f"EXISTING SUMMARY:\n{summary}\n\n"
        f"KNOWN CITATIONS:\n{citations_section}\n\n"
        f"IDENTIFIED GAPS:\n{gaps_section}{role_section}\n\n"
        "Run up to TWO targeted web searches to close the gaps. Return only new "
        "information plus citations that support it."
    )


def _merge_research_results(
    original: ExecutiveResearchResult, supplemental: ExecutiveResearchResult
) -> ExecutiveResearchResult:
    """Merge Deep Research output with incremental research findings."""

    merged = original.model_copy(deep=True)

    # Merge narrative summary
    if supplemental.research_summary.strip():
        if merged.research_summary.strip():
            merged.research_summary = (
                f"{merged.research_summary.strip()}\n\nSupplemental Research:\n"
                f"{supplemental.research_summary.strip()}"
            )
        else:
            merged.research_summary = supplemental.research_summary

    # Merge citations
    seen_urls = {citation.url for citation in merged.citations if citation.url}
    for citation in supplemental.citations:
        if citation.url and citation.url not in seen_urls:
            merged.citations.append(citation)
            seen_urls.add(citation.url)

    # Merge lists (achievements, companies, expertise, stages)
    merged.key_achievements = _merge_unique_strings(
        merged.key_achievements, supplemental.key_achievements
    )
    merged.notable_companies = _merge_unique_strings(
        merged.notable_companies, supplemental.notable_companies
    )
    merged.sector_expertise = _merge_unique_strings(
        merged.sector_expertise, supplemental.sector_expertise
    )
    merged.stage_exposure = _merge_unique_strings(
        merged.stage_exposure, supplemental.stage_exposure
    )

    # Merge career timeline entries while preventing duplicates
    seen_roles = {
        (entry.company, entry.role, entry.start_date, entry.end_date)
        for entry in merged.career_timeline
    }
    for entry in supplemental.career_timeline:
        key = (entry.company, entry.role, entry.start_date, entry.end_date)
        if key not in seen_roles:
            merged.career_timeline.append(entry)
            seen_roles.add(key)

    # Merge gaps (dedupe for readability)
    merged.gaps = _merge_unique_strings(merged.gaps, supplemental.gaps)

    # Update metadata
    merged.research_timestamp = datetime.now()
    merged.research_confidence = _pick_stronger_confidence(
        original_confidence=merged.research_confidence,
        supplemental_confidence=supplemental.research_confidence,
    )

    return merged


def _merge_unique_strings(first: list[str], second: list[str]) -> list[str]:
    """Return merged list of unique non-empty strings preserving order."""

    seen = []
    for value in [*first, *second]:
        normalized = value.strip()
        if normalized and normalized not in seen:
            seen.append(normalized)
    return seen


def _pick_stronger_confidence(
    original_confidence: "Literal['High', 'Medium', 'Low']",
    supplemental_confidence: "Literal['High', 'Medium', 'Low']",
) -> "Literal['High', 'Medium', 'Low']":
    """Choose the stronger confidence level between two options."""

    scale = {"Low": 0, "Medium": 1, "High": 2}
    return (
        original_confidence
        if scale[original_confidence] >= scale[supplemental_confidence]
        else supplemental_confidence
    )


def _build_assessment_prompt(
    research: ExecutiveResearchResult,
    role_spec_markdown: str,
    custom_instructions: Optional[str],
) -> str:
    """Create the prompt supplied to the assessment agent."""

    research_block = _format_research_for_assessment(research)
    prompt = [
        "ROLE SPECIFICATION:",
        role_spec_markdown.strip() or "(role specification missing)",
        "",
        "CANDIDATE RESEARCH:",
        research_block,
        "",
        "EVALUATION TASK:",
        "Follow the scoring rubric. Use ReasoningTools to think explicitly and "
        "mark dimensions as null when evidence is insufficient.",
    ]

    if custom_instructions:
        prompt.extend(
            [
                "",
                "CUSTOM INSTRUCTIONS:",
                custom_instructions.strip(),
            ]
        )

    return "\n".join(prompt).strip()


def _format_research_for_assessment(research: ExecutiveResearchResult) -> str:
    """Format research data into readable sections for the LLM."""

    timeline_lines = [
        f"- {entry.role} at {entry.company} ({entry.start_date or '?'} - {entry.end_date or 'Present'})"
        for entry in research.career_timeline
    ]
    timeline_text = (
        "\n".join(timeline_lines) if timeline_lines else "- Timeline not parsed yet"
    )
    citations = (
        "\n".join(
            f"- {citation.title} ({citation.url})" for citation in research.citations
        )
        if research.citations
        else "- No citations recorded"
    )
    gaps = (
        "\n".join(f"- {gap}" for gap in research.gaps)
        if research.gaps
        else "- No explicit gaps."
    )

    sections = [
        f"Candidate: {research.exec_name}",
        f"Current Role: {research.current_role} at {research.current_company}",
        "",
        "Summary:",
        research.research_summary or "(no summary provided)",
        "",
        "Career Timeline:",
        timeline_text,
        "",
        "Key Achievements:",
        "\n".join(f"- {achievement}" for achievement in research.key_achievements)
        or "- Not documented",
        "",
        "Sector Expertise: " + (", ".join(research.sector_expertise) or "Unknown"),
        "Stage Exposure: " + (", ".join(research.stage_exposure) or "Unknown"),
        "",
        "Citations:",
        citations,
        "",
        "Known Gaps:",
        gaps,
    ]

    return "\n".join(sections).strip()


def _coerce_model(raw: Any, model_cls: type[ModelT]) -> ModelT:
    """Best-effort conversion of agent output into the requested Pydantic model."""

    candidate = raw

    if isinstance(candidate, model_cls):
        return candidate

    if hasattr(candidate, "content"):
        content = getattr(candidate, "content")
        if isinstance(content, model_cls):
            return content
        candidate = content

    if isinstance(candidate, BaseModel):
        return model_cls.model_validate(candidate.model_dump())

    if isinstance(candidate, dict):
        return model_cls.model_validate(candidate)

    raise TypeError(
        f"Agent returned payload that cannot be coerced into {model_cls.__name__}"
    )
