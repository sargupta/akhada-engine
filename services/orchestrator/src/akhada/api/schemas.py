"""Request / response schemas for the public API."""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class DebateRequest(BaseModel):
    topic: str = Field(min_length=4, max_length=4000)
    language: str = "en-IN"
    n_agents: int = Field(default=50, ge=5, le=2000)
    cluster_size: int = Field(default=20, ge=2, le=100)
    rounds: int = Field(default=3, ge=1, le=5)
    mode: Literal["research", "publication"] = "research"
    persona_library_version: str = "personas:2026.Q2.0"
    weights_version: str = "weights:v0.0.0"


class PanelArchetype(BaseModel):
    """One distinct persona archetype present in the panel."""
    persona_id: str
    label: str  # e.g. "55-64 male, marginal farmer, rural Bihar"
    state: str
    religion: str
    age_band: str
    education: str
    primary_language: str
    literacy: str
    count: int  # how many copies of this archetype the panel contains


class DebateResponse(BaseModel):
    debate_id: str
    topic: str
    article: str
    conclusive_remark: str
    persona_library_version: str
    weights_version: str
    n_personas: int
    panel_archetypes: list[PanelArchetype] = Field(default_factory=list)
    minority_voice_fraction: float = 0.0  # populated V1
    cost_usd: float = 0.0  # populated V1
    latency_ms: int = 0  # populated V1


class HealthResponse(BaseModel):
    status: Literal["ok"] = "ok"
    version: str
