# Talent Signal Agent: FirstMark Case Study

**Author:** [Your Name]
**Date:** [Submission Date]
**Case:** AI Product - Talent Signal Agent

---

## Problem Framing & Agent Design

### Understanding the Problem

[2-3 sentences describing FirstMark's talent team workflow and pain points. Reference guilds, portfolio companies, and the manual nature of current process.]

### Proposed Solution

[2-3 sentences describing your agent design at a high level. What approach did you take and why does it fit this specific use case?]

**Key Assumptions:**
- [Assumption 1 about data availability, quality, or workflow]
- [Assumption 2 about user needs or constraints]
- [Assumption 3 about technical feasibility or scope]

---

## Data Sources & Architecture

### Data Integration Approach

**Structured Data:**
- `mock_guilds.csv` - [What this provides and how you use it]
- `exec_network.csv` - [What this provides and how you use it]
- `open_roles.csv` - [What this provides and how you use it]

**Unstructured Data:**
- `executive_bios.json` - [What this provides and how you use it]
- `job_descriptions/` - [What this provides and how you use it]

### Technical Architecture

[Option 1: Describe in text]
```
1. Data Ingestion → [What happens here]
2. Candidate Filtering → [What happens here]
3. Matching & Scoring → [What happens here]
4. Explanation Generation → [What happens here]
5. Output Ranking → [What happens here]
```

[Option 2: Include simple diagram using Mermaid or ASCII]
```
CSV Data ──┐
           ├──> Data Loader ──> [Next Step] ──> [Final Step]
JSON Data ─┘
```

---

## Key Design Decisions & Tradeoffs

### Decision 1: [e.g., "Simple Prompt Chain vs Agent Pattern"]

**Choice:** [What you chose]
**Rationale:** [Why - reference KISS/YAGNI principles]
**Tradeoff:** [What you gave up by making this choice]

### Decision 2: [e.g., "Keyword Filtering vs Vector Search"]

**Choice:** [What you chose]
**Rationale:** [Why - based on data size, complexity needs]
**Tradeoff:** [What you gave up]

### Decision 3: [e.g., "Output Format"]

**Choice:** [What you chose]
**Rationale:** [Why this format serves the talent team]
**Tradeoff:** [Any limitations]

---

## Production Extension Plan

### What Would Change in Production

**Data Integration:**
- [How you'd connect to real data sources - Affinity CRM, LinkedIn API, etc.]
- [Data quality and normalization pipelines]

**Scalability:**
- [How you'd handle 100s or 1000s of candidates]
- [Performance optimizations needed]

**User Experience:**
- [How talent team would interact with this (UI, API, Slack bot, etc.)]
- [Feedback loops and iteration]

**Monitoring & Improvement:**
- [How you'd measure success]
- [How you'd improve matches over time]

### Immediate Next Steps (if building this)

1. [First priority - e.g., "Validate with talent team on real use cases"]
2. [Second priority - e.g., "Integrate with Affinity CRM for live data"]
3. [Third priority - e.g., "Build feedback mechanism to improve matching"]

---

## Summary

[1-2 sentences summarizing your approach and why it fits FirstMark's needs. End with confidence in the design while acknowledging it's a prototype demonstrating thinking.]

---

*This is a case study prototype demonstrating technical thinking and product design. The implementation prioritizes clarity and explainability over production-readiness.*
