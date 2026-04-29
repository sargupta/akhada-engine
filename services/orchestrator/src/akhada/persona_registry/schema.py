"""Pydantic models for Persona + Biography (v5 schema).

Top-level: `Persona` aggregates a demographic / ideological / psych vector
with a rich `Biography` (eras, formative experiences, cultural influences
including the user-requested `top_5_books` category, mentors, worldview
shifts, vocabulary, aspirations, fears).

The `top_5_books` field stores `list[CulturalInfluence]` so that
non-literate personas can populate it with oral / audio / visual cultural
inputs (kirtan, Ramayan TV serial, JP speeches, AIR programmes) of equal
shaping force, without losing the "5 things that shaped how you see the
world" semantic.

Schema version is encoded in `Persona.version` (e.g. `personas:2026.Q3.1`).
Old debates pin a version for reproducibility.
"""
from __future__ import annotations

import re
from datetime import date
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

# ---------------------------------------------------------------------------
# Atomic enums / leaf types
# ---------------------------------------------------------------------------

DistrictType = Literal["urban", "peri_urban", "rural"]
AgeBand = Literal["18-24", "25-34", "35-44", "45-54", "55-64", "65-74", "75+"]
Gender = Literal["female", "male", "other", "prefer_not_to_say"]
Religion = Literal[
    "hindu", "muslim", "christian", "sikh", "buddhist", "jain",
    "zoroastrian", "tribal", "other", "none",
]
CasteCat = Literal["general", "obc", "sc", "st", "other_minority", "not_disclosed"]
Education = Literal[
    "none", "primary", "upper_primary", "secondary",
    "higher_secondary", "diploma", "graduate", "postgraduate", "doctorate",
]
MPCEQuintile = Literal[1, 2, 3, 4, 5]
LiteracyLevel = Literal["literate", "functional", "oral_only"]
Register = Literal["formal", "colloquial", "mixed"]
Verbosity = Literal["low", "medium", "high"]
Rhetoric = Literal["analytical", "anecdotal", "emotional", "aphoristic"]

CulturalInfluenceKind = Literal[
    "book", "film", "tv_serial", "religious_text",
    "speech", "song", "podcast", "newspaper",
    "kavi_sammelan", "kirtan_satsang", "khutba_sermon", "youtube_channel",
]

# Numeric bounds
UnitInterval = Annotated[float, Field(ge=0.0, le=1.0)]
SignedUnit = Annotated[float, Field(ge=-1.0, le=1.0)]

MBTI_RE = re.compile(r"^[EI][NS][TF][JP]$")


# ---------------------------------------------------------------------------
# Demographic / ideological / psych layers
# ---------------------------------------------------------------------------

class Demographic(BaseModel):
    state: str
    district_type: DistrictType
    age_band: AgeBand
    gender: Gender
    religion: Religion
    caste_cat: CasteCat
    mpce_quintile: MPCEQuintile
    education: Education
    occupation: str
    urban_rural: Literal["urban", "rural"]


class Ideological(BaseModel):
    """Lokniti + WVS axes; all in [-1, 1]."""
    lokniti_econ: SignedUnit
    lokniti_social: SignedUnit
    wvs_traditional_secular: SignedUnit
    wvs_survival_self_expression: SignedUnit


class Big5(BaseModel):
    openness: UnitInterval
    conscientiousness: UnitInterval
    extraversion: UnitInterval
    agreeableness: UnitInterval
    neuroticism: UnitInterval


class Psych(BaseModel):
    big5: Big5
    mbti: str

    @field_validator("mbti")
    @classmethod
    def _validate_mbti(cls, v: str) -> str:
        if not MBTI_RE.match(v):
            raise ValueError("mbti must match [EI][NS][TF][JP]")
        return v


class LanguageProfile(BaseModel):
    primary: str  # BCP-47 e.g. "hi-IN"
    literacy: LiteracyLevel
    scripts_known: list[str] = Field(default_factory=list)
    code_mix: list[str] = Field(default_factory=list)


class CommStyle(BaseModel):
    register: Register
    verbosity: Verbosity
    rhetoric: Rhetoric


