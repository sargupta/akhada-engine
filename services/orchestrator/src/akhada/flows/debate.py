"""Top-level debate flow.

V0: a synchronous Python pipeline that walks R0 → R1 → R2 → R3 stages and
returns a stub `DebateResult`.

V1 (per plan §6): rebuilds this as

    SequentialAgent(
        sub_agents=[
            framer,                              # R0
            ParallelAgent(persona_leaf x 500),   # R1 openings (5 nested ParallelAgent(100))
            ParallelAgent(cluster x 25),         # R1' cluster debate
            ParallelAgent(super_cluster x 5),    # R2
            LoopAgent(final, max_iters=2),       # R3 with conformity-check loop
        ]
    )

with state shared via `output_key`s on `session.state` keyed
`r1.persona_<id>.utterance` etc. (avoids race-condition writes per ADK
concurrency notes).
"""
from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from akhada.agents.cluster import cluster_rep_position
from akhada.agents.final import final_synthesis
from akhada.agents.persona_leaf import open_statement
from akhada.agents.super_cluster import super_cluster_synth
from akhada.persona_registry.schema import Persona


@dataclass
class DebateResult:
    topic: str
    article: str
    conclusive_remark: str
    openings: list[str]
    cluster_positions: list[str]
    super_positions: list[str]


def run_debate(topic: str, panel: Sequence[Persona], cluster_size: int = 20) -> DebateResult:
    """V0 synchronous pipeline. V1 → ADK SequentialAgent + ParallelAgent."""
    openings = [open_statement(p, topic) for p in panel]

    # cluster into groups of `cluster_size`
    clusters: list[list[Persona]] = [
        list(panel[i : i + cluster_size]) for i in range(0, len(panel), cluster_size)
    ]
    cluster_positions = [cluster_rep_position(c, topic) for c in clusters]

    # super-cluster: simple buckets of 5 cluster reps
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
