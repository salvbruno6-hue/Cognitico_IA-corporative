from elo.core.execution_boundary import ExecutionRequest, ExecutionStatus
from elo.agent_intake.hermes_worktree_boundary import WorktreeSignal
from elo.agent_intake.hermes_worktree_execution_adapter import execute_worktree

def _signal(**changes):
    values = dict(signal_id="wt-exec-001", tenant_scope="multiteiner", worktree_id="wt/exec/1",
                  source_refs=("git:worktree:wt/exec/1",), base_ref="main", isolated=True,
                  provenance_verified=True)
    values.update(changes)
    return WorktreeSignal(**values)

def _request(**changes):
    values = dict(request_id="req-wt-001", tenant_id="multiteiner", principal_id="principal-1",
                  action_id="EXT-WORKTREE-HERMES", authorization_id="auth-001",
                  evidence_ids=("evidence-wt-001",), correlation_id="corr-wt-001")
    values.update(changes)
    return ExecutionRequest(**values)

def test_worktree_executes_through_canonical_boundary_without_git_mutation():
    result = execute_worktree(_request(), signal=_signal())
    assert result.outcome.status is ExecutionStatus.EXECUTED
    assert result.outcome.executed is True
    assert result.adapted is True
    assert result.workspace_id == "forge:multiteiner:wt/exec/1"
    assert result.merge_authority is False
    assert result.canonical_authority is False
    assert result.outcome.provenance["git_mutation"] == "false"

def test_worktree_execution_fails_closed_without_authorization():
    result = execute_worktree(_request(authorization_id=None), signal=_signal())
    assert result.outcome.status is ExecutionStatus.BLOCKED
    assert result.outcome.executed is False
    assert result.adapted is False

def test_worktree_execution_rejects_tenant_mismatch():
    result = execute_worktree(_request(tenant_id="other-tenant"), signal=_signal())
    assert result.outcome.status is ExecutionStatus.FAILED
    assert result.outcome.executed is False
    assert result.adapted is False

def test_worktree_execution_rejects_unverified_signal():
    result = execute_worktree(_request(), signal=_signal(provenance_verified=False))
    assert result.outcome.status is ExecutionStatus.FAILED
    assert result.outcome.executed is False
    assert result.adapted is False
