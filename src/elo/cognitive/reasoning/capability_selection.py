"""Evidence-aware capability selection for ELO reasoning.

The registry discovers available capabilities; this module decides which one
best fits a task step. Provider names remain replaceable implementation details.
"""
from dataclasses import dataclass
from typing import Mapping

from elo.core.capability_registry import CapabilityRegistry, CapabilityStatus


@dataclass(frozen=True)
class CapabilityRequirement:
    capability: str
    preferred_kinds: tuple[str, ...] = ()
    required_metadata: Mapping[str, str] = None  # type: ignore[assignment]
    min_score: float = 0.0

    def __post_init__(self) -> None:
        if not self.capability:
            raise ValueError("capability is required")
        if not 0.0 <= self.min_score <= 1.0:
            raise ValueError("min_score must be between 0 and 1")
        if self.required_metadata is None:
            object.__setattr__(self, "required_metadata", {})


@dataclass(frozen=True)
class CapabilityDecision:
    status: str
    capability_name: str | None
    capability_kind: str | None
    score: float
    rationale: str


class CapabilitySelector:
    """Select an available registered capability without inventing providers."""

    def __init__(self, registry: CapabilityRegistry) -> None:
        self._registry = registry

    def select(self, requirement: CapabilityRequirement) -> CapabilityDecision:
        candidates = [item for item in self._registry.snapshot() if item.status == CapabilityStatus.AVAILABLE]
        scored: list[tuple[float, object]] = []
        for item in candidates:
            declared = set(filter(None, item.metadata.get("capabilities", "").split(",")))
            if requirement.capability not in declared and item.name != requirement.capability:
                continue
            metadata_score = sum(
                item.metadata.get(key) == value for key, value in requirement.required_metadata.items()
            ) / max(1, len(requirement.required_metadata))
            kind_score = 1.0 if item.kind in requirement.preferred_kinds else 0.0
            score = (0.7 * metadata_score) + (0.3 * kind_score if requirement.preferred_kinds else 0.0)
            scored.append((score, item))
        if not scored:
            return CapabilityDecision("NO_MATCH", None, None, 0.0, "no available capability satisfies requirement")
        score, item = max(scored, key=lambda pair: (pair[0], pair[1].name))
        if score < requirement.min_score:
            return CapabilityDecision("INSUFFICIENT", None, None, score, "best capability is below required score")
        return CapabilityDecision("SELECTED", item.name, item.kind, score, "best evidenced available capability")
