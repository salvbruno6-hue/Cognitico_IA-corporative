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
    resolve_requirement_with_dependencies,
)
from elo.cognitive.reasoning.requirement_resolution import (
    RequirementResolutionFlow,
    ResolutionStepResult,
)
from elo.cognitive.reasoning.semantic_matching import _stable_claim_id


def _claim(
    *,
    claim_id: str,
    requirement_id: str,
    predicate: str,
    value: str,
    state: RequirementState,
    source_type: RequirementSourceType,
    evidence_ids: tuple[str, ...],
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
            evidence_ids=evidence_ids,
            validation_status="VALIDATED",
        ),
    )


@dataclass
class FakeProvider:
    kind: ResolutionAttemptKind
    result: ResolutionStepResult

    def resolve(self, node, parameter, claims):
        return self.result


def test_retrieved_claim_rebinding_uses_exact_object_when_claim_ids_collide():
    prerequisite_claim = _claim(
        claim_id="R1-KNOWN",
        requirement_id="R1",
        predicate="base.width",
        value="2.44 m",
        state=RequirementState.KNOWN,
        source_type=RequirementSourceType.RULE,
        evidence_ids=("EV-R1",),
    )
    prerequisite = RequirementNode(requirement_id="R1", text="base")

    candidate = _claim(
        claim_id="R2-RETRIEVAL-SOURCE",
        requirement_id="R2",
        predicate="mdf.thickness",
        value="15 mm",
        state=RequirementState.KNOWN,
        source_type=RequirementSourceType.ELO,
        evidence_ids=("EV-RETRIEVAL",),
    )
    retrieved_claim_id = _stable_claim_id(
        "R2",
        "mdf.thickness",
        candidate.claim_id,
        candidate.value,
        candidate.provenance.source_reference,
    )
    preloaded_collision = _claim(
        claim_id=retrieved_claim_id,
        requirement_id="R2",
        predicate="unrelated.parameter",
        value="stale-hypothesis",
        state=RequirementState.INFERRED,
        source_type=RequirementSourceType.EXPERIENCE,
        evidence_ids=("EV-STALE",),
    )
    downstream = RequirementNode(
        requirement_id="R2",
        text="dependent",
        entity="MLT-C08",
        claims=(preloaded_collision,),
        requirement_dependencies=("R1",),
    )
    provider = FakeProvider(
        kind=ResolutionAttemptKind.RETRIEVAL,
        result=ResolutionStepResult(
            source_reference="fixture:retrieval",
            claims=(candidate,),
        ),
    )
    assessment = GapAssessment(
        requirement_id="R1",
        parameter="base.width",
        state=RequirementState.KNOWN,
        reasons=("fixture",),
        evidence_ids=("EV-R1",),
    )

    result = resolve_requirement_with_dependencies(
        flow=RequirementResolutionFlow(
            providers={ResolutionAttemptKind.RETRIEVAL: provider}
        ),
        graph=RequirementDependencyGraph((downstream, prerequisite)),
        node=downstream,
        parameter="mdf.thickness",
        prerequisite_assessments={"R1": assessment},
        prerequisite_claims={"R1": (prerequisite_claim,)},
    )

    nested = result.resolution.retrieval_resolution
    assert nested is not None
    assert nested.retrieved_claim is not None

    collisions = tuple(
        claim
        for claim in result.resolution.claims
        if claim.claim_id == retrieved_claim_id
    )
    assert len(collisions) == 2

    stale, retrieved = collisions
    assert stale.state is RequirementState.INFERRED
    assert stale.value == "stale-hypothesis"
    assert stale.dependencies == ()

    assert retrieved.state is RequirementState.RETRIEVED
    assert retrieved.value == "15 mm"
    assert nested.retrieved_claim == retrieved
    assert "R1" in retrieved.dependencies
    assert "R1-KNOWN" in retrieved.dependencies
    assert "EV-R1" in retrieved.provenance.evidence_ids
    assert "requirement-dependencies:v1" in retrieved.provenance.reasoning_method
