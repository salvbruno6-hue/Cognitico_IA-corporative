"""Enterprise methodology discovery primitives for the ELO cognitive layer.

The tenant's observed method is authoritative for tenant execution. External
patterns and learned improvements remain separate until explicitly governed.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class MethodEvidence(str, Enum):
    OBSERVED = "observed"
    LEARNED = "learned"
    PROPOSED = "proposed"
    EXTERNAL = "external"


@dataclass(frozen=True)
class MethodObservation:
    """A traceable observation of how a tenant actually performs work."""

    domain: str
    process: str
    attribute: str
    value: Any
    evidence: MethodEvidence
    source: str
    tenant_id: str | None = None
    confidence: float = 1.0
    frequency: int = 1
    context: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> None:
        if not self.domain or not self.process or not self.attribute:
            raise ValueError("domain, process and attribute are required")
        if not self.source:
            raise ValueError("source is required for provenance")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")
        if self.frequency < 1:
            raise ValueError("frequency must be at least 1")
        if self.evidence is MethodEvidence.OBSERVED and not self.tenant_id:
            raise ValueError("observed tenant methodology requires tenant_id")

    @property
    def is_private(self) -> bool:
        return self.tenant_id is not None

    def generalization_candidate(self) -> bool:
        """A tenant observation never becomes portable merely by repetition."""
        return (
            self.evidence in {MethodEvidence.LEARNED, MethodEvidence.PROPOSED, MethodEvidence.EXTERNAL}
            and not self.is_private
        )


@dataclass(frozen=True)
class MethodModel:
    """Versioned representation of an organization's working method."""

    domain: str
    version: str
    observations: tuple[MethodObservation, ...]
    tenant_id: str | None = None

    def validate(self) -> None:
        if not self.domain or not self.version:
            raise ValueError("domain and version are required")
        for observation in self.observations:
            observation.validate()
            if self.tenant_id and observation.tenant_id not in {None, self.tenant_id}:
                raise ValueError("method observation belongs to another tenant")

    def attributes(self) -> dict[str, Any]:
        """Return the latest observed value for each methodology attribute."""
        result: dict[str, Any] = {}
        for observation in self.observations:
            if observation.tenant_id in {None, self.tenant_id}:
                result[observation.attribute] = observation.value
        return result


def discover_method(observations: list[MethodObservation], *, tenant_id: str) -> MethodModel:
    """Build a tenant-scoped method model from evidenced observations."""
    if not tenant_id:
        raise ValueError("tenant_id is required")
    selected = tuple(item for item in observations if item.tenant_id == tenant_id)
    model = MethodModel(domain=selected[0].domain if selected else "unknown", version="0.1", observations=selected, tenant_id=tenant_id)
    model.validate()
    return model
