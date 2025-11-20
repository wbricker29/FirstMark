# Multi-Agent Orchestration: High-ROI Enhancements

**Focus**: Maximum value, minimum complexity
**Implementation Time**: 4-6 hours
**Philosophy**: Start simple, add complexity only when needed

---

## Design Principles

1. **Immediate Value** - Solve today's orchestration needs, not hypothetical future requirements
2. **Low Complexity** - Prefer files over databases, enhance existing tools over new infrastructure
3. **Zero Setup** - No schema migrations, no configuration files
4. **Human-Readable** - Markdown logs > SQL queries, CLI output > JSON parsing
5. **Build on Existing** - Enhance the 3 existing scripts rather than replace them

---

## Problem → Solution Map

| Pain Point | Current State | High-ROI Solution | Time |
|------------|---------------|-------------------|------|
| "I'm hitting 200k tokens, what do I drop?" | check_context_bounds.py shows total only | **Per-file token breakdown + recommendations** | 1h |
| "Agent failed, what context did I give it?" | Lost in conversation history | **Simple session logs (markdown)** | 30m |
| "How do I synthesize 5 agent outputs?" | Manual CSV input to synthesize_reports.py | **Auto-synthesis from session log** | 1-2h |
| "What agents should I deploy?" | Read docs, plan manually | **Interactive selection wizard** | 1-2h |

**Total**: 4-6 hours

---

## Enhancement 1: Per-File Context Budget Analysis

**Time**: 1 hour
**Complexity**: Low (enhance existing script)
**ROI**: ⭐⭐⭐⭐⭐

### What It Does

Extends `check_context_bounds.py` to show exactly which files consume the most tokens and what to drop if over budget.

### Implementation

**Enhanced Script**: `scripts/check_context_bounds.py`

**New Features**:
1. Per-file token breakdown with percentages
2. Recommendations for files to drop or summarize
3. Shared context identification (same file used by multiple agents)
4. Visual budget bar

### Usage Example

```bash
# Current usage still works
python scripts/check_context_bounds.py \
  --phase 3 \
  --files "spec/requirements.md,lib/types.ts,references/hnsw.md"

# New enhanced output:
┌─────────────────────────────────────────────────────────────┐
│ Context Budget Analysis - Phase 3                          │
├─────────────────────────────────────────────────────────────┤
│ Total: 85,000 / 200,000 tokens (42.5%)                     │
│ [████████████░░░░░░░░░░░░░░░░] 42.5%                       │
└─────────────────────────────────────────────────────────────┘

Per-File Breakdown:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
File                        Tokens    % of Total  Recommendation
────────────────────────────────────────────────────────────────
spec/requirements.md         1,500        1.8%    ✅ KEEP
lib/types.ts                   800        1.0%    ✅ KEEP
references/hnsw.md          82,700       41.4%    ⚠️  OPTIMIZE

Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️  references/hnsw.md (82,700 tokens)
   This file is very large. Consider:

   Option 1: Extract specific sections
   $ grep -A 50 "## Algorithm Overview" references/hnsw.md > hnsw-summary.md
   Estimated savings: ~79,000 tokens

   Option 2: Provide summary instead
   Use LLM to summarize into ~3,000 token overview
   Estimated savings: ~79,700 tokens

Budget Status:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Current budget: 115,000 tokens remaining
✅ Sufficient for deployment
```

**Advanced Features**:

```bash
# Show what's shared across multiple agents
python scripts/check_context_bounds.py \
  --files "file1.ts,file2.ts,file3.ts" \
  --shared-with "agent-1,agent-2"

# Output includes:
Shared Context Opportunity:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
constitution.md (500 tokens) appears in context for:
  - task-implementor
  - systematic-debugger
  - documentation-manager

💡 Tip: This file will be loaded 3 times (1,500 total tokens)
   Consider: Reference it once in orchestration briefing
   Savings: 1,000 tokens
```

### Code Changes

**File**: `scripts/check_context_bounds.py`

