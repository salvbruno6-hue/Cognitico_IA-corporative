from datetime import datetime, timezone

import pytest

from elo.agent_intake.runtime_operational_evidence import (
    RepeatabilityEvidence,
    RuntimeProvenance,
    create_runtime_evidence,
)
from elo.agent_intake.runtime_operational_evidence_adapter import to_production_outcome
from elo.application.use_cases.orchestrator import AuthorizationDecision
from elo.core.execution_boundary import ExecutionRequest, ExecutionStatus, execute_governed


CANDIDATE = "EXT-TOOL-SEARCH-HERMES"
EVIDENCE = ("EV-PROD-001",)
OCCURRED = datetime(2026, 9, 29, 18, 0, tzinfo=timezone.utc)


class ProductionAdapter:
    def execute(self, request):
        return {
            "environment": "production",
            "source_commit": "prod-runtime-001",
            "metric": "representation_footprint_chars",
        }


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
    return execute_governed(
        ExecutionRequest(
            request_id=execution_id,
            tenant_id="production-tenant",
            principal_id="identity-prod",
            action_id=CANDIDATE,
            authorization_id=grant_id,
            evidence_ids=EVIDENCE,
            correlation_id=f"correlation-{execution_id}",
            decision_pattern_candidate_ref="PATTERN-EXT-TOOL-SEARCH-HERMES",
        ),
        ProductionAdapter(),
    )


def _observation(execution_id: str, observed: float):
    return create_runtime_evidence(
        execution_id=execution_id,
        candidate_id=CANDIDATE,
        owner="ELO Model/Tool Routing",
        runtime_entrypoint="ExecutionRouter.search_tool_schemas",
        action_observed=True,
        metric="representation_footprint_chars",
        direction="minimize",
        baseline=100.0,
        observed_value=observed,
        attribution="candidate",
        provenance=RuntimeProvenance(
            commit="prod-runtime-001",
            runtime_trace=f"trace-{execution_id}",
        ),
        regression=False,
        repeatability=RepeatabilityEvidence(executions=1, successful=1, rate=1.0),
        timestamp=OCCURRED,
        decision_pattern_candidate_ref="PATTERN-EXT-TOOL-SEARCH-HERMES",
    )


def test_production_evidence_requires_external_authorization_and_real_execution():
    first = _execution("exec-prod-001", "grant-prod-001")
    second = _execution("exec-prod-002", "grant-prod-002")

    result = to_production_outcome(
        observations=(
            _observation("exec-prod-001", 80.0),
            _observation("exec-prod-002", 75.0),
        ),
        execution_outcomes=(first, second),
        authorizations=(
            _authorization("grant-prod-001"),
            _authorization("grant-prod-002"),
        ),
        candidate_id=CANDIDATE,
    )

    assert first.status is ExecutionStatus.EXECUTED
    assert second.status is ExecutionStatus.EXECUTED
    assert result.level == "OPERATIONAL_OUTCOME"
    assert result.production_proven is True
    assert result.repeatable is True
    assert result.attribution == "CANDIDATE_ATTRIBUTED"


def test_controlled_runtime_cannot_be_reclassified_as_production():
    class ControlledAdapter:
        def execute(self, request):
            return {"environment": "controlled", "source_commit": "prod-runtime-001"}

    outcome = execute_governed(
        ExecutionRequest(
            request_id="exec-controlled-001",
            tenant_id="controlled-tenant",
            principal_id="identity-prod",
            action_id=CANDIDATE,
            authorization_id="grant-controlled-001",
            evidence_ids=EVIDENCE,
            correlation_id="correlation-controlled",
            decision_pattern_candidate_ref="PATTERN-EXT-TOOL-SEARCH-HERMES",
        ),
        ControlledAdapter(),
    )

    with pytest.raises(ValueError, match="explicit production environment"):
        to_production_outcome(
            observations=(_observation("exec-controlled-001", 80.0), _observation("exec-controlled-002", 75.0)),
            execution_outcomes=(outcome, outcome),
            authorizations=(
                _authorization("grant-controlled-001"),
                _authorization("grant-controlled-001"),
            ),
            candidate_id=CANDIDATE,
        )


def test_invalid_or_mismatched_authorization_cannot_prove_production():
    first = _execution("exec-prod-003", "grant-prod-003")
    second = _execution("exec-prod-004", "grant-prod-004")

    with pytest.raises(ValueError, match="authorization resource"):
        to_production_outcome(
            observations=(
                _observation("exec-prod-003", 80.0),
                _observation("exec-prod-004", 75.0),
            ),
            execution_outcomes=(first, second),
            authorizations=(
                _authorization("grant-prod-003", resource_id="OTHER-CANDIDATE"),
                _authorization("grant-prod-004"),
            ),
            candidate_id=CANDIDATE,
        )


def test_single_production_execution_is_not_enough_for_repeatable_proof():
    outcome = _execution("exec-prod-005", "grant-prod-005")

    with pytest.raises(ValueError, match="at least two observations"):
        to_production_outcome(
            observations=(_observation("exec-prod-005", 80.0),),
            execution_outcomes=(outcome,),
            authorizations=(_authorization("grant-prod-005"),),
            candidate_id=CANDIDATE,
        )


def test_duplicate_execution_identity_cannot_establish_production_repeatability():
    outcome = _execution("exec-prod-006", "grant-prod-006")

    with pytest.raises(ValueError, match="distinct execution identities"):
        to_production_outcome(
            observations=(
                _observation("exec-prod-006", 80.0),
                _observation("exec-prod-006", 75.0),
            ),
            execution_outcomes=(outcome, outcome),
            authorizations=(
                _authorization("grant-prod-006"),
                _authorization("grant-prod-006"),
            ),
            candidate_id=CANDIDATE,
        )
