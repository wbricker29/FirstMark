"""
Assessment Agent - Evaluates candidate fit for roles

Uses structured LLM prompts to evaluate candidates based on:
- Technical skills match
- Experience level
- Culture fit
- Leadership qualities
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class AssessmentAgent:
    """
    Agent responsible for assessing candidate-role fit

    Uses GPT-4 with structured prompts to evaluate candidates
    across multiple dimensions
    """

    def __init__(self, openai_client):
        self.openai = openai_client
        logger.info("AssessmentAgent initialized")

    async def assess_candidate(
        self,
        candidate: Dict[str, Any],
        role: Dict[str, Any],
        research: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Assess a candidate's fit for a specific role

        Args:
            candidate: Candidate data from Airtable
            role: Role data from Airtable
            research: Research results from ResearchAgent

        Returns:
            Dict with scores, reasoning, and recommendations
        """
        candidate_name = candidate.get("name", "Unknown")
        role_title = role.get("title", "Unknown")

        logger.info(f"Assessing {candidate_name} for {role_title}")

        # Build assessment prompt
        prompt = self._build_assessment_prompt(candidate, role, research)

        # Run LLM assessment
        assessment_result = await self.openai.structured_assessment(prompt)

        # Parse and structure results
        assessment = self._parse_assessment(assessment_result, candidate, role)

        return assessment

    def _build_assessment_prompt(
        self,
        candidate: Dict[str, Any],
        role: Dict[str, Any],
        research: Dict[str, Any]
    ) -> str:
        """
        Build structured assessment prompt

        Args:
            candidate: Candidate data
            role: Role data
            research: Research results

        Returns:
            Assessment prompt string
        """
        candidate_name = candidate.get("name", "Unknown")
        role_title = role.get("title", "Unknown")
        role_spec = role.get("generated_spec", role.get("raw_description", ""))

        prompt = f"""You are an expert executive recruiter evaluating candidates for venture-backed startups.

ROLE: {role_title}

ROLE REQUIREMENTS:
{role_spec}

CANDIDATE: {candidate_name}

CANDIDATE RESEARCH SUMMARY:
{research.get('summary', 'No research available')}

KEY FINDINGS:
{self._format_findings(research.get('key_findings', {}))}

EVALUATION TASK:
Assess this candidate's fit for the role across the following dimensions:

1. TECHNICAL SKILLS (0-100):
   - Do they have the required technical expertise?
   - Relevant technologies, frameworks, systems?

2. EXPERIENCE LEVEL (0-100):
   - Years of relevant experience
   - Career progression
   - Similar role experience

3. LEADERSHIP (0-100):
   - Team management experience
   - Strategic vision
   - Execution track record

4. CULTURE FIT (0-100):
   - Startup experience
   - Adaptability
   - Alignment with company values

5. OVERALL FIT (0-100):
   - Holistic assessment
   - Probability of success

REQUIRED OUTPUT FORMAT:
Provide scores and detailed reasoning for each dimension.
Be specific and cite evidence from the research.
Highlight both strengths and potential concerns.

Output as JSON:
{{
  "technical_score": <0-100>,
  "experience_score": <0-100>,
  "leadership_score": <0-100>,
  "culture_score": <0-100>,
  "overall_score": <0-100>,
  "reasoning": {{
    "technical": "<specific reasoning>",
    "experience": "<specific reasoning>",
    "leadership": "<specific reasoning>",
    "culture": "<specific reasoning>",
    "overall": "<holistic assessment>"
  }},
  "strengths": ["<strength 1>", "<strength 2>", ...],
  "concerns": ["<concern 1>", "<concern 2>", ...],
  "recommendation": "strong_fit|moderate_fit|weak_fit"
}}
"""
        return prompt

    def _format_findings(self, findings: Dict[str, Any]) -> str:
        """Format research findings for prompt"""
        if not findings:
            return "No structured findings available"

        sections = []
        for key, items in findings.items():
            if items:
                section_title = key.replace("_", " ").title()
                items_str = "\n".join([f"  - {item}" for item in items])
                sections.append(f"{section_title}:\n{items_str}")

        return "\n\n".join(sections) if sections else "No structured findings available"

    def _parse_assessment(
        self,
        assessment_result: Dict[str, Any],
        candidate: Dict[str, Any],
        role: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Parse and structure assessment results

        Args:
            assessment_result: Raw LLM output
            candidate: Candidate data
            role: Role data

        Returns:
            Structured assessment
        """
        return {
            "candidate_id": candidate.get("id", ""),
            "candidate_name": candidate.get("name", ""),
            "role_id": role.get("id", ""),
            "role_title": role.get("title", ""),
            "scores": {
                "technical": assessment_result.get("technical_score", 0),
                "experience": assessment_result.get("experience_score", 0),
                "leadership": assessment_result.get("leadership_score", 0),
                "culture": assessment_result.get("culture_score", 0),
                "overall": assessment_result.get("overall_score", 0)
            },
            "reasoning": assessment_result.get("reasoning", {}),
            "strengths": assessment_result.get("strengths", []),
            "concerns": assessment_result.get("concerns", []),
            "recommendation": assessment_result.get("recommendation", "unknown")
        }
