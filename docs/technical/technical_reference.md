# Talent Signal Agent: Technical Reference

## Overview

This technical reference provides comprehensive documentation for developers, DevOps engineers, and technical stakeholders working with the Talent Signal Agent. It covers system architecture, API specifications, data models, deployment procedures, and operational guidelines.

## System Architecture

### High-Level Architecture

```
┌─────────────────────┐
│  Airtable Base      │
│  (Data Layer)       │
│  - Screens          │
│  - Candidates       │
│  - Role Specs       │
│  - Assessments      │
└──────────┬──────────┘
           │
           │ Webhook POST
           │ (Structured Payload)
           ▼
┌─────────────────────┐
│  ngrok Tunnel       │
│  (Dev Only)         │
└──────────┬──────────┘
           │
           │ HTTPS
           ▼
┌─────────────────────┐
│  AgentOS Runtime    │
│  (FastAPI Server)   │
│  - /screen endpoint │
│  - Session mgmt     │
│  - Auth (optional)  │
└──────────┬──────────┘
           │
           │ Workflow Execution
           ▼
┌─────────────────────┐
│  Workflow Layer     │
│  - Deep Research    │
│  - Quality Gate     │
│  - Inc. Search      │
│  - Assessment       │
└──────────┬──────────┘
           │
           │ API Calls
           ▼
┌─────────────────────┐
│  OpenAI API         │
│  - o4-mini-deep     │
│  - gpt-5-mini       │
│  - gpt-5            │
└─────────────────────┘
           │
           ▼
┌─────────────────────┐
│  SQLite Database    │
│  (Session State)    │
└─────────────────────┘
           │
           ▼
┌─────────────────────┐
│  Airtable API       │
│  (Write Results)    │
└─────────────────────┘
```

### Component Architecture

**Runtime Layer:**
- **AgentOS FastAPI Server** (`demo/agentos_app.py`): HTTP server exposing the `/screen` webhook endpoint
- **AgentOS Framework** (Agno): Workflow orchestration, session management, and monitoring
- **SQLite Session Store** (`tmp/agno_sessions.db`): Persistent session state for audit trails

**Workflow Layer:**
- **AgentOSCandidateWorkflow** (`demo/workflow.py`): Orchestrates the 4-step screening pipeline
- **Screening Service** (`demo/screening_service.py`): Shared orchestration logic and error handling

**Agent Layer:**
- **Deep Research Agent**: `o4-mini-deep-research` for comprehensive OSINT profiling
- **Research Parser Agent**: `gpt-5-mini` to structure markdown into Pydantic models
- **Incremental Search Agent**: `gpt-5` with `web_search_preview` for gap-filling
- **Assessment Agent**: `gpt-5-mini` with `ReasoningTools` for evidence-aware evaluation

**Data Layer:**
- **AirtableClient** (`demo/airtable_client.py`): Write-only client (zero read operations during execution)
- **Pydantic Models** (`demo/models.py`): Structured data validation for all payloads and outputs
- **Prompt Catalog** (`demo/prompts/catalog.yaml`): Centralized YAML-based prompt definitions

### Design Patterns

**1. Write-Only Airtable Pattern**
- All data arrives via structured webhook payloads
- Zero traversal API calls during execution
- Airtable formulas handle all read operations
- Python only writes: assessments, status updates, logs
- Performance gain: ~500ms+ latency reduction per screen

**2. Evidence-Aware Assessment**
- Explicit `None` for unknown dimensions (never 0 or NaN)
- LLM self-assessment confidence levels (High/Medium/Low)
- Citation-backed reasoning with quality gates (≥3 citations)
- Counterfactuals: "Why candidate might NOT be ideal"

**3. Quality-Gated Research**
- Heuristic check: ≥3 citations + non-empty summary
- Conditional incremental search only when quality gate fails
- Prevents infinite research loops while maintaining quality

**4. Centralized Prompt Management**
- YAML catalog (`demo/prompts/catalog.yaml`) for all agent prompts
- Code-free prompt iteration
- Dynamic placeholder substitution
- Evidence taxonomy: `[FACT]`, `[OBSERVATION]`, `[HYPOTHESIS]`

## API Reference

### Webhook Endpoint

