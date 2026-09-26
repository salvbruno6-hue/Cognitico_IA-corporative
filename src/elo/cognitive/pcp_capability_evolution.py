"""PCP-to-Symbiont capability-evolution bridge.

This is a translation boundary only. PCP supplies explicit capability
measurements and evidence; the canonical Symbiont EVOLUÇÃO_DE_CAPACIDADES
implementation is injected by the caller. No evolution logic, learning,
memory, gate or mutation is implemented here.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Sequence

from .pcp_operational_evidence import PCPOperationalEvidencePackage


@dataclass(frozen=True, slots=True)
class PCPCapabilityMetricInput:
    item: str
    baseline: float | None
    current: float | None
    direction: str
    measurement_period: str
    evidence_refs: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class PCPCapabilityEvolutionHandoff:
    package: PCPOperationalEvidencePackage
    metrics: tuple[PCPCapabilityMetricInput, ...]
    evidence_refs: tuple[str, ...]


def prepare_pcp_capability_evolution(
    package: PCPOperationalEvidencePackage,
    *,
    metrics: Sequence[PCPCapabilityMetricInput],
) -> PCPCapabilityEvolutionHandoff:
    """Prepare explicit PCP evidence for the canonical evolution trigger.

    Missing baseline/current/direction/period is preserved; this bridge never
    derives capability metrics from operational counters or diagnosis status.
    """
    normalized = tuple(metrics)
    refs = tuple(
        dict.fromkeys(
            (
                *package.evidence_ids,
                *(ref for metric in normalized for ref in metric.evidence_refs),
            )
        )
    )
    return PCPCapabilityEvolutionHandoff(
        package=package,
        metrics=normalized,
        evidence_refs=refs,
    )


def delegate_pcp_capability_evolution(
    handoff: PCPCapabilityEvolutionHandoff,
    *,
    capability_metric_factory: Callable[..., Any],
    capability_reviewer: Callable[..., Any],
) -> Any:
    """Adapt explicit metrics and delegate to the canonical Symbiont review.

    The factory/reviewer are injected so PCP does not import or recreate the
    Symbiont evolution authority. The canonical implementation remains owned
    by EVOLUÇÃO_DE_CAPACIDADES.
    """
    canonical_metrics = tuple(
        capability_metric_factory(
            item=metric.item,
            baseline=metric.baseline,
            current=metric.current,
            direction=metric.direction,
            evidence_refs=metric.evidence_refs,
            measurement_period=metric.measurement_period,
        )
        for metric in handoff.metrics
    )
    return capability_reviewer(
        metrics=canonical_metrics,
        evidence_refs=handoff.evidence_refs,
    )


__all__ = [
    "PCPCapabilityEvolutionHandoff",
    "PCPCapabilityMetricInput",
    "delegate_pcp_capability_evolution",
    "prepare_pcp_capability_evolution",
]
