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
    ResolutionAttemptStatus,
)
from elo.cognitive.reasoning.requirement_resolution import (
    RequirementResolutionFlow,
    ResolutionStepResult,
    SemanticRetrievalPolicy,
)
from elo.cognitive.reasoning.semantic_matching import SemanticResolutionState


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
        entity=None,
        claims=tuple(claims),
    )


def test_targetless_structured_claim_cannot_auto_resolve_even_with_applicability_evidence():
    claim = RequirementClaim(
        claim_id="RULE-MDF-TARGETLESS",
        requirement_id="SO-203.26:R1",
        subject="MLT-C08",
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
    provider = Provider(
        kind=ResolutionAttemptKind.RULE,
        result=ResolutionStepResult(
            source_reference="rule-engine:v1",
            claims=(claim,),
        ),
    )

    with pytest.raises(ValueError, match="requires an explicit target entity"):
        RequirementResolutionFlow(
            providers={ResolutionAttemptKind.RULE: provider},
            structured_entity_applicability_evidence={
                claim.claim_id: ("EV-ENTITY-APPLIES",),
            },
        ).resolve(node=_node(), parameter="mdf.thickness")


def test_targetless_semantic_retrieval_stays_pending_even_with_applicability_evidence():
    candidate = RequirementClaim(
        claim_id="DOC-MDF-TARGETLESS",
        requirement_id="SO-203.26:R1",
        subject="MLT-C08",
        predicate="mdf.thickness",
        value="15 mm",
        state=RequirementState.DOCUMENTED,
        provenance=ClaimProvenance(
            source_type=RequirementSourceType.DOCUMENT,
            source_reference="kb:so203:material",
            reasoning_method="explicit-key-value-extraction:v1",
            evidence_ids=("EV-DOC",),
            validation_status="VALIDATED",
        ),
    )
    provider = Provider(
        kind=ResolutionAttemptKind.RETRIEVAL,
        result=ResolutionStepResult(
            source_reference="source-resolver:so203",
            claims=(candidate,),
            evidence_ids=("EV-RETRIEVAL",),
        ),
    )

    result = RequirementResolutionFlow(
        providers={ResolutionAttemptKind.RETRIEVAL: provider},
        semantic_policy=SemanticRetrievalPolicy(
            entity_applicability_evidence={
                candidate.claim_id: ("EV-ENTITY-APPLIES",),
            },
        ),
    ).resolve(node=_node(), parameter="mdf.thickness")

    assert result.retrieval_resolution is not None
    assert result.retrieval_resolution.state is SemanticResolutionState.VALIDATION_REQUIRED
    assert result.retrieval_resolution.retrieved_claim is None
    assert result.attempts[0].kind is ResolutionAttemptKind.RETRIEVAL
    assert result.attempts[0].status is ResolutionAttemptStatus.NOT_APPLICABLE
    assert result.assessment.state is RequirementState.HUMAN_VALIDATION_REQUIRED
    assert result.assessment.human_validation_required is True
    assert "EV-DOC" in result.assessment.evidence_ids


def test_preloaded_automatic_claim_remains_fail_closed_without_entity():
    claim = RequirementClaim(
        claim_id="RULE-ORDINARY",
        requirement_id="SO-203.26:R1",
        subject="MLT-C08",
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

    with pytest.raises(ValueError, match="requires a target entity"):
        RequirementResolutionFlow(providers={}).resolve(
            node=_node(claims=(claim,)),
            parameter="mdf.thickness",
        )
