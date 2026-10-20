from elo.core.skill_approval_deployment_loop import (
    ApprovedSkillCandidate,
    DeploymentReceipt,
    ImplementationDecision,
    SkillApprovalDeploymentLoop,
    SkillApprovalState,
)


def candidate() -> ApprovedSkillCandidate:
    return ApprovedSkillCandidate(
        candidate_id="candidate-001",
        skill_id="symbiont.operational_boundary",
        approval_ref="approval-001",
        evidence_refs=("e-001",),
    )


def test_approved_candidate_deploys_automatically_after_explicit_implementation_decision():
    loop = SkillApprovalDeploymentLoop()
    cycle = loop.decide(candidate(), ImplementationDecision.APPROVE)

    deployed = loop.deploy(
        cycle,
        lambda c: DeploymentReceipt(
            candidate_id=c.candidate_id,
            deployment_ref="deploy-001",
            success=True,
            evidence_refs=("deploy-e-001",),
        ),
    )

    observed = loop.start_observation(deployed)
    outcome = loop.record_outcome(observed, outcome_evidence_refs=("outcome-001",))
    reviewed = loop.review(outcome)

    assert reviewed.state is SkillApprovalState.REVIEW
    assert reviewed.history == (
        SkillApprovalState.APPROVED,
        SkillApprovalState.IMPLEMENTATION_DECIDED,
        SkillApprovalState.DEPLOYED,
        SkillApprovalState.OBSERVING,
        SkillApprovalState.OUTCOME,
        SkillApprovalState.REVIEW,
    )


def test_unapproved_candidate_cannot_enter_deployment():
    loop = SkillApprovalDeploymentLoop()
    pending = ApprovedSkillCandidate(
        candidate_id="candidate-002",
        skill_id="symbiont.lab",
        approval_ref="",
        evidence_refs=(),
        state=SkillApprovalState.BLOCKED,
    )

    try:
        loop.decide(pending, ImplementationDecision.APPROVE)
    except ValueError:
        pass
    else:
        raise AssertionError("unapproved candidate must fail closed")


def test_hold_or_reject_does_not_deploy():
    loop = SkillApprovalDeploymentLoop()
    cycle = loop.decide(candidate(), ImplementationDecision.HOLD)

    assert cycle.state is SkillApprovalState.BLOCKED
    assert cycle.deployment is None


def test_failed_deployment_blocks_post_approval_flow():
    loop = SkillApprovalDeploymentLoop()
    cycle = loop.decide(candidate(), ImplementationDecision.APPROVE)

    blocked = loop.deploy(
        cycle,
        lambda c: DeploymentReceipt(
            candidate_id=c.candidate_id,
            deployment_ref="deploy-failed",
            success=False,
            evidence_refs=("deploy-error",),
        ),
    )

    assert blocked.state is SkillApprovalState.BLOCKED
    assert blocked.history[-1] is SkillApprovalState.BLOCKED
