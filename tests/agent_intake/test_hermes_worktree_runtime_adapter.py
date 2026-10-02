from elo.agent_intake.hermes_worktree_boundary import WorktreeSignal
from elo.agent_intake.hermes_worktree_runtime_adapter import evaluate_worktree_runtime
from elo.agent_intake.runtime_operational_evidence import (
    RepeatabilityEvidence,
    aggregate_repeatability,
)


def _signal(prefix: str) -> WorktreeSignal:
    return WorktreeSignal(
        signal_id=f"{prefix}-signal",
        tenant_scope="multiteiner",
        worktree_id=f"wt/{prefix.lower()}",
        source_refs=(f"runtime:worktree/{prefix.lower()}",),
        base_ref="main",
        isolated=True,
        provenance_verified=True,
    )


def _observation(prefix: str, execution_id: str):
    return evaluate_worktree_runtime(
        _signal(prefix),
        runtime_commit="runtime-commit",
        runtime_trace=f"trace-{prefix}",
        execution_id=execution_id,
        repeatability=RepeatabilityEvidence(executions=1, successful=1, rate=1.0),
    )


def test_worktree_runtime_emits_observed_integrity_and_repeatability():
    first = _observation("ONE", "exec-worktree-1")
    second = _observation("TWO", "exec-worktree-2")

    repeatability = aggregate_repeatability(
        (first.evidence, second.evidence)
    )

    assert first.workspace is not None
    assert first.workspace.isolated is True
    assert first.workspace.merge_authority is False
    assert first.workspace.canonical_authority is False
    assert first.evidence.action_observed is True
    assert first.evidence.observed_value == 1.0
    assert repeatability.executions == 2
    assert repeatability.successful == 2
    assert repeatability.rate == 1.0


def test_worktree_runtime_rejects_unverified_or_nonisolated_signal():
    signal = WorktreeSignal(
        signal_id="invalid-signal",
        tenant_scope="multiteiner",
        worktree_id="wt/invalid",
        source_refs=("runtime:worktree/invalid",),
        base_ref="main",
        isolated=False,
        provenance_verified=True,
    )

    result = evaluate_worktree_runtime(
        signal,
        runtime_commit="runtime-commit",
        runtime_trace="trace-invalid",
        execution_id="exec-worktree-invalid",
        repeatability=RepeatabilityEvidence(executions=1, successful=0, rate=0.0),
    )

    assert result.workspace is None
    assert result.evidence.observed_value == 0.0
    assert result.evidence.operational_outcome_proven is False
