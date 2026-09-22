from elo.agent_intake.hermes_current_extensions import build_candidate
from elo.agent_intake.symbiont_adaptation import refine_capability, refinement_is_eligible_for_test


REV = "hermes-v0.21.4@d337b73"


def test_skill_autoload_reuses_existing_skills_owner():
    candidate = build_candidate("EXT-SKILL-AUTOLOAD-HERMES")
    adaptation = refine_capability(
        "HERMES-SKILLS",
        {"controlled_test": True, "outcome": {"boundary": True}, "source_reference": REV},
    )
    assert candidate.owner == "ELO Skills"
    assert adaptation.existing_capacity == "ELO Skills"
    assert candidate.promotion_state == "candidate_only"
    assert candidate.canonical_mutation is False
    assert refinement_is_eligible_for_test(adaptation)


def test_session_search_bounds_reuses_existing_context_owner():
    candidate = build_candidate("EXT-SESSION-SEARCH-BOUNDS-HERMES")
    adaptation = refine_capability(
        "HERMES-CONTEXT",
        {"controlled_test": True, "outcome": {"boundary": True}, "source_reference": REV},
    )
    assert candidate.owner == "ELO Context"
    assert adaptation.existing_capacity == "ELO Context"
    assert candidate.promotion_state == "candidate_only"
    assert candidate.canonical_mutation is False
    assert refinement_is_eligible_for_test(adaptation)


def test_symbiont_candidates_do_not_create_new_capability_ids():
    assert build_candidate("EXT-SKILL-AUTOLOAD-HERMES").owner == "ELO Skills"
    assert build_candidate("EXT-SESSION-SEARCH-BOUNDS-HERMES").owner == "ELO Context"
