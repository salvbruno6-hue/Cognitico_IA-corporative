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
    evolution_gate_approved: bool = False,
    elo_authorized: bool = False,
) -> LoopReadiness:
    """Check technical entry evidence without deciding or performing implementation.

    Gain is deliberately not a preflight blocker. The implementation loop owns
    the measured-gain decision so a candidate with complete evidence but no
    incremental gain can be classified as MEASURED_GAIN/RETEST rather than
    being incorrectly stopped at CANDIDATE.
    """
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

    if regressions:
        missing.append("regression_free")

    # Repeatability is evaluated by the implementation loop after measured
    # gain. Blocking it here would make the REPEATABLE/RETEST stage unreachable.
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

    # Governance approvals are downstream of technical readiness. This preflight
    # must be able to hand measured evidence to the implementation loop and then
    # to Evolution Gate/ELO Review; requiring those approvals here would make the
    # governed loop unreachable.

    return LoopReadiness(
        candidate_id=candidate.candidate_id,
        ready_for_loop=not missing,
        missing=tuple(dict.fromkeys(missing)),
        canonical_mutation=False,
    )
