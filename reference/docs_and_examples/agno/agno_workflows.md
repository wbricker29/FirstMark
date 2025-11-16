# What are Workflows?

> Learn how Agno Workflows enable deterministic, controlled automation of multi-agent systems

Agno Workflows enable you to build deterministic, controlled agentic flows by orchestrating agents, teams, and functions through a series of defined steps. Unlike free-form agent interactions, workflows provide structured automation with predictable execution patterns, making them ideal for production systems that require reliable, repeatable processes.

<img className="block dark:hidden" src="https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-flow-light.png?fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=a308215dbae7c8e9050d03af47cfcf1b" alt="Workflows flow diagram" data-og-width="2994" width="2994" data-og-height="756" height="756" data-path="images/workflows-flow-light.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-flow-light.png?w=280&fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=36da448838231c986ea6fbee6cd20adf 280w, https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-flow-light.png?w=560&fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=2f79f8986f962ceed254128c04e2fff0 560w, https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-flow-light.png?w=840&fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=602db868a58a7ebadfb6849d783dacdf 840w, https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-flow-light.png?w=1100&fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=79ab80554e556943fad1bb1c54c23c1b 1100w, https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-flow-light.png?w=1650&fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=0c06010680d6e281b4ca6f90f8febc23 1650w, https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-flow-light.png?w=2500&fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=6195335508ec97552803e2920695044d 2500w" />

<img className="hidden dark:block" src="https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-flow.png?fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=e9ef16c48420b7eee9312561ab56098e" alt="Workflows flow diagram" data-og-width="2994" width="2994" data-og-height="756" height="756" data-path="images/workflows-flow.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-flow.png?w=280&fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=cb8faae1ea504803ff761ae3b89c51fb 280w, https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-flow.png?w=560&fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=498fe144844ce93806c7f590823ae666 560w, https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-flow.png?w=840&fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=e8bd51333fbf023524a636d579f489f2 840w, https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-flow.png?w=1100&fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=f4447ccd6c0c84f2ca104eb2ce7b560b 1100w, https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-flow.png?w=1650&fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=5a6c0f92fc29f107e4249432216a6b0f 1650w, https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-flow.png?w=2500&fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=0192f698b51c565c3efd9259472c8750 2500w" />

## Why should you use Workflows?

Workflows provide deterministic control over your agentic systems, enabling you to build reliable automation that executes consistently every time. They're essential when you need:

**Deterministic Execution**

* Predictable step-by-step processing with defined inputs and outputs
* Consistent results across multiple runs
* Clear audit trails for production systems

**Complex Orchestration**

* Multi-agent coordination with controlled handoffs
* Parallel processing and conditional branching
* Loop structures for iterative tasks

Workflows excel at **deterministic agent automation**, while [Teams](/concepts/teams/overview) are designed for **dynamic agentic coordination**. Use workflows when you need predictable, repeatable processes; use teams when you need flexible, collaborative problem-solving.

## Deterministic Step Execution

Workflows execute as a controlled sequence of steps, where each step produces deterministic outputs that feed into the next step. This creates predictable data flows and consistent results, unlike free-form agent conversations.

**Step Types**

* **Agents**: Individual AI executors with specific capabilities and instructions
* **Teams**: Coordinated groups of agents working together on complex problems
* **Functions**: Custom Python functions for specialized processing logic

**Deterministic Benefits**
Your agents and teams retain their individual characteristics and capabilities, but now operate within a structured framework that ensures:

* **Predictable execution**: Steps run in defined order with controlled inputs/outputs
* **Repeatable results**: Same inputs produce consistent outputs across runs
* **Clear data flow**: Output from each step explicitly becomes input for the next
* **Controlled state**: Session management and state persistence between steps
* **Reliable error handling**: Built-in retry mechanisms and error recovery

## Direct User Interaction

When users interact directly with your workflow (rather than calling it programmatically), you can make it **conversational** by adding a `WorkflowAgent`. This enables natural chat-like interactions where the workflow intelligently decides whether to answer from previous results or execute new workflow runs. Learn more in the [Conversational Workflows](/concepts/workflows/conversational-workflows) guide.

## Guides

<CardGroup cols={2}>
  <Card title="View Complete Example" icon="code" href="/examples/concepts/workflows/01-basic-workflows/sequence_of_functions_and_agents">
    See the full example with agents, teams, and functions working together
  </Card>

  <Card title="Conversational Workflows" icon="comments" href="/concepts/workflows/conversational-workflows">
    Enable chat-like interactions with your workflows for direct user engagement
  </Card>

  <Card title="Use in AgentOS" icon="play" href="/agent-os/features/chat-interface#run-a-workflow">
    Run your workflows through the AgentOS chat interface
  </Card>
</CardGroup>

# Building Workflows

> Learn how to build your workflows.

Workflows are a powerful way to orchestrate your agents and teams. They are a series of steps that are executed in a flow that you control.

## Building Blocks

1. The **`Workflow`** class is the top-level orchestrator that manages the entire execution process.
2. **`Step`** is the fundamental unit of work in the workflow system. Each step encapsulates exactly one `executor` - either an `Agent`, a `Team`, or a custom Python function. This design ensures clarity and maintainability while preserving the individual characteristics of each executor.
3. **`Loop`** is a construct that allows you to execute one or more steps multiple times. This is useful when you need to repeat a set of steps until a certain condition is met.
4. **`Parallel`** is a construct that allows you to execute one or more steps in parallel. This is useful when you need to execute a set of steps concurrently with the outputs joined together.
5. **`Condition`** makes a step conditional based on criteria you specify.
6. **`Router`** allows you to specify which step(s) to execute next, effectively creating branching logic in your workflow.

<Note>
  When using a custom Python function as an executor for a step, `StepInput` and
  `StepOutput` provides standardized interfaces for data flow between steps:
</Note>

<img className="block dark:hidden" src="https://mintcdn.com/agno-v2/ZJv0T4EM1rVInAsr/images/workflows-step-io-flow-light.png?fit=max&auto=format&n=ZJv0T4EM1rVInAsr&q=85&s=25129f55e1ead21d513c25b51dca412d" alt="Workflows step IO flow diagram" data-og-width="2001" width="2001" data-og-height="756" height="756" data-path="images/workflows-step-io-flow-light.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/agno-v2/ZJv0T4EM1rVInAsr/images/workflows-step-io-flow-light.png?w=280&fit=max&auto=format&n=ZJv0T4EM1rVInAsr&q=85&s=67a933194ccf6f39606314d48784927f 280w, https://mintcdn.com/agno-v2/ZJv0T4EM1rVInAsr/images/workflows-step-io-flow-light.png?w=560&fit=max&auto=format&n=ZJv0T4EM1rVInAsr&q=85&s=3edc1003ffbee7b7767b1a84720bc616 560w, https://mintcdn.com/agno-v2/ZJv0T4EM1rVInAsr/images/workflows-step-io-flow-light.png?w=840&fit=max&auto=format&n=ZJv0T4EM1rVInAsr&q=85&s=cd83f97d789ba6e0a1980e8d25759281 840w, https://mintcdn.com/agno-v2/ZJv0T4EM1rVInAsr/images/workflows-step-io-flow-light.png?w=1100&fit=max&auto=format&n=ZJv0T4EM1rVInAsr&q=85&s=f018b152972888a037a239342bde7602 1100w, https://mintcdn.com/agno-v2/ZJv0T4EM1rVInAsr/images/workflows-step-io-flow-light.png?w=1650&fit=max&auto=format&n=ZJv0T4EM1rVInAsr&q=85&s=bd9ba2232ddd6801f4ece40477975608 1650w, https://mintcdn.com/agno-v2/ZJv0T4EM1rVInAsr/images/workflows-step-io-flow-light.png?w=2500&fit=max&auto=format&n=ZJv0T4EM1rVInAsr&q=85&s=383ce2bcd2751e0b47a1304f797cf2d0 2500w" />

