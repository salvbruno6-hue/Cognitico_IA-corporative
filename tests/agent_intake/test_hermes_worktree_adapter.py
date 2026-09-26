from elo.agent_intake.hermes_worktree_adapter import adapt_worktree
from elo.agent_intake.hermes_worktree_boundary import WorktreeDisposition, WorktreeSignal, assess_worktree

def _signal(**changes):
    values = dict(signal_id="s-1", tenant_scope="multiteiner", worktree_id="wt/one",
                  source_refs=("git:worktree:one",), base_ref="main", isolated=True,
                  provenance_verified=True)
    values.update(changes)
    return WorktreeSignal(**values)

def test_verified_worktree_adapts_without_authority_transfer():
    workspace = adapt_worktree(_signal())
    assert workspace is not None
    assert workspace.workspace_id == "forge:multiteiner:wt/one"
    assert workspace.isolated is True
    assert workspace.merge_authority is False
    assert workspace.canonical_authority is False

def test_dirty_worktree_is_not_adapted():
    signal = _signal(dirty_state=True)
    assert assess_worktree(signal).disposition is WorktreeDisposition.OBSERVATION
    assert adapt_worktree(signal) is None

def test_unverified_worktree_is_not_adapted():
    assert adapt_worktree(_signal(provenance_verified=False)) is None
