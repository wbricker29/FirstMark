# Workflow Patterns

> Master deterministic workflow patterns including sequential, parallel, conditional, and looping execution for reliable multi-agent automation.

Build deterministic, production-ready workflows that orchestrate agents, teams, and functions with predictable execution patterns. This comprehensive guide covers all workflow types, from simple sequential processes to complex branching logic with parallel execution and dynamic routing.

Unlike free-form agent interactions, these patterns provide structured automation with consistent, repeatable results ideal for production systems.

## Building Blocks

The core building blocks of Agno Workflows are:

| Component     | Purpose                         |
| ------------- | ------------------------------- |
| **Step**      | Basic execution unit            |
| **Agent**     | AI assistant with specific role |
| **Team**      | Coordinated group of agents     |
| **Function**  | Custom Python logic             |
| **Parallel**  | Concurrent execution            |
| **Condition** | Conditional execution           |
| **Loop**      | Iterative execution             |
| **Router**    | Dynamic routing                 |

Agno Workflows support multiple execution patterns that can be combined to build sophisticated automation systems.
Each pattern serves specific use cases and can be composed together for complex workflows.

<CardGroup cols={2}>
  <Card title="Sequential Workflows" icon="arrow-right" href="/concepts/workflows/workflow-patterns/sequential">
    Linear execution with step-by-step processing
  </Card>

  <Card title="Parallel Workflows" icon="arrows-split-up-and-left" href="/concepts/workflows/workflow-patterns/parallel-workflow">
    Concurrent execution for independent tasks
  </Card>

  <Card title="Conditional Workflows" icon="code-branch" href="/concepts/workflows/workflow-patterns/conditional-workflow">
    Branching logic based on conditions
  </Card>

  <Card title="Iterative Workflows" icon="rotate" href="/concepts/workflows/workflow-patterns/iterative-workflow">
    Loop-based execution with quality controls
  </Card>

  <Card title="Branching Workflows" icon="sitemap" href="/concepts/workflows/workflow-patterns/branching-workflow">
    Dynamic routing and path selection
  </Card>

  <Card title="Grouped Steps" icon="layer-group" href="/concepts/workflows/workflow-patterns/grouped-steps-workflow">
    Reusable step sequences and modular design
  </Card>
</CardGroup>

## Advanced Patterns

<CardGroup cols={2}>
  <Card title="Function-Based Workflows" icon="function" href="/concepts/workflows/workflow-patterns/custom-function-step-workflow">
    Pure Python workflows with complete control
  </Card>

  <Card title="Multi-Pattern Combinations" icon="puzzle-piece" href="/concepts/workflows/workflow-patterns/advanced-workflow-patterns">
    Complex workflows combining multiple patterns
  </Card>
</CardGroup>

# Sequential Workflows

> Linear, deterministic processes where each step depends on the output of the previous step.

Sequential workflows ensure predictable execution order and clear data flow between steps.

**Example Flow**: Research → Data Processing → Content Creation → Final Review

Sequential workflows ensure predictable execution order and clear data flow between steps.

```python sequential_workflow.py theme={null}
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

<Note>
  For more information on how to use custom functions, refer to the
  [Workflow with custom function step](/concepts/workflows/workflow-patterns/custom-function-step-workflow) page.
</Note>

**See Example**:

* [Sequence of Functions and Agents](/examples/concepts/workflows/01-basic-workflows/sequence_of_functions_and_agents) - Complete workflow with functions and agents

<Note>
  `StepInput` and `StepOutput` provides standardized interfaces for data flow between steps:
  So if you make a custom function as an executor for a step, make sure that the input and output types are compatible with the `StepInput` and `StepOutput` interfaces.
  This will ensure that your custom function can seamlessly integrate into the workflow system.

  Take a look at the schemas for [`StepInput`](/reference/workflows/step_input) and [`StepOutput`](/reference/workflows/step_output).
</Note>

# Fully Python Workflow

> Keep it Simple with Pure Python, in v1 workflows style

**Keep it Simple with Pure Python**: If you prefer the Workflows 1.0 approach or need maximum flexibility, you can still use a single Python function to handle everything.
This approach gives you complete control over the execution flow while still benefiting from workflow features like storage, streaming, and session management.

Replace all the steps in the workflow with a single executable function where you can control everything.

```python fully_python_workflow.py theme={null}
from agno.workflow import Workflow, WorkflowExecutionInput

def custom_workflow_function(workflow: Workflow, execution_input: WorkflowExecutionInput):
    # Custom orchestration logic
    research_result = research_team.run(execution_input.message)
    analysis_result = analysis_agent.run(research_result.content)
    return f"Final: {analysis_result.content}"

