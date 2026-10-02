"""Governed runtime bridge for EXT-WORKTREE-HERMES.

The bridge reuses the existing WorktreeSignal/WorktreeAdapter boundary. It
observes bounded workspace adaptation only; it does not create, delete, merge,
activate, persist, authorize, or promote Git worktrees.
"""
from __future__ import annotations

from dataclasses import dataclass

from .hermes_worktree_adapter import WorktreeWorkspace, adapt_worktree
from .hermes_worktree_boundary import WorktreeSignal
from .runtime_operational_evidence import (
    RepeatabilityEvidence,
    RuntimeOperationalEvidence,
    RuntimeProvenance,
    create_runtime_evidence,
)

CAPABILITY_ID = "EXT-WORKTREE-HERMES"
OWNER = "ELO Forge"


@dataclass(frozen=True, slots=True)
class WorktreeRuntimeResult:
    workspace: WorktreeWorkspace | None
    evidence: RuntimeOperationalEvidence


def evaluate_worktree_runtime(
    signal: WorktreeSignal,
    *,
    runtime_commit: str,
    runtime_trace: str,
    execution_id: str,
    repeatability: RepeatabilityEvidence,
) -> WorktreeRuntimeResult:
    """Adapt one verified worktree signal and emit observational evidence."""
    workspace = adapt_worktree(signal)
    observed = 1.0 if workspace is not None and workspace.isolated else 0.0

    evidence = create_runtime_evidence(
        execution_id=execution_id,
        candidate_id=CAPABILITY_ID,
        owner=OWNER,
        runtime_entrypoint="adapt_worktree",
        action_observed=True,
        metric="isolated_workspace_integrity_rate",
        direction="maximize",
        baseline=0.0,
        observed_value=observed,
        attribution="candidate",
        provenance=RuntimeProvenance(
            commit=runtime_commit,
            runtime_trace=(
                f"{runtime_trace}:tenant={signal.tenant_scope}"
                f":worktree={signal.worktree_id}"
            ),
        ),
        regression=False,
        repeatability=repeatability,
    )
    return WorktreeRuntimeResult(workspace=workspace, evidence=evidence)


__all__ = ["WorktreeRuntimeResult", "evaluate_worktree_runtime"]
