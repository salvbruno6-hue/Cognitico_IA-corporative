from datetime import datetime, timezone

import pytest

from elo.agent_intake.hermes_functional_value_proof import FunctionalValueEvidence
from elo.agent_intake.runtime_operational_evidence import (
    RepeatabilityEvidence,
    RuntimeProvenance,
    create_runtime_evidence,
)
from elo.agent_intake.runtime_operational_evidence_adapter import (
    to_operational_outcome,
    validate_decision_pattern_execution_binding,
)
from elo.core.execution_boundary import ExecutionOutcome, ExecutionStatus


def _item(execution_id: str, *, pattern_ref: str | None = None):
    return create_runtime_evidence(
        execution_id=execution_id,
        candidate_id="EXT-CONTEXT-PLUGIN-HERMES",
        owner="HERMES-CONTEXT",
        runtime_entrypoint="ELOKnowledgeProvider.retrieve",
        action_observed=True,
        metric="context_plugin_activation_success_rate",
        direction="maximize",
        baseline=0.0,
        observed_value=1.0,
        attribution="candidate",
        provenance=RuntimeProvenance(
            commit="commit-1",
            runtime_trace=f"trace-{execution_id}",
        ),
        regression=False,
        repeatability=RepeatabilityEvidence(1, 1, 1.0),
        decision_pattern_candidate_ref=pattern_ref,
    )


def _execution(
    execution_id: str,
    *,
    pattern_ref: str | None = None,
) -> ExecutionOutcome:
    return ExecutionOutcome(
        request_id=execution_id,
        status=ExecutionStatus.EXECUTED,
        executed=True,
        reason="authorized_execution_completed",
        provenance={"source_commit": "commit-1"},
        evidence_ids=("evidence-1",),
        authorization_id="grant-1",
        occurred_at=datetime(2026, 9, 30, tzinfo=timezone.utc),
        decision_pattern_candidate_ref=pattern_ref,
    )


def test_two_real_observations_become_operational_outcome_without_production_claim():
    evidence = to_operational_outcome((_item("exec-1"), _item("exec-2")))

    assert isinstance(evidence, FunctionalValueEvidence)
    assert evidence.level == "OPERATIONAL_OUTCOME"
    assert evidence.production_proven is False
    assert evidence.repeatable is True
    assert evidence.functional_gain_proven is True
    assert len(evidence.provenance_refs) == 2


def test_single_observation_does_not_become_operational_outcome():
    evidence = to_operational_outcome((_item("exec-1"),))

    assert evidence.level == "FUNCTIONAL_CONTROLLED_GAIN"
    assert evidence.production_proven is False
    assert evidence.repeatable is False


def test_duplicate_execution_id_cannot_fake_repeatability():
    item = _item("exec-duplicate")

    with pytest.raises(ValueError, match="distinct execution_id"):
        to_operational_outcome((item, item))


def test_mixed_runtime_entrypoints_cannot_form_one_operational_proof():
    first = _item("exec-1")
    second = create_runtime_evidence(
        execution_id="exec-2",
        candidate_id="EXT-CONTEXT-PLUGIN-HERMES",
        owner="HERMES-CONTEXT",
        runtime_entrypoint="another.runtime.entrypoint",
        action_observed=True,
        metric="context_plugin_activation_success_rate",
        direction="maximize",
        baseline=0.0,
        observed_value=1.0,
        attribution="candidate",
        provenance=RuntimeProvenance(commit="commit-1", runtime_trace="trace-exec-2"),
        regression=False,
        repeatability=RepeatabilityEvidence(1, 1, 1.0),
    )

    with pytest.raises(ValueError, match="same runtime entrypoint"):
        to_operational_outcome((first, second))


def test_pattern_provenance_binds_runtime_observation_to_execution():
    observation = _item("exec-1", pattern_ref="PATTERN-REF-1")
    outcome = _execution("exec-1", pattern_ref="PATTERN-REF-1")

    valid, errors = validate_decision_pattern_execution_binding(
        observation=observation,
        execution_outcome=outcome,
    )

    assert valid is True
    assert errors == ()


def test_pattern_provenance_mismatch_is_fail_closed():
    observation = _item("exec-1", pattern_ref="PATTERN-REF-1")
    outcome = _execution("exec-1", pattern_ref="PATTERN-REF-2")

    valid, errors = validate_decision_pattern_execution_binding(
        observation=observation,
        execution_outcome=outcome,
    )

    assert valid is False
    assert "DECISION_PATTERN_PROVENANCE_MISMATCH" in errors


def test_pattern_provenance_requires_both_sides_when_binding():
    observation = _item("exec-1", pattern_ref="PATTERN-REF-1")
    outcome = _execution("exec-1")

    valid, errors = validate_decision_pattern_execution_binding(
        observation=observation,
        execution_outcome=outcome,
    )

    assert valid is False
    assert "DECISION_PATTERN_PROVENANCE_MISSING" in errors


def test_bound_observations_cannot_mix_with_unbound_observations():
    with pytest.raises(
        ValueError,
        match="must not mix bound and unbound decision pattern provenance",
    ):
        to_operational_outcome((
            _item("exec-1", pattern_ref="PATTERN-REF-1"),
            _item("exec-2"),
        ))


def test_pattern_reference_participates_in_evidence_identity():
    first = _item("exec-1", pattern_ref="PATTERN-REF-1")
    second = _item("exec-1", pattern_ref="PATTERN-REF-2")

    assert first.evidence_hash != second.evidence_hash