<img className="hidden dark:block" src="https://mintcdn.com/agno-v2/ZJv0T4EM1rVInAsr/images/workflows-step-io-flow.png?fit=max&auto=format&n=ZJv0T4EM1rVInAsr&q=85&s=faa43206bfa64265fa4d32721a12216d" alt="Workflows step IO flow diagram" data-og-width="2001" width="2001" data-og-height="756" height="756" data-path="images/workflows-step-io-flow.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/agno-v2/ZJv0T4EM1rVInAsr/images/workflows-step-io-flow.png?w=280&fit=max&auto=format&n=ZJv0T4EM1rVInAsr&q=85&s=50c47b8c564021b246ba034bc331c982 280w, https://mintcdn.com/agno-v2/ZJv0T4EM1rVInAsr/images/workflows-step-io-flow.png?w=560&fit=max&auto=format&n=ZJv0T4EM1rVInAsr&q=85&s=430d80604ed6927b914c7e9c1fcf8aa6 560w, https://mintcdn.com/agno-v2/ZJv0T4EM1rVInAsr/images/workflows-step-io-flow.png?w=840&fit=max&auto=format&n=ZJv0T4EM1rVInAsr&q=85&s=60dfe1d25956d8895f87b215607466cf 840w, https://mintcdn.com/agno-v2/ZJv0T4EM1rVInAsr/images/workflows-step-io-flow.png?w=1100&fit=max&auto=format&n=ZJv0T4EM1rVInAsr&q=85&s=8ac4c55ff3bb0c2f17baf76f0bae48a8 1100w, https://mintcdn.com/agno-v2/ZJv0T4EM1rVInAsr/images/workflows-step-io-flow.png?w=1650&fit=max&auto=format&n=ZJv0T4EM1rVInAsr&q=85&s=1c4237aa3bf8581c52b97f51f0b524e5 1650w, https://mintcdn.com/agno-v2/ZJv0T4EM1rVInAsr/images/workflows-step-io-flow.png?w=2500&fit=max&auto=format&n=ZJv0T4EM1rVInAsr&q=85&s=9ae7ba15375a9bb435b1765646047770 2500w" />

## How to make your first workflow?

There are different types of patterns you can use to build your workflows.
For example you can combine agents, teams, and functions to build a workflow.

```python  theme={null}
from agno.workflow import Step, Workflow, StepOutput

def data_preprocessor(step_input):
    # Custom preprocessing logic

    # Or you can also run any agent/team over here itself
    # response = some_agent.run(...)
    return StepOutput(content=f"Processed: {step_input.input}") # <-- Now pass the agent/team response in content here

workflow = Workflow(
    name="Mixed Execution Pipeline",
    steps=[
        research_team,      # Team
        data_preprocessor,  # Function
        content_agent,      # Agent
    ]
)

workflow.print_response("Analyze the competitive landscape for fintech startups", markdown=True)
```

# Running Workflows

> Learn how to run a workflow and get the response.

The `Workflow.run()` function runs the agent and generates a response, either as a `WorkflowRunOutput` object or a stream of `WorkflowRunOutput` objects.

Many of our examples use `workflow.print_response()` which is a helper utility to print the response in the terminal. This uses `workflow.run()` under the hood.

## Running your Workflow

Here's how to run your workflow. The response is captured in the `response`.

```python  theme={null}
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.db.sqlite import SqliteDb
from agno.team import Team
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.hackernews import HackerNewsTools
from agno.workflow import Step, Workflow
from agno.run.workflow import WorkflowRunOutput
from agno.utils.pprint import pprint_run_response

# Define agents
hackernews_agent = Agent(
    name="Hackernews Agent",
    model=OpenAIChat(id="gpt-5-mini"),
    tools=[HackerNewsTools()],
    role="Extract key insights and content from Hackernews posts",
)
web_agent = Agent(
    name="Web Agent",
    model=OpenAIChat(id="gpt-5-mini"),
    tools=[DuckDuckGoTools()],
    role="Search the web for the latest news and trends",
)

# Define research team for complex analysis
research_team = Team(
    name="Research Team",
    members=[hackernews_agent, web_agent],
    instructions="Research tech topics from Hackernews and the web",
)

content_planner = Agent(
    name="Content Planner",
    model=OpenAIChat(id="gpt-5-mini"),
    instructions=[
        "Plan a content schedule over 4 weeks for the provided topic and research content",
        "Ensure that I have posts for 3 posts per week",
    ],
)

content_creation_workflow = Workflow(
    name="Content Creation Workflow",
    description="Automated content creation from blog posts to social media",
    db=SqliteDb(db_file="tmp/workflow.db"),
    steps=[research_team, content_planner],
)

# Create and use workflow
if __name__ == "__main__":
    response: WorkflowRunOutput = content_creation_workflow.run(
        input="AI trends in 2024",
        markdown=True,
    )

    pprint_run_response(response, markdown=True)
```

<Note>
  The `Workflow.run()` function returns a `WorkflowRunOutput` object when not
  streaming. Here is detailed documentation for
  [WorkflowRunOutput](/reference/workflows/workflow_run_output).
</Note>

## Async Execution

The `Workflow.arun()` function is the async version of `Workflow.run()`.

Here is an example of how to use it:

