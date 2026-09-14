"""Regression tests for governed communication intent."""
import pytest
from src.elo.application.communication_boundary import CommunicationIntent, CommunicationBoundaryError, GovernedCommunicationBoundary


def valid():
    return CommunicationIntent("msg-1", "tenant-1", "principal-1", "email", "recipient:1", "hello", ("ev-1",), {"source": "decision"}, "auth-1", "idem-1")


def test_communication_is_prepared_without_transport_authority():
    assert GovernedCommunicationBoundary().prepare(valid()).authorization_ref == "auth-1"


def test_communication_requires_authorization_and_evidence():
    item = valid()
    object.__setattr__(item, "authorization_ref", "")
    with pytest.raises(CommunicationBoundaryError):
        GovernedCommunicationBoundary().prepare(item)


def test_communication_rejects_secret_provenance():
    item = valid()
    object.__setattr__(item, "provenance", {"token": "x"})
    with pytest.raises(CommunicationBoundaryError):
        GovernedCommunicationBoundary().prepare(item)
