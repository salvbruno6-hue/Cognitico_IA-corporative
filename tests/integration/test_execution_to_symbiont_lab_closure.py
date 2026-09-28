from types import SimpleNamespace

import pytest

from elo.agent_intake.hermes_symbiont_loop import apply_candidate_through_symbiont
from elo.application.use_cases.orchestrator import AuthorizationDecision
from elo.cognitive.symbionte_lab import SymbiontLabAdapter, SymbiontLabObservation
from elo.core.decision_outcome_loop import DecisionLifecycle, DecisionState
from elo.core.execution_boundary import ExecutionRequest, ExecutionStatus, execute_governed
from elo.core.systemic_primitives import DecisionRecord, OutcomeFeedback
from elo.core.learning_governance import GovernedLearningService


METRIC = "FPY"
BASELINE = "0.70"
CURRENT = "0.77"
DIRECTION = "maximize"
EVIDENCE = "EV-FPY-001"


class MemoryStub:
    def __init__(self):
        self.calls = []

    def remember(self, **kwargs):
        self.calls.append(kwargs)


class AuthorizedAdapter:
    def execute(self, request):
        return {
            "source_commit": "benchmark-closure-001",
            "metric": METRIC,
            "direction": DIRECTION,
            "baseline": BASELINE,
            "current": CURRENT,
        }


class FailedAdapter:
    def execute(self, request):
        raise RuntimeError("controlled execution failure")


def _implementation():
    return (
        SimpleNamespace(
            result="IMPLEMENTATION_AUTHORIZED",
            next_state="IMPLEMENTATION_AUTHORIZED",
            canonical_mutation=False,
        ),
        SimpleNamespace(candidate_id="EXT-FPY-HERMES", provenance_refs=(EVIDENCE,)),
    )


def _authorization():
    return AuthorizationDecision(
        authorized=True,
        authority="elo-authz",
        identity_id="identity-a",
        role="ELO_ADMIN",
        evidence_ref=EVIDENCE,
        session_id="session-a",
        binding_id="binding-a",
        grant_id="grant-a",
        operation="execute",
        resource_id="EXT-FPY-HERMES",
        expires_at="2099-01-01T00:00:00+00:00",
    )


def _authorized_execution(*, request_id="exec-fpy-001", decision_id="decision-fpy-001", evidence=(EVIDENCE,)):
    return execute_governed(
        ExecutionRequest(
            request_id=request_id,
            tenant_id="benchmark-tenant",
            principal_id="identity-a",
            action_id="EXT-FPY-HERMES",
            authorization_id="grant-a",
            evidence_ids=evidence,
            correlation_id=decision_id,
        ),
        AuthorizedAdapter(),
    )


def _observation(outcome):
    return SymbiontLabObservation.from_execution_outcome(
        outcome,
        observation_id="obs-fpy-001",
        tenant_id="benchmark-tenant",
        domain="HERMES",
        decision_id="decision-fpy-001",
        expected_outcome=f"{METRIC} improves from {BASELINE}",
        observed_outcome=f"{METRIC} reached {CURRENT}",
        hypothesis="controlled implementation improves FPY",
        baseline=f"{METRIC}={BASELINE}",
        experiment="authorized controlled benchmark execution",
        result=f"{METRIC}={CURRENT}",
        regression_status="PASS",
        generalization_status="CONFIRMED",
        risk="LOW",
        existing_owner=None,
        scope=f"candidate:EXT-FPY-HERMES",
    )


def _attributed_lifecycle():
    lifecycle = DecisionLifecycle(
        DecisionRecord(
            "decision-fpy-001",
            "execute governed FPY benchmark",
            "controlled closure test",
            expected_outcome=f"{METRIC}={CURRENT}",
        )
    )
    lifecycle.transition(DecisionState.APPROVED)
    lifecycle.transition(DecisionState.EXECUTED)
    lifecycle.transition(DecisionState.OBSERVING)
    return lifecycle


def test_authorized_hermes_path_reaches_governed_execution_then_lab_and_attributed_handoff():
    candidate = apply_candidate_through_symbiont(
        "EXT-FPY-HERMES",
        _implementation,
        implementation_decision_id="decision-fpy-001",
        implementation_scope="candidate:EXT-FPY-HERMES",
        implementation_evidence_refs=(EVIDENCE,),
        authorization=_authorization(),
    )
    assert candidate.status == "ACTIVE"
    assert candidate.next_state == "IMPLEMENTATION_AUTHORIZED"

    outcome = _authorized_execution()
    assert outcome.status is ExecutionStatus.EXECUTED
    assert outcome.executed is True
    assert outcome.evidence_ids == (EVIDENCE,)
    assert outcome.correlation_id == "decision-fpy-001"
    assert outcome.occurred_at is not None

    observation = _observation(outcome)
    observation.validate_execution_outcome(outcome)

    lifecycle = _attributed_lifecycle()
    lifecycle.attach_outcome(
        OutcomeFeedback(
            decision_id="decision-fpy-001",
            expected=f"{METRIC}={BASELINE}",
            observed=f"{METRIC}={CURRENT}",
            evidence_ids=(EVIDENCE,),
            observed_at=outcome.occurred_at,
        )
    )
    lifecycle.transition(DecisionState.EVALUATED, evidence_ids=(EVIDENCE,))
    lifecycle.attach_attribution({"decision": 1.0})
    lifecycle.transition(DecisionState.ATTRIBUTED, evidence_ids=(EVIDENCE,))

    evaluation = lifecycle.handoff_to_symbiont(
        adapter=SymbiontLabAdapter(GovernedLearningService(MemoryStub())),
        observation=observation,
        principal_id="identity-a",
        dataset_version="benchmark-fpy-001",
    )

    assert evaluation.observation.evidence_ids == (EVIDENCE,)
    assert evaluation.state == "LAB_ONLY"
    assert lifecycle.state == DecisionState.LEARNED


