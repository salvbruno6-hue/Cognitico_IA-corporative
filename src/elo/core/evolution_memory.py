"""Canonical ELO evolution-memory boundary.

Evolution memory preserves authorized experience without making it canonical
knowledge or changing the ELO's identity/architecture automatically.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Literal, Mapping, Optional

EvolutionStatus = Literal[
    "OBSERVATION",
    "EVIDENCE",
    "HYPOTHESIS",
    "REJECTED",
    "UNRESOLVED",
    "ARCHIVED",
    "PROMOTED",
]


@dataclass(frozen=True)
class EvolutionRecord:
    """A retained, non-canonical learning/experience record."""

    evolution_id: str
    tenant_id: str
    domain: str
    source_type: str
    source_id: str
    content: str
    status: EvolutionStatus = "OBSERVATION"
    confidence: Optional[float] = None
    tags: tuple[str, ...] = ()
    provenance: Mapping[str, str] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class EvolutionMemory:
    """Minimal storage boundary for authorized evolution records.

    This implementation is intentionally deterministic and in-memory. A
    production adapter may be added later behind this contract.
    """

    def __init__(self) -> None:
        self._records: dict[str, EvolutionRecord] = {}

    def store(self, record: EvolutionRecord) -> EvolutionRecord:
        if not record.tenant_id:
            raise ValueError("tenant_id is required")
        if not record.domain:
            raise ValueError("domain is required")
        if not record.provenance:
            raise ValueError("provenance is required")
        self._records[record.evolution_id] = record
        return record

    def get(self, evolution_id: str) -> Optional[EvolutionRecord]:
        return self._records.get(evolution_id)

    def list(self, tenant_id: str, domain: str) -> list[EvolutionRecord]:
        return [
            record
            for record in self._records.values()
            if record.tenant_id == tenant_id and record.domain == domain
        ]
