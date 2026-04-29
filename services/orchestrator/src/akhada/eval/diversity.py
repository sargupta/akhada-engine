"""Persona diversity benchmark (§16).

V1: mean pairwise cosine on 500 sampled embeddings vs random Census baseline.
Pass bar: ≥ 0.85× Census-baseline spread.
"""
from __future__ import annotations

from collections.abc import Sequence

from akhada.persona_registry.schema import Persona


def diversity_score(panel: Sequence[Persona]) -> float:
    """V0 stub returns 0.0; V1: real cosine-distance metric."""
    return 0.0
