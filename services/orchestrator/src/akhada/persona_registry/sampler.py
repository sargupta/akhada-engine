"""DPP-stratified persona sampling (V0 stub returns first N).

Real implementation lands at V1 with full k-DPP per §19.2:

  P(S | |S|=N) ∝ det(L_S) where L_ij = q_i q_j K(x_i, x_j)
  K = RBF on full-bio embeddings, q_i = library quality weight.

Pre-compute spectral decomposition L = Σ λ_k v_k v_k^T once; sample via
Kulesza-Taskar 2012. Per-draw complexity O(N · M^2).
"""
from __future__ import annotations

from collections.abc import Sequence

from akhada.persona_registry.schema import Persona


def sample_panel(library: Sequence[Persona], n: int = 500) -> list[Persona]:
    """Return N personas. V0: first N. V1: k-DPP with quotas + adversarial seeding."""
    if n > len(library):
        raise ValueError(f"library has {len(library)} personas, requested {n}")
    return list(library[:n])
