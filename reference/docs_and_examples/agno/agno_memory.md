# Agent with Memory

This example shows you how to use persistent memory with an Agent.

After each run, user memories are created/updated.

To enable this, set `enable_user_memories=True` in the Agent config.

## Code

```python agent_with_memory.py theme={null}
from uuid import uuid4

from agno.agent.agent import Agent
from agno.db.postgres import PostgresDb
from agno.models.openai import OpenAIChat
from rich.pretty import pprint

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

db = PostgresDb(db_url=db_url)

db.clear_memories()

session_id = str(uuid4())
john_doe_id = "john_doe@example.com"

agent = Agent(
    model=OpenAIChat(id="gpt-5-mini"),
    db=db,
    enable_user_memories=True,
)

agent.print_response(
    "My name is John Doe and I like to hike in the mountains on weekends.",
    stream=True,
    user_id=john_doe_id,
    session_id=session_id,
)

agent.print_response(
    "What are my hobbies?", stream=True, user_id=john_doe_id, session_id=session_id
)

memories = agent.get_user_memories(user_id=john_doe_id)
print("John Doe's memories:")
pprint(memories)

agent.print_response(
    "Ok i dont like hiking anymore, i like to play soccer instead.",
    stream=True,
    user_id=john_doe_id,
    session_id=session_id,
)

# You can also get the user memories from the agent
memories = agent.get_user_memories(user_id=john_doe_id)
print("John Doe's memories:")
pprint(memories)

```

## Usage

<Steps>
  <Snippet file="create-venv-step.mdx" />

  <Step title="Install libraries">
    ```bash  theme={null}
    pip install -U agno
    ```
  </Step>

  <Step title="Run Example">
    <CodeGroup>
      ```bash Mac theme={null}
      python cookbook/memory/01_agent_with_memory.py
      ```

      ```bash Windows theme={null}
      python cookbook/memory/01_agent_with_memory.py
      ```
    </CodeGroup>
  </Step>
</Steps>

# Agentic Memory

This example shows you how to use persistent memory with an Agent.

During each run the Agent can create/update/delete user memories.

To enable this, set `enable_agentic_memory=True` in the Agent config.

## Code

```python agentic_memory.py theme={null}
from agno.agent.agent import Agent
from agno.db.postgres import PostgresDb
from agno.models.openai import OpenAIChat
from rich.pretty import pprint

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

db = PostgresDb(db_url=db_url)


john_doe_id = "john_doe@example.com"

agent = Agent(
    model=OpenAIChat(id="gpt-5-mini"),
    db=db,
    enable_agentic_memory=True,
)

agent.print_response(
    "My name is John Doe and I like to hike in the mountains on weekends.",
    stream=True,
    user_id=john_doe_id,
)

agent.print_response("What are my hobbies?", stream=True, user_id=john_doe_id)

memories = agent.get_user_memories(user_id=john_doe_id)
print("Memories about John Doe:")
pprint(memories)


agent.print_response(
    "Remove all existing memories of me.",
    stream=True,
    user_id=john_doe_id,
)

memories = agent.get_user_memories(user_id=john_doe_id)
print("Memories about John Doe:")
pprint(memories)

agent.print_response(
    "My name is John Doe and I like to paint.", stream=True, user_id=john_doe_id
)

memories = agent.get_user_memories(user_id=john_doe_id)
print("Memories about John Doe:")
pprint(memories)


agent.print_response(
    "I don't paint anymore, i draw instead.", stream=True, user_id=john_doe_id
)

memories = agent.get_user_memories(user_id=john_doe_id)

print("Memories about John Doe:")
pprint(memories)

```

## Usage

<Steps>
  <Snippet file="create-venv-step.mdx" />

  <Step title="Install libraries">
    ```bash  theme={null}
    pip install -U agno
    ```
  </Step>

  <Step title="Run Example">
    <CodeGroup>
      ```bash Mac theme={null}
      python cookbook/memory/02_agentic_memory.py
      ```

      ```bash Windows theme={null}
      python cookbook/memory/02_agentic_memory.py
      ```
    </CodeGroup>
  </Step>
</Steps>

# Share Memory between Agents

This example demonstrates how to share memory between Agents.

This means that memories created by one Agent, will be available to the other Agents.

## Code