```python  theme={null}
from typing import AsyncIterator
import asyncio

from agno.agent import Agent
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.workflow import Condition, Step, Workflow, StepInput
from agno.run.workflow import WorkflowRunOutput, WorkflowRunOutputEvent, WorkflowRunEvent

# === BASIC AGENTS ===
researcher = Agent(
    name="Researcher",
    instructions="Research the given topic and provide detailed findings.",
    tools=[DuckDuckGoTools()],
)

summarizer = Agent(
    name="Summarizer",
    instructions="Create a clear summary of the research findings.",
)

fact_checker = Agent(
    name="Fact Checker",
    instructions="Verify facts and check for accuracy in the research.",
    tools=[DuckDuckGoTools()],
)

writer = Agent(
    name="Writer",
    instructions="Write a comprehensive article based on all available research and verification.",
)

# === CONDITION EVALUATOR ===
def needs_fact_checking(step_input: StepInput) -> bool:
    """Determine if the research contains claims that need fact-checking"""
    summary = step_input.previous_step_content or ""

    # Look for keywords that suggest factual claims
    fact_indicators = [
        "study shows",
        "breakthroughs",
        "research indicates",
        "according to",
        "statistics",
        "data shows",
        "survey",
        "report",
        "million",
        "billion",
        "percent",
        "%",
        "increase",
        "decrease",
    ]

    return any(indicator in summary.lower() for indicator in fact_indicators)


# === WORKFLOW STEPS ===
research_step = Step(
    name="research",
    description="Research the topic",
    agent=researcher,
)

summarize_step = Step(
    name="summarize",
    description="Summarize research findings",
    agent=summarizer,
)

# Conditional fact-checking step
fact_check_step = Step(
    name="fact_check",
    description="Verify facts and claims",
    agent=fact_checker,
)

write_article = Step(
    name="write_article",
    description="Write final article",
    agent=writer,
)

# === BASIC LINEAR WORKFLOW ===
basic_workflow = Workflow(
    name="Basic Linear Workflow",
    description="Research -> Summarize -> Condition(Fact Check) -> Write Article",
    steps=[
        research_step,
        summarize_step,
        Condition(
            name="fact_check_condition",
            description="Check if fact-checking is needed",
            evaluator=needs_fact_checking,
            steps=[fact_check_step],
        ),
        write_article,
    ],
)

async def main():
    try:
        response: WorkflowRunOutput = await basic_workflow.arun(
            input="Recent breakthroughs in quantum computing",
        )
        pprint_run_response(response, markdown=True)
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Streaming Responses

To enable streaming, set `stream=True` when calling `run()`. This will return an iterator of `WorkflowRunOutputEvent` objects instead of a single response.

```python  theme={null}
# Define your agents/team
...

content_creation_workflow = Workflow(
    name="Content Creation Workflow",
    description="Automated content creation from blog posts to social media",
    db=SqliteDb(db_file="tmp/workflow.db"),
    steps=[research_team, content_planner],
)

# Create and use workflow
if __name__ == "__main__":
    response: Iterator[WorkflowRunOutputEvent] = content_creation_workflow.run(
        input="AI trends in 2024",
        markdown=True,
        stream=True,
    )

    pprint_run_response(response, markdown=True)
```

### Streaming all events

By default, when you stream a response, only the `WorkflowStartedEvent` and `WorkflowCompletedEvent` events will be streamed (together with all the Agent and Team events).

You can also stream all events by setting `stream_events=True`.

This will provide real-time updates about the workflow's internal processes:

```python  theme={null}
from typing import Iterator

from agno.agent import Agent
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.workflow import Condition, Step, Workflow, StepInput
from agno.run.workflow import WorkflowRunOutput, WorkflowRunOutputEvent, WorkflowRunEvent

# === BASIC AGENTS ===
researcher = Agent(
    name="Researcher",
    instructions="Research the given topic and provide detailed findings.",
    tools=[DuckDuckGoTools()],
)

summarizer = Agent(
    name="Summarizer",
    instructions="Create a clear summary of the research findings.",
)

fact_checker = Agent(
    name="Fact Checker",
    instructions="Verify facts and check for accuracy in the research.",
    tools=[DuckDuckGoTools()],
)

writer = Agent(
    name="Writer",
    instructions="Write a comprehensive article based on all available research and verification.",
)

# === CONDITION EVALUATOR ===
def needs_fact_checking(step_input: StepInput) -> bool:
    """Determine if the research contains claims that need fact-checking"""
    summary = step_input.previous_step_content or ""

    # Look for keywords that suggest factual claims
    fact_indicators = [
        "study shows",
        "breakthroughs",
        "research indicates",
        "according to",
        "statistics",
        "data shows",
        "survey",
        "report",
        "million",
        "billion",
        "percent",
        "%",
        "increase",
        "decrease",
    ]

    return any(indicator in summary.lower() for indicator in fact_indicators)


# === WORKFLOW STEPS ===
research_step = Step(
    name="research",
    description="Research the topic",
    agent=researcher,
)

summarize_step = Step(
    name="summarize",
    description="Summarize research findings",
    agent=summarizer,
)

# Conditional fact-checking step
fact_check_step = Step(
    name="fact_check",
    description="Verify facts and claims",
    agent=fact_checker,
)

write_article = Step(
    name="write_article",
    description="Write final article",
    agent=writer,
)

# === BASIC LINEAR WORKFLOW ===
basic_workflow = Workflow(
    name="Basic Linear Workflow",
    description="Research -> Summarize -> Condition(Fact Check) -> Write Article",
    steps=[
        research_step,
        summarize_step,
        Condition(
            name="fact_check_condition",
            description="Check if fact-checking is needed",
            evaluator=needs_fact_checking,
            steps=[fact_check_step],
        ),
        write_article,
    ],
)

if __name__ == "__main__":
    try:
        response: Iterator[WorkflowRunOutputEvent] = basic_workflow.run(
            input="Recent breakthroughs in quantum computing",
            stream=True,
            stream_events=True,
        )
        for event in response:
            if event.event == WorkflowRunEvent.condition_execution_started.value:
                print(event)
                print()
            elif event.event == WorkflowRunEvent.condition_execution_completed.value:
                print(event)
                print()
            elif event.event == WorkflowRunEvent.workflow_started.value:
                print(event)
                print()
            elif event.event == WorkflowRunEvent.step_started.value:
                print(event)
                print()
            elif event.event == WorkflowRunEvent.step_completed.value:
                print(event)
                print()
            elif event.event == WorkflowRunEvent.workflow_completed.value:
                print(event)
                print()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()
```

### Streaming Executor Events

The events from Agents and Teams used inside your workflow are automatically yielded during the streaming of a Workflow. You can choose not to stream these executor events by setting `stream_executor_events=False`.

The following Workflow events will be streamed in all cases:

* `WorkflowStarted`
* `WorkflowCompleted`
* `StepStarted`
* `StepCompleted`

See the following example:

```python  theme={null}
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.workflow.step import Step
from agno.workflow.workflow import Workflow

agent = Agent(
    name="ResearchAgent",
    model=OpenAIChat(id="gpt-5-mini"),
    instructions="You are a helpful research assistant. Be concise.",
)

workflow = Workflow(
    name="Research Workflow",
    steps=[Step(name="Research", agent=agent)],
    stream=True,
    stream_executor_events=False,  # <- Filter out internal executor events
)

print("\n" + "=" * 70)
print("Workflow Streaming Example: stream_executor_events=False")
print("=" * 70)
print(
    "\nThis will show only workflow and step events and will not yield RunContent and TeamRunContent events"
)
print("filtering out internal agent/team events for cleaner output.\n")

