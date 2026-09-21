"""Integration tests for the first governed implementation-loop candidate."""
from src.elo.agent_intake.checkpoint_loop_integration import (
    close_checkpoint_approved_candidate,
    run_checkpoint_loop_probe,
)
from src.elo.agent_intake.implementation_loop import ImplementationStage


def test_checkpoint_candidate_reaches_elo_review_without_canonical_mutation():
    evidence, decision = run_checkpoint_loop_probe(
        tenant_scope="tenant-a",
        repeats=5,
    )

    assert evidence.baseline["recovery_success"] == 0.0
    assert evidence.adapted["recovery_success"] == 1.0
    assert evidence.repeatable is True
    assert evidence.regressions == ()
    assert evidence.boundary_integrity is True
    assert evidence.is_complete() is True

    assert decision.stage is ImplementationStage.ELO_REVIEW
    assert decision.result == "READY_FOR_ELO_REVIEW"
    assert decision.canonical_mutation is False


def test_checkpoint_probe_never_authorizes_without_explicit_approval():
    _, decision = run_checkpoint_loop_probe(tenant_scope="tenant-a", repeats=3)
    assert decision.result == "READY_FOR_ELO_REVIEW"
    assert decision.canonical_mutation is False


def test_checkpoint_approved_candidate_closes_only_with_explicit_approval():
    evidence, handoff = close_checkpoint_approved_candidate(
        tenant_scope="tenant-approved",
        repeats=5,
        evolution_gate_approved=True,
        elo_implementation_approved=True,
    )

    assert evidence.is_complete() is True
    assert handoff.next_state == "IMPLEMENTATION_AUTHORIZED"
    assert handoff.implementation.result == "IMPLEMENTATION_AUTHORIZED"
    assert handoff.implementation.canonical_mutation is False


def test_checkpoint_approval_loop_remains_fail_closed_without_implementation_authorization():
    _, handoff = close_checkpoint_approved_candidate(
        tenant_scope="tenant-approved",
        repeats=5,
        evolution_gate_approved=True,
        elo_implementation_approved=False,
    )

    assert handoff.next_state == "ELO_REVIEW"
    assert handoff.implementation.result == "READY_FOR_ELO_REVIEW"
    assert handoff.implementation.canonical_mutation is False
