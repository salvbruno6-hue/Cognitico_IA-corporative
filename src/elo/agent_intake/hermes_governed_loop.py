"""Single governed handoff across the existing ELO capability loops.

This module only composes existing gates. It does not create a new approval
authority, Evolution Gate, promotion engine, or canonical mutation path.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from .hermes_capability_loops import (
    ApprovalReadiness,
    HermesCapabilityLoops,
    TransformationCandidate,
)
from .implementation_loop import ImplementationDecision, ImplementationStage, run_implementation_loop
from .implementation_loop_readiness import LoopReadiness, assess_loop_readiness
from .hermes_current_extensions import HermesCandidate
from .symbiont_adaptation import SymbiontAdaptation


@dataclass(frozen=True, slots=True)
class GovernedLoopHandoff:
    candidate_id: str
    loop_readiness: LoopReadiness
    implementation: ImplementationDecision
    approval_readiness: ApprovalReadiness | None
    next_state: str
    canonical_mutation: bool = False


def advance_to_implementation(
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
    elo_approved: bool = False,
    evolution_gate_approved: bool = False,
) -> GovernedLoopHandoff:
    """Compose preflight, measurement, repeatability and ELO-review handoff."""
    readiness = assess_loop_readiness(
        candidate, adaptation, baseline, adapted,
        metric_directions=metric_directions,
        repeatable=repeatable, regressions=regressions,
        provenance_refs=provenance_refs, boundary_integrity=boundary_integrity,
    )
    if not readiness.ready_for_loop:
        decision = ImplementationDecision(
            candidate.candidate_id, ImplementationStage.CANDIDATE,
            "RETEST", False, "implementation-loop entry evidence is incomplete",
        )
        return GovernedLoopHandoff(
            candidate.candidate_id, readiness, decision, None, "CANDIDATE",
        )

    if not evolution_gate_approved:
        decision = ImplementationDecision(
            candidate.candidate_id,
            ImplementationStage.ELO_REVIEW,
            "READY_FOR_ELO_REVIEW",
            False,
            "technical evidence is ready; explicit Evolution Gate approval is still required",
        )
    else:
        decision = run_implementation_loop(
            candidate, adaptation, baseline, adapted,
            repeatable=repeatable, elo_approved=elo_approved,
            regressions=regressions, metric_directions=metric_directions,
        )
    if decision.result == "READY_FOR_ELO_REVIEW":
        next_state = "ELO_REVIEW"
    elif decision.result == "IMPLEMENTATION_AUTHORIZED":
        next_state = "IMPLEMENTATION_AUTHORIZED"
    else:
        next_state = decision.stage.value
    return GovernedLoopHandoff(
        candidate.candidate_id, readiness, decision, None, next_state,
    )


def approval_to_implementation(
    candidate: TransformationCandidate,
    *,
    implementation_passed: bool,
    provenance_passed: bool,
    consistency_passed: bool,
    governance_metadata_complete: bool,
    evolution_gate_approved: bool,
    decision: object,
):
    """Use the existing approval/readiness contract for the final handoff."""
    readiness = HermesCapabilityLoops.approval_readiness(
        candidate,
        implementation_passed=implementation_passed,
        provenance_passed=provenance_passed,
        consistency_passed=consistency_passed,
        governance_metadata_complete=governance_metadata_complete,
        evolution_gate_approved=evolution_gate_approved,
    )
    from .hermes_capability_loops import ApprovedCandidateImplementationLoop
    return ApprovedCandidateImplementationLoop.activate(
        candidate, readiness=readiness, decision=decision
    )

def close_approved_candidate(
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
    elo_implementation_approved: bool = False,
) -> GovernedLoopHandoff:
    """Close an already-approved candidate through the existing implementation loop.

    This is a handoff, not a new approval authority. Technical evidence is
    revalidated before explicit ELO implementation authorization is passed
    to run_implementation_loop. Canonical mutation remains false.
    """
    readiness = assess_loop_readiness(
        candidate,
        adaptation,
        baseline,
        adapted,
        metric_directions=metric_directions,
        repeatable=repeatable,
        regressions=regressions,
        provenance_refs=provenance_refs,
        boundary_integrity=boundary_integrity,
    )
    if not readiness.ready_for_loop:
        decision = ImplementationDecision(
            candidate.candidate_id,
            ImplementationStage.CANDIDATE,
            "RETEST",
            False,
            "approved-candidate closure blocked by incomplete implementation evidence",
        )
        return GovernedLoopHandoff(
            candidate.candidate_id, readiness, decision, None, "CANDIDATE",
        )

    if not evolution_gate_approved or not elo_implementation_approved:
        decision = ImplementationDecision(
            candidate.candidate_id,
            ImplementationStage.ELO_REVIEW,
            "READY_FOR_ELO_REVIEW",
            False,
            "explicit Evolution Gate approval and implementation authorization are both required",
        )
        return GovernedLoopHandoff(
            candidate.candidate_id, readiness, decision, None, "ELO_REVIEW",
        )

    decision = run_implementation_loop(
        candidate,
        adaptation,
        baseline,
        adapted,
        repeatable=repeatable,
        elo_approved=True,
        regressions=regressions,
        metric_directions=metric_directions,
    )
    next_state = (
        "IMPLEMENTATION_AUTHORIZED"
        if decision.result == "IMPLEMENTATION_AUTHORIZED"
        else decision.stage.value
    )
    return GovernedLoopHandoff(
        candidate.candidate_id, readiness, decision, None, next_state,
    )



__all__ = ["GovernedLoopHandoff", "advance_to_implementation", "approval_to_implementation", "close_approved_candidate"]
