from src.elo.agent_intake.hermes_memory_provider_evaluation import evaluate
def test_memory_provider_evaluation_is_deterministic_and_bounded():
    r=evaluate(); assert r.baseline_rate==1.0 and r.adapted_rate==1.0 and r.boundary_integrity_rate==1.0 and r.repeatable is True and r.result=="RETEST"
