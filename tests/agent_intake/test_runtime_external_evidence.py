from datetime import datetime, timezone

import pytest

from elo.agent_intake.runtime_external_evidence import (
    ExternalRuntimeObservation,
    ingest_external_runtime_observation,
    validate_external_runtime_binding,
)
from elo.application.use_cases.orchestrator import AuthorizationDecision
from elo.core.execution_boundary import ExecutionRequest, ExecutionStatus, execute_governed


CANDIDATE = "PATTERN-EXT-ROUTE-HERMES"
EVIDENCE = ("auth-evidence-001",)


def _observation(**overrides):
    values = {
        "execution_id": "exec-external-001",
        "candidate_id": CANDIDATE,
        "owner": "ELO Routing",
        "runtime_entrypoint": "IntelligenceRouter.execute_routed",
        "timestamp": datetime(2026, 10, 4, 22, 30, tzinfo=timezone.utc),
        "action_observed": True,
        "metric": "representation_footprint_chars",
        "direction": "minimize",
        "baseline": 100.0,
        "observed_value": 80.0,
        "attribution": "candidate",
        "runtime_commit": "prod-runtime-001",
        "runtime_trace": "trace-external-001",
        "environment": "production",
        "decision_pattern_candidate_ref": CANDIDATE,
        "authorization_id": "grant-prod-001",
        "authorization_evidence_ref": EVIDENCE[0],
    }
    values.update(overrides)
    return ExternalRuntimeObservation(**values)


def _authorization(grant_id: str, *, resource_id: str = CANDIDATE):
    return AuthorizationDecision(
        authorized=True,
        authority="elo-authz",
        identity_id="identity-prod",
        role="ELO_OPERATOR",
        evidence_ref=EVIDENCE[0],
        session_id=f"session-{grant_id}",
        binding_id=f"binding-{grant_id}",
        grant_id=grant_id,
        operation="execute",
        resource_id=resource_id,
        expires_at="2099-01-01T00:00:00+00:00",
    )


def _execution(execution_id: str, grant_id: str):
    class ProductionAdapter:
        def execute(self, request):
            return {
                "environment": "production",
                "source_commit": "prod-runtime-001",
            }

    return execute_governed(
        ExecutionRequest(
            request_id=execution_id,
            tenant_id="production-tenant",
            principal_id="identity-prod",
            action_id=CANDIDATE,
            authorization_id=grant_id,
            evidence_ids=EVIDENCE,
            correlation_id=f"correlation-{execution_id}",
            decision_pattern_candidate_ref=CANDIDATE,
        ),
        ProductionAdapter(),
    )


def test_external_runtime_binding_accepts_matching_execution_and_authorization():
    outcome = _execution("exec-external-001", "grant-prod-001")
    valid, errors = validate_external_runtime_binding(
        observation=_observation(),
        execution_outcome=outcome,
        authorization=_authorization("grant-prod-001"),
    )

    assert outcome.status is ExecutionStatus.EXECUTED
    assert valid is True
    assert errors == ()


def test_external_runtime_binding_rejects_mismatched_authorization():
    outcome = _execution("exec-external-001", "grant-prod-001")
    valid, errors = validate_external_runtime_binding(
        observation=_observation(),
        execution_outcome=outcome,
        authorization=_authorization("grant-other-001"),
    )

    assert valid is False
    assert "AUTHORIZATION_GRANT_MISMATCH" in errors


def test_external_runtime_binding_rejects_candidate_provenance_mismatch():
    outcome = _execution("exec-external-001", "grant-prod-001")
    valid, errors = validate_external_runtime_binding(
        observation=_observation(decision_pattern_candidate_ref="OTHER-PATTERN"),
        execution_outcome=outcome,
        authorization=_authorization("grant-prod-001"),
    )

    assert valid is False
    assert "DECISION_PATTERN_PROVENANCE_MISMATCH" in errors


def test_external_runtime_intake_preserves_observed_provenance():
    evidence = ingest_external_runtime_observation(_observation())

    assert evidence.execution_id == "exec-external-001"
    assert evidence.candidate_id == CANDIDATE
    assert evidence.provenance.commit == "prod-runtime-001"
    assert evidence.provenance.runtime_trace == "trace-external-001"
    assert evidence.decision_pattern_candidate_ref == CANDIDATE
    assert evidence.repeatability.executions == 1
    assert evidence.operational_outcome_proven is False


def test_external_runtime_intake_rejects_unsupported_environment():
    with pytest.raises(ValueError, match="unsupported runtime environment"):
        _observation(environment="staging")


def test_external_runtime_intake_rejects_missing_authorization_reference():
    with pytest.raises(ValueError, match="authorization_id"):
        _observation(authorization_id="")


def test_external_runtime_intake_rejects_unobserved_action():
    with pytest.raises(ValueError, match="action_observed"):
        _observation(action_observed=False)


def test_external_runtime_intake_rejects_non_candidate_attribution():
    with pytest.raises(ValueError, match="candidate attribution"):
        _observation(attribution="inferred")


def test_external_runtime_intake_does_not_promote_production_by_itself():
    evidence = ingest_external_runtime_observation(_observation())
    assert evidence.operational_outcome_proven is False
