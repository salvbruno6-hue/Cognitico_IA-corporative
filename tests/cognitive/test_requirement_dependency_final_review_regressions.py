from __future__ import annotations

from dataclasses import dataclass

from elo.cognitive.reasoning.requirement_analysis import (
    ClaimProvenance,
    RequirementClaim,
    RequirementNode,
    RequirementSourceType,
    RequirementState,
    ResolutionAttemptKind,
    assess_parameter_gap,
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
    state: RequirementState,
    source_type: RequirementSourceType,
    evidence_ids: tuple[str, ...] = (),
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
            evidence_ids=evidence_ids,
            validation_status=validation_status,
        ),
    )


def _downstream_provider() -> CountingProvider:
    claim = _claim(
        claim_id="R2-RULE",
        requirement_id="R2",
        predicate="output.value",
        value="approved",
        state=RequirementState.KNOWN,
        source_type=RequirementSourceType.RULE,
        evidence_ids=("EV-R2-RULE",),
    )
    return CountingProvider(
        kind=ResolutionAttemptKind.RULE,
        result=ResolutionStepResult(
            source_reference="fixture:rule",
            claims=(claim,),
        ),
    )


def test_contradictory_automatic_prerequisite_claims_block_downstream_execution():
    known = _claim(
        claim_id="R1-KNOWN",
        requirement_id="R1",
        predicate="base.width",
        value="2.44 m",
        state=RequirementState.KNOWN,
        source_type=RequirementSourceType.RULE,
        evidence_ids=("EV-R1-KNOWN",),
    )
    calculated = _claim(
        claim_id="R1-CALCULATED",
        requirement_id="R1",
        predicate="base.width",
        value="2.50 m",
        state=RequirementState.CALCULATED,
        source_type=RequirementSourceType.CALCULATION,
        evidence_ids=("EV-R1-CALCULATED",),
    )
    prerequisite = RequirementNode(
        requirement_id="R1",
        text="base width",
        claims=(known, calculated),
    )
    downstream = RequirementNode(
        requirement_id="R2",
        text="dependent output",
        entity="MLT-C08",
        requirement_dependencies=("R1",),
    )
    assessment = assess_parameter_gap(
        requirement_id="R1",
        parameter="base.width",
        claims=prerequisite.claims,
    )
    provider = _downstream_provider()

    result = resolve_requirement_with_dependencies(
        flow=RequirementResolutionFlow(
            providers={ResolutionAttemptKind.RULE: provider}
        ),
        graph=RequirementDependencyGraph((prerequisite, downstream)),
        node=downstream,
        parameter="output.value",
        prerequisite_assessments={"R1": assessment},
    )

    assert assessment.state is RequirementState.KNOWN
    assert provider.calls == 0
    assert result.dependency_assessment.state is RequirementDependencyState.BLOCKED
    assert result.dependency_assessment.dependency_claim_ids == ()
    assert result.dependency_assessment.blockers[0].automatic_trust_failed is True
    assert result.resolution.assessment.state is RequirementState.BLOCKED
    assert result.resolution.assessment.state is not RequirementState.GAP_CONFIRMED


