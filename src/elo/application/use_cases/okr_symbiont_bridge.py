"""OKR experience handoff to the existing Symbiont laboratory contract.

Layer: cognitive
Owner: Symbiont laboratory (authority) / strategic-objective-domain (bridge)
Status: implemented
Authority: implementation
Related: DecisionLifecycle, SymbiontLabObservation, Learning Governance

This bridge does not evaluate, promote or learn. It only creates a laboratory
observation from an already evaluated and attributed decision outcome.
"""
from __future__ import annotations

from elo.cognitive.symbionte_lab import SymbiontLabObservation
from elo.core.decision_outcome_loop import DecisionLifecycle, DecisionState
from elo.core.okr_evaluation import KeyResultEvaluation


class OkrSymbiontBridge:
    def build_observation(
        self,
        *,
        lifecycle: DecisionLifecycle,
        evaluation: KeyResultEvaluation,
        tenant_id: str,
        objective_id: str,
        observation_id: str,
        source_commit: str,
        hypothesis: str,
        experiment: str,
        regression_status: str,
        generalization_status: str,
        risk: str,
    ) -> SymbiontLabObservation:
        if lifecycle.state is not DecisionState.ATTRIBUTED:
            raise ValueError("Symbiont observation requires an attributed DecisionLifecycle")
        if lifecycle.outcome is None:
            raise ValueError("Symbiont observation requires an attached outcome")
        if not lifecycle.attribution:
            raise ValueError("Symbiont observation requires explicit attribution")
        if not lifecycle.outcome.evidence_ids:
            raise ValueError("Symbiont observation requires outcome evidence")
        if not source_commit.strip():
            raise ValueError("Symbiont observation requires source_commit")

        observation_evidence = tuple(
            dict.fromkeys([
                *evaluation.evidence_refs,
                *lifecycle.outcome.evidence_ids,
            ])
        )
        if not observation_evidence:
            raise ValueError("Symbiont observation requires evidence")

        expected = lifecycle.decision.expected_outcome or lifecycle.outcome.expected
        observed = lifecycle.outcome.observed
        baseline = (
            f"baseline={evaluation.baseline}; target={evaluation.target}; current={evaluation.current}; "
            f"progress={evaluation.progress_pct}; trend={evaluation.trend.value}; status={evaluation.status}"
        )
        result = (
            f"objective={objective_id}; key_result={evaluation.key_result_id}; "
            f"expected={expected}; observed={observed}; deviation={evaluation.deviation}"
        )

        return SymbiontLabObservation(
            observation_id=observation_id,
            tenant_id=tenant_id,
            domain="strategic_okr",
            decision_id=lifecycle.decision.decision_id,
            expected_outcome=expected,
            observed_outcome=observed,
            evidence_ids=observation_evidence,
            source_ref=lifecycle.decision.decision_id,
            source_commit=source_commit,
            hypothesis=hypothesis,
            baseline=baseline,
            experiment=experiment,
            result=result,
            regression_status=regression_status,
            generalization_status=generalization_status,
            risk=risk,
            existing_owner="strategic-objective-domain",
            scope=f"objective:{objective_id}/key_result:{evaluation.key_result_id}",
            tenant_scope=tenant_id,
            source_kind="okr_decision_outcome",
        )


__all__ = ["OkrSymbiontBridge"]
