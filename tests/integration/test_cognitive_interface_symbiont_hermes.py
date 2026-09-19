"""Integration acceptance for the canonical interface -> CognitiveCore -> Symbiont -> Hermes path."""

from __future__ import annotations

from typing import Any

from elo.cognitive import CognitiveCore
from elo.cognitive.symbiont_hermes_bridge import SymbiontHermesBridge
from elo.interface import api
from elo.interface.contracts import CognitiveRequest, CognitiveResponse


CAPABILITY = "hermes:runtime_probe"


def _fake_transport(endpoint: str, payload: dict[str, Any]) -> dict[str, Any]:
    assert endpoint == "https://hermes.integration.test"
    assert payload["mission_class"] == "runtime_probe"
    assert payload["authorized_capabilities"] == (CAPABILITY,)
    return {
        "request_id": payload["request_id"],
        "status": "completed",
        "execution": {"probe": "ok"},
        "evidence": ({"type": "runtime_probe", "status": "ok"},),
        "outcome": {"runtime": "available"},
    }


def test_interface_to_symbiont_hermes_path_preserves_governance(monkeypatch) -> None:
    monkeypatch.setenv("ELO_HERMES_ENDPOINT", "https://hermes.integration.test")

    class BridgeWithFakeTransport(SymbiontHermesBridge):
        def execute(self, request, *, capability, endpoint, transport=None):
            return super().execute(
                request,
                capability=capability,
                endpoint=endpoint,
                transport=_fake_transport,
            )

    api.core = CognitiveCore(hermes_bridge=BridgeWithFakeTransport())

    request = CognitiveRequest(
        message="Run the bounded Hermes runtime probe.",
        tenant_id="tenant-a",
        domain="integration",
        principal_id="principal-1",
        context={
            "hermes_mission": {
                "mission_class": "runtime_probe",
                "authorized_capabilities": [CAPABILITY],
            }
        },
    )

    response = api.cognitive_endpoint(request)

    assert isinstance(response, CognitiveResponse)
    assert response.tenant_id == "tenant-a"
    assert response.provenance.tenant_id == "tenant-a"
    assert response.provenance.principal_id == "principal-1"
    assert response.provenance.provider == "elo-hermes-via-symbiont"
    assert response.provenance.validation_status == "evidence_validated"
    assert response.response["type"] == "hermes_execution"
    assert response.response["status"] == "completed"
