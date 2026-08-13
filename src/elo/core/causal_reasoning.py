"""Causal assessment primitives for governed ELO reasoning."""

from dataclasses import dataclass


@dataclass(frozen=True)
class CausalAssessment:
    cause_id: str
    effect_id: str
    relation: str
    confidence: float
    evidence_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")

    @property
    def is_confirmed(self) -> bool:
        return self.relation == "CONFIRMED_CAUSE"
