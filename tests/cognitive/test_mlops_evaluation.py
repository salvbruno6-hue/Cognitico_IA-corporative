import pytest

from src.elo.cognitive.mlops_evaluation import MLOpsEvaluationError, NativeMLOpsEvaluation


def provenance():
    return {"source_ref": "github://repo", "source_commit": "abc123"}


def test_score_above_threshold_is_candidate():
    result = NativeMLOpsEvaluation().evaluate(
        evaluation_id="e1", tenant_id="t1", model_id="m1", dataset_version="d1",
        evaluator="eval", metric="quality", score=0.92, threshold=0.90,
        evidence_ids=("ev1",), provenance=provenance())
    assert result.promotion_state == "CANDIDATE"


def test_score_below_threshold_is_rejected():
    result = NativeMLOpsEvaluation().evaluate(
        evaluation_id="e1", tenant_id="t1", model_id="m1", dataset_version="d1",
        evaluator="eval", metric="quality", score=0.70, threshold=0.90,
        evidence_ids=("ev1",), provenance=provenance())
    assert result.promotion_state == "REJECTED"


def test_missing_evidence_blocks():
    with pytest.raises(MLOpsEvaluationError):
        NativeMLOpsEvaluation().evaluate(
            evaluation_id="e1", tenant_id="t1", model_id="m1", dataset_version="d1",
            evaluator="eval", metric="quality", score=0.92, threshold=0.90,
            evidence_ids=(), provenance=provenance())
