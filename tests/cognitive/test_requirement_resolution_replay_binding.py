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
        entity=None,
        claims=tuple(claims),
    )


def test_structured_binding_with_absent_entity_is_idempotent_on_replay():
    original = RequirementClaim(
        claim_id="RULE-MDF-REPLAY",
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
            claims=(original,),
        ),
    )

    first = RequirementResolutionFlow(
        providers={ResolutionAttemptKind.RULE: provider},
        structured_entity_applicability_evidence={
            original.claim_id: ("EV-ENTITY-APPLIES",),
        },
    ).resolve(node=_node(), parameter="mdf.thickness")

    bound = first.claims[-1]
    assert bound.claim_id.startswith("claim:structured-bind:")
    assert "structured-entity-applicability:v1" in bound.provenance.reasoning_method

    replay_node = _node(claims=first.claims)
    assert replay_node.entity == "MLT-C08"

    replay = RequirementResolutionFlow(providers={}).resolve(
        node=replay_node,
        parameter="mdf.thickness",
    )
    assert replay.assessment.state is RequirementState.KNOWN
    assert replay.attempts == ()


def test_semantic_binding_with_absent_entity_is_idempotent_on_replay():
    candidate = RequirementClaim(
        claim_id="DOC-MDF-REPLAY",
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
        ),
    )

    first = RequirementResolutionFlow(
        providers={ResolutionAttemptKind.RETRIEVAL: provider},
        semantic_policy=SemanticRetrievalPolicy(
            entity_applicability_evidence={
                candidate.claim_id: ("EV-ENTITY-APPLIES",),
            },
        ),
    ).resolve(node=_node(), parameter="mdf.thickness")

    bound = first.claims[-1]
    assert bound.claim_id.startswith("claim:semantic:")
    assert bound.state is RequirementState.RETRIEVED

    replay_node = _node(claims=first.claims)
    assert replay_node.entity == "MLT-C08"

    replay = RequirementResolutionFlow(providers={}).resolve(
        node=replay_node,
        parameter="mdf.thickness",
    )
    assert replay.assessment.state is RequirementState.RETRIEVED
    assert replay.attempts == ()


def test_ordinary_preloaded_claim_remains_fail_closed_without_entity():
    ordinary = RequirementClaim(
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
            evidence_ids=("EV-RULE", "EV-ENTITY-APPLIES"),
            validation_status="VALIDATED",
        ),
        dependencies=("UPSTREAM",),
    )
    node = _node(claims=(ordinary,))
    assert node.entity is None

    with pytest.raises(ValueError, match="requires a target entity"):
        RequirementResolutionFlow(providers={}).resolve(
            node=node,
            parameter="mdf.thickness",
        )
