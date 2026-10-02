from elo.agent_intake.hermes_learning_boundary import LearningGraphRelation
from elo.agent_intake.hermes_learning_graph_runtime_adapter import evaluate_learning_graph_runtime
from elo.agent_intake.runtime_operational_evidence import (
    RepeatabilityEvidence,
    aggregate_repeatability,
)


def _relations(prefix: str):
    ref = f"runtime:{prefix}"
    return (
        LearningGraphRelation("r1", "skill-pricing", "evidence-quotation", "SUPPORTS", (ref,)),
        LearningGraphRelation("r2", "skill-pricing", "evidence-quotation", "SUPPORTS", (ref,)),
        LearningGraphRelation(
            "r3",
            "skill-pricing",
            "evidence-contract",
            "SUPPORTS",
            (f"{ref}/distinct",),
        ),
    )


def _single_observation(prefix: str, execution_id: str):
    return evaluate_learning_graph_runtime(
        _relations(prefix),
        tenant_id="tenant-a",
        correlation_id=f"corr-{prefix}",
        runtime_commit="runtime-commit",
        runtime_trace=f"trace-{prefix}",
        execution_id=execution_id,
        repeatability=RepeatabilityEvidence(executions=1, successful=1, rate=1.0),
    ).evidence


def test_learning_graph_runtime_blocks_semantic_duplicates_and_aggregates_observed_repeatability():
    first = _single_observation("one", "exec-learning-graph-1")
    second = _single_observation("two", "exec-learning-graph-2")

    repeatability = aggregate_repeatability((first, second))

    assert repeatability.executions == 2
    assert repeatability.successful == 2
    assert repeatability.rate == 1.0
    assert first.action_observed is True
    assert first.observed_value == 1 / 3
    assert first.provenance.commit == "runtime-commit"
    assert "tenant=tenant-a" in first.provenance.runtime_trace
    assert first.operational_outcome_proven is False


def test_learning_graph_runtime_does_not_mutate_relation_authority():
    result = evaluate_learning_graph_runtime(
        _relations("authority"),
        tenant_id="tenant-b",
        correlation_id="corr-authority",
        runtime_commit="runtime-commit",
        runtime_trace="trace-authority",
        execution_id="exec-learning-graph-3",
        repeatability=RepeatabilityEvidence(executions=1, successful=1, rate=1.0),
    )

    assert len(result.accepted) == 2
    assert len(result.blocked_duplicates) == 1
    assert all(relation.canonical_authority is False for relation in result.accepted)
    assert all(relation.canonical_authority is False for relation in result.blocked_duplicates)
