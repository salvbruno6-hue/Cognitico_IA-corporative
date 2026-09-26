import pytest

from elo.agentic.ai_entry_runtime import ELOAIEntryRuntime, ELOAICognitiveHandoffError
from elo.agentic.entry_contract import (
    DEFAULT_BOOTSTRAP_ARTIFACTS,
    ELOAIEntryMode,
    ELOAIEntryRequest,
)

REPOSITORY = "salvbruno6-hue/Cognitico_IA-corporative"


def _request(**kwargs):
    return ELOAIEntryRequest(
        repository=REPOSITORY,
        connector="github",
        session_id="session-1",
        requested_mode=ELOAIEntryMode.READ_ONLY_CONSULTATION,
        **kwargs,
    )


def test_connected_ai_binds_to_existing_elo_request_context():
    handoff = ELOAIEntryRuntime().establish_and_bind(
        _request(
            tenant_id="tenant-a",
            principal_id="principal-a",
            request_id="request-1",
            correlation_id="correlation-1",
            authorization_scope="engineering:read",
        ),
        readable_artifacts=DEFAULT_BOOTSTRAP_ARTIFACTS,
        conversation_id="conversation-1",
    )

    assert handoff.entry_session.mode is ELOAIEntryMode.READ_ONLY_CONSULTATION
    assert handoff.request_context.tenant_id == "tenant-a"
    assert handoff.request_context.principal_id == "principal-a"
    assert handoff.request_context.request_id == "request-1"
    assert handoff.request_context.correlation_id == "correlation-1"
    assert handoff.request_context.conversation_id == "conversation-1"
    assert handoff.request_context.authorization_scope == "engineering:read"


def test_connected_ai_without_resolved_context_cannot_enter_cognitive_handoff():
    with pytest.raises(ELOAICognitiveHandoffError, match="resolved context"):
        ELOAIEntryRuntime().establish_and_bind(
            _request(),
            readable_artifacts=DEFAULT_BOOTSTRAP_ARTIFACTS,
            conversation_id="conversation-1",
        )


def test_blocked_entry_never_reaches_cognitive_context():
    with pytest.raises(ELOAICognitiveHandoffError, match="AI entry blocked"):
        ELOAIEntryRuntime().establish_and_bind(
            _request(
                tenant_id="tenant-a",
                principal_id="principal-a",
                request_id="request-1",
                correlation_id="correlation-1",
                authorization_scope="engineering:read",
            ),
            readable_artifacts=DEFAULT_BOOTSTRAP_ARTIFACTS[:-1],
            conversation_id="conversation-1",
        )
