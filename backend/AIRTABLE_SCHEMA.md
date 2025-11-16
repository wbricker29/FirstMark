# Airtable Base Schema

Complete schema for FirstMark Talent Signal Agent Airtable base.

## Base Setup

**Base Name:** FirstMark Talent Signal Agent

Create a new Airtable base with the following tables:

## Tables

### 1. Companies

Portfolio companies and hiring organizations.

| Field Name | Type | Options | Description |
|------------|------|---------|-------------|
| Name | Single line text | Primary | Company name |
| Description | Long text | | Company description |
| Industry | Single select | SaaS, FinTech, HealthTech, AI/ML, Infrastructure, Other | Industry category |
| Stage | Single select | Seed, Series A, Series B, Series C+, Growth, Public | Funding stage |
| Status | Single select | Active, Exited, Archived | Portfolio status |
| Website | URL | | Company website |
| Roles | Linked to Roles | | Open roles at this company |

**Views:**
- All Companies (default)
- Active Portfolio (filter: Status = Active)
- By Stage (group by: Stage)

---

### 2. Roles

Open positions across portfolio companies.

| Field Name | Type | Options | Description |
|------------|------|---------|-------------|
| Title | Single line text | Primary | Role title (e.g., "CTO", "CFO") |
| Company | Link to Companies | | Hiring company |
| Raw Description | Long text | | Original job description |
| Generated Spec | Long text | | LLM-generated structured spec |
| Required Skills | Multiple select | Python, AI/ML, Cloud, Leadership, Sales, Finance, etc. | Key skills needed |
| Seniority | Single select | Junior, Mid, Senior, Executive | Experience level |
| Status | Single select | Draft, Spec Generated, Assessment In Progress, Candidates Identified, Filled, Closed | Workflow status |
| Button: Generate Spec | Button | | Triggers role spec generation |
| Button: Find Candidates | Button | | Triggers candidate assessment |
| Created | Created time | | Auto-populated |
| Modified | Last modified time | | Auto-populated |

**Button Configurations:**

**"Generate Spec" Button:**
- Label: "Generate Role Spec"
- Click → Triggers Airtable Automation → Webhook to N8n

**"Find Candidates" Button:**
- Label: "Assess Candidates"
- Click → Triggers Airtable Automation → Webhook to N8n

**Views:**
- All Roles (default)
- Active Searches (filter: Status ≠ Filled, Closed)
- By Company (group by: Company)
- Need Spec (filter: Status = Draft)

---

### 3. Candidates

Executive candidates from portfolio, guilds, and LinkedIn.

| Field Name | Type | Options | Description |
|------------|------|---------|-------------|
| Name | Single line text | Primary | Full name |
| Current Title | Single line text | | Current job title |
| LinkedIn URL | URL | | LinkedIn profile |
| Bio | Long text | | Professional bio/summary |
| Skills | Multiple select | Same as Roles | Professional skills |
| Source | Single select | Portfolio, FirstMark Guild, LinkedIn, Referral | Candidate source |
| Years Experience | Number | Integer | Total years of experience |
| Location | Single line text | | Current location |
| Assessments | Link to Assessments | | Assessment records |
| Created | Created time | | Auto-populated |

**Views:**
- All Candidates (default)
- By Source (group by: Source)
- Portfolio Talent (filter: Source = Portfolio)
- Guild Members (filter: Source = FirstMark Guild)

---

### 4. Assessments

Assessment results linking candidates to roles.

| Field Name | Type | Options | Description |
|------------|------|---------|-------------|
| Role | Link to Roles | Required | Role being assessed for |
| Candidate | Link to Candidates | Required | Candidate being assessed |
| Research Summary | Long text | | Research findings summary |
| Technical Score | Number | Precision: 0, 0-100 | Technical fit score |
| Experience Score | Number | Precision: 0, 0-100 | Experience level score |
| Leadership Score | Number | Precision: 0, 0-100 | Leadership capability score |
| Culture Score | Number | Precision: 0, 0-100 | Culture fit score |
| Overall Score | Number | Precision: 0, 0-100 | Overall fit score |
| Reasoning | Long text | | Detailed assessment reasoning |
| Rank | Number | Integer | Ranking for this role |
| Recommendation | Single select | Strong Fit, Moderate Fit, Weak Fit | Final recommendation |
| Status | Single select | Pending, Researching, Complete, Presented, Hired, Passed | Assessment status |
| Button: Run Assessment | Button | | Triggers assessment workflow |
| Created | Created time | | Auto-populated |
| Modified | Last modified time | | Auto-populated |

**Formula Fields (Optional):**

**Display Name** (Formula):
```
{Candidate} & " → " & {Role}
```

