"""Preflight contract for starting the governed ELO implementation loop.

This module does not execute deployment or mutate canonical state. It validates
that a candidate evaluation contains the minimum evidence required to enter
the implementation loop.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from .hermes_current_extensions import HermesCandidate
from .implementation_loop_evidence import ImplementationEvidence
from .symbiont_adaptation import SymbiontAdaptation, refinement_is_eligible_for_test


@dataclass(frozen=True, slots=True)
class LoopReadiness:
    candidate_id: str
    ready_for_loop: bool
    missing: tuple[str, ...]
    canonical_mutation: bool = False


def assess_loop_readiness(
    candidate: HermesCandidate,
    adaptation: SymbiontAdaptation,
    baseline: Mapping[str, float],
    adapted: Mapping[str, float],
    *,
    metric_directions: Mapping[str, str],
    repeatable: bool,
    regressions: tuple[str, ...] = (),
    provenance_refs: tuple[str, ...] = (),
    boundary_integrity: bool = True,
) -> LoopReadiness:
    """Check entry evidence without deciding or performing implementation."""
    missing: list[str] = []

    if candidate.promotion_state != "candidate_only" or candidate.canonical_mutation:
        missing.append("bounded_candidate")

    if not refinement_is_eligible_for_test(adaptation):
        missing.append("controlled_evidence")

    if not baseline or not adapted:
        missing.append("baseline_and_adapted_metrics")

    common = baseline.keys() & adapted.keys()
    if not common:
        missing.append("common_metric")

    positive_gain = False
    for metric in common:
        direction = metric_directions.get(metric)
        if direction == "maximize" and adapted[metric] > baseline[metric]:
            positive_gain = True
        elif direction == "minimize" and adapted[metric] < baseline[metric]:
            positive_gain = True
    if common and not positive_gain:
        missing.append("measurable_positive_gain")

    for metric in common:
        if metric_directions.get(metric) not in {"maximize", "minimize"}:
            missing.append(f"metric_direction:{metric}")

    if regressions:
        missing.append("regression_free")

    if not repeatable:
        missing.append("repeatability")
    if not provenance_refs:
        missing.append("provenance")
    if not boundary_integrity:
        missing.append("boundary_integrity")

    evidence = ImplementationEvidence(
        candidate_id=candidate.candidate_id,
        owner=candidate.owner,
        baseline=baseline,
        adapted=adapted,
        metric_directions=metric_directions,
        regressions=regressions,
        repeatable=repeatable,
        provenance_refs=provenance_refs,
        boundary_integrity=boundary_integrity,
    )
    if not evidence.is_complete():
        missing.append("evidence_contract")

    return LoopReadiness(
        candidate_id=candidate.candidate_id,
        ready_for_loop=not missing,
        missing=tuple(dict.fromkeys(missing)),
        canonical_mutation=False,
    )