**Endpoint:** `POST /screen`

**Authentication:**
- Optional bearer token authentication
- Enable by setting `AGENTOS_SECURITY_KEY` environment variable
- Header: `Authorization: Bearer <AGENTOS_SECURITY_KEY>`

**Request Payload:**

```json
{
  "screen_slug": {
    "screen_id": "recABC123",
    "screen_edited": "2025-11-18T20:01:46.000Z",
    "role_spec_slug": {
      "role_spec": {
        "role_spec_id": "recRS123",
        "role_spec_name": "CFO - Series B",
        "role_spec_content": "# Role Spec Markdown..."
      }
    },
    "search_slug": {
      "role": {
        "ATID": "recR123",
        "portco": "Pigment",
        "role_type": "CFO",
        "role_title": "",
        "role_description": "..."
      }
    },
    "candidate_slugs": [
      {
        "candidate": {
          "ATID": "recP1",
          "candidate_name": "Jane Doe",
          "candidate_current_title": "CFO",
          "candidate_current_company": "Acme Inc",
          "candidate_linkedin": "https://linkedin.com/in/janedoe",
          "candidate_location": "San Francisco, CA",
          "candidate_bio": "..."
        }
      }
    ]
  }
}
```

**Validation:**
- Payload validated against `ScreenWebhookPayload` Pydantic model
- Required fields: `screen_id`, `role_spec_content`, `candidate_slugs[]`
- Candidate minimum: 1 (no maximum enforced)

**Response (202 Accepted):**

```json
{
  "status": "accepted",
  "message": "Screen workflow started",
  "screen_id": "recABC123",
  "candidates_queued": 3
}
```

**Error Responses:**

```json
// 400 Bad Request - Invalid payload
{
  "error": "Validation error",
  "details": [
    {
      "loc": ["screen_slug", "candidate_slugs"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}

// 500 Internal Server Error - Workflow initialization failure
{
  "error": "Internal server error",
  "message": "Failed to initialize workflow"
}
```

**Workflow Execution:**
- Endpoint returns immediately (asynchronous processing)
- Screen status updated to "Processing" in Airtable
- Each candidate processed sequentially through 4-step workflow
- Results written to Platform-Assessments table
- Screen status updated to "Complete" when finished
- Errors logged to Operations-Automation_Log table

### Additional Endpoints

**GET /healthz**
- Simple health check endpoint for monitoring and smoke tests
- Returns: `{"status": "ok"}`
- No authentication required
- Useful for load balancer health checks and deployment verification

**GET /docs**
- OpenAPI/Swagger documentation
- Auto-generated by FastAPI
- Interactive API testing interface

**GET /config** (AgentOS)
- Runtime metadata and configuration
- Registered workflows and agents
- AgentOS control plane endpoint

**AgentOS Control Plane**
- Web UI at `https://os.agno.com`
- Real-time workflow monitoring
- Session state inspection
- Agent run history

## Data Models

### Core Pydantic Models

**ScreenWebhookPayload**
- Validates complete webhook payload structure
- Nested objects: `screen_slug` → `role_spec_slug` → `role_spec`
- Convenience properties: `screen_id`, `spec_markdown`, `role_name`, `portco_name`
- Method: `get_candidates()` returns normalized candidate dicts

**ExecutiveResearchResult**
- Structured research output from parser agent
- Fields:
  - `exec_name`, `current_role`, `current_company`
  - `career_timeline`: List of `CareerEntry` objects
  - `fundraising_experience`, `operational_finance_experience` (CFO)
  - `technical_leadership_experience`, `team_building_experience` (CTO)
  - `sector_expertise[]`, `stage_exposure[]`
  - `research_summary`, `key_achievements[]`, `notable_companies[]`
  - `citations[]`: List of `Citation` objects
  - `research_confidence`: High/Medium/Low
  - `gaps[]`: Missing information
  - Metadata: `research_timestamp`, `research_model`

