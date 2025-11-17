# Create Your First AgentOS

> Quick setup guide to get your first AgentOS instance running locally

Get started with AgentOS by setting up a minimal local instance.
This guide will have you running your first agent in minutes, with optional paths to add advanced features through our examples.

<Check>
  AgentOS is a FastAPI app that you can run locally or in your cloud. If you want to build AgentOS using an existing FastAPI app, check out the [Custom FastAPI App](/agent-os/customize/custom-fastapi) guide.
</Check>

## Prerequisites

* Python 3.9+
* An LLM provider API key (e.g., `OPENAI_API_KEY`)

## Installation

Create and activate a virtual environment:

<CodeGroup>
  ```bash Mac theme={null}
  # Create virtual environment
  python -m venv venv

  # Activate virtual environment
  source venv/bin/activate
  ```

  ```bash Windows theme={null}
  # Create virtual environment
  python -m venv venv

  # Activate virtual environment
  venv\Scripts\activate
  ```
</CodeGroup>

Install dependencies:

```bash  theme={null}
pip install -U agno "fastapi[standard]" uvicorn openai
```

## Minimal Setup

Create `my_os.py`:

```python  theme={null}
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.os import AgentOS

assistant = Agent(
    name="Assistant",
    model=OpenAIChat(id="gpt-5-mini"),
    instructions=["You are a helpful AI assistant."],
    markdown=True,
)

agent_os = AgentOS(
    id="my-first-os",
    description="My first AgentOS",
    agents=[assistant],
)

app = agent_os.get_app()

if __name__ == "__main__":
    # Default port is 7777; change with port=...
    agent_os.serve(app="my_os:app", reload=True)
```

## Running Your OS

Start your AgentOS:

```bash  theme={null}
python my_os.py
```

Access your running instance:

* **App Interface**: `http://localhost:7777` - Use this URL when connecting to the AgentOS control plane
* **API Documentation**: `http://localhost:7777/docs` - Interactive API documentation and testing
* **Configuration**: `http://localhost:7777/config` - View AgentOS configuration
* **API Reference**: View the [AgentOS API documentation](/reference-api/overview) for programmatic access

## Connecting to the Control Plane

With your AgentOS now running locally (`http://localhost:7777`), you can connect it to the AgentOS control plane for a enhanced management experience. The control plane provides a centralized interface to interact with your agents, manage knowledge bases, track sessions, and monitor performance.

## Next Steps

<CardGroup cols={2}>
  <Card title="Connect to Control Plane" icon="link" href="/agent-os/connecting-your-os">
    Connect your running OS to the AgentOS control plane interface
  </Card>

  <Card title="Browse Examples" icon="code" href="/examples/agent-os/demo">
    Explore comprehensive examples for advanced AgentOS configurations
  </Card>
</CardGroup>

# Connecting Your AgentOS

> Step-by-step guide to connect your local AgentOS to the AgentOS Control Plane

## Overview

Connecting your AgentOS is the critical first step to using the AgentOS Control Plane. This process establishes a connection between your running AgentOS instance and the Control Plane, allowing you to manage, monitor, and interact with your agents through the browser.

<Note>
  **Prerequisites**: You need a running AgentOS instance before you can connect
  it to the Control Plane. If you haven't created one yet, check out our [Creating
  Your First OS](/agent-os/creating-your-first-os) guide.
</Note>

See the [AgentOS Control Plane](/agent-os/control-plane) documentation for more information about the Control Plane.

## Step-by-Step Connection Process

### 1. Access the Connection Dialog

In the Agno platform:

1. Click on the team/organization dropdown in the top navigation bar
2. Click the **"+"** (plus) button next to "Add new OS"
3. The "Connect your AgentOS" dialog will open

<Frame>
  <video autoPlay muted loop playsInline style={{ borderRadius: "0.5rem", width: "100%", height: "auto" }}>
    <source src="https://mintcdn.com/agno-v2/MMgohmDbM-qeNPya/videos/agent-os-connect-os.mp4?fit=max&auto=format&n=MMgohmDbM-qeNPya&q=85&s=c427bf5bbd76c0495540b49aa64f5604" type="video/mp4" data-path="videos/agent-os-connect-os.mp4" />
  </video>
