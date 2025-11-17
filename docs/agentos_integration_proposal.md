# AgentOS Integration Design Proposal

## Executive Summary

**Objective:** Consolidate Flask + Agno agents into a unified AgentOS FastAPI application with built-in monitoring, observability, and production-ready architecture.

**Key Changes:**
1. Migrate Flask webhook → FastAPI custom routes
2. Wrap agents in AgentOS for monitoring/observability
3. Connect to AgentOS Control Plane for visual monitoring
4. Maintain existing workflow logic (no changes to agent behavior)

**Effort:** 2-3 hours | **Value:** Production-ready architecture, live monitoring for demo, cleaner codebase

---

## Current State Analysis

### Architecture
```
Flask App (port 5000)
├── POST /webhook/airtable (ngrok tunnel)
├── Airtable signature validation
├── Direct agent execution
│   ├── ResearchAgent.run()
│   └── AssessmentAgent.run()
└── Airtable result updates

Agno Agents (in-process)
├── ResearchAgent (o4-mini-deep-research)
├── AssessmentAgent (gpt-5)
└── SqliteDb at tmp/agno_sessions.db

Data Flow:
Airtable → ngrok → Flask → Agents → Airtable
```

### Limitations
- **No observability:** Can't visualize agent execution
- **Framework fragmentation:** Flask (webhook) + Agno (agents)
- **No monitoring:** No run tracking, metrics, or session history
- **Manual debugging:** Limited insight into agent behavior
- **Deployment complexity:** Two conceptual layers (web + agents)

---

## Proposed Architecture

### System Design
```
AgentOS FastAPI App (port 7777)
│
├── Custom Routes (Your Implementation)
│   └── POST /webhook/airtable
│       ├── Signature validation
│       ├── Payload parsing
│       └── Agent workflow trigger
│
├── AgentOS Routes (Built-in)
│   ├── GET  /config              (AgentOS configuration)
│   ├── GET  /docs                (OpenAPI docs)
│   ├── GET  /sessions            (Session tracking)
│   ├── POST /agents/{id}/runs    (Agent execution API)
│   └── GET  /sessions/{id}       (Session details + metrics)
│
├── Agents (AgentOS-managed)
│   ├── ResearchAgent
│   │   ├── Model: o4-mini-deep-research
│   │   ├── Tools: Deep Research API
│   │   └── Storage: SqliteDb
│   └── AssessmentAgent
│       ├── Model: gpt-5
│       ├── Output: Pydantic schema
│       └── Storage: SqliteDb
│
└── External Connections
    ├── Airtable (webhook source + data sink)
    ├── AgentOS Control Plane (os.agno.com - monitoring)
    └── ngrok (local tunnel for development)

Data Flow:
Airtable → ngrok → FastAPI /webhook → AgentOS agents → Airtable
                                          ↓
                            AgentOS Control Plane (monitoring)
```

### Component Architecture

**1. FastAPI Application Layer**
```python
app = FastAPI(
    title="FirstMark Talent Signal Agent",
    version="1.0.0",
    description="AI-powered executive matching system"
)

# Custom webhook route
@app.post("/webhook/airtable")
async def airtable_webhook(payload: dict):
    # Validation, parsing, agent triggering
    pass
```

**2. AgentOS Integration Layer**
```python
agent_os = AgentOS(
    id="talent-signal-os",
    description="FirstMark Talent Signal Agent",
    agents=[research_agent, assessment_agent],
    base_app=app,  # Wraps custom FastAPI app
)

app = agent_os.get_app()  # Combined app
```

**3. Agent Execution Layer**
- Agents remain unchanged (existing logic preserved)
- AgentOS provides lifecycle management
- Session tracking automatic via SqliteDb

**4. Monitoring Layer**
- AgentOS Control Plane connection (os.agno.com)
- Local endpoint: http://localhost:7777
- Real-time session/run visualization

---

## Design Rationale

### 1. Framework Consolidation (Flask → FastAPI)

**Problem:** Flask for webhooks + Agno agents = fragmented architecture

**Solution:** Single FastAPI app (AgentOS is FastAPI-native)

**Benefits:**
- Unified framework (FastAPI everywhere)
- Better async support (important for agent execution)
- Automatic OpenAPI docs
- Native Pydantic integration (matches agent `output_schema`)
- Production-ready ASGI server

