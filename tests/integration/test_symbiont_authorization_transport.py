"""Integration evidence for canonical authorization transport into Symbiont pre-intake.

The test intentionally uses the existing AuthorizationDecision transport contract.
It does not mock or reimplement elo-authz policy.
"""

from elo.application.use_cases.orchestrator import AuthorizationDecision
from elo.cognitive.symbiont_pattern_intake import SkillComponent, SymbiontPatternIntake


def canonical_decision(evidence_ref: str = "authz-transport-001") -> AuthorizationDecision:
    return AuthorizationDecision(
        authorized=True,
        authority="elo-authz",
        identity_id="identity-a",
        role="ELO_ADMIN",
        evidence_ref=evidence_ref,
    )


def complete_component(evidence_ref: str = "authz-transport-001") -> SkillComponent:
    return SkillComponent(
        "precedent_search",
        "FOUND",
        documentation_status="FOUND",
        test_status="TESTED",
        authorization_status="COMPATIBLE",
        authorization_authority="elo-authz",
        authorization_evidence_ref=evidence_ref,
        compatibility_status="COMPATIBLE",
        baseline_status="PRESENT",
        measurement_status="PRESENT",
        regression_status="PASS",
    )


def test_canonical_authorization_decision_reaches_ready_pre_intake() -> None:
    decision = canonical_decision()
    assessment = SymbiontPatternIntake().assess_skill_creation(
        proposed_skill_id="ELO-KE-SKILL-TRANSPORT-001",
        existing_owner=None,
        components=(complete_component(),),
        authorization_decision=decision,
    )

    assert decision.is_canonical()
    assert assessment.disposition == "READY_FOR_INTAKE"
    assert assessment.ready_for_intake
    assert assessment.evidence_completeness == 1.0


def test_transport_cannot_cross_authorization_evidence_boundary() -> None:
    decision = canonical_decision("authz-transport-001")
    assessment = SymbiontPatternIntake().assess_skill_creation(
        proposed_skill_id="ELO-KE-SKILL-TRANSPORT-001",
        existing_owner=None,
        components=(complete_component("authz-other"),),
        authorization_decision=decision,
    )

    assert assessment.disposition == "DEVELOP_FIRST"
    assert not assessment.ready_for_intake
    assert "does not match" in assessment.rationale