```python agents_share_memory.py theme={null}
from agno.agent.agent import Agent
from agno.db.postgres import PostgresDb
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools
from rich.pretty import pprint

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

db = PostgresDb(db_url=db_url)

john_doe_id = "john_doe@example.com"

chat_agent = Agent(
    model=OpenAIChat(id="gpt-5-mini"),
    description="You are a helpful assistant that can chat with users",
    db=db,
    enable_user_memories=True,
)

chat_agent.print_response(
    "My name is John Doe and I like to hike in the mountains on weekends.",
    stream=True,
    user_id=john_doe_id,
)

chat_agent.print_response("What are my hobbies?", stream=True, user_id=john_doe_id)


research_agent = Agent(
    model=OpenAIChat(id="gpt-5-mini"),
    description="You are a research assistant that can help users with their research questions",
    tools=[DuckDuckGoTools(cache_results=True)],
    db=db,
    enable_user_memories=True,
)

research_agent.print_response(
    "I love asking questions about quantum computing. What is the latest news on quantum computing?",
    stream=True,
    user_id=john_doe_id,
)

memories = research_agent.get_user_memories(user_id=john_doe_id)
print("Memories about John Doe:")
pprint(memories)

```

## Usage

<Steps>
  <Snippet file="create-venv-step.mdx" />

  <Step title="Install libraries">
    ```bash  theme={null}
    pip install -U agno rich
    ```
  </Step>

  <Step title="Run Example">
    <CodeGroup>
      ```bash Mac theme={null}
      python cookbook/memory/03_agents_share_memory.py
      ```

      ```bash Windows theme={null}
      python cookbook/memory/03_agents_share_memory.py
      ```
    </CodeGroup>
  </Step>
</Steps>

# Share Memory and History between Agents

This example shows how to share memory and history between agents.

You can set `add_history_to_context=True` to add the history to the context of the agent.

You can set `enable_user_memories=True` to enable user memory generation at the end of each run.

## Code

```python share_memory_and_history_between_agents.py theme={null}
from uuid import uuid4

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat

db = SqliteDb(db_file="tmp/agent_sessions.db")

session_id = str(uuid4())
user_id = "john_doe@example.com"

agent_1 = Agent(
    model=OpenAIChat(id="gpt-5-mini"),
    instructions="You are really friendly and helpful.",
    db=db,
    add_history_to_context=True,
    enable_user_memories=True,
)

agent_2 = Agent(
    model=OpenAIChat(id="gpt-5-mini"),
    instructions="You are really grumpy and mean.",
    db=db,
    add_history_to_context=True,
    enable_user_memories=True,
)

agent_1.print_response(
    "Hi! My name is John Doe.", session_id=session_id, user_id=user_id
)

agent_2.print_response("What is my name?", session_id=session_id, user_id=user_id)

agent_2.print_response(
    "I like to hike in the mountains on weekends.",
    session_id=session_id,
    user_id=user_id,
)

agent_1.print_response("What are my hobbies?", session_id=session_id, user_id=user_id)

agent_1.print_response(
    "What have we been discussing? Give me bullet points.",
    session_id=session_id,
    user_id=user_id,
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
    pip install -U agno openai
    ```
  </Step>

  <Step title="Run Example">
    <CodeGroup>
      ```bash Mac theme={null}
      python cookbook/memory/07_share_memory_and_history_between_agents.py
      ```

      ```bash Windows theme={null}
      python cookbook/memory/07_share_memory_and_history_between_agents.py
      ```
    </CodeGroup>
  </Step>
</Steps>

# Custom Memory Manager

This example shows how you can configure the Memory Manager.

We also set custom system prompts for the memory manager. You can either override the entire system prompt or add additional instructions which is added to the end of the system prompt.

## Code

```python custom_memory_manager.py theme={null}
from agno.agent.agent import Agent
from agno.db.postgres import PostgresDb
from agno.memory import MemoryManager
from agno.models.openai import OpenAIChat
from rich.pretty import pprint

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

db = PostgresDb(db_url=db_url)

# You can also override the entire `system_message` for the memory manager
memory_manager = MemoryManager(
    model=OpenAIChat(id="gpt-5-mini"),
    additional_instructions="""
    IMPORTANT: Don't store any memories about the user's name. Just say "The User" instead of referencing the user's name.
    """,
    db=db,
)

john_doe_id = "john_doe@example.com"

agent = Agent(
    model=OpenAIChat(id="gpt-5-mini"),
    db=db,
    memory_manager=memory_manager,
    enable_user_memories=True,
    user_id=john_doe_id,
)

agent.print_response(
    "My name is John Doe and I like to swim and play soccer.", stream=True
)

agent.print_response("I dont like to swim", stream=True)


memories = agent.get_user_memories(user_id=john_doe_id)

print("John Doe's memories:")
pprint(memories)

```

## Usage

<Steps>
  <Snippet file="create-venv-step.mdx" />

  <Step title="Install libraries">
    ```bash  theme={null}
    pip install -U agno
    ```
  </Step>

  <Step title="Run Example">
    <CodeGroup>
      ```bash Mac theme={null}
      python cookbook/memory/04_custom_memory_manager.py
      ```

      ```bash Windows theme={null}
      python cookbook/memory/04_custom_memory_manager.py
      ```
    </CodeGroup>
  </Step>
</Steps>