# Run workflow and display events
for event in workflow.run(
    "What is Python?",
    stream=True,
    stream_events=True,
):
    event_name = event.event if hasattr(event, "event") else type(event).__name__
    print(f"  → {event_name}")
```

### Async Streaming

The `Workflow.arun(stream=True)` returns an async iterator of `WorkflowRunOutputEvent` objects instead of a single response.
So for example, if you want to stream the response, you can do the following:

```Python  theme={null}

# Define your workflow
...

async def main():
    try:
        response: AsyncIterator[WorkflowRunOutputEvent] = basic_workflow.arun(
            message="Recent breakthroughs in quantum computing",
            stream=True,
            stream_events=True,
        )
        async for event in response:
            if event.event == WorkflowRunEvent.condition_execution_started.value:
                print(event)
                print()
            elif event.event == WorkflowRunEvent.condition_execution_completed.value:
                print(event)
                print()
            elif event.event == WorkflowRunEvent.workflow_started.value:
                print(event)
                print()
            elif event.event == WorkflowRunEvent.step_started.value:
                print(event)
                print()
            elif event.event == WorkflowRunEvent.step_completed.value:
                print(event)
                print()
            elif event.event == WorkflowRunEvent.workflow_completed.value:
                print(event)
                print()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
```

See the [Async Streaming](/examples/concepts/workflows/01-basic-workflows/async_events_streaming) example for more details.

### Event Types

The following events are yielded by the `Workflow.run()` and `Workflow.arun()` functions depending on the workflow's configuration:

#### Core Events

| Event Type          | Description                                         |
| ------------------- | --------------------------------------------------- |
| `WorkflowStarted`   | Indicates the start of a workflow run               |
| `WorkflowCompleted` | Signals successful completion of the workflow run   |
| `WorkflowError`     | Indicates an error occurred during the workflow run |

#### Step Events

| Event Type      | Description                               |
| --------------- | ----------------------------------------- |
| `StepStarted`   | Indicates the start of a step             |
| `StepCompleted` | Signals successful completion of a step   |
| `StepError`     | Indicates an error occurred during a step |

#### Step Output Events (For custom functions)

| Event Type   | Description                    |
| ------------ | ------------------------------ |
| `StepOutput` | Indicates the output of a step |

#### Parallel Execution Events

| Event Type                   | Description                                      |
| ---------------------------- | ------------------------------------------------ |
| `ParallelExecutionStarted`   | Indicates the start of a parallel step           |
| `ParallelExecutionCompleted` | Signals successful completion of a parallel step |

#### Condition Execution Events

| Event Type                    | Description                                  |
| ----------------------------- | -------------------------------------------- |
| `ConditionExecutionStarted`   | Indicates the start of a condition           |
| `ConditionExecutionCompleted` | Signals successful completion of a condition |

#### Loop Execution Events

| Event Type                    | Description                                       |
| ----------------------------- | ------------------------------------------------- |
| `LoopExecutionStarted`        | Indicates the start of a loop                     |
| `LoopIterationStartedEvent`   | Indicates the start of a loop iteration           |
| `LoopIterationCompletedEvent` | Signals successful completion of a loop iteration |
| `LoopExecutionCompleted`      | Signals successful completion of a loop           |

#### Router Execution Events

| Event Type                 | Description                               |
| -------------------------- | ----------------------------------------- |
| `RouterExecutionStarted`   | Indicates the start of a router           |
| `RouterExecutionCompleted` | Signals successful completion of a router |

#### Steps Execution Events

| Event Type                | Description                                        |
| ------------------------- | -------------------------------------------------- |
| `StepsExecutionStarted`   | Indicates the start of `Steps` being executed      |
| `StepsExecutionCompleted` | Signals successful completion of `Steps` execution |

See detailed documentation in the [WorkflowRunOutputEvent](/reference/workflows/workflow_run_output) documentation.

### Storing Events

Workflows can automatically store all execution events for analysis, debugging, and audit purposes. Filter specific event types to reduce noise and storage overhead while maintaining essential execution records.

Access stored events via `workflow.run_response.events` and in the `runs` column of your workflow's session database (SQLite, PostgreSQL, etc.).

* `store_events=True`: Automatically stores all workflow events in the database
* `events_to_skip=[]`: Filter out specific event types to reduce storage and noise

Access all stored events via `workflow.run_response.events`

**Available Events to Skip:**

```python  theme={null}
from agno.run.workflow import WorkflowRunEvent

# Common events you might want to skip
events_to_skip = [
    WorkflowRunEvent.workflow_started,
    WorkflowRunEvent.workflow_completed,
    WorkflowRunEvent.workflow_cancelled,
    WorkflowRunEvent.step_started,
    WorkflowRunEvent.step_completed,
    WorkflowRunEvent.parallel_execution_started,
    WorkflowRunEvent.parallel_execution_completed,
    WorkflowRunEvent.condition_execution_started,
    WorkflowRunEvent.condition_execution_completed,
    WorkflowRunEvent.loop_execution_started,
    WorkflowRunEvent.loop_execution_completed,
    WorkflowRunEvent.router_execution_started,
    WorkflowRunEvent.router_execution_completed,
]
```

**Use Cases**

* **Debugging**: Store all events to analyze workflow execution flow
* **Audit Trails**: Keep records of all workflow activities for compliance
* **Performance Analysis**: Analyze timing and execution patterns
* **Error Investigation**: Review event sequences leading to failures
* **Noise Reduction**: Skip verbose events like `step_started` to focus on results

**Configuration Examples**

```python  theme={null}
# store everything
debug_workflow = Workflow(
    name="Debug Workflow",
    store_events=True,
    steps=[...]
)

# store only important events
production_workflow = Workflow(
    name="Production Workflow",
    store_events=True,
    events_to_skip=[
        WorkflowRunEvent.step_started,
        WorkflowRunEvent.parallel_execution_started,
        # keep step_completed and workflow_completed
    ],
    steps=[...]
)