**Migration Path:**
```python
# Before (Flask)
@app.route('/webhook/airtable', methods=['POST'])
def airtable_webhook():
    data = request.json
    # ...

# After (FastAPI)
@app.post("/webhook/airtable")
async def airtable_webhook(payload: dict):
    # ...
```

### 2. AgentOS Monitoring Integration

**Problem:** No visibility into agent execution, debugging is manual

**Solution:** AgentOS provides built-in observability

**What You Get:**
- **Session Tracking:** Each Airtable search = 1 session
- **Run Visualization:** See Research → Quality Check → Assessment timeline
- **Metrics Dashboard:** Token usage, latency, costs per search
- **Tool Call Inspection:** See Deep Research API calls, inputs/outputs
- **State Tracking:** Monitor session state throughout workflow

**Control Plane UI Features:**
- Real-time agent execution monitoring
- Historical session browsing
- Performance metrics aggregation
- Cost tracking per search

### 3. Minimal Code Changes

**Philosophy:** Wrap, don't rewrite

**Agent Code:** UNCHANGED
- Same agent definitions
- Same tools, instructions, models
- Same workflow logic
- Same SqliteDb storage

**Only Changes:**
1. Flask → FastAPI route conversion (1:1 mapping)
2. Add AgentOS wrapper (3 lines of code)
3. Optional: Trigger agents via AgentOS API (for better tracking)

### 4. Production Readiness

**Demo Value (Nov 19):**
- Live monitoring during Estuary CTO demo
- Visual timeline of agent thinking
- Metrics dashboard proves scalability
- Professional API documentation

**Production Benefits:**
- Observability from day 1
- Cost/performance tracking
- Debug capabilities
- Scalable architecture

---

## Technical Specification

### File Structure
```
project/
├── main.py                    # AgentOS FastAPI app (NEW)
├── demo/
│   ├── agents.py             # Agent definitions (UNCHANGED)
│   └── workflow.py           # Workflow logic (UNCHANGED)
├── webhooks/
│   ├── airtable_handler.py   # Webhook logic (MIGRATED from Flask)
│   └── validation.py         # Signature validation (UNCHANGED)
├── tmp/
│   └── agno_sessions.db      # Shared database (UNCHANGED)
└── requirements.txt          # Add fastapi[standard] (remove flask)
```

### Core Implementation

**main.py (New Entry Point)**
```python
from fastapi import FastAPI, HTTPException, Request
from agno.os import AgentOS
from agno.db.sqlite import SqliteDb
from demo.agents import research_agent, assessment_agent
from webhooks.airtable_handler import validate_webhook, process_search

# Create FastAPI app with custom routes
app = FastAPI(
    title="FirstMark Talent Signal Agent",
    version="1.0.0",
    description="AI-powered executive matching for FirstMark portfolio companies"
)

# Airtable webhook endpoint
@app.post("/webhook/airtable")
async def airtable_webhook(request: Request):
    """
    Airtable webhook handler - triggers screening workflow

    Flow:
    1. Validate webhook signature
    2. Parse search record data
    3. Trigger research agent (session: search-{id})
    4. Trigger assessment agent (same session)
    5. Update Airtable with results
    """
    # Get raw body for signature validation
    body = await request.body()
    headers = request.headers

    # Validate Airtable signature
    if not validate_webhook(body, headers):
        raise HTTPException(status_code=401, detail="Invalid signature")

    # Parse payload
    payload = await request.json()
    search_id = payload.get("search_id")

    if not search_id:
        raise HTTPException(status_code=400, detail="Missing search_id")

    # Process search (triggers agents internally)
    result = await process_search(
        search_id=search_id,
        research_agent=research_agent,
        assessment_agent=assessment_agent,
    )

    return {
        "status": "completed",
        "session_id": f"search-{search_id}",
        "results": result
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "talent-signal-agent"}

# Wrap with AgentOS
agent_os = AgentOS(
    id="talent-signal-os",
    description="FirstMark Talent Signal Agent - AI-powered executive matching",
    agents=[research_agent, assessment_agent],
    base_app=app,  # Pass custom FastAPI app
)

# Get combined app (custom routes + AgentOS routes)
app = agent_os.get_app()

if __name__ == "__main__":
    # Serve on port 7777 (AgentOS default)
    agent_os.serve(
        app="main:app",
        reload=True,
        port=7777,
    )

    # Access points:
    # - http://localhost:7777/webhook/airtable (custom)
    # - http://localhost:7777/docs (AgentOS)
    # - http://localhost:7777/config (AgentOS)
    # - http://localhost:7777/sessions (AgentOS)
```

