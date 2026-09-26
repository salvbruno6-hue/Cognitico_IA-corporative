from elo.agent_intake.hermes_secondary_loop_integration import run_cron_loop_probe

def test_cron_functional_gain_reaches_governed_review():
    decision, evidence = run_cron_loop_probe()
    assert evidence.adapted["idempotency_collision_free_rate"] == 1.0
    assert decision.result == "READY_FOR_ELO_REVIEW"
    assert decision.canonical_mutation is False
