"""Preflight contract for starting the governed ELO implementation loop.

This module does not execute deployment or mutate canonical state. It validates
that a candidate evaluation contains the minimum evidence required to enter
the implementation loop.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from .hermes_current_extensions import HermesCandidate
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

    for metric in common:
        if metric_directions.get(metric) not in {"maximize", "minimize"}:
            missing.append(f"metric_direction:{metric}")

    if regressions:
        missing.append("regression_free")

    if not repeatable:
        missing.append("repeatability")

    return LoopReadiness(
        candidate_id=candidate.candidate_id,
        ready_for_loop=not missing,
        missing=tuple(dict.fromkeys(missing)),
        canonical_mutation=False,
    )
