"""Authorized source resolver runtime for the canonical ELO source-discovery flow.

SourceDiscovery decides *where* information should be sought. This module
owns the governed handoff from that semantic plan to an authorized adapter and
places retrieved material into Temporal Conversation Memory before any
promotion/admission decision.

Adapters are injected capabilities. This module never assumes credentials,
provider availability or canonical truth from a retrieval result.
"""

from dataclasses import dataclass, field
from typing import Mapping, Protocol

from .source_discovery import SourceCandidate
from .temporal_memory import TemporalConversationMemory, TemporalRecord


@dataclass(frozen=True)
class SourceResolutionRequest:
    query: str
    tenant_id: str
    domain: str
    principal_id: str
    session_id: str
    request_id: str
    correlation_id: str
    conversation_id: str
    authorization_scope: str
    metadata: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class RetrievedSource:
    source_id: str
    source_type: str
    content: str
    provenance: Mapping[str, str]
    metadata: Mapping[str, str] = field(default_factory=dict)


class SourceResolverAdapter(Protocol):
    kind: str
    capability: str

    def available(self) -> bool:
        ...

    def retrieve(
        self,
        candidate: SourceCandidate,
        request: SourceResolutionRequest,
    ) -> tuple[RetrievedSource, ...]:
        ...


@dataclass(frozen=True)
class SourceResolutionResult:
    candidate: SourceCandidate
    retrieved: tuple[RetrievedSource, ...] = ()
    temporal_records: tuple[TemporalRecord, ...] = ()
    status: str = "NO_ACCESS"
    gap: str | None = None


class SourceResolver:
    """Resolve one semantic source candidate through an authorized adapter."""

    def __init__(
        self,
        adapters: tuple[SourceResolverAdapter, ...] = (),
        temporal_memory: TemporalConversationMemory | None = None,
    ) -> None:
        self._adapters = {adapter.kind: adapter for adapter in adapters}
        self._temporal = temporal_memory or TemporalConversationMemory()

    def resolve(
        self,
        candidate: SourceCandidate,
        request: SourceResolutionRequest,
    ) -> SourceResolutionResult:
        self._validate_request(request)
        adapter = self._adapters.get(candidate.kind)
        if adapter is None:
            return SourceResolutionResult(
                candidate=candidate,
                status="UNAVAILABLE",
                gap=f"no adapter registered for source kind {candidate.kind}",
            )
        if adapter.capability != candidate.required_capability:
            return SourceResolutionResult(
                candidate=candidate,
                status="UNAUTHORIZED",
                gap="adapter capability does not satisfy the discovery requirement",
            )

        declared_scope = getattr(adapter, "authorization_scope", None)
        governed_scope: str | None = None
        if declared_scope is not None:
            declared_scope_text = str(declared_scope).strip()
            if not declared_scope_text or request.authorization_scope != declared_scope_text:
                return SourceResolutionResult(
                    candidate=candidate,
                    status="UNAUTHORIZED",
                    gap="authorization scope does not satisfy the adapter contract",
                )
            governed_scope = declared_scope_text

        if not adapter.available():
            return SourceResolutionResult(
                candidate=candidate,
                status="UNAVAILABLE",
                gap=f"source adapter {candidate.kind} is unavailable",
            )

        retrieved = adapter.retrieve(candidate, request)
        if not retrieved:
            return SourceResolutionResult(
                candidate=candidate,
                status="NO_RESULT",
                gap="authorized source returned no material",
            )

        records: list[TemporalRecord] = []
        for item in retrieved:
            provenance = dict(item.provenance)
            resolver_provenance = {
                # Resolver-owned request context overrides adapter assertions.
                "tenant_id": request.tenant_id,
                "domain": request.domain,
                "principal_id": request.principal_id,
                "session_id": request.session_id,
                "request_id": request.request_id,
                "correlation_id": request.correlation_id,
                "source_id": item.source_id,
                # These values come from the capability contract validated
                # immediately above, never from adapter-provided provenance.
                "source_kind": candidate.kind,
                "required_capability": candidate.required_capability,
            }
            # Authorization scope becomes governed provenance only when the
            # selected adapter explicitly declares the same scope. Legacy/custom
            # adapters without a declared scope may still resolve evidence, but
            # the resolver will not represent their request scope as validated.
            if governed_scope is not None:
                resolver_provenance["authorization_scope"] = governed_scope
            provenance.update(resolver_provenance)
            records.append(
                self._temporal.append(
                    conversation_id=request.conversation_id,
                    record_id=item.source_id,
                    source_type=item.source_type,
                    content=item.content,
                    provenance=provenance,
                    metadata=item.metadata,
                )
            )

        return SourceResolutionResult(
            candidate=candidate,
            retrieved=retrieved,
            temporal_records=tuple(records),
            status="RETRIEVED_TO_TEMPORAL",
        )

    @staticmethod
    def _validate_request(request: SourceResolutionRequest) -> None:
        required = {
            "query": request.query,
            "tenant_id": request.tenant_id,
            "domain": request.domain,
            "principal_id": request.principal_id,
            "session_id": request.session_id,
            "request_id": request.request_id,
            "correlation_id": request.correlation_id,
            "conversation_id": request.conversation_id,
            "authorization_scope": request.authorization_scope,
        }
        missing = tuple(
            name for name, value in required.items()
            if value is None or not str(value).strip()
        )
        if missing:
            raise ValueError(f"source resolution request missing: {', '.join(missing)}")
