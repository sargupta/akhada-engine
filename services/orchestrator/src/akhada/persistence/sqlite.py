"""SQLite schema + connection management.

One database per environment. Default path: `data/akhada.db` relative to
the orchestrator working directory. Override via `AKHADA_DB_PATH`.
"""
from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Final

from akhada.config import settings

_SCHEMA: Final[str] = """
CREATE TABLE IF NOT EXISTS debates (
    id                   TEXT PRIMARY KEY,
    topic                TEXT NOT NULL,
    backend              TEXT NOT NULL,
    n_personas           INTEGER NOT NULL,
    library_version      TEXT NOT NULL,
    weights_version      TEXT NOT NULL,
    article              TEXT NOT NULL,
    conclusive_remark    TEXT NOT NULL,
    panel_archetypes_json TEXT NOT NULL,
    openings_failed      INTEGER NOT NULL,
    created_at           REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS debate_events (
    event_id     TEXT PRIMARY KEY,
    debate_id    TEXT NOT NULL,
    seq          INTEGER NOT NULL,
    event_type   TEXT NOT NULL,
    prev_hash    TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    payload_hash TEXT NOT NULL,
    ts           REAL NOT NULL,
    FOREIGN KEY (debate_id) REFERENCES debates(id),
    UNIQUE (debate_id, seq)
);

CREATE INDEX IF NOT EXISTS idx_debate_events_debate_id
    ON debate_events(debate_id);
CREATE INDEX IF NOT EXISTS idx_debates_created_at
    ON debates(created_at DESC);
"""


def _resolve_db_path() -> Path:
    if settings.akhada_db_path:
        return Path(settings.akhada_db_path).expanduser()
    return Path("data") / "akhada.db"


def get_connection() -> sqlite3.Connection:
    path = _resolve_db_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    return conn


def init_db() -> None:
    """Create tables and indexes if they don't exist."""
    conn = get_connection()
    try:
        conn.executescript(_SCHEMA)
        conn.commit()
    finally:
        conn.close()
