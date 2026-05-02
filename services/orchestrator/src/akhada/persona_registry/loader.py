"""JSONL persona-library serialisation + load.

V0.8 file format: one Persona-as-JSON per line in
`data/personas/personas-{version}.jsonl`. Each line is the result of
`Persona.model_dump_json()`.

V1: this becomes Parquet-on-GCS via Vertex Vector Search + Firestore
hot tier; loader becomes a vector-store reader.
"""
from __future__ import annotations

import json
from collections.abc import Iterable, Sequence
from pathlib import Path

from akhada.persona_registry.schema import Persona


def write_jsonl(personas: Sequence[Persona], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for p in personas:
            f.write(p.model_dump_json())
            f.write("\n")


def read_jsonl(path: Path) -> list[Persona]:
    out: list[Persona] = []
    with path.open("r", encoding="utf-8") as f:
        for raw in f:
            raw = raw.strip()
            if not raw:
                continue
            out.append(Persona.model_validate_json(raw))
    return out


def merge(*libraries: Iterable[Persona]) -> list[Persona]:
    """De-duplicate by Persona.id while preserving order."""
    seen: set[str] = set()
    out: list[Persona] = []
    for lib in libraries:
        for p in lib:
            if p.id in seen:
                continue
            seen.add(p.id)
            out.append(p)
    return out
