from types import SimpleNamespace

from elo.application.use_cases.orchestrator import AuthorizationDecision
from elo.agent_intake.hermes_symbiont_gate_continuation import HermesSymbiontGateSession
from elo.cognitive.symbiont_gate_perception import ExternalGateObservation


def _implementation():
    return SimpleNamespace(
        result="READY_FOR_ELO_REVIEW",
        next_state="ELO_REVIEW",
        canonical_mutation=False,
    )


def test_hermes_waits_on_external_gate_then_resumes_without_reexecuting_probe():
    calls = {"probe": 0}

    def probe():
        calls["probe"] += 1
        return _implementation(), SimpleNamespace(candidate_id="EXT-PROFILE-HERMES")

    session = HermesSymbiontGateSession("EXT-PROFILE-HERMES", probe)
    try:
        started = session.start()
        assert started.status == "ACTIVE"
        assert calls["probe"] == 1

        waiting = session.wait_for_gate("evolution-gate:profile", delay_seconds=10, now=100.0)
        assert waiting.waiting_for_gate is True
        assert waiting.status == "WAITING_FOR_EXTERNAL_GATE"

        not_due = session.perceive_and_resume(
            observe=lambda gate_id: ExternalGateObservation(gate_id, "COMPLETED", "evidence:gate"),
            now=lambda: 105.0,
        )
        assert not_due.waiting_for_gate is True
        assert not_due.resumed is False
        assert calls["probe"] == 1

        resumed = session.perceive_and_resume(
            observe=lambda gate_id: ExternalGateObservation(gate_id, "COMPLETED", "evidence:gate"),
            now=lambda: 110.0,
        )
        assert resumed.resumed is True
        assert resumed.status == "ACTIVE"
        assert resumed.next_state == "ELO_REVIEW"
        assert resumed.evidence is not None
        assert calls["probe"] == 1
    finally:
        session.close()


def test_hermes_external_gate_remains_waiting_when_gate_is_pending():
    session = HermesSymbiontGateSession(
        "EXT-PROFILE-HERMES",
        lambda: (_implementation(), SimpleNamespace(candidate_id="EXT-PROFILE-HERMES")),
    )
    try:
        session.start()
        session.wait_for_gate("evolution-gate:profile", delay_seconds=10, now=100.0)

        result = session.perceive_and_resume(
            observe=lambda gate_id: ExternalGateObservation(gate_id, "PENDING"),
            now=lambda: 110.0,
        )
        assert result.waiting_for_gate is True
        assert result.resumed is False
        assert result.status == "WAITING_FOR_EXTERNAL_GATE"
    finally:
        session.close()


def test_gate_session_consumes_valid_external_implementation_authorization():
    authorization = AuthorizationDecision(
        authorized=True,
        authority="elo-authz",
        identity_id="identity-a",
        role="ELO_ADMIN",
        evidence_ref="EV-FPY-001",
        session_id="session-a",
        binding_id="binding-a",
        grant_id="grant-a",
        resource_id="EXT-FPY-HERMES",
        expires_at="2099-01-01T00:00:00+00:00",
    )
    session = HermesSymbiontGateSession(
        "EXT-FPY-HERMES",
        lambda: (
            SimpleNamespace(
                result="IMPLEMENTATION_AUTHORIZED",
                next_state="IMPLEMENTATION_AUTHORIZED",
                canonical_mutation=False,
            ),
            SimpleNamespace(
                candidate_id="EXT-FPY-HERMES",
                provenance_refs=("EV-FPY-001",),
            ),
        ),
        implementation_decision_id="decision-fpy-gate",
        implementation_scope="skill:EXT-FPY-HERMES",
        implementation_evidence_refs=("EV-FPY-001",),
        authorization=authorization,
    )
    try:
        result = session.start()
        assert result.status == "ACTIVE"
        assert result.next_state == "IMPLEMENTATION_AUTHORIZED"
    finally:
        session.close()


def test_gate_session_fails_closed_when_candidate_self_authorizes_without_mutation():
    session = HermesSymbiontGateSession(
        "EXT-PROFILE-HERMES",
        lambda: (
            SimpleNamespace(
                result="IMPLEMENTATION_AUTHORIZED",
                next_state="IMPLEMENTATION_AUTHORIZED",
                canonical_mutation=False,
            ),
            SimpleNamespace(candidate_id="EXT-PROFILE-HERMES"),
        ),
    )
    try:
        result = session.start()
        assert result.status == "HUMAN_APPROVAL_REQUIRED"
        assert result.next_state == "HUMAN_APPROVAL_REQUIRED"
    finally:
        session.close()
