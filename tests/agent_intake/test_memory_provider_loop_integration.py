"""Integration tests for the EXT-MEMPROVIDER-HERMES governed loop probe."""

from src.elo.agent_intake.memory_provider_loop_integration import (
    run_memory_provider_loop_probe,
)


def test_memory_provider_candidate_enters_shared_governed_loop():
    decision, evidence = run_memory_provider_loop_probe()

    assert evidence.is_complete() is True
    assert decision.result == "RETEST"
    assert decision.canonical_mutation is False


def test_memory_provider_probe_preserves_memory_authority_boundary():
    decision, evidence = run_memory_provider_loop_probe()

    assert evidence.boundary_integrity is True
    assert decision.canonical_mutation is False
