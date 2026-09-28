from types import SimpleNamespace

import pytest

from elo.application.use_cases.orchestrator import AuthorizationDecision
from elo.agent_intake.hermes_symbiont_loop import apply_candidate_through_symbiont


def _implementation(*, result="READY_FOR_ELO_REVIEW", next_state="ELO_REVIEW", canonical_mutation=False):
    return SimpleNamespace(
        result=result,
        next_state=next_state,
        canonical_mutation=canonical_mutation,
    )


def test_candidate_enters_persistent_symbiont_boundary_and_stops_at_review():
    evidence = SimpleNamespace(candidate_id="EXT-PROFILE-HERMES")

    result = apply_candidate_through_symbiont(
        "EXT-PROFILE-HERMES",
        lambda: (_implementation(), evidence),
    )

    assert result.candidate_id == "EXT-PROFILE-HERMES"
    assert result.status == "ACTIVE"
    assert result.next_state == "ELO_REVIEW"
    assert result.evidence is evidence
    assert result.canonical_mutation is False


def test_symbiont_fails_closed_when_candidate_attempts_canonical_mutation():
    evidence = SimpleNamespace(candidate_id="EXT-PROFILE-HERMES")

    result = apply_candidate_through_symbiont(
        "EXT-PROFILE-HERMES",
        lambda: (
            _implementation(
                result="IMPLEMENTATION_AUTHORIZED",
                next_state="IMPLEMENTATION_AUTHORIZED",
                canonical_mutation=True,
            ),
            evidence,
        ),
    )

    assert result.status == "HUMAN_APPROVAL_REQUIRED"
    assert result.canonical_mutation is True


def _authorization(candidate_id: str, *, expires_at="2099-01-01T00:00:00+00:00", evidence_ref="EV-FPY-001", session_id="session-a", binding_id="binding-a"):
    return AuthorizationDecision(
        authorized=True,
        authority="elo-authz",
        identity_id="identity-a",
        role="ELO_ADMIN",
        evidence_ref=evidence_ref,
        session_id=session_id,
        binding_id=binding_id,
        grant_id="grant-a",
        operation="execute",
        resource_id=candidate_id,
        expires_at=expires_at,
    )


def _authorized_application(candidate_id: str, evidence_ref="EV-FPY-001"):
    return _implementation(
        result="IMPLEMENTATION_AUTHORIZED",
        next_state="IMPLEMENTATION_AUTHORIZED",
        canonical_mutation=False,
    ), SimpleNamespace(candidate_id=candidate_id, provenance_refs=(evidence_ref,))


def test_symbiont_consumes_valid_external_implementation_authorization():
    result = apply_candidate_through_symbiont(
        "EXT-FPY-HERMES",
        lambda: _authorized_application("EXT-FPY-HERMES"),
        implementation_decision_id="decision-fpy-001",
        implementation_scope="skill:EXT-FPY-HERMES",
        implementation_evidence_refs=("EV-FPY-001",),
        authorization=_authorization("EXT-FPY-HERMES"),
    )

    assert result.status == "ACTIVE"
    assert result.next_state == "IMPLEMENTATION_AUTHORIZED"


@pytest.mark.parametrize(
    "kwargs, expected_reason",
    [
        ({"expires_at": "2020-01-01T00:00:00+00:00"}, "invalid or expired"),
        ({"session_id": ""}, "invalid or expired"),
        ({"binding_id": ""}, "invalid or expired"),
    ],
)
def test_symbiont_blocks_invalid_external_authorization(kwargs, expected_reason):
    result = apply_candidate_through_symbiont(
        "EXT-FPY-HERMES",
        lambda: _authorized_application("EXT-FPY-HERMES"),
        implementation_decision_id="decision-fpy-002",
        implementation_scope="skill:EXT-FPY-HERMES",
        implementation_evidence_refs=("EV-FPY-001",),
        authorization=_authorization("EXT-FPY-HERMES", **kwargs),
    )
    assert result.status == "HUMAN_APPROVAL_REQUIRED"
    assert result.next_state == "HUMAN_APPROVAL_REQUIRED"


def test_symbiont_blocks_authorization_bound_to_another_candidate():
    result = apply_candidate_through_symbiont(
        "EXT-FPY-HERMES",
        lambda: _authorized_application("EXT-FPY-HERMES"),
        implementation_decision_id="decision-fpy-003",
        implementation_scope="skill:EXT-FPY-HERMES",
        implementation_evidence_refs=("EV-FPY-001",),
        authorization=_authorization("OTHER-CANDIDATE"),
    )
    assert result.status == "HUMAN_APPROVAL_REQUIRED"


def test_symbiont_blocks_authorization_with_cross_execution_evidence():
    result = apply_candidate_through_symbiont(
        "EXT-FPY-HERMES",
        lambda: _authorized_application("EXT-FPY-HERMES", evidence_ref="EV-OTHER-CANDIDATE"),
        implementation_decision_id="decision-fpy-004",
        implementation_scope="skill:EXT-FPY-HERMES",
        implementation_evidence_refs=("EV-FPY-001",),
        authorization=_authorization("EXT-FPY-HERMES", evidence_ref="EV-OTHER-CANDIDATE"),
    )
    assert result.status == "HUMAN_APPROVAL_REQUIRED"
