# akhada-orchestrator

Python orchestrator: Google ADK debate flows + FastAPI API + Pydantic persona schema.

## V0 status

Skeleton only. Stubs for:
- `akhada.persona_registry.schema` — `Persona`, `Biography` Pydantic models (real)
- `akhada.persona_registry.sampler` — DPP sampler (stub: returns first N)
- `akhada.persona_registry.prompt_renderer` — 500-tok summary vs 2k full retrieval (stub)
- `akhada.agents.*` — ADK LlmAgent templates (stubs returning fixed strings)
- `akhada.flows.debate` — SequentialAgent root (stub)
- `akhada.synthesis.*` — extract/compose/conclude/citation_verify (stubs)
- `akhada.conformity.dissent_appendix` — deterministic dissent (stub)
- `akhada.eval.*` — diversity / conformity / bias_audit / biographical_authenticity (stubs)
- `akhada.api.main` — FastAPI app with /health, /v1/debates POST stub, /v1/debates/{id} GET stub
- `akhada.telemetry.otel` — stub structured logging

## Run

```bash
~/Library/Python/3.13/bin/poetry install
~/Library/Python/3.13/bin/poetry run uvicorn akhada.api.main:app --reload --port 8080
# in another shell:
~/Library/Python/3.13/bin/poetry run adk web
~/Library/Python/3.13/bin/poetry run pytest -q
```
