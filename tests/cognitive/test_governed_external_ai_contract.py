import pytest

from elo.cognitive.governed_external_ai_contract import (
    DecisionBrief,
    ExternalAIMandateAck,
    GovernedExternalAIEnvelope,
)


def ack():
    return ExternalAIMandateAck("req-1", "ai-1", "tenant-a", "1.0", acknowledged=True)


def test_mandate_ack_is_required():
    with pytest.raises(ValueError, match="acknowledged"):
        ExternalAIMandateAck("req-1", "ai-1", "tenant-a", "1.0")


def test_envelope_binds_scope_and_cannot_grant_canonical_mutation():
    with pytest.raises(ValueError, match="canonical mutation"):
        GovernedExternalAIEnvelope(
            ack(), "tenant-a", ("read",), ("execution",), "auth-1",
            constraints={"canonical_mutation": True},
        )


def test_envelope_rejects_scope_drift():
    with pytest.raises(ValueError, match="tenant scope"):
        GovernedExternalAIEnvelope(
            ack(), "tenant-b", ("read",), ("execution",), "auth-1"
        )


def test_low_confidence_requires_escalation():
    with pytest.raises(ValueError, match="LOW_CONFIDENCE"):
        DecisionBrief(
            "req-1", "tenant-a", "problem", ("ev-1",), ("alt",),
            ("tradeoff",), "recommendation", 0.60, audit={"source": "elo"}
        )


def test_decision_brief_marks_human_escalation():
    brief = DecisionBrief(
        "req-1", "tenant-a", "problem", ("ev-1",), ("alt",),
        ("tradeoff",), "recommendation", 0.60,
        escalation_reasons=("LOW_CONFIDENCE",),
        audit={"source": "elo"},
    )
    assert brief.human_escalation_required is True


def test_confident_brief_with_evidence_remains_consultative():
    brief = DecisionBrief(
        "req-1", "tenant-a", "problem", ("ev-1",), ("alt",),
        ("tradeoff",), "recommendation", 0.80,
        audit={"source": "elo"},
    )
    assert brief.human_escalation_required is False


def test_decision_brief_rejects_incomplete_output_and_secret_audit_data():
    with pytest.raises(ValueError, match="alternatives"):
        DecisionBrief(
            "req-1", "tenant-a", "problem", ("ev-1",), (), ("tradeoff",),
            "recommendation", 0.80, audit={"source": "elo"}
        )
    with pytest.raises(ValueError, match="sensitive field"):
        DecisionBrief(
            "req-1", "tenant-a", "problem", ("ev-1",), ("alt",), ("tradeoff",),
            "recommendation", 0.80, audit={"api_key": "must-not-cross-boundary"}
        )


def test_external_ai_envelope_blocks_unmasked_pii_and_financial_limit_bypass():
    with pytest.raises(ValueError, match="PII"):
        GovernedExternalAIEnvelope(
            ack(), "tenant-a", ("read",), ("execution",), "auth-1",
            constraints={"pii_exposure": True}
        )
    with pytest.raises(ValueError, match="financial impact"):
        GovernedExternalAIEnvelope(
            ack(), "tenant-a", ("read",), ("execution",), "auth-1",
            constraints={
                "financial_impact": 150.0,
                "financial_limit": 100.0,
            }
        )


def test_financial_limit_can_be_explicitly_escalated():
    envelope = GovernedExternalAIEnvelope(
        ack(), "tenant-a", ("read",), ("execution",), "auth-1",
        constraints={
            "financial_impact": 150.0,
            "financial_limit": 100.0,
            "escalation_reasons": ("FINANCIAL_LIMIT",),
        }
    )
    assert envelope.tenant_scope == "tenant-a"


def test_envelope_requires_authorization_decision_provenance():
    with pytest.raises(ValueError, match="authorization_decision_id"):
        GovernedExternalAIEnvelope(
            ack(), "tenant-a", ("read",), ("execution",), "",
        )


def test_envelope_rejects_empty_authorized_capability():
    with pytest.raises(ValueError, match="empty values"):
        GovernedExternalAIEnvelope(
            ack(), "tenant-a", ("read", ""), ("execution",), "auth-1",
        )
