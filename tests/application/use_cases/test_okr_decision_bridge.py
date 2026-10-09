from decimal import Decimal

import pytest

from elo.application.use_cases.okr_decision_bridge import OkrDecisionBridge
from elo.core.decision_outcome_loop import DecisionState
from elo.core.okr_evaluation import KeyResultEvaluation, ValueTrend


def _evaluation(*, deviation=Decimal("2"), evidence_refs=("ev:kr",)):
    return KeyResultEvaluation(
        key_result_id="KR-1",
        baseline=Decimal("15"),
        target=Decimal("10"),
        current=Decimal("12"),
        progress_pct=Decimal("60"),
        trend=ValueTrend.DOWN,
        forecast=None,
        deviation=deviation,
        status="INDETERMINADO",
        confidence="OBSERVED",
        evidence_refs=evidence_refs,
    )


def test_diagnosis_reuses_causal_assessment_and_requires_kr_evidence():
    bridge = OkrDecisionBridge()

    diagnosis = bridge.diagnose(
        evaluation=_evaluation(),
        cause="capacity constraint",
        effect="lead time remains above target",
        confidence=0.8,
        evidence_ids=("ev:kr",),
    )

    assert diagnosis.key_result_id == "KR-1"
    assert diagnosis.assessment.cause == "capacity constraint"
    assert diagnosis.assessment.evidence_ids == ("ev:kr",)


def test_diagnosis_requires_observed_deviation():
    bridge = OkrDecisionBridge()

    with pytest.raises(ValueError, match="requires an observed KR deviation"):
        bridge.diagnose(
            evaluation=_evaluation(deviation=None),
            cause="unknown",
            effect="unknown",
            confidence=0.2,
            evidence_ids=("ev:kr",),
        )


def test_action_proposal_returns_existing_decision_lifecycle_in_proposed_state():
    bridge = OkrDecisionBridge()

    lifecycle = bridge.propose_action(
        evaluation=_evaluation(),
        decision_id="DEC-1",
        action="review production sequencing",
        rationale="lead time is above approved target",
        authority="PCP_MANAGER",
        expected_outcome="reduce lead time",
        evidence_ids=("ev:kr",),
    )

    assert lifecycle.state is DecisionState.PROPOSED
    assert lifecycle.decision.decision_id == "DEC-1"
    assert lifecycle.decision.impact == ("key_result:KR-1",)
    assert lifecycle.learning_candidate is None
    assert lifecycle.outcome is None


def test_action_proposal_rejects_evidence_not_present_in_kr_evaluation():
    bridge = OkrDecisionBridge()

    with pytest.raises(ValueError, match="contained in the KR evaluation evidence"):
        bridge.propose_action(
            evaluation=_evaluation(),
            decision_id="DEC-1",
            action="review production sequencing",
            rationale="lead time is above target",
            authority="PCP_MANAGER",
            expected_outcome="reduce lead time",
            evidence_ids=("ev:other",),
        )
