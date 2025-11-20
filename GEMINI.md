# Gemini Project Context: Talent Signal Agent

This document provides a comprehensive overview of the "Talent Signal Agent" project to be used as instructional context for Gemini.

## Project Overview

The "Talent Signal Agent" is an AI-powered executive matching system designed for FirstMark Capital. Its primary purpose is to automate the screening of executive candidates for roles within FirstMark's portfolio companies.

The system is architected as a Python-based application using FastAPI for its web server and Pydantic for data validation. It leverages a framework called "AgentOS" for orchestrating AI agent workflows. The core logic is encapsulated in a four-step pipeline that researches candidates, checks the quality of the research, performs additional searches if necessary, and finally assesses the candidate against a given role specification. The system is designed to be triggered by webhooks from Airtable, where the candidate and role data are managed.

### Core Technologies

*   **Backend:** Python, FastAPI
*   **AI Orchestration:** AgentOS
*   **Data Validation:** Pydantic
*   **Dependency Management:** uv
*   **Database:** SQLite for session storage
*   **External Services:** Airtable, OpenAI

### Key Files and Directories

*   `demo/agentos_app.py`: The main FastAPI application that defines the `/screen` webhook endpoint.
*   `demo/workflow.py`: Contains the `AgentOSCandidateWorkflow` class, which orchestrates the four-step candidate screening process.
*   `demo/models.py`: Defines the Pydantic data models used throughout the application.
*   `demo/prompts/catalog.yaml`: A centralized YAML file that defines the prompts used by the AI agents.
*   `tests/`: The test suite for the project.
*   `README.md`: The main documentation file, containing detailed setup, usage, and architectural information.
*   `.env.example`: An example file for configuring environment variables.

## Building and Running

The project uses `uv` for dependency management and a virtual environment.

### Setup

1.  **Install uv:**
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```
2.  **Install Dependencies:**
    ```bash
    uv pip install -e .
    ```
3.  **Configure Environment Variables:**
    *   Copy `.env.example` to `.env`.
    *   Populate the required API keys (`OPENAI_API_KEY`, `AIRTABLE_API_KEY`, `AIRTABLE_BASE_ID`).

### Running the Application

To run the FastAPI server locally:

```bash
uv run python demo/agentos_app.py
```

The server will start on `http://localhost:5001`. For webhook testing during development, the `README.md` recommends using `ngrok` to expose the local server to the internet.

### Running Tests

The `README.md` mentions a specific test for model validation:

```bash
.venv/bin/python tests/test_models_validation.py
```

To run the full test suite, you would likely use a test runner like `pytest`:

```bash
# TODO: Confirm the exact command to run the full test suite.
# It is likely one of the following:
pytest
# or
.venv/bin/python -m pytest
```

## Development Conventions

*   **Configuration:** All configuration is managed through environment variables loaded via a `settings.py` file. The `.env` file is used for local development.
*   **Logging:** The application uses Python's built-in `logging` module with a consistent format defined in `demo/agentos_app.py`.
*   **Workflow Orchestration:** The core business logic is structured as a series of steps within an `AgentOS` workflow. This provides a clear and repeatable process for candidate screening.
*   **State Management:** The workflow uses a SQLite database (`tmp/agno_sessions.db`) to persist session state, ensuring that the progress of each screening run is tracked.
*   **Modularity:** The application is well-structured, with clear separation of concerns between the web server, workflow logic, data models, and agent definitions.
