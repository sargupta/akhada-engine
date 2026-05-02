"""Top-level debate flow.

V0/V0.7 dispatcher between two backends:
  - offline (default): a deterministic synchronous Python stub used by
    tests + CI. No model calls.
  - online: dispatches to `runtime.online.run_real_debate`, which calls
    real Gemini Flash + Pro via google-genai. Requires `GOOGLE_API_KEY`
    and `AKHADA_OFFLINE=false`.

V1 (plan §6) rebuilds online as a real ADK SequentialAgent +
ParallelAgent pipeline with cluster/super-cluster layers and audit-
trail emission.
"""
from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from akhada.agents.cluster import cluster_rep_position
from akhada.agents.final import final_synthesis
from akhada.agents.persona_leaf import open_statement
from akhada.agents.super_cluster import super_cluster_synth
from akhada.config import online_mode_ready
from akhada.persona_registry.schema import Persona


@dataclass
class DebateResult:
    topic: str
    article: str
    conclusive_remark: str
    openings: list[str]
    cluster_positions: list[str]
    super_positions: list[str]
    backend: str = "offline-stub"
    openings_failed: int = 0


def run_debate(topic: str, panel: Sequence[Persona], cluster_size: int = 20) -> DebateResult:
    """V0 deterministic stub. Always available — no network."""
    openings = [open_statement(p, topic) for p in panel]

    clusters: list[list[Persona]] = [
        list(panel[i : i + cluster_size]) for i in range(0, len(panel), cluster_size)
    ]
    cluster_positions = [cluster_rep_position(c, topic) for c in clusters]

    super_buckets: list[list[str]] = [
        cluster_positions[i : i + 5] for i in range(0, len(cluster_positions), 5)
    ]
    super_positions = [super_cluster_synth(b, topic) for b in super_buckets]

    article = (
        f"# Debate: {topic}\n\n"
        f"## Perspectives by super-cluster\n"
        + "\n".join(f"- {s}" for s in super_positions)
        + "\n\n## Article body — V0 stub. Real synthesis lands V1.\n"
    )
    conclusive = final_synthesis(super_positions, topic)

    return DebateResult(
        topic=topic,
        article=article,
        conclusive_remark=conclusive,
        openings=openings,
        cluster_positions=cluster_positions,
        super_positions=super_positions,
    )


async def run_debate_async(
    topic: str, panel: Sequence[Persona], cluster_size: int = 20
) -> DebateResult:
    """Dispatch: online when ready, otherwise offline stub."""
    ready, _reason = online_mode_ready()
    if not ready:
        return run_debate(topic, panel, cluster_size)

    # Lazy import — google-genai only loaded in online mode.
    from akhada.runtime.online import run_real_debate

    online = await run_real_debate(topic, panel)
    return DebateResult(
        topic=online.topic,
        article=online.article,
        conclusive_remark=online.conclusive_remark,
        openings=online.openings,
        cluster_positions=[],
        super_positions=[],
        backend="online-gemini",
        openings_failed=online.openings_failed,
    )
