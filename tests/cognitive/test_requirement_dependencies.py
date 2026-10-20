from __future__ import annotations

from dataclasses import dataclass, field

import pytest

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
    RequirementDependencyState,
    audit_dependency_aware_resolution,
    audit_requirement_dependency_graph,
    blocked_gap_assessment,
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


def _assessment(
    *,
    requirement_id: str,
    parameter: str,
    state: RequirementState,
    evidence_ids: tuple[str, ...] = (),
    human_validation_required: bool = False,
) -> GapAssessment:
    return GapAssessment(
        requirement_id=requirement_id,
        parameter=parameter,
        state=state,
        reasons=("fixture",),
        evidence_ids=evidence_ids,
        human_validation_required=human_validation_required,
    )


@dataclass
class FakeProvider:
    kind: ResolutionAttemptKind
    result: ResolutionStepResult
    calls: list[tuple[str, str]] = field(default_factory=list)

    def resolve(self, node, parameter, claims):
        self.calls.append((node.requirement_id, parameter))
        return self.result


def _empty_provider(kind: ResolutionAttemptKind) -> FakeProvider:
    return FakeProvider(
        kind=kind,
        result=ResolutionStepResult(source_reference=f"fixture:{kind.value.lower()}"),
    )


def test_legacy_dependencies_remain_generic_lineage_and_do_not_trigger_gate():
    node = RequirementNode(
        requirement_id="R1",
        text="legacy lineage",
        entity="MLT-C08",
        dependencies=("container-40-hc",),
    )

    audit = audit_requirement(node)
    result = RequirementResolutionFlow(providers={}).resolve(
        node=node,
        parameter="unknown.parameter",
    )

    assert audit["dependencies"] == ("container-40-hc",)
    assert node.requirement_dependencies == ()
    assert result.assessment.state is RequirementState.GAP_CANDIDATE


def test_graph_rejects_duplicate_unknown_self_and_cycles_auditably():
    duplicate_a = RequirementNode(
        requirement_id="A",
        text="A1",
        requirement_dependencies=("B", "B", "UNKNOWN"),
    )
    duplicate_a_again = RequirementNode(requirement_id="A", text="A2")
    b = RequirementNode(
        requirement_id="B",
        text="B",
        requirement_dependencies=("B",),
    )

    invalid = RequirementDependencyGraph((duplicate_a, duplicate_a_again, b))
    audit = audit_requirement_dependency_graph(invalid)

    assert audit["valid"] is False
    assert audit["duplicate_requirement_ids"] == ("A",)
    assert audit["duplicate_dependencies"] == (("A", "B"),)
    assert audit["unknown_dependencies"] == (("A", "UNKNOWN"),)
    assert audit["self_dependencies"] == ("B",)
    with pytest.raises(ValueError, match="graph is invalid"):
        invalid.transitive_dependencies("A")

    cycle = RequirementDependencyGraph(
        (
            RequirementNode(
                requirement_id="A",
                text="A",
                requirement_dependencies=("B",),
            ),
            RequirementNode(
                requirement_id="B",
                text="B",
                requirement_dependencies=("A",),
            ),
        )
    )
    cycle_audit = audit_requirement_dependency_graph(cycle)
    assert cycle_audit["valid"] is False
    assert cycle_audit["cycles"] == (("A", "B", "A"),)


def test_typed_dependency_whitespace_is_normalized_once_for_all_graph_operations():
    r1 = RequirementNode(requirement_id="R1", text="base")
    r2 = RequirementNode(
        requirement_id="R2",
        text="dependent",
        requirement_dependencies=("  R1  ",),
    )
    graph = RequirementDependencyGraph((r2, r1))

    assert graph.validation.valid is True
    assert graph.validation.topological_order == ("R1", "R2")
    assert graph.transitive_dependencies("R2") == ("R1",)
    result = graph.assess(
        requirement_id="R2",
        assessments={
            "R1": _assessment(
                requirement_id="R1",
                parameter="base.width",
                state=RequirementState.KNOWN,
                evidence_ids=("EV-R1",),
            )
        },
    )
    assert result.direct_dependencies == ("R1",)
    assert result.transitive_dependencies == ("R1",)


def test_assessment_key_must_match_embedded_requirement_id():
    graph = RequirementDependencyGraph(
        (
            RequirementNode(requirement_id="R1", text="base"),
            RequirementNode(
                requirement_id="R2",
                text="dependent",
                requirement_dependencies=("R1",),
            ),
        )
    )

    with pytest.raises(ValueError, match="key does not match"):
        graph.assess(
            requirement_id="R2",
            assessments={
                "R1": _assessment(
                    requirement_id="OTHER",
                    parameter="base.width",
                    state=RequirementState.KNOWN,
                )
            },
        )