</Frame>

### 2. Choose Your Environment

Select **"Local"** for development or **"Live"** for production:

* **Local**: Connects to an AgentOS running on your local machine
* **Live**: Connects to a production AgentOS running on your infrastructure

<Note>Live AgentOS connections require a PRO subscription.</Note>

### 3. Configure Connection Settings

#### Endpoint URL

* **Default Local**: `http://localhost:7777`
* **Custom Local**: You can change the port if your AgentOS runs on a different port
* **Live**: Enter your production HTTPS URL

<Warning>
  Make sure your AgentOS is actually running on the specified endpoint before
  attempting to connect.
</Warning>

#### OS Name

Give your AgentOS a descriptive name:

* Use clear, descriptive names like "Development OS" or "Production Chat Bot"
* This name will appear in your OS list and help you identify different instances

#### Tags (Optional)

Add tags to organize your AgentOS instances:

* Examples: `development`, `production`, `chatbot`, `research`
* Tags help filter and organize multiple OS instances
* Click the **"+"** button to add multiple tags

### 4. Test and Connect

1. Click the **"CONNECT"** button
2. The platform will attempt to establish a connection to your AgentOS
3. If successful, you'll see your new OS in the organization dashboard

## Verifying Your Connection

Once connected, you should see:

1. **OS Status**: "Running" indicator in the platform
2. **Available Features**: Chat, Knowledge, Memory, Sessions, etc. should be accessible
3. **Agent List**: Your configured agents should appear in the chat interface

## Securing Your Connection

Protect your AgentOS APIs and Control Plane access with bearer-token authentication. Security keys provide essential protection for both development and production environments.

**Key Features:**

* Generate unique security keys per AgentOS instance
* Rotate keys easily through the organization settings
* Configure bearer-token authentication on your server

<Frame>
  <video autoPlay muted loop playsInline style={{ borderRadius: "0.5rem", width: "100%", height: "auto" }}>
    <source src="https://mintcdn.com/agno-v2/xm93WWN8gg4nzCGE/videos/agentos-security-key.mp4?fit=max&auto=format&n=xm93WWN8gg4nzCGE&q=85&s=0a87c2a894982a3eb075fe282a21c491" type="video/mp4" data-path="videos/agentos-security-key.mp4" />
  </video>
</Frame>

<Note>
  For complete security setup instructions, including environment configuration
  and best practices, see the [Security Key](/agent-os/security) documentation.
</Note>

## Managing Connected OS Instances

### Switching Between OS Instances

1. Use the dropdown in the top navigation bar
2. Select the OS instance you want to work with
3. All platform features will now connect to the selected OS

### Disconnecting an OS

1. Go to the organization settings
2. Find the OS in your list
3. Click the delete option

<Warning>
  Disconnecting an OS doesn't stop the AgentOS instance - it only removes it
  from the platform interface.
</Warning>

## Next Steps

Once your AgentOS is successfully connected:

<CardGroup cols={2}>
  <Card title="Explore the Chat Interface" icon="comment" href="/agent-os/features/chat-interface">
    Start having conversations with your connected agents
  </Card>

  <Card title="Manage Knowledge" icon="brain" href="/agent-os/features/knowledge-management">
    Upload and organize your knowledge bases
  </Card>

  <Card title="Monitor Sessions" icon="chart-line" href="/agent-os/features/session-tracking">
    Track and analyze your agent interactions
  </Card>
</CardGroup>

# AgentUI

> An Open Source AgentUI for your AgentOS

