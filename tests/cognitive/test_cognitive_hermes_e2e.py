"""Acceptance tests for the ELO Cognitive -> Symbiont -> Hermes path."""

from __future__ import annotations

from typing import Any

from elo.cognitive import CognitiveCore
from elo.cognitive.symbiont_hermes_bridge import SymbiontHermesBridge
from elo.interface.contracts import CognitiveRequest


CAPABILITY = "hermes:runtime_probe"


def _fake_transport(endpoint: str, payload: dict[str, Any]) -> dict[str, Any]:
    assert endpoint == "https://hermes.test"
    assert payload["mission_class"] == "runtime_probe"
    assert payload["authorized_capabilities"] == (CAPABILITY,)
    assert payload["constraints"]["read_only"] is True
    return {
        "request_id": payload["request_id"],
        "status": "completed",
        "execution": {"probe": "ok"},
        "evidence": ({"type": "runtime_probe", "status": "ok"},),
        "outcome": {"runtime": "available"},
    }


def test_explicit_authorized_mission_reaches_hermes(monkeypatch) -> None:
    monkeypatch.setenv("ELO_HERMES_ENDPOINT", "https://hermes.test")
    bridge = SymbiontHermesBridge()

    class BridgeWithFakeTransport(SymbiontHermesBridge):
        def execute(self, request, *, capability, endpoint, transport=None):
            return super().execute(
                request,
                capability=capability,
                endpoint=endpoint,
                transport=_fake_transport,
            )

    request = CognitiveRequest(
        message="Run the bounded Hermes runtime probe.",
        tenant_id="tenant-a",
        domain="core",
        context={
            "hermes_mission": {
                "mission_class": "runtime_probe",
                "authorized_capabilities": [CAPABILITY],
            }
        },
    )

    result = CognitiveCore(hermes_bridge=BridgeWithFakeTransport()).process(request)

    assert result["response"]["type"] == "hermes_execution"
    assert result["hermes"]["request_id"] == request.request_id
    assert result["hermes"]["status"] == "completed"
    assert result["hermes"]["outcome"]["runtime"] == "available"
    assert result["provenance"]["provider"] == "elo-hermes-via-symbiont"
    assert result["provenance"]["validation_status"] == "evidence_validated"
    assert bridge is not None


def test_hermes_is_not_invoked_without_explicit_mission(monkeypatch) -> None:
    monkeypatch.setenv("ELO_HERMES_ENDPOINT", "https://hermes.test")
    result = CognitiveCore().process(
        CognitiveRequest(message="hello", tenant_id="tenant-a")
    )
    assert result["response"]["type"] == "analysis"
    assert "hermes" not in result


def test_unauthorized_capability_is_rejected(monkeypatch) -> None:
    monkeypatch.setenv("ELO_HERMES_ENDPOINT", "https://hermes.test")
    request = CognitiveRequest(
        message="Run the bounded Hermes runtime probe.",
        tenant_id="tenant-a",
        context={
            "hermes_mission": {
                "mission_class": "runtime_probe",
                "authorized_capabilities": ["repo:modify"],
            }
        },
    )

    try:
        CognitiveCore().process(request)
    except ValueError as exc:
        assert "capability" in str(exc)
    else:
        raise AssertionError("unauthorized Hermes capability must be rejected")
