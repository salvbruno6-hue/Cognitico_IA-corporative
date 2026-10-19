"""Operational-intelligence readiness for ELO.

This module converts explicit operational evidence into governed health findings.
It distinguishes canonical operational records from governed external evidence
(e.g. a controlled PCP spreadsheet). External evidence can reduce uncertainty,
but it never masquerades as canonical persistence.

The module does not create operational records, infer missing production data,
authorize mutations, or promote learning. It reuses the canonical system-health
assessment so the Symbiont can observe and the Orchestrator can prioritize the
next evidence required.
"""
from __future__ import annotations

from dataclasses import dataclass

from elo.cognitive.system_health_assessment import (
    HealthSeverity,
    SystemHealthAssessment,
    SystemHealthFinding,
    assess_system_health,
)


@dataclass(frozen=True, slots=True)
class OperationalIntelligenceSignals:
    demand_history_rows: int
    demand_forecast_rows: int
    capacity_rule_rows: int
    capacity_daily_rows: int
    capacity_component_rows: int
    material_need_rows: int
    material_stock_rows: int
    plan_rows: int
    plan_line_rows: int
    production_order_rows: int
    production_operation_rows: int
    flow_event_rows: int
    modular_unit_rows: int
    learning_pcp_rows: int
    learning_flow_rows: int
    governed_external_capacity_rows: int = 0
    governed_external_capacity_ref: str | None = None
    evidence_ref: str = "supabase/health/elo_operational_intelligence_readiness.sql"

    def __post_init__(self) -> None:
        values = (
            self.demand_history_rows,
            self.demand_forecast_rows,
            self.capacity_rule_rows,
            self.capacity_daily_rows,
            self.capacity_component_rows,
            self.material_need_rows,
            self.material_stock_rows,
            self.plan_rows,
            self.plan_line_rows,
            self.production_order_rows,
            self.production_operation_rows,
            self.flow_event_rows,
            self.modular_unit_rows,
            self.learning_pcp_rows,
            self.learning_flow_rows,
            self.governed_external_capacity_rows,
        )
        if any(value < 0 for value in values):
            raise ValueError("operational intelligence signals cannot be negative")
        if not self.evidence_ref.strip():
            raise ValueError("evidence_ref is required")
        if self.governed_external_capacity_rows > 0 and not (
            self.governed_external_capacity_ref
            and self.governed_external_capacity_ref.strip()
        ):
            raise ValueError(
                "governed external capacity evidence requires explicit provenance"
            )


@dataclass(frozen=True, slots=True)
class OperationalIntelligenceReadiness:
    assessment: SystemHealthAssessment
    next_required_evidence: str | None
    feedback_loop_closed: bool
    canonical_mutation: bool = False

    def as_dict(self) -> dict[str, object]:
        return {
            "state": self.assessment.state.value,
            "score_percent": self.assessment.score_percent,
            "next_required_evidence": self.next_required_evidence,
            "feedback_loop_closed": self.feedback_loop_closed,
            "priority_findings": [item.finding_id for item in self.assessment.priority_findings],
            "canonical_mutation": self.canonical_mutation,
        }


def _finding(
    *,
    finding_id: str,
    dimension: str,
    severity: HealthSeverity,
    weight: float,
    owner: str,
    evidence_refs: tuple[str, ...],
    detail: str,
) -> SystemHealthFinding:
    return SystemHealthFinding(
        finding_id=finding_id,
        dimension=dimension,
        severity=severity,
        weight=weight,
        evidence_refs=evidence_refs,
        detail=detail,
        owner=owner,
    )


def _severity(passed: bool, *, review_when_false: bool = False) -> HealthSeverity:
    if passed:
        return HealthSeverity.PASS
    return HealthSeverity.REVIEW if review_when_false else HealthSeverity.GAP_HIGH


