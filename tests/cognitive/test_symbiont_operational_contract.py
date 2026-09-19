import pytest

from elo.cognitive.symbiont_operational_contract import (
    MIN_CONFIDENCE,
    SymbiontRequest,
    SymbiontRequestGuard,
)


def request(**overrides):
    values = dict(
        operation="query",
        tenant_scope="tenant-a",
        confidence=0.80,
        evidence_ids=("ev-1",),
    )
    values.update(overrides)
    return SymbiontRequest(**values)


def test_allowed_operation_is_accepted():
    SymbiontRequestGuard.validate(request())


@pytest.mark.parametrize("operation", ["write", "schema_change", "ddl", "dml", "decision_register"])
def test_mutating_operations_are_blocked(operation):
    with pytest.raises(ValueError, match="blocked"):
        SymbiontRequestGuard.validate(request(operation=operation))


def test_canonical_mutation_is_blocked():
    with pytest.raises(ValueError, match="canonical"):
        SymbiontRequestGuard.validate(request(canonical_mutation_allowed=True))


def test_authority_cannot_escape_recommendation():
    with pytest.raises(ValueError, match="recommend"):
        SymbiontRequestGuard.validate(request(authority="decide"))


def test_high_confidence_requires_evidence():
    with pytest.raises(ValueError, match="evidence"):
        SymbiontRequestGuard.validate(request(confidence=MIN_CONFIDENCE, evidence_ids=()))


def test_low_confidence_requires_human_escalation():
    assert SymbiontRequestGuard.requires_human_escalation(confidence=0.69)


def test_high_risk_requires_human_escalation():
    assert SymbiontRequestGuard.requires_human_escalation(confidence=0.90, high_risk=True)


def test_clean_request_does_not_require_escalation():
    assert not SymbiontRequestGuard.requires_human_escalation(confidence=0.90)
