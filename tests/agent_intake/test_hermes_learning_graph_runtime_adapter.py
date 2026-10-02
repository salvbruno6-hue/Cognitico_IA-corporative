from elo.agent_intake.hermes_learning_boundary import LearningGraphRelation
from elo.agent_intake.hermes_learning_graph_runtime_adapter import evaluate_learning_graph_runtime
from elo.agent_intake.runtime_operational_evidence import RepeatabilityEvidence


def _relations(prefix: str):
    ref = f"runtime:{prefix}"
    return (
        LearningGraphRelation("r1", "skill-pricing", "evidence-quotation", "SUPPORTS", (ref,)),
        LearningGraphRelation("r2", "skill-pricing", "evidence-quotation", "SUPPORTS", (ref,)),
        LearningGraphRelation("r3", "skill-pricing", "evidence-contract", "SUPPORTS", (f"{ref}/distinct",)),
    )


def test_learning_graph_runtime_blocks_semantic_duplicates_and_emits_evidence():
    result = evaluate_learning_graph_runtime(
        _relations("one"),
        tenant_id="tenant-a",
        correlation_id="corr-a",
        runtime_commit="runtime-commit",
        runtime_trace="trace-a",
        execution_id="exec-learning-graph-1",
        repeatability=RepeatabilityEvidence(executions=2, successful=2, rate=1.0),
    )

    assert len(result.accepted) == 2
    assert len(result.blocked_duplicates) == 1
    assert result.evidence.action_observed is True
    assert result.evidence.observed_value == 1 / 3
    assert result.evidence.provenance.commit == "runtime-commit"
    assert "tenant=tenant-a" in result.evidence.provenance.runtime_trace
    assert result.evidence.operational_outcome_proven is True


def test_learning_graph_runtime_does_not_mutate_relation_authority():
    result = evaluate_learning_graph_runtime(
        _relations("two"),
        tenant_id="tenant-b",
        correlation_id="corr-b",
        runtime_commit="runtime-commit",
        runtime_trace="trace-b",
        execution_id="exec-learning-graph-2",
        repeatability=RepeatabilityEvidence(executions=2, successful=2, rate=1.0),
    )

    assert all(relation.canonical_authority is False for relation in result.accepted)
    assert all(relation.canonical_authority is False for relation in result.blocked_duplicates)