workflow = Workflow(
    name="Function-Based Workflow",
    steps=custom_workflow_function  # Single function replaces all steps
)

workflow.print_response("Evaluate the market potential for quantum computing applications", markdown=True)
```

**See Example**:

* [Function-Based Workflow](/examples/concepts/workflows/01-basic-workflows/function_instead_of_steps) - Complete function-based workflow

For migration from 1.0 style workflows, refer to the page for [Migrating to Workflows 2.0](/how-to/v2-migration)

# Step-Based Workflows

> Named steps for better logging and support on the AgentOS chat page

**You can name your steps** for better logging and future support on the Agno platform.
This also changes the name of a step when accessing that step's output inside a `StepInput` object.

## Example

```python  theme={null}
from agno.workflow import Step, Workflow

# Named steps for better tracking
workflow = Workflow(
    name="Content Creation Pipeline",
    steps=[
        Step(name="Research Phase", team=researcher),
        Step(name="Analysis Phase", executor=custom_function),
        Step(name="Writing Phase", agent=writer),
    ]
)

workflow.print_response(
    "AI trends in 2024",
    markdown=True,
)
```

## Developer Resources

* [Sequence of Steps](/examples/concepts/workflows/01-basic-workflows/sequence_of_steps)
* [Step with a Custom Function](/examples/concepts/workflows/01-basic-workflows/step_with_function)

## Reference

For complete API documentation, see [Step Reference](/reference/workflows/step).

# Custom Functions in Workflows

> How to use custom functions in workflows

Custom functions provide maximum flexibility by allowing you to define specific logic for step execution. Use them to preprocess inputs, orchestrate agents and teams, and postprocess outputs with complete programmatic control.

**Key Capabilities**

* **Custom Logic**: Implement complex business rules and data transformations
* **Agent Integration**: Call agents and teams within your custom processing logic
* **Data Flow Control**: Transform outputs between steps for optimal data handling

**Implementation Pattern**
Define a `Step` with a custom function as the `executor`. The function must accept a `StepInput` object and return a `StepOutput` object, ensuring seamless integration with the workflow system.

<img className="block dark:hidden" src="https://mintcdn.com/agno-v2/jBP_3mGLN1rT3Ezh/images/custom-function-steps-light.png?fit=max&auto=format&n=jBP_3mGLN1rT3Ezh&q=85&s=d9c94fbc2094b100df2fde1e4767f358" alt="Custom function step workflow diagram" data-og-width="2001" width="2001" data-og-height="756" height="756" data-path="images/custom-function-steps-light.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/agno-v2/jBP_3mGLN1rT3Ezh/images/custom-function-steps-light.png?w=280&fit=max&auto=format&n=jBP_3mGLN1rT3Ezh&q=85&s=cc6fdbdbcd274ffd8eeaf936653e9487 280w, https://mintcdn.com/agno-v2/jBP_3mGLN1rT3Ezh/images/custom-function-steps-light.png?w=560&fit=max&auto=format&n=jBP_3mGLN1rT3Ezh&q=85&s=7135a981cbf2afbbfc9e8a772843ca90 560w, https://mintcdn.com/agno-v2/jBP_3mGLN1rT3Ezh/images/custom-function-steps-light.png?w=840&fit=max&auto=format&n=jBP_3mGLN1rT3Ezh&q=85&s=084fd07440b87980f0899dea2b0b5ba1 840w, https://mintcdn.com/agno-v2/jBP_3mGLN1rT3Ezh/images/custom-function-steps-light.png?w=1100&fit=max&auto=format&n=jBP_3mGLN1rT3Ezh&q=85&s=9d57ad4d5f051dc65185bf29ad759118 1100w, https://mintcdn.com/agno-v2/jBP_3mGLN1rT3Ezh/images/custom-function-steps-light.png?w=1650&fit=max&auto=format&n=jBP_3mGLN1rT3Ezh&q=85&s=b1ba9db7305207a7867efa4ef47912dc 1650w, https://mintcdn.com/agno-v2/jBP_3mGLN1rT3Ezh/images/custom-function-steps-light.png?w=2500&fit=max&auto=format&n=jBP_3mGLN1rT3Ezh&q=85&s=a4e94cf04d1a1bb212f971ce60cefe5b 2500w" />

<img className="hidden dark:block" src="https://mintcdn.com/agno-v2/jBP_3mGLN1rT3Ezh/images/custom-function-steps-dark.png?fit=max&auto=format&n=jBP_3mGLN1rT3Ezh&q=85&s=537393db1d76a7d4c38d43e40c622300" alt="Custom function step workflow diagram" data-og-width="2001" width="2001" data-og-height="756" height="756" data-path="images/custom-function-steps-dark.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/agno-v2/jBP_3mGLN1rT3Ezh/images/custom-function-steps-dark.png?w=280&fit=max&auto=format&n=jBP_3mGLN1rT3Ezh&q=85&s=40450040ca47de4fa286b95de2e285ed 280w, https://mintcdn.com/agno-v2/jBP_3mGLN1rT3Ezh/images/custom-function-steps-dark.png?w=560&fit=max&auto=format&n=jBP_3mGLN1rT3Ezh&q=85&s=ef0a1060f07688a21b866766dc10526b 560w, https://mintcdn.com/agno-v2/jBP_3mGLN1rT3Ezh/images/custom-function-steps-dark.png?w=840&fit=max&auto=format&n=jBP_3mGLN1rT3Ezh&q=85&s=9c5572c23d25046db363ecaeeb65e3d6 840w, https://mintcdn.com/agno-v2/jBP_3mGLN1rT3Ezh/images/custom-function-steps-dark.png?w=1100&fit=max&auto=format&n=jBP_3mGLN1rT3Ezh&q=85&s=991e880aee26c31a9484d8603e0be424 1100w, https://mintcdn.com/agno-v2/jBP_3mGLN1rT3Ezh/images/custom-function-steps-dark.png?w=1650&fit=max&auto=format&n=jBP_3mGLN1rT3Ezh&q=85&s=0a8c70a163f2ba4a5cd5dfdc487ff14d 1650w, https://mintcdn.com/agno-v2/jBP_3mGLN1rT3Ezh/images/custom-function-steps-dark.png?w=2500&fit=max&auto=format&n=jBP_3mGLN1rT3Ezh&q=85&s=aec1041004efd198455fcb6a740f008d 2500w" />

## Example

```python  theme={null}
content_planning_step = Step(
    name="Content Planning Step",
    executor=custom_content_planning_function,
)

