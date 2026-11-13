import pytest

from elo.cognitive.governed_external_ai_contract import (
    DecisionBrief,
    ExternalAIMandateAck,
    GovernedExternalAIEnvelope,
)
from elo.cognitive.symbiont_governance_contract import assess_escalation


def ack() -> ExternalAIMandateAck:
    return ExternalAIMandateAck(
        request_id="req-1",
        actor_id="ai-1",
        tenant_scope="tenant-a",
        mandate_version="1.0",
        acknowledged=True,
    )


def test_escalation_uses_contract_codes() -> None:
    result = assess_escalation(
        confidence=0.5,
        risk="HIGH",
        canonical_conflict=True,
        insufficient_evidence=True,
        financial_impact=120,
        financial_limit=100,
        irreversible_action=True,
        pii_exposure=True,
    )
    assert result.required is True
    assert result.reasons == (
        "LOW_CONFIDENCE",
        "HIGH_RISK",
        "CANON_CONFLICT",
        "INSUFFICIENT_EVIDENCE",
        "IRREVERSIBLE_ACTION",
        "PII_EXPOSURE",
        "FINANCIAL_LIMIT",
    )


def test_decision_brief_accepts_canonical_escalation_codes() -> None:
    brief = DecisionBrief(
        request_id="req-1",
        tenant_scope="tenant-a",
        problem="p",
        evidence=("e1",),
        alternatives=("a1",),
        trade_offs=("t1",),
        recommendation="r",
        confidence=0.5,
        escalation_reasons=("LOW_CONFIDENCE", "HIGH_RISK"),
        audit={"authorization_decision_id": "auth-1", "request_id": "req-1", "tenant_scope": "tenant-a"},
    )
    assert brief.human_escalation_required is True


def test_envelope_rejects_unmasked_pii() -> None:
    with pytest.raises(ValueError, match="PII"):
        GovernedExternalAIEnvelope(
            mandate=ack(),
            tenant_scope="tenant-a",
            authorized_capabilities=("query",),
            evidence_requirements=("outcome",),
            authorization_decision_id="auth-1",
            constraints={"pii_exposure": True},
        )


def test_envelope_rejects_unauthorized_non_read_only() -> None:
    with pytest.raises(ValueError, match="explicit operation authorization"):
        GovernedExternalAIEnvelope(
            mandate=ack(),
            tenant_scope="tenant-a",
            authorized_capabilities=("write",),
            evidence_requirements=("outcome",),
            authorization_decision_id="auth-1",
            constraints={"read_only": False},
        )
