import pytest

from elo.core.context_resolution import ContextEvidence, ContextQuery, ContextResolutionEngine, ContextSource
from elo.core.gpt_handoff import ConsultativeReturn, GPTDecisionHandoff
from elo.core.maturity_engine import MaturityAssessment


def maturity_discovery():
    return MaturityAssessment(scores={"enterprise_context": 0.5})


def maturity_specialist():
    return MaturityAssessment(scores={dimension: 0.9 for dimension in (
        "enterprise_context",
        "end_to_end_process",
        "systemic_reasoning",
        "evidence_analysis",
        "decision_memory",
        "uncertainty_management",
        "outcome_feedback",
    )})


def test_context_handoff_reuses_resolved_context_and_never_authorizes_change():
    engine = ContextResolutionEngine()
    context = engine.resolve(
        ContextQuery(
            "avaliar capacidade",
            tenant_id="tenant-a",
            domain="PCP",
            principal_id="principal-a",
            request_id="request-a",
            correlation_id="corr-a",
        )
    )
    handoff = GPTDecisionHandoff.from_context(
        objective="validar lacunas de capacidade",
        context=context,
        maturity=maturity_discovery(),
    )
    payload = handoff.consultation_payload()
    assert payload["tenant_id"] == "tenant-a"
    assert payload["domain"] == "PCP"
    assert payload["correlation_id"] == "corr-a"
    assert "authorize" not in payload["specialist_instruction"].lower()


def test_specialist_validation_requires_scoped_evidence():
    engine = ContextResolutionEngine()
    context = engine.resolve(ContextQuery("avaliar capacidade", tenant_id="tenant-a", domain="PCP"))
    with pytest.raises(ValueError, match="scoped evidence"):
        GPTDecisionHandoff.from_context(
            objective="validar capacidade",
            context=context,
            maturity=maturity_specialist(),
        )


def test_specialist_validation_uses_only_scoped_evidence():
    engine = ContextResolutionEngine()
    context = engine.resolve(ContextQuery("avaliar capacidade", tenant_id="tenant-a", domain="PCP"))
    context = engine.enrich(
        context,
        sources=(ContextSource("s1", "document", "external", tenant_id="tenant-a", domain="PCP"),),
        evidence=(ContextEvidence("s1", "capacity fact", 0.9, tenant_id="tenant-a", domain="PCP"),),
    )
    handoff = GPTDecisionHandoff.from_context(
        objective="validar capacidade",
        context=context,
        maturity=maturity_specialist(),
    )
    assert handoff.mode == "SPECIALIST_VALIDATION"
    assert handoff.evidence_ids == ("s1",)


def test_consultative_return_is_bounded_and_non_authoritative():
    result = ConsultativeReturn(
        status="REVIEWED",
        classification="ADAPT_REQUIRED",
        confidence=0.8,
        evidence=("s1",),
        recommended_adjustments=("validar capacidade",),
        recommended_action="REVIEW",
        human_decision_required=True,
    )
    assert result.classification == "ADAPT_REQUIRED"
    assert result.human_decision_required is True
    with pytest.raises(ValueError):
        ConsultativeReturn(status="INVALID", classification="X", confidence=1.2)
