"""V0.8 — Pro-tier biography generator.

For each `PersonaSeed`, calls Gemini Pro with a structured-JSON prompt,
parses the response, and validates it against the Pydantic schema.
On validation failure, retries once with the validation error appended.

Cost target: ~$0.03 per persona (≈ 3000 output tokens × $10/M Pro). At
the 10-pilot scale: ~$0.30. At 50: ~$1.50.

V1 swaps the prompt for a dotprompt template + adds Open Library /
Wikidata book-authenticity validation gate.
"""
from __future__ import annotations

import asyncio
import hashlib
import json
import logging
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import date
from typing import Any

from pydantic import ValidationError

from akhada.config import settings
from akhada.persona_registry.biography.seeds import PersonaSeed
from akhada.persona_registry.schema import (
    Biography,
    CommStyle,
    Ideological,
    LanguageProfile,
    Persona,
    Psych,
    SourceAnchor,
)

log = logging.getLogger("akhada.biography.generator")

LIBRARY_VERSION = "personas:2026.Q2.1"
KNOWLEDGE_CUTOFF = date(2024, 12, 1)
DATASET_TAG = "V0.8Generated"

_MAX_CONCURRENCY = 4


def _build_prompt(seed: PersonaSeed) -> str:
    d = seed.demographic
    return f"""You are designing a synthetic Indian persona for a civic-deliberation research engine. Internally coherent. Stereotype-free. Real cultural references only.

DEMOGRAPHIC SEED (fixed; do not change):
- State: {d.state}
- District type: {d.district_type}
- Age band: {d.age_band}
- Gender: {d.gender}
- Religion: {d.religion}
- Caste category: {d.caste_cat}
- MPCE quintile: {d.mpce_quintile}
- Education: {d.education}
- Occupation: {d.occupation}
- Urban/rural: {d.urban_rural}

FLAVOUR HINT: {seed.notes}

OUTPUT REQUIREMENTS — return a single JSON object with these top-level keys:

  ideological: object with keys
    lokniti_econ, lokniti_social, wvs_traditional_secular,
    wvs_survival_self_expression — each a float in [-1.0, 1.0]
  psych: object with
    big5: {{ openness, conscientiousness, extraversion, agreeableness, neuroticism }} each float [0.0, 1.0]
    mbti: 4-letter string matching [EI][NS][TF][JP]
  expertise: array of 1-4 short tag strings
  language: {{
    primary: BCP-47 code (e.g. "hi-IN"),
    literacy: "literate" | "functional" | "oral_only",
    scripts_known: array of script tags (e.g. ["Deva","Latn"]),
    code_mix: array of language codes
  }}
  comm_style: {{
    formality: "formal" | "colloquial" | "mixed",
    verbosity: "low" | "medium" | "high",
    rhetoric: "analytical" | "anecdotal" | "emotional" | "aphoristic"
  }}
  biography: {{
    narrative_summary: string, 80-2000 chars, first-person, English,
    eras: array of 3-5 objects {{ name, age_range:[lo,hi], place, description, formative_event_ids:[str] }},
    formative_experiences: array of 3-5 objects {{ id (e.g. "fe-1"), age_at_event, year, place, event, impact, influence_axis:[str] }},
    cultural_influences: array of 6-12 objects {{ kind, title, creator?, language (BCP-47), year_encountered?, age_encountered?, why_it_mattered, influence_axis:[str] }},
    top_5_books: array of EXACTLY 5 cultural_influence objects (same shape),
    mentors: array of 1-3 objects {{ relationship, teaching, influence_axis:[str] }},
    historical_events_lived: array of 4-10 strings,
    worldview_shifts: array of 0-3 objects {{ age_at_shift, from_view, to_view, trigger }},
    pet_issues: array of 2-5 short strings,
    vocabulary_quirks: array of 1-3 short quoted phrases,
    aspirations: array of 1-3 short strings,
    fears: array of 1-3 short strings
  }}

`kind` enum (CulturalInfluence.kind):
  "book" | "film" | "tv_serial" | "religious_text" | "speech" | "song"
  | "podcast" | "newspaper" | "kavi_sammelan" | "kirtan_satsang"
  | "khutba_sermon" | "youtube_channel"

RULES (strict):
- Stay tightly consistent with the demographic seed.
- Every book / film / serial / song / speech you cite MUST be a real, verifiable work. No invented titles.
- Historical events must align plausibly with this persona's birth-year range.
- top_5_books for "literate" → 5 actual books in languages they read; for "functional" → 2-3 books + 2-3 widely-encountered texts (newspapers, religious texts read aloud, school textbooks); for "oral_only" → 5 cultural inputs of equivalent shaping force (TV serials, kirtan, kavi sammelan, AIR programmes, sermon series, mass speeches attended).
- Avoid caricature. Show specific quirks over generic archetypes.
- narrative_summary: first-person, 100-200 words.
- Do NOT invent a persona name; refer to self as "I".

Return ONLY the JSON object, with no preamble, no fenced code block, no commentary."""


