# Alternative Agent Architectures

This directory contains reference implementations of multi-agent systems that use different architectural approaches than Agno.

## DeepResearchAgent-main/

**Source:** https://github.com/DVampire/DeepResearchAgent  
**Paper:** https://arxiv.org/abs/2506.12508

### Architecture

Hierarchical two-layer system:
- **Top Layer:** Planning Agent (coordinates overall workflow)
- **Bottom Layer:** Specialized agents (Deep Analyzer, Deep Researcher, Browser Use, MCP Manager, Tool Calling)

### When to Reference This

1. **Alternative Multi-Agent Pattern:** If Agno's Team approach doesn't fit, this shows hierarchical planning
2. **Browser Automation:** For automated LinkedIn/web scraping
3. **MCP Integration:** Examples of Model Context Protocol tool integration
4. **Task Decomposition:** Planning agent breaks complex tasks into sub-tasks

### Comparison to Agno

| Feature | Agno (Your Choice) | DeepResearchAgent |
|---------|-------------------|-------------------|
| **Architecture** | Team coordination | Hierarchical planning |
| **Setup Complexity** | Simple | Moderate-High |
| **Domain Examples** | ✅ Candilyzer (talent matching) | ❌ Generic research |
| **Research Tools** | Exa + Deep Research API | Browser automation + web search |
| **MCP Support** | Via tools | Native integration |
| **Learning Curve** | Gentle | Steeper |

### Usage

This is for **reference only** - you're already using Agno. Consult this if:
- You need hierarchical task planning patterns
- You want to see MCP integration examples
- You're considering browser automation for data gathering

**Don't switch to this** - Agno is the right choice for your 48-hour timeline.
