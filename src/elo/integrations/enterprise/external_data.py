"""Governed boundary for external enterprise/user data sources.

The adapter is an execution boundary, not an authorization authority. Identity,
tenant/scope resolution and capability decisions remain owned by ELO authz.
Credentials are referenced indirectly; this module never stores or accepts raw
secrets. Concrete transports are injected so Core remains independent of DB/API
drivers.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Mapping, Protocol


ALLOWED_OPERATIONS = frozenset(
    {"metadata_read", "read", "query", "write", "schema_change"}
)
DEFAULT_READ_OPERATIONS = frozenset({"metadata_read", "read", "query"})
EXTERNAL_SOURCE_KINDS = frozenset(
    {"ENTERPRISE_EXTERNAL", "USER_EXTERNAL", "INTEGRATION"}
)


@dataclass(frozen=True)
class ExternalDataSource:
    source_id: str
    source_key: str
    source_kind: str
    scope_key: str
    credential_ref: str
    connection_ref: str | None = None
    status: str = "ACTIVE"
    metadata: Mapping[str, Any] | None = None

    def validate(self) -> None:
        if not self.source_id or not self.source_key:
            raise ValueError("source identity is required")
        if self.source_kind not in EXTERNAL_SOURCE_KINDS:
            raise ValueError("source kind is not an external data source")
        if not self.scope_key:
            raise ValueError("scope_key is required")
        if not self.credential_ref:
            raise ValueError("credential_ref is required")
        if self.status != "ACTIVE":
            raise PermissionError("data source is not active")


@dataclass(frozen=True)
class ExternalDataRequest:
    request_id: str
    identity_id: str
    tenant_scope: str
    source: ExternalDataSource
    operation: str
    payload: Mapping[str, Any] | None = None

    def validate(self) -> None:
        if not self.request_id or not self.identity_id:
            raise ValueError("request_id and identity_id are required")
        if not self.tenant_scope:
            raise ValueError("tenant_scope is required")
        if self.operation not in ALLOWED_OPERATIONS:
            raise ValueError("unsupported external data operation")
        self.source.validate()


@dataclass(frozen=True)
class AuthorizationDecision:
    allowed: bool
    reason: str
    allowed_operations: frozenset[str] = DEFAULT_READ_OPERATIONS


@dataclass(frozen=True)
class ExternalDataResult:
    request_id: str
    source_id: str
    operation: str
    data: Any
    provenance: Mapping[str, str]


class ExternalDataExecutor(Protocol):
    def execute(self, request: ExternalDataRequest) -> Any:
        ...


AuthorizeCallable = Callable[[ExternalDataRequest], AuthorizationDecision]


@dataclass(frozen=True)
class GovernedExternalDataAdapter:
    """External data execution facade with fail-closed governance."""

    authorize: AuthorizeCallable
    executor: ExternalDataExecutor

    def execute(self, request: ExternalDataRequest) -> ExternalDataResult:
        request.validate()

        if request.source.scope_key != request.tenant_scope:
            raise PermissionError("data source is outside tenant scope")

        decision = self.authorize(request)
        if not decision.allowed:
            raise PermissionError(decision.reason or "external data access denied")

        if request.operation not in decision.allowed_operations:
            raise PermissionError(
                f"operation {request.operation!r} is not authorized for this source"
            )

        data = self.executor.execute(request)
        provenance = {
            "authority": "elo-governed-external-data",
            "request_id": request.request_id,
            "identity_id": request.identity_id,
            "source_id": request.source.source_id,
            "source_key": request.source.source_key,
            "source_kind": request.source.source_kind,
            "scope_key": request.source.scope_key,
            "operation": request.operation,
        }
        return ExternalDataResult(
            request_id=request.request_id,
            source_id=request.source.source_id,
            operation=request.operation,
            data=data,
            provenance=provenance,
        )
