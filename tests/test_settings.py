"""Tests for settings module configuration loading."""

from demo.settings import settings


def test_app_config_loaded():
    """Verify application configuration is loaded correctly."""
    assert settings.app.app_name == "talent-signal-agent"
    assert settings.app.app_env in ["development", "production", "test"]
    assert isinstance(settings.app.debug, bool)
    assert settings.app.log_level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


def test_openai_config_loaded():
    """Verify OpenAI configuration has required API key."""
    assert settings.openai.api_key is not None
    assert len(settings.openai.api_key) > 0
    assert settings.openai.use_deep_research is True  # v1 requires deep research


def test_airtable_config_loaded():
    """Verify Airtable configuration has required credentials."""
    assert settings.airtable.api_key is not None
    assert len(settings.airtable.api_key) > 0
    assert settings.airtable.base_id is not None
    assert len(settings.airtable.base_id) > 0


def test_airtable_clean_base_id():
    """Verify clean_base_id property extracts base ID correctly."""
    # Should extract base ID even if base_id contains "/table_id"
    clean_id = settings.airtable.clean_base_id
    assert "/" not in clean_id
    assert clean_id.startswith("app")


def test_server_config_loaded():
    """Verify server configuration is loaded correctly."""
    assert settings.server.host is not None
    # Port 5001 used to avoid macOS AirPlay Receiver conflict on port 5001
    assert settings.server.port == 5001
    assert isinstance(settings.server.debug, bool)


def test_quality_check_config_loaded():
    """Verify quality check configuration is loaded correctly."""
    assert settings.quality.min_citations >= 1
    assert isinstance(settings.quality.min_citations, int)
