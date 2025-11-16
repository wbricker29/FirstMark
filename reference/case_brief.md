# FirstMark AI Product Case Study

---

## The Context

FirstMark's network includes:

- Portfolio company executives
- Members of FirstMark Guilds (role-based peer groups: CTO, CPO, CRO, etc.)
- Broader professional networks (LinkedIn, founders, event attendees)

We want to identify which executives in this extended network could be strong candidates for open roles in our portfolio companies — and surface those insights automatically.

---

## The Challenge

You are designing an AI-powered agent that helps a VC talent team proactively surface **executive matches** for open roles across the portfolio.

Build and demonstrate (conceptually and technically) how this "Talent Signal Agent" could:

1. Integrate data from **structured** (e.g., company + role data, hiring needs) and **unstructured** (e.g., bios, articles, LinkedIn text) sources.
2. Identify and rank potential candidates for given open CTO and CFO roles.
3. Provide a clear **reasoning trail** or explanation for its matches.

Create and use **mock data** (CSV, sample bios, job descriptions, etc.), **public data**, or **synthetic examples** to create your structured and unstructured inputs. The goal is to demonstrate reasoning, architecture, and usability — not data volume. Aka should be enough individual CFO/CTO entries to show the how. This exercise mirrors the real data and decision challenges we face. We don't need a perfect working prototype nor perfect data — we want to see how you think, structure, and communicate a solution.

---

## The Data Inputs

| Type | Example | Description |
|------|---------|-------------|
| **Structured data** | "Mock_Guilds.csv" of mock data of two FirstMark Guilds | Columns: company, role title, location, seniority, function. |
| **Structured data** | "Exec_Network.csv", could be an example of a Partner's connections to fill out additional potential candidates | Columns: name, current title, company, role type (CTO, CRO, etc.), location, LinkedIn URL. |
| **Unstructured data** | Executive bios or press snippets | ~10–20 bios (mock or real) in text format. |
| **Unstructured data** | Job descriptions | Text of 3–5 open portfolio roles for CFO and CTO. |

---

## The Deliverables (Case Response)

The candidate should provide:

### 1. A short write-up or slide deck (1–2 pages):

- Overview of problem framing and agent design
- Description of data sources and architecture
- Key design decisions and tradeoffs
- How they'd extend this in production

### 2. A lightweight prototype (Python / LangChain / LlamaIndex / etc or other relevant tools/workspaces that facilitate agent creation.):

Demonstrate how the agent:

- Ingests mock structured + unstructured data
- Identifies potential matches
- Outputs ranked recommendations with reasoning (e.g., "Jane Doe → strong fit for CFO @ AcmeCo because of prior Series B fundraising experience at consumer startup")

### 3. A brief README or Loom video (optional)

- Explain what's implemented and what's conceptual.

---

## The Evaluation Rubric

| Category | Weight | What "Excellent" Looks Like |
|----------|--------|----------------------------|
| **Product Thinking** | 25% | Clear understanding of VC and talent workflows. Scopes an agent that actually fits how the firm works. Communicates assumptions and value. |
| **Technical Design** | 25% | Uses modern LLM/agent frameworks logically; modular design; thoughtful about retrieval, context, and prompting. |
| **Data Integration** | 20% | Handles structured + unstructured data elegantly (e.g., vector store, metadata joins). Sensible about what's automatable. |
| **Insight Generation** | 20% | Produces useful, explainable, ranked outputs — not just text dumps. Demonstrates reasoning or scoring logic. |
| **Communication & Clarity** | 10% | Clean, clear explanation of what was done, why, and next steps. No jargon for the sake of it. |