def test_current_prerequisite_claims_preserve_dynamic_supporting_claim_ids():
    r1 = RequirementNode(requirement_id="R1", text="base")
    r2 = RequirementNode(
        requirement_id="R2",
        text="dependent",
        requirement_dependencies=("R1",),
    )
    graph = RequirementDependencyGraph((r2, r1))
    dynamic = _claim(
        claim_id="R1-DYNAMIC",
        requirement_id="R1",
        predicate="base.width",
        value="2.44 m",
        state=RequirementState.KNOWN,
        source_type=RequirementSourceType.RULE,
        evidence_ids=("EV-DYNAMIC",),
    )

    result = graph.assess(
        requirement_id="R2",
        assessments={
            "R1": _assessment(
                requirement_id="R1",
                parameter="base.width",
                state=RequirementState.KNOWN,
                evidence_ids=("EV-DYNAMIC",),
            )
        },
        current_claims={"R1": (dynamic,)},
    )

    assert result.state is RequirementDependencyState.READY
    assert result.dependency_claim_ids == ("R1-DYNAMIC",)
    assert result.evidence_ids == ("EV-DYNAMIC",)


def test_current_prerequisite_claim_mapping_fails_closed_on_wrong_requirement():
    graph = RequirementDependencyGraph(
        (
            RequirementNode(requirement_id="R1", text="base"),
            RequirementNode(
                requirement_id="R2",
                text="dependent",
                requirement_dependencies=("R1",),
            ),
        )
    )
    forged = _claim(
        claim_id="OTHER-CLAIM",
        requirement_id="OTHER",
        predicate="base.width",
        value="2.44 m",
        state=RequirementState.KNOWN,
        source_type=RequirementSourceType.RULE,
        evidence_ids=("EV",),
    )

    with pytest.raises(ValueError, match="claim key does not match"):
        graph.assess(
            requirement_id="R2",
            assessments={
                "R1": _assessment(
                    requirement_id="R1",
                    parameter="base.width",
                    state=RequirementState.KNOWN,
                    evidence_ids=("EV",),
                )
            },
            current_claims={"R1": (forged,)},
        )


@pytest.mark.parametrize(
    ("state", "human_validation_required"),
    (
        (RequirementState.CONFLICT, True),
        (RequirementState.HUMAN_VALIDATION_REQUIRED, True),
        (RequirementState.ASSUMPTION_REQUIRED, True),
        (RequirementState.GAP_CANDIDATE, False),
    ),
)
def test_unresolved_prerequisite_blocks_without_becoming_downstream_gap(
    state,
    human_validation_required,
):
    prerequisite = RequirementNode(requirement_id="R1", text="prerequisite")
    dependent = RequirementNode(
        requirement_id="R2",
        text="dependent",
        requirement_dependencies=("R1",),
    )
    graph = RequirementDependencyGraph((dependent, prerequisite))
    dependency_assessment = graph.assess(
        requirement_id="R2",
        assessments={
            "R1": _assessment(
                requirement_id="R1",
                parameter="input.value",
                state=state,
                evidence_ids=("EV-BLOCKER",),
                human_validation_required=human_validation_required,
            )
        },
    )

    blocked = blocked_gap_assessment(
        dependency_assessment=dependency_assessment,
        parameter="output.value",
    )

    assert dependency_assessment.state is RequirementDependencyState.BLOCKED
    assert blocked.state is RequirementState.BLOCKED
    assert blocked.state is not RequirementState.GAP_CONFIRMED
    assert blocked.evidence_ids == ("EV-BLOCKER",)
    assert blocked.human_validation_required is human_validation_required


def test_unassessed_prerequisite_is_blocked_not_assumed_missing():
    graph = RequirementDependencyGraph(
        (
            RequirementNode(requirement_id="R1", text="prerequisite"),
            RequirementNode(
                requirement_id="R2",
                text="dependent",
                requirement_dependencies=("R1",),
            ),
        )
    )

    result = graph.assess(requirement_id="R2", assessments={})

    assert result.state is RequirementDependencyState.BLOCKED
    assert result.blockers[0].state is None
    assert result.evidence_ids == ()


def test_direct_resolution_rejects_typed_requirement_dependencies():
    node = RequirementNode(
        requirement_id="R2",
        text="dependent",
        entity="MLT-C08",
        requirement_dependencies=("R1",),
    )

    with pytest.raises(ValueError, match="governed dependency gate"):
        RequirementResolutionFlow(providers={}).resolve(
            node=node,
            parameter="output.value",
        )


