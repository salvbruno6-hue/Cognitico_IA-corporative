"""Governed ELO implementation loop for candidate capabilities.

The loop converts validated candidate evidence into an explicit implementation
decision without performing canonical mutation. Canonical promotion remains a
separate governed merge/approval action.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Mapping

from .hermes_current_extensions import HermesCandidate, evaluate_candidate
from .symbiont_adaptation import SymbiontAdaptation, refinement_is_eligible_for_test


class ImplementationStage(str, Enum):
    OBSERVED = "OBSERVED"
    CANDIDATE = "CANDIDATE"
    CONTROLLED_TEST = "CONTROLLED_TEST"
    MEASURED_GAIN = "MEASURED_GAIN"
    REPEATABLE = "REPEATABLE"
    EVOLUTION_GATE = "EVOLUTION_GATE"
    ELO_REVIEW = "ELO_REVIEW"
    IMPLEMENTATION_AUTHORIZED = "IMPLEMENTATION_AUTHORIZED"


@dataclass(frozen=True, slots=True)
class ImplementationDecision:
    candidate_id: str
    stage: ImplementationStage
    result: str
    canonical_mutation: bool
    reason: str


def _has_positive_gain(
    baseline: Mapping[str, float],
    adapted: Mapping[str, float],
    metric_directions: Mapping[str, str],
) -> bool:
    """Require an explicit direction for every measured metric."""
    common = baseline.keys() & adapted.keys()
    if not common:
        return False
    for metric in common:
        direction = metric_directions.get(metric)
        if direction not in {"maximize", "minimize"}:
            return False
        delta = adapted[metric] - baseline[metric]
        if (direction == "maximize" and delta > 0) or (direction == "minimize" and delta < 0):
            return True
    return False


def run_implementation_loop(
    candidate: HermesCandidate,
    adaptation: SymbiontAdaptation,
    baseline: Mapping[str, float],
    adapted: Mapping[str, float],
    *,
    repeatable: bool,
    elo_approved: bool = False,
    regressions: tuple[str, ...] = (),
    metric_directions: Mapping[str, str] | None = None,
) -> ImplementationDecision:
    """Advance a candidate through every implementation gate deterministically."""
    if candidate.promotion_state != "candidate_only" or candidate.canonical_mutation:
        return ImplementationDecision(
            candidate.candidate_id, ImplementationStage.CANDIDATE, "REJECT", False,
            "candidate is not safely bounded",
        )

    if not refinement_is_eligible_for_test(adaptation):
        return ImplementationDecision(
            candidate.candidate_id, ImplementationStage.CANDIDATE, "RETEST", False,
            "controlled evidence is insufficient",
        )

    directions = metric_directions or {}
    if not _has_positive_gain(baseline, adapted, directions):
        return ImplementationDecision(
            candidate.candidate_id, ImplementationStage.MEASURED_GAIN, "RETEST", False,
            "no measurable positive gain with explicit metric direction",
        )

    measurement = evaluate_candidate(
        candidate, baseline, adapted, regressions=regressions, repeatable=repeatable,
    )

    if measurement.result == "REJECT":
        return ImplementationDecision(
            candidate.candidate_id, ImplementationStage.CONTROLLED_TEST, "REJECT", False,
            "regression or governance boundary violation detected",
        )

    if measurement.result == "RETEST":
        return ImplementationDecision(
            candidate.candidate_id, ImplementationStage.REPEATABLE, "RETEST", False,
            "positive gain is not yet repeatable",
        )

    if not elo_approved:
        return ImplementationDecision(
            candidate.candidate_id, ImplementationStage.ELO_REVIEW, "READY_FOR_ELO_REVIEW", False,
            "technical evidence passed; explicit ELO approval is still required",
        )

    return ImplementationDecision(
        candidate.candidate_id, ImplementationStage.IMPLEMENTATION_AUTHORIZED,
        "IMPLEMENTATION_AUTHORIZED", False,
        "ELO approval is explicit; canonical mutation remains a separate governed merge",
    )


__all__ = ["ImplementationDecision", "ImplementationStage", "run_implementation_loop"]
