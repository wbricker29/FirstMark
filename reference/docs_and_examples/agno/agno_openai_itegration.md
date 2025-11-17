# OpenAI Responses

> Learn how to use OpenAI Responses with Agno.

`OpenAIResponses` is a class for interacting with OpenAI models using the Responses API. This class provides a streamlined interface for working with OpenAI's newer Responses API, which is distinct from the traditional Chat API. It supports advanced features like tool use, file processing, and knowledge retrieval.

## Authentication

Set your `OPENAI_API_KEY` environment variable. You can get one [from OpenAI here](https://platform.openai.com/account/api-keys).

<CodeGroup>

  ```bash Mac theme={null}
  export OPENAI_API_KEY=sk-***
  ```

  ```bash Windows theme={null}
  setx OPENAI_API_KEY sk-***
  ```

</CodeGroup>

## Example

Use `OpenAIResponses` with your `Agent`:

<CodeGroup>

  ```python agent.py theme={null}

  from agno.agent import Agent
  from agno.media import File
  from agno.models.openai.responses import OpenAIResponses

  agent = Agent(
      model=OpenAIResponses(id="gpt-5-mini"),
      tools=[{"type": "file_search"}, {"type": "web_search_preview"}],
      markdown=True,
  )

  agent.print_response(
      "Summarize the contents of the attached file and search the web for more information.",
      files=[File(url="https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf")],
  )

  ```

</CodeGroup>

<Note> View more examples [here](/examples/models/openai/responses/basic). </Note>

## Parameters

For more information, please refer to the [OpenAI Responses docs](https://platform.openai.com/docs/api-reference/responses) as well.

| Parameter               | Type                                               | Default             | Description                                                                       |
| ----------------------- | -------------------------------------------------- | ------------------- | --------------------------------------------------------------------------------- |
| `id`                    | `str`                                              | `"gpt-5-mini"`      | The id of the OpenAI model to use with Responses API                              |
| `name`                  | `str`                                              | `"OpenAIResponses"` | The name of the model                                                             |
| `provider`              | `str`                                              | `"OpenAI"`          | The provider of the model                                                         |
| `instructions`          | `Optional[str]`                                    | `None`              | System-level instructions for the assistant                                       |
| `response_format`       | `Optional[Union[str, Dict]]`                       | `None`              | Response format specification for structured outputs                              |
| `temperature`           | `Optional[float]`                                  | `None`              | Controls randomness in the model's output (0.0 to 2.0)                            |
| `top_p`                 | `Optional[float]`                                  | `None`              | Controls diversity via nucleus sampling (0.0 to 1.0)                              |
| `max_completion_tokens` | `Optional[int]`                                    | `None`              | Maximum number of completion tokens to generate                                   |
| `truncation_strategy`   | `Optional[Dict[str, Any]]`                         | `None`              | Strategy for truncating messages when they exceed context limits                  |
| `tool_choice`           | `Optional[Union[str, Dict]]`                       | `None`              | Controls which function is called by the model                                    |
| `parallel_tool_calls`   | `Optional[bool]`                                   | `None`              | Whether to enable parallel function calling                                       |
| `metadata`              | `Optional[Dict[str, str]]`                         | `None`              | Developer-defined metadata to associate with the response                         |
| `strict_output`         | `bool`                                             | `True`              | Controls schema adherence for structured outputs                                  |
| `api_key`               | `Optional[str]`                                    | `None`              | The API key for authenticating with OpenAI (defaults to OPENAI\_API\_KEY env var) |
| `organization`          | `Optional[str]`                                    | `None`              | The organization ID to use for requests                                           |
| `base_url`              | `Optional[Union[str, httpx.URL]]`                  | `None`              | The base URL for the OpenAI API                                                   |
| `timeout`               | `Optional[float]`                                  | `None`              | Request timeout in seconds                                                        |
| `max_retries`           | `Optional[int]`                                    | `None`              | Maximum number of retries for failed requests                                     |
| `default_headers`       | `Optional[Any]`                                    | `None`              | Default headers to include in all requests                                        |
| `http_client`           | `Optional[Union[httpx.Client, httpx.AsyncClient]]` | `None`              | HTTP client instance for making requests                                          |

`OpenAIResponses` is a subclass of the [Model](/reference/models/model) class and has access to the same params.

--- EXAMPLES ---

# Websearch Builtin Tool

## Code

```python cookbook/models/openai/responses/websearch_builtin_tool.py theme={null}
from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.tools.file import FileTools

agent = Agent(
    model=OpenAIResponses(id="gpt-5-mini"),
    tools=[{"type": "web_search_preview"}, FileTools()],
    instructions="Save the results to a file with a relevant name.",
    markdown=True,
)
agent.print_response("Whats happening in France?")

```

## Usage

<Steps>
  <Snippet file="create-venv-step.mdx" />

  <Step title="Set your API key">
    ```bash  theme={null}
    export OPENAI_API_KEY=xxx
    ```
  </Step>

  <Step title="Install libraries">
    ```bash  theme={null}
    pip install -U openai agno
    ```
  </Step>

  <Step title="Run Agent">
    <CodeGroup>
      ```bash Mac theme={null}
      python cookbook/models/openai/responses/websearch_builtin_tool.py
      ```

      ```bash Windows theme={null}
      python cookbook/models/openai/responses/websearch_builtin_tool.py
      ```
    </CodeGroup>
  </Step>
</Steps>
# Deep Research Agent

## Code

```python cookbook/models/openai/responses/deep_research_agent.py theme={null}
from textwrap import dedent

from agno.agent import Agent
from agno.models.openai import OpenAIResponses

agent = Agent(
    model=OpenAIResponses(id="o4-mini-deep-research", max_tool_calls=1),
    instructions=dedent("""
        You are an expert research analyst with access to advanced research tools.

        When you are given a schema to use, pass it to the research tool as output_schema parameter to research tool.

        The research tool has two parameters:
        - instructions (str): The research topic/question
        - output_schema (dict, optional): A JSON schema for structured output
    """),
)

agent.print_response(
    """Research the economic impact of semaglutide on global healthcare systems.
    Do:
    - Include specific figures, trends, statistics, and measurable outcomes.
    - Prioritize reliable, up-to-date sources: peer-reviewed research, health
      organizations (e.g., WHO, CDC), regulatory agencies, or pharmaceutical
      earnings reports.
    - Include inline citations and return all source metadata.

    Be analytical, avoid generalities, and ensure that each section supports
    data-backed reasoning that could inform healthcare policy or financial modeling."""
)

```

## Usage

<Steps>
  <Snippet file="create-venv-step.mdx" />

  <Step title="Set your API key">
    ```bash  theme={null}
    export OPENAI_API_KEY=xxx
    ```
  </Step>

  <Step title="Install libraries">
    ```bash  theme={null}
    pip install -U openai agno
    ```
  </Step>

  <Step title="Run Agent">
    <CodeGroup>
      ```bash Mac theme={null}
      python cookbook/models/openai/responses/deep_research_agent.py
      ```

      ```bash Windows theme={null}
      python cookbook/models/openai/responses/deep_research_agent.py
      ```
    </CodeGroup>
  </Step>
</Steps>

# Tool Use Gpt 5

## Code

```python cookbook/models/openai/responses/tool_use_gpt_5.py theme={null}
from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.tools.yfinance import YFinanceTools

agent = Agent(
    model=OpenAIResponses(id="gpt-5"),
    tools=[YFinanceTools(cache_results=True)],
    markdown=True,
    telemetry=False,
)

agent.print_response("What is the current price of TSLA?", stream=True)

```

## Usage

<Steps>
  <Snippet file="create-venv-step.mdx" />

  <Step title="Set your API key">
    ```bash  theme={null}
    export OPENAI_API_KEY=xxx
    ```
  </Step>

  <Step title="Install libraries">
    ```bash  theme={null}
    pip install -U openai agno
    ```
  </Step>

  <Step title="Run Agent">
    <CodeGroup>
      ```bash Mac theme={null}
      python cookbook/models/openai/responses/tool_use_gpt_5.py
      ```

      ```bash Windows theme={null}
      python cookbook/models/openai/responses/tool_use_gpt_5.py
      ```
    </CodeGroup>
  </Step>
</Steps>
# Async Basic

## Code

```python cookbook/models/openai/responses/async_basic.py theme={null}
import asyncio

from agno.agent import Agent, RunOutput  # noqa
from agno.models.openai import OpenAIResponses

agent = Agent(model=OpenAIResponses(id="gpt-5-mini"), markdown=True)

# Get the response in a variable
# run: RunOutput = agent.run("Share a 2 sentence horror story")
# print(run.content)

# Print the response in the terminal
asyncio.run(agent.aprint_response("Share a 2 sentence horror story"))

```

## Usage

<Steps>
  <Snippet file="create-venv-step.mdx" />

  <Step title="Set your API key">
    ```bash  theme={null}
    export OPENAI_API_KEY=xxx
    ```
  </Step>

  <Step title="Install libraries">
    ```bash  theme={null}
    pip install -U openai agno
    ```
  </Step>

  <Step title="Run Agent">
    <CodeGroup>
      ```bash Mac theme={null}
      python cookbook/models/openai/responses/async_basic.py
      ```

      ```bash Windows theme={null}
      python cookbook/models/openai/responses/async_basic.py
      ```
    </CodeGroup>
  </Step>
</Steps>

# Async Basic Stream

## Code

```python cookbook/models/openai/responses/async_basic_stream.py theme={null}
import asyncio
from typing import Iterator  # noqa

from agno.agent import Agent, RunOutputEvent  # noqa
from agno.models.openai import OpenAIResponses

agent = Agent(model=OpenAIResponses(id="gpt-5-mini"), markdown=True)

# Get the response in a variable
# run_response: Iterator[RunOutputEvent] = agent.run("Share a 2 sentence horror story", stream=True)
# for chunk in run_response:
#     print(chunk.content)

# Print the response in the terminal
asyncio.run(agent.aprint_response("Share a 2 sentence horror story", stream=True))

```

## Usage

<Steps>
  <Snippet file="create-venv-step.mdx" />

  <Step title="Set your API key">
    ```bash  theme={null}
    export OPENAI_API_KEY=xxx
    ```
  </Step>

  <Step title="Install libraries">
    ```bash  theme={null}
    pip install -U openai agno
    ```
  </Step>

  <Step title="Run Agent">
    <CodeGroup>
      ```bash Mac theme={null}
      python cookbook/models/openai/responses/async_basic_stream.py
      ```

      ```bash Windows theme={null}
      python cookbook/models/openai/responses/async_basic_stream.py
      ```
    </CodeGroup>
  </Step>
</Steps>

# Async Tool Use

## Code

```python cookbook/models/openai/responses/async_tool_use.py theme={null}
"""Run `pip install ddgs` to install dependencies."""

import asyncio

from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.tools.duckduckgo import DuckDuckGoTools

agent = Agent(
    model=OpenAIResponses(id="gpt-5-mini"),
    tools=[DuckDuckGoTools()],
    markdown=True,
)
asyncio.run(agent.aprint_response("Whats happening in France?", stream=True))

```

## Usage

<Steps>
  <Snippet file="create-venv-step.mdx" />

  <Step title="Set your API key">
    ```bash  theme={null}
    export OPENAI_API_KEY=xxx
    ```
  </Step>

  <Step title="Install libraries">
    ```bash  theme={null}
    pip install -U openai agno
    ```
  </Step>

  <Step title="Run Agent">
    <CodeGroup>
      ```bash Mac theme={null}
      python cookbook/models/openai/responses/async_tool_use.py
      ```

      ```bash Windows theme={null}
      python cookbook/models/openai/responses/async_tool_use.py
      ```
    </CodeGroup>
  </Step>
</Steps>
# Basic

## Code

```python cookbook/models/openai/responses/basic.py theme={null}
from agno.agent import Agent, RunOutput  # noqa
from agno.models.openai import OpenAIResponses

agent = Agent(model=OpenAIResponses(id="gpt-5-mini"), markdown=True)

# Get the response in a variable
# run: RunOutput = agent.run("Share a 2 sentence horror story")
# print(run.content)

# Print the response in the terminal
agent.print_response("Share a 2 sentence horror story")

```

## Usage

<Steps>
  <Snippet file="create-venv-step.mdx" />

  <Step title="Set your API key">
    ```bash  theme={null}
    export OPENAI_API_KEY=xxx
    ```
  </Step>

  <Step title="Install libraries">
    ```bash  theme={null}
    pip install -U openai agno
    ```
  </Step>

  <Step title="Run Agent">
    <CodeGroup>
      ```bash Mac theme={null}
      python cookbook/models/openai/responses/basic.py
      ```

      ```bash Windows theme={null}
      python cookbook/models/openai/responses/basic.py
      ```
    </CodeGroup>
  </Step>
</Steps>

# Basic Stream

## Code

```python cookbook/models/openai/responses/basic_stream.py theme={null}
from typing import Iterator  # noqa
from agno.agent import Agent, RunOutputEvent  # noqa
from agno.models.openai import OpenAIResponses

agent = Agent(model=OpenAIResponses(id="gpt-5-mini"), markdown=True)

# Get the response in a variable
# run_response: Iterator[RunOutputEvent] = agent.run("Share a 2 sentence horror story", stream=True)
# for chunk in run_response:
#     print(chunk.content)

# Print the response in the terminal
agent.print_response("Share a 2 sentence horror story", stream=True)

```

## Usage

<Steps>
  <Snippet file="create-venv-step.mdx" />

  <Step title="Set your API key">
    ```bash  theme={null}
    export OPENAI_API_KEY=xxx
    ```
  </Step>

  <Step title="Install libraries">
    ```bash  theme={null}
    pip install -U openai agno
    ```
  </Step>

  <Step title="Run Agent">
    <CodeGroup>
      ```bash Mac theme={null}
      python cookbook/models/openai/responses/basic_stream.py
      ```

      ```bash Windows theme={null}
      python cookbook/models/openai/responses/basic_stream.py
      ```
    </CodeGroup>
  </Step>
</Steps>

# Memory

## Code

```python cookbook/models/openai/responses/memory.py theme={null}
"""
This recipe shows how to use personalized memories and summaries in an agent.
Steps:
1. Run: `./cookbook/scripts/run_pgvector.sh` to start a postgres container with pgvector
2. Run: `pip install openai sqlalchemy 'psycopg[binary]' pgvector` to install the dependencies
3. Run: `python cookbook/agents/personalized_memories_and_summaries.py` to run the agent
"""

from agno.agent import Agent
from agno.db.base import SessionType
from agno.db.postgres import PostgresDb
from agno.models.openai import OpenAIResponses
from rich.pretty import pprint

# Setup the database
db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"
db = PostgresDb(db_url=db_url)

agent = Agent(
    model=OpenAIResponses(id="gpt-5-mini"),
    user_id="test_user",
    session_id="test_session",
    # Pass the database to the Agent
    db=db,
    # Enable user memories
    enable_user_memories=True,
    # Enable session summaries
    enable_session_summaries=True,
    # Show debug logs so, you can see the memory being created
)

# -*- Share personal information
agent.print_response("My name is john billings?", stream=True)
# -*- Print memories and summary
if agent.db:
    pprint(agent.db.get_user_memories(user_id="test_user"))
    pprint(
        agent.db.get_session(
            session_id="test_session", session_type=SessionType.AGENT
        ).summary  # type: ignore
    )

# -*- Share personal information
agent.print_response("I live in nyc?", stream=True)
# -*- Print memories
if agent.db:
    pprint(agent.db.get_user_memories(user_id="test_user"))
    pprint(
        agent.db.get_session(
            session_id="test_session", session_type=SessionType.AGENT
        ).summary  # type: ignore
    )

# -*- Share personal information
agent.print_response("I'm going to a concert tomorrow?", stream=True)
# -*- Print memories
if agent.db:
    pprint(agent.db.get_user_memories(user_id="test_user"))
    pprint(
        agent.db.get_session(
            session_id="test_session", session_type=SessionType.AGENT
        ).summary  # type: ignore
    )

# Ask about the conversation
agent.print_response(
    "What have we been talking about, do you know my name?", stream=True
)

```

## Usage

<Steps>
  <Snippet file="create-venv-step.mdx" />

  <Step title="Set your API key">
    ```bash  theme={null}
    export OPENAI_API_KEY=xxx
    ```
  </Step>

  <Step title="Install libraries">
    ```bash  theme={null}
    pip install -U openai agno
    ```
  </Step>

  <Step title="Run Agent">
    <CodeGroup>
      ```bash Mac theme={null}
      python cookbook/models/openai/responses/memory.py
      ```

      ```bash Windows theme={null}
      python cookbook/models/openai/responses/memory.py
      ```
    </CodeGroup>
  </Step>
</Steps>

# Structured Output

## Code

```python cookbook/models/openai/responses/structured_output.py theme={null}
from typing import List

from agno.agent import Agent, RunOutput  # noqa
from agno.models.openai import OpenAIResponses
from pydantic import BaseModel, Field
from rich.pretty import pprint  # noqa


class MovieScript(BaseModel):
    setting: str = Field(
        ..., description="Provide a nice setting for a blockbuster movie."
    )
    ending: str = Field(
        ...,
        description="Ending of the movie. If not available, provide a happy ending.",
    )
    genre: str = Field(
        ...,
        description="Genre of the movie. If not available, select action, thriller or romantic comedy.",
    )
    name: str = Field(..., description="Give a name to this movie")
    characters: List[str] = Field(..., description="Name of characters for this movie.")
    storyline: str = Field(
        ..., description="3 sentence storyline for the movie. Make it exciting!"
    )


# Agent that uses JSON mode
json_mode_agent = Agent(
    model=OpenAIResponses(id="gpt-5-mini"),
    description="You write movie scripts.",
    output_schema=MovieScript,
    use_json_mode=True,
)

# Agent that uses structured outputs with strict_output=True (default)
structured_output_agent = Agent(
    model=OpenAIResponses(id="gpt-5-mini"),
    description="You write movie scripts.",
    output_schema=MovieScript,
)

# Agent with strict_output=False (guided mode)
guided_output_agent = Agent(
    model=OpenAIResponses(id="gpt-5-mini", strict_output=False),
    description="You write movie scripts.",
    output_schema=MovieScript,
)


# Get the response in a variable
# json_mode_response: RunOutput = json_mode_agent.run("New York")
# pprint(json_mode_response.content)
# structured_output_response: RunOutput = structured_output_agent.run("New York")
# pprint(structured_output_response.content)

json_mode_agent.print_response("New York")
structured_output_agent.print_response("New York")
guided_output_agent.print_response("New York")

```

## Usage

<Steps>
  <Snippet file="create-venv-step.mdx" />

  <Step title="Set your API key">
    ```bash  theme={null}
    export OPENAI_API_KEY=xxx
    ```
  </Step>

  <Step title="Install libraries">
    ```bash  theme={null}
    pip install -U openai agno
    ```
  </Step>

  <Step title="Run Agent">
    <CodeGroup>
      ```bash Mac theme={null}
      python cookbook/models/openai/responses/structured_output.py
      ```

      ```bash Windows theme={null}
      python cookbook/models/openai/responses/structured_output.py
      ```
    </CodeGroup>
  </Step>
</Steps>