def custom_content_planning_function(step_input: StepInput) -> StepOutput:
    """
    Custom function that does intelligent content planning with context awareness
    """
    message = step_input.input
    previous_step_content = step_input.previous_step_content

    # Create intelligent planning prompt
    planning_prompt = f"""
        STRATEGIC CONTENT PLANNING REQUEST:

        Core Topic: {message}

        Research Results: {previous_step_content[:500] if previous_step_content else "No research results"}

        Planning Requirements:
        1. Create a comprehensive content strategy based on the research
        2. Leverage the research findings effectively
        3. Identify content formats and channels
        4. Provide timeline and priority recommendations
        5. Include engagement and distribution strategies

        Please create a detailed, actionable content plan.
    """

    try:
        response = content_planner.run(planning_prompt)

        enhanced_content = f"""
            ## Strategic Content Plan

            **Planning Topic:** {message}

            **Research Integration:** {"✓ Research-based" if previous_step_content else "✗ No research foundation"}

            **Content Strategy:**
            {response.content}

            **Custom Planning Enhancements:**
            - Research Integration: {"High" if previous_step_content else "Baseline"}
            - Strategic Alignment: Optimized for multi-channel distribution
            - Execution Ready: Detailed action items included
        """.strip()

        return StepOutput(content=enhanced_content)

    except Exception as e:
        return StepOutput(
            content=f"Custom content planning failed: {str(e)}",
            success=False,
        )
```

**Standard Pattern**
All custom functions follow this consistent structure:

```python  theme={null}
def custom_content_planning_function(step_input: StepInput) -> StepOutput:
    # 1. Custom preprocessing
    # 2. Call agents/teams as needed
    # 3. Custom postprocessing
    return StepOutput(content=enhanced_content)
```

## Class-based executor

You can also use a class-based executor by defining a class that implements the `__call__` method.

```python  theme={null}
class CustomExecutor:
    def __call__(self, step_input: StepInput) -> StepOutput:
        # 1. Custom preprocessing
        # 2. Call agents/teams as needed
        # 3. Custom postprocessing
        return StepOutput(content=enhanced_content)

