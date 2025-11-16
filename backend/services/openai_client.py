"""
OpenAI Client - Interface for OpenAI API operations

Provides methods for:
- Deep Research API
- Structured assessments
- Role spec generation
"""
import os
import json
import logging
from typing import Dict, Any
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)


class OpenAIClient:
    """
    Client for OpenAI API operations

    Handles:
    - Deep Research API for candidate research
    - GPT-4 for structured assessments
    - Role specification generation
    """

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY must be set")

        self.client = AsyncOpenAI(api_key=api_key)
        self.model = "gpt-4-turbo-preview"  # Update to latest model
        logger.info("OpenAIClient initialized")

    async def deep_research(self, query: str) -> Dict[str, Any]:
        """
        Use OpenAI Deep Research API to research a candidate

        Args:
            query: Research query

        Returns:
            Dict with summary, findings, and sources
        """
        logger.info(f"Running deep research: {query[:100]}...")

        # NOTE: This is a placeholder implementation
        # The actual Deep Research API is not publicly available yet
        # For demo, we'll use GPT-4 with web search capabilities

        try:
            # Using GPT-4 with extended context for comprehensive research
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": """You are a professional executive researcher.
                        Provide comprehensive research summaries about candidates.
                        Include: career history, technical expertise, leadership experience, notable achievements.
                        Be thorough and specific."""
                    },
                    {
                        "role": "user",
                        "content": query
                    }
                ],
                temperature=0.3,
                max_tokens=2000
            )

            summary = response.choices[0].message.content

            return {
                "summary": summary,
                "sources": [
                    # In production, these would be real sources from Deep Research API
                    {"title": "LinkedIn Profile", "url": "https://linkedin.com"},
                    {"title": "Company Website", "url": "https://example.com"}
                ],
                "raw_response": summary
            }

        except Exception as e:
            logger.error(f"Deep research failed: {str(e)}")
            raise

    async def structured_assessment(self, prompt: str) -> Dict[str, Any]:
        """
        Run structured assessment using GPT-4

        Args:
            prompt: Assessment prompt

        Returns:
            Dict with structured assessment results
        """
        logger.info("Running structured assessment...")

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert executive recruiter. Provide detailed, honest assessments."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )

            result = json.loads(response.choices[0].message.content)
            return result

        except Exception as e:
            logger.error(f"Structured assessment failed: {str(e)}")
            raise

    async def generate_role_spec(self, raw_description: str) -> Dict[str, Any]:
        """
        Generate structured role specification from raw job description

        Args:
            raw_description: Unstructured job description

        Returns:
            Dict with structured role spec
        """
        logger.info("Generating role specification...")

        prompt = f"""Extract a structured role specification from this job description:

{raw_description}

Provide the following in JSON format:
{{
  "spec": "<comprehensive role specification>",
  "skills": ["skill1", "skill2", ...],
  "responsibilities": ["resp1", "resp2", ...],
  "qualifications": ["qual1", "qual2", ...],
  "experience_years": <number>,
  "seniority_level": "<junior|mid|senior|executive>"
}}
"""

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at parsing job descriptions into structured specifications."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.2,
                response_format={"type": "json_object"}
            )

            result = json.loads(response.choices[0].message.content)
            return result

        except Exception as e:
            logger.error(f"Role spec generation failed: {str(e)}")
            raise
