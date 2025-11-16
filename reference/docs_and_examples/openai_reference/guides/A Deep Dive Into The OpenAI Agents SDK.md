---
title: A Deep Dive Into The OpenAI Agents SDK
source: https://www.siddharthbharath.com/openai-agents-sdk/
author:
  - "[[Sid]]"
published: 2025-03-13
created: 2025-11-16
description: OpenAI just announced their new Agents SDK. Learn how it works and how to build powerful AI agents with it
tags:
  - clippings
edited: 2025-11-16T11:59
---
March 13, 2025

I’ve been discussing the inevitable progression that LLM companies are taking toward agentic AI capabilities for some time now on my blog and social media.

My [Model Context Protocol series](https://www.siddharthbharath.com/ultimate-guide-to-model-context-protocol-part-1-what-is-mcp/) explored how Claude (and any AI product) can go from a mere chatbot to an AI agent capable of taking actions on your behalf.

OpenAI has also been on this path since launching ChatGPT. They’ve been adding tools like web search, code interpreter, Operator, Deep Research, and so on, to build out ChatGPT’s agentic capabilities.

This week, on March 11, 2025, they took the next step with the release of their Agents SDK, an open-source toolkit designed to make building sophisticated AI agents accessible to developers of all skill levels.

**PS** – I also recommend reading my guide on [How To Design AI Agents](https://www.siddharthbharath.com/ultimate-guide-ai-agents/), where I talk through different architectures and components of effective AI agents.

### Want to build your own AI agents?

Sign up for my newsletter covering everything from the tools, APIs, and frameworks you need, to building and serving your own multi-step AI agents.

<iframe id="hs-form-iframe-0" class="hs-form-iframe" title="Form 0" scrolling="no" width="100%" style="position: static; border: none; display: block; overflow: hidden; width: 100%; height: 320px;" height="320"></iframe>

## What is the Agents SDK?

The OpenAI Agents SDK is a lightweight, Python-based framework for constructing multi-agent workflows. Evolved from their experimental “Swarm” project, this SDK provides a comprehensive solution for developers looking to create AI agents that can reason, use tools, and collaborate with other agents to accomplish complex tasks.

The SDK addresses many of the practical challenges developers face when building AI agents. It standardizes patterns for agent communication, state management, and collaboration, reducing the complexity barrier for creating useful AI applications.

What makes it valuable? Three core concepts:

1. **Agents that think AND act** – Not just LLMs spitting out text, but AI assistants that can make decisions and execute functions
2. **Seamless teamwork through handoffs** – Specialized agents working together, passing the baton when needed
3. **Safety through guardrails** – Because nobody wants their AI going rogue after reading too many YouTube comments

## Architecture and Core Components

The OpenAI Agents SDK is built around several key components that work together to create functional agent systems:

**Agents**: The central entities that make decisions and take actions. The SDK supports various types of agents, from simple LLM-powered agents to complex multi-agent orchestrators.

**Runners**: Components that manage the execution flow of agents, handling the orchestration of messages, events, and state management.

**Tools**: Functions or capabilities that agents can use to perform specific actions, such as searching the web, executing code, or retrieving information from databases.

**Context**: A system that allows you to pass data and dependencies throughout your agent run.

**Handoffs**: The ability for one agent to transfer tasks to another agent, allowing for multi-agent systems.

**Tracing**: A way to visualize and monitor your agents.

Let’s look at each of the components in detail.

## Agents

Agents are the central entities that make decisions and take actions in your AI system.

You define an agent by providing a name, model, instructions, and tools:

- Give them a name (“Customer Support Agent”)
- Provide instructions (“Help users without saying ‘have you tried turning it off and on again?’ more than once per conversation”)
- Choose their “brain” (from quick-and-simple to deep-thinking models)
- Equip them with tools (the digital equivalent of giving someone access to the supply closet)

Pythonfrom openai.agents import Agent researcher = Agent( name=”Customer Support Agent”, model=”gpt-4o”, instructions=”Help users without saying ‘have you tried turning it off and on again?”, tools=\[web\_search, document\_retrieval\] )
```
from openai.agents import Agent

researcher = Agent(
    name="Customer Support Agent",
    model="gpt-4o",
    instructions="Help users without saying 'have you tried turning it off and on again?",
    tools=[web_search, document_retrieval]
)
```

### Model Selection and Settings

Different models have different capabilities and costs. Choose the right model for your agent’s needs:

Pythonfrom agents import Agent, ModelSettings # Fast, cost-effective agent for simple tasks quick\_agent = Agent( name=”Quick Responder”, model=”gpt-4o-mini”, # Fastest, most cost-effective instructions=”Provide quick, helpful responses to simple questions.”, model\_settings=ModelSettings( temperature=0.3, # Lower temperature for consistent responses max\_tokens=150 # Limit response length for quick interactions ) ) # Powerful agent for complex reasoning reasoning\_agent = Agent( name=”Deep Thinker”, model=”o1-preview”, # Most capable for complex reasoning instructions=”Provide thorough analysis and step-by-step reasoning for complex problems.”, model\_settings=ModelSettings( temperature=0.7, # Moderate temperature for balanced creativity # Note: o1 models don’t support max\_tokens in the same way ) ) # Creative agent for content generation creative\_agent = Agent( name=”Creative Writer”, model=”gpt-4o”, # Good balance of capability and speed instructions=”Write engaging, creative content with vivid descriptions.”, model\_settings=ModelSettings( temperature=0.9, # Higher temperature for more creativity top\_p=0.9, # Use nucleus sampling for variety presence\_penalty=0.1 # Encourage topic diversity ) )
```
from agents import Agent, ModelSettings

# Fast, cost-effective agent for simple tasks
quick_agent = Agent(
    name="Quick Responder",
    model="gpt-4o-mini",  # Fastest, most cost-effective
    instructions="Provide quick, helpful responses to simple questions.",
    model_settings=ModelSettings(
        temperature=0.3,  # Lower temperature for consistent responses
        max_tokens=150    # Limit response length for quick interactions
    )
)

# Powerful agent for complex reasoning
reasoning_agent = Agent(
    name="Deep Thinker",
    model="o1-preview",  # Most capable for complex reasoning
    instructions="Provide thorough analysis and step-by-step reasoning for complex problems.",
    model_settings=ModelSettings(
        temperature=0.7,  # Moderate temperature for balanced creativity
        # Note: o1 models don't support max_tokens in the same way
    )
)

# Creative agent for content generation
creative_agent = Agent(
    name="Creative Writer",
    model="gpt-4o",  # Good balance of capability and speed
    instructions="Write engaging, creative content with vivid descriptions.",
    model_settings=ModelSettings(
        temperature=0.9,  # Higher temperature for more creativity
        top_p=0.9,       # Use nucleus sampling for variety
        presence_penalty=0.1  # Encourage topic diversity
    )
)
```

### Output Types and Structured Responses

By default, agents produce plain text outputs. However, you can use the `output_type` parameter to ensure structured, validated outputs that your application can reliably process:

Python\# Define the structure you want the agent to return # Pydantic models provide automatic validation and clear documentation class WeatherReport(BaseModel): city: str temperature: int # Temperature in Celsius conditions: str # Weather conditions (sunny, cloudy, etc.) recommendation: str # What the user should do based on the weather # Create an agent that returns structured data instead of free-form text weather\_agent = Agent( name=”Weather Reporter”, instructions=””” You are a weather reporting agent that provides structured weather information. When users ask about weather, use the get\_weather tool and then format your response to include all required fields: – city: The city name (cleaned up and properly formatted) – temperature: The temperature as an integer – conditions: Brief weather description – recommendation: Practical advice based on the weather Be helpful and specific in your recommendations. “””, output\_type=WeatherReport, # This ensures the response matches our structure tools=\[get\_weather\] )
```
# Define the structure you want the agent to return
# Pydantic models provide automatic validation and clear documentation
class WeatherReport(BaseModel):
    city: str
    temperature: int  # Temperature in Celsius
    conditions: str   # Weather conditions (sunny, cloudy, etc.)
    recommendation: str  # What the user should do based on the weather

# Create an agent that returns structured data instead of free-form text
weather_agent = Agent(
    name="Weather Reporter",
    instructions="""
    You are a weather reporting agent that provides structured weather information.
    
    When users ask about weather, use the get_weather tool and then format your response
    to include all required fields:
    - city: The city name (cleaned up and properly formatted)
    - temperature: The temperature as an integer
    - conditions: Brief weather description
    - recommendation: Practical advice based on the weather
    
    Be helpful and specific in your recommendations.
    """,
    output_type=WeatherReport,  # This ensures the response matches our structure
    tools=[get_weather]
)
```

### Instructions

A quick note on instructions here. In the above example you can see how I’m being very explicit with my instructions. You can go even deeper than that.

Instructions are probably the biggest lever you can pull to influence the behaviour of your agent. This holds whether you’re using an SDK, or a tool like n8n, or coding an agent from scratch.

I could write an entire post on how to create good instructions for agents, and maybe I will one day, but for now you can read [my guide on designing agents](https://www.siddharthbharath.com/ultimate-guide-ai-agents/) for more information.

### Agent Loop

When your agent runs, it enters the “agent loop”, a fancy way of saying it thinks, acts, and repeats until the job is done. The SDK handles the agent loop automatically, managing tool calling, result processing, and iteration:

1. Agent gets input (like “I need help with my subscription”)
2. Agent decides if they need more info or can respond directly
3. If they need info, they use a tool and get results
4. This continues until they reach a final answer

It’s basically the digital version of how I approach cooking: assess situation, realize I need more information, google recipe, realize I’m missing ingredients, order takeout, problem solved.

Pythonfrom openai.agents import Runner<br><br>runner = Runner() result = runner.run(researcher, “What are the latest developments in quantum computing?”) print(result.final\_output)
```
from openai.agents import Runner<br><br>runner = Runner()
result = runner.run(researcher, "What are the latest developments in quantum computing?")
print(result.final_output)
```

## Tools: Extending Your Agent’s Capabilities

Without tools, agents would just be fancy chatbots. Tools are what let your AI reach out into the world and actually *do stuff*.

Creating a tool is as simple as decorating a Python function:

Pythonfrom agents.tool import function\_tool @function\_tool def search\_knowledge\_base(query: str) -> str: # Your code to search a database return “Here’s what I found about ” + query
```
from agents.tool import function_tool

@function_tool
def search_knowledge_base(query: str) -> str:
    # Your code to search a database
    return "Here's what I found about " + query
```

There are two main types:

- **Hosted tools**: Pre-built capabilities like web search (the tools already in your shed)
- **Function tools**: Turn ANY Python function into an agent tool (like going to Home Depot and buying whatever you need)

The beauty is in how naturally the agent decides when to use these tools – it’s not pre-programmed, but rather a decision the LLM makes based on the task at hand.

### Function Tools

The most straightforward way to create tools is by decorating Python functions. The SDK handles all the complex work of schema generation, parameter validation, and integration:

Pythonfrom agents import function\_tool, Agent import requests from typing import Dict, Any # Example 1: External API Integration # This shows how to wrap external services as agent tools @function\_tool def search\_wikipedia(query: str) -> str: “””Search Wikipedia for information about a topic. The agent will see this docstring and understand what this tool does. Clear descriptions help the agent choose the right tool for the task. Args: query: The search term to look up on Wikipedia. Returns: str: A summary of the Wikipedia article. “”” try: # Clean up the query for URL usage clean\_query = query.replace(” “, “\_”) # Call Wikipedia’s REST API – this is a real API call response = requests.get( f”https://en.wikipedia.org/api/rest\_v1/page/summary/{clean\_query}”, headers={‘User-Agent’: ‘OpenAI-Agents-Demo/1.0’} ) if response.status\_code == 200: data = response.json() # Format the response in a user-friendly way return f”\*\*{data\[‘title’\]}\*\*: {data\[‘extract’\]}” elif response.status\_code == 404: return f”Sorry, I couldn’t find a Wikipedia article for ‘{query}’. Try rephrasing your search.” else: return f”Wikipedia search temporarily unavailable (status: {response.status\_code})” except Exception as e: # Always handle errors gracefully in tools return f”Error searching Wikipedia: {str(e)}” # Example 2: Complex Calculations with Structured Output # This demonstrates how to return structured data from tools @function\_tool def calculate\_compound\_interest( principal: float, rate: float, time: int, compound\_frequency: int = 12 ) -> Dict\[str, Any\]: “””Calculate compound interest with detailed breakdown. This tool shows how to handle multiple parameters and return structured data that the agent can interpret and present clearly to users. Args: principal: Initial amount invested (in dollars). rate: Annual interest rate as a percentage (e.g., 5.5 for 5.5%). time: Number of years to calculate. compound\_frequency: How often interest compounds per year (default: 12 for monthly). Returns: dict: Calculation results including final amount and total interest. “”” # Input validation – important for tools that do calculations if principal <= 0: return {“error”: “Principal amount must be positive”} if rate < 0: return {“error”: “Interest rate cannot be negative”} if time <= 0: return {“error”: “Time period must be positive”} if compound\_frequency <= 0: return {“error”: “Compound frequency must be positive”} # Convert percentage to decimal decimal\_rate = rate / 100 # Apply the compound interest formula: A = P(1 + r/n)^(nt) final\_amount = principal \* (1 + decimal\_rate/compound\_frequency) \*\* (compound\_frequency \* time) total\_interest = final\_amount – principal # Return structured data that the agent can easily work with return { “status”: “success”, “calculation”: { “principal”: principal, “final\_amount”: round(final\_amount, 2), “total\_interest”: round(total\_interest, 2), “rate\_percent”: rate, “years”: time, “compound\_frequency”: compound\_frequency }, “summary”: f”${principal:,.2f} grows to ${final\_amount:,.2f} over {time} years at {rate}% annual interest” }
```
from agents import function_tool, Agent
import requests
from typing import Dict, Any

# Example 1: External API Integration
# This shows how to wrap external services as agent tools
@function_tool
def search_wikipedia(query: str) -> str:
    """Search Wikipedia for information about a topic.
    
    The agent will see this docstring and understand what this tool does.
    Clear descriptions help the agent choose the right tool for the task.
    
    Args:
        query: The search term to look up on Wikipedia.
        
    Returns:
        str: A summary of the Wikipedia article.
    """
    try:
        # Clean up the query for URL usage
        clean_query = query.replace(" ", "_")
        
        # Call Wikipedia's REST API - this is a real API call
        response = requests.get(
            f"https://en.wikipedia.org/api/rest_v1/page/summary/{clean_query}",
            headers={'User-Agent': 'OpenAI-Agents-Demo/1.0'}
        )
        
        if response.status_code == 200:
            data = response.json()
            # Format the response in a user-friendly way
            return f"**{data['title']}**: {data['extract']}"
        elif response.status_code == 404:
            return f"Sorry, I couldn't find a Wikipedia article for '{query}'. Try rephrasing your search."
        else:
            return f"Wikipedia search temporarily unavailable (status: {response.status_code})"
    
    except Exception as e:
        # Always handle errors gracefully in tools
        return f"Error searching Wikipedia: {str(e)}"

# Example 2: Complex Calculations with Structured Output
# This demonstrates how to return structured data from tools
@function_tool
def calculate_compound_interest(
    principal: float, 
    rate: float, 
    time: int, 
    compound_frequency: int = 12
) -> Dict[str, Any]:
    """Calculate compound interest with detailed breakdown.
    
    This tool shows how to handle multiple parameters and return structured data
    that the agent can interpret and present clearly to users.
    
    Args:
        principal: Initial amount invested (in dollars).
        rate: Annual interest rate as a percentage (e.g., 5.5 for 5.5%).
        time: Number of years to calculate.
        compound_frequency: How often interest compounds per year (default: 12 for monthly).
        
    Returns:
        dict: Calculation results including final amount and total interest.
    """
    # Input validation - important for tools that do calculations
    if principal <= 0:
        return {"error": "Principal amount must be positive"}
    if rate < 0:
        return {"error": "Interest rate cannot be negative"}
    if time <= 0:
        return {"error": "Time period must be positive"}
    if compound_frequency <= 0:
        return {"error": "Compound frequency must be positive"}
    
    # Convert percentage to decimal
    decimal_rate = rate / 100
    
    # Apply the compound interest formula: A = P(1 + r/n)^(nt)
    final_amount = principal * (1 + decimal_rate/compound_frequency) ** (compound_frequency * time)
    total_interest = final_amount - principal
    
    # Return structured data that the agent can easily work with
    return {
        "status": "success",
        "calculation": {
            "principal": principal,
            "final_amount": round(final_amount, 2),
            "total_interest": round(total_interest, 2),
            "rate_percent": rate,
            "years": time,
            "compound_frequency": compound_frequency
        },
        "summary": f"${principal:,.2f} grows to ${final_amount:,.2f} over {time} years at {rate}% annual interest"
    }
```

### Built-in Tools

The SDK provides several hosted tools that run on OpenAI’s servers, offering powerful capabilities without requiring external API management:

- WebSearchTool: Gives your agent the ability to search the web
- FileSearchTool: Search for information in your database
- CodeInterpreterTool: Lets your agent execute code
- ImageGenerationTool: for generating images on the fly

You just need to import them and use them like any tools:

Pythonfrom agents import Agent, WebSearchTool, FileSearchTool, CodeInterpreterTool
```
from agents import Agent, WebSearchTool, FileSearchTool, CodeInterpreterTool
```

### Agents as Tools

You can use agents as tools for other agents, creating powerful hierarchical systems where specialized agents handle specific domains:

Python\# Create specialized agents that excel at specific tasks # Each agent has focused expertise and tailored instructions # Math specialist – optimized for numerical calculations and explanations math\_agent = Agent( name=”Math Specialist”, instructions=””” You are an expert mathematician who excels at: – Solving complex mathematical problems step by step – Explaining mathematical concepts clearly – Performing accurate calculations – Showing your work and reasoning Always break down complex problems into understandable steps. When doing calculations, be precise and show intermediate results. “””, tools=\[calculate\_compound\_interest\] # From our earlier example ) # Research specialist – optimized for information gathering research\_agent = Agent( name=”Research Specialist”, instructions=””” You are an expert researcher who excels at: – Finding authoritative and current information – Synthesizing information from multiple sources – Providing well-sourced and balanced perspectives – Distinguishing between facts and opinions Always cite your sources and explain the credibility of information. When possible, find multiple sources to verify important claims. “””, tools=\[search\_wikipedia, WebSearchTool()\] ) # Create an orchestrator agent that coordinates the specialists # This agent decides which specialist to use based on the user’s needs orchestrator = Agent( name=”Task Orchestrator”, instructions=””” You are a smart coordinator that manages a team of specialist agents. Your job is to understand user requests and delegate to the right specialist. Use the math specialist for: – Numerical calculations and mathematical problems – Financial analysis and projections – Statistical analysis – Any task involving numbers or formulas Use the research specialist for: – Finding information about topics, people, or events – Gathering current news or developments – Researching background information – Fact-checking and verification For complex tasks, you can use both specialists: 1. First gather information with the research specialist 2. Then perform calculations with the math specialist 3. Synthesize the results into a comprehensive answer Always explain which specialist you’re consulting and why. “””, tools=\[ # Convert agents into tools using the as\_tool() method # This allows the orchestrator to call them like any other tool math\_agent.as\_tool( tool\_name=”get\_math\_help”, tool\_description=”Get expert help with mathematical calculations, formulas, and numerical analysis” ), research\_agent.as\_tool( tool\_name=”get\_research\_help”, tool\_description=”Get expert help researching topics, finding information, and gathering current data” ) \] )
```
# Create specialized agents that excel at specific tasks
# Each agent has focused expertise and tailored instructions

# Math specialist - optimized for numerical calculations and explanations
math_agent = Agent(
    name="Math Specialist",
    instructions="""
    You are an expert mathematician who excels at:
    - Solving complex mathematical problems step by step
    - Explaining mathematical concepts clearly
    - Performing accurate calculations
    - Showing your work and reasoning
    
    Always break down complex problems into understandable steps.
    When doing calculations, be precise and show intermediate results.
    """,
    tools=[calculate_compound_interest]  # From our earlier example
)

# Research specialist - optimized for information gathering
research_agent = Agent(
    name="Research Specialist", 
    instructions="""
    You are an expert researcher who excels at:
    - Finding authoritative and current information
    - Synthesizing information from multiple sources
    - Providing well-sourced and balanced perspectives
    - Distinguishing between facts and opinions
    
    Always cite your sources and explain the credibility of information.
    When possible, find multiple sources to verify important claims.
    """,
    tools=[search_wikipedia, WebSearchTool()]
)

# Create an orchestrator agent that coordinates the specialists
# This agent decides which specialist to use based on the user's needs
orchestrator = Agent(
    name="Task Orchestrator",
    instructions="""
    You are a smart coordinator that manages a team of specialist agents.
    Your job is to understand user requests and delegate to the right specialist.
    
    Use the math specialist for:
    - Numerical calculations and mathematical problems
    - Financial analysis and projections
    - Statistical analysis
    - Any task involving numbers or formulas
    
    Use the research specialist for:
    - Finding information about topics, people, or events
    - Gathering current news or developments
    - Researching background information
    - Fact-checking and verification
    
    For complex tasks, you can use both specialists:
    1. First gather information with the research specialist
    2. Then perform calculations with the math specialist
    3. Synthesize the results into a comprehensive answer
    
    Always explain which specialist you're consulting and why.
    """,
    tools=[
        # Convert agents into tools using the as_tool() method
        # This allows the orchestrator to call them like any other tool
        math_agent.as_tool(
            tool_name="get_math_help",
            tool_description="Get expert help with mathematical calculations, formulas, and numerical analysis"
        ),
        research_agent.as_tool(
            tool_name="get_research_help", 
            tool_description="Get expert help researching topics, finding information, and gathering current data"
        )
    ]
)
```

### Best Practices for Tool Design

Creating effective tools is crucial for agent performance. Here are key best practices:

#### **1\. Function Naming and Signature**

- **Verb-Noun Names**: Use descriptive names that clearly indicate action (e.g., `fetch_stock_price` is better than `get_stock` or simply `stocks`)
- **Parameter Naming**: Use clear, self-documenting parameter names (`city` is better than `c`)
- **Type Consistency**: Ensure parameters have consistent types throughout your application
- **Avoid Defaults**: Let the LLM decide all parameter values based on context

#### **2\. Documentation and Clarity**

- **Rich Docstrings**: Include comprehensive documentation explaining the tool’s purpose, parameters, return values, and usage guidelines
- **Usage Examples**: Consider including examples in the docstring for complex tools
- **Clear Return Format**: Document the structure of returned data

#### **3\. Performance Considerations**

- **Timeout Handling**: Implement timeouts for external API calls
- **Caching**: Consider caching results for frequently used, unchanging data
- **Async Operations**: Use async functions for time-consuming operations when possible

## Context: Keeping State Between Steps

Context is the foundation that transforms stateless agent interactions into intelligent, stateful conversations. This enables agents to access user information, maintain state, and share data between tools and agent interactions.

The SDK lets you create a context object using a dataclass. In this example, we’ll create a context class that holds all user session information and passes it to all the agents and their tools:

Pythonfrom dataclasses import dataclass from agents import Agent, RunContextWrapper, function\_tool import time # Define a context class that holds all the user session information # This will be passed to every agent and tool in your system @dataclass class UserSession: user\_id: str name: str preferences: dict conversation\_history: list session\_start\_time: float
```
from dataclasses import dataclass
from agents import Agent, RunContextWrapper, function_tool
import time

# Define a context class that holds all the user session information
# This will be passed to every agent and tool in your system
@dataclass
class UserSession:
    user_id: str
    name: str
    preferences: dict
    conversation_history: list
    session_start_time: float
```

Now let’s see how our tools can access and modify the context. Tools can access user data to provide personalized responses and remember user preferences:

Python@function\_tool def get\_user\_preferences(ctx: RunContextWrapper\[UserSession\]) -> str: “””Get the current user’s preferences. The ctx parameter gives us access to the user session data. This allows tools to personalize their behavior based on user settings. “”” prefs = ctx.context.preferences if not prefs: return “No preferences set yet. You can update them anytime!” # Format preferences in a user-friendly way formatted\_prefs = \[\] for category, value in prefs.items(): formatted\_prefs.append(f”{category}: {value}”) return f”Your current preferences: {‘, ‘.join(formatted\_prefs)}” @function\_tool def update\_preference(ctx: RunContextWrapper\[UserSession\], category: str, value: str) -> str: “””Update a user preference. This tool modifies the context data, which persists throughout the session. Changes made here will be available to all subsequent tool calls and agent interactions. “”” # Update the preferences in the context ctx.context.preferences\[category\] = value # Add to conversation history for tracking ctx.context.conversation\_history.append({ “action”: “preference\_update”, “category”: category, “value”: value, “timestamp”: time.time() }) return f”Updated your {category} preference to ‘{value}’. This will apply to all future interactions!” @function\_tool def get\_conversation\_summary(ctx: RunContextWrapper\[UserSession\]) -> str: “””Provide a summary of the user’s session activity. This demonstrates how context can be used to track state across multiple interactions. “”” session = ctx.context session\_duration = time.time() – session.session\_start\_time summary = f””” Session Summary for {session.name}: – Session duration: {session\_duration/60:.1f} minutes – Conversation events: {len(session.conversation\_history)} – Current preferences: {len(session.preferences)} set “”” # Show recent activity if available if session.conversation\_history: recent\_activity = session.conversation\_history\[-3:\] # Last 3 events summary += “\\n\\nRecent activity:” for event in recent\_activity: if event.get(“action”) == “preference\_update”: summary += f”\\n- Set {event\[‘category’\]} to {event\[‘value’\]}” return summary
```
@function_tool
def get_user_preferences(ctx: RunContextWrapper[UserSession]) -> str:
    """Get the current user's preferences.
    
    The ctx parameter gives us access to the user session data.
    This allows tools to personalize their behavior based on user settings.
    """
    prefs = ctx.context.preferences
    if not prefs:
        return "No preferences set yet. You can update them anytime!"
    
    # Format preferences in a user-friendly way
    formatted_prefs = []
    for category, value in prefs.items():
        formatted_prefs.append(f"{category}: {value}")
    
    return f"Your current preferences: {', '.join(formatted_prefs)}"

@function_tool
def update_preference(ctx: RunContextWrapper[UserSession], category: str, value: str) -> str:
    """Update a user preference.
    
    This tool modifies the context data, which persists throughout the session.
    Changes made here will be available to all subsequent tool calls and agent interactions.
    """
    # Update the preferences in the context
    ctx.context.preferences[category] = value
    
    # Add to conversation history for tracking
    ctx.context.conversation_history.append({
        "action": "preference_update",
        "category": category,
        "value": value,
        "timestamp": time.time()
    })
    
    return f"Updated your {category} preference to '{value}'. This will apply to all future interactions!"

@function_tool
def get_conversation_summary(ctx: RunContextWrapper[UserSession]) -> str:
    """Provide a summary of the user's session activity.
    
    This demonstrates how context can be used to track state across multiple interactions.
    """
    session = ctx.context
    session_duration = time.time() - session.session_start_time
    
    summary = f"""
    Session Summary for {session.name}:
    - Session duration: {session_duration/60:.1f} minutes
    - Conversation events: {len(session.conversation_history)}
    - Current preferences: {len(session.preferences)} set
    """
    
    # Show recent activity if available
    if session.conversation_history:
        recent_activity = session.conversation_history[-3:]  # Last 3 events
        summary += "\n\nRecent activity:"
        for event in recent_activity:
            if event.get("action") == "preference_update":
                summary += f"\n- Set {event['category']} to {event['value']}"
    
    return summary
```

We can also create an agent that uses context-aware tools. Note the type annotation \[UserSession\]. This tells the agent what context type to expect and prevents errors.

Pythonpersonalized\_agent = Agent\[UserSession\]( name=”Personal Assistant”, instructions=””” You are a personal assistant that provides personalized service based on user preferences. You can: – Check and update user preferences using the available tools – Provide personalized recommendations based on their settings – Track conversation history and provide session summaries Key behaviors: – Always use the user’s name when you know it – Reference their preferences when giving advice – Offer to update preferences when you notice user needs – Be helpful and remember context from earlier in the conversation “””, tools=\[get\_user\_preferences, update\_preference, get\_conversation\_summary\] )
```
personalized_agent = Agent[UserSession](
    name="Personal Assistant",
    instructions="""
    You are a personal assistant that provides personalized service based on user preferences.
    
    You can:
    - Check and update user preferences using the available tools
    - Provide personalized recommendations based on their settings
    - Track conversation history and provide session summaries
    
    Key behaviors:
    - Always use the user's name when you know it
    - Reference their preferences when giving advice
    - Offer to update preferences when you notice user needs
    - Be helpful and remember context from earlier in the conversation
    """,
    tools=[get_user_preferences, update_preference, get_conversation_summary]
)
```

All tools and agents in a run share the same context, allowing them to coordinate and build on each other’s actions. Changes made to the context in one interaction persist to the next, enabling stateful conversations. You can store complex data structures (lists, dictionaries, custom objects) and modify them throughout the session.

## Tracing

The built-in tracing system captures every step of the agent’s thinking and actions:

- What the agent was thinking
- Which tools it called and why
- What inputs it used
- What outputs it received

This means when something goes wrong (and we all know something always goes wrong), you can actually figure out why.

Pythonfrom agents import Agent, Runner, trace # Tracing is enabled by default, but you can customize it async def traced\_research\_session(): with trace(workflow\_name=”Research Session”, group\_id=”session\_123″) as trace\_context: # First research query result1 = await Runner.run( agent, “Research the history of artificial intelligence”, run\_config=RunConfig( workflow\_name=”AI History Research”, trace\_metadata={“user\_id”: “user\_456”, “session\_type”: “research”} ) ) # Follow-up query in the same trace result2 = await Runner.run( agent, f”Based on this research: {result1.final\_output}, what are the key milestones?” ) # Traces are automatically sent to OpenAI dashboard print(“Research complete. Check traces at https://platform.openai.com/traces”) # You can also disable tracing or customize processors from agents import set\_tracing\_disabled, add\_trace\_processor # Disable tracing entirely set\_tracing\_disabled(True) # Or add custom trace processors for external tools # add\_trace\_processor(your\_custom\_processor)
```
from agents import Agent, Runner, trace

# Tracing is enabled by default, but you can customize it
async def traced_research_session():
    with trace(workflow_name="Research Session", group_id="session_123") as trace_context:
        # First research query
        result1 = await Runner.run(
            agent, 
            "Research the history of artificial intelligence",
            run_config=RunConfig(
                workflow_name="AI History Research",
                trace_metadata={"user_id": "user_456", "session_type": "research"}
            )
        )
        
        # Follow-up query in the same trace
        result2 = await Runner.run(
            agent,
            f"Based on this research: {result1.final_output}, what are the key milestones?"
        )
        
    # Traces are automatically sent to OpenAI dashboard
    print("Research complete. Check traces at https://platform.openai.com/traces")

# You can also disable tracing or customize processors
from agents import set_tracing_disabled, add_trace_processor

# Disable tracing entirely
set_tracing_disabled(True)

# Or add custom trace processors for external tools
# add_trace_processor(your_custom_processor)
```

## Multi-Agent Collaboration and Handoffs

One of the most powerful features is the ability to create handoffs between specialized agents and let them collaborate:

- Simple task? Use the fast, lightweight model
- Billing questions? Send them to the “Money Person” agent
- Technical problems? That’s for the “Have You Tried Restarting It?” agent
- Complex reasoning needed? Bring in the heavyweight model

Pythonsupport\_agent = Agent(name=”support”, instructions=”You handle customer questions.”) technical\_agent = Agent(name=”technical”, instructions=”You solve technical issues.”) billing\_agent = Agent(name=”billing”, instructions=”You handle billing inquiries.”) triage\_agent = Agent( name=”triage”, instructions=”Route customer inquiries to the appropriate specialized agent.”, handoffs=\[support\_agent, technical\_agent, billing\_agent\] )
```
support_agent = Agent(name="support", instructions="You handle customer questions.")
technical_agent = Agent(name="technical", instructions="You solve technical issues.")
billing_agent = Agent(name="billing", instructions="You handle billing inquiries.")

triage_agent = Agent(
    name="triage",
    instructions="Route customer inquiries to the appropriate specialized agent.",
    handoffs=[support_agent, technical_agent, billing_agent]
)
```

This creates a workflow where agents can delegate subtasks, forming a collaborative system greater than the sum of its parts.

How handoffs work behind the scenes:

1. **Automatic Tool Creation**: When you specify handoffs, the SDK automatically creates tools that represent transfers to each specialist agent.
2. **Intelligent Routing**: The triage agent analyzes the customer’s request and decides which specialist (if any) should handle it.
3. **Context Preservation**: When a handoff occurs, the conversation context is passed to the specialist agent, so they understand the full situation.
4. **Seamless Experience**: From the customer’s perspective, this feels like talking to one intelligent system that connects them to the right expert.

The power of handoffs lies in combining the broad understanding of a generalist agent with the deep expertise of specialists, creating a system that’s both intelligent and knowledgeable.

## Safety Guardrails

Guardrails are the bouncers of your application, validating inputs before they reach your main agent. Want to prevent users from asking for the recipe to digital disaster? A guardrail can check inputs with a fast model first, saving your premium model for legitimate requests.

Developers can implement safety measures that run in parallel with agent execution:

Pythonfrom agents.guardrails import CustomGuardrail async def is\_not\_swearing(msgs, context) -> bool: content = ” “.join(m\[“content”\] for m in msgs if “content” in m) return “badword” not in content.lower() my\_guardrail = CustomGuardrail( guardrail\_function=is\_not\_swearing, tripwire\_config=lambda output: not output # if ‘False’, raise error ) agent = Agent( name=”my\_agent”, input\_guardrails=\[my\_guardrail\] )
```
from agents.guardrails import CustomGuardrail

async def is_not_swearing(msgs, context) -> bool:
    content = " ".join(m["content"] for m in msgs if "content" in m)
    return "badword" not in content.lower()

my_guardrail = CustomGuardrail(
    guardrail_function=is_not_swearing,
    tripwire_config=lambda output: not output  # if 'False', raise error
)

agent = Agent(
    name="my_agent",
    input_guardrails=[my_guardrail]
)
```

In the above example, the guardrail is triggered before invoking the LLM. Key benefits of input guardrails:

- **Layered Defense**: Works alongside other safety measures (like output filtering) to create comprehensive protection.
- **Resource Protection**: Inappropriate requests are blocked before consuming expensive LLM resources or processing time.
- **Brand Safety**: Prevents your AI from engaging with harmful or inappropriate content that could damage your brand.
- **User Experience**: Provides clear, helpful feedback when requests are blocked, rather than confusing or hostile responses.
- **Monitoring**: All guardrail decisions are logged, providing valuable data for improving safety measures and understanding usage patterns.

## Hands-On Example: Building a Multi-Agent Research System

To demonstrate the power and flexibility of OpenAI’s Agents SDK, I’ve created a practical example that showcases how multiple specialized agents can collaborate to accomplish complex tasks. This Research Agent System represents the kind of real-world application that the SDK enables developers to build quickly and efficiently.

### The Research Agent System Architecture

This system consists of four specialized agents that work together to produce comprehensive research content:

1. **Triage Agent**: Coordinates the overall research process, delegating tasks to specialized agents
2. **Researcher Agent**: Gathers information from various sources on a given topic
3. **Fact Checker Agent**: Verifies statements for accuracy and proper sourcing
4. **Writer Agent**: Synthesizes verified research into coherent, well-structured content

Each agent is designed with specific instructions, tools, and capabilities that allow it to excel at its particular role. The system demonstrates several key features of the OpenAI Agents SDK:

- **Handoffs**: Agents delegate tasks to more specialized agents
- **Context sharing**: All agents work with a shared research context
- **Guardrails**: Ensures content remains fact-based and properly sourced
- **Structured outputs**: Final content follows a consistent, well-organized format
- **Function tools**: Agents leverage specialized tools for searching, verifying, and saving content

### The Code

Each agent as described above is going to do a certain task and then give us the result of the task in an output. We want to ensure that the output is structured in a certain manner so that when they hand it off to the next agent, that agent can take it in that structure and then do more work on it.

Pythonclass ResearchFinding(BaseModel): “””A single research finding with source information.””” statement: str source: str confidence: float # 0.0 to 1.0 class VerifiedResearch(BaseModel): “””Collection of verified research findings.””” findings: List\[ResearchFinding\] verified: bool notes: Optional\[str\] = None class FinalContent(BaseModel): “””Final output content with structured sections.””” title: str introduction: str key\_points: List\[str\] body: str conclusion: str sources: List\[str\]
```
class ResearchFinding(BaseModel):
    """A single research finding with source information."""
    statement: str
    source: str
    confidence: float  # 0.0 to 1.0

class VerifiedResearch(BaseModel):
    """Collection of verified research findings."""
    findings: List[ResearchFinding]
    verified: bool
    notes: Optional[str] = None

class FinalContent(BaseModel):
    """Final output content with structured sections."""
    title: str
    introduction: str
    key_points: List[str]
    body: str
    conclusion: str
    sources: List[str]
```

We also want to give each agent some tools to do their work. The Research Agent, for example, will need a tool to search the internet as well as save the retrieved content into a file. The fact-checker agent would need a tool to verify that content, and so on.

I am not going to write all the tools here, but here’s what the web search tool might look like, using the [Exa Search API](https://www.siddharthbharath.com/the-ultimate-guide-to-building-ai-agents-with-exa/).

Python@function\_tool async def search\_web(context: AgentContextWrapper\[ResearchContext\], query: str) -> str: “”” Search the web for information about a topic using the Exa Search API. Args: query: The search query text Returns: Search results as formatted text with citations “”” topic = context.agent\_context.topic # Combine the specific query with the general topic for better results full\_query = f”{query} about {topic}” try: # Make a request to the Exa Search API async with aiohttp.ClientSession() as session: async with session.post( “https://api.exa.ai/search”, headers={ “Content-Type”: “application/json”, “x-api-key”: “YOUR\_EXA\_API\_KEY” # Replace with your actual API key }, json={ “query”: full\_query, “numResults”: 5, “useAutoprompt”: True, “type”: “keyword” } ) as response: if response.status != 200: error\_text = await response.text() return f”Error searching: {response.status} – {error\_text}” search\_results = await response.json() # Process the results formatted\_results = f”Search results for ‘{query}’ about {topic}:\\n\\n” if not search\_results.get(“results”): return f”No results found for ‘{query}’ about {topic}.” # Format each result with its title, content, and URL for i, result in enumerate(search\_results.get(“results”, \[\]), 1): title = result.get(“title”, “No title”) url = result.get(“url”, “No URL”) content = result.get(“text”, “”).strip() # Limit content length for readability if len(content) > 500: content = content\[:500\] + “…” formatted\_results += f”{i}. \*\*{title}\*\*\\n” formatted\_results += f” {content}\\n” formatted\_results += f” Source: {url}\\n\\n” # Add a summary if available if search\_results.get(“autopromptString”): formatted\_results += f”Summary: {search\_results.get(‘autopromptString’)}\\n\\n” return formatted\_results except Exception as e: # Provide a useful error message error\_message = f”Error while searching for ‘{query}’: {str(e)}” # Add fallback information if the search fails fallback\_info = f”\\n\\nFallback information about {topic}:\\n” + \\ f”1. {topic} has been studied in recent publications.\\n” + \\ f”2. Current research suggests growing interest in {topic}.\\n” + \\ f”3. Common challenges in {topic} include implementation complexity and adoption barriers.” return error\_message + fallback\_info
```
@function_tool
async def search_web(context: AgentContextWrapper[ResearchContext], query: str) -> str:
    """
    Search the web for information about a topic using the Exa Search API.
    
    Args:
        query: The search query text
        
    Returns:
        Search results as formatted text with citations
    """
    topic = context.agent_context.topic
    # Combine the specific query with the general topic for better results
    full_query = f"{query} about {topic}"
    
    try:
        # Make a request to the Exa Search API
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.exa.ai/search",
                headers={
                    "Content-Type": "application/json",
                    "x-api-key": "YOUR_EXA_API_KEY"  # Replace with your actual API key
                },
                json={
                    "query": full_query,
                    "numResults": 5,
                    "useAutoprompt": True,
                    "type": "keyword"
                }
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    return f"Error searching: {response.status} - {error_text}"
                
                search_results = await response.json()
    
        # Process the results
        formatted_results = f"Search results for '{query}' about {topic}:\n\n"
        
        if not search_results.get("results"):
            return f"No results found for '{query}' about {topic}."
        
        # Format each result with its title, content, and URL
        for i, result in enumerate(search_results.get("results", []), 1):
            title = result.get("title", "No title")
            url = result.get("url", "No URL")
            content = result.get("text", "").strip()
            
            # Limit content length for readability
            if len(content) > 500:
                content = content[:500] + "..."
            
            formatted_results += f"{i}. **{title}**\n"
            formatted_results += f"   {content}\n"
            formatted_results += f"   Source: {url}\n\n"
        
        # Add a summary if available
        if search_results.get("autopromptString"):
            formatted_results += f"Summary: {search_results.get('autopromptString')}\n\n"
            
        return formatted_results
    
    except Exception as e:
        # Provide a useful error message
        error_message = f"Error while searching for '{query}': {str(e)}"
        
        # Add fallback information if the search fails
        fallback_info = f"\n\nFallback information about {topic}:\n" + \
                        f"1. {topic} has been studied in recent publications.\n" + \
                        f"2. Current research suggests growing interest in {topic}.\n" + \
                        f"3. Common challenges in {topic} include implementation complexity and adoption barriers."
        
        return error_message + fallback_info
```

You’ll notice this tool uses the ResearchContext context to share data across other tools. Let’s define that as well:

Pythonclass ResearchContext: def \_\_init\_\_(self, topic: str): self.topic = topic self.findings = \[\] self.verified\_findings = \[\] self.draft\_content = “” self.history = \[\] def add\_finding(self, finding: ResearchFinding): self.findings.append(finding) self.history.append(f”Added finding: {finding.statement}”) def add\_verified\_findings(self, verified: VerifiedResearch): self.verified\_findings.extend(verified.findings) self.history.append(f”Added {len(verified.findings)} verified findings”) def set\_draft(self, draft: str): self.draft\_content = draft self.history.append(“Updated draft content”)
```
class ResearchContext:
    def __init__(self, topic: str):
        self.topic = topic
        self.findings = []
        self.verified_findings = []
        self.draft_content = ""
        self.history = []
        
    def add_finding(self, finding: ResearchFinding):
        self.findings.append(finding)
        self.history.append(f"Added finding: {finding.statement}")
        
    def add_verified_findings(self, verified: VerifiedResearch):
        self.verified_findings.extend(verified.findings)
        self.history.append(f"Added {len(verified.findings)} verified findings")
        
    def set_draft(self, draft: str):
        self.draft_content = draft
        self.history.append("Updated draft content")
```

You may also want to add some guardrails, for example checking if the research content is unbiased. A very simple hard-coded example might be to count the number of times an opinion is expressed vs a fact, like so:

Pythonasync def is\_fact\_based(msgs, context) -> bool: “””Check if messages appear to be fact-based and not opinion-heavy.””” content = ” “.join(m.get(“content”, “”) for m in msgs if isinstance(m, dict)) opinion\_phrases = \[“I believe”, “I think”, “in my opinion”, “probably”, “might be”, “could be”\] # Count opinion phrases opinion\_count = sum(content.lower().count(phrase) for phrase in opinion\_phrases) # Allow some opinion phrases, but not too many return opinion\_count < 3 fact\_based\_guardrail = CustomGuardrail( guardrail\_function=is\_fact\_based, tripwire\_config=lambda output: not output, error\_message=”Output contains too many opinion statements rather than fact-based research.” )
```
async def is_fact_based(msgs, context) -> bool:
    """Check if messages appear to be fact-based and not opinion-heavy."""
    content = " ".join(m.get("content", "") for m in msgs if isinstance(m, dict))
    opinion_phrases = ["I believe", "I think", "in my opinion", "probably", "might be", "could be"]
    
    # Count opinion phrases
    opinion_count = sum(content.lower().count(phrase) for phrase in opinion_phrases)
    
    # Allow some opinion phrases, but not too many
    return opinion_count < 3

fact_based_guardrail = CustomGuardrail(
    guardrail_function=is_fact_based,
    tripwire_config=lambda output: not output,
    error_message="Output contains too many opinion statements rather than fact-based research."
)
```

You can create something more powerful but this simple example highlights how the SDK checks against your guardrails.

Finally, we’ll create our Agents and give them the tools, context, and guardrails. Here’s what the Fact Checker Agent might look like:

Pythonfact\_checker\_agent = Agent( name=”fact\_checker\_agent”, model=”gpt-4o”, instructions=”””You are a meticulous fact-checking agent. Your job is to: 1. Review the research findings in the shared context 2. Verify each statement using the verify\_statement tool 3. Consolidate verified findings using save\_verified\_research 4. Be skeptical and thorough – only approve statements with sufficient evidence For each finding, check if the source is credible and if the statement contains verifiable facts rather than opinions or generalizations. “””, context\_type=ResearchContext, tools=\[verify\_statement, save\_verified\_research\], output\_type=str, output\_guardrails=\[fact\_based\_guardrail\], description=”Verifies research findings for accuracy and proper sourcing” )
```
fact_checker_agent = Agent(
    name="fact_checker_agent",
    model="gpt-4o",
    instructions="""You are a meticulous fact-checking agent. Your job is to:
    1. Review the research findings in the shared context
    2. Verify each statement using the verify_statement tool
    3. Consolidate verified findings using save_verified_research
    4. Be skeptical and thorough - only approve statements with sufficient evidence
    
    For each finding, check if the source is credible and if the statement contains verifiable
    facts rather than opinions or generalizations.
    """,
    context_type=ResearchContext,
    tools=[verify_statement, save_verified_research],
    output_type=str,
    output_guardrails=[fact_based_guardrail],
    description="Verifies research findings for accuracy and proper sourcing"
)
```

Our Triage Agent which manages the whole process would also have handoffs defined in its parameters:

Pythontriage\_agent = Agent( name=”triage\_agent”, model=”gpt-3.5-turbo”, instructions=”””You are a research coordinator who manages the research process. For any research query: 1. First, hand off to the researcher\_agent to gather information 2. Then, hand off to the fact\_checker\_agent to verify the findings 3. Finally, hand off to the writer\_agent to create the final content Monitor the process and ensure each specialized agent completes their task. “””, context\_type=ResearchContext, handoffs=\[ handoff(researcher\_agent), handoff(fact\_checker\_agent), handoff(writer\_agent) \], output\_type=FinalContent, description=”Coordinates the research process across specialized agents” )
```
triage_agent = Agent(
    name="triage_agent",
    model="gpt-3.5-turbo",
    instructions="""You are a research coordinator who manages the research process.
    For any research query:
    1. First, hand off to the researcher_agent to gather information
    2. Then, hand off to the fact_checker_agent to verify the findings
    3. Finally, hand off to the writer_agent to create the final content
    
    Monitor the process and ensure each specialized agent completes their task.
    """,
    context_type=ResearchContext,
    handoffs=[
        handoff(researcher_agent),
        handoff(fact_checker_agent),
        handoff(writer_agent)
    ],
    output_type=FinalContent,
    description="Coordinates the research process across specialized agents"
)
```

And finally, we write the main function to run the whole process:

Pythonasync def run\_research\_system(topic: str) -> FinalContent: “””Run the multi-agent research system on a given topic.””” # Create the shared context context = ResearchContext(topic=topic) # Configure the run with tracing enabled config = AgentRunConfig( run\_name=f”research\_{topic.replace(‘ ‘, ‘\_’)}”, tracing\_disabled=False ) # Run the triage agent with the initial query result = await AgentRunner.run( triage\_agent, \[f”Research the following topic thoroughly: {topic}”\], context=context, run\_config=config ) return result.agent\_output
```
async def run_research_system(topic: str) -> FinalContent:
    """Run the multi-agent research system on a given topic."""
    # Create the shared context
    context = ResearchContext(topic=topic)
    
    # Configure the run with tracing enabled
    config = AgentRunConfig(
        run_name=f"research_{topic.replace(' ', '_')}",
        tracing_disabled=False
    )
    
    # Run the triage agent with the initial query
    result = await AgentRunner.run(
        triage_agent,
        [f"Research the following topic thoroughly: {topic}"],
        context=context,
        run_config=config
    )
    
    return result.agent_output
```

## Try It Yourself

If you’re eager to explore the Agents SDK yourself, the process is straightforward:

1. Install the SDK via pip: `pip install openai-agents`
2. Check out the [official documentation](https://openai.github.io/openai-agents-python/)
3. Explore the [GitHub repository](https://github.com/openai/openai-agents-python) for examples and contributions

The documentation is comprehensive and includes numerous examples to help you understand the SDK’s capabilities and implementation patterns.

## Your Next Steps

As we venture further into the age of agentic AI, tools like the Agents SDK will become increasingly valuable. Whether you’re looking to automate complex workflows, create specialized assistants, or explore the frontiers of AI capability, this toolkit provides an excellent foundation.

I encourage you to dive in and experiment with the Agents SDK for your projects. If you’re working on something interesting or need guidance on implementation, don’t hesitate to reach out. I’m particularly interested in hearing about novel applications and creative uses of multi-agent systems.