# No event storage
fast_workflow = Workflow(
    name="Fast Workflow",
    store_events=False,
    steps=[...]
)
```

<Tip>
  See this [example](/examples/concepts/workflows/06_workflows_advanced_concepts/store_events_and_events_to_skip_in_a_workflow) for more information.
</Tip>

## Agno Telemetry

Agno logs which model an workflow used so we can prioritize updates to the most popular providers. You can disable this by setting `AGNO_TELEMETRY=false` in your environment or by setting `telemetry=False` on the workflow.

```bash  theme={null}
export AGNO_TELEMETRY=false
```

or:

```python  theme={null}
workflow = Workflow(..., telemetry=False)
```

See the [Workflow class reference](/reference/workflows/workflow) for more details.

## Developer Resources

* View the [Workflow reference](/reference/workflows/workflow)
* View the [WorkflowRunOutput schema](/reference/workflows/workflow_run_output)
* View [Cookbook](https://github.com/agno-agi/agno/tree/main/cookbook/workflows/README.md)


# Input and Output

> Learn how to use structured input and output with Workflows for reliable, production-ready systems.

Workflows support multiple input types for maximum flexibility:

| Input Type         | Example                                           | Use Case                   |
| ------------------ | ------------------------------------------------- | -------------------------- |
| **String**         | `"Analyze AI trends"`                             | Simple text prompts        |
| **Pydantic Model** | `ResearchRequest(topic="AI", depth=5)`            | Type-safe structured input |
| **List**           | `["AI", "ML", "LLMs"]`                            | Multiple items to process  |
| **Dictionary**     | `{"query": "AI", "sources": ["web", "academic"]}` | Key-value pairs            |

<Note>
  When this input is passed to an `Agent` or `Team`, it will be serialized to a
  string before being passed to the agent or team.
</Note>

See more on Pydantic as input in the [Advanced Workflows](/concepts/workflows/input-and-output#structured-inputs-with-pydantic) documentation.

## Structured Inputs with Pydantic

Leverage Pydantic models for type-safe, validated workflow inputs:

```python  theme={null}
from pydantic import BaseModel, Field

class ResearchRequest(BaseModel):
    topic: str = Field(description="Research topic")
    depth: int = Field(description="Research depth (1-10)")
    sources: List[str] = Field(description="Preferred sources")

workflow.print_response(
    message=ResearchRequest(
        topic="AI trends 2024",
        depth=8,
        sources=["academic", "industry"]
    )
)
```

### Validating the input

You can set `input_schema` on the Workflow to validate the input. If you then pass the input as a dictionary, it will be automatically validated against the schema.

```python  theme={null}
class ResearchTopic(BaseModel):
    """Structured research topic with specific requirements"""

    topic: str
    focus_areas: List[str] = Field(description="Specific areas to focus on")
    target_audience: str = Field(description="Who this research is for")
    sources_required: int = Field(description="Number of sources needed", default=5)

workflow = Workflow(
        name="Content Creation Workflow",
        description="Automated content creation from blog posts to social media",
        db=SqliteDb(
            session_table="workflow_session",
            db_file="tmp/workflow.db",
        ),
        steps=[research_step, content_planning_step],
        input_schema=ResearchTopic,
    )

workflow.print_response(
        input={
            "topic": "AI trends in 2024",
            "focus_areas": ["Machine Learning", "Computer Vision"],
            "target_audience": "Tech professionals",
            "sources_required": 8
        },
        markdown=True,
    )
```

### Developer Resources

* [Pydantic Model as Input](/examples/concepts/teams/structured_input_output/pydantic_model_as_input)
* [Workflow with Input Schema Validation](/examples/concepts/workflows/06_workflows_advanced_concepts/workflow_with_input_schema)

## Structured Input/Output at Step Level

Workflows feature a powerful type-safe data flow system enabling each step to:

1. **Receive** structured input (Pydantic models, lists, dicts, or raw strings)
2. **Produce** structured output (validated Pydantic models)
3. **Maintain** type safety throughout entire workflow execution

### Data Flow Between Steps

**Input Processing**

* First step receives the workflow's input message
* Subsequent steps receive the previous step's structured output

**Output Generation**

* Each Agent processes input using its configured `output_schema`
* Output is automatically validated against the defined model

```python  theme={null}
# Define agents with response models
research_agent = Agent(
    name="Research Specialist",
    model=OpenAIChat(id="gpt-4"),
    output_schema=ResearchFindings,  # <-- Set on Agent
)

analysis_agent = Agent(
    name="Analysis Expert", 
    model=OpenAIChat(id="gpt-4"),
    output_schema=AnalysisResults,  # <-- Set on Agent
)

# Steps reference these agents
workflow = Workflow(steps=[
    Step(agent=research_agent),  # Will output ResearchFindings
    Step(agent=analysis_agent)   # Will output AnalysisResults
])
```

### Structured Data Transformation in Custom Functions

Custom functions can access structured output from previous steps via `step_input.previous_step_content`, preserving original Pydantic model types.

**Transformation Pattern**

* **Type-Check Inputs**: Use `isinstance(step_input.previous_step_content, ModelName)` to verify input structure
* **Modify Data**: Extract fields, process them, and construct new Pydantic models
* **Return Typed Output**: Wrap the new model in `StepOutput(content=new_model)` for type safety

**Example Implementation**

```python  theme={null}
   def transform_data(step_input: StepInput) -> StepOutput:
       research = step_input.previous_step_content  # Type: ResearchFindings
       analysis = AnalysisReport(
           analysis_type="Custom",
           key_findings=[f"Processed: {research.topic}"],
           ...  # Modified fields
       )
       return StepOutput(content=analysis)
```

### Developer Resources

* [Structured IO at each Step Level](/examples/concepts/workflows/06_workflows_advanced_concepts/structured_io_at_each_step_level)

## Media Input and Processing

Workflows seamlessly handle media artifacts (images, videos, audio) throughout the execution pipeline, enabling rich multimedia processing workflows.

**Media Flow System**

* **Input Support**: Media can be provided to `Workflow.run()` and `Workflow.print_response()`
* **Step Propagation**: Media is passed through to individual steps (Agents, Teams, or Custom Functions)
* **Artifact Accumulation**: Each step receives shared media from previous steps and can produce additional outputs
* **Format Compatibility**: Automatic conversion between artifact formats ensures seamless integration
* **Complete Preservation**: Final `WorkflowRunOutput` contains all accumulated media from the entire execution chain

Here's an example of how to pass image as input:

```python  theme={null}
from agno.agent import Agent
from agno.media import Image
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.workflow import Step, Workflow
from agno.db.sqlite import SqliteDb

# Define agents
image_analyzer = Agent(
    name="Image Analyzer",
    model=OpenAIChat(id="gpt-5-mini"),
    instructions="Analyze the provided image and extract key details, objects, and context.",
)

news_researcher = Agent(
    name="News Researcher", 
    model=OpenAIChat(id="gpt-5-mini"),
    tools=[DuckDuckGoTools()],
    instructions="Search for latest news and information related to the analyzed image content.",
)

# Define steps
analysis_step = Step(
    name="Image Analysis Step",
    agent=image_analyzer,
)

research_step = Step(
    name="News Research Step", 
    agent=news_researcher,
)

# Create workflow with media input
media_workflow = Workflow(
    name="Image Analysis and Research Workflow",
    description="Analyze an image and research related news",
    steps=[analysis_step, research_step],
    db=SqliteDb(db_file="tmp/workflow.db"),
)

# Run workflow with image input
if __name__ == "__main__":
    media_workflow.print_response(
        input="Please analyze this image and find related news",
        images=[
            Image(url="https://upload.wikimedia.org/wikipedia/commons/0/0c/GoldenGateBridge-001.jpg")
        ],
        markdown=True,
    )
