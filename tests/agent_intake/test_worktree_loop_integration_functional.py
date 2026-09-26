from elo.agent_intake.hermes_secondary_loop_integration import run_worktree_loop_probe

def test_worktree_loop_remains_bounded_before_structured_functional_evidence():
    decision, _ = run_worktree_loop_probe()
    assert decision.result == "RETEST"