**webhooks/airtable_handler.py (Migrated)**
```python
from typing import Dict, Any
from demo.agents import ResearchAgent, AssessmentAgent
from pyairtable import Api

async def process_search(
    search_id: str,
    research_agent: ResearchAgent,
    assessment_agent: AssessmentAgent,
) -> Dict[str, Any]:
    """
    Execute screening workflow for a search

    Flow: Research → Quality Check → Assessment
    """
    session_id = f"search-{search_id}"

    # Step 1: Research agent
    research_response = research_agent.run(
        input={"search_id": search_id},
        session_id=session_id,
        user_id="airtable-webhook",
    )

    # Step 2: Assessment agent (uses research results via session)
    assessment_response = assessment_agent.run(
        input={"search_id": search_id},
        session_id=session_id,  # Same session
        user_id="airtable-webhook",
    )

    # Update Airtable with results
    # ... existing update logic ...

    return {
        "research": research_response.content,
        "assessment": assessment_response.content,
    }
```

### Session Management

**Session Structure:**
```
Session: "search-{search_id}"
├── Run 1: Research Agent
│   ├── Input: {"search_id": "rec123"}
│   ├── Model: o4-mini-deep-research
│   ├── Tools: [Deep Research API calls]
│   ├── Output: Research structured JSON
│   └── Metrics: tokens, latency, cost
├── Run 2: Quality Check (internal to Research Agent)
│   └── Self-assessment validation
└── Run 3: Assessment Agent
    ├── Input: {"search_id": "rec123"}
    ├── Context: Run 1 results (via session history)
    ├── Model: gpt-5
    ├── Output: Assessment structured JSON
    └── Metrics: tokens, latency, cost

Session Metrics (Aggregated):
├── Total tokens: sum(all runs)
├── Total cost: sum(all runs)
├── Duration: end_time - start_time
└── Status: completed/failed
```

### Monitoring Setup

**1. Local Development**
```bash
# Terminal 1: Start AgentOS
python main.py

# Terminal 2: Start ngrok
ngrok http 7777

# Browser: Connect to Control Plane
# Visit: os.agno.com
# Add OS: http://localhost:7777 (Local)
# Name: "Talent Signal Dev"
```

**2. Control Plane Features**
- **Sessions Tab:** Browse all searches
- **Session Detail:** Click session → see timeline
- **Metrics:** Token usage, costs, performance
- **Agent Inspector:** See tool calls, reasoning

**3. API Access**
```bash
# List all sessions
GET http://localhost:7777/sessions?type=agent

# Get specific session
GET http://localhost:7777/sessions/search-rec123

# Get session metrics
GET http://localhost:7777/sessions/search-rec123/metrics
```

---

## Implementation Plan

### Phase 1: FastAPI Migration (1 hour)

**Tasks:**
1. Create `main.py` with FastAPI app
2. Migrate Flask webhook route → FastAPI route
3. Update imports (flask → fastapi)
4. Test webhook locally with curl

**Validation:**
- ✅ Webhook endpoint responds
- ✅ Signature validation works
- ✅ Payload parsing correct

### Phase 2: AgentOS Integration (30 min)

**Tasks:**
1. Wrap FastAPI app with AgentOS
2. Configure agents in AgentOS
3. Test combined app startup
4. Verify routes don't conflict

**Validation:**
- ✅ App starts on port 7777
- ✅ `/webhook/airtable` accessible
- ✅ `/docs` shows all endpoints
- ✅ `/config` shows AgentOS config

### Phase 3: Session Tracking (30 min)

**Tasks:**
1. Update agent execution to use session_id
2. Test session persistence in SqliteDb
3. Verify session history builds correctly

**Validation:**
- ✅ Each search creates unique session
- ✅ Multiple runs tracked per session
- ✅ Session state preserved across runs

### Phase 4: Control Plane Connection (15 min)

**Tasks:**
1. Start AgentOS locally
2. Visit os.agno.com
3. Add new OS (Local, localhost:7777)
4. Test session visibility

**Validation:**
- ✅ Control Plane connects successfully
- ✅ Sessions visible in UI
- ✅ Metrics displayed correctly

### Phase 5: Integration Testing (45 min)

