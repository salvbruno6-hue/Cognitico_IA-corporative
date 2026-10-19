import pytest

from elo.cognitive.reasoning.requirement_analysis import (
    ClaimProvenance,
    RequirementClaim,
    RequirementNode,
    RequirementSourceType,
    RequirementState,
    ResolutionAttempt,
    ResolutionAttemptKind,
    ResolutionAttemptStatus,
    assess_parameter_gap,
)
from elo.cognitive.reasoning.semantic_matching import (
    SemanticMatchKind,
    SemanticResolutionState,
    audit_semantic_resolution,
    match_parameter_to_claim,
    normalize_semantic_identifier,
    normalize_semantic_text,
    normalize_semantic_value,
    resolve_requirement_parameter,
)


def node(requirement_id="SO-203.26:R5", entity="MLT.C08"):
    return RequirementNode(
        requirement_id=requirement_id,
        text="Requisito técnico pendente de resolução",
        entity=entity,
    )


def candidate(
    *,
    claim_id="knowledge-1",
    requirement_id="knowledge:MLT.C08",
    predicate="painel.mdf.espessura",
    value="15 mm",
    subject="MLT.C08",
    state=RequirementState.KNOWN,
    source_type=RequirementSourceType.ELO,
    source_reference="elo:taxonomia:MLT.C08",
    evidence_ids=("taxonomia-row-27",),
    validation_status="VALIDATED",
    requires_human_validation=False,
):
    return RequirementClaim(
        claim_id=claim_id,
        requirement_id=requirement_id,
        subject=subject,
        predicate=predicate,
        value=value,
        state=state,
        provenance=ClaimProvenance(
            source_type=source_type,
            source_reference=source_reference,
            reasoning_method="fixture",
            evidence_ids=tuple(evidence_ids),
            validation_status=validation_status,
        ),
        requires_human_validation=requires_human_validation,
    )


def applicability(*claims):
    return {
        claim.claim_id: (f"applicability:{claim.claim_id}",)
        for claim in claims
    }


def unresolved_attempts():
    return tuple(
        ResolutionAttempt(
            kind=kind,
            status=ResolutionAttemptStatus.NOT_FOUND,
            source_reference=f"fixture:{kind.value.casefold()}",
        )
        for kind in (
            ResolutionAttemptKind.RETRIEVAL,
            ResolutionAttemptKind.RULE,
            ResolutionAttemptKind.CALCULATION,
            ResolutionAttemptKind.INFERENCE,
        )
    )


def test_normalization_is_deterministic_accent_insensitive_and_unicode_safe():
    assert normalize_semantic_text("  Espessura-MDF / TÉCNICA  ") == "espessura mdf tecnica"
    assert normalize_semantic_text("espessura mdf técnica") == "espessura mdf tecnica"
    assert normalize_semantic_text("Μοντέλο Α") == "μοντελο α"


def test_identifier_normalization_preserves_technical_punctuation():
    assert normalize_semantic_identifier(" MLT.C08 ") == "mlt.c08"
    assert normalize_semantic_identifier("MLT/C08") != normalize_semantic_identifier("MLT-C08")


def test_value_normalization_preserves_technical_punctuation():
    assert normalize_semantic_value(" 15 MM ") == "15 mm"
    assert normalize_semantic_value("1.2 mm") != normalize_semantic_value("1/2 mm")


def test_exact_predicate_match_is_strong_without_rewriting_evidence():
    evidence = candidate(predicate="mdf.thickness", value="15 mm")

    match = match_parameter_to_claim(parameter="MDF.THICKNESS", candidate=evidence)

    assert match is not None
    assert match.kind is SemanticMatchKind.EXACT
    assert match.score == 1.0
    assert match.candidate.value == "15 mm"
    assert match.candidate.provenance.source_reference == "elo:taxonomia:MLT.C08"


def test_governed_alias_can_resolve_validated_evidence_as_retrieved_claim():
    evidence = candidate()

    result = resolve_requirement_parameter(
        node=node(),
        parameter="mdf.thickness",
        candidates=(evidence,),
        aliases={
            "mdf.thickness": (
                "painel.mdf.espessura",
                "espessura mdf",
            )
        },
        applicability_evidence=applicability(evidence),
    )

    assert result.state is SemanticResolutionState.RESOLVED
    assert result.human_validation_required is False
    assert result.matches[0].kind is SemanticMatchKind.GOVERNED_ALIAS
    assert result.matches[0].entity_compatible is True
    assert result.matches[0].entity_match_kind is SemanticMatchKind.EXACT
    assert result.matches[0].context_compatible is True
    assert result.retrieved_claim is not None
    assert result.retrieved_claim.requirement_id == "SO-203.26:R5"
    assert result.retrieved_claim.predicate == "mdf.thickness"
    assert result.retrieved_claim.value == "15 mm"
    assert result.retrieved_claim.state is RequirementState.RETRIEVED
    assert result.retrieved_claim.provenance.source_type is RequirementSourceType.ELO
    assert result.retrieved_claim.provenance.source_reference == "elo:taxonomia:MLT.C08"
    assert result.retrieved_claim.provenance.evidence_ids == (
        "taxonomia-row-27",
        "applicability:knowledge-1",
    )
    assert result.retrieved_claim.provenance.validation_status == "VALIDATED"
    assert "semantic-match:governed_alias:v1" == result.retrieved_claim.provenance.reasoning_method


