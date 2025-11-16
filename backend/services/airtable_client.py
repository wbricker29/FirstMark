"""
Airtable Client - Interface for reading/writing Airtable data

Provides clean abstraction for all Airtable operations
"""
import os
import logging
from typing import List, Dict, Any, Optional
from pyairtable import Api
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)


class AirtableClient:
    """
    Client for Airtable operations

    Tables:
    - Companies
    - Roles
    - Candidates
    - Assessments
    """

    def __init__(self):
        api_key = os.getenv("AIRTABLE_API_KEY")
        base_id = os.getenv("AIRTABLE_BASE_ID")

        if not api_key or not base_id:
            raise ValueError("AIRTABLE_API_KEY and AIRTABLE_BASE_ID must be set")

        self.api = Api(api_key)
        self.base = self.api.base(base_id)

        # Table references
        self.companies_table = self.base.table("Companies")
        self.roles_table = self.base.table("Roles")
        self.candidates_table = self.base.table("Candidates")
        self.assessments_table = self.base.table("Assessments")

        logger.info("AirtableClient initialized")

    # ==================== ROLES ====================

    def get_role(self, role_id: str) -> Dict[str, Any]:
        """
        Get role by ID

        Args:
            role_id: Airtable record ID

        Returns:
            Role data dict
        """
        record = self.roles_table.get(role_id)
        return self._format_role(record)

    def get_all_roles(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get all roles, optionally filtered by status

        Args:
            status: Optional status filter

        Returns:
            List of role dicts
        """
        formula = f"{{Status}} = '{status}'" if status else None
        records = self.roles_table.all(formula=formula)
        return [self._format_role(r) for r in records]

    def update_role(self, role_id: str, fields: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update role fields

        Args:
            role_id: Airtable record ID
            fields: Fields to update

        Returns:
            Updated role data
        """
        record = self.roles_table.update(role_id, fields)
        return self._format_role(record)

    def _format_role(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Format Airtable role record to standard dict"""
        fields = record.get("fields", {})
        return {
            "id": record.get("id", ""),
            "title": fields.get("Title", ""),
            "company": fields.get("Company", []),  # Link to Companies
            "raw_description": fields.get("Raw Description", ""),
            "generated_spec": fields.get("Generated Spec", ""),
            "required_skills": fields.get("Required Skills", []),
            "status": fields.get("Status", "Draft")
        }

    # ==================== CANDIDATES ====================

    def get_candidate(self, candidate_id: str) -> Dict[str, Any]:
        """
        Get candidate by ID

        Args:
            candidate_id: Airtable record ID

        Returns:
            Candidate data dict
        """
        record = self.candidates_table.get(candidate_id)
        return self._format_candidate(record)

    def get_candidates_for_role(self, role_id: str) -> List[Dict[str, Any]]:
        """
        Get all candidates linked to a role

        Args:
            role_id: Role record ID

        Returns:
            List of candidate dicts
        """
        # Query assessments table to find linked candidates
        formula = f"SEARCH('{role_id}', {{Role}})"
        assessment_records = self.assessments_table.all(formula=formula)

        # Extract unique candidate IDs
        candidate_ids = set()
        for record in assessment_records:
            fields = record.get("fields", {})
            candidate_links = fields.get("Candidate", [])
            candidate_ids.update(candidate_links)

        # Fetch all candidates
        return [self.get_candidate(cid) for cid in candidate_ids]

    def get_all_candidates(self, source: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get all candidates, optionally filtered by source

        Args:
            source: Optional source filter (Portfolio, Guild, LinkedIn)

        Returns:
            List of candidate dicts
        """
        formula = f"{{Source}} = '{source}'" if source else None
        records = self.candidates_table.all(formula=formula)
        return [self._format_candidate(r) for r in records]

    def _format_candidate(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Format Airtable candidate record to standard dict"""
        fields = record.get("fields", {})
        return {
            "id": record.get("id", ""),
            "name": fields.get("Name", ""),
            "current_title": fields.get("Current Title", ""),
            "linkedin_url": fields.get("LinkedIn URL", ""),
            "bio": fields.get("Bio", ""),
            "skills": fields.get("Skills", []),
            "source": fields.get("Source", "")
        }

    # ==================== ASSESSMENTS ====================

    def get_assessment(self, assessment_id: str) -> Dict[str, Any]:
        """Get assessment by ID"""
        record = self.assessments_table.get(assessment_id)
        return self._format_assessment(record)

    def get_assessments_for_role(self, role_id: str) -> List[Dict[str, Any]]:
        """Get all assessments for a role"""
        formula = f"SEARCH('{role_id}', {{Role}})"
        records = self.assessments_table.all(formula=formula)
        return [self._format_assessment(r) for r in records]

    def write_assessments(
        self,
        role_id: str,
        assessments: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Write or update assessment records

        Args:
            role_id: Role record ID
            assessments: List of assessment dicts

        Returns:
            List of created/updated records
        """
        results = []

        for assessment in assessments:
            # Check if assessment already exists
            candidate_id = assessment.get("candidate_id", "")
            formula = f"AND(SEARCH('{role_id}', {{Role}}), SEARCH('{candidate_id}', {{Candidate}}))"
            existing = self.assessments_table.all(formula=formula)

            fields = {
                "Role": [role_id],
                "Candidate": [candidate_id],
                "Research Summary": assessment.get("reasoning", {}).get("overall", ""),
                "Technical Score": assessment.get("scores", {}).get("technical", 0),
                "Culture Score": assessment.get("scores", {}).get("culture", 0),
                "Overall Score": assessment.get("scores", {}).get("overall", 0),
                "Reasoning": assessment.get("ranking_reasoning", ""),
                "Rank": assessment.get("rank", 0),
                "Status": "Complete"
            }

            if existing:
                # Update existing
                record = self.assessments_table.update(existing[0]["id"], fields)
            else:
                # Create new
                record = self.assessments_table.create(fields)

            results.append(self._format_assessment(record))

        return results

    def _format_assessment(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Format Airtable assessment record to standard dict"""
        fields = record.get("fields", {})
        return {
            "id": record.get("id", ""),
            "role": fields.get("Role", []),
            "candidate": fields.get("Candidate", []),
            "research_summary": fields.get("Research Summary", ""),
            "technical_score": fields.get("Technical Score", 0),
            "culture_score": fields.get("Culture Score", 0),
            "overall_score": fields.get("Overall Score", 0),
            "reasoning": fields.get("Reasoning", ""),
            "rank": fields.get("Rank", 0),
            "status": fields.get("Status", "Pending")
        }

    # ==================== COMPANIES ====================

    def get_company(self, company_id: str) -> Dict[str, Any]:
        """Get company by ID"""
        record = self.companies_table.get(company_id)
        return self._format_company(record)

    def _format_company(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Format Airtable company record to standard dict"""
        fields = record.get("fields", {})
        return {
            "id": record.get("id", ""),
            "name": fields.get("Name", ""),
            "description": fields.get("Description", ""),
            "industry": fields.get("Industry", ""),
            "stage": fields.get("Stage", ""),
            "status": fields.get("Status", "Active")
        }
