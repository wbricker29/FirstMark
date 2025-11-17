"""
Ranking Agent - Ranks candidates and generates final recommendations

Sorts candidates by overall fit and generates reasoning trails
for top candidates.
"""
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


class RankingAgent:
    """
    Agent responsible for ranking candidates

    Takes assessment results and produces ranked candidate list
    with clear reasoning trails
    """

    def __init__(self):
        logger.info("RankingAgent initialized")

    def rank_candidates(
        self,
        assessments: List[Dict[str, Any]],
        role: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Rank candidates based on assessment scores

        Args:
            assessments: List of assessment results
            role: Role data for context

        Returns:
            Ranked list of assessments with reasoning
        """
        logger.info(f"Ranking {len(assessments)} candidates")

        # Sort by overall score (descending)
        ranked = sorted(
            assessments,
            key=lambda x: x["scores"]["overall"],
            reverse=True
        )

        # Add rank and enhanced reasoning
        for i, assessment in enumerate(ranked, start=1):
            assessment["rank"] = i
            assessment["ranking_reasoning"] = self._generate_ranking_reasoning(
                assessment=assessment,
                rank=i,
                total_candidates=len(assessments)
            )

        return ranked

    def _generate_ranking_reasoning(
        self,
        assessment: Dict[str, Any],
        rank: int,
        total_candidates: int
    ) -> str:
        """
        Generate clear reasoning for why candidate received this rank

        Args:
            assessment: Assessment data
            rank: Candidate's rank
            total_candidates: Total number of candidates

        Returns:
            Reasoning string
        """
        candidate_name = assessment.get("candidate_name", "Unknown")
        overall_score = assessment["scores"]["overall"]
        recommendation = assessment.get("recommendation", "unknown")

        # Determine tier
        if rank <= 3:
            tier = "Top Tier"
        elif rank <= total_candidates // 2:
            tier = "Strong Consideration"
        else:
            tier = "Lower Priority"

        reasoning = f"**{tier}** (Rank {rank} of {total_candidates})\n\n"
        reasoning += f"Overall Score: {overall_score}/100\n\n"

        # Add key strengths
        strengths = assessment.get("strengths", [])
        if strengths:
            reasoning += "**Key Strengths:**\n"
            for strength in strengths[:3]:  # Top 3
                reasoning += f"- {strength}\n"
            reasoning += "\n"

        # Add concerns if any
        concerns = assessment.get("concerns", [])
        if concerns:
            reasoning += "**Considerations:**\n"
            for concern in concerns[:2]:  # Top 2
                reasoning += f"- {concern}\n"
            reasoning += "\n"

        # Add recommendation
        rec_text = {
            "strong_fit": "**Recommendation:** Strongly recommended for interview",
            "moderate_fit": "**Recommendation:** Consider for interview if top candidates decline",
            "weak_fit": "**Recommendation:** Not recommended at this time"
        }.get(recommendation, "**Recommendation:** Further evaluation needed")

        reasoning += rec_text

        return reasoning
