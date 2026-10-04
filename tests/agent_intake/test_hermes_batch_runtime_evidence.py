from dataclasses import replace

from elo.agent_intake.hermes_batch_boundary import BatchDisposition, BatchSignal, assess_batch
from elo.agent_intake.hermes_batch_runtime_adapter import evaluate_batch_with_runtime_evidence
from elo.agent_intake.runtime_operational_evidence_collector import RuntimeOperationalEvidenceCollector
from elo.cognitive.mlops_evaluation import NativeMLOpsEvaluation


def _signal(run: int) -> BatchSignal:
    return BatchSignal(
        batch_id=f"batch-{run}",
        tenant_scope="tenant-a",
        source_refs=(f"batch-source:{run}",),
        task_digest=f"task-digest-{run}",
        item_count=2,
        bounded=True,
        explicit_authorization=True,
        result_schema_digest="schema-1",
        canonical_mutation=False,
        promotion_attempt=False,
        max_items=100,
    )


def test_real_mlops_evaluation_records_one_batch_runtime_observation() -> None:
    result = evaluate_batch_with_runtime_evidence(
        _signal(1),
        evaluator=NativeMLOpsEvaluation(),
        model_id="model:test",
        dataset_version="dataset-v1",
        evaluator_name="batch-runtime-test",
        metric="task_identity",
        score=1.0,
        threshold=0.5,
        source_commit="abc123",
        runtime_trace="batch-trace-1",
        execution_id="batch-exec-1",
    )

    assert result is not None
    assert result.evaluation.evaluation_id == "batch-1"
    assert result.evaluation.tenant_id == "tenant-a"
    assert result.evaluation.evidence_ids == ("batch-source:1",)
    assert result.evidence.runtime_entrypoint == "NativeMLOpsEvaluation.evaluate"
    assert result.evidence.operational_outcome_proven is False


def test_two_real_batch_evaluations_become_operational_outcome() -> None:
    collector = RuntimeOperationalEvidenceCollector()
    evaluator = NativeMLOpsEvaluation()

    for run in (1, 2):
        result = evaluate_batch_with_runtime_evidence(
            _signal(run),
            evaluator=evaluator,
            model_id="model:test",
            dataset_version="dataset-v1",
            evaluator_name="batch-runtime-test",
            metric="task_identity",
            score=1.0,
            threshold=0.5,
            source_commit="abc123",
            runtime_trace=f"batch-trace-{run}",
            execution_id=f"batch-exec-{run}",
        )
        assert result is not None
        collector.append(result.evidence)

    groups = collector.ready_groups()
    assert len(groups) == 1
    group = groups[0]
    assert group.candidate_id == "EXT-BATCH-HERMES"
    assert group.repeatable is True

    outcome = group.to_operational_outcome()
    assert outcome is not None
    assert outcome.candidate_id == "EXT-BATCH-HERMES"
    assert outcome.production_proven is False
    assert outcome.repeatable is True


def test_batch_boundary_rejects_excessive_items() -> None:
    assessment = assess_batch(replace(_signal(1), item_count=101, max_items=100))
    assert assessment.disposition == BatchDisposition.REJECTED


def test_batch_boundary_rejects_invalid_item_limit() -> None:
    assessment = assess_batch(replace(_signal(1), max_items=1001))
    assert assessment.disposition == BatchDisposition.REJECTED
