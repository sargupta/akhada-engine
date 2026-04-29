"""Deterministic dissent appendix (§6 hardened conformity guard).

Replaces v1's re-run loop, which created selection bias. Mandatorily
attaches the verbatim R1 opening with the highest cosine distance from
cluster centroid as the cluster's dissenting-voice appendix.
"""
from __future__ import annotations

from collections.abc import Sequence


def select_dissent(openings: Sequence[str], centroid_idx: int = 0) -> str:
    """V0 stub: returns the last opening. V1: cosine-farthest from centroid."""
    if not openings:
        return ""
    return openings[-1]
