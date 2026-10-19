from __future__ import annotations

from dataclasses import dataclass

from elo.cognitive.reasoning.requirement_analysis import (
    ClaimProvenance,
    RequirementClaim,
    RequirementNode,
    RequirementSourceType,
    RequirementState,
    ResolutionAttemptKind,
)
from elo.cognitive.reasoning.requirement_resolution import (
    RequirementResolutionFlow,
    ResolutionStepResult,
)


@dataclass
class Provider:
    kind: ResolutionAttemptKind
    result: ResolutionStepResult

    def resolve(self, node, parameter, claims):
        return self.result


def _node(*, claims=()):
    return RequirementNode(
        requirement_id="SO-203.26:R1",
        text="Definir espessura do MDF",
        entity="MLT-C08",
        claims=tuple(claims),
    )


def test_cross_entity_rule_reuse_is_rebound_to_target_with_applicability_provenance():
    original = RequirementClaim(
        claim_id="RULE-PRODUCT-B",
        requirement_id="SO-203.26:R1",
        subject="PRODUCT-B",
        predicate="mdf.thickness",
        value="15 mm",
        state=RequirementState.KNOWN,
        provenance=ClaimProvenance(
            source_type=RequirementSourceType.RULE,
            source_reference="rule:mdf:v1",
            reasoning_method="rule-evaluation:v1",
            evidence_ids=("EV-RULE-SOURCE",),
            validation_status="VALIDATED",
        ),
    )
    provider = Provider(
        kind=ResolutionAttemptKind.RULE,
        result=ResolutionStepResult(
            source_reference="rule-engine:v1",
            claims=(original,),
        ),
    )

    result = RequirementResolutionFlow(
        providers={ResolutionAttemptKind.RULE: provider},
        structured_entity_applicability_evidence={
            original.claim_id: ("EV-ENTITY-APPLIES",),
        },
    ).resolve(node=_node(), parameter="mdf.thickness")

    assert result.assessment.state is RequirementState.KNOWN
    rebound = result.claims[-1]
    assert rebound.claim_id != original.claim_id
    assert rebound.requirement_id == "SO-203.26:R1"
    assert rebound.subject == "MLT-C08"
    assert rebound.value == "15 mm"
    assert rebound.provenance.source_reference == "rule:mdf:v1"
    assert rebound.provenance.source_type is RequirementSourceType.RULE
    assert rebound.provenance.evidence_ids == (
        "EV-RULE-SOURCE",
        "EV-ENTITY-APPLIES",
    )
    assert original.claim_id in rebound.dependencies
    assert "EV-ENTITY-APPLIES" in result.attempts[0].evidence_ids

    reused = RequirementResolutionFlow(providers={}).resolve(
        node=_node(claims=result.claims),
        parameter="mdf.thickness",
    )
    assert reused.assessment.state is RequirementState.KNOWN
    assert reused.attempts == ()


def test_pending_retrieval_is_preserved_beside_later_inference():
    retrieved = RequirementClaim(
        claim_id="PENDING-RETRIEVAL",
        requirement_id="SO-203.26:R2",
        subject="MLT-C08",
        predicate="mdf.thickness",
        value="15 mm",
        state=RequirementState.DOCUMENTED,
        provenance=ClaimProvenance(
            source_type=RequirementSourceType.DOCUMENT,
            source_reference="kb:so203:material",
            reasoning_method="explicit-key-value-extraction:v1",
            evidence_ids=("EV-RETRIEVED-PENDING",),
            validation_status="UNVERIFIED",
        ),
    )
    inferred = RequirementClaim(
        claim_id="INFERRED-MDF",
        requirement_id="SO-203.26:R1",
        subject="MLT-C08",
        predicate="mdf.thickness",
        value="18 mm",
        state=RequirementState.INFERRED,
        provenance=ClaimProvenance(
            source_type=RequirementSourceType.LLM_INFERENCE,
            source_reference="inference:controlled:v1",
            reasoning_method="controlled-inference:v1",
            evidence_ids=("EV-INFERENCE-CONTEXT",),
            validation_status="UNVERIFIED",
        ),
        requires_human_validation=True,
    )
    retrieval_provider = Provider(
        kind=ResolutionAttemptKind.RETRIEVAL,
        result=ResolutionStepResult(
            source_reference="source-resolver:so203",
            claims=(retrieved,),
        ),
    )
    inference_provider = Provider(
        kind=ResolutionAttemptKind.INFERENCE,
        result=ResolutionStepResult(
            source_reference="inference:controlled:v1",
            claims=(inferred,),
        ),
    )

    result = RequirementResolutionFlow(
        providers={
            ResolutionAttemptKind.RETRIEVAL: retrieval_provider,
            ResolutionAttemptKind.INFERENCE: inference_provider,
        }
    ).resolve(node=_node(), parameter="mdf.thickness")

    assert result.assessment.state is RequirementState.HUMAN_VALIDATION_REQUIRED
    assert result.assessment.human_validation_required is True
    assert "EV-RETRIEVED-PENDING" in result.assessment.evidence_ids
    assert "EV-INFERENCE-CONTEXT" in result.assessment.evidence_ids
    assert any("retrieval" in reason for reason in result.assessment.reasons)
    assert result.executed_order == (
        ResolutionAttemptKind.RETRIEVAL,
        ResolutionAttemptKind.INFERENCE,
    )
