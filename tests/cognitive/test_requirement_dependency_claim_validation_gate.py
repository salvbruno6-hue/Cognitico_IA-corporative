from __future__ import annotations

from dataclasses import dataclass

from elo.cognitive.reasoning.requirement_analysis import (
    ClaimProvenance,
    GapAssessment,
    RequirementClaim,
    RequirementNode,
    RequirementSourceType,
    RequirementState,
    ResolutionAttemptKind,
)
from elo.cognitive.reasoning.requirement_dependencies import (
    RequirementDependencyGraph,
    RequirementDependencyState,
    resolve_requirement_with_dependencies,
)
from elo.cognitive.reasoning.requirement_resolution import (
    RequirementResolutionFlow,
    ResolutionStepResult,
)


@dataclass
class CountingProvider:
    kind: ResolutionAttemptKind
    result: ResolutionStepResult
    calls: int = 0

    def resolve(self, node, parameter, claims):
        self.calls += 1
        return self.result


def _claim(
    *,
    claim_id: str,
    requirement_id: str,
    predicate: str,
    value: str,
    state: RequirementState = RequirementState.KNOWN,
    source_type: RequirementSourceType = RequirementSourceType.RULE,
    evidence_ids: tuple[str, ...] | None = None,
    requires_human_validation: bool = False,
    validation_status: str = "VALIDATED",
) -> RequirementClaim:
    return RequirementClaim(
        claim_id=claim_id,
        requirement_id=requirement_id,
        subject="MLT-C08",
        predicate=predicate,
        value=value,
        state=state,
        provenance=ClaimProvenance(
            source_type=source_type,
            source_reference=f"fixture:{claim_id}",
            reasoning_method="fixture",
            evidence_ids=(
                (f"EV-{claim_id}",) if evidence_ids is None else evidence_ids
            ),
            validation_status=validation_status,
        ),
        requires_human_validation=requires_human_validation,
    )


def _resolution_fixture(prerequisite_claim: RequirementClaim):
    prerequisite = RequirementNode(
        requirement_id="R1",
        text="base width",
        claims=(prerequisite_claim,),
    )
    downstream = RequirementNode(
        requirement_id="R2",
        text="dependent requirement",
        entity="MLT-C08",
        requirement_dependencies=("R1",),
    )
    downstream_claim = _claim(
        claim_id="R2-RULE",
        requirement_id="R2",
        predicate="output.value",
        value="approved",
    )
    provider = CountingProvider(
        kind=ResolutionAttemptKind.RULE,
        result=ResolutionStepResult(
            source_reference="fixture:rule",
            claims=(downstream_claim,),
        ),
    )
    graph = RequirementDependencyGraph((prerequisite, downstream))
    prerequisite_assessment = GapAssessment(
        requirement_id="R1",
        parameter="base.width",
        state=prerequisite_claim.state,
        reasons=("fixture assessment appears resolved",),
        evidence_ids=prerequisite_claim.provenance.evidence_ids,
        human_validation_required=False,
    )
    return downstream, provider, graph, prerequisite_assessment


def test_pending_supporting_claim_blocks_dependency_before_provider_execution():
    prerequisite_claim = _claim(
        claim_id="R1-PENDING",
        requirement_id="R1",
        predicate="base.width",
        value="2.44 m",
        requires_human_validation=True,
    )
    downstream, provider, graph, prerequisite_assessment = _resolution_fixture(
        prerequisite_claim
    )

    result = resolve_requirement_with_dependencies(
        flow=RequirementResolutionFlow(
            providers={ResolutionAttemptKind.RULE: provider}
        ),
        graph=graph,
        node=downstream,
        parameter="output.value",
        prerequisite_assessments={"R1": prerequisite_assessment},
    )

    assert provider.calls == 0
    assert result.dependency_assessment.state is RequirementDependencyState.BLOCKED
    assert result.dependency_assessment.dependency_claim_ids == ()
    assert result.dependency_assessment.blockers[0].human_validation_required is True
    assert result.resolution.attempts == ()
    assert result.resolution.assessment.state is RequirementState.BLOCKED
    assert result.resolution.assessment.state is not RequirementState.GAP_CONFIRMED
    assert result.resolution.assessment.human_validation_required is True


def test_unverified_supporting_claim_reuses_canonical_trust_and_blocks_downstream():
    prerequisite_claim = _claim(
        claim_id="R1-UNVERIFIED",
        requirement_id="R1",
        predicate="base.width",
        value="2.44 m",
        validation_status="UNVERIFIED",
    )
    downstream, provider, graph, prerequisite_assessment = _resolution_fixture(
        prerequisite_claim
    )

    result = resolve_requirement_with_dependencies(
        flow=RequirementResolutionFlow(
            providers={ResolutionAttemptKind.RULE: provider}
        ),
        graph=graph,
        node=downstream,
        parameter="output.value",
        prerequisite_assessments={"R1": prerequisite_assessment},
    )

    blocker = result.dependency_assessment.blockers[0]
    assert provider.calls == 0
    assert result.dependency_assessment.state is RequirementDependencyState.BLOCKED
    assert result.dependency_assessment.dependency_claim_ids == ()
    assert blocker.human_validation_required is False
    assert blocker.automatic_trust_failed is True
    assert result.resolution.attempts == ()
    assert result.resolution.claims == ()
    assert result.resolution.assessment.state is RequirementState.BLOCKED
    assert result.resolution.assessment.state is not RequirementState.GAP_CONFIRMED
    assert result.resolution.assessment.human_validation_required is False


