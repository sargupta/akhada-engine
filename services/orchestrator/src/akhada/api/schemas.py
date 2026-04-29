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


class DebateResponse(BaseModel):
    debate_id: str
    topic: str
    article: str
    conclusive_remark: str
    persona_library_version: str
    weights_version: str
    n_personas: int
    minority_voice_fraction: float = 0.0  # populated V1
    cost_usd: float = 0.0  # populated V1
    latency_ms: int = 0  # populated V1


class HealthResponse(BaseModel):
    status: Literal["ok"] = "ok"
    version: str