def _row_hash(seed: PersonaSeed) -> str:
    s = f"{seed.seed_id}|{seed.demographic.model_dump_json()}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


def _strip_fence(text: str) -> str:
    """Some Gemini outputs come in ```json fences despite our instructions."""
    s = text.strip()
    if s.startswith("```"):
        s = s.split("\n", 1)[1] if "\n" in s else s
        if s.endswith("```"):
            s = s.rsplit("```", 1)[0]
    return s.strip()


def _build_persona(seed: PersonaSeed, payload: dict[str, Any]) -> Persona:
    """Map a generator payload + seed into a fully-typed Persona. Raises
    pydantic.ValidationError if the payload doesn't match the schema."""
    return Persona(
        id=seed.seed_id,
        version=LIBRARY_VERSION,
        source_anchor=SourceAnchor(
            dataset=DATASET_TAG, row_hash=_row_hash(seed), weight=1.0
        ),
        demographic=seed.demographic,
        ideological=Ideological(**payload["ideological"]),
        psych=Psych(**payload["psych"]),
        expertise=list(payload.get("expertise", [])),
        language=LanguageProfile(**payload["language"]),
        comm_style=CommStyle(**payload["comm_style"]),
        knowledge_cutoff=KNOWLEDGE_CUTOFF,
        biography=Biography(**payload["biography"]),
    )


@dataclass
class GenerationResult:
    seed_id: str
    persona: Persona | None
    error: str | None
    attempts: int


async def _generate_one(seed: PersonaSeed, sem: asyncio.Semaphore) -> GenerationResult:
    """One generator call with up to 1 retry on validation failure."""
    from google import genai  # type: ignore[import-not-found]
    from google.genai import types  # type: ignore[import-not-found]

    if not settings.google_api_key:
        return GenerationResult(seed.seed_id, None, "GOOGLE_API_KEY missing", 0)

    client = genai.Client(api_key=settings.google_api_key)

    async with sem:
        last_error: str | None = None
        for attempt in range(2):
            prompt = _build_prompt(seed)
            if last_error:
                prompt += (
                    f"\n\nThe previous attempt failed validation with this error:\n{last_error}\n"
                    "Fix it and return only the corrected JSON."
                )

            try:
                def _call() -> str:
                    res = client.models.generate_content(
                        model=settings.gemini_model_pro,
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            response_mime_type="application/json",
                            temperature=0.9,
                        ),
                    )
                    return res.text or ""

                raw = await asyncio.to_thread(_call)
            except Exception as exc:  # noqa: BLE001
                log.warning("[%s] Pro call failed (attempt %d): %s", seed.seed_id, attempt + 1, exc)
                last_error = f"Pro call failed: {exc}"
                continue

            try:
                payload = json.loads(_strip_fence(raw))
            except json.JSONDecodeError as exc:
                log.warning("[%s] JSON parse failed (attempt %d): %s", seed.seed_id, attempt + 1, exc)
                last_error = f"JSONDecodeError: {exc}; raw output started with: {raw[:300]!r}"
                continue

            try:
                persona = _build_persona(seed, payload)
            except ValidationError as exc:
                log.warning("[%s] Pydantic validation failed (attempt %d):\n%s",
                            seed.seed_id, attempt + 1, exc)
                last_error = f"Pydantic ValidationError:\n{exc}"
                continue
            except Exception as exc:  # noqa: BLE001
                log.warning("[%s] persona construction failed (attempt %d): %s",
                            seed.seed_id, attempt + 1, exc)
                last_error = f"construction error: {exc}"
                continue

            return GenerationResult(seed.seed_id, persona, None, attempt + 1)

        return GenerationResult(seed.seed_id, None, last_error, 2)


async def generate_library(seeds: Sequence[PersonaSeed]) -> list[GenerationResult]:
    sem = asyncio.Semaphore(_MAX_CONCURRENCY)
    log.info("generating %d personas (concurrency=%d, model=%s)",
             len(seeds), _MAX_CONCURRENCY, settings.gemini_model_pro)
    results = await asyncio.gather(*[_generate_one(s, sem) for s in seeds])
    ok = sum(1 for r in results if r.persona is not None)
    log.info("generation complete: %d/%d ok", ok, len(seeds))
    return list(results)
