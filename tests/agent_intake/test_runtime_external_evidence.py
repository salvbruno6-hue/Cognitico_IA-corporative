from datetime import datetime, timezone

import pytest

from elo.agent_intake.runtime_external_evidence import (
    ExternalRuntimeObservation,
    ingest_external_runtime_observation,
)


def _observation(**overrides):
    values = {
        "execution_id": "exec-external-001",
        "candidate_id": "PATTERN-EXT-ROUTE-HERMES",
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
        "decision_pattern_candidate_ref": "PATTERN-EXT-ROUTE-HERMES",
        "authorization_id": "grant-prod-001",
        "authorization_evidence_ref": "auth-evidence-001",
    }
    values.update(overrides)
    return ExternalRuntimeObservation(**values)


def test_external_runtime_intake_preserves_observed_provenance():
    evidence = ingest_external_runtime_observation(_observation())

    assert evidence.execution_id == "exec-external-001"
    assert evidence.candidate_id == "PATTERN-EXT-ROUTE-HERMES"
    assert evidence.provenance.commit == "prod-runtime-001"
    assert evidence.provenance.runtime_trace == "trace-external-001"
    assert evidence.decision_pattern_candidate_ref == "PATTERN-EXT-ROUTE-HERMES"
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
