"""Settings for the observability MCP server."""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    victoria_logs_url: str = Field(..., alias="NANOBOT_VICTORIALOGS_URL")
    victoria_traces_url: str = Field(..., alias="NANOBOT_VICTORIATRACES_URL")


def resolve_settings(base_logs_url: str | None = None, base_traces_url: str | None = None) -> Settings:
    """Resolve settings, optionally overriding for testing."""
    if base_logs_url is not None and base_traces_url is not None:
        return Settings(
            NANOBOT_VICTORIALOGS_URL=base_logs_url,
            NANOBOT_VICTORIATRACES_URL=base_traces_url,
        )
    return Settings.model_validate({})