**New Functions**:
```python
def analyze_per_file_usage(file_paths: list[str]) -> list[dict]:
    """Analyze token usage per file with recommendations."""
    results = []
    for path in file_paths:
        char_count, _ = read_file_content(path)
        tokens = estimate_tokens(char_count)

        recommendation = "KEEP"
        tips = []

        if tokens > 50000:
            recommendation = "OPTIMIZE"
            tips.append(f"File is very large ({tokens:,} tokens)")
            tips.append("Consider extracting specific sections")
        elif tokens > 20000:
            recommendation = "REVIEW"
            tips.append(f"File is large ({tokens:,} tokens)")

        results.append({
            "path": path,
            "tokens": tokens,
            "percentage": 0,  # calculated later
            "recommendation": recommendation,
            "tips": tips
        })

    return results

def format_budget_bar(percentage: float, width: int = 40) -> str:
    """Generate visual progress bar for budget usage."""
    filled = int(percentage / 100 * width)
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}] {percentage:.1f}%"

def generate_optimization_tips(file_analysis: dict) -> list[str]:
    """Generate specific optimization tips for large files."""
    tips = []

    if file_analysis["tokens"] > 50000:
        # Suggest section extraction
        tips.append(
            f"Option 1: Extract specific sections\n"
            f"   $ grep -A 50 '## Section Name' {file_analysis['path']} > summary.md\n"
            f"   Estimated savings: ~{file_analysis['tokens'] - 3000:,} tokens"
        )

        # Suggest summarization
        tips.append(
            f"Option 2: Provide summary instead\n"
            f"   Use LLM to summarize into ~3,000 token overview\n"
            f"   Estimated savings: ~{file_analysis['tokens'] - 3000:,} tokens"
        )

    return tips
```

---

## Enhancement 2: Simple Session Logs

**Time**: 30 minutes
**Complexity**: Very Low (write markdown files)
**ROI**: ⭐⭐⭐⭐⭐

### What It Does

Automatically creates human-readable markdown logs for each orchestration session. No database, no schema, just files.

### Implementation

**New Script**: `scripts/session_logger.py`

**Storage Location**: `.claude/orchestration/sessions/`

**Log Format**: `session-{timestamp}-{short-description}.md`

### Usage Example

```bash
# Start new session
python scripts/session_logger.py start \
  --scope "Implement vector search feature" \
  --session-id "orch-2025-01-17-001"

# Creates: .claude/orchestration/sessions/session-2025-01-17-001-vector-search.md

# Log agent deployment (before deploying)
python scripts/session_logger.py log-deployment \
  --session-id "orch-2025-01-17-001" \
  --agent-type "task-implementor" \
  --scope "Implement HNSW algorithm" \
  --context-files "spec/requirements.md,lib/types.ts,references/hnsw.md" \
  --context-tokens 5300

# Log completion (after agent returns)
python scripts/session_logger.py log-completion \
  --session-id "orch-2025-01-17-001" \
  --agent-type "task-implementor" \
  --deliverables "lib/vector-search.ts,tests/vector-search.test.ts" \
  --success true

# View session log
cat .claude/orchestration/sessions/session-2025-01-17-001-vector-search.md
```

### Log File Format