def test_parameter_match_does_not_prove_applicability_to_another_entity():
    evidence = candidate(predicate="mdf.thickness", subject="MLT.M01")

    result = resolve_requirement_parameter(
        node=node(entity="MLT.C08"),
        parameter="mdf.thickness",
        candidates=(evidence,),
        applicability_evidence=applicability(evidence),
    )

    assert result.state is SemanticResolutionState.VALIDATION_REQUIRED
    assert result.human_validation_required is True
    assert result.matches[0].entity_compatible is False
    assert result.retrieved_claim is None
    assert "entity" in result.reasons[0]


def test_punctuation_distinct_entity_identifiers_do_not_match_exactly():
    evidence = candidate(predicate="mdf.thickness", subject="MLT/C08")

    result = resolve_requirement_parameter(
        node=node(entity="MLT-C08"),
        parameter="mdf.thickness",
        candidates=(evidence,),
        applicability_evidence=applicability(evidence),
    )

    assert result.state is SemanticResolutionState.VALIDATION_REQUIRED
    assert result.matches[0].entity_compatible is False
    assert result.retrieved_claim is None


def test_governed_entity_alias_can_establish_punctuation_variant_applicability():
    evidence = candidate(predicate="mdf.thickness", subject="MLT/C08")

    result = resolve_requirement_parameter(
        node=node(entity="MLT-C08"),
        parameter="mdf.thickness",
        candidates=(evidence,),
        entity_aliases={"MLT-C08": ("MLT/C08",)},
        applicability_evidence=applicability(evidence),
    )

    assert result.state is SemanticResolutionState.RESOLVED
    assert result.matches[0].entity_match_kind is SemanticMatchKind.GOVERNED_ALIAS
    assert result.retrieved_claim is not None


def test_cross_so_claim_remains_consultative_without_current_context_evidence():
    historical = candidate(
        claim_id="historical-so",
        requirement_id="SO-199.10:R3",
        predicate="mdf.thickness",
        value="15 mm",
    )

    result = resolve_requirement_parameter(
        node=node(requirement_id="SO-203.26:R5", entity="MLT.C08"),
        parameter="mdf.thickness",
        candidates=(historical,),
    )

    assert result.state is SemanticResolutionState.VALIDATION_REQUIRED
    assert result.human_validation_required is True
    assert result.matches[0].entity_compatible is True
    assert result.matches[0].context_compatible is False
    assert result.retrieved_claim is None
    assert "current requirement context" in result.reasons[0]


def test_cross_context_claim_can_resolve_with_explicit_applicability_evidence():
    historical = candidate(
        claim_id="historical-so",
        requirement_id="SO-199.10:R3",
        predicate="mdf.thickness",
        value="15 mm",
    )

    result = resolve_requirement_parameter(
        node=node(requirement_id="SO-203.26:R5", entity="MLT.C08"),
        parameter="mdf.thickness",
        candidates=(historical,),
        applicability_evidence={
            "historical-so": ("decision:SO-203.26:reuse-SO-199.10",),
        },
    )

    assert result.state is SemanticResolutionState.RESOLVED
    assert result.matches[0].context_compatible is True
    assert result.matches[0].applicability_evidence_ids == (
        "decision:SO-203.26:reuse-SO-199.10",
    )
    assert result.retrieved_claim is not None
    assert "decision:SO-203.26:reuse-SO-199.10" in result.retrieved_claim.provenance.evidence_ids


def test_same_so_requirement_context_does_not_need_cross_context_evidence():
    sibling = candidate(
        claim_id="same-so",
        requirement_id="SO-203.26:R2",
        predicate="mdf.thickness",
        value="15 mm",
    )

    result = resolve_requirement_parameter(
        node=node(requirement_id="SO-203.26:R5", entity="MLT.C08"),
        parameter="mdf.thickness",
        candidates=(sibling,),
    )

    assert result.state is SemanticResolutionState.RESOLVED
    assert result.matches[0].context_compatible is True
    assert result.matches[0].applicability_evidence_ids == ()


