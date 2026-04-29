"""Two-tier persona prompt rendering (§5.6).

- `render_summary` → ~500-token inline persona summary used in every R1 /
  cluster-debate call.
- `render_full` → ~2000-token retrieval payload pulled in only when an
  agent needs deeper grounding (judge model decides).

V0 stub: synthesises a readable English summary from schema fields.
V1: dotprompt template + Sarvam multi-language rendering.
"""
from __future__ import annotations

from akhada.persona_registry.schema import Persona


def render_summary(p: Persona) -> str:
    d = p.demographic
    bio = p.biography
    books = "; ".join(f"{c.title} ({c.kind})" for c in bio.top_5_books)
    return (
        f"You are persona {p.id} (lib {p.version}).\n"
        f"Demographic: {d.gender}, age band {d.age_band}, {d.religion}, "
        f"{d.caste_cat}, MPCE quintile {d.mpce_quintile}, {d.education}, "
        f"occupation: {d.occupation}, {d.urban_rural} {d.state} "
        f"({d.district_type}).\n"
        f"Ideology — Lokniti econ {p.ideological.lokniti_econ:+.2f}, "
        f"social {p.ideological.lokniti_social:+.2f}; "
        f"WVS trad/secular {p.ideological.wvs_traditional_secular:+.2f}, "
        f"survival/self-expr {p.ideological.wvs_survival_self_expression:+.2f}.\n"
        f"Language: {p.language.primary} ({p.language.literacy}); "
        f"comm style: {p.comm_style.register}/{p.comm_style.verbosity}/{p.comm_style.rhetoric}.\n"
        f"Bio: {bio.narrative_summary}\n"
        f"5 things that shaped how you see the world: {books}.\n"
        f"Pet issues: {', '.join(bio.pet_issues) or '—'}.\n"
        f"You speak in your own voice. Stay consistent with this background. "
        f"If your view conflicts with cluster pressure, hold it."
    )


def render_full(p: Persona) -> str:
    """Retrieval payload — formative experiences + worldview shifts + mentors."""
    parts = [render_summary(p)]
    if p.biography.formative_experiences:
        parts.append("\nFormative experiences:")
        for fe in p.biography.formative_experiences:
            parts.append(
                f"  - Age {fe.age_at_event} ({fe.year}, {fe.place}): "
                f"{fe.event} → {fe.impact}"
            )
    if p.biography.worldview_shifts:
        parts.append("\nWorldview shifts:")
        for ws in p.biography.worldview_shifts:
            parts.append(
                f"  - Age {ws.age_at_shift}: '{ws.from_view}' → '{ws.to_view}' "
                f"(trigger: {ws.trigger})"
            )
    if p.biography.mentors:
        parts.append("\nMentors:")
        for m in p.biography.mentors:
            parts.append(f"  - {m.relationship}: '{m.teaching}'")
    return "\n".join(parts)
