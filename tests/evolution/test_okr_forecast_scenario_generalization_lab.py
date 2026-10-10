"""Independent generalization trial for the OKR Forecast + Scenario composition.

This trial deliberately changes trajectory, direction and horizon from the first
laboratory experiment. It can support PARTIAL generalization only when the
existing mechanisms remain bounded and fail-closed; it is not production proof.
"""
from decimal import Decimal

from elo.core.forecasting import ForecastObservation, ForecastStatus, GovernedForecastFaculty
from elo.core.scenario_engine import Scenario, ScenarioAssumption, ScenarioOutcome


def _observation(period: str, value: str) -> ForecastObservation:
    return ForecastObservation.create(
        period=period,
        value=value,
        source_id=f"ev:independent:{period}",
        provenance={
            "source": "symbiont-lab-independent-trial",
            "kind": "okr-measurement-simulation",
        },
    )


def test_independent_decreasing_kr_trajectory_preserves_forecast_and_scenario_boundaries():
    """Second context: decreasing KR, different values and a longer evidence window."""
    result = GovernedForecastFaculty.forecast(
        observations=(
            _observation("2026-Q1", "18"),
            _observation("2026-Q2", "15"),
            _observation("2026-Q3", "12"),
            _observation("2026-Q4", "9"),
        ),
        target_period="2027-Q1",
        window=4,
    )

    assert result.status is ForecastStatus.COMPLETE
    assert result.forecast == Decimal("13.50")
    assert result.reproducible is True
    assert len(result.evidence_ids) == 4

    scenario = Scenario(
        id="SCN-OKR-INDEPENDENT-1",
        assumptions=(
            ScenarioAssumption(key="direction", value="DECREASE"),
            ScenarioAssumption(key="forecast", value=str(result.forecast)),
            ScenarioAssumption(key="target", value="8"),
            ScenarioAssumption(key="horizon", value="2027-Q1"),
        ),
    ).add_outcome(
        ScenarioOutcome(
            scenario_id="SCN-OKR-INDEPENDENT-1",
            description="Bounded forecast remains above the decreasing KR target",
            confidence=0.70,
            affected_ids=("OBJ-INDEPENDENT-1", "KR-INDEPENDENT-1"),
        )
    )

    assert scenario.outcomes[0].confidence == 0.70
    assert scenario.outcomes[0].affected_ids == ("OBJ-INDEPENDENT-1", "KR-INDEPENDENT-1")


def test_independent_trial_still_fails_closed_when_evidence_window_is_not_met():
    result = GovernedForecastFaculty.forecast(
        observations=(
            _observation("2026-Q3", "12"),
            _observation("2026-Q4", "9"),
        ),
        target_period="2027-Q1",
        window=4,
    )

    assert result.status is ForecastStatus.GAP
    assert result.forecast is None
    assert result.reproducible is False
    # The fail-closed requirement follows the requested governed window.
    assert result.gap == "at least 4 governed observations are required"
