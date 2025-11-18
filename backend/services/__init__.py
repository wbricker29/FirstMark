"""
Service clients for external integrations

Services:
- AirtableClient: Interface for Airtable operations
- OpenAIClient: Interface for OpenAI API operations
"""
from .airtable_client import AirtableClient
from .openai_client import OpenAIClient

__all__ = [
    "AirtableClient",
    "OpenAIClient"
]
