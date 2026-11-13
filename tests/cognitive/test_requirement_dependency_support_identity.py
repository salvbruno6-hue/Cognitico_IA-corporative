from __future__ import annotations

from dataclasses import dataclass

import pytest

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
    calls: int = 0

    def resolve(self, node, parameter, claims):
        self.calls += 1
        resolved = RequirementClaim(
            claim_id="R2-RULE",
            requirement_id="R2",
            subject="MLT-C08",
            predicate=parameter,
            value="resolved",
            state=RequirementState.KNOWN,
            provenance=ClaimProvenance(
                source_type=RequirementSourceType.RULE,
                source_reference="fixture:downstream-rule",
                reasoning_method="fixture",
                evidence_ids=("EV-R2",),
                validation_status="VALIDATED",
            ),
        )
        return ResolutionStepResult(
            source_reference="fixture:downstream-rule",
            claims=(resolved,),
        )


@pytest.mark.parametrize("claim_id", (" R1-SUPPORT ", "   "))
def test_noncanonical_supporting_claim_id_blocks_downstream_resolution(claim_id):
    supporting = RequirementClaim(
        claim_id=claim_id,
        requirement_id="R1",
        subject="MLT-C08",
        predicate="base.width",
        value="2.44 m",
        state=RequirementState.KNOWN,
        provenance=ClaimProvenance(
            source_type=RequirementSourceType.RULE,
            source_reference="fixture:prerequisite-rule",
            reasoning_method="fixture",
            evidence_ids=("EV-R1",),
            validation_status="VALIDATED",
        ),
    )
    prerequisite = RequirementNode(
        requirement_id="R1",
        text="base width",
        claims=(supporting,),
    )
    downstream = RequirementNode(
        requirement_id="R2",
        text="dependent output",
        entity="MLT-C08",
        requirement_dependencies=("R1",),
    )
    graph = RequirementDependencyGraph((prerequisite, downstream))
    provider = CountingProvider(kind=ResolutionAttemptKind.RULE)

    result = resolve_requirement_with_dependencies(
        flow=RequirementResolutionFlow(
            providers={ResolutionAttemptKind.RULE: provider}
        ),
        graph=graph,
        node=downstream,
        parameter="output.value",
        prerequisite_assessments={
            "R1": GapAssessment(
                requirement_id="R1",
                parameter="base.width",
                state=RequirementState.KNOWN,
                reasons=("fixture",),
                evidence_ids=("EV-R1",),
            )
        },
    )

    assert provider.calls == 0
    assert result.dependency_assessment.state is RequirementDependencyState.BLOCKED
    assert result.dependency_assessment.dependency_claim_ids == ()
    assert result.dependency_assessment.blockers[0].automatic_trust_failed is True
    assert result.dependency_assessment.evidence_ids == ("EV-R1",)
    assert result.resolution.assessment.state is RequirementState.BLOCKED
    assert result.resolution.assessment.state is not RequirementState.GAP_CONFIRMED
