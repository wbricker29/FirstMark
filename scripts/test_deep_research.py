"""
Test script to understand Deep Research API response structure via Agno.

This script creates a simple Agno agent using o4-mini-deep-research
and examines what's returned to understand citation extraction.
"""

import os
from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from pydantic import BaseModel, Field
from typing import List, Optional
from rich.pretty import pprint
from rich.console import Console

console = Console()


# Define a simple structured output schema
class Citation(BaseModel):
    url: str
    title: Optional[str] = None
    quote: Optional[str] = None


class SimpleResearchResult(BaseModel):
    """Simple research output to test structured responses."""

    executive_name: str
    current_role: str
    current_company: str
    summary: str = Field(
        description="2-3 sentence summary of the executive's background"
    )
    key_experiences: List[str] = Field(description="Notable roles and achievements")
    sector_expertise: List[str] = Field(
        description="Industry sectors they have experience in"
    )
    citations: List[Citation] = Field(description="Source URLs and quotes")


def test_deep_research_basic():
    """Test basic deep research call without structured output."""
    console.print(
        "\n[bold cyan]TEST 1: Basic Deep Research (no structured output)[/bold cyan]\n"
    )

    agent = Agent(
        model=OpenAIResponses(id="o4-mini-deep-research", max_tool_calls=1),
        instructions="""
            Research this executive comprehensively using all available sources.
            Focus on: current role, career trajectory, notable achievements.
            Include citations for all claims.
        """,
    )

    # Simple research query
    query = """
    Research: Satya Nadella
    Current Role: CEO at Microsoft

    Provide a brief summary of his background and key achievements.
    """

    console.print("[yellow]Running research query...[/yellow]")
    result = agent.run(query)

    console.print("\n[bold green]Response Type:[/bold green]", type(result))
    console.print("\n[bold green]Response Attributes:[/bold green]")
    pprint(dir(result))

    console.print("\n[bold green]Response Content:[/bold green]")
    pprint(result.content)

    # Check if there are other useful attributes
    if hasattr(result, "messages"):
        console.print("\n[bold green]Messages:[/bold green]")
        pprint(result.messages)

    if hasattr(result, "output"):
        console.print("\n[bold green]Output:[/bold green]")
        pprint(result.output)

    if hasattr(result, "model_response"):
        console.print("\n[bold green]Model Response:[/bold green]")
        pprint(result.model_response)

    return result


def test_deep_research_structured():
    """Test deep research with structured output schema."""
    console.print(
        "\n\n[bold cyan]TEST 2: Deep Research with Structured Output[/bold cyan]\n"
    )

    agent = Agent(
        model=OpenAIResponses(id="o4-mini-deep-research", max_tool_calls=1),
        instructions="""
            Research this executive comprehensively using all available sources.
            Focus on: current role, career trajectory, sector expertise, notable achievements.
            Return results in the structured format provided.
        """,
        output_schema=SimpleResearchResult,
    )

    query = """
    Research: Satya Nadella
    Current Role: CEO at Microsoft
    """

    console.print("[yellow]Running research query with structured output...[/yellow]")
    result = agent.run(query)

    console.print("\n[bold green]Response Type:[/bold green]", type(result))
    console.print(
        "\n[bold green]Response Content Type:[/bold green]", type(result.content)
    )
    console.print("\n[bold green]Response Content:[/bold green]")
    pprint(result.content)

    # Try to access structured data
    if isinstance(result.content, SimpleResearchResult):
        console.print(
            "\n[bold green]✅ Structured output successfully parsed![/bold green]"
        )
        console.print("\n[bold magenta]Citations found:[/bold magenta]")
        pprint(result.content.citations)

    return result


def test_openai_sdk_direct():
    """Test using OpenAI SDK directly for comparison."""
    console.print(
        "\n\n[bold cyan]TEST 3: OpenAI SDK Direct (for comparison)[/bold cyan]\n"
    )

    from openai import OpenAI

    client = OpenAI(timeout=3600)

    query = """
    Research: Satya Nadella, CEO at Microsoft

    Provide a brief summary of his background and key achievements.
    Include citations.
    """

    console.print("[yellow]Running research via OpenAI SDK...[/yellow]")
    response = client.responses.create(
        model="o4-mini-deep-research",
        input=query,
        tools=[{"type": "web_search_preview"}],
        max_completion_tokens=1000,  # Keep it short for testing
    )

    console.print("\n[bold green]Response Type:[/bold green]", type(response))
    console.print("\n[bold green]Response Attributes:[/bold green]")
    pprint(dir(response))

    console.print("\n[bold green]Output Text:[/bold green]")
    console.print(response.output_text)

    if hasattr(response, "output"):
        console.print("\n[bold green]Output Array:[/bold green]")
        pprint(response.output)

        # Look for annotations
        for item in response.output:
            if hasattr(item, "type") and item.type == "message":
                console.print("\n[bold magenta]Message content:[/bold magenta]")
                pprint(item.content)

                # Check for annotations
                if hasattr(item.content[0], "annotations"):
                    console.print("\n[bold green]✅ Annotations found![/bold green]")
                    pprint(item.content[0].annotations)

    return response


if __name__ == "__main__":
    console.print(
        "\n[bold blue]═══════════════════════════════════════════════════════[/bold blue]"
    )
    console.print(
        "[bold blue]     Deep Research API Citation Extraction Test        [/bold blue]"
    )
    console.print(
        "[bold blue]═══════════════════════════════════════════════════════[/bold blue]\n"
    )

    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        console.print(
            "[bold red]❌ OPENAI_API_KEY not found in environment![/bold red]"
        )
        console.print("[yellow]Please set your OpenAI API key:[/yellow]")
        console.print("  export OPENAI_API_KEY=sk-...")
        exit(1)

    try:
        # Run tests
        result1 = test_deep_research_basic()
        result2 = test_deep_research_structured()
        result3 = test_openai_sdk_direct()

        console.print(
            "\n[bold green]═══════════════════════════════════════════════════════[/bold green]"
        )
        console.print(
            "[bold green]                    Tests Complete!                      [/bold green]"
        )
        console.print(
            "[bold green]═══════════════════════════════════════════════════════[/bold green]\n"
        )

    except Exception as e:
        console.print("\n[bold red]❌ Error during testing:[/bold red]")
        console.print(f"[red]{str(e)}[/red]")
        import traceback

        console.print(f"\n[dim]{traceback.format_exc()}[/dim]")
