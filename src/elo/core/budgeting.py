"""Governed corporate budgeting capability for the canonical ELO Core.

This module is a bounded capability, not a second cognitive core or financial
authority. It reuses the repository's existing evidence/decision/outcome
contracts conceptually and keeps budget versions immutable.

Important invariants:
- missing data is a GAP, never zero;
- committed resources are not treated as available resources;
- every calculable input carries source/provenance;
- calculations are reproducible from versioned formulas and inputs;
- scenarios/sensitivities do not mutate canonical inputs;
- recommendation is distinct from approval/commit/execute;
- contextual budget experience remains outside canonical identity/Core unless
  the existing governed learning path promotes a generalizable result.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from decimal import Decimal, InvalidOperation
from enum import StrEnum
from typing import Mapping, Sequence
from uuid import uuid4

from elo.core.outcome_feedback import OutcomeFeedback


class BudgetInputClass(StrEnum):
    FACT = "FACT"
    COMMITTED = "COMMITTED"
    AVAILABLE = "AVAILABLE"
    ASSUMPTION = "ASSUMPTION"
    ESTIMATE = "ESTIMATE"
    HYPOTHESIS = "HYPOTHESIS"
    GAP = "GAP"
    CONFLICT = "CONFLICT"


class BudgetLineType(StrEnum):
    COST = "COST"
    REVENUE = "REVENUE"
    RESOURCE = "RESOURCE"


class BudgetStatus(StrEnum):
    COMPLETE = "COMPLETE"
    CONDITIONAL = "CONDITIONAL"
    CONSTRAINED = "CONSTRAINED"
    BLOCKED = "BLOCKED"


class BudgetAuthority(StrEnum):
    PREPARE = "PREPARE"
    CALCULATE = "CALCULATE"
    RECOMMEND = "RECOMMEND"
    APPROVE = "APPROVE"
    COMMIT = "COMMIT"
    EXECUTE = "EXECUTE"


class BudgetScenarioKind(StrEnum):
    BASELINE = "BASELINE"
    CONSERVATIVE = "CONSERVATIVE"
    STRESS = "STRESS"
    COUNTERFACTUAL = "COUNTERFACTUAL"
    SENSITIVITY = "SENSITIVITY"


FORMULA_ID = "QUANTITY_X_UNIT_COST"
FORMULA_VERSION = "1.0"


class BudgetingError(ValueError):
    """Base error for governed budgeting boundary violations."""


class BudgetAuthorizationError(BudgetingError):
    """Raised when an action exceeds the supplied authority."""


@dataclass(frozen=True, slots=True)
class BudgetRequest:
    request_id: str
    tenant_id: str
    principal_id: str
    domain: str
    period: str
    objective: str
    scope: str


@dataclass(frozen=True, slots=True)
class BudgetInput:
    input_id: str
    tenant_id: str
    domain: str
    name: str
    classification: BudgetInputClass
    value: Decimal | None
    unit: str
    source_id: str
    provenance: Mapping[str, str]
    valid_from: str | None = None
    valid_to: str | None = None

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        domain: str,
        name: str,
        classification: BudgetInputClass,
        value: Decimal | int | float | str | None,
        unit: str,
        source_id: str,
        provenance: Mapping[str, str],
        input_id: str | None = None,
        valid_from: str | None = None,
        valid_to: str | None = None,
    ) -> "BudgetInput":
        if not tenant_id or not domain or not name or not unit:
            raise BudgetingError("tenant_id, domain, name and unit are required")
        if not source_id or not provenance:
            raise BudgetingError("source_id and provenance are required")
        parsed: Decimal | None
        if value is None:
            parsed = None
        else:
            try:
                parsed = Decimal(str(value))
            except (InvalidOperation, ValueError) as exc:
                raise BudgetingError(f"invalid numeric input: {value!r}") from exc
        return cls(
            input_id=input_id or str(uuid4()),
            tenant_id=tenant_id,
            domain=domain,
            name=name,
            classification=classification,
            value=parsed,
            unit=unit,
            source_id=source_id,
            provenance=dict(provenance),
            valid_from=valid_from,
            valid_to=valid_to,
        )


@dataclass(frozen=True, slots=True)
class Assumption:
    assumption_id: str
    statement: str
    evidence_ids: tuple[str, ...]
    provenance: Mapping[str, str]
    valid_from: str | None = None
    valid_to: str | None = None


@dataclass(frozen=True, slots=True)
class CapacityConstraint:
    constraint_id: str
    resource: str
    required: Decimal
    available: Decimal
    unit: str
    source_id: str
    provenance: Mapping[str, str]

    @property
    def constrained(self) -> bool:
        return self.required > self.available


@dataclass(frozen=True, slots=True)
class CostComponent:
    component_id: str
    input_ids: tuple[str, ...]
    amount: Decimal | None
    formula_id: str
    formula_version: str
    source_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class BudgetLine:
    line_id: str
    description: str
    line_type: BudgetLineType
    quantity_input_id: str
    unit_cost_input_id: str
    formula_id: str = FORMULA_ID
    formula_version: str = FORMULA_VERSION
    component: CostComponent | None = None
    amount: Decimal | None = None
    status: BudgetStatus = BudgetStatus.COMPLETE
    gap: str | None = None


@dataclass(frozen=True, slots=True)
class BudgetScenario:
    scenario_id: str
    name: str
    kind: BudgetScenarioKind
    overrides: Mapping[str, Decimal]
    rationale: str


@dataclass(frozen=True, slots=True)
class BudgetSensitivity:
    sensitivity_id: str
    input_id: str
    base_value: Decimal | None
    tested_value: Decimal | None
    effect: Decimal | None
    unit: str
    rationale: str


@dataclass(frozen=True, slots=True)
class BudgetFollowUp:
    follow_up_id: str
    request_id: str
    gap: str
    responsible_domain: str | None
    required_evidence: str
    state: str = "WAITING_FEEDBACK"


@dataclass(frozen=True, slots=True)
class BudgetVersion:
    version_id: str
    request_id: str
    version_number: int
    tenant_id: str
    period: str
    inputs: tuple[BudgetInput, ...]
    lines: tuple[BudgetLine, ...]
    assumptions: tuple[Assumption, ...]
    capacity_constraints: tuple[CapacityConstraint, ...]
    follow_ups: tuple[BudgetFollowUp, ...]
    scenarios: tuple[BudgetScenario, ...]
    sensitivities: tuple[BudgetSensitivity, ...]
    formula_id: str
    formula_version: str
    known_cost_subtotal: Decimal
    known_revenue_subtotal: Decimal
    total_cost: Decimal | None
    total_revenue: Decimal | None
    gross_margin: Decimal | None
    gross_margin_pct: Decimal | None
    status: BudgetStatus
    evidence_ids: tuple[str, ...]
    provenance: tuple[Mapping[str, str], ...]
    supersedes_version_id: str | None = None

    @property
    def is_reproducible(self) -> bool:
        return bool(self.formula_id and self.formula_version and self.evidence_ids and self.provenance)


@dataclass(frozen=True, slots=True)
class BudgetDecision:
    decision_id: str
    budget_version_id: str
    status: str
    recommendation: str
    rationale: str
    authority_required: BudgetAuthority
    evidence_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class BudgetOutcome:
    outcome_id: str
    budget_version_id: str
    expected: str
    observed: str
    evidence_ids: tuple[str, ...]
    feedback: OutcomeFeedback


@dataclass(frozen=True, slots=True)
class BudgetAuthorization:
    tenant_id: str
    principal_id: str
    actions: frozenset[BudgetAuthority]


class GovernedBudgetingService:
    """Prepare, calculate and revise budgets within explicit authority."""

    def __init__(self) -> None:
        self._versions: dict[str, list[BudgetVersion]] = {}

    @staticmethod
    def _validate_request(request: BudgetRequest) -> None:
        required = (request.request_id, request.tenant_id, request.principal_id, request.domain, request.period, request.objective, request.scope)
        if not all(required):
            raise BudgetingError("request requires tenant, principal, domain, period, objective and scope")

    @staticmethod
    def _validate_inputs(request: BudgetRequest, inputs: Sequence[BudgetInput]) -> None:
        if not inputs:
            raise BudgetingError("at least one governed input is required")
        for item in inputs:
            if item.tenant_id != request.tenant_id:
                raise BudgetingError("cross-tenant budget input rejected")
            if not item.source_id or not item.provenance:
                raise BudgetingError("budget input requires source and provenance")
            if item.value is not None and item.value < 0:
                raise BudgetingError("negative budget input requires an explicit domain contract; not accepted by the baseline")

    @staticmethod
    def _gap_for_input(item: BudgetInput) -> str | None:
        if item.classification == BudgetInputClass.GAP or item.value is None:
            return f"{item.name} is unavailable and cannot be invented"
        if item.classification == BudgetInputClass.CONFLICT:
            return f"{item.name} has conflicting evidence and cannot be silently resolved"
        return None

    @staticmethod
    def _calculate_line(
        spec: BudgetLine,
        inputs_by_id: Mapping[str, BudgetInput],
    ) -> BudgetLine:
        if spec.formula_id != FORMULA_ID or spec.formula_version != FORMULA_VERSION:
            return replace(spec, amount=None, status=BudgetStatus.BLOCKED, gap="formula/version mismatch")
        quantity = inputs_by_id.get(spec.quantity_input_id)
        unit_cost = inputs_by_id.get(spec.unit_cost_input_id)
        if quantity is None or unit_cost is None:
            return replace(spec, amount=None, status=BudgetStatus.CONDITIONAL, gap="line input reference is missing")
        quantity_gap = GovernedBudgetingService._gap_for_input(quantity)
        cost_gap = GovernedBudgetingService._gap_for_input(unit_cost)
        if quantity_gap or cost_gap:
            return replace(
                spec,
                amount=None,
                status=BudgetStatus.CONDITIONAL,
                gap=quantity_gap or cost_gap,
            )
        if quantity.unit != "unit" and quantity.unit != "h":
            return replace(spec, amount=None, status=BudgetStatus.BLOCKED, gap="unsupported quantity unit for baseline formula")
        assert quantity.value is not None and unit_cost.value is not None
        amount = quantity.value * unit_cost.value
        component = CostComponent(
            component_id=f"component-{spec.line_id}",
            input_ids=(quantity.input_id, unit_cost.input_id),
            amount=amount,
            formula_id=FORMULA_ID,
            formula_version=FORMULA_VERSION,
            source_ids=(quantity.source_id, unit_cost.source_id),
        )
        return replace(spec, component=component, amount=amount, status=BudgetStatus.COMPLETE, gap=None)

    def calculate(
        self,
        request: BudgetRequest,
        *,
        inputs: Sequence[BudgetInput],
        lines: Sequence[BudgetLine],
        assumptions: Sequence[Assumption] = (),
        capacity_constraints: Sequence[CapacityConstraint] = (),
        scenarios: Sequence[BudgetScenario] = (),
        sensitivities: Sequence[BudgetSensitivity] = (),
        supersedes_version_id: str | None = None,
    ) -> BudgetVersion:
        self._validate_request(request)
        self._validate_inputs(request, inputs)
        inputs_by_id = {item.input_id: item for item in inputs}
        if len(inputs_by_id) != len(inputs):
            raise BudgetingError("duplicate budget input id")

        calculated_lines = tuple(self._calculate_line(line, inputs_by_id) for line in lines)
        gaps = [line.gap for line in calculated_lines if line.gap]
        constrained = tuple(item for item in capacity_constraints if item.constrained)
        if constrained:
            gaps.extend(
                f"capacity constraint: {item.resource} requires {item.required} {item.unit}, available {item.available} {item.unit}"
                for item in constrained
            )

        follow_ups = tuple(
            BudgetFollowUp(
                follow_up_id=str(uuid4()),
                request_id=request.request_id,
                gap=gap,
                responsible_domain=None,
                required_evidence=gap,
            )
            for gap in gaps
        )

        known_cost = sum(
            (line.amount or Decimal("0"))
            for line in calculated_lines
            if line.line_type == BudgetLineType.COST
        )
        known_revenue = sum(
            (line.amount or Decimal("0"))
            for line in calculated_lines
            if line.line_type == BudgetLineType.REVENUE
        )
        complete_lines = all(line.status == BudgetStatus.COMPLETE for line in calculated_lines)
        status = BudgetStatus.COMPLETE
        if gaps:
            status = BudgetStatus.CONSTRAINED if constrained else BudgetStatus.CONDITIONAL
        elif not calculated_lines:
            status = BudgetStatus.BLOCKED
        total_cost = known_cost if complete_lines and not constrained else None
        total_revenue = known_revenue if complete_lines and not constrained else None
        margin = (total_revenue - total_cost) if total_revenue is not None and total_cost is not None else None
        margin_pct = (margin / total_revenue * Decimal("100")) if margin is not None and total_revenue else None

        evidence_ids = tuple(dict.fromkeys(item.input_id for item in inputs))
        provenance = tuple(dict(item.provenance) for item in inputs)
        previous_versions = self._versions.setdefault(request.request_id, [])
        version = BudgetVersion(
            version_id=str(uuid4()),
            request_id=request.request_id,
            version_number=len(previous_versions) + 1,
            tenant_id=request.tenant_id,
            period=request.period,
            inputs=tuple(inputs),
            lines=calculated_lines,
            assumptions=tuple(assumptions),
            capacity_constraints=tuple(capacity_constraints),
            follow_ups=follow_ups,
            scenarios=tuple(scenarios),
            sensitivities=tuple(sensitivities),
            formula_id=FORMULA_ID,
            formula_version=FORMULA_VERSION,
            known_cost_subtotal=known_cost,
            known_revenue_subtotal=known_revenue,
            total_cost=total_cost,
            total_revenue=total_revenue,
            gross_margin=margin,
            gross_margin_pct=margin_pct,
            status=status,
            evidence_ids=evidence_ids,
            provenance=provenance,
            supersedes_version_id=supersedes_version_id,
        )
        previous_versions.append(version)
        return version

    def recalculate(
        self,
        request: BudgetRequest,
        previous_version: BudgetVersion,
        *,
        inputs: Sequence[BudgetInput],
        lines: Sequence[BudgetLine],
        assumptions: Sequence[Assumption] = (),
        capacity_constraints: Sequence[CapacityConstraint] = (),
    ) -> BudgetVersion:
        if previous_version.request_id != request.request_id:
            raise BudgetingError("previous version belongs to another request")
        return self.calculate(
            request,
            inputs=inputs,
            lines=lines,
            assumptions=assumptions,
            capacity_constraints=capacity_constraints,
            supersedes_version_id=previous_version.version_id,
        )

    @staticmethod
    def compare_scenarios(
        baseline: BudgetVersion,
        alternatives: Sequence[BudgetVersion],
    ) -> tuple[Mapping[str, object], ...]:
        results: list[Mapping[str, object]] = []
        for version in alternatives:
            if version.tenant_id != baseline.tenant_id:
                raise BudgetingError("scenario comparison across tenants rejected")
            results.append(
                {
                    "version_id": version.version_id,
                    "status": version.status,
                    "known_cost_delta": version.known_cost_subtotal - baseline.known_cost_subtotal,
                    "known_revenue_delta": version.known_revenue_subtotal - baseline.known_revenue_subtotal,
                    "total_cost": version.total_cost,
                    "total_revenue": version.total_revenue,
                    "gross_margin": version.gross_margin,
                }
            )
        return tuple(results)

    @staticmethod
    def recommend(
        version: BudgetVersion,
        *,
        recommendation: str,
        rationale: str,
    ) -> BudgetDecision:
        if version.status == BudgetStatus.BLOCKED:
            status = "BLOCKED"
        elif version.status in (BudgetStatus.CONDITIONAL, BudgetStatus.CONSTRAINED):
            status = "CONDITIONAL_RECOMMENDATION"
        else:
            status = "RECOMMENDATION"
        return BudgetDecision(
            decision_id=str(uuid4()),
            budget_version_id=version.version_id,
            status=status,
            recommendation=recommendation,
            rationale=rationale,
            authority_required=BudgetAuthority.APPROVE,
            evidence_ids=version.evidence_ids,
        )

    @staticmethod
    def authorize(
        authorization: BudgetAuthorization,
        *,
        tenant_id: str,
        principal_id: str,
        action: BudgetAuthority,
    ) -> None:
        if authorization.tenant_id != tenant_id or authorization.principal_id != principal_id:
            raise BudgetAuthorizationError("authorization principal/tenant mismatch")
        if action not in authorization.actions:
            raise BudgetAuthorizationError(f"authority {action} was not granted")

    @staticmethod
    def record_outcome(
        version: BudgetVersion,
        *,
        expected: str,
        observed: str,
        evidence_ids: tuple[str, ...],
    ) -> BudgetOutcome:
        feedback = OutcomeFeedback(
            decision_id=version.version_id,
            outcome_id=str(uuid4()),
            expected=expected,
            observed=observed,
            assessment="BUDGET_VS_ACTUAL",
            evidence_ids=evidence_ids,
        )
        return BudgetOutcome(
            outcome_id=feedback.outcome_id,
            budget_version_id=version.version_id,
            expected=expected,
            observed=observed,
            evidence_ids=evidence_ids,
            feedback=feedback,
        )

    def versions(self, request_id: str) -> tuple[BudgetVersion, ...]:
        return tuple(self._versions.get(request_id, ()))


__all__ = [
    "Assumption",
    "BudgetAuthorization",
    "BudgetAuthorizationError",
    "BudgetDecision",
    "BudgetFollowUp",
    "BudgetInput",
    "BudgetInputClass",
    "BudgetLine",
    "BudgetLineType",
    "BudgetOutcome",
    "BudgetRequest",
    "BudgetScenario",
    "BudgetScenarioKind",
    "BudgetSensitivity",
    "BudgetStatus",
    "BudgetVersion",
    "BudgetingError",
    "CapacityConstraint",
    "CostComponent",
    "GovernedBudgetingService",
    "FORMULA_ID",
    "FORMULA_VERSION",
]
