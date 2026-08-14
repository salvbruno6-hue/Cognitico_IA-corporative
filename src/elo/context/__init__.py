"""Governed context resolution for ELO-002."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from elo.interface.contracts import CognitiveRequest


class ContextConflictError(ValueError):
    """Raised when explicit and trusted context disagree."""


@dataclass(frozen=True, slots=True)
class CognitiveContext:
    tenant_id: str
    domain: str | None
    principal_id: str | None
    user_id: str | None
    session_id: str
    request_id: str
    correlation_id: str
    values: dict[str, Any] = field(default_factory=dict)


class ContextResolver:
    """Builds a canonical context without replacing the request contract."""

    def resolve(
        self,
        request: CognitiveRequest | Mapping[str, Any],
        *,
        session: Any | None = None,
    ) -> CognitiveContext:
        if isinstance(request, Mapping):
            request = CognitiveRequest.model_validate(request)

        tenant_id = request.tenant_id
        domain = request.domain
        principal_id = request.principal_id
        user_id = request.user_id
        session_id = request.session_id

        if session is not None:
            if session.tenant_id != tenant_id:
                raise ContextConflictError("session tenant conflicts with request tenant")
            if session.principal_id and principal_id and session.principal_id != principal_id:
                raise ContextConflictError("session principal conflicts with request principal")
            if session.domain and domain and session.domain != domain:
                raise ContextConflictError("session domain conflicts with request domain")
            session_id = session.id
            domain = domain or session.domain
            principal_id = principal_id or session.principal_id
            user_id = user_id or session.user_id

        if not session_id:
            raise ValueError("session_id is required after session resolution")

        values = dict(request.context)
        values.setdefault("tenant_id", tenant_id)
        if domain is not None:
            values.setdefault("domain", domain)
        if principal_id is not None:
            values.setdefault("principal_id", principal_id)

        return CognitiveContext(
            tenant_id=tenant_id,
            domain=domain,
            principal_id=principal_id,
            user_id=user_id,
            session_id=session_id,
            request_id=request.request_id,
            correlation_id=request.correlation_id or request.request_id,
            values=values,
        )


__all__ = ["CognitiveContext", "ContextConflictError", "ContextResolver"]
