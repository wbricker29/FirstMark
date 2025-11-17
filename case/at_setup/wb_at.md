# Wb AT Impleemtnation planning


### Module 1: Data Uploading

**Flow (via Airtable Interface UI):**

- Upload file via Airtable attachment field
- Select File type dropdown (person, company)
  - No role uploads for demo
- Click "Process Upload" button
  - Can either be webflow trigger button if UI allows, or can be an action that changes a field value to trigger webhook
- **Webhook triggers Flask `/upload` endpoint**
  - Python: Download file from Airtable
  - Python: Clean, normalize, dedupe
  - Python: Load into proper table
  - Python: Update status field with results

**Demo:**

- Add new people CSV
  - Could add bios in text field too

**Implementation:**

```python
@app.route('/upload', methods=['POST'])
def process_upload():
    # Get file from Airtable
    # Clean and normalize
    # Deduplicate rows (see deduplication strategy below)
    # Load to appropriate table
    # Return status
```

**Deduplication Strategy (Demo-Scoped):**

- Primary key for people imported via CSV:
  - Use a normalized combination of `full_name` + `current_company` (case-insensitive) as a soft key.
- Before inserting a new person:
  - Search the People table for an existing record with the same normalized name + company.
  - If found, skip insert and attach any additional CSV metadata as an update rather than a new row.
- This keeps the demo data clean without heavy-weight fuzzy matching.

### Module 2: New Open Role

**ALL IN AIRTABLE (no Python)**

**Definitions and Notes:**

- Open roles exist for many portcos. Not all of them we will be actively assisting with
- Portcos can provide us open roles that we provide in careers portal externally
- Note: Can have portcos submit + Aging mechanism

**Flow (via Airtable Interface UI):**

- Select Portco
- Select Role type
- Optional notes for candidate parameters
- Optional add spec
  - Select Existing
    - Ability to add bespoke requirements
  - Create Own
  - Maybe create new version of existing

**Demo:**

- Create new Role live

### Module 3: New Search

**ALL IN AIRTABLE (no Python)**

**Definitions and Notes:**

- Search is a role we are actively assisting with. Will have role spec
- Have as distinct item so we can attach other items to it (like notes)

**Flow (via Airtable Interface UI):**

- Link Role
- Link spec?
- Add notes
- Add timeline date

**Demo:**

- Create new search live

### Module 4: New Screen

**Pattern:** Airtable Button → Webhook → Flask `/screen` endpoint

**Definition:**

- Perform screening on a set of people for a search
- Main demo workflow for talent matching

**Requirements:**

- Process one or more candidates at a time
- Bulk selection via linked records
- Multiple screens per search allowed
- Can redo evals with new guidance

**Flow (via Airtable Interface UI):**

- Create new Screen record in Airtable
- Link to Search (which links to Role + Spec)
- Add custom guidance/specifications (optional)
- Link one or more candidates from People table
  - Use Airtable multi-select
- Click "Start Screening" button
  - Can either be webflow trigger button if UI allows, or can be an action that changes a field value to trigger webhook
- **Webhook triggers Flask `/screen` endpoint**
  - For each linked candidate:
    - Create Workflow record (audit trail)
    - Run Deep Research via OpenAI API
    - Store research results in Workflow record
    - Run Assessment against role spec
    - Store assessment in Workflow record
      - Overall score + confidence
      - Dimension-level scores
      - Reasoning + counterfactuals
    - Update candidate status
    - Mark Workflow as complete
  - Update Screen status to "Complete"
  - Terminal shows real-time progress

**Implementation (synchronous for demo):**

```python
@app.route('/screen', methods=['POST'])
def run_screening():
    """Synchronous screening with full event capture for audit trail."""
    screen_id = request.json['screen_id']

    # Get screen details + linked candidates
    screen = get_screen(screen_id)
    candidates = get_linked_candidates(screen)

    # Process candidates sequentially (simple, reliable for demo)
    results = []
    for candidate in candidates:
        print(f"📋 Processing: {candidate.name}")

        # Create workflow record for audit trail
        workflow = create_workflow_record(screen_id, candidate.id)

        # Research with event capture (returns ExecutiveResearchResult + events)
        research = run_deep_research(candidate)

        # Assessment with event capture
        assessment = run_assessment(candidate, research, screen.role_spec)

        # Write results to Airtable
        write_results_to_airtable(workflow, research, assessment)

        results.append(assessment)
        print(f"✅ Completed: {candidate.name}")

    # Update screen status
    update_screen_status(screen_id, 'Complete')

    return {'status': 'success', 'candidates_processed': len(results)}
```

**Demo:**

- Demo UI and kick off flow
- Use pre-run example for discussion and can check in periodically to see the live run is progressing