**AssessmentResult**
- Structured assessment output from assessment agent
- Fields:
  - `overall_score`: 0-100 float (or `None` if insufficient evidence)
  - `overall_confidence`: High/Medium/Low
  - `dimension_scores[]`: List of `DimensionScore` objects
  - `must_haves_check[]`: List of `MustHaveCheck` objects
  - `red_flags_detected[]`, `green_flags[]`
  - `summary`: 2-3 sentence topline
  - `counterfactuals[]`: "Why NOT ideal" reasoning
  - Metadata: `assessment_timestamp`, `assessment_model`, `role_spec_used`

**DimensionScore**
- Evidence-aware dimension score (1-5 scale)
- Fields:
  - `dimension`: Name of evaluation criterion
  - `score`: 1-5 integer or `None` (NOT 0 for unknown)
  - `evidence_level`: High/Medium/Low (from role spec)
  - `confidence`: High/Medium/Low (LLM self-assessment)
  - `reasoning`: 1-3 sentence explanation
  - `evidence_quotes[]`, `citation_urls[]`

**Citation**
- Source citation from research
- Fields: `url`, `title`, `snippet`, `relevance_note`

**CareerEntry**
- Timeline entry for career history
- Fields: `company`, `role`, `start_date`, `end_date`, `key_achievements[]`

**MustHaveCheck**
- Binary requirement verification
- Fields: `requirement`, `met` (boolean), `evidence`

### Database Schema

**SQLite Session Store** (`tmp/agno_sessions.db`)

Table: `agno_sessions` (managed by Agno framework)
- `session_id`: Primary key, format `screen_{screen_id}_{candidate_id}`
- `workflow_data`: JSON blob containing session state
- `created_at`, `updated_at`: Timestamps

Session State Structure:
```json
{
  "screen_id": "recABC123",
  "candidate_id": "recP1",
  "candidate_name": "Jane Doe",
  "last_step": "assessment",
  "quality_gate_triggered": false,
  "research": { /* ExecutiveResearchResult dict */ },
  "assessment": { /* AssessmentResult dict */ }
}
```

**Airtable Schema**

See `docs/airtable_ai_spec.md` for complete schema documentation.

Key Tables:
- `Platform-Screens`: Screen records with status tracking
- `Platform-Candidates` (People): Executive profiles
- `Platform-Role_Specs`: Reusable evaluation criteria
- `Platform-Searches`: Portfolio company roles
- `Platform-Assessments`: AI-generated evaluations
- `Operations-Automation_Log`: Webhook execution logs

## Configuration

### Environment Variables

**Required:**
```bash
OPENAI_API_KEY=sk-...          # OpenAI API key
AIRTABLE_API_KEY=pat...        # Airtable personal access token
AIRTABLE_BASE_ID=app...        # Airtable base ID
```

**Optional:**
```bash
AGENTOS_SECURITY_KEY=...       # Bearer token for /screen endpoint
FASTAPI_HOST=0.0.0.0           # Server bind address (default: 0.0.0.0)
FASTAPI_PORT=5001              # Server port (default: 5001)
FASTAPI_DEBUG=true             # Debug mode (default: false)
OPENAI_TIMEOUT=300             # OpenAI API timeout in seconds (default: 300)
```

### Configuration Files

**.env**
- Environment variables
- Not checked into version control
- Use `.env.example` as template

**demo/settings.py**
- Pydantic Settings model
- Loads from environment with validation
- Provides typed configuration access

**demo/prompts/catalog.yaml**
- Centralized prompt definitions
- Agent instructions and system prompts
- Evidence taxonomy guidelines
- Dynamic placeholder support

### Prompt Customization

**Editing Prompts:**

1. Open `demo/prompts/catalog.yaml`
2. Locate the agent prompt (e.g., `deep_research`, `assessment`)
3. Edit `instructions`, `description`, or `markdown_content`
4. Save file (no code changes needed)
5. Restart AgentOS server

**Dynamic Placeholders:**

```python
from demo.prompts import get_prompt

# Load with placeholders
prompt = get_prompt("assessment", role_type="CFO", company="Pigment")

# Access as agent kwargs
agent = Agent(
    name="Assessment Agent",
    **prompt.as_agent_kwargs()
)
```

**Evidence Taxonomy:**

Prompts use structured evidence markers:
- `[FACT]`: Verifiable claims with citations
- `[OBSERVATION]`: Inferred patterns from data
- `[HYPOTHESIS]`: Reasoned speculation with caveats