content_planning_step = Step(
    name="Content Planning Step",
    executor=CustomExecutor(),
)
```

**When is this useful?:**

* **Configuration at initialization**: Pass in settings, API keys, or behavior flags when creating the executor
* **Stateful execution**: Maintain counters, caches, or track information across multiple workflow runs
* **Reusable components**: Create configured executor instances that can be shared across multiple workflows

```python  theme={null}
class CustomExecutor:
    def __init__(self, max_retries: int = 3, use_cache: bool = True):
        # Configuration passed during instantiation
        self.max_retries = max_retries
        self.use_cache = use_cache
        self.call_count = 0  # Stateful tracking

    def __call__(self, step_input: StepInput) -> StepOutput:
        self.call_count += 1

        # Access instance configuration and state
        if self.use_cache and self.call_count > 1:
            return StepOutput(content="Using cached result")

        # Your custom logic with access to self.max_retries, etc.
        return StepOutput(content=enhanced_content)

# Instantiate with specific configuration
content_planning_step = Step(
    name="Content Planning Step",
    executor=CustomExecutor(max_retries=5, use_cache=False),
)
```

Also supports async execution by defining the `__call__` method to be an async function.

```python  theme={null}
class CustomExecutor:
    async def __call__(self, step_input: StepInput) -> StepOutput:
        # 1. Custom preprocessing
        # 2. Call agents/teams as needed
        # 3. Custom postprocessing
        return StepOutput(content=enhanced_content)

content_planning_step = Step(
    name="Content Planning Step",
    executor=CustomExecutor(),
)
```

For a detailed example see [Class-based Executor](/examples/concepts/workflows/01-basic-workflows/class_based_executor).

## Streaming execution with custom function step on AgentOS

If you are running an agent or team within the custom function step, you can enable streaming on the [AgentOS chat page](/agent-os/introduction#chat-page) by setting `stream=True` and `stream_events=True` when calling `run()` or `arun()` and yielding the events.

<Note>
  Using the AgentOS, runs will be asynchronous and responses will be streamed.
  This means you must keep the custom function step asynchronous, by using `.arun()` instead of `.run()` to run your Agents or Teams.
</Note>

```python custom_function_step_async_stream.py theme={null}
content_planner = Agent(
    name="Content Planner",
    model=OpenAIChat(id="gpt-4o"),
    instructions=[
        "Plan a content schedule over 4 weeks for the provided topic and research content",
        "Ensure that I have posts for 3 posts per week",
    ],
    db=InMemoryDb(),
)

async def custom_content_planning_function(
    step_input: StepInput,
) -> AsyncIterator[Union[WorkflowRunOutputEvent, StepOutput]]:
    """
    Custom function that does intelligent content planning with context awareness.

    Note: This function calls content_planner.arun() internally, and all events
    from that agent call will automatically get workflow context injected by
    the workflow execution system - no manual intervention required!
    """
    message = step_input.input
    previous_step_content = step_input.previous_step_content

    # Create intelligent planning prompt
    planning_prompt = f"""
        STRATEGIC CONTENT PLANNING REQUEST:

        Core Topic: {message}

        Research Results: {previous_step_content[:500] if previous_step_content else "No research results"}

        Planning Requirements:
        1. Create a comprehensive content strategy based on the research
        2. Leverage the research findings effectively
        3. Identify content formats and channels
        4. Provide timeline and priority recommendations
        5. Include engagement and distribution strategies

        Please create a detailed, actionable content plan.
    """

    try:
        response_iterator = content_planner.arun(
            planning_prompt, stream=True, stream_events=True
        )
        async for event in response_iterator:
            yield event

        response = content_planner.get_last_run_output()

        enhanced_content = f"""
            ## Strategic Content Plan

            **Planning Topic:** {message}

            **Research Integration:** {"✓ Research-based" if previous_step_content else "✗ No research foundation"}

            **Content Strategy:**
            {response.content}

            **Custom Planning Enhancements:**
            - Research Integration: {"High" if previous_step_content else "Baseline"}
            - Strategic Alignment: Optimized for multi-channel distribution
            - Execution Ready: Detailed action items included
        """.strip()

        yield StepOutput(content=enhanced_content)

    except Exception as e:
        yield StepOutput(
            content=f"Custom content planning failed: {str(e)}",
            success=False,
        )
