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
            ack(), "tenant-a", ("read",), ("execution",),
            constraints={"canonical_mutation": True},
        )


def test_envelope_rejects_scope_drift():
    with pytest.raises(ValueError, match="tenant scope"):
        GovernedExternalAIEnvelope(
            ack(), "tenant-b", ("read",), ("execution",)
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
