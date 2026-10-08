"""Runtime composition for governed external data access.

This module connects the canonical source metadata and authorization decision
to an injected credential resolver and transport. It intentionally does not
store secrets, invent credentials, or become a second authorization authority.
A runtime is executable only when all three boundaries are supplied:
ELO authorization, credential resolution, and an external transport.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

from elo.integrations.enterprise.external_data import (
    AuthorizationDecision,
    ExternalDataRequest,
    ExternalDataResult,
    GovernedExternalDataAdapter,
)


class CredentialResolver(Protocol):
    def resolve(self, credential_ref: str) -> Any:
        """Resolve a reference into a runtime-only credential."""


class ExternalTransport(Protocol):
    def execute(self, request: ExternalDataRequest, credential: Any) -> Any:
        """Execute against the external source using a runtime credential."""


@dataclass(frozen=True)
class RuntimeCredentialExecutor:
    credential_resolver: CredentialResolver
    transport: ExternalTransport

    def execute(self, request: ExternalDataRequest) -> Any:
        credential = self.credential_resolver.resolve(request.source.credential_ref)
        if credential is None:
            raise PermissionError("external credential could not be resolved")
        return self.transport.execute(request, credential)


@dataclass(frozen=True)
class GovernedExternalDataRuntime:
    """Executable ELO boundary: authorize first, then resolve and transport."""

    authorize: Any
    credential_resolver: CredentialResolver
    transport: ExternalTransport

    def execute(self, request: ExternalDataRequest) -> ExternalDataResult:
        executor = RuntimeCredentialExecutor(
            credential_resolver=self.credential_resolver,
            transport=self.transport,
        )
        adapter = GovernedExternalDataAdapter(
            authorize=self.authorize,
            executor=executor,
        )
        return adapter.execute(request)