```

<Note>
  Streaming in case of a class-based executor also works the same way by defining the `__call__` method to yield the events.
</Note>

## Developer Resources

* [Step with a Custom Function](/examples/concepts/workflows/01-basic-workflows/step_with_function)
* [Step with a Custom Function with Streaming on AgentOS](/examples/concepts/workflows/01-basic-workflows/step_with_function_streaming_agentos)
* [Parallel and custom function step streaming on AgentOS](/examples/concepts/workflows/04-workflows-parallel-execution/parallel_and_custom_function_step_streaming_agentos)

# Conditional Workflow

> Deterministic branching based on input analysis or business rules

**Example Use-Cases**: Content type routing, topic-specific processing, quality-based decisions

Conditional workflows provide predictable branching logic while maintaining deterministic execution paths.

<img className="block dark:hidden" src="https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-condition-steps-light.png?fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=7bc060741f060c43747d9866246d0587" alt="Workflows condition steps diagram" data-og-width="3441" width="3441" data-og-height="756" height="756" data-path="images/workflows-condition-steps-light.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-condition-steps-light.png?w=280&fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=051009cf50418538acbc49a9c690cdf8 280w, https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-condition-steps-light.png?w=560&fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=5f8e6a2ed1301cf1d4edda7804c5ec08 560w, https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-condition-steps-light.png?w=840&fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=65a6ba82ef0a22a0927439644a6c7912 840w, https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-condition-steps-light.png?w=1100&fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=f5d676c0bf82f2045e61f31126b66a42 1100w, https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-condition-steps-light.png?w=1650&fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=408f8ed2a78755b289c7a0b4e07d6f0e 1650w, https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-condition-steps-light.png?w=2500&fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=548ca991ffb6e9e5d7669bf37e98fed2 2500w" />

<img className="hidden dark:block" src="https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-condition-steps.png?fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=de3fa0bc3fc9b4079e7dd3596d6e589a" alt="Workflows condition steps diagram" data-og-width="3441" width="3441" data-og-height="756" height="756" data-path="images/workflows-condition-steps.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-condition-steps.png?w=280&fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=3b0eb6ed78b037dd85346647665f373e 280w, https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-condition-steps.png?w=560&fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=9c5e9785043d807c36b6ee130fde63ef 560w, https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-condition-steps.png?w=840&fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=5044466baae4103aadf462fb81b9be60 840w, https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-condition-steps.png?w=1100&fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=d67a6cb9bb25245259a4001be56f7d91 1100w, https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-condition-steps.png?w=1650&fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=ff169ab64d750cfb21073305fdedd213 1650w, https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-condition-steps.png?w=2500&fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=0f44b53b13a00c51b26314825d605013 2500w" />

## Example

```python conditional_workflow.py theme={null}
from agno.workflow import Condition, Step, Workflow

def is_tech_topic(step_input) -> bool:
    topic = step_input.input.lower()
    return any(keyword in topic for keyword in ["ai", "tech", "software"])

workflow = Workflow(
    name="Conditional Research",
    steps=[
        Condition(
            name="Tech Topic Check",
            evaluator=is_tech_topic,
            steps=[Step(name="Tech Research", agent=tech_researcher)]
        ),
        Step(name="General Analysis", agent=general_analyst),
    ]
)

workflow.print_response("Comprehensive analysis of AI and machine learning trends", markdown=True)
```

## Developer Resources

* [Condition Steps Workflow](/examples/concepts/workflows/02-workflows-conditional-execution/condition_steps_workflow_stream)
* [Condition with List of Steps](/examples/concepts/workflows/02-workflows-conditional-execution/condition_with_list_of_steps)

## Reference

For complete API documentation, see [Condition Steps Reference](/reference/workflows/conditional-steps).

# Parallel Workflow

> Independent, concurrent tasks that can execute simultaneously for improved efficiency

**Example Use-Cases**: Multi-source research, parallel analysis, concurrent data processing

Parallel workflows maintain deterministic results while dramatically reducing execution time for independent operations.

<img className="block dark:hidden" src="https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-parallel-steps-light.png?fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=afda5268ab0637c6064ace8edd6f35e5" alt="Workflows parallel steps diagram" data-og-width="3441" width="3441" data-og-height="756" height="756" data-path="images/workflows-parallel-steps-light.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-parallel-steps-light.png?w=280&fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=c153b9934fa98b2b886a9435022b020a 280w, https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-parallel-steps-light.png?w=560&fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=17253f58b485bb6180827516f7f947be 560w, https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-parallel-steps-light.png?w=840&fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=b067f30b291f2de8cb6a04e208ee61cc 840w, https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-parallel-steps-light.png?w=1100&fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=a814e829581fb1d7c64e49fa87ca847e 1100w, https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-parallel-steps-light.png?w=1650&fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=1cd456c3e949af82fd6325b3f3865f23 1650w, https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-parallel-steps-light.png?w=2500&fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=52fcc51f72ee6e1df2648612451cae70 2500w" />

<img className="hidden dark:block" src="https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-parallel-steps.png?fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=ec4f6c7c9a6ef76cec8f0866eb1acc5b" alt="Workflows parallel steps diagram" data-og-width="3441" width="3441" data-og-height="756" height="756" data-path="images/workflows-parallel-steps.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-parallel-steps.png?w=280&fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=39624cca7177ba0064491bb64c645db2 280w, https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-parallel-steps.png?w=560&fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=c3e5cde671f164b7dd13eb417f5f74db 560w, https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-parallel-steps.png?w=840&fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=db6672401fdf35e0eb616e72016ec41c 840w, https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-parallel-steps.png?w=1100&fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=831053d087a3bf26e966f8f896ac9b61 1100w, https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-parallel-steps.png?w=1650&fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=445e07ea13a74913e67e2a2a9c8e9c5f 1650w, https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-parallel-steps.png?w=2500&fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=77083544c8387f660207dfaf645bdaf0 2500w" />

## Example

```python parallel_workflow.py theme={null}
from agno.workflow import Parallel, Step, Workflow

