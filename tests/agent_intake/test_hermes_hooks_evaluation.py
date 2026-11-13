from src.elo.agent_intake.hermes_hooks_evaluation import evaluate

def test_hooks_controlled_evaluation_is_deterministic_and_bounded():
    r=evaluate()
    assert r.baseline_rate==1.0
    assert r.adapted_rate==1.0
    assert r.boundary_integrity_rate==1.0
    assert r.repeatable is True
    assert r.result=="RETEST"
