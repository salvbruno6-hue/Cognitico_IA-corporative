from src.elo.agent_intake.hermes_cron_evaluation import evaluate
def test_cron_controlled_evaluation_is_deterministic_and_bounded():
    r=evaluate(); assert r.baseline_rate==1.0 and r.adapted_rate==1.0 and r.boundary_integrity_rate==1.0 and r.repeatable is True and r.result=="RETEST"
