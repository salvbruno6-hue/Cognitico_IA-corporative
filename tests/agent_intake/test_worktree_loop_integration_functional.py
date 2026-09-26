from elo.agent_intake.hermes_secondary_loop_integration import run_worktree_loop_probe
from elo.agent_intake.implementation_loop import ImplementationStage

def test_worktree_loop_accepts_candidate_specific_functional_gain():
    decision, evidence = run_worktree_loop_probe()
    assert evidence.baseline["collision_free_task_rate"] == 0.0
    assert evidence.adapted["collision_free_task_rate"] == 1.0
    assert decision.stage is ImplementationStage.ELO_REVIEW
    assert decision.result == "READY_FOR_ELO_REVIEW"
    assert decision.canonical_mutation is False
