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


def _node():
    return RequirementNode(
        requirement_id="SO-203.26:R1",
        text="Definir espessura do MDF",
        entity="MLT-C08",
    )


def _candidate(*, claim_id: str, predicate: str, validation_status: str = "VALIDATED"):
    return RequirementClaim(
        claim_id=claim_id,
        requirement_id="SO-203.26:R2",
        subject="MLT-C08",
        predicate=predicate,
        value="15 mm",
        state=RequirementState.DOCUMENTED,
        provenance=ClaimProvenance(
            source_type=RequirementSourceType.DOCUMENT,
            source_reference=f"kb:{claim_id}",
            reasoning_method="fixture",
            evidence_ids=(f"EV-{claim_id}",),
            validation_status=validation_status,
        ),
    )


def _empty(kind: ResolutionAttemptKind):
    return Provider(
        kind=kind,
        result=ResolutionStepResult(source_reference=f"fixture:{kind.value.lower()}"),
    )


def _all_after_retrieval():
    return {
        ResolutionAttemptKind.RULE: _empty(ResolutionAttemptKind.RULE),
        ResolutionAttemptKind.CALCULATION: _empty(ResolutionAttemptKind.CALCULATION),
        ResolutionAttemptKind.INFERENCE: _empty(ResolutionAttemptKind.INFERENCE),
    }


def test_strong_retrieval_pending_validation_blocks_gap_confirmation():
    candidate = _candidate(
        claim_id="PENDING",
        predicate="mdf.thickness",
        validation_status="UNVERIFIED",
    )
    retrieval = Provider(
        kind=ResolutionAttemptKind.RETRIEVAL,
        result=ResolutionStepResult(
            source_reference="source-resolver:pending",
            claims=(candidate,),
        ),
    )

    result = RequirementResolutionFlow(
        providers={ResolutionAttemptKind.RETRIEVAL: retrieval, **_all_after_retrieval()}
    ).resolve(node=_node(), parameter="mdf.thickness")

    assert result.executed_order == (
        ResolutionAttemptKind.RETRIEVAL,
        ResolutionAttemptKind.RULE,
        ResolutionAttemptKind.CALCULATION,
        ResolutionAttemptKind.INFERENCE,
    )
    assert result.assessment.state is RequirementState.HUMAN_VALIDATION_REQUIRED
    assert result.assessment.human_validation_required is True
    assert "EV-PENDING" in result.assessment.evidence_ids


def test_weak_semantic_candidate_keeps_gap_as_candidate_after_all_attempts():
    candidate = _candidate(
        claim_id="WEAK",
        predicate="mdf thickness nominal",
    )
    retrieval = Provider(
        kind=ResolutionAttemptKind.RETRIEVAL,
        result=ResolutionStepResult(
            source_reference="source-resolver:weak",
            claims=(candidate,),
        ),
    )

    result = RequirementResolutionFlow(
        providers={ResolutionAttemptKind.RETRIEVAL: retrieval, **_all_after_retrieval()}
    ).resolve(node=_node(), parameter="mdf thickness")

    assert result.assessment.state is RequirementState.GAP_CANDIDATE
    assert result.assessment.human_validation_required is True
    assert "EV-WEAK" in result.assessment.evidence_ids
