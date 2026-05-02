"""Demographic seeds for the V0.8 generator pilot.

Ten seeds covering states, castes, religions, literacy levels NOT in the
five hand-curated fixtures. Each is a fully-specified Demographic plus a
short occupation string. The generator turns each into a full Persona by
calling Gemini Pro and validating the result against the Pydantic schema.

V1: this hand-list becomes a stratified Census-2011 sampler (state ×
district-type × age × religion × caste × MPCE × education) producing
5,000 seeds. V2: 50,000.
"""
from __future__ import annotations

from dataclasses import dataclass

from akhada.persona_registry.schema import Demographic


@dataclass(frozen=True)
class PersonaSeed:
    seed_id: str  # "akh-p-gen-001" etc.
    demographic: Demographic
    notes: str  # optional flavour note for the generator prompt


SEEDS: list[PersonaSeed] = [
    PersonaSeed(
        seed_id="akh-p-gen-001",
        demographic=Demographic(
            state="Uttar Pradesh", district_type="urban", age_band="25-34",
            gender="male", religion="muslim", caste_cat="other_minority",
            mpce_quintile=4, education="postgraduate",
            occupation="software engineer at a domestic IT services firm",
            urban_rural="urban",
        ),
        notes="Lucknow-raised; first-generation college; reads English + Urdu.",
    ),
    PersonaSeed(
        seed_id="akh-p-gen-002",
        demographic=Demographic(
            state="Tamil Nadu", district_type="urban", age_band="35-44",
            gender="female", religion="hindu", caste_cat="obc",
            mpce_quintile=2, education="secondary",
            occupation="garment-factory line operator",
            urban_rural="urban",
        ),
        notes="Chennai outskirts; union member; functional literate in Tamil.",
    ),
    PersonaSeed(
        seed_id="akh-p-gen-003",
        demographic=Demographic(
            state="West Bengal", district_type="urban", age_band="65-74",
            gender="male", religion="hindu", caste_cat="general",
            mpce_quintile=4, education="doctorate",
            occupation="retired economics professor (Presidency / Calcutta U.)",
            urban_rural="urban",
        ),
        notes="Kolkata Bhadralok; CPI(M)-leaning in youth, sceptical now.",
    ),
    PersonaSeed(
        seed_id="akh-p-gen-004",
        demographic=Demographic(
            state="Gujarat", district_type="urban", age_band="25-34",
            gender="female", religion="hindu", caste_cat="general",
            mpce_quintile=3, education="graduate",
            occupation="chartered-accountant junior at a mid-size firm",
            urban_rural="urban",
        ),
        notes="Ahmedabad Patel family; observant; reads Gujarati press.",
    ),
    PersonaSeed(
        seed_id="akh-p-gen-005",
        demographic=Demographic(
            state="Rajasthan", district_type="rural", age_band="45-54",
            gender="male", religion="hindu", caste_cat="general",
            mpce_quintile=3, education="primary",
            occupation="small landowner (~5 acres, mustard + bajra)",
            urban_rural="rural",
        ),
        notes="Jodhpur district; Rajput; functional literate in Hindi.",
    ),
    PersonaSeed(
        seed_id="akh-p-gen-006",
        demographic=Demographic(
            state="Assam", district_type="rural", age_band="25-34",
            gender="male", religion="christian", caste_cat="st",
            mpce_quintile=1, education="secondary",
            occupation="tea-garden labourer (permanent worker)",
            urban_rural="rural",
        ),
        notes="Upper Assam; Adivasi descent; bilingual Sadri + Asamiya.",
    ),
    PersonaSeed(
        seed_id="akh-p-gen-007",
        demographic=Demographic(
            state="Telangana", district_type="rural", age_band="35-44",
            gender="female", religion="hindu", caste_cat="sc",
            mpce_quintile=2, education="graduate",
            occupation="Anganwadi worker (ICDS)",
            urban_rural="rural",
        ),
        notes="Mahbubnagar district; first SC graduate in her family.",
    ),
    PersonaSeed(
        seed_id="akh-p-gen-008",
        demographic=Demographic(
            state="Odisha", district_type="rural", age_band="55-64",
            gender="male", religion="hindu", caste_cat="st",
            mpce_quintile=1, education="primary",
            occupation="marine fisherman (mechanised boat crew)",
            urban_rural="rural",
        ),
        notes="Ganjam coast; Kondh-adjacent ST; oral-tradition literate.",
    ),
    PersonaSeed(
        seed_id="akh-p-gen-009",
        demographic=Demographic(
            state="Delhi", district_type="urban", age_band="25-34",
            gender="female", religion="sikh", caste_cat="general",
            mpce_quintile=4, education="postgraduate",
            occupation="political journalist at an English-language daily",
            urban_rural="urban",
        ),
        notes="Trilokpuri family; first cohort post-1984 trauma.",
    ),
    PersonaSeed(
        seed_id="akh-p-gen-010",
        demographic=Demographic(
            state="Haryana", district_type="rural", age_band="45-54",
            gender="male", religion="hindu", caste_cat="obc",
            mpce_quintile=3, education="secondary",
            occupation="dairy farmer (mid-size, ~25 cattle)",
            urban_rural="rural",
        ),
        notes="Sonipat district; Yadav; Khap-aware but pragmatic.",
    ),
]
