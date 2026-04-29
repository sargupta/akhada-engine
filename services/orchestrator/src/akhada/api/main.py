"""FastAPI app entrypoint."""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from akhada import __version__
from akhada.api.routes import router
from akhada.telemetry.otel import init_logging

log = init_logging()

app = FastAPI(
    title="Akhada Orchestrator",
    description="Open Debate Engine — 500+ AI agents on Indian demographics",
    version=__version__,
)

# Studio runs on http://127.0.0.1:3000 in V0 dev.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.on_event("startup")
def _startup() -> None:
    log.info("akhada-orchestrator starting; version=%s", __version__)
