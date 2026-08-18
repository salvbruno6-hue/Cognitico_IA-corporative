from dataclasses import dataclass

import pytest

from elo.core.source_discovery import SourceCandidate
from elo.core.source_resolver import (
    RetrievedSource,
    SourceResolutionRequest,
    SourceResolver,
)
from elo.core.temporal_memory import TemporalConversationMemory


CANDIDATE = SourceCandidate(
    kind="GITHUB",
    reason="architecture source",
    priority=5,
    query="architecture",
    required_capability="architecture_review",
)


@dataclass
class FakeAdapter:
    kind: str = "GITHUB"
    capability: str = "architecture_review"
    enabled: bool = True

    def available(self) -> bool:
        return self.enabled

    def retrieve(self, candidate, request):
        return (
            RetrievedSource(
                source_id="github:1",
                source_type="GITHUB",
                content="authorized evidence",
                provenance={"origin": "fake-github"},
            ),
        )


def request():
    return SourceResolutionRequest(
        query="architecture",
        tenant_id="tenant-a",
        domain="governance",
        principal_id="principal-a",
        session_id="session-a",
        request_id="request-a",
        correlation_id="correlation-a",
        conversation_id="conversation-a",
        authorization_scope="github.read",
    )


def test_authorized_retrieval_enters_temporal_memory_with_context():
    memory = TemporalConversationMemory()
    result = SourceResolver((FakeAdapter(),), memory).resolve(CANDIDATE, request())

    assert result.status == "RETRIEVED_TO_TEMPORAL"
    assert len(result.retrieved) == 1
    records = memory.list("conversation-a")
    assert len(records) == 1
    assert records[0].provenance["tenant_id"] == "tenant-a"
    assert records[0].provenance["domain"] == "governance"
    assert records[0].provenance["request_id"] == "request-a"
    assert records[0].provenance["correlation_id"] == "correlation-a"


def test_missing_adapter_is_explicit_gap():
    result = SourceResolver().resolve(CANDIDATE, request())

    assert result.status == "UNAVAILABLE"
    assert "no adapter registered" in result.gap


def test_unavailable_adapter_is_explicit_gap():
    result = SourceResolver((FakeAdapter(enabled=False),)).resolve(CANDIDATE, request())

    assert result.status == "UNAVAILABLE"
    assert "unavailable" in result.gap


def test_capability_mismatch_blocks_retrieval():
    adapter = FakeAdapter(capability="wrong-capability")
    result = SourceResolver((adapter,)).resolve(CANDIDATE, request())

    assert result.status == "UNAUTHORIZED"
    assert "capability" in result.gap


def test_resolution_requires_full_context_boundary():
    invalid = request()
    invalid = SourceResolutionRequest(
        query=invalid.query,
        tenant_id="",
        domain=invalid.domain,
        principal_id=invalid.principal_id,
        session_id=invalid.session_id,
        request_id=invalid.request_id,
        correlation_id=invalid.correlation_id,
        conversation_id=invalid.conversation_id,
        authorization_scope=invalid.authorization_scope,
    )

    with pytest.raises(ValueError, match="tenant_id"):
        SourceResolver().resolve(CANDIDATE, invalid)