# Memory Manager - Standalone Memory

## Code

```python memory_manager/standalone_memory.py theme={null}
from agno.db.postgres import PostgresDb
from agno.memory import MemoryManager, UserMemory
from rich.pretty import pprint

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

memory = MemoryManager(db=PostgresDb(db_url=db_url))

# Add a memory for the default user
memory.add_user_memory(
    memory=UserMemory(memory="The user's name is John Doe", topics=["name"]),
)
print("Memories:")
pprint(memory.get_user_memories())

# Add memories for Jane Doe
jane_doe_id = "jane_doe@example.com"
print(f"\nUser: {jane_doe_id}")
memory_id_1 = memory.add_user_memory(
    memory=UserMemory(memory="The user's name is Jane Doe", topics=["name"]),
    user_id=jane_doe_id,
)
memory_id_2 = memory.add_user_memory(
    memory=UserMemory(memory="She likes to play tennis", topics=["hobbies"]),
    user_id=jane_doe_id,
)
memories = memory.get_user_memories(user_id=jane_doe_id)
print("Memories:")
pprint(memories)

# Delete a memory
print("\nDeleting memory")
assert memory_id_2 is not None
memory.delete_user_memory(user_id=jane_doe_id, memory_id=memory_id_2)
print("Memory deleted\n")
memories = memory.get_user_memories(user_id=jane_doe_id)
print("Memories:")
pprint(memories)

# Replace a memory
print("\nReplacing memory")
assert memory_id_1 is not None
memory.replace_user_memory(
    memory_id=memory_id_1,
    memory=UserMemory(memory="The user's name is Jane Mary Doe", topics=["name"]),
    user_id=jane_doe_id,
)
print("Memory replaced")
memories = memory.get_user_memories(user_id=jane_doe_id)
print("Memories:")
pprint(memories)
```

## Usage

## Usage

<Steps>
  <Snippet file="create-venv-step.mdx" />

  <Step title="Install libraries">
    ```bash  theme={null}
    pip install -U agno
    ```
  </Step>

  <Step title="Run Example">
    <CodeGroup>
      ```bash Mac theme={null}
      python cookbook/memory/memory_manager/01_standalone_memory.py
      ```

      ```bash Windows theme={null}
      python cookbook/memory/memory_manager/01_standalone_memory.py
      ```
    </CodeGroup>
  </Step>
</Steps>

# Memory Manager - Memory Creation

Create user memories with an Agent by providing a either text or a list of messages.

## Code

```python memory_manager/memory_creation.py theme={null}
from agno.db.postgres import PostgresDb
from agno.memory import MemoryManager, UserMemory
from agno.models.message import Message
from agno.models.openai import OpenAIChat
from rich.pretty import pprint

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

memory_db = PostgresDb(db_url=db_url)

memory = MemoryManager(model=OpenAIChat(id="gpt-5-mini"), db=memory_db)

john_doe_id = "john_doe@example.com"
memory.add_user_memory(
    memory=UserMemory(
        memory="""
I enjoy hiking in the mountains on weekends,
reading science fiction novels before bed,
cooking new recipes from different cultures,
playing chess with friends,
and attending live music concerts whenever possible.
Photography has become a recent passion of mine, especially capturing landscapes and street scenes.
I also like to meditate in the mornings and practice yoga to stay centered.
"""
    ),
    user_id=john_doe_id,
)


memories = memory.get_user_memories(user_id=john_doe_id)
print("John Doe's memories:")
pprint(memories)

jane_doe_id = "jane_doe@example.com"
# Send a history of messages and add memories
memory.create_user_memories(
    messages=[
        Message(role="user", content="My name is Jane Doe"),
        Message(role="assistant", content="That is great!"),
        Message(role="user", content="I like to play chess"),
        Message(role="assistant", content="That is great!"),
    ],
    user_id=jane_doe_id,
)

memories = memory.get_user_memories(user_id=jane_doe_id)
print("Jane Doe's memories:")
pprint(memories)

```

## Usage

<Steps>
  <Snippet file="create-venv-step.mdx" />

  <Step title="Install libraries">
    ```bash  theme={null}
    pip install -U agno
    ```
  </Step>

  <Step title="Run Example">
    <CodeGroup>
      ```bash Mac theme={null}
      python cookbook/memory/memory_manager/02_memory_creation.py
      ```

      ```bash Windows theme={null}
      python cookbook/memory/memory_manager/02_memory_creation.py
      ```
    </CodeGroup>
  </Step>
</Steps>

# Custom Memory Instructions

Create user memories with an Agent by providing a either text or a list of messages.

## Code