```markdown
# Orchestration Session: Implement vector search feature

**Session ID**: orch-2025-01-17-001
**Started**: 2025-01-17 10:00:00
**Status**: In Progress

---

## Session Scope

Implement vector search feature with HNSW algorithm, including tests and documentation.

---

## Agent Deployments

### 1. task-implementor (10:05:23)

**Execution ID**: exec-001
**Scope**: Implement HNSW algorithm
**Model**: sonnet

**Context Provided** (5,300 tokens total):
- `spec/requirements.md` - 1,500 tokens
- `lib/types.ts` - 800 tokens
- `references/hnsw-algorithm.md` - 3,000 tokens

**Deployment Command**:
```
Task tool with subagent_type=task-implementor
```

**Status**: ✅ Completed (10:32:15, duration: 27 min)

**Deliverables**:
- `lib/vector-search.ts` - 150 lines added
- `tests/vector-search.test.ts` - 80 lines added

**Validation Results**:
- ✅ Format check passed
- ✅ Lint check passed
- ✅ Type check passed
- ✅ Tests passed (8/8)
- ✅ Coverage: 85%

**Notes**:
Agent implemented HNSW with configurable M and efConstruction parameters. Tests cover basic insert, search, and edge cases.

---

### 2. documentation-manager (10:35:42)

**Execution ID**: exec-002
**Scope**: Update API documentation for vector search
**Model**: sonnet

**Context Provided** (2,800 tokens total):
- `lib/vector-search.ts` - 1,800 tokens (lines 1-120 only)
- `docs/api-template.md` - 1,000 tokens

**Dependencies**:
- ⬅️ Requires completion of exec-001 (task-implementor)

**Status**: ✅ Completed (10:42:33, duration: 7 min)

**Deliverables**:
- `docs/vector-search-api.md` - New file created

---

## Session Summary

**Agents Deployed**: 2
**Total Duration**: 42 minutes
**Deliverables**: 3 files created/modified
**Overall Status**: ✅ All agents completed successfully

**Context Budget Used**: 8,100 / 200,000 tokens (4.1%)

**Next Steps**:
- Run integration tests with vector-search.ts
- Deploy to staging environment
- Update changelog

---

**Session Completed**: 2025-01-17 10:45:00
```

### Code Implementation

**File**: `scripts/session_logger.py`

```python
#!/usr/bin/env python3
"""Simple session logger for multi-agent orchestration."""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

SESSION_DIR = Path(".claude/orchestration/sessions")

def ensure_session_dir():
    """Ensure session directory exists."""
    SESSION_DIR.mkdir(parents=True, exist_ok=True)

def get_session_path(session_id: str) -> Path:
    """Get path for session log file."""
    # Find existing session file or create new one
    for path in SESSION_DIR.glob(f"session-{session_id}*.md"):
        return path

    # Create new with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M")
    return SESSION_DIR / f"session-{session_id}-{timestamp}.md"

def start_session(session_id: str, scope: str) -> None:
    """Start new orchestration session."""
    ensure_session_dir()
    path = get_session_path(session_id)

    content = f"""# Orchestration Session: {scope}

**Session ID**: {session_id}
**Started**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Status**: In Progress

---

## Session Scope

{scope}

---

## Agent Deployments

"""
    path.write_text(content)
    print(f"Session started: {path}")

def log_deployment(
    session_id: str,
    agent_type: str,
    scope: str,
    context_files: str,
    context_tokens: int
) -> None:
    """Log agent deployment."""
    path = get_session_path(session_id)

    if not path.exists():
        print(f"Error: Session {session_id} not found", file=sys.stderr)
        sys.exit(1)

    # Count existing deployments
    content = path.read_text()
    deployment_count = content.count("###") - content.count("### Session Summary")

    timestamp = datetime.now().strftime("%H:%M:%S")

    deployment_entry = f"""
### {deployment_count + 1}. {agent_type} ({timestamp})

**Scope**: {scope}
**Model**: sonnet

**Context Provided** ({context_tokens:,} tokens total):
"""

    # Add context files
    for file_spec in context_files.split(","):
        deployment_entry += f"- `{file_spec.strip()}`\n"

    deployment_entry += f"""
**Status**: 🔄 Running...

---
"""

    # Insert before "## Session Summary" or append
    if "## Session Summary" in content:
        content = content.replace("## Session Summary", deployment_entry + "\n## Session Summary")
    else:
        content += deployment_entry

    path.write_text(content)
    print(f"Logged deployment: {agent_type}")

def log_completion(
    session_id: str,
    agent_type: str,
    deliverables: str,
    success: bool
) -> None:
    """Log agent completion."""
    path = get_session_path(session_id)
    content = path.read_text()

    # Find the last occurrence of agent_type
    # Update status from Running to Completed
    # Add deliverables section

    status = "✅ Completed" if success else "❌ Failed"
    timestamp = datetime.now().strftime("%H:%M:%S")

    deliverables_section = f"""
**Status**: {status} ({timestamp})

**Deliverables**:
"""

    for deliverable in deliverables.split(","):
        deliverables_section += f"- `{deliverable.strip()}`\n"

    # Simple replacement (in production, would use more robust parsing)
    content = content.replace("**Status**: 🔄 Running...", deliverables_section)

    path.write_text(content)
    print(f"Logged completion: {agent_type}")

def main():
    parser = argparse.ArgumentParser(description="Session logger for orchestration")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Start session
    start_parser = subparsers.add_parser("start")
    start_parser.add_argument("--session-id", required=True)
    start_parser.add_argument("--scope", required=True)

    # Log deployment
    deploy_parser = subparsers.add_parser("log-deployment")
    deploy_parser.add_argument("--session-id", required=True)
    deploy_parser.add_argument("--agent-type", required=True)
    deploy_parser.add_argument("--scope", required=True)
    deploy_parser.add_argument("--context-files", required=True)
    deploy_parser.add_argument("--context-tokens", type=int, required=True)

    # Log completion
    complete_parser = subparsers.add_parser("log-completion")
    complete_parser.add_argument("--session-id", required=True)
    complete_parser.add_argument("--agent-type", required=True)
    complete_parser.add_argument("--deliverables", required=True)
    complete_parser.add_argument("--success", type=bool, default=True)

    args = parser.parse_args()

    if args.command == "start":
        start_session(args.session_id, args.scope)
    elif args.command == "log-deployment":
        log_deployment(
            args.session_id,
            args.agent_type,
            args.scope,
            args.context_files,
            args.context_tokens
        )
    elif args.command == "log-completion":
        log_completion(
            args.session_id,
            args.agent_type,
            args.deliverables,
            args.success
        )

if __name__ == "__main__":
    main()
```

