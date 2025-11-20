# Demo Prep Checklist - Minimal Viable Path (Option 1)

**Target:** Demo-ready in 3-4 hours
**Deadline:** Nov 19, 2025 at 5:00 PM
**Last Updated:** 2025-01-19 Evening

---

## 🎯 Critical Path (3-4 hours)

### Task 1: Execute 1 Quality Pre-Run (90 min) **HIGHEST PRIORITY**

**Objective:** Create 1 polished pre-run scenario with 8-10 candidates to demonstrate full workflow capabilities and provide assessment outputs for presentation storytelling.

**Scenario:** Pigment CFO (already has test execution with 3 candidates - expand to 8-10)

**Steps:**
1. **Select 8-10 candidates from Airtable** (10 min)
   - Query People table for CFOs
   - Ensure good mix of backgrounds
   - Verify bio files and LinkedIn profiles exist

2. **Create Screen record in Airtable** (5 min)
   - Link to Pigment CFO Search
   - Link 8-10 selected candidates
   - Set status = "Ready to Screen"
   - Ensure `Admin-screen_slug` formula populates

3. **Execute screening workflow** (60 min)
   - Trigger via Airtable automation webhook
   - Monitor AgentOS server logs for progress
   - Watch AgentOS control plane UI for step execution
   - Capture screenshots of:
     - Workflow execution in AgentOS
     - Research step outputs
     - Assessment results
     - Airtable assessment records

4. **Validate results** (15 min)
   - Check Screen status = "Complete"
   - Verify 8-10 Assessment records created
   - Inspect assessment JSON quality (scores, flags, counterfactuals)
   - Review citation counts (≥3 per assessment)
   - Document any errors or quality issues

**Deliverables:**
- ✅ 8-10 completed assessments with rich data
- ✅ Screenshots of workflow execution
- ✅ AgentOS session logs/screenshots
- ✅ Sample assessment outputs for presentation

---

### Task 2: Finalize Presentation Deck (60 min)

**Objective:** Complete slides with assessment screenshots and demo narrative.

**Current State:** Deck exists at `case/WB_VCDeck_2.1 (1).pptx` - completion status unknown

**Steps:**
1. **Review existing deck** (10 min)
   - Open PowerPoint file
   - Identify incomplete sections
   - Note placeholders for screenshots/data

2. **Add assessment screenshots** (20 min)
   - Insert screenshots from Task 1 (AgentOS workflow, assessment results)
   - Create "Before/After" slide showing candidate ranking
   - Add example assessment with scores/flags/counterfactuals
   - Include citation evidence example

3. **Refine narrative flow** (20 min)
   - Ensure product context → architecture → demo → results flow
   - Add talking points for live demo section
   - Highlight key achievements:
     - Zero-traversal Airtable pattern (100% API read elimination)
     - Evidence-aware scoring (None for unknown)
     - Quality-gated research workflow
     - AgentOS observability

4. **Add backup materials** (10 min)
   - Include curl command for manual webhook trigger
   - Add ngrok URL reference
   - Include error recovery instructions

**Deliverables:**
- ✅ Complete presentation deck (slides/PDF)
- ✅ Talking points integrated
- ✅ Screenshots embedded
- ✅ Backup instructions included

---

### Task 3: Quick Rehearsal (45 min)

**Objective:** Practice full demo flow and validate timing.

**Steps:**
1. **Setup validation** (10 min)
   - Start AgentOS server: `uv run python demo/agentos_app.py`
   - Start ngrok tunnel: `ngrok http 5001`
   - Document current ngrok URL
   - Verify Airtable automation is enabled

2. **Dry run presentation** (25 min)
   - Practice slide walkthrough (target: 15-20 min)
   - Time each section:
     - Intro + context (3 min)
     - Architecture overview (5 min)
     - Live demo or screenshot walkthrough (7 min)
     - Results + roadmap (5 min)
   - Practice transitions between slides
   - Rehearse live demo backup plan (if webhook fails)

3. **Q&A preparation** (10 min)
   - Prepare answers for likely questions:
     - "How accurate are the assessments?"
     - "How does this scale?"
     - "What data sources do you use?"
     - "How do you handle unknown/insufficient data?"
   - Reference key docs: README.md, DESIGN_SYNTHESIS.md, DEMO_RUNBOOK.md

