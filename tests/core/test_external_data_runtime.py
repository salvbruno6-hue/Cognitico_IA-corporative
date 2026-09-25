import pytest

from elo.integrations.enterprise.external_data import (
    AuthorizationDecision,
    ExternalDataRequest,
    ExternalDataSource,
)
from elo.integrations.enterprise.external_data_runtime import GovernedExternalDataRuntime


def make_request():
    return ExternalDataRequest(
        request_id="req-runtime-1",
        identity_id="identity-1",
        tenant_scope="tenant-a",
        source=ExternalDataSource(
            source_id="source-1",
            source_key="erp-a",
            source_kind="ENTERPRISE_EXTERNAL",
            scope_key="tenant-a",
            credential_ref="secret://erp-a",
        ),
        operation="query",
        payload={"query": "customers"},
    )


class FakeCredentialResolver:
    def __init__(self, credential="runtime-secret"):
        self.credential = credential
        self.refs = []

    def resolve(self, credential_ref):
        self.refs.append(credential_ref)
        return self.credential


class FakeTransport:
    def __init__(self):
        self.calls = []

    def execute(self, request, credential):
        self.calls.append((request, credential))
        return {"rows": [{"id": 7}]}


def test_runtime_authorizes_before_resolving_credentials():
    resolver = FakeCredentialResolver()
    transport = FakeTransport()
    runtime = GovernedExternalDataRuntime(
        authorize=lambda request: AuthorizationDecision(False, "denied"),
        credential_resolver=resolver,
        transport=transport,
    )

    with pytest.raises(PermissionError, match="denied"):
        runtime.execute(make_request())

    assert resolver.refs == []
    assert transport.calls == []


def test_runtime_resolves_credential_only_after_authorization():
    resolver = FakeCredentialResolver()
    transport = FakeTransport()
    runtime = GovernedExternalDataRuntime(
        authorize=lambda request: AuthorizationDecision(True, "ok"),
        credential_resolver=resolver,
        transport=transport,
    )

    result = runtime.execute(make_request())

    assert resolver.refs == ["secret://erp-a"]
    assert transport.calls[0][1] == "runtime-secret"
    assert result.data == {"rows": [{"id": 7}]}
    assert "runtime-secret" not in result.provenance.values()


def test_runtime_fails_closed_when_credential_is_unavailable():
    resolver = FakeCredentialResolver(credential=None)
    transport = FakeTransport()
    runtime = GovernedExternalDataRuntime(
        authorize=lambda request: AuthorizationDecision(True, "ok"),
        credential_resolver=resolver,
        transport=transport,
    )

    with pytest.raises(PermissionError, match="credential could not be resolved"):
        runtime.execute(make_request())

    assert transport.calls == []


def test_runtime_provenance_keeps_external_source_boundary():
    resolver = FakeCredentialResolver()
    transport = FakeTransport()
    runtime = GovernedExternalDataRuntime(
        authorize=lambda request: AuthorizationDecision(True, "ok"),
        credential_resolver=resolver,
        transport=transport,
    )

    result = runtime.execute(make_request())

    assert result.provenance["authority"] == "elo-governed-external-data"
    assert result.provenance["source_kind"] == "ENTERPRISE_EXTERNAL"
    assert result.provenance["scope_key"] == "tenant-a"
