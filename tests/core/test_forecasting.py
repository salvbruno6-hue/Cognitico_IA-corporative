from decimal import Decimal

from elo.core.forecasting import ForecastStatus, ForecastObservation, GovernedForecastFaculty


def obs(period: str, value: int, source: str) -> ForecastObservation:
    return ForecastObservation.create(
        period=period,
        value=value,
        source_id=source,
        provenance={"origin": f"source:{source}"},
    )


def test_forecast_requires_governed_evidence_and_returns_reproducible_mean():
    result = GovernedForecastFaculty.forecast(
        observations=(obs("p1", 100, "s1"), obs("p2", 120, "s2"), obs("p3", 140, "s3")),
        target_period="p4",
        window=3,
    )
    assert result.status is ForecastStatus.COMPLETE
    assert result.forecast == Decimal("120.00")
    assert result.method == "ARITHMETIC_MEAN_V1"
    assert result.reproducible is True
    assert result.evidence_ids == ("s1", "s2", "s3")


def test_forecast_with_insufficient_history_is_gap_not_zero_or_guess():
    result = GovernedForecastFaculty.forecast(
        observations=(obs("p1", 100, "s1"), obs("p2", 120, "s2")),
        target_period="p3",
        window=3,
    )
    assert result.status is ForecastStatus.GAP
    assert result.forecast is None
    assert result.gap


def test_forecast_uses_only_requested_window_and_preserves_provenance():
    result = GovernedForecastFaculty.forecast(
        observations=(
            obs("p1", 10, "s1"),
            obs("p2", 20, "s2"),
            obs("p3", 30, "s3"),
            obs("p4", 50, "s4"),
        ),
        target_period="p5",
        window=2,
    )
    assert result.forecast == Decimal("40.00")
    assert result.observation_ids == ("p3", "p4")
    assert result.evidence_ids == ("s3", "s4")
    assert result.provenance[0]["origin"] == "source:s3"
