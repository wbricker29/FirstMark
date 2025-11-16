# FirstMark Talent Signal Agent - Backend

Multi-agent Python backend for matching executives to portfolio company roles.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        AIRTABLE                              │
│  Data Layer: Companies, Roles, Candidates, Assessments      │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ↓ Trigger via N8n webhook
┌─────────────────────────────────────────────────────────────┐
│              PYTHON BACKEND (FastAPI)                        │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │         Multi-Agent Orchestrator                       │ │
│  │                                                         │ │
│  │  Research → Assessment → Ranking → Airtable Update     │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Components

### 1. Multi-Agent System (`/agent`)

**TalentOrchestrator** (`orchestrator.py`)
- Main coordinator for all workflows
- Manages agent communication and data flow

**ResearchAgent** (`researcher.py`)
- Uses OpenAI Deep Research API
- Gathers comprehensive candidate information
- Runs in parallel for multiple candidates

**AssessmentAgent** (`assessor.py`)
- Evaluates candidates using structured LLM prompts
- Scores: Technical, Experience, Leadership, Culture, Overall
- Generates detailed reasoning for each dimension

**RankingAgent** (`ranker.py`)
- Ranks candidates by overall fit
- Generates clear reasoning trails
- Creates final recommendations

### 2. Service Clients (`/services`)

**AirtableClient** (`airtable_client.py`)
- Read/write operations for all Airtable tables
- Clean abstraction over pyairtable library
- Handles record formatting and relationships

**OpenAIClient** (`openai_client.py`)
- Deep Research API integration
- Structured assessments with GPT-4
- Role specification generation

### 3. FastAPI Server (`/api`)

**main.py**
- REST API endpoints for all workflows
- `/assess-role` - Run complete assessment workflow
- `/generate-role-spec` - Generate role specification
- `/research-candidate` - Research single candidate
- `/ingest-data` - Data ingestion endpoint

## Setup

### 1. Install Dependencies

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your API keys:
# - OPENAI_API_KEY
# - AIRTABLE_API_KEY
# - AIRTABLE_BASE_ID
```

### 3. Run Server

```bash
# Development mode
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

Server will be available at `http://localhost:8000`

API docs: `http://localhost:8000/docs`

## Usage

### Assess Candidates for a Role

**Endpoint:** `POST /assess-role`

```bash
curl -X POST http://localhost:8000/assess-role \
  -H "Content-Type: application/json" \
  -d '{
    "role_id": "rec123456",
    "candidate_ids": ["recABC", "recDEF"]  # Optional
  }'
```

**Response:**
```json
{
  "role_id": "rec123456",
  "role_title": "CTO - AI Infrastructure Startup",
  "assessments": [
    {
      "candidate_id": "recABC",
      "candidate_name": "Jane Smith",
      "overall_score": 87,
      "technical_score": 92,
      "culture_score": 85,
      "reasoning": "Strong technical background...",
      "rank": 1
    }
  ],
  "total_candidates": 2
}
```

### Generate Role Specification

**Endpoint:** `POST /generate-role-spec`

```bash
curl -X POST http://localhost:8000/generate-role-spec \
  -H "Content-Type: application/json" \
  -d '{"role_id": "rec123456"}'
```

### Research Single Candidate

**Endpoint:** `POST /research-candidate`

```bash
curl -X POST http://localhost:8000/research-candidate \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_id": "recABC",
    "role_context": "CTO role requiring AI/ML expertise"
  }'
```

## Workflow Example

### Complete Assessment Workflow

1. **User clicks "Run Assessment" button in Airtable**
2. **Airtable Automation** → Sends webhook to N8n
3. **N8n** → Calls `POST /assess-role`
4. **Python Backend**:
   - Fetches role and candidates from Airtable
   - Researches all candidates in parallel (ResearchAgent)
   - Assesses each candidate (AssessmentAgent)
   - Ranks candidates (RankingAgent)
   - Writes results back to Airtable
5. **User sees results** in Airtable Assessments table

## Integration with N8n

N8n workflows call these endpoints via HTTP Request nodes:

**N8n Workflow: "Assess Candidates"**
```
1. Webhook Trigger (from Airtable)
2. HTTP Request → POST localhost:8000/assess-role
3. Wait for Response
4. (Optional) Update Airtable status
```

## Multi-Agent Workflow Details

### Parallel Research Phase

```python
# ResearchAgent runs in parallel for all candidates
research_tasks = [
    researcher.research_candidate(candidate, role)
    for candidate in candidates
]
research_results = await asyncio.gather(*research_tasks)
```

### Sequential Assessment Phase

```python
# AssessmentAgent evaluates each candidate
assessment_tasks = [
    assessor.assess_candidate(candidate, role, research)
    for candidate, research in zip(candidates, research_results)
]
assessments = await asyncio.gather(*assessment_tasks)
```

### Ranking Phase

```python
# RankingAgent sorts and adds reasoning
ranked = ranker.rank_candidates(assessments, role)
```

## Directory Structure

```
backend/
├── agent/                  # Multi-agent system
│   ├── __init__.py
│   ├── orchestrator.py    # Main coordinator
│   ├── researcher.py      # Research agent
│   ├── assessor.py        # Assessment agent
│   └── ranker.py          # Ranking agent
├── api/                   # FastAPI server
│   ├── __init__.py
│   └── main.py           # API endpoints
├── services/             # External service clients
│   ├── __init__.py
│   ├── airtable_client.py
│   └── openai_client.py
├── models/               # Data models (future)
│   └── __init__.py
├── utils/                # Utility functions (future)
├── requirements.txt      # Python dependencies
├── .env.example         # Environment template
└── README.md            # This file
```

## Development

### Adding New Agents

1. Create agent file in `/agent/`
2. Implement agent class with clear interface
3. Register in `orchestrator.py`
4. Update `agent/__init__.py`

### Adding New Endpoints

1. Add endpoint in `api/main.py`
2. Add Pydantic models for request/response
3. Call orchestrator methods
4. Update API documentation

## Deployment Options

### Option 1: Railway (Recommended for Production)

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

### Option 2: Local Development

```bash
# Run server locally (recommended for demo)
uvicorn api.main:app --reload --port 8000
```

### Option 3: Docker

```dockerfile
# Future: Add Dockerfile for containerized deployment
```

## Testing

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests (future)
pytest
```

## Next Steps

1. **Set up Airtable base** with required tables
2. **Configure N8n workflows** to trigger Python endpoints
3. **Test end-to-end** with sample data
4. **Deploy to Railway** (optional, for persistent hosting)

## Troubleshooting

**Issue: Import errors**
```bash
# Make sure you're in the backend directory and venv is activated
cd /home/user/FirstMark/backend
source venv/bin/activate
export PYTHONPATH="${PYTHONPATH}:/home/user/FirstMark/backend"
```

**Issue: Airtable connection fails**
- Check `AIRTABLE_API_KEY` and `AIRTABLE_BASE_ID` in `.env`
- Verify table names match exactly (case-sensitive)

**Issue: OpenAI API errors**
- Check `OPENAI_API_KEY` in `.env`
- Verify API key has sufficient credits
- Check rate limits

## Support

For questions about this implementation, contact Will Bricker.