### Benefits

- ✅ Human-readable with any text editor
- ✅ Version-controllable (commit session logs with code)
- ✅ Searchable with grep: `grep -r "systematic-debugger" .claude/orchestration/`
- ✅ Zero setup - just write files
- ✅ Natural audit trail
- ✅ Can review months later without database

---

## Enhancement 3: Auto-Synthesis Helper

**Time**: 1-2 hours
**Complexity**: Low
**ROI**: ⭐⭐⭐⭐

### What It Does

Reads session log and automatically feeds data to existing `synthesize_reports.py`. No more manual CSV input.

### Implementation

**New Script**: `scripts/auto_synthesize.py`

### Usage Example

```bash
# Auto-synthesize from session log
python scripts/auto_synthesize.py \
  --session .claude/orchestration/sessions/session-2025-01-17-001-vector-search.md \
  --template assets/synthesis-report.tmpl \
  --output final-report.md

# Output: Reads session log, extracts agent names and deliverables,
# calls synthesize_reports.py automatically
```

### How It Works

1. Parse session markdown file
2. Extract agent types from `### N. agent-type` headers
3. Extract deliverables from **Deliverables** sections
4. Call existing `synthesize_reports.py` with extracted data
5. Optionally enhance report with context budget info from session

### Code Implementation

**File**: `scripts/auto_synthesize.py`

