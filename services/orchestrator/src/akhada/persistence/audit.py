"""Hash-chained audit log (plan §20.10).

Every debate writes a sequence of events. Each event:

  prev_hash    = the previous event's payload_hash (or 64×"0" at the chain root)
  payload_hash = SHA-256(canonical_json(payload + prev_hash))

The chain is verifiable post-hoc: re-walk events in seq order, recompute
each payload_hash from the stored payload + the prior payload_hash, and
check it matches the stored payload_hash. Any tampering breaks the chain.

V1: a daily Merkle root over each day's events is committed to a GCS
WORM bucket with retention-lock so the whole chain is tamper-evident
even against database operators (per plan §20.10).
"""
from __future__ import annotations

import hashlib
import json
import time
import uuid
from dataclasses import dataclass
from typing import Any

ROOT_PREV_HASH = "0" * 64


def canonical_payload_json(payload: dict[str, Any]) -> str:
    """Sorted-key JSON for deterministic hashing."""
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)


def compute_payload_hash(payload: dict[str, Any], prev_hash: str) -> str:
    """SHA-256 over canonical(payload) ⊕ prev_hash. Linking via prev_hash
    inside the digest is what binds the chain — not just sequence order."""
    body = canonical_payload_json(payload) + "|" + prev_hash
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


@dataclass
class AuditEvent:
    event_id: str
    debate_id: str
    seq: int
    event_type: str
    prev_hash: str
    payload: dict[str, Any]
    payload_hash: str
    ts: float

    @classmethod
    def chain_next(
        cls,
        *,
        debate_id: str,
        seq: int,
        event_type: str,
        payload: dict[str, Any],
        prev_hash: str,
    ) -> "AuditEvent":
        ph = compute_payload_hash(payload, prev_hash)
        return cls(
            event_id=str(uuid.uuid4()),
            debate_id=debate_id,
            seq=seq,
            event_type=event_type,
            prev_hash=prev_hash,
            payload=payload,
            payload_hash=ph,
            ts=time.time(),
        )


def verify_chain(events: list[AuditEvent]) -> tuple[bool, str | None]:
    """Walk events in seq order, recompute hashes, check the chain."""
    if not events:
        return True, None
    sorted_events = sorted(events, key=lambda e: e.seq)
    expected_prev = ROOT_PREV_HASH
    for e in sorted_events:
        if e.prev_hash != expected_prev:
            return False, (
                f"event seq={e.seq} prev_hash mismatch: "
                f"expected {expected_prev[:8]}…, got {e.prev_hash[:8]}…"
            )
        recomputed = compute_payload_hash(e.payload, e.prev_hash)
        if recomputed != e.payload_hash:
            return False, (
                f"event seq={e.seq} payload_hash mismatch: "
                f"expected {recomputed[:8]}…, got {e.payload_hash[:8]}…"
            )
        expected_prev = e.payload_hash
    return True, None
