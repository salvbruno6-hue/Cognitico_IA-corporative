"""Governed ELO implementation loop for candidate capabilities.

The loop converts validated candidate evidence into an explicit implementation
decision without performing canonical mutation. Canonical promotion remains a
separate governed merge/approval action.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Callable, Mapping

from .hermes_current_extensions import HermesCandidate, evaluate_candidate
from .hermes_capability_loops import ImplementationDecision, ImplementationStage
from .symbiont_adaptation import SymbiontAdaptation, refinement_is_eligible_for_test


class SymbiontAutonomyState(str, Enum):
    """Governed autonomy state for the adjustment portion of the loop."""
    AUTONOMOUS_UNTIL_BLOCKED = "AUTONOMOUS_UNTIL_BLOCKED"
    COMPLETED = "COMPLETED"
    HUMAN_APPROVAL_REQUIRED = "HUMAN_APPROVAL_REQUIRED"
    BLOCKED = "BLOCKED"


@dataclass(frozen=True, slots=True)
class SymbiontAdjustmentIteration:
    iteration: int
    outcome: str
    changed: bool
    evidence_ref: str | None = None
    blocker: str | None = None


@dataclass(frozen=True, slots=True)
class SymbiontAutonomousAdjustmentResult:
    state: SymbiontAutonomyState
    iterations: tuple[SymbiontAdjustmentIteration, ...]
    next_action: str
    human_required: bool
    canonical_mutation: bool = False

    @property
    def completed(self) -> bool:
        return self.state is SymbiontAutonomyState.COMPLETED


Adjustment = Callable[[int], tuple[bool, str | None]]
Evaluation = Callable[[int], tuple[str, str | None]]
HumanBoundary = Callable[[int], str | None]


def run_symbiont_autonomous_adjustment_loop(
    *,
    adjust: Adjustment,
    evaluate: Evaluation,
    human_boundary: HumanBoundary | None = None,
    max_iterations: int = 5,
) -> SymbiontAutonomousAdjustmentResult:
    """Run adjustments autonomously until success, a governed boundary, or bound.

    Ordinary iterations do not request confirmation. Human involvement occurs
    only when the supplied governance boundary explicitly returns a reason.
    Production authorization, canonical mutation, promotion, authority
    changes, and unresolved ambiguity belong at that existing boundary.
    """
    if max_iterations < 1:
        raise ValueError("max_iterations must be >= 1")

    history: list[SymbiontAdjustmentIteration] = []
    boundary = human_boundary or (lambda _iteration: None)

    for iteration in range(1, max_iterations + 1):
        blocker = boundary(iteration)
        if blocker:
            history.append(SymbiontAdjustmentIteration(
                iteration=iteration,
                outcome="HUMAN_APPROVAL_REQUIRED",
                changed=False,
                blocker=blocker,
            ))
            return SymbiontAutonomousAdjustmentResult(
                state=SymbiontAutonomyState.HUMAN_APPROVAL_REQUIRED,
                iterations=tuple(history),
                next_action=blocker,
                human_required=True,
            )

        changed, evidence_ref = adjust(iteration)
        outcome, evaluation_blocker = evaluate(iteration)
        if evaluation_blocker:
            history.append(SymbiontAdjustmentIteration(
                iteration=iteration,
                outcome="BLOCKED",
                changed=changed,
                evidence_ref=evidence_ref,
                blocker=evaluation_blocker,
            ))
            return SymbiontAutonomousAdjustmentResult(
                state=SymbiontAutonomyState.BLOCKED,
                iterations=tuple(history),
                next_action=evaluation_blocker,
                human_required=True,
            )

        history.append(SymbiontAdjustmentIteration(
            iteration=iteration,
            outcome=outcome,
            changed=changed,
            evidence_ref=evidence_ref,
        ))
        if outcome == "SUCCESS":
            return SymbiontAutonomousAdjustmentResult(
                state=SymbiontAutonomyState.COMPLETED,
                iterations=tuple(history),
                next_action="Continue through the existing governed handoff; do not infer production or promotion.",
                human_required=False,
            )

    return SymbiontAutonomousAdjustmentResult(
        state=SymbiontAutonomyState.AUTONOMOUS_UNTIL_BLOCKED,
        iterations=tuple(history),
        next_action="Bounded autonomous attempts exhausted; diagnose the unresolved condition and use the existing governance boundary if a human decision is required.",
        human_required=False,
    )


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
        return ImplementationDecision(decision_id="", candidate_id=candidate.candidate_id, approved=False, scope="", stage=ImplementationStage.CANDIDATE, result="REJECT", reason="candidate is not safely bounded")

    if not refinement_is_eligible_for_test(adaptation):
        return ImplementationDecision(decision_id="", candidate_id=candidate.candidate_id, approved=False, scope="", stage=ImplementationStage.CANDIDATE, result="RETEST", reason="controlled evidence is insufficient")

    directions = metric_directions or {}
    if regressions:
        return ImplementationDecision(decision_id="", candidate_id=candidate.candidate_id, approved=False, scope="", stage=ImplementationStage.CONTROLLED_TEST, result="REJECT", reason="regression or governance boundary violation detected")

    if not _has_positive_gain(baseline, adapted, directions):
        return ImplementationDecision(decision_id="", candidate_id=candidate.candidate_id, approved=False, scope="", stage=ImplementationStage.MEASURED_GAIN, result="RETEST", reason="no measurable positive gain with explicit metric direction")

    measurement = evaluate_candidate(
        candidate, baseline, adapted, regressions=regressions, repeatable=repeatable,
        metric_directions=directions,
    )

    if measurement.result == "REJECT":
        return ImplementationDecision(decision_id="", candidate_id=candidate.candidate_id, approved=False, scope="", stage=ImplementationStage.CONTROLLED_TEST, result="REJECT", reason="regression or governance boundary violation detected")

    if measurement.result == "RETEST":
        return ImplementationDecision(decision_id="", candidate_id=candidate.candidate_id, approved=False, scope="", stage=ImplementationStage.REPEATABLE, result="RETEST", reason="positive gain is not yet repeatable")

    if not elo_approved:
        return ImplementationDecision(decision_id="", candidate_id=candidate.candidate_id, approved=False, scope="", stage=ImplementationStage.ELO_REVIEW, result="READY_FOR_ELO_REVIEW", reason="technical evidence passed; explicit ELO approval is still required")

    return ImplementationDecision(
        decision_id="legacy-elo-approval",
        candidate_id=candidate.candidate_id,
        approved=True,
        scope="UNBOUND",
        evidence_refs=(),
        authority="elo_cognitive",
        stage=ImplementationStage.IMPLEMENTATION_AUTHORIZED,
        result="IMPLEMENTATION_AUTHORIZED",
        canonical_mutation=False,
        reason="legacy ELO approval state; canonical Symbiont consumption still requires a separate elo-authz AuthorizationDecision",
    )


__all__ = [
    "ImplementationDecision",
    "ImplementationStage",
    "SymbiontAdjustmentIteration",
    "SymbiontAutonomousAdjustmentResult",
    "SymbiontAutonomyState",
    "run_implementation_loop",
    "run_symbiont_autonomous_adjustment_loop",
]
