"""CRUD for the debate store + audit chain."""
from __future__ import annotations

import asyncio
import json
import time
from dataclasses import dataclass
from typing import Any

from akhada.persistence.audit import (
    ROOT_PREV_HASH,
    AuditEvent,
    canonical_payload_json,
)
from akhada.persistence.sqlite import get_connection


@dataclass
class StoredDebate:
    id: str
    topic: str
    backend: str
    n_personas: int
    library_version: str
    weights_version: str
    article: str
    conclusive_remark: str
    panel_archetypes: list[dict[str, Any]]
    openings_failed: int
    created_at: float


def _row_to_debate(r: Any) -> StoredDebate:
    return StoredDebate(
        id=r["id"],
        topic=r["topic"],
        backend=r["backend"],
        n_personas=r["n_personas"],
        library_version=r["library_version"],
        weights_version=r["weights_version"],
        article=r["article"],
        conclusive_remark=r["conclusive_remark"],
        panel_archetypes=json.loads(r["panel_archetypes_json"]),
        openings_failed=r["openings_failed"],
        created_at=r["created_at"],
    )


def _row_to_event(r: Any) -> AuditEvent:
    return AuditEvent(
        event_id=r["event_id"],
        debate_id=r["debate_id"],
        seq=r["seq"],
        event_type=r["event_type"],
        prev_hash=r["prev_hash"],
        payload=json.loads(r["payload_json"]),
        payload_hash=r["payload_hash"],
        ts=r["ts"],
    )


def save_debate_with_audit(
    *,
    debate_id: str,
    topic: str,
    backend: str,
    n_personas: int,
    library_version: str,
    weights_version: str,
    article: str,
    conclusive_remark: str,
    panel_archetypes: list[dict[str, Any]],
    openings_failed: int,
    audit_payloads: list[tuple[str, dict[str, Any]]],
) -> list[AuditEvent]:
    """Atomically persist the debate doc and the four audit events.

    audit_payloads: list of (event_type, payload) pairs in seq order.
    Returns the resulting AuditEvent list with computed prev_hash chain.
    """
    now = time.time()
    conn = get_connection()
    try:
        with conn:
            conn.execute(
                """
                INSERT INTO debates (
                    id, topic, backend, n_personas, library_version,
                    weights_version, article, conclusive_remark,
                    panel_archetypes_json, openings_failed, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    debate_id, topic, backend, n_personas,
                    library_version, weights_version, article,
                    conclusive_remark,
                    json.dumps(panel_archetypes),
                    openings_failed, now,
                ),
            )

            events: list[AuditEvent] = []
            prev_hash = ROOT_PREV_HASH
            for seq, (event_type, payload) in enumerate(audit_payloads):
                ev = AuditEvent.chain_next(
                    debate_id=debate_id, seq=seq,
                    event_type=event_type, payload=payload, prev_hash=prev_hash,
                )
                events.append(ev)
                prev_hash = ev.payload_hash
                conn.execute(
                    """
                    INSERT INTO debate_events (
                        event_id, debate_id, seq, event_type,
                        prev_hash, payload_json, payload_hash, ts
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        ev.event_id, ev.debate_id, ev.seq, ev.event_type,
                        ev.prev_hash, canonical_payload_json(ev.payload),
                        ev.payload_hash, ev.ts,
                    ),
                )
            return events
    finally:
        conn.close()


def get_debate(debate_id: str) -> StoredDebate | None:
    conn = get_connection()
    try:
        r = conn.execute(
            "SELECT * FROM debates WHERE id = ?", (debate_id,)
        ).fetchone()
        return _row_to_debate(r) if r else None
    finally:
        conn.close()


def list_debates(limit: int = 50) -> list[StoredDebate]:
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT * FROM debates ORDER BY created_at DESC LIMIT ?",
            (limit,),
        ).fetchall()
        return [_row_to_debate(r) for r in rows]
    finally:
        conn.close()


def get_events(debate_id: str) -> list[AuditEvent]:
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT * FROM debate_events WHERE debate_id = ? ORDER BY seq",
            (debate_id,),
        ).fetchall()
        return [_row_to_event(r) for r in rows]
    finally:
        conn.close()


# ---- async wrappers (FastAPI handlers are async) ----------------------

async def save_async(**kwargs: Any) -> list[AuditEvent]:
    return await asyncio.to_thread(save_debate_with_audit, **kwargs)


async def get_debate_async(debate_id: str) -> StoredDebate | None:
    return await asyncio.to_thread(get_debate, debate_id)


async def list_debates_async(limit: int = 50) -> list[StoredDebate]:
    return await asyncio.to_thread(list_debates, limit)


async def get_events_async(debate_id: str) -> list[AuditEvent]:
    return await asyncio.to_thread(get_events, debate_id)