```

<Note>
  If you are using `Workflow.run()`, you need to use `WorkflowRunOutput` to access the images, videos, and audio.

  ```python  theme={null}
  from agno.run.workflow import WorkflowRunOutput

  response: WorkflowRunOutput = media_workflow.run(
      input="Please analyze this image and find related news",
      images=[
          Image(url="https://upload.wikimedia.org/wikipedia/commons/0/0c/GoldenGateBridge-001.jpg")
      ],
      markdown=True,
  )

  print(response.images)
  ```
</Note>

Similarly, you can pass `Video` and `Audio` as input.

### Developer Resources

* [Image/Video Selection Sequence](/examples/concepts/workflows/05_workflows_conditional_branching/selector_for_image_video_generation_pipelines)

# How does shared state work between workflows, teams and agents?

> Learn to handle shared state between the different components of a Workflow.

Workflow session state enables sharing and updating state data across all components within a workflow: agents, teams, and custom functions.

Session state data will be persisted if a database is available, and loaded from there in subsequent runs of the workflow.

<img className="block dark:hidden" src="https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-session-state-light.png?fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=eb9f2f37de2699763ae1cab8b26e5792" alt="Workflows session state diagram" data-og-width="2199" width="2199" data-og-height="1203" height="1203" data-path="images/workflows-session-state-light.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-session-state-light.png?w=280&fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=be8235601f44c3d5c899e769bd7e10a7 280w, https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-session-state-light.png?w=560&fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=c54d2a340511cf08b6f62ee2dc725ab6 560w, https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-session-state-light.png?w=840&fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=a8704d97da7f5fd6490acd6e9e847f21 840w, https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-session-state-light.png?w=1100&fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=88b25555c12572fbb92d1b7724e77cc6 1100w, https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-session-state-light.png?w=1650&fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=e0c24367b61326e2115cfa74059d1316 1650w, https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-session-state-light.png?w=2500&fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=c5d4f68f953670a714b4a5d334f9b5fb 2500w" />

<img className="hidden dark:block" src="https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-session-state.png?fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=5e56bc8354bbb79f31d6c4140e5dea2e" alt="Workflows session state diagram" data-og-width="2199" width="2199" data-og-height="1203" height="1203" data-path="images/workflows-session-state.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-session-state.png?w=280&fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=494e73f94a71a1611b068a2561ed6c7a 280w, https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-session-state.png?w=560&fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=3c754db0830ab28e7640f553c9dd93a9 560w, https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-session-state.png?w=840&fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=fa17e5cf5ebf2d45a85a328abbd52bf7 840w, https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-session-state.png?w=1100&fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=e82eae67add368163f04fcb09dab4271 1100w, https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-session-state.png?w=1650&fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=d66bd915da648ef787dd86aa2a5eede6 1650w, https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-session-state.png?w=2500&fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=5bf1239ad621457d50d67b28153b9a1b 2500w" />

## How Workflow Session State Works

### 1. State Initialization

Initialize session state when creating a workflow. The session state can start empty or with predefined data that all workflow components can access and modify.

```python  theme={null}
shopping_workflow = Workflow(
    name="Shopping List Workflow",
    steps=[manage_items_step, view_list_step],
    session_state={"shopping_list": []},  # Initialize with structured data
)
```

### 2. Access and Modify State Data

All workflow components - agents, teams, and functions - can read from and write to the shared session state. This enables persistent data flow and coordination across the entire workflow execution.

From tools, you can access the session state via `run_context.session_state`.

**Example: Shopping List Management**

```python  theme={null}
from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai.chat import OpenAIChat
from agno.workflow.step import Step
from agno.workflow.workflow import Workflow
from agno.run import RunContext

db = SqliteDb(db_file="tmp/workflow.db")


# Define tools to manage a shopping list in workflow session state
def add_item(run_context: RunContext, item: str) -> str:
    """Add an item to the shopping list in workflow session state.

    Args:
        item (str): The item to add to the shopping list
    """
    if not run_context.session_state:
        run_context.session_state = {}

    # Check if item already exists (case-insensitive)
    existing_items = [
        existing_item.lower() for existing_item in run_context.session_state["shopping_list"]
    ]
    if item.lower() not in existing_items:
        run_context.session_state["shopping_list"].append(item)
        return f"Added '{item}' to the shopping list."
    else:
        return f"'{item}' is already in the shopping list."


def remove_item(run_context: RunContext, item: str) -> str:
    """Remove an item from the shopping list in workflow session state.

    Args:
        item (str): The item to remove from the shopping list
    """
    if not run_context.session_state:
        run_context.session_state = {}

    if len(run_context.session_state["shopping_list"]) == 0:
        return f"Shopping list is empty. Cannot remove '{item}'."

    # Find and remove item (case-insensitive)
    shopping_list = run_context.session_state["shopping_list"]
    for i, existing_item in enumerate(shopping_list):
        if existing_item.lower() == item.lower():
            removed_item = shopping_list.pop(i)
            return f"Removed '{removed_item}' from the shopping list."

    return f"'{item}' not found in the shopping list."


def remove_all_items(run_context: RunContext) -> str:
    """Remove all items from the shopping list in workflow session state."""
    if not run_context.session_state:
        run_context.session_state = {}

    run_context.session_state["shopping_list"] = []
    return "Removed all items from the shopping list."


def list_items(run_context: RunContext) -> str:
    """List all items in the shopping list from workflow session state."""
    if not run_context.session_state:
        run_context.session_state = {}

    if len(run_context.session_state["shopping_list"]) == 0:
        return "Shopping list is empty."

    items = run_context.session_state["shopping_list"]
    items_str = "\n".join([f"- {item}" for item in items])
    return f"Shopping list:\n{items_str}"


# Create agents with tools that use workflow session state
shopping_assistant = Agent(
    name="Shopping Assistant",
    model=OpenAIChat(id="gpt-5-mini"),
    tools=[add_item, remove_item, list_items],
    instructions=[
        "You are a helpful shopping assistant.",
        "You can help users manage their shopping list by adding, removing, and listing items.",
        "Always use the provided tools to interact with the shopping list.",
        "Be friendly and helpful in your responses.",
    ],
)

list_manager = Agent(
    name="List Manager",
    model=OpenAIChat(id="gpt-5-mini"),
    tools=[list_items, remove_all_items],
    instructions=[
        "You are a list management specialist.",
        "You can view the current shopping list and clear it when needed.",
        "Always show the current list when asked.",
        "Confirm actions clearly to the user.",
    ],
)

# Create steps
manage_items_step = Step(
    name="manage_items",
    description="Help manage shopping list items (add/remove)",
    agent=shopping_assistant,
)

view_list_step = Step(
    name="view_list",
    description="View and manage the complete shopping list",
    agent=list_manager,
)

# Create workflow with workflow_session_state
shopping_workflow = Workflow(
    name="Shopping List Workflow",
    db=db,
    steps=[manage_items_step, view_list_step],
    session_state={"shopping_list": []},
)

