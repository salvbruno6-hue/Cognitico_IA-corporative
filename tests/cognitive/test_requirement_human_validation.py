from __future__ import annotations

import pytest

from elo.cognitive.reasoning.requirement_analysis import (
    ClaimProvenance,
    ConfidenceBand,
    GapAssessment,
    RequirementClaim,
    RequirementNode,
    RequirementSourceType,
    RequirementState,
)
from elo.cognitive.reasoning.requirement_human_validation import (
    HumanValidationAction,
    HumanValidationDecision,
    HumanValidationStatus,
    apply_human_validation,
    audit_human_validation,
)
from elo.cognitive.reasoning.requirement_resolution import (
    RequirementResolutionFlow,
    RequirementResolutionResult,
)
from elo.cognitive.reasoning.semantic_matching import (
    SemanticMatch,
    SemanticMatchKind,
    SemanticResolution,
    SemanticResolutionState,
)


PARAMETER = "installation.allowance"


def _node(*, requirement_id: str = "REQ-01", entity: str | None = "MLT-C08"):
    return RequirementNode(
        requirement_id=requirement_id,
        text="Determine installation allowance",
        entity=entity,
    )


def _inference_claim(*, claim_id: str = "INF-01", value: str = "12%"):
    return RequirementClaim(
        claim_id=claim_id,
        requirement_id="REQ-01",
        subject="MLT-C08",
        predicate=PARAMETER,
        value=value,
        state=RequirementState.INFERRED,
        provenance=ClaimProvenance(
            source_type=RequirementSourceType.LLM_INFERENCE,
            source_reference="intelligence-router:openai:test:req-1",
            reasoning_method="controlled-llm-inference:v1",
            evidence_ids=("EV-INF",),
            validation_status="UNVERIFIED",
        ),
        requires_human_validation=True,
    )


def _pending_resolution(*, claims=(), retrieval_resolution=None, state=RequirementState.HUMAN_VALIDATION_REQUIRED):
    return RequirementResolutionResult(
        requirement_id="REQ-01",
        parameter=PARAMETER,
        claims=tuple(claims),
        attempts=(),
        assessment=GapAssessment(
            requirement_id="REQ-01",
            parameter=PARAMETER,
            state=state,
            reasons=("human decision required",),
            evidence_ids=tuple(
                dict.fromkeys(
                    evidence
                    for claim in claims
                    for evidence in claim.provenance.evidence_ids
                )
            ),
            confidence=ConfidenceBand.LOW,
            human_validation_required=True,
        ),
        retrieval_resolution=retrieval_resolution,
    )


def _decision(
    action: HumanValidationAction,
    *,
    target_claim_id: str | None = None,
    value: str | None = None,
    decision_id: str = "DEC-001",
    requirement_id: str = "REQ-01",
    parameter: str = PARAMETER,
):
    return HumanValidationDecision(
        decision_id=decision_id,
        reviewer_id="reviewer-01",
        requirement_id=requirement_id,
        parameter=parameter,
        action=action,
        target_claim_id=target_claim_id,
        value=value,
        evidence_ids=("EV-HUMAN-REVIEW",),
    )


def test_approve_inference_creates_new_human_known_claim_without_mutating_source():
    source = _inference_claim()
    original = source
    resolution = _pending_resolution(claims=(source,))

    result = apply_human_validation(
        node=_node(),
        resolution=resolution,
        decision=_decision(HumanValidationAction.APPROVE, target_claim_id="INF-01"),
    )

    assert source == original
    assert source.state is RequirementState.INFERRED
    assert source.requires_human_validation is True
    assert result.status is HumanValidationStatus.APPROVED
    assert result.source_claim_id == "INF-01"
    assert result.can_execute is False

    claim = result.validated_claim
    assert claim is not None
    assert claim is not source
    assert claim.requirement_id == "REQ-01"
    assert claim.subject == "MLT-C08"
    assert claim.predicate == PARAMETER
    assert claim.value == "12%"
    assert claim.state is RequirementState.KNOWN
    assert claim.provenance.source_type is RequirementSourceType.HUMAN
    assert claim.provenance.validation_status == "APPROVED"
    assert claim.requires_human_validation is False
    assert "INF-01" in claim.dependencies
    assert "EV-INF" in claim.provenance.evidence_ids
    assert "EV-HUMAN-REVIEW" in claim.provenance.evidence_ids
    assert any(
        evidence.startswith("evidence:human-validation:")
        for evidence in claim.provenance.evidence_ids
    )


def test_approved_human_claim_short_circuits_only_through_existing_canonical_trust_checks():
    source = _inference_claim()
    validation = apply_human_validation(
        node=_node(),
        resolution=_pending_resolution(claims=(source,)),
        decision=_decision(HumanValidationAction.APPROVE, target_claim_id="INF-01"),
    )
    claim = validation.validated_claim
    assert claim is not None

    replay_node = RequirementNode(
        requirement_id="REQ-01",
        text="Determine installation allowance",
        entity="MLT-C08",
        claims=(claim,),
    )
    resolved = RequirementResolutionFlow(providers={}).resolve(
        node=replay_node,
        parameter=PARAMETER,
    )

    assert resolved.attempts == ()
    assert resolved.assessment.state is RequirementState.KNOWN
    assert resolved.assessment.human_validation_required is False
    assert resolved.assessment.confidence is ConfidenceBand.HIGH


