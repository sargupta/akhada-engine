"""Unit tests for the V0.9 k-DPP sampler.

We can't fully verify the negative-association property without a large
library, but we can check:
  - dpp_sample returns the right size
  - distinct personas (no duplicates)
  - falls back to cycle when n >= |library|
  - sample_panel still works against the 5-fixture default library
"""
from __future__ import annotations

from akhada.persona_registry.fixtures import _HAND_CURATED
from akhada.persona_registry.sampler import dpp_sample, sample_panel


def test_dpp_returns_requested_size_when_smaller_than_library() -> None:
    panel = dpp_sample(_HAND_CURATED, n=3, seed=0)
    assert len(panel) == 3
    assert len({p.id for p in panel}) == 3  # no duplicates


def test_dpp_returns_full_library_when_n_ge_size() -> None:
    panel = dpp_sample(_HAND_CURATED, n=10, seed=0)
    assert {p.id for p in panel} == {p.id for p in _HAND_CURATED}


def test_sample_panel_default_returns_correct_size() -> None:
    # Backward-compat path: library smaller than n → cycle.
    panel = sample_panel(_HAND_CURATED, n=12)
    assert len(panel) == 12
    # First 5 in order then cycles.
    assert [p.id for p in panel[:5]] == [p.id for p in _HAND_CURATED]


def test_dpp_deterministic_under_seed() -> None:
    a = dpp_sample(_HAND_CURATED, n=3, seed=42)
    b = dpp_sample(_HAND_CURATED, n=3, seed=42)
    assert [p.id for p in a] == [p.id for p in b]