workflow = Workflow(
    name="Parallel Research Pipeline",
    steps=[
        Parallel(
            Step(name="HackerNews Research", agent=hn_researcher),
            Step(name="Web Research", agent=web_researcher),
            Step(name="Academic Research", agent=academic_researcher),
            name="Research Step"
        ),
        Step(name="Synthesis", agent=synthesizer),  # Combines the results and produces a report
    ]
)

workflow.print_response("Write about the latest AI developments", markdown=True)
```

## Handling Session State Data in Parallel Steps

When using custom Python functions in your steps, you can access and update the Worfklow session state via the `run_context` parameter.

If you are performing session state updates in Parallel Steps, be aware that concurrent access to shared state will require coordination to avoid race conditions.

## Developer Resources

* [Parallel Steps Workflow](/examples/concepts/workflows/04-workflows-parallel-execution/parallel_steps_workflow)

## Reference

For complete API documentation, see [Parallel Steps Reference](/reference/workflows/parallel-steps).

# Iterative Workflow

> Quality-driven processes requiring repetition until specific conditions are met

**Example Use-Cases**: Quality improvement loops, retry mechanisms, iterative refinement

Iterative workflows provide controlled repetition with deterministic exit conditions, ensuring consistent quality standards.

<img className="block dark:hidden" src="https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-loop-steps-light.png?fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=edba198de555846a2ea8b2e5b65c6d8e" alt="Workflows loop steps diagram" data-og-width="3441" width="3441" data-og-height="756" height="756" data-path="images/workflows-loop-steps-light.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-loop-steps-light.png?w=280&fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=96d954f1d665b4b01e0fb030c0544504 280w, https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-loop-steps-light.png?w=560&fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=f4ce273ba17af6b0b5b417ec2e73385c 560w, https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-loop-steps-light.png?w=840&fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=15eb9ff0487ff79dccaa1a046ad7c32d 840w, https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-loop-steps-light.png?w=1100&fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=ac3e8fb6db4326f2e78948c467924f7c 1100w, https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-loop-steps-light.png?w=1650&fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=45c09671d2bb3190bb14f23ecab28f85 1650w, https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-loop-steps-light.png?w=2500&fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=05a4004d7c8228caefbacbc21a2efd2f 2500w" />

<img className="hidden dark:block" src="https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-loop-steps.png?fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=30027b401899598a38a73c6038d1d988" alt="Workflows loop steps diagram" data-og-width="3441" width="3441" data-og-height="756" height="756" data-path="images/workflows-loop-steps.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-loop-steps.png?w=280&fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=aa15df4e2e353012150474b5fa26d5c5 280w, https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-loop-steps.png?w=560&fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=f411273ea9e60981989e16324940fbc0 560w, https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-loop-steps.png?w=840&fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=a71354c338a1520f27797ca6e53dc378 840w, https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-loop-steps.png?w=1100&fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=cf1495378fc757cd5995b96c734cda71 1100w, https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-loop-steps.png?w=1650&fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=3d32977904938d0cc22407d61c6efd8e 1650w, https://mintcdn.com/agno-v2/JYIBgMrzFEujZh3_/images/workflows-loop-steps.png?w=2500&fit=max&auto=format&n=JYIBgMrzFEujZh3_&q=85&s=e3e1c672c2953455defceb971b803bce 2500w" />

## Example

```python iterative_workflow.py theme={null}
from agno.workflow import Loop, Step, Workflow

def quality_check(outputs) -> bool:
    # Return True to break loop, False to continue
    return any(len(output.content) > 500 for output in outputs)

