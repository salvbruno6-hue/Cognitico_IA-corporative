"""Provider-neutral model evaluation boundary for ELO learning evidence."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


class MLOpsEvaluationError(ValueError):
    """Raised when evaluation metadata is incomplete or unsafe."""


@dataclass(frozen=True)
class ModelEvaluation:
    evaluation_id: str
    tenant_id: str
    model_id: str
    dataset_version: str
    evaluator: str
    metric: str
    score: float
    threshold: float
    evidence_ids: tuple[str, ...]
    provenance: Mapping[str, str]
    promotion_state: str = "CANDIDATE"


class NativeMLOpsEvaluation:
    """Evaluate a model candidate without creating a model registry authority."""

    _SECRET_KEYS = {"password", "token", "access_token", "refresh_token", "api_key", "service_role"}

    def evaluate(self, *, evaluation_id: str, tenant_id: str, model_id: str,
                 dataset_version: str, evaluator: str, metric: str, score: float,
                 threshold: float, evidence_ids: tuple[str, ...] | list[str],
                 provenance: Mapping[str, str]) -> ModelEvaluation:
        if any(not str(v).strip() for v in (evaluation_id, tenant_id, model_id,
                                             dataset_version, evaluator, metric)):
            raise MLOpsEvaluationError("evaluation identity and reproducibility metadata are required")
        if not evidence_ids:
            raise MLOpsEvaluationError("evaluation evidence is required")
        if not 0.0 <= float(score) <= 1.0 or not 0.0 <= float(threshold) <= 1.0:
            raise MLOpsEvaluationError("score and threshold must be normalized to [0, 1]")
        if not provenance.get("source_ref") or not provenance.get("source_commit"):
            raise MLOpsEvaluationError("provenance requires source_ref and source_commit")
        if any(key.lower() in self._SECRET_KEYS for key in provenance):
            raise MLOpsEvaluationError("secret-bearing provenance is forbidden")
        state = "CANDIDATE" if score >= threshold else "REJECTED"
        return ModelEvaluation(evaluation_id.strip(), tenant_id.strip(), model_id.strip(),
                               dataset_version.strip(), evaluator.strip(), metric.strip(),
                               float(score), float(threshold), tuple(evidence_ids),
                               dict(provenance), state)
