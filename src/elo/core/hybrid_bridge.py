"""Provider-neutral hybrid capability bridge and evidence-based maturity.

Remote and local providers are interchangeable capabilities. The bridge selects
only healthy registered capabilities and returns explicit degradation when none
are available. It never becomes a provider authority or a second Core.
"""
from dataclasses import dataclass
from typing import Mapping

from .capability_registry import CapabilityRegistry, CapabilityStatus
from .maturity_engine import MaturityAssessment, MATURITY_DIMENSIONS


@dataclass(frozen=True)
class ProviderSelection:
    status: str
    capability_name: str | None
    capability_kind: str | None
    reason: str


class HybridCapabilityBridge:
    def __init__(self, registry: CapabilityRegistry) -> None:
        self._registry = registry

    def select(self, *, preferred_kinds: tuple[str, ...] = ()) -> ProviderSelection:
        snapshots = self._registry.snapshot()
        ordered = [item for kind in preferred_kinds for item in snapshots if item.kind == kind]
        ordered.extend(item for item in snapshots if item not in ordered)
        for item in ordered:
            if item.status == CapabilityStatus.AVAILABLE:
                return ProviderSelection("AVAILABLE", item.name, item.kind, "healthy capability selected")
        if snapshots:
            return ProviderSelection("DEGRADED", None, None, "registered capabilities are unavailable")
        return ProviderSelection("NO_CAPABILITY", None, None, "no provider capability registered")

    @staticmethod
    def assess_maturity(evidence: Mapping[str, float], *, threshold: float = 0.75) -> MaturityAssessment:
        scores = {dimension: float(evidence.get(dimension, 0.0)) for dimension in MATURITY_DIMENSIONS}
        return MaturityAssessment(scores=scores, minimum_threshold=threshold)