## Deployment

### Local Development

**Prerequisites:**
- Python 3.11+
- uv package manager
- ngrok (for webhook testing)

**Setup:**

```bash
# 1. Clone repository
git clone <repo-url>
cd talent-signal-agent

# 2. Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 3. Create virtual environment
uv venv
source .venv/bin/activate

# 4. Install dependencies
uv pip install -e .

# 5. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 6. Run AgentOS server
uv run python demo/agentos_app.py

# 7. Start ngrok (separate terminal)
ngrok http 5001
```

**Verification:**

```bash
# Check server is running
curl http://localhost:5001/config

# View API docs
open http://localhost:5001/docs

# Test webhook (replace with your ngrok URL)
curl -X POST https://YOUR_NGROK_URL/screen \
  -H "Content-Type: application/json" \
  -d @scripts/test_payload.json
```

### Production Deployment

**Recommended Stack:**
- **Hosting:** Google Cloud Run, Heroku, or Railway
- **Database:** PostgreSQL (for AgentOS session storage)
- **Monitoring:** AgentOS Control Plane + Sentry
- **Secrets:** Google Secret Manager or similar

**Cloud Run Example:**

```bash
# 1. Build container
docker build -t gcr.io/PROJECT_ID/talent-signal-agent .

# 2. Push to Container Registry
docker push gcr.io/PROJECT_ID/talent-signal-agent

# 3. Deploy to Cloud Run
gcloud run deploy talent-signal-agent \
  --image gcr.io/PROJECT_ID/talent-signal-agent \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars "OPENAI_API_KEY=$OPENAI_API_KEY,AIRTABLE_API_KEY=$AIRTABLE_API_KEY,AIRTABLE_BASE_ID=$AIRTABLE_BASE_ID"
```

**Environment Variables (Production):**

```bash
# Required
OPENAI_API_KEY=sk-...
AIRTABLE_API_KEY=pat...
AIRTABLE_BASE_ID=app...
AGENTOS_SECURITY_KEY=<generate-random-string>

# PostgreSQL (for AgentOS)
DATABASE_URL=postgresql://user:pass@host:5432/dbname

# Monitoring
SENTRY_DSN=https://...
```

**Security Checklist:**
- [ ] Enable `AGENTOS_SECURITY_KEY` for bearer token auth
- [ ] Use HTTPS for all endpoints
- [ ] Rotate API keys regularly
- [ ] Enable request logging and monitoring
- [ ] Set up error alerting (Sentry, PagerDuty)
- [ ] Implement rate limiting on `/screen` endpoint
- [ ] Use secret management service (not plain env vars)

### Airtable Automation Setup

**Automation Script:** `scripts/airtable_webhook_automation.js`

**Configuration Steps:**

1. Open Airtable base → Automations
2. Create new automation: "Trigger Candidate Screening"
3. **Trigger:** When record matches conditions
   - Table: Platform-Screens
   - Condition: `Status` changes to "Ready to Screen"
4. **Action:** Run a script
5. Paste contents of `scripts/airtable_webhook_automation.js`
6. Update `WEBHOOK_URL` variable:
   - Dev: `https://YOUR_NGROK_URL/screen`
   - Prod: `https://your-domain.com/screen`
7. Enable automation

**Automation Features:**
- Assembles nested `screen_slug` payload
- Adds bearer token header if `AGENTOS_SECURITY_KEY` is set
- Handles errors and logs to Automation_Log table
- Sets Screen status to "Processing" before POST
- Sets Screen status to "Failed" on error

## Operations

### Monitoring

**AgentOS Control Plane:**
- URL: `https://os.agno.com`
- Features:
  - Real-time workflow execution view
  - Session state inspection
  - Agent run history
  - Performance metrics (latency, token usage)
  - Error tracking

**Application Logs:**
- Structured logging with emoji indicators:
  - 🔍 Step start
  - ✅ Step success
  - 🔄 Incremental search triggered
  - ❌ Errors
- Log levels: INFO (default), DEBUG, ERROR
- Example log:
  ```
  2025-11-19 | INFO | 🔍 Starting deep research for Jane Doe
  2025-11-19 | INFO | ✅ Deep research completed for Jane Doe with 5 citations
  ```