def assess_operational_intelligence_readiness(
    signals: OperationalIntelligenceSignals,
) -> OperationalIntelligenceReadiness:
    """Assess whether ELO has enough real operational evidence to learn safely.

    The chain is evaluated in operational order:
    demand -> capacity -> materials -> plan -> execution -> physical genealogy
    -> planned-vs-actual closure -> learning grounded in execution.

    Canonical capacity data produces PASS. Governed external capacity evidence
    produces REVIEW plus an explicit canonicalization requirement. This prevents
    a real empirical observation from being discarded while also preventing an
    external spreadsheet from silently becoming a competing source of truth.
    """
    demand_ready = signals.demand_history_rows > 0 or signals.demand_forecast_rows > 0
    canonical_capacity_ready = (
        signals.capacity_rule_rows > 0
        or signals.capacity_daily_rows > 0
        or signals.capacity_component_rows > 0
    )
    external_capacity_ready = signals.governed_external_capacity_rows > 0
    if canonical_capacity_ready:
        capacity_severity = HealthSeverity.PASS
        capacity_condition: str | None = None
    elif external_capacity_ready:
        capacity_severity = HealthSeverity.REVIEW
        capacity_condition = "capacity_canonicalization"
    else:
        capacity_severity = HealthSeverity.GAP_HIGH
        capacity_condition = "capacity_evidence"

    materials_ready = signals.material_need_rows > 0 and signals.material_stock_rows > 0
    planning_ready = signals.plan_rows > 0 and signals.plan_line_rows > 0
    execution_ready = (
        signals.production_order_rows > 0
        and (signals.production_operation_rows > 0 or signals.flow_event_rows > 0)
    )
    genealogy_ready = signals.modular_unit_rows > 0
    feedback_loop_closed = planning_ready and execution_ready and signals.flow_event_rows > 0
    learning_present = signals.learning_pcp_rows > 0 or signals.learning_flow_rows > 0
    learning_grounded = learning_present and feedback_loop_closed

    capacity_refs = (signals.evidence_ref,)
    if external_capacity_ready and signals.governed_external_capacity_ref:
        capacity_refs = (signals.evidence_ref, signals.governed_external_capacity_ref)

    checks: tuple[
        tuple[str, HealthSeverity, str | None, str, float, str, str, tuple[str, ...]], ...
    ] = (
        (
            "OP_INTEL_DEMAND_EVIDENCE",
            _severity(demand_ready),
            None if demand_ready else "demand_evidence",
            "operational_demand",
            5.0,
            "SKILL_PLANEJAMENTO_MULTITEINER",
            f"history={signals.demand_history_rows} forecast={signals.demand_forecast_rows}",
            (signals.evidence_ref,),
        ),
        (
            "OP_INTEL_CAPACITY_EVIDENCE",
            capacity_severity,
            capacity_condition,
            "operational_capacity",
            5.0,
            "SKILL_PLANEJAMENTO_MULTITEINER",
            (
                f"rules={signals.capacity_rule_rows} daily={signals.capacity_daily_rows} "
                f"components={signals.capacity_component_rows} "
                f"governed_external={signals.governed_external_capacity_rows}"
            ),
            capacity_refs,
        ),
        (
            "OP_INTEL_MATERIAL_EVIDENCE",
            _severity(materials_ready),
            None if materials_ready else "material_evidence",
            "operational_materials",
            4.0,
            "SKILL_PLANEJAMENTO_MULTITEINER",
            f"needs={signals.material_need_rows} stock={signals.material_stock_rows}",
            (signals.evidence_ref,),
        ),
        (
            "OP_INTEL_PLANNING_EVIDENCE",
            _severity(planning_ready),
            None if planning_ready else "planning_evidence",
            "operational_planning",
            5.0,
            "SKILL_PLANEJAMENTO_MULTITEINER",
            f"plans={signals.plan_rows} lines={signals.plan_line_rows}",
            (signals.evidence_ref,),
        ),
        (
            "OP_INTEL_EXECUTION_EVIDENCE",
            _severity(execution_ready),
            None if execution_ready else "execution_evidence",
            "operational_execution",
            6.0,
            "SKILL_PLANEJAMENTO_MULTITEINER",
            (
                f"orders={signals.production_order_rows} operations={signals.production_operation_rows} "
                f"events={signals.flow_event_rows}"
            ),
            (signals.evidence_ref,),
        ),
        (
            "OP_INTEL_PHYSICAL_GENEALOGY",
            _severity(genealogy_ready),
            None if genealogy_ready else "physical_genealogy",
            "operational_genealogy",
            4.0,
            "mt-data-governance",
            f"modular_units={signals.modular_unit_rows}",
            (signals.evidence_ref,),
        ),
        (
            "OP_INTEL_PLANNED_ACTUAL_CLOSURE",
            _severity(feedback_loop_closed),
            None if feedback_loop_closed else "planned_actual_closure",
            "operational_feedback",
            6.0,
            "SKILL_PLANEJAMENTO_MULTITEINER",
            (
                f"plan_lines={signals.plan_line_rows} orders={signals.production_order_rows} "
                f"flow_events={signals.flow_event_rows}"
            ),
            (signals.evidence_ref,),
        ),
        (
            "OP_INTEL_LEARNING_GROUNDED",
            _severity(
                learning_grounded,
                review_when_false=learning_present and not feedback_loop_closed,
            ),
            None if learning_grounded else "grounded_learning",
            "operational_learning",
            5.0,
            "ELO-SYMBIONT",
            (
                f"learning_pcp={signals.learning_pcp_rows} learning_flow={signals.learning_flow_rows} "
                f"feedback_loop_closed={feedback_loop_closed}"
            ),
            (signals.evidence_ref,),
        ),
    )

    findings = tuple(
        _finding(
            finding_id=finding_id,
            dimension=dimension,
            severity=severity,
            weight=weight,
            owner=owner,
            evidence_refs=evidence_refs,
            detail=detail,
        )
        for (
            finding_id,
            severity,
            _condition,
            dimension,
            weight,
            owner,
            detail,
            evidence_refs,
        ) in checks
    )
    assessment = assess_system_health(findings)
    next_required_evidence = next(
        (
            condition
            for (
                _finding_id,
                severity,
                condition,
                _dimension,
                _weight,
                _owner,
                _detail,
                _evidence_refs,
            ) in checks
            if severity is not HealthSeverity.PASS and condition is not None
        ),
        None,
    )
    return OperationalIntelligenceReadiness(
        assessment=assessment,
        next_required_evidence=next_required_evidence,
        feedback_loop_closed=feedback_loop_closed,
    )


__all__ = [
    "OperationalIntelligenceReadiness",
    "OperationalIntelligenceSignals",
    "assess_operational_intelligence_readiness",
]
