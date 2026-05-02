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

    # V0.7: online vs offline mode.
    # offline (default) returns the deterministic stub debate. Tests stay
    # hermetic and CI green. online dispatches to runtime.online which
    # makes real Gemini calls — requires google_api_key set.
    akhada_offline: bool = True

    # V0.8: optional path to a JSONL persona library. When set + readable,
    # `persona_registry.fixtures` merges the 5 hand-curated fixtures with
    # the loaded library, de-duplicated by Persona.id.
    akhada_personas_file: str = ""

    # V0.10: SQLite path for the debate store + hash-chained audit log.
    # Defaults to ./data/akhada.db relative to the orchestrator working dir.
    akhada_db_path: str = ""


settings = Settings()


def online_mode_ready() -> tuple[bool, str | None]:
    """Returns (ready, reason). Ready means online debates can run."""
    if settings.akhada_offline:
        return False, "AKHADA_OFFLINE=true (default V0 stub)"
    if not settings.google_api_key:
        return False, "GOOGLE_API_KEY not set"
    return True, None
