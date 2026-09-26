from src.elo.agent_intake.hermes_functional_value_proof import CURRENT_EVIDENCE, functional_candidates

def test_candidate_attributed_functional_gains_are_selected():
    assert [item.candidate_id for item in functional_candidates()] == [
        "EXT-CONTEXT-PLUGIN-HERMES", "EXT-HOOK-HERMES"
    ]

def test_checkpoint_is_not_misattributed_to_hermes_candidate():
    item = next(x for x in CURRENT_EVIDENCE if x.candidate_id == "EXT-CHECKPOINT-HERMES")
    assert item.level == "IMPLEMENTATION_BOUNDARY"
    assert item.attribution == "OWNER_ATTRIBUTED"
    assert not item.functional_gain_proven

def test_contract_gain_does_not_become_functional_gain():
    item = next(x for x in CURRENT_EVIDENCE if x.candidate_id == "EXT-PROMPT-CACHE-HERMES")
    assert item.level == "CONTRACT_ONLY"
    assert not item.functional_gain_proven

def test_no_incremental_gain_candidates_are_not_promoted_by_fixture_integrity():
    for candidate_id in ("EXT-LEARNING-GRAPH-HERMES", "EXT-CONTEXTREF-HERMES"):
        item = next(x for x in CURRENT_EVIDENCE if x.candidate_id == candidate_id)
        assert item.gain == 0.0
        assert not item.functional_gain_proven

def test_candidate_evidence_requires_metric_scope_and_provenance():
    item = next(x for x in CURRENT_EVIDENCE if x.candidate_id == "EXT-HOOK-HERMES")
    assert item.metric and item.proof_scope and item.provenance_refs
