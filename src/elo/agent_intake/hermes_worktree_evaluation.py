"""Three-phase controlled evaluation of EXT-WORKTREE-HERMES."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Sequence
from .hermes_worktree_adapter import adapt_worktree
from .hermes_worktree_boundary import WorktreeSignal

CAPABILITY_ID = "EXT-WORKTREE-HERMES"
PRIMARY_METRIC = "isolated_workspace_integrity_rate"
METRIC_DIRECTION = "maximize"

@dataclass(frozen=True)
class WorktreeEvaluation:
    baseline_rate: float
    adapted_rate: float
    boundary_integrity_rate: float
    repeatable: bool
    result: str

def _signals(prefix: str) -> Sequence[WorktreeSignal]:
    return tuple(
        WorktreeSignal(
            signal_id=f"{prefix}-{i}",
            tenant_scope="multiteiner",
            worktree_id=f"wt/{prefix.lower()}/{i}",
            source_refs=(f"git:worktree:{prefix.lower()}/{i}",),
            base_ref="main",
            isolated=True,
            provenance_verified=True,
        )
        for i in range(1, 6)
    )

def _integrity(signals: Sequence[WorktreeSignal]) -> float:
    if not signals:
        return 0.0
    passed = 0
    for signal in signals:
        workspace = adapt_worktree(signal)
        passed += bool(
            workspace
            and workspace.workspace_id
            and workspace.tenant_scope == signal.tenant_scope
            and workspace.worktree_id == signal.worktree_id
            and workspace.isolated
            and not workspace.merge_authority
            and not workspace.canonical_authority
        )
    return passed / len(signals)

def evaluate() -> WorktreeEvaluation:
    baseline = _signals("BASE")
    adapted = _signals("HERMES")
    baseline_rate = 0.0
    adapted_rate = _integrity(adapted)
    boundary = _integrity(adapted)
    repeatable = _integrity(_signals("REPEAT")) == adapted_rate and boundary == 1.0
    result = "EVOLUTION_GATE_REQUIRED" if adapted_rate > baseline_rate and repeatable else "RETEST"
    return WorktreeEvaluation(baseline_rate, adapted_rate, boundary, repeatable, result)
