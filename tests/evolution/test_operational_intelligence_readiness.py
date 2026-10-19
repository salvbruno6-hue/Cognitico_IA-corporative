from dataclasses import asdict

from elo.cognitive.operational_intelligence_readiness import (
    OperationalIntelligenceSignals,
    assess_operational_intelligence_readiness,
)
from elo.cognitive.system_health_assessment import HealthSeverity


def empty_live_signals() -> OperationalIntelligenceSignals:
    return OperationalIntelligenceSignals(
        demand_history_rows=0,
        demand_forecast_rows=0,
        capacity_rule_rows=0,
        capacity_daily_rows=0,
        capacity_component_rows=0,
        material_need_rows=0,
        material_stock_rows=0,
        plan_rows=0,
        plan_line_rows=0,
        production_order_rows=0,
        production_operation_rows=0,
        flow_event_rows=0,
        modular_unit_rows=0,
        learning_pcp_rows=2,
        learning_flow_rows=1,
    )


def test_live_operational_gap_is_fail_closed_and_prioritized():
    readiness = assess_operational_intelligence_readiness(empty_live_signals())

    assert readiness.feedback_loop_closed is False
    assert readiness.next_required_evidence == "demand_evidence"
    assert readiness.canonical_mutation is False
    findings = {item.finding_id: item for item in readiness.assessment.findings}
    assert findings["OP_INTEL_DEMAND_EVIDENCE"].severity is HealthSeverity.GAP_HIGH
    assert findings["OP_INTEL_EXECUTION_EVIDENCE"].severity is HealthSeverity.GAP_HIGH
    assert findings["OP_INTEL_LEARNING_GROUNDED"].severity is HealthSeverity.REVIEW
    assert readiness.assessment.score_percent is not None
    assert readiness.assessment.score_percent < 50


def test_complete_chain_closes_feedback_loop_without_authorizing_mutation():
    readiness = assess_operational_intelligence_readiness(
        OperationalIntelligenceSignals(
            demand_history_rows=120,
            demand_forecast_rows=20,
            capacity_rule_rows=5,
            capacity_daily_rows=60,
            capacity_component_rows=10,
            material_need_rows=200,
            material_stock_rows=180,
            plan_rows=4,
            plan_line_rows=40,
            production_order_rows=30,
            production_operation_rows=120,
            flow_event_rows=500,
            modular_unit_rows=80,
            learning_pcp_rows=12,
            learning_flow_rows=8,
        )
    )

    assert readiness.feedback_loop_closed is True
    assert readiness.next_required_evidence is None
    assert readiness.assessment.score_percent == 100.0
    assert readiness.canonical_mutation is False
    assert all(item.severity is HealthSeverity.PASS for item in readiness.assessment.findings)


def test_learning_without_execution_is_review_not_false_validated_learning():
    readiness = assess_operational_intelligence_readiness(empty_live_signals())
    learning = next(
        item
        for item in readiness.assessment.findings
        if item.finding_id == "OP_INTEL_LEARNING_GROUNDED"
    )

    assert learning.severity is HealthSeverity.REVIEW
    assert "feedback_loop_closed=False" in learning.detail


def test_negative_counts_are_rejected():
    values = asdict(empty_live_signals())
    values["plan_rows"] = -1

    try:
        OperationalIntelligenceSignals(**values)
    except ValueError as exc:
        assert "cannot be negative" in str(exc)
    else:
        raise AssertionError("negative operational counts must fail closed")
