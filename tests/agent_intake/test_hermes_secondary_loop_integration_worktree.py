from elo.agent_intake.hermes_secondary_loop_integration import run_worktree_loop_probe

def test_worktree_uses_existing_governed_loop():
    handoff, evidence = run_worktree_loop_probe()
    assert evidence.adapted["collision_free_task_rate"] == 1.0
    assert handoff.result == "RETEST"
    assert handoff.result == "RETEST"
    assert handoff.canonical_mutation is False
