from elo.cognitive.symbiont_capability_evolution import CapabilityMetric, Curvature, curvature, review_capabilities
from scripts.run_symbiont_capability_evolution import metrics_from_production_runs


def test_positive_curvature_uses_measured_gain():
    metric = CapabilityMetric("validated_learning", 0.62, 0.74, "maximize", ("ev-1",), "2026-09")
    assert curvature(metric) is Curvature.POSITIVE
    assert metric.delta == 0.12


def test_minimize_metric_can_be_positive():
    metric = CapabilityMetric("rework_rate", 0.20, 0.16, "minimize", ("ev-2",), "2026-09")
    assert curvature(metric) is Curvature.POSITIVE


def test_missing_evidence_is_not_measured_and_generates_action():
    metric = CapabilityMetric("observability", 0.5, 0.6, "maximize")
    review = review_capabilities(metrics=(metric,))
    assert review.status == "NOT_MEASURED"
    assert curvature(metric) is Curvature.NOT_MEASURED
    assert review.actions[0].priority == "P1"


def test_regression_gets_bounded_correction_action():
    metric = CapabilityMetric("test_coverage", 0.90, 0.70, "maximize", ("ev-3",), "2026-09")
    review = review_capabilities(metrics=(metric,))
    assert curvature(metric) is Curvature.CRITICAL
    assert review.actions[0].priority == "P0"


def test_review_never_grants_canonical_mutation():
    review = review_capabilities(metrics=())
    assert review.trigger_id == "EVOLUÇÃO_DE_CAPACIDADES"
    assert review.canonical_mutation is False


def test_existing_evolution_measurement_shape_is_reused():
    metrics = CapabilityMetric.from_evolution_measurement(
        item="route", baseline={"success_rate": 0.80}, adapted={"success_rate": 0.88},
        metric_directions={"success_rate": "maximize"}, evidence_refs=("evolution-run-1",),
        measurement_period="2026-09",
    )
    assert len(metrics) == 1
    assert review_capabilities(metrics=metrics).actions[0].priority == "P3"


def test_not_measured_review_is_not_ready_for_analysis():
    metric = CapabilityMetric("coverage", None, None, "")
    assert review_capabilities(metrics=(metric,)).ready_for_analysis is False


def test_implementation_evidence_shape_is_reused_without_new_measurement_owner():
    metrics = CapabilityMetric.from_implementation_evidence(
        item="implementation_loop", baseline={"success_rate": 0.80}, adapted={"success_rate": 0.88},
        metric_directions={"success_rate": "maximize"}, provenance_refs=("implementation-run-1",),
        measurement_period="2026-09",
    )
    assert metrics[0].item == "implementation_loop:success_rate"
    assert curvature(metrics[0]) is Curvature.POSITIVE


def test_production_metric_feed_reuses_explicit_metrics_only():
    runs = (
        {"id": "run-001", "details": {"report": {"capability_metrics": [{
            "item": "validated_learning", "baseline": 0.62, "current": 0.74,
            "direction": "maximize", "evidence_refs": ["ev-001"], "measurement_period": "2026-09"}]}}},
        {"id": "run-002", "details": {"report": {"learning": {"experiences": 999}, "capability_metrics": []}}},
    )
    metrics = metrics_from_production_runs(runs)
    assert len(metrics) == 1
    assert metrics[0].item == "validated_learning"
    assert "elo_automation_runs:run-001" in metrics[0].evidence_refs


def test_production_feed_rejects_incomplete_metrics_without_fabricating_values():
    runs = ({"id": "run-invalid", "details": {"report": {"capability_metrics": [{
        "item": "coverage", "baseline": 0.8, "current": 0.7, "direction": "maximize",
        "evidence_refs": [], "measurement_period": ""}]}}},)
    assert metrics_from_production_runs(runs) == ()


def test_validated_downstream_experience_can_corroborate_a_capability():
    metric = CapabilityMetric.from_indirect_experience(
        item="Progressive Tool Schema Disclosure",
        baseline=0.80,
        current=0.88,
        direction="maximize",
        evidence_refs=("performance-evidence:hermes-001",),
        measurement_period="2026-09",
        observer_capability="ExecutionRouter",
        experience_ref="experience:execution-router-001",
    )
    review = review_capabilities(metrics=(metric,))
    assert metric.evidence_mode == "INDIRECT_EXPERIENCE"
    assert metric.observer_capability == "ExecutionRouter"
    assert metric.experience_ref == "experience:execution-router-001"
    assert curvature(metric) is Curvature.POSITIVE
    assert review.ready_for_analysis is True
    assert "Validated downstream observer: ExecutionRouter" in review.actions[0].rationale
    assert review.canonical_mutation is False


def test_indirect_experience_requires_explicit_observer_and_experience():
    try:
        CapabilityMetric.from_indirect_experience(
            item="Progressive Tool Schema Disclosure",
            baseline=0.80,
            current=0.88,
            direction="maximize",
            evidence_refs=("ev-1",),
            measurement_period="2026-09",
            observer_capability="",
            experience_ref="experience:1",
        )
    except ValueError as exc:
        assert "observer capability" in str(exc)
    else:
        raise AssertionError("missing observer must be rejected")
