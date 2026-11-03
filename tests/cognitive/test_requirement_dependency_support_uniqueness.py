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
    calls: int = 0

    def resolve(self, node, parameter, claims):
        self.calls += 1
        resolved = RequirementClaim(
            claim_id=f"{node.requirement_id}-RULE",
            requirement_id=node.requirement_id,
            subject=node.entity or "MLT-C08",
            predicate=parameter,
            value="resolved",
            state=RequirementState.KNOWN,
            provenance=ClaimProvenance(
                source_type=RequirementSourceType.RULE,
                source_reference="fixture:downstream-rule",
                reasoning_method="fixture",
                evidence_ids=("EV-DOWNSTREAM",),
                validation_status="VALIDATED",
            ),
        )
        return ResolutionStepResult(
            source_reference="fixture:downstream-rule",
            claims=(resolved,),
        )


def _claim(*, requirement_id: str, claim_id: str, evidence_id: str, source: str):
    return RequirementClaim(
        claim_id=claim_id,
        requirement_id=requirement_id,
        subject="MLT-C08",
        predicate="base.width",
        value="2.44 m",
        state=RequirementState.KNOWN,
        provenance=ClaimProvenance(
            source_type=RequirementSourceType.RULE,
            source_reference=source,
            reasoning_method="fixture",
            evidence_ids=(evidence_id,),
            validation_status="VALIDATED",
        ),
    )


def _assessment(requirement_id: str, *evidence_ids: str):
    return GapAssessment(
        requirement_id=requirement_id,
        parameter="base.width",
        state=RequirementState.KNOWN,
        reasons=("fixture",),
        evidence_ids=tuple(evidence_ids),
    )


def test_duplicate_selected_support_id_within_one_prerequisite_blocks_downstream():
    first = _claim(
        requirement_id="R1",
        claim_id="SHARED-SUPPORT",
        evidence_id="EV-R1-A",
        source="fixture:r1-a",
    )
    second = _claim(
        requirement_id="R1",
        claim_id="SHARED-SUPPORT",
        evidence_id="EV-R1-B",
        source="fixture:r1-b",
    )
    prerequisite = RequirementNode(
        requirement_id="R1",
        text="base width",
        claims=(first, second),
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
            "R1": _assessment("R1", "EV-R1-A", "EV-R1-B")
        },
    )

    assert provider.calls == 0
    assert result.dependency_assessment.state is RequirementDependencyState.BLOCKED
    assert result.dependency_assessment.dependency_claim_ids == ()
    assert result.dependency_assessment.evidence_ids == ("EV-R1-A", "EV-R1-B")
    assert result.dependency_assessment.blockers[0].automatic_trust_failed is True
    assert result.resolution.claims == ()
    assert result.resolution.assessment.state is RequirementState.BLOCKED
    assert result.resolution.assessment.state is not RequirementState.GAP_CONFIRMED


def test_duplicate_selected_support_id_across_prerequisites_blocks_downstream():
    first = _claim(
        requirement_id="R1",
        claim_id="SHARED-SUPPORT",
        evidence_id="EV-R1",
        source="fixture:r1",
    )
    second = _claim(
        requirement_id="R2",
        claim_id="SHARED-SUPPORT",
        evidence_id="EV-R2",
        source="fixture:r2",
    )
    prerequisite_one = RequirementNode(
        requirement_id="R1",
        text="first prerequisite",
        claims=(first,),
    )
    prerequisite_two = RequirementNode(
        requirement_id="R2",
        text="second prerequisite",
        claims=(second,),
    )
    downstream = RequirementNode(
        requirement_id="R3",
        text="dependent output",
        entity="MLT-C08",
        requirement_dependencies=("R1", "R2"),
    )
    graph = RequirementDependencyGraph(
        (prerequisite_one, prerequisite_two, downstream)
    )
    provider = CountingProvider(kind=ResolutionAttemptKind.RULE)

    result = resolve_requirement_with_dependencies(
        flow=RequirementResolutionFlow(
            providers={ResolutionAttemptKind.RULE: provider}
        ),
        graph=graph,
        node=downstream,
        parameter="output.value",
        prerequisite_assessments={
            "R1": _assessment("R1", "EV-R1"),
            "R2": _assessment("R2", "EV-R2"),
        },
    )

    assert provider.calls == 0
    assert result.dependency_assessment.state is RequirementDependencyState.BLOCKED
    assert result.dependency_assessment.dependency_claim_ids == ()
    assert result.dependency_assessment.evidence_ids == ("EV-R1", "EV-R2")
    assert {blocker.requirement_id for blocker in result.dependency_assessment.blockers} == {
        "R1",
        "R2",
    }
    assert all(
        blocker.automatic_trust_failed
        for blocker in result.dependency_assessment.blockers
    )
    assert result.resolution.claims == ()
    assert result.resolution.assessment.state is RequirementState.BLOCKED
    assert result.resolution.assessment.state is not RequirementState.GAP_CONFIRMED