class SourceAnchor(BaseModel):
    """Distribution-anchor receipt: which dataset row this persona is sampled against."""
    dataset: str
    row_hash: str
    weight: float


# ---------------------------------------------------------------------------
# Biographical layer
# ---------------------------------------------------------------------------

class FormativeExperience(BaseModel):
    """A pivotal life event tagged with its influence on belief."""
    id: str
    age_at_event: int = Field(ge=0, le=110)
    year: int = Field(ge=1900, le=2100)
    place: str
    event: str
    impact: str
    influence_axis: list[str] = Field(default_factory=list)


class LifeEra(BaseModel):
    name: str
    age_range: tuple[int, int]
    place: str
    description: str
    formative_event_ids: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def _check_age_range(self) -> "LifeEra":
        lo, hi = self.age_range
        if lo < 0 or hi > 120 or lo > hi:
            raise ValueError(f"invalid age_range {self.age_range}")
        return self


class CulturalInfluence(BaseModel):
    """A book / film / serial / song / sermon / kirtan that shaped this persona."""
    kind: CulturalInfluenceKind
    title: str
    creator: str | None = None
    language: str  # BCP-47
    year_encountered: int | None = None
    age_encountered: int | None = None
    why_it_mattered: str
    influence_axis: list[str] = Field(default_factory=list)


class Mentor(BaseModel):
    relationship: str  # e.g. "school principal", "elder uncle", "first boss"
    teaching: str
    influence_axis: list[str] = Field(default_factory=list)


class WorldviewShift(BaseModel):
    age_at_shift: int = Field(ge=0, le=120)
    from_view: str
    to_view: str
    trigger: str


class Biography(BaseModel):
    """Rich biographical layer that turns a demographic vector into a person."""

    narrative_summary: str = Field(min_length=80, max_length=2000)
    eras: list[LifeEra]
    formative_experiences: list[FormativeExperience]
    cultural_influences: list[CulturalInfluence]
    top_5_books: list[CulturalInfluence]
    mentors: list[Mentor] = Field(default_factory=list)
    historical_events_lived: list[str] = Field(default_factory=list)
    worldview_shifts: list[WorldviewShift] = Field(default_factory=list)
    pet_issues: list[str] = Field(default_factory=list)
    vocabulary_quirks: list[str] = Field(default_factory=list)
    aspirations: list[str] = Field(default_factory=list)
    fears: list[str] = Field(default_factory=list)

    @field_validator("top_5_books")
    @classmethod
    def _exactly_five(cls, v: list[CulturalInfluence]) -> list[CulturalInfluence]:
        if len(v) != 5:
            raise ValueError(
                "top_5_books must have exactly 5 entries (books for literate; "
                "oral / audio / visual cultural inputs of equal shaping force "
                "for functionally-literate or oral-only personas)"
            )
        return v


# ---------------------------------------------------------------------------
# Persona top-level
# ---------------------------------------------------------------------------

class Persona(BaseModel):
    """A synthetic, biographically-grounded persona for the debate engine."""
    model_config = ConfigDict(frozen=True, extra="forbid")

    id: str  # akh-p-000142
    version: str  # personas:2026.Q3.1
    source_anchor: SourceAnchor
    demographic: Demographic
    ideological: Ideological
    psych: Psych
    expertise: list[str] = Field(default_factory=list)
    language: LanguageProfile
    comm_style: CommStyle
    knowledge_cutoff: date
    embedding: list[float] | None = None  # 1536-d, JL-projected (§19.16)
    biography: Biography

    @field_validator("id")
    @classmethod
    def _id_pattern(cls, v: str) -> str:
        if not re.match(r"^akh-p-[a-z0-9-]+$", v):
            raise ValueError("Persona.id must look like akh-p-xxxxxx")
        return v

    @field_validator("version")
    @classmethod
    def _version_pattern(cls, v: str) -> str:
        if not re.match(r"^personas:\d{4}\.Q[1-4]\.\d+$", v):
            raise ValueError("Persona.version must look like personas:2026.Q3.1")
        return v
