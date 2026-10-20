from elo.cognitive.reasoning.requirement_analysis import (
    ClaimProvenance,
    RequirementClaim,
    RequirementNode,
    RequirementSourceType,
    RequirementState,
)
from elo.cognitive.reasoning.semantic_matching import (
    SemanticResolutionState,
    audit_semantic_resolution,
    resolve_requirement_parameter,
)


def _candidate() -> RequirementClaim:
    return RequirementClaim(
        claim_id="same-so-product-a",
        requirement_id="SO-203.26:R2",
        subject="PRODUCT-A",
        predicate="mdf.thickness",
        value="15 mm",
        state=RequirementState.KNOWN,
        provenance=ClaimProvenance(
            source_type=RequirementSourceType.ELO,
            source_reference="elo:knowledge:product-a",
            reasoning_method="fixture",
            evidence_ids=("knowledge-product-a",),
            validation_status="VALIDATED",
        ),
    )


def test_missing_target_entity_fails_closed_without_entity_applicability_evidence():
    evidence = _candidate()
    target = RequirementNode(
        requirement_id="SO-203.26:R5",
        text="Requisito sem entidade explicitada",
        entity=None,
    )

    result = resolve_requirement_parameter(
        node=target,
        parameter="mdf.thickness",
        candidates=(evidence,),
    )

    assert result.state is SemanticResolutionState.VALIDATION_REQUIRED
    assert result.human_validation_required is True
    assert result.matches[0].entity_compatible is False
    assert result.matches[0].entity_applicability_evidence_ids == ()
    assert result.retrieved_claim is None


def test_blank_target_entity_also_fails_closed_without_entity_applicability_evidence():
    evidence = _candidate()
    target = RequirementNode(
        requirement_id="SO-203.26:R5",
        text="Requisito com entidade em branco",
        entity="   ",
    )

    result = resolve_requirement_parameter(
        node=target,
        parameter="mdf.thickness",
        candidates=(evidence,),
    )

    assert result.state is SemanticResolutionState.VALIDATION_REQUIRED
    assert result.matches[0].entity_compatible is False
    assert result.retrieved_claim is None


def test_missing_target_entity_can_resolve_only_with_explicit_entity_applicability_evidence():
    evidence = _candidate()
    target = RequirementNode(
        requirement_id="SO-203.26:R5",
        text="Requisito sem entidade explicitada",
        entity=None,
    )

    result = resolve_requirement_parameter(
        node=target,
        parameter="mdf.thickness",
        candidates=(evidence,),
        entity_applicability_evidence={
            evidence.claim_id: ("decision:SO-203.26:R5:PRODUCT-A-applicable",),
        },
    )

    assert result.state is SemanticResolutionState.RESOLVED
    assert result.human_validation_required is False
    assert result.matches[0].entity_compatible is True
    assert result.matches[0].entity_match_kind is None
    assert result.matches[0].entity_applicability_evidence_ids == (
        "decision:SO-203.26:R5:PRODUCT-A-applicable",
    )
    assert result.retrieved_claim is not None
    assert result.retrieved_claim.subject == "PRODUCT-A"
    assert "decision:SO-203.26:R5:PRODUCT-A-applicable" in (
        result.retrieved_claim.provenance.evidence_ids
    )

    trace = audit_semantic_resolution(result)
    assert trace["matches"][0]["entity_applicability_evidence_ids"] == (
        "decision:SO-203.26:R5:PRODUCT-A-applicable",
    )


def test_explicit_cross_entity_target_resolves_only_with_governed_applicability_evidence():
    evidence = _candidate()
    target = RequirementNode(
        requirement_id="SO-203.26:R5",
        text="Requisito para PRODUCT-B",
        entity="PRODUCT-B",
    )

    blocked = resolve_requirement_parameter(
        node=target,
        parameter="mdf.thickness",
        candidates=(evidence,),
    )
    assert blocked.state is SemanticResolutionState.VALIDATION_REQUIRED
    assert blocked.matches[0].entity_compatible is False
    assert blocked.retrieved_claim is None

    resolved = resolve_requirement_parameter(
        node=target,
        parameter="mdf.thickness",
        candidates=(evidence,),
        entity_applicability_evidence={
            evidence.claim_id: ("decision:PRODUCT-A-applies-to-PRODUCT-B",),
        },
    )

    assert resolved.state is SemanticResolutionState.RESOLVED
    assert resolved.matches[0].entity_compatible is True
    assert resolved.matches[0].entity_match_kind is None
    assert resolved.matches[0].entity_applicability_evidence_ids == (
        "decision:PRODUCT-A-applies-to-PRODUCT-B",
    )
    assert resolved.retrieved_claim is not None
    assert resolved.retrieved_claim.subject == "PRODUCT-B"
    assert "decision:PRODUCT-A-applies-to-PRODUCT-B" in (
        resolved.retrieved_claim.provenance.evidence_ids
    )
