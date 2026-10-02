"""Governed execution adapter for EXT-WORKTREE-HERMES.

This adapter does not create, delete, mutate, merge, or activate Git worktrees.
It only materializes the already verified Hermes worktree signal through the
canonical ExecutionBoundary as a bounded Forge workspace descriptor.
"""
from __future__ import annotations
from collections.abc import Mapping
from dataclasses import dataclass
from elo.core.execution_boundary import ExecutionAdapter, ExecutionOutcome, ExecutionRequest, execute_governed
from elo.agent_intake.hermes_worktree_adapter import WorktreeAdapter
from elo.agent_intake.hermes_worktree_boundary import WorktreeSignal

@dataclass(frozen=True)
class WorktreeExecutionResult:
    outcome: ExecutionOutcome
    adapted: bool
    worktree_id: str
    workspace_id: str | None
    merge_authority: bool
    canonical_authority: bool

class WorktreeExecutionAdapter(ExecutionAdapter):
    """Execute one authorized, already verified worktree observation."""
    def __init__(self, *, signal: WorktreeSignal) -> None:
        self.signal = signal
    def execute(self, request: ExecutionRequest) -> Mapping[str, str]:
        if request.action_id != "EXT-WORKTREE-HERMES":
            raise ValueError("unsupported_execution_action")
        if request.tenant_id != self.signal.tenant_scope:
            raise ValueError("worktree_tenant_scope_mismatch")
        workspace = WorktreeAdapter().adapt(self.signal)
        if workspace is None:
            raise ValueError("worktree_signal_not_adapted")
        return {
            "execution_entrypoint": "elo.forge.worktree.boundary",
            "worktree_adapted": "true",
            "worktree_id": workspace.worktree_id,
            "workspace_id": workspace.workspace_id,
            "worktree_isolated": str(workspace.isolated).lower(),
            "merge_authority": str(workspace.merge_authority).lower(),
            "canonical_authority": str(workspace.canonical_authority).lower(),
            "git_mutation": "false",
        }

def execute_worktree(request: ExecutionRequest, *, signal: WorktreeSignal) -> WorktreeExecutionResult:
    """Execute the candidate through the canonical governed execution boundary."""
    outcome = execute_governed(request, WorktreeExecutionAdapter(signal=signal))
    provenance = dict(outcome.provenance)
    return WorktreeExecutionResult(
        outcome=outcome,
        adapted=provenance.get("worktree_adapted") == "true",
        worktree_id=signal.worktree_id,
        workspace_id=provenance.get("workspace_id"),
        merge_authority=provenance.get("merge_authority") == "true",
        canonical_authority=provenance.get("canonical_authority") == "true",
    )

__all__ = ["WorktreeExecutionAdapter", "WorktreeExecutionResult", "execute_worktree"]
