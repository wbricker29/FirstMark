"""Agno agent definitions and workflow orchestration.

This module defines the three core agents (Deep Research, Incremental Search, Assessment)
and the linear screening workflow that coordinates them.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any, Optional, TypeVar

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIResponses
from agno.tools.reasoning import ReasoningTools
from agno.workflow import Step, Workflow
from pydantic import BaseModel

from demo.models import (
    AssessmentResult,
    Citation,
    DimensionScore,
    ExecutiveResearchResult,
)
from demo.prompts import get_prompt

if TYPE_CHECKING:
    from typing import Literal


ModelT = TypeVar("ModelT", bound=BaseModel)


logger = logging.getLogger("demo.agents")
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
    logger.addHandler(handler)
logger.setLevel(logging.INFO)


_SCREENING_WORKFLOW: Optional[Workflow] = None


def _noop_step_executor(*_: Any, **__: Any) -> None:  # pragma: no cover - placeholder
    """Placeholder executor so Workflow can document the linear step order."""


def create_screening_workflow() -> Workflow:
    """Create (or return cached) Workflow configured for screening runs.

    The workflow persists session state to ``tmp/agno_sessions.db`` using ``SqliteDb``
    and models the four linear steps (research → quality gate → optional incremental
    search → assessment). Steps use placeholder executors because orchestration is
    currently handled synchronously inside ``screen_single_candidate``.
    """

    global _SCREENING_WORKFLOW

    if _SCREENING_WORKFLOW is not None:
        return _SCREENING_WORKFLOW

    db_path = Path("tmp") / "agno_sessions.db"
    db_path.parent.mkdir(parents=True, exist_ok=True)

    workflow = Workflow(
        name="Talent Signal Screening Workflow",
        description="Deep research → quality gate → optional incremental search → assessment",
        db=SqliteDb(db_file=str(db_path)),
        session_state={
            "screen_id": None,
            "candidate_id": None,
            "candidate_name": None,
            "last_step": None,
            "quality_gate_triggered": False,
        },
        stream_events=True,
        steps=[
            Step(
                name="deep_research",
                description="Run Deep Research agent",
                executor=_noop_step_executor,  # type: ignore[arg-type]
            ),
            Step(
                name="quality_check",
                description="Evaluate research sufficiency",
                executor=_noop_step_executor,  # type: ignore[arg-type]
            ),
            Step(
                name="incremental_search",
                description="Optional single-pass incremental search",
                executor=_noop_step_executor,  # type: ignore[arg-type]
            ),
            Step(
                name="assessment",
                description="Evaluate candidate against role spec",
                executor=_noop_step_executor,  # type: ignore[arg-type]
            ),
        ],
    )

    _SCREENING_WORKFLOW = workflow
    return workflow


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

    prompt = get_prompt("deep_research")

    return Agent(
        name="Deep Research Agent",
        model=OpenAIResponses(id="o4-mini-deep-research", max_tool_calls=1),
        # CRITICAL: NO output_schema - Deep Research API doesn't support structured outputs
        **prompt.as_agent_kwargs(),
        add_datetime_to_context=True,
        exponential_backoff=True,
        retries=2,
        delay_between_retries=1,
    )


def create_research_parser_agent() -> Agent:
    """Create parser agent that converts markdown into structured results."""

    prompt = get_prompt("research_parser")

    return Agent(
        name="Research Parser Agent",
        model=OpenAIResponses(id="gpt-5-mini"),
        output_schema=ExecutiveResearchResult,
        **prompt.as_agent_kwargs(),
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

    prompt = get_prompt("incremental_search")

    return Agent(
        name="Incremental Search Agent",
        model=OpenAIResponses(id="gpt-5", max_tool_calls=max_tool_calls),
        tools=[{"type": "web_search_preview"}],
        output_schema=ExecutiveResearchResult,
        **prompt.as_agent_kwargs(),
        add_datetime_to_context=True,
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

    prompt = get_prompt("assessment")

    return Agent(
        name="Assessment Agent",
        model=OpenAIResponses(id="gpt-5-mini"),
        tools=[ReasoningTools(add_instructions=True)],
        output_schema=AssessmentResult,
        **prompt.as_agent_kwargs(),
        add_datetime_to_context=True,
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

    research_markdown: str = str(result.content) if hasattr(result, "content") else ""
    citation_dicts = _extract_citation_dicts(result)
    fallback_citations = _convert_dicts_to_citations(citation_dicts)

    parser_agent = create_research_parser_agent()
    parser_prompt = _build_parser_prompt(
        candidate_name=candidate_name,
        current_title=current_title,
        current_company=current_company,
        research_markdown=research_markdown,
        citations=citation_dicts,
    )

    try:
        parser_output = parser_agent.run(parser_prompt)
    except Exception as exc:  # pragma: no cover - API failure path
        raise RuntimeError(
            f"Research parser failed for {candidate_name} after Deep Research: {exc}"
        ) from exc

    structured = _coerce_model(parser_output, ExecutiveResearchResult)

    structured.research_markdown_raw = research_markdown
    structured.citations = _merge_citation_models(
        structured.citations,
        fallback_citations,
    )
    structured.research_summary = (
        structured.research_summary.strip()
        if structured.research_summary.strip()
        else _extract_summary(research_markdown)
    )
    structured.research_confidence = _estimate_confidence(
        structured.citations,
        research_markdown,
    )
    structured.gaps = structured.gaps or _identify_gaps(
        research_markdown,
        structured.citations,
    )
    structured.research_timestamp = datetime.now()
    structured.research_model = "o4-mini-deep-research"

    return structured


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

    return merge_research_results(
        original=initial_research,
        supplemental=supplemental,
    )


def merge_research_results(
    original: ExecutiveResearchResult,
    supplemental: Optional[ExecutiveResearchResult],
) -> ExecutiveResearchResult:
    """Merge Deep Research output with incremental search findings.

    Args:
        original: Primary Deep Research result.
        supplemental: Incremental search addendum (may be ``None``).

    Returns:
        Combined ExecutiveResearchResult with updated citations, summary, and confidence.
    """

    if supplemental is None:
        return original

    merged = original.model_copy(deep=True)

    # Merge narrative summaries.
    summary_sections: list[str] = []
    if merged.research_summary.strip():
        summary_sections.append(merged.research_summary.strip())
    if supplemental.research_summary.strip():
        summary_sections.append(
            "Supplemental Research:\n" + supplemental.research_summary.strip()
        )
    if summary_sections:
        merged.research_summary = "\n\n".join(summary_sections).strip()

    merged.research_markdown_raw = _merge_markdown_content(
        merged.research_markdown_raw,
        supplemental.research_markdown_raw or supplemental.research_summary,
    )

    # Merge citations with URL-based deduplication.
    seen_urls = {citation.url for citation in merged.citations if citation.url}
    for citation in supplemental.citations:
        url = citation.url
        if url and url in seen_urls:
            continue
        merged.citations.append(citation)
        if url:
            seen_urls.add(url)

    # Merge list fields.
    merged.key_achievements = _merge_unique_strings(
        merged.key_achievements,
        supplemental.key_achievements,
    )
    merged.notable_companies = _merge_unique_strings(
        merged.notable_companies,
        supplemental.notable_companies,
    )
    merged.sector_expertise = _merge_unique_strings(
        merged.sector_expertise,
        supplemental.sector_expertise,
    )
    merged.stage_exposure = _merge_unique_strings(
        merged.stage_exposure,
        supplemental.stage_exposure,
    )

    # Preserve career timeline ordering while appending new entries.
    seen_roles = {
        (entry.company, entry.role, entry.start_date, entry.end_date)
        for entry in merged.career_timeline
    }
    for entry in supplemental.career_timeline:
        key = (entry.company, entry.role, entry.start_date, entry.end_date)
        if key not in seen_roles:
            merged.career_timeline.append(entry)
            seen_roles.add(key)

    merged.gaps = _merge_unique_strings(merged.gaps, supplemental.gaps)

    # Update metadata and confidence based on the combined artifact.
    merged.research_timestamp = datetime.now()
    markdown_source = merged.research_markdown_raw.strip() or merged.research_summary
    merged.research_confidence = _estimate_confidence(merged.citations, markdown_source)

    return merged


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


def screen_single_candidate(
    candidate_data: dict[str, Any],
    role_spec_markdown: str,
    screen_id: str,
) -> AssessmentResult:
    """Run the full 4-step screening workflow for a single candidate.

    Args:
        candidate_data: Dictionary of Airtable candidate fields.
        role_spec_markdown: Markdown description of the role.
        screen_id: Airtable record ID for the active screen.

    Returns:
        AssessmentResult for the candidate.
    """

    workflow = create_screening_workflow()
    if workflow.session_state is None:  # pragma: no cover - defensive guard
        workflow.session_state = {}

    state = workflow.session_state

    # Extract Airtable fields (candidate_data has structure: {id: "recXXX", fields: {...}})
    fields = candidate_data.get("fields", {})

    candidate_id = (
        candidate_data.get("id")
        or candidate_data.get("record_id")
        or candidate_data.get("airtable_id")
    )
    candidate_name = (
        fields.get("Name")
        or fields.get("Full Name")
        or candidate_data.get("Full Name")
        or candidate_data.get("name")
        or "Unnamed Candidate"
    )
    current_title = (
        fields.get("Current Title")
        or fields.get("Title")
        or candidate_data.get("current_title")
        or candidate_data.get("title")
        or ""
    )
    current_company = (
        fields.get("Current Company")
        or fields.get("Company")
        or candidate_data.get("current_company")
        or candidate_data.get("company")
        or ""
    )
    linkedin_url = (
        fields.get("LinkedIn URL")
        or fields.get("LinkedIn")
        or candidate_data.get("linkedin_url")
    )

    # Use screen_id as the unique session identifier
    session_id = f"screen_{screen_id}_{candidate_id or 'unknown'}"

    state.update(
        {
            "screen_id": screen_id,
            "candidate_id": candidate_id,
            "candidate_name": candidate_name,
            "session_id": session_id,
        }
    )

    # Helper to persist session state to database
    def persist_session() -> None:
        """Save current session state to SQLite database."""
        if workflow.db:
            try:
                from agno.session.workflow import WorkflowSession

                session = WorkflowSession(
                    session_id=session_id,
                    workflow_id=workflow.id or "screening_workflow",
                    workflow_name=workflow.name,
                    session_data=state.copy(),
                )
                workflow.db.upsert_session(session)
                logger.debug("💾 Session persisted: %s", session_id)
            except Exception as e:
                logger.warning("Failed to persist session: %s", e)

    try:
        # Persist initial session state
        persist_session()

        logger.info(
            "🔍 Starting deep research for %s (%s at %s)",
            candidate_name,
            current_title or "Title Unknown",
            current_company or "Company Unknown",
        )
        research = run_research(
            candidate_name=candidate_name,
            current_title=current_title or "Unknown",
            current_company=current_company or "Unknown",
            linkedin_url=linkedin_url,
        )
        state["last_step"] = "deep_research"
        state["research_citations_count"] = len(research.citations)
        persist_session()
        logger.info(
            "✅ Deep research completed for %s with %d citations",
            candidate_name,
            len(research.citations),
        )

        logger.info("🔍 Checking research quality for %s", candidate_name)
        quality_ok = check_research_quality(research)
        state["last_step"] = "quality_check"
        state["quality_gate_triggered"] = not quality_ok
        persist_session()

        working_research = research
        if quality_ok:
            logger.info("✅ Research quality threshold met for %s", candidate_name)
        else:
            logger.info(
                "🔄 Quality gate failed for %s (citations=%d). Running incremental search.",
                candidate_name,
                len(research.citations),
            )
            working_research = run_incremental_search(
                candidate_name=candidate_name,
                initial_research=research,
                quality_gaps=research.gaps,
                role_spec_markdown=role_spec_markdown,
            )
            state["last_step"] = "incremental_search"
            state["incremental_citations_count"] = len(working_research.citations)
            persist_session()
            logger.info(
                "✅ Incremental search merged for %s. Citations now %d",
                candidate_name,
                len(working_research.citations),
            )

        logger.info("🔍 Starting assessment for %s", candidate_name)
        assessment = assess_candidate(
            research=working_research,
            role_spec_markdown=role_spec_markdown,
        )
        state["last_step"] = "assessment"
        state["overall_score"] = assessment.overall_score
        persist_session()
        logger.info(
            "✅ Assessment complete for %s (overall_score=%s)",
            candidate_name,
            assessment.overall_score,
        )
        return assessment
    except Exception as exc:  # pragma: no cover - runtime defensive path
        state["last_error"] = str(exc)
        persist_session()
        logger.error("❌ Workflow failed for %s: %s", candidate_name, exc)
        raise


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


def _extract_citation_dicts(result: Any) -> list[dict[str, str]]:
    """Normalize citations emitted by the Deep Research API."""

    sources: list[Any] = []
    if hasattr(result, "citations") and result.citations:
        sources.append(result.citations)

    messages = getattr(result, "messages", None)
    if isinstance(messages, (list, tuple)) and messages:
        last_message = messages[-1]
        last_citations = getattr(last_message, "citations", None)
        if last_citations:
            sources.append(last_citations)

    normalized: list[dict[str, str]] = []
    seen: set[str] = set()

    for source in sources:
        if hasattr(source, "urls") and getattr(source, "urls") is not None:
            items = list(source.urls)
        elif isinstance(source, (list, tuple)):
            items = list(source)
        else:
            items = [source]

        for item in items:
            citation_dict = _coerce_citation_like(item)
            url = citation_dict.get("url", "").strip()
            title = citation_dict.get("title", "").strip()
            snippet = citation_dict.get("snippet", "").strip()
            key = url or f"{title}:{snippet}"
            if not key or key in seen:
                continue
            seen.add(key)
            normalized.append(
                {
                    "url": url,
                    "title": title or url or "Unknown Source",
                    "snippet": snippet,
                }
            )

    return normalized


def _coerce_citation_like(item: Any) -> dict[str, str]:
    """Convert an arbitrary citation-like object into a simple dict."""

    if isinstance(item, Citation):
        return {
            "url": item.url,
            "title": item.title,
            "snippet": item.snippet,
        }

    if isinstance(item, dict):
        return {
            "url": str(item.get("url", "")),
            "title": str(item.get("title", "")),
            "snippet": str(
                item.get("snippet") or item.get("text") or item.get("quote") or ""
            ),
        }

    url = str(getattr(item, "url", ""))
    title = str(getattr(item, "title", ""))
    snippet = str(
        getattr(item, "snippet", "")
        or getattr(item, "text", "")
        or getattr(item, "quote", "")
    )

    return {
        "url": url,
        "title": title,
        "snippet": snippet,
    }


def _convert_dicts_to_citations(citation_dicts: list[dict[str, str]]) -> list[Citation]:
    """Convert normalized citation dicts into Citation models."""

    converted: list[Citation] = []
    seen_urls: set[str] = set()

    for data in citation_dicts:
        url = data.get("url", "").strip()
        title = data.get("title", "").strip() or url or "Unknown Source"
        snippet = data.get("snippet", "")
        if url and url in seen_urls:
            continue
        converted.append(
            Citation(
                url=url,
                title=title,
                snippet=snippet,
                relevance_note=None,
            )
        )
        if url:
            seen_urls.add(url)

    return converted


def _merge_citation_models(
    primary: Optional[list[Citation]], supplemental: list[Citation]
) -> list[Citation]:
    """Merge two citation lists while preserving order and removing duplicates."""

    merged = list(primary or [])
    seen_urls = {citation.url for citation in merged if citation.url}

    for citation in supplemental:
        if citation.url and citation.url in seen_urls:
            continue
        merged.append(citation)
        if citation.url:
            seen_urls.add(citation.url)

    return merged


def _build_parser_prompt(
    candidate_name: str,
    current_title: str,
    current_company: str,
    research_markdown: str,
    citations: list[dict[str, str]],
) -> str:
    """Create instructions for the parser agent."""

    citations_block = json.dumps(citations, indent=2) if citations else "[]"
    markdown_block = research_markdown.strip() or "(no research markdown provided)"

    return (
        f"Candidate: {candidate_name}\n"
        f"Current Role: {current_title} at {current_company}\n\n"
        "You are a parser that converts Deep Research markdown into the "
        "ExecutiveResearchResult schema. Extract structured data, preserve "
        "citations, and list explicit gaps when information is missing."
        "\n\nRESEARCH MARKDOWN:\n"
        f"{markdown_block}\n\nCITATIONS:\n{citations_block}"
    ).strip()


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


def _merge_unique_strings(first: list[str], second: list[str]) -> list[str]:
    """Return merged list of unique non-empty strings preserving order."""

    seen = []
    for value in [*first, *second]:
        normalized = value.strip()
        if normalized and normalized not in seen:
            seen.append(normalized)
    return seen


def _merge_markdown_content(primary: str, secondary: Optional[str]) -> str:
    """Combine markdown sections while preserving readable separation."""

    blocks = [primary.strip()] if primary and primary.strip() else []
    if secondary and secondary.strip():
        blocks.append(secondary.strip())

    return "\n\n".join(blocks).strip()


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
