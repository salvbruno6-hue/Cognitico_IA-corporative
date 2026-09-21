from elo.agent_intake.hermes_mcp_evaluation import evaluate
from elo.agent_intake.hermes_secondary_loop_integration import run_mcp_loop_probe


def test_mcp_evaluation_is_repeatable_candidate_only():
    result = evaluate()
    assert result.baseline_rate == 1.0
    assert result.adapted_rate == 1.0
    assert result.boundary_integrity_rate == 1.0
    assert result.repeatable is True
    assert result.result == "RETEST"


def test_mcp_governed_loop_handoff_preserves_boundary():
    handoff = run_mcp_loop_probe()
    implementation = handoff.implementation
    evidence = handoff.loop_evidence
    assert implementation.result == "RETEST"
    assert implementation.canonical_mutation is False
    assert evidence.candidate_id == "EXT-MCP-HERMES"
    assert evidence.boundary_integrity is True
    assert evidence.provenance_refs