<Frame>
  <img height="200" src="https://mintcdn.com/agno-v2/QfHdyhk-tu-JEw8s/images/agent-ui.png?fit=max&auto=format&n=QfHdyhk-tu-JEw8s&q=85&s=72cd1f0888dea4f1ec60a67bff5664c4" style={{ borderRadius: '8px' }} data-og-width="5364" data-og-height="2808" data-path="images/agent-ui.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/agno-v2/QfHdyhk-tu-JEw8s/images/agent-ui.png?w=280&fit=max&auto=format&n=QfHdyhk-tu-JEw8s&q=85&s=8a962c7d75c6fd40d37b696f258b69fc 280w, https://mintcdn.com/agno-v2/QfHdyhk-tu-JEw8s/images/agent-ui.png?w=560&fit=max&auto=format&n=QfHdyhk-tu-JEw8s&q=85&s=729e6c42c46d47f9c56c66451576c53a 560w, https://mintcdn.com/agno-v2/QfHdyhk-tu-JEw8s/images/agent-ui.png?w=840&fit=max&auto=format&n=QfHdyhk-tu-JEw8s&q=85&s=cabb3ed5cb4c1934bd3a5a1cba70a2d1 840w, https://mintcdn.com/agno-v2/QfHdyhk-tu-JEw8s/images/agent-ui.png?w=1100&fit=max&auto=format&n=QfHdyhk-tu-JEw8s&q=85&s=d880656a6c120ed2ef06879bb522b840 1100w, https://mintcdn.com/agno-v2/QfHdyhk-tu-JEw8s/images/agent-ui.png?w=1650&fit=max&auto=format&n=QfHdyhk-tu-JEw8s&q=85&s=55b22efc72db2bbb9e26079d46aea5b5 1650w, https://mintcdn.com/agno-v2/QfHdyhk-tu-JEw8s/images/agent-ui.png?w=2500&fit=max&auto=format&n=QfHdyhk-tu-JEw8s&q=85&s=5331541ccf7abdb289f0e213f65c9649 2500w" />
</Frame>

Agno provides a beautiful UI for interacting with your agents, completely open source, free to use and build on top of. It's a simple interface that allows you to chat with your agents, view their memory, knowledge, and more.

<Note>
  The AgentOS only uses data in your database. No data is sent to Agno.
</Note>

The Open Source Agent UI is built with Next.js and TypeScript. After the success of the [Agent AgentOS](/agent-os/introduction), the community asked for a self-hosted alternative and we delivered!

## Get Started with Agent UI

To clone the Agent UI, run the following command in your terminal:

```bash  theme={null}
npx create-agent-ui@latest
```

Enter `y` to create a new project, install dependencies, then run the agent-ui using:

```bash  theme={null}
cd agent-ui && npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to view the Agent UI, but remember to connect to your local agents.

<Frame>
  <img height="200" src="https://mintcdn.com/agno-v2/QfHdyhk-tu-JEw8s/images/agent-ui-homepage.png?fit=max&auto=format&n=QfHdyhk-tu-JEw8s&q=85&s=8f6e365622aefac39432083f2ec587df" style={{ borderRadius: '8px' }} data-og-width="3096" data-og-height="1832" data-path="images/agent-ui-homepage.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/agno-v2/QfHdyhk-tu-JEw8s/images/agent-ui-homepage.png?w=280&fit=max&auto=format&n=QfHdyhk-tu-JEw8s&q=85&s=f1d2aa67b73246a4d71f84fc9b581cd0 280w, https://mintcdn.com/agno-v2/QfHdyhk-tu-JEw8s/images/agent-ui-homepage.png?w=560&fit=max&auto=format&n=QfHdyhk-tu-JEw8s&q=85&s=969732c206fb7c33e7f575aae105294a 560w, https://mintcdn.com/agno-v2/QfHdyhk-tu-JEw8s/images/agent-ui-homepage.png?w=840&fit=max&auto=format&n=QfHdyhk-tu-JEw8s&q=85&s=f1cf21fec03209156f4d1eeec6a12163 840w, https://mintcdn.com/agno-v2/QfHdyhk-tu-JEw8s/images/agent-ui-homepage.png?w=1100&fit=max&auto=format&n=QfHdyhk-tu-JEw8s&q=85&s=adf49bc5198a1c4283d0bdb9ffcf91f7 1100w, https://mintcdn.com/agno-v2/QfHdyhk-tu-JEw8s/images/agent-ui-homepage.png?w=1650&fit=max&auto=format&n=QfHdyhk-tu-JEw8s&q=85&s=438d2965108fb49d808e89f9928613a3 1650w, https://mintcdn.com/agno-v2/QfHdyhk-tu-JEw8s/images/agent-ui-homepage.png?w=2500&fit=max&auto=format&n=QfHdyhk-tu-JEw8s&q=85&s=b02e0c727983bc3329b8046dfa18d3a5 2500w" />
</Frame>

<br />

<Accordion title="Clone the repository manually" icon="github">
  You can also clone the repository manually

  ```bash  theme={null}
  git clone https://github.com/agno-agi/agent-ui.git
  ```

  And run the agent-ui using

  ```bash  theme={null}
  cd agent-ui && pnpm install && pnpm dev
  ```
</Accordion>

## Connect your AgentOS

The Agent UI needs to connect to a AgentOS server, which you can run locally or on any cloud provider.

Let's start with a local AgentOS server. Create a file `agentos.py`

```python agentos.py theme={null}
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.os import AgentOS
from agno.db.sqlite import SqliteDb
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools

