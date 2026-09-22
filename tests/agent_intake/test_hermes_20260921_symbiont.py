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


def test_symbiont_loop_blocks_without_measured_gain():
    from elo.agent_intake.hermes_governed_loop import advance_to_implementation

    candidate = build_candidate("EXT-SKILL-AUTOLOAD-HERMES")
    adaptation = refine_capability(
        "HERMES-SKILLS",
        {"controlled_test": True, "outcome": {"boundary": True}, "source_reference": REV},
    )
    handoff = advance_to_implementation(
        candidate,
        adaptation,
        {"retrieval_misses": 10.0},
        {"retrieval_misses": 10.0},
        metric_directions={"retrieval_misses": "minimize"},
        repeatable=True,
        provenance_refs=(REV,),
    )
    assert handoff.next_state == "MEASURED_GAIN"
    assert handoff.implementation.result == "RETEST"
    assert handoff.canonical_mutation is False


def test_symbiont_loop_reaches_elo_review_only_after_repeatable_gain():
    from elo.agent_intake.hermes_governed_loop import advance_to_implementation

    candidate = build_candidate("EXT-SESSION-SEARCH-BOUNDS-HERMES")
    adaptation = refine_capability(
        "HERMES-CONTEXT",
        {"controlled_test": True, "outcome": {"boundary": True}, "source_reference": REV},
    )
    handoff = advance_to_implementation(
        candidate,
        adaptation,
        {"bounded_misses": 10.0},
        {"bounded_misses": 7.0},
        metric_directions={"bounded_misses": "minimize"},
        repeatable=True,
        provenance_refs=(REV,),
    )
    assert handoff.next_state == "ELO_REVIEW"
    assert handoff.implementation.result == "READY_FOR_ELO_REVIEW"
    assert handoff.implementation.canonical_mutation is False


def test_symbiont_loop_retests_when_gain_is_not_repeatable():
    from elo.agent_intake.hermes_governed_loop import advance_to_implementation

    candidate = build_candidate("EXT-SESSION-SEARCH-BOUNDS-HERMES")
    adaptation = refine_capability(
        "HERMES-CONTEXT",
        {"controlled_test": True, "outcome": {"boundary": True}, "source_reference": REV},
    )
    handoff = advance_to_implementation(
        candidate,
        adaptation,
        {"bounded_misses": 10.0},
        {"bounded_misses": 7.0},
        metric_directions={"bounded_misses": "minimize"},
        repeatable=False,
        provenance_refs=(REV,),
    )
    assert handoff.next_state == "CANDIDATE"
    assert handoff.implementation.result == "RETEST"
    assert "repeatability" in handoff.loop_readiness.missing
    assert handoff.canonical_mutation is False
