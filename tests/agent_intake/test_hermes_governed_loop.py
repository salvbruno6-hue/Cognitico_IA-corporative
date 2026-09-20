from elo.agent_intake.hermes_current_extensions import build_candidate
from elo.agent_intake.hermes_governed_loop import advance_to_implementation
from elo.agent_intake.symbiont_adaptation import refine_capability


def verified_adaptation():
    return refine_capability(
        "HERMES-CHECKPOINT",
        {"controlled_test": True, "outcome": {"boundary": True}, "source_reference": "hermes-checkpoint"},
    )


def test_incomplete_evidence_stops_before_elo_review():
    result = advance_to_implementation(
        build_candidate("EXT-CHECKPOINT-HERMES"), verified_adaptation(),
        {"latency": 10.0}, {"latency": 10.0},
        metric_directions={"latency": "minimize"}, repeatable=True,
        provenance_refs=("eval-001",),
    )
    assert result.next_state == "CANDIDATE"
    assert result.implementation.result == "RETEST"
    assert not result.implementation.canonical_mutation


def test_positive_repeatable_gain_reaches_elo_review_not_approval():
    result = advance_to_implementation(
        build_candidate("EXT-CHECKPOINT-HERMES"), verified_adaptation(),
        {"latency": 10.0}, {"latency": 8.0},
        metric_directions={"latency": "minimize"}, repeatable=True,
        provenance_refs=("eval-002", "eval-003"),
    )
    assert result.next_state == "ELO_REVIEW"
    assert result.implementation.result == "READY_FOR_ELO_REVIEW"


def test_explicit_elo_approval_reaches_implementation_authorized_only():
    result = advance_to_implementation(
        build_candidate("EXT-CHECKPOINT-HERMES"), verified_adaptation(),
        {"latency": 10.0}, {"latency": 8.0},
        metric_directions={"latency": "minimize"}, repeatable=True,
        provenance_refs=("eval-004", "eval-005"), elo_approved=True,
    )
    assert result.next_state == "IMPLEMENTATION_AUTHORIZED"
    assert result.implementation.result == "IMPLEMENTATION_AUTHORIZED"
    assert not result.implementation.canonical_mutation