def test_strong_but_unvalidated_match_requires_validation_and_does_not_create_fact():
    evidence = candidate(validation_status="UNVERIFIED")

    result = resolve_requirement_parameter(
        node=node(),
        parameter="painel.mdf.espessura",
        candidates=(evidence,),
        applicability_evidence=applicability(evidence),
    )

    assert result.state is SemanticResolutionState.VALIDATION_REQUIRED
    assert result.human_validation_required is True
    assert result.retrieved_claim is None


def test_candidate_pending_human_validation_never_auto_resolves():
    evidence = candidate(
        predicate="mdf.thickness",
        requires_human_validation=True,
    )

    result = resolve_requirement_parameter(
        node=node(),
        parameter="mdf.thickness",
        candidates=(evidence,),
        applicability_evidence=applicability(evidence),
    )

    assert result.state is SemanticResolutionState.VALIDATION_REQUIRED
    assert result.human_validation_required is True
    assert result.retrieved_claim is None


def test_pending_human_validation_candidate_blocks_same_value_auto_resolution():
    governed = candidate(
        claim_id="governed",
        predicate="mdf.thickness",
    )
    pending = candidate(
        claim_id="pending",
        predicate="mdf.thickness",
        requires_human_validation=True,
        source_reference="elo:knowledge:pending",
        evidence_ids=("pending-evidence",),
    )

    result = resolve_requirement_parameter(
        node=node(),
        parameter="mdf.thickness",
        candidates=(governed, pending),
        applicability_evidence=applicability(governed, pending),
    )

    assert result.state is SemanticResolutionState.VALIDATION_REQUIRED
    assert result.human_validation_required is True
    assert result.retrieved_claim is None


def test_empty_candidate_value_never_resolves_a_parameter():
    evidence = candidate(predicate="mdf.thickness", value="   ")

    result = resolve_requirement_parameter(
        node=node(),
        parameter="mdf.thickness",
        candidates=(evidence,),
        applicability_evidence=applicability(evidence),
    )

    assert result.state is SemanticResolutionState.VALIDATION_REQUIRED
    assert result.retrieved_claim is None


def test_empty_value_does_not_masquerade_as_conflict_with_valid_evidence():
    valid = candidate(
        claim_id="valid",
        predicate="mdf.thickness",
        value="15 mm",
    )
    empty = candidate(
        claim_id="empty",
        predicate="mdf.thickness",
        value="   ",
        source_reference="elo:knowledge:empty",
        evidence_ids=("empty-evidence",),
    )

    result = resolve_requirement_parameter(
        node=node(),
        parameter="mdf.thickness",
        candidates=(valid, empty),
        applicability_evidence=applicability(valid, empty),
    )

    assert result.state is SemanticResolutionState.RESOLVED
    assert result.retrieved_claim is not None
    assert result.retrieved_claim.value == "15 mm"


def test_llm_inference_never_becomes_retrieved_fact_even_when_marked_confirmed():
    evidence = candidate(
        state=RequirementState.INFERRED,
        source_type=RequirementSourceType.LLM_INFERENCE,
        validation_status="CONFIRMED",
    )

    result = resolve_requirement_parameter(
        node=node(),
        parameter="painel.mdf.espessura",
        candidates=(evidence,),
        applicability_evidence=applicability(evidence),
    )

    assert result.state is SemanticResolutionState.VALIDATION_REQUIRED
    assert result.retrieved_claim is None


def test_token_overlap_is_diagnostic_only_and_never_auto_resolves():
    evidence = candidate(predicate="window.frame.material")

    result = resolve_requirement_parameter(
        node=node(),
        parameter="window.material",
        candidates=(evidence,),
    )

    assert result.state is SemanticResolutionState.CANDIDATE
    assert result.matches[0].kind is SemanticMatchKind.TOKEN_OVERLAP
    assert result.retrieved_claim is None


def test_conflicting_strong_applicable_matches_are_ambiguous_and_require_human_validation():
    first = candidate(claim_id="k-15", predicate="mdf.thickness", value="15 mm")
    second = candidate(
        claim_id="k-18",
        predicate="mdf.thickness",
        value="18 mm",
        source_reference="elo:knowledge:mdf-18",
        evidence_ids=("knowledge-row-18",),
    )

    result = resolve_requirement_parameter(
        node=node(),
        parameter="mdf.thickness",
        candidates=(first, second),
        applicability_evidence=applicability(first, second),
    )

    assert result.state is SemanticResolutionState.AMBIGUOUS
    assert result.human_validation_required is True
    assert result.retrieved_claim is None


