"""Stage D: NLI citation verifier (§7, §19.13). V0 stub.

Real impl: judge model computes p_entail(d ⊨ j); strip if < 0.85.
"""
from __future__ import annotations

from akhada.synthesis.extract import Claim

NLI_THRESHOLD = 0.85


def verify(claim: Claim, doc_text: str) -> tuple[bool, float]:
    """V0 stub: returns (True, 1.0). V1 calls Vertex NLI judge."""
    return True, 1.0
