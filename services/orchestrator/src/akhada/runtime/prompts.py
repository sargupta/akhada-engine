"""Prompt templates for online debate runs.

Kept in their own module so the V0 prompts are inspectable + version-able.
V1 these become dotprompt files with versioned hashes that flow into the
audit trail.
"""
from __future__ import annotations

from collections.abc import Sequence

from akhada.persona_registry.prompt_renderer import render_summary
from akhada.persona_registry.schema import Persona


def opening_prompt(p: Persona, topic: str) -> str:
    return (
        f"{render_summary(p)}\n\n"
        f"TOPIC: {topic}\n\n"
        "Give your opening statement on this topic in 80–150 words. "
        "First-person voice. Stay consistent with the background above. "
        "Do NOT pretend to be neutral — argue from your lived experience and "
        "your top-5 cultural inputs. If you have a minority view, state it "
        "plainly. Do not mention you are an AI."
    )


def synthesis_prompt(openings: Sequence[tuple[str, str]], topic: str) -> str:
    """openings: list of (persona_id, text)."""
    transcript = "\n\n---\n\n".join(f"[{pid}]\n{txt}" for pid, txt in openings)
    return (
        "You are an institutional policy analyst writing for a serious civic-"
        f"deliberation publication. Below are {len(openings)} opening "
        f'statements from a diverse Indian panel debating: "{topic}".\n\n'
        "Synthesise a structured article in clean Markdown with these EXACT "
        "seven sections, in this order:\n\n"
        "1. **Context & Framing** — restate the question, sub-questions, "
        "stakes (~100 words)\n"
        "2. **Perspectives by Cluster** — group similar statements; one "
        "paragraph per cluster (~80 words each); name the cluster by its "
        "core stance\n"
        "3. **Points of Agreement** — claims most personas converge on "
        "(~80 words)\n"
        "4. **Points of Contention** — steelman both sides (~120 words)\n"
        "5. **Evidence Map** — note where claims need evidence; mark "
        "`[unverified]` where the panel asserts without grounding\n"
        "6. **Recommendations / Decision Tree** — concrete next steps a "
        "policymaker could take (~100 words)\n"
        "7. **Minority Voices Appendix** — the 3 most distinctive minority "
        "statements, verbatim, with the persona id in square brackets\n\n"
        "Rules:\n"
        "- Use only what the openings say. Do not invent statistics, "
        "personas, or quotations.\n"
        "- Keep persona ids exactly as given (e.g. `[akh-p-fixture-002]`).\n"
        "- Do NOT include a top-level `# Heading` — sections start at H2.\n"
        "- Tone: institutional, restrained, NYT-policy-explainer.\n\n"
        f"OPENINGS:\n\n{transcript}"
    )


def conclusive_prompt(article: str, topic: str) -> str:
    return (
        f'Read this synthesised article on the topic "{topic}":\n\n'
        f"{article}\n\n"
        "Now write the CONCLUSIVE REMARK in 80–120 words. It must:\n"
        "- Cite the strongest *argument*, not the most popular *side*\n"
        "- Name the most important point of contention\n"
        "- Acknowledge what evidence is missing\n"
        "- End with one sentence the policymaker should act on\n\n"
        "Tone: serious institutional. One paragraph. No bullet points. No "
        "preface. Plain prose."
    )
