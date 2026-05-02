"""HTTP routes.

V0.5  — draws from fixtures, cycles to fill n_agents.
V0.7  — async dispatch online vs offline.
V0.9  — k-DPP sampling when panel < library.
V0.10 — persists every debate to SQLite + writes a hash-chained audit
        log; serves GET /v1/debates, /v1/debates/{id},
        /v1/debates/{id}/audit (plan §20.10).
"""
from __future__ import annotations

import uuid
from collections import Counter

from fastapi import APIRouter, HTTPException

from akhada.api.schemas import (
    AuditEventOut,
    DebateAuditResponse,
    DebateListItem,
    DebateRecord,
    DebateRequest,
    DebateResponse,
    HealthResponse,
    PanelArchetype,
)
from akhada.config import online_mode_ready
from akhada.flows.debate import run_debate_async
from akhada.persistence.audit import verify_chain
from akhada.persistence.store import (
    get_debate_async,
    get_events_async,
    list_debates_async,
    save_async,
)
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

    debate_id = str(uuid.uuid4())
    archetypes = _summarise_panel(panel)

    # Persist + write the V0.10 hash-chained audit log.
    await save_async(
        debate_id=debate_id,
        topic=result.topic,
        backend=result.backend,
        n_personas=len(panel),
        library_version=req.persona_library_version,
        weights_version=req.weights_version,
        article=result.article,
        conclusive_remark=result.conclusive_remark,
        panel_archetypes=[a.model_dump() for a in archetypes],
        openings_failed=result.openings_failed,
        audit_payloads=[
            (
                "topic_received",
                {
                    "topic": result.topic,
                    "n_personas": len(panel),
                    "library_version": req.persona_library_version,
                    "weights_version": req.weights_version,
                    "mode": req.mode,
                    "panel_persona_ids": [p.id for p in panel],
                },
            ),
            (
                "openings_complete",
                {
                    "openings_count": len(result.openings),
                    "openings_failed": result.openings_failed,
                    "backend": result.backend,
                },
            ),
            (
                "synthesis_complete",
                {
                    "article_chars": len(result.article),
                    "article_h2_count": result.article.count("\n## "),
                },
            ),
            (
                "conclusive_complete",
                {
                    "remark_chars": len(result.conclusive_remark),
                },
            ),
        ],
    )

    return DebateResponse(
        debate_id=debate_id,
        topic=result.topic,
        article=result.article,
        conclusive_remark=result.conclusive_remark,
        persona_library_version=req.persona_library_version,
        weights_version=req.weights_version,
        n_personas=len(panel),
        panel_archetypes=archetypes,
        backend=result.backend,
        openings_failed=result.openings_failed,
    )


@router.get("/v1/debates", response_model=list[DebateListItem])
async def list_debates_route(limit: int = 50) -> list[DebateListItem]:
    debates = await list_debates_async(limit=limit)
    return [
        DebateListItem(
            debate_id=d.id, topic=d.topic, backend=d.backend,
            n_personas=d.n_personas, created_at=d.created_at,
        )
        for d in debates
    ]


@router.get("/v1/debates/{debate_id}", response_model=DebateRecord)
async def get_debate_route(debate_id: str) -> DebateRecord:
    d = await get_debate_async(debate_id)
    if d is None:
        raise HTTPException(status_code=404, detail=f"debate {debate_id} not found")
    return DebateRecord(
        debate_id=d.id,
        topic=d.topic,
        backend=d.backend,
        n_personas=d.n_personas,
        library_version=d.library_version,
        weights_version=d.weights_version,
        article=d.article,
        conclusive_remark=d.conclusive_remark,
        panel_archetypes=[PanelArchetype(**a) for a in d.panel_archetypes],
        openings_failed=d.openings_failed,
        created_at=d.created_at,
    )


@router.get("/v1/debates/{debate_id}/audit", response_model=DebateAuditResponse)
async def get_debate_audit(debate_id: str) -> DebateAuditResponse:
    d = await get_debate_async(debate_id)
    if d is None:
        raise HTTPException(status_code=404, detail=f"debate {debate_id} not found")
    events = await get_events_async(debate_id)
    chain_valid, error = verify_chain(events)
    return DebateAuditResponse(
        debate_id=debate_id,
        topic=d.topic,
        chain_valid=chain_valid,
        chain_error=error,
        events=[
            AuditEventOut(
                event_id=e.event_id, seq=e.seq, event_type=e.event_type,
                prev_hash=e.prev_hash, payload_hash=e.payload_hash,
                payload=e.payload, ts=e.ts,
            )
            for e in events
        ],
    )


@router.get("/v1/runtime")
def runtime_status() -> dict[str, object]:
    """Reports whether the online runtime is ready, and why if not."""
    ready, reason = online_mode_ready()
    return {"online_ready": ready, "reason": reason}