def test_evidence_free_documented_prerequisite_survives_unrelated_hypothesis_evidence():
    documented = _claim(
        claim_id="R1-DOC",
        requirement_id="R1",
        predicate="base.width",
        value="2.44 m",
        state=RequirementState.DOCUMENTED,
        source_type=RequirementSourceType.DOCUMENT,
        evidence_ids=(),
        validation_status="EXTRACTED",
    )
    hypothesis = _claim(
        claim_id="R1-HYP",
        requirement_id="R1",
        predicate="base.width",
        value="2.46 m",
        state=RequirementState.INFERRED,
        source_type=RequirementSourceType.LLM_INFERENCE,
        evidence_ids=("EV-R1-HYP",),
        validation_status="UNVERIFIED",
    )
    prerequisite = RequirementNode(
        requirement_id="R1",
        text="base width",
        claims=(documented, hypothesis),
    )
    downstream = RequirementNode(
        requirement_id="R2",
        text="dependent output",
        entity="MLT-C08",
        requirement_dependencies=("R1",),
    )
    assessment = assess_parameter_gap(
        requirement_id="R1",
        parameter="base.width",
        claims=prerequisite.claims,
    )
    provider = _downstream_provider()

    result = resolve_requirement_with_dependencies(
        flow=RequirementResolutionFlow(
            providers={ResolutionAttemptKind.RULE: provider}
        ),
        graph=RequirementDependencyGraph((prerequisite, downstream)),
        node=downstream,
        parameter="output.value",
        prerequisite_assessments={"R1": assessment},
    )

    assert assessment.state is RequirementState.DOCUMENTED
    assert assessment.evidence_ids == ("EV-R1-HYP",)
    assert provider.calls == 1
    assert result.dependency_assessment.state is RequirementDependencyState.READY
    assert result.dependency_assessment.dependency_claim_ids == ("R1-DOC",)
    assert result.dependency_assessment.evidence_ids == ()
    assert result.resolution.assessment.state is RequirementState.KNOWN


def test_dependency_context_binds_to_evidence_free_documented_downstream_result():
    prerequisite_claim = _claim(
        claim_id="R1-KNOWN",
        requirement_id="R1",
        predicate="base.width",
        value="2.44 m",
        state=RequirementState.KNOWN,
        source_type=RequirementSourceType.RULE,
        evidence_ids=("EV-R1",),
    )
    prerequisite = RequirementNode(
        requirement_id="R1",
        text="base width",
        claims=(prerequisite_claim,),
    )
    documented = _claim(
        claim_id="R2-DOC",
        requirement_id="R2",
        predicate="output.value",
        value="documented-value",
        state=RequirementState.DOCUMENTED,
        source_type=RequirementSourceType.DOCUMENT,
        evidence_ids=(),
        validation_status="EXTRACTED",
    )
    hypothesis = _claim(
        claim_id="R2-HYP",
        requirement_id="R2",
        predicate="output.value",
        value="hypothesis-value",
        state=RequirementState.INFERRED,
        source_type=RequirementSourceType.LLM_INFERENCE,
        evidence_ids=("EV-R2-HYP",),
        validation_status="UNVERIFIED",
    )
    downstream = RequirementNode(
        requirement_id="R2",
        text="dependent output",
        entity="MLT-C08",
        claims=(documented, hypothesis),
        requirement_dependencies=("R1",),
    )
    prerequisite_assessment = assess_parameter_gap(
        requirement_id="R1",
        parameter="base.width",
        claims=prerequisite.claims,
    )

    result = resolve_requirement_with_dependencies(
        flow=RequirementResolutionFlow(providers={}),
        graph=RequirementDependencyGraph((prerequisite, downstream)),
        node=downstream,
        parameter="output.value",
        prerequisite_assessments={"R1": prerequisite_assessment},
    )

    assert result.dependency_assessment.state is RequirementDependencyState.READY
    assert result.resolution.assessment.state is RequirementState.DOCUMENTED
    assert result.resolution.assessment.evidence_ids == ("EV-R2-HYP", "EV-R1")

    bound_documented = next(
        claim for claim in result.resolution.claims if claim.claim_id == "R2-DOC"
    )
    untouched_hypothesis = next(
        claim for claim in result.resolution.claims if claim.claim_id == "R2-HYP"
    )

    assert bound_documented.dependencies == ("R1", "R1-KNOWN")
    assert bound_documented.provenance.evidence_ids == ("EV-R1",)
    assert "requirement-dependencies:v1" in bound_documented.provenance.reasoning_method
    assert untouched_hypothesis.dependencies == ()
    assert untouched_hypothesis.provenance.evidence_ids == ("EV-R2-HYP",)
