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
    requires_human_validation: bool = False,
) -> RequirementClaim:
    return RequirementClaim(
        claim_id=claim_id,
        requirement_id=requirement_id,
        subject="MLT-C08",
        predicate=predicate,
        value=value,
        state=RequirementState.KNOWN,
        provenance=ClaimProvenance(
            source_type=RequirementSourceType.RULE,
            source_reference=f"fixture:{claim_id}",
            reasoning_method="fixture",
            evidence_ids=(f"EV-{claim_id}",),
            validation_status="VALIDATED",
        ),
        requires_human_validation=requires_human_validation,
    )


def test_pending_supporting_claim_blocks_dependency_before_provider_execution():
    prerequisite_claim = _claim(
        claim_id="R1-PENDING",
        requirement_id="R1",
        predicate="base.width",
        value="2.44 m",
        requires_human_validation=True,
    )
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
        state=RequirementState.KNOWN,
        reasons=("fixture assessment appears resolved",),
        evidence_ids=("EV-R1-PENDING",),
        human_validation_required=False,
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
