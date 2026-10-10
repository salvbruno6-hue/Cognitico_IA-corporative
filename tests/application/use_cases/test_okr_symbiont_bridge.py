from decimal import Decimal

import pytest

from elo.application.use_cases.okr_symbiont_bridge import OkrSymbiontBridge
from elo.core.decision_outcome_loop import DecisionLifecycle, DecisionState
from elo.core.okr_evaluation import KeyResultEvaluation, ValueTrend
from elo.core.systemic_primitives import DecisionRecord, OutcomeFeedback


def _evaluation():
    return KeyResultEvaluation(
        key_result_id="KR-1",
        baseline=Decimal("15"),
        target=Decimal("10"),
        current=Decimal("11"),
        progress_pct=Decimal("80"),
        trend=ValueTrend.DOWN,
        forecast=None,
        deviation=Decimal("1"),
        status="INDETERMINADO",
        confidence="OBSERVED",
        evidence_refs=("ev:kr",),
    )


def _attributed_lifecycle():
    lifecycle = DecisionLifecycle(
        decision=DecisionRecord(
            decision_id="DEC-1",
            decision="review production sequencing",
            rationale="lead time above target",
            evidence_ids=("ev:kr",),
            authority="PCP_MANAGER",
            expected_outcome="reduce lead time",
        )
    )
    lifecycle.transition(DecisionState.APPROVED, actor="human")
    lifecycle.transition(DecisionState.EXECUTED, actor="execution-boundary")
    lifecycle.transition(DecisionState.OBSERVING, actor="monitor")
    lifecycle.attach_outcome(
        OutcomeFeedback(
            decision_id="DEC-1",
            expected="reduce lead time",
            observed="lead time reduced to 11 days",
            variance="1 day above target",
            evidence_ids=("ev:outcome",),
        )
    )
    lifecycle.transition(DecisionState.EVALUATED, evidence_ids=("ev:outcome",), actor="evaluator")
    lifecycle.attach_attribution({"sequencing_change": 1.0})
    lifecycle.transition(DecisionState.ATTRIBUTED, evidence_ids=("ev:outcome",), actor="evaluator")
    return lifecycle


def test_bridge_creates_existing_symbiont_observation_without_learning_promotion():
    lifecycle = _attributed_lifecycle()

    observation = OkrSymbiontBridge().build_observation(
        lifecycle=lifecycle,
        evaluation=_evaluation(),
        tenant_id="tenant-a",
        objective_id="OBJ-1",
        observation_id="OBS-1",
        source_commit="abc123",
        hypothesis="sequencing change may improve lead time",
        experiment="compare pre/post lead time",
        regression_status="NOT_EVALUATED",
        generalization_status="UNCONFIRMED",
        risk="context-specific result",
    )

    assert observation.domain == "strategic_okr"
    assert observation.existing_owner == "strategic-objective-domain"
    assert set(observation.evidence_ids) == {"ev:kr", "ev:outcome"}
    assert lifecycle.state is DecisionState.ATTRIBUTED
    assert lifecycle.learning_candidate is None
    assert "objective:OBJ-1/key_result:KR-1" == observation.scope


def test_bridge_rejects_pre_attribution_lifecycle():
    lifecycle = DecisionLifecycle(
        decision=DecisionRecord(
            decision_id="DEC-1",
            decision="review production sequencing",
            rationale="lead time above target",
            evidence_ids=("ev:kr",),
        )
    )

    with pytest.raises(ValueError, match="attributed DecisionLifecycle"):
        OkrSymbiontBridge().build_observation(
            lifecycle=lifecycle,
            evaluation=_evaluation(),
            tenant_id="tenant-a",
            objective_id="OBJ-1",
            observation_id="OBS-1",
            source_commit="abc123",
            hypothesis="hypothesis",
            experiment="experiment",
            regression_status="NOT_EVALUATED",
            generalization_status="UNCONFIRMED",
            risk="unknown",
        )