**Airtable Monitoring:**
- `Operations-Automation_Log` table tracks all webhook calls
- Fields: `timestamp`, `screen_id`, `status`, `error_message`, `duration`

**Metrics to Monitor:**
- Webhook response time (target: <500ms)
- Workflow execution time (target: 3-5 min/candidate)
- Error rate (target: <5%)
- OpenAI API latency
- Citation count per research (target: ≥3)

### Troubleshooting

**Issue: Webhook not triggering**

Diagnosis:
1. Check Airtable Automation → Runs tab for errors
2. Verify ngrok tunnel is active (dev) or URL is correct (prod)
3. Test endpoint directly with curl

Fix:
```bash
# Test endpoint
curl -X POST http://localhost:5001/screen \
  -H "Content-Type: application/json" \
  -d @scripts/test_payload.json

# Check AgentOS logs
tail -f logs/agentos.log
```

**Issue: Screen stuck in "Processing"**

Diagnosis:
1. Check AgentOS Control Plane for workflow status
2. Review application logs for errors
3. Check Operations-Automation_Log for error details

Fix:
- If workflow failed: Create new Screen with same candidates
- If timeout: Increase `OPENAI_TIMEOUT` env var
- If API quota: Wait for rate limit reset

**Issue: Low-quality assessments**

Diagnosis:
1. Check citation count in research (should be ≥3)
2. Review role spec for clarity
3. Verify candidate has public LinkedIn profile

Fix:
- Refine role spec with clearer criteria
- Ensure candidates have robust online presence
- Use Custom Spec to A/B test evaluation criteria

**Issue: API rate limits**

Diagnosis:
- OpenAI API returns 429 status
- Logs show "Rate limit exceeded"

Fix:
```python
# Increase retry delays in demo/agents.py
Agent(
    retries=3,  # Increase from 2
    delay_between_retries=2,  # Increase from 1
    exponential_backoff=True
)
```

**Issue: Database locked errors**

Diagnosis:
- SQLite write contention (rare in single-threaded mode)

Fix:
- Migrate to PostgreSQL for production:
  ```python
  # In demo/agentos_app.py
  from agno.storage import PostgresDb

  storage = PostgresDb(
      connection_string=os.getenv("DATABASE_URL")
  )
  ```

### Performance Optimization

**1. Reduce OpenAI API Latency**
- Use streaming responses (already enabled for Deep Research)
- Implement response caching for repeated queries
- Consider using `gpt-5-mini` instead of `gpt-5` for incremental search

**2. Optimize Workflow Execution**
- Enable parallel candidate processing (Phase 2+)
- Implement fast mode with skip logic for high-quality profiles
- Cache role spec embeddings for dimension matching

**3. Database Performance**
- Migrate to PostgreSQL for production (SQLite is dev-only)
- Add indexes on `session_id` and `screen_id`
- Implement session cleanup for old records

**4. Monitoring and Alerting**
- Set up Sentry for error tracking
- Create dashboards for key metrics (Grafana, Datadog)
- Alert on error rate >5% or latency >10 min/candidate

## Extension Points

### Adding New Agents

**Example: Add "Culture Fit" agent**

1. **Define prompt in catalog:**

```yaml
# demo/prompts/catalog.yaml
culture_fit:
  instructions: |
    Analyze the candidate's communication style, values, and work preferences.
    Evaluate cultural alignment with {company} based on research.
  description: "Culture Fit Agent"
  markdown_content: true
```

2. **Create agent factory:**

```python
# demo/agents.py
def create_culture_fit_agent() -> Agent:
    prompt = get_prompt("culture_fit")
    return Agent(
        name="Culture Fit Agent",
        model=OpenAIResponses(id="gpt-5-mini"),
        output_schema=CultureFitResult,  # Define new model
        **prompt.as_agent_kwargs()
    )
```

3. **Add to workflow:**

```python
# demo/workflow.py
def run_candidate_workflow(self, ...):
    # ... existing steps ...

    # Step 5: Culture Fit
    culture_agent = create_culture_fit_agent()
    culture_result = culture_agent.run(research_summary)

    # Merge into assessment
    assessment.culture_fit = culture_result
```

### Custom Scoring Logic

