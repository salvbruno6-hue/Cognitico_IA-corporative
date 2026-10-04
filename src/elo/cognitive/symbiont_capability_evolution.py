"""Read-only production capability evolution review for the Symbiont.

This module intentionally does not create a second Evolution Gate, learning
store, dashboard authority, or promotion path. It consumes governed metrics
and evidence and returns a deterministic review contract that an external
analyst may interpret into an improvement proposal.

Trigger: EVOLUÇÃO_DE_CAPACIDADES
Boundary: production observation -> diagnostic review -> governed proposal.
Canonical mutation is always false.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Mapping, Sequence


class Curvature(str, Enum):
    POSITIVE = "POSITIVE"
    STABLE = "STABLE"
    NEGATIVE = "NEGATIVE"
    CRITICAL = "CRITICAL"
    NOT_MEASURED = "NOT_MEASURED"


@dataclass(frozen=True, slots=True)
class CapabilityMetric:
    item: str
    baseline: float | None
    current: float | None
    direction: str
    evidence_refs: tuple[str, ...] = ()
    measurement_period: str = ""
    evidence_mode: str = "DIRECT"
    observer_capability: str | None = None
    experience_ref: str | None = None
    evidence_strength: str = "STANDARD"
    evolution_impact: str = "UNASSESSED"

    @classmethod
    def from_evolution_measurement(
        cls, *, item: str, baseline: Mapping[str, float], adapted: Mapping[str, float],
        metric_directions: Mapping[str, str], evidence_refs: Sequence[str],
        measurement_period: str,
    ) -> tuple["CapabilityMetric", ...]:
        common = baseline.keys() & adapted.keys()
        return tuple(
            cls(
                item=f"{item}:{metric}",
                baseline=baseline[metric],
                current=adapted[metric],
                direction=metric_directions.get(metric, ""),
                evidence_refs=tuple(evidence_refs),
                measurement_period=measurement_period,
            )
            for metric in sorted(common)
        )

    @classmethod
    def from_implementation_evidence(
        cls, *, item: str, baseline: Mapping[str, float], adapted: Mapping[str, float],
        metric_directions: Mapping[str, str], provenance_refs: Sequence[str],
        measurement_period: str,
    ) -> tuple["CapabilityMetric", ...]:
        return cls.from_evolution_measurement(
            item=item, baseline=baseline, adapted=adapted,
            metric_directions=metric_directions, evidence_refs=provenance_refs,
            measurement_period=measurement_period,
        )

    @classmethod
    def from_indirect_experience(
        cls, *, item: str, baseline: float | None, current: float | None,
        direction: str, evidence_refs: Sequence[str], measurement_period: str,
        observer_capability: str, experience_ref: str,
        evidence_strength: str = "STANDARD", evolution_impact: str = "UNASSESSED",
    ) -> "CapabilityMetric":
        if not observer_capability.strip():
            raise ValueError("indirect evidence requires observer capability")
        if not experience_ref.strip():
            raise ValueError("indirect evidence requires experience reference")
        refs = tuple(ref.strip() for ref in evidence_refs if str(ref).strip())
        if not refs:
            raise ValueError("indirect evidence requires evidence references")
        if evidence_strength not in {"STANDARD", "STRONG"}:
            raise ValueError("evidence_strength must be STANDARD or STRONG")
        if evolution_impact not in {"UNASSESSED", "SUPPORTED", "STRONG"}:
            raise ValueError("evolution_impact must be UNASSESSED, SUPPORTED or STRONG")
        return cls(
            item=item,
            baseline=baseline,
            current=current,
            direction=direction,
            evidence_refs=refs,
            measurement_period=measurement_period,
            evidence_mode="INDIRECT_EXPERIENCE",
            observer_capability=observer_capability.strip(),
            experience_ref=experience_ref.strip(),
            evidence_strength=evidence_strength,
            evolution_impact=evolution_impact,
        )

    @property
    def delta(self) -> float | None:
        if self.baseline is None or self.current is None:
            return None
        return round(self.current - self.baseline, 10)


@dataclass(frozen=True, slots=True)
class CapabilityAction:
    item: str
    exact_action: str
    priority: str
    start_here: str
    rationale: str


@dataclass(frozen=True, slots=True)
class CapabilityEvolutionReview:
    trigger_id: str
    status: str
    metrics: tuple[CapabilityMetric, ...]
    actions: tuple[CapabilityAction, ...]
    evidence_refs: tuple[str, ...]
    canonical_mutation: bool = False

    @property
    def persistent_adjustment_required(self) -> bool:
        return any(
            metric.evidence_mode == "INDIRECT_EXPERIENCE"
            and metric.evidence_strength == "STRONG"
            and metric.evolution_impact == "STRONG"
            and _curvature(metric) is Curvature.POSITIVE
            for metric in self.metrics
        )

    @property
    def production_pending(self) -> bool:
        return self.persistent_adjustment_required and not any(
            metric.evidence_mode == "DIRECT"
            and metric.measurement_period.upper().startswith("PRODUCTION:")
            for metric in self.metrics
        )

    @property
    def next_intervention(self) -> str:
        if self.production_pending:
            return (
                "Continue the governed adjustment loop: inspect the last result, "
                "apply the smallest justified correction, retest, and seek the "
                "authorized production execution. Do not convert lab/indirect "
                "evidence into production evidence."
            )
        if self.persistent_adjustment_required:
            return "Prepare the candidate for the existing Evolution Gate and the separate production-observation boundary."
        return "Follow the existing capability-evolution action for the current evidence state."

    @property
    def ready_for_analysis(self) -> bool:
        return self.status == "ANALYSIS_READY"


def _curvature(metric: CapabilityMetric) -> Curvature:
    if (
        metric.baseline is None or metric.current is None
        or not metric.evidence_refs or not metric.measurement_period
    ):
        return Curvature.NOT_MEASURED

    delta = metric.current - metric.baseline
    direction = metric.direction.lower().strip()
    if direction not in {"maximize", "minimize"}:
        return Curvature.NOT_MEASURED

    gain = delta if direction == "maximize" else -delta
    baseline = abs(metric.baseline)
    if gain < 0:
        return Curvature.CRITICAL if baseline and abs(gain) / baseline >= 0.20 else Curvature.NEGATIVE
    if baseline == 0:
        return Curvature.POSITIVE if gain > 0 else Curvature.STABLE

    return Curvature.POSITIVE if gain / baseline >= 0.05 else Curvature.STABLE


def curvature(metric: CapabilityMetric) -> Curvature:
    return _curvature(metric)


def review_capabilities(
    *, metrics: Sequence[CapabilityMetric], evidence_refs: Sequence[str] = (),
) -> CapabilityEvolutionReview:
    normalized = tuple(metrics)
    actions: list[CapabilityAction] = []
    for metric in normalized:
        state = _curvature(metric)
        evidence_origin = (
            f"Validated downstream observer: {metric.observer_capability} "
            f"(experience {metric.experience_ref})."
            if metric.evidence_mode == "INDIRECT_EXPERIENCE"
            else "Direct governed measurement."
        )
        if state is Curvature.POSITIVE and metric.evidence_mode == "INDIRECT_EXPERIENCE" and metric.evidence_strength == "STRONG" and metric.evolution_impact == "STRONG":
            actions.append(CapabilityAction(
                item=metric.item,
                exact_action="Keep the Symbiont adjustment loop active until the candidate reaches an authorized production observation.",
                priority="P1",
                start_here="Apply the smallest justified correction from the latest validated experience, retest in the Lab, then seek the separate production boundary when authorized.",
                rationale="Strong gain and evolutionary-impact evidence support continued adjustment, but indirect/Lab evidence cannot be relabeled as production evidence.",
            ))
        elif state is Curvature.POSITIVE:
            actions.append(CapabilityAction(
                item=metric.item,
                exact_action="Preserve the verified gain and repeat the same measurement to confirm durability.",
                priority="P3",
                start_here="Repeat the measurement with the same baseline rule, source and metric direction.",
                rationale=f"{evidence_origin} A positive result is evidence of improvement, not authorization for automatic promotion.",
            ))
        elif state is Curvature.NOT_MEASURED:
            actions.append(CapabilityAction(
                item=metric.item,
                exact_action="Collect baseline/current values with source, period and evidence references.",
                priority="P1",
                start_here="Instrument the metric at the production observation boundary.",
                rationale="Missing evidence is not converted into zero or an assumed trend.",
            ))
        elif state in {Curvature.NEGATIVE, Curvature.CRITICAL}:
            actions.append(CapabilityAction(
                item=metric.item,
                exact_action="Investigate the regression against the last verified baseline and open a bounded correction experiment.",
                priority="P0" if state is Curvature.CRITICAL else "P1",
                start_here="Reproduce the regression using the same measurement rule and evidence source.",
                rationale=f"{evidence_origin} Regression requires diagnosis and controlled correction before any promotion decision.",
            ))
        else:
            actions.append(CapabilityAction(
                item=metric.item,
                exact_action="Run a bounded improvement experiment and measure the same metric again.",
                priority="P2",
                start_here="Keep the current baseline and define the smallest measurable intervention.",
                rationale=f"{evidence_origin} Stable performance is not evidence of improvement.",
            ))

    all_refs = tuple(dict.fromkeys((*evidence_refs, *(ref for m in normalized for ref in m.evidence_refs))))
    status = "NOT_MEASURED" if not normalized or all(_curvature(m) is Curvature.NOT_MEASURED for m in normalized) else "ANALYSIS_READY"
    return CapabilityEvolutionReview(
        trigger_id="EVOLUÇÃO_DE_CAPACIDADES",
        status=status,
        metrics=normalized,
        actions=tuple(actions),
        evidence_refs=all_refs,
    )


class CapabilityConditionStatus(str, Enum):
    ABSENT = "ABSENT"
    PRESENT = "PRESENT"
    VERIFIED = "VERIFIED"
    BLOCKED = "BLOCKED"
    NOT_EVIDENCED = "NOT_EVIDENCED"


class CapabilityReadinessStatus(str, Enum):
    NOT_IMPLEMENTED = "NOT_IMPLEMENTED"
    IMPLEMENTED_NOT_TESTED = "IMPLEMENTED_NOT_TESTED"
    TESTED_NOT_EVIDENCED = "TESTED_NOT_EVIDENCED"
    EVIDENCED_NOT_RUNTIME = "EVIDENCED_NOT_RUNTIME"
    RUNTIME_INTEGRATED = "RUNTIME_INTEGRATED"
    OPERATIONALLY_EVIDENCED = "OPERATIONALLY_EVIDENCED"
    READY_FOR_EVOLUTION_GATE = "READY_FOR_EVOLUTION_GATE"
    PRODUCTION_PROVEN = "PRODUCTION_PROVEN"
    BLOCKED = "BLOCKED"


@dataclass(frozen=True, slots=True)
class CapabilityCondition:
    name: str
    status: CapabilityConditionStatus
    evidence_refs: tuple[str, ...] = ()
    detail: str = ""


@dataclass(frozen=True, slots=True)
class CapabilityStatusReport:
    capability_id: str
    capability_name: str
    owner: str
    authority: str
    status: CapabilityReadinessStatus
    conditions: tuple[CapabilityCondition, ...]
    missing_conditions: tuple[str, ...]
    blockers: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    next_action: str
    production_proven: bool
    canonical_mutation: bool = False

    def as_dict(self) -> dict[str, object]:
        return {
            "capability_id": self.capability_id,
            "capability_name": self.capability_name,
            "owner": self.owner,
            "authority": self.authority,
            "status": self.status.value,
            "conditions": [
                {
                    "name": condition.name,
                    "status": condition.status.value,
                    "evidence_refs": list(condition.evidence_refs),
                    "detail": condition.detail,
                }
                for condition in self.conditions
            ],
            "missing_conditions": list(self.missing_conditions),
            "blockers": list(self.blockers),
            "evidence_refs": list(self.evidence_refs),
            "next_action": self.next_action,
            "production_proven": self.production_proven,
            "canonical_mutation": self.canonical_mutation,
        }


def _condition(
    name: str,
    present: bool,
    *,
    verified: bool = False,
    blocked: bool = False,
    evidence_refs: Sequence[str] = (),
    detail: str = "",
) -> CapabilityCondition:
    refs = tuple(dict.fromkeys(str(ref).strip() for ref in evidence_refs if str(ref).strip()))
    if blocked:
        state = CapabilityConditionStatus.BLOCKED
    elif not present:
        state = CapabilityConditionStatus.ABSENT
    elif verified and refs:
        state = CapabilityConditionStatus.VERIFIED
    elif present and not refs:
        state = CapabilityConditionStatus.NOT_EVIDENCED
    else:
        state = CapabilityConditionStatus.PRESENT
    return CapabilityCondition(name=name, status=state, evidence_refs=refs, detail=detail)


def diagnose_capability_status(
    *,
    capability_id: str,
    capability_name: str,
    owner: str,
    authority: str,
    contract_present: bool,
    implementation_present: bool,
    tests_present: bool,
    evidence_present: bool,
    runtime_integrated: bool,
    operational_evidence: bool,
    production_outcome: bool,
    governance_approved: bool = False,
    contract_refs: Sequence[str] = (),
    implementation_refs: Sequence[str] = (),
    test_refs: Sequence[str] = (),
    evidence_refs: Sequence[str] = (),
    runtime_refs: Sequence[str] = (),
    operational_refs: Sequence[str] = (),
    production_refs: Sequence[str] = (),
    governance_refs: Sequence[str] = (),
    blockers: Sequence[str] = (),
) -> CapabilityStatusReport:
    """Return a read-only status diagnosis for one capability.

    This is a diagnostic read model for the Symbiont. It does not authorize
    execution, promotion, deployment, learning, or canonical mutation.
    A claimed state is considered verified only when explicit evidence
    references accompany it. Production proof is never inferred from tests,
    runtime integration, or operational evidence alone.
    """
    required = (
        _condition("CONTRACT", contract_present, verified=contract_present, evidence_refs=contract_refs),
        _condition("IMPLEMENTATION", implementation_present, verified=implementation_present, evidence_refs=implementation_refs),
        _condition("TESTS", tests_present, verified=tests_present, evidence_refs=test_refs),
        _condition("EVIDENCE", evidence_present, verified=evidence_present, evidence_refs=evidence_refs),
        _condition("RUNTIME_INTEGRATION", runtime_integrated, verified=runtime_integrated, evidence_refs=runtime_refs),
        _condition("OPERATIONAL_EVIDENCE", operational_evidence, verified=operational_evidence, evidence_refs=operational_refs),
        _condition("PRODUCTION_OUTCOME", production_outcome, verified=production_outcome, evidence_refs=production_refs),
        _condition("GOVERNANCE_APPROVAL", governance_approved, verified=governance_approved, evidence_refs=governance_refs),
    )
    normalized_blockers = tuple(dict.fromkeys(str(item).strip() for item in blockers if str(item).strip()))
    refs = tuple(dict.fromkeys(
        ref
        for condition in required
        for ref in condition.evidence_refs
    ))

    if normalized_blockers:
        status = CapabilityReadinessStatus.BLOCKED
        next_action = "Resolve the explicit blocker using the existing canonical owner; do not bypass the governance boundary."
    elif not implementation_present:
        status = CapabilityReadinessStatus.NOT_IMPLEMENTED
        next_action = "Locate or implement the capability through its existing canonical owner."
    elif not tests_present:
        status = CapabilityReadinessStatus.IMPLEMENTED_NOT_TESTED
        next_action = "Create or execute the relevant tests and retain their evidence."
    elif not evidence_present:
        status = CapabilityReadinessStatus.TESTED_NOT_EVIDENCED
        next_action = "Collect explicit implementation/runtime evidence; do not infer operational status from test existence."
    elif not runtime_integrated:
        status = CapabilityReadinessStatus.EVIDENCED_NOT_RUNTIME
        next_action = "Trace and connect the capability to its real canonical runtime entrypoint without creating a parallel authority."
    elif not operational_evidence:
        status = CapabilityReadinessStatus.RUNTIME_INTEGRATED
        next_action = "Collect repeatable operational evidence from the real runtime path."
    elif production_outcome and governance_approved:
        status = CapabilityReadinessStatus.PRODUCTION_PROVEN
        next_action = "Maintain observation and reassess against the next verified baseline."
    elif production_outcome and not governance_approved:
        status = CapabilityReadinessStatus.READY_FOR_EVOLUTION_GATE
        next_action = "Use the existing Evolution Gate; production evidence does not self-authorize promotion."
    else:
        status = CapabilityReadinessStatus.OPERATIONALLY_EVIDENCED
        next_action = "Continue governed observation until a verified production outcome or an explicit governance decision exists."

    missing = tuple(
        condition.name
        for condition in required
        if condition.status in {CapabilityConditionStatus.ABSENT, CapabilityConditionStatus.NOT_EVIDENCED}
    )
    return CapabilityStatusReport(
        capability_id=capability_id,
        capability_name=capability_name,
        owner=owner,
        authority=authority,
        status=status,
        conditions=required,
        missing_conditions=missing,
        blockers=normalized_blockers,
        evidence_refs=refs,
        next_action=next_action,
        production_proven=status is CapabilityReadinessStatus.PRODUCTION_PROVEN,
    )


__all__ = [
    "CapabilityAction", "CapabilityCondition", "CapabilityConditionStatus",
    "CapabilityEvolutionReview", "CapabilityMetric", "CapabilityReadinessStatus",
    "CapabilityStatusReport", "Curvature", "curvature", "diagnose_capability_status",
    "review_capabilities",
]
