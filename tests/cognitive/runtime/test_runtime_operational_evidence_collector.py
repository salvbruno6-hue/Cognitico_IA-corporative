from datetime import datetime, timezone

import pytest

from elo.agent_intake.runtime_operational_evidence import (
    RepeatabilityEvidence,
    RuntimeProvenance,
    create_runtime_evidence,
)
from elo.agent_intake.runtime_operational_evidence_collector import (
    RuntimeOperationalEvidenceCollector,
)


def _item(execution_id: str, candidate: str = "EXT-CONTEXT-PLUGIN-HERMES"):
    return create_runtime_evidence(
        execution_id=execution_id,
        candidate_id=candidate,
        owner="HERMES-CONTEXT",
        runtime_entrypoint="elo.context.resolve",
        action_observed=True,
        metric="context_plugin_activation_success_rate",
        direction="maximize",
        baseline=0.0,
        observed_value=1.0,
        attribution="candidate",
        provenance=RuntimeProvenance(
            commit="runtime-commit",
            runtime_trace=f"trace-{execution_id}",
        ),
        regression=False,
        repeatability=RepeatabilityEvidence(1, 1, 1.0),
        timestamp=datetime(2026, 9, 27, tzinfo=timezone.utc),
    )


def test_one_execution_is_collected_but_not_ready():
    collector = RuntimeOperationalEvidenceCollector()
    collector.append(_item("exec-1"))

    assert len(collector.observations()) == 1
    assert collector.ready_groups() == ()


def test_two_distinct_executions_produce_operational_outcome():
    collector = RuntimeOperationalEvidenceCollector()
    collector.append(_item("exec-1"))
    collector.append(_item("exec-2"))

    groups = collector.ready_groups()
    assert len(groups) == 1
    outcome = groups[0].to_operational_outcome()

    assert outcome.level == "OPERATIONAL_OUTCOME"
    assert outcome.production_proven is True
    assert outcome.repeatable is True


def test_duplicate_execution_id_cannot_increase_repeatability():
    collector = RuntimeOperationalEvidenceCollector()
    first = _item("exec-1")
    collector.append(first)

    with pytest.raises(ValueError, match="duplicate execution_id"):
        collector.append(first)

    assert collector.ready_groups() == ()


def test_different_candidates_never_share_a_repeatability_group():
    collector = RuntimeOperationalEvidenceCollector()
    collector.append(_item("exec-1", "EXT-CONTEXT-PLUGIN-HERMES"))
    collector.append(_item("exec-2", "EXT-CHECKPOINT-HERMES"))

    assert len(collector.groups()) == 2
    assert collector.ready_groups() == ()


def test_regression_blocks_operational_outcome():
    collector = RuntimeOperationalEvidenceCollector()
    collector.append(_item("exec-1"))
    regressed = create_runtime_evidence(
        execution_id="exec-2",
        candidate_id="EXT-CONTEXT-PLUGIN-HERMES",
        owner="HERMES-CONTEXT",
        runtime_entrypoint="elo.context.resolve",
        action_observed=True,
        metric="context_plugin_activation_success_rate",
        direction="maximize",
        baseline=0.0,
        observed_value=0.0,
        attribution="candidate",
        provenance=RuntimeProvenance(
            commit="runtime-commit",
            runtime_trace="trace-exec-2",
        ),
        regression=True,
        repeatability=RepeatabilityEvidence(1, 1, 1.0),
    )
    collector.append(regressed)

    outcome = collector.ready_groups()[0].to_operational_outcome()
    assert outcome.level == "FUNCTIONAL_CONTROLLED_GAIN"
    assert outcome.production_proven is False
