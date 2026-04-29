"""Stage B: claims → 7-section article. V0 stub."""
from __future__ import annotations

from collections.abc import Sequence

from akhada.synthesis.extract import Claim


def compose_article(claims: Sequence[Claim], topic: str) -> str:
    """V0 stub. V1 emits the 7 fixed sections (§7)."""
    return (
        f"# {topic}\n\n"
        f"## 1. Context & Framing — pending V1\n"
        f"## 2. Perspectives by Cluster — pending V1\n"
        f"## 3. Points of Agreement — {sum(1 for c in claims if c.contention_score < 0.2)} claims\n"
        f"## 4. Points of Contention — {sum(1 for c in claims if c.contention_score > 0.5)} claims\n"
        f"## 5. Evidence Map — pending V1\n"
        f"## 6. Recommendations / Decision Tree — pending V1\n"
        f"## 7. Minority Voices Appendix — pending V1\n"
    )
