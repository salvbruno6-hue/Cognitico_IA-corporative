from src.elo.agent_intake.hermes_profile_evaluation import evaluate
def test_profile_evaluation_is_deterministic_and_bounded():
 r=evaluate();assert r.baseline_rate==1.0 and r.adapted_rate==1.0 and r.boundary_integrity_rate==1.0 and r.repeatable is True and r.result=="RETEST"
