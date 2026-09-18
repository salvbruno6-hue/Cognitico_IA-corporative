"""Tests for the consolidated Symbiont operational boundary."""

import pytest

from elo.cognitive.symbiont_operational_contract import (
    DecisionArtifact,
    SymbiontDecisionBrief,
    SymbiontRequestGuard,
    validate_artifact,
    validate_operation,
    reject_canonical_or_secret_fields,
)


def test_ack_authorization_and_non_destructive_boundary():
    guard = SymbiontRequestGuard("req-1", "tenant-a", True, True)
    assert guard.human_escalation().required is False


def test_missing_ack_is_blocked():
    with pytest.raises(ValueError, match="acknowledgement"):
        SymbiontRequestGuard("req-1", "tenant-a", False, True)


def test_high_risk_and_financial_limit_escalate():
    guard = SymbiontRequestGuard(
        "req-1", "tenant-a", True, True,
        high_risk=True, financial_impact=101, owner_financial_limit=100,
    )
    escalation = guard.human_escalation()
    assert escalation.required is True
    assert "high_risk" in escalation.reasons
    assert "financial_impact_above_owner_limit" in escalation.reasons


def test_pii_escalates_only_when_present_and_unmasked():
    no_pii = SymbiontRequestGuard("req-1", "tenant-a", True, True)
    assert no_pii.human_escalation().required is False
    pii = SymbiontRequestGuard("req-1", "tenant-a", True, True, pii_present=True)
    assert "pii_masking_not_confirmed" in pii.human_escalation().reasons


def test_low_confidence_requires_human_escalation():
    brief = SymbiontDecisionBrief(
        request_id="req-1",
        tenant_scope="tenant-a",
        problem="p",
        evidence=("e1",),
        alternatives=("a1",),
        trade_offs=("t1",),
        recommendation="r",
        confidence=0.69,
        risks=("r1",),
        audit_refs=("audit-1",),
    )
    assert "confidence_below_minimum" in brief.human_escalation.reasons


@pytest.mark.parametrize("operation", ["write", "schema_change", "ddl", "dml", "decision_register"])
def test_mutating_and_second_ledger_operations_are_blocked(operation):
    with pytest.raises(ValueError):
        validate_operation(operation)


def test_governed_operations_and_artifacts_are_explicit():
    assert validate_operation("query").value == "query"
    assert validate_operation("scenario_sim").value == "scenario_sim"
    assert validate_artifact("decision_brief") is DecisionArtifact.DECISION_BRIEF


@pytest.mark.parametrize("field", ["service_role_key", "canonical_knowledge", "decision_ledger", "memory_ledger"])
def test_forbidden_authority_or_secret_fields_are_rejected(field):
    with pytest.raises(ValueError):
        reject_canonical_or_secret_fields({field: "x"})


def test_decision_brief_cannot_be_canonical_mutation():
    with pytest.raises(ValueError, match="canonical"):
        SymbiontDecisionBrief(
            request_id="req-1",
            tenant_scope="tenant-a",
            problem="p",
            evidence=("e1",),
            alternatives=("a1",),
            trade_offs=("t1",),
            recommendation="r",
            confidence=0.9,
            risks=(),
            audit_refs=("audit-1",),
            canonical_mutation_allowed=True,
        )
