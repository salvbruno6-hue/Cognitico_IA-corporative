from elo.agentic.entry_contract import (
    DEFAULT_BOOTSTRAP_ARTIFACTS,
    ELOAIEntryBlock,
    ELOAIEntryGate,
    ELOAIEntryMode,
    ELOAIEntryRequest,
    ELOAIEntryState,
)


REPOSITORY = "salvbruno6-hue/Cognitico_IA-corporative"


def _request(mode=ELOAIEntryMode.READ_ONLY_CONSULTATION, **kwargs):
    return ELOAIEntryRequest(
        repository=REPOSITORY,
        connector="github",
        session_id="session-1",
        requested_mode=mode,
        **kwargs,
    )


def test_new_github_connection_defaults_to_read_only_and_cannot_write():
    session = ELOAIEntryGate().establish(
        _request(),
        readable_artifacts=DEFAULT_BOOTSTRAP_ARTIFACTS,
    )

    assert session.state is ELOAIEntryState.READY
    assert session.mode is ELOAIEntryMode.READ_ONLY_CONSULTATION
    assert session.repository_ref == "main"
    assert session.execution_binding_ready is False


def test_missing_bootstrap_artifact_blocks_entry():
    session = ELOAIEntryGate().establish(
        _request(),
        readable_artifacts=DEFAULT_BOOTSTRAP_ARTIFACTS[:-1],
    )

    assert session.state is ELOAIEntryState.BLOCKED
    assert session.block is ELOAIEntryBlock.BOOTSTRAP_INCOMPLETE


def test_broader_github_access_than_elo_scope_blocks_entry():
    session = ELOAIEntryGate().establish(
        _request(),
        readable_artifacts=DEFAULT_BOOTSTRAP_ARTIFACTS,
        access_scope_valid=False,
    )

    assert session.state is ELOAIEntryState.BLOCKED
    assert session.block is ELOAIEntryBlock.ACCESS_SCOPE_VIOLATION


def test_specialist_requires_external_binding():
    session = ELOAIEntryGate().establish(
        _request(ELOAIEntryMode.AUTHORIZED_SPECIALIST),
        readable_artifacts=DEFAULT_BOOTSTRAP_ARTIFACTS,
        tenant_id="tenant-a",
        domain="engineering",
        principal_id="principal-a",
        authorization_scope="engineering:read",
    )

    assert session.state is ELOAIEntryState.BLOCKED
    assert session.block is ELOAIEntryBlock.AUTHORIZATION_REQUIRED


def test_specialist_can_enter_after_required_binding_is_present():
    session = ELOAIEntryGate().establish(
        _request(
            ELOAIEntryMode.AUTHORIZED_SPECIALIST,
            tenant_id="tenant-a",
            domain="engineering",
            principal_id="principal-a",
            authorization_scope="engineering:read",
            authenticated_github_identity="github-user",
            elo_operator_record="operator-record",
            capability="specialist:engineering",
        ),
        readable_artifacts=DEFAULT_BOOTSTRAP_ARTIFACTS,
    )

    assert session.state is ELOAIEntryState.READY
    assert session.can_write is False


def test_governed_execution_requires_full_operator_binding_and_correlation():
    session = ELOAIEntryGate().establish(
        _request(
            ELOAIEntryMode.GOVERNED_EXECUTION,
            tenant_id="tenant-a",
            domain="engineering",
            principal_id="principal-a",
            authorization_scope="repo:write",
            authenticated_github_identity="github-user",
            elo_operator_record="operator-record",
            capability="repository:write",
            operation_classification="IMPLEMENTATION",
            request_id="request-1",
            correlation_id="correlation-1",
        ),
        readable_artifacts=DEFAULT_BOOTSTRAP_ARTIFACTS,
    )

    assert session.state is ELOAIEntryState.READY
    assert session.execution_binding_ready is True


def test_governed_execution_without_binding_fails_closed():
    session = ELOAIEntryGate().establish(
        _request(
            ELOAIEntryMode.GOVERNED_EXECUTION,
            tenant_id="tenant-a",
            domain="engineering",
            principal_id="principal-a",
            authorization_scope="repo:write",
            request_id="request-1",
            correlation_id="correlation-1",
        ),
        readable_artifacts=DEFAULT_BOOTSTRAP_ARTIFACTS,
    )

    assert session.state is ELOAIEntryState.BLOCKED
    assert session.block is ELOAIEntryBlock.AUTHORIZATION_REQUIRED


def test_contract_conflict_blocks_even_with_valid_access():
    session = ELOAIEntryGate().establish(
        _request(),
        readable_artifacts=DEFAULT_BOOTSTRAP_ARTIFACTS,
        contract_conflict=True,
    )

    assert session.state is ELOAIEntryState.BLOCKED
    assert session.block is ELOAIEntryBlock.CONTRACT_CONFLICT
