"""Tests for runtime-generated operational evidence."""

from datetime import datetime, timezone

import pytest

from elo.agent_intake.runtime_operational_evidence import (
    RepeatabilityEvidence,
    aggregate_repeatability,
    create_execution_id,
    create_runtime_evidence,
    validate_operational_evidence,
    RuntimeProvenance,
)


def _evidence(execution_id: str = "exec-1", *, successful: int = 2):
    return create_runtime_evidence(
        execution_id=execution_id,
        candidate_id="EXT-CONTEXT-PLUGIN-HERMES",
        owner="HERMES-CONTEXT",
        runtime_entrypoint="elo.context.resolve",
        action_observed=True,
        metric="task_success_rate",
        direction="maximize",
        baseline=0.50,
        observed_value=1.00,
        attribution="candidate",
        provenance=RuntimeProvenance(
            commit="abc123",
            runtime_trace="trace-123",
            test_run="runtime-test-1",
        ),
        regression=False,
        repeatability=RepeatabilityEvidence(
            executions=2,
            successful=successful,
            rate=successful / 2,
        ),
        timestamp=datetime(2026, 9, 27, tzinfo=timezone.utc),
    )


def test_execution_id_is_created_at_runtime_boundary():
    execution_id = create_execution_id(
        "EXT-CONTEXT-PLUGIN-HERMES",
        now=datetime(2026, 9, 27, 12, 30, tzinfo=timezone.utc),
    )

    assert execution_id.startswith("exec-20260927T123000000000Z-")


def test_real_runtime_evidence_requires_observed_action():
    with pytest.raises(ValueError, match="observed runtime action"):
        create_runtime_evidence(
            execution_id="exec-1",
            candidate_id="EXT-CONTEXT-PLUGIN-HERMES",
            owner="HERMES-CONTEXT",
            runtime_entrypoint="elo.context.resolve",
            action_observed=False,
            metric="task_success_rate",
            direction="maximize",
            baseline=0.0,
            observed_value=1.0,
            attribution="candidate",
            provenance=RuntimeProvenance(commit="abc", runtime_trace="trace"),
            regression=False,
            repeatability=RepeatabilityEvidence(2, 2, 1.0),
        )


def test_real_runtime_evidence_requires_candidate_attribution():
    with pytest.raises(ValueError, match="candidate attribution"):
        create_runtime_evidence(
            execution_id="exec-1",
            candidate_id="EXT-CONTEXT-PLUGIN-HERMES",
            owner="HERMES-CONTEXT",
            runtime_entrypoint="elo.context.resolve",
            action_observed=True,
            metric="task_success_rate",
            direction="maximize",
            baseline=0.0,
            observed_value=1.0,
            attribution="owner",
            provenance=RuntimeProvenance(commit="abc", runtime_trace="trace"),
            regression=False,
            repeatability=RepeatabilityEvidence(2, 2, 1.0),
        )


def test_operational_outcome_requires_repeatability():
    evidence = _evidence(successful=1)

    assert evidence.operational_outcome_proven is False
    valid, errors = validate_operational_evidence(evidence)
    assert valid is False
    assert "REPEATABILITY_NOT_ESTABLISHED" in errors


def test_operational_outcome_requires_provenance():
    with pytest.raises(ValueError, match="commit and runtime_trace"):
        create_runtime_evidence(
            execution_id="exec-1",
            candidate_id="EXT-CONTEXT-PLUGIN-HERMES",
            owner="HERMES-CONTEXT",
            runtime_entrypoint="elo.context.resolve",
            action_observed=True,
            metric="task_success_rate",
            baseline=0.0,
            observed_value=1.0,
            attribution="candidate",
            provenance=RuntimeProvenance(commit="", runtime_trace=""),
            regression=False,
            repeatability=RepeatabilityEvidence(2, 2, 1.0),
        )


def test_repeated_real_observations_can_be_aggregated():
    observations = (_evidence("exec-1"), _evidence("exec-2"))

    repeatability = aggregate_repeatability(observations)

    assert repeatability.executions == 2
    assert repeatability.successful == 2
    assert repeatability.rate == 1.0
    assert all(item.operational_outcome_proven for item in observations)


def test_evidence_is_hashable_for_provenance_integrity():
    evidence = _evidence()

    assert len(evidence.evidence_hash) == 64
    assert evidence.evidence_hash != ""


def test_regression_blocks_operational_proof():
    evidence = create_runtime_evidence(
        execution_id="exec-regression",
        candidate_id="EXT-CONTEXT-PLUGIN-HERMES",
        owner="HERMES-CONTEXT",
        runtime_entrypoint="elo.context.resolve",
        action_observed=True,
        metric="task_success_rate",
        direction="minimize",
        baseline=0.50,
        observed_value=0.40,
        attribution="candidate",
        provenance=RuntimeProvenance(commit="abc", runtime_trace="trace"),
        regression=True,
        repeatability=RepeatabilityEvidence(2, 2, 1.0),
    )

    valid, errors = validate_operational_evidence(evidence)

    assert valid is False
    assert "REGRESSION_DETECTED" in errors
    assert evidence.operational_outcome_proven is False


def test_sink_persists_unique_runtime_execution_records():
    from elo.agent_intake.runtime_operational_evidence import InMemoryRuntimeEvidenceSink

    sink = InMemoryRuntimeEvidenceSink()
    first = _evidence("exec-sink-1")
    second = _evidence("exec-sink-2")

    sink.append(first)
    sink.append(second)

    assert tuple(item.execution_id for item in sink.list()) == ("exec-sink-1", "exec-sink-2")


def test_sink_rejects_duplicate_execution_id():
    from elo.agent_intake.runtime_operational_evidence import InMemoryRuntimeEvidenceSink

    sink = InMemoryRuntimeEvidenceSink()
    first = _evidence("exec-sink-duplicate")
    sink.append(first)

    with pytest.raises(ValueError, match="duplicate execution_id"):
        sink.append(first)
