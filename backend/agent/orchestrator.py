"""
Multi-Agent Orchestrator for Talent Signal Agent

Coordinates research, assessment, and ranking agents to match
candidates to roles.
"""
import asyncio
from typing import List, Optional, Dict, Any
import logging

from services.airtable_client import AirtableClient
from services.openai_client import OpenAIClient
from agent.researcher import ResearchAgent
from agent.assessor import AssessmentAgent
from agent.ranker import RankingAgent

logger = logging.getLogger(__name__)


class TalentOrchestrator:
    """
    Main orchestrator for talent matching workflows

    Implements multi-agent pattern:
    - Research Agent: Gathers candidate information
    - Assessment Agent: Evaluates candidate fit
    - Ranking Agent: Ranks candidates and generates final recommendations
    """

    def __init__(self):
        # Initialize service clients
        self.airtable = AirtableClient()
        self.openai = OpenAIClient()

        # Initialize agents
        self.researcher = ResearchAgent(openai_client=self.openai)
        self.assessor = AssessmentAgent(openai_client=self.openai)
        self.ranker = RankingAgent()

        logger.info("TalentOrchestrator initialized")

    async def assess_role(
        self,
        role_id: str,
        candidate_ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Run complete assessment workflow for a role

        Steps:
        1. Fetch role details from Airtable
        2. Get candidates (all linked or specified subset)
        3. Research each candidate in parallel
        4. Run assessment for each candidate
        5. Rank all candidates
        6. Write results to Airtable
        7. Return ranked results

        Args:
            role_id: Airtable record ID for the role
            candidate_ids: Optional list of specific candidates to assess

        Returns:
            Dict with role info and ranked assessments
        """
        logger.info(f"Starting assessment workflow for role: {role_id}")

        # Step 1: Fetch role from Airtable
        role = self.airtable.get_role(role_id)
        logger.info(f"Role: {role['title']}")

        # Step 2: Get candidates
        if candidate_ids:
            candidates = [self.airtable.get_candidate(cid) for cid in candidate_ids]
        else:
            candidates = self.airtable.get_candidates_for_role(role_id)

        logger.info(f"Assessing {len(candidates)} candidates")

        # Step 3: Research candidates in parallel
        logger.info("Phase 1: Researching candidates...")
        research_tasks = [
            self.researcher.research_candidate(
                candidate=candidate,
                role_context=role
            )
            for candidate in candidates
        ]
        research_results = await asyncio.gather(*research_tasks)

        # Step 4: Assess each candidate
        logger.info("Phase 2: Assessing candidates...")
        assessment_tasks = [
            self.assessor.assess_candidate(
                candidate=candidates[i],
                role=role,
                research=research_results[i]
            )
            for i in range(len(candidates))
        ]
        assessments = await asyncio.gather(*assessment_tasks)

        # Step 5: Rank candidates
        logger.info("Phase 3: Ranking candidates...")
        ranked_assessments = self.ranker.rank_candidates(
            assessments=assessments,
            role=role
        )

        # Step 6: Write results to Airtable
        logger.info("Writing results to Airtable...")
        self.airtable.write_assessments(
            role_id=role_id,
            assessments=ranked_assessments
        )

        # Step 7: Return results
        return {
            "role_id": role_id,
            "role_title": role["title"],
            "assessments": ranked_assessments,
            "total_candidates": len(candidates)
        }

    async def generate_role_spec(self, role_id: str) -> Dict[str, Any]:
        """
        Generate structured role specification from raw job description

        Uses LLM to extract structured requirements from unstructured text

        Args:
            role_id: Airtable record ID for the role

        Returns:
            Dict with generated role specification
        """
        logger.info(f"Generating role spec for: {role_id}")

        # Fetch role from Airtable
        role = self.airtable.get_role(role_id)
        raw_description = role.get("raw_description", "")

        # Generate structured spec using LLM
        role_spec = await self.openai.generate_role_spec(raw_description)

        # Update Airtable with generated spec
        self.airtable.update_role(
            role_id=role_id,
            fields={
                "generated_spec": role_spec["spec"],
                "required_skills": role_spec["skills"],
                "status": "Spec Generated"
            }
        )

        logger.info(f"Role spec generated and saved for: {role_id}")

        return {
            "role_id": role_id,
            "role_title": role["title"],
            "spec": role_spec
        }

    async def ingest_data(self, source: str, table: str) -> Dict[str, Any]:
        """
        Ingest data from various sources into Airtable

        Args:
            source: Data source type ("csv", "airtable_attachment")
            table: Target table name

        Returns:
            Dict with ingestion results
        """
        logger.info(f"Ingesting {source} data to {table}")

        # This is a placeholder - implement based on actual data sources
        # For MVP, this could be a simple CSV parser

        return {
            "status": "success",
            "records_processed": 0,
            "source": source,
            "table": table
        }

    async def research_candidate(
        self,
        candidate_id: str,
        role_context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Research a single candidate independently

        Args:
            candidate_id: Airtable record ID for candidate
            role_context: Optional role context for focused research

        Returns:
            Dict with research results
        """
        logger.info(f"Researching candidate: {candidate_id}")

        candidate = self.airtable.get_candidate(candidate_id)

        research = await self.researcher.research_candidate(
            candidate=candidate,
            role_context=role_context
        )

        return {
            "candidate_id": candidate_id,
            "candidate_name": candidate["name"],
            "research": research
        }
