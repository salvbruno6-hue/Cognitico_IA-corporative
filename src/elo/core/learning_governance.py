"""Governed learning and MLOps metadata lifecycle for ELO-008."""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass
from typing import Any, Mapping

from elo.memory.persistent import PersistentMemoryStore
from .evolution_gate import EvolutionClassification, EvolutionDecision


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


@dataclass(frozen=True)
class PromotionPackage:
    status: str
    reason: str
    source_learning_id: str
    knowledge_key: str
    payload: Mapping[str, Any]


@dataclass(frozen=True)
class ExternalMechanismCandidate:
    """Evidence-backed intake record for a mechanism found outside ELO.

    This is deliberately a candidate, not a registry or authority. Source
    material remains external; only the mechanism's generalized value is
    evaluated through ELO's existing learning/evolution governance.
    """

    candidate_id: str
    source_name: str
    source_kind: str
    source_ref: str
    mechanism_id: str
    mechanism: str
    proposed_capability: str
    existing_owner: str
    disposition: str
    evidence_refs: tuple[str, ...]
    scope: str
    generalized: bool
    state: str = "CANDIDATE"


class LearningGovernanceError(ValueError):
    """Raised when a learning lifecycle transition violates governance."""


class GovernedLearningService:
    """Canonical lifecycle for experience, validation and knowledge eligibility."""

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
            experience_id=str(uuid.uuid4()), tenant_id=tenant_id, domain=domain,
            decision_id=decision_id, expected_outcome=expected_outcome,
            observed_outcome=observed_outcome, evidence_ids=evidence_ids, captured_at=time.time(),
        )
        self.memory.remember(
            tenant_id=tenant_id, domain=domain, principal_id=principal_id,
            content=f"decision={decision_id}; expected={expected_outcome}; observed={observed_outcome}",
            source_id=experience.experience_id,
            provenance={"type": "outcome_feedback", "evidence_ids": list(evidence_ids)}, kind="experience",
        )
        return experience

    def propose_candidate(self, experience: ExperienceRecord, *, dataset_version: str, hypothesis: str) -> LearningCandidate:
        if not dataset_version or not hypothesis:
            raise LearningGovernanceError("dataset_version and hypothesis are required")
        return LearningCandidate(
            candidate_id=str(uuid.uuid4()), experience_id=experience.experience_id,
            tenant_id=experience.tenant_id, domain=experience.domain, hypothesis=hypothesis,
            dataset_version=dataset_version, provenance={"experience_id": experience.experience_id},
        )

    @staticmethod
    def evaluate(candidate: LearningCandidate, *, metric: str, score: float, threshold: float, evaluator: str) -> EvaluationRecord:
        if not 0.0 <= score <= 1.0 or not 0.0 <= threshold <= 1.0:
            raise LearningGovernanceError("score and threshold must be between 0 and 1")
        if not evaluator:
            raise LearningGovernanceError("evaluator is required")
        return EvaluationRecord(candidate.candidate_id, metric, score, threshold, evaluator, candidate.dataset_version, time.time())

    @staticmethod
    def approve_for_promotion(candidate: LearningCandidate, evaluation: EvaluationRecord, *, human_approved: bool) -> LearningCandidate:
        if evaluation.candidate_id != candidate.candidate_id:
            raise LearningGovernanceError("evaluation does not belong to candidate")
        if evaluation.score < evaluation.threshold:
            raise LearningGovernanceError("candidate failed evaluation threshold")
        if not human_approved:
            raise LearningGovernanceError("human approval is required for promotion")
        return LearningCandidate(
            candidate_id=candidate.candidate_id, experience_id=candidate.experience_id,
            tenant_id=candidate.tenant_id, domain=candidate.domain, hypothesis=candidate.hypothesis,
            dataset_version=candidate.dataset_version, provenance=dict(candidate.provenance), state="APPROVED",
        )

    @staticmethod
    def ingest_external_mechanism(
        *,
        source_name: str,
        source_kind: str,
        source_ref: str,
        mechanism_id: str,
        mechanism: str,
        proposed_capability: str,
        existing_owner: str,
        disposition: str,
        evidence_refs: tuple[str, ...] | list[str],
        scope: str,
        generalized: bool,
    ) -> ExternalMechanismCandidate:
        """Register an external mechanism as a governed candidate only.

        Allowed dispositions are the canonical reuse-first decisions. This
        method performs intake/normalization and never promotes, writes Core,
        mutates Forge, creates a capability, or creates a second authority.
        """
        required = {
            "source_name": source_name,
            "source_kind": source_kind,
            "source_ref": source_ref,
            "mechanism_id": mechanism_id,
            "mechanism": mechanism,
            "proposed_capability": proposed_capability,
            "existing_owner": existing_owner,
            "disposition": disposition,
            "scope": scope,
        }
        for name, value in required.items():
            if not value or not value.strip():
                raise LearningGovernanceError(f"{name} is required")
        allowed = {"REUSE", "STRENGTHEN", "REFACTOR", "DEPRECATE", "CREATE"}
        normalized_disposition = disposition.strip().upper()
        if normalized_disposition not in allowed:
            raise LearningGovernanceError("invalid external mechanism disposition")
        if not evidence_refs:
            raise LearningGovernanceError("evidence_refs are required")
        if normalized_disposition == "CREATE" and existing_owner.strip().upper() not in {"NONE", "ABSENT", "PROVEN_ABSENT"}:
            raise LearningGovernanceError("CREATE requires proven absence of an existing owner")
        if normalized_disposition == "CREATE" and not generalized:
            raise LearningGovernanceError("CREATE requires a generalized mechanism")
        return ExternalMechanismCandidate(
            candidate_id=str(uuid.uuid4()),
            source_name=source_name.strip(),
            source_kind=source_kind.strip().lower(),
            source_ref=source_ref.strip(),
            mechanism_id=mechanism_id.strip(),
            mechanism=mechanism.strip(),
            proposed_capability=proposed_capability.strip(),
            existing_owner=existing_owner.strip(),
            disposition=normalized_disposition,
            evidence_refs=tuple(evidence_refs),
            scope=scope.strip(),
            generalized=generalized,
        )

    @staticmethod
    def prepare_knowledge_promotion(
        *, learning_id: str, knowledge_key: str, title: str, concept: str,
        provenance: Mapping[str, Any], scope: str, evidence_refs: tuple[str, ...] | list[str],
        confidence: float, evolution_decision: EvolutionDecision | None = None,
        duplicate_found: bool = False, conflict_open: bool = False,
        faculty_relevant: bool = False,
    ) -> PromotionPackage:
        """Prepare a promotion package after the real Evolution Gate decision.

        This is eligibility only: it never writes Git/Supabase, changes Core,
        or grants mutation authority. Materialization remains a separate
        governed operation.
        """
        required = {"learning_id": learning_id, "knowledge_key": knowledge_key, "title": title, "concept": concept, "scope": scope}
        for name, value in required.items():
            if not value or not value.strip():
                return PromotionPackage("PROMOTION_BLOCKED", f"{name}_missing", learning_id, knowledge_key, {})
        if not provenance:
            return PromotionPackage("PROMOTION_BLOCKED", "provenance_missing", learning_id, knowledge_key, {})
        if not 0.0 <= confidence <= 1.0:
            return PromotionPackage("PROMOTION_BLOCKED", "confidence_invalid", learning_id, knowledge_key, {})
        if not evidence_refs:
            return PromotionPackage("PROMOTION_BLOCKED", "evidence_missing", learning_id, knowledge_key, {})
        if duplicate_found:
            return PromotionPackage("PROMOTION_BLOCKED", "duplicate_or_parallel_knowledge", learning_id, knowledge_key, {})
        if conflict_open:
            return PromotionPackage("PROMOTION_BLOCKED", "unresolved_conflict", learning_id, knowledge_key, {})
        if evolution_decision is None:
            return PromotionPackage("PROMOTION_BLOCKED", "evolution_gate_decision_missing", learning_id, knowledge_key, {})
        if evolution_decision.classification is not EvolutionClassification.COMPATIBLE:
            return PromotionPackage("PROMOTION_BLOCKED", f"evolution_gate_not_compatible:{evolution_decision.classification.value}", learning_id, knowledge_key, {})
        if evolution_decision.canonical_mutation_allowed:
            return PromotionPackage("PROMOTION_BLOCKED", "unexpected_gate_mutation_authority", learning_id, knowledge_key, {})
        status = "FACULTY_CANDIDATE" if faculty_relevant else "PROMOTABLE_KNOWLEDGE"
        payload = {
            "knowledge_key": knowledge_key.strip(), "title": title.strip(), "concept": concept.strip(),
            "source_learning_id": learning_id.strip(), "provenance": dict(provenance), "scope": scope.strip(),
            "evidence_refs": tuple(evidence_refs), "confidence": confidence, "status": status,
            "promotion": "VALIDATED_LEARNING_TO_REUSABLE_KNOWLEDGE",
            "evolution_gate_classification": evolution_decision.classification.value,
            "evolution_gate_proposal_id": evolution_decision.proposal_id,
        }
        return PromotionPackage(status, "eligible_after_all_governance_gates", learning_id.strip(), knowledge_key.strip(), payload)
