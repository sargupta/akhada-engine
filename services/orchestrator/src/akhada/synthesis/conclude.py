"""Stage C: argument-quality-weighted conclusive remark.

Bradley-Terry calibrated weights (§19.6). V0 stub uses uniform weights.

  q_j = β1·g_j + β2·l_j + β3·r_j + β4·s_j − β5·c_j

where g, l, r, s, c ∈ [0, 1] are evidence groundedness, logical coherence,
cross-cluster reach, red-team survival, conformity inflation. β fit via
B-T MLE on a 50-debate × 3-rater calibration set.
"""
from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from akhada.synthesis.extract import Claim


@dataclass(frozen=True)
class QualityWeights:
    """Versioned weights. Default `weights:v0.0.0` — all 1, no calibration."""
    version: str = "weights:v0.0.0"
    beta_evidence: float = 1.0
    beta_coherence: float = 1.0
    beta_reach: float = 1.0
    beta_red_team: float = 1.0
    beta_conformity: float = -0.5  # penalty


def quality_score(c: Claim, w: QualityWeights = QualityWeights()) -> float:
    """V0 stub: confidence × (1 - contention_score). V1 implements full formula."""
    return c.confidence * (1.0 - c.contention_score)


def conclusive_remark(
    claims: Sequence[Claim], topic: str, k: int = 5, w: QualityWeights = QualityWeights()
) -> str:
    if not claims:
        return f"Conclusive remark on '{topic}' pending V1."
    ranked = sorted(claims, key=lambda c: quality_score(c, w), reverse=True)[:k]
    bullets = "\n".join(f"- {c.text}" for c in ranked)
    return f"Conclusive on '{topic}' (weights {w.version}):\n{bullets}"
