# Crawl4ai Tools

## Code

```python cookbook/tools/crawl4ai_tools.py theme={null}
from agno.agent import Agent
from agno.tools.crawl4ai import Crawl4aiTools

agent = Agent(tools=[Crawl4aiTools(max_length=None)])
agent.print_response("Tell me about https://github.com/agno-agi/agno.")
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
    pip install -U crawl4ai openai agno
    ```
  </Step>

  <Step title="Run Agent">
    <CodeGroup>
      ```bash Mac theme={null}
      python cookbook/tools/crawl4ai_tools.py
      ```

      ```bash Windows theme={null}
      python cookbook/tools/crawl4ai_tools.py
      ```
    </CodeGroup>
  </Step>
</Steps>
