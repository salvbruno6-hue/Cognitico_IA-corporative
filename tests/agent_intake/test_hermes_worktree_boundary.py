from src.elo.agent_intake.hermes_worktree_boundary import (
    WorktreeSignal, WorktreeDisposition, assess_worktree,
)

def _signal(**kw):
    base = dict(signal_id="wt-001", tenant_scope="multiteiner", worktree_id="wt/a",
                source_refs=("git:worktree:wt/a",), base_ref="main",
                isolated=True, provenance_verified=True)
    base.update(kw)
    return WorktreeSignal(**base)

def test_verified_isolated_clean_worktree_is_candidate_only():
    a = assess_worktree(_signal())
    assert a.disposition is WorktreeDisposition.CANDIDATE
    assert a.canonical_authority is False
    assert a.merge_permitted is False

def test_dirty_worktree_remains_observation():
    a = assess_worktree(_signal(dirty_state=True))
    assert a.disposition is WorktreeDisposition.OBSERVATION

def test_nonisolated_worktree_is_rejected():
    a = assess_worktree(_signal(isolated=False))
    assert a.disposition is WorktreeDisposition.REJECTED

def test_missing_provenance_is_rejected():
    a = assess_worktree(_signal(provenance_verified=False))
    assert a.disposition is WorktreeDisposition.REJECTED

def test_missing_identity_is_rejected():
    a = assess_worktree(_signal(worktree_id=""))
    assert a.disposition is WorktreeDisposition.REJECTED