workflow = Workflow(
    name="Quality-Driven Research",
    steps=[
        Loop(
            name="Research Loop",
            steps=[Step(name="Deep Research", agent=researcher)],
            end_condition=quality_check,
            max_iterations=3
        ),
        Step(name="Final Analysis", agent=analyst),
    ]
)

workflow.print_response("Research the impact of renewable energy on global markets", markdown=True)
```

## Developer Resources

* [Loop Steps Workflow](/examples/concepts/workflows/03_workflows_loop_execution/loop_steps_workflow)

## Reference

For complete API documentation, see [Loop Steps Reference](/reference/workflows/loop-steps).

# Branching Workflow

> Complex decision trees requiring dynamic path selection based on content analysis

**Example Use-Cases**: Expert routing, content type detection, multi-path processing

Dynamic routing workflows provide intelligent path selection while maintaining predictable execution within each chosen branch.

<img className="block dark:hidden" src="https://mintcdn.com/agno-v2/6A2IKapU7R02zCpZ/images/workflows-router-steps-light.png?fit=max&auto=format&n=6A2IKapU7R02zCpZ&q=85&s=11256e6d5ebe78ee137ba56647bb732c" alt="Workflows router steps diagram" data-og-width="2493" width="2493" data-og-height="921" height="921" data-path="images/workflows-router-steps-light.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/agno-v2/6A2IKapU7R02zCpZ/images/workflows-router-steps-light.png?w=280&fit=max&auto=format&n=6A2IKapU7R02zCpZ&q=85&s=bbbf338fb349e3d6e9e66f92873ca74b 280w, https://mintcdn.com/agno-v2/6A2IKapU7R02zCpZ/images/workflows-router-steps-light.png?w=560&fit=max&auto=format&n=6A2IKapU7R02zCpZ&q=85&s=3c341c1b87faa0eca3092ea8f93c5d0b 560w, https://mintcdn.com/agno-v2/6A2IKapU7R02zCpZ/images/workflows-router-steps-light.png?w=840&fit=max&auto=format&n=6A2IKapU7R02zCpZ&q=85&s=75dabdfd37b0806915bd56520c176d0a 840w, https://mintcdn.com/agno-v2/6A2IKapU7R02zCpZ/images/workflows-router-steps-light.png?w=1100&fit=max&auto=format&n=6A2IKapU7R02zCpZ&q=85&s=8e91a1cb88327098c3420a0bd4994e69 1100w, https://mintcdn.com/agno-v2/6A2IKapU7R02zCpZ/images/workflows-router-steps-light.png?w=1650&fit=max&auto=format&n=6A2IKapU7R02zCpZ&q=85&s=e948b1e5b7f48fde2637265f2daef7f5 1650w, https://mintcdn.com/agno-v2/6A2IKapU7R02zCpZ/images/workflows-router-steps-light.png?w=2500&fit=max&auto=format&n=6A2IKapU7R02zCpZ&q=85&s=74139a11491c79a755974923831ad406 2500w" />

<img className="hidden dark:block" src="https://mintcdn.com/agno-v2/6A2IKapU7R02zCpZ/images/workflows-router-steps.png?fit=max&auto=format&n=6A2IKapU7R02zCpZ&q=85&s=593bc69b1647af6571151c051145e7c6" alt="Workflows router steps diagram" data-og-width="2493" width="2493" data-og-height="921" height="921" data-path="images/workflows-router-steps.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/agno-v2/6A2IKapU7R02zCpZ/images/workflows-router-steps.png?w=280&fit=max&auto=format&n=6A2IKapU7R02zCpZ&q=85&s=575bc73e719bb2ccf703278e5aaaa4b3 280w, https://mintcdn.com/agno-v2/6A2IKapU7R02zCpZ/images/workflows-router-steps.png?w=560&fit=max&auto=format&n=6A2IKapU7R02zCpZ&q=85&s=6886d723d73a9fc1ffec318b2fe33d3c 560w, https://mintcdn.com/agno-v2/6A2IKapU7R02zCpZ/images/workflows-router-steps.png?w=840&fit=max&auto=format&n=6A2IKapU7R02zCpZ&q=85&s=0c364bb81456fc509a64fcac0cb8373a 840w, https://mintcdn.com/agno-v2/6A2IKapU7R02zCpZ/images/workflows-router-steps.png?w=1100&fit=max&auto=format&n=6A2IKapU7R02zCpZ&q=85&s=d9ede7db094389fc173c590ea28aa21c 1100w, https://mintcdn.com/agno-v2/6A2IKapU7R02zCpZ/images/workflows-router-steps.png?w=1650&fit=max&auto=format&n=6A2IKapU7R02zCpZ&q=85&s=117488ab5bcecbf9e982474dd91580e8 1650w, https://mintcdn.com/agno-v2/6A2IKapU7R02zCpZ/images/workflows-router-steps.png?w=2500&fit=max&auto=format&n=6A2IKapU7R02zCpZ&q=85&s=e0f5a19e133076f0ba74ced4f21ba411 2500w" />

## Example

```python branching_workflow.py theme={null}
from agno.workflow import Router, Step, Workflow

