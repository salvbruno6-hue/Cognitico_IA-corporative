from elo.agent_intake.hermes_secondary_loop_integration import (
    run_independent_review_loop_probe,
)


def test_independent_review_refines_delegation_without_new_authority():
    decision, evidence = run_independent_review_loop_probe()

    assert decision.result == "RETEST"
    assert evidence.candidate_id == "EXT-MULTIAGENT-HERMES"
    assert evidence.baseline["independent_review_validation_rate"] == 1.0
    assert evidence.adapted["independent_review_validation_rate"] == 1.0
    assert evidence.boundary_integrity is True
    assert decision.canonical_mutation is False
