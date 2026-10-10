"""Controlled Symbiont Lab comparison for OKR forecast/scenario candidates.

Repository-owned simulation only. This test does not create operational evidence,
authorize execution, promote learning, or create a second forecast/scenario owner.
"""
from decimal import Decimal

from elo.core.forecasting import (
    ForecastObservation,
    ForecastStatus,
    GovernedForecastFaculty,
)
from elo.core.scenario_engine import Scenario, ScenarioAssumption, ScenarioOutcome


def _observation(period: str, value: str) -> ForecastObservation:
    return ForecastObservation.create(
        period=period,
        value=value,
        source_id=f"evidence-{period}",
        provenance={"source": "symbiont-lab", "kind": "okr-measurement-simulation"},
    )


def test_forecast_candidate_adds_bounded_reproducible_signal_without_execution_authority():
    observations = (
        _observation("2026-07", "40"),
        _observation("2026-08", "50"),
        _observation("2026-09", "60"),
    )

    result = GovernedForecastFaculty.forecast(
        observations=observations,
        target_period="2026-10",
        window=3,
    )

    assert result.status is ForecastStatus.COMPLETE
    assert result.forecast == Decimal("50.00")
    assert result.reproducible is True
    assert result.method == "ARITHMETIC_MEAN_V1"
    assert result.evidence_ids == (
        "evidence-2026-07",
        "evidence-2026-08",
        "evidence-2026-09",
    )


def test_forecast_candidate_fails_closed_when_okr_history_is_insufficient():
    result = GovernedForecastFaculty.forecast(
        observations=(
            _observation("2026-08", "50"),
            _observation("2026-09", "60"),
        ),
        target_period="2026-10",
        window=3,
    )

    assert result.status is ForecastStatus.GAP
    assert result.forecast is None
    assert result.reproducible is False
    assert result.gap == "at least 3 governed observations are required"


def test_scenario_candidate_adds_bounded_consequence_analysis_without_action_execution():
    scenario = Scenario(
        id="okr-kr-risk-001",
        assumptions=(
            ScenarioAssumption(key="forecast", value="50.00"),
            ScenarioAssumption(key="target", value="80.00"),
            ScenarioAssumption(key="deadline", value="2026-10"),
        ),
    )

    evaluated = scenario.add_outcome(
        ScenarioOutcome(
            scenario_id=scenario.id,
            description="Forecast remains below KR target at the evaluated horizon",
            confidence=0.80,
            affected_ids=("objective-001", "kr-001"),
        )
    )

    assert scenario.outcomes == ()
    assert len(evaluated.outcomes) == 1
    assert evaluated.outcomes[0].affected_ids == ("objective-001", "kr-001")
    assert evaluated.outcomes[0].confidence == 0.80


def test_scenario_candidate_rejects_invalid_confidence_instead_of_inventing_certainty():
    try:
        ScenarioOutcome(
            scenario_id="okr-kr-risk-001",
            description="invalid certainty",
            confidence=1.1,
        )
    except ValueError as exc:
        assert str(exc) == "confidence must be between 0 and 1"
    else:
        raise AssertionError("ScenarioOutcome must reject confidence outside [0, 1]")
