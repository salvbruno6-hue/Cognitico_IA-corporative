from __future__ import annotations

from dataclasses import dataclass, field

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
    audit_requirement_resolution,
)


@dataclass
class FakeProvider:
    kind: ResolutionAttemptKind
    result: ResolutionStepResult
    calls: list[tuple[str, str, tuple[str, ...]]] = field(default_factory=list)

    def resolve(self, node, parameter, claims):
        self.calls.append(
            (node.requirement_id, parameter, tuple(claim.claim_id for claim in claims))
        )
        return self.result


def _node(*, entity: str | None = "MLT-C08", claims=()):
    return RequirementNode(
        requirement_id="SO-203.26:R1",
        text="Definir espessura do MDF para o modelo MLT-C08",
        entity=entity,
        claims=tuple(claims),
    )


def _claim(
    *,
    claim_id: str,
    requirement_id: str = "SO-203.26:R1",
    subject: str = "MLT-C08",
    predicate: str = "mdf.thickness",
    value: str = "15 mm",
    state: RequirementState = RequirementState.KNOWN,
    source_type: RequirementSourceType = RequirementSourceType.RULE,
    source_reference: str = "fixture:source",
    evidence_ids=("EV-1",),
    validation_status: str = "VALIDATED",
    requires_human_validation: bool = False,
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


def _empty_provider(kind: ResolutionAttemptKind):
    return FakeProvider(
        kind=kind,
        result=ResolutionStepResult(source_reference=f"fixture:{kind.value.lower()}"),
    )


def test_four_real_attempts_run_in_canonical_order_and_can_confirm_gap():
    providers = {
        ResolutionAttemptKind.INFERENCE: _empty_provider(ResolutionAttemptKind.INFERENCE),
        ResolutionAttemptKind.CALCULATION: _empty_provider(ResolutionAttemptKind.CALCULATION),
        ResolutionAttemptKind.RETRIEVAL: _empty_provider(ResolutionAttemptKind.RETRIEVAL),
        ResolutionAttemptKind.RULE: _empty_provider(ResolutionAttemptKind.RULE),
    }

    result = RequirementResolutionFlow(providers=providers).resolve(
        node=_node(), parameter="mdf.thickness"
    )

    assert result.executed_order == (
        ResolutionAttemptKind.RETRIEVAL,
        ResolutionAttemptKind.RULE,
        ResolutionAttemptKind.CALCULATION,
        ResolutionAttemptKind.INFERENCE,
    )
    assert result.assessment.state is RequirementState.GAP_CONFIRMED
    assert result.assessment.human_validation_required is True


def test_missing_provider_does_not_count_as_attempt_and_keeps_gap_candidate():
    providers = {
        kind: _empty_provider(kind)
        for kind in (
            ResolutionAttemptKind.RETRIEVAL,
            ResolutionAttemptKind.RULE,
            ResolutionAttemptKind.CALCULATION,
        )
    }

    result = RequirementResolutionFlow(providers=providers).resolve(
        node=_node(), parameter="mdf.thickness"
    )

    assert result.executed_order == (
        ResolutionAttemptKind.RETRIEVAL,
        ResolutionAttemptKind.RULE,
        ResolutionAttemptKind.CALCULATION,
    )
    assert result.assessment.state is RequirementState.GAP_CANDIDATE


def test_so203_semantic_retrieval_prevents_false_gap_and_stops_later_stages():
    retrieved = _claim(
        claim_id="KNOW-203-MDF",
        requirement_id="SO-203.26:R2",
        predicate="espessura mdf",
        state=RequirementState.DOCUMENTED,
        source_type=RequirementSourceType.DOCUMENT,
        source_reference="kb:so203:material",
        evidence_ids=("EV-SO203-MDF",),
    )
    retrieval = FakeProvider(
        kind=ResolutionAttemptKind.RETRIEVAL,
        result=ResolutionStepResult(
            source_reference="source-resolver:so203",
            claims=(retrieved,),
            evidence_ids=("EV-RETRIEVAL-SO203",),
        ),
    )
    rule = _empty_provider(ResolutionAttemptKind.RULE)
    calculation = _empty_provider(ResolutionAttemptKind.CALCULATION)
    inference = _empty_provider(ResolutionAttemptKind.INFERENCE)

    result = RequirementResolutionFlow(
        providers={
            ResolutionAttemptKind.RETRIEVAL: retrieval,
            ResolutionAttemptKind.RULE: rule,
            ResolutionAttemptKind.CALCULATION: calculation,
            ResolutionAttemptKind.INFERENCE: inference,
        },
        semantic_policy=SemanticRetrievalPolicy(
            aliases={"mdf.thickness": ("espessura mdf",)},
        ),
    ).resolve(node=_node(), parameter="mdf.thickness")

    assert result.assessment.state is RequirementState.RETRIEVED
    assert result.executed_order == (ResolutionAttemptKind.RETRIEVAL,)
    assert result.attempts[0].status is ResolutionAttemptStatus.RESOLVED
    assert result.claims[-1].value == "15 mm"
    assert result.claims[-1].provenance.source_reference == "kb:so203:material"
    assert "EV-SO203-MDF" in result.claims[-1].provenance.evidence_ids
    assert rule.calls == []
    assert calculation.calls == []
    assert inference.calls == []


def test_cross_context_retrieval_without_applicability_requires_validation():
    candidate = _claim(
        claim_id="OTHER-SO-MDF",
        requirement_id="SO-114.26:R1",
        state=RequirementState.DOCUMENTED,
        source_type=RequirementSourceType.DOCUMENT,
        source_reference="kb:so114:material",
    )
    retrieval = FakeProvider(
        kind=ResolutionAttemptKind.RETRIEVAL,
        result=ResolutionStepResult(
            source_reference="source-resolver:cross-context",
            claims=(candidate,),
        ),
    )

    result = RequirementResolutionFlow(
        providers={ResolutionAttemptKind.RETRIEVAL: retrieval}
    ).resolve(node=_node(), parameter="mdf.thickness")

    assert result.attempts[0].status is ResolutionAttemptStatus.NOT_APPLICABLE
    assert result.assessment.state is RequirementState.HUMAN_VALIDATION_REQUIRED
    assert result.assessment.human_validation_required is True
    assert "EV-1" in result.assessment.evidence_ids
    assert not any(claim.state is RequirementState.RETRIEVED for claim in result.claims)


def test_cross_context_retrieval_resolves_only_with_explicit_applicability_evidence():
    candidate = _claim(
        claim_id="OTHER-SO-MDF",
        requirement_id="SO-114.26:R1",
        state=RequirementState.DOCUMENTED,
        source_type=RequirementSourceType.DOCUMENT,
        source_reference="kb:so114:material",
        evidence_ids=("EV-SOURCE",),
    )
    retrieval = FakeProvider(
        kind=ResolutionAttemptKind.RETRIEVAL,
        result=ResolutionStepResult(
            source_reference="source-resolver:cross-context",
            claims=(candidate,),
        ),
    )

    result = RequirementResolutionFlow(
        providers={ResolutionAttemptKind.RETRIEVAL: retrieval},
        semantic_policy=SemanticRetrievalPolicy(
            applicability_evidence={"OTHER-SO-MDF": ("EV-APPLIES-SO203",)},
        ),
    ).resolve(node=_node(), parameter="mdf.thickness")

    assert result.assessment.state is RequirementState.RETRIEVED
    assert "EV-APPLIES-SO203" in result.claims[-1].provenance.evidence_ids


def test_missing_target_entity_requires_explicit_entity_applicability_evidence():
    candidate = _claim(
        claim_id="ENTITY-MDF",
        requirement_id="SO-203.26:R2",
        state=RequirementState.DOCUMENTED,
        source_type=RequirementSourceType.DOCUMENT,
    )
    retrieval = FakeProvider(
        kind=ResolutionAttemptKind.RETRIEVAL,
        result=ResolutionStepResult(
            source_reference="source-resolver:no-target-entity",
            claims=(candidate,),
        ),
    )

    blocked = RequirementResolutionFlow(
        providers={ResolutionAttemptKind.RETRIEVAL: retrieval}
    ).resolve(node=_node(entity=None), parameter="mdf.thickness")
    assert blocked.assessment.state is RequirementState.HUMAN_VALIDATION_REQUIRED
    assert blocked.assessment.human_validation_required is True
    assert blocked.attempts[0].status is ResolutionAttemptStatus.NOT_APPLICABLE

    resolved = RequirementResolutionFlow(
        providers={ResolutionAttemptKind.RETRIEVAL: retrieval},
        semantic_policy=SemanticRetrievalPolicy(
            entity_applicability_evidence={
                "ENTITY-MDF": ("EV-ENTITY-APPLIES",),
            },
        ),
    ).resolve(node=_node(entity=None), parameter="mdf.thickness")
    assert resolved.assessment.state is RequirementState.RETRIEVED
    assert "EV-ENTITY-APPLIES" in resolved.claims[-1].provenance.evidence_ids


def test_invalid_rule_claim_for_another_requirement_fails_closed():
    bad = _claim(claim_id="BAD-RULE", requirement_id="SO-OTHER:R1")
    provider = FakeProvider(
        kind=ResolutionAttemptKind.RULE,
        result=ResolutionStepResult(source_reference="rule-engine:v1", claims=(bad,)),
    )

    with pytest.raises(ValueError, match="another requirement"):
        RequirementResolutionFlow(
            providers={ResolutionAttemptKind.RULE: provider}
        ).resolve(node=_node(), parameter="mdf.thickness")


def test_rule_known_claim_requires_validated_governed_evidence():
    unvalidated = _claim(
        claim_id="RULE-UNVALIDATED",
        validation_status="UNVERIFIED",
    )
    provider = FakeProvider(
        kind=ResolutionAttemptKind.RULE,
        result=ResolutionStepResult(
            source_reference="rule-engine:v1",
            claims=(unvalidated,),
        ),
    )

    with pytest.raises(ValueError, match="governed validation"):
        RequirementResolutionFlow(
            providers={ResolutionAttemptKind.RULE: provider}
        ).resolve(node=_node(), parameter="mdf.thickness")


def test_calculation_can_resolve_after_retrieval_and_rule_fail():
    retrieval = _empty_provider(ResolutionAttemptKind.RETRIEVAL)
    rule = _empty_provider(ResolutionAttemptKind.RULE)
    calculated = _claim(
        claim_id="CALC-MDF",
        state=RequirementState.CALCULATED,
        source_type=RequirementSourceType.CALCULATION,
        source_reference="calculator:mdf:v1",
        evidence_ids=("EV-CALC-INPUT", "EV-CALC-FORMULA"),
    )
    calculation = FakeProvider(
        kind=ResolutionAttemptKind.CALCULATION,
        result=ResolutionStepResult(
            source_reference="calculator:mdf:v1",
            claims=(calculated,),
        ),
    )
    inference = _empty_provider(ResolutionAttemptKind.INFERENCE)

    result = RequirementResolutionFlow(
        providers={
            ResolutionAttemptKind.RETRIEVAL: retrieval,
            ResolutionAttemptKind.RULE: rule,
            ResolutionAttemptKind.CALCULATION: calculation,
            ResolutionAttemptKind.INFERENCE: inference,
        }
    ).resolve(node=_node(), parameter="mdf.thickness")

    assert result.assessment.state is RequirementState.CALCULATED
    assert result.executed_order == (
        ResolutionAttemptKind.RETRIEVAL,
        ResolutionAttemptKind.RULE,
        ResolutionAttemptKind.CALCULATION,
    )
    assert inference.calls == []


def test_inference_never_becomes_automatic_fact():
    inferred = _claim(
        claim_id="INF-MDF",
        state=RequirementState.INFERRED,
        source_type=RequirementSourceType.LLM_INFERENCE,
        source_reference="inference:controlled:v1",
        evidence_ids=("EV-CONTEXT",),
        validation_status="UNVERIFIED",
        requires_human_validation=True,
    )
    inference = FakeProvider(
        kind=ResolutionAttemptKind.INFERENCE,
        result=ResolutionStepResult(
            source_reference="inference:controlled:v1",
            claims=(inferred,),
        ),
    )

    result = RequirementResolutionFlow(
        providers={ResolutionAttemptKind.INFERENCE: inference}
    ).resolve(node=_node(), parameter="mdf.thickness")

    assert result.attempts[0].status is ResolutionAttemptStatus.NOT_APPLICABLE
    assert result.assessment.state is RequirementState.HUMAN_VALIDATION_REQUIRED
    assert result.assessment.human_validation_required is True


def test_inference_provider_cannot_emit_known_fact():
    known = _claim(
        claim_id="INF-KNOWN",
        state=RequirementState.KNOWN,
        source_type=RequirementSourceType.LLM_INFERENCE,
        requires_human_validation=False,
    )
    inference = FakeProvider(
        kind=ResolutionAttemptKind.INFERENCE,
        result=ResolutionStepResult(
            source_reference="inference:controlled:v1",
            claims=(known,),
        ),
    )

    with pytest.raises(ValueError, match="cannot emit state KNOWN"):
        RequirementResolutionFlow(
            providers={ResolutionAttemptKind.INFERENCE: inference}
        ).resolve(node=_node(), parameter="mdf.thickness")


def test_ambiguous_retrieval_values_surface_conflict_instead_of_false_resolution():
    first = _claim(
        claim_id="MDF-15",
        requirement_id="SO-203.26:R2",
        state=RequirementState.DOCUMENTED,
        source_type=RequirementSourceType.DOCUMENT,
        value="15 mm",
        evidence_ids=("EV-15",),
    )
    second = _claim(
        claim_id="MDF-18",
        requirement_id="SO-203.26:R3",
        state=RequirementState.DOCUMENTED,
        source_type=RequirementSourceType.DOCUMENT,
        value="18 mm",
        evidence_ids=("EV-18",),
    )
    retrieval = FakeProvider(
        kind=ResolutionAttemptKind.RETRIEVAL,
        result=ResolutionStepResult(
            source_reference="source-resolver:ambiguous",
            claims=(first, second),
        ),
    )

    result = RequirementResolutionFlow(
        providers={ResolutionAttemptKind.RETRIEVAL: retrieval}
    ).resolve(node=_node(), parameter="mdf.thickness")

    assert result.attempts[0].status is ResolutionAttemptStatus.CONFLICT
    assert result.assessment.state is RequirementState.CONFLICT


def test_existing_governed_claim_short_circuits_without_calling_providers():
    existing = _claim(claim_id="EXISTING-RULE")
    retrieval = _empty_provider(ResolutionAttemptKind.RETRIEVAL)

    result = RequirementResolutionFlow(
        providers={ResolutionAttemptKind.RETRIEVAL: retrieval}
    ).resolve(node=_node(claims=(existing,)), parameter="mdf.thickness")

    assert result.assessment.state is RequirementState.KNOWN
    assert result.attempts == ()
    assert retrieval.calls == []


def test_audit_trace_exposes_only_bounded_resolution_evidence():
    providers = {
        kind: _empty_provider(kind)
        for kind in (
            ResolutionAttemptKind.RETRIEVAL,
            ResolutionAttemptKind.RULE,
            ResolutionAttemptKind.CALCULATION,
        )
    }
    result = RequirementResolutionFlow(providers=providers).resolve(
        node=_node(), parameter="mdf.thickness"
    )

    audit = audit_requirement_resolution(result)

    assert audit["executed_order"] == ("RETRIEVAL", "RULE", "CALCULATION")
    assert audit["final"]["state"] == "GAP_CANDIDATE"
    assert set(audit) == {
        "requirement_id",
        "parameter",
        "executed_order",
        "attempts",
        "final",
    }
    assert all("note" not in attempt for attempt in audit["attempts"])


def test_provider_kind_mismatch_is_rejected():
    wrong = _empty_provider(ResolutionAttemptKind.RULE)
    with pytest.raises(ValueError, match="does not match provider kind"):
        RequirementResolutionFlow(
            providers={ResolutionAttemptKind.RETRIEVAL: wrong}
        )
