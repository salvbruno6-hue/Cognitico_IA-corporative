from src.elo.agent_intake.hermes_context_reference_evaluation import evaluate

def test_context_reference_evaluation_is_deterministic_and_bounded():
    r=evaluate()
    assert r.baseline_rate==1.0
    assert r.adapted_rate==1.0
    assert r.boundary_integrity_rate==1.0
    assert r.repeatable is True
    assert r.result=="RETEST"


def test_contextref_final_review_preserves_no_incremental_gain():
    result = evaluate()
    assert result.baseline_rate == 1.0
    assert result.adapted_rate == 1.0
    assert result.repeatable is True
    assert result.boundary_integrity_rate == 1.0
    assert result.result == "RETEST"
