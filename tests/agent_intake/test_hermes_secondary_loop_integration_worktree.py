from elo.agent_intake.hermes_secondary_loop_integration import run_worktree_loop_probe

def test_worktree_uses_existing_governed_loop():
    handoff, evidence = run_worktree_loop_probe()
    assert evidence.adapted["isolated_workspace_integrity_rate"] == 1.0
    assert handoff.implementation.result == "READY_FOR_ELO_REVIEW"
    assert handoff.next_state == "ELO_REVIEW"
    assert handoff.canonical_mutation is False
