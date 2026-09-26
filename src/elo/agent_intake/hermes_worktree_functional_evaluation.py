"""Candidate-specific functional evaluation for EXT-WORKTREE-HERMES.

The experiment measures whether concurrent controlled tasks receive distinct
isolated workspace identities. It does not create or merge real Git worktrees.
"""
from __future__ import annotations
from dataclasses import dataclass
from .hermes_worktree_adapter import adapt_worktree
from .hermes_worktree_boundary import WorktreeSignal

@dataclass(frozen=True, slots=True)
class WorktreeFunctionalEvidence:
    baseline_collision_free_rate: float
    adapted_collision_free_rate: float
    repeatable: bool
    boundary_integrity: bool
    provenance_refs: tuple[str, ...]

def _signals(prefix: str) -> tuple[WorktreeSignal, ...]:
    return tuple(
        WorktreeSignal(
            signal_id=f"{prefix}-{i}",
            tenant_scope="multiteiner",
            worktree_id=f"wt/{prefix.lower()}/{i}",
            source_refs=(f"controlled-eval:worktree-functional/{prefix.lower()}/{i}",),
            base_ref="main",
            isolated=True,
            provenance_verified=True,
        )
        for i in (1, 2)
    )

def _baseline_collision_free_rate(signals: tuple[WorktreeSignal, ...]) -> float:
    shared_workspace_id = "forge:multiteiner:shared"
    return float(len({shared_workspace_id for _ in signals}) == len(signals))

def _adapted_collision_free_rate(signals: tuple[WorktreeSignal, ...]) -> float:
    workspaces = tuple(adapt_worktree(signal) for signal in signals)
    ids = tuple(workspace.workspace_id for workspace in workspaces if workspace is not None)
    return float(len(ids) == len(signals) and len(set(ids)) == len(ids))

def evaluate_worktree_functional_gain() -> WorktreeFunctionalEvidence:
    baseline = _signals("BASELINE")
    adapted = _signals("HERMES")
    baseline_rate = _baseline_collision_free_rate(baseline)
    adapted_rate = _adapted_collision_free_rate(adapted)
    repeat = _adapted_collision_free_rate(_signals("REPEAT")) == adapted_rate
    workspaces = tuple(adapt_worktree(signal) for signal in adapted)
    boundary = all(
        workspace is not None
        and workspace.isolated
        and not workspace.merge_authority
        and not workspace.canonical_authority
        for workspace in workspaces
    )
    refs = tuple(ref for signal in adapted for ref in signal.source_refs)
    return WorktreeFunctionalEvidence(
        baseline_rate, adapted_rate, repeat, boundary, refs
    )
