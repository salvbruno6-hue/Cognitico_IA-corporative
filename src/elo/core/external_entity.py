"""Canonical contracts for identifying and consulting external entities.

An external entity is something such as a company, customer, supplier, product,
or organization that may not yet exist in ELO knowledge. Resolution is
provider-neutral and never makes external information canonical by itself.
"""

from dataclasses import dataclass
from typing import Literal, Mapping

EntityKind = Literal["COMPANY", "PERSON", "PRODUCT", "ORGANIZATION", "PLACE", "OTHER"]


@dataclass(frozen=True)
class ExternalEntityRequest:
    """A consultant request involving an external entity."""

    query: str
    entity_name: str
    entity_kind: EntityKind = "OTHER"
    tenant_id: str = ""
    domain: str = ""
    principal: str = ""
    session_id: str = ""
    request_id: str = ""
    correlation_id: str = ""
    external_consultation_authorized: bool = False


@dataclass(frozen=True)
class EntityResolution:
    """Resolved identity and confidence before external consultation."""

    canonical_name: str
    entity_kind: EntityKind
    identifiers: Mapping[str, str]
    confidence: float
    internal_match: bool
    internal_evidence_count: int


@dataclass(frozen=True)
class EntityKnowledgeResult:
    """Provider-neutral result returned to the ELO consultant."""

    entity: EntityResolution
    facts: tuple[str, ...] = ()
    evidence: tuple[str, ...] = ()
    assumptions: tuple[str, ...] = ()
    contradictions: tuple[str, ...] = ()
    provider: str | None = None
    provider_request_id: str | None = None
    provenance: Mapping[str, str] = None  # type: ignore[assignment]
    external: bool = True

    def __post_init__(self) -> None:
        if self.provenance is None:
            object.__setattr__(self, "provenance", {})
