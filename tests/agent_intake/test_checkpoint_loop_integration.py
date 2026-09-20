"""Integration tests for the first governed implementation-loop candidate."""
from src.elo.agent_intake.checkpoint_loop_integration import run_checkpoint_loop_probe
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
