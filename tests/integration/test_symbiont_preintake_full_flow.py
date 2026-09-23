"""End-to-end evidence for the canonical Symbiont pre-intake flow.

The test composes existing authorities only:
SpecialistSkillResolver -> evidence assessment -> canonical elo-authz transport
-> compatibility/measurement/regression evidence -> READY_FOR_INTAKE
-> Evolution Gate.

It does not create or mock a new authority.
"""

from elo.application.use_cases.orchestrator import AuthorizationDecision
from elo.cognitive.symbiont_pattern_intake import SkillComponent, SymbiontPatternIntake
from elo.core.evolution_gate import EvolutionClassification, EvolutionGate, EvolutionProposal
from elo.core.specialist_skill_resolution import SpecialistSkill, SpecialistSkillResolver


def test_full_preintake_flow_reaches_evolution_gate_without_new_authority() -> None:
    resolver = SpecialistSkillResolver(
        [
            SpecialistSkill(
                skill_id="FORGE-PRECEDENT-001",
                domain_family="KNOWLEDGE",
                maturity="GOVERNED",
                scope="tenant:lab",
                boundaries="evidence-only",
                authorization_required=True,
            )
        ]
    )

    resolution = resolver.resolve(
        domain_family="KNOWLEDGE",
        authorized=lambda skill: skill.scope == "tenant:lab"
        and skill.boundaries == "evidence-only",
        minimum_maturity="GOVERNED",
    )
    assert resolution.resolved
    assert resolution.skill_id == "FORGE-PRECEDENT-001"

    authorization = AuthorizationDecision(
        authorized=True,
        authority="elo-authz",
        identity_id="identity-a",
        role="ELO_ADMIN",
        evidence_ref="authz-full-flow-001",
    )

    component = SkillComponent(
        "precedent_search",
        "FOUND",
        path="src/elo/cognitive",
        documentation_status="FOUND",
        test_status="TESTED",
        authorization_status="COMPATIBLE",
        authorization_authority="elo-authz",
        authorization_evidence_ref="authz-full-flow-001",
        compatibility_status="COMPATIBLE",
        baseline_status="PRESENT",
        measurement_status="PRESENT",
        regression_status="PASS",
    )

    assessment = SymbiontPatternIntake().assess_skill_creation(
        proposed_skill_id="ELO-KE-SKILL-PREINTAKE-FULL-001",
        existing_owner=None,
        domain_family="KNOWLEDGE",
        skill_resolver=resolver,
        components=(component,),
        authorization_decision=authorization,
    )

    assert assessment.existing_owner is None
    assert assessment.disposition == "READY_FOR_INTAKE"
    assert assessment.ready_for_intake
    assert assessment.evidence_completeness == 1.0
    assert assessment.blocking_gaps == ()

    proposal = EvolutionProposal(
        proposal_id="evolution-preintake-full-001",
        tenant_id="tenant-lab",
        source_id="ELO-KE-SKILL-PREINTAKE-FULL-001",
        summary="Validated pre-intake candidate with complete governed evidence",
        purpose_alignment=True,
        identity_compatible=True,
        architecture_compatible=True,
        governance_compatible=True,
        evidence_ids=("authz-full-flow-001",),
        maturity_score=1.0,
        provenance={
            "source": "symbiont-preintake-full-flow",
            "owner": resolution.skill_id,
            "authorization_authority": authorization.authority,
            "authorization_evidence_ref": authorization.evidence_ref,
        },
    )

    decision = EvolutionGate().evaluate(proposal)

    assert decision.classification is EvolutionClassification.COMPATIBLE
    assert decision.canonical_mutation_allowed is False
    assert decision.preserve_as_alternative is False
    assert decision.human_decision_required is False
    assert decision.evidence_ids == ("authz-full-flow-001",)
