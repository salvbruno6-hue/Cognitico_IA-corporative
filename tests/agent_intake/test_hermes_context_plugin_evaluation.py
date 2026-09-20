from elo.agent_intake.hermes_context_plugin_evaluation import evaluate_context_plugin_candidate

def test_context_plugin_controlled_evaluation_is_repeatable_without_claiming_gain():
    result = evaluate_context_plugin_candidate()
    assert result.candidate_id == "EXT-CONTEXT-PLUGIN-HERMES"
    assert result.baseline_success_rate == 1.0
    assert result.adapted_success_rate == 1.0
    assert result.boundary_integrity_rate == 1.0
    assert result.repeatable is True
    assert result.result == "RETEST"
