"""Governed post-approval loop for ELO skills.

This module does not grant approval and does not promote canonical authority.
It only consumes an already-approved candidate plus an explicit implementation
decision, then advances the candidate into controlled deployment/observation.

Canonical chain:
APPROVED -> IMPLEMENTATION_DECIDED -> DEPLOYED/USED -> OBSERVING -> OUTCOME -> REVIEW

Any missing approval, implementation decision, evidence, or deployment result
fails closed.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Callable


class SkillApprovalState(StrEnum):
    APPROVED = "approved"
    IMPLEMENTATION_DECIDED = "implementation_decided"
    DEPLOYED = "deployed"
    OBSERVING = "observing"
    OUTCOME = "outcome"
    REVIEW = "review"
    BLOCKED = "blocked"


class ImplementationDecision(StrEnum):
    APPROVE = "approve"
    HOLD = "hold"
    REJECT = "reject"


@dataclass(frozen=True)
class ApprovedSkillCandidate:
    candidate_id: str
    skill_id: str
    approval_ref: str
    evidence_refs: tuple[str, ...]
    state: SkillApprovalState = SkillApprovalState.APPROVED


@dataclass(frozen=True)
class DeploymentReceipt:
    candidate_id: str
    deployment_ref: str
    success: bool
    evidence_refs: tuple[str, ...]


@dataclass(frozen=True)
class SkillApprovalCycle:
    candidate: ApprovedSkillCandidate
    decision: ImplementationDecision | None = None
    state: SkillApprovalState = SkillApprovalState.APPROVED
    deployment: DeploymentReceipt | None = None
    history: tuple[SkillApprovalState, ...] = (SkillApprovalState.APPROVED,)


DeployFn = Callable[[ApprovedSkillCandidate], DeploymentReceipt]


class SkillApprovalDeploymentLoop:
    """Advance explicitly approved candidates after an implementation decision."""

    def decide(
        self,
        candidate: ApprovedSkillCandidate,
        decision: ImplementationDecision,
    ) -> SkillApprovalCycle:
        if candidate.state is not SkillApprovalState.APPROVED:
            raise ValueError("candidate must be explicitly approved")
        if not candidate.candidate_id or not candidate.skill_id:
            raise ValueError("candidate identity is required")
        if not candidate.approval_ref:
            raise ValueError("approval reference is required")
        if not candidate.evidence_refs:
            raise ValueError("approval evidence is required")

        if decision is not ImplementationDecision.APPROVE:
            return SkillApprovalCycle(
                candidate=candidate,
                decision=decision,
                state=SkillApprovalState.BLOCKED,
                history=(SkillApprovalState.APPROVED, SkillApprovalState.BLOCKED),
            )

        return SkillApprovalCycle(
            candidate=candidate,
            decision=decision,
            state=SkillApprovalState.IMPLEMENTATION_DECIDED,
            history=(
                SkillApprovalState.APPROVED,
                SkillApprovalState.IMPLEMENTATION_DECIDED,
            ),
        )

    def deploy(
        self,
        cycle: SkillApprovalCycle,
        deploy: DeployFn,
    ) -> SkillApprovalCycle:
        if cycle.state is not SkillApprovalState.IMPLEMENTATION_DECIDED:
            raise ValueError("deployment requires an approved implementation decision")
        receipt = deploy(cycle.candidate)
        if receipt.candidate_id != cycle.candidate.candidate_id:
            raise ValueError("deployment receipt candidate mismatch")
        if not receipt.success:
            return SkillApprovalCycle(
                candidate=cycle.candidate,
                decision=cycle.decision,
                state=SkillApprovalState.BLOCKED,
                deployment=receipt,
                history=cycle.history + (SkillApprovalState.BLOCKED,),
            )
        if not receipt.deployment_ref or not receipt.evidence_refs:
            raise ValueError("successful deployment requires reference and evidence")

        return SkillApprovalCycle(
            candidate=cycle.candidate,
            decision=cycle.decision,
            state=SkillApprovalState.DEPLOYED,
            deployment=receipt,
            history=cycle.history + (SkillApprovalState.DEPLOYED,),
        )

    def start_observation(self, cycle: SkillApprovalCycle) -> SkillApprovalCycle:
        if cycle.state is not SkillApprovalState.DEPLOYED:
            raise ValueError("observation requires successful deployment")
        return SkillApprovalCycle(
            candidate=cycle.candidate,
            decision=cycle.decision,
            state=SkillApprovalState.OBSERVING,
            deployment=cycle.deployment,
            history=cycle.history + (SkillApprovalState.OBSERVING,),
        )

    def record_outcome(
        self,
        cycle: SkillApprovalCycle,
        *,
        outcome_evidence_refs: tuple[str, ...],
    ) -> SkillApprovalCycle:
        if cycle.state is not SkillApprovalState.OBSERVING:
            raise ValueError("outcome requires observation")
        if not outcome_evidence_refs:
            raise ValueError("outcome evidence is required")
        return SkillApprovalCycle(
            candidate=cycle.candidate,
            decision=cycle.decision,
            state=SkillApprovalState.OUTCOME,
            deployment=cycle.deployment,
            history=cycle.history + (SkillApprovalState.OUTCOME,),
        )

    def review(self, cycle: SkillApprovalCycle) -> SkillApprovalCycle:
        if cycle.state is not SkillApprovalState.OUTCOME:
            raise ValueError("post-approval review requires an outcome")
        return SkillApprovalCycle(
            candidate=cycle.candidate,
            decision=cycle.decision,
            state=SkillApprovalState.REVIEW,
            deployment=cycle.deployment,
            history=cycle.history + (SkillApprovalState.REVIEW,),
        )