**Score Summary** (Formula):
```
"Overall: " & {Overall Score} & " | Tech: " & {Technical Score} & " | Culture: " & {Culture Score}
```

**Button Configuration:**

**"Run Assessment" Button:**
- Label: "Run Assessment"
- Click → Triggers Airtable Automation → Webhook to N8n

**Views:**
- All Assessments (default)
- By Role (group by: Role)
- By Rank (sort by: Rank ascending)
- Top Candidates (filter: Overall Score ≥ 70, sort by: Overall Score desc)
- Pending (filter: Status = Pending)
- Completed (filter: Status = Complete)

---

## Airtable Automations

Create these automations to trigger workflows:

### Automation 1: Generate Role Spec

**Trigger:** When button clicked (Generate Spec)
**Actions:**
1. **Send webhook request**
   - URL: `http://localhost:5678/webhook/generate-role-spec`
   - Method: POST
   - Body:
   ```json
   {
     "role_id": "{Role ID}",
     "trigger": "generate_spec"
   }
   ```

### Automation 2: Assess Candidates

**Trigger:** When button clicked (Assess Candidates or Run Assessment)
**Actions:**
1. **Send webhook request**
   - URL: `http://localhost:5678/webhook/assess-role`
   - Method: POST
   - Body:
   ```json
   {
     "role_id": "{Role ID}",
     "trigger": "assess_candidates"
   }
   ```

---

## Sample Data

### Companies

| Name | Industry | Stage | Status |
|------|----------|-------|--------|
| Anthropic | AI/ML | Series C+ | Active |
| Ramp | FinTech | Series C+ | Active |
| Retool | SaaS | Series B | Active |
| Hex | SaaS | Series B | Active |

### Roles

| Title | Company | Seniority | Status |
|-------|---------|-----------|--------|
| CTO | Anthropic | Executive | Active Searches |
| VP Engineering | Ramp | Executive | Active Searches |
| Head of Product | Retool | Senior | Active Searches |
| CFO | Hex | Executive | Active Searches |

### Candidates

| Name | Current Title | Source | Skills |
|------|---------------|--------|--------|
| Jane Smith | VP Engineering, OpenAI | Portfolio | AI/ML, Python, Leadership |
| John Doe | CTO, Stripe | FirstMark Guild | FinTech, Infrastructure, Leadership |
| Sarah Johnson | Head of Product, Figma | LinkedIn | SaaS, Product, Design |

---

## Setup Instructions

### 1. Create Airtable Base

1. Go to https://airtable.com
2. Create new base: "FirstMark Talent Signal Agent"
3. Create all 4 tables above
4. Configure fields exactly as specified

### 2. Add Sample Data

1. Add 3-5 companies
2. Add 2-3 roles per company
3. Add 10-15 candidates
4. Link some candidates to roles in Assessments table

### 3. Configure Automations

1. Go to Automations tab
2. Create "Generate Role Spec" automation
3. Create "Assess Candidates" automation
4. Test with webhook.site first to verify payload

### 4. Get API Credentials

1. Go to https://airtable.com/create/tokens
2. Create new personal access token
3. Grant permissions: `data.records:read`, `data.records:write`
4. Copy token to `.env` file as `AIRTABLE_API_KEY`

5. Get Base ID:
   - Open base
   - Go to Help → API Documentation
   - Base ID is in URL: `https://airtable.com/app{BASE_ID}/api/docs`
   - Copy to `.env` as `AIRTABLE_BASE_ID`

### 5. Test Connection

```bash
cd backend
source venv/bin/activate
python -c "from services.airtable_client import AirtableClient; client = AirtableClient(); print(client.get_all_roles())"
```

---

## Best Practices

### Field Naming
- Use exact field names (case-sensitive)
- Don't add extra spaces
- Match schema exactly for API compatibility

### Data Entry
- Fill out LinkedIn URLs for better research
- Write detailed bios (helps with assessment)
- Add comprehensive role descriptions

### Workflow
1. Create company
2. Create role with raw description
3. Click "Generate Spec" button
4. Add candidates to Assessments table (link to role)
5. Click "Run Assessment" button on Assessment record
6. Review results in Assessments table

---

## Troubleshooting

**Issue: Button doesn't trigger**
- Check automation is turned ON
- Verify webhook URL is correct
- Test with webhook.site

**Issue: Python can't connect**
- Verify API token permissions
- Check Base ID is correct
- Ensure table names match exactly

**Issue: Missing fields**
- Python expects exact field names
- Check capitalization
- Verify field types match schema

---

## Next Steps

After setting up Airtable:
1. Configure N8n workflows (see N8N_SETUP.md)
2. Connect Python backend
3. Test end-to-end workflow
4. Populate with real data
