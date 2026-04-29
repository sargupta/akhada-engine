"""Super-cluster aggregator. V0 stub."""
from __future__ import annotations

from collections.abc import Sequence


def super_cluster_synth(cluster_positions: Sequence[str], topic: str) -> str:
    return (
        f"Super-cluster on '{topic}' aggregating {len(cluster_positions)} "
        f"clusters: synthesis pending V1."
    )