def test_so203_unresolved_dependency_stops_all_attempts_and_false_gap():
    input_requirement = RequirementNode(
        requirement_id="SO-203.26:R4",
        text="Definir quantidade de painéis",
        entity="MLT-C08",
    )
    downstream = RequirementNode(
        requirement_id="SO-203.26:R5",
        text="Calcular consumo de MDF",
        entity="MLT-C08",
        requirement_dependencies=("SO-203.26:R4",),
    )
    graph = RequirementDependencyGraph((downstream, input_requirement))
    providers = {
        kind: _empty_provider(kind)
        for kind in (
            ResolutionAttemptKind.RETRIEVAL,
            ResolutionAttemptKind.RULE,
            ResolutionAttemptKind.CALCULATION,
            ResolutionAttemptKind.INFERENCE,
        )
    }

    result = resolve_requirement_with_dependencies(
        flow=RequirementResolutionFlow(providers=providers),
        graph=graph,
        node=downstream,
        parameter="mdf.consumption",
        prerequisite_assessments={
            "SO-203.26:R4": _assessment(
                requirement_id="SO-203.26:R4",
                parameter="panel.count",
                state=RequirementState.GAP_CANDIDATE,
            )
        },
    )

    assert result.resolution.assessment.state is RequirementState.BLOCKED
    assert result.resolution.executed_order == ()
    assert all(provider.calls == [] for provider in providers.values())
    assert result.resolution.assessment.state is not RequirementState.GAP_CONFIRMED


def test_ready_dependency_allows_resolution_and_binds_prerequisite_provenance():
    prerequisite = RequirementNode(
        requirement_id="SO-203.26:R4",
        text="Definir quantidade de painéis",
        entity="MLT-C08",
    )
    downstream = RequirementNode(
        requirement_id="SO-203.26:R5",
        text="Calcular consumo de MDF",
        entity="MLT-C08",
        dependencies=("legacy-container-lineage",),
        requirement_dependencies=("SO-203.26:R4",),
    )
    prerequisite_claim = _claim(
        claim_id="SO203-R4-PANELS",
        requirement_id="SO-203.26:R4",
        predicate="panel.count",
        value="4",
        state=RequirementState.KNOWN,
        source_type=RequirementSourceType.RULE,
        evidence_ids=("EV-SO203-PANELS",),
    )
    calculated = _claim(
        claim_id="SO203-R5-CALC",
        requirement_id="SO-203.26:R5",
        predicate="mdf.consumption",
        value="9.76 m2",
        state=RequirementState.CALCULATED,
        source_type=RequirementSourceType.CALCULATION,
        evidence_ids=("EV-SO203-FORMULA",),
    )
    calculation = FakeProvider(
        kind=ResolutionAttemptKind.CALCULATION,
        result=ResolutionStepResult(
            source_reference="calculator:so203:mdf",
            claims=(calculated,),
        ),
    )
    graph = RequirementDependencyGraph((downstream, prerequisite))

    result = resolve_requirement_with_dependencies(
        flow=RequirementResolutionFlow(
            providers={ResolutionAttemptKind.CALCULATION: calculation}
        ),
        graph=graph,
        node=downstream,
        parameter="mdf.consumption",
        prerequisite_assessments={
            "SO-203.26:R4": _assessment(
                requirement_id="SO-203.26:R4",
                parameter="panel.count",
                state=RequirementState.KNOWN,
                evidence_ids=("EV-SO203-PANELS",),
            )
        },
        prerequisite_claims={"SO-203.26:R4": (prerequisite_claim,)},
    )

    assert result.dependency_assessment.state is RequirementDependencyState.READY
    assert result.resolution.assessment.state is RequirementState.CALCULATED
    assert calculation.calls == [("SO-203.26:R5", "mdf.consumption")]
    resolved_claim = result.resolution.claims[-1]
    assert "SO-203.26:R4" in resolved_claim.dependencies
    assert "SO203-R4-PANELS" in resolved_claim.dependencies
    assert "EV-SO203-PANELS" in resolved_claim.provenance.evidence_ids
    assert "EV-SO203-FORMULA" in resolved_claim.provenance.evidence_ids
    assert "requirement-dependencies:v1" in resolved_claim.provenance.reasoning_method
    assert "EV-SO203-PANELS" in result.resolution.assessment.evidence_ids
    assert downstream.dependencies == ("legacy-container-lineage",)

    audit = audit_dependency_aware_resolution(result)
    assert audit["dependencies"]["state"] == "READY"
    assert audit["dependencies"]["dependency_claim_ids"] == ("SO203-R4-PANELS",)
    assert audit["resolution"]["final"]["state"] == "CALCULATED"