def test_human_validation_replay_is_deterministic():
    source = _inference_claim()
    resolution = _pending_resolution(claims=(source,))
    decision = _decision(HumanValidationAction.APPROVE, target_claim_id="INF-01")

    first = apply_human_validation(node=_node(), resolution=resolution, decision=decision)
    second = apply_human_validation(node=_node(), resolution=resolution, decision=decision)

    assert first == second
    assert first.validated_claim is not None
    assert second.validated_claim is not None
    assert first.validated_claim.claim_id == second.validated_claim.claim_id
    assert first.evidence_ids == second.evidence_ids


def test_revise_confirmed_gap_can_create_explicit_human_fact_without_candidate():
    resolution = _pending_resolution(claims=(), state=RequirementState.GAP_CONFIRMED)

    result = apply_human_validation(
        node=_node(),
        resolution=resolution,
        decision=_decision(HumanValidationAction.REVISE, value="15%"),
    )

    assert result.status is HumanValidationStatus.APPROVED
    assert result.source_claim_id is None
    assert result.validated_claim is not None
    assert result.validated_claim.value == "15%"
    assert result.validated_claim.state is RequirementState.KNOWN
    assert result.validated_claim.provenance.source_type is RequirementSourceType.HUMAN
    assert result.validated_claim.dependencies == ()


def test_reject_creates_no_fact_and_preserves_source_hypothesis():
    source = _inference_claim()
    resolution = _pending_resolution(claims=(source,))

    result = apply_human_validation(
        node=_node(),
        resolution=resolution,
        decision=_decision(HumanValidationAction.REJECT, target_claim_id="INF-01"),
    )

    assert result.status is HumanValidationStatus.REJECTED
    assert result.validated_claim is None
    assert result.source_claim_id == "INF-01"
    assert source.state is RequirementState.INFERRED
    assert source.requires_human_validation is True


def test_requirement_or_parameter_mismatch_fails_closed():
    source = _inference_claim()
    resolution = _pending_resolution(claims=(source,))

    with pytest.raises(ValueError, match="requirement_id mismatch"):
        apply_human_validation(
            node=_node(),
            resolution=resolution,
            decision=_decision(
                HumanValidationAction.APPROVE,
                target_claim_id="INF-01",
                requirement_id="OTHER",
            ),
        )

    with pytest.raises(ValueError, match="parameter mismatch"):
        apply_human_validation(
            node=_node(),
            resolution=resolution,
            decision=_decision(
                HumanValidationAction.APPROVE,
                target_claim_id="INF-01",
                parameter="other.parameter",
            ),
        )


def test_duplicate_candidate_claim_identity_is_ambiguous_and_fails_closed():
    first = _inference_claim(claim_id="DUP", value="12%")
    second = RequirementClaim(
        claim_id="DUP",
        requirement_id="REQ-01",
        subject="MLT-C08",
        predicate=PARAMETER,
        value="14%",
        state=RequirementState.ASSUMPTION_REQUIRED,
        provenance=ClaimProvenance(
            source_type=RequirementSourceType.LLM_INFERENCE,
            source_reference="intelligence-router:openai:test:req-2",
            reasoning_method="controlled-llm-inference:v1",
            evidence_ids=("EV-INF-2",),
            validation_status="UNVERIFIED",
        ),
        requires_human_validation=True,
    )

    with pytest.raises(ValueError, match="identity is ambiguous"):
        apply_human_validation(
            node=_node(),
            resolution=_pending_resolution(claims=(first, second)),
            decision=_decision(HumanValidationAction.APPROVE, target_claim_id="DUP"),
        )


def test_retrieval_applicability_candidate_can_be_human_approved_and_rebound_to_exact_target():
    candidate = RequirementClaim(
        claim_id="RET-CANDIDATE",
        requirement_id="OTHER:R1",
        subject="OTHER-ENTITY",
        predicate=PARAMETER,
        value="18%",
        state=RequirementState.KNOWN,
        provenance=ClaimProvenance(
            source_type=RequirementSourceType.ELO,
            source_reference="knowledge:item:42",
            reasoning_method="retrieval",
            evidence_ids=("EV-RETRIEVAL",),
            validation_status="VALIDATED",
        ),
    )
    match = SemanticMatch(
        candidate=candidate,
        kind=SemanticMatchKind.EXACT,
        score=1.0,
        matched_terms=(PARAMETER,),
        entity_compatible=False,
        context_compatible=False,
    )
    semantic = SemanticResolution(
        requirement_id="REQ-01",
        parameter=PARAMETER,
        state=SemanticResolutionState.VALIDATION_REQUIRED,
        matches=(match,),
        reasons=("applicability requires human validation",),
        human_validation_required=True,
    )
    resolution = _pending_resolution(
        claims=(),
        retrieval_resolution=semantic,
    )

    result = apply_human_validation(
        node=_node(),
        resolution=resolution,
        decision=_decision(
            HumanValidationAction.APPROVE,
            target_claim_id="RET-CANDIDATE",
        ),
    )

    claim = result.validated_claim
    assert claim is not None
    assert claim.subject == "MLT-C08"
    assert claim.requirement_id == "REQ-01"
    assert claim.value == "18%"
    assert claim.provenance.source_type is RequirementSourceType.HUMAN
    assert "RET-CANDIDATE" in claim.dependencies
    assert "EV-RETRIEVAL" in claim.provenance.evidence_ids