**Tasks:**
1. Update ngrok tunnel to port 7777
2. Update Airtable webhook URL
3. Trigger test search from Airtable
4. Monitor execution in Control Plane
5. Verify results written to Airtable

**Validation:**
- ✅ Webhook receives Airtable payload
- ✅ Agents execute successfully
- ✅ Session tracked in Control Plane
- ✅ Results written to Airtable
- ✅ Metrics captured correctly

---

## Risk Assessment

### Technical Risks

**Risk 1: Route Conflicts**
- **Issue:** AgentOS routes might conflict with custom routes
- **Mitigation:** Use `on_route_conflict="preserve_base_app"`
- **Probability:** Low
- **Impact:** Low

**Risk 2: Session Tracking Overhead**
- **Issue:** AgentOS session tracking adds latency
- **Mitigation:** SqliteDb already used; minimal overhead
- **Probability:** Low
- **Impact:** Low

**Risk 3: ngrok Port Change**
- **Issue:** Changing from port 5000 → 7777 breaks ngrok
- **Mitigation:** Update ngrok command; test before Airtable update
- **Probability:** Medium
- **Impact:** Low (5 min fix)

### Migration Risks

**Risk 4: Flask → FastAPI Compatibility**
- **Issue:** Request handling differences
- **Mitigation:** FastAPI Request object similar to Flask
- **Probability:** Low
- **Impact:** Low

**Risk 5: Time Constraint**
- **Issue:** Implementation takes longer than estimated
- **Mitigation:** Phased approach; can roll back to Flask
- **Probability:** Medium
- **Impact:** Medium

### Rollback Plan

If AgentOS integration fails:
1. Keep Flask app as backup
2. Revert to direct agent execution
3. Total rollback time: <5 minutes

---

## Success Criteria

### Functional Requirements
- ✅ Airtable webhook triggers screening workflow
- ✅ Research → Assessment pipeline executes correctly
- ✅ Results written to Airtable Assessments table
- ✅ All 4 demo scenarios work (Pigment, Mockingbird, Synthesia, Estuary)

### Technical Requirements
- ✅ Single FastAPI application
- ✅ AgentOS monitoring active
- ✅ Sessions tracked per search
- ✅ Metrics captured (tokens, costs, latency)
- ✅ Control Plane connection established

### Demo Requirements (Nov 19)
- ✅ Live monitoring during Estuary CTO demo
- ✅ Visual timeline of agent execution
- ✅ Metrics dashboard shows performance
- ✅ API documentation at /docs

### Performance Requirements
- ✅ Webhook response time: <500ms (validation + trigger)
- ✅ Agent execution time: <2 min (unchanged from current)
- ✅ Session tracking overhead: <100ms

---

## Post-Implementation

### Monitoring Dashboard
- Track all searches in Control Plane
- Weekly metrics review (costs, performance)
- Identify optimization opportunities

### Documentation Updates
- Update README with AgentOS setup
- Document monitoring access
- Add troubleshooting guide

### Future Enhancements (Phase 2+)
- Async agent execution (webhook returns immediately)
- Email notifications on completion
- Advanced metrics (quality scores over time)
- Multi-search batch processing

---

## Appendix: Code Comparison

### Before (Flask)
```python
from flask import Flask, request

app = Flask(__name__)

@app.route('/webhook/airtable', methods=['POST'])
def airtable_webhook():
    data = request.json
    # Direct agent execution
    research_agent.run(...)
    return {"status": "ok"}

if __name__ == '__main__':
    app.run(port=5000)
```

### After (AgentOS FastAPI)
```python
from fastapi import FastAPI
from agno.os import AgentOS

app = FastAPI()

@app.post("/webhook/airtable")
async def airtable_webhook(payload: dict):
    # Agent execution (tracked by AgentOS)
    research_agent.run(session_id=...)
    return {"status": "ok"}

agent_os = AgentOS(agents=[...], base_app=app)
app = agent_os.get_app()

if __name__ == '__main__':
    agent_os.serve(app="main:app", port=7777)
```

**Difference:** 3 lines added, monitoring/observability included

---

## Recommendation

**Proceed with AgentOS integration:** Strong recommend

**Rationale:**
- Low risk (2-3 hour effort, phased approach, rollback available)
- High value (production architecture, live monitoring for demo)
- Clean architecture (consolidates Flask + Agno → unified FastAPI)
- Demo impact (shows technical maturity, observability, scalability)

**Timeline:** Implement before Nov 19 demo (allows 1-2 days for testing)
