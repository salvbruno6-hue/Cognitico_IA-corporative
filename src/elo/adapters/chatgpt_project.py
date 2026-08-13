"""Authorized ChatGPT Project source adapter contract.

This module deliberately does not invent access to private ChatGPT Projects.
It defines the capability boundary ELO needs: project discovery/search only
through an explicitly connected adapter, with authorization and provenance.
A concrete transport can implement the protocol when an official/authorized
connector exposes the required Project resources.
"""

from dataclasses import dataclass
from typing import Mapping, Protocol


@dataclass(frozen=True)
class ProjectSourceRef:
    project_id: str
    project_name: str
    source_id: str
    source_type: str
    title: str
    provenance: Mapping[str, str]


@dataclass(frozen=True)
class ProjectSearchRequest:
    query: str
    project_id: str | None = None
    tenant_id: str = ""
    principal: str = ""
    authorization_scope: str = "chatgpt_project.read"


class ChatGPTProjectAccess(Protocol):
    """Capability required to read authorized ChatGPT Project sources."""

    def search(self, request: ProjectSearchRequest) -> tuple[ProjectSourceRef, ...]:
        ...


class ChatGPTProjectAdapter:
    """Guarded facade; no credentials or private-project access are embedded."""

    def __init__(self, access: ChatGPTProjectAccess | None = None) -> None:
        self._access = access

    @property
    def available(self) -> bool:
        return self._access is not None

    def search(self, request: ProjectSearchRequest) -> tuple[ProjectSourceRef, ...]:
        if not request.query.strip():
            raise ValueError("query is required")
        if not request.tenant_id or not request.principal:
            raise PermissionError("tenant_id and principal are required")
        if request.authorization_scope != "chatgpt_project.read":
            raise PermissionError("unsupported ChatGPT Project authorization scope")
        if self._access is None:
            raise RuntimeError(
                "ChatGPT Project connector is not connected; ELO must report the access gap"
            )
        return self._access.search(request)
