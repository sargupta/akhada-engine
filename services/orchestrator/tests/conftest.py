"""Test environment guards.

The orchestrator reads `.env` at startup. In dev .env carries
AKHADA_OFFLINE=false + GOOGLE_API_KEY + AKHADA_PERSONAS_FILE so real
debates and the loaded persona library are live. In tests we must:

  - force AKHADA_OFFLINE=true
  - clear GOOGLE_API_KEY (so an accidental online call refuses)
  - clear AKHADA_PERSONAS_FILE (so fixtures.LIBRARY = 5 hand-curated only)
  - point AKHADA_DB_PATH at a per-session temp SQLite (so persistence
    tests don't pollute the dev store)

These overrides MUST happen before pydantic-settings instantiates
`Settings` from the .env file. pytest loads `conftest.py` top-level
code BEFORE collecting test modules, so we set os.environ here at
top level (not inside a fixture, which would run too late).
"""
from __future__ import annotations

import os
import tempfile

os.environ["AKHADA_OFFLINE"] = "true"
os.environ["GOOGLE_API_KEY"] = ""
os.environ["AKHADA_PERSONAS_FILE"] = ""

_TMPDB = os.path.join(tempfile.gettempdir(), "akhada-test.db")
try:
    os.remove(_TMPDB)
except FileNotFoundError:
    pass
os.environ["AKHADA_DB_PATH"] = _TMPDB
