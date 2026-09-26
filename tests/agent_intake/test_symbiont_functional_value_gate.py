from elo.agent_intake.hermes_secondary_loop_integration import run_context_plugin_loop_probe, run_multiagent_loop_probe


def test_context_plugin_functional_gain_can_cross_governed_handoff():
    decision, _ = run_context_plugin_loop_probe()
    assert decision.result == "READY_FOR_ELO_REVIEW"


def test_contract_only_multiagent_gain_stops_before_elo_review():
    decision, _ = run_multiagent_loop_probe()
    assert decision.result == "READY_FOR_ELO_REVIEW"
    assert decision.result == "RETEST"