def test_llm_inference_cannot_supply_automatic_dependency_support():
    prerequisite_claim = _claim(
        claim_id="R1-LLM",
        requirement_id="R1",
        predicate="base.width",
        value="2.44 m",
        source_type=RequirementSourceType.LLM_INFERENCE,
    )
    downstream, provider, graph, prerequisite_assessment = _resolution_fixture(
        prerequisite_claim
    )

    result = resolve_requirement_with_dependencies(
        flow=RequirementResolutionFlow(
            providers={ResolutionAttemptKind.RULE: provider}
        ),
        graph=graph,
        node=downstream,
        parameter="output.value",
        prerequisite_assessments={"R1": prerequisite_assessment},
    )

    blocker = result.dependency_assessment.blockers[0]
    assert provider.calls == 0
    assert result.dependency_assessment.state is RequirementDependencyState.BLOCKED
    assert result.dependency_assessment.dependency_claim_ids == ()
    assert result.dependency_assessment.evidence_ids == ("EV-R1-LLM",)
    assert blocker.evidence_ids == ("EV-R1-LLM",)
    assert blocker.automatic_trust_failed is True
    assert result.resolution.attempts == ()
    assert result.resolution.claims == ()
    assert result.resolution.assessment.state is RequirementState.BLOCKED
    assert result.resolution.assessment.state is not RequirementState.GAP_CONFIRMED


def test_documented_extraction_exception_remains_valid_dependency_support():
    prerequisite_claim = _claim(
        claim_id="R1-DOCUMENTED",
        requirement_id="R1",
        predicate="base.width",
        value="2.44 m",
        state=RequirementState.DOCUMENTED,
        source_type=RequirementSourceType.DOCUMENT,
        evidence_ids=(),
        validation_status="EXTRACTED",
    )
    downstream, provider, graph, prerequisite_assessment = _resolution_fixture(
        prerequisite_claim
    )

    result = resolve_requirement_with_dependencies(
        flow=RequirementResolutionFlow(
            providers={ResolutionAttemptKind.RULE: provider}
        ),
        graph=graph,
        node=downstream,
        parameter="output.value",
        prerequisite_assessments={"R1": prerequisite_assessment},
    )

    assert provider.calls == 1
    assert result.dependency_assessment.state is RequirementDependencyState.READY
    assert result.dependency_assessment.blockers == ()
    assert result.dependency_assessment.dependency_claim_ids == ("R1-DOCUMENTED",)
    assert result.dependency_assessment.evidence_ids == ()
    assert result.resolution.assessment.state is RequirementState.KNOWN


def test_claimless_resolved_assessment_cannot_unlock_downstream_provider():
    prerequisite = RequirementNode(requirement_id="R1", text="base width")
    downstream = RequirementNode(
        requirement_id="R2",
        text="dependent requirement",
        entity="MLT-C08",
        requirement_dependencies=("R1",),
    )
    downstream_claim = _claim(
        claim_id="R2-RULE",
        requirement_id="R2",
        predicate="output.value",
        value="approved",
    )
    provider = CountingProvider(
        kind=ResolutionAttemptKind.RULE,
        result=ResolutionStepResult(
            source_reference="fixture:rule",
            claims=(downstream_claim,),
        ),
    )
    graph = RequirementDependencyGraph((prerequisite, downstream))
    forged_summary = GapAssessment(
        requirement_id="R1",
        parameter="base.width",
        state=RequirementState.KNOWN,
        reasons=("summary without factual supporting claim",),
        evidence_ids=("EV-SUMMARY",),
        human_validation_required=False,
    )

    result = resolve_requirement_with_dependencies(
        flow=RequirementResolutionFlow(
            providers={ResolutionAttemptKind.RULE: provider}
        ),
        graph=graph,
        node=downstream,
        parameter="output.value",
        prerequisite_assessments={"R1": forged_summary},
    )

    blocker = result.dependency_assessment.blockers[0]
    assert provider.calls == 0
    assert result.dependency_assessment.state is RequirementDependencyState.BLOCKED
    assert result.dependency_assessment.dependency_claim_ids == ()
    assert result.dependency_assessment.evidence_ids == ("EV-SUMMARY",)
    assert blocker.automatic_trust_failed is True
    assert blocker.evidence_ids == ("EV-SUMMARY",)
    assert result.resolution.attempts == ()
    assert result.resolution.claims == ()
    assert result.resolution.assessment.state is RequirementState.BLOCKED
    assert result.resolution.assessment.state is not RequirementState.GAP_CONFIRMED
