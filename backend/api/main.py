"""
FastAPI server for FirstMark Talent Signal Agent
Provides endpoints for multi-agent talent matching workflows
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import logging

from agent.orchestrator import TalentOrchestrator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="FirstMark Talent Signal Agent",
    description="Multi-agent system for matching executives to portfolio roles",
    version="0.1.0"
)

# CORS middleware for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize orchestrator
orchestrator = TalentOrchestrator()


# Request/Response Models
class AssessRoleRequest(BaseModel):
    role_id: str
    candidate_ids: Optional[List[str]] = None  # If None, assess all linked candidates


class AssessmentResult(BaseModel):
    candidate_id: str
    candidate_name: str
    overall_score: float
    technical_score: float
    culture_score: float
    reasoning: str
    rank: int


class AssessRoleResponse(BaseModel):
    role_id: str
    role_title: str
    assessments: List[AssessmentResult]
    total_candidates: int


class GenerateRoleSpecRequest(BaseModel):
    role_id: str


class IngestDataRequest(BaseModel):
    data_source: str  # "csv" or "airtable_attachment"
    table_name: str  # "companies", "candidates", etc.


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "talent-signal-agent"}


# Main workflow endpoints
@app.post("/assess-role", response_model=AssessRoleResponse)
async def assess_role(request: AssessRoleRequest):
    """
    Run multi-agent assessment workflow for a role

    This endpoint:
    1. Fetches role details and candidates from Airtable
    2. Runs parallel research on each candidate
    3. Evaluates candidates using LLM assessment agents
    4. Ranks candidates and generates reasoning trails
    5. Writes results back to Airtable
    """
    try:
        logger.info(f"Starting assessment for role: {request.role_id}")

        result = await orchestrator.assess_role(
            role_id=request.role_id,
            candidate_ids=request.candidate_ids
        )

        logger.info(f"Assessment complete for role: {request.role_id}")
        return result

    except Exception as e:
        logger.error(f"Assessment failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate-role-spec")
async def generate_role_spec(request: GenerateRoleSpecRequest):
    """
    Generate structured role specification from raw job description

    Uses LLM to extract:
    - Required skills and experience
    - Responsibilities
    - Key qualifications
    - Culture fit requirements
    """
    try:
        logger.info(f"Generating role spec for: {request.role_id}")

        result = await orchestrator.generate_role_spec(request.role_id)

        logger.info(f"Role spec generated for: {request.role_id}")
        return result

    except Exception as e:
        logger.error(f"Role spec generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ingest-data")
async def ingest_data(request: IngestDataRequest):
    """
    Ingest and normalize data from various sources

    Supports:
    - CSV files
    - Airtable attachments
    - Direct Airtable table syncs
    """
    try:
        logger.info(f"Ingesting data from {request.data_source} to {request.table_name}")

        result = await orchestrator.ingest_data(
            source=request.data_source,
            table=request.table_name
        )

        logger.info(f"Data ingestion complete: {result['records_processed']} records")
        return result

    except Exception as e:
        logger.error(f"Data ingestion failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Research endpoint (can be called independently)
@app.post("/research-candidate")
async def research_candidate(candidate_id: str, role_context: Optional[str] = None):
    """
    Research a single candidate using OpenAI Deep Research API

    Returns comprehensive research summary with sources
    """
    try:
        logger.info(f"Researching candidate: {candidate_id}")

        result = await orchestrator.research_candidate(
            candidate_id=candidate_id,
            role_context=role_context
        )

        return result

    except Exception as e:
        logger.error(f"Candidate research failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
