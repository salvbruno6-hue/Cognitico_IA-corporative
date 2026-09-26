from elo.agent_intake.hermes_profile_evaluation import evaluate

def test_profile_three_phase_controlled_evaluation():
    r=evaluate()
    assert r.baseline_rate==0.0
    assert r.adapted_rate==1.0
    assert r.boundary_integrity_rate==1.0
    assert r.repeatable is True
    assert r.result=="EVOLUTION_GATE_REQUIRED"
