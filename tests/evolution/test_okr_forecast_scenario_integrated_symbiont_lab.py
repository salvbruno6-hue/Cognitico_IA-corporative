"""Integrated controlled Symbiont Lab for strategic_okr + Forecast + Scenario.

Repository-owned simulation only. The composition uses existing owners and does
not authorize execution, fabricate operational proof, or promote learning.
"""
from dataclasses import replace
from decimal import Decimal

from elo.application.use_cases.okr_symbiont_bridge import OkrSymbiontBridge
from elo.core.decision_outcome_loop import DecisionLifecycle, DecisionState
from elo.core.forecasting import ForecastObservation, ForecastStatus, GovernedForecastFaculty
from elo.core.okr_evaluation import KeyResultEvaluation, ValueTrend
from elo.core.scenario_engine import Scenario, ScenarioAssumption, ScenarioOutcome
from elo.core.systemic_primitives import DecisionRecord, OutcomeFeedback


def _forecast_observation(period: str, value: str) -> ForecastObservation:
    return ForecastObservation.create(
        period=period,
        value=value,
        source_id=f"ev:{period}",
        provenance={"source": "symbiont-lab", "kind": "okr-measurement-simulation"},
    )


def _attributed_lifecycle(evidence_ids: tuple[str, ...]) -> DecisionLifecycle:
    lifecycle = DecisionLifecycle(
        decision=DecisionRecord(
            decision_id="DEC-OKR-FORECAST-1",
            decision="review KR trajectory before human intervention",
            rationale="forecast is below the approved KR target",
            evidence_ids=evidence_ids,
            authority="PCP_MANAGER",
            expected_outcome="improve KR trajectory",
        )
    )
    lifecycle.transition(DecisionState.APPROVED, actor="human")
    lifecycle.transition(DecisionState.EXECUTED, actor="execution-boundary")
    lifecycle.transition(DecisionState.OBSERVING, actor="monitor")
    lifecycle.attach_outcome(
        OutcomeFeedback(
            decision_id="DEC-OKR-FORECAST-1",
            expected="improve KR trajectory",
            observed="trajectory reviewed in controlled laboratory",
            variance="productive effect not established",
            evidence_ids=("ev:lab-outcome",),
        )
    )
    lifecycle.transition(DecisionState.EVALUATED, evidence_ids=("ev:lab-outcome",), actor="evaluator")
    lifecycle.attach_attribution({"controlled_lab_composition": 1.0})
    lifecycle.transition(DecisionState.ATTRIBUTED, evidence_ids=("ev:lab-outcome",), actor="evaluator")
    return lifecycle


def test_strategic_okr_forecast_scenario_reaches_existing_symbiont_bridge_without_learning():
    base_evaluation = KeyResultEvaluation(
        key_result_id="KR-FORECAST-1",
        baseline=Decimal("40"),
        target=Decimal("80"),
        current=Decimal("60"),
        progress_pct=Decimal("50"),
        trend=ValueTrend.UP,
        forecast=None,
        deviation=Decimal("-20"),
        status="INDETERMINADO",
        confidence="OBSERVED",
        evidence_refs=("ev:2026-07", "ev:2026-08", "ev:2026-09"),
    )

    forecast = GovernedForecastFaculty.forecast(
        observations=(
            _forecast_observation("2026-07", "40"),
            _forecast_observation("2026-08", "50"),
            _forecast_observation("2026-09", "60"),
        ),
        target_period="2026-10",
        window=3,
    )
    assert forecast.status is ForecastStatus.COMPLETE
    assert forecast.reproducible is True

    evaluation = replace(base_evaluation, forecast=forecast.forecast)
    assert evaluation.forecast == Decimal("50.00")
    assert evaluation.status == "INDETERMINADO"

    scenario = Scenario(
        id="SCN-OKR-FORECAST-1",
        assumptions=(
            ScenarioAssumption(key="forecast", value=str(evaluation.forecast)),
            ScenarioAssumption(key="target", value=str(evaluation.target)),
            ScenarioAssumption(key="deadline", value="2026-10"),
        ),
    ).add_outcome(
        ScenarioOutcome(
            scenario_id="SCN-OKR-FORECAST-1",
            description="Forecast remains below KR target at evaluated horizon",
            confidence=0.80,
            affected_ids=("OBJ-FORECAST-1", evaluation.key_result_id),
        )
    )
    assert scenario.outcomes[0].affected_ids == ("OBJ-FORECAST-1", "KR-FORECAST-1")

    lifecycle = _attributed_lifecycle(forecast.evidence_ids)
    observation = OkrSymbiontBridge().build_observation(
        lifecycle=lifecycle,
        evaluation=evaluation,
        tenant_id="tenant-lab",
        objective_id="OBJ-FORECAST-1",
        observation_id="OBS-OKR-FORECAST-1",
        source_commit="81a98928036dbd188ae8aa409bfcff9d650b58e3",
        hypothesis="bounded forecast plus scenario may improve strategic diagnosis",
        experiment="compose strategic_okr evaluation, governed forecast, scenario consequence and existing Symbiont bridge",
        regression_status="PASS",
        generalization_status="UNCONFIRMED",
        risk="controlled simulation only; no productive OKR outcome evidence",
    )

    assert observation.domain == "strategic_okr"
    assert observation.existing_owner == "strategic-objective-domain"
    assert observation.generalization_status == "UNCONFIRMED"
    assert lifecycle.learning_candidate is None
    assert set(forecast.evidence_ids).issubset(set(observation.evidence_ids))


def test_integrated_composition_fails_closed_before_scenario_when_forecast_has_gap():
    forecast = GovernedForecastFaculty.forecast(
        observations=(
            _forecast_observation("2026-08", "50"),
            _forecast_observation("2026-09", "60"),
        ),
        target_period="2026-10",
        window=3,
    )

    assert forecast.status is ForecastStatus.GAP
    assert forecast.forecast is None
    assert forecast.reproducible is False
    assert forecast.gap == "at least 3 governed observations are required"
