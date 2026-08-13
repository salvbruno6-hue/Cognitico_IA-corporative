"""Uncertainty primitives for evidence-aware ELO decisions."""

from dataclasses import dataclass


@dataclass(frozen=True)
class UncertaintyAssessment:
    level: str
    confidence: float
    evidence_count: int = 0
    reason: str = ""

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")
        if self.evidence_count < 0:
            raise ValueError("evidence_count cannot be negative")


HIGH_IMPACT_LEVELS = frozenset({"STRATEGIC", "CRITICAL"})
