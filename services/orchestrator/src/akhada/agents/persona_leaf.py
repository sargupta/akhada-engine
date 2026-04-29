"""R1 persona-leaf agent template.

V0 stub — produces a deterministic placeholder utterance from the persona's
prompt summary. V1 wires `google.adk.agents.LlmAgent(model=Flash, ...)` with
the rendered persona prompt as system instruction and S²-MAD sparse-comm
callbacks.
"""
from __future__ import annotations

from akhada.persona_registry.schema import Persona


def open_statement(persona: Persona, topic: str) -> str:
    """Return persona's R1 opening (80-150 words). V0 stub."""
    return (
        f"[{persona.id}] On '{topic}': "
        f"From a {persona.demographic.age_band} {persona.demographic.gender} "
        f"{persona.demographic.occupation} in "
        f"{persona.demographic.urban_rural} {persona.demographic.state}, "
        f"my view is shaped by my experience and the "
        f"{len(persona.biography.top_5_books)} formative inputs in my life."
    )
