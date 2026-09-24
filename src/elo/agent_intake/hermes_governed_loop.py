"""Single governed handoff across the existing ELO capability loops.

This module composes existing gates and now exposes mandatory governance
read views at the start and end of each Symbiont implementation handoff.
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
from .symbiont_implementation_view import (
    ImplementationOwnership,
    SymbiontImplementationView,
    create_loop_views,
)


@dataclass(frozen=True, slots=True)
class ImplementationGovernanceContext:
    """Canonical attachment information supplied by the caller."""

    functional_branch: str
    capability: str
    source_ref: str
    source_commit: str
    specialization: str | None = None
    ownership: ImplementationOwnership = ImplementationOwnership.EXTENSION
    related_contracts: tuple[str, ...] = ()
    dependencies: tuple[str, ...] = ()
    environment: str = "CONTROLLED_TEST"
    evolution_gate_status: str = "NOT_EVALUATED"
    governance_status: str = "NOT_EVALUATED"
    runtime_status: str = "NOT_DEPLOYED"


@dataclass(frozen=True, slots=True)
class GovernedLoopHandoff:
    candidate_id: str
    loop_readiness: LoopReadiness
    implementation: ImplementationDecision
    approval_readiness: ApprovalReadiness | None
    next_state: str
    start_view: SymbiontImplementationView
    end_view: SymbiontImplementationView
    canonical_mutation: bool = False


def _unresolved_context() -> ImplementationGovernanceContext:
    return ImplementationGovernanceContext(
        functional_branch="UNRESOLVED",
        capability="UNRESOLVED",
        source_ref="UNRESOLVED",
        source_commit="UNRESOLVED",
        ownership=ImplementationOwnership.UNRESOLVED,
    )


def _views(
    candidate: HermesCandidate,
    context: ImplementationGovernanceContext,
    *,
    stage: str,
    result: str | None,
    evidence_refs: tuple[str, ...] = (),
) -> tuple[SymbiontImplementationView, SymbiontImplementationView]:
    return create_loop_views(
        implementation_id=f"symbiont:{candidate.candidate_id}",
        candidate_id=candidate.candidate_id,
        owner=candidate.owner,
        functional_branch=context.functional_branch,
        capability=context.capability,
        source_ref=context.source_ref,
        source_commit=context.source_commit,
        end_stage=stage,
        end_result=result,
        specialization=context.specialization,
        ownership=context.ownership,
        related_contracts=context.related_contracts,
        dependencies=context.dependencies,
        evidence_refs=tuple(evidence_refs),
        environment=context.environment,
        evolution_gate_status=context.evolution_gate_status,
        governance_status=context.governance_status,
        runtime_status=context.runtime_status,
    )


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
    governance_context: ImplementationGovernanceContext | None = None,
) -> GovernedLoopHandoff:
    """Compose preflight, implementation and governance read views.

    Every invocation produces START and END views. Missing attachment context
    is surfaced as GOVERNANCE_LINK_REQUIRED rather than silently inferred.
    """
    context = governance_context or _unresolved_context()
    start_view, _ = _views(candidate, context, stage="OBSERVED", result=None, evidence_refs=provenance_refs)

    readiness = assess_loop_readiness(
        candidate, adaptation, baseline, adapted,
        metric_directions=metric_directions,
        repeatable=repeatable, regressions=regressions,
        provenance_refs=provenance_refs, boundary_integrity=boundary_integrity,
    )

    if context.ownership == ImplementationOwnership.UNRESOLVED:
        decision = ImplementationDecision(
            candidate.candidate_id, ImplementationStage.CANDIDATE,
            "RETEST", False, "implementation ownership/branch linkage is unresolved",
        )
        _, end_view = _views(candidate, context, stage=decision.stage.value, result=decision.result, evidence_refs=provenance_refs)
        return GovernedLoopHandoff(
            candidate.candidate_id, readiness, decision, None,
            "GOVERNANCE_LINK_REQUIRED", start_view, end_view,
        )

    if not readiness.ready_for_loop:
        decision = ImplementationDecision(
            candidate.candidate_id, ImplementationStage.CANDIDATE,
            "RETEST", False, "implementation-loop entry evidence is incomplete",
        )
        _, end_view = _views(candidate, context, stage=decision.stage.value, result=decision.result)
        return GovernedLoopHandoff(
            candidate.candidate_id, readiness, decision, None, "CANDIDATE",
            start_view, end_view,
        )

    decision = run_implementation_loop(
        candidate,
        adaptation,
        baseline,
        adapted,
        repeatable=repeatable,
        elo_approved=(elo_approved and evolution_gate_approved),
        regressions=regressions,
        metric_directions=metric_directions,
    )
    if decision.result == "IMPLEMENTATION_AUTHORIZED":
        next_state = "IMPLEMENTATION_AUTHORIZED"
    elif decision.result == "READY_FOR_ELO_REVIEW":
        next_state = "ELO_REVIEW"
    else:
        next_state = decision.stage.value

    _, end_view = _views(
        candidate, context, stage=decision.stage.value, result=decision.result,
    )
    return GovernedLoopHandoff(
        candidate.candidate_id, readiness, decision, None, next_state,
        start_view, end_view,
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
    governance_context: ImplementationGovernanceContext | None = None,
) -> GovernedLoopHandoff:
    """Close an approved candidate while emitting both governance views."""
    context = governance_context or _unresolved_context()
    start_view, _ = _views(candidate, context, stage="OBSERVED", result=None)

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

    if context.ownership == ImplementationOwnership.UNRESOLVED:
        decision = ImplementationDecision(
            candidate.candidate_id,
            ImplementationStage.CANDIDATE,
            "RETEST",
            False,
            "implementation ownership/branch linkage is unresolved",
        )
        _, end_view = _views(candidate, context, stage=decision.stage.value, result=decision.result)
        return GovernedLoopHandoff(
            candidate.candidate_id, readiness, decision, None,
            "GOVERNANCE_LINK_REQUIRED", start_view, end_view,
        )

    if not readiness.ready_for_loop:
        decision = ImplementationDecision(
            candidate.candidate_id,
            ImplementationStage.CANDIDATE,
            "RETEST",
            False,
            "approved-candidate closure blocked by incomplete implementation evidence",
        )
        _, end_view = _views(candidate, context, stage=decision.stage.value, result=decision.result)
        return GovernedLoopHandoff(
            candidate.candidate_id, readiness, decision, None, "CANDIDATE",
            start_view, end_view,
        )

    if not evolution_gate_approved or not elo_implementation_approved:
        decision = ImplementationDecision(
            candidate.candidate_id,
            ImplementationStage.ELO_REVIEW,
            "READY_FOR_ELO_REVIEW",
            False,
            "explicit Evolution Gate approval and implementation authorization are both required",
        )
        _, end_view = _views(candidate, context, stage=decision.stage.value, result=decision.result)
        return GovernedLoopHandoff(
            candidate.candidate_id, readiness, decision, None, "ELO_REVIEW",
            start_view, end_view,
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
    _, end_view = _views(
        candidate, context, stage=decision.stage.value, result=decision.result,
    )
    return GovernedLoopHandoff(
        candidate.candidate_id, readiness, decision, None, next_state,
        start_view, end_view,
    )


__all__ = [
    "GovernedLoopHandoff",
    "ImplementationGovernanceContext",
    "advance_to_implementation",
    "approval_to_implementation",
    "close_approved_candidate",
]
