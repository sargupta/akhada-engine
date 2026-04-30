"""Persona sampling.

V0.5: delegates to `fixtures.get_panel(n)` (cycle of 5 hand-curated personas).

V1 (per plan §19.2): full k-DPP per

  P(S | |S|=N) ∝ det(L_S),  L_ij = q_i q_j K(x_i, x_j)

where K is RBF on full-bio embeddings and q_i is library quality weight.
Pre-computes spectral decomposition once; per-draw complexity O(N · M^2).
"""
from __future__ import annotations

from collections.abc import Sequence

from akhada.persona_registry.fixtures import LIBRARY, get_panel
from akhada.persona_registry.schema import Persona


def sample_panel(library: Sequence[Persona] | None = None, n: int = 500) -> list[Persona]:
    """Return N personas. V0.5: cycle fixtures. V1: k-DPP with quotas + adversarial seeding."""
    src = list(library) if library is not None else LIBRARY
    if not src:
        raise ValueError("empty persona library")
    if library is None:
        return get_panel(n)
    if n > len(src):
        # When a real library is supplied but smaller than n, cycle for now.
        # V1: this raises and forces caller to expand the library or lower n.
        return [src[i % len(src)] for i in range(n)]
    return list(src[:n])
