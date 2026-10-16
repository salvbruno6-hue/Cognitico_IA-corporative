from elo.agent_intake.symbiont_adaptation import refine_capability, refinement_is_eligible_for_test


SKILL_CHANGE_ID = "EXT-SKILL-CHANGE-AWARENESS-HERMES"


def test_skill_change_awareness_uses_existing_owner_and_stays_candidate_only():
    evidence = {
        "controlled_test": True,
        "outcome": {"delta_detected": True, "repeatable": True},
        "source_reference": "controlled-eval:skill-inventory-delta/1",
    }
    first = refine_capability(SKILL_CHANGE_ID, evidence)
    second = refine_capability(SKILL_CHANGE_ID, evidence)

    assert first == second
    assert first.existing_capacity == "ELO Knowledge & Skills"
    assert first.mechanism == "deterministic skill inventory delta"
    assert first.evidence_quality == "controlled_verified"
    assert refinement_is_eligible_for_test(first) is True
    assert first.promotion_state == "candidate_only"
    assert first.canonical_mutation is False


def test_skill_change_awareness_without_successful_evidence_is_not_eligible():
    adaptation = refine_capability(SKILL_CHANGE_ID, {"controlled_test": True, "outcome": {"delta_detected": False}})
    assert adaptation.evidence_quality == "insufficient"
    assert refinement_is_eligible_for_test(adaptation) is False
    assert adaptation.canonical_mutation is False
