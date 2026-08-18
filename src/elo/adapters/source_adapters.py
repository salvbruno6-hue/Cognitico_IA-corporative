"""Concrete authorized source adapters for the canonical SourceResolver.

Adapters are execution boundaries, not authorities. They receive a semantic
SourceCandidate plus the complete request context and delegate retrieval to an
injected capability. This keeps credentials, transport and provider SDKs out of
Core while making authorization and provenance testable.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Mapping

from elo.core.source_discovery import SourceCandidate
from elo.core.source_resolver import RetrievedSource, SourceResolutionRequest

RetrievalCallable = Callable[[SourceCandidate, SourceResolutionRequest], tuple[RetrievedSource, ...]]


@dataclass(frozen=True)
class AuthorizedSourceAdapter:
    """Reusable adapter boundary with explicit capability and authorization scope."""

    kind: str
    capability: str
    authorization_scope: str
    fetch: RetrievalCallable
    available_state: bool = True

    def available(self) -> bool:
        return self.available_state

    def retrieve(
        self,
        candidate: SourceCandidate,
        request: SourceResolutionRequest,
    ) -> tuple[RetrievedSource, ...]:
        if request.authorization_scope != self.authorization_scope:
            raise PermissionError(
                f"authorization scope {request.authorization_scope!r} is not valid "
                f"for source adapter {self.kind!r}"
            )
        retrieved = self.fetch(candidate, request)
        return tuple(
            _with_adapter_provenance(item, self.kind, self.capability)
            for item in retrieved
        )


class GitHubSourceAdapter(AuthorizedSourceAdapter):
    def __init__(self, fetch: RetrievalCallable, *, available_state: bool = True) -> None:
        super().__init__(
            kind="GITHUB",
            capability="source.github.read",
            authorization_scope="source:github:read",
            fetch=fetch,
            available_state=available_state,
        )


class ChatGPTProjectSourceAdapter(AuthorizedSourceAdapter):
    def __init__(self, fetch: RetrievalCallable, *, available_state: bool = True) -> None:
        super().__init__(
            kind="CHATGPT_PROJECTS",
            capability="source.chatgpt_projects.read",
            authorization_scope="source:chatgpt_projects:read",
            fetch=fetch,
            available_state=available_state,
        )


class DocumentSourceAdapter(AuthorizedSourceAdapter):
    def __init__(self, fetch: RetrievalCallable, *, available_state: bool = True) -> None:
        super().__init__(
            kind="DOCUMENTS",
            capability="source.documents.read",
            authorization_scope="source:documents:read",
            fetch=fetch,
            available_state=available_state,
        )


class WebSourceAdapter(AuthorizedSourceAdapter):
    def __init__(self, fetch: RetrievalCallable, *, available_state: bool = True) -> None:
        super().__init__(
            kind="WEB",
            capability="source.web.read",
            authorization_scope="source:web:read",
            fetch=fetch,
            available_state=available_state,
        )


class AIProviderSourceAdapter(AuthorizedSourceAdapter):
    def __init__(self, fetch: RetrievalCallable, *, available_state: bool = True) -> None:
        super().__init__(
            kind="AI_PROVIDER",
            capability="source.ai_provider.read",
            authorization_scope="source:ai_provider:read",
            fetch=fetch,
            available_state=available_state,
        )


def _with_adapter_provenance(
    item: RetrievedSource,
    kind: str,
    capability: str,
) -> RetrievedSource:
    provenance: Mapping[str, str] = {
        **dict(item.provenance),
        "adapter_kind": kind,
        "adapter_capability": capability,
        "authority": "external_source_evidence",
    }
    return RetrievedSource(
        source_id=item.source_id,
        source_type=item.source_type,
        content=item.content,
        provenance=provenance,
        metadata=item.metadata,
    )