agent_storage: str = "tmp/agents.db"

web_agent = Agent(
    name="Web Agent",
    model=OpenAIChat(id="gpt-5-mini"),
    tools=[DuckDuckGoTools()],
    instructions=["Always include sources"],
    # Store the agent sessions in a sqlite database
    db=SqliteDb(db_file=agent_storage),
    # Adds the current date and time to the context
    add_datetime_to_context=True,
    # Adds the history of the conversation to the messages
    add_history_to_context=True,
    # Number of history responses to add to the messages
    num_history_runs=5,
    # Adds markdown formatting to the messages
    markdown=True,
)

finance_agent = Agent(
    name="Finance Agent",
    model=OpenAIChat(id="gpt-5-mini"),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True, company_news=True)],
    instructions=["Always use tables to display data"],
    db=SqliteDb(db_file=agent_storage),
    add_datetime_to_context=True,
    add_history_to_context=True,
    num_history_runs=5,
    markdown=True,
)

agent_os = AgentOS(agents=[web_agent, finance_agent])
app = agent_os.get_app()

if __name__ == "__main__":
    agent_os.serve("agentos:app", reload=True)
```

In another terminal, run the AgentOS server:

<Steps>
  <Step title="Setup your virtual environment">
    <CodeGroup>
      ```bash Mac theme={null}
      python3 -m venv .venv
      source .venv/bin/activate
      ```

      ```bash Windows theme={null}
      python3 -m venv aienv
      aienv/scripts/activate
      ```
    </CodeGroup>
  </Step>

  <Step title="Install dependencies">
    <CodeGroup>
      ```bash Mac theme={null}
      pip install -U openai ddgs yfinance sqlalchemy 'fastapi[standard]' agno
      ```

      ```bash Windows theme={null}
      pip install -U openai ddgs yfinance sqlalchemy 'fastapi[standard]' agno
      ```
    </CodeGroup>
  </Step>

  <Step title="Export your OpenAI key">
    <CodeGroup>
      ```bash Mac theme={null}
      export OPENAI_API_KEY=sk-***
      ```

      ```bash Windows theme={null}
      setx OPENAI_API_KEY sk-***
      ```
    </CodeGroup>
  </Step>

  <Step title="Run the AgentOS">
    ```shell  theme={null}
    python agentos.py
    ```
  </Step>
</Steps>

<Tip>Make sure the `serve_agentos_app()` points to the file containing your `AgentOS` app.</Tip>

## View the AgentUI

* Open [http://localhost:3000](http://localhost:3000) to view the Agent UI
* Enter the `localhost:7777` endpoint on the left sidebar and start chatting with your agents and teams!

<video autoPlay muted controls className="w-full aspect-video" src="https://mintcdn.com/agno-v2/APlycdxch1exeM4A/videos/agent-ui-demo.mp4?fit=max&auto=format&n=APlycdxch1exeM4A&q=85&s=646f460d718e8c3d09b479277088fa19" data-path="videos/agent-ui-demo.mp4" />
