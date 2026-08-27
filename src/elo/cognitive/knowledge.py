"""Knowledge-boundary primitives for the ELO cognitive layer."""

from dataclasses import dataclass
from enum import Enum
from typing import Any


class KnowledgeScope(str, Enum):
    CANONICAL = "canonical"
    TENANT = "tenant"
    LEARNED = "learned"
    PROPOSED = "proposed"
    EXTERNAL = "external"


@dataclass(frozen=True)
class KnowledgeRecord:
    """Evidence-bearing knowledge with explicit scope and provenance."""

    key: str
    value: Any
    scope: KnowledgeScope
    tenant_id: str | None = None
    source: str | None = None
    confidence: float | None = None

    def is_portable(self) -> bool:
        """Return whether the record can safely travel with the ELO essence."""
        return self.scope is KnowledgeScope.CANONICAL and self.tenant_id is None

    def can_promote_to_canonical(self) -> bool:
        """Only non-private, governed candidates may enter canonical review."""
        return (
            self.scope in {KnowledgeScope.LEARNED, KnowledgeScope.PROPOSED, KnowledgeScope.EXTERNAL}
            and self.tenant_id is None
        )

    def validate(self) -> None:
        if self.scope is KnowledgeScope.TENANT and not self.tenant_id:
            raise ValueError("tenant knowledge requires tenant_id")
        if self.scope is KnowledgeScope.CANONICAL and self.tenant_id is not None:
            raise ValueError("canonical knowledge cannot be tenant-scoped")
        if self.confidence is not None and not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")