```python
#!/usr/bin/env python3
"""Auto-synthesis from session logs."""

import argparse
import re
import subprocess
import sys
from pathlib import Path

def parse_session_log(session_path: Path) -> dict:
    """Parse session log to extract agents and deliverables."""
    content = session_path.read_text()

    agents = []
    deliverables = []

    # Extract agent deployments
    agent_pattern = r"### \d+\. (\S+) \(\d+:\d+:\d+\)"
    for match in re.finditer(agent_pattern, content):
        agents.append(match.group(1))

    # Extract deliverables
    deliverable_pattern = r"- `([^`]+)`"
    in_deliverables = False
    for line in content.split("\n"):
        if "**Deliverables**:" in line:
            in_deliverables = True
            continue
        if in_deliverables and line.startswith("- `"):
            match = re.search(deliverable_pattern, line)
            if match:
                deliverables.append(match.group(1))
        elif in_deliverables and not line.startswith("- "):
            in_deliverables = False

    return {
        "agents": agents,
        "deliverables": deliverables
    }

def main():
    parser = argparse.ArgumentParser(
        description="Auto-synthesize report from session log"
    )
    parser.add_argument("--session", required=True, help="Path to session log")
    parser.add_argument("--template", default=None, help="Report template")
    parser.add_argument("--output", default=None, help="Output file")

    args = parser.parse_args()

    session_path = Path(args.session)
    if not session_path.exists():
        print(f"Error: Session log not found: {args.session}", file=sys.stderr)
        sys.exit(1)

    # Parse session log
    data = parse_session_log(session_path)

    print(f"Found {len(data['agents'])} agents")
    print(f"Found {len(data['deliverables'])} deliverables")

    # Build synthesize_reports.py command
    cmd = [
        "python3",
        "scripts/synthesize_reports.py",
        "--agents", ",".join(data["agents"]),
        "--deliverables", ",".join(data["deliverables"])
    ]

    if args.template:
        cmd.extend(["--template", args.template])

    if args.output:
        cmd.extend(["--output", args.output])

    # Execute
    print(f"Calling: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        print("✅ Synthesis complete")
        if not args.output:
            print(result.stdout)
    else:
        print(f"❌ Synthesis failed: {result.stderr}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

---

## Enhancement 4: Agent Selection Wizard

**Time**: 1-2 hours
**Complexity**: Medium
**ROI**: ⭐⭐⭐⭐⭐

### What It Does

Interactive CLI that helps plan orchestration by recommending agents based on task description.

### Implementation

**New Script**: `scripts/plan_orchestration.py`

### Usage Example

```bash
python scripts/plan_orchestration.py

# Interactive prompts:
┌─────────────────────────────────────────────────┐
│ Multi-Agent Orchestration Planner              │
└─────────────────────────────────────────────────┘

What are you trying to accomplish?
> Implement vector search feature with HNSW algorithm

Analyzing task... ✓

Identified Components:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Core implementation (algorithm, data structures)
2. Unit tests
3. Integration tests
4. API documentation

Recommended Agents:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Agent 1: task-implementor
  Scope: Implement HNSW algorithm core
  Why: Handles algorithm implementation, data structures
  Estimated tokens: 5,000-10,000

Agent 2: task-implementor
  Scope: Write unit tests for vector search
  Why: Handles test creation
  Dependencies: Agent 1 must complete first
  Estimated tokens: 3,000-5,000

Agent 3: documentation-manager
  Scope: Update API documentation
  Why: Documents new vector search API
  Dependencies: Agent 1 must complete first
  Estimated tokens: 2,000-3,000

Dependency Graph:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    Agent 1 (task-implementor)
    ├─→ Agent 2 (task-implementor)
    └─→ Agent 3 (documentation-manager)

Execution Strategy: Sequential (dependencies exist)
Total Estimated Tokens: 10,000-18,000 (5-9% of budget)

Validation:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Dependencies are acyclic
✅ Token budget is manageable
✅ No conflicting agent scopes

Proceed with this plan? (y/n/edit)
> y

Starting orchestration session...
Session ID: orch-2025-01-17-001
Session log: .claude/orchestration/sessions/session-2025-01-17-001-vector-search.md

Ready to deploy Agent 1!
```

### Code Implementation

**File**: `scripts/plan_orchestration.py`

```python
#!/usr/bin/env python3
"""Interactive orchestration planner."""

import argparse
import re
import sys
from datetime import datetime
from typing import List, Dict

# Agent type knowledge base
AGENT_CAPABILITIES = {
    "task-implementor": {
        "keywords": ["implement", "create", "build", "develop", "code", "feature"],
        "description": "Implements code, creates features, builds components",
        "typical_scope": "Implementation tasks, feature development"
    },
    "systematic-debugger": {
        "keywords": ["debug", "fix", "error", "bug", "issue", "failing"],
        "description": "Debugs errors, fixes bugs, investigates failures",
        "typical_scope": "Bug fixes, error investigation"
    },
    "code-prettier": {
        "keywords": ["refactor", "clean", "format", "style", "readability"],
        "description": "Refactors code, improves readability, no functional changes",
        "typical_scope": "Code cleanup, formatting, refactoring"
    },
    "documentation-manager": {
        "keywords": ["document", "docs", "api", "readme", "guide"],
        "description": "Updates documentation, maintains consistency",
        "typical_scope": "Documentation updates, API docs, guides"
    },
    "principle-evaluator": {
        "keywords": ["validate", "check", "compliance", "standards", "quality"],
        "description": "Validates KISS/YAGNI adherence, quality checks",
        "typical_scope": "Principle validation, quality gates"
    }
}

def analyze_task(description: str) -> List[str]:
    """Analyze task description and recommend agents."""
    description_lower = description.lower()
    recommendations = []

    for agent_type, info in AGENT_CAPABILITIES.items():
        score = 0
        for keyword in info["keywords"]:
            if keyword in description_lower:
                score += 1

        if score > 0:
            recommendations.append({
                "agent_type": agent_type,
                "score": score,
                "description": info["description"]
            })

    # Sort by score
    recommendations.sort(key=lambda x: x["score"], reverse=True)

    return recommendations

def detect_components(description: str) -> List[str]:
    """Detect task components."""
    components = []

    patterns = {
        "implementation": r"implement|create|build",
        "tests": r"test|testing|unit test|integration",
        "documentation": r"document|docs|api doc",
        "debugging": r"fix|debug|error|bug"
    }

    for component, pattern in patterns.items():
        if re.search(pattern, description, re.IGNORECASE):
            components.append(component)

    return components

def estimate_tokens(scope: str) -> tuple:
    """Estimate token range for scope."""
    # Simple heuristic based on scope length
    if "implement" in scope.lower() or "create" in scope.lower():
        return (5000, 10000)
    elif "test" in scope.lower():
        return (3000, 5000)
    elif "document" in scope.lower():
        return (2000, 3000)
    else:
        return (1000, 5000)

def print_plan(agents: List[Dict], components: List[str]):
    """Print formatted orchestration plan."""
    print("\n" + "━" * 60)
    print("Identified Components:")
    print("━" * 60)
    for i, component in enumerate(components, 1):
        print(f"{i}. {component.capitalize()}")

    print("\n" + "━" * 60)
    print("Recommended Agents:")
    print("━" * 60)

    for i, agent in enumerate(agents, 1):
        tokens_min, tokens_max = estimate_tokens(agent.get("scope", ""))

        print(f"\nAgent {i}: {agent['type']}")
        print(f"  Scope: {agent.get('scope', 'TBD')}")
        print(f"  Why: {agent.get('reason', 'Based on task analysis')}")

        if agent.get("dependencies"):
            print(f"  Dependencies: {', '.join(agent['dependencies'])}")

        print(f"  Estimated tokens: {tokens_min:,}-{tokens_max:,}")

    # Calculate totals
    total_min = sum(estimate_tokens(a.get("scope", ""))[0] for a in agents)
    total_max = sum(estimate_tokens(a.get("scope", ""))[1] for a in agents)

    print("\n" + "━" * 60)
    print(f"Total Estimated Tokens: {total_min:,}-{total_max:,}")
    print(f"Budget Usage: {total_min/200000*100:.1f}%-{total_max/200000*100:.1f}%")

def main():
    print("┌" + "─" * 58 + "┐")
    print("│ Multi-Agent Orchestration Planner" + " " * 24 + "│")
    print("└" + "─" * 58 + "┘\n")

    # Get task description
    description = input("What are you trying to accomplish?\n> ")

    if not description:
        print("Error: Task description required", file=sys.stderr)
        sys.exit(1)

    print("\nAnalyzing task... ✓\n")

    # Detect components
    components = detect_components(description)

    # Get recommendations
    recommendations = analyze_task(description)

    # Build agent plan (simplified - in production would be more sophisticated)
    agents = []

    if any("implement" in c for c in components):
        agents.append({
            "type": "task-implementor",
            "scope": "Core implementation",
            "reason": "Handles algorithm implementation, data structures"
        })

    if any("test" in c for c in components):
        agents.append({
            "type": "task-implementor",
            "scope": "Write tests",
            "reason": "Handles test creation",
            "dependencies": ["Agent 1"]
        })

    if any("document" in c for c in components):
        agents.append({
            "type": "documentation-manager",
            "scope": "Update documentation",
            "reason": "Documents new API/features",
            "dependencies": ["Agent 1"]
        })

    # Print plan
    print_plan(agents, components)

    # Ask for confirmation
    print("\n" + "━" * 60)
    response = input("Proceed with this plan? (y/n/edit)\n> ")

    if response.lower() == 'y':
        # Create session
        session_id = f"orch-{datetime.now().strftime('%Y-%m-%d-%H%M')}"
        print(f"\nStarting orchestration session...")
        print(f"Session ID: {session_id}")
        print(f"\n✅ Ready to deploy agents!")
    else:
        print("Plan cancelled.")

if __name__ == "__main__":
    main()
```

---

## Implementation Roadmap

### Week 1: Core Enhancements (3-4 hours)

**Day 1** (1.5 hours):
- ✅ Enhanced `check_context_bounds.py` with per-file breakdown
- ✅ Add recommendations engine
- ✅ Add visual budget bar

**Day 2** (1.5 hours):
- ✅ Implement `session_logger.py`
- ✅ Test session log creation and updates
- ✅ Create example session logs

**Day 3** (1 hour):
- ✅ Implement `auto_synthesize.py`
- ✅ Test integration with existing `synthesize_reports.py`

### Week 2: Planning Tools (1-2 hours)

**Day 4** (1-2 hours):
- ✅ Implement `plan_orchestration.py`
- ✅ Build agent recommendation engine
- ✅ Add dependency detection

### Week 2: Documentation & Validation (1 hour)

**Day 5** (1 hour):
- ✅ Update SKILL.md with new tools
- ✅ Create usage examples
- ✅ Run validation with skill-creator-unified

**Total**: 4-6 hours

---

## Integration with Existing Workflow

### Updated Phase 3: Execute

**Before** (manual):
```
1. Manually track which agents to deploy
2. Deploy via Task tool
3. Manually note what context was provided
4. Wait for completion
5. Manually collect outputs
```

**After** (enhanced):
```bash
# 1. Plan orchestration (NEW)
python scripts/plan_orchestration.py
# Interactive wizard recommends agents

# 2. Start session logging (NEW)
python scripts/session_logger.py start \
  --scope "Implement vector search" \
  --session-id "orch-2025-01-17-001"

# 3. Check context budget with breakdown (ENHANCED)
python scripts/check_context_bounds.py \
  --files "spec/requirements.md,lib/types.ts,references/hnsw.md" \
  --show-breakdown
# Shows per-file usage, recommends optimizations

# 4. Log deployment (NEW)
python scripts/session_logger.py log-deployment \
  --session-id "orch-2025-01-17-001" \
  --agent-type "task-implementor" \
  --scope "Implement HNSW" \
  --context-files "spec/requirements.md,lib/types.ts" \
  --context-tokens 5300

# 5. Deploy agent via Task tool
# (unchanged - use Claude Code Task tool)

# 6. Log completion (NEW)
python scripts/session_logger.py log-completion \
  --session-id "orch-2025-01-17-001" \
  --agent-type "task-implementor" \
  --deliverables "lib/vector-search.ts,tests/vector-search.test.ts" \
  --success true

# 7. Auto-synthesize report (NEW)
python scripts/auto_synthesize.py \
  --session .claude/orchestration/sessions/session-2025-01-17-001.md \
  --output final-report.md
```

---

## Success Metrics

### Immediate (Day 1)

- ✅ Zero context overflow errors (caught by enhanced budget tool)
- ✅ 100% of orchestrations logged (session logs created)
- ✅ Reduce synthesis time from 5 min to 30 sec (auto-synthesis)

### Short-term (Week 1)

- ✅ 50% reduction in time planning orchestrations (selection wizard)
- ✅ Human-readable audit trail (review session logs without tools)
- ✅ Identify and eliminate 15-25% token waste (per-file breakdown)

### Long-term (Month 1)

- ✅ Learn from history: grep session logs for patterns
- ✅ Share orchestration strategies: commit session logs to git
- ✅ Onboard new users: session logs as examples

---

## Why This Approach Has Higher ROI

### vs. SQLite Database

| SQLite Approach | Simple Files Approach |
|-----------------|----------------------|
| 2-3 hours setup | 30 min implementation |
| Requires SQL queries | `cat` or text editor |
| Schema migrations | No maintenance |
| Not git-friendly | Version controllable |
| Debugging: SQL client | Debugging: grep/ripgrep |

### vs. Full Context Manager

| Full Context Manager | Enhanced Budget Tool |
|---------------------|---------------------|
| Bundle creation/storage | Show breakdown + tips |
| Deduplication engine | Identify shared files |
| 2-3 hours implementation | 1 hour enhancement |
| New concepts to learn | Extends existing tool |

### vs. Manual Synthesis

| Manual Input | Auto-Synthesis |
|--------------|----------------|
| User provides CSVs | Parse from session log |
| Error-prone | Automated |
| 5 min per synthesis | 30 sec per synthesis |

---

## Future Enhancements (Only If Needed)

**If you later discover you need more:**

1. **Session Database** (2-3 hours)
   - Migrate from markdown to SQLite
   - Keep markdown as export format
   - Build only when historical queries become critical

2. **Context Bundle Storage** (1-2 hours)
   - Persist prepared context bundles
   - Enable "replay with same context" debugging
   - Build only when debugging context issues frequently

3. **Agent Analytics** (2-3 hours)
   - Parse session logs for patterns
   - "Which agents fail most often?"
   - "What context bundles work best?"
   - Build only when you have 20+ orchestrations to analyze

**Start simple. Add complexity only when pain is real.**

---

## Questions Answered

**Q: "How do I review what context I gave an agent?"**
A: `cat .claude/orchestration/sessions/session-2025-01-17-001.md` → See full context list

**Q: "I'm hitting 200k tokens, what do I drop?"**
A: `python scripts/check_context_bounds.py --show-breakdown` → See per-file usage + recommendations

**Q: "How do I synthesize 5 agent outputs?"**
A: `python scripts/auto_synthesize.py --session session-2025-01-17-001.md` → Automatic

**Q: "What agents should I deploy for X?"**
A: `python scripts/plan_orchestration.py` → Interactive wizard

**Q: "Can I search past orchestrations?"**
A: `grep -r "systematic-debugger" .claude/orchestration/` → Full-text search

**Q: "Can I share my orchestration strategy?"**
A: `git add .claude/orchestration/sessions/*.md && git commit` → Version controlled

---

## Summary

**Total Implementation**: 4-6 hours
**Total New Scripts**: 3 (session_logger, auto_synthesize, plan_orchestration)
**Enhanced Scripts**: 1 (check_context_bounds)
**New Infrastructure**: 0 (just files)

**Immediate Value**:
- ✅ Context budget optimization (prevent overflow)
- ✅ Session audit trail (debug failures)
- ✅ Automated synthesis (save time)
- ✅ Planning assistance (avoid mistakes)

**Philosophy**: Solve today's problems today. Build complex infrastructure only when simple solutions fail.
