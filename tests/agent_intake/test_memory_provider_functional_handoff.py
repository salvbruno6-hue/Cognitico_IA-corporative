from elo.agent_intake.hermes_secondary_loop_integration import run_memory_provider_loop_probe

def test_memory_provider_functional_gain_reaches_governed_review():
    decision, evidence = run_memory_provider_loop_probe()
    assert evidence.adapted["provider_identity_preservation_rate"] == 1.0
    assert decision.result == "READY_FOR_ELO_REVIEW"
    assert decision.canonical_mutation is False
