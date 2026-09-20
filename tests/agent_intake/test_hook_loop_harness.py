from elo.agent_intake.hook_loop_harness import evaluate_hook_loop_harness, to_candidate_measurement
def test_hook_harness_measures_repeatable_gain():
    m = evaluate_hook_loop_harness(repeats=5)
    assert m.baseline["guardrail_interception_coverage"] == 0.0
    assert m.adapted["guardrail_interception_coverage"] == 1.0
    assert m.metric_directions["guardrail_interception_coverage"] == "maximize"
    assert m.repeatable is True and m.regressions == ()
    assert to_candidate_measurement(m).result == "EVOLUTION_GATE_REQUIRED"