```python memory_manager/custom_memory_instructions.py theme={null}
from agno.db.postgres import PostgresDb
from agno.memory import MemoryManager
from agno.models.anthropic.claude import Claude
from agno.models.message import Message
from agno.models.openai import OpenAIChat
from rich.pretty import pprint

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

memory_db = PostgresDb(db_url=db_url)

memory = MemoryManager(
    model=OpenAIChat(id="gpt-5-mini"),
    memory_capture_instructions="""\
                    Memories should only include details about the user's academic interests.
                    Only include which subjects they are interested in.
                    Ignore names, hobbies, and personal interests.
                    """,
    db=memory_db,
)

john_doe_id = "john_doe@example.com"

memory.create_user_memories(
    input="""\
My name is John Doe.

I enjoy hiking in the mountains on weekends,
reading science fiction novels before bed,
cooking new recipes from different cultures,
playing chess with friends.

I am interested to learn about the history of the universe and other astronomical topics.
""",
    user_id=john_doe_id,
)


memories = memory.get_user_memories(user_id=john_doe_id)
print("John Doe's memories:")
pprint(memories)


# Use default memory manager
memory = MemoryManager(model=Claude(id="claude-3-5-sonnet-latest"), db=memory_db)
jane_doe_id = "jane_doe@example.com"

# Send a history of messages and add memories
memory.create_user_memories(
    messages=[
        Message(role="user", content="Hi, how are you?"),
        Message(role="assistant", content="I'm good, thank you!"),
        Message(role="user", content="What are you capable of?"),
        Message(
            role="assistant",
            content="I can help you with your homework and answer questions about the universe.",
        ),
        Message(role="user", content="My name is Jane Doe"),
        Message(role="user", content="I like to play chess"),
        Message(
            role="user",
            content="Actually, forget that I like to play chess. I more enjoy playing table top games like dungeons and dragons",
        ),
        Message(
            role="user",
            content="I'm also interested in learning about the history of the universe and other astronomical topics.",
        ),
        Message(role="assistant", content="That is great!"),
        Message(
            role="user",
            content="I am really interested in physics. Tell me about quantum mechanics?",
        ),
    ],
    user_id=jane_doe_id,
)

memories = memory.get_user_memories(user_id=jane_doe_id)
print("Jane Doe's memories:")
pprint(memories)
```

## Usage

<Steps>
  <Snippet file="create-venv-step.mdx" />

  <Step title="Install libraries">
    ```bash  theme={null}
    pip install -U agno
    ```
  </Step>

  <Step title="Run Example">
    <CodeGroup>
      ```bash Mac theme={null}
      python cookbook/memory/memory_manager/03_custom_memory_instructions.py
      ```

      ```bash Windows theme={null}
      python cookbook/memory/memory_manager/03_custom_memory_instructions.py
      ```
    </CodeGroup>
  </Step>
</Steps>

# Memory Manager - Memory Search

How to search for user memories using different retrieval methods.

* `last_n`: Retrieves the last n memories
* `first_n`: Retrieves the first n memories
* `agentic`: Retrieves memories using agentic search

## Code

```python memory_manager/memory_search.py theme={null}
from agno.db.postgres import PostgresDb
from agno.memory import MemoryManager, UserMemory
from agno.models.openai import OpenAIChat
from rich.pretty import pprint

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

memory_db = PostgresDb(db_url=db_url)

memory = MemoryManager(model=OpenAIChat(id="gpt-5-mini"), db=memory_db)

john_doe_id = "john_doe@example.com"
memory.add_user_memory(
    memory=UserMemory(memory="The user enjoys hiking in the mountains on weekends"),
    user_id=john_doe_id,
)
memory.add_user_memory(
    memory=UserMemory(
        memory="The user enjoys reading science fiction novels before bed"
    ),
    user_id=john_doe_id,
)
print("John Doe's memories:")
pprint(memory.get_user_memories(user_id=john_doe_id))

memories = memory.search_user_memories(
    user_id=john_doe_id, limit=1, retrieval_method="last_n"
)
print("\nJohn Doe's last_n memories:")
pprint(memories)

memories = memory.search_user_memories(
    user_id=john_doe_id, limit=1, retrieval_method="first_n"
)
print("\nJohn Doe's first_n memories:")
pprint(memories)

memories = memory.search_user_memories(
    user_id=john_doe_id,
    query="What does the user like to do on weekends?",
    retrieval_method="agentic",
)
print("\nJohn Doe's memories similar to the query (agentic):")
pprint(memories)

```

## Usage

<Steps>
  <Snippet file="create-venv-step.mdx" />

  <Step title="Install libraries">
    ```bash  theme={null}
    pip install -U agno
    ```
  </Step>

  <Step title="Run Example">
    <CodeGroup>
      ```bash Mac theme={null}
      python cookbook/memory/memory_manager/04_memory_search.py
      ```

      ```bash Windows theme={null}
      python cookbook/memory/memory_manager/04_memory_search.py
      ```
    </CodeGroup>
  </Step>
</Steps>
