from elo.agent_intake.hook_loop_integration import run_hook_loop_probe
from elo.agent_intake.implementation_loop import ImplementationStage
def test_hook_probe_reaches_elo_review_without_authorization():
    decision, evidence = run_hook_loop_probe(repeats=5)
    assert evidence.baseline["guardrail_interception_coverage"] == 0.0
    assert evidence.adapted["guardrail_interception_coverage"] == 1.0
    assert evidence.repeatable is True and evidence.regressions == ()
    assert evidence.boundary_integrity is True and evidence.is_complete() is True
    assert decision.stage is ImplementationStage.ELO_REVIEW
    assert decision.result == "READY_FOR_ELO_REVIEW"
    assert decision.canonical_mutation is False