def test_already_resolved_automatic_result_cannot_be_overwritten_by_human_gate():
    automatic = RequirementClaim(
        claim_id="KNOWN-01",
        requirement_id="REQ-01",
        subject="MLT-C08",
        predicate=PARAMETER,
        value="10%",
        state=RequirementState.KNOWN,
        provenance=ClaimProvenance(
            source_type=RequirementSourceType.RULE,
            source_reference="rule:known",
            reasoning_method="rule",
            evidence_ids=("EV-KNOWN",),
            validation_status="VALIDATED",
        ),
    )
    resolution = RequirementResolutionResult(
        requirement_id="REQ-01",
        parameter=PARAMETER,
        claims=(automatic,),
        attempts=(),
        assessment=GapAssessment(
            requirement_id="REQ-01",
            parameter=PARAMETER,
            state=RequirementState.KNOWN,
            reasons=("already resolved",),
            evidence_ids=("EV-KNOWN",),
            confidence=ConfidenceBand.HIGH,
            human_validation_required=False,
        ),
    )

    with pytest.raises(ValueError, match="does not require human validation"):
        apply_human_validation(
            node=_node(),
            resolution=resolution,
            decision=_decision(HumanValidationAction.REVISE, value="15%"),
        )


def test_conflict_cannot_be_approved_as_fact_but_can_be_revised_explicitly():
    conflict = RequirementClaim(
        claim_id="CONFLICT-01",
        requirement_id="REQ-01",
        subject="MLT-C08",
        predicate=PARAMETER,
        value="12% versus 15%",
        state=RequirementState.CONFLICT,
        provenance=ClaimProvenance(
            source_type=RequirementSourceType.LLM_INFERENCE,
            source_reference="inference:conflict",
            reasoning_method="controlled-llm-inference:v1",
            evidence_ids=("EV-CONFLICT",),
            validation_status="UNVERIFIED",
        ),
        requires_human_validation=True,
    )
    resolution = _pending_resolution(claims=(conflict,), state=RequirementState.CONFLICT)

    with pytest.raises(ValueError, match="cannot be approved as a fact"):
        apply_human_validation(
            node=_node(),
            resolution=resolution,
            decision=_decision(
                HumanValidationAction.APPROVE,
                target_claim_id="CONFLICT-01",
            ),
        )

    revised = apply_human_validation(
        node=_node(),
        resolution=resolution,
        decision=_decision(
            HumanValidationAction.REVISE,
            target_claim_id="CONFLICT-01",
            value="15%",
            decision_id="DEC-002",
        ),
    )
    assert revised.validated_claim is not None
    assert revised.validated_claim.value == "15%"
    assert revised.validated_claim.state is RequirementState.KNOWN


def test_missing_or_noncanonical_target_entity_fails_closed():
    source = _inference_claim()
    resolution = _pending_resolution(claims=(source,))
    decision = _decision(HumanValidationAction.APPROVE, target_claim_id="INF-01")

    with pytest.raises(ValueError, match="explicit target entity"):
        apply_human_validation(node=_node(entity=None), resolution=resolution, decision=decision)

    with pytest.raises(ValueError, match="target entity must be canonical"):
        apply_human_validation(
            node=_node(entity=" MLT-C08 "),
            resolution=resolution,
            decision=decision,
        )


def test_decision_value_and_action_contracts_fail_closed():
    with pytest.raises(ValueError, match="HumanValidationAction"):
        HumanValidationDecision(
            decision_id="DEC-001",
            reviewer_id="reviewer-01",
            requirement_id="REQ-01",
            parameter=PARAMETER,
            action="APPROVE",  # type: ignore[arg-type]
            target_claim_id="INF-01",
        )

    with pytest.raises(ValueError, match="canonical without surrounding whitespace"):
        _decision(HumanValidationAction.REVISE, value=" 15% ")


def test_audit_is_bounded_and_does_not_grant_execution():
    source = _inference_claim()
    result = apply_human_validation(
        node=_node(),
        resolution=_pending_resolution(claims=(source,)),
        decision=_decision(HumanValidationAction.APPROVE, target_claim_id="INF-01"),
    )

    audit = audit_human_validation(result)
    assert set(audit) == {
        "decision_id",
        "reviewer_id",
        "requirement_id",
        "parameter",
        "action",
        "status",
        "source_claim_id",
        "evidence_ids",
        "validated_claim_id",
        "validated_value",
        "can_execute",
    }
    assert audit["can_execute"] is False
    assert "reasoning" not in audit
    assert "metadata" not in audit
