"""Online runtime — real Gemini calls via google-genai.

V0.7 architecture: simple sequential pipeline that produces a real
debate end-to-end without ADK Runner ceremony, but using ADK-compatible
prompt structure so V1 swap to ADK ParallelAgent + SequentialAgent is
mechanical.

Flow:
  1. R1 openings — gather_openings fans out 50 Flash calls in parallel
     (asyncio.gather with a semaphore-bounded concurrency = 10 to stay
     under regional RPM limits).
  2. Synthesis — one Pro call composes the 7-section article.
  3. Conclusion — one Pro call writes the conclusive remark.

Concurrency is bounded; failed leaf calls fall back to the persona's
demographic line so synthesis still runs. Total expected cost (default
50 fixtures): ~$0.005 Flash + ~$0.005 Pro ≈ $0.01 / debate.
"""
from __future__ import annotations

import asyncio
import logging
from collections.abc import Sequence
from dataclasses import dataclass

from akhada.config import settings
from akhada.persona_registry.schema import Persona
from akhada.runtime.prompts import (
    conclusive_prompt,
    opening_prompt,
    synthesis_prompt,
)

log = logging.getLogger("akhada.runtime.online")

_MAX_CONCURRENCY = 10


@dataclass
class _Opening:
    persona_id: str
    text: str
    failed: bool = False


def _client() -> object:
    """Lazy google-genai client. Imports deferred so offline mode never
    pulls google.genai into the process."""
    from google import genai  # type: ignore[import-not-found]

    if not settings.google_api_key:
        raise RuntimeError("GOOGLE_API_KEY missing; cannot run online debate")
    return genai.Client(api_key=settings.google_api_key)


async def _generate(model: str, prompt: str) -> str:
    """One Gemini generate_content call, async wrapper around the sync SDK."""
    client = _client()

    def _call() -> str:
        res = client.models.generate_content(model=model, contents=prompt)  # type: ignore[attr-defined]
        return res.text or ""

    return await asyncio.to_thread(_call)


async def _one_opening(p: Persona, topic: str, sem: asyncio.Semaphore) -> _Opening:
    async with sem:
        try:
            text = await _generate(settings.gemini_model_flash, opening_prompt(p, topic))
            return _Opening(persona_id=p.id, text=text.strip())
        except Exception as exc:  # noqa: BLE001
            log.warning("R1 opening failed for %s: %s", p.id, exc)
            d = p.demographic
            fallback = (
                f"As a {d.age_band} {d.gender} {d.occupation} from "
                f"{d.urban_rural} {d.state}, my view on this topic is "
                "shaped by my own experience. (LLM call failed; recorded "
                "as a placeholder for the synthesis layer.)"
            )
            return _Opening(persona_id=p.id, text=fallback, failed=True)


async def gather_openings(panel: Sequence[Persona], topic: str) -> list[_Opening]:
    sem = asyncio.Semaphore(_MAX_CONCURRENCY)
    return await asyncio.gather(*[_one_opening(p, topic, sem) for p in panel])


async def synthesise_article(openings: Sequence[_Opening], topic: str) -> str:
    pairs = [(o.persona_id, o.text) for o in openings]
    return (await _generate(settings.gemini_model_pro, synthesis_prompt(pairs, topic))).strip()


async def conclude(article: str, topic: str) -> str:
    return (await _generate(settings.gemini_model_pro, conclusive_prompt(article, topic))).strip()


@dataclass
class OnlineResult:
    topic: str
    article: str
    conclusive_remark: str
    openings: list[str]
    openings_failed: int


async def run_real_debate(topic: str, panel: Sequence[Persona]) -> OnlineResult:
    log.info("online debate begins; topic=%r n=%d", topic, len(panel))
    openings = await gather_openings(panel, topic)
    failed = sum(1 for o in openings if o.failed)
    log.info("R1 done; %d/%d failed", failed, len(openings))

    article = await synthesise_article(openings, topic)
    remark = await conclude(article, topic)
    log.info("online debate ok; article=%d chars remark=%d chars", len(article), len(remark))

    # Render article with the topic as the leading H1 so the existing
    # frontend strip-leading-H1 step continues to work.
    article_with_topic = f"# {topic}\n\n{article}"

    return OnlineResult(
        topic=topic,
        article=article_with_topic,
        conclusive_remark=remark,
        openings=[o.text for o in openings],
        openings_failed=failed,
    )
