from elo.cognitive.symbiont_capability_evolution import (
    CapabilityMetric,
    Curvature,
    curvature,
    review_capabilities,
)
from scripts.run_symbiont_capability_evolution import metrics_from_production_runs


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


def test_existing_evolution_measurement_shape_is_reused():
    metrics = CapabilityMetric.from_evolution_measurement(
        item="route",
        baseline={"success_rate": 0.80},
        adapted={"success_rate": 0.88},
        metric_directions={"success_rate": "maximize"},
        evidence_refs=("evolution-run-1",),
        measurement_period="2026-09",
    )
    assert len(metrics) == 1
    review = review_capabilities(metrics=metrics)
    assert review.status == "ANALYSIS_READY"
    assert review.actions[0].priority == "P3"


def test_not_measured_review_is_not_ready_for_analysis():
    metric = CapabilityMetric(item="coverage", baseline=None, current=None, direction="")
    review = review_capabilities(metrics=(metric,))
    assert review.ready_for_analysis is False


def test_implementation_evidence_shape_is_reused_without_new_measurement_owner():
    metrics = CapabilityMetric.from_implementation_evidence(
        item="implementation_loop",
        baseline={"success_rate": 0.80},
        adapted={"success_rate": 0.88},
        metric_directions={"success_rate": "maximize"},
        provenance_refs=("implementation-run-1",),
        measurement_period="2026-09",
    )
    assert len(metrics) == 1
    assert metrics[0].item == "implementation_loop:success_rate"
    assert metrics[0].evidence_refs == ("implementation-run-1",)
    assert curvature(metrics[0]) is Curvature.POSITIVE


def test_production_metric_feed_reuses_explicit_metrics_only():
    runs = (
        {
            "id": "run-001",
            "details": {
                "report": {
                    "capability_metrics": [
                        {
                            "item": "validated_learning",
                            "baseline": 0.62,
                            "current": 0.74,
                            "direction": "maximize",
                            "evidence_refs": ["ev-001"],
                            "measurement_period": "2026-09",
                        }
                    ]
                }
            },
        },
        {
            "id": "run-002",
            "details": {
                "report": {
                    "learning": {"experiences": 999},
                    "capability_metrics": [],
                }
            },
        },
    )
    metrics = metrics_from_production_runs(runs)
    assert len(metrics) == 1
    assert metrics[0].item == "validated_learning"
    assert "elo_automation_runs:run-001" in metrics[0].evidence_refs