**Deliverables:**
- ✅ Timed presentation (under 30 min)
- ✅ Infrastructure validated
- ✅ Q&A preparation complete

---

### Task 4: Environment Validation (30 min)

**Objective:** Smoke test full infrastructure and create backup plan.

**Steps:**
1. **Infrastructure smoke test** (15 min)
   - Verify `.env` has all required API keys:
     - OPENAI_API_KEY
     - AIRTABLE_API_KEY
     - AIRTABLE_BASE_ID
   - Test AgentOS server startup
   - Test ngrok tunnel stability
   - Verify Airtable webhook automation
   - Test `/healthz` endpoint

2. **Create backup execution plan** (15 min)
   - Document manual webhook trigger command:
     ```bash
     curl -X POST https://[ngrok-url]/screen \
       -H "Content-Type: application/json" \
       -d @test_payload.json
     ```
   - Prepare test payload JSON file
   - Document rollback procedures if demo fails
   - Prepare "screenshot demo" as fallback (use Task 1 screenshots)

**Deliverables:**
- ✅ Environment validated
- ✅ Backup plan documented
- ✅ Test payload ready
- ✅ Rollback procedures clear

---

## 📋 Pre-Flight Checklist

**Before Demo:**
- [ ] AgentOS server running (port 5001)
- [ ] ngrok tunnel active and URL documented
- [ ] Airtable automation enabled
- [ ] Presentation deck complete with screenshots
- [ ] Backup materials prepared (curl command, test payload)
- [ ] Demo rehearsal complete (timing validated)
- [ ] Q&A prep complete

**Demo Day:**
- [ ] Start AgentOS server 30 min before presentation
- [ ] Start ngrok and verify URL
- [ ] Open Airtable base in browser tab
- [ ] Open AgentOS control plane in browser tab
- [ ] Load presentation deck
- [ ] Have backup screenshots ready
- [ ] Test webhook trigger once before presentation

---

## 🚨 Risk Mitigation

**High Risk Items:**
1. **ngrok URL expires** → Have backup: restart ngrok 30 min before demo, update Airtable automation
2. **Webhook timeout** → Use async endpoint (already implemented), have curl backup ready
3. **API rate limits** → Pre-run completed assessments, demo uses existing data
4. **Live demo fails** → Fallback to screenshot walkthrough from Task 1

**Medium Risk Items:**
1. **Presentation timing** → Practice 2x, have "short version" ready
2. **Q&A stumpers** → Admit unknowns, reference docs for detailed answers
3. **Infrastructure issues** → Have backup plan documented (Task 4)

---

## ✅ Success Criteria

**Minimal Viable Demo Achieved When:**
- ✅ 1 polished pre-run scenario complete (8-10 candidates)
- ✅ Presentation deck finalized with screenshots
- ✅ Demo rehearsed and timed (under 30 min)
- ✅ Infrastructure validated and backup plan ready
- ✅ Airtable shows rich assessment data for storytelling

**Demo Quality Indicators:**
- Assessment JSON blobs contain all 7 fields (research, assessment, dimensions, must-haves, flags, counterfactuals)
- Scores in 0-100 range, citations ≥3 per assessment
- AgentOS session logs show clear workflow steps
- Presentation tells compelling product story with evidence

---

## 📊 Time Allocation

| Task | Est. Time | Priority |
|------|-----------|----------|
| Task 1: Quality Pre-Run | 90 min | **CRITICAL** |
| Task 2: Presentation Deck | 60 min | **HIGH** |
| Task 3: Rehearsal | 45 min | **HIGH** |
| Task 4: Environment Validation | 30 min | **MEDIUM** |
| **Total** | **3h 45min** | |

**Buffer:** 15 min for unexpected issues

---

## 🎬 Next Actions

**Start immediately with Task 1** - the pre-run execution is the longest task and provides the screenshots/data needed for Task 2.

**Sequence:**
1. Task 1 (90 min) → Provides screenshots and data
2. Task 2 (60 min) → Uses Task 1 outputs
3. Task 3 (45 min) → Validates complete flow
4. Task 4 (30 min) → Final safety checks

**Goal:** Demo-ready by end of this checklist execution.
