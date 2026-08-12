"""Executable acceptance tests for PR1 canonical alignment."""

import pytest

from elo.cognitive import CognitiveCore
from elo.interface.api import safe_cognitive
from elo.interface.contracts import CognitiveRequest, ErrorContract
from elo.interface.session import SessionManager


def test_request_requires_tenant() -> None:
    with pytest.raises(ValueError):
        CognitiveRequest(message="hello", tenant_id=" ")


def test_vertical_slice_preserves_identity() -> None:
    request = CognitiveRequest(message="analyze this", tenant_id="tenant-a", domain="finance", principal_id="principal-1")
    response = safe_cognitive(request)
    assert not isinstance(response, ErrorContract)
    assert response.tenant_id == "tenant-a"
    assert response.domain == "finance"
    assert response.request_id == request.request_id
    assert response.correlation_id == request.correlation_id
    assert response.provenance.tenant_id == "tenant-a"
    assert response.provenance.principal_id == "principal-1"
    assert response.processing_time_ms >= 0


def test_session_rejects_cross_tenant_access() -> None:
    manager = SessionManager()
    session = manager.get_or_create(tenant_id="tenant-a", principal_id="principal-1")
    with pytest.raises(PermissionError):
        manager.get_or_create(session.id, tenant_id="tenant-b", principal_id="principal-1")


def test_core_emits_provenance_identity() -> None:
    request = CognitiveRequest(message="hello", tenant_id="tenant-a")
    result = CognitiveCore().process(request)
    assert result["provenance"]["tenant_id"] == "tenant-a"
    assert result["provenance"]["request_id"] == request.request_id
