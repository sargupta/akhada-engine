"""Smoke tests — validate the V0 scaffold imports cleanly and the stub
debate pipeline runs end-to-end."""
from __future__ import annotations

from fastapi.testclient import TestClient


def test_import_persona_schema() -> None:
    from akhada.persona_registry.schema import Persona  # noqa: F401


def test_health() -> None:
    from akhada.api.main import app

    client = TestClient(app)
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_debate_stub_runs() -> None:
    from akhada.api.main import app

    client = TestClient(app)
    r = client.post(
        "/v1/debates",
        json={"topic": "MSP for all crops", "n_agents": 5, "cluster_size": 5, "rounds": 1},
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["topic"] == "MSP for all crops"
    assert body["n_personas"] == 5
    assert "MSP for all crops" in body["article"]


def test_publication_mode_blocked_without_attestation() -> None:
    from akhada.api.main import app

    client = TestClient(app)
    r = client.post(
        "/v1/debates",
        json={"topic": "test", "n_agents": 5, "mode": "publication"},
    )
    assert r.status_code == 400
