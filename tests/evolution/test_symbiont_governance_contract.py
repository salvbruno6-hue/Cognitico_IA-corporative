import pytest

from elo.cognitive.symbiont_governance_contract import (
    CONFIDENCE_MINIMUM,
    DecisionBrief,
    MandateAcknowledgement,
    assess_escalation,
    validate_symbiont_operation,
)


def ack() -> MandateAcknowledgement:
    return MandateAcknowledgement("req-1", "identity-1", "tenant-a", "1.0", True)


def test_ack_is_required_before_operation() -> None:
    with pytest.raises(ValueError, match="acknowledgement"):
        validate_symbiont_operation(
            acknowledgement=None,
            operation="query",
        )


def test_operation_contract_fails_closed_for_pii_and_canonical_mutation() -> None:
    with pytest.raises(ValueError, match="PII"):
        validate_symbiont_operation(
            acknowledgement=ack(),
            operation="query",
            pii_exposure=True,
        )
    with pytest.raises(ValueError, match="canonical mutation"):
        validate_symbiont_operation(
            acknowledgement=ack(),
            operation="write",
            canonical_mutation=True,
        )


def test_decision_brief_requires_evidence_and_exposes_confidence_gate() -> None:
    with pytest.raises(ValueError, match="evidence"):
        DecisionBrief(
            "req-1", "tenant-a", "problem", (), ("alt",), ("tradeoff",),
            "recommendation", CONFIDENCE_MINIMUM, ("risk",), "audit-1",
        )
    brief = DecisionBrief(
        "req-1", "tenant-a", "problem", ("e-1",), ("alt",), ("tradeoff",),
        "recommendation", CONFIDENCE_MINIMUM, ("risk",), "audit-1",
    )
    assert brief.confidence_sufficient is True


def test_escalation_covers_confidence_risk_conflict_evidence_and_financial_limit() -> None:
    result = assess_escalation(
        confidence=0.69,
        risk="HIGH",
        canonical_conflict=True,
        insufficient_evidence=True,
        financial_impact=101,
        financial_limit=100,
    )
    assert result.required is True
    assert {
        "confidence_below_minimum",
        "high_risk",
        "canonical_conflict",
        "insufficient_evidence",
        "financial_limit_exceeded",
    } <= set(result.reasons)


def test_escalation_does_not_invent_a_financial_threshold() -> None:
    result = assess_escalation(
        confidence=0.90,
        risk="LOW",
        financial_impact=1000000,
        financial_limit=None,
    )
    assert result.required is False


def test_valid_read_operation_passes() -> None:
    validate_symbiont_operation(
        acknowledgement=ack(),
        operation="query",
    )
