"""Bounded in-memory adapter for EXT-WORKTREE-HERMES.

The adapter does not create, delete, merge, or activate Git worktrees. It turns
an already verified worktree signal into an explicit ELO Forge workspace
descriptor while preserving the existing merge/authority boundary.
"""
from __future__ import annotations
from dataclasses import dataclass
from .hermes_worktree_boundary import WorktreeDisposition, WorktreeSignal, assess_worktree

@dataclass(frozen=True, slots=True)
class WorktreeWorkspace:
    workspace_id: str
    tenant_scope: str
    worktree_id: str
    base_ref: str
    source_refs: tuple[str, ...]
    isolated: bool
    merge_authority: bool = False
    canonical_authority: bool = False

class WorktreeAdapter:
    """Adapt verified worktree signals into a bounded Forge workspace."""
    def adapt(self, signal: WorktreeSignal) -> WorktreeWorkspace | None:
        assessment = assess_worktree(signal)
        if assessment.disposition is not WorktreeDisposition.CANDIDATE:
            return None
        return WorktreeWorkspace(
            workspace_id=f"forge:{signal.tenant_scope}:{signal.worktree_id}",
            tenant_scope=signal.tenant_scope,
            worktree_id=signal.worktree_id,
            base_ref=signal.base_ref,
            source_refs=assessment.evidence_refs,
            isolated=signal.isolated,
        )

def adapt_worktree(signal: WorktreeSignal) -> WorktreeWorkspace | None:
    return WorktreeAdapter().adapt(signal)

__all__ = ["WorktreeWorkspace", "WorktreeAdapter", "adapt_worktree"]
