import pytest

from elo.cognitive.reasoning.requirement_analysis import (
    ClaimProvenance,
    ConfidenceBand,
    RequirementClaim,
    RequirementNode,
    RequirementSourceType,
    RequirementState,
    ResolutionAttempt,
    ResolutionAttemptKind,
    ResolutionAttemptStatus,
    assess_parameter_gap,
    audit_requirement,
    confidence_for_claims,
)


def claim(
    *,
    claim_id: str,
    predicate: str,
    value: str,
    state: RequirementState,
    source_type: RequirementSourceType,
    source_reference: str,
    evidence_ids=("ev-1",),
    validation_status="UNVERIFIED",
    requires_human_validation=False,
):
    return RequirementClaim(
        claim_id=claim_id,
        requirement_id="SO-203.26:R1",
        subject="container-40-hc",
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


def unresolved_attempts():
    return tuple(
        ResolutionAttempt(kind, ResolutionAttemptStatus.NOT_FOUND, f"fixture:{kind.value.lower()}")
        for kind in (
            ResolutionAttemptKind.RETRIEVAL,
            ResolutionAttemptKind.RULE,
            ResolutionAttemptKind.CALCULATION,
            ResolutionAttemptKind.INFERENCE,
        )
    )


def test_documented_information_never_becomes_gap():
    documented = claim(
        claim_id="c-window-count",
        predicate="window.quantity",
        value="2",
        state=RequirementState.DOCUMENTED,
        source_type=RequirementSourceType.DOCUMENT,
        source_reference="SO-203.26:item-window",
        validation_status="VALIDATED",
    )

    result = assess_parameter_gap(
        requirement_id=documented.requirement_id,
        parameter="window.quantity",
        claims=(documented,),
        attempts=unresolved_attempts(),
    )

    assert result.state is RequirementState.DOCUMENTED
    assert result.human_validation_required is False
    assert result.confidence is ConfidenceBand.HIGH


def test_retrieved_elo_knowledge_resolves_false_gap_before_confirmation():
    retrieved = claim(
        claim_id="c-product-base",
        predicate="product.base",
        value="MLT.C08",
        state=RequirementState.RETRIEVED,
        source_type=RequirementSourceType.ELO,
        source_reference="elo:taxonomia:MLT.C08",
        evidence_ids=("taxonomia-row-1", "model-link-1"),
    )

    result = assess_parameter_gap(
        requirement_id=retrieved.requirement_id,
        parameter="product.base",
        claims=(retrieved,),
        attempts=(
            ResolutionAttempt(
                ResolutionAttemptKind.RETRIEVAL,
                ResolutionAttemptStatus.RESOLVED,
                "elo-memory",
                evidence_ids=("taxonomia-row-1",),
            ),
        ),
    )

    assert result.state is RequirementState.RETRIEVED
    assert result.state is not RequirementState.GAP_CONFIRMED
    assert result.confidence is ConfidenceBand.MEDIUM


def test_inference_is_not_silently_promoted_to_fact():
    inferred = claim(
        claim_id="c-reinforcement",
        predicate="window.reinforcement",
        value="possible structural reinforcement",
        state=RequirementState.INFERRED,
        source_type=RequirementSourceType.LLM_INFERENCE,
        source_reference="provider:test-model",
        requires_human_validation=True,
    )

    result = assess_parameter_gap(
        requirement_id=inferred.requirement_id,
        parameter="window.reinforcement",
        claims=(inferred,),
    )

    assert result.state is RequirementState.HUMAN_VALIDATION_REQUIRED
    assert result.human_validation_required is True
    assert "contractual fact" in result.reasons[0]


def test_conflict_requires_investigation_and_never_silent_resolution():
    a = claim(
        claim_id="c-thickness-a",
        predicate="mdf.thickness",
        value="15 mm",
        state=RequirementState.RETRIEVED,
        source_type=RequirementSourceType.EXPERIENCE,
        source_reference="experience:SO-155.26",
    )
    b = claim(
        claim_id="c-thickness-b",
        predicate="mdf.thickness",
        value="18 mm",
        state=RequirementState.CONFLICT,
        source_type=RequirementSourceType.ELO,
        source_reference="knowledge:mdf-standard",
        evidence_ids=("ev-2",),
    )

    result = assess_parameter_gap(
        requirement_id=a.requirement_id,
        parameter="mdf.thickness",
        claims=(a, b),
    )

    assert result.state is RequirementState.CONFLICT
    assert result.human_validation_required is True
    assert result.confidence is ConfidenceBand.LOW


def test_gap_is_candidate_until_governed_resolution_is_exhausted():
    candidate = assess_parameter_gap(
        requirement_id="SO-203.26:R1",
        parameter="mdf.thickness",
        claims=(),
        attempts=(
            ResolutionAttempt(
                ResolutionAttemptKind.RETRIEVAL,
                ResolutionAttemptStatus.NOT_FOUND,
                "elo-memory",
            ),
        ),
    )

    assert candidate.state is RequirementState.GAP_CANDIDATE
    assert candidate.human_validation_required is False


def test_gap_confirmed_only_after_retrieval_rule_calculation_and_inference_fail():
    result = assess_parameter_gap(
        requirement_id="SO-203.26:R1",
        parameter="mdf.thickness",
        claims=(),
        attempts=unresolved_attempts(),
    )

    assert result.state is RequirementState.GAP_CONFIRMED
    assert result.human_validation_required is True
    assert "retrieval, rule, calculation and controlled inference" in result.reasons[1]


def test_so_203_26_regression_not_in_document_is_not_equal_to_elo_gap():
    documented = claim(
        claim_id="c-container",
        predicate="container.type",
        value="40 HC",
        state=RequirementState.DOCUMENTED,
        source_type=RequirementSourceType.DOCUMENT,
        source_reference="SO-203.26:object",
    )
    retrieved = claim(
        claim_id="c-base-model",
        predicate="product.base",
        value="MLT.C08",
        state=RequirementState.RETRIEVED,
        source_type=RequirementSourceType.ELO,
        source_reference="elo:taxonomia",
        evidence_ids=("taxonomy-candidate",),
    )
    inferred = claim(
        claim_id="c-opening",
        predicate="window.opening_required",
        value="true",
        state=RequirementState.INFERRED,
        source_type=RequirementSourceType.RULE,
        source_reference="rule:window-requires-opening",
        evidence_ids=("rule-window-1",),
        requires_human_validation=False,
    )

    assert assess_parameter_gap(
        requirement_id=documented.requirement_id,
        parameter="container.type",
        claims=(documented, retrieved, inferred),
    ).state is RequirementState.DOCUMENTED

    assert assess_parameter_gap(
        requirement_id=documented.requirement_id,
        parameter="product.base",
        claims=(documented, retrieved, inferred),
    ).state is RequirementState.RETRIEVED

    opening = assess_parameter_gap(
        requirement_id=documented.requirement_id,
        parameter="window.opening_required",
        claims=(documented, retrieved, inferred),
    )
    assert opening.state is RequirementState.HUMAN_VALIDATION_REQUIRED
    assert opening.state is not RequirementState.GAP_CONFIRMED


def test_audit_trace_contains_sources_and_evidence_without_private_reasoning():
    documented = claim(
        claim_id="c-floor",
        predicate="floor.material",
        value="vinyl",
        state=RequirementState.DOCUMENTED,
        source_type=RequirementSourceType.DOCUMENT,
        source_reference="SO-203.26:floor",
    )
    node = RequirementNode(
        requirement_id=documented.requirement_id,
        text="Container 40 HC com piso vinílico",
        entity="container-40-hc",
        claims=(documented,),
        dependencies=("container-40-hc",),
    )

    trace = audit_requirement(node)

    assert trace["requirement_id"] == "SO-203.26:R1"
    assert trace["evidence_ids"] == ("ev-1",)
    assert trace["source_claims"][0]["source_type"] == "DOCUMENT"
    assert "reasoning" not in trace
    assert "chain_of_thought" not in trace


def test_claim_state_requires_compatible_provenance():
    with pytest.raises(ValueError, match="DOCUMENT provenance"):
        claim(
            claim_id="bad",
            predicate="door.type",
            value="metal",
            state=RequirementState.DOCUMENTED,
            source_type=RequirementSourceType.LLM_INFERENCE,
            source_reference="provider:test",
        )


def test_confidence_does_not_become_high_from_llm_inference_alone():
    inferred = claim(
        claim_id="c-llm",
        predicate="electrical.layout",
        value="hypothesis",
        state=RequirementState.INFERRED,
        source_type=RequirementSourceType.LLM_INFERENCE,
        source_reference="provider:test",
        validation_status="CONFIRMED",
    )

    assert confidence_for_claims((inferred,)) is ConfidenceBand.LOW
