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


def _has_positive_gain(
    baseline: Mapping[str, float],
    adapted: Mapping[str, float],
    metric_directions: Mapping[str, str],
) -> bool:
    """Require at least one strictly positive, direction-correct metric delta."""
    for metric in baseline.keys() & adapted.keys():
        direction = metric_directions[metric]
        delta = adapted[metric] - baseline[metric]
        if (direction == "maximize" and delta > 0) or (
            direction == "minimize" and delta < 0
        ):
            return True
    return False


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
    evolution_gate_approved: bool = False,
    elo_authorized: bool = False,
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

    invalid_directions = [
        metric
        for metric in common
        if metric_directions.get(metric) not in {"maximize", "minimize"}
    ]
    if invalid_directions:
        missing.extend(f"metric_direction:{metric}" for metric in invalid_directions)

    if common and not invalid_directions and not _has_positive_gain(
        baseline, adapted, metric_directions
    ):
        missing.append("measured_gain")

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

    if not evolution_gate_approved:
        missing.append("evolution_gate_approval")

    if not elo_authorized:
        missing.append("elo_authorization")

    return LoopReadiness(
        candidate_id=candidate.candidate_id,
        ready_for_loop=not missing,
        missing=tuple(dict.fromkeys(missing)),
        canonical_mutation=False,
    )