if __name__ == "__main__":
    # Example 1: Add items to the shopping list
    print("=== Example 1: Adding Items ===")
    shopping_workflow.print_response(
        input="Please add milk, bread, and eggs to my shopping list."
    )
    print("Workflow session state:", shopping_workflow.get_session_state())

    # Example 2: Add more items and view list
    print("\n=== Example 2: Adding More Items ===")
    shopping_workflow.print_response(
        input="Add apples and bananas to the list, then show me the complete list."
    )
    print("Workflow session state:", shopping_workflow.get_session_state())

    # Example 3: Remove items
    print("\n=== Example 3: Removing Items ===")
    shopping_workflow.print_response(
        input="Remove bread from the list and show me what's left."
    )
    print("Workflow session state:", shopping_workflow.get_session_state())

    # Example 4: Clear the entire list
    print("\n=== Example 4: Clearing List ===")
    shopping_workflow.print_response(
        input="Clear the entire shopping list and confirm it's empty."
    )
    print("Final workflow session state:", shopping_workflow.get_session_state())
```

See the [RunContext schema](/reference/run/run_context) for more information.

### 3. `run_context` as a parameter for custom python functions step in workflow

You can add the `run_context` parameter to the Python functions you use as custom steps.

The `run_context` object will be automatically injected when running the function.

You can use it to read and modify the session state, via `run_context.session_state`.

<Note>
  On the function of the custom python function step for a workflow

  ```python  theme={null}
  from agno.run import RunContext

  def custom_function_step(step_input: StepInput, run_context: RunContext):
      """Update the workflow session state"""
      run_context.session_state["test"] = test_1
  ```
</Note>

See [examples](/examples/concepts/workflows/06_workflows_advanced_concepts/access_session_state_in_custom_python_function_step) for more details.

The `run_context` is also available as a parameter in the evaluator and selector functions of the `Condition` and `Router` steps:

```python  theme={null}
from agno.run import RunContext

def evaluator_function(step_input: StepInput, run_context: RunContext):
    return run_context.session_state["test"] == "test_1"

condition_step = Condition(
    name="condition_step",
    evaluator=evaluator_function,
    steps=[step_1, step_2],
)
```

```python  theme={null}
from agno.run import RunContext

def selector_function(step_input: StepInput, run_context: RunContext):
    return run_context.session_state["test"] == "test_1"

router_step = Router(
    name="router_step",
    selector=selector_function,
    choices=[step_1, step_2],
)
```

See example of [Session State in Condition Evaluator Function](/examples/concepts/workflows/06_workflows_advanced_concepts/access_session_state_in_condition_evaluator_function)
and [Session State in Router Selector Function](/examples/concepts/workflows/06_workflows_advanced_concepts/access_session_state_in_router_selector_function) for more details.

## Key Benefits

**Persistent State Management**

* Data persists across all workflow steps and components
* Enables complex, stateful workflows with memory
* Supports deterministic execution with consistent state

**Cross-Component Coordination**

* Agents, teams, and functions share the same state object
* Enables sophisticated collaboration patterns
* Maintains data consistency across workflow execution

**Flexible Data Structure**

* Use any Python data structure (dictionaries, lists, objects)
* Structure data to match your workflow requirements
* Access and modify state through standard Python operations

<Note>
  The `run_context` object, containing the session state, is automatically passed to all agents and teams within a
  workflow, enabling seamless collaboration and data sharing between different
  components without manual state management.
</Note>

## Useful Links

<CardGroup cols={2}>
  <Card title="Agent Examples" icon="user" href="https://github.com/agno-agi/agno/tree/main/cookbook/workflows/_06_advanced_concepts/_04_shared_session_state/shared_session_state_with_agent.py">
    See how agents interact with shared session state
  </Card>

  <Card title="Team Examples" icon="users" href="https://github.com/agno-agi/agno/tree/main/cookbook/workflows/_06_advanced_concepts/_04_shared_session_state/shared_session_state_with_team.py">
    Learn how teams coordinate using shared state
  </Card>
</CardGroup>


# Additional Data and Metadata

> How to pass additional data to workflows

**When to Use**
Pass metadata, configuration, or contextual information to specific steps without cluttering the main workflow message flow.

**Key Benefits**

* **Separation of Concerns**: Keep workflow logic separate from metadata
* **Step-Specific Context**: Access additional information in custom functions
* **Clean Message Flow**: Main message stays focused on content
* **Flexible Configuration**: Pass user info, priorities, settings, and more

**Access Pattern**
Use `step_input.additional_data` for dictionary access to all additional data passed to the workflow.

## Example

```python  theme={null}
from agno.workflow import Step, Workflow, StepInput, StepOutput

def custom_content_planning_function(step_input: StepInput) -> StepOutput:
    """Custom function that uses additional_data for enhanced context"""
    
    # Access the main workflow message
    message = step_input.input
    previous_content = step_input.previous_step_content
    
    # Access additional_data that was passed with the workflow
    additional_data = step_input.additional_data or {}
    user_email = additional_data.get("user_email", "No email provided")
    priority = additional_data.get("priority", "normal")
    client_type = additional_data.get("client_type", "standard")
    
    # Create enhanced planning prompt with context
    planning_prompt = f"""
        STRATEGIC CONTENT PLANNING REQUEST:
        
        Core Topic: {message}
        Research Results: {previous_content[:500] if previous_content else "No research results"}
        
        Additional Context:
        - Client Type: {client_type}
        - Priority Level: {priority}
        - Contact Email: {user_email}
        
        {"🚨 HIGH PRIORITY - Expedited delivery required" if priority == "high" else "📝 Standard delivery timeline"}
        
        Please create a detailed, actionable content plan.
    """
    
    response = content_planner.run(planning_prompt)
    
    enhanced_content = f"""
        ## Strategic Content Plan
        
        **Planning Topic:** {message}
        **Client Details:** {client_type} | {priority.upper()} priority | {user_email}
        
        **Content Strategy:**
        {response.content}
    """
    
    return StepOutput(content=enhanced_content)

# Define workflow with steps
workflow = Workflow(
    name="Content Creation Workflow",
    steps=[
        Step(name="Research Step", team=research_team),
        Step(name="Content Planning Step", executor=custom_content_planning_function),
    ]
)

# Run workflow with additional_data
workflow.print_response(
    input="AI trends in 2024",
    additional_data={
        "user_email": "kaustubh@agno.com",
        "priority": "high",
        "client_type": "enterprise",
        "budget": "$50000",
        "deadline": "2024-12-15"
    },
    markdown=True,
    stream=True
)
```

## Developer Resources

* [Step with Function and Additional Data](/examples/concepts/workflows/06_workflows_advanced_concepts/step_with_function_additional_data)


# Workflow History & Continuous Execution

> Build conversational workflows that maintain context across multiple executions, creating truly intelligent and natural interactions.

Workflow History enables your Agno workflows to remember and reference previous conversations, transforming isolated executions into continuous, context-aware interactions.

Instead of starting fresh each time, with Workflow History you can:

* **Build on previous interactions** - Reference the context of past interactions
* **Avoid repetitive questions** - Avoid requesting previously provided information
* **Maintain context continuity** - Create a conversational experience
* **Learn from patterns** - Analyze historical data to make better decisions

<Tip>
  Note that this feature is different from `add_history_to_context`.
  This does not add the history of a particular agent or team, but the full workflow history to either all or some steps.
</Tip>

## How It Works

When workflow history is enabled, previous messages are automatically injected into agent/team inputs as structured context:

```xml  theme={null}
<workflow_history_context>
[run-1]
input: Create content about AI in healthcare
response: # AI in Healthcare: Transforming Patient Care...

