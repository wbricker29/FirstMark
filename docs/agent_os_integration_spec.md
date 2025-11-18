# AgentOS Integration Implementation Spec

## Context

Stage 4 of the Talent Signal roadmap (spec/spec.md §4.2) focuses on polishing the webhook/API experience while Stage 5 expands into multi-candidate orchestration and observability. AgentOS (`demo/agentos_app.py`) is now the canonical `/screen` runtime (README + spec updated; Airtable automation instructions point to it), but Flask (`demo/app.py`) still exists for legacy compatibility. FastAPI tests (`tests/test_agentos_app.py`) verify parity, and shared logic lives in `demo/screening_service.py`. This document captures current findings, the target design, and the detailed remaining work required for a complete AgentOS deployment so any developer can pick up the baton.

## Findings (Current State)

- **Runtime + Control Plane:** AgentOS ships with an SSE-compatible FastAPI app and UI control plane. It exposes the same REST API the UI uses, and it can be embedded into an existing FastAPI app via `base_app`. Authentication can rely on bearer tokens backed by a configured security key (docs.agno.com/agent-os/api).
- **Deployment Paths:** Official templates exist for Docker Compose (portable to ECS/GCE/Azure/on-prem) and AWS ECS + managed Postgres. Either path keeps data private because AgentOS always runs in the customer’s cloud (docs.agno.com/templates/agent-infra-* and introduction).
- **Extensibility:** We can keep custom middleware, mount legacy routes, and optionally expose `/mcp` by setting `enable_mcp_server=True`. MCP tools can also be injected into agents with lifecycle management handled by AgentOS (docs.agno.com/agent-os/customize/* and /mcp/*).
- **Data Requirements:** Sessions, memories, and knowledge entries can live in Sqlite for local prototypes (matching today’s `tmp/agno_sessions.db`) but production guidance prefers Postgres for durability and concurrent access.
- **Integration Fit:** AgentOS (`demo/agentos_app.py`) is the preferred runtime; Flask remains only for backwards compatibility. Both share `demo/screening_service.py`, so the behavior is identical. Airtable automation should now hit the AgentOS endpoint (as documented), but we still need to confirm that every automation + script has been updated and, once validated, deprecate the Flask path entirely.
- **ROI Snapshot:** The highest ROI is to finish the AgentOS cutover quickly—remove the Flask entrypoint once tests/docs are updated—then invest incremental effort in AgentOS-native capabilities (workflow configuration, runtime metrics, eval dashboards) that are only possible via the UI.

## Proposed Design

### Runtime Architecture

1. **FastAPI Host:** Instantiate `AgentOS` with our existing agents/workflows (`deep research`, `quality gate`, optional incremental search). Provide a custom FastAPI `base_app` if we need to keep legacy Flask semantics or additional diagnostic routes.
2. **Database Layer:** Reuse `SqliteDb` for initial parity and swap to `PostgresDb` when deploying through Docker/AWS templates. Migration scripts move the current Sqlite session data (if needed) to Postgres.
3. **Security:** Configure an AgentOS security key so the control plane and Airtable automation authenticate via `Authorization: Bearer <token>`. Optionally insert custom middleware for IP allow lists or request logging.

### Workflow Integration

1. **/screen Entry Point:** Replace Flask route with a FastAPI handler mounted either before AgentOS routes or as a lightweight proxy that calls `agent_os.run_workflow("screen_workflow", input=payload)`. Validation logic mirrors `demo/app.py` but now leverages Pydantic request models for stricter typing.
2. **Agent Definitions:** Map the current `demo/agents.py` factories into AgentOS-managed agents. Prompt templates and settings stay canonical via `spec/spec.md` references to avoid drift.
3. **Airtable Client Calls:** Continue to rely on `demo/airtable_client.py` but instantiate the client inside the workflow step (or share via dependency injection). Responses update Airtable tables exactly as the Flask version does today.

### Observability & Ops

1. **Control Plane:** Connect every environment (local/ngrok/demo) to the AgentOS UI so we can inspect sessions, runs, and logs without tailing the console. Document the connection flow (URL, optional security key) and capture required screenshots for demo readiness.
2. **Runtime Configuration:** Use AgentOS config files (or the `AgentOS` constructor) to expose tunables (log level, model IDs, incremental search max calls) that the UI can read/write. This gives stakeholders a UI-based way to tweak the system without redeploying code.
3. **Metrics & Logs:** Surface AgentOS metrics endpoints and SSE logs inside the control plane. If desired, add FastAPI middleware to forward logs to stdout in parallel so CI snapshots and legacy observability tools still get the emoji output.
4. **Evals + MCP (Stage 5+):** After the cutover, enable AgentOS evals for workflow regression tracking, and consider `enable_mcp_server=True` to expose the workflow to external MCP clients. These features extend monitoring/control beyond what Flask could offer.

## Implementation Plan (Prioritized)

1. **Prototype AgentOS Locally** ✅ (complete)
   - `demo/agentos_app.py` runs the existing agents/workflow via AgentOS with shared `process_screen`.
   - FastAPI `/screen` matches Flask behavior; `/docs` + control plane endpoints are available.
2. **Define Integration Contracts** ✅ (complete)
   - FastAPI request/response contract documented in `spec/spec.md` (“Screening API” section).
   - Airtable automation payloads, headers, and curl examples now reference the AgentOS `/screen` endpoint.
3. **Replace Flask Runtime (In Progress)**
   - ✅ FastAPI-specific regression tests (`tests/test_agentos_app.py`) and README/runbook updates pointing to AgentOS.
   - ✅ Update CI to treat `demo/app.py` tests as optional/legacy (pyproject default `-m 'not legacy'`; run `pytest -m legacy tests/test_app.py`).
   - ⬜ Ensure Airtable automation + any scripts (ngrok launchers, Procfiles, demo notes) reference only AgentOS URLs (helper scripts + AGENTS runbooks updated; Airtable automation still to be confirmed).
   - ⬜ Announce deprecation timeline for Flask, then remove the entrypoint after confirmation.
   - ✅ Add warning banner to `demo/app.py` directing developers to the AgentOS runtime (remaining references can now be cleaned up incrementally).
4. **Harden Data + Deployment**
   - Introduce Postgres via the Agent Infra Docker template; add migration scripts and settings plumbing.
   - Wire CI to run uv tasks against the new service and capture metrics snapshots as artifacts.
   - Configure optional bearer auth (`AGENTOS_SECURITY_KEY`) before exposing the service via ngrok or cloud.
5. **Incremental Monitoring Enhancements (Stage 5/6)**
   - Enable AgentOS eval endpoints for structured regression tests.
   - Turn on `/mcp` to expose the workflow as an MCP server once we integrate external orchestrators.
   - Add runtime dashboards/screenshots to `docs/` showcasing control-plane monitoring, configuration toggles, and eval results.

Each numbered item represents a milestone; tackle them sequentially, only pulling optional enhancements once Stage 4 parity and Stage 5 infra readiness are complete.

## Outstanding Work Checklist (Developer Hand-off)

The following tasks remain to finish the cutover and make AgentOS production-ready. A developer with no prior context can follow these steps:

### 1. Airtable Automation Verification
- Confirm every Airtable automation hitting `/screen` uses the AgentOS ngrok URL and `Content-Type: application/json`.
- If we enable `AGENTOS_SECURITY_KEY`, add the `Authorization: Bearer ...` header and document how the key is stored/distributed.
- Update Airtable automation descriptions/comments to note the AgentOS endpoint and remove references to Flask.
- Inventory every automation touching Screens/Searches (name, trigger, action) and track findings in a lightweight audit table (e.g., `tmp/automation_audit.md`).
- For each webhook action: verify POST method, ensure the body is exactly `{ "screen_id": "{RECORD_ID}" }`, and confirm headers include `Content-Type: application/json` plus `Authorization: Bearer <key>` when applicable.
- Use Airtable's built-in **Test** for each automation with a real Screen record; record the timestamp + outcome in the audit log and capture terminal logs showing the AgentOS runtime handling the request.
- Only mark this section complete once every automation entry has: updated description referencing AgentOS, verified URL/headers, and a successful test recorded in the audit log.

### 2. Legacy Runtime Decommission
- ✅ Update CI to skip legacy Flask tests by default (pyproject `addopts = "-m 'not legacy'"`; run `pytest -m legacy tests/test_app.py` when desired).
- ✅ Add warning banner at the top of `demo/app.py` directing developers to `demo/agentos_app.py`.
- ⬜ Remove any remaining CLI scripts/Procfiles referencing `demo/app.py` now that helper scripts have been updated.
- ⬜ Delete Flask-specific setup instructions from README once no teams rely on it.

### 3. Deployment & Infrastructure
- Choose a deployment template (Docker Compose or AWS ECS) from the Agno docs and document the exact commands to run AgentOS in that environment.
- Add configuration for Postgres (connection URL, migrations) and security key management in `.env` and docs.
- Extend the README/runbook with a “Production launch” section covering: building the image, running migrations, starting AgentOS, verifying `/healthz`, connecting the control plane, and rotating security keys.

### 4. Monitoring & Evaluations
- Enable AgentOS metrics/evals and capture a sample eval run for Stage 5 demo readiness.
- Document how to connect the AgentOS control plane (URL, auth, common troubleshooting steps) so future operators can monitor workflows without digging through logs.
- Consider enabling `enable_mcp_server=True` if we plan to expose the workflow to MCP clients; document the contract and authentication requirements.

Finishing these items will leave the repository with a single, well-documented AgentOS runtime, clear deployment steps, and the observability hooks needed for Stage 5 and beyond.
