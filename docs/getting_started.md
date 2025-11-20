# Getting Started

This guide will walk you through setting up and running the Talent Signal Agent on your local machine.

## Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv): A fast Python package installer and resolver.

## Installation

1.  **Install uv:**

    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

2.  **Create a virtual environment:**

    ```bash
    uv venv
    ```

3.  **Activate the virtual environment:**

    ```bash
    source .venv/bin/activate
    ```

4.  **Install dependencies:**

    ```bash
    uv pip install -e .
    ```

## Configuration

The application is configured using environment variables.

1.  **Create a `.env` file:**

    Copy the example file:

    ```bash
    cp .env.example .env
    ```

2.  **Edit the `.env` file:**

    You will need to add the following API keys and configuration values:

    -   `OPENAI_API_KEY`: Your OpenAI API key.
    -   `AIRTABLE_API_KEY`: Your Airtable API key.
    -   `AIRTABLE_BASE_ID`: The ID of your Airtable base.
    -   `AGENTOS_SECURITY_KEY`: (Optional) A secret token for authenticating with the `/screen` endpoint via bearer token.

## Running the Application

To run the FastAPI server locally:

```bash
uv run python demo/agentos_app.py
```

The server will start on `http://localhost:5001`.

## Running Tests

To run the test suite:

```bash
uv run pytest
```

Run targeted suites when iterating fast (e.g., `uv run pytest tests/test_agentos_app.py tests/test_workflow.py`) to keep the 75% coverage baseline healthy.

**Current test metrics:** 130 tests, 75% coverage
