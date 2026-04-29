"""Stage A: transcript → JSON `claims[]`. V0 stub."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Claim:
    text: str
    supporting_personas: list[str]
    opposing_personas: list[str]
    evidence_doc_ids: list[str]
    confidence: float
    contention_score: float
    cluster_distribution: dict[int, float]


def extract_claims(transcript: str) -> list[Claim]:
    """V0 stub. V1: Pro-tier extraction with structured JSON output."""
    return []
