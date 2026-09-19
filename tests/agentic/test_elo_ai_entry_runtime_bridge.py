from elo.agentic.entry_contract import (
    DEFAULT_BOOTSTRAP_ARTIFACTS,
    ELOAIEntryGate,
    ELOAIEntryMode,
    ELOAIEntryState,
    ELOAIEntryRequest,
)
from elo.agentic.entry_runtime_bridge import bind_to_elo_runtime


REPOSITORY = "salvbruno6-hue/Cognitico_IA-corporative"


def _ready_session():
    request = ELOAIEntryRequest(
        repository=REPOSITORY,
        connector="github",
        session_id="session-1",
        requested_mode=ELOAIEntryMode.READ_ONLY_CONSULTATION,
        tenant_id="tenant-a",
        principal_id="principal-a",
        request_id="request-1",
        correlation_id="corr-1",
        authorization_scope="elo:read",
    )
    return ELOAIEntryGate().establish(
        request,
        readable_artifacts=DEFAULT_BOOTSTRAP_ARTIFACTS,
    )


def test_entry_session_binds_to_existing_request_context():
    session = _ready_session()
    binding = bind_to_elo_runtime(session, conversation_id="conversation-1")

    assert binding.session is session
    assert binding.request_context.tenant_id == "tenant-a"
    assert binding.request_context.principal_id == "principal-a"
    assert binding.request_context.session_id == "session-1"
    assert binding.request_context.request_id == "request-1"
    assert binding.request_context.correlation_id == "corr-1"
    assert binding.request_context.conversation_id == "conversation-1"
    assert binding.request_context.authorization_scope == "elo:read"
    assert binding.knowledge_provider.request_context is binding.request_context
    assert binding.knowledge_provider.allow_temporal_trace is False


def test_blocked_entry_cannot_reach_runtime():
    request = ELOAIEntryRequest(
        repository=REPOSITORY,
        connector="github",
        session_id="session-1",
        requested_mode=ELOAIEntryMode.READ_ONLY_CONSULTATION,
        tenant_id="tenant-a",
        principal_id="principal-a",
        request_id="request-1",
        correlation_id="corr-1",
        authorization_scope="elo:read",
    )
    session = ELOAIEntryGate().establish(
        request,
        readable_artifacts=DEFAULT_BOOTSTRAP_ARTIFACTS[:-1],
    )

    assert session.state is ELOAIEntryState.BLOCKED

    try:
        bind_to_elo_runtime(session, conversation_id="conversation-1")
    except ValueError as exc:
        assert "blocked entry session" in str(exc)
    else:
        raise AssertionError("blocked session unexpectedly reached runtime")


def test_read_only_entry_does_not_enable_temporal_trace():
    binding = bind_to_elo_runtime(_ready_session(), conversation_id="conversation-1")
    assert binding.knowledge_provider.allow_temporal_trace is False