def route_by_topic(step_input) -> List[Step]:
    topic = step_input.input.lower()

    if "tech" in topic:
        return [Step(name="Tech Research", agent=tech_expert)]
    elif "business" in topic:
        return [Step(name="Business Research", agent=biz_expert)]
    else:
        return [Step(name="General Research", agent=generalist)]

workflow = Workflow(
    name="Expert Routing",
    steps=[
        Router(
            name="Topic Router",
            selector=route_by_topic,
            choices=[tech_step, business_step, general_step]
        ),
        Step(name="Synthesis", agent=synthesizer),
    ]
)

workflow.print_response("Latest developments in artificial intelligence and machine learning", markdown=True)
```

## Developer Resources

* [Router Steps Workflow](/examples/concepts/workflows/05_workflows_conditional_branching/router_steps_workflow)

## Reference

For complete API documentation, see [Router Steps Reference](/reference/workflows/router-steps).

# Grouped Steps Workflow

> Organize multiple steps into reusable, logical sequences for complex workflows with clean separation of concerns

**Key Benefits**: Reusable sequences, cleaner branching logic, modular workflow design

Grouped steps enable modular workflow architecture with reusable components and clear logical boundaries.

## Basic Example

```python grouped_steps_workflow.py theme={null}
from agno.workflow import Steps, Step, Workflow

# Create a reusable content creation sequence
article_creation_sequence = Steps(
    name="ArticleCreation",
    description="Complete article creation workflow from research to final edit",
    steps=[
        Step(name="research", agent=researcher),
        Step(name="writing", agent=writer),
        Step(name="editing", agent=editor),
    ],
)

# Use the sequence in a workflow
workflow = Workflow(
    name="Article Creation Workflow",
    steps=[article_creation_sequence]  # Single sequence
)

workflow.print_response("Write an article about renewable energy", markdown=True)
```

## Steps with Router

This is where `Steps` really shines - creating distinct sequences for different content types or workflows:

```python  theme={null}
from agno.workflow import Steps, Router, Step, Workflow

# Define two completely different workflows as Steps
image_sequence = Steps(
    name="image_generation",
    description="Complete image generation and analysis workflow",
    steps=[
        Step(name="generate_image", agent=image_generator),
        Step(name="describe_image", agent=image_describer),
    ],
)

video_sequence = Steps(
    name="video_generation",
    description="Complete video production and analysis workflow",
    steps=[
        Step(name="generate_video", agent=video_generator),
        Step(name="describe_video", agent=video_describer),
    ],
)

def media_sequence_selector(step_input) -> List[Step]:
    """Route to appropriate media generation pipeline"""
    if not step_input.input:
        return [image_sequence]

    message_lower = step_input.input.lower()

    if "video" in message_lower:
        return [video_sequence]
    elif "image" in message_lower:
        return [image_sequence]
    else:
        return [image_sequence]  # Default

# Clean workflow with clear branching
media_workflow = Workflow(
    name="AI Media Generation Workflow",
    description="Generate and analyze images or videos using AI agents",
    steps=[
        Router(
            name="Media Type Router",
            description="Routes to appropriate media generation pipeline",
            selector=media_sequence_selector,
            choices=[image_sequence, video_sequence],  # Clear choices
        )
    ],
)

# Usage examples
media_workflow.print_response("Create an image of a magical forest", markdown=True)
media_workflow.print_response("Create a cinematic video of city timelapse", markdown=True)
```

## Developer Resources

* [`workflow_using_steps.py`](/examples/concepts/workflows/01-basic-workflows/workflow_using_steps)
* [`workflow_using_steps_nested.py`](/examples/concepts/workflows/01-basic-workflows/workflow_using_steps_nested)
* [`selector_for_image_video_generation_pipelines.py`](/examples/concepts/workflows/05_workflows_conditional_branching/selector_for_image_video_generation_pipelines)

## Reference

For complete API documentation, see [Steps Reference](/reference/workflows/steps-step).