def test_decimal_and_fraction_values_remain_conflicting():
    decimal = candidate(
        claim_id="decimal",
        predicate="mdf.thickness",
        value="1.2 mm",
    )
    fraction = candidate(
        claim_id="fraction",
        predicate="mdf.thickness",
        value="1/2 mm",
        source_reference="elo:knowledge:fraction",
        evidence_ids=("ev-fraction",),
    )

    result = resolve_requirement_parameter(
        node=node(),
        parameter="mdf.thickness",
        candidates=(decimal, fraction),
        applicability_evidence=applicability(decimal, fraction),
    )

    assert result.state is SemanticResolutionState.AMBIGUOUS
    assert result.retrieved_claim is None


def test_explicit_conflict_state_blocks_resolution_even_when_value_matches():
    governed = candidate(
        claim_id="governed",
        predicate="mdf.thickness",
        value="15 mm",
    )
    conflict = candidate(
        claim_id="conflict",
        predicate="mdf.thickness",
        value="15 mm",
        state=RequirementState.CONFLICT,
        source_reference="elo:knowledge:conflict",
        evidence_ids=("ev-conflict",),
    )

    result = resolve_requirement_parameter(
        node=node(),
        parameter="mdf.thickness",
        candidates=(governed, conflict),
        applicability_evidence=applicability(governed, conflict),
    )

    assert result.state is SemanticResolutionState.AMBIGUOUS
    assert result.human_validation_required is True
    assert result.retrieved_claim is None
    assert "conflict" in result.reasons[0]


def test_same_value_from_multiple_governed_sources_can_resolve_deterministically():
    first = candidate(claim_id="k-b", predicate="mdf.thickness", value="15 mm")
    second = candidate(
        claim_id="k-a",
        predicate="mdf.thickness",
        value="15 MM",
        source_reference="elo:knowledge:mdf-standard",
        evidence_ids=("knowledge-row-15",),
    )

    result = resolve_requirement_parameter(
        node=node(),
        parameter="mdf.thickness",
        candidates=(first, second),
        applicability_evidence=applicability(first, second),
    )

    assert result.state is SemanticResolutionState.RESOLVED
    assert result.retrieved_claim is not None
    assert result.retrieved_claim.value in {"15 mm", "15 MM"}
    assert len(result.matches) == 2


def test_alias_collision_fails_closed_instead_of_guessing_equivalence():
    evidence = candidate(predicate="painel.mdf.espessura")

    with pytest.raises(ValueError, match="alias collision"):
        match_parameter_to_claim(
            parameter="mdf.thickness",
            candidate=evidence,
            aliases={
                "mdf.thickness": ("espessura mdf",),
                "panel.thickness": ("espessura mdf",),
            },
        )


def test_so_203_26_semantic_equivalence_prevents_false_gap_confirmation():
    evidence = candidate(
        claim_id="so203-taxonomy",
        predicate="espessura mdf",
        value="15 mm",
        subject="MLT.C08",
        source_reference="elo:knowledge:mdf-standard",
        evidence_ids=("knowledge-mdf-standard",),
    )
    result = resolve_requirement_parameter(
        node=node("SO-203.26:R-MDF", entity="MLT.C08"),
        parameter="mdf.thickness",
        candidates=(evidence,),
        aliases={"mdf.thickness": ("espessura mdf",)},
        applicability_evidence={
            "so203-taxonomy": ("applicability:SO-203.26:MLT.C08",),
        },
    )

    assert result.retrieved_claim is not None
    assessment = assess_parameter_gap(
        requirement_id="SO-203.26:R-MDF",
        parameter="mdf.thickness",
        claims=(result.retrieved_claim,),
        attempts=unresolved_attempts(),
    )

    assert assessment.state is RequirementState.RETRIEVED
    assert assessment.state is not RequirementState.GAP_CONFIRMED


def test_audit_trace_exposes_original_context_recovered_value_and_applicability():
    evidence = candidate(predicate="mdf.thickness")
    result = resolve_requirement_parameter(
        node=node(),
        parameter="mdf.thickness",
        candidates=(evidence,),
        applicability_evidence={
            evidence.claim_id: ("applicability:SO-203.26:MLT.C08",),
        },
    )

    trace = audit_semantic_resolution(result)
    match = trace["matches"][0]

    assert trace["state"] == "RESOLVED"
    assert match["candidate_requirement_id"] == "knowledge:MLT.C08"
    assert match["candidate_subject"] == "MLT.C08"
    assert match["recovered_value"] == "15 mm"
    assert match["source_reference"] == "elo:taxonomia:MLT.C08"
    assert match["evidence_ids"] == ("taxonomia-row-27",)
    assert match["entity_compatible"] is True
    assert match["entity_match_kind"] == "EXACT"
    assert match["context_compatible"] is True
    assert match["applicability_evidence_ids"] == (
        "applicability:SO-203.26:MLT.C08",
    )
    assert match["candidate_requires_human_validation"] is False
    assert "reasoning" not in trace
    assert "chain_of_thought" not in trace
