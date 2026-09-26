from elo.agent_intake.hermes_current_mechanism_candidates import CANDIDATES, CandidateState, get_candidate, validate_candidate_contract

def test_new_hermes_mechanisms_are_candidate_only() -> None:
    expected = {"EXT-CODE-EXEC-HERMES", "EXT-API-HERMES", "EXT-ACP-HERMES", "EXT-PLUGIN-CATALOG-HERMES", "EXT-PROMPT-CACHE-HERMES"}
    assert expected == {candidate.candidate_id for candidate in CANDIDATES}
    assert all(candidate.state == CandidateState.CANDIDATE_ONLY and candidate.canonical_mutation is False for candidate in CANDIDATES)

def test_candidate_contract_is_complete_and_non_authoritative() -> None:
    assert all(validate_candidate_contract(candidate) for candidate in CANDIDATES)

def test_unknown_candidate_is_not_fabricated() -> None:
    try:
        get_candidate("EXT-NOT-REAL-HERMES")
    except KeyError:
        pass
    else:
        raise AssertionError("unknown Hermes candidate must not be fabricated")