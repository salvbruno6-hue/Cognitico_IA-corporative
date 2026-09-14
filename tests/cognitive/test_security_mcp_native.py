from __future__ import annotations

import pytest

from elo.cognitive.security_forensics import SecurityForensics, SecurityObservation
from elo.cognitive.symbiont_mcp_contracts import MCPCapabilityDescriptor, MCPCapabilityState
from elo.forge.mcp_capability_resolver import MCPCapabilityResolver


def test_security_requires_evidence_and_rejects_secret_metadata() -> None:
    with pytest.raises(ValueError, match="requires evidence"):
        SecurityObservation("s1", "t1", "repo", "source", "sha", (), ("fact",))
    with pytest.raises(ValueError, match="secret field"):
        SecurityObservation("s1", "t1", "repo", "source", "sha", ("EV-1",), ("fact",), metadata={"access_token": "x"})


def test_security_classification_reuses_evolution_gate() -> None:
    observation = SecurityObservation(
        "s1", "t1", "repo", "github://repo", "abc123", ("EV-1",), ("commit is signed",), ("[HYPOTHESIS] benign maintenance"),
    )
    decision = SecurityForensics().classify(observation)
    assert decision.candidate_creation_allowed
    assert decision.pattern.domain == "security-forensics"


def test_mcp_resolver_enforces_tenant_authorization_state_and_bound() -> None:
    descriptor = MCPCapabilityDescriptor(
        capability_id="m1", server_id="srv", provider="external", tool_name="search",
        purpose="read-only search", mechanism="constrained query", interface_contract={"input": "query"},
        source_ref="mcp://server", source_commit="sha", tenant_id="t1", domain="research",
        state=MCPCapabilityState.TESTED,
    )
    resolver = MCPCapabilityResolver()
    assert resolver.resolve(descriptor, tenant_id="other", authorized=True).allowed is False
    assert resolver.resolve(descriptor, tenant_id="t1", authorized=False).allowed is False
    assert resolver.resolve(descriptor, tenant_id="t1", authorized=True, requested_tool_calls=11).allowed is False
    allowed = resolver.resolve(descriptor, tenant_id="t1", authorized=True, requested_tool_calls=2)
    assert allowed.allowed is True
    assert allowed.max_tool_calls == 2


def test_mcp_resolver_fails_closed_for_discovered_only_capability() -> None:
    descriptor = MCPCapabilityDescriptor(
        capability_id="m2", server_id="srv", provider="external", tool_name="read",
        purpose="read", mechanism="read", interface_contract={"input": "path"},
        source_ref="mcp://server", source_commit="sha", tenant_id="t1", domain="files",
    )
    result = MCPCapabilityResolver().resolve(descriptor, tenant_id="t1", authorized=True)
    assert result.allowed is False
