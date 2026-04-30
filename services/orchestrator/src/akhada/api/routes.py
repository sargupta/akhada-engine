"""HTTP routes — V0.5. Draws from `persona_registry.fixtures` (5 hand-curated
diverse Indian personas) cycled to fill `n_agents`. V1 wires real ADK + SSE
+ Cloud Tasks fan-out + 5K-persona library.
"""
from __future__ import annotations

import uuid

from collections import Counter

from fastapi import APIRouter, HTTPException

from akhada.api.schemas import DebateRequest, DebateResponse, HealthResponse, PanelArchetype
from akhada.flows.debate import run_debate
from akhada.persona_registry.fixtures import get_panel
from akhada.persona_registry.schema import Persona


def _summarise_panel(panel: list[Persona]) -> list[PanelArchetype]:
    counts = Counter(p.id for p in panel)
    by_id: dict[str, Persona] = {p.id: p for p in panel}
    out: list[PanelArchetype] = []
    for pid, n in counts.most_common():
        p = by_id[pid]
        d = p.demographic
        out.append(
            PanelArchetype(
                persona_id=pid,
                label=f"{d.age_band} {d.gender}, {d.occupation}, {d.urban_rural} {d.state}",
                state=d.state,
                religion=d.religion,
                age_band=d.age_band,
                education=d.education,
                primary_language=p.language.primary,
                literacy=p.language.literacy,
                count=n,
            )
        )
    return out

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    from akhada import __version__

    return HealthResponse(status="ok", version=__version__)


@router.post("/v1/debates", response_model=DebateResponse)
def create_debate(req: DebateRequest) -> DebateResponse:
    """V0.5 — runs the synchronous Python debate pipeline against
    a panel cycled from the 5 hand-curated fixtures.

    V1 wires real persona registry (5K library) + ADK SequentialAgent
    + SSE stream + audit trail to BigQuery.
    """
    if req.mode == "publication":
        # ECI guard placeholder — V1 reads the election lookup table
        raise HTTPException(
            status_code=400,
            detail="publication mode requires gov-tier attestation; V0 supports research mode only",
        )

    panel = get_panel(req.n_agents)
    result = run_debate(req.topic, panel, cluster_size=req.cluster_size)

    return DebateResponse(
        debate_id=str(uuid.uuid4()),
        topic=result.topic,
        article=result.article,
        conclusive_remark=result.conclusive_remark,
        persona_library_version=req.persona_library_version,
        weights_version=req.weights_version,
        n_personas=len(panel),
        panel_archetypes=_summarise_panel(panel),
    )
