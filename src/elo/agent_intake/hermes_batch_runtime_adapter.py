"""Runtime bridge for EXT-BATCH-HERMES over NativeMLOpsEvaluation.

The batch candidate is admitted by its existing boundary and then evaluated
through the real ELO MLOps evaluation runtime. Evidence is observational only.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from .hermes_batch_adapter import BatchIntakeContract, adapt_batch
from .hermes_batch_boundary import BatchSignal
from .runtime_operational_evidence import (
    RepeatabilityEvidence,
    RuntimeOperationalEvidence,
    RuntimeProvenance,
    create_runtime_evidence,
)
from elo.cognitive.mlops_evaluation import ModelEvaluation, NativeMLOpsEvaluation


CAPABILITY_ID = "EXT-BATCH-HERMES"


@dataclass(frozen=True, slots=True)
class BatchRuntimeObservation:
    contract: BatchIntakeContract
    evaluation: ModelEvaluation
    evidence: RuntimeOperationalEvidence


def evaluate_batch_with_runtime_evidence(
    signal: BatchSignal,
    *,
    evaluator: NativeMLOpsEvaluation,
    model_id: str,
    dataset_version: str,
    evaluator_name: str,
    metric: str,
    score: float,
    threshold: float,
    source_commit: str,
    runtime_trace: str,
    execution_id: str,
) -> BatchRuntimeObservation | None:
    contract = adapt_batch(signal)
    if contract is None:
        return None

    evaluation = evaluator.evaluate(
        evaluation_id=contract.batch_id,
        tenant_id=contract.tenant_scope,
        model_id=model_id,
        dataset_version=dataset_version,
        evaluator=evaluator_name,
        metric=metric,
        score=score,
        threshold=threshold,
        evidence_ids=contract.source_refs,
        provenance={
            "source_ref": contract.source_refs[0],
            "source_commit": source_commit,
            "batch_id": contract.batch_id,
            "task_digest": contract.task_digest,
            "result_schema_digest": contract.result_schema_digest,
        },
    )
    integrity = (
        evaluation.evaluation_id == contract.batch_id
        and evaluation.tenant_id == contract.tenant_scope
        and evaluation.evidence_ids == contract.source_refs
        and evaluation.provenance.get("batch_id") == contract.batch_id
        and evaluation.provenance.get("task_digest") == contract.task_digest
        and evaluation.provenance.get("result_schema_digest") == contract.result_schema_digest
    )
    evidence = create_runtime_evidence(
        execution_id=execution_id,
        candidate_id=CAPABILITY_ID,
        owner="ELO Evaluation & Learning",
        runtime_entrypoint="NativeMLOpsEvaluation.evaluate",
        action_observed=True,
        metric="collision_free_batch_task_rate",
        direction="maximize",
        baseline=0.0,
        observed_value=1.0 if integrity else 0.0,
        attribution="candidate",
        provenance=RuntimeProvenance(commit=source_commit, runtime_trace=runtime_trace),
        regression=not integrity,
        repeatability=RepeatabilityEvidence(
            executions=1,
            successful=1 if integrity else 0,
            rate=1.0 if integrity else 0.0,
        ),
    )
    return BatchRuntimeObservation(contract, evaluation, evidence)
