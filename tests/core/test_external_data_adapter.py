import pytest

from elo.integrations.enterprise.external_data import (
    AuthorizationDecision,
    ExternalDataRequest,
    ExternalDataSource,
    GovernedExternalDataAdapter,
)


class FakeExecutor:
    def __init__(self):
        self.requests = []

    def execute(self, request):
        self.requests.append(request)
        return {"rows": [{"id": 1}]}


def make_request(operation="query", scope="tenant-a"):
    return ExternalDataRequest(
        request_id="req-1",
        identity_id="identity-1",
        tenant_scope=scope,
        source=ExternalDataSource(
            source_id="source-1",
            source_key="erp-a",
            source_kind="ENTERPRISE_EXTERNAL",
            scope_key=scope,
            credential_ref="secret://erp-a",
        ),
        operation=operation,
        payload={"query": "customers"},
    )


def test_external_data_requires_explicit_authorization():
    executor = FakeExecutor()
    adapter = GovernedExternalDataAdapter(
        authorize=lambda request: AuthorizationDecision(False, "denied"),
        executor=executor,
    )

    with pytest.raises(PermissionError, match="denied"):
        adapter.execute(make_request())

    assert executor.requests == []


def test_external_data_is_tenant_scoped_and_fail_closed():
    executor = FakeExecutor()
    adapter = GovernedExternalDataAdapter(
        authorize=lambda request: AuthorizationDecision(True, "ok"),
        executor=executor,
    )

    with pytest.raises(PermissionError, match="outside tenant scope"):
        adapter.execute(make_request(scope="tenant-b"))

    assert executor.requests == []


def test_external_data_allows_query_when_authorized_and_returns_provenance():
    executor = FakeExecutor()
    adapter = GovernedExternalDataAdapter(
        authorize=lambda request: AuthorizationDecision(True, "ok"),
        executor=executor,
    )

    result = adapter.execute(make_request())

    assert result.data == {"rows": [{"id": 1}]}
    assert result.provenance["authority"] == "elo-governed-external-data"
    assert result.provenance["source_id"] == "source-1"
    assert result.provenance["request_id"] == "req-1"


def test_external_write_requires_explicit_operation_grant():
    executor = FakeExecutor()
    adapter = GovernedExternalDataAdapter(
        authorize=lambda request: AuthorizationDecision(
            True, "ok", frozenset({"metadata_read", "read", "query"})
        ),
        executor=executor,
    )

    with pytest.raises(PermissionError, match="not authorized"):
        adapter.execute(make_request(operation="write"))

    assert executor.requests == []


def test_external_write_can_be_enabled_only_by_authorization_decision():
    executor = FakeExecutor()
    adapter = GovernedExternalDataAdapter(
        authorize=lambda request: AuthorizationDecision(
            True, "ok", frozenset({"query", "write"})
        ),
        executor=executor,
    )

    result = adapter.execute(make_request(operation="write"))

    assert result.operation == "write"
    assert len(executor.requests) == 1


def test_source_requires_indirect_credential_reference():
    source = ExternalDataSource(
        source_id="source-1",
        source_key="erp-a",
        source_kind="ENTERPRISE_EXTERNAL",
        scope_key="tenant-a",
        credential_ref="",
    )
    request = ExternalDataRequest(
        request_id="req-1",
        identity_id="identity-1",
        tenant_scope="tenant-a",
        source=source,
        operation="query",
    )

    with pytest.raises(ValueError, match="credential_ref"):
        request.validate()


def test_canonical_elo_source_cannot_use_external_adapter():
    source = ExternalDataSource(
        source_id="source-1",
        source_key="elo",
        source_kind="ELO_CANONICAL",
        scope_key="tenant-a",
        credential_ref="internal",
    )
    request = ExternalDataRequest(
        request_id="req-1",
        identity_id="identity-1",
        tenant_scope="tenant-a",
        source=source,
        operation="query",
    )

    with pytest.raises(ValueError, match="external data source"):
        request.validate()
