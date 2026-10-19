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
    normalize_semantic_text,
    resolve_requirement_parameter,
)


def node(requirement_id="SO-203.26:R5"):
    return RequirementNode(
        requirement_id=requirement_id,
        text="Requisito técnico pendente de resolução",
        entity="container-40-hc",
    )


def candidate(
    *,
    claim_id="knowledge-1",
    predicate="painel.mdf.espessura",
    value="15 mm",
    state=RequirementState.KNOWN,
    source_type=RequirementSourceType.ELO,
    source_reference="elo:taxonomia:MLT.C08",
    evidence_ids=("taxonomia-row-27",),
    validation_status="VALIDATED",
):
    return RequirementClaim(
        claim_id=claim_id,
        requirement_id="knowledge:MLT.C08",
        subject="MLT.C08",
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
    )


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


def test_normalization_is_deterministic_and_accent_insensitive():
    assert normalize_semantic_text("  Espessura-MDF / TÉCNICA  ") == "espessura mdf tecnica"
    assert normalize_semantic_text("espessura mdf técnica") == "espessura mdf tecnica"


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
    )

    assert result.state is SemanticResolutionState.RESOLVED
    assert result.human_validation_required is False
    assert result.matches[0].kind is SemanticMatchKind.GOVERNED_ALIAS
    assert result.retrieved_claim is not None
    assert result.retrieved_claim.requirement_id == "SO-203.26:R5"
    assert result.retrieved_claim.predicate == "mdf.thickness"
    assert result.retrieved_claim.value == "15 mm"
    assert result.retrieved_claim.state is RequirementState.RETRIEVED
    assert result.retrieved_claim.provenance.source_type is RequirementSourceType.ELO
    assert result.retrieved_claim.provenance.source_reference == "elo:taxonomia:MLT.C08"
    assert result.retrieved_claim.provenance.evidence_ids == ("taxonomia-row-27",)
    assert result.retrieved_claim.provenance.validation_status == "VALIDATED"
    assert "semantic-match:governed_alias:v1" == result.retrieved_claim.provenance.reasoning_method


def test_strong_but_unvalidated_match_requires_validation_and_does_not_create_fact():
    evidence = candidate(validation_status="UNVERIFIED")

    result = resolve_requirement_parameter(
        node=node(),
        parameter="painel.mdf.espessura",
        candidates=(evidence,),
    )

    assert result.state is SemanticResolutionState.VALIDATION_REQUIRED
    assert result.human_validation_required is True
    assert result.retrieved_claim is None


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


def test_conflicting_strong_matches_are_ambiguous_and_require_human_validation():
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
    )

    assert result.state is SemanticResolutionState.AMBIGUOUS
    assert result.human_validation_required is True
    assert result.retrieved_claim is None


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
        source_reference="elo:knowledge:mdf-standard",
        evidence_ids=("knowledge-mdf-standard",),
    )
    result = resolve_requirement_parameter(
        node=node("SO-203.26:R-MDF"),
        parameter="mdf.thickness",
        candidates=(evidence,),
        aliases={"mdf.thickness": ("espessura mdf",)},
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


def test_audit_trace_exposes_match_evidence_without_private_reasoning():
    result = resolve_requirement_parameter(
        node=node(),
        parameter="mdf.thickness",
        candidates=(candidate(predicate="mdf.thickness"),),
    )

    trace = audit_semantic_resolution(result)

    assert trace["state"] == "RESOLVED"
    assert trace["matches"][0]["source_reference"] == "elo:taxonomia:MLT.C08"
    assert trace["matches"][0]["evidence_ids"] == ("taxonomia-row-27",)
    assert "reasoning" not in trace
    assert "chain_of_thought" not in trace
