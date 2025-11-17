"""Application configuration and environment variable loading.

This module loads and validates environment variables from .env,
providing typed configuration objects for the application.
"""

from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Load .env file from project root
project_root = Path(__file__).parent.parent
env_file = project_root / ".env"
load_dotenv(dotenv_path=env_file)


class AppConfig(BaseSettings):
    """Application-level configuration."""

    model_config = SettingsConfigDict(populate_by_name=True)

    app_name: str = Field(default="talent-signal-agent", alias="APP_NAME")
    app_env: Literal["development", "production", "test"] = Field(
        default="development", alias="APP_ENV"
    )
    debug: bool = Field(default=True, alias="DEBUG")
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO", alias="LOG_LEVEL"
    )


class OpenAIConfig(BaseSettings):
    """OpenAI API configuration."""

    model_config = SettingsConfigDict(populate_by_name=True)

    api_key: str = Field(..., alias="OPENAI_API_KEY")
    use_deep_research: bool = Field(default=True, alias="USE_DEEP_RESEARCH")


class AirtableConfig(BaseSettings):
    """Airtable API configuration."""

    model_config = SettingsConfigDict(populate_by_name=True)

    api_key: str = Field(..., alias="AIRTABLE_API_KEY")
    base_id: str = Field(..., alias="AIRTABLE_BASE_ID")

    @property
    def clean_base_id(self) -> str:
        """Extract base ID from potential base_id/table_id format.

        Returns:
            Base ID without table suffix (e.g., 'appeY64iIwU5CEna7')
        """
        # Handle case where AIRTABLE_BASE_ID contains "/table_id"
        return self.base_id.split("/")[0]


class FlaskConfig(BaseSettings):
    """Flask server configuration."""

    model_config = SettingsConfigDict(populate_by_name=True)

    host: str = Field(default="0.0.0.0", alias="FLASK_HOST")
    port: int = Field(default=5000, alias="FLASK_PORT")
    debug: bool = Field(default=True, alias="FLASK_DEBUG")


class QualityCheckConfig(BaseSettings):
    """Quality check configuration for research validation."""

    model_config = SettingsConfigDict(populate_by_name=True)

    min_citations: int = Field(default=3, alias="MIN_CITATIONS")


class Settings:
    """Global settings container with all configuration sections."""

    def __init__(self):
        """Initialize all configuration sections."""
        self.app = AppConfig()
        self.openai = OpenAIConfig()
        self.airtable = AirtableConfig()
        self.flask = FlaskConfig()
        self.quality = QualityCheckConfig()


# Global settings instance
settings = Settings()
