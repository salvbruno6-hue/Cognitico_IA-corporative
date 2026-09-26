from elo.agent_intake.hermes_secondary_loop_integration import run_multiagent_loop_probe

def test_multiagent_uses_bounded_adapter_and_governed_loop():
    handoff, evidence = run_multiagent_loop_probe()
    assert evidence.adapted["bounded_delegation_contract_integrity_rate"] == 1.0
    assert handoff.result == "RETEST"
    assert handoff.result == "RETEST"
    assert handoff.canonical_mutation is False