def test_automation_without_external_authorization_is_blocked():
    result = apply_candidate_through_symbiont(
        "EXT-FPY-HERMES",
        _implementation,
        implementation_decision_id="decision-fpy-unauthorized",
        implementation_scope="candidate:EXT-FPY-HERMES",
        implementation_evidence_refs=(EVIDENCE,),
        authorization=None,
    )
    assert result.status == "HUMAN_APPROVAL_REQUIRED"


def test_execution_without_evidence_is_blocked_and_cannot_become_lab_observation():
    outcome = execute_governed(
        ExecutionRequest(
            request_id="exec-fpy-no-evidence",
            tenant_id="benchmark-tenant",
            principal_id="identity-a",
            action_id="EXT-FPY-HERMES",
            authorization_id="grant-a",
            evidence_ids=(),
            correlation_id="decision-fpy-001",
        ),
        AuthorizedAdapter(),
    )
    assert outcome.status is ExecutionStatus.BLOCKED
    assert outcome.executed is False
    with pytest.raises(ValueError, match="successfully executed"):
        _observation(outcome)


def test_failed_execution_cannot_enter_lab_as_positive_observation():
    outcome = execute_governed(
        ExecutionRequest(
            request_id="exec-fpy-failed",
            tenant_id="benchmark-tenant",
            principal_id="identity-a",
            action_id="EXT-FPY-HERMES",
            authorization_id="grant-a",
            evidence_ids=(EVIDENCE,),
            correlation_id="decision-fpy-001",
        ),
        FailedAdapter(),
    )
    assert outcome.status is ExecutionStatus.FAILED
    assert outcome.executed is False
    with pytest.raises(ValueError, match="successfully executed"):
        _observation(outcome)


def test_cross_execution_outcome_is_rejected_by_the_existing_lab_owner():
    first = _authorized_execution(request_id="exec-fpy-001")
    second = _authorized_execution(request_id="exec-fpy-002")
    observation = _observation(first)

    with pytest.raises(ValueError, match="execution identity"):
        observation.validate_execution_outcome(second)


def test_cross_decision_outcome_is_rejected():
    outcome = _authorized_execution(
        request_id="exec-fpy-other-decision",
        decision_id="decision-other",
    )
    with pytest.raises(ValueError, match="not bound to the decision"):
        SymbiontLabObservation.from_execution_outcome(
            outcome,
            observation_id="obs-other",
            tenant_id="benchmark-tenant",
            domain="HERMES",
            decision_id="decision-fpy-001",
            expected_outcome="expected",
            observed_outcome="observed",
            hypothesis="controlled hypothesis",
            baseline=BASELINE,
            experiment="controlled experiment",
            result=CURRENT,
            regression_status="PASS",
            generalization_status="CONFIRMED",
            risk="LOW",
            existing_owner=None,
            scope="candidate:EXT-FPY-HERMES",
            source_commit="benchmark-closure-001",
        )


def test_handoff_rejects_lifecycle_that_is_not_attributed():
    outcome = _authorized_execution()
    observation = _observation(outcome)
    lifecycle = _attributed_lifecycle()

    lifecycle.attach_outcome(
        OutcomeFeedback(
            decision_id="decision-fpy-001",
            expected=f"{METRIC}={BASELINE}",
            observed=f"{METRIC}={CURRENT}",
            evidence_ids=(EVIDENCE,),
        )
    )
    lifecycle.transition(DecisionState.EVALUATED, evidence_ids=(EVIDENCE,))

    with pytest.raises(ValueError, match="attributed state"):
        lifecycle.handoff_to_symbiont(
            adapter=SymbiontLabAdapter(GovernedLearningService(MemoryStub())),
            observation=observation,
            principal_id="identity-a",
            dataset_version="benchmark-fpy-001",
        )


def test_implementation_authorization_is_consumed_but_not_issued_by_symbiont():
    result = apply_candidate_through_symbiont(
        "EXT-FPY-HERMES",
        _implementation,
        implementation_decision_id="decision-fpy-consume",
        implementation_scope="candidate:EXT-FPY-HERMES",
        implementation_evidence_refs=(EVIDENCE,),
        authorization=_authorization(),
    )
    assert result.status == "ACTIVE"
    assert result.next_state == "IMPLEMENTATION_AUTHORIZED"
    assert result.canonical_mutation is False
