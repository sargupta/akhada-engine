"""V0.10 persistence + hash-chained audit.

Round-trip: save a debate + 4 events, read them back, verify chain.
Tampering: mutate a row in the DB and verify_chain detects it.
"""
from __future__ import annotations

import json
import sqlite3
import uuid

from fastapi.testclient import TestClient

from akhada.persistence.audit import compute_payload_hash, verify_chain
from akhada.persistence.sqlite import _resolve_db_path, init_db
from akhada.persistence.store import (
    get_debate,
    get_events,
    list_debates,
    save_debate_with_audit,
)


def _seed_debate() -> str:
    init_db()
    debate_id = str(uuid.uuid4())
    save_debate_with_audit(
        debate_id=debate_id,
        topic="MSP for all crops",
        backend="offline-stub",
        n_personas=5,
        library_version="personas:2026.Q2.1",
        weights_version="weights:v0.0.0",
        article="# Debate\n\n## Section\n",
        conclusive_remark="…",
        panel_archetypes=[],
        openings_failed=0,
        audit_payloads=[
            ("topic_received",       {"topic": "MSP for all crops", "n": 5}),
            ("openings_complete",    {"count": 5, "failed": 0}),
            ("synthesis_complete",   {"chars": 100}),
            ("conclusive_complete",  {"chars": 50}),
        ],
    )
    return debate_id


def test_save_and_get_roundtrip() -> None:
    debate_id = _seed_debate()
    d = get_debate(debate_id)
    assert d is not None
    assert d.id == debate_id
    assert d.topic == "MSP for all crops"
    assert d.backend == "offline-stub"
    assert d.n_personas == 5


def test_audit_chain_is_valid() -> None:
    debate_id = _seed_debate()
    events = get_events(debate_id)
    assert len(events) == 4
    assert [e.seq for e in events] == [0, 1, 2, 3]
    valid, err = verify_chain(events)
    assert valid is True, err


def test_chain_each_prev_hash_links_to_prior_payload_hash() -> None:
    debate_id = _seed_debate()
    events = get_events(debate_id)
    expected_prev = "0" * 64
    for e in events:
        assert e.prev_hash == expected_prev
        # Recompute the payload_hash from the stored payload + prev_hash.
        recomputed = compute_payload_hash(e.payload, e.prev_hash)
        assert recomputed == e.payload_hash
        expected_prev = e.payload_hash


def test_tampering_breaks_the_chain() -> None:
    debate_id = _seed_debate()

    # Mutate a stored payload directly in SQLite, simulating a tamper.
    conn = sqlite3.connect(_resolve_db_path())
    try:
        conn.execute(
            "UPDATE debate_events SET payload_json = ? WHERE debate_id = ? AND seq = 1",
            (json.dumps({"count": 999, "failed": 0}), debate_id),
        )
        conn.commit()
    finally:
        conn.close()

    events = get_events(debate_id)
    valid, err = verify_chain(events)
    assert valid is False
    assert err and "payload_hash mismatch" in err


def test_list_returns_most_recent_first() -> None:
    a = _seed_debate()
    b = _seed_debate()
    rows = list_debates(limit=10)
    ids = [r.id for r in rows]
    # b was inserted last; it should appear at or near the top.
    assert ids.index(b) <= ids.index(a)


def test_post_debate_persists_with_4_audit_events() -> None:
    from akhada.api.main import app

    client = TestClient(app)
    r = client.post(
        "/v1/debates",
        json={"topic": "Smoke test", "n_agents": 5, "cluster_size": 5, "rounds": 1},
    )
    assert r.status_code == 200
    debate_id = r.json()["debate_id"]

    audit = client.get(f"/v1/debates/{debate_id}/audit")
    assert audit.status_code == 200
    body = audit.json()
    assert body["chain_valid"] is True
    assert len(body["events"]) == 4
    assert [e["event_type"] for e in body["events"]] == [
        "topic_received",
        "openings_complete",
        "synthesis_complete",
        "conclusive_complete",
    ]


def test_get_missing_debate_returns_404() -> None:
    from akhada.api.main import app

    client = TestClient(app)
    r = client.get("/v1/debates/does-not-exist")
    assert r.status_code == 404