[run-2] 
input: Make it more family-focused
response: # AI in Family Healthcare: A Parent's Guide...
</workflow_history_context>

Your current input goes here...
```

Along with this, in using Steps with custom functions, you can access this history in the following ways:

1. As a formatted context string as shown above
2. In a structured format as well for more control

```bash  theme={null}
[
    (<workflow input from run 1>)(<workflow output from run 1>),
    (<workflow input from run 2>)(<workflow output from run 2>),
]
```

<Note>
  A database is required to use Workflow history. Runs across different executions will be persisted there.
</Note>

Example-

```python  theme={null}
def custom_function(step_input: StepInput) -> StepOutput:
    # Option 1: Structured data for analysis
    history_tuples = step_input.get_workflow_history(num_runs=3)
    for user_input, workflow_output in history_tuples:
        # Process each conversation turn

    # Option 2: Formatted context for agents  
    context_string = step_input.get_workflow_history_context(num_runs=3)

    return StepOutput(content="Analysis complete")
```

<Note>
  You can use these helper functions to access the history:

  * `step_input.get_workflow_history(num_runs=3)`
  * `step_input.get_workflow_history_context(num_runs=3)`
</Note>

Refer to [StepInput](/reference/workflows/step_input) reference for more details.

## Control Levels

You can be specific about which Steps to add the history to:

### Workflow-Level History

Add workflow history to **all steps** in the workflow:

```python  theme={null}
workflow = Workflow(
    steps=[research_step, analysis_step, writing_step],
    add_workflow_history_to_steps=True  # All steps get history
)
```

### Step-Level History

Add workflow history to **specific steps** only:

```python  theme={null}
Step(
    name="Content Creator", 
    agent=content_agent,
    add_workflow_history=True  # Only this step gets history
)
```

<Note>
  You can also put `add_workflow_history=False` to disable history for a specific step.
</Note>

## Precedence Logic

**Step-level settings always take precedence over workflow-level settings**:

```python  theme={null}
workflow = Workflow(
    steps=[
        Step("Research", agent=research_agent),                              # None → inherits workflow setting
        Step("Analysis", agent=analysis_agent, add_workflow_history=False),  # False → overrides workflow  
        Step("Writing", agent=writing_agent, add_workflow_history=True),     # True → overrides workflow
    ],
    add_workflow_history_to_steps=True  # Default for all steps
)
```

### History Length Control

**By default, all available history is included** (no limit). It is recommended to use a fixed history run limit to avoid bloating the LLM context window.

You can control this at both levels:

```python  theme={null}
# Workflow-level: limit history for all steps
workflow = Workflow(
    add_workflow_history_to_steps=True,
    num_history_runs=5  # Only last 5 runs
)

# Step-level: override for specific steps
Step("Analysis", agent=analysis_agent, 
     add_workflow_history=True,
     num_history_runs=3  # Only last 3 runs for this step
)
```

## Developer Resources

Explore the different examples in [Workflow History Examples](/examples/concepts/workflows/06_workflows_advanced_concepts/workflow_history/01_single_step_continuous_execution_workflow) for more details.


# Metrics

> Understanding workflow run and session metrics in Agno

When you run a workflow in Agno, the response you get (**WorkflowRunOutput**) includes detailed metrics about the workflow execution.

These metrics help you understand token usage, execution time, performance, and step-level details across all agents, teams, and custom functions in your workflow.

Metrics are available at multiple levels:

* **Per workflow**: Each `WorkflowRunOutput` includes a metrics object containing the workflow duration.
* **Per step**: Each step has its own metrics including duration, token usage, and model information.
* **Per session**: Session metrics aggregate all step-level metrics across all runs in the session.

## Example Usage

Here's how you can access and use workflow metrics:

```python  theme={null}
from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.team import Team
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.hackernews import HackerNewsTools
from agno.workflow import Step, Workflow
from rich.pretty import pprint

# Define agents
hackernews_agent = Agent(
    name="Hackernews Agent",
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[HackerNewsTools()],
    role="Extract key insights from Hackernews posts",
)

web_agent = Agent(
    name="Web Agent",
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[DuckDuckGoTools()],
    role="Search the web for latest trends",
)

# Define research team
research_team = Team(
    name="Research Team",
    members=[hackernews_agent, web_agent],
    instructions="Research tech topics from Hackernews and the web",
)

content_planner = Agent(
    name="Content Planner",
    model=OpenAIChat(id="gpt-4o"),
    instructions="Plan a content schedule based on research",
)

# Create workflow
workflow = Workflow(
    name="Content Creation Workflow",
    db=SqliteDb(db_file="tmp/workflow.db"),
    steps=[
        Step(name="Research Step", team=research_team),
        Step(name="Content Planning Step", agent=content_planner),
    ],
)

# Run workflow
response = workflow.run(input="AI trends in 2024")

# Print workflow-level metrics
print("Workflow Metrics")
if response.metrics:
    pprint(response.metrics.to_dict())

# Print workflow duration
if response.metrics and response.metrics.duration:
    print(f"\nTotal execution time: {response.metrics.duration:.2f} seconds")

# Print step-level metrics
print("Step Metrics")
if response.metrics:
    for step_name, step_metrics in response.metrics.steps.items():
        print(f"\nStep: {step_name}")
        print(f"Executor: {step_metrics.executor_name} ({step_metrics.executor_type})")
        if step_metrics.metrics:
            print(f"Duration: {step_metrics.metrics.duration:.2f}s")
            print(f"Tokens: {step_metrics.metrics.total_tokens}")

# Print session metrics
print("Session Metrics")
pprint(workflow.get_session_metrics().to_dict())
```

You'll see the outputs with following information:

**Workflow-level metrics:**

* `duration`: Total workflow execution time in seconds (from start to finish, including orchestration overhead)
* `steps`: Dictionary mapping step names to their individual step metrics

**Step-level metrics:**

* `step_name`: Name of the step
* `executor_type`: Type of executor ("agent", "team", or "function")
* `executor_name`: Name of the executor
* `metrics`: Execution metrics including tokens, duration, and model information (see [Metrics schema](/reference/agents/metrics))

**Session metrics:**

* Aggregates step-level metrics (tokens, duration) across all runs in the session
* Includes only agent/team execution time, not workflow orchestration overhead

## Developer Resources

* View the [WorkflowRunOutput schema](/reference/workflows/workflow_run_output)
