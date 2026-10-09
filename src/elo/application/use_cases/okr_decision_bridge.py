"""Bridge OKR evaluation to existing ELO diagnosis/decision/outcome owners.

Layer: cognitive
Owner: strategic-objective-domain (bridge); ELO Core retains decision authority
Status: implemented
Authority: implementation
Related: CausalAssessment, DecisionRecord, DecisionLifecycle, OutcomeFeedback

No OKR-specific decision lifecycle is introduced. This bridge only translates
an evidence-backed KR evaluation into canonical Core primitives.
"""
from __future__ import annotations

from dataclasses import dataclass

from elo.core.decision_outcome_loop import DecisionLifecycle
from elo.core.okr_evaluation import KeyResultEvaluation
from elo.core.systemic_primitives import CausalAssessment, DecisionRecord


@dataclass(frozen=True, slots=True)
class OkrDiagnosis:
    key_result_id: str
    assessment: CausalAssessment


class OkrDecisionBridge:
    def diagnose(
        self,
        *,
        evaluation: KeyResultEvaluation,
        cause: str,
        effect: str,
        confidence: float,
        evidence_ids: tuple[str, ...],
        assumptions: tuple[str, ...] = (),
    ) -> OkrDiagnosis:
        if evaluation.deviation is None:
            raise ValueError("diagnosis requires an observed KR deviation")
        if not evidence_ids:
            raise ValueError("diagnosis requires evidence")
        if not set(evidence_ids).issubset(set(evaluation.evidence_refs)):
            raise ValueError("diagnosis evidence must be contained in the KR evaluation evidence")
        return OkrDiagnosis(
            key_result_id=evaluation.key_result_id,
            assessment=CausalAssessment(
                cause=cause,
                effect=effect,
                confidence=confidence,
                evidence_ids=evidence_ids,
                assumptions=assumptions,
            ),
        )

    def propose_action(
        self,
        *,
        evaluation: KeyResultEvaluation,
        decision_id: str,
        action: str,
        rationale: str,
        authority: str | None,
        expected_outcome: str,
        evidence_ids: tuple[str, ...],
    ) -> DecisionLifecycle:
        if not evidence_ids:
            raise ValueError("action proposal requires evidence")
        if not set(evidence_ids).issubset(set(evaluation.evidence_refs)):
            raise ValueError("action evidence must be contained in the KR evaluation evidence")

        record = DecisionRecord(
            decision_id=decision_id,
            decision=action,
            rationale=rationale,
            impact=(f"key_result:{evaluation.key_result_id}",),
            evidence_ids=evidence_ids,
            authority=authority,
            expected_outcome=expected_outcome,
        )
        return DecisionLifecycle(decision=record)


__all__ = ["OkrDecisionBridge", "OkrDiagnosis"]
