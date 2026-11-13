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
    audit_requirement,
)
from elo.cognitive.reasoning.requirement_dependencies import (
    RequirementDependencyGraph,
    audit_requirement_dependency_graph,
    resolve_requirement_with_dependencies,
)
from elo.cognitive.reasoning.requirement_resolution import (
    RequirementResolutionFlow,
    ResolutionStepResult,
)


def _claim(
    *,
    claim_id: str,
    requirement_id: str,
    predicate: str,
    value: str,
    state: RequirementState,
    source_type: RequirementSourceType,
    evidence_ids: tuple[str, ...],
    reasoning_method: str = "fixture",
    dependencies: tuple[str, ...] = (),
    requires_human_validation: bool = False,
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
            reasoning_method=reasoning_method,
            evidence_ids=evidence_ids,
            validation_status="VALIDATED",
        ),
        dependencies=dependencies,
        requires_human_validation=requires_human_validation,
    )


def _assessment(
    *,
    requirement_id: str,
    parameter: str,
    state: RequirementState,
    evidence_ids: tuple[str, ...],
) -> GapAssessment:
    return GapAssessment(
        requirement_id=requirement_id,
        parameter=parameter,
        state=state,
        reasons=("fixture",),
        evidence_ids=evidence_ids,
    )


@dataclass
class FakeProvider:
    kind: ResolutionAttemptKind
    result: ResolutionStepResult

    def resolve(self, node, parameter, claims):
        return self.result


def test_typed_edges_are_distinct_and_normalized_adjacency_is_auditable():
    r1 = RequirementNode(requirement_id="R1", text="base")
    r2 = RequirementNode(
        requirement_id="R2",
        text="dependent",
        dependencies=("legacy-lineage",),
        requirement_dependencies=("  R1  ",),
    )
    graph = RequirementDependencyGraph((r2, r1))

    node_audit = audit_requirement(r2)
    graph_audit = audit_requirement_dependency_graph(graph)

    assert node_audit["dependencies"] == ("legacy-lineage",)
    assert node_audit["requirement_dependencies"] == ("  R1  ",)
    assert graph_audit["adjacency"] == (("R1", ()), ("R2", ("R1",)))


def test_only_final_automatic_claim_receives_dependency_provenance():
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

    hypothesis = _claim(
        claim_id="R2-HYPOTHESIS",
        requirement_id="R2",
        predicate="output.value",
        value="draft",
        state=RequirementState.INFERRED,
        source_type=RequirementSourceType.EXPERIENCE,
        evidence_ids=("EV-HYPOTHESIS",),
        reasoning_method="prior-hypothesis:v1",
        dependencies=("prior-context",),
        requires_human_validation=True,
    )
    downstream = RequirementNode(
        requirement_id="R2",
        text="dependent",
        entity="MLT-C08",
        claims=(hypothesis,),
        requirement_dependencies=("R1",),
    )
    resolved = _claim(
        claim_id="R2-RULE",
        requirement_id="R2",
        predicate="output.value",
        value="approved",
        state=RequirementState.KNOWN,
        source_type=RequirementSourceType.RULE,
        evidence_ids=("EV-RULE",),
    )
    provider = FakeProvider(
        kind=ResolutionAttemptKind.RULE,
        result=ResolutionStepResult(
            source_reference="fixture:rule",
            claims=(resolved,),
        ),
    )
    graph = RequirementDependencyGraph((downstream, prerequisite))

    result = resolve_requirement_with_dependencies(
        flow=RequirementResolutionFlow(
            providers={ResolutionAttemptKind.RULE: provider}
        ),
        graph=graph,
        node=downstream,
        parameter="output.value",
        prerequisite_assessments={
            "R1": _assessment(
                requirement_id="R1",
                parameter="base.width",
                state=RequirementState.KNOWN,
                evidence_ids=("EV-R1",),
            )
        },
        prerequisite_claims={"R1": (prerequisite_claim,)},
    )

    returned_hypothesis = next(
        claim for claim in result.resolution.claims if claim.claim_id == hypothesis.claim_id
    )
    returned_resolved = next(
        claim for claim in result.resolution.claims if claim.claim_id == resolved.claim_id
    )

    assert returned_hypothesis.dependencies == ("prior-context",)
    assert returned_hypothesis.provenance.evidence_ids == ("EV-HYPOTHESIS",)
    assert returned_hypothesis.provenance.reasoning_method == "prior-hypothesis:v1"
    assert "requirement-dependencies:v1" not in (
        returned_hypothesis.provenance.reasoning_method
    )

    assert "R1" in returned_resolved.dependencies
    assert "R1-KNOWN" in returned_resolved.dependencies
    assert "EV-R1" in returned_resolved.provenance.evidence_ids
    assert "requirement-dependencies:v1" in (
        returned_resolved.provenance.reasoning_method
    )


def test_nested_retrieved_claim_matches_dependency_bound_result_claim():
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
    downstream = RequirementNode(
        requirement_id="R2",
        text="dependent",
        entity="MLT-C08",
        requirement_dependencies=("R1",),
    )
    candidate = _claim(
        claim_id="R2-RETRIEVAL-SOURCE",
        requirement_id="R2",
        predicate="mdf.thickness",
        value="15 mm",
        state=RequirementState.KNOWN,
        source_type=RequirementSourceType.ELO,
        evidence_ids=("EV-RETRIEVAL",),
    )
    provider = FakeProvider(
        kind=ResolutionAttemptKind.RETRIEVAL,
        result=ResolutionStepResult(
            source_reference="fixture:retrieval",
            claims=(candidate,),
        ),
    )
    graph = RequirementDependencyGraph((downstream, prerequisite))

    result = resolve_requirement_with_dependencies(
        flow=RequirementResolutionFlow(
            providers={ResolutionAttemptKind.RETRIEVAL: provider}
        ),
        graph=graph,
        node=downstream,
        parameter="mdf.thickness",
        prerequisite_assessments={
            "R1": _assessment(
                requirement_id="R1",
                parameter="base.width",
                state=RequirementState.KNOWN,
                evidence_ids=("EV-R1",),
            )
        },
        prerequisite_claims={"R1": (prerequisite_claim,)},
    )

    nested = result.resolution.retrieval_resolution
    assert nested is not None
    assert nested.retrieved_claim is not None
    visible = next(
        claim
        for claim in result.resolution.claims
        if claim.claim_id == nested.retrieved_claim.claim_id
    )

    assert nested.retrieved_claim == visible
    assert "R1" in visible.dependencies
    assert "R1-KNOWN" in visible.dependencies
    assert "EV-R1" in visible.provenance.evidence_ids
    assert "requirement-dependencies:v1" in visible.provenance.reasoning_method
