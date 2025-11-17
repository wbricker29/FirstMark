# N8n Setup Guide

Guide for setting up N8n locally to orchestrate workflows between Airtable and Python backend.

## Quick Start

### 1. Install N8n Locally

```bash
# Option 1: Using npx (no installation needed)
npx n8n

# Option 2: Install globally
npm install n8n -g
n8n

# N8n will start at http://localhost:5678
```

### 2. Initial Setup

1. Open browser to `http://localhost:5678`
2. Create account (local only, no cloud sync needed)
3. You're ready to create workflows!

---

## Create Workflows

### Workflow 1: Generate Role Spec

This workflow receives webhook from Airtable and triggers role spec generation.

**Nodes:**

1. **Webhook Node**
   - Name: "Airtable Trigger"
   - Webhook Path: `generate-role-spec`
   - Method: POST
   - Response Mode: "When Last Node Finishes"

2. **HTTP Request Node**
   - Name: "Call Python API"
   - Method: POST
   - URL: `http://localhost:8000/generate-role-spec`
   - Body:
   ```json
   {
     "role_id": "{{ $json.role_id }}"
   }
   ```

3. **Set Node** (Optional)
   - Name: "Format Response"
   - Keep only relevant fields

**Webhook URL:** `http://localhost:5678/webhook/generate-role-spec`

---

### Workflow 2: Assess Candidates

This workflow orchestrates the complete assessment workflow.

**Nodes:**

1. **Webhook Node**
   - Name: "Airtable Trigger"
   - Webhook Path: `assess-role`
   - Method: POST
   - Response Mode: "When Last Node Finishes"

2. **HTTP Request Node**
   - Name: "Trigger Assessment"
   - Method: POST
   - URL: `http://localhost:8000/assess-role`
   - Body:
   ```json
   {
     "role_id": "{{ $json.role_id }}",
     "candidate_ids": "{{ $json.candidate_ids }}"
   }
   ```
   - Timeout: 300000 (5 minutes - assessments can be slow)

3. **Set Node**
   - Name: "Extract Results"
   - Set fields for response

**Webhook URL:** `http://localhost:5678/webhook/assess-role`

---

### Workflow 3: Enhanced with Airtable Integration (Advanced)

For more direct integration, you can use N8n's Airtable nodes to read/write directly.

**Nodes:**

1. **Webhook Trigger**
2. **Airtable Node (Read)**
   - Operation: Get
   - Table: Roles
   - Record ID: `{{ $json.role_id }}`

3. **HTTP Request to Python**
4. **Airtable Node (Update)**
   - Operation: Update
   - Table: Roles
   - Record ID: `{{ $json.role_id }}`
   - Fields: Generated Spec, Status

---

## N8n Configuration

### Environment Variables (Optional)

Create `.n8n/config` file:

```bash
export N8N_BASIC_AUTH_ACTIVE=true
export N8N_BASIC_AUTH_USER=admin
export N8N_BASIC_AUTH_PASSWORD=your_password

export N8N_HOST=localhost
export N8N_PORT=5678
export N8N_PROTOCOL=http
```

### Credentials Setup

If using Airtable nodes directly:

1. Go to Credentials in N8n
2. Add "Airtable API" credential
3. Enter your Airtable API key

---

## Workflow Templates

### Template: Simple Webhook → Python API

```json
{
  "nodes": [
    {
      "parameters": {
        "path": "workflow-name",
        "responseMode": "lastNode",
        "options": {}
      },
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "position": [250, 300]
    },
    {
      "parameters": {
        "method": "POST",
        "url": "http://localhost:8000/endpoint",
        "options": {},
        "bodyParametersJson": "={{ $json }}"
      },
      "name": "HTTP Request",
      "type": "n8n-nodes-base.httpRequest",
      "position": [450, 300]
    }
  ],
  "connections": {
    "Webhook": {
      "main": [
        [
          {
            "node": "HTTP Request",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  }
}
```

---

## Testing Workflows

### Test with curl

```bash
# Test Generate Role Spec
curl -X POST http://localhost:5678/webhook/generate-role-spec \
  -H "Content-Type: application/json" \
  -d '{"role_id": "rec123456"}'

# Test Assess Candidates
curl -X POST http://localhost:5678/webhook/assess-role \
  -H "Content-Type: application/json" \
  -d '{"role_id": "rec123456", "candidate_ids": ["recABC", "recDEF"]}'
```

### Test from Airtable

1. Create automation in Airtable
2. Set webhook URL to N8n webhook
3. Click button in Airtable
4. Check N8n execution log

---

## N8n Best Practices

### Error Handling

Add error workflow:

1. **On Workflow Error** trigger
2. **Airtable Update** - Set status to "Error"
3. **Send Email** (optional) - Notify on failure

### Logging

Enable execution logging:
- Settings → Workflows → Save execution data: All
- View executions in "Executions" tab

### Performance

For long-running workflows:
- Increase timeout on HTTP Request nodes
- Use "Response Mode: When Last Node Finishes"
- Consider async patterns for very long operations

---

## Architecture Patterns

### Pattern 1: N8n as Thin Trigger Layer (Recommended)

```
Airtable Button
  ↓ Webhook
N8n (minimal logic)
  ↓ HTTP POST
Python Backend (heavy lifting)
  ↓ Direct write
Airtable (results)
```

**Pros:**
- Fast N8n execution
- Complex logic in Python
- Easy to debug

### Pattern 2: N8n as Orchestrator

```
Airtable Button
  ↓ Webhook
N8n reads from Airtable
  ↓ Multiple HTTP calls to Python
  ↓ Data transformation
N8n writes to Airtable
```

**Pros:**
- Visible workflow in N8n
- Can add conditional logic
- Good for demos

---

## Deployment

### Local Development (Recommended for Demo)

```bash
# Terminal 1: Python backend
cd backend
source venv/bin/activate
uvicorn api.main:app --reload --port 8000

# Terminal 2: N8n
npx n8n
```

### Production (Railway)

If deploying to Railway:

1. **Python Backend:**
   ```bash
   railway init
   railway up
   # Note the URL: https://your-app.railway.app
   ```

2. **Update N8n workflows:**
   - Change `http://localhost:8000` to Railway URL
   - Keep N8n local or deploy separately

3. **Update Airtable webhooks:**
   - Point to Railway-hosted Python API
   - Or keep N8n local and update Python URL in N8n

---

## Troubleshooting

### Issue: Webhook not receiving data

1. Check N8n is running
2. Test webhook URL with curl
3. Verify Airtable automation is ON
4. Check webhook path matches exactly

### Issue: Python API not responding

1. Check Python backend is running (`http://localhost:8000/health`)
2. Verify port 8000 is not blocked
3. Check logs for errors

### Issue: Timeout errors

1. Increase timeout on HTTP Request node (default: 5 minutes)
2. Consider making workflow async
3. Check Python backend logs for slow operations

### Issue: N8n port 5678 already in use

```bash
# Find process using port
lsof -i :5678

# Kill process
kill -9 <PID>

# Or use different port
N8N_PORT=5679 n8n
```

---

## Next Steps

1. **Start N8n:** `npx n8n`
2. **Create workflows** using templates above
3. **Test with curl** to verify endpoints
4. **Connect to Airtable** via automations
5. **Run end-to-end test** with real data

---

## Resources

- [N8n Documentation](https://docs.n8n.io/)
- [N8n Workflow Templates](https://n8n.io/workflows)
- [N8n Community Forum](https://community.n8n.io/)

For questions, contact Will Bricker.
