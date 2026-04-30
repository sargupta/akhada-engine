"""V0.5 fixtures sanity: 5 distinct personas, each with a real biography
that respects the schema; cycling fills any N."""
from __future__ import annotations

from akhada.persona_registry.fixtures import LIBRARY, get_panel


def test_library_has_five_personas() -> None:
    assert len(LIBRARY) == 5
    ids = {p.id for p in LIBRARY}
    assert len(ids) == 5  # all distinct


def test_state_diversity() -> None:
    states = {p.demographic.state for p in LIBRARY}
    # 5 personas, 5 states
    assert states == {"Karnataka", "Bihar", "Maharashtra", "Kerala", "Punjab"}


def test_religion_and_ideology_diversity() -> None:
    religions = {p.demographic.religion for p in LIBRARY}
    assert religions >= {"hindu", "christian", "sikh"}

    econ_axis = sorted(p.ideological.lokniti_econ for p in LIBRARY)
    # Spans both protectionist (Bihar farmer ~+0.5) and market-pro (founder ~-0.4)
    assert econ_axis[0] <= -0.3 and econ_axis[-1] >= 0.4


def test_literacy_spectrum_covered() -> None:
    levels = {p.language.literacy for p in LIBRARY}
    assert "literate" in levels
    assert "functional" in levels


def test_every_persona_has_five_top_books() -> None:
    for p in LIBRARY:
        assert len(p.biography.top_5_books) == 5
        # each top_5_books entry is a CulturalInfluence with non-empty title
        for c in p.biography.top_5_books:
            assert c.title.strip()


def test_top_5_books_kinds_vary_across_library() -> None:
    """Across the 5 personas, top_5_books should include kinds beyond 'book'
    — TV serials / religious texts / songs / films — proving the field
    handles non-literate / oral-tradition personas without losing meaning."""
    kinds: set[str] = set()
    for p in LIBRARY:
        for c in p.biography.top_5_books:
            kinds.add(c.kind)
    assert "book" in kinds
    assert kinds & {"religious_text", "tv_serial", "song", "film", "speech"}


def test_get_panel_cycles_to_fill_n() -> None:
    panel = get_panel(12)
    assert len(panel) == 12
    # First 5 are the library, then it cycles
    assert [p.id for p in panel[:5]] == [p.id for p in LIBRARY]
    assert panel[5].id == LIBRARY[0].id


def test_get_panel_smaller_than_library() -> None:
    panel = get_panel(3)
    assert len(panel) == 3
    assert [p.id for p in panel] == [p.id for p in LIBRARY[:3]]


def test_each_persona_has_lived_events_consistent_with_age() -> None:
    """Sanity: a 65-74 persona should have lived through more events than a 25-34."""
    veteran = next(p for p in LIBRARY if p.demographic.age_band == "65-74")
    founder = next(p for p in LIBRARY if p.demographic.age_band == "25-34")
    assert len(veteran.biography.historical_events_lived) > len(
        founder.biography.historical_events_lived
    )
