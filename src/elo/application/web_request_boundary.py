"""Provider-neutral governed boundary for ELO web/application requests."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


class WebRequestBoundaryError(ValueError):
    """Raised when an application request violates ELO boundary invariants."""


@dataclass(frozen=True)
class WebRequest:
    request_id: str
    tenant_id: str
    principal_id: str
    intent: str
    scope: str
    evidence_ids: tuple[str, ...]
    provenance: Mapping[str, str]


class GovernedWebRequestBoundary:
    """Validate browser/application input without granting authority or credentials."""

    _SECRET_KEYS = {"password", "token", "access_token", "refresh_token", "api_key", "service_role"}

    def accept(
        self,
        *,
        request_id: str,
        tenant_id: str,
        principal_id: str,
        intent: str,
        scope: str,
        evidence_ids: tuple[str, ...] | list[str],
        provenance: Mapping[str, str],
    ) -> WebRequest:
        values = (request_id, tenant_id, principal_id, intent, scope)
        if any(not str(value).strip() for value in values):
            raise WebRequestBoundaryError("request identity, tenant, principal, intent and scope are required")
        if any(key.lower() in self._SECRET_KEYS for key in provenance):
            raise WebRequestBoundaryError("secret-bearing request metadata is forbidden")
        return WebRequest(
            request_id=request_id.strip(),
            tenant_id=tenant_id.strip(),
            principal_id=principal_id.strip(),
            intent=intent.strip(),
            scope=scope.strip(),
            evidence_ids=tuple(evidence_ids),
            provenance=dict(provenance),
        )