**Example: Weighted dimension scoring**

```python
# demo/screening_helpers.py
def calculate_weighted_score(
    dimension_scores: list[DimensionScore],
    weights: dict[str, float]
) -> float:
    """
    Calculate weighted average instead of simple average.

    Args:
        dimension_scores: List of dimension scores
        weights: Dict mapping dimension names to weights (0-1)

    Returns:
        Weighted score (0-100)
    """
    total_score = 0
    total_weight = 0

    for dim in dimension_scores:
        if dim.score is not None and dim.dimension in weights:
            weight = weights[dim.dimension]
            total_score += dim.score * weight
            total_weight += weight

    if total_weight == 0:
        return None

    # Normalize to 0-100 scale
    return (total_score / total_weight) * 20
```

### Integration with External Systems

**Example: Greenhouse ATS integration**

```python
# demo/integrations/greenhouse.py
import requests

def sync_assessment_to_greenhouse(
    assessment: AssessmentResult,
    candidate_id: str,
    greenhouse_api_key: str
):
    """
    Post assessment results to Greenhouse scorecard.
    """
    url = f"https://harvest.greenhouse.io/v1/candidates/{candidate_id}/scorecards"

    payload = {
        "scorecard": {
            "interview": "AI Screening",
            "overall_recommendation": map_score_to_recommendation(assessment.overall_score),
            "attributes": [
                {
                    "name": dim.dimension,
                    "rating": dim.score,
                    "note": dim.reasoning
                }
                for dim in assessment.dimension_scores
            ]
        }
    }

    response = requests.post(
        url,
        json=payload,
        headers={"Authorization": f"Basic {greenhouse_api_key}"}
    )

    return response.json()
```

## Testing

### Running Tests

**Full Test Suite:**
```bash
uv run pytest
```

**Coverage Report:**
```bash
uv run pytest --cov=demo --cov-report=term-missing
```

**Specific Test Files:**
```bash
uv run pytest tests/test_workflow.py -v
uv run pytest tests/test_agentos_app.py::test_screen_endpoint -v
```

### Test Categories

**Unit Tests:**
- `tests/test_models_validation.py`: Pydantic model validation
- `tests/test_scoring.py`: Score calculation logic
- `tests/test_quality_check.py`: Research quality gate

**Integration Tests:**
- `tests/test_workflow.py`: End-to-end workflow execution
- `tests/test_agentos_app.py`: Webhook endpoint and AgentOS integration
- `tests/test_airtable_client.py`: Airtable write operations

**Validation Scripts:**
- `scripts/validate_airtable_client.py`: Verify Airtable schema alignment

### Writing Tests

**Example: Test dimension scoring**

```python
# tests/test_custom_scoring.py
from demo.models import DimensionScore
from demo.screening_helpers import calculate_weighted_score

def test_weighted_scoring():
    """Test weighted dimension scoring."""
    dimensions = [
        DimensionScore(
            dimension="Fundraising Experience",
            score=5,
            evidence_level="High",
            confidence="High",
            reasoning="Led $100M Series C"
        ),
        DimensionScore(
            dimension="Team Building",
            score=3,
            evidence_level="Medium",
            confidence="Medium",
            reasoning="Built team from 5 to 20"
        )
    ]

    weights = {
        "Fundraising Experience": 0.7,
        "Team Building": 0.3
    }

    score = calculate_weighted_score(dimensions, weights)

    # (5 * 0.7 + 3 * 0.3) / 1.0 * 20 = 82
    assert score == 82.0
```

## Best Practices

### Code Style

**Formatting:**
- Use `ruff` for linting and formatting
- Run before commits: `ruff check demo/ && ruff format demo/`

**Type Hints:**
- All functions should have type hints
- Use Pydantic models for structured data
- Use `Optional[T]` for nullable fields

**Documentation:**
- Docstrings for all public functions
- Google-style format
- Include examples for complex functions

**Example:**

