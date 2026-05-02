"""Open Library book-authenticity validator.

For every CulturalInfluence with kind=="book" in the persona library,
look up Open Library's search endpoint and check whether a record exists
that plausibly matches the claimed title + creator. Returns a structured
ValidationReport.

Open Library has a soft rate limit; we respect it via a semaphore (4
concurrent requests) and a small per-request timeout.

V1 extends this to:
- Wikidata SPARQL for films / TV serials / songs / historical events
- Per-language filters (currently we accept any language in the result set)
- Quarterly bias-audit pass that compares verified-book distribution
  against published readership surveys (Nielsen India BookScan,
  Pratham ASER reading-habit data) per plan §5.7
"""
from __future__ import annotations

import asyncio
import logging
import re
from collections.abc import Sequence
from dataclasses import dataclass, field

import httpx

from akhada.persona_registry.schema import CulturalInfluence, Persona

log = logging.getLogger("akhada.validation.book_authenticity")

OPEN_LIBRARY_SEARCH = "https://openlibrary.org/search.json"
_TIMEOUT_S = 8.0
_MAX_CONCURRENCY = 4

# Books we accept without an Open Library record (often missing for
# regional / oral / sacred texts because OL coverage is uneven for India).
_KNOWN_INDIAN_TEXTS = {
    "ramcharitmanas",
    "bhagavad gita",
    "bhagavadgita",
    "guru granth sahib",
    "quran",
    "qur'an",
    "bible",
    "new revised standard bible",
    "new revised standard version bible",
    "ramayan",
    "mahabharat",
    "mahabharata",
    "ramayana",
    "tirukkural",
    "thirukkural",
    "gitanjali",
    "godan",
    "samskara",
    "devi mahatmya",
    "jagannatha dasa's odia bhāgabata",
    "jagannatha dasa's odia bhagabata",
    "odia bhagabata",
    "bhagabata",
}


def _norm(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[‘’“”]", "'", s)
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"[^\w\s']", "", s)
    return s.strip()


def _is_known_indian_text(title: str) -> bool:
    n = _norm(title)
    return any(known in n or n in known for known in _KNOWN_INDIAN_TEXTS)


@dataclass
class BookCheck:
    persona_id: str
    title: str
    creator: str | None
    verified: bool
    reason: str  # "ol-match" | "known-indian-text" | "no-match" | "timeout"
    matched_title: str | None = None


@dataclass
class ValidationReport:
    persona_count: int
    book_count: int
    book_verified: int
    book_known_indian: int
    book_unverified: int
    checks: list[BookCheck] = field(default_factory=list)

    @property
    def book_verified_fraction(self) -> float:
        return (self.book_verified + self.book_known_indian) / self.book_count if self.book_count else 1.0

    @property
    def book_unverified_fraction(self) -> float:
        return self.book_unverified / self.book_count if self.book_count else 0.0

    def summary(self) -> str:
        lines = [
            "=== Book authenticity report ===",
            f"  personas         : {self.persona_count}",
            f"  total books      : {self.book_count}",
            f"  Open-Library hit : {self.book_verified}",
            f"  Indian sacred    : {self.book_known_indian} (allow-listed; OL coverage gap)",
            f"  unverified       : {self.book_unverified}",
            f"  verified fraction: {self.book_verified_fraction:.2%}",
        ]
        if self.book_unverified > 0:
            lines.append("")
            lines.append("  Unverified books:")
            for c in self.checks:
                if not c.verified and c.reason in ("no-match", "timeout"):
                    lines.append(f"    [{c.persona_id}] {c.title!r} by {c.creator!r}  ({c.reason})")
        return "\n".join(lines)


async def _check_one(
    client: httpx.AsyncClient,
    persona_id: str,
    inf: CulturalInfluence,
    sem: asyncio.Semaphore,
) -> BookCheck:
    if _is_known_indian_text(inf.title):
        return BookCheck(persona_id, inf.title, inf.creator, True, "known-indian-text")

    params: dict[str, object] = {"title": inf.title, "limit": 5}
    if inf.creator:
        params["author"] = inf.creator

    async with sem:
        try:
            r = await client.get(OPEN_LIBRARY_SEARCH, params=params, timeout=_TIMEOUT_S)
            r.raise_for_status()
            data = r.json()
        except (httpx.HTTPError, ValueError) as exc:
            log.debug("OL lookup failed for %r: %s", inf.title, exc)
            return BookCheck(persona_id, inf.title, inf.creator, False, "timeout")

    docs = data.get("docs", []) or []
    target_title = _norm(inf.title)

    for d in docs:
        ol_title = _norm(str(d.get("title", "")))
        if not ol_title:
            continue
        if (
            target_title == ol_title
            or target_title in ol_title
            or ol_title in target_title
            or _token_overlap(target_title, ol_title) >= 0.6
        ):
            return BookCheck(
                persona_id, inf.title, inf.creator, True, "ol-match",
                matched_title=str(d.get("title")),
            )

    return BookCheck(persona_id, inf.title, inf.creator, False, "no-match")


def _token_overlap(a: str, b: str) -> float:
    ta, tb = set(a.split()), set(b.split())
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / max(len(ta), len(tb))


async def verify_library(personas: Sequence[Persona]) -> ValidationReport:
    sem = asyncio.Semaphore(_MAX_CONCURRENCY)
    tasks: list[asyncio.Task[BookCheck]] = []

    async with httpx.AsyncClient(headers={"User-Agent": "akhada-engine/0.0.1"}) as client:
        for p in personas:
            for inf in p.biography.cultural_influences:
                if inf.kind != "book":
                    continue
                tasks.append(asyncio.create_task(_check_one(client, p.id, inf, sem)))
        checks = await asyncio.gather(*tasks)

    verified = sum(1 for c in checks if c.verified and c.reason == "ol-match")
    known = sum(1 for c in checks if c.verified and c.reason == "known-indian-text")
    unverified = sum(1 for c in checks if not c.verified)

    return ValidationReport(
        persona_count=len(personas),
        book_count=len(checks),
        book_verified=verified,
        book_known_indian=known,
        book_unverified=unverified,
        checks=list(checks),
    )
