from datetime import datetime, timezone

import pytest

from elo.agent_intake.runtime_operational_evidence import (
    RepeatabilityEvidence,
    RuntimeProvenance,
    create_runtime_evidence,
)
from elo.agent_intake.runtime_operational_evidence_collector import (
    RuntimeEvidenceKey,
    RuntimeOperationalEvidenceCollector,
)


KEY = RuntimeEvidenceKey(
    candidate_id="EXT-CONTEXT-PLUGIN-HERMES",
    owner="HERMES-CONTEXT",
    runtime_entrypoint="elo.context.resolve",
    metric="task_success_rate",
    direction="maximize",
)


def _item(
    execution_id: str,
    *,
    observed_value: float = 1.0,
    regression: bool = False,
    runtime_entrypoint: str = "elo.context.resolve",
):
    return create_runtime_evidence(
        execution_id=execution_id,
        candidate_id="EXT-CONTEXT-PLUGIN-HERMES",
        owner="HERMES-CONTEXT",
        runtime_entrypoint=runtime_entrypoint,
        action_observed=True,
        metric="task_success_rate",
        direction="maximize",
        baseline=0.5,
        observed_value=observed_value,
        attribution="candidate",
        provenance=RuntimeProvenance(
            commit="runtime-commit",
            runtime_trace=f"trace-{execution_id}",
        ),
        regression=regression,
        repeatability=RepeatabilityEvidence(1, 1, 1.0),
        timestamp=datetime(2026, 9, 27, tzinfo=timezone.utc),
    )


def test_one_execution_remains_controlled_gain():
    collector = RuntimeOperationalEvidenceCollector()
    collector.observe(_item("exec-1"))

    outcome = collector.outcome(KEY)

    assert outcome.level == "FUNCTIONAL_CONTROLLED_GAIN"
    assert outcome.production_proven is False
    assert outcome.repeatable is False


def test_two_distinct_successful_executions_become_operational_outcome():
    collector = RuntimeOperationalEvidenceCollector()
    collector.observe(_item("exec-1"))
    collector.observe(_item("exec-2"))

    outcome = collector.outcome(KEY)

    assert outcome.level == "OPERATIONAL_OUTCOME"
    assert outcome.production_proven is True
    assert outcome.repeatable is True
    assert len(outcome.provenance_refs) == 2


def test_duplicate_execution_is_rejected_before_aggregation():
    collector = RuntimeOperationalEvidenceCollector()
    evidence = _item("exec-duplicate")
    collector.observe(evidence)

    with pytest.raises(ValueError, match="duplicate execution_id"):
        collector.observe(evidence)


def test_regression_blocks_operational_outcome():
    collector = RuntimeOperationalEvidenceCollector()
    collector.observe(_item("exec-1"))
    collector.observe(_item("exec-2", regression=True))

    outcome = collector.outcome(KEY)

    assert outcome.level == "FUNCTIONAL_CONTROLLED_GAIN"
    assert outcome.production_proven is False
    assert "REGRESSION_DETECTED" in outcome.regressions


def test_collector_does_not_mix_runtime_entrypoints():
    collector = RuntimeOperationalEvidenceCollector()
    collector.observe(_item("exec-1"))
    collector.observe(_item("exec-other", runtime_entrypoint="elo.other.resolve"))

    observations = collector.observations(KEY)

    assert tuple(item.execution_id for item in observations) == ("exec-1",)
    assert collector.outcome(KEY).production_proven is False


def test_missing_observations_cannot_claim_outcome():
    collector = RuntimeOperationalEvidenceCollector()

    with pytest.raises(ValueError, match="no runtime observations"):
        collector.outcome(KEY)
