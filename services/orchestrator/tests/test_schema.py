"""Validates the Persona / Biography Pydantic schema enforces
the v3-onwards rules (top_5_books exactly 5; mbti / version / id format)."""
from __future__ import annotations

from datetime import date

import pytest
from pydantic import ValidationError

from akhada.persona_registry.schema import (
    Biography,
    CulturalInfluence,
    LifeEra,
    Persona,
)


def _book(title: str) -> CulturalInfluence:
    return CulturalInfluence(
        kind="book", title=title, language="en-IN", why_it_mattered="…",
    )


def _bio(books: list[CulturalInfluence]) -> Biography:
    return Biography(
        narrative_summary="I am a stub persona used in tests for the schema.",
        eras=[LifeEra(name="era", age_range=(0, 30), place="x", description="y")],
        formative_experiences=[],
        cultural_influences=books,
        top_5_books=books,
    )


def test_top_5_books_must_be_exactly_5() -> None:
    with pytest.raises(ValidationError):
        _bio([_book(f"b{i}") for i in range(4)])
    with pytest.raises(ValidationError):
        _bio([_book(f"b{i}") for i in range(6)])
    bio = _bio([_book(f"b{i}") for i in range(5)])
    assert len(bio.top_5_books) == 5


def test_persona_id_pattern() -> None:
    from akhada.api.routes import _stub_persona

    p = _stub_persona(1)
    assert p.id.startswith("akh-p-")
    assert p.version.startswith("personas:")


def test_persona_immutable() -> None:
    from akhada.api.routes import _stub_persona

    p = _stub_persona(1)
    with pytest.raises(ValidationError):
        p.id = "changed"  # type: ignore[misc]


def test_invalid_mbti_rejected() -> None:
    from akhada.persona_registry.schema import Big5, Psych

    with pytest.raises(ValidationError):
        Psych(
            big5=Big5(openness=0.5, conscientiousness=0.5, extraversion=0.5,
                      agreeableness=0.5, neuroticism=0.5),
            mbti="ZZZZ",
        )


def test_age_range_invalid_rejected() -> None:
    with pytest.raises(ValidationError):
        LifeEra(name="x", age_range=(50, 30), place="y", description="z")
