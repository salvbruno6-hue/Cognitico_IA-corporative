from elo.agent_intake.hermes_20260927_surface_candidates import CURRENT_SURFACE_CANDIDATES, validate_surface_candidate

def test_current_surface_candidates():
    ids = [x.candidate_id for x in CURRENT_SURFACE_CANDIDATES]
    assert len(ids) == 3
    assert len(ids) == len(set(ids))
    for item in CURRENT_SURFACE_CANDIDATES:
        ok, issues = validate_surface_candidate(item)
        assert ok, issues
        assert item.native_name.startswith("elo_")
