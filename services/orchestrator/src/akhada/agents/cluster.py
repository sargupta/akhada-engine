"""Cluster sub-flow (20 personas debate within cluster). V0 stub."""
from __future__ import annotations

from collections.abc import Sequence

from akhada.persona_registry.schema import Persona


def cluster_rep_position(personas: Sequence[Persona], topic: str) -> str:
    """V0: return concatenated openings as a fake cluster position."""
    return f"Cluster of {len(personas)} on '{topic}': aggregated stance pending V1."
