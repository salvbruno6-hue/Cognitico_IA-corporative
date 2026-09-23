from elo.cognitive.symbiont_capability_evolution import (
    CapabilityMetric,
    Curvature,
    curvature,
    review_capabilities,
)


def test_positive_curvature_uses_measured_gain():
    metric = CapabilityMetric(
        item="validated_learning",
        baseline=0.62,
        current=0.74,
        direction="maximize",
        evidence_refs=("ev-1",),
        measurement_period="2026-09",
    )
    assert curvature(metric) is Curvature.POSITIVE
    assert metric.delta == 0.12


def test_minimize_metric_can_be_positive():
    metric = CapabilityMetric(
        item="rework_rate",
        baseline=0.20,
        current=0.16,
        direction="minimize",
        evidence_refs=("ev-2",),
        measurement_period="2026-09",
    )
    assert curvature(metric) is Curvature.POSITIVE


def test_missing_evidence_is_not_measured_and_generates_action():
    metric = CapabilityMetric(
        item="observability",
        baseline=0.5,
        current=0.6,
        direction="maximize",
    )
    review = review_capabilities(metrics=(metric,))
    assert review.status == "NOT_MEASURED"
    assert curvature(metric) is Curvature.NOT_MEASURED
    assert review.actions[0].priority == "P1"


def test_regression_gets_bounded_correction_action():
    metric = CapabilityMetric(
        item="test_coverage",
        baseline=0.90,
        current=0.70,
        direction="maximize",
        evidence_refs=("ev-3",),
        measurement_period="2026-09",
    )
    review = review_capabilities(metrics=(metric,))
    assert curvature(metric) is Curvature.CRITICAL
    assert review.actions[0].priority == "P0"
    assert "regression" in review.actions[0].start_here.lower()


def test_review_never_grants_canonical_mutation():
    review = review_capabilities(metrics=())
    assert review.trigger_id == "EVOLUÇÃO_DE_CAPACIDADES"
    assert review.canonical_mutation is False
