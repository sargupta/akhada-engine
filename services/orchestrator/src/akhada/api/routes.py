"""HTTP routes — V0.5. Draws from `persona_registry.fixtures` (5 hand-curated
diverse Indian personas) cycled to fill `n_agents`. V1 wires real ADK + SSE
+ Cloud Tasks fan-out + 5K-persona library.
"""
from __future__ import annotations

import uuid

from collections import Counter

from fastapi import APIRouter, HTTPException

from akhada.api.schemas import DebateRequest, DebateResponse, HealthResponse, PanelArchetype
from akhada.config import online_mode_ready
from akhada.flows.debate import run_debate_async
from akhada.persona_registry.fixtures import LIBRARY
from akhada.persona_registry.sampler import sample_panel
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
async def create_debate(req: DebateRequest) -> DebateResponse:
    """V0.7 — async dispatcher.

    Defaults to the offline stub. When AKHADA_OFFLINE=false AND
    GOOGLE_API_KEY is set, dispatches to runtime.online.run_real_debate
    which makes real Gemini Flash + Pro calls and produces a genuine
    article + conclusive remark.

    V1 swaps the online backend to real ADK SequentialAgent + ParallelAgent
    + SSE stream + audit trail.
    """
    if req.mode == "publication":
        # ECI guard placeholder — V1 reads the election lookup table
        raise HTTPException(
            status_code=400,
            detail="publication mode requires gov-tier attestation; V0 supports research mode only",
        )

    panel = sample_panel(LIBRARY, req.n_agents)
    result = await run_debate_async(req.topic, panel, cluster_size=req.cluster_size)

    return DebateResponse(
        debate_id=str(uuid.uuid4()),
        topic=result.topic,
        article=result.article,
        conclusive_remark=result.conclusive_remark,
        persona_library_version=req.persona_library_version,
        weights_version=req.weights_version,
        n_personas=len(panel),
        panel_archetypes=_summarise_panel(panel),
        backend=result.backend,
        openings_failed=result.openings_failed,
    )


@router.get("/v1/runtime")
def runtime_status() -> dict[str, object]:
    """Reports whether the online runtime is ready, and why if not."""
    ready, reason = online_mode_ready()
    return {"online_ready": ready, "reason": reason}
