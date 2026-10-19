from __future__ import annotations

from dataclasses import dataclass

import pytest

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
    SemanticRetrievalPolicy,
    audit_requirement_resolution,
)


@dataclass
class Provider:
    kind: ResolutionAttemptKind
    result: ResolutionStepResult

    def resolve(self, node, parameter, claims):
        return self.result


def _node(*, entity: str | None = "MLT-C08"):
    return RequirementNode(
        requirement_id="SO-203.26:R1",
        text="Definir espessura do MDF",
        entity=entity,
    )


def _rule_claim(*, subject: str = "MLT-C08"):
    return RequirementClaim(
        claim_id="RULE-MDF",
        requirement_id="SO-203.26:R1",
        subject=subject,
        predicate="mdf.thickness",
        value="15 mm",
        state=RequirementState.KNOWN,
        provenance=ClaimProvenance(
            source_type=RequirementSourceType.RULE,
            source_reference="rule:mdf:v1",
            reasoning_method="rule-evaluation:v1",
            evidence_ids=("EV-RULE",),
            validation_status="VALIDATED",
        ),
    )


def test_rule_claim_for_different_entity_is_rejected_without_applicability():
    provider = Provider(
        kind=ResolutionAttemptKind.RULE,
        result=ResolutionStepResult(
            source_reference="rule-engine:v1",
            claims=(_rule_claim(subject="PRODUCT-B"),),
        ),
    )

    with pytest.raises(ValueError, match="entity does not match target entity"):
        RequirementResolutionFlow(
            providers={ResolutionAttemptKind.RULE: provider}
        ).resolve(node=_node(), parameter="mdf.thickness")


def test_rule_claim_for_different_entity_requires_explicit_applicability_evidence():
    claim = _rule_claim(subject="PRODUCT-B")
    provider = Provider(
        kind=ResolutionAttemptKind.RULE,
        result=ResolutionStepResult(
            source_reference="rule-engine:v1",
            claims=(claim,),
        ),
    )

    result = RequirementResolutionFlow(
        providers={ResolutionAttemptKind.RULE: provider},
        structured_entity_applicability_evidence={
            claim.claim_id: ("EV-ENTITY-APPLIES",),
        },
    ).resolve(node=_node(), parameter="mdf.thickness")

    assert result.assessment.state is RequirementState.KNOWN
    assert "EV-ENTITY-APPLIES" in result.attempts[0].evidence_ids


def test_structured_claim_requires_entity_evidence_when_target_entity_is_absent():
    claim = _rule_claim()
    provider = Provider(
        kind=ResolutionAttemptKind.RULE,
        result=ResolutionStepResult(
            source_reference="rule-engine:v1",
            claims=(claim,),
        ),
    )

    with pytest.raises(ValueError, match="target entity is absent"):
        RequirementResolutionFlow(
            providers={ResolutionAttemptKind.RULE: provider}
        ).resolve(node=_node(entity=None), parameter="mdf.thickness")


def test_resolution_audit_includes_bounded_semantic_provenance_for_cross_context_reuse():
    candidate = RequirementClaim(
        claim_id="SO114-MDF",
        requirement_id="SO-114.26:R2",
        subject="MLT-C08",
        predicate="mdf.thickness",
        value="15 mm",
        state=RequirementState.DOCUMENTED,
        provenance=ClaimProvenance(
            source_type=RequirementSourceType.DOCUMENT,
            source_reference="kb:so114:material",
            reasoning_method="explicit-key-value-extraction:v1",
            evidence_ids=("EV-SOURCE",),
            validation_status="VALIDATED",
        ),
    )
    retrieval = Provider(
        kind=ResolutionAttemptKind.RETRIEVAL,
        result=ResolutionStepResult(
            source_reference="source-resolver:cross-context",
            claims=(candidate,),
        ),
    )
    result = RequirementResolutionFlow(
        providers={ResolutionAttemptKind.RETRIEVAL: retrieval},
        semantic_policy=SemanticRetrievalPolicy(
            applicability_evidence={
                candidate.claim_id: ("EV-APPLIES-SO203",),
            },
        ),
    ).resolve(node=_node(), parameter="mdf.thickness")

    audit = audit_requirement_resolution(result)
    semantic = audit["attempts"][0]["semantic"]
    match = semantic["matches"][0]

    assert semantic["state"] == "RESOLVED"
    assert match["candidate_requirement_id"] == "SO-114.26:R2"
    assert match["candidate_subject"] == "MLT-C08"
    assert match["recovered_value"] == "15 mm"
    assert match["kind"] == "EXACT"
    assert match["applicability_evidence_ids"] == ("EV-APPLIES-SO203",)
    assert match["source_reference"] == "kb:so114:material"
    assert "EV-SOURCE" in match["evidence_ids"]
