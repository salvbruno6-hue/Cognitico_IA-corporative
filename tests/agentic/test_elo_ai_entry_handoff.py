from elo.agentic.entry_contract import (
    DEFAULT_BOOTSTRAP_ARTIFACTS,
    ELOAIEntryGate,
    ELOAIEntryMode,
    ELOAIEntryRequest,
    ELOAIEntryState,
)
from elo.agentic.entry_handoff import ELOAIEntryHandoff, ELOAIEntryHandoffError


REPOSITORY = "salvbruno6-hue/Cognitico_IA-corporative"


def _request(mode=ELOAIEntryMode.AUTHORIZED_SPECIALIST, **kwargs):
    return ELOAIEntryRequest(
        repository=REPOSITORY,
        connector="github",
        session_id="session-1",
        requested_mode=mode,
        tenant_id="tenant-a",
        domain="engineering",
        principal_id="principal-a",
        request_id="request-1",
        correlation_id="corr-1",
        authorization_scope="engineering:read",
        authenticated_github_identity="github-ai",
        elo_operator_record="operator-a",
        capability="elo:knowledge.read",
        **kwargs,
    )


def _entry(**kwargs):
    return ELOAIEntryGate().establish(
        _request(**kwargs),
        readable_artifacts=DEFAULT_BOOTSTRAP_ARTIFACTS,
    )


def test_established_specialist_entry_binds_existing_elo_request_context():
    session = ELOAIEntryHandoff().bind(_entry())
    assert session.request_context.tenant_id == "tenant-a"
    assert session.request_context.principal_id == "principal-a"
    assert session.request_context.request_id == "request-1"
    assert session.request_context.correlation_id == "corr-1"
    assert session.request_context.authorization_scope == "engineering:read"


def test_handoff_does_not_accept_blocked_entry():
    entry = ELOAIEntryGate().establish(
        ELOAIEntryRequest(
            repository=REPOSITORY,
            connector="github",
            session_id="session-1",
            requested_mode=ELOAIEntryMode.AUTHORIZED_SPECIALIST,
        ),
        readable_artifacts=DEFAULT_BOOTSTRAP_ARTIFACTS[:-1],
    )
    assert entry.state is ELOAIEntryState.BLOCKED
    try:
        ELOAIEntryHandoff().bind(entry)
    except ELOAIEntryHandoffError:
        pass
    else:
        raise AssertionError("blocked entry must not reach ELO Cognitive")


def test_read_only_repository_entry_is_not_enough_for_elo_query():
    entry = ELOAIEntryGate().establish(
        ELOAIEntryRequest(
            repository=REPOSITORY,
            connector="github",
            session_id="session-1",
        ),
        readable_artifacts=DEFAULT_BOOTSTRAP_ARTIFACTS,
    )
    assert entry.state is ELOAIEntryState.READY
    assert ELOAIEntryHandoff.can_query(entry) is False
    try:
        ELOAIEntryHandoff().bind(entry)
    except ELOAIEntryHandoffError:
        pass
    else:
        raise AssertionError("repository read access must not become ELO Cognitive identity")


def test_governed_execution_entry_preserves_correlation_for_handoff():
    entry = _entry(
        mode=ELOAIEntryMode.GOVERNED_EXECUTION,
        operation_classification="bounded_write",
    )
    session = ELOAIEntryHandoff().bind(entry)
    assert session.entry.execution_binding_ready is True
    assert session.request_context.session_id == "session-1"
