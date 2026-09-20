"""Tests for the governed ELO implementation loop."""

from elo.agent_intake.hermes_current_extensions import build_candidate
from elo.agent_intake.implementation_loop import ImplementationStage, run_implementation_loop
from elo.agent_intake.symbiont_adaptation import refine_capability


def _adaptation(candidate_id: str):
    return refine_capability(
        candidate_id,
        {"controlled_test": True, "outcome": {"verified": True}},
    )


def test_loop_stops_for_repeatable_gain_before_review():
    candidate = build_candidate("EXT-CONTEXT-PLUGIN-HERMES")
    adaptation = _adaptation("HERMES-CONTEXT")
    decision = run_implementation_loop(
        candidate, adaptation, {"latency": 10.0}, {"latency": 10.0}, repeatable=True,
    )
    assert decision.stage is ImplementationStage.MEASURED_GAIN
    assert decision.result == "RETEST"
    assert decision.canonical_mutation is False


def test_loop_requires_explicit_elo_approval_after_positive_repeatable_gain():
    candidate = build_candidate("EXT-CONTEXT-PLUGIN-HERMES")
    adaptation = _adaptation("HERMES-CONTEXT")
    ready = run_implementation_loop(
        candidate, adaptation, {"coverage": 0.5}, {"coverage": 0.8}, repeatable=True,
    )
    assert ready.stage is ImplementationStage.ELO_REVIEW
    assert ready.result == "READY_FOR_ELO_REVIEW"
    assert ready.canonical_mutation is False

    authorized = run_implementation_loop(
        candidate, adaptation, {"coverage": 0.5}, {"coverage": 0.8},
        repeatable=True, elo_approved=True,
    )
    assert authorized.stage is ImplementationStage.IMPLEMENTATION_AUTHORIZED
    assert authorized.result == "IMPLEMENTATION_AUTHORIZED"
    assert authorized.canonical_mutation is False


def test_loop_rejects_regression():
    candidate = build_candidate("EXT-CONTEXT-PLUGIN-HERMES")
    adaptation = _adaptation("HERMES-CONTEXT")
    decision = run_implementation_loop(
        candidate, adaptation, {"coverage": 0.8}, {"coverage": 0.7},
        repeatable=True, regressions=("coverage",),
    )
    assert decision.result == "REJECT"
    assert decision.canonical_mutation is False
