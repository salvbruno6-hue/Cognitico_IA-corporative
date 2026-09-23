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
        if state is Curvature.POSITIVE:
            actions.append(CapabilityAction(
                item=metric.item,
                exact_action="Preserve the verified gain and repeat the same measurement to confirm durability.",
                priority="P3",
                start_here="Repeat the measurement with the same baseline rule, source and metric direction.",
                rationale="A positive result is evidence of improvement, not authorization for automatic promotion.",
            ))
        elif state is Curvature.NOT_MEASURED:
            actions.append(CapabilityAction(
                item=metric.item,
                exact_action="Collect baseline/current values with source, period and evidence references.",
                priority="P1",
                start_here="Instrument the metric at the production observation boundary.",
                rationale="Missing evidence is not converted into zero or an assumed score.",
            ))
        elif state in {Curvature.NEGATIVE, Curvature.CRITICAL}:
            actions.append(CapabilityAction(
                item=metric.item,
                exact_action="Investigate the regression against the last verified baseline and open a bounded correction experiment.",
                priority="P0" if state is Curvature.CRITICAL else "P1",
                start_here="Reproduce the regression using the same measurement rule and evidence source.",
                rationale="Regression requires diagnosis and controlled correction before any promotion decision.",
            ))
        else:
            actions.append(CapabilityAction(
                item=metric.item,
                exact_action="Run a bounded improvement experiment and measure the same metric again.",
                priority="P2",
                start_here="Keep the current baseline and define the smallest measurable intervention.",
                rationale="Stable performance is not evidence of improvement.",
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


__all__ = [
    "CapabilityAction", "CapabilityEvolutionReview", "CapabilityMetric",
    "Curvature", "curvature", "review_capabilities",
]
