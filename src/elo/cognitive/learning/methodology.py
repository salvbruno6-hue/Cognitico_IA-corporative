"""Tenant methodology discovery and evidence boundaries.

This module learns how a tenant actually works without promoting tenant data
into ELO Canon. It deliberately keeps discovery, evidence, and proposals
separate from governed promotion.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class EvidenceKind(str, Enum):
    OBSERVED = "observed"
    DECLARED = "declared"
    LEARNED = "learned"
    PROPOSED = "proposed"
    EXTERNAL = "external"


@dataclass(frozen=True)
class MethodEvidence:
    domain: str
    process: str
    attribute: str
    value: Any
    kind: EvidenceKind
    source: str
    tenant_id: str | None = None
    confidence: float = 1.0
    occurrences: int = 1
    context: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> None:
        if not all((self.domain, self.process, self.attribute, self.source)):
            raise ValueError("domain, process, attribute and source are required")
        if not 0 <= self.confidence <= 1:
            raise ValueError("confidence must be between 0 and 1")
        if self.occurrences < 1:
            raise ValueError("occurrences must be positive")
        if self.kind in {EvidenceKind.OBSERVED, EvidenceKind.DECLARED} and not self.tenant_id:
            raise ValueError("tenant evidence requires tenant_id")


@dataclass(frozen=True)
class TenantMethod:
    tenant_id: str
    version: str
    evidence: tuple[MethodEvidence, ...]

    def validate(self) -> None:
        if not self.tenant_id or not self.version:
            raise ValueError("tenant_id and version are required")
        for item in self.evidence:
            item.validate()
            if item.tenant_id not in {self.tenant_id, None}:
                raise ValueError("cross-tenant evidence is not allowed")

    def resolve(self, attribute: str) -> Any:
        """Resolve the most recent tenant-scoped evidence for an attribute."""
        candidates = [
            item for item in self.evidence
            if item.attribute == attribute and item.tenant_id in {self.tenant_id, None}
        ]
        if not candidates:
            raise KeyError(attribute)
        return candidates[-1].value


def discover_tenant_method(evidence: list[MethodEvidence], tenant_id: str) -> TenantMethod:
    """Create a tenant method only from evidence belonging to that tenant."""
    if not tenant_id:
        raise ValueError("tenant_id is required")
    selected = tuple(item for item in evidence if item.tenant_id == tenant_id)
    method = TenantMethod(tenant_id=tenant_id, version="0.1", evidence=selected)
    method.validate()
    return method


def can_generalize(item: MethodEvidence) -> bool:
    """Tenant-scoped evidence never becomes portable by repetition alone."""
    return item.tenant_id is None and item.kind in {
        EvidenceKind.LEARNED,
        EvidenceKind.PROPOSED,
        EvidenceKind.EXTERNAL,
    }
