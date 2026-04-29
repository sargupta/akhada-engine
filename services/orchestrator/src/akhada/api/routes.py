"""HTTP routes — V0 stub. V1 wires real ADK + SSE + Cloud Tasks fan-out."""
from __future__ import annotations

import uuid
from datetime import date

from fastapi import APIRouter, HTTPException

from akhada.api.schemas import DebateRequest, DebateResponse, HealthResponse
from akhada.flows.debate import run_debate
from akhada.persona_registry.schema import (
    Big5,
    Biography,
    CommStyle,
    CulturalInfluence,
    Demographic,
    FormativeExperience,
    Ideological,
    LanguageProfile,
    LifeEra,
    Mentor,
    Persona,
    Psych,
    SourceAnchor,
    WorldviewShift,
)

router = APIRouter()


def _stub_persona(i: int) -> Persona:
    """Single hand-curated stub persona for V0 demo."""
    return Persona(
        id=f"akh-p-stub-{i:04d}",
        version="personas:2026.Q2.0",
        source_anchor=SourceAnchor(dataset="V0Stub", row_hash=f"stub-{i}", weight=1.0),
        demographic=Demographic(
            state="Karnataka",
            district_type="urban",
            age_band="35-44",
            gender="female",
            religion="hindu",
            caste_cat="general",
            mpce_quintile=3,
            education="graduate",
            occupation="school teacher",
            urban_rural="urban",
        ),
        ideological=Ideological(
            lokniti_econ=-0.1,
            lokniti_social=0.2,
            wvs_traditional_secular=0.0,
            wvs_survival_self_expression=0.3,
        ),
        psych=Psych(
            big5=Big5(
                openness=0.7,
                conscientiousness=0.6,
                extraversion=0.5,
                agreeableness=0.6,
                neuroticism=0.4,
            ),
            mbti="INFJ",
        ),
        expertise=["primary_education", "child_development"],
        language=LanguageProfile(
            primary="kn-IN", literacy="literate", scripts_known=["Knda", "Latn"], code_mix=["en"]
        ),
        comm_style=CommStyle(formality="mixed", verbosity="medium", rhetoric="anecdotal"),
        knowledge_cutoff=date(2024, 12, 1),
        biography=Biography(
            narrative_summary=(
                "I grew up in a middle-class Brahmin family in Hubli, "
                "studied at a Kannada-medium school, and trained as a teacher. "
                "I have taught primary kids for fifteen years. The Right to "
                "Education Act felt personal — I saw both its promise and its "
                "rough edges in my own classroom."
            ),
            eras=[
                LifeEra(
                    name="Childhood in Hubli",
                    age_range=(0, 17),
                    place="Hubli, Karnataka",
                    description="Kannada-medium schooling; joint family",
                    formative_event_ids=["fe-001"],
                ),
            ],
            formative_experiences=[
                FormativeExperience(
                    id="fe-001",
                    age_at_event=12,
                    year=2002,
                    place="Hubli",
                    event="State school strike on teacher salaries",
                    impact="Realised state and unions can both fail kids",
                    influence_axis=["education_policy", "labor_skepticism"],
                ),
            ],
            cultural_influences=[
                CulturalInfluence(
                    kind="book", title="Tota-Chan", creator="Tetsuko Kuroyanagi",
                    language="en-IN", age_encountered=14,
                    why_it_mattered="Made me believe school can be joy",
                    influence_axis=["pedagogy"],
                ),
            ],
            top_5_books=[
                CulturalInfluence(
                    kind="book", title="Tota-Chan", creator="Tetsuko Kuroyanagi",
                    language="en-IN", age_encountered=14,
                    why_it_mattered="Made me believe school can be joy",
                    influence_axis=["pedagogy"],
                ),
                CulturalInfluence(
                    kind="book", title="Samskara", creator="U.R. Ananthamurthy",
                    language="kn-IN", age_encountered=22,
                    why_it_mattered="Taught me to question caste from the inside",
                    influence_axis=["caste_critique"],
                ),
                CulturalInfluence(
                    kind="book", title="The Argumentative Indian", creator="Amartya Sen",
                    language="en-IN", age_encountered=30,
                    why_it_mattered="Pluralism is older than the modern state",
                    influence_axis=["pluralism"],
                ),
                CulturalInfluence(
                    kind="religious_text", title="Bhagavad Gita",
                    language="sa-IN", age_encountered=18,
                    why_it_mattered="Duty over outcome — anchors my classroom",
                    influence_axis=["dharma", "stoicism"],
                ),
                CulturalInfluence(
                    kind="film", title="Taare Zameen Par", creator="Aamir Khan",
                    language="hi-IN", age_encountered=33,
                    why_it_mattered="Saw my own struggling students on screen",
                    influence_axis=["pedagogy", "neurodiversity"],
                ),
            ],
            mentors=[
                Mentor(
                    relationship="school principal",
                    teaching="Always ask the quietest child first",
                    influence_axis=["pedagogy"],
                ),
            ],
            historical_events_lived=[
                "1991 economic liberalisation",
                "2002 Karnataka school strike",
                "2009 Right to Education Act",
                "2020 COVID school closures",
            ],
            worldview_shifts=[
                WorldviewShift(
                    age_at_shift=33,
                    from_view="State should run everything",
                    to_view="State sets floor; community runs",
                    trigger="Watching my school fail under pure state control",
                ),
            ],
            pet_issues=["foundational literacy", "teacher pay", "child mental health"],
            vocabulary_quirks=["'I will tell you frankly,'"],
            aspirations=["see every child read by age 7"],
            fears=["another lockdown closing schools"],
        ),
    )


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    from akhada import __version__

    return HealthResponse(status="ok", version=__version__)


@router.post("/v1/debates", response_model=DebateResponse)
def create_debate(req: DebateRequest) -> DebateResponse:
    """V0 stub — runs the synchronous Python debate pipeline against
    a hand-curated single persona repeated `req.n_agents` times.

    V1 wires real persona registry + ADK SequentialAgent + SSE stream.
    """
    if req.mode == "publication":
        # ECI guard placeholder — V1 reads the election lookup table
        raise HTTPException(
            status_code=400,
            detail="publication mode requires gov-tier attestation; V0 supports research mode only",
        )

    panel = [_stub_persona(i) for i in range(req.n_agents)]
    result = run_debate(req.topic, panel, cluster_size=req.cluster_size)

    return DebateResponse(
        debate_id=str(uuid.uuid4()),
        topic=result.topic,
        article=result.article,
        conclusive_remark=result.conclusive_remark,
        persona_library_version=req.persona_library_version,
        weights_version=req.weights_version,
        n_personas=len(panel),
    )