```python
def calculate_overall_score(
    dimension_scores: list[DimensionScore]
) -> Optional[float]:
    """
    Calculate overall score from dimension scores.

    Uses simple average of scored dimensions, ignoring None values.
    Returns None if no dimensions are scored.

    Args:
        dimension_scores: List of dimension scores (1-5 or None)

    Returns:
        Overall score (0-100) or None if insufficient data

    Example:
        >>> dims = [
        ...     DimensionScore(dimension="A", score=5, ...),
        ...     DimensionScore(dimension="B", score=3, ...),
        ...     DimensionScore(dimension="C", score=None, ...)
        ... ]
        >>> calculate_overall_score(dims)
        80.0  # (5 + 3) / 2 * 20
    """
    # Implementation...
```

### Error Handling

**Agent Retries:**
- Use exponential backoff for transient failures
- Set reasonable retry limits (2-3)
- Log retry attempts

**Validation:**
- Use Pydantic for all external data
- Provide clear error messages
- Log validation errors with context

**Graceful Degradation:**
- Continue workflow even if optional steps fail
- Use None for unknown data (don't crash)
- Log warnings for degraded operation

### Logging

**Structured Logging:**

```python
import logging

logger = logging.getLogger(__name__)

# Good: Structured with context
logger.info(
    "✅ Deep research completed",
    extra={
        "candidate_id": candidate_id,
        "citation_count": len(citations),
        "execution_time": duration
    }
)

# Avoid: Unstructured
logger.info(f"Research done for {candidate_id}")
```

**Log Levels:**
- `DEBUG`: Detailed diagnostic information
- `INFO`: General informational messages
- `WARNING`: Warning messages (degraded operation)
- `ERROR`: Error messages (failed operations)

### Security

**API Keys:**
- Never commit `.env` files
- Use secret management in production
- Rotate keys regularly

**Input Validation:**
- Validate all webhook payloads with Pydantic
- Sanitize user inputs before LLM prompts
- Limit payload sizes to prevent DoS

**Rate Limiting:**
- Implement rate limiting on `/screen` endpoint
- Use bearer token authentication in production
- Monitor for unusual traffic patterns

## FAQ

**Q: Can I use a different LLM provider (Anthropic, Cohere)?**

A: Yes, Agno supports multiple providers. Update agent definitions:

```python
from agno.models.anthropic import Claude

agent = Agent(
    model=Claude(id="claude-3-5-sonnet"),
    # ... rest of config
)
```

**Q: How do I migrate from SQLite to PostgreSQL?**

A: Update `demo/agentos_app.py`:

```python
from agno.storage import PostgresDb

storage = PostgresDb(
    connection_string=os.getenv("DATABASE_URL")
)

app = create_agentos_app(storage=storage)
```

**Q: Can I run multiple Screens in parallel?**

A: The current implementation is sequential. For parallel processing, deploy multiple AgentOS instances behind a load balancer.

**Q: How do I customize the assessment scoring algorithm?**

A: Edit `demo/screening_helpers.py::calculate_overall_score()` to implement custom logic (weighted average, threshold-based, etc.).

**Q: What's the expected OpenAI API cost per screen?**

A: Approximately $0.10-0.30 per candidate (varies by research depth and model pricing). Deep Research is the primary cost driver.

## Additional Resources

**Documentation:**
- [Getting Started](../getting_started.md) - Setup guide
- [Architecture](../how_it_works/architecture.md) - High-level overview
- [Design Synthesis](DESIGN_SYNTHESIS.md) - Comprehensive architectural analysis
- [Agent Definitions](AGENT_DEFINITIONS.md) - Agent specifications
- [Airtable Schema](../how_it_works/airtable_ai_spec.md) - Database schema

**Code References:**
- `demo/agentos_app.py` - AgentOS server implementation
- `demo/workflow.py` - Workflow orchestration
- `demo/agents.py` - Agent factories
- `demo/models.py` - Data models
- `demo/prompts/catalog.yaml` - Prompt definitions

**External Resources:**
- [Agno Framework Docs](https://docs.agno.com)
- [FastAPI Docs](https://fastapi.tiangolo.com)
- [Pydantic Docs](https://docs.pydantic.dev)
- [OpenAI API Docs](https://platform.openai.com/docs)
- [Airtable API Docs](https://airtable.com/developers/web/api)

## Support

For technical support:
- Internal: Contact DevOps team
- Agno Framework: https://discord.gg/agno
- Issues: GitHub Issues (if applicable)
