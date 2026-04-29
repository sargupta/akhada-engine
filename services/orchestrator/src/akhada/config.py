"""Runtime configuration via env vars."""
from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    google_genai_use_vertexai: bool = False
    google_api_key: str = ""
    gemini_model_flash: str = "gemini-2.5-flash"
    gemini_model_pro: str = "gemini-2.5-pro"

    gcp_project: str = ""
    gcp_region: str = "asia-south1"

    sarvam_api_key: str = ""
    anthropic_api_key: str = ""

    otel_exporter_otlp_endpoint: str = ""
    otel_service_name: str = "akhada-orchestrator"

    akhada_api_host: str = "127.0.0.1"
    akhada_api_port: int = 8080
    akhada_log_level: str = "INFO"


settings = Settings()
