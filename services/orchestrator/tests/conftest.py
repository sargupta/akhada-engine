"""Test environment guards.

The orchestrator reads `AKHADA_OFFLINE` from the .env file at startup.
In dev we set it to `false` so /v1/debates fires real Gemini. In tests
we MUST force offline mode so no test ever spends real money or makes a
network call.

This conftest:
1. Forces AKHADA_OFFLINE=true via pydantic-settings before any test
   imports the API.
2. Clears GOOGLE_API_KEY so even if a test accidentally bypasses the
   flag, the online runtime will refuse to start.
"""
from __future__ import annotations

import os

import pytest


@pytest.fixture(autouse=True, scope="session")
def _force_offline_runtime() -> None:
    os.environ["AKHADA_OFFLINE"] = "true"
    os.environ.pop("GOOGLE_API_KEY", None)

    # If `akhada.config.settings` was already imported (e.g. from .env),
    # patch it back to the offline defaults.
    try:
        from akhada import config

        config.settings.akhada_offline = True
        config.settings.google_api_key = ""
    except Exception:
        pass
