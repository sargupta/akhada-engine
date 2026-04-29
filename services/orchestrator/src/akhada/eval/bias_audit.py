"""Quarterly bias audit (§5.7, §19.12).

50 known-stance issues × KS-test against CSDS/Pew poll baselines + Earth
Mover's distance. Pass: max KS ≤ 0.15 ∧ mean EM ≤ 0.10. Bonferroni
α_per = 0.001 over 50 tests.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class BiasAuditResult:
    max_ks: float
    mean_em: float
    passed: bool
    failed_topics: list[str]


def run_audit() -> BiasAuditResult:
    """V0 stub returns vacuous pass."""
    return BiasAuditResult(max_ks=0.0, mean_em=0.0, passed=True, failed_topics=[])
