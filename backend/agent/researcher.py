"""
Research Agent - Gathers information about candidates

Uses OpenAI Deep Research API to gather comprehensive information
about candidates in the context of specific roles.
"""
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class ResearchAgent:
    """
    Agent responsible for researching candidates

    Uses OpenAI Deep Research API for comprehensive candidate research
    """

    def __init__(self, openai_client):
        self.openai = openai_client
        logger.info("ResearchAgent initialized")

    async def research_candidate(
        self,
        candidate: Dict[str, Any],
        role_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Research a candidate using OpenAI Deep Research API

        Args:
            candidate: Candidate data from Airtable
            role_context: Optional role context for focused research

        Returns:
            Dict with research summary, key findings, and sources
        """
        candidate_name = candidate.get("name", "Unknown")
        logger.info(f"Researching: {candidate_name}")

        # Build research query
        query = self._build_research_query(candidate, role_context)

        # Use OpenAI Deep Research API
        research_result = await self.openai.deep_research(query)

        # Extract and structure key findings
        findings = self._extract_key_findings(research_result, role_context)

        return {
            "summary": research_result.get("summary", ""),
            "key_findings": findings,
            "sources": research_result.get("sources", []),
            "raw_research": research_result
        }

    def _build_research_query(
        self,
        candidate: Dict[str, Any],
        role_context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Build research query optimized for the role context

        Args:
            candidate: Candidate data
            role_context: Optional role context

        Returns:
            Research query string
        """
        name = candidate.get("name", "")
        current_title = candidate.get("current_title", "")
        linkedin = candidate.get("linkedin_url", "")

        # Base query
        query = f"Research {name}"

        if current_title:
            query += f", currently {current_title}"

        # Add role-specific focus if provided
        if role_context:
            role_title = role_context.get("title", "")
            required_skills = role_context.get("required_skills", [])

            query += f"\n\nContext: Evaluating for {role_title} role"

            if required_skills:
                skills_str = ", ".join(required_skills[:5])  # Top 5 skills
                query += f"\n\nFocus areas: {skills_str}"

        query += "\n\nProvide: Career history, technical expertise, leadership experience, notable achievements"

        if linkedin:
            query += f"\n\nLinkedIn: {linkedin}"

        return query

    def _extract_key_findings(
        self,
        research_result: Dict[str, Any],
        role_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Extract structured key findings from research results

        Args:
            research_result: Raw research results
            role_context: Optional role context for relevance scoring

        Returns:
            Structured key findings
        """
        # This is a placeholder - in production, you'd use LLM to extract
        # structured findings from the research summary

        return {
            "career_highlights": [],
            "technical_expertise": [],
            "leadership_experience": [],
            "relevant_achievements": [],
            "potential_concerns": []
        }
