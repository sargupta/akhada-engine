"""FastAPI app entrypoint."""
from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from akhada import __version__
from akhada.api.routes import router
from akhada.telemetry.otel import init_logging

log = init_logging()


@asynccontextmanager
async def _lifespan(_app: FastAPI) -> AsyncIterator[None]:
    log.info("akhada-orchestrator starting; version=%s", __version__)
    yield
    log.info("akhada-orchestrator stopping")


app = FastAPI(
    title="Akhada Orchestrator",
    description="Open Debate Engine — 500+ AI agents on Indian demographics",
    version=__version__,
    lifespan=_lifespan,
)

# V0 dev: allow any localhost port (Next.js may auto-pick when 3000 is taken).
# V1 prod: lock to studio.akhada.in / akhada.in only.
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?",
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
