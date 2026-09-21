from elo.agent_intake.hermes_secondary_loop_integration import (
    run_context_plugin_loop_probe,
    run_multiagent_loop_probe,
)


def test_multiagent_uses_shared_governed_mediator_without_gain():
    decision, evidence = run_multiagent_loop_probe()
    assert decision.result == "RETEST"
    assert evidence.candidate_id == "EXT-MULTIAGENT-HERMES"
    assert evidence.boundary_integrity is True
    assert decision.canonical_mutation is False


def test_context_plugin_uses_shared_governed_mediator_without_gain():
    decision, evidence = run_context_plugin_loop_probe()
    assert decision.result == "RETEST"
    assert evidence.candidate_id == "EXT-CONTEXT-PLUGIN-HERMES"
    assert evidence.boundary_integrity is True
    assert decision.canonical_mutation is False
