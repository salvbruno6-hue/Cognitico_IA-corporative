"""Governed learning and MLOps metadata lifecycle for ELO-008."""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass
from typing import Any

from elo.memory.persistent import PersistentMemoryStore


@dataclass(frozen=True)
class ExperienceRecord:
    experience_id: str
    tenant_id: str
    domain: str
    decision_id: str
    expected_outcome: str
    observed_outcome: str
    evidence_ids: tuple[str, ...]
    captured_at: float


@dataclass(frozen=True)
class LearningCandidate:
    candidate_id: str
    experience_id: str
    tenant_id: str
    domain: str
    hypothesis: str
    dataset_version: str
    provenance: dict[str, Any]
    state: str = "CANDIDATE"


@dataclass(frozen=True)
class EvaluationRecord:
    candidate_id: str
    metric: str
    score: float
    threshold: float
    evaluator: str
    dataset_version: str
    evaluated_at: float


class LearningGovernanceError(ValueError):
    """Raised when a learning lifecycle transition violates governance."""


class GovernedLearningService:
    """Captures experience and evaluates candidates without self-modification."""

    def __init__(self, memory: PersistentMemoryStore) -> None:
        self.memory = memory

    def capture_outcome(
        self,
        *,
        tenant_id: str,
        domain: str,
        principal_id: str,
        decision_id: str,
        expected_outcome: str,
        observed_outcome: str,
        evidence_ids: tuple[str, ...],
    ) -> ExperienceRecord:
        experience = ExperienceRecord(
            experience_id=str(uuid.uuid4()),
            tenant_id=tenant_id,
            domain=domain,
            decision_id=decision_id,
            expected_outcome=expected_outcome,
            observed_outcome=observed_outcome,
            evidence_ids=evidence_ids,
            captured_at=time.time(),
        )
        self.memory.remember(
            tenant_id=tenant_id,
            domain=domain,
            principal_id=principal_id,
            content=(
                f"decision={decision_id}; expected={expected_outcome}; observed={observed_outcome}"
            ),
            source_id=experience.experience_id,
            provenance={"type": "outcome_feedback", "evidence_ids": list(evidence_ids)},
            kind="experience",
        )
        return experience

    def propose_candidate(
        self,
        experience: ExperienceRecord,
        *,
        dataset_version: str,
        hypothesis: str,
    ) -> LearningCandidate:
        if not dataset_version or not hypothesis:
            raise LearningGovernanceError("dataset_version and hypothesis are required")
        candidate = LearningCandidate(
            candidate_id=str(uuid.uuid4()),
            experience_id=experience.experience_id,
            tenant_id=experience.tenant_id,
            domain=experience.domain,
            hypothesis=hypothesis,
            dataset_version=dataset_version,
            provenance={"experience_id": experience.experience_id},
        )
        return candidate

    @staticmethod
    def evaluate(
        candidate: LearningCandidate,
        *,
        metric: str,
        score: float,
        threshold: float,
        evaluator: str,
    ) -> EvaluationRecord:
        if not 0.0 <= score <= 1.0 or not 0.0 <= threshold <= 1.0:
            raise LearningGovernanceError("score and threshold must be between 0 and 1")
        if not evaluator:
            raise LearningGovernanceError("evaluator is required")
        return EvaluationRecord(
            candidate_id=candidate.candidate_id,
            metric=metric,
            score=score,
            threshold=threshold,
            evaluator=evaluator,
            dataset_version=candidate.dataset_version,
            evaluated_at=time.time(),
        )

    @staticmethod
    def approve_for_promotion(candidate: LearningCandidate, evaluation: EvaluationRecord, *, human_approved: bool) -> LearningCandidate:
        if evaluation.candidate_id != candidate.candidate_id:
            raise LearningGovernanceError("evaluation does not belong to candidate")
        if evaluation.score < evaluation.threshold:
            raise LearningGovernanceError("candidate failed evaluation threshold")
        if not human_approved:
            raise LearningGovernanceError("human approval is required for promotion")
        return LearningCandidate(
            candidate_id=candidate.candidate_id,
            experience_id=candidate.experience_id,
            tenant_id=candidate.tenant_id,
            domain=candidate.domain,
            hypothesis=candidate.hypothesis,
            dataset_version=candidate.dataset_version,
            provenance=dict(candidate.provenance),
            state="APPROVED",
        )
